"""iter-97 acceptance — st-6a, travel as a separate action (phases.md §5,
D-116 (5)'s amended price law; the STATUS queue's live row after
name-1: travel is the movement TWIN with an edge price, never a
weighted move — move's semantics, `adjacent_to` and the T1 golden
fixtures stay untouched).

The laws pinned here:

- **The price law** (`core/travel.py::travel_ticks`): the pack
  override wins per edge (the "pack wins" law, both directions of the
  undirected edge read the same price); else the DERIVED price — a
  pure integer function of the WorldModel (lattice cell steps *
  `step_ticks` + the height-band spread * `climb_ticks` + river
  endpoints * `river_ticks`; integer add/multiply only, NO runtime
  division), read at the MINIMAL cross-pair (the road takes the
  closest approach; place-1 bounds every cross-pair for correctness,
  the price reads the cheapest for cost). Neither source -> a loud
  TravelError (the runtime backstop family).
- **The accept door** (`core/loop.py`'s EDGE_TICKS branch): the
  completion is scheduled at `t + price` — the clock jumps ahead, so
  day-scale durations are queue-cheap (MVP_SCOPE §8), and the
  crossings (beats, rotations, macro turns) still fire MID-TRAVEL in
  tick order (D-038). The price draws NOTHING (INV-2-clean: a pure
  function of pack data + the genesis-frozen model — the fingerprint
  never sees a travel).
- **The pairing law** (`core/pack.py::_travel`): the travel block
  exists exactly when an edge-priced action does (dead vocabulary and
  dead data both refused at load); `ticks: "edge"` is legal only on
  the movement resolver (the travel action IS the movement twin); the
  coverage law — every exits edge priceable (an override or two
  claimed endpoints; the travel verb never hard-fails mid-run).
- **The unarmed law** (the 68a pattern): the committed pack declares
  no travel block and no edge-priced action — the v0.1 bytes are
  untouched by construction, zero corpus re-pins; the crafted twin
  carries the vocabulary, and the armed arm is deterministic
  (byte-identical double-run).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.travel import TravelError, travel_ticks
from core.worldgen import WorldModel

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

TRAVEL_EVENT = "travel"
TRAVEL_LINE = "{actor} travels to {target_location}."
# day-scale roads for the unclaimed-endpoint edges (the coverage law:
# the derived law prices the claimed pair alone, the overrides carry
# the rest — authored packs price their own roads, the pack wins)
OVERRIDES: list[dict[str, Any]] = [
    {"from": "loc_tavern", "to": "loc_backyard", "ticks": 400},
    {"from": "loc_street", "to": "loc_backyard", "ticks": 350},
    {"from": "loc_street", "to": "loc_guardroom", "ticks": 200},
    {"from": "loc_street", "to": "loc_market", "ticks": 250},
]
WEIGHTS: dict[str, Any] = {
    "step_ticks": 600,
    "climb_ticks": 300,
    "river_ticks": 150,
}
TRAVEL_ACTION: dict[str, Any] = {
    "intent": "travel",
    "label": "journey",
    "resolver": "movement",
    "ticks": "edge",
    "check": None,
    "on_failure": None,
    "events": {"success": TRAVEL_EVENT},
    "requires": [
        {"noun": "target", "test": "kind", "is": "location"},
        {"noun": "target", "test": "adjacent_to", "with": "actor"},
    ],
    "fields": [],
    "knowledge": {
        "success": [
            {
                "who": "same_location",
                "except": ["actor"],
                "channel": "saw",
                "fidelity": "partial",
                "knows": "{actor}_left_toward_{target}",
            },
            {
                "who": "destination_location",
                "except": ["actor"],
                "channel": "saw",
                "fidelity": "partial",
                "knows": "{actor}_arrived",
            },
        ],
        "failure": [],
    },
    "hooks": {"success": [], "failure": []},
    "notes": (
        "st-6a (D-116 (5)): the movement twin with an edge price — "
        "duration = the exits edge's price (pack override wins, else "
        "derived from the WorldModel: lattice distance + height/river "
        "modifiers, integer math); the completion rides the queue at "
        "t + price, crossings fire mid-travel (D-038)"
    ),
}


def travel_pack(
    tmp_path: Path,
    name: str,
    *,
    weights: dict[str, Any] | None = None,
    overrides: list[dict[str, Any]] | None = None,
) -> tuple[Path, Pack]:
    """A committed-pack copy carrying the travel vocabulary (the 68a
    arming: the crafted twin; the committed pack stays unarmed): the
    travel action (the movement twin, ticks 'edge'), the template line,
    and the travel block (the weights + the overrides covering every
    unclaimed-endpoint edge — the coverage law). Returns the pack dir
    (for post-hoc JSON edits) and the loaded pack."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)

    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    actions["actions"].append(json.loads(json.dumps(TRAVEL_ACTION)))
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates["events"][TRAVEL_EVENT] = TRAVEL_LINE
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    travel = dict(weights if weights is not None else WEIGHTS)
    travel["edges"] = list(
        overrides if overrides is not None else OVERRIDES
    )
    rules["travel"] = travel
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target, load_pack(target)


def _mutated(
    tmp_path: Path, name: str, mutate: Callable[[Path], None]
) -> Pack:
    """A crafted pack mutated post-lint-setup (the lint probes — the
    test_groups pattern)."""
    _base, _pack = travel_pack(tmp_path, f"base_{name}")
    target = tmp_path / name
    shutil.copytree(_base, target)
    mutate(target)
    return load_pack(target)


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> Path:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": pack.name_version, "steps": steps}
    )
    sim.close()
    return log


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return events


# -- the price law (hand-built rules + world: exact numbers) ------------------


def _world(
    height: tuple[int, ...], rivers: frozenset[int]
) -> WorldModel:
    """A hand-built WorldModel with known heights/rivers — the derived
    formula's exact-number oracle (the price reads extent/height/rivers
    alone; sites/moisture/biomes/flow/regions/capitals/years are
    unread by the law)."""
    return WorldModel(
        extent=48,  # columns = extent // spacing = 6
        sites=tuple(
            (8 * (site % 6), 8 * (site // 6)) for site in range(len(height))
        ),
        height=height,
        moisture=tuple(0 for _ in height),
        biomes=tuple("plain" for _ in height),
        flow=tuple(0 for _ in height),
        rivers=rivers,
        regions=tuple("reg_a" for _ in height),
        capitals=frozenset(),
        years=0,
    )


def _rules(
    claims: list[dict[str, Any]],
    travel: dict[str, Any],
) -> dict[str, Any]:
    return {
        "worldgen": {
            "map": {"extent": 48, "spacing": 8},
            "biomes": {"height_bands": [4000, 5000, 7000]},
            "claims": claims,
        },
        "travel": travel,
    }


def test_derived_distance_step() -> None:
    """The base term: lattice cell steps * step_ticks (equal heights,
    dry sites — the modifiers read zero)."""
    rules = _rules(
        claims=[
            {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
            {"location": "loc_b", "slot": "y", "field": "biome", "site": 5},
        ],
        travel={"step_ticks": 10},
    )
    world = _world(height=(5000,) * 6, rivers=frozenset())
    # site 0 = cell (0,0), site 5 = cell (0,5) -> Chebyshev 5
    assert travel_ticks(rules, world, "loc_a", "loc_b") == 5 * 10


def test_derived_climb_spread() -> None:
    """The height modifier: the BAND SPREAD between the endpoints (the
    pack's own height_bands vocabulary — crossing band edges is the
    climb), symmetric both directions."""
    rules = _rules(
        claims=[
            {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
            {"location": "loc_b", "slot": "y", "field": "biome", "site": 1},
        ],
        travel={"step_ticks": 10, "climb_ticks": 100},
    )
    world = _world(height=(0, 9999), rivers=frozenset())
    # bands 0 and 3 (edges 4000/5000/7000) -> spread 3
    assert travel_ticks(rules, world, "loc_a", "loc_b") == 1 * 10 + 3 * 100
    assert travel_ticks(rules, world, "loc_b", "loc_a") == 1 * 10 + 3 * 100


def test_derived_river_fords() -> None:
    """The river modifier: one tick per river-touching endpoint (0, 1
    or 2 fords)."""
    rules = _rules(
        claims=[
            {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
            {"location": "loc_b", "slot": "y", "field": "biome", "site": 1},
        ],
        travel={"step_ticks": 10, "river_ticks": 50},
    )
    world = _world(height=(5000, 5000), rivers=frozenset({1}))
    assert travel_ticks(rules, world, "loc_a", "loc_b") == 1 * 10 + 1 * 50
    assert travel_ticks(rules, world, "loc_b", "loc_a") == 1 * 10 + 1 * 50
    both = _world(height=(5000, 5000), rivers=frozenset({0, 1}))
    assert travel_ticks(rules, both, "loc_a", "loc_b") == 1 * 10 + 2 * 50


def test_derived_min_cross_pair() -> None:
    """The road takes the closest approach: a multi-site location's
    price reads the MINIMAL cross-pair (place-1 bounds every pair for
    correctness; the price reads the cheapest for cost)."""
    rules = _rules(
        claims=[
            {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
            {"location": "loc_a", "slot": "x2", "field": "region", "site": 5},
            {"location": "loc_b", "slot": "y", "field": "biome", "site": 1},
        ],
        travel={"step_ticks": 10},
    )
    world = _world(height=(5000,) * 6, rivers=frozenset())
    # cross-pairs: 0-1 (1 step) and 5-1 (4 steps) -> the minimum is 1
    assert travel_ticks(rules, world, "loc_a", "loc_b") == 1 * 10


def test_override_wins() -> None:
    """The pack override beats the derived price — the "pack wins" law,
    symmetric (both directions of the undirected edge read it)."""
    rules = _rules(
        claims=[
            {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
            {"location": "loc_b", "slot": "y", "field": "biome", "site": 5},
        ],
        travel={
            "step_ticks": 10,
            "edges": [{"from": "loc_a", "to": "loc_b", "ticks": 999}],
        },
    )
    world = _world(height=(0,) * 5 + (9999,), rivers=frozenset({5}))
    assert travel_ticks(rules, world, "loc_a", "loc_b") == 999
    assert travel_ticks(rules, world, "loc_b", "loc_a") == 999


def test_no_price_is_a_loud_refusal() -> None:
    """Neither source -> TravelError with the edge named: an unclaimed
    endpoint (an edge-local price needs edge-local sites), an unarmed
    world, a missing travel block — the runtime backstop family."""
    claims = [
        {"location": "loc_a", "slot": "x", "field": "biome", "site": 0},
        {"location": "loc_b", "slot": "y", "field": "biome", "site": 1},
    ]
    world = _world(height=(5000, 5000), rivers=frozenset())
    # the unclaimed endpoint
    rules = _rules(claims=[claims[0]], travel={"step_ticks": 10})
    with pytest.raises(TravelError, match="is an unclaimed location"):
        travel_ticks(rules, world, "loc_a", "loc_b")
    # the unarmed world
    with pytest.raises(TravelError, match="the world is unarmed"):
        travel_ticks(_rules(claims, travel={"step_ticks": 10}), None, "loc_a", "loc_b")
    # the missing block
    rules_none = _rules(claims, travel={"step_ticks": 10})
    rules_none.pop("travel")
    with pytest.raises(TravelError, match="no 'travel' block"):
        travel_ticks(rules_none, world, "loc_a", "loc_b")


# -- the pack lint (the crafted-twin probes) ---------------------------------


def test_committed_pack_stays_unarmed() -> None:
    """The 68a pattern: the committed pack declares no travel block and
    no edge-priced action — the v0.1 bytes untouched, zero corpus
    re-pins by construction; the arming rides with a future content
    row (world-2's province)."""
    assert "travel" not in PACK.rules
    actions = json.loads(
        (REPO / "content" / "tavern_pack" / "actions.json").read_text(encoding="utf-8")
    )["actions"]
    assert all(action["ticks"] != "edge" for action in actions)


def test_the_armed_twin_loads(tmp_path: Path) -> None:
    """The crafted twin is legal: the pairing holds, the weights are
    well-formed, every unclaimed-endpoint edge carries an override (the
    coverage law over the committed exits graph)."""
    _target, pack = travel_pack(tmp_path, "armed")
    assert "travel" in pack.rules
    assert pack.action("travel") is not None


def _rules_mutate(**field: Any) -> Callable[[Path], None]:
    """A rules.json mutator: overwrite the travel block's fields (DEL
    drops the whole block)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        travel = rules.get("travel", {})
        for key, value in field.items():
            if value is DEL:
                travel.pop(key, None)
            else:
                travel[key] = value
        if travel:
            rules["travel"] = travel
        else:
            rules.pop("travel", None)
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


DEL = object()


def _drop_block(target: Path) -> None:
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules.pop("travel", None)
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _drop_action(target: Path) -> None:
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    actions["actions"] = [
        a for a in actions["actions"] if a["intent"] != "travel"
    ]
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _action_mutate(**field: Any) -> Callable[[Path], None]:
    """An actions.json mutator: overwrite the travel action's fields."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
        action = next(a for a in actions["actions"] if a["intent"] == "travel")
        for key, value in field.items():
            if value is DEL:
                action.pop(key, None)
            else:
                action[key] = value
        (target / "actions.json").write_text(
            json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


def test_lint_pairing_both_ways(tmp_path: Path) -> None:
    """An edge-priced action without the block is dead vocabulary; a
    block without an edge-priced action is dead data — both refused."""
    with pytest.raises(PackError, match="no 'travel' block"):
        _mutated(tmp_path, "no_block", _drop_block)
    with pytest.raises(PackError, match="without an edge-priced action"):
        _mutated(tmp_path, "no_action", _drop_action)


def test_lint_edge_ticks_movement_only(tmp_path: Path) -> None:
    """`ticks: 'edge'` is the movement family's price mode — any other
    resolver is refused (the status_effects family law)."""
    with pytest.raises(PackError, match="movement family's price mode"):
        _mutated(tmp_path, "wrong_resolver", _action_mutate(resolver="wait"))
    with pytest.raises(PackError, match="must be int, \\{min,max\\}, 'N' or 'edge'"):
        _mutated(tmp_path, "bad_ticks", _action_mutate(ticks="road"))


def test_lint_weights(tmp_path: Path) -> None:
    """step_ticks >= 1 (zero makes same-cell edges free); the modifiers
    >= 0 — an off modifier is policy, and OMITTED is legal."""
    with pytest.raises(PackError, match="step_ticks must be an integer >= 1"):
        _mutated(tmp_path, "step_zero", _rules_mutate(step_ticks=0))
    with pytest.raises(PackError, match="step_ticks must be an integer >= 1"):
        _mutated(tmp_path, "step_missing", _rules_mutate(step_ticks=DEL))
    with pytest.raises(PackError, match="climb_ticks must be an integer >= 0"):
        _mutated(tmp_path, "climb_negative", _rules_mutate(climb_ticks=-1))
    # omitted modifiers are legal policy (the derived law alone)
    pack = _mutated(tmp_path, "climb_off", _rules_mutate(climb_ticks=DEL))
    assert "climb_ticks" not in pack.rules["travel"]


def test_lint_override_shapes(tmp_path: Path) -> None:
    """One entry per undirected REAL edge: a non-edge pair prices a
    road that does not exist, a duplicate double-declares, zero ticks
    are degenerate, unknown keys are refused, an empty list is dead
    data."""
    with pytest.raises(PackError, match="is not an exits edge"):
        _mutated(
            tmp_path, "non_edge",
            _rules_mutate(edges=[{"from": "loc_tavern", "to": "loc_market", "ticks": 10}]),
        )
    with pytest.raises(PackError, match="overridden twice"):
        _mutated(
            tmp_path, "duplicate",
            _rules_mutate(edges=OVERRIDES + [dict(OVERRIDES[0])]),
        )
    with pytest.raises(PackError, match="ticks must be an integer >= 1"):
        _mutated(
            tmp_path, "zero_ticks",
            _rules_mutate(edges=[{"from": "loc_tavern", "to": "loc_backyard", "ticks": 0}]),
        )
    with pytest.raises(PackError, match="unknown keys \\['weight'\\]"):
        _mutated(
            tmp_path, "unknown_key",
            _rules_mutate(
                edges=[{"from": "loc_tavern", "to": "loc_backyard",
                        "ticks": 10, "weight": 2}]
            ),
        )
    with pytest.raises(PackError, match="an empty list is dead data"):
        _mutated(tmp_path, "empty_edges", _rules_mutate(edges=[]))


def test_lint_coverage(tmp_path: Path) -> None:
    """The coverage law: with the travel verb declared, every exits
    edge is priceable — dropping an unclaimed-endpoint edge's override
    leaves a road the verb would hard-fail on, refused at load."""
    shortened = [e for e in OVERRIDES if e["to"] != "loc_market"]
    assert len(shortened) < len(OVERRIDES)
    with pytest.raises(PackError, match="carries no override and an endpoint is unclaimed"):
        _mutated(tmp_path, "uncovered", _rules_mutate(edges=shortened))


# -- the accept door (the e2e over the crafted twin) --------------------------


def test_travel_completes_at_the_derived_price(tmp_path: Path) -> None:
    """The completion lands at `t + price` with the price in the
    outcome; the position change is the movement twin's; the departure
    and arrival sightings ride the event (the movement twin's
    knowledge). The derived arm: the claimed pair (street <-> tavern)
    prices from the WorldModel — the PC starts at the street."""
    _target, pack = travel_pack(tmp_path, "e2e")
    log = tmp_path / "e2e.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    price = travel_ticks(pack.rules, sim.world, "loc_street", "loc_tavern")
    assert price >= 600  # the step term alone (1 lattice step)
    sim.run_steps([{"intent": "travel", "target": "loc_tavern"}])
    sim.close()
    travels = [e for e in _events(log) if e.type == TRAVEL_EVENT]
    assert len(travels) == 1
    event = travels[0]
    assert event.t == price
    assert event.outcome["duration"] == price  # the price IS the duration
    changes = list(event.state_changes)
    assert changes[0].entity == "pc_01"
    assert changes[0].prop == "position"
    assert changes[0].from_ == "loc_street"
    assert changes[0].to_ == "loc_tavern"
    knows = {record.knows for record in event.knowledge}
    # the arrival sighting: the tavern's occupants see the PC arrive
    # (the movement twin's destination_location record; the street holds
    # no other observer, so the departure record has no audience)
    assert "pc_01_arrived" in knows


def test_travel_completes_at_the_override_price(tmp_path: Path) -> None:
    """The override arm: an authored per-edge price beats the derived
    law (the pack wins) — the street -> backyard road prices at 350,
    the backyard -> tavern return at 400."""
    _target, pack = travel_pack(tmp_path, "e2e_override")
    steps = [
        {"intent": "travel", "target": "loc_backyard"},
        {"intent": "travel", "target": "loc_tavern"},
    ]
    log = _run(tmp_path, pack, 42, steps, "e2e_override")
    travels = [e for e in _events(log) if e.type == TRAVEL_EVENT]
    assert [e.outcome["duration"] for e in travels] == [350, 400]
    assert travels[1].t == 350 + 400


def test_travel_rejects_nonadjacent(tmp_path: Path) -> None:
    """Travel follows the exits graph like move (the adjacent_to
    precondition): from the market (whose only exit is the street) the
    backyard is NOT adjacent — a rejection, no ticks consumed, the
    movement twin's own door."""
    _target, pack = travel_pack(tmp_path, "reject")
    steps = [
        {"intent": "travel", "target": "loc_market"},  # adjacent to the street
        {"intent": "travel", "target": "loc_backyard"},  # NOT adjacent to the market
    ]
    log = _run(tmp_path, pack, 42, steps, "reject")
    events = _events(log)
    rejected = [e for e in events if e.type == "intent_rejected"]
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "target.adjacent_to"
    travels = [e for e in events if e.type == TRAVEL_EVENT]
    assert len(travels) == 1  # the first step only
    assert rejected[0].t == travels[0].t  # a rejection consumes no ticks


def test_crossings_fire_mid_travel(tmp_path: Path) -> None:
    """D-038's letter: beats and rotations still fire mid-travel in
    tick order — a day-scale road (the street -> backyard override
    raised to 1500) spans the rotation at 360 and the beats, and the
    completion lands AFTER them all."""
    long_road = [
        {"from": "loc_street", "to": "loc_backyard", "ticks": 1500},
        *OVERRIDES[:1],
        *OVERRIDES[2:],
    ]
    _target, pack = travel_pack(tmp_path, "midtravel", overrides=long_road)
    log = _run(
        tmp_path, pack, 42,
        [{"intent": "travel", "target": "loc_backyard"}], "midtravel",
    )
    events = _events(log)
    travel = next(e for e in events if e.type == TRAVEL_EVENT)
    assert travel.t == 1500
    rotations = [
        e for e in events if e.type == "watch_change" and 0 < e.t < 1500
    ]
    assert rotations, "the watch rotation must fire mid-travel (D-038)"
    assert all(e.t < travel.t for e in rotations)


def test_determinism_byte_identical(tmp_path: Path) -> None:
    """The armed twin is deterministic: the same seed, the same steps —
    byte-identical logs (the price is a pure function of pack data +
    the genesis-frozen model; no stream is ever touched)."""
    _target, pack = travel_pack(tmp_path, "det")
    steps = [
        {"intent": "travel", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 5},
        {"intent": "travel", "target": "loc_backyard"},
    ]
    first = _run(tmp_path, pack, 42, steps, "det_a")
    second = _run(tmp_path, pack, 42, steps, "det_b")
    assert first.read_bytes() == second.read_bytes()
    travels = [e for e in _events(first) if e.type == TRAVEL_EVENT]
    assert len(travels) == 2
