"""The deterministic validator (VALIDATION_SPEC.md owns the contract;
`docs/blueprint/phases.md` §1 owns the donor design).

The mediator's gate between every LLM output and canon: `proposal → check →
commit → narrative`. This module is the LLM-free half — **a pure function of
(proposal, log, pack)** (the D-042 read-side family): no RNG, no wall-clock,
writes nothing to the log (INV-1), no network (INV-4 — the narrator call
itself is a later, owner-gated iteration). The commit step is the intent door
and only the intent door (D-037): intents pass through with their anchors
unchanged, ids stay writer-side, the validator never merges and never
executes.

The structural boundary (D-018): the validator accepts ONE closed structured
document shape — there is no prose field anywhere in it, so prompt injection
carries nothing that can cross into canon, and no post-hoc text sanitization
exists. Shape violations are loud (`ProposalError` — the emitter is the
author, author bugs crash); world content is judged softly by verdicts
(`supported | contradicted | insufficient_data`, the honest-verdict law:
canon never fabricates an opinion it does not hold).
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Literal

from core.fold import Projection, apply_event, fold, initial_projection
from core.intent import IntentData, RunnerError, validate_shape
from core.knowledge import KnowledgeView
from core.log import EventRecord
from core.pack import Pack

__all__ = [
    "CONTRADICTED",
    "Claim",
    "ClaimVerdict",
    "EventClaim",
    "GoldenCase",
    "GoldenReport",
    "GoldenResult",
    "GoldenSet",
    "INSUFFICIENT_DATA",
    "IntentProposal",
    "KnowledgeClaim",
    "MAX_REGENS",
    "Proposal",
    "ProposalError",
    "REASONS",
    "REGEN_EXHAUSTED",
    "RegenBudget",
    "SUPPORTED",
    "StateClaim",
    "Verdict",
    "claim_from_mapping",
    "intent_proposal_from_mapping",
    "load_golden_set",
    "proposal_from_mapping",
    "refusal_note",
    "run_golden_set",
    "validate_proposal",
]

# -- verdict vocabulary (architecture — VALIDATION_SPEC §4) --------------------

SUPPORTED: Final = "supported"
CONTRADICTED: Final = "contradicted"
INSUFFICIENT_DATA: Final = "insufficient_data"
Verdict = Literal["supported", "contradicted", "insufficient_data"]

#: Closed reason vocabulary — one per verdict cause, never prose.
REASONS: Final = (
    "matches_canon",
    "value_mismatch",
    "unmodeled_prop",
    "unknown_entity",
    "cannot_know",
    "token_absent",
    "unknown_event",
    "event_type_mismatch",
    "stale_broken",
)

#: The per-beat regen ceiling (VALIDATION_SPEC §7 — architecture, not pack data).
MAX_REGENS: Final = 2
#: The dry-mode signal returned when the regen budget is exhausted.
REGEN_EXHAUSTED: Final = False

_MISSING: Final = object()  # tells "prop absent" from "prop holds null"


class ProposalError(RuntimeError):
    """Document-shape violation: the emitter is the author, author bugs crash."""


# -- the proposal document (VALIDATION_SPEC §3) --------------------------------


@dataclass(frozen=True, slots=True)
class StateClaim:
    """`state` claim: the projection holds exactly this value on this entity."""

    entity: str
    prop: str
    value: Any


@dataclass(frozen=True, slots=True)
class KnowledgeClaim:
    """`knowledge` claim: the knower holds this token (channel and fidelity
    are render details, never claim fields — VALIDATION_SPEC §3)."""

    who: str
    knows: str


@dataclass(frozen=True, slots=True)
class EventClaim:
    """`event` claim: this event exists, with this type (when given)."""

    event_id: str
    type: str | None = None


Claim = StateClaim | KnowledgeClaim | EventClaim


@dataclass(frozen=True, slots=True)
class IntentProposal:
    """One fact proposal for the intent door (INTENT_SCHEMA §2 grammar —
    the phase-2 C-parser's target shape). `based_on_event_seq` is the OCC
    anchor; the door re-checks it at completion — one mechanism."""

    kind: str
    actor: str
    based_on_event_seq: int
    target: str | None = None
    fields: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Proposal:
    """One narrator call's structured side-band (the closed document —
    the structural injection-neutralization boundary, VALIDATION_SPEC §2)."""

    expected_event_seq: int
    claims: tuple[Claim, ...] = ()
    intents: tuple[IntentProposal, ...] = ()


# -- JSON boundary parsing (loud; the closed document, §2/§3) ------------------


def _mapping(data: Any, what: str) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise ProposalError(f"{what} must be an object, got {type(data).__name__}")
    return data


def _exact_keys(
    data: Mapping[str, Any], required: tuple[str, ...], optional: tuple[str, ...], what: str
) -> None:
    missing = [key for key in required if key not in data]
    if missing:
        raise ProposalError(f"{what}: missing required keys {missing}")
    allowed = set(required) | set(optional)
    unknown = [key for key in data if key not in allowed]
    if unknown:
        raise ProposalError(
            f"{what}: unknown keys {sorted(unknown)} — the document is closed "
            f"(VALIDATION_SPEC §3)"
        )


def _non_empty_str(value: Any, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProposalError(f"{what} must be a non-empty string, got {value!r}")
    return value


def _seq(value: Any, what: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ProposalError(f"{what} must be a non-negative integer, got {value!r}")
    return value


def claim_from_mapping(data: Any) -> Claim:
    """Parse one claim (loud on any shape drift — closed kinds, closed keys)."""
    doc = _mapping(data, "claim")
    kind = doc.get("kind")
    if kind == "state":
        _exact_keys(doc, ("kind", "entity", "prop", "value"), (), "state claim")
        return StateClaim(
            entity=_non_empty_str(doc["entity"], "state claim entity"),
            prop=_non_empty_str(doc["prop"], "state claim prop"),
            value=doc["value"],
        )
    if kind == "knowledge":
        _exact_keys(doc, ("kind", "who", "knows"), (), "knowledge claim")
        return KnowledgeClaim(
            who=_non_empty_str(doc["who"], "knowledge claim who"),
            knows=_non_empty_str(doc["knows"], "knowledge claim knows"),
        )
    if kind == "event":
        _exact_keys(doc, ("kind", "event_id"), ("type",), "event claim")
        etype = doc.get("type")
        return EventClaim(
            event_id=_non_empty_str(doc["event_id"], "event claim event_id"),
            type=None if etype is None else _non_empty_str(etype, "event claim type"),
        )
    raise ProposalError(f"unknown claim kind {kind!r} (state | knowledge | event)")


def intent_proposal_from_mapping(data: Any) -> IntentProposal:
    """Parse one intent proposal (INTENT_SCHEMA §2 grammar, loud)."""
    doc = _mapping(data, "intent proposal")
    _exact_keys(doc, ("kind", "actor", "based_on_event_seq"), ("target", "fields"), "intent")
    fields = doc.get("fields", {})
    if not isinstance(fields, Mapping):
        raise ProposalError("intent fields must be an object")
    target = doc.get("target")
    return IntentProposal(
        kind=_non_empty_str(doc["kind"], "intent kind"),
        actor=_non_empty_str(doc["actor"], "intent actor"),
        based_on_event_seq=_seq(
            doc["based_on_event_seq"], "intent based_on_event_seq"
        ),
        target=None if target is None else _non_empty_str(target, "intent target"),
        fields=dict(fields),
    )


def proposal_from_mapping(data: Any) -> Proposal:
    """Parse the proposal document (the JSON boundary — loud, closed)."""
    doc = _mapping(data, "proposal")
    _exact_keys(doc, ("expected_event_seq",), ("claims", "intents"), "proposal")
    raw_claims = doc.get("claims", [])
    raw_intents = doc.get("intents", [])
    if not isinstance(raw_claims, list) or not isinstance(raw_intents, list):
        raise ProposalError("proposal claims and intents must be lists")
    return Proposal(
        expected_event_seq=_seq(doc["expected_event_seq"], "proposal expected_event_seq"),
        claims=tuple(claim_from_mapping(claim) for claim in raw_claims),
        intents=tuple(intent_proposal_from_mapping(intent) for intent in raw_intents),
    )


# -- verdicts (VALIDATION_SPEC §4 — the honest-verdict law) ---------------------


@dataclass(frozen=True, slots=True)
class ClaimVerdict:
    """One claim's judgment: the verdict, the closed reason, and structured
    evidence (the canon value / actual type / source event) plus the breaking
    event id when staleness flipped the claim (§5)."""

    claim: Claim
    verdict: Verdict
    reason: str
    evidence: Any = None
    cause: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """The validation outcome for one proposal: per-claim verdicts against
    current canon, the OCC resolution, and the shape-checked intents ready
    for the door (anchors untouched — §6)."""

    claim_verdicts: tuple[ClaimVerdict, ...]
    stale: bool
    rebased_to: int | None
    intent_proposals: tuple[IntentProposal, ...]

    @property
    def refused(self) -> bool:
        """Any contradicted claim — the §7 refusal trigger."""
        return any(v.verdict == CONTRADICTED for v in self.claim_verdicts)

    @property
    def invented(self) -> int:
        """The invented-facts count (bg-3's harness metric)."""
        return sum(1 for v in self.claim_verdicts if v.verdict == CONTRADICTED)

    @property
    def unverifiable(self) -> int:
        """How many claims canon cannot judge (unmodeled — never fabricated)."""
        return sum(1 for v in self.claim_verdicts if v.verdict == INSUFFICIENT_DATA)


def _state_verdict(
    claim: StateClaim, pack: Pack, state: Projection, cause: str | None
) -> ClaimVerdict:
    if pack.kind_of(claim.entity) is None:
        return ClaimVerdict(claim, CONTRADICTED, "unknown_entity")
    value = state.get(claim.entity, {}).get(claim.prop, _MISSING)
    if value is _MISSING:
        return ClaimVerdict(claim, INSUFFICIENT_DATA, "unmodeled_prop")
    if value == claim.value:
        return ClaimVerdict(claim, SUPPORTED, "matches_canon", evidence=value)
    if cause is not None:  # held at the anchor, broke since (§5 invariant)
        return ClaimVerdict(claim, CONTRADICTED, "stale_broken", evidence=value, cause=cause)
    return ClaimVerdict(claim, CONTRADICTED, "value_mismatch", evidence=value)


def _knowledge_verdict(claim: KnowledgeClaim, pack: Pack, view: KnowledgeView) -> ClaimVerdict:
    kind = pack.kind_of(claim.who)
    if kind is None:
        return ClaimVerdict(claim, CONTRADICTED, "unknown_entity")
    if kind in ("item", "location"):
        return ClaimVerdict(claim, CONTRADICTED, "cannot_know")
    if view.holds(claim.who, claim.knows):
        source = next(
            (r.source for r in view.records_of(claim.who) if r.knows == claim.knows), None
        )
        return ClaimVerdict(claim, SUPPORTED, "matches_canon", evidence=source)
    return ClaimVerdict(claim, CONTRADICTED, "token_absent")


def _event_verdict(
    claim: EventClaim, events_by_id: Mapping[str, EventRecord]
) -> ClaimVerdict:
    event = events_by_id.get(claim.event_id)
    if event is None:
        return ClaimVerdict(claim, CONTRADICTED, "unknown_event")
    if claim.type is not None and event.type != claim.type:
        return ClaimVerdict(claim, CONTRADICTED, "event_type_mismatch", evidence=event.type)
    return ClaimVerdict(claim, SUPPORTED, "matches_canon", evidence=event.id)


def _checked_intent(intent: IntentProposal, pack: Pack, current_seq: int) -> IntentProposal:
    """The fact-transaction grammar gate (§6): loud on a kind outside the
    pack's action grammar, an unknown actor/target entity, a future anchor,
    or field/target violations (reusing the door's own shape law). The
    returned proposal is the pass-through — anchor untouched, id assignment
    stays writer-side (INTENT_SCHEMA §2)."""
    action = pack.action(intent.kind)
    if action is None:
        raise ProposalError(f"intent kind {intent.kind!r} is not in the pack action grammar")
    if pack.kind_of(intent.actor) is None:
        raise ProposalError(f"intent {intent.kind!r}: unknown actor {intent.actor!r}")
    if intent.target is not None and pack.kind_of(intent.target) is None:
        raise ProposalError(f"intent {intent.kind!r}: unknown target {intent.target!r}")
    if intent.based_on_event_seq > current_seq:
        raise ProposalError(
            f"intent {intent.kind!r}: based_on_event_seq {intent.based_on_event_seq} "
            f"is in the future (the log holds {current_seq} events)"
        )
    probe = IntentData(  # throwaway: validate_shape reads kind/target/fields only
        id="intent_shape_probe", kind=intent.kind, actor=intent.actor,
        target=intent.target, fields=dict(intent.fields),
        based_on_event_seq=intent.based_on_event_seq,
    )
    try:
        validate_shape(action, probe)
    except RunnerError as exc:
        raise ProposalError(f"intent {intent.kind!r}: {exc}") from exc
    return intent


def validate_proposal(
    proposal: Proposal, events: Sequence[EventRecord], pack: Pack
) -> ValidationReport:
    """Validate one proposal against the log (pure — VALIDATION_SPEC §2–§6).

    Verdicts are always evaluated against current canon; the anchor decides
    fresh / stale / rebased (§5). Stale proposals are never accepted on their
    own terms: every claim is re-validated, a claim that held at the anchor
    and broke since is attributed to the first breaking event (the
    INTENT_SCHEMA §4 first-break semantics); an all-hold stale proposal is
    rebased. Knowledge and events only grow, so only state claims can flip
    via staleness.
    """
    current = len(events)
    anchor = proposal.expected_event_seq
    if anchor > current:
        raise ProposalError(
            f"expected_event_seq {anchor} is in the future (the log holds {current} events)"
        )
    intents = tuple(_checked_intent(intent, pack, current) for intent in proposal.intents)
    if not proposal.claims:
        return ValidationReport(
            claim_verdicts=(),
            stale=anchor < current,
            rebased_to=current if anchor < current else None,
            intent_proposals=intents,
        )

    initial = initial_projection(pack.entities)
    if anchor == current:
        state_now = fold(events, initial)
        attribution: dict[int, str] = {}
    else:
        state_anchor = fold(events[:anchor], initial)
        pending = {
            index: claim
            for index, claim in enumerate(proposal.claims)
            if isinstance(claim, StateClaim)
            and state_anchor.get(claim.entity, {}).get(claim.prop, _MISSING) == claim.value
        }
        state_now = {entity: dict(props) for entity, props in state_anchor.items()}
        attribution = {}
        for index in range(anchor, current):
            apply_event(state_now, events[index])
            for idx, claim in list(pending.items()):
                if state_now.get(claim.entity, {}).get(claim.prop, _MISSING) != claim.value:
                    attribution[idx] = events[index].id  # first break wins
                    del pending[idx]

    view = KnowledgeView.from_events(events)
    events_by_id = {event.id: event for event in events}
    verdicts = []
    for index, claim in enumerate(proposal.claims):
        if isinstance(claim, StateClaim):
            verdicts.append(_state_verdict(claim, pack, state_now, attribution.get(index)))
        elif isinstance(claim, KnowledgeClaim):
            verdicts.append(_knowledge_verdict(claim, pack, view))
        else:
            verdicts.append(_event_verdict(claim, events_by_id))
    refused = any(v.verdict == CONTRADICTED for v in verdicts)
    return ValidationReport(
        claim_verdicts=tuple(verdicts),
        stale=anchor < current,
        rebased_to=current if anchor < current and not refused else None,
        intent_proposals=intents,
    )


# -- the regen protocol (VALIDATION_SPEC §7) ------------------------------------


@dataclass(slots=True)
class RegenBudget:
    """The per-beat regen counter: ≤2 regens, exhaustion → dry mode (L12) —
    never a silent drop, never a blocked beat. Session render state: the
    boundary constructs one per beat; the counter is the §7 law's executable
    form (the narrator call itself is the owner-gated half)."""

    max_regens: int = MAX_REGENS
    used: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.max_regens, int) or isinstance(self.max_regens, bool):
            raise ProposalError(f"max_regens must be an integer, got {self.max_regens!r}")
        if self.max_regens < 0:
            raise ProposalError(f"max_regens must be >= 0, got {self.max_regens!r}")

    @property
    def remaining(self) -> int:
        return max(0, self.max_regens - self.used)

    @property
    def exhausted(self) -> bool:
        return self.used >= self.max_regens

    def spend(self) -> bool:
        """Consume one regen. True = regen granted; REGEN_EXHAUSTED = the
        budget is spent, the beat falls to dry mode (the L12 floor)."""
        if self.exhausted:
            return REGEN_EXHAUSTED
        self.used += 1
        return True


def _describe(claim: Claim) -> str:
    if isinstance(claim, StateClaim):
        return f"state {claim.entity}.{claim.prop} == {claim.value!r}"
    if isinstance(claim, KnowledgeClaim):
        return f"knowledge {claim.who} knows {claim.knows!r}"
    suffix = f" type {claim.type!r}" if claim.type is not None else ""
    return f"event {claim.event_id}{suffix}"


def refusal_note(report: ValidationReport) -> tuple[str, ...]:
    """The dry structured refusal lines riding the next narrator call's
    directives (D-049): one line per contradicted claim — reason, canon's
    evidence, the breaking cause when staleness flipped it. Supported and
    unverifiable claims never appear (only what must change does)."""
    lines: list[str] = []
    for verdict in report.claim_verdicts:
        if verdict.verdict != CONTRADICTED:
            continue
        line = f"CONTRADICTED {_describe(verdict.claim)} ({verdict.reason}"
        if verdict.evidence is not None:
            line += f", canon: {verdict.evidence!r}"
        if verdict.cause is not None:
            line += f", cause: {verdict.cause}"
        lines.append(line + ")")
    return tuple(lines)


# -- golden-set plumbing (VALIDATION_SPEC §9 — computed, never LLM-judged) ------


@dataclass(frozen=True, slots=True)
class GoldenCase:
    """One pinned verdict expectation against the golden set's log."""

    name: str
    claim: Claim
    expect: Verdict


@dataclass(frozen=True, slots=True)
class GoldenSet:
    """A committed golden-set document: the referenced log (repo-relative
    path) + the cases. Pins §4 semantics; regressions are loud by diff."""

    log: str
    cases: tuple[GoldenCase, ...]


@dataclass(frozen=True, slots=True)
class GoldenResult:
    name: str
    expected: Verdict
    actual: Verdict

    @property
    def ok(self) -> bool:
        return self.expected == self.actual


@dataclass(frozen=True, slots=True)
class GoldenReport:
    results: tuple[GoldenResult, ...]

    @property
    def passed(self) -> int:
        return sum(1 for result in self.results if result.ok)

    @property
    def failed(self) -> int:
        return sum(1 for result in self.results if not result.ok)

    @property
    def ok(self) -> bool:
        return self.failed == 0


def load_golden_set(path: Path) -> GoldenSet:
    """Load and shape-check a golden-set JSON document (loud on drift —
    the fixture is test data; a malformed fixture is an author bug)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProposalError(f"golden set {path}: unreadable ({exc})") from exc
    doc = _mapping(data, f"golden set {path}")
    _exact_keys(doc, ("log", "cases"), (), f"golden set {path}")
    raw_cases = doc["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ProposalError(f"golden set {path}: cases must be a non-empty list")
    cases: list[GoldenCase] = []
    names: set[str] = set()
    for raw in raw_cases:
        case = _mapping(raw, "golden case")
        _exact_keys(case, ("name", "claim", "expect"), (), "golden case")
        name = _non_empty_str(case["name"], "golden case name")
        if name in names:
            raise ProposalError(f"duplicate golden case name {name!r}")
        names.add(name)
        expect = case["expect"]
        if expect not in (SUPPORTED, CONTRADICTED, INSUFFICIENT_DATA):
            raise ProposalError(
                f"golden case {name!r}: expect must be one of "
                f"{[SUPPORTED, CONTRADICTED, INSUFFICIENT_DATA]}, got {expect!r}"
            )
        cases.append(
            GoldenCase(name=name, claim=claim_from_mapping(case["claim"]), expect=expect)
        )
    return GoldenSet(
        log=_non_empty_str(doc["log"], "golden set log"), cases=tuple(cases)
    )


def run_golden_set(
    golden: GoldenSet, events: Sequence[EventRecord], pack: Pack
) -> GoldenReport:
    """Compute every case's verdict and diff it against the expectation —
    a pure dict-equality comparison; no LLM judges anything, ever. Each case
    runs as a fresh one-claim proposal anchored at the log's end (§4 pins
    verdict semantics; the stale flow lives in the unit suite)."""
    results = []
    for case in golden.cases:
        report = validate_proposal(
            Proposal(claims=(case.claim,), expected_event_seq=len(events)), events, pack
        )
        actual = report.claim_verdicts[0].verdict
        results.append(
            GoldenResult(name=case.name, expected=case.expect, actual=actual)
        )
    return GoldenReport(results=tuple(results))
