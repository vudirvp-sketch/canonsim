"""Tick driver + playscript runner (KeeperRL `Model::update` shape,
`docs/blueprint/phase0.md` §1): pop the next queue entry in
`(tick, sub_order, actor_id, seq)` order, advance the clock, execute.
Intents enter at the PLAYER_INTENT band; resolvers validate preconditions
against the projection, draw durations from the substantive stream and
enqueue a SCHEDULED completion at `t + duration`; the completion emits the
event (the only canon write, via `core/log.py`) and updates the projection.

Resolver dispatch is a name→callable registry keyed by the pack's
`resolver` field (INV-3: intent names are pack data; core code knows only
generic resolver keys). Iter-1 ships the two check-less actions — movement
(along the pack's exit graph; teleport is impossible) and wait. The ten
check-bearing actions land in iter-2 with the full ActionResolver registry.

Playscript = seed + ordered intents (`MVP_SCOPE.md` §13). The whole run
executes under `assure('substantive')` — a cosmetic draw on this path is
an INV-2 violation made loud (RNG-1).
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from core.clock import Clock
from core.fold import Projection, apply_event, initial_projection
from core.ids import sequence_id
from core.log import EventDraft, EventLogWriter, Importance, StateChange
from core.pack import Pack
from core.queue import PLAYER_INTENT, SCHEDULED, EventQueue
from core.rng import SUBSTANTIVE, RngBank

__all__ = [
    "Acceptance",
    "CompletionPayload",
    "IntentData",
    "Resolver",
    "RunResult",
    "RunnerError",
    "Simulator",
    "load_playscript",
]


class RunnerError(RuntimeError):
    """Run-time violation: unknown intent, broken precondition, bad step."""


@dataclass(frozen=True, slots=True)
class IntentData:
    """One playscript intent: a proposal, not yet an event."""

    id: str
    kind: str
    actor: str
    target: str | None
    fields: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class Acceptance:
    """A resolver's decision: duration + the completion's payload."""

    duration: int
    state_changes: tuple[StateChange, ...] = ()
    outcome: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CompletionPayload:
    intent: IntentData
    acceptance: Acceptance


@dataclass(frozen=True, slots=True)
class RunResult:
    """What a finished run produced."""

    log_path: Path
    event_count: int
    last_tick: int
    fingerprint: int


Resolver = Callable[[Pack, Projection, RngBank, IntentData], Acceptance]


# -- resolvers (generic core vocabulary; setting data stays in the pack) ----


def _resolve_movement(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData
) -> Acceptance:
    """Move the actor to an adjacent location; teleport is impossible."""
    if intent.target is None:
        raise RunnerError("move requires a target location")
    if intent.fields:
        raise RunnerError(f"move takes no extra step fields: {sorted(intent.fields)}")
    entities = pack.entities
    locations = {loc["id"]: loc for loc in entities["locations"]}
    if intent.target not in locations:
        raise RunnerError(f"unknown location {intent.target!r}")
    current = projection[intent.actor]["position"]
    if intent.target not in locations[current]["exits"]:
        raise RunnerError(
            f"teleport stays impossible: {intent.target!r} is not adjacent to {current!r}"
        )
    ticks = pack.action(intent.kind)["ticks"]
    duration = bank.randint(ticks["min"], ticks["max"])
    change = StateChange(
        entity=intent.actor, prop="position", from_=current, to_=intent.target
    )
    return Acceptance(duration=duration, state_changes=(change,))


def _resolve_wait(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData
) -> Acceptance:
    """Advance N ticks; the duration is caller-supplied (MVP_SCOPE §7)."""
    ticks = intent.fields.get("ticks")
    if not isinstance(ticks, int) or isinstance(ticks, bool) or ticks < 1:
        raise RunnerError(f"wait requires a positive integer 'ticks' step field, got {ticks!r}")
    if set(intent.fields) != {"ticks"}:
        raise RunnerError(f"wait takes only the 'ticks' field: {sorted(intent.fields)}")
    return Acceptance(duration=ticks)


_REGISTRY: Final[dict[str, Resolver]] = {
    "movement": _resolve_movement,
    "wait": _resolve_wait,
}


def load_playscript(path: Path) -> dict[str, Any]:
    """Load a playscript fixture (seed + ordered intents, MVP_SCOPE §13)."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


# -- the simulator ---------------------------------------------------------


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
        self._intent_seq = 0

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
                f"playscript pack {script['pack']!r} != loaded pack {self._pack.name_version!r}"
            )
        steps = list(script["steps"])
        self._writer.write_header(
            seed=self._seed, commit=self._commit, pack=self._pack.name_version
        )
        try:
            if steps:
                with self._bank.assure(SUBSTANTIVE):
                    self._queue.push(
                        tick=self._clock.tick, sub_order=PLAYER_INTENT,
                        actor_id=self._pack.player_id(), kind="intent",
                        payload=self._intent_from_step(steps[0]),
                    )
                    remaining = steps[1:]
                    while len(self._queue):
                        entry = self._queue.pop()
                        self._clock.advance_to(entry.tick)
                        if entry.kind == "intent":
                            self._execute_intent(entry)
                        else:
                            self._complete(entry)
                            if remaining:
                                self._queue.push(
                                    tick=entry.tick, sub_order=PLAYER_INTENT,
                                    actor_id=self._pack.player_id(), kind="intent",
                                    payload=self._intent_from_step(remaining[0]),
                                )
                                remaining = remaining[1:]
            return RunResult(
                log_path=self._writer.path,
                event_count=self._writer.event_count,
                last_tick=self._clock.tick,
                fingerprint=self._bank.fingerprint,
            )
        finally:
            self._writer.close()

    def _intent_from_step(self, step: Mapping[str, Any]) -> IntentData:
        kind = step.get("intent")
        if not isinstance(kind, str):
            raise RunnerError(f"playscript step missing 'intent': {step!r}")
        intent_id = sequence_id("intent", self._intent_seq)
        self._intent_seq += 1
        fields = {key: value for key, value in step.items() if key not in ("intent", "target")}
        return IntentData(
            id=intent_id, kind=kind, actor=self._pack.player_id(),
            target=step.get("target"), fields=fields,
        )

    def _execute_intent(self, entry: Any) -> None:
        intent: IntentData = entry.payload
        action = self._pack.action(intent.kind)
        if action is None:
            raise RunnerError(f"unknown intent {intent.kind!r} (not in the pack's actions)")
        resolver_key = action.get("resolver")
        if not isinstance(resolver_key, str):
            raise RunnerError(
                f"action {intent.kind!r} has no resolver yet (action resolvers land iter-2)"
            )
        resolver = _REGISTRY.get(resolver_key)
        if resolver is None:
            raise RunnerError(f"unknown resolver key {resolver_key!r}")
        acceptance = resolver(self._pack, self._projection, self._bank, intent)
        self._queue.push(
            tick=entry.tick + acceptance.duration, sub_order=SCHEDULED,
            actor_id=intent.actor, kind="completion",
            payload=CompletionPayload(intent=intent, acceptance=acceptance),
        )

    def _complete(self, entry: Any) -> None:
        payload: CompletionPayload = entry.payload
        if payload.intent.kind not in self._pack.event_types():
            raise RunnerError(
                f"event type {payload.intent.kind!r} is unknown to the pack "
                f"(closed vocabulary, EVENT_SCHEMA §11)"
            )
        draft = EventDraft(
            t=entry.tick,
            type=payload.intent.kind,
            actor=payload.intent.actor,
            target=payload.intent.target,
            cause=self._writer.last_id,  # None only for the run-start event
            outcome={"duration": payload.acceptance.duration, **payload.acceptance.outcome},
            state_changes=payload.acceptance.state_changes,
            importance=self._importance(payload),
            provenance={"seed": self._seed, "cause_intent": payload.intent.id},
        )
        record = self._writer.append(draft)
        apply_event(self._projection, record)

    def _importance(self, payload: CompletionPayload) -> Importance:
        """Pack-rule importance (MVP_SCOPE §9): entities touched +
        irreversibility + hooks — never by feel. iter-1 events carry no
        hooks; the per-hook term joins when Acceptance grows hooks (iter-2)."""
        score_rule = self._pack.rules["importance"]["score"]
        thresholds = self._pack.rules["importance"]["thresholds"]
        entities = {payload.intent.actor}
        if payload.intent.target is not None:
            entities.add(payload.intent.target)
        entities.update(change.entity for change in payload.acceptance.state_changes)
        score = 0
        if len(entities) >= 2:
            score += score_rule["entities_touched_at_least_2"]
        if any(change.irreversible for change in payload.acceptance.state_changes):
            score += score_rule["irreversible_state_change"]
        if score >= thresholds["high"]:
            return "high"
        if score >= thresholds["medium"]:
            return "medium"
        return "low"
