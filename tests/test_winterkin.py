"""winterkin — the W5 heartbreak station's design material (iter-203,
the owner's queue-order call «withhold → the heartbreak probe» firing
STATUS Next step item 1, the station's second row): the winter kin's
embodiment landed as PURE PACK DATA over the committed substrate —
ANCHOR_REGION §6.3's three first-exposure gaps answered on the
intake-36 C03+F02 consult's named machinery (on_action deltas + pair
axes + requires gates — the threshold's bar the on_action arithmetic's
own number), zero core change (the KI#87 precedent class).

The three gaps, answered:

- the RELATION FORM: the `kin` pair axis (rules.relations.axes) — the
  recognized standing's own measure, never a trust value; the seeded
  bilateral edge (the toll-taker and the flood-year guest's son, both
  carrying the inherited 40 — the drowned generation's notch now the
  toll-taker's holding, the guests' children carrying the same
  duties).
- the PROOF'S READ: `read_kinmark` — the read hinge family's fifth
  instance (the pole's SECOND story: the payment tallies the flood
  story, the guest count the winter kin), minting the literal token
  `the_winter_kin` — the secrets registry's fourth key, a CARE debt
  over the house that sheltered (the notch prices care, never coin).
- the MOURNING SURFACE: `say_the_names` — the drowned generation's
  names said aloud at the crossing's table, the grief given its second
  holder (the seeded-entry gap answered by the token + the beat, the
  the_flood_story precedent's family — the grievance axis deliberately
  not ridden: the wergeld ratio's two houses stay two).

The formation side (the C03 triple — repeated consequential
co-presence × reciprocity × selective disclosure) tested IN A COMMITTED
PACK for the first time: the winter's board (`share_board`) moves the
kin axis through the on_action table (both sides climbing — the
guests' kin toward the host, the host's counter-climb), four sharings
carrying the inherited 40 to the recognition bar 80; the claim
(`claim_kinmark`) is the F02 criterion's mechanical form — the
leverage-gated door only the proof-holder passes, the edge's expansion
of future legal options.

The claim packet (TEST_PLAN §9):

- Claim: the winter kin's chain is one pack-data arming — the relation
  form (the axis + the bilateral seed), the formation mechanism (the
  board's two climbs), the proof (the second read of the pole), the
  claim's door (the leverage gate), the mourning (the names said) —
  the heartbreak's surfaces (the loss: the drowned generation, carried
  on the committed cause fields; the memory: the names kept by name
  outside the bloodline; the future option: the claim, the option no
  other mechanism expresses), zero core.
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader of the return's tale sees the claim and what it
  completes; the designer reads the kin axis's two paths to the bar:
  the winter's board or the claim's echo); the boundary lens (the
  rarity gate held — the ordinary winter prices nothing, the verb
  season-blind but the numeric-home law filtering to the seeded pair;
  the recognition's release-hook form PARKED — hooks seed only from
  committed event tags (D-005) and no resolver mints knowledge and
  hooks on one success branch, the constraint recorded in
  director.notes — the bilateral climb the used form).
- Prism: the committed-pack census; the formation walk (the stranded
  winter's four sharings); the return walk (the read's fail-then-pass,
  the claim, the echo, the mourning); the proof-less claimant (the
  door's falsifier); the golden corpus (the price PAID deliberately —
  the son at the crofts hears the wergeld count, the murmur's
  knowledge line the byte-diff).
- Oracle: the event log scans (the climbs' from_/to_ pairs, the
  intent_rejected's failed_test), the projection reads, the tale
  render, the byte-compares.
- Falsifier: the kin climb touching a coin fund or an unseeded pair
  (the numeric-home law broken); the claim passing without the proof
  (the door's edge gone); the goldens shifting outside the recorded
  murmur line (an unrecorded price).
- Expected evidence: the census pins; the formation's bilateral climb
  exactly (40→80 both sides over four sharings, both echo lines in the
  tale); the return's chain (the failed read, the proof, the claim,
  Ketta's side completing at the echo 40→80, the names line); the
  proof-less claim refused (attempts are facts); the smoke golden
  byte-identical to the regenerated fixture.
- Observed evidence: CONFIRMED at the measured band (seed 42).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded: the
  recognition's release-hook form parked — the seeding law's
  constraint; the purse question's exclusion rung rides the authored
  law, no pair-prop requires test exists — the probe's audit
  vocabulary; the heartbreak PROBE itself the station's next beat, the
  surface it reads now committed).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

TORK = "npc_winterkin_01"
KETTA = "npc_weirkeeper_01"
POLE = "punt_pole_01"
STAIR = "loc_weirstair"

#: the kin axis's two paths to the bar: the winter's board (four
#: sharings x +10 on both sides) and the claim's echo (+40 on the
#: host's side alone) — the on_action arithmetic the bar's only owner.
BOARD_CLIMB: tuple[tuple[int, int, int], ...] = (
    (40, 50, 50),  # (tork_from, tork_to, ketta_to) at sharing 1
    (50, 60, 60),
    (60, 70, 70),
    (70, 80, 80),
)


def _run(
    tmp_path: Path, name: str, steps: list[dict[str, Any]]
) -> tuple[list, Any, Simulator]:
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": 42, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, pack, sim


def _walk_to_the_stair() -> list[dict[str, Any]]:
    """The return's walk: the crofts' man down-country to the crossing
    his father wintered at (the artery's walk, the travel twin's own
    pricing)."""
    return [
        {"intent": "move", "actor": TORK, "target": "loc_keep"},
        {"intent": "move", "actor": TORK, "target": "loc_riverroad"},
        {"intent": "move", "actor": TORK, "target": STAIR},
    ]


# -- the census (the arming as pack data) ---------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the kin axis
    (the relation form — §6.3's gap answered with its OWN measure,
    never a trust value), the bilateral seed (the inherited edge, both
    sides at 40 — the recognition pending), the son (the named
    stranger, the crofts' tongue, no generated_name), the four actions
    (the board, the proof's read, the claim, the mourning), the two
    formation entries + the claim's echo (the kin axis's ONLY movers),
    the fourth secret (the care debt over the house that sheltered),
    the tale lines story-critical, the budget's honest re-declares."""
    pack = load_pack(PACK_DIR)
    rules = pack.rules
    # the relation form: the fifth axis
    assert rules["relations"]["axes"] == [
        "reputation", "suspicion", "trust", "fear", "kin",
    ]
    ketta = next(n for n in pack.entities["npcs"] if n["id"] == KETTA)
    tork = next(n for n in pack.entities["npcs"] if n["id"] == TORK)
    assert {p["with"]: p["kin"] for p in ketta["pair_relations"]
            if "kin" in p} == {TORK: 40}
    assert {p["with"]: p["kin"] for p in tork["pair_relations"]
            if "kin" in p} == {KETTA: 40}
    assert tork["position"] == "loc_crofts"  # the crofts' tongue
    assert "generated_name" not in tork  # the fixed name, the claim's surface
    assert tork["spine"]["cause"].startswith("the flood year stranded")
    # the actions: the board, the fifth read hinge, the claim, the mourning
    intents = {a["intent"] for a in pack.data["actions.json"]["actions"]}
    assert {"share_board", "read_kinmark", "claim_kinmark",
            "say_the_names"} <= intents
    # the kin axis's ONLY movers: the two formation entries + the echo
    board = rules["on_action"]["board_shared"]
    assert [(e["event"], e["state"]["prop"], e["state"]["add"])
            for e in board] == [
        ("kin_stirs", f"pair.{KETTA}.kin", 10),
        ("the_house_answers", f"pair.{TORK}.kin", 10),
    ]
    echo = rules["on_action"]["kinmark_claimed"]
    assert [(e["event"], e["state"]["prop"], e["state"]["add"])
            for e in echo] == [
        ("the_edge_answers", f"pair.{TORK}.kin", 40),
    ]
    # the fourth secret: the care debt over the toll-taker
    assert rules["secrets"]["tokens"]["the_winter_kin"] == {
        "subject": KETTA, "type": "debt", "expires_ticks": 129600,
    }
    # the tale lines story-critical
    for line in ("board_shared", "kin_stirs", "the_house_answers",
                 "kinmark_read", "kinmark_claimed", "the_edge_answers",
                 "the_names_kept"):
        assert line in rules["importance"]["story_critical_events"]
    # the budget's honest re-declares: the cast at twelve, the ceiling
    # widened for the crafted-successor twin, the templates at 75
    assert len(pack.entities["npcs"]) == 12
    assert rules["budget"]["npcs"] == {"min": 7, "max": 13}
    assert rules["budget"]["templates"]["max"] == 75
    assert len(pack.templates["events"]) == 75


# -- the formation walk (the C03 triple, live) -----------------------------------


def test_the_formation_walks_the_winter(tmp_path: Path) -> None:
    """The formation side tested in a committed pack — the C03 triple's
    co-presence factor walked live: four sharings of the winter's board
    climb the kin axis BILATERALLY (the guests' side and the host's
    counter-climb — the care flowing one way, the duties flowing
    back), both sides crossing the recognition bar 80 together at the
    fourth sharing; the tale carries the winter's rhythm (the board,
    the kin stirring, the house answering — the formation's own
    texture)."""
    events, _pack, sim = _run(tmp_path, "formation.jsonl", _walk_to_the_stair() + [
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "say_the_names", "actor": TORK, "target": POLE},
    ])
    sim.close()
    stirs = [e for e in events if e.type == "kin_stirs"]
    answers = [e for e in events if e.type == "the_house_answers"]
    assert len(stirs) == len(answers) == 4
    # the bilateral climb, exact: both sides 40 -> 80 over the winter
    for i, (st, an) in enumerate(zip(stirs, answers, strict=True)):
        t_from, t_to, k_to = BOARD_CLIMB[i]
        assert (st.state_changes[0].entity, st.state_changes[0].prop,
                st.state_changes[0].from_, st.state_changes[0].to_) == (
            TORK, f"pair.{KETTA}.kin", t_from, t_to)
        assert (an.state_changes[0].entity, an.state_changes[0].prop,
                an.state_changes[0].from_, an.state_changes[0].to_) == (
            KETTA, f"pair.{TORK}.kin", t_from, k_to)
    assert sim.projection[TORK][f"pair.{KETTA}.kin"] == 80
    assert sim.projection[KETTA][f"pair.{TORK}.kin"] == 80
    # the mourning: the recognition's enactment (the duty performed)
    names = [e for e in events if e.type == "the_names_kept"]
    assert len(names) == 1 and names[0].actor == TORK


def test_the_formation_tale_carries_the_winters_rhythm(tmp_path: Path) -> None:
    """The changed-next-decision unit, rendered: the tale carries the
    formation's texture — the board's line, the kin stirring, the
    house answering (the bilateral climb made prose), and the mourning
    line (the drowned generation's names kept by name outside the
    bloodline, their line, their duties and their holdings never
    handed on — the loss's future-option dimension on the reader
    surface, iter-205's rendering fix)."""
    events, pack, sim = _run(tmp_path, "tale.jsonl", _walk_to_the_stair() + [
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "share_board", "actor": KETTA, "target": TORK},
        {"intent": "say_the_names", "actor": TORK, "target": POLE},
    ])
    sim.close()
    tale = render_chronicle(events, pack, seed=42)
    assert tale.count(
        "Ketta shares the winter's board with Tork at the weir stair"
        " — the shelter law's meal, the stores eaten against the debt."
    ) == 4
    assert tale.count(
        "The old kin stirs at the weir stair — the winter's board"
        " answering the drowned generation's notch, care's recipient"
        " bound to its bearer."
    ) == 4
    assert tale.count(
        "The toll-taker's house answers at the weir stair — the"
        " winter's board eaten against the debt, the notch's own count"
        " kept, the edge standing both ways."
    ) == 4
    assert (
        "Tork says the drowned generation's names at the weir stair —"
        " the flood year's dead kept by name outside the bloodline,"
        " their line, their duties and their holdings never handed on,"
        " the grief given its second holder." in tale
    )


# -- the return walk (the heartbreak's chain) ------------------------------------


def test_the_return_claims_the_edge(tmp_path: Path) -> None:
    """The return's chain, exact: the honest failure surface first (the
    read failing at seed 42 — the marks staying marks, the perception
    gate the poleseed precedent's own law), then the proof (the second
    read minting the_winter_kin to the reader ALONE — the selective
    disclosure), then the claim (the door's lever spent aloud where
    the road can hear), then the echo (the host's side completing at
    the bar — 40 + 40 = 80, the rarity gate intact: the claim answers
    the generation-old notch, no new winter), then the mourning (the
    duty performed). The echo line carries the opened forward
    possibility (the crossing's table open to the claimant's line —
    iter-205's rendering fix, never only the present standing). The
    son's own side stays 40 — the honest state:
    his own winter not spent, the carried edge's claim answered."""
    events, _pack, sim = _run(tmp_path, "return.jsonl", _walk_to_the_stair() + [
        {"intent": "read_kinmark", "actor": TORK, "target": POLE},
        {"intent": "read_kinmark", "actor": TORK, "target": POLE},
        {"intent": "claim_kinmark", "actor": TORK, "target": KETTA},
        {"intent": "say_the_names", "actor": TORK, "target": POLE},
    ])
    sim.close()
    # the honest failure surface, then the proof
    reads = [e for e in events if e.type.startswith("kinmark_read")]
    assert [e.type for e in reads] == ["kinmark_read_failed", "kinmark_read"]
    proof = reads[1]
    assert [(k.who, k.knows) for k in proof.knowledge] == [
        (TORK, "the_winter_kin"),
    ]
    # the claim: the road hears (the token public, the counter-record spent)
    claim = next(e for e in events if e.type == "kinmark_claimed")
    assert claim.actor == TORK and claim.target == KETTA
    heard = {k.who for k in claim.knowledge}
    assert {KETTA, TORK, "npc_secondhand_01"} <= heard
    # the echo: the host's side completing at the bar
    echo = next(e for e in events if e.type == "the_edge_answers")
    assert (echo.state_changes[0].entity, echo.state_changes[0].prop,
            echo.state_changes[0].from_, echo.state_changes[0].to_) == (
        KETTA, f"pair.{TORK}.kin", 40, 80,
    )
    assert sim.projection[KETTA][f"pair.{TORK}.kin"] == 80
    assert sim.projection[TORK][f"pair.{KETTA}.kin"] == 40  # the honest state
    # the mourning: the names said
    assert any(e.type == "the_names_kept" for e in events)
    # the tale: the heartbreak's own lines
    tale = render_chronicle(events, load_pack(PACK_DIR), seed=42)
    assert (
        "Tork reads the kin notch on the punt pole's haft — the"
        " winter's guests cut into the family's count, the same blade,"
        " the same staff, the flood-year mark a generation deep." in tale
    )
    assert (
        "Tork claims the kin notch at the weir stair — the flood-year"
        " guest's son at the crossing his father wintered at, the proof"
        " shown where the road can hear." in tale
    )
    assert (
        "The old edge answers at the weir stair — the toll-taker's"
        " house holding the drowned generation's notch, the recognition"
        " the claim completes, the crossing's table open to the"
        " claimant's line from this day." in tale
    )


def test_the_proofless_claimant_is_refused(tmp_path: Path) -> None:
    """The F02 criterion's mechanical edge, falsified: the proof-less
    claimant (the runner at the stair, no the_winter_kin cluster over
    the toll-taker) is refused SOFTLY at the door — the intent_rejected
    event the fact, the failed test the leverage gate (attempts are
    facts; the option's edge is real: only the proof-holder may
    claim)."""
    events, _pack, sim = _run(tmp_path, "falsifier.jsonl", [
        {"intent": "move", "target": STAIR},
        {"intent": "claim_kinmark", "target": KETTA},
    ])
    sim.close()
    rejected = [e for e in events if e.type == "intent_rejected"]
    assert len(rejected) == 1
    assert rejected[0].actor == "pc_01"
    assert rejected[0].outcome == {
        "action": "claim_kinmark", "reason": "precondition",
        "failed_test": "actor.leverage_over",
    }


# -- the corpus price + the determinism ------------------------------------------


def test_the_corpus_price_paid_deliberately() -> None:
    """The price recorded, not hidden: the son at the crofts HEARS the
    wergeld count (the ambient murmur's same_location knowledge line —
    the crofts' man hearing the blood price is canonical world state),
    the smoke golden regenerated with exactly that delta (the iter-157
    precedent's own law — the companion's arrival paid the same class
    of price); the fixture committed is the fresh run's bytes."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "smoke.jsonl"
        sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
        sim.run_playscript(script)
        sim.close()
        assert log.read_bytes() == golden
    # the delta's own shape: the murmur's knowers now include the son
    _, events = read_log(
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl", SCHEMA
    )
    murmur = next(e for e in events if e.type == "ramble"
                  and e.actor == "npc_smelter_01")
    assert any(k.who == TORK and k.knows == "rambling_by_npc_smelter_01"
               for k in murmur.knowledge)


def test_the_walks_are_deterministic(tmp_path: Path) -> None:
    """The T1 law at the walk's own band: same seed + steps +
    environment, byte-identical logs (the return's chain the probe's
    package source — the instrument deterministic)."""
    steps = _walk_to_the_stair() + [
        {"intent": "read_kinmark", "actor": TORK, "target": POLE},
        {"intent": "read_kinmark", "actor": TORK, "target": POLE},
        {"intent": "claim_kinmark", "actor": TORK, "target": KETTA},
        {"intent": "say_the_names", "actor": TORK, "target": POLE},
    ]
    for name in ("det_a", "det_b"):
        _run(tmp_path, f"{name}.jsonl", steps)
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
