"""maintenance — the guild's upkeep office (wt-fill-1's U2, iter-405).

The anchor's `ANCHOR_REGION.md` §6.2 question: who repairs the weir, the
stair, the troughs? The function-loss arbiter's answer, made data: the
guild's paper prices MONEY, the crossing's custom prices the SEASON, and
nothing in the pack read the STAIR'S CONDITION or paid to restore it. This
unit arms that missing function and nothing else — no axis, no threshold, no
institutional door of its own (§6.2's anti-council check).

The cycle (ALL PACK DATA, ZERO CORE, the macro year):

1. `the_stair_wears` — a bounded source on the stair: +2 wear a year, CAPACITY
   8. The year's water works whether or not anyone watches; at the cap the
   flow falls SILENT (the every-miss form) — the recorded infrastructure debt.
2. `mend_the_stair` — the office's door: the guild's own hand walks to the
   stair and pays from the chest. Inputs wear 2 off the crossing + coin 3 out
   of Malby's ledger; output coin 1 back to the keeper for the timbers'
   setting (the labour's wage — the office pays for work, never for a paper).
3. The co-present learn `the_stair_mended` — the mending public.

HONEST RESIDUE (named, never patched): the `step` account is NOT touched. Its
ladder (three the working head, four the rise — the flood's committed line,
never a setting) has NO `account_at_most` gate in the substrate, so a mend
that pushed the head past three would read as the flood. The timbers' standing
head therefore stays the keeper's own door (`set_the_timbers`), and the
office's mending rides the WEAR's clearance. The at_most gap is the unit's
boundary and the owner's substrate call.

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the guild's maintenance office performs a function no committed
  mechanism performed — the infrastructure's wear accrues unread, saturates
  at its declared bound, and is cleared only by an institutional payment made
  in person — with the canonical corpus byte-untouched and zero core.
- Lens(es): the changed-next-decision unit (the office's visit is the only
  reader of a condition nobody else prices); the boundary lens (the step
  ladder's at_most gap, named rather than faked).
- Prism: the macro-year band (`province_maintenance`, five crossings + the
  office's walk) and the canonical day-scale corpus as the inertness oracle.
- Oracle: the account events' own state changes; the ablation arm (the door
  removed — the wear then saturates and clears never).
- Falsifier: a wear level above the cap, a mend without the actor present, a
  negative stock, a change to the `step` account, or one byte of movement in
  the canonical corpus refutes it.
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
STAIR = "loc_weirstair"
CHEST = "loc_malby"
KEEPER = "npc_weirkeeper_01"
OFFICE = "npc_marketmistress_01"
WEAR_CAP = 8
WEAR_STEP = 2
MEND_COIN = 3
MEND_WAGE = 1
CROSSINGS = 5
TICK_YEAR = 518_400


def _run_committed(tmp_path: Path, log_name: str) -> tuple[list, object]:
    script = load_playscript(REPO / "tests" / "playscripts" / "province_maintenance.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / log_name
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events, sim


def _trail(events: list, entity: str, kind: str) -> list:
    return [
        (e.t, e.type, ch.from_, ch.to_)
        for e in events
        for ch in e.state_changes
        if ch.entity == entity and ch.prop.endswith(kind)
    ]


# -- (1) the armed census --------------------------------------------------------


def test_the_armed_census() -> None:
    """The unit's named elements as committed pack data: the kind, the
    bounded flow, the recipe, the door and its two holder gates, the
    glosses and the token."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    assert "wear" in economy["accounts"]
    stair = next(loc for loc in pack.entities["locations"] if loc["id"] == STAIR)
    assert stair["accounts"] == {"wear": 0}  # the genesis: no wear yet
    assert [
        (f["verb"], f["kind"], f["to"], f["amount"], f["capacity"])
        for f in economy["flows"] if f["id"] == "the_stair_wears"
    ] == [("source", "wear", STAIR, WEAR_STEP, WEAR_CAP)]
    # the recipe: the condition and the money in, the wage out
    assert [r for r in economy["recipes"] if r["id"] == "the_mend"] == [{
        "id": "the_mend",
        "inputs": [
            {"holder": STAIR, "kind": "wear", "amount": WEAR_STEP},
            {"holder": CHEST, "kind": "coin", "amount": MEND_COIN},
        ],
        "outputs": [{"holder": KEEPER, "kind": "coin", "amount": MEND_WAGE}],
    }]
    door = next(
        a for a in pack.data["actions.json"]["actions"]
        if a["intent"] == "mend_the_stair"
    )
    assert door["resolver"] == "account"
    assert door["account"] == {"verb": "convert", "recipe": "the_mend"}
    assert door["events"] == {"success": "account_converted"}
    # both input legs carry their holder-form solvency gate (the lint's law)
    gates = {
        (c.get("holder"), c.get("kind"), c.get("value"))
        for c in door["requires"] if c.get("test") == "account_at_least"
    }
    assert gates == {
        (STAIR, "wear", WEAR_STEP),
        (CHEST, "coin", MEND_COIN),
    }
    # the actor must be PRESENT — the office comes in person
    assert {"noun": "target", "test": "same_location",
            "with": "actor"} in door["requires"]
    assert [k["knows"] for k in door["knowledge"]["success"]] == [
        "the_stair_mended"]
    templates = pack.templates
    assert "wear" in templates["account_kinds"]
    assert "the_stair_wears" in templates["flow_glosses"]
    assert "the_stair_mended" in templates["knows"]
    # the no-amortization law holds: no flow touches the step or the notch
    assert not [f for f in economy["flows"] if f["kind"] in ("step", "notch")]


# -- (2) the condition accrues and saturates --------------------------------------


def test_the_wear_accrues_and_saturates_at_its_bound(tmp_path: Path) -> None:
    """The year's water: +2 a crossing, NEVER above the declared cap, and
    SILENT once full — the infrastructure debt nobody reads."""
    events, _sim = _run_committed(tmp_path, "maint.jsonl")
    trail = _trail(events, STAIR, "wear")
    mints = [row for row in trail if row[1] == "account_sourced"]
    assert [row[3] for row in mints] == [2, 4, 6, 8]
    assert len(mints) == CROSSINGS - 1, "the fifth crossing is the cap's silence"
    assert all(row[3] <= WEAR_CAP for row in trail)
    assert trail[0][0] == TICK_YEAR


# -- (3) the office's visit ------------------------------------------------------


def test_the_office_mends_in_person_and_clears_the_wear(tmp_path: Path) -> None:
    """The mend as ONE atomic convert: the wear down two, the chest down
    three, the keeper up one — and the mending public to the co-present."""
    events, sim = _run_committed(tmp_path, "maint.jsonl")
    mend = next(e for e in events if e.type == "account_converted")
    assert mend.actor == OFFICE
    assert mend.target == STAIR
    assert mend.outcome["recipe"] == "the_mend"
    changes = {(ch.entity, ch.prop): (ch.from_, ch.to_)
               for ch in mend.state_changes}
    assert changes[(STAIR, "account.wear")] == (WEAR_CAP, WEAR_CAP - WEAR_STEP)
    assert changes[(CHEST, "account.coin")][1] == (
        changes[(CHEST, "account.coin")][0] - MEND_COIN)
    assert changes[(KEEPER, "account.coin")][1] == (
        changes[(KEEPER, "account.coin")][0] + MEND_WAGE)
    # the keeper himself is the only witness at the stair's edge, and he learns
    assert [k.knows for k in mend.knowledge] == ["the_stair_mended"]
    assert [k.who for k in mend.knowledge] == [KEEPER]
    # the step account is NOT touched by the office (the named boundary)
    assert _trail(events, KEEPER, "step") == []
    assert sim.projection[STAIR]["account.wear"] == WEAR_CAP - WEAR_STEP


def test_the_mend_is_refused_out_of_place(tmp_path: Path) -> None:
    """The office comes in person: the same door attempted away from the
    stair is refused SOFTLY at the door — attempts are facts."""
    pack = load_pack(PACK_DIR)
    steps = [
        {"actor": OFFICE, "intent": "wait", "ticks": TICK_YEAR},
        {"actor": OFFICE, "intent": "mend_the_stair", "target": STAIR},
    ]
    log = tmp_path / "absent.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "absent", "seed": 42, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    rejected = [e for e in events
                if e.type == "intent_rejected"
                and e.outcome.get("action") == "mend_the_stair"]
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "target.same_location"
    assert not [e for e in events if e.type == "account_converted"]
    assert sim.projection[STAIR]["account.wear"] == WEAR_STEP


# -- (4) the ablation: the function lost ------------------------------------------


def test_without_the_office_the_wear_never_clears(tmp_path: Path) -> None:
    """The function-loss probe, run: drop the door and the cycle's second
    half is gone — the wear saturates at its cap and stays there forever.
    That difference is the office's own function, nothing else's."""
    twin = tmp_path / "nopost"
    twin.mkdir()
    for name in ("rules.json", "entities.json", "actions.json", "templates.json"):
        (twin / name).write_text(
            (PACK_DIR / name).read_text(encoding="utf-8"), encoding="utf-8")
    actions = json.loads((twin / "actions.json").read_text(encoding="utf-8"))
    actions["actions"] = [
        a for a in actions["actions"] if a["intent"] != "mend_the_stair"
    ]
    (twin / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8")
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules["economy"]["recipes"] = [
        r for r in rules["economy"]["recipes"] if r["id"] != "the_mend"
    ]
    # iter-443: the keeper's drive names the door as its `helper_verb`, and
    # the pack lint refuses a helper on an undeclared action — the COMPLETE
    # ablation drops the declaration with the function it names (the same
    # law the psyche block's own ablations follow).
    rules["psyche"]["drives"] = [
        d for d in rules["psyche"]["drives"] if d["id"] != "keep_the_crossing"
    ]
    (twin / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8")

    log = tmp_path / "worn.jsonl"
    sim = Simulator(load_pack(twin), 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "worn", "seed": 42, "pack": "province_pack@0.1",
        "steps": [{"intent": "wait", "ticks": TICK_YEAR * CROSSINGS}],
    })
    _, events = read_log(log, SCHEMA)
    assert sim.projection[STAIR]["account.wear"] == WEAR_CAP
    assert not [e for e in events if e.type == "account_converted"]


# -- (5) the corpus law and the fingerprint --------------------------------------


def test_the_canonical_corpus_is_untouched(tmp_path: Path) -> None:
    """INERT-FIRST (`PACK_SPEC` §9.1): the day-scale smoke run is
    byte-identical to the committed golden — the wear flow fires only at
    the macro crossing, far beyond its horizon."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    Simulator(pack, script["seed"], log, SCHEMA, commit="0000000").run_playscript(script)
    assert log.read_bytes() == (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl").read_bytes()


def test_the_visit_is_byte_identical_across_twins(tmp_path: Path) -> None:
    """INV-2: the same script twice, the same bytes; fingerprints agree."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_maintenance.json")
    pack = load_pack(PACK_DIR)
    arms = []
    for name in ("m_a.jsonl", "m_b.jsonl"):
        log = tmp_path / name
        sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
        result = sim.run_playscript(script)
        arms.append((result.fingerprint, log.read_bytes()))
    assert arms[0][1] == arms[1][1]
    assert arms[0][0] == arms[1][0]
