"""The narrator boundary's document layer (iter-12, D-055 — the
agent-in-the-loop door; format owner `docs/BRIEF_SPEC.md` §7.1, protocol
owner `docs/VALIDATION_SPEC.md` §7.1).

The narrator lives OUTSIDE the codebase: the dev-time engine is the
owner's assistant (or any operator) reading a call document and writing a
reply document; local inference (llama.cpp + GBNF, `TECH_NOTES.md` §1)
and any frontend integration stay deferred to the phase-1 gate
(`ROADMAP.md` §6). This module holds the boundary's PURE half — document
assembly and inspection as functions of (log, ledger, pack):

- the **call document** = the brief (BRIEF_SPEC §7 bytes, unchanged) plus
  one `narrator_protocol` section (actor / anchor / regen counter /
  query + retrieval rows / refusal notes) — everything the external
  narrator may draw on for one beat; mode B (scene-1) passes
  `knower=<npc>` — the actor call, one NPC per call, the chorus queue's
  own document (the actor line names whose beat-projection it carries);
  mode B's session wiring (scene-2) also passes the **keyword query**
  that ranked the actor's memory (§3.5's relevance signal — the `query:`
  line) and the retrieval ladder's top rows for it (the `retrieval:`
  lines — dry demand handles: the evidence and lore the query surfaced,
  source event ids inline, the ladder's precedence law visible in the
  order); mode A's bytes carry neither — the committed corpus shape;
- the **response document** — one CLOSED document `{prose, texture_delta?,
  proposal?}`: prose for the player, the structural texture delta, and
  the fact proposal, all in the same call (one call, two jobs, D-049).
  The deep shape gates run HERE, at the boundary: a malformed document
  raises the DeltaError/ProposalError family loudly, and the mediator's
  ladder (cli/) catches it BEFORE the gateway is invoked — the gates
  never guess, never repair (VALIDATION_SPEC §2);
- **feedable intents** — the mediator's noun resolution: proposal intents
  survive to the door only when their texture entry is live (an
  unresolvable noun never becomes an Intent — blueprint §1), the actor
  is the call's own caller (scene-2's mode-B half: a reply proposes its
  own caller's actions — mode A's caller is the player, mode B's the
  actor whose call the reply answers), and no two intents ride the same
  texture entry (a duplicate promotion would crash `mark_promoted`'s
  live-only law). Withdrawals are notes, never events (the texture-OCC
  mirror).

No RNG, no wall-clock, no I/O, writes nothing (INV-1/2/4; the D-049
determinism quarantine — same (log, ledger, pack) → same call bytes).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from brief.assembler import assemble_brief, render_brief
from brief.ledger import (
    SceneLedger,
    check_delta_shape,
    split_scope,
)
from brief.validator import (
    MAX_REGENS,
    IntentProposal,
    Proposal,
    proposal_from_mapping,
)
from core.log import EventRecord
from core.pack import Pack
from core.retrieval import Retrieved

__all__ = [
    "PROTOCOL_BLOCK",
    "RETRIEVAL_LINES",
    "NarratorError",
    "NarratorResponse",
    "feedable_intents",
    "narrator_call",
    "narrator_response_from_mapping",
    "promotions_in",
]

#: The protocol section's block id (BRIEF_SPEC §7.1 block geometry).
PROTOCOL_BLOCK: Final = "narrator_protocol"

#: The actor call's retrieval-line budget (BRIEF_SPEC §7.1 — the
#: protocol's own geometry, architecture not balance: the ladder's top
#: rows ride as dry demand handles, capped by the document's line
#: budget the way the notes ride uncapped-free but bounded by design).
RETRIEVAL_LINES: Final = 3


class NarratorError(RuntimeError):
    """The response document's outer shape violation: the emitter (the
    external narrator) is outside the codebase, so the boundary treats
    this family as MALFORMED output — the ladder (regen → dry) handles it
    BEFORE any gate runs (VALIDATION_SPEC §2); it never crashes a beat."""


@dataclass(frozen=True, slots=True)
class NarratorResponse:
    """One narrator reply, parsed: the prose (the beat's narrative —
    always present), plus the optional structural side-band — the texture
    delta and the fact proposal — deep-gated at the boundary."""

    prose: str
    texture_delta: Mapping[str, Any] | None
    proposal: Proposal | None


def narrator_response_from_mapping(doc: Any) -> NarratorResponse:
    """Parse the response document (closed — VALIDATION_SPEC §7.1).

    `prose` is a non-empty string; `texture_delta` and `proposal` are
    optional but, when present, pass their own deep shape gates HERE
    (`ledger._delta_shape` / `validator.proposal_from_mapping`) so a
    malformed document never reaches the gateway — the caller catches the
    (NarratorError | DeltaError | ProposalError) family and degrades.
    """
    if not isinstance(doc, Mapping):
        raise NarratorError(
            f"response must be an object, got {type(doc).__name__}"
        )
    unknown = [key for key in doc if key not in ("prose", "texture_delta", "proposal")]
    if unknown:
        raise NarratorError(
            f"response: unknown keys {sorted(unknown)} — the document is closed"
        )
    if "prose" not in doc:
        raise NarratorError("response: missing required key 'prose'")
    prose = doc["prose"]
    if not isinstance(prose, str) or not prose.strip():
        raise NarratorError(f"response prose must be a non-empty string, got {prose!r}")
    delta = doc.get("texture_delta")
    if delta is not None:
        if not isinstance(delta, Mapping):
            raise NarratorError(
                f"response texture_delta must be an object, got {type(delta).__name__}"
            )
        check_delta_shape(delta)  # the deep gate, loud DeltaError at the boundary
    proposal = doc.get("proposal")
    if proposal is not None:
        proposal = proposal_from_mapping(proposal)  # loud ProposalError
    return NarratorResponse(prose=prose, texture_delta=delta, proposal=proposal)


def narrator_call(
    events: Sequence[EventRecord],
    pack: Pack,
    ledger: SceneLedger,
    *,
    knower: str | None = None,
    notes: Sequence[str] = (),
    regens_used: int = 0,
    max_regens: int = MAX_REGENS,
    query: str | None = None,
    retrieval: Sequence[Retrieved] = (),
) -> str:
    """Assemble the narrator call document (pure): the brief bytes
    (BRIEF_SPEC §7, unchanged) + the `narrator_protocol` section —
    `actor` (mode B only: the knower whose beat-projection the call
    carries — mode A omits the line, the player is the narrator's own
    subject by construction, the committed corpus bytes), `anchor` (the
    log's event count: the OCC anchor a proposal must carry), `regen`
    (the per-beat counter, VALIDATION_SPEC §7), `query` (mode B, scene-2:
    the keyword query that ranked this actor's memory — §3.5's
    relevance signal made visible to the operator; mode A never carries
    it), the `retrieval` rows (the ladder's top hits for the query —
    dry demand handles, the source ids inline; the order IS the
    ladder's precedence law), and the refusal/withdrawal note lines
    verbatim. Same (log, ledger, pack, knower, query, retrieval) → same
    bytes."""
    brief = render_brief(
        assemble_brief(events, pack, ledger, knower=knower, query=query)
    )
    lines = [f"## {PROTOCOL_BLOCK}"]
    if knower is not None and knower != pack.player_id():
        lines.append(f"actor: {knower}")
    lines.extend(
        [
            f"anchor: {len(events)}",
            f"regen: {regens_used}/{max_regens}",
        ]
    )
    if query:
        lines.append(f"query: {query}")
    lines.extend(_retrieval_lines(retrieval))
    lines.extend(notes)
    return f"{brief}\n" + "\n".join(lines) + "\n"


def _retrieval_lines(rows: Sequence[Retrieved]) -> list[str]:
    """The ladder's top rows as the actor call's dry demand handles
    (BRIEF_SPEC §7.1): `retrieval: fact <ref> (<channel>/<fidelity>,
    <source>)` — the record's address and the minting event id, the
    expansion law's handle; `retrieval: lore <ref>` — the static
    background the query surfaced. No scores, no prose (L2): the ORDER
    carries the ranking (the source-outranks law visible — the derived
    view never shadows its own evidence); capped by RETRIEVAL_LINES."""
    out: list[str] = []
    for row in rows[:RETRIEVAL_LINES]:
        if row.kind == "lore":
            out.append(f"retrieval: lore {row.ref}")
        else:
            out.append(
                f"retrieval: fact {row.ref} "
                f"({row.channel}/{row.fidelity}, {row.source})"
            )
    return out


def feedable_intents(
    intents: Sequence[IntentProposal],
    ledger: SceneLedger,
    caller: str,
) -> tuple[tuple[IntentProposal, ...], tuple[str, ...]]:
    """The mediator's noun resolution, pre-door (blueprint §1): keep the
    intents that may legally reach the door; return dry WITHDRAWN notes
    for the rest (withdrawal is not an event — the attempt never reached
    the world, VALIDATION_SPEC §8).

    Dropped kinds: an actor that is not the call's own caller (scene-2's
    mode-B half of the mode-A law: a reply proposes its own caller's
    actions — mode A's caller is the player, mode B's the actor whose
    call the reply answers; another NPC's or the player's proposals ride
    a mode-B reply only as withdrawals), a texture reference whose entry
    is not live (retired / contradicted / promoted / unknown — the
    unresolvable-noun law), and a second intent on a texture entry
    already claimed within the same document (one promotion per entry
    per beat: the live-only `mark_promoted` would crash on the
    duplicate).
    """
    live_ids = {entry.id for entry in ledger.live()}
    claimed: set[str] = set()
    feedable: list[IntentProposal] = []
    withdrawn: list[str] = []
    for intent in intents:
        if intent.actor != caller:
            withdrawn.append(
                f"WITHDRAWN intent {intent.kind} (actor {intent.actor!r} is not "
                f"the caller {caller!r} — a reply proposes its own caller's "
                f"actions only)"
            )
            continue
        reference = intent.fields.get("texture")
        entry_id = (
            reference.get("entry")
            if isinstance(reference, Mapping) and "entry" in reference
            else None
        )
        if entry_id is not None:
            if entry_id not in live_ids:
                withdrawn.append(
                    f"WITHDRAWN intent {intent.kind} (texture entry not live: "
                    f"{entry_id})"
                )
                continue
            if entry_id in claimed:
                withdrawn.append(
                    f"WITHDRAWN intent {intent.kind} (duplicate texture entry "
                    f"in one document: {entry_id})"
                )
                continue
            claimed.add(entry_id)
        feedable.append(intent)
    return tuple(feedable), tuple(withdrawn)


def promotions_in(events: Sequence[EventRecord]) -> tuple[tuple[str, str], ...]:
    """The committed promotions among `events`, in log order:
    `(entry_id, event_id)` pairs — an event carrying a texture reference
    in its outcome WHOSE state_changes touch the scope target's slot (the
    canon-birth shape, D-054; a failed attempt has no matching change and
    promotes nothing). The mediator wires these to `mark_promoted`."""
    out: list[tuple[str, str]] = []
    for event in events:
        reference = event.outcome.get("texture")
        if not isinstance(reference, Mapping) or "entry" not in reference:
            continue
        split = split_scope(str(reference.get("scope", "")))
        target = split[1] if split is not None else None
        promoted = any(
            change.entity == target and change.prop == reference.get("slot")
            for change in event.state_changes
        )
        if promoted:
            out.append((str(reference["entry"]), event.id))
    return tuple(out)
