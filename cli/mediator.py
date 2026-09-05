"""The mediator session loop (iter-12, D-055 — the agent-in-the-loop
narrator door; protocol owner `docs/VALIDATION_SPEC.md` §7.1, call format
`docs/BRIEF_SPEC.md` §7.1; scene-2 — the mode-B session wiring, the
chorus drain inside the beat cycle).

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
(delta refusals or contradicted claims) regens the WHOLE exchange — the
regen re-delivers prose, delta and proposal; intents feed the door only
on an accepted document (VALIDATION_SPEC §7.1); accepted delta items
stay applied across regens (the gateway's idempotent duplicate rule).

Scene-2's drain (mode B, BRIEF_SPEC §3.9): a beat = the player's
exchange, then the chorus. On the player's ACCEPT the mediator
snapshots the chorus queue (`brief/scene.py::speaking_queue` over the
post-action log — the beat's own cast, fixed at curtain: mid-beat
arrivals join the NEXT beat's chorus) and drains it head-first, ONE
actor call per queued NPC (`narrator_call(knower=<npc>, query=...)` —
the keyword query that ranked the actor's memory, plus the retrieval
ladder's top rows as demand handles; the ladder's first runtime QUERY
consumer, retr-1's DORMANT gate opened here — one index build per actor
call, mode A never pays it). Each actor exchange is the SAME cycle with
its own regen budget and its own caller gate (`feedable_intents`':
a reply proposes its own caller's actions). The drain ends when the
queue empties; an actor no longer present at the current scene is
skipped (the live presence re-verification — the template rung, the
chronicle already renders its beats); `narrate dry` on an actor call
skips that actor, on the player's call closes the beat (the chorus
never starts — declining the head declines the beat); a bare `narrate`
(emit_call) DROPS a pending drain — the operator moved on, the actors
fall to the template rung: never a blocked beat, never a silent drop.

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
from brief.scene import present_at_scene, recall_query, speaking_queue
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
from core.retrieval import RetrievalIndex, Retrieved
from render.chronicle import RenderError, chronicle_from_log
from render.tracery import GrammarError

__all__ = ["BeatResult", "Mediator", "MediatorError"]


class MediatorError(RuntimeError):
    """Session-loop misuse (no open beat, unreadable reply): an operator
    error — the session prints it and lives on, never a crash."""


@dataclass(slots=True)
class BeatResult:
    """One completed exchange step (the player's or an actor's). `status`:

    - `accepted` — the narrator reply passed both gates; `prose` is the
      narrator's text, shown to the player; `notes` carries the
      exchange's dry `BEAT` summary lines (KI#44 — claims/texture/
      intents/rebased counts; operator output only, never riding the
      next call); `call_path` carries the NEXT call awaiting a reply
      (the chorus's actor call) or None (the exchange was the beat's
      last);
    - `regen` — the document was refused or malformed; `notes` carries
      the dry refusal lines, `call_path` the auto-emitted re-invocation;
    - `dry` — the L12 floor: the exchange closed without a narrator
      (the player's: the beat itself; an actor's: that actor falls to
      the template rung, `call_path` the next chorus call if any).
    """

    status: str
    prose: str
    notes: tuple[str, ...]
    call_path: Path | None
    regens_used: int
    max_regens: int
    actor: str | None = None


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
        # scene-2: the chorus drain's state
        self._chorus: tuple[str, ...] = ()  # the beat's remaining drain (the accept's snapshot)
        self._knower: str | None = None  # the open call's subject (None = the player's)
        self._actor_notes: list[str] = []  # the actor exchange's refusal notes

    @property
    def beat_open(self) -> bool:
        return self._beat_open

    @property
    def knower(self) -> str | None:
        """The open call's subject (mode B session state): None = the
        player's exchange, an npc id = the actor call awaiting its reply."""
        return self._knower

    @property
    def shown_lines(self) -> int:
        """The chronicle-line watermark the session adopts after every
        mediator command (one shared delta-print counter over one log)."""
        return self._shown_lines

    # -- the beat cycle --------------------------------------------------------

    def emit_call(self) -> Path:
        """Open (or re-open) the PLAYER's beat: retire texture contradicted
        by the window's new canon, sync the scene, assemble the call
        document (mode A bytes — the committed corpus shape). Consumes
        any pending refusal/withdrawal notes (they ride this call's
        protocol section). A PENDING chorus drain is dropped — the
        unanswered actor calls fall to the template rung (the operator
        moved on; the chronicle already renders their beats; never a
        blocked beat)."""
        if self._beat_open and self._knower is not None:
            self._close_beat()
        events = self._events()
        self.ledger.retire_contradicted(events[self._call_events :])
        self.ledger.sync_scene(events, self._pack)
        notes = tuple(self._pending_notes)
        self._pending_notes.clear()
        document = narrator_call(
            events, self._pack, self.ledger,
            notes=notes, regens_used=self._regens.used,
        )
        self._knower = None
        return self._write_call(document, len(events))

    def apply_reply(self, reply_path: Path) -> BeatResult:
        """Ingest one narrator reply (the open call's — the player's or an
        actor's) and run it through the whole cycle: shape gate →
        proposal verdicts → texture gateway → (on accept) the caller's
        intents through the door + promotion wiring → advance (the
        player's accept starts the chorus drain; an actor's accept pops
        the next queued NPC; the last accept closes the beat).
        Malformed output and refusals never crash — they spend the
        exchange's regen budget; exhaustion falls to the ladder's floor
        (the player's exchange dies with the beat; an actor falls to the
        template rung and the drain advances)."""
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
                report.intent_proposals, self.ledger, self._caller()
            )
            self._pending_notes.extend(withdrawn_notes)
            fed, withdrawn = len(feedable), len(withdrawn_notes)
            if feedable:
                before = len(events)
                self._sim.run_steps(
                    [self._step(intent) for intent in feedable]
                )
                fresh = self._events()
                for entry_id, event_id in promotions_in(fresh[before:]):
                    self.ledger.mark_promoted(entry_id, event_id)
        summary = self._beat_summary(
            response, report, delta_report, fed=fed, withdrawn=withdrawn
        )
        used, ceiling = self._regens.used, self._regens.max_regens
        actor = self._knower
        next_call = self._advance()
        return BeatResult(
            status="accepted", prose=response.prose, notes=summary,
            call_path=next_call, regens_used=used, max_regens=ceiling,
            actor=actor,
        )

    def dry_close(self) -> BeatResult:
        """Close the open call without a narrator reply — the operator
        declines to narrate (`narrate dry`). On the PLAYER's call the
        beat itself closes: the chorus never starts (declining the head
        declines the beat; the template rung renders the whole beat).
        On an ACTOR's call the actor falls to the template rung and the
        drain advances — the next queued NPC's call awaits (the beat
        lives on; never a blocked beat, never a silent drop)."""
        if not self._beat_open:
            raise MediatorError("no open narrator beat — emit a call first")
        if self._knower is not None:
            return self._skip_actor()
        used, ceiling = self._regens.used, self._regens.max_regens
        prose = self._template_prose()
        self._close_beat()
        return BeatResult(
            status="dry", prose=prose, notes=(),
            call_path=None, regens_used=used, max_regens=ceiling,
        )

    # -- the chorus drain (scene-2, mode B) ------------------------------------

    def _advance(self) -> Path | None:
        """The beat's advance after an accepted exchange: the player's
        accept snapshots the chorus queue over the post-action log (the
        beat's own cast, BRIEF_SPEC §3.9 — fixed at curtain: mid-beat
        arrivals join the NEXT beat's chorus); an actor's accept pops
        the next head. Emits the next actor call (a fresh exchange: its
        own regen budget); None when the drain empties (the beat
        closes)."""
        if self._knower is None:
            self._chorus = speaking_queue(self._events(), self._pack)
        return self._drain_next()

    def _drain_next(self) -> Path | None:
        """Pop the drain's head and emit its call — the LIVE presence
        re-verification (`brief/scene.py::present_at_scene`): an actor
        who left the scene mid-drain is skipped (the template rung, its
        beats already render through the chronicle — a call never goes
        to an NPC standing elsewhere). None when the drain empties (the
        beat closes)."""
        events = self._events()
        while self._chorus:
            head, self._chorus = self._chorus[0], self._chorus[1:]
            if not present_at_scene(events, self._pack, head):
                continue
            self._knower = head
            self._regens = RegenBudget()  # one budget per narrator exchange
            self._actor_notes = []
            return self._emit_actor()
        self._close_beat()
        return None

    def _emit_actor(self) -> Path:
        """Emit (or re-emit) the current actor's call — mode B: the
        knower's own brief, the keyword query that ranked its memory
        (`query:` — BRIEF_SPEC §3.5's relevance signal), the retrieval
        ladder's top rows for that query (`retrieval:` — the ladder's
        first runtime QUERY consumer, one index build per actor call;
        mode A never pays it), and the actor's own exchange notes (its
        regen refusals — the player's pending notes wait for the
        player's next call, BRIEF_SPEC §7.1's subject-scoped note law)."""
        events = self._events()
        self.ledger.retire_contradicted(events[self._call_events :])
        self.ledger.sync_scene(events, self._pack)
        query = recall_query(events, self._pack, self._knower) or None
        retrieval: tuple[Retrieved, ...] = ()
        index = RetrievalIndex.build(self._pack, events)
        if index is not None:
            try:
                if query is not None:
                    retrieval = index.query(query, knower=self._knower)
            finally:
                index.close()
        notes = tuple(self._actor_notes)
        self._actor_notes.clear()
        document = narrator_call(
            events, self._pack, self.ledger,
            knower=self._knower, notes=notes,
            regens_used=self._regens.used,
            query=query, retrieval=retrieval,
        )
        return self._write_call(document, len(events))

    def _skip_actor(self, notes: tuple[str, ...] = ()) -> BeatResult:
        """The actor's L12 floor (a dry or an exhausted regen budget):
        the actor's exchange ends on the template rung — its beats
        already render through the chronicle — and the drain advances.
        The exhaustion's refusal notes ride the result (the operator
        sees why the actor fell)."""
        actor = self._knower
        used, ceiling = self._regens.used, self._regens.max_regens
        prose = self._template_prose()
        next_call = self._drain_next()
        return BeatResult(
            status="dry", prose=prose, notes=notes,
            call_path=next_call, regens_used=used, max_regens=ceiling,
            actor=actor,
        )

    def _caller(self) -> str:
        """The open call's caller — whose actions a reply may propose
        (mode A: the player; mode B: the actor whose call is open)."""
        if self._knower is None:
            return self._pack.player_id()
        return self._knower

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
        if self._knower is None:
            self._pending_notes.extend(notes)
        else:
            self._actor_notes.extend(notes)
        if self._regens.spend():
            path = (
                self._emit_actor() if self._knower is not None
                else self.emit_call()
            )  # the notes ride the re-invocation (the subject's own buffer)
            return BeatResult(
                status="regen", prose="", notes=tuple(notes),
                call_path=path, regens_used=self._regens.used,
                max_regens=self._regens.max_regens, actor=self._knower,
            )
        if self._knower is None:
            return self.dry_close()
        # an actor's exhausted budget: the template rung, the drain lives on
        return self._skip_actor(tuple(notes))

    def _close_beat(self) -> None:
        self._beat_open = False
        self._regens = RegenBudget()
        self._knower = None
        self._chorus = ()
        self._actor_notes = []

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
            # The beat may hold canon events that sit BELOW the tale gate
            # (routine drift, waits) — "no new canon events" would be a lie
            # under the tune-1 medium gate; say what actually happened.
            events = self._events()
            if len(events) > self._call_events:
                return "(dry beat — no tale-worthy lines this beat)"
            return "(dry beat — no new canon events)"
        return "\n".join(fresh_lines)

    @staticmethod
    def _step(intent: IntentProposal) -> dict[str, Any]:
        """IntentProposal → the step grammar the door already owns
        (INTENT_SCHEMA §9; scene-2: the actor key — the caller's
        proposals feed as actor steps through the same front door);
        the door re-anchors at feed time — the proposal anchor was
        validated fresh in the same cycle."""
        step: dict[str, Any] = {"intent": intent.kind, "actor": intent.actor}
        if intent.target is not None:
            step["target"] = intent.target
        step.update(intent.fields)
        return step

    def _write_call(self, document: str, event_count: int) -> Path:
        """Write one call document and stamp the emit state (the
        subject-agnostic half of both emits — the file is the contract)."""
        path = self._out_dir / f"call_{self._call_seq:04d}.md"
        path.write_text(document, encoding="utf-8")
        self._call_seq += 1
        self._call_events = event_count
        self._beat_open = True
        self._shown_lines = len(self._chronicle_lines())
        return path

    def _events(self) -> list[EventRecord]:
        _header, events = read_log(self._log_path, self._schema)
        return list(events)

    def _chronicle_lines(self) -> list[str]:
        return chronicle_from_log(
            self._log_path, self._pack, self._schema
        ).splitlines()
