"""needphrase-1 (iter-446) — ONE SENTENCE PER PURSUIT: the board's `need=`
phrase is the DRIVE's own, the record's `spine.need` only its fallback.
Extended by needphrase-2 (iter-447): the law's reach is the ROLE CLOSURE (the
role a TURNING brings is the person's own pursuit too), and the road row
declares its phrase — the born carrier's only possible sentence.

iter-445 §6 measured the defect this unit owns: the board printed the
person's recorded `spine.need` beside whichever drive was dominant, so once
the smith's debt was MET and his craft drive took over, the craft offer
carried the PAID debt's words (`offer=burn_the_stacks 6/1 need=the charcoal
debt repaid`). The phrase is a narrator's line, never a term (iter-435), so
nothing was miscalculated — the SENTENCE was: it named a closed need beside a
live pursuit. This module walks the fix on the witness iter-445 left behind:

- the drive row gains an optional `need` phrase; the board reads IT first and
  the record's `spine.need` only when the row declares none
  (`core/offers.py::_need`), so the sentence follows the pursuit;
- the pack lint owns both halves — the phrase's FORM (one line, no `=`, the
  card-budget's word bound, never on a drive that cannot be offered) and the
  LAW (`_need_phrases`): two OFFERABLE drives a person can carry — his role's
  now plus every role a TURNING reaches (needphrase-2, iter-447) — may not
  resolve to the same sentence, because the board prints one phrase per
  dominant drive;
- content: the craft row declares its own phrase and the road row declares
  its own ditto (the born carrier's only possible sentence, and the
  post-turn pursuit's), the debt row keeps the record's (the FALLBACK arm) —
  so the corpus's flip prints two different sentences and the canon does not
  move a byte.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the board's `need=` phrase names the OFFERED pursuit — a two-pursuit
  person's offers carry two different sentences across the dominance flip,
  authored per drive and never a second source of truth; and the phrase is a
  read-time line only (the log is byte-identical when its words change).
- Lens: the read surfaces (the card at the flip's first half, the
  `mechanics offers` oracle at its second — the one owner of the text form),
  the load-time refusals, and the canon bytes.
- Prism: the committed witness `tests/playscripts/province_debtpaid.json`
  (seed 42) over the committed pack, its read at three cuts (t=1, t=1180,
  end t=1 558 153), and in-tmp twins of the pack for the capability and the
  refusal arms.
- Oracle: `Offer.segments` (the text form's owner) + the projection's own
  dominance read (`core.agenda`) + `load_pack`'s lint.
- Falsifier: a dominant craft offer still printing the paid debt's words; a
  phrase the row does not declare; a drive phrase leaking into the canon log;
  two pursuits of one role loading green on one sentence; a phrase on an
  appetite drive (dead data) loading green.
- Ablation: the same witness run twice — committed pack vs a twin whose only
  difference is the craft phrase's WORDS — byte-identical logs.
- Epistemic class: FACT on the committed pack + script (seed 42); the
  refusal arms are FACT on the twins.

Honest limit, named: the law reads the roles a person can HOLD — his own now
plus every role a TURNING can bring him through (needphrase-2, iter-447
extended the origin-role law to that closure); the post-turn pursuit therefore
carries the road row's own words, never the recorded debt's. What stays out of
reach is a pursuit whose row declares no phrase AND whose person carries no
`spine`: the board then prints no phrase at all — the honest negative, never a
borrowed sentence.
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
from core.echo import echo_scores  # noqa: E402
from core.fold import fold, initial_projection  # noqa: E402
from core.knowledge import KnowledgeView  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.offers import offers  # noqa: E402
from core.pack import PackError, load_pack  # noqa: E402
from core.psyche import ROLE_PROP  # noqa: E402
from core.traits import crystallized_traits  # noqa: E402

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
SCRIPT = REPO / "tests" / "playscripts" / "province_debtpaid.json"
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
SMELTER = "npc_smelter_01"
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")
FUND = "see_the_debt_paid"
CRAFT = "fire_the_year_cut"
PAY = "pay_the_bloom"
NEED = "the charcoal debt repaid"  # the smelter's authored spine.need
CRAFT_NEED = "the coppice's wood down to one load"  # the craft row's own
ROAD_NEED = "the road known"  # the road row's own (the born carrier's sentence)
ROAD_ROLE = "the_road_wanderer"  # the smith's turn target (the closure's other role)


def _twin(tmp_path: Path, name: str, mutate: Any) -> Path:
    """The committed pack copied into tmp with `rules.json` mutated — never a
    committed edit (the content's only change is the craft row's phrase)."""
    twin = tmp_path / name
    shutil.copytree(PACK_DIR, twin)
    path = twin / "rules.json"
    rules = json.loads(path.read_text(encoding="utf-8"))
    mutate(rules)
    path.write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return twin


def _drive(rules: dict[str, Any], drive_id: str) -> dict[str, Any]:
    return next(
        row for row in rules["psyche"]["drives"] if row["id"] == drive_id
    )


def _run(tmp_path: Path, name: str = "need.jsonl") -> tuple[Any, list[Any], bytes]:
    """The committed witness script over the committed pack, in tmp."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript(load_playscript(SCRIPT))
    sim.close()
    _, events = read_log(log, SCHEMA)
    return pack, events, log.read_bytes()


def _board(pack: Any, events: list[Any], tick: int) -> tuple[Any, ...]:
    cut = [event for event in events if event.t <= tick]
    projection = fold(cut, initial_projection(pack.entities))
    view = KnowledgeView()
    for event in cut:
        view.add(event)
    echoes = echo_scores(pack, view, tick)
    traits = crystallized_traits(pack, view, tick)
    roster = [str(npc["id"]) for npc in pack.entities.get("npcs", ())]
    return tuple(
        offer
        for offer in offers(
            pack, projection, roster, echoes=echoes, traits=traits,
        )
        if offer.npc == SMELTER
    )


def _card(events: list[Any], pack: Any, tick: int) -> list[str]:
    text = render_brief(
        assemble_brief([event for event in events if event.t <= tick], pack)
    )
    return [
        line for line in text.splitlines()
        if line.startswith("-") and SMELTER in line and "drive=" in line
    ]


# -- (1) the witness: the sentence follows the pursuit -----------------------


def test_the_flip_prints_two_sentences_and_the_craft_is_the_own_one(
    tmp_path: Path,
) -> None:
    """iter-445's witness, read at its two halves. At t=1180 the smith's
    dominant drive is the DEBT: the card prints `offer=pay_the_bloom 9/16`
    with the RECORD's phrase (the debt row declares none — the fallback arm).
    At the end the debt is MET (the wonder's own years, 18 of 16) and the
    CRAFT dominates: the board prints `offer=burn_the_stacks 6/1` with the
    ROW's own phrase — never the paid debt's words. Two pursuits, two
    sentences; the same pack, the same canon."""
    pack, events, _raw = _run(tmp_path)
    end = events[-1].t

    mid = _board(pack, events, 1180)
    assert [offer.drive for offer in mid] == [FUND]
    paid = mid[0]
    assert paid.verb == PAY and paid.need == NEED  # the record FALLBACK
    card = _card(events, pack, 1180)
    assert len(card) == 1
    assert f"offer={PAY} 9/16" in card[0]
    assert f"need={NEED}" in card[0]

    after = _board(pack, events, end)
    assert [offer.drive for offer in after] == [CRAFT]
    craft = after[0]
    assert (craft.verb, craft.held, craft.required) == ("burn_the_stacks", 6, 1)
    assert craft.need == CRAFT_NEED
    assert craft.need != NEED
    assert craft.segments() == (
        "offer=burn_the_stacks 6/1", f"need={CRAFT_NEED}",
    )
    # the paid need's words are nowhere on the board that addresses the man
    endread = mechanics.render_offers(pack, events)
    assert f"{SMELTER} · {CRAFT} · offer=burn_the_stacks 6/1 need={CRAFT_NEED}" in endread
    assert SMELTER not in "\n".join(
        line for line in endread.splitlines() if PAY in line
    )
    assert f"need={NEED}" not in "\n".join(
        line for line in endread.splitlines() if SMELTER in line
    )
    # and the first half is still the payment: the offer existed, then closed
    assert f"{SMELTER} · {FUND} · offer={PAY} 9/16" in mechanics.render_offers(
        pack, events, at_tick=1180
    )


# -- (2) the born carrier and the turn: the ROLE's phrase --------------------


def test_a_born_carrier_takes_the_roles_phrase(tmp_path: Path) -> None:
    """A BORN person carries no dossier (no `spine`), so the board has no
    record phrase to fall back on: the ROLE's own `need` is the only sentence
    their offer can carry. (needphrase-2, iter-447: the road row declares it,
    which is also what makes the smith's post-turn pursuit legal — §2b.) The
    three travellers share the words because they share the ROLE, which is
    the point: the sentence names the pursuit, never the person."""
    pack = load_pack(PACK_DIR)
    _header, events = read_log(GOLDEN, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))
    spelled = offers(pack, projection, TRAVELLERS)
    assert [offer.need for offer in spelled] == [ROAD_NEED] * len(TRAVELLERS)
    for offer in spelled:
        assert offer.drive == "scan_the_road"
        assert offer.segments() == (
            "offer=look_around", "payable=?", f"need={ROAD_NEED}",
        )


def test_the_post_turn_road_pursuit_carries_the_roads_words() -> None:
    """The turning closure's own case, read directly (needphrase-2): with the
    smith's LIVE role folded to `the_road_wanderer` (the prop a canon turn
    writes, `core.psyche.role_of`'s first precedence), his dominating pursuit
    is the road's watch — and its offer carries the ROAD's sentence. Without
    the closure law an unphrased road row would have printed his recorded
    debt's words here, the same defect one role over."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    projection[SMELTER][ROLE_PROP] = ROAD_ROLE
    board = offers(pack, projection, [SMELTER])
    assert len(board) == 1
    turned = board[0]
    assert (turned.drive, turned.verb) == ("scan_the_road", "look_around")
    assert turned.need == ROAD_NEED
    assert turned.need != NEED
    assert turned.segments() == (
        "offer=look_around", "payable=?", f"need={ROAD_NEED}",
    )


def test_the_turning_trajectory_may_not_print_the_record_phrase(
    tmp_path: Path,
) -> None:
    """The law's reach is the role CLOSURE, not the origin role alone
    (needphrase-2): drop the road row's phrase and the smith's post-turn
    pursuit would fall back to his recorded `spine.need` — the debt's words
    beside the road's offer — so the pack refuses at LOAD, naming both rows
    and the phrase. The closure is why the road row cannot stay silent."""
    twin = _twin(
        tmp_path,
        "unroaded",
        lambda rules: _drive(rules, "scan_the_road").pop("need"),
    )
    with pytest.raises(PackError) as refused:
        load_pack(twin)
    message = str(refused.value)
    assert SMELTER in message
    assert "scan_the_road" in message and FUND in message
    assert NEED in message
    assert "one sentence per PURSUIT" in message


# -- (3) the phrase is a line, never a term ---------------------------------


def test_the_phrases_words_never_reach_the_canon(tmp_path: Path) -> None:
    """The phrase is READ at assembly, never written: the same witness script
    over a twin whose only difference is the craft phrase's WORDS produces a
    byte-identical log (the header included — same env, same pack name). The
    changed sentence shows only on the read surface."""
    _pack, _events, raw = _run(tmp_path, "committed.jsonl")
    twin = _twin(
        tmp_path,
        "reworded",
        lambda rules: _drive(rules, CRAFT).update(
            {"need": "a wholly different sentence"}
        ),
    )
    log = tmp_path / "reworded.jsonl"
    sim = Simulator(load_pack(twin), 42, log, SCHEMA, commit="0000000")
    sim.run_playscript(load_playscript(SCRIPT))
    sim.close()
    assert log.read_bytes() == raw
    endread = mechanics.render_offers(load_pack(twin), read_log(log, SCHEMA)[1])
    assert "need=a wholly different sentence" in endread
    assert CRAFT_NEED not in endread


# -- (4) the law: one sentence per pursuit ----------------------------------


def test_the_paid_needs_words_cannot_be_authored_beside_the_craft(
    tmp_path: Path,
) -> None:
    """The measured defect made ILLEGAL: with the craft row's own phrase
    dropped, both of the smith's OFFERABLE drives resolve to the record's
    `spine.need` — two pursuits, one sentence — and the pack refuses at LOAD,
    naming the person, both drives and the phrase. The sentence iter-445 §6
    printed can no longer be authored green."""
    twin = _twin(
        tmp_path,
        "unphrased",
        lambda rules: _drive(rules, CRAFT).pop("need"),
    )
    with pytest.raises(PackError) as refused:
        load_pack(twin)
    message = str(refused.value)
    assert SMELTER in message
    assert CRAFT in message and FUND in message
    assert NEED in message
    assert "one sentence per PURSUIT" in message


def test_two_drives_of_one_role_may_not_share_a_phrase(tmp_path: Path) -> None:
    """The same law without the fallback: a second OFFERABLE drive added to
    the smelter's role with the craft's own phrase is refused — the board
    would print one sentence for two different acts."""
    def shadow(rules: dict[str, Any]) -> None:
        rules["psyche"]["drives"].append({
            "id": "a_second_pursuit",
            "archetypes": ["the_smelter_master"],
            "base": 5,
            "max_per_beat": 10,
            "verb": "look_around",
            "measure": [
                {"noun": "actor", "test": "account_at_least", "kind": "coin",
                 "value": 99},
            ],
            "need": CRAFT_NEED,
        })

    twin = _twin(tmp_path, "samephrase", shadow)
    with pytest.raises(PackError, match="one sentence per PURSUIT"):
        load_pack(twin)


# -- (5) the phrase's form is the card's -------------------------------------


def test_the_phrases_form_is_the_cards(tmp_path: Path) -> None:
    """Four dead shapes, each refused at LOAD: a blank phrase, one carrying
    `=` (the `need=` segment's grammar) or a line break (the card is one
    line), one over the card-budget's word bound, and one on a drive with no
    `measure` — the board offers only a FAILING measure row, so an appetite's
    sentence can never print (dead data)."""
    def set_need(value: Any, drive_id: str = CRAFT) -> Any:
        return lambda rules: _drive(rules, drive_id).update({"need": value})

    dead = (
        ("blank", set_need("   ")),
        ("equals", set_need("the wood = the load")),
        ("newline", set_need("the wood\nthe load")),
        ("long", set_need("word " * 9)),
    )
    for name, mutate in dead:
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate))

    def appetite(rules: dict[str, Any]) -> None:
        rules["psyche"]["drives"].append({
            "id": "an_appetite",
            "archetypes": ["the_smelter_master"],
            "base": 5,
            "max_per_beat": 10,
            "verb": "look_around",
            "measure": [],
            "need": "a sentence nothing can offer",
        })

    with pytest.raises(PackError, match="dead data"):
        load_pack(_twin(tmp_path, "appetite", appetite))
