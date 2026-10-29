"""iter-9 acceptance — the validator's LLM-free half (`docs/VALIDATION_SPEC.md`
owns the contract; `docs/blueprint/phases.md` §1 owns the donor design).

The suite pins the four laws the spec owns: the structural boundary (a
closed document — no prose field can even appear, §2), the honest-verdict
truth table against the committed golden fixture log (§4, plus the committed
golden set itself), ExpectedVersion OCC (fresh / stale-fabricated /
stale-broken with first-break attribution / rebased, §5), and the regen
protocol core (≤2, exhaustion → dry mode, §7). Purity: the validator is a
pure function of (proposal, log, pack) — no RNG, writes nothing (INV-1/2).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from brief.validator import (
    CONTRADICTED,
    INSUFFICIENT_DATA,
    SUPPORTED,
    ClaimVerdict,
    EventClaim,
    GoldenCase,
    IntentProposal,
    KnowledgeClaim,
    Proposal,
    ProposalError,
    RegenBudget,
    StateClaim,
    claim_from_mapping,
    load_golden_set,
    proposal_from_mapping,
    refusal_note,
    run_golden_set,
    validate_proposal,
)
from core.log import EventRecord, LoggedKnowledgeRecord, StateChange
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "validation_golden.json"
PLAYER = PACK.player_id()


def _ev(
    eid: str, t: int, etype: str, actor: str, cause: str | None,
    *, target: str | None = None,
    knowledge: tuple[LoggedKnowledgeRecord, ...] = (),
    changes: tuple[StateChange, ...] = (),
) -> EventRecord:
    return EventRecord(
        id=eid, t=t, type=etype, actor=actor, cause=cause, outcome={},
        knowledge=knowledge, state_changes=changes, hooks=(),
        importance="low", provenance={"seed": 42}, target=target,
    )


def _rec(who: str, knows: str, at: int, source: str) -> LoggedKnowledgeRecord:
    return LoggedKnowledgeRecord(
        who=who, channel="saw", fidelity="exact", knows=knows, at=at, source=source,
    )


def _events() -> list[EventRecord]:
    """The committed smoke-fixture log, rebuilt in memory (log hygiene: the
    fixture itself is read once in the golden-set tests below)."""
    return [
        _ev("ev_0000", 0, "move", PLAYER, None, target="loc_tavern",
            knowledge=(_rec("npc_guard_01", "pc_01_arrived", 0, "ev_0000"),),
            changes=(StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _ev("ev_0001", 5, "wait", PLAYER, "ev_0000"),
        _ev("ev_0002", 10, "move", PLAYER, "ev_0001", target="loc_backyard",
            changes=(StateChange("pc_01", "position", "loc_tavern", "loc_backyard"),)),
        _ev("ev_0003", 20, "wait", PLAYER, "ev_0002"),
        _ev("ev_0004", 30, "move", PLAYER, "ev_0003", target="loc_street",
            changes=(StateChange("pc_01", "position", "loc_backyard", "loc_street"),)),
        _ev("ev_0005", 58, "move", PLAYER, "ev_0004", target="loc_market",
            knowledge=(_rec("npc_market_crowd_01", "pc_01_arrived", 58, "ev_0005"),),
            changes=(StateChange("pc_01", "position", "loc_street", "loc_market"),)),
    ]


def _verdict_of(claims: tuple[Any, ...], events: list[EventRecord], anchor: int) -> ClaimVerdict:
    report = validate_proposal(Proposal(claims=claims, expected_event_seq=anchor), events, PACK)
    assert len(report.claim_verdicts) == len(claims)
    return report.claim_verdicts[0]


# -- purity: same inputs -> same report (INV-2, no RNG) ------------------------


def test_pure_function_of_inputs() -> None:
    events = _events()
    proposal = Proposal(
        claims=(
            StateClaim("pc_01", "position", "loc_market"),
            KnowledgeClaim("npc_guard_01", "pc_01_arrived"),
        ),
        expected_event_seq=len(events),
    )
    assert validate_proposal(proposal, events, PACK) == validate_proposal(proposal, events, PACK)


def test_empty_proposal_is_legal() -> None:
    report = validate_proposal(Proposal(expected_event_seq=6), _events(), PACK)
    assert report.claim_verdicts == ()
    assert not report.refused
    assert report.invented == 0 and report.unverifiable == 0


# -- the structural boundary (§2): the closed document -------------------------


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ({"kind": "vibe", "entity": "pc_01"}, "unknown claim kind"),
        ({"kind": "state", "entity": "pc_01", "prop": "position"}, "missing required keys"),
        (
            {
                "kind": "state", "entity": "pc_01", "prop": "position",
                "value": "loc_market", "prose": "you stand in the market",
            },
            "unknown keys",
        ),
        ({"kind": "knowledge", "who": "npc_guard_01"}, "missing required keys"),
        (
            {
                "kind": "knowledge", "who": "npc_guard_01", "knows": "x",
                "fidelity": "exact",
            },
            "unknown keys",
        ),
        ({"kind": "event", "event_id": "ev_0005", "actor": "pc_01"}, "unknown keys"),
        ({"kind": "state", "entity": "", "prop": "position", "value": None}, "non-empty string"),
        ("the guard saw a figure by the door", "must be an object"),
    ],
)
def test_claim_shape_is_loud(raw: Any, message: str) -> None:
    with pytest.raises(ProposalError, match=message):
        claim_from_mapping(raw)


def test_proposal_shape_is_loud() -> None:
    with pytest.raises(ProposalError, match="unknown keys"):
        proposal_from_mapping({"expected_event_seq": 0, "prose": "once upon a tavern"})
    with pytest.raises(ProposalError, match="non-negative integer"):
        proposal_from_mapping({"expected_event_seq": -1})
    with pytest.raises(ProposalError, match="must be lists"):
        proposal_from_mapping({"expected_event_seq": 0, "claims": {}})


def test_future_anchor_is_loud() -> None:
    with pytest.raises(ProposalError, match="in the future"):
        validate_proposal(Proposal(expected_event_seq=7), _events(), PACK)


def test_valid_documents_parse() -> None:
    proposal = proposal_from_mapping(
        {
            "expected_event_seq": 6,
            "claims": [
                {"kind": "state", "entity": "pc_01", "prop": "position", "value": "loc_market"},
                {"kind": "knowledge", "who": "npc_guard_01", "knows": "pc_01_arrived"},
                {"kind": "event", "event_id": "ev_0005", "type": "move"},
            ],
            "intents": [
                {"kind": "wait", "actor": "pc_01", "based_on_event_seq": 6, "fields": {"ticks": 5}},
            ],
        }
    )
    assert proposal.claims == (
        StateClaim("pc_01", "position", "loc_market"),
        KnowledgeClaim("npc_guard_01", "pc_01_arrived"),
        EventClaim("ev_0005", "move"),
    )
    assert proposal.intents[0].fields == {"ticks": 5}


# -- verdicts (§4): the honest-verdict truth table -----------------------------


def test_state_verdicts() -> None:
    events = _events()
    supported = _verdict_of((StateClaim("pc_01", "position", "loc_market"),), events, 6)
    assert (supported.verdict, supported.reason, supported.evidence) == (
        SUPPORTED, "matches_canon", "loc_market",
    )
    mismatch = _verdict_of((StateClaim("pc_01", "position", "loc_tavern"),), events, 6)
    assert (mismatch.verdict, mismatch.reason, mismatch.evidence) == (
        CONTRADICTED, "value_mismatch", "loc_market",
    )
    unmodeled = _verdict_of((StateClaim("npc_guard_01", "mood", "calm"),), events, 6)
    assert (unmodeled.verdict, unmodeled.reason) == (INSUFFICIENT_DATA, "unmodeled_prop")
    invented = _verdict_of((StateClaim("npc_ghost_99", "position", "loc_tavern"),), events, 6)
    assert (invented.verdict, invented.reason) == (CONTRADICTED, "unknown_entity")


def test_null_canonical_value_is_not_unmodeled() -> None:
    # carrier: null is a modeled value (the _MISSING sentinel law) — never
    # confused with an unmodeled prop.
    held = _verdict_of((StateClaim("oil_lamp_01", "carrier", None),), _events(), 6)
    assert (held.verdict, held.reason) == (SUPPORTED, "matches_canon")
    wrong = _verdict_of((StateClaim("oil_lamp_01", "carrier", "pc_01"),), _events(), 6)
    assert (wrong.verdict, wrong.reason, wrong.evidence) == (
        CONTRADICTED, "value_mismatch", None,
    )


def test_knowledge_verdicts() -> None:
    events = _events()
    held = _verdict_of((KnowledgeClaim("npc_market_crowd_01", "pc_01_arrived"),), events, 6)
    assert (held.verdict, held.reason, held.evidence) == (
        SUPPORTED, "matches_canon", "ev_0005",
    )
    blind = _verdict_of(
        (KnowledgeClaim("npc_market_crowd_01", "pc_01_left_toward_loc_backyard"),), events, 6
    )
    assert (blind.verdict, blind.reason) == (CONTRADICTED, "token_absent")
    stranger = _verdict_of((KnowledgeClaim("npc_stranger_77", "pc_01_arrived"),), events, 6)
    assert (stranger.verdict, stranger.reason) == (CONTRADICTED, "unknown_entity")
    item = _verdict_of((KnowledgeClaim("purse_01", "pc_01_arrived"),), events, 6)
    assert (item.verdict, item.reason) == (CONTRADICTED, "cannot_know")
    location = _verdict_of((KnowledgeClaim("loc_market", "pc_01_arrived"),), events, 6)
    assert (location.verdict, location.reason) == (CONTRADICTED, "cannot_know")


def test_event_verdicts() -> None:
    events = _events()
    ok = _verdict_of((EventClaim("ev_0005", "move"),), events, 6)
    assert (ok.verdict, ok.reason, ok.evidence) == (SUPPORTED, "matches_canon", "ev_0005")
    ok_no_type = _verdict_of((EventClaim("ev_0003"),), events, 6)
    assert ok_no_type.verdict == SUPPORTED
    missing = _verdict_of((EventClaim("ev_0009"),), events, 6)
    assert (missing.verdict, missing.reason) == (CONTRADICTED, "unknown_event")
    wrong_type = _verdict_of((EventClaim("ev_0005", "wait"),), events, 6)
    assert (wrong_type.verdict, wrong_type.reason, wrong_type.evidence) == (
        CONTRADICTED, "event_type_mismatch", "move",
    )


# -- ExpectedVersion OCC (§5): fresh / stale / rebased -------------------------


def test_fresh_proposal_is_never_marked_stale() -> None:
    events = _events()
    report = validate_proposal(
        Proposal(claims=(StateClaim("pc_01", "position", "loc_market"),), expected_event_seq=6),
        events, PACK,
    )
    assert not report.stale and report.rebased_to is None and not report.refused


def test_stale_all_hold_rebases() -> None:
    events = _events()
    report = validate_proposal(
        Proposal(
            claims=(
                StateClaim("pc_01", "position", "loc_market"),
                StateClaim("npc_guard_01", "position", "loc_tavern"),
            ),
            expected_event_seq=4,  # the log has moved (ev_0005) but nothing broke
        ),
        events, PACK,
    )
    assert report.stale and report.rebased_to == 6 and not report.refused
    assert all(v.verdict == SUPPORTED for v in report.claim_verdicts)


def test_stale_broken_attributed_to_first_breaker() -> None:
    report = validate_proposal(
        Proposal(claims=(StateClaim("pc_01", "position", "loc_street"),), expected_event_seq=5),
        _events(), PACK,
    )
    verdict = report.claim_verdicts[0]
    assert (verdict.verdict, verdict.reason, verdict.cause, verdict.evidence) == (
        CONTRADICTED, "stale_broken", "ev_0005", "loc_market",
    )
    assert report.refused and report.rebased_to is None


def test_stale_fabricated_is_value_mismatch_not_stale_broken() -> None:
    # loc_tavern was NOT the position at the anchor either — a fabrication,
    # not staleness; no cause is invented.
    report = validate_proposal(
        Proposal(claims=(StateClaim("pc_01", "position", "loc_tavern"),), expected_event_seq=4),
        _events(), PACK,
    )
    verdict = report.claim_verdicts[0]
    assert (verdict.verdict, verdict.reason, verdict.cause) == (
        CONTRADICTED, "value_mismatch", None,
    )


def test_first_break_wins_over_later_rebreaks() -> None:
    # position: street -> tavern (break) -> street (re-hold) -> backyard;
    # the FIRST breaker is the cause, per INTENT_SCHEMA §4 semantics.
    events = [
        _ev("ev_0000", 1, "move", PLAYER, None,
            changes=(StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _ev("ev_0001", 2, "move", PLAYER, "ev_0000",
            changes=(StateChange("pc_01", "position", "loc_tavern", "loc_street"),)),
        _ev("ev_0002", 3, "move", PLAYER, "ev_0001",
            changes=(StateChange("pc_01", "position", "loc_street", "loc_backyard"),)),
    ]
    report = validate_proposal(
        Proposal(claims=(StateClaim("pc_01", "position", "loc_street"),), expected_event_seq=0),
        events, PACK,
    )
    verdict = report.claim_verdicts[0]
    assert (verdict.verdict, verdict.reason, verdict.cause) == (
        CONTRADICTED, "stale_broken", "ev_0000",
    )


def test_knowledge_claims_never_flip_via_staleness() -> None:
    # the crowd's record was born AFTER the anchor — the claim was false at
    # the anchor, true in current canon: verdicts follow current canon, the
    # anchor never fabricates a contradiction (canon only grows).
    report = validate_proposal(
        Proposal(
            claims=(KnowledgeClaim("npc_market_crowd_01", "pc_01_arrived"),),
            expected_event_seq=4,
        ),
        _events(), PACK,
    )
    assert report.claim_verdicts[0].verdict == SUPPORTED
    assert report.stale and report.rebased_to == 6


# -- the fact transaction (§6): grammar gate, anchors untouched ----------------


def test_intent_passes_through_with_anchor_unchanged() -> None:
    intent = IntentProposal(
        kind="wait", actor=PLAYER, based_on_event_seq=4, fields={"ticks": 5}
    )
    report = validate_proposal(
        Proposal(expected_event_seq=4, intents=(intent,)), _events(), PACK
    )
    assert report.intent_proposals == (intent,)  # anchor untouched: the door re-checks


@pytest.mark.parametrize(
    ("intent", "message"),
    [
        (
            IntentProposal(kind="fireball", actor="pc_01", based_on_event_seq=6),
            "not in the pack action grammar",
        ),
        (
            IntentProposal(kind="wait", actor="pc_01", based_on_event_seq=6, fields={"foo": 1}),
            "takes no step fields",
        ),
        (IntentProposal(kind="steal", actor="pc_01", based_on_event_seq=6), "requires a target"),
        (IntentProposal(kind="wait", actor="npc_wizard_99", based_on_event_seq=6), "unknown actor"),
        (
            IntentProposal(kind="wait", actor="pc_01", based_on_event_seq=6, target="loc_nowhere"),
            "unknown target",
        ),
        (IntentProposal(kind="wait", actor="pc_01", based_on_event_seq=7), "in the future"),
    ],
)
def test_intent_grammar_is_loud(intent: IntentProposal, message: str) -> None:
    with pytest.raises(ProposalError, match=message):
        validate_proposal(Proposal(expected_event_seq=6, intents=(intent,)), _events(), PACK)


# -- the regen protocol (§7) ----------------------------------------------------


def test_regen_budget_two_then_dry() -> None:
    budget = RegenBudget()
    assert budget.max_regens == 2 and budget.used == 0 and not budget.exhausted
    assert budget.spend() is True  # regen 1
    assert budget.spend() is True  # regen 2
    assert budget.exhausted and budget.remaining == 0
    assert budget.spend() is False  # exhaustion -> dry mode for the beat
    assert budget.used == 2  # the counter never grows past the ceiling


def test_regen_budget_validates_ceiling() -> None:
    with pytest.raises(ProposalError, match=">= 0"):
        RegenBudget(max_regens=-1)


def test_refusal_note_lists_only_contradictions() -> None:
    report = validate_proposal(
        Proposal(
            claims=(
                StateClaim("pc_01", "position", "loc_tavern"),
                StateClaim("pc_01", "position", "loc_market"),
                KnowledgeClaim("npc_market_crowd_01", "pc_01_left_toward_loc_backyard"),
            ),
            expected_event_seq=6,
        ),
        _events(), PACK,
    )
    assert report.refused and report.invented == 2 and report.unverifiable == 0
    note = refusal_note(report)
    assert len(note) == 2
    assert note[0] == (
        "CONTRADICTED state pc_01.position == 'loc_tavern' "
        "(value_mismatch, canon: 'loc_market')"
    )
    assert note[1].startswith("CONTRADICTED knowledge npc_market_crowd_01 knows")


def test_refusal_note_carries_stale_cause() -> None:
    report = validate_proposal(
        Proposal(claims=(StateClaim("pc_01", "position", "loc_street"),), expected_event_seq=5),
        _events(), PACK,
    )
    assert refusal_note(report) == (
        "CONTRADICTED state pc_01.position == 'loc_street' "
        "(stale_broken, canon: 'loc_market', cause: ev_0005)",
    )


# -- golden-set plumbing (§9): computed, never LLM-judged -----------------------


def test_committed_golden_set_passes() -> None:
    golden = load_golden_set(GOLDEN)
    header, events = _read_fixture_log(golden.log)
    assert header["seed"] == 42
    report = run_golden_set(golden, events, PACK)
    assert report.ok, [r for r in report.results if not r.ok]
    assert report.passed == len(golden.cases)


def test_golden_set_pins_every_verdict() -> None:
    golden = load_golden_set(GOLDEN)
    expects = {case.expect for case in golden.cases}
    assert expects == {SUPPORTED, CONTRADICTED, INSUFFICIENT_DATA}


def test_golden_drift_is_loud() -> None:
    golden = load_golden_set(GOLDEN)
    header, events = _read_fixture_log(golden.log)
    wrong = GoldenCase(
        name="drift", claim=StateClaim("pc_01", "position", "loc_market"), expect=CONTRADICTED
    )
    report = run_golden_set(
        golden.__class__(log=golden.log, cases=(wrong,)), events, PACK
    )
    assert not report.ok and report.failed == 1
    assert report.results[0].actual == SUPPORTED  # the computed truth, never the label


def test_golden_set_shape_is_loud(tmp_path: Path) -> None:
    bad = tmp_path / "bad_golden.json"
    bad.write_text(
        '{"log": "x", "cases": [{"name": "a", "claim": {}, "expect": "supported"}]}',
        encoding="utf-8",
    )
    with pytest.raises(ProposalError, match="claim"):
        load_golden_set(bad)
    dup = tmp_path / "dup_golden.json"
    case = {"name": "a", "claim": {"kind": "event", "event_id": "ev_0000"}, "expect": "supported"}
    dup.write_text(json.dumps({"log": "x", "cases": [case, case]}), encoding="utf-8")
    with pytest.raises(ProposalError, match="duplicate golden case name"):
        load_golden_set(dup)


def _read_fixture_log(log_ref: str) -> tuple[dict[str, Any], list[EventRecord]]:
    from core.log import read_log

    return read_log(REPO / log_ref, SCHEMA)
