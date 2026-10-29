"""The drive ticker (agenda-1 P0, iter-417): an NPC's goal pursuit as a
DERIVED-probability roll over pack-declared drives — the faction-goal
small formula turned inward (`core/factions.py` the twin: a faction
derives its bar from its members' live axes; a drive derives its bar
from the NPC's declared personality profile and the unmet share of its
goal measure). No planner, no priority queue, no stored goal state: the
goal is a READING of the world through a declared lens, the decision is
one roll, the consequence is the ordinary door's.

Pack vocabulary (both halves optional — the unarmed law, the 68a
pattern: a pack declaring no `psyche` block keeps the v0.1 draws and
behaviour exactly; the committed anchor carries the block's shape with
no profile on any NPC, so its corpus price is ZERO until a content row
arms profiles — INERT-FIRST measured, never assumed):

- `rules.json::psyche` — `axes` (the trait axes: id + the low/high
  bands), `archetypes` (the profile templates: id + one value per axis),
  `distributions` (the generative rows: which archetypes a born person
  may carry, the ± jitter, and the extra extremes a draw may add),
  `drives` (id, archetypes, base, max_per_beat, verb, target?, fields?,
  measure?, need?, modifiers?), `notes`;
- a `modifiers` row: `{axis, low_pct, high_pct}` reads the PROFILE's
  value on that axis (its bands live on the axis row — one owner); a row
  also declaring `source: echo` reads the NPC's echo residue on that
  axis instead, and then owns its bands (`low` / `high`), because an
  echo axis has no `psyche.axes` row (`core.echo.py` owns the score
  scale, `rules.json::echo`). `source` defaults to `profile` — a pack
  that declares no echo row keeps every byte and every draw
  (INERT-FIRST);
- `entities.json::npcs[].psyche` — the AUTHORED per-NPC profile
  `{archetype, axes}`; `entities.json::npcs[].generated_psyche` — the
  BORN origin (agenda-1 P1: a distribution id drawn into the
  projection's `psyche` prop at the canon birth). Both are read through
  `core.psyche.profile_of` (the authored key first, the born prop
  after); an NPC with neither runs no drive.

The parse is a function of (the pack's immutable tables, the profiles
the projection holds): a pack whose profiles are all AUTHORED parses
once at run start (the memo, byte-identical by construction — the E03
law); a pack declaring a born origin parses per beat against the live
projection, because a profile that did not exist at the previous beat
now arms its drives. The skip and the walk read the SAME parse of the
SAME frozen projection, which is what keeps the skip's counter
arithmetic exact (a birth always forces the skip to the very next beat:
`core.groups.condensation_pending`).

The bar (pure integer arithmetic, INV-2-clean; the division order is the
declaration order — the parse is a function of immutable pack data):

    weight  = drive.base, then every declared modifier in pack order:
              value <= the row's low band  -> * low_pct  // 100
              value >= the row's high band -> * high_pct // 100
              (the value is the profile's axis for a `source: profile`
              row — the frozen seed — and the NPC's echo score at the
              READ TICK for a `source: echo` row; a residue the NPC does
              not carry reads as zero, the world's honest answer)
    deficit = the count of the drive's `measure` conditions that FAIL now
    bar     = 0                                  if deficit == 0
            = min(max_per_beat, weight * deficit) otherwise

An echo-sourced modifier makes the bar TIME-DEPENDENT (the residue
decays): the quiet-beat skip's exactness fence is the loop's fold demand
(`core.loop` adds the echo test when any drive declares such a row), so
a pack arming one keeps the exact tick-by-tick path — the same law a
fold-gated urgency already follows. The card and the brief read the SAME
weight (`core.agenda` + `brief/assembler.py` pass their own fold): one
reading, never a second truth about who is dominant.

`measure` is the CLOSED precondition vocabulary (`core.intent`), read
through the same evaluator the door uses (`first_failing`) and never
through a second one. A satisfied goal stops pushing — the continuity
law: a goal that is met does not repeat itself every beat; a partly-met
one pushes proportionally to its unmet share. A drive with no measure
pushes at its full weight (an appetite with no satisfier — pack data's
own choice; the closed vocabulary reads it as "always unmet"). The
windowed tests are REFUSED in a measure by the pack lint: the quiet-beat
skip evaluates bars against the frozen projection, and a time-dependent
fold read there would desync the skip's arithmetic.

The roll: d100 on the drive's OWN stream `drive:<npc>:<drive>`
(`core/rng.py` — the D-079 family law's eighth member), ONE draw per
rolling drive per walk regardless of the bar (the cadence law: the
formula shapes the comparison, never the draw count). At most ONE intent
per NPC per walk: the strongest hit wins, a tie keeps the declaration
order (the pack's own order is the law — INV-2).

Everything else is the urgency/faction families' own discipline, not a
new one: the rolling predicate (present in the projection, positioned
inside the ticking zone, not caught), the silent gate failure (the door
re-validates and rejects as a fact — attempts are canon), the scene-LOD
filter (`locations`), the quiet-beat skip's scan (zero draws, the SAME
predicates), and through-the-door enqueueing only (D-037: the world's
logic is one mechanism).
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.intent import IntentData, first_failing
from core.psyche import HIGH_BAND, LOW_BAND, profile_of, role_of
from core.rng import drive_stream_name

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.rng import RngBank
    from core.worldgen import WorldModel

__all__ = [
    "DRIVE_PREFIX",
    "ECHO_SOURCE",
    "PROFILE_SOURCE",
    "DriveModifier",
    "DriveSpec",
    "drive_bar",
    "drive_demand",
    "drive_intents",
    "drive_rolls",
    "drive_scan",
    "drive_specs",
    "drive_weight",
    "echo_modifiers_declared",
]

DRIVE_PREFIX: Final = "drive"  # intent ids (drive_<npc>_<drive>)

#: The modifier row's two value sources (agenda-1 P5-unit-2, iter-427): the
#: frozen PROFILE axis (the v0.1 row, the default) or the decaying ECHO
#: residue read at the caller's own tick.
PROFILE_SOURCE: Final = "profile"
ECHO_SOURCE: Final = "echo"


@dataclass(frozen=True, slots=True)
class DriveModifier:
    """One resolved modifier row: the ordered band test with its bands
    already resolved — from the axis row for a profile source (the one
    owner of the profile bands), from the row itself for an echo source
    (an echo axis has no `psyche.axes` row)."""

    source: str
    axis: str
    low: int
    high: int
    low_pct: int
    high_pct: int


@dataclass(frozen=True, slots=True)
class DriveSpec:
    """One NPC-carried drive (the parse's product: the pack's drive row
    joined with the NPC's own profile and archetype).

    - `npc` / `drive`: the identities — the stream is `drive:<npc>:<drive>`
      (content-addressed, add-safe: a new drive or a re-armed profile adds
      a NEW stream and shifts no other draw);
    - `verb` / `target` / `fields`: the intent template the drive attempts
      (the action's own `requires` are the door's, re-validated there);
    - `measure`: the goal's closed-vocabulary conditions — the bar's
      deficit source, never a door gate;
    - `need`: the drive's own phrase for the board's `need=` sentence
      (`need` on the row, needphrase-1, iter-446) — a narrator's line, never
      a term; None means the board falls back to the person's `spine.need`
      (`core.offers._need` owns the order);
    - `base` / `modifiers`: the bar's declared shape, the rows in pack
      order with their bands resolved (`drive_weight` applies them);
    - `probe`: the frozen IntentData the walk enqueues (the loop stamps
      `based_on_event_seq` and `assignment_tick` — the urgency family's
      own sharing law).
    """

    npc: str
    drive: str
    verb: str
    target: str | None
    fields: Mapping[str, Any]
    measure: tuple[Mapping[str, Any], ...]
    need: str | None
    base: int
    modifiers: tuple[DriveModifier, ...]
    max_per_beat: int
    stream: str
    probe: IntentData


def _modifiers(
    drive: Mapping[str, Any],
    axes: Mapping[str, Mapping[str, Any]],
) -> tuple[DriveModifier, ...]:
    """The drive's declared rows resolved into the weight's ordered
    program: a profile row takes its bands from the AXIS row (the one
    owner — a second band on the modifier would be a second truth), an
    echo row declares its own (no `psyche.axes` row exists for an echo
    axis; the lint owns the shape and the scale bounds)."""
    rows: list[DriveModifier] = []
    for modifier in drive.get("modifiers", ()):
        axis = str(modifier["axis"])
        source = str(modifier.get("source", PROFILE_SOURCE))
        if source == ECHO_SOURCE:
            low = int(modifier["low"])
            high = int(modifier["high"])
        else:
            declared = axes[axis]
            low = int(declared.get("low", LOW_BAND))
            high = int(declared.get("high", HIGH_BAND))
        rows.append(
            DriveModifier(
                source=source,
                axis=axis,
                low=low,
                high=high,
                low_pct=int(modifier["low_pct"]),
                high_pct=int(modifier["high_pct"]),
            )
        )
    return tuple(rows)


def echo_modifiers_declared(pack: "Pack") -> bool:
    """Does any drive row read the ECHO fold? The loop's fence predicate:
    an echo-sourced modifier makes the bar time-dependent (the residue
    decays), so the pack must compute the echo fold per beat and may not
    use the quiet-beat skip (the `core.loop._fold_demand` fence). Cheap
    (the pack's immutable tables, read once at init)."""
    config = pack.rules.get("psyche")
    if not isinstance(config, Mapping):
        return False
    for drive in config.get("drives", ()):
        if not isinstance(drive, Mapping):
            continue
        for modifier in drive.get("modifiers", ()):
            if (
                isinstance(modifier, Mapping)
                and str(modifier.get("source", PROFILE_SOURCE)) == ECHO_SOURCE
            ):
                return True
    return False


def _echo_by_axis(npc: str, echoes: Sequence[Any]) -> dict[str, int]:
    """The NPC's own residue, axis -> score, from the caller's fold read.
    A pair the fold omits reads as zero (`core.echo`'s honest answer: no
    residue)."""
    scores: dict[str, int] = {}
    for score in echoes:
        if getattr(score, "who", None) != npc:
            continue
        scores[str(score.axis)] = int(score.score)
    return scores


def drive_weight(
    spec: DriveSpec,
    pack: "Pack",
    projection: "Projection",
    echoes: Sequence[Any] = (),
) -> int:
    """The drive's CURRENT weight: `base` then every declared row in pack
    order, `* pct // 100` at the row's own band. A profile row reads the
    FROZEN seed (`core.psyche.profile_of` — the same one read the birth
    and the card use); an echo row reads the residue at the caller's tick
    (a decaying read model — never stored, never a second fold). A
    profile holding no value on the axis applies no row (the honest read:
    the profile says nothing about it — the lint requires completeness,
    this is the defensive form)."""
    profile = profile_of(pack, projection, spec.npc)
    profile_axes = (profile or {}).get("axes") or {}
    scores: dict[str, int] = {}
    weight = spec.base
    for modifier in spec.modifiers:
        if modifier.source == ECHO_SOURCE:
            if not scores:
                scores = _echo_by_axis(spec.npc, echoes)
            value: Any = scores.get(modifier.axis, 0)
        else:
            value = profile_axes.get(modifier.axis)
        if not isinstance(value, int) or isinstance(value, bool):
            continue
        if value <= modifier.low:
            weight = weight * modifier.low_pct // 100
        elif value >= modifier.high:
            weight = weight * modifier.high_pct // 100
    return weight


def _specs(pack: "Pack", projection: "Projection | None" = None) -> tuple[DriveSpec, ...]:
    """Parse the pack's `psyche` block and every NPC's profile into the
    walk's specs (the parse-once memo's input when no profile is born:
    pure over immutable pack data, byte-identical by construction). Order:
    NPC declaration order, then the archetype's drive declaration order —
    the pack's own order is the canon order (INV-2). With `projection`,
    the born profiles join (the P1 lazy birth) — the same walk, the same
    order, the profile read through `core.psyche.profile_of` (authored
    key first, born prop after)."""
    config = pack.rules.get("psyche")
    if not isinstance(config, Mapping):
        return ()
    axes = {
        axis["id"]: axis
        for axis in config.get("axes", ())
        if isinstance(axis, Mapping)
    }
    by_archetype: dict[str, list[Mapping[str, Any]]] = {}
    for drive in config.get("drives", ()):
        if not isinstance(drive, Mapping):
            continue
        for archetype in drive.get("archetypes", ()):
            by_archetype.setdefault(archetype, []).append(drive)
    specs: list[DriveSpec] = []
    state: Mapping[str, Mapping[str, Any]] = projection or {}
    for npc in pack.entities.get("npcs", ()):
        profile = profile_of(pack, state, npc["id"])
        if profile is None:
            continue
        # agenda-1 P5 (iter-426): the drives bind the CURRENT ROLE, not the
        # born archetype — a turning event rebinds the set (the old role's
        # drives fall silent, the new role's arm) while the TEMPERAMENT (the
        # profile's five numbers) stays the person's own seed.
        role = role_of(pack, state, npc["id"])
        if role is None:
            continue
        for drive in by_archetype.get(role, ()):
            verb = drive["verb"]
            target = drive.get("target")
            fields = dict(drive.get("fields") or {})
            # the board's phrase for THIS pursuit (needphrase-1, iter-446):
            # the row's own `need`; the pack lint owns its shape, so the read
            # here is defensive only (a non-string answers None, never a
            # broken segment).
            need = drive.get("need")
            probe = IntentData(
                # roster-2 (iter-434, KI#116): the probe id names the
                # probe's own IDENTITY, never its ordinal — a content row
                # declared earlier can no longer renumber another probe's
                # `cause_intent` (the positional form did, measured
                # iter-429). Unique per probe by construction: ids repeat
                # every beat, and the OCC snapshot FIFO
                # (`core/loop.py:449-461`) pairs same-id enqueues in push
                # order, so two DISTINCT probes must never share an id —
                # the same probe's repeats keep it (the FIFO's design;
                # probeids-1, iter-436, states the law family-wide).
                id=f"{DRIVE_PREFIX}_{npc['id']}_{drive['id']}",
                kind=verb,
                actor=npc["id"],
                target=target,
                fields=fields,
                based_on_event_seq=0,
            )
            specs.append(
                DriveSpec(
                    npc=npc["id"],
                    drive=drive["id"],
                    verb=verb,
                    target=target,
                    fields=fields,
                    measure=tuple(drive.get("measure", ())),
                    need=need if isinstance(need, str) and need else None,
                    base=int(drive["base"]),
                    modifiers=_modifiers(drive, axes),
                    max_per_beat=int(drive["max_per_beat"]),
                    stream=drive_stream_name(npc["id"], drive["id"]),
                    probe=probe,
                )
            )
    return tuple(specs)


def drive_specs(
    pack: "Pack", projection: "Projection | None" = None,
) -> tuple[DriveSpec, ...]:
    """The parse-once accessor (the loop's init-time memo — the same E03
    law the urgency/faction families follow: the parse is pure, so reading
    it once instead of per beat changes no byte). With `projection`, the
    parse also sees the profiles the canon has born (agenda-1 P1) and the
    result is per-beat, not per-run: a birth arms a NEW drive, so the
    caller re-reads it while the projection is live."""
    return _specs(pack, projection)


def drive_bar(
    spec: DriveSpec,
    pack: "Pack",
    projection: "Projection",
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    world: "WorldModel | None" = None,
) -> int:
    """The drive's CURRENT probability bar (0..`max_per_beat`) from the
    live projection: zero when the goal's measure is fully met, the
    weight times the unmet count otherwise, clamped at the ceiling. Pure
    projection + fold reads (the closed evaluator), no entropy — the same
    input always yields the same bar, which is what lets the quiet-beat
    skip evaluate it once per stretch (a pack reading the echo fold keeps
    the tick-by-tick path instead: the residue decays, see the module
    docstring)."""
    weight = drive_weight(spec, pack, projection, echoes)
    if not spec.measure:
        return weight  # an appetite with no satisfier
    deficit = 0
    for condition in spec.measure:
        failing = first_failing(
            pack, projection, spec.probe, (condition,),
            facts=facts, echoes=echoes, traits=traits, world=world,
        )
        if failing is not None:
            deficit += 1
    if deficit == 0:
        return 0  # the continuity law: a met goal stops pushing
    return min(spec.max_per_beat, weight * deficit)


def drive_demand(pack: "Pack") -> frozenset[str]:
    """The fold TESTS the drive measures read — the E04 demand twin
    (iter-439, `drivegoals-1`). A measure on an EVENT-DRIVEN fold
    (`trait_held`) is legal (`core/packlint/psyche.py::_measure`), but the
    loop computes a fold only on a declared consumer: without this demand
    the ticker would read an empty tuple, the trait condition would answer
    failing forever and the bar would sit at its full deficit — the
    silent-dead-gate trap `turning_demand` closes for the turning rows.
    The same non-empty answer spends the quiet-beat skip: a bar that moves
    between events cannot be evaluated once per stretch (`core/loop.py`'s
    fence reads this demand)."""
    config = pack.rules.get("psyche")
    if not isinstance(config, Mapping):
        return frozenset()
    return frozenset(
        str(condition.get("test"))
        for drive in config.get("drives", ())
        if isinstance(drive, Mapping)
        for condition in drive.get("measure", ())
        if isinstance(condition, Mapping)
    )


def drive_rolls(
    spec: DriveSpec,
    projection: "Projection",
    locations: Collection[str] | None,
) -> bool:
    """The rolling predicate — ONE law, TWO consumers (the urgency /
    faction families' own extraction law): the drive rolls this walk iff
    its NPC is present in the projection, positioned inside the ticking
    zone (None = the unarmed one-scene world), and not caught. A
    diverging copy would desync the quiet-beat skip's counter arithmetic
    against the walk's draw pattern, so both read THIS function."""
    if spec.npc not in projection:
        return False
    if (
        locations is not None
        and projection[spec.npc].get("position") not in locations
    ):
        return False
    if projection[spec.npc].get("crime_status") == "caught":
        return False
    return True


def drive_scan(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[DriveSpec] | None" = None,
    limit: int = 0,
) -> tuple[dict[str, int], int | None]:
    """The quiet-beat skip's drive twin (`core.factions.faction_scan`
    owns the family's law): the rolling set's streams with their
    per-beat draw counts (1 each — the cadence law: a bar-0 drive still
    consumes its roll) and the smallest beat offset in ``[1, limit]`` at
    which a hit passes the bar. Zero draws, zero enqueues; the bars and
    the predicate read the FROZEN projection the caller pinned, so one
    evaluation serves the whole stretch (the scan's exactness law).

    The bars here read the PROFILE half only: a pack whose drives declare
    an echo-sourced modifier is refused the skip by the loop's fold
    demand (`echo_modifiers_declared`), and so is a pack whose `measure`
    reads the event-driven fold (`drive_demand` joins `_fold_demand`,
    iter-439) — this frozen-evaluation form never answers for a bar that
    moves between events."""
    streams: dict[str, int] = {}
    rolls: dict[str, int] = {}
    for spec in (_specs(pack) if specs is None else specs):
        if not drive_rolls(spec, projection, locations):
            continue
        streams[spec.stream] = 1
        bar = drive_bar(spec, pack, projection, world=world)
        if bar <= 0:
            continue  # rolls, never fires
        if bar > rolls.get(spec.stream, 0):
            rolls[spec.stream] = bar
    return streams, bank.first_d100_hit(rolls, limit)


def drive_intents(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[DriveSpec] | None" = None,
) -> list[IntentData]:
    """One walk's worth of drive intents: for each rolling drive, the
    live bar, ONE d100 on the drive's own stream, and — among the hits —
    at most one intent per NPC (the strongest bar; a tie keeps the
    declaration order). A hit whose roll exceeds the bar stays silent
    (the world did not call for it — never a rejection event; the
    urgency family's noise-floor law). The door re-validates the action's
    own `requires` at the entry tick: a gate failure THERE is an attempt
    and lands as canon (`intent_rejected`), exactly as for any actor."""
    rolling = [
        spec
        for spec in (_specs(pack) if specs is None else specs)
        if drive_rolls(spec, projection, locations)
    ]
    if not rolling:
        return []
    rolls = bank.family_rolls([spec.stream for spec in rolling], 1, 100)
    best: dict[str, tuple[int, int, IntentData]] = {}
    for position, (spec, roll) in enumerate(
        zip(rolling, rolls, strict=True)
    ):
        bar = drive_bar(
            spec, pack, projection,
            facts=facts, echoes=echoes, traits=traits, world=world,
        )
        if roll > bar:
            continue
        incumbent = best.get(spec.npc)
        if incumbent is None or bar > incumbent[0]:
            best[spec.npc] = (bar, position, spec.probe)
    return [
        probe
        for _bar, _position, probe in sorted(
            best.values(), key=lambda item: item[1]
        )
    ]
