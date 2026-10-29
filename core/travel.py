"""The travel price law (st-6a, D-116 (5) — travel as a separate
action, never a weighted move; phases.md §5 is the architecture owner):

- The DURATION of one travel is the PRICE of the exits edge it
  traverses — computed at the accept door (resolve time, L3: derive,
  never store), the completion enqueued at `t + price` (MVP_SCOPE §8 —
  the clock jumps ahead, so day-scale durations are queue-cheap; beats,
  rotations and macro crossings still fire mid-travel in tick order,
  D-038).
- THE PACK OVERRIDE WINS per edge (`rules.json::travel.edges` —
  authored packs price their own roads; the "pack wins" law).
- Otherwise the price is DERIVED from the WorldModel — a pure integer
  function of distance + height/river modifiers (D-116 (5), the
  amended law: generated worlds never hand-author prices). place-1's
  claim↔exits consistency is what makes derived prices meaningful —
  an edge-local price needs edge-local sites, so both endpoints must
  be CLAIMED locations (D-122's map↔graph coherence).
- INTEGER MATH ONLY, no runtime division anywhere in the derivation:
  lattice cell steps and height-band spreads are already small
  integers; the pack declares the per-unit weights, the engine only
  adds and multiplies.
- Draws NOTHING (INV-2-clean by construction: the price is a pure
  function of pack data + the genesis-frozen model — no stream is
  ever touched, the fingerprint never sees a travel).

The macro-cadence consumer half (edge-state aggregate macro-events,
road-traffic counts) is the space pack's own future row (D-116's
contradiction ledger: "the space-pack return") — the cadence owner
already landed (`core/macro.py`, maclock-1); this module stays the
price law alone.
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Final

from core.intent import IntentData, RunnerError
from core.worldgen import WORLDGEN_BLOCK, lattice_distance

if TYPE_CHECKING:  # the model is a duck-typed argument — no runtime cycle
    from core.worldgen import WorldModel

__all__ = [
    "EDGE_OVERRIDES_KEY",
    "TRAVEL_BLOCK",
    "TRAVEL_KEYS",
    "TravelError",
    "edge_duration",
    "travel_ticks",
]

#: The rules.json block this module reads (`core/pack.py::_travel` owns
#: the load-time shape lint). Absent -> no edge-priced action may exist
#: (the lint's pairing law); an edge-priced action without the block is
#: dead vocabulary, refused at load.
TRAVEL_BLOCK: Final = "travel"

#: The closed vocabulary of the travel block (the lint owns the
#: load-time contract; this is the engine-side mirror the docs cite —
#: one owner per shape, the lint the authority).
TRAVEL_KEYS: Final = ("step_ticks", "climb_ticks", "river_ticks", "edges")

#: The per-edge override list's key (authored prices — the pack wins).
EDGE_OVERRIDES_KEY: Final = "edges"


class TravelError(ValueError):
    """A travel-price contract failure (raw-read surfaces fail loud,
    never with a KeyError — the pred-contract family law, D-111)."""


def _claimed_sites(rules: Mapping[str, Any]) -> dict[str, tuple[int, ...]]:
    """Every claimed location's declared sites, deduplicated and sorted
    (the claims list is pack data — the site is the claim's own
    declaration, never a fold value; a location may claim several slots
    at one site (the committed pack's own twin claims) or, in the
    strictest pack shapes, slots at several sites — the price reads the
    cross-pairs, place-1's own all-cross-pairs discipline)."""
    worldgen = rules.get(WORLDGEN_BLOCK)
    if not isinstance(worldgen, Mapping):
        return {}
    sites: dict[str, set[int]] = {}
    for entry in worldgen.get("claims", ()):
        if isinstance(entry, Mapping):
            location = entry.get("location")
            site = entry.get("site")
            if isinstance(location, str) and isinstance(site, int):
                sites.setdefault(location, set()).add(site)
    return {location: tuple(sorted(values)) for location, values in sites.items()}


def _height_band(height: int, band_edges: Sequence[int]) -> int:
    """The height band index of a site (the pack's `height_bands` edges,
    the same bisect read `_pass_biomes` owns on the drawing side — one
    band vocabulary, two readers; 0..len(edges) small integers, never a
    ratio)."""
    return bisect_right(band_edges, height)


def _weight(
    travel: Mapping[str, Any], key: str, minimum: int, default: int
) -> int:
    """One declared weight, validated loud (the lint owns the load-time
    contract; a hand-built runtime config that skips it fails here with
    the key named — the MacroError backstop family)."""
    value = travel.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise TravelError(
            f"travel.{key} must be an integer >= {minimum}, got {value!r}"
        )
    return value


def _spacing_of(rules: Mapping[str, Any]) -> int:
    """The map's spacing (the lattice metric's other half — the extent
    alone does not fix the column count). The armed-worldgen contract
    guarantees the map block; the backstop is loud for hand-built
    configs (the TravelError family)."""
    spacing = rules.get(WORLDGEN_BLOCK, {}).get("map", {}).get("spacing")
    if not isinstance(spacing, int) or isinstance(spacing, bool) or spacing < 1:
        raise TravelError(
            f"worldgen.map.spacing must be an integer >= 1 for the "
            f"derived travel price, got {spacing!r}"
        )
    return spacing


def travel_ticks(
    rules: Mapping[str, Any],
    world: WorldModel | None,
    origin: str,
    destination: str,
) -> int:
    """The price of one exits edge, in ticks (the accept door's call):

    1. The PACK OVERRIDE wins (an authored per-edge price under
       `travel.edges` — the "pack wins" law, both directions of the
       undirected edge read the same override).
    2. Else the DERIVED price, when both endpoints are CLAIMED
       locations and the world is armed: the minimal cross-pair price
       (the road takes the closest approach between the two grounds —
       place-1 bounds every cross-pair for CORRECTNESS, the price
       reads the cheapest for COST):

           lattice_distance(a, b) * step_ticks
             + abs(band(a) - band(b)) * climb_ticks
             + river_endpoints(a, b) * river_ticks

       — integer add/multiply only, no division anywhere; the height
       modifier is the BAND SPREAD between the endpoints (crossing
       band edges is the climb, the pack's own `height_bands`
       vocabulary), the river modifier counts river-touching endpoints
       (0, 1 or 2 fords). `step_ticks` is required (>= 1 — zero would
       make same-cell edges free); `climb_ticks`/`river_ticks` default
       to 0 (an off modifier is policy, never dead data).
    3. Neither -> NO PRICE: a loud TravelError (the load-time lint
       guarantees full edge coverage for linted packs — a hand-built
       runtime config that skips it fails here with the edge named,
       the MacroError backstop family).
    """
    travel = rules.get(TRAVEL_BLOCK)
    if not isinstance(travel, Mapping):
        raise TravelError(
            "travel_ticks reads an armed travel block — the rules "
            f"declare no {TRAVEL_BLOCK!r} block (the pack lint refuses "
            "an edge-priced action without one; this call is the "
            "runtime backstop for hand-built configs)"
        )
    # 1. the pack override wins — the undirected pair, both directions
    for entry in travel.get(EDGE_OVERRIDES_KEY, ()):
        if not isinstance(entry, Mapping):
            continue
        if {entry.get("from"), entry.get("to")} == {origin, destination}:
            price = entry.get("ticks")
            if (
                not isinstance(price, int)
                or isinstance(price, bool)
                or price < 1
            ):
                raise TravelError(
                    f"travel.edges override {origin!r} <-> "
                    f"{destination!r} reads ticks {price!r} — a positive "
                    "integer is the load-time contract (the lint owns "
                    "it; this is the runtime backstop)"
                )
            return price
    # 2. the derived price — both endpoints claimed, the world armed
    if world is None:
        raise TravelError(
            f"the edge {origin!r} -> {destination!r} carries no override "
            "and the world is unarmed (no generated model to derive "
            "from) — declare a travel.edges override or arm the "
            "worldgen block"
        )
    sites = _claimed_sites(rules)
    origin_sites = sites.get(origin)
    destination_sites = sites.get(destination)
    if not origin_sites or not destination_sites:
        missing = origin if not origin_sites else destination
        raise TravelError(
            f"the edge {origin!r} -> {destination!r} carries no override "
            f"and {missing!r} is an unclaimed location (an edge-local "
            "price needs edge-local sites, D-116 (5) — declare a "
            "travel.edges override or claim the location's sites)"
        )
    step_ticks = _weight(travel, "step_ticks", 1, 0)
    climb_ticks = _weight(travel, "climb_ticks", 0, 0)
    river_ticks = _weight(travel, "river_ticks", 0, 0)
    band_edges: Sequence[int] = (
        rules.get(WORLDGEN_BLOCK, {}).get("biomes", {}).get("height_bands", ())
    )
    best: int | None = None
    for site_a in origin_sites:
        for site_b in destination_sites:
            price = (
                lattice_distance(
                    site_a, site_b, world.extent, _spacing_of(rules)
                )
                * step_ticks
                + abs(
                    _height_band(world.height[site_a], band_edges)
                    - _height_band(world.height[site_b], band_edges)
                )
                * climb_ticks
                + ((site_a in world.rivers) + (site_b in world.rivers))
                * river_ticks
            )
            if best is None or price < best:
                best = price
    assert best is not None  # both site tuples are non-empty here
    return best


def edge_duration(
    rules: Mapping[str, Any],
    world: WorldModel | None,
    projection: Mapping[str, Mapping[str, Any]],
    intent: IntentData,
) -> int:
    """The accept door's edge-priced duration (the loop's branch target
    on `core.intent.EDGE_TICKS`): the actor's LIVE position is the
    origin, the intent's target the destination — the same origin the
    movement resolver's state changes will read at completion (a moved
    projection between accept and completion is the OCC re-check's own
    rejection, never a re-price: the price commits to the completion
    entry the moment it is scheduled). A missing target is the shape
    gate's own author error (RunnerError, the movement twin's
    wording)."""
    if intent.target is None:
        raise RunnerError(
            f"{intent.kind} requires a target location"
        )
    return travel_ticks(
        rules, world, str(projection[intent.actor]["position"]), intent.target
    )
