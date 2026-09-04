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
  refusal notes) — everything the external narrator may draw on for one
  beat; mode B (scene-1) passes `knower=<npc>` — the actor call, one NPC
  per call, the chorus queue's own document (the actor line names whose
  beat-projection it carries);
- the **response document** — one CLOSED document `{prose, texture_delta?,
  proposal?}`: prose for the player, the structural texture delta, and
  the fact proposal, all in the same call (one call, two jobs, D-049).
  The deep shape gates run HERE, at the boundary: a malformed document
  raises the DeltaError/ProposalError family loudly, and the mediator's
  ladder (cli/) catches it BEFORE the gateway is invoked — the gates
  never guess, never repair (VALIDATION_SPEC §2);
- **feedable intents** — the mediator's noun resolution: proposal intents
  survive to the door only when their texture entry is live (an
  unresolvable noun never becomes an Intent — blueprint §1), the actor is
  the player (mode A), and no two intents ride the same texture entry (a
  duplicate promotion would crash `mark_promoted`'s live-only law).
  Withdrawals are notes, never events (the texture-OCC mirror).

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

__all__ = [
    "PROTOCOL_BLOCK",
    "NarratorError",
    "NarratorResponse",
    "feedable_intents",
    "narrator_call",
    "narrator_response_from_mapping",
    "promotions_in",
]

#: The protocol section's block id (BRIEF_SPEC §7.1 block geometry).
PROTOCOL_BLOCK: Final = "narrator_protocol"


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
) -> str:
    """Assemble the narrator call document (pure): the brief bytes
    (BRIEF_SPEC §7, unchanged) + the `narrator_protocol` section —
    `actor` (mode B only: the knower whose beat-projection the call
    carries — mode A omits the line, the player is the narrator's own
    subject by construction, the committed corpus bytes), `anchor` (the
    log's event count: the OCC anchor a proposal must carry), `regen`
    (the per-beat counter, VALIDATION_SPEC §7), and the
    refusal/withdrawal note lines verbatim (they ride the call's top,
    where directives live). Same (log, ledger, pack, knower) → same
    bytes."""
    brief = render_brief(assemble_brief(events, pack, ledger, knower=knower))
    lines = [f"## {PROTOCOL_BLOCK}"]
    if knower is not None and knower != pack.player_id():
        lines.append(f"actor: {knower}")
    lines.extend(
        [
            f"anchor: {len(events)}",
            f"regen: {regens_used}/{max_regens}",
            *notes,
        ]
    )
    return f"{brief}\n" + "\n".join(lines) + "\n"


def feedable_intents(
    intents: Sequence[IntentProposal],
    ledger: SceneLedger,
    player_id: str,
) -> tuple[tuple[IntentProposal, ...], tuple[str, ...]]:
    """The mediator's noun resolution, pre-door (blueprint §1): keep the
    intents that may legally reach the door; return dry WITHDRAWN notes
    for the rest (withdrawal is not an event — the attempt never reached
    the world, VALIDATION_SPEC §8).

    Dropped kinds: a non-player actor (mode A — the narrator proposes the
    player's actions only), a texture reference whose entry is not live
    (retired / contradicted / promoted / unknown — the unresolvable-noun
    law), and a second intent on a texture entry already claimed within
    the same document (one promotion per entry per beat: the live-only
    `mark_promoted` would crash on the duplicate).
    """
    live_ids = {entry.id for entry in ledger.live()}
    claimed: set[str] = set()
    feedable: list[IntentProposal] = []
    withdrawn: list[str] = []
    for intent in intents:
        if intent.actor != player_id:
            withdrawn.append(
                f"WITHDRAWN intent {intent.kind} (actor {intent.actor!r} is not "
                f"the player — mode A proposes player actions only)"
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
