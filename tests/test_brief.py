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
    SceneLedger,
    assemble_brief,
    beats_crossed,
    brief_from_log,
    last_beat_tick,
    render_brief,
    token_count,
)
from core.log import (
    EventRecord,
    LoggedKnowledgeRecord,
    StateChange,
    read_log,
)
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
    """The golden fixture carries no session ledger — scene_texture is an
    explicit empty header, never an omission (BRIEF_SPEC §7). (Until st-1
    this pin rode recalled_facts: the smoke PC held no records; the
    arrival snapshot now seeds presence tokens on every move.)"""
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert "## scene_texture\n\n" in text


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


# -- scheduled lore (BRIEF_SPEC §3.6; was §3.5 — the renumber rode a stale
# §3.4 citation, KI#45) ------------------------------------------------------------


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


# -- scene texture: the 7th block (BRIEF_SPEC §3.3, iter-10) ---------------------


def _texture_ledger(events: list[Any]) -> SceneLedger:
    """A ledger with tavern scene texture + guard entity texture, live."""
    ledger = SceneLedger()
    ledger.apply_delta(
        {
            "source": "turn:1",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "candles", "value": "lit",
                 "surface": "Tallow candles guttered on the bar."},
                {"scope": "entity:npc_guard_01", "slot": "cloak", "value": "muddy hem",
                 "surface": "The guard's cloak trailed a muddy hem."},
            ],
        },
        events,
        PACK,
    )
    return ledger


def test_scene_texture_sits_at_position_three() -> None:
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    headers = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert headers.index("scene_texture") == 2  # after scene_delta, before recalled_facts


def test_no_ledger_renders_an_explicit_empty_block() -> None:
    """ledger=None is the same bytes as an empty ledger (explicit absence,
    never omission — BRIEF_SPEC §7); the golden log carries no session."""
    text = brief_from_log(GOLDEN, PACK, SCHEMA)
    assert "## scene_texture\n\n" in text


def test_none_ledger_equals_empty_ledger_bytes() -> None:
    from core.log import read_log

    _header, events = read_log(GOLDEN, SCHEMA)
    assert render_brief(assemble_brief(events, PACK)) == render_brief(
        assemble_brief(events, PACK, SceneLedger())
    )


def test_scene_texture_window_and_line_shapes() -> None:
    from core.log import read_log

    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = _texture_ledger(events[:2])
    body = _blocks(render_brief(assemble_brief(events[:2], PACK, ledger)))["scene_texture"]
    assert body == [
        "- [t 32, active] npc_guard_01: cloak = muddy hem",  # newest first
        "- [t 32, active] candles = lit",
    ]
    # at the full log the PC is at the market: the tavern scene closed
    # (auto-sync) and the guard is absent — the window is empty
    body_full = _blocks(render_brief(assemble_brief(events, PACK, ledger)))["scene_texture"]
    assert body_full == []


def test_scene_texture_pinned_first_ranking() -> None:
    from core.log import read_log

    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = _texture_ledger(events[:2])
    ledger.apply_delta(
        {"source": "turn:2", "refs": [{"id": "tex_0000"}]}, events[:2], PACK
    )  # pin the OLDER entry
    body = _blocks(render_brief(assemble_brief(events[:2], PACK, ledger)))["scene_texture"]
    assert body == [
        "- [t 32, pinned] candles = lit",  # pinned outranks newer actives
        "- [t 32, active] npc_guard_01: cloak = muddy hem",
    ]


def test_scene_texture_stale_scene_scoped_entries_are_invisible() -> None:
    """Texture from an earlier scene at the SAME location is gone with
    that scene even if the ledger never synced (the window law is
    belt-and-braces: `t >= scene.from_tick` — a revisit starts empty)."""
    from core.log import StateChange

    def _move(eid: str, t: int, cause: str | None, from_: str, to: str) -> EventRecord:
        return EventRecord(
            id=eid, t=t, type="move", actor=PLAYER, cause=cause, outcome={},
            knowledge=(), hooks=(), importance="low", provenance={"seed": 42},
            target=to,
            state_changes=(StateChange(PLAYER, "position", from_, to),),
        )

    events = [
        _move("ev_0000", 2, None, "loc_street", "loc_tavern"),
        _ev("ev_0001", 30, "wait", PLAYER, "ev_0000"),
        _move("ev_0002", 40, "ev_0001", "loc_tavern", "loc_backyard"),
        _move("ev_0003", 50, "ev_0002", "loc_backyard", "loc_tavern"),  # revisit
    ]
    ledger = SceneLedger()
    ledger.apply_delta(
        {
            "source": "turn:1",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "candles", "value": "lit",
                 "surface": "Tallow candles."}
            ],
        },
        events[:2],
        PACK,
    )  # established in tavern scene 0 (t=30); never synced again
    body = _blocks(render_brief(assemble_brief(events, PACK, ledger)))["scene_texture"]
    assert body == []  # tavern scene 1 starts empty


def test_scene_texture_max_items_is_a_ranking_cap_not_a_drop() -> None:
    from core.log import read_log

    pack = _mutated_pack(
        lambda rules: rules["brief"]["scene_texture"].update(max_items=1)
    )
    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = _texture_ledger(events[:2])
    text = render_brief(assemble_brief(events[:2], pack, ledger))
    body = _blocks(text)["scene_texture"]
    assert len(body) == 1  # the top-k survivor, newest-first
    assert "[truncated:" not in text.split("## scene_texture")[1].split("##")[0]


def test_scene_texture_tombstones_render_with_cause_and_cap() -> None:
    from core.log import StateChange, read_log

    pack = _mutated_pack(
        lambda rules: rules["brief"]["scene_texture"].update(tombstone_max_items=1)
    )
    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = SceneLedger()
    ledger.apply_delta(
        {
            "source": "turn:1",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "candles", "value": "lit",
                 "surface": "Tallow candles."},
                {"scope": "scene:loc_tavern", "slot": "shutters", "value": "ajar",
                 "surface": "The shutters stood ajar."},
            ],
        },
        events[:2],
        PACK,
    )
    ledger.retire_contradicted(
        (
            EventRecord(
                id="ev_9000", t=40, type="gust", actor="npc_drunk_01", cause=None,
                outcome={}, knowledge=(), hooks=(), importance="low",
                provenance={"seed": 42}, target=None,
                state_changes=(StateChange("loc_tavern", "candles", None, "scattered"),),
            ),
            EventRecord(
                id="ev_9001", t=44, type="gust", actor="npc_drunk_01", cause="ev_9000",
                outcome={}, knowledge=(), hooks=(), importance="low",
                provenance={"seed": 42}, target=None,
                state_changes=(StateChange("loc_tavern", "shutters", None, "slammed"),),
            ),
        )
    )
    text = render_brief(assemble_brief(events[:2], pack, ledger))
    body = _blocks(text)["scene_texture"]
    assert body == ["- [t 32, refuted] shutters (cause: ev_9001)"]  # newest tombstone only


def test_scene_texture_byte_identity_across_calls() -> None:
    from core.log import read_log

    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = _texture_ledger(events[:2])
    first = render_brief(assemble_brief(events[:2], PACK, ledger))
    second = render_brief(assemble_brief(events[:2], PACK, ledger))
    assert first == second  # same (log, ledger, pack) → same brief bytes (D-049)


def test_scene_texture_evicted_after_scene_delta_before_exemplars() -> None:
    """scene_texture's eviction rank: below scene_delta, above
    voice_exemplars (BRIEF_SPEC §5.2 — continuity outranks lore, sits
    under voice/options)."""
    from core.log import read_log

    _header, events = read_log(GOLDEN, SCHEMA)
    ledger = _texture_ledger(events[:2])

    pack_free = _mutated_pack(
        lambda rules: rules["brief"].update(total_hard=10**9)
    )
    base = assemble_brief(events[:2], pack_free, ledger)
    base_total = sum(
        token_count(line) for block in base.blocks for line in block.render()
    )

    def freed(block_id: str) -> int:
        block = next(b for b in base.blocks if b.block_id == block_id)
        block_tokens = sum(token_count(line) for line in block.render())
        marker = token_count("[truncated:1 items dropped]")
        return block_tokens - token_count(f"## {block_id}") - marker

    # evicting {scheduled_lore, recalled_facts, scene_delta} fits:
    # scene_texture SURVIVES (it outranks scene_delta)
    total_hard = base_total - (
        freed("scheduled_lore") + freed("recalled_facts") + freed("scene_delta")
    )
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=total_hard))
    text = render_brief(assemble_brief(events[:2], pack, ledger))
    assert _blocks(text)["scene_texture"]  # survived
    assert _blocks(text)["voice_exemplars"]  # higher priority, obviously alive

    # evicting through scene_texture fits: voice_exemplars still SURVIVES
    total_hard = base_total - (
        freed("scheduled_lore") + freed("recalled_facts") + freed("scene_delta")
        + freed("scene_texture")
    )
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=total_hard))
    text = render_brief(assemble_brief(events[:2], pack, ledger))
    assert _blocks(text)["scene_texture"] == []  # evicted whole
    assert _blocks(text)["voice_exemplars"]  # scene_texture fell first


def test_pack_lint_requires_scene_texture_config(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        del rules["brief"]["scene_texture"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="scene_texture must be an object"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_bad_texture_caps(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["scene_texture"]["max_items"] = 0
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="max_items must be an integer >= 1"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_duplicate_unique_slots(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["scene_texture"]["unique_slots"] = ["cloak", "cloak"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="unique_slots must be unique"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- present entities: the 8th block (BRIEF_SPEC §3.8, st-1) ----------------------


def _golden_prefix(ticks: int = 2) -> list[EventRecord]:
    _header, events = read_log(GOLDEN, SCHEMA)
    return list(events[:ticks])


def test_present_entities_cards_and_pair_tokens() -> None:
    """The entity cards on the tavern prefix: the scene line
    (pack-declared layout field, canon-from-birth), then one dry line per
    present non-carried entity in pack order, status markers from the
    pack table, carried items folded into the carrier's segment, then
    the directed pair lines (the cross-NPC-consistency home)."""
    text = render_brief(assemble_brief(_golden_prefix(), PACK))
    assert _blocks(text)["present_entities"] == [
        "- scene loc_tavern (Three Barrels tavern) layout=low_beamed_hall",
        "- pc_01 (the player)",
        "- npc_guard_01 (Doren) carries=purse_01",
        "- npc_barkeep_01 (the barkeep) carries=club_01",
        "- npc_drunk_01 (the drunkard) markers=drunk",
        "- npc_maid_01 (the serving maid)",
        "- oil_lamp_01 (the oil lamp)",
        "- ale_mug_01 (the mug of ale)",
        "- pair npc_drunk_01 -> npc_guard_01 fear=40",
        "- pair npc_maid_01 -> npc_barkeep_01 trust=70",
    ]


def test_present_entities_absent_pair_partner_renders_no_pair_line() -> None:
    """The guards' mutual trust seeds never render in the tavern prefix —
    npc_guard_02 is at the guardroom: pair lines need BOTH present."""
    text = render_brief(assemble_brief(_golden_prefix(), PACK))
    assert "npc_guard_02" not in _blocks(text)["present_entities"].__str__()


def test_present_entities_empty_log_renders_the_starting_scene() -> None:
    """No events: the scene is the PC's pack-start location (the street);
    presence is the structural projection read (the quiet-beat answer
    needs no events at all) and the scene line already carries the
    pack-declared layout — canon from birth, no promotion required."""
    text = render_brief(assemble_brief((), PACK))
    assert _blocks(text)["present_entities"] == [
        "- scene loc_street (the street in front of the tavern) layout=open_street",
        "- pc_01 (the player)",
    ]


def test_present_entities_marker_thresholds_are_pack_data() -> None:
    """The drunkard's `drunk` marker is the pack's (prop, min) call: at
    min=60 the intoxicication 50 no longer carries a marker."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["present_entities"]["card_markers"].__setitem__(
            0, {"prop": "status.intoxication", "min": 60, "marker": "drunk"}
        )
    )
    text = render_brief(assemble_brief(_golden_prefix(), pack))
    assert "markers=drunk" not in text


def test_present_entities_caps_are_ranking_caps_never_drops() -> None:
    """max_entities/max_pairs cap the ranking (D-047 law): beyond-cap
    items render nothing and NEVER produce a [truncated:N] marker."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["present_entities"].update(max_entities=2)
    )
    text = render_brief(assemble_brief(_golden_prefix(), pack))
    body = _blocks(text)["present_entities"]
    # the scene line is structural (≤1, never capped); two entity cards
    # (pack order: the player, then Doren) — the pair lines are a separate
    # ranking, unaffected by max_entities
    assert body[0] == (
        "- scene loc_tavern (Three Barrels tavern) layout=low_beamed_hall"
    )
    assert body[1:3] == [
        "- pc_01 (the player)",
        "- npc_guard_01 (Doren) carries=purse_01",
    ]
    assert body[3:] == [
        "- pair npc_drunk_01 -> npc_guard_01 fear=40",
        "- pair npc_maid_01 -> npc_barkeep_01 trust=70",
    ]
    assert "[truncated:" not in text.split("## present_entities")[1].split("##")[0]

    pack = _mutated_pack(
        lambda rules: rules["brief"]["present_entities"].update(max_pairs=1)
    )
    body = render_brief(assemble_brief(_golden_prefix(), pack)) \
        .split("## present_entities")[1].split("##")[0]
    assert body.count("- pair ") == 1


def _promotion_event(
    eid: str, t: int, scope: str, slot: str, value: str, target: str
) -> EventRecord:
    """A committed D-054 promotion: a take event whose outcome carries the
    texture reference and whose state_changes birth the slot on the scope
    target (the same detection law as brief/mediator.py::promotions_in)."""
    return EventRecord(
        id=eid, t=t, type="take", actor=PLAYER, cause=None, target=None,
        outcome={"texture": {"entry": "tex_0000", "scope": scope,
                             "slot": slot, "value": value}},
        knowledge=(),
        state_changes=(
            StateChange(entity=target, prop=slot, from_=None, to_=value),
        ),
        hooks=(), importance="low", provenance={"seed": 42},
    )


def test_present_entities_scene_line_renders_pack_fields_then_promotions() -> None:
    """The scene line is canon-from-birth architecture plus canon-born
    props: the pack-declared location fields (scene_line_fields) render
    with no promotions at all; a scene-scoped promotion appends its props
    after them (the card law: static surface first, event-born news
    last — post-promotion texture stays visible to the narrator)."""
    text = render_brief(assemble_brief(_golden_prefix(), PACK))
    assert (
        "- scene loc_tavern (Three Barrels tavern) layout=low_beamed_hall"
        in _blocks(text)["present_entities"]
    )

    events = _golden_prefix() + [
        _promotion_event(
            "ev_9000", 2, "scene:loc_tavern", "candles", "lit", "loc_tavern"
        )
    ]
    text = render_brief(assemble_brief(events, PACK))
    assert (
        "- scene loc_tavern (Three Barrels tavern) "
        "layout=low_beamed_hall candles=lit"
        in _blocks(text)["present_entities"]
    )


def test_present_entities_scene_line_fields_are_pack_data() -> None:
    """A pack that declares no scene_line_fields keeps the pre-iter-20
    behavior: no scene line without promoted props (the block is an
    opt-in, never an engine assumption)."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["present_entities"].pop("scene_line_fields")
    )
    text = render_brief(assemble_brief(_golden_prefix(), pack))
    assert "- scene" not in text


def test_present_entities_entity_scoped_promotion_rides_the_card() -> None:
    """An entity-scoped promotion renders on the present entity's card —
    the promoted-prop visibility law; an absent holder renders nothing."""
    events = _golden_prefix() + [
        _promotion_event(
            "ev_9000", 2, "entity:npc_maid_01", "kerchief", "blue", "npc_maid_01"
        )
    ]
    text = render_brief(assemble_brief(events, PACK))
    assert (
        "- npc_maid_01 (the serving maid) kerchief=blue"
        in _blocks(text)["present_entities"]
    )


def test_present_entities_outranks_scene_texture_in_eviction() -> None:
    """BRIEF_SPEC §5.2 order: scene_texture evicts before
    present_entities (canon-projection structure outranks narrator
    texture), voice_exemplars after it. Needs a NON-empty scene_texture —
    an empty block frees nothing and is skipped by the eviction loop."""
    events = _golden_prefix()
    ledger = _texture_ledger(events)
    base = assemble_brief(events, PACK, ledger)
    base_total = sum(
        token_count(line) for block in base.blocks for line in block.render()
    )

    def freed(block_id: str) -> int:
        block = next(b for b in base.blocks if b.block_id == block_id)
        body_tokens = (
            sum(token_count(line) for line in block.render())
            - token_count(f"## {block_id}")
        )
        if not block.lines:
            return 0  # an empty block frees nothing (skipped by the loop)
        marker = token_count(f"[truncated:{len(block.lines)} items dropped]")
        return body_tokens - marker

    # evicting through scene_texture fits: present_entities SURVIVES
    total_hard = base_total - (
        freed("scheduled_lore") + freed("recalled_facts") + freed("scene_delta")
        + freed("scene_texture")
    )
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=total_hard))
    text = render_brief(assemble_brief(events, pack, ledger))
    assert _blocks(text)["present_entities"]  # survived
    assert _blocks(text)["scene_texture"] == []  # fell first

    # evicting through present_entities fits: voice_exemplars survives
    total_hard = base_total - (
        freed("scheduled_lore") + freed("recalled_facts") + freed("scene_delta")
        + freed("scene_texture") + freed("present_entities")
    )
    pack = _mutated_pack(lambda rules: rules["brief"].update(total_hard=total_hard))
    text = render_brief(assemble_brief(events, pack, ledger))
    assert _blocks(text)["present_entities"] == []  # evicted whole
    assert _blocks(text)["voice_exemplars"]  # never fell before presence


def test_pack_lint_requires_present_entities_config(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        del rules["brief"]["present_entities"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="present_entities must be an object"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_bad_presence_caps(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["max_pairs"] = 0
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="max_pairs must be an integer >= 1"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_marker_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["card_markers"].append(
            {"prop": "status.grace", "min": 1, "marker": "elegant"}
        )
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="is not one of the pack's"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_scene_line_field(tmp_path: Path) -> None:
    """iter-20/D-057: scene_line_fields must reference real location
    fields — a typo'd field name fails at load time, never silently
    renders nothing."""

    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["scene_line_fields"] = ["layoutx"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="scene_line_fields must reference"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- tune-2 (iter-28, D-060): the crime cascade renders on the cards ------------


def _suspicion_event(eid: str, t: int, level: int) -> EventRecord:
    """A suspicion_changed event in the ev_0007 shape: the watcher's
    relations.suspicion moves and the suspect's crime_status flips on the
    first crossing of the pack's suspect threshold."""
    return EventRecord(
        id=eid, t=t, type="suspicion_changed", actor="npc_guard_01",
        cause=None, target=PLAYER,
        outcome={"token": "figure_reaching_for_purse", "delta": 25,
                 "from": 0, "to": level},
        knowledge=(),
        state_changes=(
            StateChange(entity="npc_guard_01", prop="relations.suspicion",
                        from_=0, to_=level),
            StateChange(entity=PLAYER, prop="crime_status",
                        from_="unknown", to_="suspect"),
        ),
        hooks=(), importance="low", provenance={"seed": 42},
    )


def test_card_markers_render_the_crime_cascade() -> None:
    """tune-2 (iter-17's finding): the suspicion axis and the crime_status
    flip were invisible through the brief — the marker table's axis lookup
    was status-prefixed, so a relations.suspicion row was not even
    expressible in pack data. The card_markers table is prop-path keyed
    with threshold rows (numeric min) and value rows (string value): the
    guard's card renders `wary` at suspicion >= 25 and the player's card
    renders `suspect` on the status flip."""
    events = _golden_prefix() + [_suspicion_event("ev_9000", 2, 35)]
    text = render_brief(assemble_brief(events, PACK))
    body = _blocks(text)["present_entities"]
    assert "- npc_guard_01 (Doren) markers=wary carries=purse_01" in body
    assert "- pc_01 (the player) markers=suspect" in body


def test_card_markers_threshold_row_respects_the_pack_number() -> None:
    """The wary threshold is the table's own number (v0.1 aligns it with
    the status_suspect_at flip at 25): session 8's watch-handover
    boundary — suspicion 20 both guards, crime_status stays unknown —
    renders no marker (the threshold row reads the pack data, not the
    flip)."""
    events = _golden_prefix() + [
        EventRecord(
            id="ev_9000", t=2, type="suspicion_changed", actor="npc_guard_01",
            cause=None, target=PLAYER,
            outcome={"token": "trail_and_noise", "delta": 20, "from": 0, "to": 20},
            knowledge=(),
            state_changes=(
                StateChange(entity="npc_guard_01", prop="relations.suspicion",
                            from_=0, to_=20),
            ),
            hooks=(), importance="low", provenance={"seed": 42},
        )
    ]
    text = render_brief(assemble_brief(events, PACK))
    body = _blocks(text)["present_entities"]
    assert "- npc_guard_01 (Doren) carries=purse_01" in body  # no wary at 20
    assert "markers=suspect" not in text  # no flip below the threshold


def test_card_markers_value_row_is_pack_data() -> None:
    """The value-row kind is generic pack data: a mutated pack renders a
    different marker for the same crime_status value (the row, not the
    engine, owns the vocabulary)."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["present_entities"]["card_markers"].__setitem__(
            5, {"prop": "crime_status", "value": "suspect", "marker": "marked"}
        )
    )
    events = _golden_prefix() + [_suspicion_event("ev_9000", 2, 35)]
    text = render_brief(assemble_brief(events, pack))
    assert "markers=marked" in _blocks(text)["present_entities"].__str__()


def test_scene_delta_stays_blind_to_interior_suspicion() -> None:
    """The scene_delta half of the iter-17 finding is NOT a defect:
    suspicion_changed rides no knowledge record, and the delta window is
    the PC's own perception (the blind-NPC law, BRIEF_SPEC §3.2) — the
    card is the narrator's read surface for standing state, the delta
    window is the player's. The two halves have different owners."""
    events = _golden_prefix() + [_suspicion_event("ev_9000", 2, 35)]
    text = render_brief(assemble_brief(events, PACK))
    delta = _blocks(text)["scene_delta"]
    assert "suspicion_changed" not in delta
