"""agenda-1 P0 (iter-417) — the drive ticker: the laws, the witness, the
ablation, and the inert arm.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: an NPC's declared personality profile changes its DECISIONS
  measurably — the drive's derived bar fires the attempt while the
  profile's modifier table says the drive matters, and the same corpus
  goes silent when the table zeroes it or the profile is absent.
- Problem: before this row the world's own acts were 10 hand-written
  urgency rows; personality existed as prose (`goal`/`mood`) with no
  runtime reader (iter-415 §3).
- Lens: "this binding is causally live" → the one-knob perturbation of
  the weight table + the empty-profile arm.
- Prism: the committed pack (INERT: block declared, no profile — zero
  draws, zero drives) vs three in-tmp twins of it: BASE (the profile
  armed, the modifier table as declared), FLAT (the same profile, every
  modifier per-cent zeroed — the table says the drive does not matter),
  NO-PROFILE (the key absent).
- Scenario + corpus: the province pack, seed 42, the PC walks to the
  crofts (the active scene) and waits; the winter kin's drive attempts
  `look_around` through the door. No committed fixture is written: the
  witness lives in the tmp twin (PACK_SPEC §8's law), so the canonical
  corpora stay byte-identical (the separate T1 laws remain the oracle).
- Oracle: the canonical events (type/actor/tick of the kin's
  `look_around` attempts); the projection reads; the pack lint's
  refusals of the malformed forms.
- Falsifier: FLAT producing the same attempts as BASE (the table is
  not the cause); NO-PROFILE producing any (the profile is not the
  switch); one tick carrying two attempts (the one-per-NPC budget
  broken); a committed pack arming a drive by itself.
- Expected evidence: BASE ≥ 1 attempt, FLAT 0, NO-PROFILE 0, at most
  one per tick; the committed pack's `drive_specs` empty.
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED at the measured band (seed 42) — the bar's
  formula is unit-pinned too (met measure → 0, unmet → weight × count,
  clamped).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.drives import (
    drive_bar,
    drive_demand,
    drive_intents,
    drive_specs,
    drive_weight,
)
from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.traits import Trait

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
KIN = "npc_winterkin_01"
VERB = "look_around"

PROFILE: dict[str, Any] = {
    "archetype": "the_road_wanderer",
    "axes": {
        "openness": 78,
        "conscientiousness": 28,
        "extraversion": 45,
        "agreeableness": 50,
        "neuroticism": 55,
    },
}

STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "wait", "ticks": 4000},
]


# -- the twin ---------------------------------------------------------------


def _twin(
    tmp_path: Path,
    name: str,
    *,
    profile: dict[str, Any] | None = PROFILE,
    zero_modifiers: bool = False,
    mutate: Any = None,
) -> Path:
    """The committed pack copied into tmp and edited — never a committed
    edit (PACK_SPEC §8: the witness lives in the twin). `profile` arms
    the kin's `psyche`; `zero_modifiers` zeroes every psych modifier
    per-cent (the table's ablation); `mutate` is the malformed forms'
    hook (raises at load, never at run)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    entities = json.loads(
        (target / "entities.json").read_text(encoding="utf-8")
    )
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    for record in entities["npcs"]:
        if record["id"] != KIN:
            continue
        if profile is not None:
            record["psyche"] = json.loads(json.dumps(profile))
    if zero_modifiers:
        for drive in rules["psyche"]["drives"]:
            for modifier in drive.get("modifiers", ()):
                modifier["low_pct"] = 0
                modifier["high_pct"] = 0
    if mutate is not None:
        mutate(rules, entities)
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    return target


def _run(
    pack_dir: Path, tmp_path: Path, name: str
) -> tuple[list[Any], Any]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(
        {
            "name": name,
            "seed": 42,
            "pack": "province_pack@0.1",
            "steps": STEPS,
        }
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, result


def _kin_attempts(events: list[Any]) -> list[Any]:
    return [
        event
        for event in events
        if event.type == VERB and event.actor == KIN
    ]


# -- the inert law ----------------------------------------------------------


def test_the_committed_pack_declares_the_vocabulary_and_arms_two_authored_profiles() -> None:
    """The block is declared (axes / archetypes / distributions / drives),
    and since iter-443 TWO committed npcs carry an AUTHORED profile:
    Garrick (`the_smelter_master`, iter-429, D-281) and Ketta
    (`the_weir_keeper` — the crossing's keeper, whose drive reads the
    stair's wear and offers the OFFICE's mend as the helper act, the
    content arming of quest-1 B). The projection-free parse therefore
    memoizes two specs, in npc declaration order. P1 (iter-418) arms the
    three road travellers with the BORN origin instead: those specs exist
    only against the live projection, and `tests/test_psyche.py` owns that
    half (the ticker's own laws stay this module's)."""
    pack = load_pack(PACK_DIR)
    psyche = pack.rules["psyche"]
    assert [axis["id"] for axis in psyche["axes"]] == [
        "openness", "conscientiousness", "extraversion",
        "agreeableness", "neuroticism",
    ]
    assert {a["id"] for a in psyche["archetypes"]} == {
        "the_smelter_master", "the_road_wanderer", "the_weir_keeper",
    }
    assert {d["id"] for d in psyche["drives"]} == {
        "fire_the_year_cut", "scan_the_road", "keep_the_crossing",
        "see_the_debt_paid",
    }
    assert [(spec.npc, spec.drive) for spec in drive_specs(pack)] == [
        ("npc_weirkeeper_01", "keep_the_crossing"),
        ("npc_smelter_01", "fire_the_year_cut"),
        ("npc_smelter_01", "see_the_debt_paid"),
    ]


def test_the_probe_id_names_the_probe_not_its_ordinal(tmp_path: Path) -> None:
    """roster-2 (iter-434, KI#116): a probe's `cause_intent` is
    `drive_<npc>_<drive>` — the probe's own identity, never its position in
    the walk. The witness: a NEW drive row inserted FIRST for the first npc
    (the smelter) used to renumber every later probe (`drive_0000 →
    drive_0001`, measured iter-429); under the content-addressed form the
    existing labels are byte-identical. Uniqueness is per probe by
    construction — the ids repeat every beat and the OCC snapshot FIFO
    pairs same-id enqueues in push order (`core/loop.py:449-461`), so two
    live probes must never share one."""
    base = load_pack(PACK_DIR)
    base_ids = {
        (spec.npc, spec.drive): spec.probe.id
        for spec in drive_specs(base)
    }
    assert base_ids == {
        ("npc_weirkeeper_01", "keep_the_crossing"):
            "drive_npc_weirkeeper_01_keep_the_crossing",
        ("npc_smelter_01", "fire_the_year_cut"):
            "drive_npc_smelter_01_fire_the_year_cut",
        ("npc_smelter_01", "see_the_debt_paid"):
            "drive_npc_smelter_01_see_the_debt_paid",
    }

    twin = tmp_path / "shifted"
    shutil.copytree(PACK_DIR, twin)
    path = twin / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    rules["psyche"]["drives"].insert(
        0,
        {
            "id": "a_named_second_drive",
            "archetypes": ["the_smelter_master"],
            "base": 1,
            "max_per_beat": 1,
            "verb": "look_around",
        },
    )
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    shifted = load_pack(twin)
    after = {
        (spec.npc, spec.drive): spec.probe.id
        for spec in drive_specs(shifted)
    }
    for key, label in base_ids.items():
        assert after[key] == label, "an inserted drive row renamed a probe"
    assert after[("npc_smelter_01", "a_named_second_drive")] == (
        "drive_npc_smelter_01_a_named_second_drive"
    )


# -- the parse and the bar --------------------------------------------------


def test_the_parse_resolves_the_profile_weight_and_the_bar(
    tmp_path: Path,
) -> None:
    """The weight is `base × the modifier's per-cent // 100` at the
    profile's own band (openness 78 ≥ 70 → 200 % → 20 × 200 // 100 = 40);
    the bar is the weight times the unmet count while the measure fails,
    clamped at `max_per_beat`."""
    twin = _twin(tmp_path, "armed")
    pack = load_pack(twin)
    specs = drive_specs(pack)
    assert [(spec.npc, spec.drive) for spec in specs] == [
        ("npc_weirkeeper_01", "keep_the_crossing"),
        ("npc_smelter_01", "fire_the_year_cut"),  # the committed authored carriers
        ("npc_smelter_01", "see_the_debt_paid"),
        (KIN, "scan_the_road"),
    ]
    spec = specs[3]  # the twin's own authored profile
    assert drive_weight(spec, pack, initial_projection(pack.entities)) == 40  # 20 * 200 // 100
    assert spec.max_per_beat == 50
    assert spec.verb == VERB
    bar = drive_bar(spec, pack, initial_projection(pack.entities))
    assert bar == 40  # one unmet condition (the belief is absent)


def test_the_bar_is_zero_when_the_measure_is_met(tmp_path: Path) -> None:
    """The continuity law: a met goal stops pushing. The measure reads the
    EVENT-DRIVEN fold (`trait_held`, iter-439): the caller passes the fold
    read it took, and a held belief collapses the bar to 0 — while the same
    drive without it stays at its weight."""
    twin = _twin(tmp_path, "met")
    pack = load_pack(twin)
    spec = drive_specs(pack)[3]
    projection = initial_projection(pack.entities)
    held = (Trait(who=spec.npc, token="the_road_known", sources=("ev_0001",)),)
    assert drive_bar(spec, pack, projection) == 40
    assert drive_bar(spec, pack, projection, traits=held) == 0


def test_the_measure_fold_is_a_declared_demand() -> None:
    """The E04 demand twin (iter-439): the fold a measure reads must be
    computed by the beat walk, or the ticker would read an empty tuple and
    the goal could never complete (the silent-dead-gate trap)."""
    pack = load_pack(PACK_DIR)
    assert "trait_held" in drive_demand(pack)


# -- the witness and its two ablations --------------------------------------


def test_the_profile_drives_the_decision_and_the_table_is_the_cause(
    tmp_path: Path,
) -> None:
    """BASE (the profile + the declared table) produces the kin's
    attempts; FLAT (the same profile, every modifier per-cent zeroed)
    produces none — the declared table, not the mere presence of a
    profile, is the cause; NO-PROFILE (the key absent) produces none —
    the profile is the switch. At most one attempt per NPC per tick (the
    one-per-NPC budget)."""
    base_events, _ = _run(_twin(tmp_path, "base"), tmp_path, "base.jsonl")
    flat_events, _ = _run(
        _twin(tmp_path, "flat", zero_modifiers=True),
        tmp_path,
        "flat.jsonl",
    )
    none_events, _ = _run(
        _twin(tmp_path, "none", profile=None), tmp_path, "none.jsonl"
    )
    base = _kin_attempts(base_events)
    flat = _kin_attempts(flat_events)
    none = _kin_attempts(none_events)
    assert base, "the armed profile must attempt on the horizon (empty-ablation rule)"
    assert flat == [], "the zeroed table must silence the drive"
    assert none == [], "an unprofiled NPC runs no drive"


def test_at_most_one_intent_per_npc_per_walk() -> None:
    """The one-per-NPC budget (one decision a beat, not a burst): two
    drives of the same NPC that both roll under their bars yield ONE
    intent — the stronger bar's; a tie keeps the declaration order. The
    walk's own law, unit-pinned (a stub bank returns the same roll for
    both streams)."""
    npc = "npc_x"
    strong = _spec(npc, "strong", 50)
    weak = _spec(npc, "weak", 30)
    projection = {npc: {"position": "loc_a"}}

    class _Bank:
        def family_rolls(self, streams: Any, lo: int, hi: int) -> list[int]:
            return [10 for _ in streams]

    intents = drive_intents(
        None, projection, _Bank(), specs=(strong, weak)
    )
    assert intents == [strong.probe]
    assert drive_intents(None, projection, _Bank(), specs=(weak, strong)) == [
        strong.probe
    ]  # the stronger bar wins regardless of position
    assert drive_intents(None, projection, _Bank(), specs=(strong,)) == [
        strong.probe
    ]


def test_the_walk_falls_silent_once_the_belief_holds() -> None:
    """The goal completes on a BELIEF (iter-439, `drivegoals-1`): with the
    trait the measure reads HELD, the walk enqueues nothing (bar 0, the
    continuity law) while the same spec without it enqueues its intent —
    the bar's fold is the caller's own read, never a second one."""
    from dataclasses import replace

    pack = load_pack(PACK_DIR)
    npc = "npc_x"
    spec = replace(
        _spec(npc, "believer", 100),
        measure=(
            {"noun": "actor", "test": "trait_held", "token": "the_road_known"},
        ),
    )
    projection = {npc: {"position": "loc_a"}}
    held = (Trait(who=npc, token="the_road_known", sources=("ev_0001",)),)

    class _Bank:
        def family_rolls(self, streams: Any, lo: int, hi: int) -> list[int]:
            return [1 for _ in streams]

    assert drive_intents(pack, projection, _Bank(), traits=held, specs=(spec,)) == []
    assert drive_intents(pack, projection, _Bank(), specs=(spec,)) == [spec.probe]


def _spec(npc: str, drive: str, weight: int) -> Any:
    """A hand-built spec for the walk's unit law (no measure — the bar is
    the weight, the pack is never read)."""
    from core.drives import DriveSpec
    from core.intent import IntentData

    return DriveSpec(
        npc=npc,
        drive=drive,
        verb="look_around",
        target=None,
        fields={},
        measure=(),
        need=None,
        base=weight,
        modifiers=(),
        max_per_beat=100,
        stream=f"drive:{npc}:{drive}",
        probe=IntentData(
            id=f"drive_{drive}",
            kind="look_around",
            actor=npc,
            target=None,
            fields={},
            based_on_event_seq=0,
        ),
    )


# -- the lint's refusals ----------------------------------------------------


def test_the_lint_refuses_the_malformed_forms(tmp_path: Path) -> None:
    """Six dead shapes, each refused at LOAD (never a silent ignore):
    a CLOCKED test in a measure (the quiet-beat skip's fence), a STATIC one
    (the dead measure — `deadmeasure-1`), an unknown block key, an
    incomplete profile, a third extreme axis, and a drive worded on an
    undeclared archetype. The EVENT-DRIVEN fold is the legal middle
    (iter-439): the committed pack's own `trait_held` measure loads."""

    def windowed(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["drives"][0]["measure"] = [
            {"noun": "actor", "test": "leverage_over", "who": "target"}
        ]

    def static(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["drives"][1]["measure"] = [
            {"noun": "actor", "test": "flag", "flag": "the_road_known"}
        ]

    def unknown_key(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["personality"] = {}

    def incomplete_profile(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == KIN:
                record["psyche"]["axes"].pop("openness")

    def third_extreme(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == KIN:
                record["psyche"]["axes"]["neuroticism"] = 90

    def unknown_archetype(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["drives"][0]["archetypes"] = ["the_ghost"]

    for name, mutate in (
        ("windowed", windowed),
        ("static", static),
        ("unknown-key", unknown_key),
        ("incomplete", incomplete_profile),
        ("extremes", third_extreme),
        ("archetype", unknown_archetype),
    ):
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate=mutate))
