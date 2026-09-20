"""stepread — the step bench's first embodiment (iter-167, the owner's
«продолжай работы, что логичнее всего сейчас начать» continuation call
over STATUS's embodiment routing — the natural doc-streak breaker after
three doc-only iterations): the step's close read, the SETTING VERB of
the second authored meso unit (`ANCHOR_REGION.md` §6.2, the reading at
the stair that had no committed action — the gap text's own "a future
embodiment's own class, the read_pole precedent"), landed as pure pack
data, zero core change (the pole's iter-161 precedent class; the read
hinge's third instance — the grim read_ticket first, the pole second).

The one seed (the W4 working set's named embodiment option,
`WORLD_WORKPLAN.md` §6 candidate 3): the `read_stair` hinge over the
weir stair — the stone IS the law's own text (the water law lives in
stone, four rungs, the head each names), and the close read mints the
literal token `the_step_law`: the ORDER the road never learns from the
books (§6.2's knowledge asymmetry — the stranger reads a stingy
ferryman, never the order; §7.1's stranger row, the road's misread
correctable in play).

The claim packet (TEST_PLAN §9):

- Claim: the step bench's setting verb is ONE pack-data read hinge —
  the step law becomes a reachable knowledge state at the committed
  band, the meaning slice's misread-correcting half widened from the
  authored band; zero core change.
- Lens(es): the changed-next-decision unit (who simulates differently —
  the reader's brief carries the order: the narrator document's
  recalled facts re-priced); the boundary lens (the read pinned to the
  weirstair by the field_in id read and gated on standing at the stair
  — studying any other stone mints nothing; the token deliberately
  plain knowledge — no secrets entry, no cluster, the pole's debt-lever
  class NOT duplicated: the step law is the vale's own category, public
  custom, no lever over any subject).
- Prism: two deterministic chains on the committed pack (the day-read
  chain, the night twin with the wait into the night phase) at probed
  seeds — the reads are check-deterministic at every seed (perception
  50 vs difficulty 30, both d20: the healthy reader never fails); the
  off-site and far arms ride the door's own rejections.
- Oracle: the event log scans (the read's knowledge record, the
  rejection outcomes, the absence of any leverage cluster); the brief's
  recalled-facts line (the read surface — `brief_from_log`, mode A);
  the same-seed twin.
- Falsifier: no knowledge minted on the read (the token dead); a
  leverage cluster minting anyway (the plain-knowledge boundary a lie);
  the night read staying exact (the acquisition arm not riding the new
  verb); the brief not carrying the order; the twin byte-shifting.
- Expected evidence: stair_read -> (pc_01, the_step_law, saw, exact) on
  the day arm; partial on the night arm (the unlit weir after dark);
  the brief line "- [t N, saw, exact] the_step_law"; the off-site read
  rejected on target.field_in and the far read on target.same_location
  (attempts are facts); the twin identical.
- Observed evidence: CONFIRMED at the measured band (seed 42 the day
  and night chains and both rejection arms; seeds 2/7 the
  check-determinism of the day read).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues: no NPC driver reads the
  stair — the player-facing verb, the pole's own dormant-family class;
  the PRESENT step never minted — the phases carry no head, the water
  level stays owner-routed per the separate-track law; the law is what
  the stone says, not what the river does today).
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
STAIR = "loc_weirstair"
ROAD = "loc_riverroad"
LAW = "the_step_law"

#: The read chain (seed 42, probed: the move lands at t=705, the read
#: check-deterministic): the walk to the stair, the close read.
READ_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": STAIR},
    {"intent": "read_stair", "target": STAIR},
)
#: The night twin: the same walk plus the wait to the night phase
#: (t=1080) — the unlit weir's acquisition arm on the read.
NIGHT_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": STAIR},
    {"intent": "wait", "ticks": 375},
    {"intent": "read_stair", "target": STAIR},
)
#: The off-site arm: the reader studies another stone at their own
#: feet — the field_in pin rejects (the id vocabulary, never the kind).
OFFSITE_CHAIN: tuple[dict, ...] = (
    {"intent": "read_stair", "target": ROAD},
)
#: The far arm: the reader studies the stair from the road — the
#: co-location gate rejects (the reading happens AT the water).
FAR_CHAIN: tuple[dict, ...] = (
    {"intent": "read_stair", "target": STAIR},
)
SEED_DAY = 42  # the read exact, the brief carrying the order
SEED_NIGHT = 42  # the same clock: the read lands at t=1082, in the night


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


def test_the_read_is_pinned_to_the_stair() -> None:
    """The setting verb's hinge: a pack-specific close read (the grim
    read_ticket shape at its third instance — the first LOCATION-kind
    target: the stair is the carrier itself, not a thing at the stair),
    perception-gated, minting the LITERAL token on success and only the
    vague unread steps on failure — a failed read mints no order."""
    pack = load_pack(PACK_DIR)
    read = _action(pack, "read_stair")
    assert read["resolver"] == "inspect"
    assert read["check"] == {"kind": "perception", "difficulty": 30}
    assert read["requires"] == [
        {"noun": "target", "test": "kind", "is": "location"},
        {"noun": "target", "test": "same_location", "with": "actor"},
        {"noun": "target", "test": "field_in", "field": "id",
         "values": [STAIR]},
    ]
    assert read["knowledge"]["success"] == [
        {"who": "actor", "channel": "saw", "fidelity": "exact",
         "knows": LAW}
    ]
    assert read["knowledge"]["failure"] == [
        {"who": "actor", "channel": "saw", "fidelity": "vague",
         "knows": "unread_steps_on_the_stair"}
    ]
    # the tale renders both arms (EVENT_SCHEMA §11)
    assert "stair_read" in pack.templates["events"]
    assert "stair_read_failed" in pack.templates["events"]


def test_the_token_is_plain_knowledge() -> None:
    """The boundary the pole's read deliberately crossed and this one
    deliberately does not: the step law is the vale's own category —
    public custom held by the practitioners' reading (the humor probe's
    shared-categories proof), no lever over any subject. No secrets
    entry, no echo valence, no crime-watch or belief consumer: the
    knowledge state itself (the brief's recalled facts) is the read
    surface, and the registry stays two keys."""
    pack = load_pack(PACK_DIR)
    assert LAW not in pack.rules["secrets"]["tokens"]
    assert "unread_steps_on_the_stair" not in pack.rules["secrets"]["tokens"]
    assert LAW not in pack.rules["echo"]["tokens"]
    assert LAW not in pack.rules["crime_watch"]["suspicion_from_knowledge"]
    assert all(
        LAW not in belief.get("family", ())
        for belief in pack.rules.get("traits", {}).get("beliefs", {}).values()
    )


# -- the read chain (the order -> the reader's brief) ---------------------------


def test_the_read_mints_the_step_law(tmp_path: Path) -> None:
    """The setting verb, live: the close read at the stair mints the
    exact step law on the reader — and nothing else: no leverage
    cluster (the plain-knowledge boundary), the knowledge state the
    only change. Check-deterministic at every probed seed (the healthy
    reader never fails the perception gate)."""
    for seed in (42, 2, 7):
        events = _run(tmp_path, f"day_{seed}.jsonl", seed, READ_CHAIN)
        reads = [e for e in events if e.type == "stair_read"]
        assert len(reads) == 1, f"seed {seed}: exactly one close read"
        assert (PC, LAW, "saw", "exact") in {
            (r.who, r.knows, r.channel, r.fidelity) for r in reads[0].knowledge
        }
        assert not [e for e in events if e.type == "leverage_gained"], (
            "the step law is public custom — no cluster mints"
        )


def test_the_read_corrects_the_roads_misread(tmp_path: Path) -> None:
    """The changed-next-decision unit: the reader's brief carries the
    order — the meaning slice's stranger row (§7.1) widened to the
    committed band. Before the read the books show the toll; after it
    the recalled facts show the step — the narrator document's own
    re-pricing of the doubled toll (the fourth step's own text, never
    the ferryman's greed)."""
    events = _run(tmp_path, "brief.jsonl", SEED_DAY, READ_CHAIN)
    read = next(e for e in events if e.type == "stair_read")
    text = brief_from_log(tmp_path / "brief.jsonl", load_pack(PACK_DIR), SCHEMA)
    assert f"- [t {read.t}, saw, exact] {LAW}" in text.splitlines()


def test_the_night_read_steps_the_order_down(tmp_path: Path) -> None:
    """The acquisition arm rides the new verb unchanged: the weir stair
    is unlit, and a read in the night phase steps the record down the
    fidelity chain — the order learned PARTIAL by dark, half the rungs
    legible. No cluster mints on this arm either (the partial-knowing
    reader holds knowledge, never a lever)."""
    events = _run(tmp_path, "night.jsonl", SEED_NIGHT, NIGHT_CHAIN)
    read = next(e for e in events if e.type == "stair_read")
    assert 1080 <= read.t < 1440  # the night phase pinned by the wait
    assert (PC, LAW, "saw", "partial") in {
        (r.who, r.knows, r.channel, r.fidelity) for r in read.knowledge
    }
    assert not [e for e in events if e.type == "leverage_gained"]


def test_the_read_dies_at_the_door_off_site_and_far(tmp_path: Path) -> None:
    """The pin and the gate, live: studying another stone at the
    reader's own feet rejects on the field_in id read (the closed
    vocabulary — the kind test alone would admit any location), and
    studying the stair from the road rejects on the co-location gate
    (the reading happens at the water). Attempts are facts — the
    rejections name the failed tests, nothing mints."""
    offsite = _run(tmp_path, "off.jsonl", SEED_DAY, OFFSITE_CHAIN)
    assert not [e for e in offsite if e.type == "stair_read"]
    rejection = next(e for e in offsite if e.type == "intent_rejected")
    assert rejection.outcome == {
        "action": "read_stair", "reason": "precondition",
        "failed_test": "target.field_in",
    }
    far = _run(tmp_path, "far.jsonl", SEED_DAY, FAR_CHAIN)
    assert not [e for e in far if e.type == "stair_read"]
    rejection = next(e for e in far if e.type == "intent_rejected")
    assert rejection.outcome == {
        "action": "read_stair", "reason": "precondition",
        "failed_test": "target.same_location",
    }
    assert not [e for e in far if e.type == "leverage_gained"]


def test_the_chains_are_deterministic(tmp_path: Path) -> None:
    """The twin of T1's law at the seeds' own band: same seed + script
    + environment, byte-identical logs — both chains."""
    for name, steps in (("day", READ_CHAIN), ("night", NIGHT_CHAIN)):
        first = _run(tmp_path, f"{name}_a.jsonl", SEED_DAY, steps)
        second = _run(tmp_path, f"{name}_b.jsonl", SEED_DAY, steps)
        assert first == second
