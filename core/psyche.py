"""The psyche birth (agenda-1 P1, iter-418): the per-NPC personality
profile drawn lazily at the canon birth — the exact twin of the name
generator (`core/names.py::materialize_name`: the D-054 lazy-slot
shape, one materialization, first-commit-wins; this module is its P1
sibling, never a second mechanism).

- **The pack data**: `rules.json::psyche` — the trait `axes` (id + the
  low/high bands), the `archetypes` (the profile templates: one value
  per axis), and the `distributions` (the generative rows: which
  archetypes a born person may carry, the ± `jitter` around the
  archetype's defaults, and how many EXTRA extreme axes the draw may
  add on top of the archetype's own). The npc record declares the
  origin: `generated_psyche: <distribution id>` — mutually exclusive
  with an authored `psyche` (one profile origin per npc, the
  `generated_name` twin's law). A distribution id is engine-opaque
  (INV-3: the words live in the pack).
- **The draw** (`materialize_psyche`): the archetype is drawn uniformly
  from the distribution's declared list (declaration order is the index
  law, INV-2); every axis is then drawn within its ARCHETYPE DEFAULT'S
  BAND CLASS around that default (± the distribution's `jitter`), so
  the draw never turns a mid axis extreme by accident; then up to the
  remaining authoring budget (`EXTREME_BUDGET`) extra axes are drawn
  extreme (which axes: one combinatorial index — a draw, never a
  rejection walk; which side and value: one draw each). The guide's
  1-2-extremes law (`live_char_guide` OCEAN) holds for a BORN profile
  by construction, never by a post-hoc check.
- **The stream**: the whole draw runs on the npc's own `psyche:<npc>`
  stream (`core/rng.py::psyche_stream_name`, the D-079 family law's
  ninth member), so adding, removing, or re-arming a declaration
  shifts neither a canon check draw nor another npc's profile.
- **The birth** is the CONDENSATION's (the recorded consumer,
  `core/groups.py::condensation_drafts` — the same event that births
  the member's name and membership, one member one block). The
  committed event's `state_changes` carry `StateChange(npc, "psyche",
  None -> {archetype, axes})`; a profile already in the folded
  projection is SKIPPED — first-commit-wins, never a redraw (canon is
  the answer).
- **The unarmed law** (the 68a pattern): no `generated_psyche`
  declaration answers None BEFORE any stream is touched — zero
  assures, zero draws, the fingerprint and the v0.1 bytes untouched by
  construction.

The profile is READ through `profile_of`: the authored record key first
(the author's override — a pack may still hand-write a profile), the
born prop in the folded projection after the birth; an NPC with neither
runs no drive (the ticker's inert form). The birth is a PROFILE, never
a live score: the five values are immutable seed data born once, exactly
like a name — the live state stays the ordinary one (`status`,
accounts, relations, knowledge).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from itertools import combinations
from typing import TYPE_CHECKING, Any, Final

from core.log import StateChange
from core.rng import RngBank, psyche_stream_name

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle
    from core.pack import Pack

__all__ = [
    "EXTREME_BUDGET",
    "GENERATED_PSYCHE_KEY",
    "HIGH_BAND",
    "LOW_BAND",
    "PSYCHE_BLOCK",
    "PSYCHE_PROP",
    "ROLE_PROP",
    "PsycheError",
    "born_declared",
    "materialize_psyche",
    "profile_of",
    "role_of",
]

#: The rules.json block the reader and the birth share (`core/drives.py` is
#: the reading twin, `core/packlint/psyche.py` the shape lint). Absent ->
#: the unarmed law.
PSYCHE_BLOCK: Final = "psyche"

#: The npc record's declaration key — `generated_psyche: <distribution id>`
#: — and the born profile's prop on the npc entity (one string, two
#: namespaces: the record's declaration site and the projection's slot).
#: The authored record key `psyche` stays the author's override; the two
#: origins are mutually exclusive (the lint's law).
GENERATED_PSYCHE_KEY: Final = "generated_psyche"
PSYCHE_PROP: Final = "psyche"

#: The CURRENT-role prop (agenda-1 P5, iter-426): the npc's role as the
#: canon has it — written by a turning event only, absent while the person
#: still carries the role it was born with. The profile's `archetype` stays
#: the SEED (a fact of birth); this prop is the live role, and
#: `role_of` is the ONE read with a named precedence.
ROLE_PROP: Final = "archetype"

#: The axis band defaults when the pack's axis row omits them (the
#: guide's own extremum thresholds — `data/ocean.json` — as DATA, never a
#: hardcoded score: the pack's row wins when declared). The single owner:
#: the bar formula (`core/drives.py`) reads these too.
LOW_BAND: Final = 30
HIGH_BAND: Final = 70

#: The guide's EXTREME BUDGET (the authoring law `live_char_guide` §OCEAN:
#: 1-2 extremes per profile; more = unresolved internal conflict). The
#: authored-profile lint and the birth's draw both read THIS number — one
#: owner, never two copies.
EXTREME_BUDGET: Final = 2


class PsycheError(RuntimeError):
    """A profile-side contract failure (an undeclared distribution or an
    empty archetype list reached the draw — the post-lint backstop, loud
    like `core.names.NamesError`)."""


def born_declared(pack: "Pack") -> bool:
    """Does any npc declare a generated profile? The loop's parse-law gate:
    a pack WITHOUT a declaration keeps the static spec memo (zero per-beat
    re-parse — the E03 law where it still applies), a pack with one parses
    per beat against the live projection."""
    return any(
        npc.get(GENERATED_PSYCHE_KEY) is not None
        for npc in pack.entities.get("npcs", ())
    )


def profile_of(
    pack: "Pack",
    projection: "Mapping[str, Mapping[str, Any]]",
    npc_id: str,
) -> Mapping[str, Any] | None:
    """The npc's profile, or None: the authored record key first (the
    author's override), the born prop in the folded projection second
    (canon is the answer after the birth). Duck-typed packs without an
    `entity` accessor answer the born prop alone."""
    record = pack.entity(npc_id) if hasattr(pack, "entity") else None
    if record is not None:
        authored = record.get(PSYCHE_PROP)
        if isinstance(authored, Mapping):
            return authored
    born = projection.get(npc_id, {}).get(PSYCHE_PROP)
    return born if isinstance(born, Mapping) else None


def role_of(
    pack: "Pack",
    projection: "Mapping[str, Mapping[str, Any]]",
    npc_id: str,
) -> str | None:
    """The npc's CURRENT role (its archetype), by ONE precedence: the folded
    `archetype` prop (a canon turning outranks every record — the same
    principle as the fold-first display name), then the authored
    `psyche.archetype`, then the born profile's archetype. None when the npc
    carries no profile at all (no role, no drives, no want).

    This is the ONLY reader of "who is this person now": the drive ticker's
    binding, the agenda view's want and the brief all go through it, so a
    turning can never leave a card mixing two roles (the P5 one-law design)."""
    held = projection.get(npc_id, {}).get(ROLE_PROP)
    if isinstance(held, str) and held:
        return held
    profile = profile_of(pack, projection, npc_id)
    if profile is None:
        return None
    archetype = profile.get("archetype")
    return str(archetype) if isinstance(archetype, str) and archetype else None


def _bands(axis: Mapping[str, Any]) -> tuple[int, int]:
    """The axis's own extremum bands (the pack row wins; the guide's
    thresholds are the fallback)."""
    return (
        int(axis.get("low", LOW_BAND)),
        int(axis.get("high", HIGH_BAND)),
    )


def _extreme(value: int, low: int, high: int) -> bool:
    """The band law: a value AT or beyond a band threshold is extreme
    (inclusive — the donor's thresholds are the edges, not the middles)."""
    return value <= low or value >= high


def _draw_axes(
    bank: RngBank,
    axes: Sequence[Mapping[str, Any]],
    archetype: Mapping[str, Any],
    distribution: Mapping[str, Any],
) -> dict[str, int]:
    """The profile's five values: per declared axis (pack order) one draw
    around the archetype's default, clamped INSIDE the default's own band
    class; then the extra extremes the distribution allows, up to the
    remaining authoring budget. Pure over (the active `psyche:<npc>`
    stream, the pack's immutable tables) — the same seed and the same
    tables answer the same profile, and the extreme count can never
    exceed `EXTREME_BUDGET` by construction."""
    defaults = archetype["defaults"]
    jitter = int(distribution.get("jitter", 0))
    values: dict[str, int] = {}
    for axis in axes:
        axis_id = str(axis["id"])
        low, high = _bands(axis)
        default = int(defaults[axis_id])
        drawn = bank.randint(
            max(0, default - jitter), min(100, default + jitter),
        )
        if default <= low:
            values[axis_id] = min(drawn, low)
        elif default >= high:
            values[axis_id] = max(drawn, high)
        else:
            values[axis_id] = min(max(drawn, low + 1), high - 1)
    extremes = sum(
        1 for axis in axes
        if _extreme(values[str(axis["id"])], *_bands(axis))
    )
    middles = [
        axis for axis in axes
        if not _extreme(values[str(axis["id"])], *_bands(axis))
    ]
    cap = min(
        int(distribution.get("extremes", 0)),
        EXTREME_BUDGET - extremes,
        len(middles),
    )
    if cap > 0:
        count = bank.randint(1, cap)
        picks = list(combinations(range(len(middles)), count))
        chosen = picks[bank.randint(0, len(picks) - 1)]
        for index in chosen:
            axis = middles[index]
            low, high = _bands(axis)
            if bank.randint(0, 1) == 0:
                values[str(axis["id"])] = bank.randint(0, low)
            else:
                values[str(axis["id"])] = bank.randint(high, 100)
    return values


def materialize_psyche(
    bank: RngBank, pack: "Pack",
    projection: "Mapping[str, Mapping[str, Any]]", npc_id: str,
) -> StateChange | None:
    """The npc's profile birth, or None: an npc without the declaration
    (or a pack without the block) answers None BEFORE any stream is
    touched (the unarmed law, zero draws); a profile already held by the
    folded projection is canon — skipped, never redrawn (the
    first-commit-wins twin). Otherwise ONE profile is drawn from the
    npc's own `psyche:<npc>` stream and returned as the birth
    StateChange. The caller rides it on its event — the condensation's
    own state_changes, beside the name (the name-1 law extended)."""
    record = pack.entity(npc_id) if hasattr(pack, "entity") else None
    distribution_id = (
        record.get(GENERATED_PSYCHE_KEY) if record is not None else None
    )
    if distribution_id is None:
        return None  # authored or absent — the unarmed law
    if projection.get(npc_id, {}).get(PSYCHE_PROP) is not None:
        return None  # canon holds a profile — first-commit-wins
    config = pack.rules.get(PSYCHE_BLOCK)
    if not isinstance(config, Mapping):
        raise PsycheError(
            f"{npc_id}: generated_psyche declared but rules.json carries no "
            "psyche block (the lint owns the shape — this path is the "
            "post-lint backstop)"
        )
    distributions = {
        str(row["id"]): row
        for row in config.get("distributions", ())
        if isinstance(row, Mapping)
    }
    distribution = distributions.get(str(distribution_id))
    if distribution is None:
        raise PsycheError(
            f"{npc_id}: generated_psyche {distribution_id!r} has no row in "
            "rules.json psyche.distributions (the lint owns the shape — "
            "this path is the post-lint backstop)"
        )
    axes = [
        axis for axis in config.get("axes", ()) if isinstance(axis, Mapping)
    ]
    archetypes = {
        str(row["id"]): row
        for row in config.get("archetypes", ())
        if isinstance(row, Mapping)
    }
    candidates = [
        archetypes[str(name)] for name in distribution.get("archetypes", ())
        if str(name) in archetypes
    ]
    if not candidates:
        raise PsycheError(
            f"{npc_id}: distribution {distribution_id!r} names no declared "
            "archetype (the post-lint backstop)"
        )
    with bank.assure(psyche_stream_name(npc_id)):
        archetype = candidates[bank.randint(0, len(candidates) - 1)]
        values = _draw_axes(bank, axes, archetype, distribution)
    return StateChange(
        entity=npc_id,
        prop=PSYCHE_PROP,
        from_=None,
        to_={"archetype": str(archetype["id"]), "axes": values},
    )
