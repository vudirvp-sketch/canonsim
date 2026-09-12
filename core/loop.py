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
maclock-1: the macro-clock crossings join the same discipline (L4
layered clocks — the third crossing): the positive multiples of the
pack-declared `time.macro.cadence_ticks`, fired coarsest-first at a
co-occurring tick (the year turns before the day's rotation, the
rotation before the beat), each turn ONE event through the canon door
(the calendar's increments are canon, INV-1 — `core/macro.py` owns the
primitive).
weather-1: the ambient family rides the same crossing — the weather
chain rolls its next state AFTER the turn (`core/weather.py` owns the
family; the event chained to the turn, the drift's precedent) and its
SEEDED erosion follow-ups run as SCHEDULED entries (the fire
shape, TIME-1).
depth-3: the macro crossing is the scene LOD's WARM cadence — under
an armed clock the turn carries the cold-background census (the D-112
count on the aggregate surface), the warm ring's NPCs tick at the
crossing (drift + goal rolls, `core/lod.py` owns the zones), and the
beats scope to the ACTIVE scene alone; the unarmed law keeps the
one-scene world (the whole simulation per-beat, the v0.1 bytes).
depth-7: the write-side LOD at group scale rides the same discipline
(`core/groups.py`) — the condensation (a group's anchor crossing into
the warm/active zones births its members' canon `member_of`, the
tombstone marker stopping the group's population-tier macro-ticks)
and the cold background's macro-tick aggregates (one cardinality
event per cold group per crossing, actor = the group id — D-112's
one id, all tiers).
"""

from __future__ import annotations

import json
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from core.checkpoint import (
    INDEX_NAME,
    CheckpointError,
    load_checkpoint,
    prefix_digest,
    read_index,
)
from core.clock import Clock
from core.crime import (
    arrest_resolution_draft,
    briefing_draft,
    iter_suspicion_reactions,
    next_rotation_tick,
    rotation_plan,
)
from core.cursor import CursorError
from core.director import Director, policy_from_rules
from core.echo import echo_scores
from core.factions import faction_intents
from core.fold import Projection, apply_event, fold, initial_projection
from core.groups import condensation_drafts, macro_tick_drafts
from core.ids import sequence_id
from core.intent import (
    ECHO_TEST,
    EDGE_TICKS,
    LEVERAGE_TEST,
    REJECTION_EVENT,
    TRAIT_TEST,
    IntentData,
    RunnerError,
    action_duration,
    first_failing,
    occ_breaking_cause,
    pack_importance,
    requires_for,
    run_check,
    validate_shape,
)
from core.knowledge import KnowledgeView, expectation_drafts, telling_reaction
from core.leverage import leverage_drafts, live_leverage, spendable_leverage
from core.lod import COLD_COUNT_KEY, SceneZones, npc_population, scene_zones
from core.log import EventDraft, EventLogWriter, EventRecord
from core.macro import macro_turn_draft, next_macro_tick
from core.onaction import on_action_drafts
from core.pack import Pack
from core.queue import NPC_REACTION, PLAYER_INTENT, SCHEDULED, SYSTEM_PASS, EventQueue
from core.reflection import reflection_drafts
from core.resolvers import REGISTRY
from core.rng import SUBSTANTIVE, RngBank
from core.scheduler import build, decls_from_rules
from core.states import decay_drafts, rotation_resets
from core.traits import crystallized_traits
from core.transitions import WORLD, Ignition, follow_up_draft, ignite, spread_tick
from core.travel import edge_duration
from core.urgencies import urgency_intents
from core.weather import (
    current_weather,
    erosion_drafts,
    erosion_specs,
    weather_turn_draft,
)
from core.worldgen import (
    WORLDGEN_BLOCK,
    WorldModel,
    generate_world,
    genesis,
)

__all__ = [
    "CompletionPayload",
    "FollowUpPayload",
    "IntentData",
    "PassPayload",
    "REJECTION_EVENT",
    "RunResult",
    "RunnerError",
    "Simulator",
    "WeatherPayload",
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
class WeatherPayload:
    """A SEEDED weather erosion follow-up at its trigger tick (the fire
    follow-ups' shape over the ambient family's own rule): the rule's event
    type IS the queue identity (unique per block by lint); the drafts
    read the fold at fire time — the world's state then, never the
    state it held at seed time."""

    event_type: str
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
        *,
        director_enabled: bool = True,
        append_writer: EventLogWriter | None = None,
    ) -> None:
        self._pack = pack
        self._seed = int(seed)
        self._bank = RngBank(self._seed)
        self._clock = Clock.from_rules(dict(pack.rules["time"]))
        self._queue = EventQueue()
        # The resume door (iter-106/D-139): a pre-opened APPEND-mode
        # writer rides in — positioned over an existing log (its own
        # construction validated every line, T0). `log_path` is ignored
        # in that case (the writer owns its path); fresh runs keep the
        # write-mode writer and the header written by `open()`.
        self._writer = (
            EventLogWriter(log_path, event_schema)
            if append_writer is None
            else append_writer
        )
        self._commit_id = commit
        self._projection = initial_projection(pack.entities)
        self._initial = initial_projection(pack.entities)
        self._events: list[EventRecord] = []
        self._intent_seq = 0
        self._player_id = pack.player_id()
        # the current playscript step's intent id (scene-2: the KI#17
        # generalization — the feed advances on THE STEP'S OWN ending,
        # whatever its actor; autonomous intents carry other ids and
        # never advance the script)
        self._step_intent_id: str | None = None
        self._schedule = build(decls_from_rules(pack.rules))
        self._system_order = {
            decl.name: index for index, decl in enumerate(self._schedule)
        }
        # spread-pass state (KI#16): one live pass per layer, causes shared
        self._pass_causes: dict[str, dict[str, str]] = {}
        self._pass_live: set[str] = set()
        # derived knowledge index (L3) + the next watch rotation tick
        self._knowledge = KnowledgeView()
        # derived last-change index (L3): (entity, prop) -> tick of the
        # latest committed event that changed it — the decay baseline
        # without a per-beat log scan; `_commit` is its only writer
        self._last_change: dict[tuple[str, str], int] = {}
        self._next_rotation = next_rotation_tick(
            pack.rules, self._clock.ticks_per_day, 0
        )
        # maclock-1 (L4): the macro-clock's next crossing — None for an
        # unarmed pack (no `time.macro` block; zero crossings, zero
        # events, the v0.1 bytes untouched — the 68a pattern). The
        # crossing state persists across `run_steps` calls like the
        # rotation and beat cursors (the session law).
        self._next_macro = next_macro_tick(
            pack.rules["time"].get("macro"), 0
        )
        # iter-4: the director + the beat cycle (decay / urgencies /
        # entropy). The beat fires at clock crossings (phase boundaries
        # by default; pack-tunable via `urgencies.beat_ticks` —
        # DIRECTOR_SPEC §7 owns the beat axis; KI#61).
        # Director-off keeps the buffer seeding (D-005 hygiene) but
        # suppresses releases — the T8 A/B baseline.
        self._director = Director(
            pack=pack, policy=policy_from_rules(pack.rules, director_enabled)
        )
        self._next_beat = self._first_beat(pack.rules)
        # depth-5: the generated world (None for an unarmed pack — the
        # 68a pattern; `open` runs the genesis only when the pack
        # declares the worldgen block)
        self._world: WorldModel | None = None

    @property
    def projection(self) -> Projection:
        """The runtime incremental projection (STATE-1)."""
        return self._projection

    @property
    def world(self) -> WorldModel | None:
        """The generated world model (depth-5): None for an unarmed
        pack, else the ordered passes' output — derived, rebuildable
        from the seed, never truth (L11)."""
        return self._world

    @property
    def knowledge(self) -> KnowledgeView:
        """The runtime knowledge index (L3 — derived, rebuildable from the log)."""
        return self._knowledge

    @property
    def director(self) -> Director:
        """The runtime director (T8 A/B uses director_enabled=False at construction)."""
        return self._director

    @property
    def drained(self) -> bool:
        """Whether the run sits at a clean drain boundary: the queue is
        empty — every scheduled completion, seeded follow-up and spread
        pass has fired, the world is settled between player inputs. The
        cursor's save law (`export_cursor`): a mid-drain state is not
        resume-able (its pending queue entries are not log-derivable),
        so the cursor is pinned only here (D-139)."""
        return not len(self._queue)

    def open(self) -> None:
        """Write the run header — an incremental session starts here.

        The CLI play loop (`cli/`) opens once, feeds steps through
        `run_steps` between commands, and closes at exit; the log is one
        continuous run either way (`run_playscript` is the batch front
        over the same three doors).

        depth-5: an ARMED pack (the `worldgen` block) runs the genesis
        here — the ordered passes over the seed, the claims through the
        gate, then the pre-PC history events committed through the one
        canon door BEFORE any player step: the PC walks into a running
        world, the director's buffer pre-seeded (phases.md §5). The
        first genesis event is the run's run-start event (cause null).
        chron-2 (L7 — the chain visible at record time): the worldgen
        owns the CAUSE TREE (the parent map, draft indices — a
        collection member chains to its nearest lower-tier predecessor,
        a top-level event to the previous top-level event; the flat
        form is the linear chain); this loop resolves each parent
        through the WRITER'S OWN ids as it commits — the id law stays
        the writer's single owner. The worldgen streams are
        family-isolated from the
        substantive canon checks, so the run's canon draws never move —
        the armed arm's price is the genesis events alone. An unarmed
        pack answers `(None, (), ())` before any stream touch: zero
        draws, zero events, the v0.1 bytes untouched by construction.
        """
        self._writer.write_header(
            seed=self._seed, commit=self._commit_id, pack=self._pack.name_version
        )
        model, drafts, parents = genesis(
            self._bank, self._pack.rules, self._events, self._seed
        )
        self._world = model
        if model is None:
            return
        with self._bank.assure(SUBSTANTIVE):
            ids: list[str] = []
            for draft, parent in zip(drafts, parents, strict=True):
                record = self._commit(
                    replace(draft, cause=None if parent < 0 else ids[parent])
                )
                ids.append(record.id)

    def run_steps(self, steps: Sequence[Mapping[str, Any]]) -> RunResult:
        """Feed player steps through the live simulator until the queue
        drains. Callable repeatedly on one opened Simulator (the session
        pattern): each call is a self-contained feed-and-drain cycle, so
        the world between calls moves only through the queue it seeded —
        beats, rotations and reactions fire on clock crossings during
        entry processing, exactly as in a batch run.
        """
        steps = list(steps)
        if steps:
            with self._bank.assure(SUBSTANTIVE):
                remaining = steps[1:]
                first = self._intent_from_step(steps[0])
                self._step_intent_id = first.id
                self._queue.push(
                    tick=self._clock.tick, sub_order=self._step_band(first),
                    actor_id=first.actor, kind="intent", payload=first,
                )
                while len(self._queue):
                    entry = self._queue.pop()
                    # clock-crossing beats fire before the popped entry —
                    # rotations (iter-3) AND decay/urgencies/director
                    # (iter-4) all ride the same crossing discipline,
                    # never pre-seeded (a run still ends when its
                    # script's queue drains). Crossings fire in TICK
                    # ORDER: a beat at T=720 between rotations at T=360
                    # and T=1080 fires between them, not after both —
                    # otherwise the log writer's tick-monotonicity
                    # invariant would reject the out-of-order commit.
                    while True:
                        candidates: list[int] = []
                        if (
                            self._next_rotation is not None
                            and self._next_rotation <= entry.tick
                        ):
                            candidates.append(self._next_rotation)
                        if (
                            self._next_beat is not None
                            and self._next_beat <= entry.tick
                        ):
                            candidates.append(self._next_beat)
                        if (
                            self._next_macro is not None
                            and self._next_macro <= entry.tick
                        ):
                            candidates.append(self._next_macro)
                        if not candidates:
                            break
                        crossing = min(candidates)
                        self._clock.advance_to(crossing)
                        # maclock-1: at a co-occurring tick the COARSEST
                        # clock fires first (the year turns before the
                        # day's rotation, the rotation before the beat —
                        # the calendar contains the day, the day contains
                        # the beat); one crossing kind per iteration, the
                        # equal-tick remaining candidates re-loop (the
                        # writer's tick-monotonicity allows equal ticks).
                        if crossing == self._next_macro:
                            self._run_macro(crossing, entry.tick)
                            self._next_macro = next_macro_tick(
                                self._pack.rules["time"].get("macro"),
                                crossing,
                            )
                        elif crossing == self._next_rotation:
                            self._run_rotation(crossing)
                            self._next_rotation = next_rotation_tick(
                                self._pack.rules,
                                self._clock.ticks_per_day,
                                crossing,
                            )
                        else:
                            self._run_beat(crossing, entry.tick)
                            self._next_beat = self._next_beat_after(crossing)
                    self._clock.advance_to(entry.tick)
                    if entry.kind == "intent":
                        accepted = self._execute_intent(entry)
                        # only the CURRENT step's own lifecycle feeds the
                        # next playscript step — an autonomous (urgency /
                        # director) intent ending must never advance the
                        # script (KI#17: step 3 committed before step 2;
                        # scene-2 generalizes the proxy "the actor is the
                        # player" to the exact law: the ending entry IS
                        # the step's own intent — actor steps chain the
                        # same way, autonomous intents never match)
                        if (
                            not accepted and remaining
                            and entry.payload.id == self._step_intent_id
                        ):
                            self._feed_next(entry.tick, remaining)
                    elif entry.kind == "completion":
                        self._complete(entry)
                        if (
                            remaining
                            and entry.payload.intent.id == self._step_intent_id
                        ):
                            self._feed_next(entry.tick, remaining)
                    elif entry.kind == "pass":
                        self._run_pass(entry)
                    elif entry.kind == "weather":
                        self._run_weather_follow_up(entry)
                    else:
                        self._run_follow_up(entry)
        return RunResult(
            log_path=self._writer.path,
            event_count=self._writer.event_count,
            last_tick=self._clock.tick,
            fingerprint=self._bank.fingerprint,
        )

    def close(self) -> None:
        """Flush and close the log — the run is over, the log is canon."""
        self._writer.close()

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
        self.open()
        try:
            return self.run_steps(list(script["steps"]))
        finally:
            self.close()

    # -- the resume door (iter-106, D-139: resume is invisible to the log)

    def export_cursor(self, *, director_enabled: bool) -> dict[str, Any]:
        """The run cursor payload (`core/cursor.py` owns the artifact):
        the run's entropy-and-clock position, pinned at a CLEAN drain
        boundary — mid-drain is refused loudly (the queue's pending
        entries are not log-derivable; saving there would promise a
        resume the artifact cannot honor). Everything the fold rebuilds
        is deliberately absent: the projection, the knowledge index, the
        last-change index, the seeded-hook buffer (exactly rebuildable
        by `Director.seed` over the log), the WorldModel (a pure
        function of seed + pack config, re-derived at resume). What
        rides here is ONLY what silent draws and run cursors own: bank
        positions, director run marks, the clock, the crossing cursors,
        the intent counter. `director_enabled` is the caller's live
        policy toggle (the session's own flag — a per-run knob, not
        canon; the resumed run restores it, D-139)."""
        if len(self._queue):
            raise RunnerError(
                f"the cursor is a drain-boundary artifact: the queue holds "
                f"{len(self._queue)} pending entries — finish or abandon the "
                "drain before pinning run state"
            )
        return {
            "seed": self._seed,
            "pack": self._pack.name_version,
            "event_count": self._writer.event_count,
            "prefix_sha256": prefix_digest(
                self._writer.path, self._writer.event_count
            ),
            "tick": self._clock.tick,
            "next_rotation": self._next_rotation,
            "next_beat": self._next_beat,
            "next_macro": self._next_macro,
            "intent_seq": self._intent_seq,
            "director_enabled": director_enabled,
            "bank": self._bank.export_state(),
            "director": self._director.export_run_state(),
        }

    @classmethod
    def resume(
        cls,
        pack: Pack,
        log_path: Path,
        event_schema: Mapping[str, Any],
        cursor: Mapping[str, Any],
        *,
        commit: str = "unknown",
        checkpoints_dir: Path | None = None,
    ) -> "Simulator":
        """Open a live session over an existing log (the resume door,
        `phases.md` §7 — owner-gated since iter-80, opened by the
        owner's iter-106 call; D-139: **resume is invisible to the
        log** — a session interrupted at a drain boundary and resumed
        with the same remaining steps is byte-identical to the
        uninterrupted run; interruption is not an input, only steps
        are).

        The binding chain, every link loud: the append-mode writer's
        own read validates the whole log (T0) plus the schema-version
        and env-pin laws; the cursor must name THIS run (seed, pack)
        and THIS log exactly (`event_count` + `prefix_sha256` — a log
        that moved past the cursor, e.g. a mid-drain crash, refuses:
        the extra events' entropy is unrecoverable and guessing it
        would be save-scumming, not determinism). The log-derivable
        state rebuilds from the log — the projection through the
        checkpoint fast-path when the operator's artifacts exist and
        anchor cleanly (`_restore_projection`), the indexes and the
        director buffer by one ordered pass — and the entropy position
        restores from the cursor (bank positions, director run marks,
        clock, crossing cursors, intent counter). The WorldModel
        re-derives through `generate_world` (a pure function of seed +
        pack config; the genesis commits are already in the log, and
        the bank's worldgen streams were excluded from the cursor
        exactly so this rebuild re-draws their original positions).

        A resumed simulator feeds `run_steps` like any session; the
        batch front (`run_playscript`) is a fresh-run door — its
        `open()` refuses on an already-written header, loudly.
        `checkpoints_dir` follows the operator convention
        (`output/checkpoints/<log_stem>/`, `scripts/checkpoint.py`);
        absent artifacts are normal operation (the plain fold answers).
        """
        writer = EventLogWriter(log_path, event_schema, append=True)
        try:
            appended = writer.appended
            assert appended is not None  # append mode always populates it
            header, events = appended
            if cursor["seed"] != header["seed"]:
                raise CursorError(
                    f"cursor seed {cursor['seed']!r} != log header seed "
                    f"{header['seed']!r} — the cursor belongs to another run"
                )
            if cursor["pack"] != header["pack"] or header["pack"] != pack.name_version:
                raise CursorError(
                    f"cursor pack {cursor['pack']!r} / log header "
                    f"{header['pack']!r} != loaded pack {pack.name_version!r} "
                    "— the initial projection would be a lie"
                )
            if writer.event_count != cursor["event_count"]:
                raise CursorError(
                    f"stale cursor: the log holds {writer.event_count} events, "
                    f"the cursor pins {cursor['event_count']} — the run moved "
                    "past the pin (a mid-drain crash or a manual append); the "
                    "extra events' entropy state is unrecoverable"
                )
            digest = prefix_digest(log_path, int(cursor["event_count"]))
            if digest != cursor["prefix_sha256"]:
                raise CursorError(
                    f"cursor prefix digest {cursor['prefix_sha256']!r} != this "
                    f"log's {digest!r} at the pinned offset — the log or the "
                    "cursor was edited; refusing to guess"
                )
            sim = cls(
                pack, int(cursor["seed"]), log_path, event_schema,
                commit=commit, director_enabled=bool(cursor["director_enabled"]),
                append_writer=writer,
            )
            sim._events = list(events)
            sim._projection = sim._restore_projection(events, checkpoints_dir)
            for event in events:
                sim._knowledge.add(event)
                for change in event.state_changes:
                    sim._last_change[(change.entity, change.prop)] = event.t
                sim._director.seed(event)
            sim._director.restore_run_state(cursor["director"])
            sim._bank.restore_state(cursor["bank"])
            if events and int(cursor["tick"]) < events[-1].t:
                raise CursorError(
                    f"cursor tick {cursor['tick']} sits behind the log's last "
                    f"event at t={events[-1].t} — the cursor is a lie about "
                    "its run"
                )
            sim._clock.advance_to(int(cursor["tick"]))
            for key, attr in (
                ("next_rotation", "_next_rotation"),
                ("next_beat", "_next_beat"),
                ("next_macro", "_next_macro"),
            ):
                value = cursor[key]
                if value is not None and value <= sim._clock.tick:
                    raise CursorError(
                        f"cursor {key} = {value} does not sit strictly after "
                        f"the pinned tick {sim._clock.tick} — the never-regress "
                        "law is part of the run state"
                    )
                setattr(sim, attr, value)
            sim._intent_seq = int(cursor["intent_seq"])
            if pack.rules.get(WORLDGEN_BLOCK) is not None:
                sim._world = generate_world(
                    sim._bank, pack.rules[WORLDGEN_BLOCK]
                )
            return sim
        except BaseException:
            writer.close()
            raise

    def _restore_projection(
        self,
        events: Sequence[EventRecord],
        checkpoints_dir: Path | None,
    ) -> Projection:
        """The resume projection: the checkpoint fast-path when the
        operator's artifacts exist and anchor cleanly (snapshot + tail
        replay, `phases.md` §5 — `core/checkpoint.py`'s first RUNTIME
        consumer; the module was built for exactly this door), else the
        plain fold over the pack-seeded initial projection. Both paths
        answer the same state (the re-fold law); the checkpoint only
        cuts the fold cost. Present-but-wrong is LOUD — the anchors
        have teeth (a foreign index, a mismatched prefix digest, a
        corrupted artifact); ABSENT is normal operation, never an
        error."""
        if checkpoints_dir is None or not (checkpoints_dir / INDEX_NAME).is_file():
            return fold(events, self._initial)
        index = read_index(checkpoints_dir)
        if index.log != self._writer.path.name:
            raise CheckpointError(
                f"checkpoint index names log {index.log!r} != "
                f"{self._writer.path.name!r} — the artifacts are foreign"
            )
        if index.pack != self._pack.name_version:
            raise CheckpointError(
                f"checkpoint index pack {index.pack!r} != loaded "
                f"{self._pack.name_version!r} — the snapshots folded a "
                "different initial projection"
            )
        record = index.records[-1]  # sorted by offset: the latest
        if record.offset > len(events):
            raise CheckpointError(
                f"checkpoint offset {record.offset} exceeds the log's "
                f"{len(events)} events — the artifacts are foreign"
            )
        if prefix_digest(self._writer.path, record.offset) != record.prefix_sha256:
            raise CheckpointError(
                f"checkpoint prefix digest at offset {record.offset} does not "
                "match this log — the snapshot or the log drifted"
            )
        checkpoint = load_checkpoint(record, checkpoints_dir)
        return checkpoint.restore(events)

    def _feed_next(self, tick: int, remaining: list[Mapping[str, Any]]) -> None:
        intent = self._intent_from_step(remaining.pop(0))
        self._step_intent_id = intent.id
        self._queue.push(
            tick=tick, sub_order=self._step_band(intent),
            actor_id=intent.actor, kind="intent", payload=intent,
        )

    def _step_band(self, intent: IntentData) -> int:
        """The step's sub_order band: PLAYER_INTENT for the player's own
        steps (mode A — the default, no actor key), NPC_REACTION for an
        actor step (mode B's reply door — the chorus rides the same band
        as the autonomous intents, after the player's intents at the
        same tick, before scheduled completions; D-037's band law)."""
        if intent.actor == self._player_id:
            return PLAYER_INTENT
        return NPC_REACTION

    def _intent_from_step(self, step: Mapping[str, Any]) -> IntentData:
        kind = step.get("intent")
        if not isinstance(kind, str):
            raise RunnerError(f"playscript step missing 'intent': {step!r}")
        actor = step.get("actor", self._player_id)
        if actor != self._player_id and (
            not isinstance(actor, str) or self._pack.kind_of(actor) != "npc"
        ):
            raise RunnerError(
                f"playscript step actor must be a pack npc id, got {actor!r} "
                f"(the player needs no actor key — mode A's default)"
            )
        intent_id = sequence_id("intent", self._intent_seq)
        self._intent_seq += 1
        fields = {
            key: value
            for key, value in step.items()
            if key not in ("intent", "target", "actor")
        }
        return IntentData(
            id=intent_id, kind=kind, actor=actor,
            target=step.get("target"), fields=fields,
            based_on_event_seq=self._writer.event_count,
        )

    # -- the intent front door -------------------------------------------------

    def _windowed(self, preconditions: Sequence[Mapping[str, Any]]) -> bool:
        """Whether the precondition list carries any tick-windowed test
        (the leverage liveness window, iter-45; the echo decay, iter-46;
        the trait crystallization, iter-67 — beliefwire): those intents
        are evaluated against the derived folds read at THE CALLER'S OWN
        TICK — pure reads, no RNG, no events, computed only when the
        action asks for them (every other action pays nothing)."""
        return any(
            cond.get("test") in (LEVERAGE_TEST, ECHO_TEST, TRAIT_TEST)
            for cond in preconditions
        )

    def _fold_reads(
        self, preconditions: Sequence[Mapping[str, Any]], tick: int
    ) -> tuple[tuple[Any, ...], tuple[Any, ...], tuple[Any, ...]]:
        """The lazy fold triple for one evaluation: the live leverage
        facts, the echo scores, and the crystallized traits, each
        computed ONLY when the precondition list reads that fold (the
        iter-45 laziness law — an echo-gated intent never pays the
        leverage scan, a trait-gated one never pays either, and an
        ungated one pays nothing), all read at the caller's own tick
        (the window law — beliefwire, iter-67, joins the family: the
        fold's answer is per-tick, the counter-block can un-crystallize
        a belief on records born between evaluations)."""
        tests = {cond.get("test") for cond in preconditions}
        facts = (
            live_leverage(self._pack, self._events, tick)
            if LEVERAGE_TEST in tests
            else ()
        )
        echoes = (
            echo_scores(self._pack, self._knowledge, tick)
            if ECHO_TEST in tests
            else ()
        )
        traits = (
            crystallized_traits(self._pack, self._knowledge, tick)
            if TRAIT_TEST in tests
            else ()
        )
        return facts, echoes, traits

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
        preconditions = requires_for(action, intent)
        facts, echoes, traits = self._fold_reads(preconditions, entry.tick)
        failing = first_failing(
            self._pack, self._projection, intent, preconditions,
            facts=facts, echoes=echoes, traits=traits,
        )
        if failing is not None:
            self._emit_rejection(
                intent, entry.tick, reason="precondition", failed_test=failing,
                cause_id=self._writer.last_id,
            )
            return False
        # st-6a (D-116 (5)): an edge-priced action — travel, the
        # movement twin — prices its completion through the travel
        # price law at THIS door (resolve time, L3: derive, never
        # store): the pack override wins per edge, else the WorldModel
        # derivation (integer math, no division, draw-free — the
        # fingerprint never sees a price). The completion entry then
        # rides the queue like any other: `t + price`, the clock jumps
        # ahead (day-scale durations queue-cheap, MVP_SCOPE §8), and
        # beats/rotations/macro crossings still fire mid-travel in tick
        # order (D-038). A moved projection between accept and
        # completion is the OCC re-check's own rejection — the price is
        # committed to the entry here, never re-read at completion.
        duration = (
            edge_duration(
                self._pack.rules, self._world, self._projection, intent
            )
            if action["ticks"] == EDGE_TICKS
            else action_duration(action, self._bank, intent)
        )
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
        world reactions (ignitions, passes, follow-ups).

        iter-45 (social-1b): the OCC re-check is UNCONDITIONAL for
        intents carrying a tick-windowed test (the leverage window, the
        echo decay) — the projection is event-driven, but the windows
        are tick-driven: they can close between accept and completion
        with no event committed, and the re-check must catch that too
        (the rejection chains to the last committed event —
        `occ_breaking_cause` never attributes a window close to an
        event it did not break). The spend stamping: an intent
        resolving to the pack-declared `secrets.spend_event` type
        carries the spent cluster's id, secret and type in its
        outcome — the log names the fact it consumed (the loop owns the
        log, so the loop owns the reference; the resolver stays
        fold-blind — the arrest-resolution precedent for loop-side,
        event-type-keyed, pack-declared decoration)."""
        payload: CompletionPayload = entry.payload
        intent = payload.intent
        action = self._pack.action(intent.kind)
        assert action is not None  # validated at the front door

        preconditions = requires_for(action, intent)
        windowed = self._windowed(preconditions)
        facts, echoes, traits = self._fold_reads(preconditions, entry.tick)
        if self._writer.event_count > payload.based_on_event_seq or windowed:
            failing = first_failing(
                self._pack, self._projection, intent, preconditions,
                facts=facts, echoes=echoes, traits=traits,
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
        outcome: dict[str, Any] = {
            "duration": payload.duration, **resolution.outcome,
        }
        spend_type = self._pack.rules.get("secrets", {}).get("spend_event")
        if spend_type is not None and resolution.event_type == spend_type:
            if intent.target is None:  # unreachable: the door demands a target
                raise RunnerError("a leverage spend requires a target npc")
            fact = spendable_leverage(facts, intent.actor, intent.target)
            outcome["cluster"] = fact.source
            outcome["secret"] = fact.secret
            outcome["type"] = fact.type
        draft = EventDraft(
            t=entry.tick,
            type=resolution.event_type,
            actor=intent.actor,
            target=intent.target,
            cause=self._writer.last_id,  # None only for the run-start event
            outcome=outcome,
            knowledge=resolution.knowledge,
            state_changes=resolution.state_changes,
            hooks=resolution.hooks,
            importance=pack_importance(
                self._pack.rules, entities,
                irreversible=sum(
                    1 for change in resolution.state_changes if change.irreversible
                ),
                hooks=len(resolution.hooks),
                event_type=resolution.event_type,
            ),
            provenance=self._provenance(intent),
        )
        record = self._commit(draft)

        for ignition in resolution.ignitions:
            self._execute_ignition(
                ignition, entry.tick, intent.actor, record.id
            )

    def _execute_ignition(
        self, ignition: Ignition, tick: int, actor: str, cause_id: str
    ) -> None:
        """Run a transition ignition: emit the layer's events (cause
        chained), seed the smoke/burnout follow-ups, start the spread pass.
        A pass already running for the layer absorbs the new fire (the
        shared cause map gains the location) — one pass, one chance per
        tick per spot, one intact cause chain (KI#16). The first layer
        event chains to the ACTION that ignited (suspectaxis-2: the
        commit door may run knowledge reactions between the action and
        the ignition — the fire's cause is the igniting action, never a
        bystander's suspicion reaction)."""
        layer_cfg = self._pack.rules["transitions"][ignition.layer]
        plan = ignite(self._pack, self._projection, tick, ignition, actor)
        last_id = cause_id
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

    def _run_weather_follow_up(self, entry: Any) -> None:
        """A SEEDED weather erosion at its trigger tick (weather-1,
        TIME-1 — the fire follow-ups' shape): the drafts read the fold
        NOW (the state the world holds at fire time, never the state it
        held at seed time — the interim may have told this story
        already), one event per eroded entity, cause-chained to the
        seeding weather event. No matches -> nothing commits (the
        idempotence law: no no-op duplicates in the canon, KI#13's
        family)."""
        payload: WeatherPayload = entry.payload
        for draft in erosion_drafts(
            self._pack.rules, self._projection, entry.tick,
            payload.event_type, payload.cause_id,
        ):
            self._commit(replace(draft, provenance={"seed": self._seed}))

    # -- the iter-4 beat cycle (decay / urgencies / director releases) --------

    def _scene_zones(self) -> SceneZones | None:
        """The zone partition under an ARMED macro clock (depth-3, the
        scene LOD); None under the unarmed law — the one-scene world,
        the whole simulation per-beat (the v0.1 behavior, zero corpus
        price by construction — the 68a pattern). The partition is a
        pure fold view recomputed at each tick it scopes: the PC moves,
        the zones follow (the LOD tracks the reader)."""
        if self._next_macro is None:
            return None
        return scene_zones(self._pack, self._projection)

    def _first_beat(self, rules: Mapping[str, Any]) -> int | None:
        """The first beat tick strictly after 0 (the run-start tick). Beat
        offsets are pack-declared intraday ticks repeated daily, like
        watch rotations. None when the pack declares no beats (the
        urgencies/states/director stay silent — a degenerate config)."""
        offsets = sorted(rules.get("urgencies", {}).get("beat_ticks", ()))
        if not offsets:
            return None
        day = self._clock.ticks_per_day
        for offset in offsets:
            if offset > 0:
                return offset
        # all offsets are at 0 — the next beat is on day 1
        return day + offsets[0]

    def _next_beat_after(self, after: int) -> int | None:
        """The smallest beat tick strictly after `after`. Intraday offsets
        repeated daily; the rotation's `next_rotation_tick` arithmetic
        generalised — except the first beat may precede the first
        rotation (a tick-0 beat belongs to day 1)."""
        rules = self._pack.rules
        offsets = sorted(rules.get("urgencies", {}).get("beat_ticks", ()))
        if not offsets:
            return None
        day = self._clock.ticks_per_day
        day_idx = after // day
        candidates = sorted(
            d * day + offset
            for d in (day_idx, day_idx + 1)
            for offset in offsets
        )
        for candidate in candidates:
            if candidate > after:
                return candidate
        raise AssertionError("unreachable: next-day offsets always exceed `after`")

    def _condense_groups(self, zones: SceneZones, tick: int) -> None:
        """depth-7's tier-transition pass (one law, two ride points —
        the zone recomputations at the beats AND the crossings): the
        groups whose ANCHOR crossed into the warm ring or the active
        scene (the PC's approach; the partition follows the reader)
        and are not yet condensed materialize — ONE event per group
        carrying the un-born members' canon `member_of` births + the
        tombstone marker (`core/groups.py` owns the drafts; the
        materialization precedes every tick the members then ride —
        the beat machinery below, the warm ring's crossing cadence).
        name-1: the members' generated names materialize on the same
        event, drawn on their own `name:<npc>` family streams (the
        bank rides here for that alone — the tier half stays
        draw-free). Chained to the writer's last id (the
        chronological-chain law) and committed through the canon door
        (INV-1). The load state counts as the origin: a group
        warm/active at the FIRST computation condenses immediately —
        the PC walks into a materialized world (the DF precedent)."""
        for draft in condensation_drafts(
            self._bank, self._pack, self._projection, tick,
            locations=(*zones.warm, zones.active),
        ):
            self._commit(replace(
                draft, cause=self._writer.last_id,
                provenance={"seed": self._seed},
            ))

    def _run_beat(self, beat_tick: int, entry_tick: int) -> None:
        """One clock-crossing beat (iter-4): the depth-7 condensation
        pass (under an armed clock — the tier transitions detected at
        this zone computation materialize BEFORE the machinery the
        members then ride), states decay passes, NPC
        urgencies roll, faction goals roll (depth-6), and the director
        releases one seeded hook. Each piece rides the commit door —
        the world never changes outside an event (INV-1). Order
        matters: the condensation first (the members are canon before
        they tick), decay second (so the urgency sees the new
        status), urgencies third (so the director sees their effects
        in entropy), the director last.

        Decay events are committed at ``beat_tick`` (their canonical
        tick — the log records them at the beat). Urgency and director
        Intents are enqueued at ``entry_tick`` (the tick of the entry
        the loop is currently processing): the entry was already
        popped, and the queue discipline forbids enqueuing at a tick
        the clock has already passed (regression). The intents thus
        fire at the entry's tick — conceptually "after the beat, at
        the moment the world resumes moving"."""
        # depth-3 (the scene LOD): the beat's zone scoping — under an
        # armed macro clock the ACTIVE scene alone ticks per-beat (the
        # PC's location); the unarmed law keeps the whole world
        # per-beat (the one-scene world, the v0.1 bytes — the filter
        # is None). The DIRECTOR stays global either way: it is the
        # story layer (pack-authored hooks, budget 1 per beat), not
        # the ambient life the LOD throttles — its zone-scoping is
        # never the clock's consumer business.
        zones = self._scene_zones()
        locations: Collection[str] | None = (
            None if zones is None else (zones.active,)
        )
        # 0) depth-7 (the write-side LOD): the condensation pass —
        # under an armed clock the zone recomputation detects the
        # tier transitions FIRST (the members' canon births precede
        # the beat machinery they then ride); the unarmed law has no
        # tiers at all (the one-scene world — no zones, no
        # condensation, the v0.1 bytes).
        if zones is not None:
            self._condense_groups(zones, beat_tick)
        # 1) states decay — every NPC whose status.* deltas are non-zero
        for draft in decay_drafts(
            self._pack, self._projection, self._last_change, beat_tick,
            locations=locations,
        ):
            self._commit(replace(
                draft, cause=self._writer.last_id,
                provenance={"seed": self._seed},
            ))
        # 2) NPC urgencies — small-formula goal rolls through the intent door;
        # the derived folds read at the BEAT tick ride the gates (a
        # leverage-gated urgency stays silent until the holder actually
        # holds a live cluster — iter-45; an echo-gated one until the
        # residue clears the bar — iter-46; a trait-gated one until the
        # belief crystallizes — iter-67, beliefwire; the front door
        # re-validates at the entry tick with its own reads)
        self._director.next_beat()
        beat_echoes = echo_scores(self._pack, self._knowledge, beat_tick)
        for intent in urgency_intents(
            self._pack, self._projection, self._bank,
            facts=live_leverage(self._pack, self._events, beat_tick),
            echoes=beat_echoes,
            traits=crystallized_traits(self._pack, self._knowledge, beat_tick),
            locations=locations,
        ):
            self._enqueue_autonomous(intent, entry_tick)
        # 2b) faction goals (depth-6) — the small-formula dynamics at
        # the urgencies' own cadence: the KeeperRL ratio+threshold bar
        # computed from the LIVE fold (per-member status axes, D-006),
        # rolled on the entry's own faction-family stream, through the
        # SAME front door (D-112's one id: the group entity IS the
        # actor). The LOD filter scopes by the faction's ANCHOR
        # position; the collective after the individual (construction
        # order — INV-2).
        for intent in faction_intents(
            self._pack, self._projection, self._bank,
            facts=live_leverage(self._pack, self._events, beat_tick),
            echoes=beat_echoes,
            traits=crystallized_traits(self._pack, self._knowledge, beat_tick),
            locations=locations,
        ):
            self._enqueue_autonomous(intent, entry_tick)
        # 3) director releases — explicit triggers + stagnation; budget 1
        for intent in self._director.releases(self._projection, beat_tick):
            self._enqueue_autonomous(intent, entry_tick)

    def _enqueue_autonomous(self, intent: IntentData, tick: int) -> None:
        """Enqueue a director or urgency Intent through the same door as a
        playscript step — band NPC_REACTION (after the player's intents
        in the same tick) and stamped with the current event_count so
        OCC re-checks against the live projection. The intent fires at
        the tick passed by the caller — for beat-born intents that is
        the popped entry's tick, never the beat tick itself (the queue
        discipline forbids enqueuing at a tick the clock has already
        passed; the `_run_beat` docstring owns the rationale). The
        queue's (tick, sub_order) ordering puts it AFTER same-tick
        system passes (0..99) and player intents (100..199), BEFORE
        scheduled completions (300+)."""
        stamped = IntentData(
            id=intent.id, kind=intent.kind, actor=intent.actor,
            target=intent.target, fields=dict(intent.fields),
            based_on_event_seq=self._writer.event_count,
            origin_hook=intent.origin_hook,
        )
        self._queue.push(
            tick=tick, sub_order=NPC_REACTION, actor_id=intent.actor,
            kind="intent", payload=stamped,
        )

    def _run_macro(self, tick: int, entry_tick: int) -> None:
        """One macro-clock crossing (maclock-1, L4; depth-3's consumer,
        the scene LOD's warm ring): the year turns — ONE event through
        the canon door, cause-chained to the writer's last id (the
        chronological-chain law, the rotation's scheduled-beat
        precedent) — and the turn now carries the COLD CENSUS (the
        D-112 cardinality shape: the cold background's NPC population
        as one flat count, its only representation in the log — counts
        for populations, events for notables). The WARM RING ticks
        here (the scheduler rule: the crossings are the warm cadence —
        the active zone keeps the beats): the warm NPCs' decay drafts
        commit at the crossing tick chained AFTER the turn (the clock's
        own event opens its crossing; the consumer rides it), and
        their urgency entries roll at the crossing tick (the gates'
        fold reads at this tick — the beat's own law) enqueued at the
        ENTRY tick (the queue discipline: never a tick the clock has
        passed). depth-6: the warm ring's FACTION goals ride the same
        crossings (the small formula over the members' live axes, the
        anchor scoping the ring; the cold zone's factions stay silent —
        their population-scale representation is depth-7's aggregate
        machinery). No knowledge on the turn (a world event), no
        state_changes (the year and the census are derived, L3), no
        hooks (the director boundary is the consumers' own rows,
        never the clock's); importance rides the pack's own rule (the
        story-critical listing decides tale visibility — the tune-1
        split). depth-7: the write-side LOD rides the crossing in
        order — the CONDENSATIONS first (the groups whose anchor
        crossed into the warm ring or the active scene birth their
        members' canon `member_of`, the materialization preceding
        every warm tick the members then ride), then the COLD
        background's MACRO-TICK AGGREGATES (one cardinality event per
        cold uncondensed group, actor = the group id, chained to the
        turn — the population tier's only per-group representation;
        the tombstone silences a condensed group's ticks for good);
        both draw-free (the counts and the births are pure fold
        reads, the fingerprint never sees a tier event)."""
        zones = scene_zones(self._pack, self._projection)
        draft = macro_turn_draft(
            self._pack.rules, tick,
            counts={
                COLD_COUNT_KEY: npc_population(
                    self._pack, self._projection, zones.cold
                )
            },
        )
        self._commit(
            replace(
                draft,
                cause=self._writer.last_id,
                provenance={"seed": self._seed},
            )
        )
        # weather-1: the ambient family rides the crossing — the chain
        # rolls its next state from the fold's current weather, and a
        # CHANGE commits ONE event chained to the turn (the drift's
        # precedent: the consumer rides the clock's own event); the new
        # state's erosion follow-ups seed HERE (the fire follow-ups'
        # shape — SEEDED at event time, SCHEDULED on the queue, the
        # drafts read the fold at fire time). The draw rides the
        # family's own isolated stream (`weather:chain`, the D-079
        # law's seventh member) — the substantive fingerprint never
        # sees a weather roll. The unarmed law: no `weather` block, no
        # branch (the macro clock may run without the family).
        if self._pack.rules.get("weather") is not None:
            weather_draft = weather_turn_draft(
                self._pack.rules, self._bank, tick,
                current_weather(self._pack.rules, self._events),
            )
            if weather_draft is not None:
                weather_record = self._commit(
                    replace(
                        weather_draft,
                        cause=self._writer.last_id,
                        provenance={"seed": self._seed},
                    )
                )
                for spec in erosion_specs(
                    self._pack.rules,
                    str(weather_record.outcome["weather"]),
                ):
                    # the never-regress law (the queue discipline the
                    # warm ring's intents already ride): a crossing that
                    # fires LATE — a batch of missed crossings before a
                    # far entry — seeds its follow-ups no earlier than
                    # the world's resumed tick (the clock jumps to the
                    # entry's tick after the batch; a tick behind it
                    # would be a clock regression at pop). The deferral
                    # bends, the ORDER never does.
                    self._queue.push(
                        tick=max(tick + spec.at_tick, entry_tick),
                        sub_order=SCHEDULED,
                        actor_id=f"weather:{spec.event_type}",
                        kind="weather",
                        payload=WeatherPayload(
                            event_type=spec.event_type,
                            cause_id=weather_record.id,
                        ),
                    )
        # depth-7 (the write-side LOD): the tier transitions first —
        # the condensations ride the crossing's own event, before the
        # warm ring's machinery (the members materialize, then stir)
        self._condense_groups(zones, tick)
        # depth-7: the cold background's macro-tick aggregates — one
        # cardinality event per cold uncondensed group, chained to the
        # turn (the consumer rides the clock's own event, the drift's
        # precedent); the tombstone gates a realized group silent
        for tick_draft in macro_tick_drafts(
            self._pack, self._projection, tick, locations=zones.cold,
        ):
            self._commit(
                replace(
                    tick_draft, cause=self._writer.last_id,
                    provenance={"seed": self._seed},
                )
            )
        # the warm ring's status drift, chained to the turn (the
        # consumer rides the clock's own event)
        for drift in decay_drafts(
            self._pack, self._projection, self._last_change, tick,
            locations=zones.warm,
        ):
            self._commit(
                replace(
                    drift, cause=self._writer.last_id,
                    provenance={"seed": self._seed},
                )
            )
        # the warm ring's goal rolls — the gates read at the crossing
        # tick (the beat's own law), the intents enqueue at the entry
        # tick (the never-regress law)
        for intent in urgency_intents(
            self._pack, self._projection, self._bank,
            facts=live_leverage(self._pack, self._events, tick),
            echoes=echo_scores(self._pack, self._knowledge, tick),
            traits=crystallized_traits(self._pack, self._knowledge, tick),
            locations=zones.warm,
        ):
            self._enqueue_autonomous(intent, entry_tick)
        # the warm ring's FACTION goals (depth-6) — the same clock's
        # crossings, the same door: a faction anchored in the warm ring
        # rolls its small formula here (the beat machinery minus the
        # director, exactly as the warm NPCs above; the cold zone's
        # factions are silent — their population-scale ride is depth-7's
        # aggregate machinery, never this walk's)
        for intent in faction_intents(
            self._pack, self._projection, self._bank,
            facts=live_leverage(self._pack, self._events, tick),
            echoes=echo_scores(self._pack, self._knowledge, tick),
            traits=crystallized_traits(self._pack, self._knowledge, tick),
            locations=zones.warm,
        ):
            self._enqueue_autonomous(intent, entry_tick)

    def _run_rotation(self, tick: int) -> None:
        """One watch rotation at a crossed tick (phase0 §3): the post swap
        (positions), the expectation checks (P2d — violations chain to the
        events that moved the items), then the briefing (D-006 — the
        outgoing holder's records pass, one fidelity step down). Each piece
        commits through the canon door, so its reactions cascade."""
        rotation = self._pack.rules["crime_watch"]["rotation"]
        changes, outgoing, incoming = rotation_plan(self._pack, self._projection)
        # KI#19: the pack's `reset_on_rotation` status axes reset for the
        # participants on the same watch_change event — one committer, one
        # cause chain ("the relief wakes fresh").
        changes = changes + rotation_resets(
            self._pack, self._projection, rotation["participants"]
        )
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
                    event_type=rotation["watch_event"],
                ),
                provenance={"seed": self._seed},
            )
        )
        for draft in expectation_drafts(
            self._pack, self._projection, self._knowledge, self._events, tick
        ):
            self._commit(replace(draft, provenance={"seed": self._seed}))
        briefing = briefing_draft(
            self._pack, self._knowledge, tick,
            watch_record.id, outgoing, incoming,
        )
        if briefing is not None:
            self._commit(replace(briefing, provenance={"seed": self._seed}))

    def _react(self, record: EventRecord) -> None:
        """Event-driven system reactions (phase0 §3), dispatched from the
        canon door so no call site can forget them: crime first (suspicion,
        status flip, arrest — chained per knower), then the arrest
        resolution (iter-4: capture/escape on the attempt), then the
        telling (the conversation's teller shares their most salient novel
        fact), then the pack's on_action reactions (drama-3 — appended,
        never overwriting the systems), then the director buffer seeding.
        iter-4 also seeds the director's buffer (D-005: every hook
        is seeded at event time, never invented later)."""
        for group in iter_suspicion_reactions(
            self._pack, self._projection, self._knowledge, record
        ):
            previous = record.id
            for draft in group:
                committed = self._commit(
                    replace(draft, cause=previous, provenance={"seed": self._seed})
                )
                previous = committed.id
        # iter-4: arrest resolution rides the same commit-door discipline
        # as the rest of the reactions (D-037) — the attempt is a fact,
        # the resolution is its completion.
        arrest = self._pack.rules["crime_watch"]["arrest"].get("event")
        if record.type == arrest:
            resolution = arrest_resolution_draft(
                self._pack, self._projection, self._bank, record
            )
            if resolution is not None:
                self._commit(
                    replace(resolution, provenance={"seed": self._seed})
                )
        telling = telling_reaction(
            self._pack, self._projection, self._knowledge, self._bank, record
        )
        if telling is not None:
            self._commit(
                replace(
                    telling, cause=record.id, provenance={"seed": self._seed}
                )
            )
        # drama-3 (iter-42): the pack's on_action reactions, appended
        # AFTER the hardcoded systems (the donor's append-not-overwrite
        # composition — vanilla logic runs, custom entries add, never
        # replace) and BEFORE the director seeding. Lazy on purpose:
        # each entry's draft reads the projection as left by the
        # previously committed reactions (the KI#13 discipline).
        for draft in on_action_drafts(self._pack, self._projection, record):
            self._commit(
                replace(draft, cause=record.id, provenance={"seed": self._seed})
            )
        # social-1 (iter-44, P3a): the secrets reaction — a novel knower
        # of a pack-declared secret mints the leverage fact cluster (the
        # CK3 add_hook precedent: a hook IS an event). Appended after the
        # on_action dispatch (the same append composition), before the
        # director seeding; the drafts carry no knowledge and no hooks,
        # so the cascade terminates by construction (the one-hop law's
        # sibling) and the director buffer is untouched (L6).
        for draft in leverage_drafts(self._pack, self._knowledge, record):
            self._commit(
                replace(draft, cause=record.id, provenance={"seed": self._seed})
            )
        # leg-3 (iter-57): reflection-on-recurrence — the memory
        # compaction mint (Generative Agents' reflection, event-sourced:
        # the higher-level entry is itself an event, originals never
        # dropped — INV-1; never letta's in-place summarization). A
        # knower whose family records reach the pack's recurrence
        # threshold mints ONE reflection event per (knower, insight) per
        # run (the never-re-reflect gate rides the live view). Appended
        # after the leverage reaction (the same append composition),
        # before the director seeding; the drafts carry no hooks and no
        # state changes, so the cascade terminates by construction and
        # the entropy is untouched (L6 — a reflection is knowledge-side
        # canon, never an entropy input).
        for draft in reflection_drafts(self._pack, self._knowledge, record):
            self._commit(
                replace(draft, cause=record.id, provenance={"seed": self._seed})
            )
        # iter-4: the director seeds hooks at commit time (D-005). The
        # release decision fires later, at the beat cycle.
        self._director.seed(record)

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
            provenance=self._provenance(intent),
        )
        self._commit(draft)

    def _provenance(self, intent: IntentData) -> dict[str, Any]:
        """The intent-side provenance block: the run seed, the intent id,
        and — for a director-built intent — the discharged hook's tag
        (`cause_hook`, D-140): the release's causal provenance, pairing
        the event with the seeding event for payoff latency and the
        trace family. Rejections carry it too: a released attempt is a
        fact (the hook discharged, the budget was spent)."""
        provenance: dict[str, Any] = {
            "seed": self._seed,
            "cause_intent": intent.id,
        }
        if intent.origin_hook is not None:
            provenance["cause_hook"] = intent.origin_hook
        return provenance

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
        for change in record.state_changes:
            self._last_change[(change.entity, change.prop)] = record.t
        self._knowledge.add(record)  # derived index (L3)
        self._react(record)  # event-driven reactions (phase0 §3)
        return record
