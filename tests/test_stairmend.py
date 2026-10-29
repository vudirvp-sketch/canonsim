"""stairmend-1 (iter-444) — the receipt's PAID half on committed content:
the unread year's water -> the reader at the stair -> the office's door taken
by the player's hand -> the wear cleared -> the need gone.

`keeperarm-1` (iter-443, D-289) armed the content, but no committed playscript
stood the player at the crossing after the year's water, so the armed read
could only be pinned on a projection. This module walks it: a year passes
while the player waits on the river road (the wear accrues 0 -> 2, unread by
any door), he walks to the stair, the board offers him the OFFICE's own act
(`mend_the_stair`, `payable` from the recipe's wear leg, no blocker at the
stair), he takes it, the convert clears the wear 2 -> 0 and pays the keeper
her wage, and the keeper's drive measure is met — the card flips OPEN ->
SATISFIED with no offer and the board drops her.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a need whose OWNER cannot close it is closed by the READER on
  committed pack data — the offer the board prints is the office's door, the
  reader's presence is the gate, and the closure is the recipe's own
  arithmetic (wear -2, the guild's chest -3, the keeper +1), never a script
  flag.
- Lens: the account trail (the flow's source, the convert's legs), the two
  read surfaces (the card, `mechanics.render_offers`) at the SAME cuts, and
  the drive's own bar.
- Prism: one committed playscript (`tests/playscripts/province_stairmend.json`,
  seed 42) over the committed province pack, run in tmp — no golden, no twin
  pack, no pack byte.
- Oracle: the state changes the log records; the recipe's declared legs; the
  measure's own verdict (`account_at_most wear 1`).
- Falsifier: a wear above 2 before the year's crossing; a mend without the
  player at the stair; a convert with legs other than the recipe's; an offer
  that survives the mend; a card that stays OPEN with the wear at 0.
- Ablation: the SAME run's own earlier cut (the reader still on the road) —
  the pre-state is the log's own read, not an assumption.
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
from core.drives import drive_bar, drive_specs  # noqa: E402
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
SCRIPT = REPO / "tests" / "playscripts" / "province_stairmend.json"
KEEPER = "npc_weirkeeper_01"
PLAYER = "pc_01"
STAIR = "loc_weirstair"
CHEST = "loc_malby"
WAGE = 1
MEND_COIN = 3
WEAR_STEP = 2


def _run(tmp_path: Path, name: str = "stairmend.jsonl") -> tuple[Any, list[Any], Any]:
    """The committed script over the committed pack, in tmp. The log is the
    run's truth; nothing is read back from a fixture."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(load_playscript(SCRIPT))
    sim.close()
    _, events = read_log(log, SCHEMA)
    return pack, events, result


def _cut(events: list[Any], tick: int) -> list[Any]:
    return [event for event in events if event.t <= tick]


def _folds(
    pack: Any, events: list[Any], tick: int
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The two fold reads the card and the board pass at a tick — the same
    pair `core.offers` takes (echo residue, event-driven traits)."""
    view = KnowledgeView()
    for event in _cut(events, tick):
        view.add(event)
    return echo_scores(pack, view, tick), crystallized_traits(pack, view, tick)


def _board(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    projection = fold(_cut(events, tick), initial_projection(pack.entities))
    echoes, traits = _folds(pack, events, tick)
    roster = [str(npc["id"]) for npc in pack.entities.get("npcs", ())]
    return offers(pack, projection, roster, echoes=echoes, traits=traits)


def _keeper_offer(pack: Any, events: list[Any], tick: int) -> Any:
    return next(
        (offer for offer in _board(pack, events, tick) if offer.npc == KEEPER),
        None,
    )


def _card(text: str, npc: str) -> str:
    lines = [
        line for line in text.splitlines()
        if line.startswith("-") and npc in line and "drive=" in line
    ]
    assert lines, f"{npc} carries no card at this cut"
    return lines[0]


def _trail(events: list[Any], entity: str, kind: str) -> list[Any]:
    return [
        (event.t, event.type, change.from_, change.to_)
        for event in events
        for change in event.state_changes
        if change.entity == entity and change.prop.endswith(kind)
    ]


def _ticks(pack: Any, events: list[Any]) -> tuple[int, int, int]:
    """The run's three cuts, read from the log: the year's crossing (the
    flow's own source), the reader's arrival (his move), the mend."""
    year = next(
        event.t for event in events
        if event.type == "account_sourced"
        and any(
            change.entity == STAIR for change in event.state_changes
        )
    )
    move = next(
        event.t for event in events
        if event.type == "move" and event.actor == PLAYER
    )
    mend = next(
        event.t for event in events if event.type == "account_converted"
    )
    return year, move, mend


# -- (1) the year's water stands on the stair, unread and unpaid ------------


def test_the_years_water_stands_unread_and_the_reader_is_the_gate(
    tmp_path: Path,
) -> None:
    """The flow is the world's, not an act's: the stair sources wear 0 -> 2
    at the macro crossing with no actor, and the need stands in the world
    before anyone walks to it. The reader is still on the road — the board
    prints the offer (the need is real) but WITH the reader's own gate: he
    is not at the stair, so the door would refuse him."""
    pack, events, _ = _run(tmp_path)
    year, move, _mend = _ticks(pack, events)
    assert _trail(events, STAIR, "wear")[0] == (year, "account_sourced", 0, WEAR_STEP)
    before = _keeper_offer(pack, events, year + 1)
    assert before is not None
    assert before.verb == "mend_the_stair"
    assert before.payable is True
    assert before.segments() == (
        "offer=mend_the_stair 2/1",
        "blocked=target.same_location",
        "need=the stair's wear cleared",
    )
    # the reader is not there yet, and the year's crossing precedes his walk
    assert move > year


# -- (2) the reader at the stair: the office's door, free -------------------


def test_the_reader_at_the_stair_sees_a_free_offer(tmp_path: Path) -> None:
    """The same offer one move later: the blocker is gone (the reader
    stands at the stair), the terms are the recipe's, and the card carries
    the board's own sentence — `drive=keep_the_crossing:OPEN`, the offer,
    the need phrase — the need is open because the wear is above its
    bound."""
    pack, events, _ = _run(tmp_path)
    _year, move, mend = _ticks(pack, events)
    assert move < mend
    arrival = move + 1
    offer = _keeper_offer(pack, events, arrival)
    assert offer is not None
    assert offer.segments() == (
        "offer=mend_the_stair 2/1",
        "need=the stair's wear cleared",
    )
    card = _card(
        render_brief(assemble_brief(_cut(events, arrival), pack)), KEEPER
    )
    assert "drive=keep_the_crossing:OPEN" in card
    assert "offer=mend_the_stair 2/1" in card
    assert "need=the stair's wear cleared" in card
    # the bar is the keeper's own diligence: base 12 x 150 % (deficit 1)
    projection = fold(_cut(events, arrival), initial_projection(pack.entities))
    spec = next(
        spec for spec in drive_specs(pack, projection) if spec.npc == KEEPER
    )
    echoes, traits = _folds(pack, events, arrival)
    assert drive_bar(
        spec, pack, projection, echoes=echoes, traits=traits,
    ) == 18


# -- (3) the owner reads, and cannot close it -------------------------------


def test_the_owner_reads_and_cannot_close_it(tmp_path: Path) -> None:
    """The third-party thesis on the log itself (iter-443's own-verb law):
    while the wear stands above its bound the KEEPER's own drive fires —
    `read_stair`, her only honest act about it — and the read moves NO
    stock: the wear is still 2 until the player takes the office's door.
    Her first read mints the step law for herself (the act's own knowledge,
    never the wear's bookkeeping)."""
    pack, events, _ = _run(tmp_path)
    _year, move, mend = _ticks(pack, events)
    reads = [
        event for event in events
        if event.actor == KEEPER and event.type == "stair_read"
    ]
    assert reads, "the keeper's own read never fired at the stair"
    first = reads[0]
    assert move < first.t < mend
    assert first.target == STAIR
    assert [(record.who, record.knows) for record in first.knowledge] == [
        (KEEPER, "the_step_law"),
    ]
    wear = [
        (change.from_, change.to_)
        for event in events
        for change in event.state_changes
        if change.entity == STAIR and change.prop.endswith("wear")
    ]
    assert wear == [(0, WEAR_STEP), (WEAR_STEP, 0)]  # her read changed nothing


# -- (4) the hand takes the office's door: the recipe's own arithmetic ------


def test_the_hand_takes_the_office_door(tmp_path: Path) -> None:
    """The convert as ONE atomic act, the player for the actor: wear 2 -> 0
    off the crossing, the guild's chest -3, the keeper +1 (the labour's
    wage) — exactly `the_mend`'s declared legs, never a term the card
    invented. The co-present keeper learns `the_stair_mended`, and the
    STEP account is untouched by the mend (the named boundary: the standing
    head is the keeper's own door)."""
    pack, events, _result = _run(tmp_path)
    mends = [event for event in events if event.type == "account_converted"]
    assert len(mends) == 1
    mend = mends[0]
    assert mend.actor == PLAYER and mend.target == STAIR
    assert mend.outcome["recipe"] == "the_mend"
    changes = {(change.entity, change.prop): change for change in mend.state_changes}
    wear = changes[(STAIR, "account.wear")]
    assert (wear.from_, wear.to_) == (WEAR_STEP, 0)
    chest = changes[(CHEST, "account.coin")]
    assert chest.to_ == chest.from_ - MEND_COIN
    keeper = changes[(KEEPER, "account.coin")]
    assert keeper.to_ == keeper.from_ + WAGE
    # the recipe's declared input/output legs ARE the movement
    assert mend.outcome["inputs"] == [
        {"holder": STAIR, "kind": "wear", "amount": WEAR_STEP},
        {"holder": CHEST, "kind": "coin", "amount": MEND_COIN},
    ]
    assert mend.outcome["outputs"] == [
        {"holder": KEEPER, "kind": "coin", "amount": WAGE},
    ]
    # the standing head is NOT touched by this act (the maintenance boundary)
    assert not [
        change for change in mend.state_changes
        if change.prop == "account.step"
    ]
    assert [(record.who, record.knows) for record in mend.knowledge] == [
        (KEEPER, "the_stair_mended"),
    ]


# -- (5) the met measure drops the need from both surfaces ------------------


def test_the_mended_crossing_drops_the_need(tmp_path: Path) -> None:
    """The receipt's closure: the measure `account_at_most wear 1` is MET
    (the wear is 0), so the continuity law zeroes the bar, the card flips
    OPEN -> SATISFIED with no `offer=`, the board drops the keeper, and the
    oracle's own listing loses her — while the act's earlier cut still had
    her (the same run, never a twin)."""
    pack, events, _ = _run(tmp_path)
    _year, move, mend = _ticks(pack, events)
    assert _keeper_offer(pack, events, events[-1].t) is None
    card = _card(render_brief(assemble_brief(events, pack)), KEEPER)
    assert "drive=keep_the_crossing:SATISFIED" in card
    assert "offer=" not in card
    projection = fold(events, initial_projection(pack.entities))
    spec = next(
        spec for spec in drive_specs(pack, projection) if spec.npc == KEEPER
    )
    echoes, traits = _folds(pack, events, events[-1].t)
    assert drive_bar(
        spec, pack, projection, echoes=echoes, traits=traits,
    ) == 0
    # the oracle board, before and after, on the SAME run
    before = mechanics.render_offers(pack, events, at_tick=move + 1)
    assert (
        f"{KEEPER} · keep_the_crossing · offer=mend_the_stair 2/1 "
        "need=the stair's wear cleared" in before
    )
    after = mechanics.render_offers(pack, events)
    assert KEEPER not in after
    assert mend < events[-1].t


# -- (6) INV-2: the walk is byte-identical across twins ---------------------


def test_the_walk_is_byte_identical_across_twins(tmp_path: Path) -> None:
    """The same script twice, the same bytes; the run's fingerprints agree
    (the determinism law over the new committed artifact)."""
    arms = []
    for name in ("a.jsonl", "b.jsonl"):
        _pack, events, result = _run(tmp_path, name)
        arms.append((result.fingerprint, (tmp_path / name).read_bytes()))
    assert arms[0][1] == arms[1][1]
    assert arms[0][0] == arms[1][0]
