"""iter-107 — the blast-radius drift test (the risk-synthesis §5 rider:
"declared system components vs the actual state prefixes").

Two tables already own the system ⇔ state-vocabulary wiring:
`rules.json::systems` (the scheduler DAG's reads/writes annotations)
and `core/metrics.py::_PROP_PREFIX_TO_SYSTEM` (M1's prop-prefix →
system classification). They drift independently — a new mechanic
starts writing new `state_change` prefixes, a pack edits its systems
table, and M1 silently undercounts (unclassified props cross nothing).
This suite pins the contract in four directions:

(a) no phantom systems — every system the metrics map names is
    declared in the pack's systems table;
(b) claimed prefixes — every metrics key is claimed (reads ∪ writes)
    by its mapped system, modulo the two pinned ALIASES (the
    per-target and crime-lifecycle axes);
(c) declared-write coverage — every component a system declares as a
    WRITE is classified by the metrics map or is a declared
    NON-state_change channel (the clock axis, the knowledge records);
(d) the observed vocabulary — every `state_change.prop` head over the
    reference corpus (both gate scripts, the fire arm included) is
    classified, derived pack vocabulary (worldgen claim slots,
    transition follow-up flags, scene-detail slots), or one of the two
    pinned item-side families — anything NEW fails here until the
    metrics map (or the registry) grows with it.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.metrics import _PROP_PREFIX_TO_SYSTEM
from core.pack import load_pack
from core.scheduler import decls_from_rules

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(PACK_DIR)
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

#: (b) — the pinned aliases: prefixes the metrics map routes to a
#: system through a family axis, not a literal reads/writes entry.
#: Renaming either axis (suspectaxis-2, the crime lifecycle) without
#: updating the metrics map is exactly the drift this table prevents.
ALIASES: dict[str, str] = {
    "pair": "the relations system's per-target axis "
            "(pair.<figure>.suspicion, suspectaxis-2)",
    "crime_status": "the crime_watch system's status-lifecycle marker",
}

#: (c) — declared WRITE components that are not state_change
#: vocabulary by design (side-band channels): each with its reason.
NON_STATE_CHANNELS: dict[str, str] = {
    "time": "the clock axis — folded by the projection, never a "
            "state_change prop",
    "knowledge": "the records ride event.knowledge (a side-band array), "
                 "never state_changes",
}

#: (d) — the pinned item-side families: mechanic props with no
#: systems-table row (the scheduler never runs them; M1 leaves them
#: uncrossed by the map's own docstring law). A future pack declaring
#: an acquisition/conditioning system row must retire its entry here.
UNCLASSIFIED_REGISTRY: dict[str, str] = {
    "carrier": "the acquisition family (depth-1): an item's holder — "
               "no systems row declares it",
    "condition": "the status-effects family (tune-1): an item's broken "
                 "flag — no systems row declares it",
}


def _derived_pack_vocabulary(rules: dict) -> set[str]:
    """The non-mechanic prop vocabulary derived from the pack's own
    data: worldgen claim slots, transition follow-up flags, scene-detail
    slots — generated/optional surfaces, deliberately uncrossed."""
    vocab: set[str] = set()
    for claim in rules.get("worldgen", {}).get("claims", ()):
        if isinstance(claim, dict) and "slot" in claim:
            vocab.add(str(claim["slot"]))
    for layer in rules.get("transitions", {}).values():
        if not isinstance(layer, dict):
            continue
        for spec in layer.get("follow_ups", ()):
            if isinstance(spec, dict) and "flag" in spec:
                vocab.add(str(spec["flag"]))
    for slots in rules.get("scene_detail", {}).values():
        for spec in slots:
            if isinstance(spec, dict) and "slot" in spec:
                vocab.add(str(spec["slot"]))
    return vocab


def _observed_heads(log_path: Path) -> set[str]:
    _header, events = read_log(log_path, SCHEMA)
    return {
        change.prop.split(".", 1)[0]
        for event in events
        for change in event.state_changes
    }


def _run(script_name: str, seed: int, directors: bool, tmp_path: Path) -> Path:
    script = load_playscript(REPO / "tests" / "playscripts" / script_name)
    log = tmp_path / f"drift_{script_name}_{seed}_{'on' if directors else 'off'}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000",
                    director_enabled=directors)
    sim.run_playscript(dict(script, seed=seed))
    return log


# -- (a) no phantom systems ----------------------------------------------------


def test_metrics_map_names_no_phantom_systems() -> None:
    """Every system the prop-prefix map routes to must exist as a
    declared systems row — a renamed/removed row with a stale map is
    the cheapest drift to catch and the loudest to run with."""
    declared = set(decls_from_rules(PACK.rules))
    for prop, system in sorted(_PROP_PREFIX_TO_SYSTEM.items()):
        assert system in declared, (
            f"metrics map routes {prop!r} to undeclared system {system!r} "
            f"(declared: {sorted(declared)})"
        )


# -- (b) claimed prefixes ------------------------------------------------------


def test_metrics_prefixes_claimed_by_their_systems() -> None:
    """Every mapped prefix is claimed by its system's own reads/writes
    declaration — through a literal entry or one of the pinned
    ALIASES (the family axes; the alias table documents why the literal
    entry does not exist)."""
    declared = decls_from_rules(PACK.rules)
    for prop, system in sorted(_PROP_PREFIX_TO_SYSTEM.items()):
        if prop in ALIASES:
            assert system in declared  # the alias still names a real row
            continue
        decl = declared[system]
        claimed = set(decl.reads) | set(decl.writes)
        assert prop in claimed, (
            f"{system!r} does not claim {prop!r} "
            f"(reads {list(decl.reads)}, writes {list(decl.writes)}) — "
            "either the pack drifted or the metrics map did"
        )
    # the alias table itself stays pinned to the map's real keys
    assert set(ALIASES) <= set(_PROP_PREFIX_TO_SYSTEM)


# -- (c) declared-write coverage -----------------------------------------------


def test_declared_write_components_classified_or_sideband() -> None:
    """Every component declared as a WRITE by a system is either
    classified by the metrics map (a state_change vocabulary the M1
    crossing owns), a pinned non-state_change side-band channel (the
    clock axis, the knowledge records), or derived follow-up-flag
    vocabulary (the `smoke`/`destroyed` location lifecycle — state
    changes the map deliberately leaves uncrossed). A new write
    component joins one of the three or fails here."""
    classified = set(_PROP_PREFIX_TO_SYSTEM)
    derived = _derived_pack_vocabulary(dict(PACK.rules))
    for name, decl in sorted(decls_from_rules(PACK.rules).items()):
        for component in decl.writes:
            assert (
                component in classified
                or component in NON_STATE_CHANNELS
                or component in derived
            ), (
                f"system {name!r} declares write {component!r} that the "
                "metrics map neither classifies, nor the side-band table "
                "exempts, nor the follow-up flags derive — the tables "
                "drifted apart"
            )
    assert set(NON_STATE_CHANNELS).isdisjoint(classified)


# -- (d) the observed corpus vocabulary -----------------------------------------


def test_observed_prop_heads_are_known_vocabulary(tmp_path: Path) -> None:
    """The reference corpus (both gate scripts, the fire arm at its
    deterministic seed, directors on and off) writes only classified
    mechanic prefixes, derived pack vocabulary, or the pinned
    item-side families. A new mechanic family (res-1's res.*, a
    containers law) fails here until its vocabulary is deliberate."""
    allowed = (
        set(_PROP_PREFIX_TO_SYSTEM)
        | set(UNCLASSIFIED_REGISTRY)
        | _derived_pack_vocabulary(dict(PACK.rules))
    )
    observed: set[str] = set()
    for script_name, seed, directors in (
        ("day1_full.json", 100, True),
        ("day1_full.json", 100, False),
        ("day1_theft_and_arson.json", 8, True),
    ):
        observed |= _observed_heads(_run(script_name, seed, directors, tmp_path))
    unknown = observed - allowed
    assert not unknown, (
        f"unregistered state_change prop heads observed: {sorted(unknown)} "
        f"(allowed: {sorted(allowed)}) — a new mechanic vocabulary landed "
        "without joining the metrics map or the registry"
    )
    # the corpus must actually exercise the fire family (the seed-8 arm)
    assert "fire" in observed or "smoke" in observed or "destroyed" in observed
    # and the genesis/claim family (worldgen's armed genesis)
    assert "terrain" in observed
    # and the item-side registry families (take/drop run in both scripts)
    assert "carrier" in observed


def test_registry_stays_honest_against_the_pack() -> None:
    """The registry's families may not silently become classified: if a
    future pack declares systems rows that claim `carrier`/`condition`,
    the registry entry retires (this test fails until it does) — the
    drift contract cuts both ways."""
    declared = decls_from_rules(PACK.rules)
    for prop in UNCLASSIFIED_REGISTRY:
        for decl in declared.values():
            claimed = set(decl.reads) | set(decl.writes)
            assert prop not in claimed or prop in _PROP_PREFIX_TO_SYSTEM, (
                f"{prop!r} is now claimed by {decl.name!r} but stays in the "
                "unclassified registry — retire the entry"
            )
