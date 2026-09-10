"""The name generator (name-1, `phases.md` §5 — TASKS name-1, D-116
(12): the Azgaar split — condensation's canon-birth events need names;
`region_00`-style engine ids do not scale to a story). The lazy
scene-detail twin at npc scale (`core/detail.py` is the law's first
owner, the D-054 texture-promotion shape — never a second mechanism):

- **The pack data**: `rules.json::names` — the phonotactic PROFILES,
  culture-keyed n-gram pools (the Azgaar nameBase shape: the syllable
  component pools + the syllable-count bounds; the CK3 culture-keying —
  one profile per culture, the profile id names it). INV-3: the pools
  are pack data, the generator below is pure functions over them; a
  profile id is engine-opaque (any non-empty key, the pack's own
  vocabulary). The npc record declares the origin:
  `generated_name: <profile id>` — one or the other, never both with
  an authored `name` (the lint's law; `name` stays the pure string
  surface every existing reader already knows).
- **The lazy draw** (`materialize_name`): an npc's unmaterialized name
  is generated deterministically from the content-addressed stream
  `name:<npc>` (`core/rng.py::name_stream_name`, the D-079 family law's
  sixth member — the scene-detail twin: one stream per declared
  npc, so adding, removing, or re-arming a declaration shifts neither
  a canon check draw nor another npc's name). The first materialization
  is the CONDENSATION's own (the recorded consumer: depth-7's
  `condensation_drafts` — the members' canon births carry their name
  births; `world-2`'s cultures are the phase-6 consumer). The committed
  event's `state_changes` carry the birth as `StateChange(npc, "name",
  None -> value)`; a name already in the folded projection is SKIPPED —
  first-commit-wins, never a redraw (canon is the answer).
- **The output namespace law** (the TASKS row's lint line): a drawn
  name must not collide with the ENTITY NAMESPACE — every declared
  entity id, all categories. The render maps id-valued strings to
  display names (`render/chronicle.py::_display_if_entity`), so a name
  equal to an id would corrupt the mapping; the walk skips colliding
  candidates and redraws (deterministic — the stream advances per
  attempt), bounded by `WALK_MAX` before the loud refusal: a profile
  whose derivable space cannot clear the namespace is a pack design
  error (widen the pools), the vacuity family. The namespace is
  load-time static — the draw-side walk is the law's single owner
  (a load-time lint cannot check a seed-dependent space).
- **The unarmed law (the 68a pattern)**: a pack without the `names`
  block, or an npc without the declaration, answers None BEFORE any
  stream is touched — zero assures, zero draws, the fingerprint and
  the v0.1 bytes untouched by construction.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Final

from core.log import StateChange
from core.rng import RngBank, name_stream_name

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle
    from core.pack import Pack

__all__ = [
    "GENERATED_NAME_KEY",
    "NAMES_BLOCK",
    "NAME_PROP",
    "PROFILE_KEYS",
    "WALK_MAX",
    "NamesError",
    "materialize_name",
]

#: The rules.json block this module reads (the profiles; `core/pack.py::
#: _names` owns the shape lint). Absent -> the unarmed law.
NAMES_BLOCK: Final = "names"

#: The npc record's declaration key — `generated_name: <profile id>`.
#: The authored `name` field stays the pure string surface; the two are
#: mutually exclusive (the lint's law — one name origin per npc).
GENERATED_NAME_KEY: Final = "generated_name"

#: The born name's prop on the npc entity — the D-054 slot shape: the
#: projection seeds NOTHING for it (absence IS the unborn name), the
#: materialization event births it, and canon never redraws.
NAME_PROP: Final = "name"

#: The profile record's closed vocabulary: the three syllable-component
#: pools + the syllable-count bounds (the Azgaar nameBase shape).
PROFILE_KEYS: Final = ("onsets", "nuclei", "codas", "syllables")

#: The collision walk's bound — candidates tried per name before the
#: loud `NamesError` (the states pass's `10 * count` retry family: a
#: bounded walk, never an unbounded one; the refusal names the fix).
WALK_MAX: Final = 16

#: The entity categories the reserved namespace walks (the same order
#: `Pack.entity` reads — the single namespace of record).
_CATEGORIES: Final = (
    "locations", "npcs", "ambient_entities", "items", "groups",
)


class NamesError(RuntimeError):
    """A name-side contract failure (an undeclared profile reached the
    draw, or a profile that cannot clear the entity namespace)."""


def _reserved(pack: "Pack") -> frozenset[str]:
    """The entity namespace: every declared entity id, all categories
    (the pack's load-time static set — the collision walk's universe).
    Duck-typed packs without an `entities` mapping answer an empty set
    (the unit-test stubs that declare no namespace)."""
    entities = getattr(pack, "entities", None) or {}
    return frozenset(
        record["id"]
        for category in _CATEGORIES
        for record in entities.get(category, ())
    )


def _assemble(bank: RngBank, profile: Mapping[str, Any]) -> str:
    """One candidate name: the syllable count drawn inside the profile's
    bounds, then per syllable one onset + one nucleus + one coda draw
    (pool indices, the profile's own declaration order — INV-2). The
    surface form capitalizes the first letter; the pools are lowercase
    fragments by lint. Pure over (the active stream, the profile)."""
    bounds = profile["syllables"]
    count = bank.randint(int(bounds[0]), int(bounds[1]))
    parts: list[str] = []
    for _ in range(count):
        for key in ("onsets", "nuclei", "codas"):
            pool = profile[key]
            parts.append(pool[bank.randint(0, len(pool) - 1)])
    return "".join(parts).capitalize()


def materialize_name(
    bank: RngBank, pack: "Pack",
    projection: Mapping[str, Mapping[str, Any]], npc_id: str,
) -> StateChange | None:
    """The npc's name birth, or None: an npc without the declaration
    (or a pack without the block) answers None BEFORE any stream is
    touched — the unarmed law, zero draws; a name already held by the
    folded projection is canon — skipped, never redrawn (the
    first-commit-wins twin). Otherwise ONE birth is drawn from the
    npc's own `name:<npc>` stream (assured here — the family law), the
    collision walk skipping candidates that collide with the entity
    namespace (deterministic redraw, bounded by `WALK_MAX`, then the
    loud refusal). The caller rides the birth on its event — the
    condensation's own state_changes (depth-7's law extended)."""
    record = pack.entity(npc_id) if hasattr(pack, "entity") else None
    profile_id = (
        record.get(GENERATED_NAME_KEY) if record is not None else None
    )
    if profile_id is None:
        return None  # authored or absent — the unarmed law
    if projection.get(npc_id, {}).get(NAME_PROP) is not None:
        return None  # canon holds a name — first-commit-wins
    profiles = pack.rules.get(NAMES_BLOCK, {}).get("profiles", {})
    profile = profiles.get(str(profile_id))
    if profile is None:
        raise NamesError(
            f"{npc_id}: generated_name {profile_id!r} has no profile in "
            "rules.json names.profiles (the lint owns the shape — this "
            "path is the post-lint backstop)"
        )
    reserved = _reserved(pack)
    with bank.assure(name_stream_name(npc_id)):
        for _attempt in range(WALK_MAX):
            candidate = _assemble(bank, profile)
            if candidate not in reserved:
                return StateChange(
                    entity=npc_id, prop=NAME_PROP, from_=None, to_=candidate,
                )
    raise NamesError(
        f"{npc_id}: the profile {profile_id!r} could not clear the entity "
        f"namespace in {WALK_MAX} draws — widen the pools (the collision "
        "walk's refusal, the vacuity family)"
    )
