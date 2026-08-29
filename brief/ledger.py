"""The session scene ledger — the texture stream (D-048/D-049; mechanism
owner `docs/blueprint/phases.md` §1; the block/window contract is
`docs/BRIEF_SPEC.md` §3.3, the protocol clauses `docs/VALIDATION_SPEC.md`
§8).

Canon vs texture: the narrator inevitably invents *texture* (candles, a
cloak on a chair) the log never knew. The ledger is a session-scoped,
append-only record of established texture — never folded into canonical
state, never committed, never replayed (the D-049 determinism quarantine:
canon replay T1/T2 never touches it; nondeterminism enters only at the
narrator call and is captured structurally once, then frozen). Its only
write path into canon is the intent door (promotion), never a direct one.

This module is the LLM-free half: the entry shape, the scene definition
(PC-location interval, derived by folding the log — zero new event types),
the discrete lifecycle, the structural-pinning + validation gateway, the
beat-pass contradiction retirement, scene-close retirement, and the
texture-OCC mirror. The live narrator call is the owner-gated boundary
(AGENTS §8); tests drive the gateway with fixture-shaped deltas. The
gateway is a pure function of (delta, events, pack) — no RNG, no
wall-clock, writes nothing to the log (INV-1/2/4).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any, Final

from core.fold import Projection, fold, initial_projection, present_entities
from core.log import EventRecord
from core.pack import Pack

# `present_entities` is re-exported from `core.fold` (st-1: the structural
# presence read moved beside its projection — core owns it; the write-side
# per-present-target `knows` expansion and this module's window law read
# the same single set).

__all__ = [
    "ACTIVE",
    "CONTRADICTED",
    "DeltaError",
    "DeltaReport",
    "ENTITY_SCOPE_PREFIX",
    "LedgerEntry",
    "LIVE_STATUSES",
    "PINNED",
    "PROMOTED",
    "REFUSAL_REASONS",
    "RETIRED",
    "Refusal",
    "SCENE_CLOSE_CAUSE",
    "SCENE_SCOPE_PREFIX",
    "Scene",
    "SceneLedger",
    "SceneSync",
    "TERMINAL_STATUSES",
    "check_delta_shape",
    "current_scene",
    "present_entities",
    "refusal_lines",
    "scenes",
    "split_scope",
]

# -- lifecycle vocabulary (blueprint §1: discrete states, no floats) ------------

ACTIVE: Final = "active"
PINNED: Final = "pinned"
RETIRED: Final = "retired"
CONTRADICTED: Final = "contradicted"
PROMOTED: Final = "promoted"

#: The live states — the only ones the brief window can show or pinning
#: can act on; `{active, pinned}` end in a terminal state, one-way.
LIVE_STATUSES: Final = (ACTIVE, PINNED)
#: Terminal states — no un-pinning, no resurrection (the trust-state law).
TERMINAL_STATUSES: Final = (RETIRED, CONTRADICTED, PROMOTED)

#: Scope prefixes — `scene:<location_id>` or `entity:<entity_id>`, FIXED at
#: establishment (scope-as-key; a revisit of the same location is a NEW
#: scene, scene-scoped texture starts empty, entity-scoped survives).
SCENE_SCOPE_PREFIX: Final = "scene:"
ENTITY_SCOPE_PREFIX: Final = "entity:"
#: The cause recorded for scene-close retirement (an event-caused recorded
#: decision — never a TTL timer).
SCENE_CLOSE_CAUSE: Final = "scene_close"

#: Closed gateway-refusal reason vocabulary — one per cause, never prose
#: (the same law as the validator's REASONS; VALIDATION_SPEC §4/§8).
REFUSAL_REASONS: Final = (
    "scope_target",    # malformed scope, or an id canon does not know
    "scene_mismatch",  # scene-scoped establishment outside the current scene
    "absent_entity",   # entity-scoped establishment for a non-present entity
    "canon_slot",      # the slot is canon-modeled on the scope target already
    "laundering",      # re-asserting a contradicted / promoted-away value
    "unique_slot",     # cross-scope re-establishment of a pack-unique slot
    "slot_conflict",   # same slot, different value, live in scope
    "stale_ref",       # a ref naming no live entry (retired/refuted/promoted)
)


class DeltaError(RuntimeError):
    """Delta-document shape violation: the emitter is the author, author
    bugs crash (the loud/soft front-door law; malformed LLM output is the
    boundary's degradation problem, handled BEFORE this gateway)."""


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    """One established texture fact (the blueprint §1 entry shape).

    `slot` + `value` are the normalized fact; `surface` is the verbatim
    prose that introduced it (evidence-before-belief); `source` cites the
    narration turn; `t` is stamped by the gateway from the log state the
    delta was applied against (derive-never-store, L3); `cause` records
    the terminal transition's reason — an event id, or `scene_close`.
    """

    id: str
    t: int
    scope: str
    slot: str
    value: str
    surface: str
    status: str
    cause: str | None
    source: str


@dataclass(frozen=True, slots=True)
class Scene:
    """One PC-location interval: opens at session start or PC arrival,
    closes when canon moves the PC. Identity `(location_id, ordinal)` —
    a revisit is a NEW scene. Read-side view state, never logged."""

    location_id: str
    ordinal: int
    from_tick: int
    to_tick: int | None  # None = still open (the current scene)


@dataclass(frozen=True, slots=True)
class Refusal:
    """One refused delta item: a dry item description + the closed reason
    (the §7 protocol's raw material — one refusal shape, one regen
    budget; VALIDATION_SPEC §8)."""

    item: str
    reason: str


@dataclass(frozen=True, slots=True)
class DeltaReport:
    """What one applied delta did: the entries established, the ids pinned
    and retired, the idempotent no-ops, and the refusals (which trigger
    the regen protocol — the caller owns the budget)."""

    established: tuple[LedgerEntry, ...]
    pinned: tuple[str, ...]
    retired: tuple[LedgerEntry, ...]
    no_ops: tuple[str, ...]
    refusals: tuple[Refusal, ...]

    @property
    def refused(self) -> bool:
        return bool(self.refusals)


def refusal_lines(report: DeltaReport) -> tuple[str, ...]:
    """Dry structured refusal lines riding the next narrator call's
    directives — the same protocol shape as the validator's refusal note
    (VALIDATION_SPEC §7/§8); the ledger prefix is `REFUSED` because these
    are gateway refusals, not claim verdicts."""
    return tuple(f"REFUSED {refusal.item} ({refusal.reason})" for refusal in report.refusals)


# -- scene derivation (PC-location interval; a pure fold of the log) ------------


def scenes(events: Sequence[EventRecord], pack: Pack) -> tuple[Scene, ...]:
    """Derive every scene from the log by watching the PC's `position`:

    the maximal session intervals over which the PC's location is
    constant (blueprint §1, D-049). Zero new event types — scene markers
    are read-side view state, never logged. A move event changing the
    PC's position closes the current scene at that event's tick and opens
    the next; a move to the same location keeps the scene (the interval
    stays maximal). The last scene is open (`to_tick=None`).
    """
    player = pack.player_id()
    location = str(pack.entity(player)["position"])
    closed_counts: dict[str, int] = {}
    opened_at = 0
    out: list[Scene] = []
    for event in events:
        for change in event.state_changes:
            if change.entity != player or change.prop != "position":
                continue
            if change.to_ == location:
                continue  # location constant: the interval stays maximal
            out.append(
                Scene(location, closed_counts.get(location, 0), opened_at, event.t)
            )
            closed_counts[location] = closed_counts.get(location, 0) + 1
            location = str(change.to_)
            opened_at = event.t
    out.append(Scene(location, closed_counts.get(location, 0), opened_at, None))
    return tuple(out)


def current_scene(events: Sequence[EventRecord], pack: Pack) -> Scene:
    """The open scene — the last PC-location interval (the scene the next
    narrator call renders)."""
    return scenes(events, pack)[-1]


def split_scope(scope: str) -> tuple[str, str] | None:
    """`scene:<id>` / `entity:<id>` into `(prefix, target_id)`, or None
    when malformed (the gateway's scope-shape test)."""
    if scope.startswith(SCENE_SCOPE_PREFIX):
        return SCENE_SCOPE_PREFIX, scope[len(SCENE_SCOPE_PREFIX):]
    if scope.startswith(ENTITY_SCOPE_PREFIX):
        return ENTITY_SCOPE_PREFIX, scope[len(ENTITY_SCOPE_PREFIX):]
    return None


# (present_entities lives in core.fold since st-1 — re-exported above;
# the window law below reads it through that import.)


# -- the ledger (session render state — auditable, never replayable) ------------


@dataclass(frozen=True, slots=True)
class SceneSync:
    """The outcome of one `sync_scene` call: the scene that closed (None
    on first adoption / no change) and the scene-scoped entries its close
    retired in bulk (cause `scene_close`)."""

    closed: Scene | None
    retired: tuple[LedgerEntry, ...]


class SceneLedger:
    """Session render state: the append-only entry list plus the scene it
    is synced to. Entries are never edited in place — an in-scene update
    is a retire + establish pair in one delta; status transitions replace
    the frozen entry instance at its index (ids never reuse, gap-free,
    allocation in append order — a counter, never a hash, INV-2). The
    ledger never evicts ANY entry (D-049): it only transitions them; all
    boundedness lives in the brief's window law."""

    def __init__(self) -> None:
        self._entries: list[LedgerEntry] = []
        self._scene: Scene | None = None  # the scene the ledger is synced to

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        """Every entry ever established, in append order (frozen data — a
        read-only snapshot for the assembler)."""
        return tuple(self._entries)

    @property
    def scene(self) -> Scene | None:
        """The scene this ledger is synced to (None before the first
        `sync_scene` — session start)."""
        return self._scene

    def live(self) -> tuple[LedgerEntry, ...]:
        """Active + pinned entries, construction order (the window law's
        candidate set before scope filtering)."""
        return tuple(e for e in self._entries if e.status in LIVE_STATUSES)

    def _replace_status(self, index: int, status: str, cause: str | None) -> LedgerEntry:
        entry = replace(self._entries[index], status=status, cause=cause)
        self._entries[index] = entry
        return entry

    def _live_by_selector(self, item: Mapping[str, Any]) -> LedgerEntry | None:
        if "id" in item:
            return next(
                (e for e in self._entries if e.id == item["id"] and e.status in LIVE_STATUSES),
                None,
            )
        return next(
            (
                e
                for e in self._entries
                if e.status in LIVE_STATUSES
                and e.scope == item["scope"]
                and e.slot == item["slot"]
            ),
            None,
        )

    # -- scene close (the bulk retirement of scene-scoped texture) -------------

    def close_scene(self, location_id: str) -> tuple[LedgerEntry, ...]:
        """Retire every live entry scoped `scene:<location_id>` in bulk
        (cause `scene_close`) — an event-caused recorded decision, not a
        TTL timer. Entity-scoped texture survives scene changes. Returns
        the retired entries in construction order."""
        retired: list[LedgerEntry] = []
        scope = f"{SCENE_SCOPE_PREFIX}{location_id}"
        for index, entry in enumerate(self._entries):
            if entry.scope == scope and entry.status in LIVE_STATUSES:
                retired.append(self._replace_status(index, RETIRED, SCENE_CLOSE_CAUSE))
        return tuple(retired)

    def sync_scene(self, events: Sequence[EventRecord], pack: Pack) -> SceneSync:
        """Sync the ledger to the log's current scene: adopt it on first
        call (session start — nothing to retire), and on every later
        identity change `(location, ordinal)` close the previous scene
        (retiring its scene-scoped texture — a revisit starts empty) and
        adopt the new one. The mediator runs this after commits, BEFORE
        the next narrator call."""
        scene = current_scene(events, pack)
        if self._scene is not None and (
            self._scene.location_id, self._scene.ordinal
        ) == (scene.location_id, scene.ordinal):
            return SceneSync(None, ())
        closed: Scene | None = None
        retired: tuple[LedgerEntry, ...] = ()
        if self._scene is not None:
            closed = self._scene
            retired = self.close_scene(self._scene.location_id)
        self._scene = scene
        return SceneSync(closed=closed, retired=retired)

    # -- the beat pass (canon always outranks texture) --------------------------

    def retire_contradicted(
        self, window_events: Sequence[EventRecord]
    ) -> tuple[LedgerEntry, ...]:
        """Cross-check live entries against the beat's new canon delta and
        retire overlaps as `contradicted`, cause-linked to the FIRST event
        that modeled the prop (blueprint §1). STRUCTURAL only — slot/prop
        overlap on the scope target; semantic invalidation is narrator
        retirement or a validator catch, never mediator guessing."""
        retired: list[LedgerEntry] = []
        for event in window_events:  # log order: first break wins the cause
            touched = {
                (change.entity, change.prop) for change in event.state_changes
            }
            if not touched:
                continue
            for index, entry in enumerate(self._entries):
                if entry.status not in LIVE_STATUSES:
                    continue
                split = split_scope(entry.scope)
                target = split[1] if split is not None else entry.scope
                if (target, entry.slot) in touched:
                    retired.append(self._replace_status(index, CONTRADICTED, event.id))
        return tuple(retired)

    # -- promotion + the texture-OCC mirror (protocol: VALIDATION_SPEC §8) ------

    def mark_promoted(self, entry_id: str, cause_event_id: str) -> LedgerEntry:
        """Flip a live entry to `promoted` (cause: the committed event) —
        the mediator observes the committed promotion event and records
        it; the committed event IS the promotion (canon birth). One-way:
        only a live entry can promote; anything else is a mediator bug
        and crashes loudly (the withdrawal mirror should have removed the
        pending intent first)."""
        if not isinstance(cause_event_id, str) or not cause_event_id.strip():
            raise DeltaError(f"promotion cause must be an event id, got {cause_event_id!r}")
        for index, entry in enumerate(self._entries):
            if entry.id != entry_id:
                continue
            if entry.status not in LIVE_STATUSES:
                raise DeltaError(
                    f"{entry_id}: only a live entry can be promoted "
                    f"(status {entry.status!r})"
                )
            return self._replace_status(index, PROMOTED, cause_event_id)
        raise DeltaError(f"{entry_id}: no such ledger entry")

    def withdrawals(self, pending: Mapping[str, str]) -> tuple[str, ...]:
        """The texture-OCC mirror: of `pending` (intent id → texture entry
        id), return the intent ids to WITHDRAW — every one whose entry is
        not live (retired, contradicted, promoted, unknown). Withdrawal
        happens BEFORE the door could complete the intent and is not an
        event: the attempt never reached the world (VALIDATION_SPEC §8).
        Construction order, like every ledger iteration."""
        by_id = {entry.id: entry for entry in self._entries}
        out: list[str] = []
        for intent_id, entry_id in pending.items():
            entry = by_id.get(entry_id)
            if entry is None or entry.status not in LIVE_STATUSES:
                out.append(intent_id)
        return tuple(out)

    # -- the validation gateway (ONE gateway — blueprint §1, D-049) -------------

    def apply_delta(
        self, delta: Mapping[str, Any], events: Sequence[EventRecord], pack: Pack
    ) -> DeltaReport:
        """Apply one narrator texture delta through the validation gateway
        (inline deltas and extraction output pass the SAME checks — the
        governed write gateway). The call first syncs the ledger to the
        log's current scene (`sync_scene` — idempotent), so no call site
        can forget the sync and leak scene-scoped texture past a close
        (the D-037 discipline); the mediator's own beat order stays
        `commit → retire_contradicted(window) → assemble → narrator →
        apply_delta`. Processing order within the delta is
        `retired → established → refs`, so an in-scene update is one
        retire + establish pair. The establishment checks, in order:
        scope shape/target, scene match or entity presence, the
        idempotent duplicate rule, laundering, the pack unique-slot flag,
        establishment-time canon overlap, and the live slot-conflict
        rule. Refusals are recorded, never raised — they ride the next
        call's directives and trigger the regen protocol (§7). `t` is
        stamped from the log state (L3), never taken from the delta.
        """
        source, raw_established, raw_retired, raw_refs = _delta_shape(delta)
        self.sync_scene(events, pack)
        state = fold(events, initial_projection(pack.entities))
        scene = current_scene(events, pack)
        tick = events[-1].t if events else 0

        retired: list[LedgerEntry] = []
        no_ops: list[str] = []
        for item in raw_retired:
            entry = self._live_by_selector(item)
            if entry is None:
                no_ops.append(f"retire {_selector_name(item)}: not live")
            else:
                index = self._entries.index(entry)
                retired.append(self._replace_status(index, RETIRED, source))

        established: list[LedgerEntry] = []
        refusals: list[Refusal] = []
        unique_slots = frozenset(pack.rules["brief"]["scene_texture"]["unique_slots"])
        for item in raw_established:
            outcome = self._establish(
                item, pack=pack, state=state, scene=scene,
                tick=tick, source=source, unique_slots=unique_slots,
            )
            if isinstance(outcome, LedgerEntry):
                self._entries.append(outcome)
                established.append(outcome)
            elif isinstance(outcome, Refusal):
                refusals.append(outcome)
            else:
                no_ops.append(outcome)

        pinned: list[str] = []
        for item in raw_refs:
            entry = self._live_by_selector(item)
            if entry is None:
                refusals.append(Refusal(f"ref {_selector_name(item)}", "stale_ref"))
            elif entry.status == PINNED:
                no_ops.append(f"ref {entry.id}: already pinned")
            else:
                index = self._entries.index(entry)
                self._replace_status(index, PINNED, None)
                pinned.append(entry.id)

        return DeltaReport(
            established=tuple(established),
            pinned=tuple(pinned),
            retired=tuple(retired),
            no_ops=tuple(no_ops),
            refusals=tuple(refusals),
        )

    def _establish(
        self,
        item: Mapping[str, Any],
        *,
        pack: Pack,
        state: Projection,
        scene: Scene,
        tick: int,
        source: str,
        unique_slots: frozenset[str],
    ) -> LedgerEntry | Refusal | str:
        """Run the gateway checks for one establishment; returns the new
        entry, a Refusal, or a no-op description string (the idempotent
        duplicate rule)."""
        scope, slot, value = item["scope"], item["slot"], item["value"]
        split = split_scope(scope)
        if split is None or pack.kind_of(split[1]) is None:
            return Refusal(f"establish {scope}.{slot} = {value}", "scope_target")
        prefix, target = split
        if prefix == SCENE_SCOPE_PREFIX:
            if target != scene.location_id:
                return Refusal(
                    f"establish {scope}.{slot} = {value}", "scene_mismatch"
                )
        else:
            if pack.kind_of(target) == "location":
                return Refusal(f"establish {scope}.{slot} = {value}", "scope_target")
            if target not in present_entities(state, scene.location_id, pack):
                return Refusal(f"establish {scope}.{slot} = {value}", "absent_entity")

        for entry in self._entries:
            if entry.scope != scope or entry.slot != slot or entry.value != value:
                continue
            if entry.status in LIVE_STATUSES:
                return f"establish {scope}.{slot} = {value}: duplicate"  # no-op
            if entry.status in (CONTRADICTED, PROMOTED):
                return Refusal(
                    f"establish {scope}.{slot} = {value}", "laundering"
                )  # re-asserted refuted/promoted-away value

        if slot in unique_slots:
            # The claim is held by every status except retirement: live
            # texture, promoted (the object is canon now), contradicted
            # (canon overrode the slot — the object exists as canon). Only
            # a narrator-declared retirement releases the claim (the slot
            # denotes one object, not one lifetime).
            for entry in self._entries:
                if (
                    entry.slot == slot
                    and entry.scope != scope
                    and entry.status != RETIRED
                ):
                    return Refusal(
                        f"establish {scope}.{slot} = {value}", "unique_slot"
                    )

        # Canon overlap is BOTH prop sources: the folded runtime projection
        # (event-born props, incl. promotions) and the pack-modeled fields
        # (exits, fire_spots, name, mood, …) — "texture occupies only slots
        # canon does not model" (blueprint §1) reads canon as the whole
        # entity record, not just the event-derived half.
        if slot in state.get(target, {}) or slot in pack.entity(target):
            return Refusal(f"establish {scope}.{slot} = {value}", "canon_slot")

        for entry in self._entries:
            if (
                entry.scope == scope
                and entry.slot == slot
                and entry.status in LIVE_STATUSES
                and entry.value != value
            ):
                return Refusal(f"establish {scope}.{slot} = {value}", "slot_conflict")

        return LedgerEntry(
            id=f"tex_{len(self._entries):04d}",
            t=tick,
            scope=scope,
            slot=slot,
            value=value,
            surface=item["surface"],
            status=ACTIVE,
            cause=None,
            source=source,
        )


# -- the delta document boundary (loud shape gate — D-018's sibling law) --------


def check_delta_shape(delta: Mapping[str, Any]) -> None:
    """The delta document's shape gate, boundary-side (`brief/mediator.py`
    runs it BEFORE the gateway so a malformed document never reaches
    `apply_delta` — the degradation ladder's problem, never the gateway's;
    VALIDATION_SPEC §2/§7.1). Loud `DeltaError` on any drift; silent when
    the document is well-shaped."""
    _delta_shape(delta)


def _selector_name(item: Mapping[str, Any]) -> str:
    if "id" in item:
        return str(item["id"])
    return f"{item['scope']}.{item['slot']}"


def _non_empty(value: Any, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeltaError(f"{what} must be a non-empty string, got {value!r}")
    return value


def _selector(item: Any, what: str) -> Mapping[str, Any]:
    """A retire/ref selector: exactly `id`, or exactly `scope`+`slot`."""
    doc = _mapping(item, what)
    keys = set(doc)
    if keys not in ({"id"}, {"scope", "slot"}):
        raise DeltaError(
            f"{what}: must be exactly {{'id'}} or {{'scope', 'slot'}}, got {sorted(keys)}"
        )
    if "id" in doc:
        _non_empty(doc["id"], f"{what} id")
    else:
        _non_empty(doc["scope"], f"{what} scope")
        _non_empty(doc["slot"], f"{what} slot")
    return doc


def _mapping(data: Any, what: str) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise DeltaError(f"{what} must be an object, got {type(data).__name__}")
    return data


def _delta_shape(
    delta: Mapping[str, Any],
) -> tuple[str, list[Mapping[str, Any]], list[Mapping[str, Any]], list[Mapping[str, Any]]]:
    """The loud shape gate: the delta document is closed, like the
    validator's proposal document (VALIDATION_SPEC §2/§3 — the emitter is
    the author, author bugs crash; there is no prose field to sanitize)."""
    doc = _mapping(delta, "delta")
    allowed = {"source", "established", "retired", "refs"}
    unknown = [key for key in doc if key not in allowed]
    if unknown:
        raise DeltaError(f"delta: unknown keys {sorted(unknown)} — the document is closed")
    for key in ("established", "retired", "refs"):
        if key in doc and not isinstance(doc[key], list):
            raise DeltaError(f"delta {key} must be a list, got {type(doc[key]).__name__}")
    source = _non_empty(doc.get("source"), "delta source")
    established: list[Mapping[str, Any]] = []
    for raw in doc.get("established", ()):
        item = _mapping(raw, "established item")
        missing = {"scope", "slot", "value", "surface"} - set(item)
        if missing:
            raise DeltaError(f"established item: missing required keys {sorted(missing)}")
        unknown_keys = [key for key in item if key not in {"scope", "slot", "value", "surface"}]
        if unknown_keys:
            raise DeltaError(
                f"established item: unknown keys {sorted(unknown_keys)} — closed document"
            )
        for key in ("scope", "slot", "value", "surface"):
            _non_empty(item[key], f"established item {key}")
        established.append(item)
    retired = [_selector(raw, "retired item") for raw in doc.get("retired", ())]
    refs = [_selector(raw, "ref item") for raw in doc.get("refs", ())]
    return source, established, retired, refs
