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

from core.ids import sequence_id
from core.intent import IntentData, first_failing
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

FACTION_PREFIX: Final = "faction"  # intent ids (faction_0000…)


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


def _specs(pack: "Pack") -> tuple[_FactionSpec, ...]:
    """Parse the pack's `factions.entries` (load order: pack-declared;
    the walk respects it as given — INV-2 via construction order). The
    members ride the GROUP entity's own declaration order (the group
    record is the membership's single pack-side owner; the runtime
    `member_of` state door is depth-7's row, never this walk's)."""
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
        specs.append(
            _FactionSpec(
                group=entry["group"],
                axis=entry["axis"],
                trigger_value=int(entry["trigger_value"]),
                threshold=int(entry["threshold"]),
                max_per_beat=int(entry["max_per_beat"]),
                intent_kind=entry["intent"]["kind"],
                intent_target=entry["intent"].get("target"),
                intent_fields=dict(entry["intent"].get("fields", {})),
                requires=tuple(entry.get("requires", ())),
                members=tuple(group.get("members", ())),
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


def _build_intent(spec: _FactionSpec, seq: int) -> IntentData:
    """Materialize an IntentData from a pack spec; the loop stamps the
    real `based_on_event_seq` at enqueue time."""
    return IntentData(
        id=sequence_id(FACTION_PREFIX, seq),
        kind=spec.intent_kind,
        actor=spec.group,  # D-112: the group IS the actor — one id
        target=spec.intent_target,
        fields=spec.intent_fields,
        based_on_event_seq=0,
    )


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
    bar-100 entry with open gates exactly as the urgency twin."""
    streams: dict[str, int] = {}
    rolls: dict[str, int] = {}
    for seq, spec in enumerate(
        _specs(pack) if specs is None else specs
    ):
        if not faction_rolls(spec, projection, locations):
            continue
        name = faction_stream_name(spec.group, spec.intent_kind)
        streams[name] = 1
        bar = faction_bar(spec, projection)
        if bar <= 0:
            continue  # rolls, never fires (the cadence law)
        if spec.requires:
            probe = _build_intent(spec, seq)
            if first_failing(
                pack, projection, probe, list(spec.requires),
                facts=(), echoes=(), traits=(), world=world,
            ) is not None:
                continue  # the gates are shut for the whole stretch
        # the duplicate-(group, kind) fold (iter-362): the max bar's
        # first hit IS the minimum over the entries' first hits on the
        # shared stream (the monotonicity law, `first_d100_hit`'s
        # contract)
        if bar > rolls.get(name, 0):
            rolls[name] = bar
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
    for seq, spec in enumerate(
        _specs(pack) if specs is None else specs
    ):
        # the rolling filter — the shared predicate (iter-337): an
        # absent or out-of-zone faction never rolls
        if not faction_rolls(spec, projection, locations):
            continue
        values = _member_values(spec, projection)
        bar = faction_probability(
            values, spec.trigger_value, spec.threshold, spec.max_per_beat,
        )
        # the roll: d100 on the entry's OWN faction-family stream
        # (engine-2's per-entry isolation, D-079) — one draw per walk,
        # the cadence law; the formula only sets the comparison bar
        with bank.assure(faction_stream_name(spec.group, spec.intent_kind)):
            roll = bank.randint(1, 100)
        if roll > bar:
            continue
        intent = _build_intent(spec, seq)
        if spec.requires:
            failing = first_failing(
                pack, projection, intent, list(spec.requires),
                facts=facts, echoes=echoes, traits=traits, world=world,
            )
            if failing is not None:
                continue  # the world said no — silent, no rejection event
        out.append(intent)
    return out
