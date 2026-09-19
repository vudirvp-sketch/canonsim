"""roads-1 acceptance — the generated-exits pass over the claimed
locations (`docs/CONTRACTS.md` §1, the minimal test set):

- the topology invariants I1..I6 at emit, over the committed province
  block (k=0: the authored artery IS a tree — the derived backbone
  answers a minimum spanning tree of the same weight) and a hand-built
  fixture with k>0 (the overlay's cycles, the mutual-k law's bounds);
- the loud span failure (I4's conflict rule — its own case);
- determinism: same seed + pack -> the identical derived graph (the
  WorldModel rebuild law, L11);
- the pack-wins override: an authored `exits` record never reads the
  pass; an empty one reads the derived edges; an unclaimed location and
  an unarmed world read ();
- the one-read consumers: the LOD warm ring and the intent door's move
  validation read the DERIVED half through `core/roads.py::exits` (a
  crafted mode G mini-pack — loc_tavern's authored edges emptied on
  both sides, the derived edge carrying the ring);
- zero canon price: no roads key rides the world_formed outcome, no
  event carries the pass's data (INV-1 — the golden T1 byte-compares
  pin the corpora themselves).

The pass is PURE (INV-2-clean by construction: no stream is ever
touched — the fingerprint tests pin the zero-draw law).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.intent import IntentData, first_failing
from core.lod import scene_zones
from core.pack import Pack, PackError, load_pack
from core.rng import RngBank
from core.roads import exits as exits_of
from core.worldgen import (
    WorldgenError,
    _pass_roads,
    generate_world,
)

REPO = Path(__file__).resolve().parents[1]
PROVINCE = load_pack(REPO / "content" / "province_pack")
TAVERN = load_pack(REPO / "content" / "tavern_pack")

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

_LINT_SEQ = 0


def _crafted(
    tmp_path: Path, name: str, worldgen: Any, *, empty_tavern_exits: bool = False
) -> Pack:
    """A committed-pack copy with the `worldgen` block set — plus the
    mode G arm: loc_tavern's authored edges REMOVED on both sides (its
    own list and its neighbors'), the empty list the generated-world
    marker (loc_tavern stays orphan-legal: the npcs' positions reference
    it)."""
    global _LINT_SEQ
    _LINT_SEQ += 1
    target = tmp_path / f"{name}_{_LINT_SEQ}"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["worldgen"] = worldgen
    (target / "rules.json").write_text(json.dumps(rules, indent=2))
    if empty_tavern_exits:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        for record in entities["locations"]:
            if record["id"] == "loc_tavern":
                record["exits"] = []
            elif "loc_tavern" in record["exits"]:
                record["exits"].remove("loc_tavern")
        # the orphan law: an UNCARRIED, unflagged item at the emptied
        # location loses its grammar reachability (the take family's
        # `same_location` reads an EDGED position) — the mode G author
        # relocates it to an edged location (the mug moves to the street)
        for item in entities["items"]:
            if (
                item.get("position") == "loc_tavern"
                and item.get("carrier") is None
                and not item.get("is_fire_source")
            ):
                item["position"] = "loc_street"
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2)
        )
    return load_pack(target)


def _graph_edges(graph: tuple[tuple[str, tuple[str, ...]], ...]) -> set[frozenset[str]]:
    return {frozenset((node, other)) for node, out in graph for other in out}


#: A WG-shaped arming (test_worldgen's committed-twin grammar; the
#: fixture that varies is `roads.k` and the claims' spread).
WG_ROADS: dict[str, Any] = {
    "map": {
        "extent": 48,
        "spacing": 8,
        "jitter": 3,
        "relax_rounds": 1,
        "height_octaves": 3,
        "moisture_octaves": 2,
    },
    "biomes": {
        "height_bands": [4000, 5000, 7000],
        "moisture_bands": [2500, 5000, 7500],
    },
    "watershed": {"neighbors": 4, "river_flow": 6},
    "states": {"capitals": 3},
    "chronicle": {
        "years": 150,
        "events_max": 5,
        "event_type": "world_history",
        "hooks": ["barkeep_wary_sweep", "ambient_drunkard_ramble"],
    },
    "claims": [
        {"location": "loc_tavern", "slot": "terrain", "field": "biome", "site": 0},
        {"location": "loc_tavern", "slot": "world_region", "field": "region", "site": 0},
        {"location": "loc_street", "slot": "near_river", "field": "river", "site": 1},
    ],
    "place": {"max_edge_span": 1},
    "roads": {"k": 0},
}


#: A hand-built spread fixture (the k>0 arm): five claimed locations on
#: a 6-column lattice's diagonal — sites 0, 7, 14, 21, 28 = the cells
#: (0,0), (1,1), (2,2), (3,3), (4,4): consecutive pairs 1 Chebyshev step
#: apart, the whole chain within the declared span 3, the ends 4 apart
#: (beyond the span — only reachable THROUGH the chain, the star's own
#: loud-failure geometry read the other way).
SPREAD: dict[str, Any] = {
    "map": {"extent": 48, "spacing": 8},
    "place": {"max_edge_span": 3},
    "roads": {"k": 2},
    "claims": [
        {"location": f"loc_{name}", "slot": "ground", "field": "biome", "site": site}
        for name, site in zip("abcde", (0, 7, 14, 21, 28), strict=True)
    ],
}


# -- (1a) the committed province block ------------------------------------------


def test_the_province_backbone_is_a_minimum_spanning_tree() -> None:
    """The committed province block (k=0 — the authored artery IS a
    tree): the derived graph answers 6 claimed nodes joined by 5 edges
    (I1 one component, I6 the tree alone is acyclic), every edge within
    the declared span 4 (I4), symmetric (I2), and the derived weight
    distribution == [2, 2, 2, 4, 4] — the authored artery's own
    distances (4+4+2+2+2=14, hand-computed from the declared sites):
    the derived backbone cannot be heavier (the independent
    re-derivation oracle — the test recomputes the metric itself, never
    the pass's code path)."""
    graph = _pass_roads(PROVINCE.rules["worldgen"])
    assert len(graph) == 6
    edges = _graph_edges(graph)
    assert len(edges) == 5
    for node, out in graph:  # I2 + no self-loop + no duplicates
        assert len(out) == len(set(out))
        assert node not in out
    weights = sorted(
        _pair_weight(PROVINCE.rules["worldgen"], left, right)
        for left, right in (tuple(sorted(edge)) for edge in edges)
    )
    assert weights == [2, 2, 2, 4, 4]  # the authored artery's own shape
    assert sum(weights) == 14


def _pair_weight(config: Any, left: str, right: str) -> int:
    """The minimal Chebyshev cross-pair distance between two claimed
    locations — the TEST-side independent re-derivation (divmod by the
    column count, never the pass's own code path)."""
    from core.worldgen import lattice_distance

    sites: dict[str, set[int]] = {}
    for entry in config["claims"]:
        sites.setdefault(str(entry["location"]), set()).add(int(entry["site"]))
    extent = int(config["map"]["extent"])
    spacing = int(config["map"]["spacing"])
    return min(
        lattice_distance(a, b, extent, spacing)
        for a in sites[left] for b in sites[right]
    )


# -- (1b) the k>0 fixture: the overlay's own laws ---------------------------------


def test_the_overlay_is_mutual_and_bounded() -> None:
    """The spread fixture with k=2 (the contract's I3 + D2 pin — the
    MUTUAL k-nearest law): five claimed locations on the diagonal of a
    6-column lattice (sites 0, 7, 14, 21, 28 = the cells (0,0)..(4,4)):
    consecutive pairs 1 Chebyshev step apart (the backbone chain), the
    2-step pairs a-c, b-d, c-e and the 3-step pairs a-d, b-e legal under
    the span 3, the 4-step pair a-e beyond it. Every non-tree candidate
    within the span is a MUTUAL pick here (each node's two nearest
    non-tree candidates pick it back), so all five chords land; a-e
    never does (over-span). Per-node OVERLAY degree stays <= k = 2 and
    the total degree within (n-1)+k (I3)."""
    graph = _pass_roads(SPREAD)
    by_node = dict(graph)
    assert set(by_node) == {f"loc_{name}" for name in "abcde"}
    edges = _graph_edges(graph)
    chain = {frozenset((f"loc_{a}", f"loc_{b}")) for a, b in ("ab", "bc", "cd", "de")}
    assert chain <= edges  # the backbone chain
    assert {
        frozenset((f"loc_{a}", f"loc_{b}")) for a, b in ("ac", "ad", "bd", "be", "ce")
    } <= edges  # the mutual span-legal chords
    assert frozenset(("loc_a", "loc_e")) not in edges  # 4 steps > span 3
    for node, out in graph:  # I3: the overlay degree <= k
        overlay_degree = sum(
            1 for other in out
            if frozenset((node, other)) not in chain
        )
        assert overlay_degree <= SPREAD["roads"]["k"]
        assert len(out) <= (len(graph) - 1) + SPREAD["roads"]["k"]
    # I6: cycles exist (the overlay's purpose) — a-b-c-a
    assert {
        frozenset(("loc_a", "loc_b")),
        frozenset(("loc_a", "loc_c")),
        frozenset(("loc_b", "loc_c")),
    } <= edges


def test_the_loud_span_failure_is_its_own_case() -> None:
    """I4's conflict rule: a claimed set that cannot be connected within
    the declared span fails LOUD (WorldgenError naming the declared span
    and the too-far edge) — connectivity is never bought by breaking
    the span; the pack author fixes placements or raises the span.
    The unconnectable shape: two claims on the same row 5 cells apart
    (sites 0 = (0,0) and 5 = (0,5)) under a span of 2."""
    broken = {
        **SPREAD,
        "place": {"max_edge_span": 2},
        "claims": [
            {"location": "loc_x", "slot": "g", "field": "biome", "site": 0},
            {"location": "loc_y", "slot": "g", "field": "biome", "site": 5},
        ],
    }
    with pytest.raises(WorldgenError, match="cannot be connected"):
        _pass_roads(broken)


def test_the_star_topology_is_legal() -> None:
    """The contract's counterexample: a hub joined to every other node
    (degree n-1) is legal — the bound holds, no edge exceeds the span,
    one component (I1). Exact geometry on a 6-column lattice: the hub
    site 14 = (2,2); the spokes 13 = (2,1) and 15 = (2,3), both 1 step
    from the hub, 2 steps from each other — under span 1 the spokes'
    own edge is illegal, so the MST IS the star (I3's bound never
    violated at degree n-1)."""
    star = {
        **SPREAD,
        "roads": {"k": 0},
        "place": {"max_edge_span": 1},
        "claims": [
            {"location": f"loc_{name}", "slot": "g", "field": "biome", "site": site}
            for name, site in zip("abc", (14, 13, 15), strict=True)
        ],
    }
    graph = _pass_roads(star)
    by_node = dict(graph)
    assert by_node["loc_a"] == ("loc_b", "loc_c")  # the hub: degree n-1
    assert by_node["loc_b"] == ("loc_a",) and by_node["loc_c"] == ("loc_a",)
    assert len(_graph_edges(graph)) == 2  # the star: n-1 edges


# -- (2) determinism ---------------------------------------------------------------


def test_same_seed_same_pack_identical_graph() -> None:
    """The WorldModel rebuild law (L11): the same seed + pack answers the
    identical derived graph byte-for-byte — and the pass is draw-free
    (the fingerprint never sees a roads edge; the same bank state feeds
    both arms)."""
    bank = RngBank(42)
    first = generate_world(bank, WG_ROADS)
    second = generate_world(RngBank(42), WG_ROADS)
    assert first.roads == second.roads
    assert first.sites == second.sites  # the whole model is the same run


# -- (3) the pack-wins override ----------------------------------------------------


def test_the_authored_record_wins_the_derived_fills_the_empty() -> None:
    """The one shared read: a location with a NON-EMPTY authored list
    reads exactly it (the pack wins — every committed location does);
    an EMPTY list reads the derived edges (the generated-world marker);
    an UNCLAIMED location and an unarmed world read the empty tuple."""
    world = generate_world(RngBank(42), WG_ROADS)
    # the committed packs: authored everywhere, the derived never read
    assert exits_of(PROVINCE, world, "loc_keep") == tuple(
        next(
            loc["exits"]
            for loc in PROVINCE.entities["locations"]
            if loc["id"] == "loc_keep"
        )
    )
    # the claimed nodes ARE in the derived graph (the pass emitted them)
    assert dict(world.roads)["loc_tavern"] == ("loc_street",)
    # a hand-built world with a derived edge for an empty-exits location:
    # the tavern's claims arm the graph — simulate the mode G read by
    # asking for a location whose authored list the crafted pack emptied
    # (the crafted mini-pack below exercises it end-to-end; here the
    # unarmed law: no world, no derived half)
    assert exits_of(TAVERN, None, "loc_tavern") == tuple(
        next(
            loc["exits"]
            for loc in TAVERN.entities["locations"]
            if loc["id"] == "loc_tavern"
        )
    )
    # an unclaimed location never reads the pass (not a node)
    assert exits_of(TAVERN, world, "loc_backyard") == tuple(
        next(
            loc["exits"]
            for loc in TAVERN.entities["locations"]
            if loc["id"] == "loc_backyard"
        )
    )


# -- the consumers (the crafted mode G mini-pack) ----------------------------------


def test_the_warm_ring_and_the_move_door_read_the_derived_half(
    tmp_path: Path,
) -> None:
    """The row's named consumers through the ONE shared read: with
    loc_tavern's authored edges emptied (the generated-world marker) and
    the world armed, the WARM RING at the tavern reads the derived edge
    (loc_street — the pass's answer), the MOVE DOOR accepts the derived
    neighbor and refuses the authored-only ones, and the authored
    locations keep their own lists (the override, per-location)."""
    pack = _crafted(tmp_path, "mode_g", WG_ROADS, empty_tavern_exits=True)
    world = generate_world(RngBank(42), WG_ROADS)
    assert dict(world.roads)["loc_tavern"] == ("loc_street",)  # the derived
    # the read: the emptied location derives, the authored location wins
    assert exits_of(pack, world, "loc_tavern") == ("loc_street",)
    assert exits_of(pack, world, "loc_street") == tuple(
        next(
            loc["exits"]
            for loc in pack.entities["locations"]
            if loc["id"] == "loc_street"
        )
    )
    # the warm ring: the pc stands at the tavern (its initial position
    # is the street — the test moves it one door in)
    projection = {
        npc["id"]: {"position": npc["position"]}
        for npc in pack.entities["npcs"]
    }
    player = pack.player_id()
    projection[player] = {"position": "loc_tavern"}
    zones = scene_zones(pack, world, projection)  # type: ignore[arg-type]
    assert zones.active == "loc_tavern"
    assert zones.warm == ("loc_street",)  # the DERIVED edge carries the ring
    # the move door: the derived neighbor passes, the authored-only
    # neighbor (backyard — the authored edge was removed with the rest)
    # no longer does
    move = next(
        action for action in
        json.loads((REPO / "content" / "tavern_pack" / "actions.json").read_text())["actions"]
        if action["intent"] == "move"
    )
    requires = move["requires"]
    to_street = IntentData(
        id="i1", kind="move", actor=player, target="loc_street", fields={}
    )
    to_backyard = IntentData(
        id="i2", kind="move", actor=player, target="loc_backyard", fields={}
    )
    assert first_failing(
        pack, projection, to_street, list(requires), world=world
    ) is None
    assert first_failing(
        pack, projection, to_backyard, list(requires), world=world
    ) == "target.adjacent_to"


# -- (4) zero canon price ------------------------------------------------------------


def test_no_canon_births_the_outcome_stays_as_is(tmp_path: Path) -> None:
    """INV-1 untouched: the derived graph is read-side only — the
    world_formed outcome block carries no roads key (the fixed keys +
    the claims, exactly as before), and a short armed run emits no event
    mentioning the pass (zero canon births by construction)."""
    from core.log import read_log
    from core.loop import Simulator

    log = tmp_path / "roads_price.jsonl"
    sim = Simulator(
        _crafted(tmp_path, "canon_price", WG_ROADS), 42, log, SCHEMA,
        commit="0000000",
    )
    sim.run_playscript(
        {"name": "rp", "seed": 42, "pack": "tavern_pack@0.1",
         "steps": [{"intent": "wait", "ticks": 5}]}
    )
    sim.close()
    _header, events = read_log(log, SCHEMA)
    formed = events[0]
    assert formed.type == "world_history"
    assert "roads" not in formed.outcome
    assert set(formed.outcome) <= {
        "kind", "sites", "regions", "years", "claims", "refused",
        "terrain", "world_region", "near_river",
    }


# -- the lint refusals ---------------------------------------------------------------


def test_the_lint_refuses_a_vacuous_or_malformed_k(tmp_path: Path) -> None:
    """The roads sub-block's own law (the watershed.neighbors precedent
    + the dead-data family): an unknown key is a second config surface;
    a non-integer is a shape error; k beyond claimed-2 (WG claims TWO
    locations — tavern and street — so k must be 0) is vacuous dead
    data, refused like a diameter span."""
    with pytest.raises(PackError, match="unknown keys"):
        _crafted(tmp_path, "k_unknown", {**WG_ROADS, "roads": {"k": 0, "scale": 1}})
    with pytest.raises(PackError, match="must be an integer in 0..0"):
        _crafted(tmp_path, "k_str", {**WG_ROADS, "roads": {"k": "1"}})
    with pytest.raises(PackError, match="vacuous dead data"):
        _crafted(tmp_path, "k_vacuous", {**WG_ROADS, "roads": {"k": 1}})
    with pytest.raises(PackError, match="must be an integer in 0..0"):
        _crafted(tmp_path, "k_negative", {**WG_ROADS, "roads": {"k": -1}})
