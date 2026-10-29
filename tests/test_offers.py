"""quest-1 v0 (iter-435) — the derived offer board: the laws, the witness,
the honest-negative arm and the twin arm.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the world's unmet needs are derivable and EXACT from canonical
  state alone — a drive's failing `measure` row IS a need, the drive's own
  verb is the closing act, that verb's declared `account` block is the
  terms, and the door's own `first_failing` is the blocker.
- Lens: derivability + exactness (the read vs the door), never "the board
  looks plausible".
- Prism: the committed province corpus (the honest-negative arm: the drive's
  measure is the BELIEF `the_road_known` — an event-driven fold the corpus
  never completes, so the board prints `payable=?`: the terms are not a
  stock movement, and the goal is canon-reachable but unmet) and three
  in-tmp twins of it — a payable FLOOR (`reprice_paper` sources paper at the
  actor), an UNFED floor (the transfer pays the chest, so the actor's stock
  only falls), a payable CEILING (the committed smelter drive with the yard
  seeded over its bar).
- Oracle: `first_failing` on the SAME measure row + the projection read —
  the board prints exactly the rows the door refuses, and its numbers are
  the projection's own.
- Falsifier: an offer whose measure row the door PASSES (over-claim); a
  failing row the board omits (under-claim); a term the pack does not
  declare (an invented amount); a `payable=True` whose delta the account
  block denies.
- Ablation: the card segment is the only surface the board adds — the
  other brief blocks and the canon log are byte-identical with and without
  it (the board is a read).
- Epistemic class: FACT on the committed corpus and the twins (seed 42).

The helper act (iter-442, D-288) — the board is the READER's sentence: a
need row may declare `helper_verb`, the act a THIRD PARTY performs to close
it (the player is one). The offer then names THAT act, `payable` from the
same declared-terms arithmetic with the holder as the act's counterparty,
and `blocked` from ITS requirements read on the player's own probe — while
a row without the key reads exactly as v0 did. The laws below pin the three
sides: the offer names the helper, the gate is the reader's (position and
stock), and the lint refuses a helper that cannot close the stock (dead
data). The `convert` arm of the terms law — a recipe that pays a person —
is pinned here too (it was an INFERENCE in iter-433 §9 until this unit).

The CONTENT arming (iter-443, D-289) is the same law read off the COMMITTED
pack: the keeper's drive `keep_the_crossing` measures the stair's wear
(`account_at_most 1`) and declares `helper_verb=mend_the_stair`, the office's
own door — an act her hands cannot take, offered to the reader instead. The
arming is INERT at genesis (wear 0 meets the measure), so the day-scale
golden is byte-identical; the laws below pin the armed read (the reader's
gate, the recipe's own wear leg) and the owner's own act (the read, which
closes nothing — the third-party thesis made content).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import mechanics  # type: ignore[import-not-found]  # noqa: E402

from brief.assembler import assemble_brief, render_brief  # noqa: E402
from core.agenda import agenda_view  # noqa: E402
from core.drives import drive_specs  # noqa: E402
from core.echo import echo_scores  # noqa: E402
from core.fold import fold, initial_projection  # noqa: E402
from core.intent import first_failing  # noqa: E402
from core.knowledge import KnowledgeView  # noqa: E402
from core.log import read_log  # noqa: E402
from core.offers import act_delta, offers  # noqa: E402
from core.pack import PackError, load_pack  # noqa: E402
from core.traits import crystallized_traits  # noqa: E402

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")
SMELTER = "npc_smelter_01"
NEED = "the charcoal debt repaid"  # the smelter's own authored spine.need
#: The craft drive's OWN phrase (needphrase-1, iter-446): the board prints it
#: beside `burn_the_stacks`, never the paid debt's recorded words.
CRAFT_NEED = "the coppice's wood down to one load"
#: The road drive's own phrase (needphrase-2, iter-447): a born traveller has
#: no dossier, so the ROLE's sentence is the only one their offer can carry.
ROAD_NEED = "the road known"


def _events() -> list[Any]:
    _, events = read_log(GOLDEN, SCHEMA)
    return events


def _fold_end(pack: Any, events: list[Any]) -> Any:
    return fold(events, initial_projection(pack.entities))


def _echoes_at(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    view = KnowledgeView()
    for event in events:
        if event.t > tick:
            break
        view.add(event)
    return echo_scores(pack, view, tick)


def _folds_at(
    pack: Any, events: list[Any], tick: int
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """Both fold reads the brief passes at a tick: the echo residue and the
    event-driven traits (`core.offers` reads them, iter-439)."""
    view = KnowledgeView()
    for event in events:
        if event.t > tick:
            break
        view.add(event)
    return echo_scores(pack, view, tick), crystallized_traits(pack, view, tick)


def _twin(tmp_path: Path, name: str, *, rules_mutate: Any, entities_mutate: Any = None) -> Path:
    twin = tmp_path / name
    shutil.copytree(PACK_DIR, twin)
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules_mutate(rules)
    (twin / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    if entities_mutate is not None:
        entities = json.loads((twin / "entities.json").read_text(encoding="utf-8"))
        entities_mutate(entities)
        (twin / "entities.json").write_text(
            json.dumps(entities, indent=2), encoding="utf-8"
        )
    return twin


def _add_drive(drive: dict[str, Any]) -> Any:
    """The twin's OWN terms row for the smelter: the smelter's COMMITTED
    drives are dropped and the test drive stands alone (iter-445: the pack
    now carries the craft and the debt drives too, and each terms-law arm is
    about ONE declared row — the dominance must not be decided by content the
    arm never authored). The travellers' drive stays: the road_folk
    distribution's reachability law reads it."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["psyche"]["drives"] = [
            row for row in rules["psyche"]["drives"]
            if row["id"] not in ("fire_the_year_cut", "see_the_debt_paid")
        ] + [drive]
    return mutate


def _cut_head(events: list[Any]) -> list[Any]:
    """The run's opening scene: the player still stands with the three road
    travellers at the crossing (before the first player move)."""
    cut = next(
        index
        for index, event in enumerate(events)
        if event.type == "move" and event.actor == "pc_01"
    )
    return events[:cut]


# -- the committed corpus: the honest-negative arm ----------------------------


def test_the_corpus_witnesses_the_board_its_negative_and_its_first_payment() -> None:
    """The committed corpus's board, both arms at once. The three travellers
    keep the HONEST NEGATIVE: their measure is the BELIEF `the_road_known`
    (iter-439), an event-driven fold the corpus never completes, so their
    closing verb declares no stock terms and the board prints `payable=?`,
    inventing nothing — while the phrase beside it is the ROLE's own (a born
    person carries no dossier, needphrase-2/iter-447). And the corpus now
    carries its FIRST PAYABLE witness
    (iter-445, the payment stripe): the smelter's debt drive measures his own
    coin fund (3 of the charcoal paper's sixteen) and declares
    `helper_verb=pay_the_bloom` — the reader's own transfer to his person —
    so the board names the act the READER can take, `payable` from the
    transfer's declared +3 coin, and the blocker his DISTANCE (the corpus ends
    at Thornmill); its phrase is the RECORD's fallback (the debt row declares
    none, needphrase-1/iter-446). The keeper's wear need stays silent (met at
    seed: wear 0 <= 1), and the smith has no offer from his CRAFT drive (the
    wood ceiling is met too)."""
    pack = load_pack(PACK_DIR)
    events = _events()
    projection = _fold_end(pack, events)
    _, traits = _folds_at(pack, events, events[-1].t)
    board = offers(
        pack, projection, [str(npc["id"]) for npc in pack.entities["npcs"]],
        traits=traits,
    )
    assert sorted(offer.npc for offer in board) == sorted(
        (*TRAVELLERS, SMELTER)
    )
    by_npc = {offer.npc: offer for offer in board}
    for traveller in TRAVELLERS:
        offer = by_npc[traveller]
        assert offer.drive == "scan_the_road"
        assert offer.test == "trait_held"
        assert offer.where == "actor.trait_held"
        assert offer.payable is None  # not a stock movement: the honest "?"
        assert offer.kind is None and offer.held is None
        assert offer.need == ROAD_NEED  # the ROLE's phrase, no dossier
        assert offer.segments() == (
            "offer=look_around", "payable=?", f"need={ROAD_NEED}",
        )
    paid = by_npc[SMELTER]
    assert (paid.drive, paid.verb, paid.test) == (
        "see_the_debt_paid", "pay_the_bloom", "account_at_least",
    )
    assert (paid.kind, paid.held, paid.required, paid.deficit) == (
        "coin", 3, 16, 13,
    )
    assert paid.payable is True  # the transfer feeds the holder: +3 coin
    assert paid.need == NEED
    assert paid.segments() == (
        "offer=pay_the_bloom 3/16",
        "blocked=target.same_location",
        f"need={NEED}",
    )
    assert KEEPER not in by_npc  # wear 0: met, silent


def test_the_corpus_leaves_the_belief_unformed() -> None:
    """INERT-FIRST by measurement (iter-439): the committed corpus mints ONE
    of the three scenes the belief family names (`scene_loc_riverroad`), so
    `the_road_known` never crystallizes and the drive's measure stays
    failing — which is exactly why the committed corpus is byte-identical
    and the board keeps its honest-negative witness."""
    pack = load_pack(PACK_DIR)
    events = _events()
    _, traits = _folds_at(pack, events, events[-1].t)
    assert traits == ()
    family = pack.rules["traits"]["beliefs"]["the_road_known"]["family"]
    assert sorted(family) == sorted(
        ["scene_loc_riverroad", "scene_loc_weirstair", "scene_loc_malby"]
    )


def test_the_board_prints_exactly_the_rows_the_door_refuses() -> None:
    """The oracle: every printed offer re-derives the SAME failing row
    through the door's own `first_failing` and the SAME stock value from
    the projection — no over-claim, no under-claim on this corpus."""
    pack = load_pack(PACK_DIR)
    events = _events()
    projection = _fold_end(pack, events)
    echoes, traits = _folds_at(pack, events, events[-1].t)
    specs = {
        (spec.npc, spec.drive): spec
        for spec in drive_specs(pack, projection)
    }
    board = offers(
        pack, projection, list(specs_at(specs)), echoes=echoes, traits=traits,
    )
    assert board
    for offer in board:
        spec = specs[(offer.npc, offer.drive)]
        row = next(
            cond for cond in spec.measure
            if f"{cond.get('noun') or cond.get('holder')}.{cond['test']}"
            == offer.where
        )
        assert first_failing(
            pack, projection, spec.probe, (row,), echoes=echoes, traits=traits,
        ) == offer.where


def specs_at(specs: Any) -> list[str]:
    """The NPCs the parse holds (order: the parse's own)."""
    seen: list[str] = []
    for npc, _drive in specs:
        if npc not in seen:
            seen.append(npc)
    return seen


# -- the twin arm: a payable floor, an unfed floor, a payable ceiling --------


def test_a_floor_the_closing_act_feeds_is_payable(tmp_path: Path) -> None:
    """`reprice_paper` SOURCES paper at the actor (+2), so a floor on the
    actor's paper is closable by the drive's own verb: held 16, required 20,
    deficit 4, payable=True. The need phrase is the record's `spine.need` —
    the FALLBACK arm, since this twin's drive row declares no `need`
    (needphrase-1/iter-446)."""
    twin = _twin(
        tmp_path,
        "floor",
        rules_mutate=_add_drive({
            "id": "hold_paper",
            "archetypes": ["the_smelter_master"],
            "base": 10,
            "max_per_beat": 20,
            "verb": "reprice_paper",
            "target": "npc_peddler_01",
            "measure": [
                {"noun": "actor", "test": "account_at_least", "kind": "paper",
                 "value": 20},
            ],
        }),
    )
    pack = load_pack(twin)
    projection = initial_projection(pack.entities)
    board = offers(pack, projection, [SMELTER])
    assert len(board) == 1
    offer = board[0]
    assert (offer.test, offer.kind, offer.held, offer.required, offer.deficit) == (
        "account_at_least", "paper", 16, 20, 4,
    )
    assert offer.payable is True
    # closable in principle, refused at the door TODAY: the peddler is on
    # the road, the smelter at the crofts — both statements are printed
    assert offer.blocked == "target.same_location"
    assert offer.need == NEED
    assert offer.segments() == (
        "offer=reprice_paper 16/20",
        "blocked=target.same_location",
        f"need={NEED}",
    )


def test_an_unfed_floor_is_not_payable(tmp_path: Path) -> None:
    """The corpus's own counter-example by computation: `trade_at_market`
    TRANSFERS coin OUT of the actor (to the market chest), so a coin floor
    on the actor is not closable by it — payable=False even though the act
    is otherwise gated by the target's location."""
    twin = _twin(
        tmp_path,
        "unfed",
        rules_mutate=_add_drive({
            "id": "coin_for_the_debt",
            "archetypes": ["the_smelter_master"],
            "base": 10,
            "max_per_beat": 20,
            "verb": "trade_at_market",
            "target": "loc_malby",
            "measure": [
                {"noun": "actor", "test": "account_at_least", "kind": "coin",
                 "value": 20},
            ],
        }),
    )
    pack = load_pack(twin)
    projection = initial_projection(pack.entities)
    offer = offers(pack, projection, [SMELTER])[0]
    assert (offer.held, offer.required, offer.deficit) == (3, 20, 17)
    assert offer.payable is False
    assert offer.blocked == "target.same_location"
    assert "payable=no" in offer.segments()
    assert "blocked=target.same_location" in offer.segments()


def test_a_ceiling_the_closing_act_lowers_is_payable(tmp_path: Path) -> None:
    """The committed smelter drive, with the yard seeded ABOVE its ceiling
    (wood 5 > 1): the failing ceiling row becomes an offer, and the burn's
    `convert` recipe (2 wood consumed at the crofts) moves the stock DOWN —
    the ceiling's direction, so payable=True."""
    def seed(entities: dict[str, Any]) -> None:
        for record in entities["locations"]:
            if record["id"] == "loc_crofts":
                record["accounts"]["wood"] = 5

    twin = _twin(tmp_path, "ceiling", rules_mutate=lambda rules: None,
                 entities_mutate=seed)
    pack = load_pack(twin)
    projection = initial_projection(pack.entities)
    offer = offers(pack, projection, [SMELTER])[0]
    assert (offer.drive, offer.test, offer.kind) == (
        "fire_the_year_cut", "account_at_most", "wood",
    )
    assert (offer.held, offer.required, offer.deficit) == (5, 1, 4)
    assert offer.payable is True
    assert offer.blocked is None
    assert offer.need == CRAFT_NEED  # the drive's OWN sentence, not the debt's


# -- the surfaces: the card and the oracle read share the text form ----------


def test_the_card_renders_the_offer_for_a_present_person() -> None:
    """quest-1 v0's only canon-facing surface: one `offer=` sentence on the
    present person's card — the three travellers at the crossing carry it
    (and their `drive=`/`want=` segments are untouched beside it)."""
    pack = load_pack(PACK_DIR)
    events = _cut_head(_events())
    text = render_brief(assemble_brief(events, pack))
    lines = [line for line in text.splitlines() if "offer=" in line]
    assert len(lines) == 3
    for traveller in TRAVELLERS:
        mine = [line for line in text.splitlines() if traveller in line]
        assert mine, f"{traveller} has no card"
        assert any(
            "drive=scan_the_road:OPEN" in line
            and "want=the road's own sign read" in line
            and "offer=look_around payable=?" in line
            for line in mine
        )


def test_the_script_read_is_the_card_read() -> None:
    """The oracle surface prints the same sentences the card does — the text
    form has ONE owner (`Offer.segments`), so the two reads cannot drift."""
    pack = load_pack(PACK_DIR)
    events = _events()
    out = mechanics.render_offers(pack, events)
    for traveller in TRAVELLERS:
        assert f"{traveller} · scan_the_road · offer=look_around payable=?" in out
    assert (
        f"{SMELTER} · see_the_debt_paid · offer=pay_the_bloom 3/16 "
        f"blocked=target.same_location need={NEED}" in out
    )
    assert "4 need(s)" in out
    mid = mechanics.render_offers(pack, events, at_tick=1000)
    assert "4 need(s)" in mid and "payable=?" in mid


def test_the_payable_witness_is_the_readers_own_purse() -> None:
    """The committed payment offer read on the PLAYER's probe (D-288's
    reader law, now on committed content): standing at the crofts with the
    coin the act is free; short of it the gate names the READER's purse —
    never the owner's. The smith's own 3 coin is the act's counterparty, not
    its gate."""
    pack = load_pack(PACK_DIR)
    standing = initial_projection(pack.entities)
    standing["pc_01"]["position"] = "loc_crofts"
    free = offers(pack, standing, [SMELTER])[0]
    assert "blocked=" not in " ".join(free.segments())
    assert free.payable is True
    broke = initial_projection(pack.entities)
    broke["pc_01"]["position"] = "loc_crofts"
    broke["pc_01"]["account.coin"] = 2
    gate = offers(pack, broke, [SMELTER])[0]
    assert "blocked=actor.account_at_least" in gate.segments()


# -- the helper act: the board is the READER's sentence (iter-442, D-288) -----


HELPER = "pay_the_smith"
KEEPER = "npc_weirkeeper_01"
COIN_FLOOR: dict[str, Any] = {
    "holder": SMELTER,
    "test": "account_at_least",
    "kind": "coin",
    "value": 6,
}


def _payer_action(amount: int = 3) -> dict[str, Any]:
    """The twin's helper act: a third party pays the smith. A `transfer`
    actor->target, so whoever acts pays and the smith receives вЂ” the player
    is one possible payer, never a special case."""
    return {
        "intent": HELPER,
        "label": "pay the smith",
        "resolver": "account",
        "ticks": 2,
        "events": {"success": "account_transferred"},
        "requires": [
            {"noun": "target", "test": "kind", "is": "npc"},
            {"noun": "target", "test": "field_in", "field": "id",
             "values": [SMELTER]},
            {"noun": "target", "test": "same_location", "with": "actor"},
            {"noun": "actor", "test": "account_at_least", "kind": "coin",
             "value": amount},
            {"noun": "target", "test": "account_at_least", "kind": "coin",
             "value": 0},
        ],
        "fields": [],
        "account": {"verb": "transfer", "kind": "coin", "amount": amount},
        "knowledge": {"success": [], "failure": []},
        "hooks": {"success": [], "failure": []},
        "notes": "iter-442 test twin: the helper act",
    }


def _helper_twin(tmp_path: Path, measure: dict[str, Any]) -> Path:
    """The committed pack with ONE drive carrying the given measure row and a
    declared payer act вЂ” a twin, so the committed corpus keeps its own law."""
    twin = tmp_path / "pack_helper"
    if twin.exists():
        shutil.rmtree(twin)
    shutil.copytree(PACK_DIR, twin)
    actions = json.loads((twin / "actions.json").read_text(encoding="utf-8"))
    actions["actions"].append(_payer_action())
    (twin / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8",
    )
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules["psyche"]["drives"].append({
        "id": "the_debt_paid",
        "archetypes": ["the_smelter_master"],
        "base": 25,
        "max_per_beat": 60,
        "verb": "pass_the_seat",
        "target": "npc_winterkin_01",
        "measure": [measure],
        # needphrase-1 (iter-446): an OFFERABLE twin row beside the smith's
        # committed debt drive owes its own phrase — the record's fallback
        # would otherwise put the debt's sentence on this twin's offer, which
        # the one-sentence-per-pursuit law now refuses at load.
        "need": "the seat's own ledger squared",
        "modifiers": [
            {"axis": "conscientiousness", "low_pct": 60, "high_pct": 150},
        ],
        "notes": "iter-442 test twin",
    })
    (twin / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8",
    )
    return twin


def test_a_declared_helper_is_the_offer(tmp_path: Path) -> None:
    """The row's `helper_verb` replaces the owner's own act in the offer: the
    board names the act the READER can take, and the terms stay the pack's
    own (`payable` from the transfer's declared movement on the holder вЂ”
    the third party's act delivered TO them)."""
    pack = load_pack(_helper_twin(tmp_path, dict(COIN_FLOOR, helper_verb=HELPER)))
    board = offers(pack, initial_projection(pack.entities), [SMELTER])
    assert len(board) == 1
    offer = board[0]
    assert offer.verb == HELPER
    assert offer.payable is True
    assert (offer.held, offer.required, offer.deficit) == (3, 6, 3)
    segments = offer.segments()
    assert segments[0] == f"offer={HELPER} 3/6"
    # the player still stands at the crossing: the READER's gate is named
    assert "blocked=target.same_location" in segments


def test_the_helper_gate_is_the_readers(tmp_path: Path) -> None:
    """`blocked` is read on the PLAYER's probe, never the owner's: standing
    at the crofts with the coin the act is free; without the coin the gate
    names the player's own stock вЂ” the owner carries 3 coin and is never the
    gate of the act he would never take."""
    pack = load_pack(_helper_twin(tmp_path, dict(COIN_FLOOR, helper_verb=HELPER)))
    standing = initial_projection(pack.entities)
    standing["pc_01"]["position"] = "loc_crofts"
    free = offers(pack, standing, [SMELTER])[0]
    assert "blocked=" not in " ".join(free.segments())
    broke = initial_projection(pack.entities)
    broke["pc_01"]["position"] = "loc_crofts"
    broke["pc_01"]["account.coin"] = 0
    gate = offers(pack, broke, [SMELTER])[0]
    assert "blocked=actor.account_at_least" in gate.segments()


def test_a_helper_that_cannot_close_the_stock_is_refused(tmp_path: Path) -> None:
    """The pack lint owes the helper the resolvability law (dead data): a
    DECLARED action whose movement on the need's `(holder, kind)` closes the
    test's direction. Four dead shapes refuse at load вЂ” a gift of another
    kind, an unknown act, a knowledge need (no terms), and the `noun` form
    (the holder unresolved at load)."""
    dead = (
        dict(COIN_FLOOR, helper_verb="pass_the_seat"),   # paper, not coin
        dict(COIN_FLOOR, helper_verb="nonesuch"),        # not declared
        {"noun": "actor", "test": "trait_held",
         "token": "the_road_known", "helper_verb": HELPER},
        {"noun": "actor", "test": "account_at_least", "kind": "coin",
         "value": 6, "helper_verb": HELPER},
    )
    for row in dead:
        with pytest.raises(PackError):
            load_pack(_helper_twin(tmp_path, row))


def test_the_recipe_wage_is_the_converts_terms() -> None:
    """The `convert` arm of the terms law, pinned on the committed pack: the
    mend's recipe pays the weir keeper one coin and consumes two wear off the
    stair вЂ” the arithmetic the board reads for a keeper's coin need
    (iter-433 В§9 left it an INFERENCE; here it is FACT)."""
    pack = load_pack(PACK_DIR)
    assert act_delta(pack, "mend_the_stair", KEEPER, "coin", target=KEEPER) == 1
    assert act_delta(
        pack, "mend_the_stair", "loc_weirstair", "wear",
        target="loc_weirstair",
    ) == -2


# -- the committed content arming: the keeper's wear (iter-443, D-289) -------


def test_the_committed_pack_offers_the_office_mend_to_the_reader() -> None:
    """The arming read off the COMMITTED pack: the keeper's drive
    `keep_the_crossing` measures the stair's wear (`account_at_most 1`) and
    declares `helper_verb=mend_the_stair` — the office's door, an act her
    hands cannot take, so the board offers it to the READER. With the wear
    standing above the bound: `payable` from the recipe's own wear leg
    (-2, the `convert` arm), the numbers the projection's, the NEED phrase
    the record's own, and `blocked` the reader's POSITION (never the
    keeper's) — the reader walks to the stair and the act is free."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    projection["loc_weirstair"]["account.wear"] = 2
    board = offers(pack, projection, [KEEPER])
    assert len(board) == 1
    offer = board[0]
    assert offer.verb == "mend_the_stair"
    assert offer.payable is True
    assert (offer.held, offer.required, offer.deficit) == (2, 1, 1)
    assert offer.need == "the stair's wear cleared"
    assert offer.segments() == (
        "offer=mend_the_stair 2/1",
        "blocked=target.same_location",
        "need=the stair's wear cleared",
    )
    projection["pc_01"]["position"] = "loc_weirstair"
    standing = offers(pack, projection, [KEEPER])[0]
    assert standing.segments() == (
        "offer=mend_the_stair 2/1", "need=the stair's wear cleared",
    )


def test_the_arming_is_inert_at_genesis_and_its_owner_cannot_close_it() -> None:
    """INERT-FIRST and the third-party thesis, both measured on the committed
    pack. (1) At genesis the stair seeds wear 0, the measure is MET, the bar
    is 0 and the board prints nothing — the day-scale golden therefore stays
    byte-identical (`test_maintenance` owns that oracle). (2) The drive's
    OWN verb is the READ: `read_stair` moves no stock of the measured kind,
    so the keeper's own act can never close her need — the row says so by
    construction (the ticker may read, only a third party mends), which is
    why the helper key exists at all."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    assert offers(pack, projection, [KEEPER]) == ()
    view = agenda_view(pack, projection, KEEPER)
    assert (view.drive, view.status, view.bar) == (
        "keep_the_crossing", "SATISFIED", 0,
    )
    spec = next(s for s in drive_specs(pack) if s.npc == KEEPER)
    assert spec.verb == "read_stair"
    assert act_delta(
        pack, spec.verb, "loc_weirstair", "wear",
        actor=KEEPER, target="loc_weirstair",
    ) == 0
    # the wear stands above the bound: the goal is OPEN and the bar is the
    # keeper's own diligence (base 12, conscientiousness 74 >= 70 -> 150 %)
    projection["loc_weirstair"]["account.wear"] = 2
    view = agenda_view(pack, projection, KEEPER)
    assert (view.status, view.bar) == ("OPEN", 18)
