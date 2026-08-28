"""iter-8 acceptance — the deterministic brief assembler (`docs/BRIEF_SPEC.md`
owns the contract; `docs/blueprint/phases.md` §1 owns the donor design).

The assembler is a pure function of the log (the D-042/D-043/D-044
read-side family): no RNG, no wall-clock, construction order or explicit
sorts only — the byte-identity tests are the point (BRIEF_SPEC §2).
Budgets + eviction are unit-tested incl. the `[truncated:N]` marker and
the never-drop-directives law (§5); the pack lint for the brief section
is exercised through the same broken-pack pattern as the core lint
suite (`tests/test_core.py`).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from brief import (
    assemble_brief,
    beats_crossed,
    brief_from_log,
    last_beat_tick,
    render_brief,
    token_count,
)
from core.log import EventRecord, LoggedKnowledgeRecord
from core.pack import BRIEF_BLOCK_IDS, Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
PLAYER = PACK.player_id()


def _ev(
    eid: str, t: int, etype: str, actor: str, cause: str | None,
    *, target: str | None = None,
    knowledge: tuple[LoggedKnowledgeRecord, ...] = (),
    importance: str = "low",
) -> EventRecord:
    return EventRecord(
        id=eid, t=t, type=etype, actor=actor, cause=cause,
        outcome={}, knowledge=knowledge, state_changes=(), hooks=(),
        importance=importance, provenance={"seed": 42}, target=target,
    )


def _rec(who: str, knows: str, at: int, source: str) -> LoggedKnowledgeRecord:
    return LoggedKnowledgeRecord(
        who=who, channel="saw", fidelity="exact", knows=knows, at=at,
        source=source,
    )


def _mutated_pack(mutate: Callable[[dict[str, Any]], None]) -> Pack:
    """A deep-copied pack with mutated rules (budget/eviction tests)."""
    data = json.loads(json.dumps(dict(PACK.data)))
    mutate(data["rules.json"])
    return Pack(data=data)


def _broken_pack(tmp_path: Path, mutate: Callable[[Path], None]) -> Path:
    target = tmp_path / "broken_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    mutate(target)
    return target


def _blocks(text: str) -> dict[str, list[str]]:
    """Parse a rendered brief into block bodies (no headers, no markers)."""
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            blocks[current] = []
        elif line.strip():
            assert current is not None
            if not line.startswith("[truncated:"):
                blocks[current].append(line)
    return blocks


# -- purity: same log -> same brief bytes (the AC) ----------------------------


def test_golden_fixture_brief_byte_identical_across_calls() -> None:
    first = brief_from_log(GOLDEN, PACK, SCHEMA)
    second = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert first == second


def test_assemble_is_a_pure_function_of_the_log() -> None:
    """Two independently-read event lists render to identical bytes —
    no call-order state, no RNG, no wall-clock (BRIEF_SPEC §2)."""
    from core.log import read_log

    _header, events_a = read_log(GOLDEN, SCHEMA)
    _header, events_b = read_log(GOLDEN, SCHEMA)
    assert render_brief(assemble_brief(events_a, PACK)) == render_brief(
        assemble_brief(events_b, PACK)
    )
    # assemble+render compose to exactly brief_from_log's bytes
    assert render_brief(assemble_brief(events_a, PACK)) == brief_from_log(
        GOLDEN, PACK, SCHEMA
    )


def test_brief_block_headers_in_pipeline_order() -> None:
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    headers = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert tuple(headers) == BRIEF_BLOCK_IDS


def test_brief_format_blank_line_separation_and_trailing_newline() -> None:
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert text.endswith("\n")
    assert "\n\n## " in text  # blocks separated by exactly one blank line
    assert not text.startswith("\n")


def test_empty_block_renders_header_alone() -> None:
    """The golden fixture's PC holds no knowledge records — recalled_facts
    is an explicit empty header, never an omission (BRIEF_SPEC §7)."""
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert "## recalled_facts\n\n" in text


def test_empty_event_list_renders_all_headers() -> None:
    text = render_brief(assemble_brief((), PACK))
    assert text.count("## ") == len(BRIEF_BLOCK_IDS)


# -- scene delta (BRIEF_SPEC §3.2) ---------------------------------------------


def test_scene_delta_newest_first() -> None:
    body = _blocks(brief_from_log(GOLDEN, PACK, SCHEMA))["scene_delta"]
    ticks = [int(line.split("]")[0][3:]) for line in body]
    assert ticks == sorted(ticks, reverse=True)


def test_scene_delta_whole_log_when_no_beat_crossed() -> None:
    body = _blocks(brief_from_log(GOLDEN, PACK, SCHEMA))["scene_delta"]
    assert len(body) == 6  # all events: the log never reaches beat 360


def test_scene_delta_only_pc_perceived_events() -> None:
    events = [
        _ev("ev_0000", 10, "wait", PLAYER, None),
        # NPC event the PC learns from (a record with who == player)
        _ev(
            "ev_0001", 12, "talk", "npc_barkeep_01", "ev_0000",
            knowledge=(_rec(PLAYER, "noise_by_the_bar", 12, "ev_0001"),),
        ),
        # NPC event witnessed only by another NPC — invisible to the PC (T3)
        _ev(
            "ev_0002", 14, "talk", "npc_drunk_01", "ev_0001",
            knowledge=(_rec("npc_guard_01", "anything", 14, "ev_0002"),),
        ),
    ]
    body = _blocks(render_brief(assemble_brief(events, PACK)))["scene_delta"]
    assert len(body) == 2
    assert body[0].startswith("[t 14]") is False  # newest first is ev_0001, not ev_0002
    assert body[0].startswith("[t 12]")
    assert body[1].startswith("[t 10]")


def test_scene_delta_beat_window_excludes_before_last_beat() -> None:
    # tick-monotonic (log-shaped) events: the writer's invariant — the
    # assembler's newest-first walk and the window break both rely on it
    events = [
        _ev("ev_0000", 100, "wait", PLAYER, None),
        _ev("ev_0001", 360, "wait", PLAYER, "ev_0000"),  # AT the beat — excluded
        _ev("ev_0002", 400, "wait", PLAYER, "ev_0001"),  # after beat 360
    ]
    body = _blocks(render_brief(assemble_brief(events, PACK)))["scene_delta"]
    assert body == ["[t 400] wait: the player"]


# -- recalled facts (BRIEF_SPEC §3.3) -------------------------------------------


def test_recalled_facts_ranked_by_recency_and_importance() -> None:
    events = [
        _ev("ev_0000", 10, "rumor_told", "npc_drunk_01", None,
            knowledge=(_rec(PLAYER, "old_low", 10, "ev_0000"),), importance="low"),
        _ev("ev_0001", 20, "rumor_told", "npc_drunk_01", "ev_0000",
            knowledge=(_rec(PLAYER, "old_high", 20, "ev_0001"),), importance="high"),
        _ev("ev_0002", 590, "rumor_told", "npc_drunk_01", "ev_0001",
            knowledge=(_rec(PLAYER, "recent_low", 590, "ev_0002"),), importance="low"),
        _ev("ev_0003", 600, "wait", PLAYER, "ev_0002"),
    ]
    body = _blocks(render_brief(assemble_brief(events, PACK)))["recalled_facts"]
    tokens = [line.rsplit(" ", 1)[1] for line in body]
    # importance dominates: old_high (rank 2) outranks recent_low (rank 0)
    # despite the 570-tick age gap; old_low is last.
    assert tokens == ["old_high", "recent_low", "old_low"]


def test_recalled_facts_dedup_by_token_and_player_only() -> None:
    events = [
        _ev("ev_0000", 10, "rumor_told", "npc_drunk_01", None,
            knowledge=(_rec(PLAYER, "same_token", 10, "ev_0000"),)),
        _ev("ev_0001", 20, "rumor_told", "npc_drunk_01", "ev_0000",
            knowledge=(_rec(PLAYER, "same_token", 20, "ev_0001"),), importance="high"),
        _ev("ev_0002", 30, "talk", "npc_barkeep_01", "ev_0001",
            knowledge=(_rec("npc_guard_01", "other_npc_token", 30, "ev_0002"),)),
    ]
    body = _blocks(render_brief(assemble_brief(events, PACK)))["recalled_facts"]
    assert len(body) == 1  # dedup keeps the best-ranked (t 20, high); NPC record excluded
    assert body[0].endswith("same_token")
    assert body[0].startswith("- [t 20, saw, exact]")


def test_recalled_facts_max_items_is_a_ranking_cap_not_a_drop() -> None:
    """13 records, max_items 12: 12 lines and NO marker — the top-k is the
    O(relevance) law, not a budget drop (BRIEF_SPEC §3.3)."""
    events = []
    for i in range(13):
        events.append(
            _ev(f"ev_{i:04d}", i, "rumor_told", "npc_drunk_01",
                None if i == 0 else f"ev_{i - 1:04d}",
                knowledge=(_rec(PLAYER, f"token_{i:02d}", i, f"ev_{i:04d}"),))
        )
    text = render_brief(assemble_brief(events, PACK))
    body = _blocks(text)["recalled_facts"]
    assert len(body) == 12
    assert "[truncated:" not in text.split("## recalled_facts")[1].split("##")[0]


# -- scheduled lore (BRIEF_SPEC §3.4) -------------------------------------------


def test_lore_beat_windows() -> None:
    def lore_at(tick: int) -> list[str]:
        events = [_ev("ev_0000", tick, "wait", PLAYER, None)]
        return _blocks(render_brief(assemble_brief(events, PACK)))["scheduled_lore"]

    both = [entry["text"] for entry in PACK.rules["brief"]["lore"]]
    assert lore_at(0) == [PACK.rules["brief"]["lore"][0]["text"]]  # beat 0: salt_road
    assert lore_at(400) == both  # beats 1-2: both entries eligible
    assert lore_at(1456) == [PACK.rules["brief"]["lore"][1]["text"]]  # beat 3
    assert lore_at(9000) == []  # beat 6+: window closed


# -- beat arithmetic (the read-side mirror of core/loop.py) ---------------------


def test_last_beat_tick_mirrors_the_loop_law() -> None:
    rules = PACK.rules
    assert last_beat_tick(rules, 58) is None
    assert last_beat_tick(rules, 360) == 360
    assert last_beat_tick(rules, 400) == 360
    assert last_beat_tick(rules, 1456) == 1080
    assert last_beat_tick(rules, 1800) == 1800  # day-1 first beat
    assert beats_crossed(rules, 1456) == 3
    assert beats_crossed(rules, 359) == 0


def test_zero_offset_beat_never_fires_at_t0() -> None:
    """The loop's day-1 edge (`core/loop.py` `_first_beat`): an offset of 0
    belongs to day 1+ — the backward mirror must agree."""
    rules = json.loads(json.dumps(dict(PACK.rules)))
    rules["urgencies"]["beat_ticks"] = [0, 720]
    assert last_beat_tick(rules, 0) is None
    assert last_beat_tick(rules, 719) is None
    assert last_beat_tick(rules, 1440) == 1440
    # beats at or before 1440: 720 (day 0) + 1440 (day 1, offset 0) = 2
    assert beats_crossed(rules, 1440) == 2
    assert beats_crossed(rules, 2160) == 3  # + 2160 (day 1, offset 720)


# -- the token model (BRIEF_SPEC §4) ---------------------------------------------


def test_token_count_is_whitespace_tokens() -> None:
    assert token_count("") == 0
    assert token_count("one") == 1
    assert token_count("  a  b   c ") == 3


# -- the fill law (BRIEF_SPEC §5.1) ----------------------------------------------


def test_fill_stops_at_soft_target() -> None:
    pack = _mutated_pack(
        lambda rules: rules["brief"]["blocks"].update(
            scene_delta={"soft": 1, "hard": 500}
        )
    )
    events = [
        _ev(f"ev_{i:04d}", i, "wait", PLAYER, None if i == 0 else f"ev_{i - 1:04d}")
        for i in range(5)
    ]
    text = render_brief(assemble_brief(events, pack))
    body = _blocks(text)["scene_delta"]
    assert len(body) == 1  # soft=1: the first item crosses the target, filling stops
    assert "[truncated:4 items dropped]" in text


def test_fill_hard_ceiling_skips_busting_item_greedy_best_fit() -> None:
    """A too-big item is skipped; a smaller lower-ranked one still fits."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["blocks"].update(
            scheduled_lore={"soft": 100, "hard": 12}
        )
    )
    big = " ".join(["word"] * 20)     # 20 tokens — busts the hard ceiling
    small = " ".join(["word"] * 10)   # 10 tokens — fits
    pack.data["rules.json"]["brief"]["lore"] = [
        {"id": "big", "text": big, "from_beat": 0, "to_beat": 9},
        {"id": "small", "text": small, "from_beat": 0, "to_beat": 9},
    ]
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    text = render_brief(assemble_brief(events, pack))
    body = _blocks(text)["scheduled_lore"]
    assert body == [small]
    assert "[truncated:1 items dropped]" in text


def test_no_marker_when_nothing_dropped() -> None:
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert "[truncated:" not in text


# -- whole-block eviction (BRIEF_SPEC §5.2) ---------------------------------------


def test_total_overflow_evicts_scheduled_lore_first() -> None:
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=1))
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    text = render_brief(assemble_brief(events, pack))
    # every evictable block is evicted (total_hard=1 can never fit):
    # header + marker only, no body lines anywhere but directives
    for block_id in ("scene_delta", "recalled_facts", "scheduled_lore",
                     "voice_exemplars", "active_options"):
        assert _blocks(text)[block_id] == []
    assert "[truncated:" in text


def test_directives_never_evicted() -> None:
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=1))
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    text = render_brief(assemble_brief(events, pack))
    directives = _blocks(text)["directives"]
    assert directives == [
        "Narrate only what the brief contains; the log is the canon.",
        "Facts are immutable; prose is yours.",
        "Never invent events, names, or outcomes.",
    ]


def test_evicted_block_renders_header_and_marker_only() -> None:
    """A moderate overflow: scheduled_lore (lowest priority) is evicted
    whole — its items count in the marker, its header stays. The ceiling
    is computed from the un-evicted render so the test stays robust to
    pack text edits: evicting exactly scheduled_lore makes it fit."""
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    pack_free = _mutated_pack(
        lambda rules: rules["brief"].update(total_hard=10**9)
    )
    base = assemble_brief(events, pack_free)
    base_total = sum(
        token_count(line) for block in base.blocks for line in block.render()
    )
    lore = next(b for b in base.blocks if b.block_id == "scheduled_lore")
    lore_tokens = sum(token_count(line) for line in lore.render())
    marker_tokens = token_count("[truncated:1 items dropped]")
    freed = lore_tokens - token_count(f"## {lore.block_id}") - marker_tokens
    total_hard = base_total - freed  # overflow by exactly the freed amount

    pack = _mutated_pack(
        lambda rules: rules["brief"].update(total_hard=total_hard)
    )
    text = render_brief(assemble_brief(events, pack))
    lore_section = text.split("## scheduled_lore")[1].split("##")[0]
    assert "[truncated:" in lore_section
    assert "salt road" not in lore_section  # the lore text itself is gone
    # and higher-priority blocks survived untouched
    assert _blocks(text)["active_options"]


def test_empty_block_is_not_evicted() -> None:
    """An empty block frees nothing — eviction skips it (no marker spam)."""
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=1))
    # craft an event far past every lore window so scheduled_lore is EMPTY
    events = [_ev("ev_0000", 9000, "wait", PLAYER, None)]
    text = render_brief(assemble_brief(events, pack))
    lore_section = text.split("## scheduled_lore")[1].split("##")[0]
    assert lore_section.strip() == ""  # header alone: no body, no marker


# -- pack lint (BRIEF_SPEC §6, the core/pack.py enforcement) ----------------------


def test_pack_lint_requires_brief_section(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        del rules["brief"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="brief section is required"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_block_set_mismatch(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        del rules["brief"]["blocks"]["voice_exemplars"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="blocks must be exactly"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_soft_above_hard(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["blocks"]["scene_delta"]["soft"] = 9999
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="soft must be <= hard"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_directives_over_own_hard(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["directives"].append(" ".join(["filler"] * 100))
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="exceed their own hard budget"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_inverted_lore_window(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["lore"][0]["from_beat"] = 5
        rules["brief"]["lore"][0]["to_beat"] = 2
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="from_beat must be < to_beat"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_duplicate_lore_ids(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["lore"].append(dict(rules["brief"]["lore"][0]))
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="unique non-empty strings"):
        load_pack(_broken_pack(tmp_path, mutate))
