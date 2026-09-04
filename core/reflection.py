"""Reflection & memory compaction (leg-3, phase 4; `phases.md` §4 — the
Generative Agents reflection-on-recurrence donor, letta's
`summarize_messages_in_place` the named anti-pattern). The contract
owner is `docs/LEGEND_SPEC.md` (written just-in-time at this row, the
D-022 law); the runtime block is `rules.json::reflection` (linted by
`core/pack.py::_reflection`).

Unlike the echo and the traits (read models over the knowledge view),
reflection is a WRITE: compaction emits higher-level entries that are
themselves LOG ENTRIES — a reflection is an event minted through the
canon door, never a mutation of existing records. The originals are
never dropped and never edited (INV-1/INV-5: the append-only log is
the only truth; letta's in-place summarization is the anti-pattern
this module exists to refuse). What compacts: a knower whose held
records of a declared token family reach the block's `threshold`
(same tokens REPEATED — recurrence, the echo's renewal made known,
breadth staying the traits' business) mints ONE reflection event per
(knower, insight) for the whole run — the never-re-reflect law
(`view.holds` on the insight token: records are never dropped, so one
mint is final; a third recurrence changes nothing).

The reflection event's shape: the pack-declared `reflection.event`
type; `outcome` carries `about` (the insight token),
`provenance` (the `list[event_id]` of the source records it
summarizes — phases.md §4's provenance law: the source is always
queryable, the reflection a derived view, never a replacement), and
`recurrence` (the evidence count at mint); `knowledge` mints ONE
record for the reflector, channel `inferred` (P2d's channel — an
inference from one's own memory, not a perception), fidelity `exact`
(the reflection faithfully states what the knower holds; its
evidence's quality rides the provenance, not this record). The event
carries NO hooks and NO state changes: the director buffer is
untouched by construction (L6 — a reflection is knowledge-side canon,
never an entropy input; entropy reads observable state only,
DIRECTOR_SPEC §4) and the cascade terminates exactly as the leverage
and on_one-hop laws do. The insight record is ordinary knowledge from
then on — tellable onward at the telling reaction's own fidelity
decay, salient in the fold like any record.

The read side, two pure functions over the log: `stale_reflections`
(the stale law — a reflection whose provenance no longer resolves is
flagged and excluded from retrieval; in the runtime log this is
impossible by construction, INV-1 — originals are never dropped —
the flag exists for the DERIVED stores after offline scavenge
(leg-4's tombstones), and retr-1's retrieval must consult it), and
`expand_reflection` (the expansion law's demand side, the
`expand_trait` twin: every family record the reflector holds, in
acquisition order — evidence is evidence, not just the
threshold-crossing subset).

Determinism (INV-2): no RNG anywhere (reflection is an inference, not
a stochastic act — the telling rolls acceptance, the reflection does
not), iteration in event order and declaration order, provenance ids
deduped first-seen in acquisition order — construction order only.
The knower gate: kind `npc` only (an ambient group does not reflect
in v0.1 — the leverage knower law). A pack without a `reflection`
block yields nothing and the run is byte-identical to v0.1 (the
pack's own declaration is the gate, INV-3; the committed v0.1 pack
carries no block — DORMANT on landing, the arc-1 precedent, the
corpus price tagged in TASKS)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Final

from core.intent import pack_importance
from core.log import EventDraft, KnowledgeRecord

if TYPE_CHECKING:  # pack + view are duck-typed — no runtime cycle
    from core.knowledge import KnowledgeView
    from core.log import EventRecord, LoggedKnowledgeRecord
    from core.pack import Pack

__all__ = [
    "REFLECTION_BLOCK_KEYS",
    "REFLECTION_INSIGHT_KEYS",
    "expand_reflection",
    "reflection_drafts",
    "stale_reflections",
]

REFLECTION_BLOCK_KEYS: Final = ("event", "threshold", "reflections", "notes")
"""The closed `rules.json::reflection` key set (an unknown key is a lint
error, never a silent ignore): the reflection event's type, the
recurrence count that compacts, the insight table, prose."""

REFLECTION_INSIGHT_KEYS: Final = ("family", "notes")
"""The closed per-insight key set: the recurring knowledge-token family
whose held records count against the block's threshold (the traits'
`family` vocabulary — the same concept, one word), and prose."""


def reflection_drafts(
    pack: "Pack",
    view: "KnowledgeView",
    record: "EventRecord",
) -> Iterator[EventDraft]:
    """Yield the reflection drafts for one committed record: one per
    (knower, insight) whose family's held-record count just reached the
    block's threshold, in event order (lazy: the loop commits between
    yields, so the never-re-reflect gate rides the live view). A pack
    without a `reflection` block yields nothing (the v0.1 behavior,
    byte-identical — the pack's own declaration is the gate, INV-3)."""
    config: Mapping[str, Any] | None = pack.rules.get("reflection")
    if config is None:
        return
    threshold = int(config["threshold"])
    event_type = config["event"]
    table: Mapping[str, Mapping[str, Any]] = config["reflections"]
    seen: set[tuple[str, str]] = set()  # (knower, insight) minted this event
    for knowledge in record.knowledge:  # event order — deterministic
        if pack.kind_of(knowledge.who) != "npc":
            continue  # an ambient group does not reflect (v0.1)
        for insight, spec in table.items():  # declaration order
            if knowledge.knows not in spec["family"]:
                continue
            if (knowledge.who, insight) in seen:
                continue  # one reflection per (knower, insight) per event
            if view.holds(knowledge.who, insight):
                continue  # never re-reflect: the insight is already held
            family = frozenset(spec["family"])
            contributing = [
                held
                for held in view.records_of(knowledge.who)  # acquisition order
                if held.knows in family
            ]
            if len(contributing) < threshold:
                continue
            sources = list(
                dict.fromkeys(held.source for held in contributing)
            )
            seen.add((knowledge.who, insight))
            yield EventDraft(
                t=record.t,
                type=event_type,
                actor=knowledge.who,
                target=None,  # a reflection has no direct object
                cause=None,  # the loop chains the cause to the triggering event
                outcome={
                    "about": insight,
                    "provenance": sources,
                    "recurrence": len(contributing),
                },
                knowledge=(
                    KnowledgeRecord(
                        who=knowledge.who,
                        channel="inferred",  # type: ignore[arg-type]
                        fidelity="exact",
                        knows=insight,
                        at=record.t,
                    ),
                ),
                state_changes=(),  # the fact is the entry, not a delta
                hooks=(),  # never an entropy input (L6)
                importance=pack_importance(
                    pack.rules,
                    {knowledge.who},
                    irreversible=0,
                    hooks=0,
                    event_type=event_type,
                ),
                provenance={},  # the loop stamps the seed at commit
            )


def stale_reflections(
    pack: "Pack",
    events: Sequence["EventRecord"],
) -> frozenset[str]:
    """The stale law's read side: the ids of reflection events whose
    `outcome.provenance` ids do not all resolve within `events` — the
    screening the retrieval consumer (retr-1) must consult (a stale
    reflection is EXCLUDED from retrieval, phases.md §4). In the
    runtime log this folds empty by construction: originals are never
    dropped (INV-1), so every minted provenance id resolves. The flag
    earns its keep only in derived stores after offline scavenge
    (leg-4's tombstones — the log itself is never edited, INV-5). A
    pack without a `reflection` block folds empty; log order,
    deterministic."""
    config: Mapping[str, Any] | None = pack.rules.get("reflection")
    if config is None:
        return frozenset()
    event_type = config["event"]
    resolvable = {event.id for event in events}
    stale: set[str] = set()
    for event in events:
        if event.type != event_type:
            continue
        provenance = event.outcome.get("provenance")
        if not isinstance(provenance, Sequence) or isinstance(
            provenance, (str, bytes)
        ):
            continue  # a malformed outcome is validation's loud business
        if not all(
            isinstance(source, str) and source in resolvable
            for source in provenance
        ):
            stale.add(event.id)
    return frozenset(stale)


def expand_reflection(
    pack: "Pack",
    view: "KnowledgeView",
    reflection: "EventRecord",
) -> tuple["LoggedKnowledgeRecord", ...]:
    """The expansion law's demand side (the `expand_trait` twin): every
    family record the reflector holds, in acquisition order — the
    reflection's `outcome.provenance` is the mint-time subset, this is
    the live fold (evidence is evidence; a post-mint recurrence record
    expands too, though it never re-triggers). Pure: reads the view,
    writes nothing. An `about` token no longer declared folds to the
    empty tuple — the honest answer, never an error (the crafted-view
    law shared with the traits)."""
    config: Mapping[str, Any] | None = pack.rules.get("reflection")
    spec = (
        config["reflections"].get(reflection.outcome.get("about"))
        if config is not None
        else None
    )
    if spec is None:
        return ()
    family = frozenset(spec["family"])
    return tuple(
        held
        for held in view.records_of(reflection.actor)  # acquisition order
        if held.knows in family
    )
