"""drama-1 acceptance (iter-40, phase 3; phases.md §3 — the Paradox
trigger block adapted per L10): the JSON predicate grammar over the
folded projection. `core/predicates.py` owns the grammar; the donor
mechanics live in `docs/ref/paradox_scripting.md`; the contract owner
is `docs/DIRECTOR_SPEC.md` §3.

The laws pinned here:
- The three v0.1 leaf kinds (time / place / threshold) evaluate
  byte-identically to the pre-drama-1 `_trigger_fires` semantics — the
  committed pack's own trigger spec is replayed as the parity pin.
- The `prop` leaf is the generalized projection read (any entity, any
  path, four comparators); a missing prop answers honestly (False
  under ordering and equals, True under not_equals); Python's
  `True == 1` conflation is guarded.
- Compounds compose: `all` (AND), `any` (OR), `not` (single inner),
  and the implicit-AND list root (the Paradox trigger body shape).
- The grammar is loud: unknown kinds, malformed shapes, and unknown
  comparators raise ValueError — never a silent False (L10: validated
  content; the pack lint is the first line, this the backstop).
- Purity (INV-2): the evaluator reads (spec, projection, beat_tick)
  and nothing else — no RNG, no wall-clock, no iteration over entities.
"""

from __future__ import annotations

from typing import Any

import pytest

from core.predicates import COMPARATORS, COMPOUND_KEYS, LEAF_KINDS, evaluate

PROJECTION: dict[str, dict[str, Any]] = {
    "npc_guard_01": {
        "position": "loc_tavern",
        "relations.suspicion": 50,
        "status.fatigue": 30,
        "status.intoxication": 0,
        "crime_status": "unknown",
        "on_duty": True,
    },
    "npc_drunk_01": {
        "position": "loc_backyard",
        "relations.suspicion": 0,
        "status.intoxication": 40,
    },
}


# -- the v0.1 leaf kinds (parity: the pre-drama-1 semantics, unchanged) -------


def test_time_leaf_fires_at_and_after_the_tick() -> None:
    spec = {"kind": "time", "tick": 360}
    assert evaluate(spec, PROJECTION, 359) is False
    assert evaluate(spec, PROJECTION, 360) is True
    assert evaluate(spec, PROJECTION, 720) is True


def test_place_leaf_reads_the_projection_position() -> None:
    spec = {"kind": "place", "target_npc": "npc_guard_01", "location": "loc_tavern"}
    assert evaluate(spec, PROJECTION, 0) is True
    moved = dict(PROJECTION, npc_guard_01={**PROJECTION["npc_guard_01"],
                "position": "loc_backyard"})
    assert evaluate(spec, moved, 0) is False


def test_place_leaf_missing_npc_is_false_not_loud() -> None:
    """An absent entity is a world answer (False), not a shape error —
    the projection is folded state, the pack lint already validated the
    id at load time."""
    spec = {"kind": "place", "target_npc": "npc_absent", "location": "loc_tavern"}
    assert evaluate(spec, PROJECTION, 0) is False


def test_threshold_leaf_at_least_and_at_most() -> None:
    at_least = {
        "kind": "threshold", "target_npc": "npc_guard_01",
        "axis": "suspicion", "comparator": "at_least", "value": 50,
    }
    at_most = {
        "kind": "threshold", "target_npc": "npc_guard_01",
        "axis": "suspicion", "comparator": "at_most", "value": 49,
    }
    assert evaluate(at_least, PROJECTION, 0) is True
    assert evaluate(at_most, PROJECTION, 0) is False


def test_threshold_leaf_non_integer_axis_is_false() -> None:
    """A non-integer or missing axis value never satisfies a threshold
    (the pre-drama-1 law: only int axes compare, bools excluded)."""
    spec = {
        "kind": "threshold", "target_npc": "npc_drunk_01",
        "axis": "suspicion", "comparator": "at_least", "value": -1,
    }
    assert evaluate(spec, PROJECTION, 0) is True  # 0 >= -1
    spec["axis"] = "trust"  # not present on the drunkard
    assert evaluate(spec, PROJECTION, 0) is False


def test_threshold_leaf_unknown_comparator_is_loud() -> None:
    spec = {
        "kind": "threshold", "target_npc": "npc_guard_01",
        "axis": "suspicion", "comparator": "exactly", "value": 50,
    }
    with pytest.raises(ValueError, match="comparator"):
        evaluate(spec, PROJECTION, 0)


def test_pack_trigger_spec_replays_unchanged() -> None:
    """Parity pin: the committed pack's own trigger (the
    possible_document_check threshold leaf) evaluates through the
    grammar exactly as the v0.1 evaluator did — the leaf vocabulary is
    the bottom layer of the grammar, never a second dialect."""
    spec = {
        "kind": "threshold", "target_npc": "npc_guard_01",
        "axis": "suspicion", "value": 50, "comparator": "at_least",
    }
    at_49 = dict(PROJECTION, npc_guard_01={**PROJECTION["npc_guard_01"],
                 "relations.suspicion": 49})
    assert evaluate(spec, at_49, 0) is False
    assert evaluate(spec, PROJECTION, 0) is True


# -- the prop leaf (drama-1: the generalized projection read) -----------------


def test_prop_leaf_orders_numeric_paths() -> None:
    spec = {
        "kind": "prop", "of": "npc_drunk_01", "path": "status.intoxication",
        "comparator": "at_least", "value": 30,
    }
    assert evaluate(spec, PROJECTION, 0) is True
    assert evaluate({**spec, "comparator": "at_most", "value": 30}, PROJECTION, 0) is False


def test_prop_leaf_equals_and_not_equals_read_any_scalar() -> None:
    base = {
        "kind": "prop", "of": "npc_guard_01", "path": "crime_status",
    }
    assert evaluate({**base, "comparator": "equals", "value": "unknown"},
                    PROJECTION, 0) is True
    assert evaluate({**base, "comparator": "not_equals", "value": "suspect"},
                    PROJECTION, 0) is True
    flag = {
        "kind": "prop", "of": "npc_guard_01", "path": "on_duty",
    }
    assert evaluate({**flag, "comparator": "equals", "value": True},
                    PROJECTION, 0) is True


def test_prop_leaf_bool_never_equals_one() -> None:
    """Python's `True == 1` is a conflation, not a fact: a flag is not a
    count. The evaluator guards the type kind before comparing."""
    flag_as_one = {
        "kind": "prop", "of": "npc_guard_01", "path": "on_duty",
        "comparator": "equals", "value": 1,
    }
    assert evaluate(flag_as_one, PROJECTION, 0) is False
    assert evaluate({**flag_as_one, "comparator": "not_equals"}, PROJECTION, 0) is True


def test_prop_leaf_missing_prop_answers_honestly() -> None:
    """A missing prop: not equal to anything (False under equals, True
    under not_equals), never comparable (False under ordering)."""
    base = {
        "kind": "prop", "of": "npc_drunk_01", "path": "status.injury",
    }
    assert evaluate({**base, "comparator": "equals", "value": 0}, PROJECTION, 0) is False
    assert evaluate({**base, "comparator": "not_equals", "value": 0},
                    PROJECTION, 0) is True
    assert evaluate({**base, "comparator": "at_least", "value": 0},
                    PROJECTION, 0) is False


def test_prop_leaf_unknown_comparator_is_loud() -> None:
    spec = {
        "kind": "prop", "of": "npc_guard_01", "path": "status.fatigue",
        "comparator": "roughly", "value": 30,
    }
    with pytest.raises(ValueError, match="prop comparator"):
        evaluate(spec, PROJECTION, 0)


# -- compounds (the Paradox logic blocks, minus the implicit-this footguns) ---


def test_all_is_and() -> None:
    spec = {
        "all": [
            {"kind": "threshold", "target_npc": "npc_guard_01",
             "axis": "suspicion", "comparator": "at_least", "value": 25},
            {"kind": "place", "target_npc": "npc_guard_01",
             "location": "loc_tavern"},
        ]
    }
    assert evaluate(spec, PROJECTION, 0) is True
    moved = dict(PROJECTION, npc_guard_01={**PROJECTION["npc_guard_01"],
                "position": "loc_backyard"})
    assert evaluate(spec, moved, 0) is False


def test_any_is_or() -> None:
    spec = {
        "any": [
            {"kind": "place", "target_npc": "npc_drunk_01",
             "location": "loc_tavern"},  # false
            {"kind": "threshold", "target_npc": "npc_guard_01",
             "axis": "suspicion", "comparator": "at_least", "value": 25},  # true
        ]
    }
    assert evaluate(spec, PROJECTION, 0) is True


def test_not_negates_a_single_inner_spec() -> None:
    spec = {
        "not": {"kind": "place", "target_npc": "npc_guard_01",
                "location": "loc_backyard"},
    }
    assert evaluate(spec, PROJECTION, 0) is True  # the guard is NOT in the yard
    moved = dict(PROJECTION, npc_guard_01={**PROJECTION["npc_guard_01"],
                "position": "loc_backyard"})
    assert evaluate(spec, moved, 0) is False


def test_list_root_is_the_implicit_and() -> None:
    """The Paradox trigger body shape: a bare list of predicates is an
    implicit AND root."""
    spec = [
        {"kind": "time", "tick": 100},
        {"kind": "prop", "of": "npc_guard_01", "path": "crime_status",
         "comparator": "equals", "value": "unknown"},
    ]
    assert evaluate(spec, PROJECTION, 100) is True
    assert evaluate(spec, PROJECTION, 99) is False


def test_compounds_nest_freely() -> None:
    spec = {
        "all": [
            {"any": [
                {"kind": "time", "tick": 720},
                {"not": {"kind": "time", "tick": 360}},
            ]},
            [{"kind": "place", "target_npc": "npc_drunk_01",
              "location": "loc_backyard"}],
        ]
    }
    # any(time>=720, not(time>=360)) = any(True, False) at t=720
    assert evaluate(spec, PROJECTION, 720) is True
    # at t=0: any(False, True) = True; nested list holds → True
    assert evaluate(spec, PROJECTION, 0) is True


def test_empty_all_is_vacuously_true_empty_any_is_false() -> None:
    """Standard empty-AND/empty-OR semantics. The pack lint rejects
    empty lists as dead vocabulary (L1) — the evaluator stays
    mathematically honest either way."""
    assert evaluate({"all": []}, PROJECTION, 0) is True
    assert evaluate({"any": []}, PROJECTION, 0) is False


# -- the loud backstop (unknown/malformed shapes never guess) -----------------


def test_unknown_kind_is_loud() -> None:
    with pytest.raises(ValueError, match="unknown predicate kind"):
        evaluate({"kind": "vibes", "target_npc": "npc_guard_01"}, PROJECTION, 0)


def test_non_object_spec_is_loud() -> None:
    with pytest.raises(ValueError, match="object or a list"):
        evaluate("guard is suspicious", PROJECTION, 0)  # type: ignore[arg-type]


def test_empty_object_is_loud() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        evaluate({}, PROJECTION, 0)


def test_compound_with_extra_keys_is_loud() -> None:
    spec = {
        "all": [{"kind": "time", "tick": 1}],
        "any": [{"kind": "time", "tick": 2}],
    }
    with pytest.raises(ValueError, match="extra keys"):
        evaluate(spec, PROJECTION, 0)


def test_non_integer_leaf_field_is_loud() -> None:
    with pytest.raises(ValueError, match="'tick'"):
        evaluate({"kind": "time", "tick": "soon"}, PROJECTION, 0)
    with pytest.raises(ValueError, match="'value'"):
        evaluate({"kind": "threshold", "target_npc": "npc_guard_01",
                  "axis": "suspicion", "comparator": "at_least",
                  "value": "high"}, PROJECTION, 0)


# -- the closed vocabularies (single owner: core/predicates.py) ---------------


def test_leaf_and_compound_vocabularies_are_closed() -> None:
    assert LEAF_KINDS == ("time", "place", "threshold", "prop")
    assert COMPOUND_KEYS == ("all", "any", "not")
    assert COMPARATORS == ("at_least", "at_most", "equals", "not_equals")
