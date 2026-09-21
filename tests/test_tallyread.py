"""tallyread — the charcoal camp's first embodiment (iter-185, the
owner's «можешь продолжать мир трек» continuation call over STATUS's
embodiment routing — the natural doc-streak breaker after two
doc-only iterations, the iter-167 precedent's own reading): the
camp's TALLY READ, the re-weigh's proof surface of the fourth
authored meso unit (`ANCHOR_REGION.md` §6.4 — the gap text's own
"the count has no read hinge — the `read_pole` family; the re-weigh's
proof would need its own hinge, the pole's iter-161 precedent's
class"), landed as pure pack data, zero core change (the pole's
iter-161 precedent class; the read hinge's fourth instance — the grim
read_ticket first, the pole second, the stair third, the family's
second item-kind target).

The one seed: the `read_tally` hinge over the tally-stick
(`camp_tally_01`, committed with it — the notch habit's own class,
the count cut in wood at the stacks, carried by the master: the
seat's badge, the paper names the master, the camp reads the seat).
The close read mints the literal token `the_camps_word` — weight is
weight, shaved is shaved, the anti-shave discipline the brief's own
directive carries — and the secrets registry's third key turns it
into the lever over the master (the debt's named holder, the
withhold's keeper): the count public, the withhold harder to keep,
the re-weigh's two records meeting at last.

The claim packet (TEST_PLAN §9):

- Claim: the camp's tally gap is ONE pack-data read hinge — the
  camp's word becomes a reachable knowledge state and a live lever
  over the master at the committed band (the crisis probe's tally
  leg now walks on a committed surface: the runner reads the tally,
  the re-weigh's proof); zero core change.
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader's brief carries the word, the audit's own material;
  the reader holds a live cluster over the master); the boundary lens
  (the read pinned to the tally-stick by the field_in id read and
  gated on standing at the stacks — studying any other stave mints
  nothing; the token deliberately a SECRET, the pole's lever class
  NOT the stair's plain-custom boundary: the count is the crews'
  bounded knowledge, not a category the whole vale owns — the
  registry's THIRD key, the first pack whose secrets table names two
  debt-type subjects; the read mints the WORD, never the PRESENT
  count — the freight's volume surface stays owner-routed, the
  separate-track law).
- Prism: two deterministic chains on the committed pack plus both
  rejection arms at probed seeds — the crofts a day's walk
  up-country, the family's own day/night order INVERTED by the honest
  geography (the walk itself lands at night: the night arm is the
  direct chain, the day arm waits out the night at the camp); the
  reads are check-deterministic at every seed (perception 50 vs
  difficulty 30, both d20: the healthy reader never fails).
- Oracle: the event log scans (the read's knowledge record, the
  leverage mint's cluster, the coerce balance, the rejection
  outcomes); the brief's recalled-facts line (the read surface —
  `brief_from_log`, mode A); the same-seed twin.
- Falsifier: no knowledge minted on the read (the token dead); no
  cluster minted (the lever a lie); the coerce landing without the
  read (the door ungated); the night read staying exact (the
  acquisition arm not riding the new verb); the brief not carrying
  the word; the twin byte-shifting.
- Expected evidence: tally_read -> (pc_01, the_camps_word, saw,
  exact) on the day arm (the morning after the walk) and partial on
  the night arm (the unlit crofts, the drowned country after dark);
  leverage_gained (pc over the master, type debt, fidelity the
  read's own, expiry read.t + 129600 — the weighing season's window);
  coerce (trust 25 / fear 75, the fresh pair — D-030's break-fast
  law); the off-site read rejected on target.field_in and the far
  read on target.same_location (attempts are facts).
- Observed evidence: CONFIRMED at the measured band (seed 42 the day
  and night chains and both rejection arms; seeds 2/7 the
  check-determinism of the day read).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the secrets
  notes: the camp's own read mints nothing — the crews' lived
  knowledge is not event-recorded (INV-1) and no committed NPC holds
  it, and the master's own read mints nothing (the holder != subject
  guard); the PRESENT count never minted — the read_stair precedent's
  LAW-never-PRESENT boundary; the remaining two gaps — the camp's
  account, the freight's volume — stay owner-routed, the
  separate-track law).
"""

from __future__ import annotations

import json
from pathlib import Path

from brief.assembler import brief_from_log
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

PC = "pc_01"
MASTER = "npc_smelter_01"
TALLY = "camp_tally_01"
SACK = "charcoal_sack_01"
WORD = "the_camps_word"
SEASON = 129600  # one full season — the weighing season's own window

#: The day chain (seed 42, probed: the two hops land at t=1110, the
#: wait out the night to the morning after, the read check-deterministic
#: at t=1512): the crofts are a day's walk up-country — the family's
#: first chain that needs the overnight wait to read by daylight.
DAY_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "wait", "ticks": 400},
    {"intent": "read_tally", "target": TALLY},
)
#: The lever chain: the day read plus the corner at the master.
LEVER_CHAIN: tuple[dict, ...] = DAY_CHAIN + (
    {"intent": "coerce", "target": MASTER},
)
#: The night twin: the walk itself lands at night (t=1110, the
#: unlit crofts) — the read steps down the acquisition arm directly.
NIGHT_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "read_tally", "target": TALLY},
)
#: The off-site arm: the reader studies another thing at their own
#: feet — the field_in pin rejects (the id vocabulary, never the kind).
OFFSITE_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "read_tally", "target": SACK},
)
#: The far arm: the reader studies the tally from the road — the
#: co-location gate rejects (the reading happens at the stacks).
FAR_CHAIN: tuple[dict, ...] = (
    {"intent": "read_tally", "target": TALLY},
)
SEED_DAY = 42  # the read exact on the morning after, the lever spent
SEED_NIGHT = 42  # the same walk: the read lands at t=1112, in the night


def _run(tmp_path: Path, name: str, seed: int, steps: tuple[dict, ...]) -> list:
    pack = load_pack(PACK_DIR)
    sim = Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": [dict(step) for step in steps],
    })
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events


def _action(pack, intent: str) -> dict:
    return next(a for a in pack.data["actions.json"]["actions"]
                if a["intent"] == intent)


# -- the census (the seed as pack data) ----------------------------------------


def test_the_read_is_pinned_to_the_tally() -> None:
    """The re-weigh's proof hinge: a pack-specific close read (the pole's
    item-kind shape — the read hinge family's fourth instance, the
    field_in id pin means studying any other stave mints nothing),
    perception-gated, minting the LITERAL token on success and only
    the vague unread notches on failure — a failed read mints no
    cluster."""
    pack = load_pack(PACK_DIR)
    read = _action(pack, "read_tally")
    assert read["resolver"] == "inspect"
    assert read["check"] == {"kind": "perception", "difficulty": 30}
    assert read["requires"] == [
        {"noun": "target", "test": "kind", "is": "item"},
        {"noun": "target", "test": "same_location", "with": "actor"},
        {"noun": "target", "test": "field_in", "field": "id",
         "values": [TALLY]},
    ]
    assert read["knowledge"]["success"] == [
        {"who": "actor", "channel": "saw", "fidelity": "exact",
         "knows": WORD}
    ]
    assert read["knowledge"]["failure"] == [
        {"who": "actor", "channel": "saw", "fidelity": "vague",
         "knows": "unread_notches_on_the_tally"}
    ]
    # the honest failure surface: the vague token is not a secret
    assert "unread_notches_on_the_tally" not in pack.rules["secrets"]["tokens"]
    # the tale renders both arms (EVENT_SCHEMA §11)
    assert "tally_read" in pack.templates["events"]
    assert "tally_read_failed" in pack.templates["events"]


def test_the_word_is_registered_over_the_master() -> None:
    """The lever's registration: the camp's word is a DEBT-type secret
    whose subject is the master (the debt's named holder, the
    withhold's keeper) — the counter-record's claim in the debt's
    reconciliation, the pole's lever class (the registry's third key,
    the first pack with two debt-type subjects); the expiry one full
    season (129600 — the weighing season's own window, the lever
    living through the re-weigh)."""
    pack = load_pack(PACK_DIR)
    spec = pack.rules["secrets"]["tokens"][WORD]
    assert spec == {
        "subject": MASTER, "type": "debt", "expires_ticks": SEASON,
    }


def test_the_tally_rides_the_seat_unflagged() -> None:
    """The carrier binding, committed with the hinge: the tally-stick
    is the seat's own badge — carried by the master (the paper names
    the master, the camp reads the seat, §6.4's two theories of one
    debt), the position contract riding his legs. The verb-gate
    boundary's honest default: carried and UNFLAGGED — the pole's
    steal_target flag deliberately NOT duplicated (the re-weigh's
    proof is not pocketable); take keeps its uncarried gate, steal
    keeps the flag's unless-arm, drop_break stays the carrier's own."""
    pack = load_pack(PACK_DIR)
    tally = next(i for i in pack.entities["items"] if i["id"] == TALLY)
    assert tally["carrier"] == MASTER
    assert "steal_target" not in tally  # unflagged: the proof rides the seat
    master = next(n for n in pack.entities["npcs"] if n["id"] == MASTER)
    assert tally["id"] in master["carries"]  # the two-way carrier law
    take = _action(pack, "take")
    assert {"noun": "target", "test": "uncarried"} in take["requires"]
    steal = _action(pack, "steal")
    assert {"noun": "target", "test": "carries_flagged",
            "flag": "steal_target"} in steal["requires"]
    drop = _action(pack, "drop_break")
    assert {"noun": "target", "test": "carried_by", "who": "actor"} in drop["requires"]


# -- the read chain (the word -> the lever -> the corner) ------------------------


def test_the_day_read_mints_the_word_and_the_lever(tmp_path: Path) -> None:
    """The re-weigh's proof, live: the close read on the morning after
    the walk mints the exact camp's word on the reader, and the
    secrets registry turns it into the lever over the master — one
    leverage_gained cluster, holder the reader, subject the master,
    expiry the weighing season's window. Check-deterministic at every
    probed seed (the healthy reader never fails the perception gate)."""
    for seed in (42, 2, 7):
        events = _run(tmp_path, f"day_{seed}.jsonl", seed, DAY_CHAIN)
        reads = [e for e in events if e.type == "tally_read"]
        assert len(reads) == 1, f"seed {seed}: exactly one close read"
        assert (PC, WORD, "saw", "exact") in {
            (r.who, r.knows, r.channel, r.fidelity) for r in reads[0].knowledge
        }
        gained = [e for e in events if e.type == "leverage_gained"]
        assert len(gained) == 1
        cluster = gained[0]
        assert cluster.actor == PC and cluster.target == MASTER
        assert cluster.t == reads[0].t  # the mint rides the read's own commit
        assert cluster.outcome == {
            "secret": WORD, "type": "debt", "fidelity": "exact",
            "expires_at": reads[0].t + SEASON,
        }


def test_the_read_carries_the_re_weighs_proof(tmp_path: Path) -> None:
    """The changed-next-decision unit: the reader's brief carries the
    word — the crisis probe's tally leg walks on a committed surface
    (the runner reads the tally, the audit's own material: the
    counter-record the books never carried, the two records meeting
    at last). Before the read the books show the paper; after it the
    recalled facts show the count's law."""
    events = _run(tmp_path, "brief.jsonl", SEED_DAY, DAY_CHAIN)
    read = next(e for e in events if e.type == "tally_read")
    text = brief_from_log(tmp_path / "brief.jsonl", load_pack(PACK_DIR), SCHEMA)
    assert f"- [t {read.t}, saw, exact] {WORD}" in text.splitlines()


def test_the_lever_opens_the_corner_and_shifts_the_pair(tmp_path: Path) -> None:
    """The lever is spendable at the crofts: the coerce door reads the
    live cluster and the corner lands — the master's directed pair
    homes toward the reader break (trust from neutral 50-25) and spike
    (fear 50+75, D-030's break-fast law). The count prices trust,
    never coin: the debt's arithmetic untouched, the pair relation the
    lever's whole spend. The province's standing shape: no spend_event
    declared, so the event carries no cluster stamp and the cluster
    stays live (the grim one-spend-door law is that pack's own)."""
    events = _run(tmp_path, "lever.jsonl", SEED_DAY, LEVER_CHAIN)
    corners = [e for e in events if e.type == "coerce"]
    assert len(corners) == 1
    corner = corners[0]
    assert corner.actor == PC and corner.target == MASTER
    assert "cluster" not in corner.outcome  # no spend_event declared
    assert {(c.entity, c.prop, c.from_, c.to_) for c in corner.state_changes} == {
        (MASTER, "pair.pc_01.trust", None, 25),
        (MASTER, "pair.pc_01.fear", None, 75),
    }


def test_the_corner_without_the_read_dies_at_the_door(tmp_path: Path) -> None:
    """The leverage test IS the door (social-1b's law): no word, no
    corner — the attempt is a fact (intent_rejected names the failed
    lever test), never a write."""
    events = _run(tmp_path, "bare.jsonl", SEED_DAY, DAY_CHAIN[:2] + (
        {"intent": "coerce", "target": MASTER},
    ))
    assert not [e for e in events if e.type == "coerce"]
    rejections = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "coerce"
    ]
    assert len(rejections) == 1
    assert "leverage_over" in rejections[0].outcome["failed_test"]


def test_the_night_read_steps_the_word_down(tmp_path: Path) -> None:
    """The acquisition arm rides the new verb unchanged: the crofts
    are unlit (the drowned country after dark), and the walk itself
    lands at night — the read steps the record down the fidelity
    chain, the word learned PARTIAL by dark, half the notches
    legible. The cluster still mints (a partial-knowing holder still
    holds the lever, the cluster recording how well)."""
    events = _run(tmp_path, "night.jsonl", SEED_NIGHT, NIGHT_CHAIN)
    read = next(e for e in events if e.type == "tally_read")
    assert 1080 <= read.t < 1440  # the walk lands in the night phase
    assert (PC, WORD, "saw", "partial") in {
        (r.who, r.knows, r.channel, r.fidelity) for r in read.knowledge
    }
    cluster = next(e for e in events if e.type == "leverage_gained")
    assert cluster.outcome["fidelity"] == "partial"


def test_the_read_dies_at_the_door_off_site_and_far(tmp_path: Path) -> None:
    """The pin and the gate, live: studying another thing at the
    reader's own feet (the camp's own sack) rejects on the field_in id
    read (the closed vocabulary — the kind test alone would admit any
    item), and studying the tally from the road rejects on the
    co-location gate (the reading happens at the stacks). Attempts
    are facts — the rejections name the failed tests, nothing mints."""
    offsite = _run(tmp_path, "off.jsonl", SEED_DAY, OFFSITE_CHAIN)
    assert not [e for e in offsite if e.type == "tally_read"]
    rejection = next(e for e in offsite if e.type == "intent_rejected")
    assert rejection.outcome == {
        "action": "read_tally", "reason": "precondition",
        "failed_test": "target.field_in",
    }
    far = _run(tmp_path, "far.jsonl", SEED_DAY, FAR_CHAIN)
    assert not [e for e in far if e.type == "tally_read"]
    rejection = next(e for e in far if e.type == "intent_rejected")
    assert rejection.outcome == {
        "action": "read_tally", "reason": "precondition",
        "failed_test": "target.same_location",
    }
    assert not [e for e in far if e.type == "leverage_gained"]


def test_the_chains_are_deterministic(tmp_path: Path) -> None:
    """The twin of T1's law at the seeds' own band: same seed + script
    + environment, byte-identical logs — both chains."""
    for name, steps in (("day", DAY_CHAIN), ("night", NIGHT_CHAIN)):
        first = _run(tmp_path, f"{name}_a.jsonl", SEED_DAY, steps)
        second = _run(tmp_path, f"{name}_b.jsonl", SEED_DAY, steps)
        assert first == second
