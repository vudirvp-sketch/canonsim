"""debtpaid-1 (iter-445) — the payment stripe: the READER pays a PERSON, and
the need's own number moves; the world's own clock finishes what the purse
could not.

The receipt's paid half had one gap left (iter-441 M3 measured it): no
committed verb moved coin from an actor to a PERSON, so a need whose closure
is a payment could only be pinned on a twin. This unit closes it with pack
data: the smith's debt drive measures his own coin fund (the charcoal paper's
sixteen) and declares `helper_verb=pay_the_bloom` — the buyer's transfer to
his person, off the weighbeam. This module walks the whole stripe: the offer
at the start, the two payments (the coin's walk and the co-present word), the
purse's own refusal at the third, and the years' climb that finishes the fund
— after which the debt's offer is gone and the smith's pursuit reverts to his
craft (the continuity law: a met goal stops pushing).

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a person's need is payable by the READER on committed pack data — a
  declared `transfer` verb feeds the measured fund, the need's own number
  moves by exactly the act's legs, the reader's PURSE is the door's gate, and
  the need closes when the world's clock (the fund's yearly net) covers the
  rest.
- Lens: the account trail (the transfer's legs, the yearly source), the two
  read surfaces (the card, `mechanics.render_offers`), the drive's own bar.
- Prism: one committed playscript (`tests/playscripts/province_debtpaid.json`,
  seed 42) over the committed province pack, run in tmp — no golden, no twin
  pack, no pack byte.
- Oracle: the log's `state_changes`; the transfer's declared legs; the
  measure's own verdict.
- Falsifier: a payment whose legs are not the declared ones; a card whose
  number does not move with the stock; a refusal by any gate but the player's
  own purse; a `pay_the_bloom` offer surviving a met measure; a craft drive
  that stays silent with the wood grown.
- Ablation: the same run's own earlier cuts (the offer before the walk, the
  board between the two payments).
- Epistemic class: FACT on the committed pack + script (seed 42).

RESIDUE, CLOSED (iter-446, `needphrase-1`): the board's `need=` phrase was
the RECORD's `spine.need` — one phrase per person — so when a two-pursuit
smith's CRAFT drive became dominant (the grown wood, after the debt was met),
the craft offer printed the debt's (now PAID) words beside it. The owning
unit gave the drive row its own optional `need` phrase (read first, the
record the fallback) and a lint law that refuses two OFFERABLE pursuits of
one person resolving to the same sentence; `tests/test_needphrase.py` walks
the flip on this very script (the debt's phrase at t=1180, the coppice's own
at the end) and the law's refusals.
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
from core.agenda import agenda_view  # noqa: E402
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
SCRIPT = REPO / "tests" / "playscripts" / "province_debtpaid.json"
SMELTER = "npc_smelter_01"
PLAYER = "pc_01"
WITNESS = "npc_winterkin_01"
FUND = "see_the_debt_paid"
PAY = "pay_the_bloom"
PRICE = 3
PAPER = 16
NEED = "the charcoal debt repaid"


def _run(tmp_path: Path, name: str = "debtpaid.jsonl") -> tuple[Any, list[Any], Any]:
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
    view = KnowledgeView()
    for event in _cut(events, tick):
        view.add(event)
    return echo_scores(pack, view, tick), crystallized_traits(pack, view, tick)


def _board(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    projection = fold(_cut(events, tick), initial_projection(pack.entities))
    echoes, traits = _folds(pack, events, tick)
    roster = [str(npc["id"]) for npc in pack.entities.get("npcs", ())]
    return offers(pack, projection, roster, echoes=echoes, traits=traits)


def _mine(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    return tuple(
        offer for offer in _board(pack, events, tick) if offer.npc == SMELTER
    )


def _card(text: str, npc: str) -> str:
    lines = [
        line for line in text.splitlines()
        if line.startswith("-") and npc in line and "drive=" in line
    ]
    assert lines, f"{npc} carries no card at this cut"
    return lines[0]


def _payments(events: list[Any]) -> list[Any]:
    return [
        event for event in events
        if event.type == "account_transferred" and event.actor == PLAYER
    ]


def _fund(events: list[Any]) -> list[tuple[int, str, int, int]]:
    return [
        (event.t, event.type, change.from_, change.to_)
        for event in events
        for change in event.state_changes
        if change.entity == SMELTER and change.prop == "account.coin"
    ]


# -- (1) the offer stands before the walk, with the reader's gate -------------


def test_the_offer_stands_with_the_readers_gate(tmp_path: Path) -> None:
    """The committed content's payment need, read at the first tick: the
    smith's fund is 3 of the paper's 16, the terms are the declared transfer
    (+3 coin to the holder), and the blocker is the READER's distance — the
    need exists whether or not anyone stands at the crofts."""
    pack, events, _ = _run(tmp_path)
    board = _mine(pack, events, 1)
    assert len(board) == 1
    offer = board[0]
    assert (offer.drive, offer.verb, offer.test) == (
        FUND, PAY, "account_at_least",
    )
    assert (offer.held, offer.required, offer.deficit) == (3, PAPER, PAPER - 3)
    assert offer.payable is True  # the transfer feeds the holder: +3 coin
    assert offer.need == NEED
    assert offer.segments() == (
        f"offer={PAY} 3/16",
        "blocked=target.same_location",
        f"need={NEED}",
    )


# -- (2) the reader's hand: the coin walks, the number moves ------------------


def test_the_readers_hand_moves_the_needs_own_number(tmp_path: Path) -> None:
    """Two payments, each exactly the declared legs (the payer −3, the smith
    +3), the co-present learning `the_bloom_bought`; between them the
    OFFER's own number moves with the stock — 6/16 after the first, 9/16
    after the second — the board reading the projection, never a memory of
    the act."""
    pack, events, _ = _run(tmp_path)
    pays = _payments(events)
    assert len(pays) == 2
    first, second = pays
    assert (first.t, second.t) == (1178, 1180)
    assert first.outcome["kind"] == "coin"
    for payment in pays:
        assert payment.target == SMELTER
        legs = {(change.entity, change.prop): change for change in payment.state_changes}
        paid = legs[(PLAYER, "account.coin")]
        got = legs[(SMELTER, "account.coin")]
        assert paid.to_ == paid.from_ - PRICE
        assert got.to_ == got.from_ + PRICE
        assert [(record.who, record.knows) for record in payment.knowledge] == [
            (SMELTER, "the_bloom_bought"),
            (WITNESS, "the_bloom_bought"),
        ]
    # the board at each cut reads the projection's own coin
    after_one = _mine(pack, events, first.t)[0]
    assert (after_one.held, after_one.required) == (6, PAPER)
    assert "blocked=" not in " ".join(after_one.segments())
    after_two = _mine(pack, events, second.t)[0]
    assert (after_two.held, after_two.required) == (9, PAPER)
    # the card at that cut: OPEN, the offer, the need phrase, one sentence
    card = _card(
        render_brief(assemble_brief(_cut(events, second.t), pack)), SMELTER
    )
    assert f"drive={FUND}:OPEN" in card
    assert f"offer={PAY} 9/16" in card
    assert f"need={NEED}" in card


# -- (3) the purse is the door's own gate -------------------------------------


def test_the_purse_is_the_gate_and_the_attempt_is_canon(tmp_path: Path) -> None:
    """The third payment with an empty purse is refused SOFTLY at the door —
    the world's own arithmetic (`actor.account_at_least`), never the owner's
    terms: the attempt lands as canon (`intent_rejected`), the stocks do not
    move, and the co-present learn nothing from a refusal."""
    pack, events, _ = _run(tmp_path)
    rejected = [event for event in events if event.type == "intent_rejected"]
    assert len(rejected) == 1
    assert rejected[0].actor == PLAYER
    assert rejected[0].outcome["action"] == PAY
    assert rejected[0].outcome["failed_test"] == "actor.account_at_least"
    assert rejected[0].target == SMELTER
    assert not [change for change in rejected[0].state_changes]
    assert not rejected[0].knowledge
    # the payer is empty and the fund stands where the two payments left it
    assert _fund(events)[1] == (1180, "account_transferred", 6, 9)


# -- (4) the years close the rest, and the met goal stops pushing -------------


def test_the_years_close_the_fund_and_the_met_goal_stops_pushing(
    tmp_path: Path,
) -> None:
    """The world's own clock finishes what the purse could not: the fund's
    yearly net (+3) walks 9 → 12 → 15 → 18 at the three macro crossings, the
    measure `account_at_least coin 16` turns MET, the debt drive's bar goes 0,
    the `pay_the_bloom` offer disappears from the board — and, by the
    continuity law, the grown wood's CRAFT pursuit becomes the smith's
    dominant drive (the debt drive stops pushing because it is satisfied)."""
    pack, events, _ = _run(tmp_path)
    trail = _fund(events)
    assert [(tick, to) for tick, _type, _fr, to in trail] == [
        (1178, 6), (1180, 9), (518400, 12), (1036800, 15), (1555200, 18),
    ]
    end = events[-1].t
    board = _mine(pack, events, end)
    assert all(offer.verb != PAY for offer in board)
    assert PAY not in " ".join(
        segment for offer in board for segment in offer.segments()
    )
    projection = fold(events, initial_projection(pack.entities))
    specs = {spec.drive: spec for spec in drive_specs(pack, projection) if spec.npc == SMELTER}
    echoes, traits = _folds(pack, events, end)
    assert drive_bar(
        specs[FUND], pack, projection, echoes=echoes, traits=traits,
    ) == 0
    assert drive_bar(
        specs["fire_the_year_cut"], pack, projection, echoes=echoes, traits=traits,
    ) == 37  # the grown wood: the craft's ceiling fails, its full weight
    view = agenda_view(
        pack, projection, SMELTER, echoes=echoes, traits=traits,
    )
    assert (view.drive, view.status) == ("fire_the_year_cut", "OPEN")
    assert mechanics.render_offers(pack, events, at_tick=1180).count(PAY) == 1
    assert PAY not in mechanics.render_offers(pack, events)


# -- (5) INV-2: the walk is byte-identical across twins ----------------------


def test_the_walk_is_byte_identical_across_twins(tmp_path: Path) -> None:
    """The same script twice, the same bytes; the run's fingerprints agree."""
    arms = []
    for name in ("a.jsonl", "b.jsonl"):
        _pack, _events, result = _run(tmp_path, name)
        arms.append((result.fingerprint, (tmp_path / name).read_bytes()))
    assert arms[0][1] == arms[1][1]
    assert arms[0][0] == arms[1][0]
