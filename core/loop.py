"""Tick driver + playscript runner (KeeperRL `Model::update` shape,
`docs/blueprint/phase0.md` §1-§2): pop the next queue entry in
`(tick, sub_order, actor_id, seq)` order, advance the clock, execute.

The intent front door (INTENT_SCHEMA.md is the contract owner): shape
errors are loud (`RunnerError` — author bugs); a well-formed but
world-impossible intent is REJECTED with an `intent_rejected` no-op event
(cause-chained, never silently dropped). Accepted intents draw their
duration at accept time and enqueue a SCHEDULED completion carrying
`based_on_event_seq` — intent OCC. At completion the OCC re-check runs
first (the projection moved *and* the precondition broke → reject with the
cause chain to the breaking event), then the opposed check, then the
resolver; ignitions hand control to the transition engine, whose spread
pass runs as a self-rescheduling SYSTEM_PASS entry and whose smoke /
burnout follow-ups run as SEEDED SCHEDULED entries (TIME-1).

The whole run executes under `assure('substantive')` — a cosmetic draw on
this path is an INV-2 violation made loud (RNG-1). Resolver dispatch is a
name→callable registry keyed by the pack's `resolver` field (INV-3).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from core.clock import Clock
from core.fold import Projection, apply_event, initial_projection
from core.ids import sequence_id
from core.intent import (
    REJECTION_EVENT,
    IntentData,
    RunnerError,
    action_duration,
    first_failing,
    occ_breaking_cause,
    pack_importance,
    run_check,
    validate_shape,
)
from core.log import EventDraft, EventLogWriter, EventRecord
from core.pack import Pack
from core.queue import PLAYER_INTENT, SCHEDULED, SYSTEM_PASS, EventQueue
from core.resolvers import REGISTRY
from core.rng import SUBSTANTIVE, RngBank
from core.scheduler import build, decls_from_rules
from core.transitions import Ignition, follow_up_draft, ignite, spread_tick

__all__ = [
    "CompletionPayload",
    "FollowUpPayload",
    "IntentData",
    "PassPayload",
    "REJECTION_EVENT",
    "RunResult",
    "RunnerError",
    "Simulator",
    "load_playscript",
]


@dataclass(frozen=True, slots=True)
class CompletionPayload:
    """An accepted intent pending its SCHEDULED completion (the
    ACCEPTED state of the intent lifecycle)."""

    intent: IntentData
    duration: int
    based_on_event_seq: int


@dataclass(frozen=True, slots=True)
class PassPayload:
    """A transition layer's spread pass; `causes` maps location → the
    location's last transition event id (the cause chain within a fire)."""

    system: str
    layer: str
    causes: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class FollowUpPayload:
    """A SEEDED follow-up (smoke / burnout) at its trigger tick."""

    layer: str
    location: str
    kind: str
    cause_id: str


@dataclass(frozen=True, slots=True)
class RunResult:
    """What a finished run produced."""

    log_path: Path
    event_count: int
    last_tick: int
    fingerprint: int


def load_playscript(path: Path) -> dict[str, Any]:
    """Load a playscript fixture (seed + ordered intents, MVP_SCOPE §13)."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class Simulator:
    """One deterministic run: bank + clock + queue + writer + projection."""

    def __init__(
        self,
        pack: Pack,
        seed: int,
        log_path: Path,
        event_schema: Mapping[str, Any],
        commit: str = "unknown",
    ) -> None:
        self._pack = pack
        self._seed = int(seed)
        self._bank = RngBank(self._seed)
        self._clock = Clock.from_rules(dict(pack.rules["time"]))
        self._queue = EventQueue()
        self._writer = EventLogWriter(log_path, event_schema)
        self._commit = commit
        self._projection = initial_projection(pack.entities)
        self._initial = initial_projection(pack.entities)
        self._events: list[EventRecord] = []
        self._intent_seq = 0
        self._schedule = build(decls_from_rules(pack.rules))
        self._system_order = {
            decl.name: index for index, decl in enumerate(self._schedule)
        }

    @property
    def projection(self) -> Projection:
        """The runtime incremental projection (STATE-1)."""
        return self._projection

    def run_playscript(self, script: Mapping[str, Any]) -> RunResult:
        """Play seed + ordered intents end-to-end; returns the run summary."""
        for key in ("name", "seed", "pack", "steps"):
            if key not in script:
                raise RunnerError(f"playscript missing key {key!r}")
        if script["seed"] != self._seed:
            raise RunnerError(
                f"playscript seed {script['seed']} != simulator seed {self._seed}"
            )
        if script["pack"] != self._pack.name_version:
            raise RunnerError(
                f"playscript pack {script['pack']!r} != loaded pack "
                f"{self._pack.name_version!r}"
            )
        steps = list(script["steps"])
        self._writer.write_header(
            seed=self._seed, commit=self._commit, pack=self._pack.name_version
        )
        try:
            if steps:
                with self._bank.assure(SUBSTANTIVE):
                    remaining = steps[1:]
                    self._queue.push(
                        tick=self._clock.tick, sub_order=PLAYER_INTENT,
                        actor_id=self._pack.player_id(), kind="intent",
                        payload=self._intent_from_step(steps[0]),
                    )
                    while len(self._queue):
                        entry = self._queue.pop()
                        self._clock.advance_to(entry.tick)
                        if entry.kind == "intent":
                            accepted = self._execute_intent(entry)
                            if not accepted and remaining:
                                self._feed_next(entry.tick, remaining)
                        elif entry.kind == "completion":
                            self._complete(entry)
                            if remaining:
                                self._feed_next(entry.tick, remaining)
                        elif entry.kind == "pass":
                            self._run_pass(entry)
                        else:
                            self._run_follow_up(entry)
            return RunResult(
                log_path=self._writer.path,
                event_count=self._writer.event_count,
                last_tick=self._clock.tick,
                fingerprint=self._bank.fingerprint,
            )
        finally:
            self._writer.close()

    def _feed_next(self, tick: int, remaining: list[Mapping[str, Any]]) -> None:
        self._queue.push(
            tick=tick, sub_order=PLAYER_INTENT,
            actor_id=self._pack.player_id(), kind="intent",
            payload=self._intent_from_step(remaining.pop(0)),
        )

    def _intent_from_step(self, step: Mapping[str, Any]) -> IntentData:
        kind = step.get("intent")
        if not isinstance(kind, str):
            raise RunnerError(f"playscript step missing 'intent': {step!r}")
        intent_id = sequence_id("intent", self._intent_seq)
        self._intent_seq += 1
        fields = {
            key: value
            for key, value in step.items()
            if key not in ("intent", "target")
        }
        return IntentData(
            id=intent_id, kind=kind, actor=self._pack.player_id(),
            target=step.get("target"), fields=fields,
            based_on_event_seq=self._writer.event_count,
        )

    # -- the intent front door -------------------------------------------------

    def _execute_intent(self, entry: Any) -> bool:
        """PROPOSED → ACCEPTED (SCHEDULED) | REJECTED (no-op event).
        Returns whether the intent was accepted."""
        intent: IntentData = entry.payload
        action = self._pack.action(intent.kind)
        if action is None:
            raise RunnerError(
                f"unknown intent {intent.kind!r} (not in the pack's actions)"
            )
        validate_shape(action, intent)
        failing = first_failing(
            self._pack, self._projection, intent, list(action.get("requires", ()))
        )
        if failing is not None:
            self._emit_rejection(
                intent, entry.tick, reason="precondition", failed_test=failing,
                cause_id=self._writer.last_id,
            )
            return False
        duration = action_duration(action, self._bank, intent)
        self._queue.push(
            tick=entry.tick + duration, sub_order=SCHEDULED,
            actor_id=intent.actor, kind="completion",
            payload=CompletionPayload(
                intent=intent, duration=duration,
                based_on_event_seq=intent.based_on_event_seq,
            ),
        )
        return True

    def _complete(self, entry: Any) -> None:
        """Completion: OCC re-check → opposed check → resolver → event →
        world reactions (ignitions, passes, follow-ups)."""
        payload: CompletionPayload = entry.payload
        intent = payload.intent
        action = self._pack.action(intent.kind)
        assert action is not None  # validated at the front door

        if self._writer.event_count > payload.based_on_event_seq:
            failing = first_failing(
                self._pack, self._projection, intent,
                list(action.get("requires", ())),
            )
            if failing is not None:
                cause = occ_breaking_cause(
                    self._pack, self._events, payload.based_on_event_seq,
                    intent, self._initial,
                )
                self._emit_rejection(
                    intent, entry.tick, reason="projection_moved",
                    failed_test=failing, cause_id=cause or self._writer.last_id,
                )
                return

        check = run_check(self._pack, self._projection, self._bank, intent, action)
        resolver = REGISTRY.get(action["resolver"])
        if resolver is None:
            raise RunnerError(f"unknown resolver key {action['resolver']!r}")
        resolution = resolver(
            self._pack, self._projection, self._bank, intent, action,
            check, entry.tick,
        )

        entities = {intent.actor}
        if intent.target is not None:
            entities.add(intent.target)
        entities.update(change.entity for change in resolution.state_changes)
        draft = EventDraft(
            t=entry.tick,
            type=resolution.event_type,
            actor=intent.actor,
            target=intent.target,
            cause=self._writer.last_id,  # None only for the run-start event
            outcome={"duration": payload.duration, **resolution.outcome},
            knowledge=resolution.knowledge,
            state_changes=resolution.state_changes,
            hooks=resolution.hooks,
            importance=pack_importance(
                self._pack.rules, entities,
                irreversible=sum(
                    1 for change in resolution.state_changes if change.irreversible
                ),
                hooks=len(resolution.hooks),
            ),
            provenance={"seed": self._seed, "cause_intent": intent.id},
        )
        record = self._writer.append(draft)
        self._apply(record)

        for ignition in resolution.ignitions:
            self._execute_ignition(ignition, entry.tick, intent.actor)

    def _execute_ignition(self, ignition: Ignition, tick: int, actor: str) -> None:
        """Run a transition ignition: emit the layer's events (cause
        chained), seed the smoke/burnout follow-ups, start the spread pass."""
        layer_cfg = self._pack.rules["transitions"][ignition.layer]
        plan = ignite(self._pack, self._projection, tick, ignition, actor)
        last_id = self._writer.last_id
        started_id: str | None = None
        for draft in plan.drafts:
            record = self._writer.append(
                replace(draft, cause=last_id, provenance={"seed": self._seed})
            )
            self._apply(record)
            last_id = record.id
            if started_id is None:
                started_id = record.id
        if started_id is None:
            return
        for spec in plan.follow_ups:
            self._queue.push(
                tick=spec.at_tick, sub_order=SCHEDULED,
                actor_id=f"{ignition.layer}:{ignition.location}",
                kind="follow_up",
                payload=FollowUpPayload(
                    layer=ignition.layer, location=ignition.location,
                    kind=spec.kind, cause_id=started_id,
                ),
            )
        if plan.seed_pass:
            system = layer_cfg["system"]
            self._queue.push(
                tick=tick + 1,
                sub_order=SYSTEM_PASS + self._system_order[system],
                actor_id=f"pass:{system}", kind="pass",
                payload=PassPayload(
                    system=system, layer=ignition.layer,
                    causes={ignition.location: started_id},
                ),
            )

    def _run_pass(self, entry: Any) -> None:
        """One spread pass tick over burning locations; re-enqueues itself
        while unburning spots remain (the self-rescheduling system pass)."""
        payload: PassPayload = entry.payload
        result = spread_tick(
            self._pack, self._projection, self._bank, entry.tick,
            payload.layer, payload.causes,
        )
        causes = dict(payload.causes)
        for draft in result.drafts:
            location = draft.target
            record = self._writer.append(
                replace(
                    draft, cause=causes.get(location),
                    provenance={"seed": self._seed},
                )
            )
            self._apply(record)
            causes[location] = record.id
        if result.continue_pass:
            self._queue.push(
                tick=entry.tick + 1,
                sub_order=SYSTEM_PASS + self._system_order[payload.system],
                actor_id=f"pass:{payload.system}", kind="pass",
                payload=PassPayload(
                    system=payload.system, layer=payload.layer, causes=causes
                ),
            )

    def _run_follow_up(self, entry: Any) -> None:
        """A SEEDED smoke / burnout at its trigger tick (TIME-1)."""
        payload: FollowUpPayload = entry.payload
        draft = follow_up_draft(
            self._pack, self._projection, entry.tick, payload.layer,
            payload.location, payload.kind, payload.cause_id,
        )
        if draft is not None:
            record = self._writer.append(
                replace(draft, provenance={"seed": self._seed})
            )
            self._apply(record)

    def _emit_rejection(
        self,
        intent: IntentData,
        tick: int,
        reason: str,
        failed_test: str,
        cause_id: str | None,
    ) -> None:
        """REJECTED: a no-op event with a cause chain — the world did not
        change, but the attempt is canon (phase0 §2)."""
        draft = EventDraft(
            t=tick,
            type=REJECTION_EVENT,
            actor=intent.actor,
            target=intent.target,
            cause=cause_id,
            outcome={
                "action": intent.kind, "reason": reason, "failed_test": failed_test,
            },
            importance="low",
            provenance={"seed": self._seed, "cause_intent": intent.id},
        )
        record = self._writer.append(draft)
        self._apply(record)

    def _apply(self, record: EventRecord) -> None:
        apply_event(self._projection, record)
        self._events.append(record)  # in-memory cache: OCC attribution only
