"""The ordered worldgen passes (depth-5, phase 5; `docs/blueprint/phases.md`
§5 — the phase's build-column headline, TASKS depth-5). The Azgaar +
Red Blob donor discipline: **ordered focused passes over the seed** —
each pass a small algorithm with clear inputs/outputs (L9: a small
alphabet, deep composition), composed into one `WorldModel`. Donor
shapes, not donor bytes: sites (a jittered integer lattice), Lloyd
relaxation (integer centroids), value-noise height/moisture (integer
octaves, fixed-point interpolation that divides out), downhill flow
(the watershed), the biome band table (+ the coastal refinement),
capitals + growth (the states), the chronicle (pre-PC history — DF
"history without a player").

**The geometry discipline (the named cause: Azgaar's cross-engine float
drift; Brogue's fixed-point is the precedent):** the canonical path is
INTEGER-ONLY — every coordinate, height, moisture, distance, and flow
count is a Python int. Floats live in the render layer only
(phases.md §5); a test walks the model and pins the discipline.

**The stream law (D-079's family law's fourth member,**
`core/rng.py::worldgen_stream_name`): every DRAWING pass owns one
content-addressed `worldgen:<pass>` stream; the pure passes (relax,
watershed, biomes) draw nothing — their determinism is by construction.
Arming, re-tuning, adding, or removing a pass shifts neither a canon
check draw nor another pass's draws: the corpus price of worldgen is
the genesis events alone (the isolation law at pass granularity).

**The unarmed law (the 68a pattern):** a pack without the
`rules.json::worldgen` block answers `(None, ())` from `genesis` BEFORE
any stream is touched — zero assures, zero draws, zero events, the v0.1
bytes untouched by construction. The pack's own declaration is the
arming (depth-5b); `core/pack.py::_worldgen` owns the block's shape.

**The arming laws (depth-5b, D-116):** CONDUCTANCE — the genesis event
types must clear the pack's tale gate through the pack's own importance
rule (the lint computes `pack_importance` for both genesis shapes and
refuses a dead arming: template lines that can never render are dead
data; the trap is measured — world_formed scores 0, a history event 1
per_far_hook, against the medium gate's 2). REACHABILITY (L1) — every
armed claim names at least one LIVE consumer: a template line binding
the slot (the flat claim key is the binding surface — `{slot}` and
`{slot?…}` references; the scene-line joins the consumer set at
bridge-1) or a declared director hook reading the (location, slot)
pair through a prop predicate. NO lint ceilings (D-116: geo-1 is the
wall's answer, the queue order the enforcement).

**The claim gate (`core/detail.py::detail_claim`) — the first legal
caller, pinned since depth-2:** the worldgen never writes a scene slot
directly. Each pack-declared claim `{location, slot, field, site}` reads
its value from the model and is validated against the committed log
through the gate — `commit` rides the world-forming event's
`state_changes`; `no_op` (canon already holds the value — the
idempotent duplicate) is skipped; `slot_conflict` is refused with the
cause chain, recorded in the event's outcome. First-commit-wins for the
claimer, canon outranks the generator — never a second write path
beside the ledger/promotion door.

**The genesis (pre-PC history, chron-2's DF legends shape):** `WorldModel`
is DERIVED data (a pure function of seed + pack config, rebuildable,
never truth — L11); the world's canon-visible facts ride EVENTS like
everything else (INV-1). `genesis_drafts` builds them: event 0 =
`world_formed` (the map's shape in the outcome + the committed claims
as births, `from` None — the canon-birth shape of the texture
promotion), then history events in ascending macro-year — each carrying
the DF legends event shape (`outcome: {kind, year, participants,
places}` + `collection` when grouped): PARTICIPANTS are two distinct
region ids (the DF war's attacker/defender — the pair is drawn once at
the collection's root anchor and INHERITED by its members, the DF
collection-role shape; independents draw their own), PLACES are site
indices (one drawn per event, the DF `site_id`), and the COLLECTION
field names the tier a grouped event belongs to. The war→battle→episode
hierarchy is a PACK-DECLARED collection vocabulary (the DF
`event_collections` donor shape, L10: JSON in the rules, linted —
never string languages): the pack's `chronicle.collections` lists the
tiers root-first, each `{type, kinds}` (the root anchors) or
`{type, kinds, members}` (the nested tiers carry the member caps);
HISTORY_KINDS stays closed — the four engine verbs are the kinds the
tiers may name, the collection types are the pack's own layer. The
walk is DRAW-FREE (a pure function of the drawn kinds and the
declaration — DF measured: only a minority of events sit in any
collection; the grouping is opportunistic, not structural). Micro-ticks
and macro-years are layered clocks, the same authority at two
granularities (L4). History events carry NO knowledge records (the DF
discipline measured at bg-2: DF history is canon-dense,
epistemology-empty — the world the PC walks into has a past nobody
knows) and carry the pack-declared hook tags that seed the director's
initial buffer (D-005: a complication is seeded at event time — here,
at world time). The CAUSE is the chron-2 law (L7 — the chain visible
at record time): the drafts ride a PARENT MAP (draft indices, -1 = the
run-start `world_formed`) — a collection member chains to its nearest
lower-tier predecessor in the run, a top-level event (an anchor or an
independent) to the previous top-level event. The loop commits the
drafts through the one canon door (`Simulator._commit`), resolving the
parents through the writer's own ids (the id law stays the writer's
single owner). `events_max` caps the genesis — log growth
O(declared), never O(years).

Not here (phases.md §5/§7): populations as macro-tick aggregates (the
group family, depth-7 — the first tranche seeds the map, the claims,
and the buffer); the lazy mid-run materialization door (a site's passes
re-running against a non-empty log — the claim gate's conflict/no_op
verdicts are that door's law, pinned here by tests, live the day the
door lands); the region entities as projection citizens (one id all
tiers is the depth-7 row).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from core.detail import COMMIT, detail_claim
from core.intent import pack_importance
from core.log import EventDraft, EventRecord, StateChange
from core.rng import RngBank, worldgen_stream_name
from core.transitions import WORLD

__all__ = [
    "BIOMES",
    "FIELD_MAX",
    "CLAIM_FIELDS",
    "HISTORY_KINDS",
    "PASS_ORDER",
    "RESERVED_CLAIM_SLOTS",
    "WORLDGEN_BLOCK",
    "HistoryDraw",
    "ResolvedClaim",
    "WorldModel",
    "genesis",
    "generate_world",
    "genesis_drafts",
    "resolve_claims",
]

#: The rules.json block this module reads (the arming; `core/pack.py::
#: _worldgen` owns the shape lint). Absent -> the unarmed law.
WORLDGEN_BLOCK: Final = "worldgen"

#: The ordered pass pipeline (the Azgaar/Red Blob shapes). The DRAWING
#: passes (sites, height, moisture, states, chronicle) each own one
#: `worldgen:<pass>` stream; the pure passes (relax, watershed,
#: biomes) draw nothing.
PASS_ORDER: Final = (
    "sites",
    "relax",
    "height",
    "moisture",
    "watershed",
    "biomes",
    "states",
    "chronicle",
)

#: The closed biome vocabulary (the band table + the coastal rule).
#: World-gen vocabulary, not setting nouns (INV-3): the pack's claims
#: carry the values into slots; the biome names never live in
#: `content/`.
BIOMES: Final = (
    "ocean",
    "coast",
    "desert",
    "plain",
    "marsh",
    "hills",
    "forest",
    "mountain",
)

#: The claim-field closed set: which model read a claim's value takes.
CLAIM_FIELDS: Final = ("biome", "height", "region", "river")

#: The claim slots' reserved vocabulary (depth-5b + chron-2): a slot
#: colliding with the world_formed outcome's fixed keys is CLOBBERED
#: (the flat claim keys write after them), a slot named for the render
#: context's derived slots is SHADOWED (`render/chronicle.py::
#: _event_context` writes the derived slots first, so the claim's flat
#: key would never surface — restated here because core may not import
#: render; the lint refuses the collision either way), and a slot
#: named for a HISTORY event's outcome key is a BRANCH FAKE (chron-2:
#: the line's `{year?…}` conditional branches on the outcome shape — a
#: claim slot named `year` would flip world_formed's render to the
#: history arm, `participants`/`places`/`collection` would collide
#: with the history events' own fields across the genesis family).
#: The flat keys are the template binding surface — the reachability
#: law's live consumer.
RESERVED_CLAIM_SLOTS: Final = (
    # the world_formed outcome's fixed keys
    "kind", "sites", "regions", "years", "claims", "refused",
    # the history events' outcome keys (chron-2, the DF legends shape)
    "year", "participants", "places", "collection",
    # the render context's derived slots
    "t", "event_type", "actor", "target", "target_location",
    "location", "action_label", "knows", "fidelity", "axes",
    "texture_slot",
)

#: The closed history-kind vocabulary (the chronicle pass's draws) —
#: generic history verbs, never setting nouns (INV-3).
HISTORY_KINDS: Final = (
    "settlement_founded",
    "war_fought",
    "pact_signed",
    "lineage_ended",
)

#: The fixed-point scale of the bilinear interpolation (divides out
#: before any value is stored — the integer discipline).
_SCALE: Final = 1024

#: The height/moisture ceiling: the noise octaves normalize into
#: 0..9999 so the pack's band edges live in one fixed range regardless
#: of the octave count (the pack lint's band-edge bound reads the same
#: constant — one owner).
FIELD_MAX: Final = 9999

#: The biome band table: (height band, moisture band) -> biome. Four
#: bands per axis (the pack declares the three edges of each); the
#: coastal refinement rewrites height-band-1 cells that neighbor an
#: ocean cell (Azgaar's coast detection).
_BIOME_TABLE: Final[dict[tuple[int, int], str]] = {
    (0, 0): "ocean",
    (0, 1): "ocean",
    (0, 2): "ocean",
    (0, 3): "ocean",
    (1, 0): "desert",
    (1, 1): "plain",
    (1, 2): "plain",
    (1, 3): "marsh",
    (2, 0): "desert",
    (2, 1): "hills",
    (2, 2): "forest",
    (2, 3): "marsh",
    (3, 0): "mountain",
    (3, 1): "mountain",
    (3, 2): "mountain",
    (3, 3): "mountain",
}

#: The sub-blocks of the worldgen config (the lint's closed key set).
_SUB_BLOCKS: Final = ("map", "biomes", "watershed", "states", "chronicle", "claims")

#: The required ints of each sub-block (the runtime raw-read backstop;
#: the lint owns the full contract at load).
_REQUIRED: Final[dict[str, tuple[str, ...]]] = {
    "map": ("extent", "spacing", "jitter", "relax_rounds",
            "height_octaves", "moisture_octaves"),
    "biomes": ("height_bands", "moisture_bands"),
    "watershed": ("neighbors", "river_flow"),
    "states": ("capitals",),
    "chronicle": ("years", "events_max", "event_type", "hooks"),
}


class WorldgenError(ValueError):
    """A worldgen config or claim shape error, loud before the world
    answer (the `_require` family law, D-111 — KeyError/IndexError
    never leak). Load-time shapes are the pack lint's; this is the
    raw-read backstop for runtime-constructed configs."""


def _require_config(config: Mapping[str, Any]) -> None:
    """The runtime shape backstop (D-111): every key the passes read is
    present and of the right kind — a hand-built config goes loud with
    the missing key NAMED, never a KeyError from the fold."""
    for block in _SUB_BLOCKS:
        if block not in config:
            raise WorldgenError(
                f"worldgen config missing the {block!r} block "
                f"(the lint owns the full contract — see core/pack.py)"
            )
        value = config[block]
        if block == "claims":
            if not isinstance(value, list):
                raise WorldgenError("worldgen.claims must be a list")
            for entry in value:
                if not isinstance(entry, Mapping):
                    raise WorldgenError(
                        "worldgen.claims entries must be objects "
                        "(the closed vocabulary: location | slot | field | site)"
                    )
            continue
        if not isinstance(value, Mapping):
            raise WorldgenError(f"worldgen.{block} must be an object")
        if block == "chronicle":
            # chron-2: the optional collection tiers — each entry an
            # object carrying `type` + `kinds` (+ `members` past the
            # root); the LINT owns the full closed vocabulary, this is
            # the raw-read backstop (the walk reads these keys).
            tiers = value.get("collections")
            if isinstance(tiers, list):
                for index, tier in enumerate(tiers):
                    if not isinstance(tier, Mapping):
                        raise WorldgenError(
                            "worldgen.chronicle.collections entries must "
                            "be objects (the tier vocabulary: type | kinds "
                            "| members)"
                        )
                    for key in ("type", "kinds") + (
                        ("members",) if index else ()
                    ):
                        if key not in tier:
                            raise WorldgenError(
                                f"worldgen.chronicle.collections[{index}] "
                                f"is missing the {key!r} key (the lint owns "
                                "the full contract)"
                            )
        for key in _REQUIRED.get(block, ()):
            if key not in value:
                raise WorldgenError(
                    f"worldgen.{block}.{key} is required (the lint owns "
                    "the full contract)"
                )


@dataclass(frozen=True, slots=True)
class WorldModel:
    """The generated world: a pure function of (seed, pack config) —
    derived, rebuildable, never truth (L11). INTEGER-ONLY by
    construction (the geometry discipline). All per-site sequences are
    index-aligned (`sites[i]` <-> `height[i]` <-> `biomes[i]` ...)."""

    extent: int
    sites: tuple[tuple[int, int], ...]
    height: tuple[int, ...]
    moisture: tuple[int, ...]
    biomes: tuple[str, ...]
    flow: tuple[int, ...]
    rivers: frozenset[int]
    regions: tuple[str, ...]
    capitals: frozenset[int]
    years: int

    def claim_value(self, field: str, site: int) -> Any:
        """One claim's model read (the closed CLAIM_FIELDS set; the
        site bound is checked loud — the raw-read backstop)."""
        if field not in CLAIM_FIELDS:
            raise WorldgenError(
                f"claim field {field!r} is not in the closed set "
                f"{list(CLAIM_FIELDS)}"
            )
        if not 0 <= site < len(self.sites):
            raise WorldgenError(
                f"claim site {site} is outside 0..{len(self.sites) - 1} "
                "(the site count is (extent // spacing)^2 — the lint "
                "cross-checks it; a hand-built config goes loud here)"
            )
        if field == "biome":
            return self.biomes[site]
        if field == "height":
            return self.height[site]
        if field == "region":
            return self.regions[site]
        return site in self.rivers  # "river"


@dataclass(frozen=True, slots=True)
class ResolvedClaim:
    """One claim's answer from the gate: the spec echo (location, slot),
    the model-read value, the verdict (`core/detail.py`'s
    commit/no_op/slot_conflict), and the refusing cause (the winning
    event's id — the authority the claim conflicted with; None unless
    refused)."""

    location: str
    slot: str
    value: Any
    outcome: str
    cause: str | None

    @property
    def refused(self) -> bool:
        return self.outcome == "slot_conflict"


@dataclass(frozen=True, slots=True)
class HistoryDraw:
    """One drawn pre-PC history event, the DF legends shape (chron-2):
    the pass-1 draw (kind, macro-year, hook tag), the participants (two
    distinct region ids — the run's ROOT ANCHOR's draw, inherited by the
    members: the DF collection's role fields; an independent's own),
    the place (one site index, per event — the DF `site_id`), and the
    walk's answers: the collection tier's pack-declared type (None =
    independent) and the cause parent (the DRAFT index it chains to:
    0 = world_formed, i+1 = history event i — L7, the chain recorded
    at draw time)."""

    kind: str
    year: int
    tag: str
    participants: tuple[str, str]
    place: int
    collection: str | None
    parent: int


# -- the passes (each a focused algorithm; drawing passes own a stream) ------


def _pass_sites(
    bank: RngBank, config: Mapping[str, Any]
) -> tuple[tuple[int, int], ...]:
    """The lattice pass: (extent // spacing)^2 sites at the cell
    centers, each jittered ±jitter on both axes (drawn per site,
    row-major — construction order, INV-2). Coordinates stay integers
    inside [0, extent)."""
    extent = int(config["extent"])
    spacing = int(config["spacing"])
    jitter = int(config["jitter"])
    sites: list[tuple[int, int]] = []
    with bank.assure(worldgen_stream_name("sites")):
        for row in range(extent // spacing):
            for col in range(extent // spacing):
                x = col * spacing + spacing // 2 + bank.randint(-jitter, jitter)
                y = row * spacing + spacing // 2 + bank.randint(-jitter, jitter)
                sites.append((x, y))
    return tuple(sites)


def _pass_relax(
    config: Mapping[str, Any], sites: Sequence[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    """One Lloyd-relaxation round (the Red Blob Voronoi+Lloyd shape) in
    integers: partition the extent×extent lattice points by nearest
    site (squared distance, ties by site index), move each site to its
    cell's centroid (round-half-up integer division). Pure — no draws;
    `relax_rounds` repeats it. A site whose cell empties (swallowed by
    a neighbor after a move) keeps its position — the degenerate-cell
    law."""
    extent = int(config["extent"])
    rounds = int(config["relax_rounds"])
    current = list(sites)
    for _ in range(max(0, rounds)):
        sums: list[list[int]] = [[0, 0, 0] for _ in current]  # x, y, count
        for y in range(extent):
            for x in range(extent):
                best = min(
                    range(len(current)),
                    key=lambda i: (
                        (x - current[i][0]) ** 2 + (y - current[i][1]) ** 2,
                        i,
                    ),
                )
                sums[best][0] += x
                sums[best][1] += y
                sums[best][2] += 1
        moved = list(current)
        for i, (total_x, total_y, count) in enumerate(sums):
            if count:
                moved[i] = (
                    (total_x * 2 + count) // (2 * count),
                    (total_y * 2 + count) // (2 * count),
                )
        current = moved
    return tuple(current)


def _octave_noise(
    bank: RngBank,
    stream: str,
    extent: int,
    spacing: int,
    octaves: int,
    sites: Sequence[tuple[int, int]],
) -> tuple[int, ...]:
    """Value noise (the Red Blob shape) over the sites: per octave a
    lattice of node values (drawn row-major on the pass's own stream),
    bilinearly interpolated per site with fixed-point weights that
    divide out; the octave amplitude halves per octave; the sum
    normalizes into 0..9999 so the pack's band edges live in one fixed
    range regardless of the octave count. Integer-only."""
    values: list[int] = [0] * len(sites)
    total_amp = 0
    amplitude = FIELD_MAX
    for octave in range(max(1, octaves)):
        step = max(1, spacing >> octave)
        node_axis = list(range(0, extent, step))
        grid: dict[tuple[int, int], int] = {}
        with bank.assure(stream):
            for ny in node_axis:
                for nx in node_axis:
                    grid[(nx, ny)] = bank.randint(0, FIELD_MAX)
        last = node_axis[-1]
        for i, (x, y) in enumerate(sites):
            x0 = (x // step) * step
            y0 = (y // step) * step
            x1 = x0 + step if x0 + step <= last else last
            y1 = y0 + step if y0 + step <= last else last
            fx = ((x - x0) * _SCALE) // max(1, x1 - x0)
            fy = ((y - y0) * _SCALE) // max(1, y1 - y0)
            v00 = grid[(x0, y0)]
            v10 = grid[(x1, y0)]
            v01 = grid[(x0, y1)]
            v11 = grid[(x1, y1)]
            cell = (
                v00 * (_SCALE - fx) * (_SCALE - fy)
                + v10 * fx * (_SCALE - fy)
                + v01 * (_SCALE - fx) * fy
                + v11 * fx * fy
            ) // (_SCALE * _SCALE)
            values[i] += cell * amplitude
        total_amp += amplitude
        amplitude //= 2
    # normalize: the weighted octave sum spans [0, FIELD_MAX * total_amp],
    # so one division by total_amp lands it back in [0, FIELD_MAX]
    return tuple(value // total_amp for value in values)


def _neighbors(
    sites: Sequence[tuple[int, int]], k: int
) -> tuple[tuple[int, ...], ...]:
    """The k nearest sites per site (squared integer distance, ties by
    index — the Delaunay-adjacency surrogate the watershed and the
    coastal refinement read). Pure."""
    result: list[tuple[int, ...]] = []
    for i, (x, y) in enumerate(sites):
        ranked = sorted(
            ((x - sx) ** 2 + (y - sy) ** 2, j)
            for j, (sx, sy) in enumerate(sites)
            if j != i
        )
        result.append(tuple(j for _, j in ranked[:k]))
    return tuple(result)


def _pass_watershed(
    config: Mapping[str, Any],
    sites: Sequence[tuple[int, int]],
    height: Sequence[int],
) -> tuple[tuple[int, ...], frozenset[int]]:
    """The downhill flow (the Red Blob watershed): sites in
    height-DESCENDING order (ties by index — INV-2) each pass their
    accumulated flow to their lowest-height neighbor; a site lower than
    all neighbors is a sink (its flow stays). Rivers = sites whose
    accumulated flow reaches the pack-declared threshold. Pure."""
    k = int(config["neighbors"])
    threshold = int(config["river_flow"])
    neighbor_sets = _neighbors(sites, k)
    flow = [1] * len(sites)
    order = sorted(range(len(sites)), key=lambda i: (-height[i], i))
    for i in order:
        lower = [j for j in neighbor_sets[i] if height[j] < height[i]]
        if lower:
            target = min(lower, key=lambda j: (height[j], j))
            flow[target] += flow[i]
    rivers = frozenset(i for i, f in enumerate(flow) if f >= threshold)
    return tuple(flow), rivers


def _band(value: int, edges: Sequence[int]) -> int:
    """The band index of `value` under three ascending edges (0..3)."""
    for index, edge in enumerate(edges):
        if value < edge:
            return index
    return len(edges)


def _pass_biomes(
    config: Mapping[str, Any],
    sites: Sequence[tuple[int, int]],
    height: Sequence[int],
    moisture: Sequence[int],
) -> tuple[str, ...]:
    """The biome table: (height band × moisture band) -> biome over the
    pack-declared edges, then the coastal refinement (height-band-1
    sites neighboring an ocean site become coast — Azgaar's coast
    detection over the same neighbor structure the watershed reads).
    Pure."""
    biome_cfg = config["biomes"]
    k = int(config["watershed"]["neighbors"])
    neighbor_sets = _neighbors(sites, k)
    base = [
        _BIOME_TABLE[
            (_band(height[i], biome_cfg["height_bands"]),
             _band(moisture[i], biome_cfg["moisture_bands"]))
        ]
        for i in range(len(sites))
    ]
    result = list(base)
    for i in range(len(sites)):
        if _band(height[i], biome_cfg["height_bands"]) == 1 and any(
            base[j] == "ocean" for j in neighbor_sets[i]
        ):
            result[i] = "coast"
    return tuple(result)


def _pass_states(
    bank: RngBank, config: Mapping[str, Any],
    sites: Sequence[tuple[int, int]],
) -> tuple[tuple[str, ...], frozenset[int]]:
    """The capitals + growth (the Azgaar states shape): the pack's
    count of capitals drawn as distinct site indices (then sorted —
    region ids are stable across draw orders), then every site joins
    its nearest capital (squared distance, ties by the lower region
    index). Region ids `region_00..` are engine vocabulary, never pack
    data."""
    count = int(config["capitals"])
    chosen: list[int] = []
    with bank.assure(worldgen_stream_name("states")):
        attempts = 0
        target = min(count, len(sites))
        while len(chosen) < target and attempts < 10 * count:
            pick = bank.randint(0, len(sites) - 1)
            if pick not in chosen:
                chosen.append(pick)
            attempts += 1
        if len(chosen) < target:
            raise WorldgenError(
                f"states.capitals {count} could not be drawn distinctly "
                f"over {len(sites)} sites"
            )
    chosen.sort()
    regions: list[str] = []
    for x, y in sites:
        owner = min(
            range(len(chosen)),
            key=lambda r: (
                (x - sites[chosen[r]][0]) ** 2 + (y - sites[chosen[r]][1]) ** 2,
                r,
            ),
        )
        regions.append(f"region_{owner:02d}")
    return tuple(regions), frozenset(chosen)


def _walk_collections(
    kinds: Sequence[str],
    tiers: Sequence[Mapping[str, Any]] | None,
) -> tuple[list[str | None], list[int], list[int]]:
    """Group the year-sorted kinds into collection runs (chron-2, the
    DF `event_collections` tree over the single-parent cause chain).
    ZERO DRAWS — a pure function of the drawn kinds and the pack's
    declaration (root tier first). A run opens at a root-tier kind;
    the following events join while their kinds match a NESTED tier
    (searched from tier 1 up, the first match) and that tier's member
    count is under its cap; anything else — a root kind, an
    unaffiliated kind, a capped tier — CLOSES the run, and the closing
    event re-processes fresh (a root kind opens the next run, an
    unaffiliated kind goes independent). Returns per event: the
    collection tier's TYPE (None = independent), the assigned TIER
    index (-1 = independent), and the cause parent in HISTORY index
    space (-1 = world_formed) — a member chains to its nearest
    preceding STRICTLY-lower-tier event in the run (the anchor is
    tier 0, always found), a top-level event to the previous
    top-level event (never a run member: the sagas chain, not the
    episodes)."""

    n = len(kinds)
    collection: list[str | None] = [None] * n
    tier_of: list[int] = [-1] * n
    parent: list[int] = [-1] * n
    if tiers is None:
        # the flat form (no vocabulary declared): every event
        # top-level, the linear chain — the iter-86 law preserved.
        for i in range(n):
            parent[i] = i - 1
        return collection, tier_of, parent
    root_kinds = frozenset(tiers[0]["kinds"])
    nested = tuple(
        (t, frozenset(tiers[t]["kinds"])) for t in range(1, len(tiers))
    )
    last_top = -1
    i = 0
    while i < n:
        if kinds[i] in root_kinds:
            tier_of[i] = 0
            collection[i] = str(tiers[0]["type"])
            parent[i] = last_top
            last_top = i
            counts: dict[int, int] = {}
            j = i + 1
            while j < n:
                member_tier = next(
                    (t for t, k in nested if kinds[j] in k), None
                )
                if member_tier is None:
                    break
                if counts.get(member_tier, 0) >= int(tiers[member_tier]["members"]):
                    break
                counts[member_tier] = counts.get(member_tier, 0) + 1
                tier_of[j] = member_tier
                collection[j] = str(tiers[member_tier]["type"])
                parent[j] = next(
                    k for k in range(j - 1, i - 1, -1)
                    if tier_of[k] < member_tier
                )
                j += 1
            i = j
        else:
            parent[i] = last_top
            last_top = i
            i += 1
    return collection, tier_of, parent


def _pass_chronicle(
    bank: RngBank, config: Mapping[str, Any], model: WorldModel,
) -> tuple[HistoryDraw, ...]:
    """The chronicle draws (the Azgaar chronology shape + the DF
    legends event shape, chron-2): TWO passes over the one
    `worldgen:chronicle` stream. Pass 1 draws exactly the depth-5
    triple per event (year, kind, hook tag) in index order — those
    stream positions are FROZEN (the murmur's pre-seed corpus pins
    ride them; re-tuning the shape may not move the drawn content),
    then sorts by year (log order = chronology order — the INV-2
    output discipline). The WALK groups the sorted kinds into
    collections per the pack-declared tier vocabulary — zero draws, a
    pure function of the drawn kinds and the declaration. Pass 2
    draws the DF legends shape: per top-level event (an anchor or an
    independent) TWO DISTINCT regions (the offset draw — always
    distinct, always two draws; the members INHERIT the root anchor's
    pair, the DF collection's role fields), per event ONE site (the
    place). `events_max` counts the WHOLE genesis: event 0 is
    world_formed, so history draws events_max - 1."""
    chronicle = config["chronicle"]
    years = int(chronicle["years"])
    events_max = int(chronicle["events_max"])
    hook_tags = list(chronicle["hooks"])
    tiers = chronicle.get("collections")
    history_count = max(0, events_max - 1)
    drawn: list[tuple[int, str, str]] = []
    with bank.assure(worldgen_stream_name("chronicle")):
        for _ in range(history_count):
            year = bank.randint(1, years)
            kind = HISTORY_KINDS[bank.randint(0, len(HISTORY_KINDS) - 1)]
            tag = hook_tags[bank.randint(0, len(hook_tags) - 1)]
            drawn.append((year, kind, tag))
        drawn.sort(key=lambda item: (item[0],))
        collection, tier, parent = _walk_collections(
            [kind for _year, kind, _tag in drawn], tiers
        )
        regions = sorted(set(model.regions))
        if len(regions) < 2:
            raise WorldgenError(
                "the chronicle's history events need two distinct "
                f"regions for their participants — the states pass drew "
                f"{len(regions)} (states.capitals >= 2, the DF war shape; "
                "the lint owns the full contract)"
            )
        site_count = len(model.sites)
        history: list[HistoryDraw] = []
        for index, (year, kind, tag) in enumerate(drawn):
            if tier[index] <= 0:  # an anchor (0) or an independent (-1)
                first = bank.randint(0, len(regions) - 1)
                second = (
                    first + 1 + bank.randint(0, len(regions) - 2)
                ) % len(regions)
                pair = (regions[first], regions[second])
            else:
                # the members inherit the run's ROOT anchor's pair —
                # the DF collection's role fields (the anchor precedes
                # its members in the sorted order, so the pair is drawn)
                anchor = next(
                    a for a in range(index - 1, -1, -1) if tier[a] == 0
                )
                pair = history[anchor].participants
            history.append(
                HistoryDraw(
                    kind=kind, year=year, tag=tag, participants=pair,
                    place=bank.randint(0, site_count - 1),
                    collection=collection[index],
                    parent=parent[index] + 1,  # draft space: 0 = world_formed
                )
            )
    return tuple(history)


# -- the one door --------------------------------------------------------------


def genesis(
    bank: RngBank, rules: Mapping[str, Any], events: Sequence[EventRecord],
    seed: int,
) -> tuple[WorldModel | None, tuple[EventDraft, ...], tuple[int, ...]]:
    """The one door the loop calls at open time: generate the world from
    the seed, validate the pack's claims against the committed log
    through the claim gate, and build the genesis drafts with their
    PARENT MAP (draft indices into the drafts tuple, -1 = the run-start
    world_formed — chron-2's L7 law: the loop resolves each parent into
    the writer's own event id at commit time). An UNARMED
    pack (no `worldgen` block) answers `(None, (), ())` BEFORE any stream
    is touched — the 68a pattern; the v0.1 bytes are untouched by
    construction. The armed arm's corpus price is the genesis events
    alone: the worldgen streams are isolated from the substantive canon
    checks (the family law), so the run's canon draws never move."""
    config = rules.get(WORLDGEN_BLOCK)
    if config is None:
        return None, (), ()
    _require_config(config)
    model = generate_world(bank, config)
    claims = resolve_claims(events, model, config["claims"])
    history = _pass_chronicle(bank, config, model)
    drafts, parents = genesis_drafts(
        model, claims, config, history, rules, seed
    )
    return model, drafts, parents


def generate_world(bank: RngBank, config: Mapping[str, Any]) -> WorldModel:
    """Run the ordered passes over the seed and build the model. Pass
    order is `PASS_ORDER`; each drawing pass runs inside its own
    content-addressed `worldgen:<pass>` assure scope, so the passes are
    draw-isolated from each other and from the canon checks."""
    _require_config(config)
    sites = _pass_sites(bank, config["map"])
    sites = _pass_relax(config["map"], sites)
    height = _octave_noise(
        bank, worldgen_stream_name("height"),
        int(config["map"]["extent"]), int(config["map"]["spacing"]),
        int(config["map"]["height_octaves"]), sites,
    )
    moisture = _octave_noise(
        bank, worldgen_stream_name("moisture"),
        int(config["map"]["extent"]), int(config["map"]["spacing"]),
        int(config["map"]["moisture_octaves"]), sites,
    )
    flow, rivers = _pass_watershed(config["watershed"], sites, height)
    biomes = _pass_biomes(config, sites, height, moisture)
    regions, capitals = _pass_states(bank, config["states"], sites)
    return WorldModel(
        extent=int(config["map"]["extent"]),
        sites=sites,
        height=height,
        moisture=moisture,
        biomes=biomes,
        flow=flow,
        rivers=rivers,
        regions=regions,
        capitals=capitals,
        years=int(config["chronicle"]["years"]),
    )


def resolve_claims(
    events: Sequence[EventRecord],
    model: WorldModel,
    specs: Sequence[Mapping[str, Any]],
) -> tuple[ResolvedClaim, ...]:
    """Validate the pack's worldgen claims against the committed log
    through `core/detail.py::detail_claim` — the gate's first legal
    caller (pinned at depth-2, live here). Each spec is
    `{location, slot, field, site}`; the value is the model read. The
    loop's own lazy draw never calls the gate (it skips canon slots
    before drawing); the worldgen — an external claimer — must: canon
    outranks the generator, first-commit-wins for the claimer, never a
    second write path. At open time the log is empty, so every legal
    claim commits; the no_op/conflict verdicts are the future lazy
    mid-run door's law (pinned by tests)."""
    resolved: list[ResolvedClaim] = []
    for spec in specs:
        location = str(spec["location"])
        slot = str(spec["slot"])
        value = model.claim_value(str(spec["field"]), int(spec["site"]))
        verdict = detail_claim(events, location, slot, value)
        resolved.append(
            ResolvedClaim(
                location=location, slot=slot, value=value,
                outcome=verdict.outcome, cause=verdict.cause,
            )
        )
    return tuple(resolved)


def genesis_drafts(
    model: WorldModel,
    claims: Sequence[ResolvedClaim],
    config: Mapping[str, Any],
    history: Sequence[HistoryDraw],
    rules: Mapping[str, Any],
    seed: int,
) -> tuple[tuple[EventDraft, ...], tuple[int, ...]]:
    """Build the pre-PC genesis events + their cause parent map.
    Event 0 = `world_formed`: the map's shape in the outcome + the
    COMMIT verdicts' claims as canon births (`StateChange(location,
    slot, None -> value)`) + the refused claims with their cause chains
    (both keys present only when non-empty — the drifted_from law).
    Then the history events in ascending macro-year — the DF legends
    shape (`outcome: {kind, year, participants, places}` + `collection`
    when grouped; the participants/places ride canon as LISTS, the
    tracery value-rendering law joins them at render time), the drawn
    hook tags, NO knowledge records (the DF discipline: history is
    canon-dense, epistemology-empty). Importance rides the pack's own
    rule (`pack_importance` — one rule for action events and world
    events). The CAUSE is the chron-2 law (L7 — the chain visible at
    record time): the drafts carry `cause: None` and the returned
    PARENT MAP (draft indices, -1 = the run-start world_formed)
    carries the semantic tree — the loop resolves the parents through
    the writer's own ids as it commits (the id law stays the writer's
    single owner, the chain the worldgen's semantic one)."""
    event_type = str(config["chronicle"]["event_type"])
    committed = [claim for claim in claims if claim.outcome == COMMIT]
    refused = [claim for claim in claims if claim.refused]
    outcome: dict[str, Any] = {
        "kind": "world_formed",
        "sites": len(model.sites),
        "regions": len(model.capitals),
        "years": model.years,
    }
    if committed:
        outcome["claims"] = [
            {"slot": claim.slot, "value": claim.value} for claim in committed
        ]
        # depth-5b: each committed claim's slot rides the outcome as a
        # FLAT key — the template binding surface (D-116 (4): the line
        # binds it through `_event_context`; the `claims` list stays
        # the structured record, the flat key is the render surface —
        # two jobs, two shapes). Written AFTER the fixed keys, so the
        # lint's RESERVED_CLAIM_SLOTS collision law is the backstop.
        for claim in committed:
            outcome[claim.slot] = claim.value
    if refused:
        outcome["refused"] = [
            {"slot": claim.slot, "cause": claim.cause} for claim in refused
        ]
    state_changes = tuple(
        StateChange(
            entity=claim.location, prop=claim.slot, from_=None,
            to_=claim.value,
        )
        for claim in committed
    )
    entities = {change.entity for change in state_changes}
    drafts = [
        EventDraft(
            t=0,
            type=event_type,
            actor=WORLD,
            cause=None,
            outcome=outcome,
            knowledge=(),
            state_changes=state_changes,
            hooks=(),
            importance=pack_importance(
                rules, entities, irreversible=0, hooks=0,
                event_type=event_type,
            ),
            provenance={"seed": seed, "worldgen": True},
        )
    ]
    parents: list[int] = [-1]
    for draw in history:
        history_outcome: dict[str, Any] = {
            "kind": draw.kind,
            "year": draw.year,
            "participants": list(draw.participants),
            "places": [draw.place],
        }
        if draw.collection is not None:
            history_outcome["collection"] = draw.collection
        drafts.append(
            EventDraft(
                t=0,
                type=event_type,
                actor=WORLD,
                cause=None,
                outcome=history_outcome,
                knowledge=(),
                state_changes=(),
                hooks=(draw.tag,),
                importance=pack_importance(
                    rules, set(), irreversible=0, hooks=1,
                    event_type=event_type,
                ),
                provenance={"seed": seed, "worldgen": True},
            )
        )
        parents.append(draw.parent)
    return tuple(drafts), tuple(parents)
