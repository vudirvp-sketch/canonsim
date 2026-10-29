"""roadloop-1 (iter-440) — the first need the world CLOSES on committed
pack data: need -> offer -> the drive's own act -> the belief -> the
offer gone.

The unit the earlier iterations could only pin on a twin band is measured
here end to end: `drivegoals-1` (iter-439) made the traveller's goal the
belief `the_road_known` — three named scenes minted by `look_around`'s
own `scene_{location}` template — and INERT-FIRST held on the committed
province corpus because the drover sees one scene of the three. This
module walks him down the artery in a committed playscript and watches
the same machinery complete the goal: the board prints the need at the
crossing, the third scene mints the last token, the belief crystallizes
at that event's tick, the bar collapses to zero, the watch stops, and the
card flips to SATISFIED with no offer — while the two companions who
stayed at the crossing keep theirs.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a drive whose `measure` reads the event-driven fold is a GOAL
  the world can complete — the offer the board printed is withdrawn by
  the drive's own act, and the withdrawal is canon (the trait), not a
  timer or a script flag.
- Lens: the ticker's own arithmetic (`drive_bar`), the fold's own record
  set (`crystallized_traits`), and the two read surfaces (`assemble_brief`
  → `render_brief`'s card, `mechanics.render_offers`) — never "the log
  looks right".
- Prism: one committed playscript (`tests/playscripts/province_road.json`,
  seed 42) over the committed province pack, run in tmp — no golden, no
  twin pack, no pack byte.
- Oracle: the third distinct scene's own record event; the belief's
  sources; the bar at a cut before and at the end; the card and the script
  board read at the SAME ticks.
- Falsifier: a belief that crystallizes before the third distinct scene;
  a `look_around` by the drover after the crystallization tick; a board
  that still prints him; a card that stays OPEN; a bar above 0 with the
  belief held.
- Ablation: the SAME run's crossing cut — the pre-state is not assumed,
  it is the run's own earlier read.
- Epistemic class: FACT on the committed pack + script (seed 42).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import mechanics  # type: ignore[import-not-found]  # noqa: E402

from brief.assembler import assemble_brief, render_brief  # noqa: E402
from core.drives import DriveSpec, drive_bar, drive_specs  # noqa: E402
from core.echo import echo_scores  # noqa: E402
from core.fold import fold, initial_projection  # noqa: E402
from core.knowledge import KnowledgeView  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.offers import offers  # noqa: E402
from core.pack import load_pack  # noqa: E402
from core.traits import crystallized_traits  # noqa: E402

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
SCRIPT = REPO / "tests" / "playscripts" / "province_road.json"
DROVER = "npc_drover_01"
STAYED = ("npc_peddler_01", "npc_carrier_01")
BELIEF = "the_road_known"
CROSSING = 700  # the player's first wait ends here: the crossing's own cut


def _run(tmp_path: Path) -> tuple[Any, list[Any]]:
    """The committed script over the committed pack, in tmp. The log is
    the run's truth; nothing is read back from a fixture."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / "province_road.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript(load_playscript(SCRIPT))
    sim.close()
    _, events = read_log(log, SCHEMA)
    return pack, events


def _cut(events: list[Any], tick: int) -> list[Any]:
    return [event for event in events if event.t <= tick]


def _folds(
    pack: Any, events: list[Any], tick: int
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The two fold reads the card/board pass at a tick — the same pair
    `core.offers` takes (echo residue, event-driven traits)."""
    view = KnowledgeView()
    for event in _cut(events, tick):
        view.add(event)
    return echo_scores(pack, view, tick), crystallized_traits(pack, view, tick)


def _board(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    projection = fold(_cut(events, tick), initial_projection(pack.entities))
    echoes, traits = _folds(pack, events, tick)
    roster = [str(npc["id"]) for npc in pack.entities.get("npcs", ())]
    return offers(pack, projection, roster, echoes=echoes, traits=traits)


def _spec(pack: Any, events: list[Any], tick: int) -> DriveSpec:
    projection = fold(_cut(events, tick), initial_projection(pack.entities))
    return next(
        spec
        for spec in drive_specs(pack, projection)
        if spec.npc == DROVER
    )


def _card(text: str, npc: str) -> str:
    lines = [
        line for line in text.splitlines()
        if line.startswith("-") and npc in line and "drive=" in line
    ]
    assert lines, f"{npc} carries no card at this cut"
    return lines[0]


def _scenes(events: list[Any]) -> list[tuple[int, str, str]]:
    """The drover's own scene records: (tick, token, minting event id),
    in acquisition order — the log's arithmetic, never a recomputation."""
    out: list[tuple[int, str, str]] = []
    for event in events:
        for record in getattr(event, "knowledge", ()) or ():
            if record.who != DROVER:
                continue
            if not str(record.knows).startswith("scene_"):
                continue
            out.append((event.t, str(record.knows), event.id))
    return out


def _first_acquisition(
    scenes: list[tuple[int, str, str]]
) -> tuple[dict[str, int], dict[str, str]]:
    ticks: dict[str, int] = {}
    minters: dict[str, str] = {}
    for tick, token, event_id in scenes:
        ticks.setdefault(token, tick)
        minters.setdefault(token, event_id)
    return ticks, minters


# -- (1) the pre-state: the crossing prints the open need --------------------


def test_the_crossing_prints_the_open_need(tmp_path: Path) -> None:
    """The world at the crossing: the drive's measure (the belief) fails,
    the bar is the full weight times the one unmet row, the card reads
    OPEN and the board prints the closing act — the need exists before
    anything closes it."""
    pack, events = _run(tmp_path)
    board = _board(pack, events, CROSSING)
    # iter-445: the smith's payment need is canon from the first beat (his
    # fund is short of the charcoal paper's sixteen) and no committed script
    # brings the reader to the crofts — it is the board's permanent fourth
    # need, never part of this receipt.
    assert {offer.npc for offer in board} == {DROVER, *STAYED, "npc_smelter_01"}
    mine = next(offer for offer in board if offer.npc == DROVER)
    assert mine.drive == "scan_the_road"
    assert mine.verb == "look_around"
    assert mine.payable is None  # a knowledge act declares no stock terms
    # needphrase-2 (iter-447): the sentence is the ROLE's own — the born
    # traveller carries no dossier, so the drive row supplies the phrase.
    assert mine.need == "the road known"
    assert mine.segments() == (
        "offer=look_around", "payable=?", "need=the road known",
    )
    spec = _spec(pack, events, CROSSING)
    echoes, traits = _folds(pack, events, CROSSING)
    projection = fold(_cut(events, CROSSING), initial_projection(pack.entities))
    # the born profile's openness 85 sits in the 200 % band: 20 -> 40, and
    # the one unmet measure row makes the bar the weight (deficit 1)
    assert drive_bar(
        spec, pack, projection, echoes=echoes, traits=traits,
    ) == 40
    card = _card(render_brief(assemble_brief(_cut(events, CROSSING), pack)), DROVER)
    assert "drive=scan_the_road:OPEN" in card
    assert "offer=look_around payable=?" in card


# -- (2) the road mints its three scenes -------------------------------------


def test_the_road_mints_exactly_its_three_scenes(tmp_path: Path) -> None:
    """The goal's evidence is the pack's own family, learned by the drive's
    own act: exactly the three declared scene tokens, each minted by a
    `look_around` event (never an authored fact), in the declaration
    order of the road — the artery, the crossing, the market."""
    pack, events = _run(tmp_path)
    family = list(
        pack.rules["traits"]["beliefs"][BELIEF]["family"]
    )
    scenes = _scenes(events)
    ticks, minters = _first_acquisition(scenes)
    assert set(ticks) == set(family)
    assert [token for token, _ in sorted(ticks.items(), key=lambda kv: kv[1])] == family
    for event_id in minters.values():
        event = next(event for event in events if event.id == event_id)
        assert event.type == "look_around"
        assert event.actor == DROVER


# -- (3) the third scene crystallizes the belief -----------------------------


def test_the_third_scene_crystallizes_the_belief(tmp_path: Path) -> None:
    """The fold's own law: one scene short is not a belief; the third
    scene's own event is the tick the belief appears, and its provenance
    is the records that minted the family (the duplicate weir-stair look
    contributes a source, never a second breadth token)."""
    pack, events = _run(tmp_path)
    family = list(pack.rules["traits"]["beliefs"][BELIEF]["family"])
    ticks, minters = _first_acquisition(_scenes(events))
    third = ticks[family[2]]
    view = KnowledgeView()
    for event in _cut(events, third - 1):
        view.add(event)
    before = crystallized_traits(pack, view, third - 1)
    assert [trait for trait in before if trait.who == DROVER] == []
    view = KnowledgeView()
    for event in _cut(events, third):
        view.add(event)
    at = crystallized_traits(pack, view, third)
    belief = next(
        trait for trait in at
        if trait.who == DROVER and trait.token == BELIEF
    )
    assert set(minters.values()) <= set(belief.sources)


# -- (4) a met goal stops pushing --------------------------------------------


def test_the_met_goal_stops_the_watch(tmp_path: Path) -> None:
    """The continuity law on canon: after the belief's tick the traveller
    no longer looks — the drive's bar is zero, so the ticker enqueues
    nothing, and the log's remaining beats carry no `look_around` of his.
    The silence band is counted, not assumed."""
    pack, events = _run(tmp_path)
    family = list(pack.rules["traits"]["beliefs"][BELIEF]["family"])
    ticks, _ = _first_acquisition(_scenes(events))
    third = ticks[family[2]]
    after = [event for event in events if event.t > third]
    assert len(after) >= 20
    assert [
        event for event in after
        if event.type == "look_around" and event.actor == DROVER
    ] == []
    end = events[-1].t
    spec = _spec(pack, events, end)
    echoes, traits = _folds(pack, events, end)
    projection = fold(events, initial_projection(pack.entities))
    assert drive_bar(spec, pack, projection, echoes=echoes, traits=traits) == 0


# -- (5) the receipt: the card flips and the board drops him -----------------


def test_the_card_flips_and_the_board_drops_him(tmp_path: Path) -> None:
    """The readable receipt: the same card that read OPEN at the crossing
    reads SATISFIED with no `offer=` at the market, the oracle board
    keeps the two companions who never left the crossing, and the read is
    the same sentence on both surfaces (`Offer.segments` is the one
    owner)."""
    pack, events = _run(tmp_path)
    card = _card(render_brief(assemble_brief(events, pack)), DROVER)
    assert "drive=scan_the_road:SATISFIED" in card
    assert "offer=" not in card
    board = _board(pack, events, events[-1].t)
    assert {offer.npc for offer in board} == {*STAYED, "npc_smelter_01"}
    out = mechanics.render_offers(pack, events)
    assert "3 need(s)" in out
    assert DROVER not in out
    for npc in STAYED:
        assert f"{npc} · scan_the_road · offer=look_around payable=?" in out
    before = mechanics.render_offers(pack, events, at_tick=CROSSING)
    assert "4 need(s)" in before
    assert f"{DROVER} · scan_the_road · offer=look_around payable=?" in before
