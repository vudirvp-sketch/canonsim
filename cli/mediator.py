"""The mediator session loop (iter-12, D-055 — the agent-in-the-loop
narrator door; protocol owner `docs/VALIDATION_SPEC.md` §7.1, call format
`docs/BRIEF_SPEC.md` §7.1).

The narrator is EXTERNAL: the owner's assistant (or any operator obeying
the response document contract) reads a call file and writes a reply
file — the repo itself stays LLM-free and network-free (INV-4, exactly
as written; the boundary landed WITHOUT opening the runtime-inference
gate). Files are the contract, both gitignored runtime artifacts under
`output/mediator/`:

    call_<NNNN>.md   the narrator's input: the brief + narrator_protocol
    reply_<NNNN>.json  the narrator's output: {prose, texture_delta?, proposal?}

One beat follows the D-049 order: commit → `retire_contradicted(window)`
→ `sync_scene` → assemble/emit → narrator reply → `apply_delta` →
intents through the door → `mark_promoted`. The L12 degradation ladder
from day one: narrator → template (the beat's own chronicle lines — the
deterministic prose of phase 0) → dry log line. A refused document
(delta refusals or contradicted claims) regens the WHOLE beat — the
regen re-delivers prose, delta and proposal; intents feed the door only
on an accepted document (VALIDATION_SPEC §7.1); accepted delta items
stay applied across regens (the gateway's idempotent duplicate rule).

This module is periphery (D-046): it owns files, the Simulator handle
and session state — never engine mechanics. All engine-side work is
`brief/` pure functions.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from brief.ledger import DeltaError, DeltaReport, SceneLedger, refusal_lines
from brief.mediator import (
    NarratorError,
    NarratorResponse,
    feedable_intents,
    narrator_call,
    narrator_response_from_mapping,
    promotions_in,
)
from brief.validator import (
    IntentProposal,
    ProposalError,
    RegenBudget,
    ValidationReport,
    refusal_note,
    validate_proposal,
)
from core.log import EventRecord, read_log
from core.loop import Simulator
from core.pack import Pack
from render.chronicle import RenderError, chronicle_from_log
from render.tracery import GrammarError

__all__ = ["BeatResult", "Mediator", "MediatorError"]


class MediatorError(RuntimeError):
    """Session-loop misuse (no open beat, unreadable reply): an operator
    error — the session prints it and lives on, never a crash."""


@dataclass(slots=True)
class BeatResult:
    """One completed beat-cycle step. `status`:

    - `accepted` — the narrator reply passed both gates; `prose` is the
      narrator's text, shown to the player; `notes` carries the beat's
      dry `BEAT` summary lines (KI#44 — claims/texture/intents/rebased
      counts; operator output only, never riding the next call);
    - `regen` — the document was refused or malformed; `notes` carries
      the dry refusal lines, `call_path` the auto-emitted re-invocation;
    - `dry` — the L12 floor: the beat closed without a narrator, `prose`
      is the template (or the dry log line).
    """

    status: str
    prose: str
    notes: tuple[str, ...]
    call_path: Path | None
    regens_used: int
    max_regens: int


class Mediator:
    """One session's mediator: the live beat loop over an opened
    Simulator plus the session scene ledger. The ledger dies with the
    session (the D-049 death law: texture is never summarized, never
    persisted); a seed restart constructs a fresh Mediator."""

    def __init__(
        self,
        sim: Simulator,
        pack: Pack,
        schema: Mapping[str, Any],
        log_path: Path,
        out_dir: Path,
    ) -> None:
        self._sim = sim
        self._pack = pack
        self._schema = schema
        self._log_path = log_path
        self._out_dir = Path(out_dir)
        self._out_dir.mkdir(parents=True, exist_ok=True)
        self.ledger = SceneLedger()
        self._call_seq = 0
        self._call_events = 0  # the log length at the last emit (retire window edge)
        self._pending_notes: list[str] = []
        self._regens = RegenBudget()
        self._beat_open = False
        self._shown_lines = 0  # chronicle lines already emitted as template prose

    @property
    def beat_open(self) -> bool:
        return self._beat_open

    @property
    def shown_lines(self) -> int:
        """The chronicle-line watermark the session adopts after every
        mediator command (one shared delta-print counter over one log)."""
        return self._shown_lines

    # -- the beat cycle --------------------------------------------------------

    def emit_call(self) -> Path:
        """Open (or re-open) a beat: retire texture contradicted by the
        window's new canon, sync the scene, assemble the call document.
        Consumes any pending refusal/withdrawal notes (they ride this
        call's protocol section)."""
        events = self._events()
        self.ledger.retire_contradicted(events[self._call_events :])
        self.ledger.sync_scene(events, self._pack)
        notes = tuple(self._pending_notes)
        self._pending_notes.clear()
        document = narrator_call(
            events, self._pack, self.ledger,
            notes=notes, regens_used=self._regens.used,
        )
        path = self._out_dir / f"call_{self._call_seq:04d}.md"
        path.write_text(document, encoding="utf-8")
        self._call_seq += 1
        self._call_events = len(events)
        self._beat_open = True
        self._shown_lines = len(self._chronicle_lines())
        return path

    def apply_reply(self, reply_path: Path) -> BeatResult:
        """Ingest one narrator reply and run it through the whole cycle:
        shape gate → proposal verdicts → texture gateway → (on accept)
        intents through the door + promotion wiring. Malformed output and
        refusals never crash — they spend the regen budget; exhaustion
        falls to dry mode (L12)."""
        if not self._beat_open:
            raise MediatorError("no open narrator beat — emit a call first")
        try:
            doc = json.loads(reply_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MediatorError(f"cannot read reply {reply_path}: {exc}") from exc
        try:
            response = narrator_response_from_mapping(doc)
        except (NarratorError, DeltaError, ProposalError) as exc:
            return self._regen_or_dry((f"MALFORMED {exc}",))

        events = self._events()
        report = None
        if response.proposal is not None:
            try:
                report = validate_proposal(response.proposal, events, self._pack)
            except ProposalError as exc:
                return self._regen_or_dry((f"MALFORMED {exc}",))
        delta_report = None
        if response.texture_delta is not None:
            delta_report = self.ledger.apply_delta(
                response.texture_delta, events, self._pack
            )

        notes: list[str] = []
        if delta_report is not None and delta_report.refused:
            notes.extend(refusal_lines(delta_report))
        if report is not None and report.refused:
            notes.extend(refusal_note(report))
        if notes:
            return self._regen_or_dry(notes)

        # Accepted: the fact transaction completes. Withdrawals resolve
        # nouns against the post-delta ledger; only feedable intents
        # reach the door; committed promotions flip their entries.
        fed = withdrawn = 0
        if report is not None and report.intent_proposals:
            feedable, withdrawn_notes = feedable_intents(
                report.intent_proposals, self.ledger, self._pack.player_id()
            )
            self._pending_notes.extend(withdrawn_notes)
            fed, withdrawn = len(feedable), len(withdrawn_notes)
            if feedable:
                before = len(events)
                self._sim.run_steps([self._step(intent) for intent in feedable])
                fresh = self._events()
                for entry_id, event_id in promotions_in(fresh[before:]):
                    self.ledger.mark_promoted(entry_id, event_id)
        summary = self._beat_summary(
            response, report, delta_report, fed=fed, withdrawn=withdrawn
        )
        used, ceiling = self._regens.used, self._regens.max_regens
        self._close_beat()
        return BeatResult(
            status="accepted", prose=response.prose, notes=summary,
            call_path=None, regens_used=used, max_regens=ceiling,
        )

    def dry_close(self) -> BeatResult:
        """Close the beat without a narrator reply — the operator declines
        to narrate (`narrate dry`) or the ladder has fallen here. The
        template rung renders the beat's own chronicle lines; the dry log
        line is the floor when even rendering fails (L12: never a blocked
        beat, never a silent drop)."""
        if not self._beat_open:
            raise MediatorError("no open narrator beat — emit a call first")
        used, ceiling = self._regens.used, self._regens.max_regens
        prose = self._template_prose()
        self._close_beat()
        return BeatResult(
            status="dry", prose=prose, notes=(),
            call_path=None, regens_used=used, max_regens=ceiling,
        )

    # -- internals --------------------------------------------------------------

    @staticmethod
    def _beat_summary(
        response: NarratorResponse,
        report: ValidationReport | None,
        delta_report: DeltaReport | None,
        *,
        fed: int,
        withdrawn: int,
    ) -> tuple[str, ...]:
        """The accepted beat's dry verdict summary (KI#44): the honest-
        verdict law made observable at the session level, so a live
        session can tally the phase-1 exit numbers (invented/unverifiable/
        rebased/regens per beats — ROADMAP §2; the refusal side is already
        visible via the regen notes). Operator output only: these lines
        never enter `_pending_notes`, never ride the next call (only
        refusals and withdrawals do — BRIEF_SPEC §7.1)."""
        lines: list[str] = []
        if report is not None and report.claim_verdicts:
            supported = (
                len(report.claim_verdicts) - report.invented - report.unverifiable
            )
            parts = [f"{supported} supported"] if supported else []
            if report.unverifiable:
                parts.append(f"{report.unverifiable} unverifiable")
            if parts:
                lines.append(f"BEAT claims: {', '.join(parts)}")
            if report.rebased_to is not None:
                lines.append(
                    f"BEAT rebased: {response.proposal.expected_event_seq} "
                    f"-> {report.rebased_to}"
                )
        if delta_report is not None:
            parts = []
            if delta_report.established:
                parts.append(f"{len(delta_report.established)} established")
            if delta_report.pinned:
                parts.append(f"{len(delta_report.pinned)} pinned")
            if delta_report.retired:
                parts.append(f"{len(delta_report.retired)} retired")
            if delta_report.no_ops:
                parts.append(f"{len(delta_report.no_ops)} no-op")
            if parts:
                lines.append(f"BEAT texture: {', '.join(parts)}")
        if report is not None and report.intent_proposals:
            lines.append(f"BEAT intents: {fed} fed, {withdrawn} withdrawn")
        return tuple(lines)

    def _regen_or_dry(self, notes: Sequence[str]) -> BeatResult:
        self._pending_notes.extend(notes)
        if self._regens.spend():
            path = self.emit_call()  # notes ride the re-invocation
            return BeatResult(
                status="regen", prose="", notes=tuple(notes),
                call_path=path, regens_used=self._regens.used,
                max_regens=self._regens.max_regens,
            )
        return self.dry_close()

    def _close_beat(self) -> None:
        self._beat_open = False
        self._regens = RegenBudget()

    def _template_prose(self) -> str:
        try:
            lines = self._chronicle_lines()
        except (RenderError, GrammarError):
            events = self._events()
            fresh = events[self._call_events :]
            types = ", ".join(sorted({event.type for event in fresh})) or "none"
            tick = events[-1].t if events else 0
            return f"[t {tick}] (dry beat) events: {types}"
        fresh_lines = lines[self._shown_lines :]
        self._shown_lines = len(lines)
        if not fresh_lines:
            return "(dry beat — no new canon events)"
        return "\n".join(fresh_lines)

    @staticmethod
    def _step(intent: IntentProposal) -> dict[str, Any]:
        """IntentProposal → the step grammar the door already owns
        (INTENT_SCHEMA §9); the door re-anchors at feed time — the
        proposal anchor was validated fresh in the same cycle."""
        step: dict[str, Any] = {"intent": intent.kind}
        if intent.target is not None:
            step["target"] = intent.target
        step.update(intent.fields)
        return step

    def _events(self) -> list[EventRecord]:
        _header, events = read_log(self._log_path, self._schema)
        return list(events)

    def _chronicle_lines(self) -> list[str]:
        return chronicle_from_log(
            self._log_path, self._pack, self._schema
        ).splitlines()
