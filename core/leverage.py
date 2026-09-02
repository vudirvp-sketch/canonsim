"""The secrets & leverage system (social-1, phase 3; `phases.md` §3 P3a —
the CK3 `add_hook` precedent: secrets and leverage as first-class FACT
CLUSTERS, a hook IS an event). The donor mechanics live in
`docs/ref/paradox_scripting.md`; the runtime block is `rules.json::secrets`
(linted by `core/pack.py::_secrets`).

What the donor gave, minus its mutable-state footgun: CK3's
`add_hook = {type, target, secret, days}` writes leverage into a
character's hook list — mutable state. Our adaptation keeps the cluster
SHAPE (holder, subject, the secret token, a type, an expiry tick, a
cause) but the leverage is born as an EVENT and never mutates: the
liveness window is a read-side fold (INV-1 — the fact is immutable, its
expiry is derived), the spend is a future event, not a mutation. The
word "hook" itself is taken: the director's `SeededHook` owns it (D-005,
a deferred consequence tag); the CK3 hook is our LEVERAGE — a social
fact, never a release.

The birth law: a committed event's knowledge records ride the reaction
cascade (`loop._react`); a record whose token the pack's `secrets` table
declares, held by a NOVEL knower (the crime reaction's novelty law —
`view.holds(..., before_source=record.id)`), mints ONE fact event per
(knower, token) pair, in event order. Told secrets confer leverage too
(the transfer event's records are knowledge like any other) — a secret
learned second-hand is still leverage, at the acquisition's own fidelity
(the cluster records how well the holder knows it). The holder guards:
kind npc (an ambient group is not a social actor in v0.1 — a group
entity never holds leverage), and holder != subject (nobody holds
leverage over themselves).

The cluster carries NO knowledge (the holder's knowledge record is the
epistemic fact; the leverage event is the social fact — the subject must
not learn of it), NO hooks (D-005 — deferred consequences ride the
actions' own hooks), NO state changes (the fact is the cluster, not a
delta): the reaction systems skip it by construction, so the cascade
terminates exactly as the on_action one-hop law does (DIRECTOR_SPEC §3c).

The spend (social-1b, iter-45): the coerce door — the fact cluster's
first runtime consumer. The spend is a NEW EVENT naming the cluster's
id in its `outcome.cluster` (never a mutation — INV-1): the fold treats
a cluster as dead from its spend event's tick on, exactly as expiry
does. The pack declares the spend's event type in `secrets.spend_event`
(the action producing it must carry the `leverage_over` precondition —
the pack lint owns that contract). `spendable_leverage` picks the fact
a spend consumes: the first live fact with the holder/subject pair, in
log order (deterministic).

Pure per INV-2: a function of (pack data, knowledge view, record) with
no RNG, no clock (only `record.t`), iteration in event order; the
generator is lazy (each draft is built only when consumed — the KI#13
discipline)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.intent import RunnerError, pack_importance
from core.log import EventDraft

if TYPE_CHECKING:  # pack + view are duck-typed — no runtime cycle
    from core.knowledge import KnowledgeView
    from core.log import EventRecord
    from core.pack import Pack

__all__ = [
    "SECRETS_BLOCK_KEYS",
    "TOKEN_KEYS",
    "LeverageFact",
    "leverage_drafts",
    "live_leverage",
    "spendable_leverage",
]

SECRETS_BLOCK_KEYS: Final = ("event", "spend_event", "tokens", "notes")
"""The closed `rules.json::secrets` key set (an unknown key is a lint
error, never a silent ignore): the fact event's type, the spend event's
type (optional — absent means the pack declares clusters no action can
spend; they simply expire), the token table, prose."""

TOKEN_KEYS: Final = ("subject", "type", "expires_ticks")
"""The closed per-token key set: the secret's subject (whom the cluster
targets), the leverage type (the donor's `type` — what the holder can do
with it; v0.1 vocabulary, no consumer yet), and the expiry window in
ticks (the donor's `days`)."""


@dataclass(frozen=True, slots=True)
class LeverageFact:
    """One leverage fact as derived by the read-side fold (`live_leverage`).

    `source` is the fact event's id — the future spend path references
    it (a spend is a new event naming its cluster, never a mutation).
    """

    holder: str
    subject: str
    secret: str
    type: str
    expires_at: int
    source: str


def leverage_drafts(
    pack: "Pack",
    view: "KnowledgeView",
    record: "EventRecord",
) -> Iterator[EventDraft]:
    """Yield the leverage fact-cluster drafts for one committed record,
    one per novel (knower, token) pair in event order (lazy: the loop
    commits between yields). A pack without a `secrets` block yields
    nothing (the v0.1 behavior, byte-identical — the pack's own
    declaration is the gate, INV-3)."""
    config = pack.rules.get("secrets")
    if config is None:
        return
    tokens: Mapping[str, Mapping[str, Any]] = config.get("tokens", {})
    event_type = config["event"]
    seen: set[tuple[str, str]] = set()
    for knowledge in record.knowledge:  # event order — deterministic
        spec = tokens.get(knowledge.knows)
        if spec is None:
            continue
        if view.holds(knowledge.who, knowledge.knows, before_source=record.id):
            continue  # not novel: the knower already holds the token
        if knowledge.who == spec["subject"]:
            continue  # nobody holds leverage over themselves
        if pack.kind_of(knowledge.who) != "npc":
            continue  # crowds and items never hold leverage (v0.1)
        if (knowledge.who, knowledge.knows) in seen:
            continue  # one cluster per (knower, token) per event
        seen.add((knowledge.who, knowledge.knows))
        yield EventDraft(
            t=record.t,
            type=event_type,
            actor=knowledge.who,
            target=spec["subject"],
            cause=None,  # the loop chains the cause to the triggering event
            outcome={
                "secret": knowledge.knows,
                "type": spec["type"],
                "fidelity": knowledge.fidelity,
                "expires_at": record.t + int(spec["expires_ticks"]),
            },
            knowledge=(),  # the social fact, not an epistemic one
            state_changes=(),  # the fact IS the cluster, not a delta
            hooks=(),  # deferred consequences ride the actions (D-005)
            importance=pack_importance(
                pack.rules,
                {knowledge.who, spec["subject"]},
                irreversible=0,
                hooks=0,
                event_type=event_type,
            ),
            provenance={},  # the loop stamps the seed at commit
        )


def live_leverage(
    pack: "Pack",
    events: Sequence["EventRecord"],
    at_tick: int,
) -> tuple[LeverageFact, ...]:
    """The read-side fold: every leverage fact live at `at_tick`, in log
    order. Liveness is a window, never an event (INV-1 — the immutable
    fact expires by derivation): live iff `at_tick < expires_at`, dead at
    the boundary tick itself — and dead from the tick of the event that
    SPENT it (the spend names the cluster's id in `outcome.cluster`; the
    holder cannot milk one secret twice). A pack without a `secrets` block
    folds to the empty tuple. The spend (a new event naming `source`)
    joined with the first consumer, iter-45: the fold's shape supports
    it by construction — a second pass over the log, not a log edit."""
    config = pack.rules.get("secrets")
    if config is None:
        return ()
    event_type = config["event"]
    spend_type = config.get("spend_event")
    spent: set[str] = set()
    if spend_type is not None:
        for event in events:
            if event.type == spend_type and event.t <= at_tick:
                cluster = event.outcome.get("cluster")
                if isinstance(cluster, str):
                    spent.add(cluster)
    facts: list[LeverageFact] = []
    for event in events:
        if event.type != event_type:
            continue
        if event.id in spent:
            continue
        expires_at = int(event.outcome["expires_at"])
        if at_tick >= expires_at:
            continue
        facts.append(
            LeverageFact(
                holder=event.actor,
                subject=event.target,
                secret=str(event.outcome["secret"]),
                type=str(event.outcome["type"]),
                expires_at=expires_at,
                source=event.id,
            )
        )
    return tuple(facts)


def spendable_leverage(
    facts: Sequence[LeverageFact], holder: str, subject: str
) -> LeverageFact:
    """The fact a spend consumes: the first live fact with the
    holder/subject pair, in log order — deterministic. Loud when none
    exists (a spend without a live cluster is unreachable by construction:
    the `leverage_over` precondition gates the door and the OCC re-check;
    reaching this with an empty fold is a contract break, never a silent
    no-op — the KI#15 family)."""
    for fact in facts:
        if fact.holder == holder and fact.subject == subject:
            return fact
    raise RunnerError(
        f"no live leverage held by {holder!r} over {subject!r} — the spend "
        "requires a live fact cluster (the leverage_over precondition and "
        "the OCC re-check guarantee one; reaching here empty is a contract "
        "break)"
    )
