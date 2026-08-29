"""iter-5 acceptance — the renderer (CHRON-1, `docs/blueprint/phase0.md`
§5): the tracery engine + the chronicle as a pure function of the log.

The renderer invariants made executable: determinism (same log → same
bytes, T1 covers the chronicle), cosmetic-stream-only draws (INV-2 /
RNG-1), zero log writes (INV-1 — nothing to assert directly, but every
entry point here takes events and returns strings), the importance
gate, prefix stability under log growth, and the ink-shuffle
no-immediate-repeat discipline.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import Pack, load_pack
from core.rng import RngBank
from render.chronicle import (
    RenderError,
    chronicle_from_log,
    render_chronicle,
    render_entity_view,
    render_scene_card,
)
from render.tracery import Engine, Grammar, GrammarError

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")

MINI_TEMPLATES = {
    "day_header": "— Day #day#, #phase.capitalize# —",
    "scene_card": "{location_name}: {present_names}",
    "fallback": "[{t}] {event_type}: {actor}",
    "tale_gate": {"min_importance": "low"},
    "symbols": {
        "flame_take": ["Flame takes to {location}.", "Fire catches at {location}."],
    },
    "events": {
        "fire_spread": [
            "A spreads within {location}.",
            "B spreads within {location}.",
            "C spreads within {location}.",
        ],
        "rumor_told": (
            "{accepted?{actor} tells {target}: {knows}."
            "|{target} does not believe {actor}.}"
        ),
        "save_demo": "[thing:#flame_take#]First: #thing# — again: #thing#",
    },
}


def run_day1(tmp_path: Path, seed: int = 8) -> list[EventRecord]:
    """The §3 walkthrough shape: theft, arson, and a long wait crossing
    beats and rotations — every reaction system gets a chance to fire."""
    script = load_playscript(REPO / "tests" / "playscripts" / "day1_theft_and_arson.json")
    script = dict(script, steps=script["steps"][:5] + [{"intent": "wait", "ticks": 1400}])
    sim = Simulator(PACK, seed, tmp_path / "day1.jsonl", SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(tmp_path / "day1.jsonl", SCHEMA)
    return events


def crafted_event(
    event_id: str, t: int, event_type: str, importance: str = "low"
) -> EventRecord:
    """A minimal valid event for renderer-level tests."""
    return EventRecord(
        id=event_id, t=t, type=event_type, actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=(), hooks=(),
        importance=importance, provenance={"seed": 42}, target="loc_tavern",
    )


# -- the grammar (lint + engine) ----------------------------------------------


def test_pack_grammar_loads_and_lints() -> None:
    grammar = Grammar(PACK.templates)
    assert grammar.tale_gate == "low"
    assert "event.fire_spread" in grammar
    assert grammar.alternatives("event.fire_spread")  # pooled variety exists


def test_lint_rejects_unknown_modifier() -> None:
    broken = copy.deepcopy(MINI_TEMPLATES)
    broken["events"]["bad"] = "#x.past#"
    with pytest.raises(GrammarError, match="unknown modifier"):
        Grammar(broken)


def test_lint_rejects_unterminated_reference() -> None:
    broken = copy.deepcopy(MINI_TEMPLATES)
    broken["events"]["bad"] = "broken #symbol"
    with pytest.raises(GrammarError, match="unterminated"):
        Grammar(broken)


def test_unknown_symbol_is_loud_at_expand() -> None:
    broken = copy.deepcopy(MINI_TEMPLATES)
    broken["events"]["bad"] = "#nope#"
    with pytest.raises(GrammarError, match="neither a symbol nor a context slot"):
        Engine(Grammar(broken), RngBank(42)).expand_symbol("event.bad", {})


def test_shuffle_pool_never_repeats_immediately() -> None:
    engine = Engine(Grammar(MINI_TEMPLATES), RngBank(42))
    picks = [
        engine.expand_symbol("event.fire_spread", {"location": "the backyard"})
        for _ in range(12)
    ]
    for earlier, later in zip(picks, picks[1:], strict=False):
        assert earlier != later  # ink's no-immediate-repeat


def test_engine_is_deterministic_per_seed() -> None:
    def sequence(seed: int) -> list[str]:
        engine = Engine(Grammar(MINI_TEMPLATES), RngBank(seed))
        return [
            engine.expand_symbol("event.fire_spread", {"location": "x"})
            for _ in range(10)
        ]

    assert sequence(42) == sequence(42)
    assert sequence(42) != sequence(43)


def test_engine_prefix_stability() -> None:
    """A longer log renders every earlier line identically (the session
    delta-print contract rides on this)."""
    grammar = Grammar(MINI_TEMPLATES)
    full_engine = Engine(grammar, RngBank(42))
    prefix_engine = Engine(grammar, RngBank(42))
    full = [full_engine.expand_symbol("event.fire_spread", {"location": "x"})
            for _ in range(8)]
    prefix = [prefix_engine.expand_symbol("event.fire_spread", {"location": "x"})
              for _ in range(5)]
    assert full[:5] == prefix


def test_modifiers() -> None:
    engine = Engine(Grammar(MINI_TEMPLATES), RngBank(42))
    text = engine.expand_text("#word.a# #name.capitalize# #shout.upper#", {
        "word": "tale", "name": "doren", "shout": "fire",
    })
    assert text == "a tale Doren FIRE"


def test_save_and_restore_scope() -> None:
    engine = Engine(Grammar(MINI_TEMPLATES), RngBank(7))
    text = engine.expand_symbol("event.save_demo", {"location": "the yard"})
    first = text.split("First: ")[1].split(" —")[0]
    again = text.split("— again: ")[1]
    assert first == again  # the save holds the same expansion


def test_conditional_reads_raw_truthiness() -> None:
    engine = Engine(Grammar(MINI_TEMPLATES), RngBank(42))
    context = {"actor": "A", "target": "B", "knows": "tok"}
    true_line = engine.expand_symbol("event.rumor_told", {**context, "accepted": True})
    false_line = engine.expand_symbol("event.rumor_told", {**context, "accepted": False})
    assert true_line == "A tells B: tok."
    assert false_line == "B does not believe A."
    # booleans stay booleans — a stringified False must not read as truthy
    assert engine.expand_text("{flag?yes|no}", {"flag": False}) == "no"


def test_slot_reference_with_modifier() -> None:
    engine = Engine(Grammar(MINI_TEMPLATES), RngBank(42))
    assert engine.expand_symbol("day_header", {"day": 3, "phase": "night"}) == (
        "— Day 3, Night —"
    )


def test_render_draws_only_cosmetic() -> None:
    bank = RngBank(42)
    engine = Engine(Grammar(PACK.templates), bank)
    with bank.audit("substantive"):  # RNG-1: zero substantive draws in render
        for _ in range(10):
            engine.expand_symbol("event.fire_spread", {"location": "x"})


def test_grammar_cycle_fails_loudly() -> None:
    cyclic = copy.deepcopy(MINI_TEMPLATES)
    cyclic["symbols"] = {"a": ["#b#"], "b": ["#a#"]}
    with pytest.raises(GrammarError):
        Engine(Grammar(cyclic), RngBank(1)).expand_symbol("a", {})


# -- the chronicle -------------------------------------------------------------


def test_chronicle_renders_day_header_and_lines(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    text = render_chronicle(events, PACK, seed=8)
    assert text.startswith("— Day 1, ")
    assert "the player lifts the purse unseen." in text
    assert "burns out. Nothing will be the same here." in text
    assert "Doren grows warier of the player." in text  # actor=watcher, target=suspect
    assert text.endswith("\n")


def _texture_take(event_id: str, t: int, event_type: str) -> EventRecord:
    """A texture-path take event (iter-11, D-054): the outcome carries the
    mediator-resolved reference, the canon target is None."""
    return EventRecord(
        id=event_id, t=t, type=event_type, actor="pc_01", cause=None,
        outcome={"texture": {"entry": "tex_0000", "scope": "scene:loc_tavern",
                             "slot": "candles", "value": "lit"}},
        knowledge=(), state_changes=(), hooks=(),
        importance="low", provenance={"seed": 42}, target=None,
    )


def test_chronicle_texture_take_renders_the_slot_noun() -> None:
    """iter-11a, KI#39: a texture-path take carries no canon target — the
    take templates branch on {target} and render the promoted slot noun
    (before the fix both lines read 'the player takes .')."""
    events = [
        _texture_take("ev_0000", 4, "take"),
        _texture_take("ev_0001", 6, "take_failed"),
    ]
    text = render_chronicle(events, PACK, seed=42)
    assert "the player takes the candles." in text
    assert "the player reaches for the candles — and is noticed." in text


def test_chronicle_canon_take_line_is_unchanged() -> None:
    """The conditional's true branch keeps the canon line byte-for-byte —
    a targeted take renders exactly as it did before the texture branch
    existed (the T1 chronicle byte-identity depends on this)."""
    events = [EventRecord(
        id="ev_0000", t=4, type="take", actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=(), hooks=(),
        importance="low", provenance={"seed": 42}, target="purse_01",
    )]
    text = render_chronicle(events, PACK, seed=42)
    assert "the player takes the purse." in text


def test_chronicle_groups_days() -> None:
    events = [crafted_event("ev_0000", 100, "move"),
              crafted_event("ev_0001", 1500, "move")]
    text = render_chronicle(events, PACK, seed=42)
    assert "— Day 1, Morning —" in text
    assert "— Day 2, Morning —" in text


def test_chronicle_importance_gate(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    data = copy.deepcopy(dict(PACK.data))
    data["templates.json"] = copy.deepcopy(dict(PACK.templates))
    data["templates.json"]["tale_gate"] = {"min_importance": "medium"}
    strict_pack = Pack(data=data)
    text = render_chronicle(events, strict_pack, seed=8)
    assert "the player lifts the purse unseen." not in text  # low: gated out
    assert "burns out. Nothing will be the same here." in text  # medium: stays


def test_chronicle_fallback_for_unknown_type() -> None:
    events = [crafted_event("ev_0000", 5, "alien_event", importance="high")]
    text = render_chronicle(events, PACK, seed=42)
    assert "(t 5) alien_event: the player" in text


def test_chronicle_is_byte_identical_across_renders(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    first = render_chronicle(events, PACK, seed=8)
    second = render_chronicle(events, PACK, seed=8)
    assert first == second  # fresh bank + fresh pools per pass


def test_chronicle_prefix_stable_under_log_growth(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    prefix = render_chronicle(events[:6], PACK, seed=8)
    full = render_chronicle(events, PACK, seed=8)
    assert full.startswith(prefix)


def test_t1_chronicle_golden_fixture_equals_fresh_run(tmp_path: Path) -> None:
    """T1 covers the chronicle: the committed fixture log and a fresh
    byte-identical run render to identical chronicle bytes."""
    sim = Simulator(PACK, SCRIPT["seed"], tmp_path / "fresh.jsonl", SCHEMA,
                    commit="0000000")
    sim.run_playscript(SCRIPT)
    _, fresh_events = read_log(tmp_path / "fresh.jsonl", SCHEMA)
    _, golden_events = read_log(GOLDEN, SCHEMA)
    assert render_chronicle(golden_events, PACK, seed=42) == render_chronicle(
        fresh_events, PACK, seed=42
    )


def test_chronicle_from_log_reads_seed_from_header(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    log = tmp_path / "seed_check.jsonl"
    lines = [json.dumps({"header": True, "schema_version": "0.1", "seed": 8,
                         "python": "3.11", "commit": "0000000",
                         "pack": "tavern_pack@0.1"})]
    from core.log import event_to_mapping

    lines += [json.dumps(event_to_mapping(e)) for e in events]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert chronicle_from_log(log, PACK, SCHEMA) == render_chronicle(
        events, PACK, seed=8
    )


# -- scene card + entity view ----------------------------------------------------


def test_scene_card_lists_present_entities(tmp_path: Path) -> None:
    projection = initial_projection(PACK.entities)
    projection["pc_01"]["position"] = "loc_tavern"  # walk in from the street
    card = render_scene_card(projection, PACK, seed=42)
    assert card == (
        "Three Barrels tavern: Doren, the barkeep, the drunkard, the serving maid"
    )


def test_scene_card_empty_location(tmp_path: Path) -> None:
    projection = initial_projection(PACK.entities)
    projection["pc_01"]["position"] = "loc_backyard"
    assert render_scene_card(projection, PACK, seed=42) == "the backyard: no one"


def test_entity_view_full_history_and_state(tmp_path: Path) -> None:
    events = run_day1(tmp_path)
    projection = fold(events, initial_projection(PACK.entities))
    text = render_entity_view(events, projection, PACK, "purse_01", seed=8)
    assert text.startswith("the purse (purse_01)")
    assert "carrier: the player" in text
    assert "[t 6] the player lifts the purse unseen." in text
    assert "checks on the purse" in text  # the expectation violation mentions it


def test_entity_view_unknown_entity_is_loud() -> None:
    with pytest.raises(RenderError, match="unknown entity"):
        render_entity_view([], {}, PACK, "npc_ghost_99", seed=42)
