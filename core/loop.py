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

Every event passes the `_commit` gate (D-035): state deltas are validated
against the projection BEFORE the write, so a resolver bug fails loudly
while the log stays clean — the append-only truth never receives a draft
that disagrees with the world it describes (KI#13). The spread pass is a
per-layer singleton: one pass entry per layer at a time, its cause map
shared with the ignitions (a second fire while a pass runs merges into it
instead of forking a parallel pass — parallel passes double the pack's
chance_per_tick and lose the cause chain, KI#16).

iter-3: `_commit` also feeds the derived knowledge index and dispatches
the event-driven system reactions (crime first, then the telling) — every
committed event's records get their reactions, reaction events carry no
knowledge of their own beyond what legitimately cascades, so the cascade
terminates. Watch rotations fire when the clock CROSSES a rotation tick
(never pre-seeded): the swap, the expectation checks (P2d), then the
briefing (D-006) — each piece cause-chained (phase0 §3).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from core.clock import Clock
from core.crime import briefing_draft, iter_suspicion_reactions, next_rotation_tick, rotation_plan
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
from core.knowledge import KnowledgeView, expectation_drafts, telling_reaction
from core.log import EventDraft, EventLogWriter, EventRecord
from core.pack import Pack
from core.queue import PLAYER_INTENT, SCHEDULED, SYSTEM_PASS, EventQueue
from core.resolvers import REGISTRY
from core.rng import SUBSTANTIVE, RngBank
from core.scheduler import build, decls_from_rules
from core.transitions import WORLD, Ignition, follow_up_draft, ignite, spread_tick

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
    """A transition layer's spread pass. The per-layer cause map (location
    → the location's last transition event id) lives on the Simulator
    (`_pass_causes`) — shared with ignitions so a running pass can chain
    spreads of a fire it did not seed (KI#16)."""

    system: str
    layer: str


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
        self._commit_id = commit
        self._projection = initial_projection(pack.entities)
        self._initial = initial_projection(pack.entities)
        self._events: list[EventRecord] = []
        self._intent_seq = 0
        self._schedule = build(decls_from_rules(pack.rules))
        self._system_order = {
            decl.name: index for index, decl in enumerate(self._schedule)
        }
        # spread-pass state (KI#16): one live pass per layer, causes shared
        self._pass_causes: dict[str, dict[str, str]] = {}
        self._pass_live: set[str] = set()
        # derived knowledge index (L3) + the next watch rotation tick
        self._knowledge = KnowledgeView()
        self._next_rotation = next_rotation_tick(
            pack.rules, self._clock.ticks_per_day, 0
        )

    @property
    def projection(self) -> Projection:
        """The runtime incremental projection (STATE-1)."""
        return self._projection

    @property
    def knowledge(self) -> KnowledgeView:
        """The runtime knowledge index (L3 — derived, rebuildable from the log)."""
        return self._knowledge

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
            seed=self._seed, commit=self._commit_id, pack=self._pack.name_version
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
                        # rotations fire when the clock crosses their tick —
                        # before the entry the crossing happened for
                        while (
                            self._next_rotation is not None
                            and self._next_rotation <= entry.tick
                        ):
                            rotation_tick = self._next_rotation
                            self._clock.advance_to(rotation_tick)
                            self._run_rotation(rotation_tick)
                            self._next_rotation = next_rotation_tick(
                                self._pack.rules,
                                self._clock.ticks_per_day,
                                rotation_tick,
                            )
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
        self._commit(draft)

        for ignition in resolution.ignitions:
            self._execute_ignition(ignition, entry.tick, intent.actor)

    def _execute_ignition(self, ignition: Ignition, tick: int, actor: str) -> None:
        """Run a transition ignition: emit the layer's events (cause
        chained), seed the smoke/burnout follow-ups, start the spread pass.
        A pass already running for the layer absorbs the new fire (the
        shared cause map gains the location) — one pass, one chance per
        tick per spot, one intact cause chain (KI#16)."""
        layer_cfg = self._pack.rules["transitions"][ignition.layer]
        plan = ignite(self._pack, self._projection, tick, ignition, actor)
        last_id = self._writer.last_id
        started_id: str | None = None
        for draft in plan.drafts:
            record = self._commit(
                replace(draft, cause=last_id, provenance={"seed": self._seed})
            )
            last_id = record.id
            if started_id is None:
                started_id = record.id
        if started_id is None:
            return
        self._pass_causes.setdefault(ignition.layer, {})[
            ignition.location
        ] = started_id
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
        if plan.seed_pass and ignition.layer not in self._pass_live:
            self._pass_live.add(ignition.layer)
            system = layer_cfg["system"]
            self._queue.push(
                tick=tick + 1,
                sub_order=SYSTEM_PASS + self._system_order[system],
                actor_id=f"pass:{system}", kind="pass",
                payload=PassPayload(system=system, layer=ignition.layer),
            )

    def _run_pass(self, entry: Any) -> None:
        """One spread pass tick over burning locations; re-enqueues itself
        while unburning spots remain (the self-rescheduling system pass)."""
        payload: PassPayload = entry.payload
        causes = self._pass_causes[payload.layer]
        result = spread_tick(
            self._pack, self._projection, self._bank, entry.tick,
            payload.layer, causes,
        )
        for draft in result.drafts:
            location = draft.target
            record = self._commit(
                replace(
                    draft, cause=causes.get(location),
                    provenance={"seed": self._seed},
                )
            )
            causes[location] = record.id
        if result.continue_pass:
            self._queue.push(
                tick=entry.tick + 1,
                sub_order=SYSTEM_PASS + self._system_order[payload.system],
                actor_id=f"pass:{payload.system}", kind="pass",
                payload=PassPayload(system=payload.system, layer=payload.layer),
            )
        else:
            self._pass_live.discard(payload.layer)

    def _run_follow_up(self, entry: Any) -> None:
        """A SEEDED smoke / burnout at its trigger tick (TIME-1)."""
        payload: FollowUpPayload = entry.payload
        draft = follow_up_draft(
            self._pack, self._projection, entry.tick, payload.layer,
            payload.location, payload.kind, payload.cause_id,
        )
        if draft is not None:
            self._commit(replace(draft, provenance={"seed": self._seed}))

    def _run_rotation(self, tick: int) -> None:
        """One watch rotation at a crossed tick (phase0 §3): the post swap
        (positions), the expectation checks (P2d — violations chain to the
        events that moved the items), then the briefing (D-006 — the
        outgoing holder's records pass, one fidelity step down). Each piece
        commits through the canon door, so its reactions cascade."""
        rotation = self._pack.rules["crime_watch"]["rotation"]
        changes, outgoing, incoming = rotation_plan(self._pack, self._projection)
        watch_record = self._commit(
            EventDraft(
                t=tick,
                type=rotation["watch_event"],
                actor=WORLD,
                cause=self._writer.last_id,  # a scheduled beat: chronological chain
                outcome={"outgoing": outgoing, "incoming": incoming},
                state_changes=changes,
                importance=pack_importance(
                    self._pack.rules,
                    {p for p in (outgoing, incoming) if p is not None},
                    irreversible=0,
                    hooks=0,
                ),
                provenance={"seed": self._seed},
            )
        )
        for draft in expectation_drafts(
            self._pack, self._projection, self._knowledge, self._events, tick
        ):
            self._commit(replace(draft, provenance={"seed": self._seed}))
        briefing = briefing_draft(
            self._pack, self._projection, self._knowledge, tick,
            watch_record.id, outgoing, incoming,
        )
        if briefing is not None:
            self._commit(replace(briefing, provenance={"seed": self._seed}))

    def _react(self, record: EventRecord) -> None:
        """Event-driven system reactions (phase0 §3), dispatched from the
        canon door so no call site can forget them: crime first (suspicion,
        status flip, arrest — chained per knower), then the telling (the
        conversation's teller shares their most salient novel fact)."""
        for group in iter_suspicion_reactions(
            self._pack, self._projection, self._knowledge, record
        ):
            previous = record.id
            for draft in group:
                committed = self._commit(
                    replace(draft, cause=previous, provenance={"seed": self._seed})
                )
                previous = committed.id
        telling = telling_reaction(
            self._pack, self._projection, self._knowledge, self._bank, record
        )
        if telling is not None:
            self._commit(
                replace(
                    telling, cause=record.id, provenance={"seed": self._seed}
                )
            )

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
        self._commit(draft)

    def _commit(self, draft: EventDraft) -> EventRecord:
        """The one door from a draft to the canon (D-035): validate the
        state deltas against the projection, THEN append, THEN apply.
        A draft that disagrees with the world fails here — before the
        write — so the log never holds a desynced event (KI#13);
        `apply_event`'s own from_-check stays as the post-write net.
        Progressive semantics: change N is checked against the state as
        changed by changes 0..N-1 of the same event."""
        pending: dict[tuple[str, str], Any] = {}
        for change in draft.state_changes:
            props = self._projection.get(change.entity)
            key = (change.entity, change.prop)
            current = pending.get(key, props.get(change.prop) if props else None)
            if props is None or current != change.from_:
                held = props.get(change.prop) if props else None
                raise ValueError(
                    f"{draft.type}: state_change {change.entity}.{change.prop} "
                    f"expected from {change.from_!r} but projection holds {held!r}"
                )
            pending[key] = change.to_
        record = self._writer.append(draft)
        apply_event(self._projection, record)
        self._events.append(record)  # in-memory cache: OCC attribution only
        self._knowledge.add(record)  # derived index (L3)
        self._react(record)  # event-driven reactions (phase0 §3)
        return record
