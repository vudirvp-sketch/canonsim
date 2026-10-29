"""Factions with goals (depth-6, phases.md §5 P3b — the TASKS row
`depth-6`): SMALL-FORMULA DYNAMICS, the KeeperRL rebellion precedent
(`docs/ref/keeperrl.md` — `getRebellionProbability`: a ratio and a
threshold, never a psychology engine). A faction is a GROUP ENTITY
(`entities.json::groups` — D-112's "one id, all tiers": kind `group`,
a pack entity acting through the SAME intent door as the NPCs, actor =
the entity id; the projection seeds its anchor `position`) whose goal
fires through the door when its membership's own per-entity axes cross
a pack-declared bar. D-006 holds — axes are PER-ENTITY data: the
formula reads each member's `status.<axis>` from the LIVE fold, never
a stored group score (no group reputation; the ratio is derived at
roll time, L3, and recorded only through the events the door emits).

The formula (pure integer arithmetic, INV-2-clean — the KeeperRL
shape, per-cent):

    affected  = |{m in members : value(m) >= trigger_value}|
    fraction  = affected * 100 // total          (floor)
    p         = 0                                  if fraction <= threshold
              = min(max_per_beat,
                    (fraction - threshold) * max_per_beat // (100 - threshold))

The deadband (fraction at-or-below the bar never fires) makes the
probability form churn-free by construction — no state flips, so no
hysteresis is owed (the D-105 intake-4 deadband law's spirit, one less
knob). A member with no value on the axis sits the ratio out (the
decay pass's read family: "NPC has no value on this axis"); a
memberless or valueless faction never fires (the vacuity law — the
dead-data floor, pinned by test).

The roll: d100 on the entry's OWN stream `faction:<group>:<kind>`
(`core/rng.py` — the D-079 family's fifth member, engine-2's
per-entry isolation), ONE draw per walk per entry (the cadence law —
the stream advances uniformly like the urgency family's; the formula
only shapes the comparison bar). On a hit the intent enqueues through
the front door (D-037/D-039: band NPC_REACTION at the entry tick, the
same OCC/resolver pipeline as the player's steps — the world's logic
is one mechanism, never two).

The cadence + the scene LOD (depth-3's one-gate law): the walk rides
the same clock crossings as the NPC urgencies — per-beat under the
unarmed macro clock (the one-scene world, `locations=None`), the
ACTIVE zone's beats + the WARM ring's crossings under an armed one;
the faction's ANCHOR position scopes it (the zones follow the reader).
The cold zone's factions are silent — their population-scale
representation (the D-112 aggregate macro-ticks, condensation) is
depth-7's row, never this one's.

Pack vocabulary (both optional — the unarmed law, the 68a pattern:
the committed pack declares neither; zero entries, zero draws, the
v0.1 bytes untouched; the arming rides with a future content row):

- `entities.json::groups` — `{id, name?, position, members, notes?}`;
- `rules.json::factions` — entries `{group, axis, trigger_value,
  threshold, max_per_beat, intent{kind,target?,fields?}, requires?,
  notes?}` (closed vocabulary, pack-linted).

Determinism (INV-2): pack declaration order everywhere — the entries
walk in the pack's own order, the members read in the group's own
order; never a set iteration.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.intent import (
    WINDOWED_TESTS,
    IntentData,
    ScanGateFold,
    ScanGateMemo,
    first_failing,
    pair_values,
    precondition_read_pairs,
)
from core.rng import faction_stream_name

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.rng import RngBank
    from core.worldgen import WorldModel

__all__ = [
    "FACTION_PREFIX",
    "faction_bar",
    "faction_intents",
    "faction_probability",
    "faction_rolls",
    "faction_scan",
    "faction_specs",
]

FACTION_PREFIX: Final = "faction"  # intent ids (faction_<group>_<kind>)


@dataclass(frozen=True, slots=True)
class _FactionSpec:
    """One pack-declared faction goal (rules.json `factions.entries`).

    - `axis` + `trigger_value`: a member counts as affected when their
      `status.<axis>` is at least `trigger_value` (per-entity data,
      D-006 — read from the live fold at the roll tick).
    - `threshold` (0..99, per-cent of the membership): the affected
      fraction must EXCEED it before the goal can fire (the deadband).
    - `max_per_beat` (1..100): the probability at a fully affected
      membership — the ramp's endpoint, the pack's own ceiling.
    - `intent` / `requires`: the goal's IntentData template and
      optional precondition gates (the closed test set, the urgency
      family's own discipline: a hit that fails the gates stays
      silent).
    - `pairs` (iter-375, the gate-answer memo): the DECLARED READ SET
      of the entry's `requires` (`precondition_read_pairs` — the occ-1
      read-pairs twin, sorted at parse), or None when the entry is
      ungated OR any require reads a time-dependent fold (the windowed
      family — the urgency twin's own law; the scans stay exact under
      any caller: never memoized, always evaluated fresh).
    """

    group: str
    axis: str
    trigger_value: int
    threshold: int
    max_per_beat: int
    intent_kind: str
    intent_target: str | None
    intent_fields: Mapping[str, Any]
    requires: tuple[Mapping[str, Any], ...]
    members: tuple[str, ...]
    stream: str
    probe: IntentData
    pairs: tuple[tuple[str, str], ...] | None


def _specs(pack: "Pack") -> tuple[_FactionSpec, ...]:
    """Parse the pack's `factions.entries` (load order: pack-declared;
    the walk respects it as given — INV-2 via construction order). The
    members ride the GROUP entity's own declaration order (the group
    record is the membership's single pack-side owner; the runtime
    `member_of` state door is depth-7's row, never this walk's). The
    parse also builds each entry's STREAM name and gate PROBE (iter-370,
    the static-resolution family — the urgency twin's own form): both
    are pure functions of the entry, so the parse-once memo carries
    them and the per-beat walks never re-derive."""
    config = pack.rules.get("factions")
    if config is None:
        return ()
    groups = {
        record["id"]: record
        for record in pack.entities.get("groups", ())
    }
    specs: list[_FactionSpec] = []
    for entry in config.get("entries", ()):
        group = groups[entry["group"]]
        intent_kind = entry["intent"]["kind"]
        target = entry["intent"].get("target")
        fields = dict(entry["intent"].get("fields", {}))
        requires = tuple(entry.get("requires", ()))
        probe = IntentData(
            # probeids-1 (iter-436): the entry's declared identity, never its
            # ordinal — the goal stream's own address
            # (`faction:<group>:<kind>`) in id form. Unique per probe by the
            # pack-linted (group, kind) pair the stream rides
            # (`core/packlint/actors.py::_factions`); repeats keep it.
            id=f"{FACTION_PREFIX}_{entry['group']}_{intent_kind}",
            kind=intent_kind,
            actor=entry["group"],  # D-112: the group IS the actor
            target=target,
            fields=fields,
            based_on_event_seq=0,
        )
        specs.append(
            _FactionSpec(
                group=entry["group"],
                axis=entry["axis"],
                trigger_value=int(entry["trigger_value"]),
                threshold=int(entry["threshold"]),
                max_per_beat=int(entry["max_per_beat"]),
                intent_kind=intent_kind,
                intent_target=target,
                intent_fields=fields,
                requires=requires,
                members=tuple(group.get("members", ())),
                stream=faction_stream_name(entry["group"], intent_kind),
                probe=probe,
                pairs=(
                    tuple(sorted(precondition_read_pairs(pack, probe, requires)))
                    if requires
                    and not any(
                        cond.get("test") in WINDOWED_TESTS for cond in requires
                    )
                    else None
                ),
            )
        )
    return tuple(specs)


def faction_specs(pack: "Pack") -> tuple[_FactionSpec, ...]:
    """The parse-once accessor (scale-1-impl, P0.5-B — the E03 fix):
    the same pure parse `_specs` owns, named for the LOOP's init-time
    memo — the per-beat re-parse was the measured E03 waste (one
    urgency + one faction parse per beat, 2.0/beat at iter-328, the
    faction arm firing even on packs without the block); pure over
    immutable pack data, so the memo is byte-identical by
    construction."""
    return _specs(pack)


def faction_probability(
    values: Sequence[int],
    trigger_value: int,
    threshold: int,
    max_per_beat: int,
) -> int:
    """The KeeperRL small formula over one membership's live axis
    values: the affected fraction (per-cent, floored) against the
    threshold, ramping linearly to `max_per_beat` at a fully affected
    membership. Zero on the deadband (fraction at-or-below the bar)
    and on the vacuity law (no values — a memberless or valueless
    faction never acts). Pure integer arithmetic — no entropy, no
    state, INV-2-clean; the same input always yields the same bar."""
    total = len(values)
    if total == 0:
        return 0  # the vacuity law: nobody reads, nobody burns
    affected = sum(1 for value in values if value >= trigger_value)
    fraction = affected * 100 // total
    if fraction <= threshold:
        return 0  # the deadband: at-or-below the bar never fires
    return min(
        max_per_beat,
        (fraction - threshold) * max_per_beat // (100 - threshold),
    )


def _member_values(
    spec: _FactionSpec, projection: "Projection"
) -> list[int]:
    """The members' live axis values (the per-entity read, D-006): each
    member's `status.<axis>` from the fold at the roll tick. A member
    absent from the projection (arrested, fled, removed) or holding no
    value on the axis sits the ratio out — the decay pass's read family
    ("NPC has no value on this axis"), never an error; the ratio is
    over the membership that HOLDS the data, honest to the fold."""
    prop = f"status.{spec.axis}"
    values: list[int] = []
    for member in spec.members:
        value = projection.get(member, {}).get(prop)
        if isinstance(value, int) and not isinstance(value, bool):
            values.append(value)
    return values


def faction_rolls(
    spec: "_FactionSpec",
    projection: "Projection",
    locations: Collection[str] | None,
) -> bool:
    """The rolling predicate — ONE law, TWO consumers (iter-337, H9):
    the faction rolls this walk iff its group entity is present in the
    projection and anchored inside the ticking zone. The walk itself
    (`faction_intents`) and the quiet-beat skip's rolling-set
    computation (the loop's `_quiet_landing`) read the SAME predicate
    — the urgency family's own extraction law (a diverging copy would
    desync the skip's counter arithmetic against the walk's draw
    pattern)."""
    props = projection.get(spec.group)
    if props is None:
        return False
    if locations is not None and props.get("position") not in locations:
        return False
    return True


def faction_bar(spec: "_FactionSpec", projection: "Projection") -> int:
    """The entry's CURRENT probability bar from the live fold (iter-337,
    H9): the small formula over the members' axis values — the same
    number `faction_intents` rolls against, exposed for the quiet-beat
    skip's landing scan (the bar is a pure projection read, frozen
    between events — the scan never re-derives the formula's inputs,
    it reads this)."""
    return faction_probability(
        _member_values(spec, projection),
        spec.trigger_value,
        spec.threshold,
        spec.max_per_beat,
    )


def faction_scan(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[_FactionSpec] | None" = None,
    limit: int = 0,
    gate_memo: ScanGateMemo | None = None,
    gate_fold: ScanGateFold | None = None,
) -> tuple[dict[str, int], int | None]:
    """H9's rolling-set + first-hit scan, the faction twin
    (iter-337 — `core.urgencies.urgency_scan` owns the family's law;
    this walk adds the ratio bar): the bar is a pure projection read
    (the members' live axes, frozen between events), so the scan
    evaluates it once per stretch and ONE collective
    `RngBank.first_d100_hit` walks the entries' own streams for the
    first draw under any of them (iter-362, the walk half of
    iter-347's named address — the same restructure as the urgency
    twin). ``streams`` maps every rolling
    faction's stream to 1 draw per beat (the cadence law: the roll
    fires once per walk regardless of the bar — a bar-0 entry still
    consumes its roll); ``first_fire`` is the smallest beat offset in
    ``[1, limit]`` at which the walk would enqueue a goal (a hit
    passing the ``requires`` gates), or ``None``; ``1`` answers a
    bar-100 entry with open gates exactly as the urgency twin.

    `gate_memo` (iter-375): the scan-family gate-answer memo — the
    urgency twin's own law (the key comparison IS the invalidation;
    `ScanGateMemo`). None (the default) keeps the fresh evaluation.

    `gate_fold` (iter-382): the memo's commit-path twin, the urgency
    twin's own law — the confirmed probe skips the key build (THE
    SERVE LAW: the fast path serves exactly the verdict the key
    compare would, never more); None (the default) keeps the key
    compare."""
    if gate_memo is not None:
        gate_memo.bind(pack, world)
    fold = (
        gate_fold
        if gate_memo is not None
        and gate_fold is not None
        and gate_fold.serves(projection)
        else None
    )
    streams: dict[str, int] = {}
    rolls: dict[str, int] = {}
    for spec in (_specs(pack) if specs is None else specs):
        if not faction_rolls(spec, projection, locations):
            continue
        streams[spec.stream] = 1
        bar = faction_bar(spec, projection)
        if bar <= 0:
            continue  # rolls, never fires (the cadence law)
        if spec.requires:
            if gate_memo is not None and spec.pairs is not None:
                open_gate = None
                if fold is not None:
                    entry = gate_memo.entry_at(spec.probe.id)
                    if entry is not None and fold.confirmed(
                        spec.probe.id, spec.pairs, entry
                    ):
                        open_gate = gate_memo.answer(spec.probe.id)
                if open_gate is None:
                    key = pair_values(projection, spec.pairs)
                    open_gate = gate_memo.lookup(spec.probe.id, key)
                    if open_gate is None:
                        open_gate = first_failing(
                            pack, projection, spec.probe, spec.requires,
                            facts=(), echoes=(), traits=(), world=world,
                        ) is None
                        gate_memo.store(spec.probe.id, key, open_gate)
                    if fold is not None:
                        fold.confirm(
                            spec.probe.id, spec.pairs,
                            gate_memo.entry_at(spec.probe.id),
                        )
            else:
                open_gate = first_failing(
                    pack, projection, spec.probe, spec.requires,
                    facts=(), echoes=(), traits=(), world=world,
                ) is None
            if not open_gate:
                continue  # the gates are shut for the whole stretch
        # the duplicate-(group, kind) fold (iter-362): the max bar's
        # first hit IS the minimum over the entries' first hits on the
        # shared stream (the monotonicity law, `first_d100_hit`'s
        # contract)
        if bar > rolls.get(spec.stream, 0):
            rolls[spec.stream] = bar
    first = bank.first_d100_hit(rolls, limit)
    return streams, first


def faction_intents(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[_FactionSpec] | None" = None,
) -> list[IntentData]:
    """One walk's worth of faction goal intents (depth-6): for each
    pack-declared faction — compute the small formula's probability
    bar from the LIVE fold, roll d100 on the entry's own
    `faction:<group>:<kind>` stream, and on a hit that passes the
    `requires` gates yield the IntentData (actor = the group entity
    id, through the front door like any urgency — D-037/D-039). A hit
    that fails the gates stays silent (the world said no — the
    urgency family's noise-floor law); the door re-validates with its
    own reads at the entry tick.

    The cadence is the caller's clock (the beat, the macro crossing —
    the loop owns which); the roll draws once per entry per walk
    regardless of the bar (the cadence law — the formula shapes the
    comparison, never the draw count; p=0 still consumes the roll,
    exactly like a probability-0 urgency entry).

    depth-3 (the scene-LOD filter): `locations` scopes the walk to
    factions ANCHORED there (the group's `position` — the active zone
    at a beat, the warm ring at a macro crossing); None (the default)
    is the one-scene law — every entry (the unarmed world's per-beat
    behavior). The cold zone's factions never roll here: their
    population-scale ride is depth-7's aggregate machinery.

    `facts` / `echoes` / `traits`: the caller's derived-fold reads at
    the walk's own tick, for `requires` gates that read them — the
    same duck-typed discipline as `urgency_intents` (this module never
    imports the fold owners; the import direction stays one-way).
    roads-1: `world` threads the generated model for the adjacent_to
    gate (the ONE shared exits read); None is the unarmed default.
    `specs` (scale-1-impl, P0.5-B): the caller's PRE-PARSED specs
    (the loop's init-time memo via `faction_specs`) — None (the
    default) keeps the standalone parse; the memo is
    byte-identical (the parse is pure)."""
    out: list[IntentData] = []
    # the rolling filter first (iter-383): the shared predicate walks
    # the specs and collects the entries that will roll — the draws
    # then cross the door ONCE for the whole set (`family_rolls`,
    # the urgency twin's own fusion; the filter and the bar compute
    # draw nothing and the projection is frozen for the walk's
    # duration, so the collect-then-draw order is the per-entry
    # order, fused)
    rolling = [
        spec
        for spec in (_specs(pack) if specs is None else specs)
        if faction_rolls(spec, projection, locations)
    ]
    if not rolling:
        return out
    # the roll: d100 on the entry's OWN faction-family stream
    # (engine-2's per-entry isolation, D-079) — one draw per walk,
    # the cadence law; the formula only sets the comparison bar.
    # iter-370: the draw rides `family_randint` — the fused
    # assure+randint form (same word, same counter position, same
    # nesting law — the urgency twin's own change). iter-383: the
    # WHOLE SET rides `family_rolls` — one door crossing per walk
    # (the next fusion; same words, same counter positions, the
    # rolling order — the per-call form stays the law's owner and
    # the tests' oracle)
    rolls = bank.family_rolls([spec.stream for spec in rolling], 1, 100)
    for spec, roll in zip(rolling, rolls, strict=True):
        values = _member_values(spec, projection)
        bar = faction_probability(
            values, spec.trigger_value, spec.threshold, spec.max_per_beat,
        )
        if roll > bar:
            continue
        intent = spec.probe
        if spec.requires:
            failing = first_failing(
                pack, projection, intent, spec.requires,
                facts=facts, echoes=echoes, traits=traits, world=world,
            )
            if failing is not None:
                continue  # the world said no — silent, no rejection event
        out.append(intent)
    return out
