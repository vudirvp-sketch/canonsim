"""The worldgen block lint (depth-5; mechanics in `core/worldgen.py`,
the genesis wiring in `core/loop.py::open`, the streams in
`core/rng.py::worldgen_stream_name`) — plus roads-1's `worldgen.roads`
sub-block (the overlay knob). The D-175 split's worldgen family."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.intent import pack_importance
from core.log import IMPORTANCE_ORDER
from core.packlint.helpers import (
    _BRACE_COND,
    _BRACE_SLOT,
    PackError,
    _bound_template_slots,
    _director_prop_reads,
    _is_int,
    _require,
)
from core.worldgen import (
    CLAIM_FIELDS,
    FIELD_MAX,
    HISTORY_KINDS,
    RESERVED_CLAIM_SLOTS,
    WORLDGEN_BLOCK,
    lattice_distance,
)

# The worldgen block's closed sub-block and map-key vocabularies
# (depth-5; `core/worldgen.py` owns the pass semantics, the lint owns
# the shape).
WORLDGEN_SUB_BLOCKS: Final = (
    "map",
    "biomes",
    "watershed",
    "states",
    "chronicle",
    "claims",
    "place",
    "roads",
)
WORLDGEN_MAP_KEYS: Final = (
    "extent",
    "spacing",
    "jitter",
    "relax_rounds",
    "height_octaves",
    "moisture_octaves",
)


class WorldgenLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _worldgen(self) -> None:
        """The worldgen contract (depth-5, `phases.md` §5 — the ordered
        passes' config home; mechanics in `core/worldgen.py`, the
        genesis wiring in `core/loop.py::open`, the streams in
        `core/rng.py::worldgen_stream_name`). The block is OPTIONAL and
        lives at rules.json top level (`worldgen`); a pack without it
        runs the v0.1 bytes, byte-identically (the pack's own
        declaration is the arming — the 68a pattern, depth-5b). Closed
        key vocabulary per sub-block; every value an explicit integer
        (a default would be a second config surface — D-024). The
        cross-lints: the chronicle event type must live in the template
        vocabulary (EVENT_SCHEMA §11 — closed per pack); the chronicle
        hook tags must be DECLARED director hooks (a genesis hook the
        director does not know is dead data); the claims' site index
        must name a generated site (the site count is
        (extent // spacing)^2); the claims' slots obey the
        double-claim law family — never modeled by the location entity
        (the scene_detail law verbatim: lazy/worldgen detail occupies
        only slots canon does not model), never declared in
        scene_detail for the same location (the overlap refusal: the
        genesis claims at open time, before any observation, so the
        scene's lazy draw could never fire — dead pack data), never in
        the reserved flat-key vocabulary (a colliding slot is clobbered
        or shadowed, never bound), and the (location, slot) pairs are
        unique within the block (a double claim is the
        double-declaration refusal). The depth-5b laws (D-116):
        CONDUCTANCE — the genesis event types must clear the tale gate
        through the pack's own importance rule (dead template lines
        are dead data); REACHABILITY (L1) — every armed claim names at
        least one live consumer (a template line binding the slot, a
        declared director hook reading the pair, or the scene line
        declaring the slot — bridge-1's brief-side consumer arm). The
        chron-2 laws (the history bridge): the chronicle's optional
        `collections` is the PACK-DECLARED tier vocabulary (the DF
        event_collections donor shape, L10 — at least two tiers, the
        list order is the hierarchy, the kinds ⊆ the closed
        HISTORY_KINDS, the types unique, the nested caps ≥ 1) and the
        chronicle line's every alternative binds the DF legends fields
        (`participants`/`places` unconditionally, `collection` when
        the vocabulary is declared — the L1 law at alternative
        granularity); states.capitals ≥ 2 (the participants' two
        distinct regions). The place-1 law (W1, the placement
        discipline): the claim↔exits consistency — every exits edge
        joining two CLAIMED locations must read sites within the
        pack-declared `place.max_edge_span` lattice steps (the graph's
        edge contract; the metric is the engine's lattice, the
        threshold the pack's — INV-3). The roads-1 law (the generated
        half): the `roads` sub-block carries the overlay's `k` — the
        mutual k-nearest knob over the claimed locations, 0..claimed-2
        (the vacuity refusal, the dead-data family); the pass asserts
        the span against its own edges AT EMIT, and the runtime
        backstop's set gained `place` and `roads` with it."""
        rules = self._data["rules.json"]
        config = rules.get(WORLDGEN_BLOCK)
        if config is None:
            return
        where = f"rules.json::{WORLDGEN_BLOCK}"
        _require(
            isinstance(config, Mapping),
            f"{where} must be an object (the closed vocabulary: map | "
            "biomes | watershed | states | chronicle | claims | place | "
            "roads)",
        )
        unknown = sorted(set(config) - set(WORLDGEN_SUB_BLOCKS))
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "map | biomes | watershed | states | chronicle | claims | "
                "place | roads)"
            )
        # KI#82: a MISSING sub-block is a loud PackError naming the
        # block, never a raw KeyError from the indexing below (the
        # pred-contract family law — only unknown EXTRA keys were
        # checked before; the leak was probed on a crafted twin).
        for block in WORLDGEN_SUB_BLOCKS:
            _require(
                block in config,
                f"{where} is missing the {block!r} sub-block (the "
                "closed vocabulary: map | biomes | watershed | states | "
                "chronicle | claims | place | roads)",
            )

        map_cfg = config["map"]
        _require(
            isinstance(map_cfg, Mapping),
            f"{where}.map must be an object",
        )
        unknown = sorted(set(map_cfg) - set(WORLDGEN_MAP_KEYS))
        if unknown:
            raise PackError(
                f"{where}.map: unknown keys {unknown} (the closed "
                f"vocabulary: {sorted(WORLDGEN_MAP_KEYS)})"
            )
        for key in WORLDGEN_MAP_KEYS:
            _require(
                _is_int(map_cfg.get(key)),
                f"{where}.map.{key} must be an integer",
            )
        _require(
            map_cfg["extent"] > map_cfg["spacing"] > 0,
            f"{where}.map: extent must exceed spacing (both positive)",
        )
        _require(
            2 * map_cfg["jitter"] < map_cfg["spacing"],
            f"{where}.map: 2*jitter < spacing (a bigger jitter collapses "
            "the lattice — the sites would stop being distinct cells)",
        )
        _require(
            0 <= map_cfg["relax_rounds"] <= 4,
            f"{where}.map.relax_rounds must be 0..4 (relaxation beyond a "
            "few rounds buys nothing — the lattice already regularizes)",
        )
        for key in ("height_octaves", "moisture_octaves"):
            _require(
                1 <= map_cfg[key] <= 5,
                f"{where}.map.{key} must be 1..5 (the octave range the "
                "integer noise normalizes over)",
            )
        columns = map_cfg["extent"] // map_cfg["spacing"]
        site_count = columns**2

        biome_cfg = config["biomes"]
        _require(
            isinstance(biome_cfg, Mapping),
            f"{where}.biomes must be an object",
        )
        unknown = sorted(set(biome_cfg) - {"height_bands", "moisture_bands"})
        if unknown:
            raise PackError(
                f"{where}.biomes: unknown keys {unknown} (the closed "
                "vocabulary: height_bands | moisture_bands)"
            )
        for key in ("height_bands", "moisture_bands"):
            bands = biome_cfg.get(key)
            _require(
                isinstance(bands, list) and len(bands) == 3
                and all(_is_int(edge) for edge in bands),
                f"{where}.biomes.{key} must be a list of three integer "
                "band edges (four bands per axis)",
            )
            _require(
                all(
                    0 < left < right < FIELD_MAX
                    for left, right in zip(bands, bands[1:], strict=False)
                ),
                f"{where}.biomes.{key} must be strictly ascending inside "
                "(0, 9999) — the fields' normalized range",
            )

        watershed_cfg = config["watershed"]
        _require(
            isinstance(watershed_cfg, Mapping),
            f"{where}.watershed must be an object",
        )
        unknown = sorted(set(watershed_cfg) - {"neighbors", "river_flow"})
        if unknown:
            raise PackError(
                f"{where}.watershed: unknown keys {unknown} (the closed "
                "vocabulary: neighbors | river_flow)"
            )
        for key in ("neighbors", "river_flow"):
            _require(
                _is_int(watershed_cfg.get(key)),
                f"{where}.watershed.{key} must be an integer",
            )
        _require(
            2 <= watershed_cfg["neighbors"] <= 8,
            f"{where}.watershed.neighbors must be 2..8 (the k-nearest "
            "adjacency window)",
        )
        _require(
            watershed_cfg["river_flow"] >= 2,
            f"{where}.watershed.river_flow must be at least 2 (a "
            "threshold of 1 makes every site a river)",
        )

        states_cfg = config["states"]
        _require(
            isinstance(states_cfg, Mapping),
            f"{where}.states must be an object",
        )
        unknown = sorted(set(states_cfg) - {"capitals"})
        if unknown:
            raise PackError(
                f"{where}.states: unknown keys {unknown} (the closed "
                "vocabulary: capitals)"
            )
        _require(
            _is_int(states_cfg.get("capitals")),
            f"{where}.states.capitals must be an integer",
        )
        _require(
            2 <= states_cfg["capitals"] <= site_count,
            f"{where}.states.capitals must be 2..{site_count} (the history "
            "events' participants need two distinct regions — the DF war "
            "shape's two sides; a one-region world cannot arm the "
            "chronicle)",
        )

        chronicle_cfg = config["chronicle"]
        _require(
            isinstance(chronicle_cfg, Mapping),
            f"{where}.chronicle must be an object",
        )
        unknown = sorted(
            set(chronicle_cfg) - {"years", "events_max", "event_type", "hooks", "collections"}
        )
        if unknown:
            raise PackError(
                f"{where}.chronicle: unknown keys {unknown} (the closed "
                "vocabulary: years | events_max | event_type | hooks | "
                "collections)"
            )
        for key in ("years", "events_max"):
            _require(
                _is_int(chronicle_cfg.get(key)) and chronicle_cfg[key] >= 1,
                f"{where}.chronicle.{key} must be an integer >= 1 (zero "
                "or negative is dead data — omit the block for v0.1 "
                "bytes)",
            )
        templates = self._data["templates.json"]["events"]
        event_type = chronicle_cfg.get("event_type")
        _require(
            isinstance(event_type, str) and event_type in templates,
            f"{where}.chronicle.event_type {event_type!r} is not in the "
            "template vocabulary (EVENT_SCHEMA §11 — closed per pack)",
        )
        hooks = chronicle_cfg.get("hooks")
        _require(
            isinstance(hooks, list) and hooks
            and all(isinstance(tag, str) and tag.strip() for tag in hooks)
            and len(set(hooks)) == len(hooks),
            f"{where}.chronicle.hooks must be a non-empty list of unique "
            "non-empty strings",
        )
        declared_hooks = set(self._data["rules.json"].get("director", {}).get("hooks", {}))
        unknown = sorted(set(hooks) - declared_hooks)
        if unknown:
            raise PackError(
                f"{where}.chronicle.hooks names undeclared director "
                f"hooks {unknown} — a genesis hook the director does not "
                "know would never release (dead data; declare it in "
                "director.hooks first)"
            )

        # chron-2, the PACK-DECLARED collection vocabulary (the DF
        # event_collections donor shape, L10: JSON + lint, never string
        # languages). The list order IS the hierarchy — the root tier
        # anchors (type + kinds), each nested tier carries its member
        # cap. HISTORY_KINDS stays closed: the kinds the tiers may name
        # are the engine's four verbs, the collection types are the
        # pack's own layer (INV-3).
        collections = chronicle_cfg.get("collections")
        if collections is not None:
            _require(
                isinstance(collections, list) and len(collections) >= 2,
                f"{where}.chronicle.collections must be a list of at least "
                "two tiers (the root + a member tier — a single tier "
                "labels every event without grouping it, dead "
                "vocabulary; omit the key for the flat form)",
            )
            tier_types: set[str] = set()
            for index, tier in enumerate(collections):
                spot = f"{where}.chronicle.collections[{index}]"
                _require(
                    isinstance(tier, Mapping),
                    f"{spot}: must be an object",
                )
                legal = (
                    {"type", "kinds"} if index == 0
                    else {"type", "kinds", "members"}
                )
                unknown = sorted(set(tier) - legal)
                if unknown:
                    raise PackError(
                        f"{spot}: unknown keys {unknown} (the tier "
                        f"vocabulary: {sorted(legal)} — the list order is "
                        "the hierarchy, the root first; the root anchors, "
                        "the nested tiers carry the member caps)"
                    )
                tier_type = tier.get("type")
                _require(
                    isinstance(tier_type, str) and tier_type.strip(),
                    f"{spot}.type must be a non-empty string",
                )
                _require(
                    tier_type not in tier_types,
                    f"{spot}.type {tier_type!r} is declared twice (the "
                    "tier types are the collection vocabulary — unique)",
                )
                tier_types.add(tier_type)
                kinds = tier.get("kinds")
                _require(
                    isinstance(kinds, list) and kinds
                    and all(isinstance(kind, str) for kind in kinds)
                    and len(set(kinds)) == len(kinds),
                    f"{spot}.kinds must be a non-empty list of unique "
                    "strings",
                )
                unknown_kinds = sorted(set(kinds) - set(HISTORY_KINDS))
                if unknown_kinds:
                    raise PackError(
                        f"{spot}.kinds names {unknown_kinds} — not in the "
                        f"closed history vocabulary {list(HISTORY_KINDS)} "
                        "(HISTORY_KINDS stays closed; the collection types "
                        "are the pack's layer, the kinds are the engine's)"
                    )
                if index > 0:
                    _require(
                        _is_int(tier.get("members")) and tier["members"] >= 1,
                        f"{spot}.members must be an integer >= 1 (the "
                        "tier's member cap within one collection)",
                    )

        # chron-2, the template closure (EVENT_SCHEMA §11 — the genesis
        # event types are pack vocabulary, the line is the fields'
        # consumer): every alternative of the chronicle line binds the
        # DF legends fields (a shuffle pick that drops them leaves canon
        # data unrendered — the L1 law at alternative granularity), and
        # the collection slot when the tier vocabulary is declared (the
        # tier types would be dead data otherwise).
        line = self._data["templates.json"]["events"][event_type]
        alternatives = line if isinstance(line, list) else [line]
        required = ["participants", "places"] + (
            ["collection"] if collections is not None else []
        )
        for index, alternative in enumerate(alternatives):
            bound = set(_BRACE_SLOT.findall(alternative)) | set(
                _BRACE_COND.findall(alternative)
            )
            missing = [slot for slot in required if slot not in bound]
            if missing:
                raise PackError(
                    f"templates.json events.{event_type}[{index}]: binds "
                    f"no {{{missing[0]}}} — the history events carry "
                    "the DF legends shape unconditionally (dead data, the "
                    "L1 law; the chronicle line is the fields' consumer)"
                )

        # place-1 (W1), the placement discipline's own block: the
        # PACK-DECLARED edge contract. `max_edge_span` is the maximum
        # lattice distance (Chebyshev cell steps, `lattice_distance`)
        # the exits graph tolerates between the claimed sites of two
        # exits-joined locations. 0 = co-located rooms (the building
        # scale); the lattice diameter (columns - 1) is REFUSED — a
        # span there accepts every site pair including the opposite
        # corners, vacuous dead data (the single-tier collection's
        # twin law, NOT a policy ceiling — D-116 (3) refuses those).
        place_cfg = config["place"]
        _require(
            isinstance(place_cfg, Mapping),
            f"{where}.place must be an object",
        )
        unknown = sorted(set(place_cfg) - {"max_edge_span"})
        if unknown:
            raise PackError(
                f"{where}.place: unknown keys {unknown} (the closed "
                "vocabulary: max_edge_span)"
            )
        span = place_cfg.get("max_edge_span")
        _require(
            _is_int(span) and 0 <= span <= columns - 2,
            f"{where}.place.max_edge_span must be an integer in "
            f"0..{columns - 2} (0 = co-located rooms; {columns - 1} is "
            f"the {columns}-column lattice's diameter — a span there "
            "accepts every site pair, vacuous dead data)",
        )

        claims = config.get("claims")
        _require(
            isinstance(claims, list) and claims,
            f"{where}.claims must be a non-empty list of claim entries "
            "(an empty list is dead data — omit the key)",
        )
        scene_detail = rules.get("scene_detail", {})
        locations = {
            record["id"]: record
            for record in self._data["entities.json"]["locations"]
        }
        seen_pairs: set[tuple[str, str]] = set()
        for index, entry in enumerate(claims):
            spot = f"{where}.claims[{index}]"
            _require(isinstance(entry, Mapping), f"{spot}: must be an object")
            unknown = sorted(set(entry) - {"location", "slot", "field", "site"})
            if unknown:
                raise PackError(
                    f"{spot}: unknown keys {unknown} (the closed "
                    "vocabulary: location | slot | field | site)"
                )
            location = entry.get("location")
            record = locations.get(location)
            _require(
                record is not None,
                f"{spot}.location {location!r}: unknown location id "
                "(entities.json locations is the single owner)",
            )
            slot = entry.get("slot")
            _require(
                isinstance(slot, str) and slot.strip(),
                f"{spot}.slot must be a non-empty string",
            )
            modeled = set(record) | set(record.get("flags", {}))
            _require(
                slot not in modeled,
                f"{spot}.slot {slot!r} is modeled by the location entity "
                "(the double-claim law, the scene_detail twin: lazy and "
                "worldgen detail occupy only slots canon does not "
                "model — the fold seeds flags as raw site props, so a "
                "pre-claimed slot could never birth)",
            )
            _require(
                slot not in {spec["slot"] for spec in scene_detail.get(location, ())},
                f"{spot}.slot {slot!r} is also declared in scene_detail "
                "for the same location (the overlap refusal: the genesis "
                "claims at open time, before any observation, so the "
                "scene's lazy draw could never fire — dead pack data)",
            )
            field = entry.get("field")
            _require(
                field in CLAIM_FIELDS,
                f"{spot}.field {field!r} is not in the closed set "
                f"{list(CLAIM_FIELDS)}",
            )
            site = entry.get("site")
            _require(
                _is_int(site) and 0 <= site < site_count,
                f"{spot}.site must be an integer in 0..{site_count - 1} "
                "(the site count is (extent // spacing)^2)",
            )
            pair = (location, slot)
            _require(
                pair not in seen_pairs,
                f"{spot}: the (location, slot) pair {pair} is claimed "
                "twice (the double-declaration refusal — first-commit-"
                "wins decides runtime order, not pack duplication)",
            )
            seen_pairs.add(pair)
            _require(
                slot not in RESERVED_CLAIM_SLOTS,
                f"{spot}.slot {slot!r} is reserved (the world_formed "
                "outcome's fixed keys are CLOBBERED by the flat claim "
                "key, the render context's derived slots SHADOW it — "
                "a colliding claim can never bind; see "
                "core/worldgen.py::RESERVED_CLAIM_SLOTS)",
            )

        # place-1 (W1), the claim↔exits consistency: a location's
        # claimed site must be topologically compatible with its
        # exits. For every UNDIRECTED exits edge joining two CLAIMED
        # locations, every cross-pair of their claimed sites must sit
        # within the declared max_edge_span lattice steps — two
        # locations joined by exits never read sites from opposite
        # corners of the map (the map↔graph coherence the derived
        # travel prices of st-6a read, D-116 (5): an edge-local price
        # needs edge-local sites). Edges with an unclaimed endpoint
        # impose nothing (the law is edge-mediated — an unclaimed
        # neighbor renders its pack-record fields); a location's own
        # claims are unordered (all cross-pairs checked, the strictest
        # reading — a far claim is refused whatever its siblings).
        # The exits graph is symmetric (the entities lint runs before
        # this one), so the sorted unique pairs cover every edge once.
        sites_by_location: dict[str, list[int]] = {}
        for entry in claims:
            sites_by_location.setdefault(
                str(entry["location"]), []
            ).append(int(entry["site"]))
        edges: set[tuple[str, str]] = set()
        for record in self._data["entities.json"]["locations"]:
            for exit_id in record["exits"]:
                left, right = sorted((str(record["id"]), str(exit_id)))
                edges.add((left, right))
        for left, right in sorted(edges):
            left_sites = sites_by_location.get(left, ())
            right_sites = sites_by_location.get(right, ())
            if not left_sites or not right_sites:
                continue
            for site_a in left_sites:
                for site_b in right_sites:
                    distance = lattice_distance(
                        site_a, site_b,
                        map_cfg["extent"], map_cfg["spacing"],
                    )
                    _require(
                        distance <= span,
                        f"{where}.place: the exits edge {left} <-> {right} "
                        f"reads sites {site_a} and {site_b} — {distance} "
                        f"lattice steps apart, beyond max_edge_span {span} "
                        "(the claim-exits consistency law: two locations "
                        "joined by exits never claim sites the edge cannot "
                        "reach — claim reachable sites or raise the span)",
                    )

        # roads-1 (the generated half's own sub-block, `docs/CONTRACTS.md`
        # §1 D2): `k` is the overlay's knob — the number of nearest
        # non-tree neighbors each claimed location may gain through the
        # MUTUAL k-nearest overlay (the pass: `core/worldgen.py::
        # _pass_roads`). The watershed.neighbors precedent: a pass's
        # shape parameter is declared, never engine-constant (D-024 —
        # no defaults, the arming is a complete declaration). k=0 is
        # legal (the tree-only world). The VACUITY bound (the dead-data
        # law, D-116 (3)'s family): a node can gain at most n-2 NEW
        # non-tree neighbors (n-1 others minus at least one tree edge in
        # a connected n-node world), so k beyond claimed-2 can never add
        # an edge — refused like a diameter span, never a policy ceiling.
        roads_cfg = config["roads"]
        _require(
            isinstance(roads_cfg, Mapping),
            f"{where}.roads must be an object",
        )
        unknown = sorted(set(roads_cfg) - {"k"})
        if unknown:
            raise PackError(
                f"{where}.roads: unknown keys {unknown} (the closed "
                "vocabulary: k)"
            )
        claimed_count = len(sites_by_location)
        _require(
            _is_int(roads_cfg.get("k")) and 0 <= roads_cfg["k"] <= max(
                0, claimed_count - 2
            ),
            f"{where}.roads.k must be an integer in 0.."
            f"{max(0, claimed_count - 2)} (k=0 is the tree-only world; "
            f"{claimed_count} claimed locations gain at most "
            f"{max(0, claimed_count - 2)} overlay neighbors each — a "
            "bigger k can never add an edge, vacuous dead data)",
        )

        # D-116 (2), CONDUCTANCE: dead template lines are dead data. The
        # genesis event types must clear the tale gate THROUGH THE PACK'S
        # OWN RULE (pack_importance — one rule for action events and
        # world events, never a second scoring path). The shapes are the
        # runtime's own: world_formed scores its DISTINCT claim
        # locations (the committed claims' entities), a history event
        # one far hook (its drawn tag). The trap is live and measured:
        # without the story-critical listing world_formed reads 0 and a
        # history event 1 per_far_hook against the medium gate's 2 —
        # the genesis would commit and never render.
        templates_all = self._data["templates.json"]
        gate = templates_all.get("tale_gate", {}).get("min_importance", "low")
        _require(
            gate in IMPORTANCE_ORDER,
            f"{where}: templates.json tale_gate.min_importance {gate!r} "
            f"is not in {list(IMPORTANCE_ORDER)}",
        )
        claim_locations = {str(entry["location"]) for entry in claims}
        formed = pack_importance(rules, claim_locations, 0, 0, event_type)
        history = pack_importance(rules, set(), 0, 1, event_type)
        _require(
            IMPORTANCE_ORDER.index(formed) >= IMPORTANCE_ORDER.index(gate)
            and IMPORTANCE_ORDER.index(history) >= IMPORTANCE_ORDER.index(gate),
            f"{where}.chronicle: the genesis events cannot clear the "
            f"tale gate ({gate!r}) — world_formed scores {formed!r}, a "
            f"history event {history!r} (dead template lines = dead "
            "data, D-116; list the chronicle event type in "
            "importance.story_critical_events — tune-1's law: the rule "
            "owns the split)",
        )

        # D-116 (2), REACHABILITY (L1): every armed claim names at least
        # one LIVE consumer — a template line binding the slot (a
        # `{slot}` / `{slot?…}` reference; the flat claim key is the
        # binding surface), a declared director hook reading the
        # (location, slot) pair through a prop predicate, or the SCENE
        # LINE declaring the slot (bridge-1, D-116 (1) — the claims'
        # first brief-side consumer: the pipe reads the slot from the
        # folded projection into the scene line).
        bound = _bound_template_slots(templates_all)
        reads = _director_prop_reads(rules)
        scene_fields = frozenset(
            rules.get("brief", {})
            .get("present_entities", {})
            .get("scene_line_fields", ())
        )
        for index, entry in enumerate(claims):
            slot = str(entry["slot"])
            if slot in bound:
                continue
            if (str(entry["location"]), slot) in reads:
                continue
            if slot in scene_fields:
                continue
            raise PackError(
                f"{where}.claims[{index}]: the slot {slot!r} names no "
                "live consumer — no template line binds it, no declared "
                f"director hook reads ({entry['location']}, {slot}), and "
                "the scene line does not declare it (dead pack data, "
                "the L1 law)"
            )
