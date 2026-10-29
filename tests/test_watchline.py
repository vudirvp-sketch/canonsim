"""watchline — the watch's own round (wt-fill-1's U3, iter-405).

The anchor's `ANCHOR_REGION.md` §4 Actors row named Osgar and Ferra with no
surface holding their decision: the `patrol` verb existed as a bare story
beat (wait resolver, no knowledge, no holder) and the garrison's group arm
read GROUP fear at a bar the committed corpora never cross (MEASURED: the
institutional run's alarm spikes the location's occupants; the pair's own
fear never reaches 40 — zero patrols in every committed corpus).

This unit arms the missing holder as the committed substrate's own causal
form — a DIRECTOR HOOK with an explicit trigger:

- SEEDED by the steal-failure family (`pickpocket_failed` carries the tag
  beside the rest of the watcher hooks — the evidence event is the seed,
  D-005's law);
- RELEASED when the SERGEANT'S OWN suspicion over pc_01 crosses 50 (the
  `prop` predicate reads the live `pair.pc_01.suspicion` fold — the same
  read the committed `sergeant_wary_of_pc` weight modifier makes);
- the release intent is the `patrol` verb ITSELF, carrying the target — the
  round walks TOWARD the suspect, the `garrison_patrols` line rendering at
  the sergeant's location;
- `first_time_only`: once per evidence chain — a standing suspect is the
  document-check family's business (the arrest ladder), never a walking
  beat;
- the threat channel owns the release (the institutional arm).

The measured walk (`tests/playscripts/province_watchline.json`, the
institutional family's own script, seed 2): the arson alarm at the keep
(t=834), the failed pickpocket at Malby seeding the hook with the rest
(t=1797, suspicion 55), the rotation's beat landing the release at t=2899 —
ONE `garrison_patrols` event, actor the sergeant, provenance
`director_osgar_walks_the_suspect`, its semantic origin stamped
1800 (B3's provenance law).

The two roads, and where they stand now:

1. the URGENCY-POST form was refused by the STORAGE SPLIT:
   `relation_at_least` read `relations.<axis>` from the projection while
   the crime write landed on `pair.<with>.suspicion` — two storages that
   never met (MEASURED at iter-405: suspicion 85 on the pair key,
   `relations.suspicion` None, the gate never passed; the record-reading
   tests `field_nonempty`/`flag` read the SEEDED record and were
   always-armed, not decisions). **CLOSED by substrate-1 C, iter-411**:
   the gate reads BOTH stores with a named precedence (the pair overrides
   the seeded axis; the gate's `with` noun names the other party), so the
   post now fires on the sergeant's own suspicion — and stays silent
   above the bar the walk never reaches (the two arms below).
2. the OPTION-only form still fails: an option's `trigger` is an
   availability gate, not a causal release — a hook with `trigger: None`
   is stagnation-only and never fires on its own (MEASURED: zero releases
   in the same walk). That split stands: the hook form is the release
   instrument, by design.

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the watch pair's decision — the round walked toward the suspect —
  is a live causal consequence of the evidence they hold, over committed
  primitives only (the hook buffer, the prop predicate, the patrol verb),
  with the canonical corpus byte-untouched and zero core.
- Lens(es): the changed-next-decision unit (evidence crossing 50 arms the
  walk; below it the sergeant only stares); the boundary lens (the two
  refused forms above — the storage split and the gate-vs-release split —
  are substrate facts, named not faked).
- Prism: the institutional band (`province_watchline`, seed 2) + the
  canonical day-scale corpus as the inertness oracle.
- Oracle: the released event's own provenance (cause_hook
  `osgar_walks_the_suspect`), never a recomputed guess.
- Falsifier: a patrol without the hook's provenance, a release below the
  50 bar, a second release in one evidence chain, or one byte of movement
  in the canonical corpus refutes it.
- Epistemic class: FACT at the measured band.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
OSGAR = "npc_sergeant_01"
FERRA = "npc_corporal_01"
HOOK = "osgar_walks_the_suspect"
BAR = 50
SEED = 2


def _run_committed(tmp_path: Path, log_name: str) -> tuple[list, object]:
    script = load_playscript(REPO / "tests" / "playscripts" / "province_watchline.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / log_name
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events, sim


def _patrols(events: list) -> list:
    return [e for e in events if e.type == "garrison_patrols"]


# -- (1) the armed census --------------------------------------------------------


def test_the_armed_census() -> None:
    """The unit's named elements as committed pack data: the hook, its
    trigger, its channel, its seed site, and the bare verb it releases."""
    pack = load_pack(PACK_DIR)
    hook = pack.rules["director"]["hooks"][HOOK]
    assert hook["target_npc"] == OSGAR
    assert hook["intent"] == {"kind": "patrol", "target": "pc_01"}
    assert hook["trigger"] == {
        "kind": "prop", "of": OSGAR, "path": "pair.pc_01.suspicion",
        "value": BAR, "comparator": "at_least",
    }
    assert hook["channel"] == "threat"
    assert hook["first_time_only"] is True
    # the seed site: the steal-failure family carries the tag
    steal = next(a for a in pack.data["actions.json"]["actions"]
                 if a["intent"] == "steal")
    assert HOOK in steal["hooks"]["failure"]
    # the bare verb the hook releases (the committed story beat)
    patrol = next(a for a in pack.data["actions.json"]["actions"]
                  if a["intent"] == "patrol")
    assert patrol["events"] == {"success": "garrison_patrols"}


# -- (2) the walk is causal ------------------------------------------------------


def test_the_round_walks_when_the_evidence_crosses_the_bar(tmp_path: Path) -> None:
    """The measured walk: the failed pickpocket seeds the hook (suspicion
    55 over the sergeant), the next rotation beat releases ONE patrol
    toward the suspect, and the event's own provenance names the hook —
    the decision's holder, never a guess."""
    events, sim = _run_committed(tmp_path, "watch.jsonl")
    patrols = _patrols(events)
    assert len(patrols) == 1, "one round per evidence chain"
    walk = patrols[0]
    assert walk.actor == OSGAR
    assert walk.provenance["cause_hook"] == HOOK
    # the release is the evidence's own consequence: suspicion crossed the bar
    assert sim.projection[OSGAR]["pair.pc_01.suspicion"] >= BAR
    # the seed: the failed pickpocket's event carries the tag
    seeded = [e for e in events if e.type == "pickpocket_failed"]
    assert seeded and HOOK in seeded[0].hooks


def test_no_round_below_the_bar(tmp_path: Path) -> None:
    """The decision's edge: a quiet day (no crime family, suspicion seeded
    0) releases NOTHING — below the bar the sergeant only stares (the
    committed sergeant_wary_of_pc's quiet options), never walks."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / "quiet.jsonl"
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "quiet", "seed": SEED, "pack": "province_pack@0.1",
        "steps": [{"intent": "wait", "ticks": 1500}],
    })
    _, events = read_log(log, SCHEMA)
    assert _patrols(events) == []
    assert sim.projection[OSGAR]["pair.pc_01.suspicion"] == 0


# -- (3) the two refused forms, measured ------------------------------------------


def _twin_with_post(
    tmp_path: Path, name: str, value: int,
) -> tuple[Path, Path]:
    """The crafted institutional twin: the committed pack plus ONE urgency
    post whose gate is `relation_at_least` over the suspicion axis. The
    same walk runs it twice: at a bar the crime write crosses, and at a
    bar it never does (the discriminator — a real decision, never an
    always-armed post)."""
    import shutil

    tw = tmp_path / name
    tw.mkdir()
    for fname in ("rules.json", "entities.json", "actions.json", "templates.json"):
        shutil.copy(PACK_DIR / fname, tw / fname)
    rules = json.loads((tw / "rules.json").read_text(encoding="utf-8"))
    rules["urgencies"]["entries"].append({
        "npc": OSGAR, "probability_per_beat": 100,
        "intent": {"kind": "patrol", "target": "pc_01"},
        "requires": [{"noun": "actor", "test": "relation_at_least",
                      "with": "target", "axis": "suspicion", "value": value}],
        "notes": "the watch post: the sergeant's own suspicion decides",
    })
    (tw / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return tw, REPO / "tests" / "playscripts" / "province_watchline.json"


def test_the_urgency_post_now_reads_the_pair_store(tmp_path: Path) -> None:
    """ROAD 1, CLOSED (substrate-1 C, iter-411). This witness used to
    prove the SPLIT: `relation_at_least` read `relations.<axis>` while the
    crime write landed on `pair.<with>.suspicion`, so the post never
    fired. The gate now reads BOTH stores with a named precedence (the
    pair overrides the seeded axis), so the same crafted twin releases
    the urgency round — the sergeant's OWN suspicion, the value the
    dial reads, decides the walk."""
    tw, script_path = _twin_with_post(tmp_path, "post", value=1)
    crafted = load_pack(tw)

    script = load_playscript(script_path)
    log = tmp_path / "post.jsonl"
    sim = Simulator(crafted, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)

    # The pair store carries the suspicion; the seeded axis never exists —
    # so a passing gate can ONLY have read the pair (the exact inverse of
    # the old refusal).
    assert sim.projection[OSGAR]["pair.pc_01.suspicion"] >= BAR
    assert sim.projection[OSGAR].get("relations.suspicion") is None

    hook_walks = [e for e in _patrols(events)
                  if e.provenance.get("cause_hook") == HOOK]
    urgency_walks = [e for e in _patrols(events)
                     if e.provenance.get("cause_hook") is None
                     and str(e.provenance.get("cause_intent", "")).startswith("urgency")]
    assert len(hook_walks) == 1, "the hook's own round still walks once"
    assert urgency_walks, "the pair store now feeds the relation gate"


def test_the_urgency_post_stays_silent_above_the_reached_suspicion(
    tmp_path: Path,
) -> None:
    """The discriminator: the same post with a bar the walk never crosses
    releases NOTHING — the gate is a live decision over the pair store,
    never an always-armed post (the field-reading forms' own defect,
    measured at iter-405)."""
    tw, script_path = _twin_with_post(tmp_path, "high", value=999)
    crafted = load_pack(tw)

    script = load_playscript(script_path)
    log = tmp_path / "high.jsonl"
    sim = Simulator(crafted, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)

    assert sim.projection[OSGAR]["pair.pc_01.suspicion"] >= BAR
    urgency_walks = [e for e in _patrols(events)
                     if e.provenance.get("cause_hook") is None
                     and str(e.provenance.get("cause_intent", "")).startswith("urgency")]
    assert urgency_walks == [], "below the bar the post never fires"


def test_the_option_form_is_an_availability_gate_never_a_release(
    tmp_path: Path,
) -> None:
    """ROAD 2, refused: an option's `trigger` gates AVAILABILITY, not
    release — a hook with `trigger: None` is stagnation-only and never
    fires on its own. The crafted twin (the wary round as an option on the
    committed sergeant hook, first_time_only off) releases ZERO patrols on
    the same walk."""
    import shutil

    tw = tmp_path / "optform"
    tw.mkdir()
    for name in ("rules.json", "entities.json", "actions.json", "templates.json"):
        shutil.copy(PACK_DIR / name, tw / name)
    rules = json.loads((tw / "rules.json").read_text(encoding="utf-8"))
    wary = rules["director"]["hooks"]["sergeant_wary_of_pc"]
    wary["first_time_only"] = False
    wary["options"].append({
        "weight": {"base": 5, "modifiers": []},
        "intent": {"kind": "patrol", "target": "pc_01"},
        "notes": "the refused form: an option is never a causal release",
    })
    # the hook form removed everywhere it is named (the lint refuses a tag
    # whose hook is gone: the seeded consequence must be declared)
    wary["notes"] = wary["notes"] + " (probe: the option form alone)"
    del rules["director"]["hooks"][HOOK]
    actions = json.loads((tw / "actions.json").read_text(encoding="utf-8"))
    for x in actions["actions"]:
        if x["intent"] == "steal":
            x["hooks"]["failure"] = [
                t for t in x["hooks"]["failure"] if t != HOOK]
    (tw / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8")
    (tw / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    crafted = load_pack(tw)

    script = load_playscript(REPO / "tests" / "playscripts" / "province_watchline.json")
    log = tmp_path / "optform.jsonl"
    sim = Simulator(crafted, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    assert _patrols(events) == [], "no hook-level trigger, no causal release"


# -- (4) the corpus law and the fingerprint --------------------------------------


def test_the_canonical_corpus_is_untouched(tmp_path: Path) -> None:
    """INERT-FIRST (`PACK_SPEC` §9.1): the day-scale smoke run is
    byte-identical to the committed golden — the hook seeds only on the
    crime family's failure, which the smoke script never commits."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    Simulator(pack, script["seed"], log, SCHEMA, commit="0000000").run_playscript(script)
    assert log.read_bytes() == (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl").read_bytes()


def test_the_walk_is_byte_identical_across_twins(tmp_path: Path) -> None:
    """INV-2: the same script twice, the same bytes; fingerprints agree."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_watchline.json")
    pack = load_pack(PACK_DIR)
    arms = []
    for name in ("w_a.jsonl", "w_b.jsonl"):
        log = tmp_path / name
        sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
        result = sim.run_playscript(script)
        arms.append((result.fingerprint, log.read_bytes()))
    assert arms[0][1] == arms[1][1]
    assert arms[0][0] == arms[1][0]
