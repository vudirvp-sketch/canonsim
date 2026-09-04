"""Trait crystallization (P3f, phase 4; `phases.md` §4 — the LEGEND_SPEC
sketch: 3+ related knowledge records collapse into a discrete belief
token; traits are derived state, never primary data). The runtime block
is `rules.json::traits` (linted by `core/pack.py::_traits`).

The fold is a READ MODEL, the echo's sibling (`core/echo.py`, iter-46):
when a knower holds at least `threshold` DISTINCT tokens from a declared
belief family, the belief crystallizes, carrying the contributing
records' source event ids as PROVENANCE — the expansion law (phases.md
§4, the reflection-provenance paragraph applied to traits): on demand,
the trait expands back to source records for the brief; the source is
always queryable, the belief a derived view, never a replacement. The
module writes NOTHING: no events, no knowledge, no hooks, no state
changes (INV-1 by construction). It renders nothing and feeds no
metric — a belief becomes visible only through the consumer that reads
it (the brief's derived-trait read, BRIEF_SPEC's phase-4 clause — leg-2,
`brief/assembler.py::_recalled_fact_lines`; `expand_trait` below is the
expansion law's demand side).

The DISTINCT-token law (v0.1 engine semantics): crystallization counts
breadth, not repetition — a family's held distinct tokens against the
threshold. Repetition is the echo's business (a token heard twice
renews the residue there); the never-re-learn law keeps duplicates rare
regardless, and the breadth reading keeps a family smaller than the
threshold honestly dead (the pack lint refuses it at load). The fold is
read as DATA at the caller's own tick: `at_tick` gates contribution (a
record born after it contributes nothing — the honest read-model law
shared with the echo); a crystallized belief itself has no decay term —
records are never dropped (INV-1), so the evidence holds while the log
holds, stability by construction, not by a timer.

The L6 fence (the echo's twin): a belief is per-NPC derived state over
the NPC's own records — never player-adapted, never an entropy input
(DIRECTOR_SPEC §4); the director is untouched by construction.

Determinism (INV-2): knowers in first-acquisition order, beliefs in
declaration order, sources in acquisition order deduped first-seen —
construction order only, no randomness anywhere in the fold. The pack
without a `traits` block folds to the empty tuple (the v0.1 behavior;
the pack's own declaration is the gate, INV-3)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:  # pack + view are duck-typed — no runtime imports
    from core.knowledge import KnowledgeView
    from core.log import LoggedKnowledgeRecord
    from core.pack import Pack

__all__ = [
    "TRAIT_BLOCK_KEYS",
    "TRAIT_BELIEF_KEYS",
    "Trait",
    "crystallized_traits",
    "expand_trait",
]

TRAIT_BLOCK_KEYS: Final = ("threshold", "beliefs", "notes")
"""The closed `rules.json::traits` key set (an unknown key is a lint
error, never a silent ignore): the family-size threshold that
crystallizes a belief, the belief table, prose."""

TRAIT_BELIEF_KEYS: Final = ("family", "notes")
"""The closed per-belief key set: the knowledge-token family whose held
distinct tokens count against the block's threshold, and prose."""


@dataclass(frozen=True, slots=True)
class Trait:
    """One knower's crystallized belief as derived by the read-side fold
    (`crystallized_traits`). `sources` carries the contributing records'
    event ids — the provenance the brief expands back to."""

    who: str
    token: str
    sources: tuple[str, ...]


def crystallized_traits(
    pack: "Pack",
    view: "KnowledgeView",
    at_tick: int,
) -> tuple[Trait, ...]:
    """The read-side fold: every knower's crystallized beliefs at
    `at_tick`. Knowers in first-acquisition order, beliefs in declaration
    order; `sources` in acquisition order, deduped first-seen (an event
    minting two family records is one source event, provenance is event
    ids). A pack without a `traits` block folds to the empty tuple; a
    family whose held distinct tokens sit below the threshold
    contributes nothing (the honest answer, never an error)."""
    config: Mapping[str, Any] | None = pack.rules.get("traits")
    if config is None:
        return ()
    threshold = int(config["threshold"])
    out: list[Trait] = []
    for who in view.knowers():
        for belief, spec in config["beliefs"].items():
            family = frozenset(spec["family"])
            contributing = [
                record
                for record in view.records_of(who)  # acquisition order
                if record.knows in family and record.at <= at_tick
            ]
            if len({record.knows for record in contributing}) < threshold:
                continue
            sources = tuple(
                dict.fromkeys(record.source for record in contributing)
            )
            out.append(Trait(who=who, token=belief, sources=sources))
    return tuple(out)


def expand_trait(
    pack: "Pack",
    view: "KnowledgeView",
    trait: Trait,
) -> tuple["LoggedKnowledgeRecord", ...]:
    """The expansion law's read side (phases.md §4, the reflection
    provenance paragraph applied to traits): the records a crystallized
    belief derives from, read back from the knowledge view in
    acquisition order — EVERY family record the knower holds, evidence
    is evidence, not just the threshold-crossing subset. The source is
    always queryable, the belief a derived view, never a replacement;
    the brief's derived-trait read (BRIEF_SPEC §3.5) replaces the raw
    family lines with the belief and hands the source ids to the
    consumer — this is the demand side of that contract. Pure: reads
    the view, writes nothing. A trait whose family the knower no longer
    fully mirrors (possible only in crafted views — records are never
    dropped, INV-1) still expands to whatever is held; an unknown
    belief token folds to the empty tuple, the honest answer."""
    config: Mapping[str, Any] | None = pack.rules.get("traits")
    spec = config["beliefs"].get(trait.token) if config is not None else None
    if spec is None:
        return ()
    family = frozenset(spec["family"])
    return tuple(
        record
        for record in view.records_of(trait.who)  # acquisition order
        if record.knows in family
    )
