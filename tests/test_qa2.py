"""qa2 — the KI#88/#89 lint-side closures (iter-169, the owner's
«проработай открытые в прошлой итерации ki и все связанное, нужно
доделать все с технической частью» call over the two holes qa-1 opened
and routed): the load-time halves of the two schema-surface holes the
type-discipline audit made loud — the runtime asserts landed with
iter-168 stay as backstops, the pack lint now refuses the malformed
shapes BEFORE the pack ever reaches the simulation.

The claim packet (TEST_PLAN §9):

- Claim: the two KIs' lint-side residues are closed at load — KI#89 (the
  five record-reading tests' directly-indexed keys: flag / field /
  values on carries_flagged, flagged_accessible, field_in,
  field_nonempty, has_field — the iter-45 leverage `who` family) via ONE
  shared lint row served by every `requires` declaration site (the
  action canon, the texture block, the urgency beat gate, the faction
  gate); KI#88 (both arms) via the on_action actor vocabulary narrowed
  to `world | source_actor` (the reaction event's actor is a
  schema-required string — `source_target` drafts None on a targetless
  source) and the target-sourced check row (the action must pin the
  intent's target with a target-noun precondition — the door's own
  `needs_target` predicate, one source, two readers).
- Lens(es): the KI#15 family lens (refuse at load what would crash —
  or silently nonsense-roll — at completion); the single-owner lens
  (the vocabulary splits live in `core/onaction.py`, the predicate in
  `core/intent.py` — the lint reads, never restates).
- Prism: linted pack variants over the committed tavern and pressure
  packs — one mutation per refusal row, plus the wiring arms proving
  the shared row fires at the beat-gate, texture and faction sites.
- Oracle: `PackError` message fragments naming the refused key and the
  family law; the committed packs themselves still load (the
  smoke/e2e suites own that half).
- Falsifier: a malformed cond loading silently; the refusal firing at
  only some declaration sites; a target-sourced check action without a
  target pin loading and rolling against the base skill at the door.
- Expected evidence: each mutation refused with its named key; the
  on_action actor row refusing `source_target` with the schema
  rationale; the narrowed actor vocabulary listed as
  `['world', 'source_actor']`.
- Observed evidence: CONFIRMED — every row refuses at load; the five
  committed packs load untouched (the golden T1 corpus byte-identical).
- Epistemic class: structural, deterministic (pure load-time checks).
- Disposition: CONFIRMED (the `flag` test itself — unused by every
  committed pack — stays outside the row set exactly as the KI scoped
  it; its twin hole is the owner's call, recorded not routed).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]


def _pack_copy(tmp_path: Path, pack: str) -> Path:
    target = tmp_path / f"pack_{pack}"
    shutil.copytree(REPO / "content" / pack, target)
    return target


def _actions_doc(target: Path) -> dict[str, Any]:
    return json.loads((target / "actions.json").read_text(encoding="utf-8"))


def _save_actions_doc(target: Path, doc: dict[str, Any]) -> None:
    (target / "actions.json").write_text(
        json.dumps(doc, indent=2), encoding="utf-8"
    )


def _cond_of(actions: list[dict[str, Any]], intent: str, test: str) -> dict[str, Any]:
    action = next(a for a in actions if a["intent"] == intent)
    return next(c for c in action["requires"] if c.get("test") == test)


# -- KI#89: the five presence rows (the canon actions site) -------------------


@pytest.mark.parametrize(
    ("intent", "test", "key"),
    [
        ("steal", "carries_flagged", "flag"),
        ("arson", "flagged_accessible", "flag"),
        ("arson", "field_in", "field"),
        ("arson", "field_in", "values"),
        ("arson", "field_nonempty", "field"),
        ("use", "has_field", "field"),
    ],
)
def test_ki89_requires_the_directly_indexed_keys(
    tmp_path: Path, intent: str, test: str, key: str
) -> None:
    """A cond of the five record-reading tests without its named key is
    refused at load — the door subscripts `cond[key]`, so a missing key
    KeyErrors mid-run (the iter-45 leverage `who` family)."""
    target = _pack_copy(tmp_path, "tavern_pack")
    doc = _actions_doc(target)
    _cond_of(doc["actions"], intent, test).pop(key)
    _save_actions_doc(target, doc)

    with pytest.raises(PackError, match=f"requires '{key}'"):
        load_pack(target)


def test_ki89_refuses_an_empty_flag_name(tmp_path: Path) -> None:
    """The string arm's full row: an empty flag name is dead vocabulary
    (no pack field is named "") — refused with the same message."""
    target = _pack_copy(tmp_path, "tavern_pack")
    doc = _actions_doc(target)
    _cond_of(doc["actions"], "steal", "carries_flagged")["flag"] = ""
    _save_actions_doc(target, doc)

    with pytest.raises(PackError, match="requires 'flag'"):
        load_pack(target)


def test_ki89_refuses_an_empty_field_in_values(tmp_path: Path) -> None:
    """The list arm's full row: an empty `values` set is dead vocabulary
    — the gate can never pass."""
    target = _pack_copy(tmp_path, "tavern_pack")
    doc = _actions_doc(target)
    _cond_of(doc["actions"], "arson", "field_in")["values"] = []
    _save_actions_doc(target, doc)

    with pytest.raises(PackError, match="dead vocabulary"):
        load_pack(target)


# -- KI#89: the shared row's other declaration sites --------------------------


def test_ki89_refuses_at_the_urgency_beat_gate(tmp_path: Path) -> None:
    """The same cond shape declared in an urgency entry's `requires` is
    refused identically — the beat gate runs the same evaluator, a
    missing key would KeyError at the beat."""
    target = _pack_copy(tmp_path, "tavern_pack")
    path = target / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    entry = next(
        e
        for e in rules["urgencies"]["entries"]
        if any(
            c.get("test") == "flagged_accessible"
            for c in e.get("requires", ())
        )
    )
    cond = next(
        c for c in entry["requires"] if c.get("test") == "flagged_accessible"
    )
    cond.pop("flag")
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    with pytest.raises(PackError, match="requires 'flag'"):
        load_pack(target)


def test_ki89_refuses_at_the_texture_block(tmp_path: Path) -> None:
    """The texture path's `requires` ride the same row — the door
    evaluates them in place of the canon list."""
    target = _pack_copy(tmp_path, "tavern_pack")
    doc = _actions_doc(target)
    take = next(a for a in doc["actions"] if a["intent"] == "take")
    take["texture"]["requires"].append(
        {"noun": "actor", "test": "carries_flagged"}
    )
    _save_actions_doc(target, doc)

    with pytest.raises(PackError, match="requires 'flag'"):
        load_pack(target)


def test_ki89_refuses_at_the_faction_gate(tmp_path: Path) -> None:
    """The faction entry's `requires` ride the same row — the faction
    gate runs the evaluator against the beat-tick reads."""
    target = _pack_copy(tmp_path, "pressure_pack")
    path = target / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    entry = next(
        e
        for e in rules["factions"]["entries"]
        if e.get("requires")
    )
    entry["requires"].append(
        {"noun": "target", "test": "field_in", "field": "flammability"}
    )
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    with pytest.raises(PackError, match="requires 'values'"):
        load_pack(target)


# -- KI#88 arm 1: the on_action actor vocabulary -------------------------------


def test_ki88_refuses_source_target_as_the_reaction_actor(tmp_path: Path) -> None:
    """The reaction event's actor is a schema-required string; a
    targetless source would draft None — `actor: source_target` is
    refused at load with the rationale (the runtime assert stays the
    programmatic backstop)."""
    target = _pack_copy(tmp_path, "tavern_pack")
    path = target / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    rules["on_action"]["document_check"][0]["actor"] = "source_target"
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    with pytest.raises(PackError, match="may not be 'source_target'"):
        load_pack(target)


def test_ki88_the_actor_vocabulary_is_narrowed(tmp_path: Path) -> None:
    """The actor-side declaration vocabulary is `world | source_actor`
    (ACTOR_KEYS, owned by core/onaction.py) — a typo'd actor value is
    refused against the NARROWED list, not the resolution triple."""
    target = _pack_copy(tmp_path, "tavern_pack")
    path = target / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    rules["on_action"]["document_check"][0]["actor"] = "source_actr"
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    with pytest.raises(
        PackError, match=r"must be one of \['world', 'source_actor'\]"
    ):
        load_pack(target)


# -- KI#88 arm 2: the target-sourced check row ---------------------------------


def test_ki88_a_target_sourced_check_must_pin_the_target(tmp_path: Path) -> None:
    """A check kind defending from the target builds its defender total
    from the intent's target — the door demands one only when a
    precondition references the noun. Without the pin a targetless
    intent would reach the check and roll against the base skill (the
    silent nonsense roll); refused at load instead."""
    target = _pack_copy(tmp_path, "tavern_pack")
    doc = _actions_doc(target)
    steal = next(a for a in doc["actions"] if a["intent"] == "steal")
    steal["requires"] = [{"noun": "actor", "test": "kind", "is": "npc"}]
    _save_actions_doc(target, doc)

    with pytest.raises(PackError, match="defends from the target"):
        load_pack(target)


def test_ki88_a_pinned_target_sourced_check_loads(tmp_path: Path) -> None:
    """The row's negative arm: the committed shape — a target-sourced
    check whose action pins the target with a target-noun precondition —
    loads (the door then demands the target; the five committed packs
    carry exactly this shape)."""
    target = _pack_copy(tmp_path, "tavern_pack")
    pack = load_pack(target)
    assert pack.name_version == "tavern_pack@0.1"
