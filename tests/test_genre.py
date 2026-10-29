"""genre — the W6 genre-matrix witness (iter-278, the owner's
«открывай задачу по W6» call — the station's first row: the genre
matrix run on the SAME canonical package, the committed province_pack
untouched, zero core, zero pack change, the LOG untouched, zero
corpus price).

The station's law (WORLD_WORKPLAN §8, WORLD_TRACK_AGENT_CONTEXT §9):
a genre succeeds when it emerges from a different reading of the same
pressures, never from switching to another authored world; a FAILED
test identifies the missing world substrate — it never triggers plot
writing. The matrix: adventure / mystery / politics / relationship
drama / tragedy / comedy / biography. Four genres carry their W5
evidence (biography clean iter-191; comedy and tragedy carried at the
live band iter-194/206/208/209/270; relationship drama the winter-kin
line iter-165/203–206/270) — the census pins their committed
surfaces. THREE genres were untested and are MEASURED here at the
deterministic band:

- ADVENTURE — `departure -> risk that can realize -> objective ->
  changed return`. The tally journey (the iter-185 chain's own
  material, read under the genre's lens): the runner leaves the
  riverroad, walks the artery up-country, lands at night (the crofts
  unlit — the drowned country after dark), waits out the night, reads
  the tally in the morning (the word minted exact), holds the lever,
  corners the master (the pair moved), walks home changed. The hard
  risk: the riverroad-keep edge closed (the divergence-probe form,
  the I0 twin's own shape — one pack-data edge between two runs of
  the same script) — the world refuses the journey outright, the
  attempts the only residue.
- MYSTERY — `hidden fact -> bounded discovery path -> revelation
  that changes future options`. The shave is a registered secret
  (the_camps_word over the master); the world NEVER volunteers it
  (the silent-world run: a full morning at the stacks, nothing
  mints); the discovery path is the read hinge (the iter-185 gates);
  the revelation IS the door — the coerce lands only through the
  word (the fork measured: same morning, same place, the discovery
  the only difference).
- POLITICS — `competing interests over one pressure -> differential
  institutional response -> a move that changes the standing balance
  with public residue`. The triangle's committed arms (the feud
  script seed 53, the keep road seed 139, the both-fires road seed 2
  — the pinned seeds, never shopped): the same pressure family (the
  fire's fear) tips the GUILD on the market road, the GARRISON on
  the keep road, the FAMILIES only when both elders wake — plus the
  squeeze (reprice_paper, iter-271's door): the standing terms
  moved 16->18->20, public, and the balance persists.

The mechanics measured here are owned by their witnesses
(test_tallyread iter-185, test_triangle iter-135, test_repricing
iter-271 — cited, never re-derived); THIS witness owns the
matrix-level claim: the same package's pressure network carries all
seven genres' causal requirements at the measured band.

The claim packet (TEST_PLAN §9):

- Claim: the SAME canonical package (the committed province_pack,
  zero modification) expresses the three untested genres' minimal
  causal requirements — the adventure's four legs (incl. the world's
  own refusal), the mystery's hidden-fact/discovery/revelation
  chain, the politics' differential response and balance-moving
  move — while the four carried genres' surfaces stay committed
  (the census).
- Lens(es): the genre-requirement lens (each genre's minimal causal
  legs, named before measurement); the same-package lens (every
  probe over the identical committed pack — the B arm's one
  pack-data edge the only perturbation, the divergence-probe form);
  the reading-band lens (the deterministic band measures the genres'
  CAUSAL PRECONDITIONS — the human/LLM reading band is the W5
  precedent's own row, owner-routed, never claimed here).
- Prism: the crafted runs — A/M0/P2 on the committed pack, B on the
  one-edge-closed twin, P1 the committed arms at their pinned seeds;
  the fork pairs (A vs B, A vs M0) the same script, one difference.
- Oracle: the event-log scans (the reads, the levers, the coerce,
  the rejections' failed tests, the institutional events, the
  squeeze's account events), the projection reads (the pair, the
  paper, the positions), the knowledge census (the word, the public
  rows), the golden corpus bytes.
- Falsifier: the word minted without the read (the silence broken);
  the coerce landing without the lever (the door ungated); the
  journey succeeding through the closed edge (the refusal broken);
  the three institutions answering identically (the differential
  denied); the squeeze leaving the terms unmoved or unwitnessed; the
  four carried genres' surfaces missing from the census; the golden
  T1 bytes shifting.
- Expected evidence: A — the word exact at t=1512, the lever minted
  at the read's own commit, the coerce's pair (trust 25, fear 75),
  home at the riverroad; B — the move refused at target.adjacent_to,
  the read and coerce refused at target.same_location, nothing
  minted, the pair untouched; M0 — zero the_camps_word records, the
  coerce refused at actor.leverage_over in the morning at the
  stacks; P1 — the feud arm 1 council + the public row, the keep arm
  1 patrol + no council, the both-fires arm 2 vigils + 1 council +
  both public rows, each single fire waking exactly one elder; P2 —
  the paper 16->18->20, the market's witnesses holding
  the_paper_repriced exact, the coin untouched by the squeeze.
- Observed evidence: CONFIRMED at the measured band (seed 42 the
  adventure/mystery probes; seeds 53/139/2 the committed politics
  arms — the pinned seeds).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED at the deterministic band — the matrix's
  substrate-side expressed. The honest boundaries, classified per
  the station's vocabulary: (a) the adventure's hard-risk arm rides
  an AUTHORED edge closure — no runtime route writer (the I0
  inventory's standing candidate, SUBSTRATE_GAP named and awaiting
  repetition, never routed here); (b) the mystery's measured band is
  ONE hidden fact, ONE bounded path, ONE state-changing revelation —
  the full genre shape (many clues, red herrings, the inference
  chain) is beyond the band, named, not owed; (c) the politics'
  player-side agency over the terms is iter-271's own recorded
  residue (the runner's re-pricing power a future row's own call);
  the reading band (W5's human/LLM form) owner-routed, never
  claimed. No plot written, no machinery promoted, no pack change.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

PC = "pc_01"
MASTER = "npc_smelter_01"        # the seat's own hand — the camp's person
TALLY = "camp_tally_01"          # the count cut in wood — the clue
WORD = "the_camps_word"          # the hidden fact — the shave, two seasons back
ROAD = "loc_riverroad"           # the runner's home — the departure and return
KEEP = "loc_keep"                # the artery's node
CROFTS = "loc_crofts"            # the stacks — the journey's objective
CHEST = "loc_malby"              # the beam's town — the politics stage
PAPER = 16                       # the starved winter's stores — the standing terms
MARGIN = 2                       # the withheld margin's own number
SEASON = 129600                  # the weighing season's window — the lever's life


# -- the helpers ----------------------------------------------------------------


def _genre_twin(tmp_path: Path, name: str) -> Path:
    """The one-edge-closed twin: the riverroad-keep edge removed BOTH
    ways (the divergence-probe form, the I0 twin's own shape — the
    artery's root ford drowned; every location keeps an edge, the
    lint's orphan law respected — the closure class the lint admits)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    entities = json.loads(
        (target / "entities.json").read_text(encoding="utf-8")
    )
    for loc in entities["locations"]:
        if loc["id"] == ROAD:
            loc["exits"] = [e for e in loc["exits"] if e != KEEP]
        if loc["id"] == KEEP:
            loc["exits"] = [e for e in loc["exits"] if e != ROAD]
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return target


def _run(
    pack_dir: Path, tmp_path: Path, name: str, seed: int,
    steps: list[dict[str, Any]],
) -> tuple[list, Simulator]:
    pack = load_pack(pack_dir)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, sim


def _knows(events: list, token: str) -> set[tuple[str, str]]:
    """The knowledge census for one token: (who, fidelity) pairs."""
    return {
        (r.who, r.fidelity) for e in events for r in e.knowledge
        if r.knows == token
    }


#: The adventure's journey (the iter-185 day chain's own material,
#: read under the genre's lens): depart, walk up-country, land at
#: night, wait for the morning, read, corner, walk home.
JOURNEY: list[dict[str, Any]] = [
    {"intent": "move", "target": KEEP},
    {"intent": "move", "target": CROFTS},
    {"intent": "wait", "ticks": 400},
    {"intent": "read_tally", "target": TALLY},
    {"intent": "coerce", "target": MASTER},
    {"intent": "move", "target": KEEP},
    {"intent": "move", "target": ROAD},
    {"intent": "wait", "ticks": 10},
]
#: The refused journey: the same intents against the closed artery —
#: the world's own no.
REFUSED: list[dict[str, Any]] = [
    {"intent": "move", "target": KEEP},
    {"intent": "read_tally", "target": TALLY},
    {"intent": "coerce", "target": MASTER},
    {"intent": "wait", "ticks": 10},
]
#: The silent world: the full morning at the stacks, the deliberate
#: read withheld — the world never volunteers the secret.
SILENT: list[dict[str, Any]] = [
    {"intent": "move", "target": KEEP},
    {"intent": "move", "target": CROFTS},
    {"intent": "wait", "ticks": 400},
    {"intent": "coerce", "target": MASTER},
    {"intent": "move", "target": KEEP},
    {"intent": "move", "target": ROAD},
    {"intent": "wait", "ticks": 10},
]
#: The squeeze: the master at the beam's town, the terms re-priced
#: twice — the balance moved and stayed (the committed pack, no twin).
SQUEEZE: list[dict[str, Any]] = [
    {"intent": "move", "actor": MASTER, "target": KEEP},
    {"intent": "move", "actor": MASTER, "target": CHEST},
    {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
    {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
    {"intent": "wait", "ticks": 10},
]
#: The keep road (the committed arm's own steps, seed 139 — the
#: garrison's answer).
KEEP_ROAD: list[dict[str, Any]] = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 30},
    {"intent": "move", "target": ROAD},
    {"intent": "wait", "ticks": 15},
    {"intent": "move", "target": KEEP},
    {"intent": "arson", "target": KEEP},
    {"intent": "wait", "ticks": 2000},
]
#: The both-fires road (the committed arm's own steps, seed 2 — the
#: families' answer).
BOTH_ROAD: list[dict[str, Any]] = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 30},
    {"intent": "move", "target": ROAD},
    {"intent": "wait", "ticks": 15},
    {"intent": "move", "target": KEEP},
    {"intent": "arson", "target": KEEP},
    {"intent": "wait", "ticks": 600},
    {"intent": "move", "target": CHEST},
    {"intent": "arson", "target": CHEST},
    {"intent": "wait", "ticks": 600},
    {"intent": "move", "target": "loc_thornmill"},
    {"intent": "wait", "ticks": 900},
]


# -- the census (the matrix's substrate inventory) --------------------------------


def test_the_matrix_census() -> None:
    """The W6 hypothesis's substrate-side: ONE committed package
    carrying all SEVEN genres' surfaces — the adventure's walkable
    artery and the unlit crofts (the night risk); the mystery's
    registered secret, its read hinge and the lever door; the
    politics' triangle and the squeeze; the relationship drama's
    winter-kin doors and its own secret; the tragedy's heartbreak
    pair (rs-7's opened option, rs-8's re-subjectivation); the
    comedy's answer-frame gloss (rs-6) on the dated chain (rs-10);
    the biography's account-chain doors — the life course's own
    material."""
    pack = load_pack(PACK_DIR)
    actions = {a["intent"] for a in pack.data["actions.json"]["actions"]}
    # ADVENTURE: the artery walkable, the crofts unlit (the risk's
    # soft form — the drowned country after dark)
    locations = {loc["id"]: loc for loc in pack.entities["locations"]}
    assert locations[ROAD]["exits"] == ["loc_weirstair", KEEP]
    assert locations[KEEP]["exits"] == [ROAD, CHEST, CROFTS]
    assert locations[CROFTS]["exits"] == [KEEP]
    assert locations[KEEP]["flags"] == {"lit": True}   # the lit keep
    assert "flags" not in locations[CROFTS]            # the unlit stacks
    # MYSTERY: the registered secret + the pinned hinge + the door
    assert pack.rules["secrets"]["tokens"][WORD] == {
        "subject": MASTER, "type": "debt", "expires_ticks": SEASON,
    }
    read = next(a for a in pack.data["actions.json"]["actions"]
                if a["intent"] == "read_tally")
    assert {"noun": "target", "test": "field_in", "field": "id",
            "values": [TALLY]} in read["requires"]
    coerce = next(a for a in pack.data["actions.json"]["actions"]
                  if a["intent"] == "coerce")
    assert {"noun": "actor", "test": "leverage_over",
            "who": "target"} in coerce["requires"]
    # POLITICS: the triangle's three doors + the squeeze
    entries = {e["group"]: e for e in pack.rules["factions"]["entries"]}
    assert {e["intent"]["kind"] for e in entries.values()} == {
        "council", "hold_vigil", "patrol",
    }
    assert "reprice_paper" in actions
    # RELATIONSHIP DRAMA: the winter kin's doors + its own secret
    assert {"share_board", "read_kinmark", "claim_kinmark",
            "say_the_names"} <= actions
    assert "the_winter_kin" in pack.rules["secrets"]["tokens"]
    # TRAGEDY: the heartbreak pair's committed rows (rs-7 / rs-8)
    assert "the crossing's table open to the claimant's line" in (
        pack.templates["events"]["the_edge_answers"]
    )
    assert "their own futures the flood took down with them" in (
        pack.templates["events"]["the_names_kept"]
    )
    # COMEDY: the withhold's answer-frame (rs-6) on the dated
    # chain (rs-10) — the humor's own surface
    assert pack.templates["flow_glosses"]["the_withhold_banks"] == (
        "the camp's answer to a tilted beam: unweighable at it, "
        "the paper still paid"
    )
    assert "two seasons back" in pack.templates["account_kinds"]["bloom"]
    # BIOGRAPHY: the life course's account-chain doors
    assert {"settle_paper", "render_toll", "pass_paper", "buy_punt",
            "reckon_paper", "render_fund", "pass_the_seat"} <= actions


# -- ADVENTURE: the journey and the changed return --------------------------------


def test_adventure_the_journey_and_the_changed_return(
    tmp_path: Path,
) -> None:
    """The adventure's four legs on the committed package: the
    DEPARTURE (the runner leaves the riverroad for the artery), the
    RISK's soft form paid honestly (the walk lands at night — the
    unlit crofts; the patient traveler waits out the dark rather
    than read half-legible notches, the iter-185 night-step law
    cited, never re-measured), the OBJECTIVE (the morning read mints
    the word exact — and the lever with it, at the read's own
    commit), the CHANGED RETURN (the corner taken — the master's
    pair moved break-fast — and the runner home with the word, the
    lever and the changed relation: the journey's three residues)."""
    events, sim = _run(PACK_DIR, tmp_path, "adv_a", 42, JOURNEY)
    reads = [e for e in events if e.type == "tally_read"]
    assert len(reads) == 1
    assert (PC, "exact") in _knows(events, WORD)
    levers = [e for e in events if e.type == "leverage_gained"]
    assert len(levers) == 1
    assert levers[0].actor == PC and levers[0].target == MASTER
    assert levers[0].t == reads[0].t  # the mint rides the read's commit
    corners = [e for e in events if e.type == "coerce"]
    assert len(corners) == 1
    assert {(c.entity, c.prop, c.to_) for c in corners[0].state_changes} == {
        (MASTER, "pair.pc_01.trust", 25),
        (MASTER, "pair.pc_01.fear", 75),
    }
    # home — the loop closed, the three residues carried
    assert sim.projection[PC]["position"] == ROAD
    assert sim.projection[MASTER]["pair.pc_01.trust"] == 25
    assert sim.projection[MASTER]["pair.pc_01.fear"] == 75
    assert (PC, "exact") in _knows(events, WORD)


def test_adventure_the_refused_road(tmp_path: Path) -> None:
    """The adventure's hard risk: the world CAN refuse the journey.
    The artery's root edge closed (the divergence-probe form — one
    pack-data edge between two runs of the same script): the move
    refused at the adjacency gate, the read and the corner refused
    at the geography gate — three attempts as facts, nothing minted,
    the master's pair untouched, the runner never left home. The
    honest boundary: the closure is AUTHORED between runs, never a
    world event — the I0 inventory's standing candidate (no runtime
    route writer), SUBSTRATE_GAP named, awaiting repetition, never
    routed here."""
    events, sim = _run(_genre_twin(tmp_path, "adv_b_pack"),
                       tmp_path, "adv_b", 42, REFUSED)
    assert not [e for e in events if e.type == "tally_read"]
    assert not [e for e in events if e.type == "leverage_gained"]
    assert not [e for e in events if e.type == "coerce"]
    rejections = [
        e for e in events if e.type == "intent_rejected"
    ]
    failed = {(r.outcome["action"], r.outcome["failed_test"])
              for r in rejections}
    assert failed == {
        ("move", "target.adjacent_to"),
        ("read_tally", "target.same_location"),
        ("coerce", "target.same_location"),
    }
    assert not _knows(events, WORD)
    assert sim.projection[PC]["position"] == ROAD      # never left
    assert sim.projection[MASTER].get("pair.pc_01.trust") is None
    assert sim.projection[MASTER].get("pair.pc_01.fear") is None


def test_adventure_the_two_returns_diverge(tmp_path: Path) -> None:
    """The genre's stakes measured as the fork: the same script, one
    pack-data edge the only difference — run A returns with the word
    exact, the lever held and the master's pair moved; run B returns
    with none of it, the attempts the only residue. The changed
    return is EARNED against the world's own shape, never granted."""
    events_a, sim_a = _run(PACK_DIR, tmp_path, "adv_d_a", 42, JOURNEY)
    events_b, sim_b = _run(_genre_twin(tmp_path, "adv_d_b_pack"),
                           tmp_path, "adv_d_b", 42, REFUSED)
    assert _knows(events_a, WORD) == {(PC, "exact")}
    assert not _knows(events_b, WORD)
    assert [e for e in events_a if e.type == "coerce"]
    assert not [e for e in events_b if e.type == "coerce"]
    assert sim_a.projection[MASTER]["pair.pc_01.fear"] == 75
    assert sim_b.projection[MASTER].get("pair.pc_01.fear") is None
    # both travelers home — one changed, one refused
    assert sim_a.projection[PC]["position"] == ROAD
    assert sim_b.projection[PC]["position"] == ROAD


# -- MYSTERY: the hidden fact and the revelation's door ----------------------------


def test_mystery_the_world_never_volunteers_the_secret(
    tmp_path: Path,
) -> None:
    """The mystery's first leg: the hidden fact stays hidden. A full
    morning at the stacks — the tally-stick in reach, the master
    present, the debt standing — and WITHOUT the deliberate read
    nothing mints: zero the_camps_word records anywhere in the log,
    zero levers, the corner refused at the lever gate itself (the
    door IS the leverage test). The world's silence is the genre's
    own negative space: nobody hands the reader the answer."""
    events, sim = _run(PACK_DIR, tmp_path, "mys_m0", 42, SILENT)
    assert not _knows(events, WORD)
    assert not [e for e in events if e.type == "leverage_gained"]
    assert not [e for e in events if e.type == "coerce"]
    refusals = [e for e in events if e.type == "intent_rejected"
                and e.outcome["action"] == "coerce"]
    assert len(refusals) == 1
    assert "leverage_over" in refusals[0].outcome["failed_test"]
    assert sim.projection[MASTER].get("pair.pc_01.trust") is None


def test_mystery_the_revelation_is_the_door(tmp_path: Path) -> None:
    """The mystery's last leg: the revelation changes future options.
    The fork — the same morning, the same stacks, the discovery the
    ONLY difference: with the read, the corner lands (the pair
    moved, the relation changed); without it, the door refuses at
    the lever gate. The knowledge is not prose — it is the
    difference between a moved relation and a dead door."""
    events_a, sim_a = _run(PACK_DIR, tmp_path, "mys_a", 42, JOURNEY)
    events_m, sim_m = _run(PACK_DIR, tmp_path, "mys_m", 42, SILENT)
    assert _knows(events_a, WORD) == {(PC, "exact")}
    assert not _knows(events_m, WORD)
    assert [e for e in events_a if e.type == "coerce"]
    refused = [e for e in events_m if e.type == "intent_rejected"
               and e.outcome["action"] == "coerce"]
    assert len(refused) == 1
    assert "leverage_over" in refused[0].outcome["failed_test"]
    assert sim_a.projection[MASTER]["pair.pc_01.trust"] == 25
    assert sim_m.projection[MASTER].get("pair.pc_01.trust") is None


# -- POLITICS: the differential answer and the moved balance -----------------------


def test_politics_the_same_pressure_three_answers(
    tmp_path: Path,
) -> None:
    """The politics' core: the SAME pressure family (the fire's
    fear) tipping THREE different institutions — the market fire
    moves the GUILD (the council, the stalls barred, the public
    row), the keep fire moves the GARRISON (the patrol, the crown's
    slower answer), and only BOTH fires wake the FAMILIES (each
    single fire wakes exactly one elder — the deadband: the old
    blood moves together or not at all). The committed arms at
    their pinned seeds (rng-1's epoch re-measured: 39 / 142 / 229 —
    the witnesses' own, never shopped); the mechanics owned by
    test_triangle (iter-135), read here under the genre's lens."""
    # the market road (the committed feud script, seed 53): the guild
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_feud.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "feud.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, feud = read_log(log, SCHEMA)
    assert len([e for e in feud if e.type == "guild_councils"]) == 1
    assert not [e for e in feud if e.type == "garrison_patrols"]
    assert not [e for e in feud if e.type == "wergeld_vigil"]
    assert _knows(feud, "the_guild_bars_the_stalls")  # the public row
    # the keep road (seed 142, the epoch's re-pin): the garrison — and the guild still
    assert len([e for e in feud if e.type == "grief_wakes"]) == 1
    keep_events, _ = _run(PACK_DIR, tmp_path, "pol_keep", 142, KEEP_ROAD)
    assert len([e for e in keep_events if e.type == "garrison_patrols"]) == 1
    assert not [e for e in keep_events if e.type == "guild_councils"]
    assert not [e for e in keep_events if e.type == "wergeld_vigil"]
    # the both-fires road (seed 229, the epoch's re-pin): the families —
    # the vigil (ki114-1-impl: twice -> once — the second fire's
    # realization missed the faction deadband's window at the shifted
    # phase, F2; the LAW held: both fires wake the families, each
    # single fire wakes none — the vigil still fires, the elders still
    # both wake)
    both_events, _ = _run(PACK_DIR, tmp_path, "pol_both", 229, BOTH_ROAD)
    assert len([e for e in both_events if e.type == "wergeld_vigil"]) == 1
    assert len([e for e in both_events if e.type == "guild_councils"]) == 1
    assert len([e for e in both_events if e.type == "grief_wakes"]) == 2
    assert _knows(both_events, "the_blood_price_spoken")  # the vigil's row


def test_politics_the_squeeze_moves_the_balance(tmp_path: Path) -> None:
    """The politics' second leg: a move that changes the standing
    balance with public residue — the guild's squeeze (iter-271's
    door) re-priced twice at the beam's town on the COMMITTED
    package: the paper 16 -> 18 -> 20 (the coupled liabilities' own
    escalation), the market's own people learning the re-priced
    terms exact (the public residue), the coin untouched by the
    squeeze itself (the squeeze prices paper, never coin) — and the
    terms PERSIST at the run's end: the balance moved and stayed."""
    events, sim = _run(PACK_DIR, tmp_path, "pol_squeeze", 42, SQUEEZE)
    squeezes = [e for e in events if e.type == "account_sourced"
                and e.outcome.get("kind") == "paper"]
    assert len(squeezes) == 2
    for e in squeezes:
        assert e.actor == MASTER and e.target == MASTER
        assert e.outcome["amount"] == MARGIN
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in squeezes[0].state_changes] == [
        (MASTER, "account.paper", PAPER, PAPER + MARGIN),
    ]
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in squeezes[1].state_changes] == [
        (MASTER, "account.paper", PAPER + MARGIN, PAPER + 2 * MARGIN),
    ]
    # the public residue: the beam's own people learned, exact
    knowers = _knows(events, "the_paper_repriced")
    assert knowers
    assert all(fidelity == "exact" for _, fidelity in knowers)
    assert "npc_marketmistress_01" in {who for who, _ in knowers}
    # the terms persist; the coin untouched by the squeeze itself
    assert sim.projection[MASTER]["account.paper"] == PAPER + 2 * MARGIN
    assert sim.projection[MASTER]["account.coin"] == 3


# -- the corpus laws ----------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the genre matrix is a set of
    crafted runs — the committed pack untouched, the golden T1
    fixture byte-identical."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == golden


def test_the_probes_are_deterministic(tmp_path: Path) -> None:
    """The T1 law at the witness's own band: same seed + steps +
    pack, each run byte-identical — the journey and the refused road
    (both arms), the silent world, and the squeeze."""
    arms = [
        (PACK_DIR, "det_journey", 42, JOURNEY),
        (_genre_twin(tmp_path, "det_refused_pack"), "det_refused", 42,
         REFUSED),
        (PACK_DIR, "det_silent", 42, SILENT),
        (PACK_DIR, "det_squeeze", 42, SQUEEZE),
    ]
    for pack_dir, name, seed, steps in arms:
        first = tmp_path / f"{name}_a.jsonl"
        second = tmp_path / f"{name}_b.jsonl"
        for log in (first, second):
            pack = load_pack(pack_dir)
            sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
            sim.run_playscript({
                "name": name, "seed": seed, "pack": "province_pack@0.1",
                "steps": steps,
            })
        assert first.read_bytes() == second.read_bytes()
