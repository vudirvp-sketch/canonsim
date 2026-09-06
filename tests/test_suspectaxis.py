"""iter-69 acceptance — suspectaxis (the v0.2 refinement family's fifth
segment, D-095/D-101/TASKS: "per-target suspicion: the pair axis + the
parameterized suspect_id" — the drift teeth's first CONSUMER). Mechanics
landed declarative-only: the committed pack keeps the flat v0.1 mapping
(the string shape), so the committed bytes are the v0.1 bytes by
construction — the arming (the committed pack's per-target switch + the
measured corpus price) is suspectaxis-2's row, the 68a→68b pattern.

The laws pinned here:

- **The mode law (suspectaxis):** a `suspicion_from_knowledge` entry is
  either the v0.1 flat string (token → source; the axis
  `relations.<axis>`, the suspect hard-wired to the player) or the
  per-target object (token → `{source, figure}`; the knower's axis
  `pair.<figure>.<axis>`, the status flip and the arrest aimed at the
  figure). One mode per pack — the lint refuses mixing; a flat mapping
  keeps the v0.1 event shapes verbatim (the zero-price construction).
- **The pair-home law:** the reaction's permission is the SEEDED pair
  axis (the P2a home — the "no suspicion home" law translated from the
  flat seed); a knower without the home never reacts, the player
  included.
- **The blame law (the drift teeth):** a rumor-mutated token reacts
  under the MUTATED token's figure — the blame lands where the drift
  put it, never where the sighting did. The figure's status flip rides
  the crossing exactly as the player's did (the ev_0007 shape, aimed at
  the figure).
- **The aggregate law:** the director's global suspicion sums the axis
  in either home — a pack runs one mode, the other home never moves;
  the director senses the axis, not the storage.

Seeds are probed to be deterministic (T1 discipline; the drift-hit seed
2 and the miss seed 1 reuse the 68b guard-talk geometry verbatim).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.director import _global_suspicion
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

GUARD = "npc_guard_01"
PLAYER = "pc_01"
BARKEEP = "npc_barkeep_01"
SOURCE = "figure_reaching_for_purse"
SIBLING = "figure_starting_fire"

GUARD_TALK: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": GUARD},
    {"intent": "talk", "target": GUARD},
]

# the crafted per-target deltas: the arson source rides the sibling token
WITNESSED_ARSON = {"witnessed_arson": 30}


def targeted_pack(
    tmp_path: Path,
    name: str,
    mapping: dict[str, Any],
    pair_seeds: dict[str, dict[str, int]] | None = None,
    status_seeds: dict[str, str] | None = None,
    extra_sources: dict[str, int] | None = None,
) -> Pack:
    """A committed-pack copy switched to the per-target mode: the
    mapping re-shaped (token → {source, figure}), the named pair homes
    seeded (`pair.<with>.<axis>` on the holder), optional crime_status
    seeds, optional new suspicion sources. The drift family and every
    check number ride the committed pack verbatim — no draw shifts, the
    68b seed geometry replicates (the mechanism-proof pattern,
    test_crime.py's tuned_pack)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["crime_watch"]["suspicion_from_knowledge"] = mapping
    if extra_sources:
        rules["crime_watch"]["suspicion_sources"].update(extra_sources)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    for npc in entities["npcs"]:
        for other, value in (pair_seeds or {}).get(npc["id"], {}).items():
            npc.setdefault("pair_relations", []).append(
                {"with": other, "suspicion": value}
            )
        if npc["id"] in (status_seeds or {}):
            npc["crime_status"] = status_seeds[npc["id"]]
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[list[Any], Simulator]:
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, sim


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


def suspicion_changes(events: list[Any]) -> list[Any]:
    """Every state change on a suspicion home (either mode) in log order."""
    out = []
    for event in events:
        for change in event.state_changes:
            if change.prop == "relations.suspicion" or (
                change.prop.startswith("pair.") and change.prop.endswith(".suspicion")
            ):
                out.append(change)
    return out


# -- the zero-price construction (the declarative-only law) --------------------


def test_the_committed_pack_stays_flat() -> None:
    """The declarative-only pin: every committed mapping entry is the
    v0.1 string shape — the flat mode, the suspect hard-wired to the
    player. The per-target shape is live on crafted packs only until
    suspectaxis-2 arms the committed pack (the 68a→68b pattern: the
    mechanics land, the arming is its own measured row)."""
    mapping = PACK.rules["crime_watch"]["suspicion_from_knowledge"]
    assert mapping, "the committed pack must map suspicion tokens"
    assert all(isinstance(spec, str) for spec in mapping.values())


def test_flat_mode_events_are_the_v01_shapes(tmp_path: Path) -> None:
    """The zero-price pin's live half: the committed (flat) pack over the
    68b guard-talk geometry emits the v0.1 event shapes verbatim — the
    guard's reaction lands on `relations.suspicion`, the event targets
    the player, the outcome carries exactly the v0.1 fields, and no
    pair-axis suspicion state change exists anywhere in the log (the
    mechanics changed nothing for the committed mode; test_crime.py's
    suite pins the same contract on the other geometries)."""
    events, _ = run(tmp_path, PACK, 2, GUARD_TALK, "flat.jsonl")
    reactions = by_type(events, "suspicion_changed")
    assert reactions, "the failed steal must move the guard's suspicion"
    for event in reactions:
        assert event.target == PLAYER
        assert set(event.outcome) == {"token", "source", "delta", "from", "to"}
        for change in event.state_changes:
            assert change.prop in ("relations.suspicion", "crime_status")
    assert all(
        change.prop == "relations.suspicion" for change in suspicion_changes(events)
    )


# -- the per-target mechanics (crafted packs) ----------------------------------


def test_the_pair_axis_write_and_the_v0007_shape(tmp_path: Path) -> None:
    """The per-target reaction: the knower's axis lives at
    `pair.<figure>.<axis>` (the P2a home), the event targets the FIGURE,
    and the crossing carries the status flip on the figure exactly as
    ev_0007 carried it on the player — one event, both changes (the
    ev_0007 shape aimed at the parameterized suspect)."""
    pack = targeted_pack(
        tmp_path, "paired",
        mapping={SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER}},
        pair_seeds={GUARD: {PLAYER: 0}},
    )
    events, _ = run(tmp_path, pack, 2, GUARD_TALK, "paired.jsonl")
    reaction = by_type(events, "suspicion_changed")[0]
    assert reaction.actor == GUARD and reaction.target == PLAYER
    assert reaction.outcome == {
        "token": SOURCE, "source": "witnessed_steal_failure",
        "delta": 25, "from": 0, "to": 25,
    }
    assert [(c.entity, c.prop, c.from_, c.to_) for c in reaction.state_changes] == [
        (GUARD, f"pair.{PLAYER}.suspicion", 0, 25),
        (PLAYER, "crime_status", "unknown", "suspect"),
    ]


def test_two_figures_never_share_a_pair_record(tmp_path: Path) -> None:
    """The separation law (the parameterized suspect's whole point): two
    tokens with different figures move two DIFFERENT pair records — the
    guard witnessing the purse-reach (figure: the player) moves
    `pair.pc_01.suspicion` and never touches the barkeep's record, even
    though the guard holds both homes (per-target suspicion is directed
    state, not a watch-score)."""
    pack = targeted_pack(
        tmp_path, "two_figures",
        mapping={
            SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER},
            SIBLING: {"source": "witnessed_arson", "figure": BARKEEP},
        },
        pair_seeds={GUARD: {PLAYER: 0, BARKEEP: 0}},
        status_seeds={BARKEEP: "unknown"},
        extra_sources=WITNESSED_ARSON,
    )
    events, _ = run(tmp_path, pack, 2, GUARD_TALK[:2], "two_figures.jsonl")
    moves = {(c.entity, c.prop, c.to_) for c in suspicion_changes(events)}
    assert (GUARD, f"pair.{PLAYER}.suspicion", 25) in moves
    assert not any(prop.endswith(f"{BARKEEP}.suspicion") for _, prop, _ in moves)


def test_a_knower_without_the_pair_home_never_reacts(tmp_path: Path) -> None:
    """The pair-home law: the reaction's permission is the seeded pair
    axis — the v0.1 "no suspicion home" law translated to the P2a home.
    The player (who receives the drifted token in the 68b geometry)
    holds no pair home toward the barkeep here, so the mutated token
    moves nothing; the guard's own home fires exactly once (the direct
    sighting)."""
    pack = targeted_pack(
        tmp_path, "homeless",
        mapping={
            SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER},
            SIBLING: {"source": "witnessed_arson", "figure": BARKEEP},
        },
        pair_seeds={GUARD: {PLAYER: 0}},
        status_seeds={BARKEEP: "unknown"},
        extra_sources=WITNESSED_ARSON,
    )
    events, _ = run(tmp_path, pack, 2, GUARD_TALK, "homeless.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["drifted_from"] == SOURCE  # the 68b hit replicates
    reactors = {e.actor for e in by_type(events, "suspicion_changed")}
    assert reactors == {GUARD}
    assert not any(
        c.entity == PLAYER for c in suspicion_changes(events)
    )


# -- the drift teeth (the first consumer, live) --------------------------------


def test_the_mutated_token_blames_its_own_figure(tmp_path: Path) -> None:
    """The blame law — the landing's headline: the guard's sighting of
    the purse-reach (figure: the player) mutates as it is told, and the
    LISTENER reacts under the MUTATED token's figure (the barkeep) —
    the blame lands where the drift put it, never where the sighting
    did. The received delta is the sibling's source (the arson delta,
    not the theft delta), the flip lands on the barkeep's crime_status,
    and no fire ever happened in the geometry: the drift's teeth
    manufacture a suspect out of a mutated retelling (the 68b liveness
    geometry, seed 2's hit, reused verbatim)."""
    pack = targeted_pack(
        tmp_path, "teeth",
        mapping={
            SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER},
            SIBLING: {"source": "witnessed_arson", "figure": BARKEEP},
        },
        pair_seeds={GUARD: {PLAYER: 0}, PLAYER: {BARKEEP: 0}},
        status_seeds={BARKEEP: "unknown"},
        extra_sources=WITNESSED_ARSON,
    )
    events, sim = run(tmp_path, pack, 2, GUARD_TALK, "teeth.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is True
    assert telling.outcome["knows"] == SIBLING
    assert telling.outcome["drifted_from"] == SOURCE
    assert (SIBLING, "told", "vague") in [
        (r.knows, r.channel, r.fidelity) for r in sim.knowledge.records_of(PLAYER)
    ]
    # the guard's own sighting still blames the player (+25, flat twin)
    # the player's reaction blames the BARKEEP (+30, the arson delta)
    reaction = next(
        e for e in by_type(events, "suspicion_changed") if e.actor == PLAYER
    )
    assert reaction.target == BARKEEP
    assert reaction.outcome["source"] == "witnessed_arson"
    assert reaction.outcome["from"] == 0 and reaction.outcome["to"] == 30
    assert [(c.entity, c.prop, c.from_, c.to_) for c in reaction.state_changes] == [
        (PLAYER, f"pair.{BARKEEP}.suspicion", 0, 30),
        (BARKEEP, "crime_status", "unknown", "suspect"),
    ]


def test_the_arrest_aims_at_the_mutated_figure(tmp_path: Path) -> None:
    """The arrest ladder, aimed: the player's pair record crossing the
    arrest threshold co-located with the FIGURE emits the attempt
    against the barkeep (the parameterized suspect's teeth — an arrest
    manufactured by a mutated rumor), and the resolution resolves
    against the figure's evasion (its own skills, its own status; the
    caught flip lands on the barkeep, irreversible per the pack)."""
    pack = targeted_pack(
        tmp_path, "arrest",
        mapping={
            SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER},
            SIBLING: {"source": "witnessed_arson", "figure": BARKEEP},
        },
        pair_seeds={GUARD: {PLAYER: 0}, PLAYER: {BARKEEP: 70}},
        status_seeds={BARKEEP: "unknown"},
        extra_sources=WITNESSED_ARSON,
    )
    events, _ = run(tmp_path, pack, 2, GUARD_TALK, "arrest.jsonl")
    attempt = by_type(events, "arrest_attempt")[0]
    assert attempt.actor == PLAYER and attempt.target == BARKEEP
    assert attempt.outcome == {"suspicion": 100, "threshold": 75}
    resolution = by_type(events, "arrest_resolved")[0]
    assert resolution.actor == PLAYER and resolution.target == BARKEEP
    if resolution.outcome["caught"]:
        flip = next(
            c for c in resolution.state_changes if c.prop == "crime_status"
        )
        assert (flip.entity, flip.to_, flip.irreversible) == (
            BARKEEP, "caught", True,
        )
    else:
        assert resolution.state_changes == ()


def test_a_miss_keeps_the_true_tokens_blame(tmp_path: Path) -> None:
    """The miss law (the blame's other arm): seed 1's drift roll misses
    — the listener receives the TRUE token (the purse sighting, figure:
    the player), and no barkeep blame ever fires: the guard's reaction
    blames the player under the theft source, and the player holds no
    home toward their own figure (a self-pair is pack-illegal — the
    home law makes self-blame structurally impossible, not merely
    unseeded). The blame follows the token actually received, never
    the family's orbit."""
    pack = targeted_pack(
        tmp_path, "miss",
        mapping={
            SOURCE: {"source": "witnessed_steal_failure", "figure": PLAYER},
            SIBLING: {"source": "witnessed_arson", "figure": BARKEEP},
        },
        pair_seeds={GUARD: {PLAYER: 0}},
        extra_sources=WITNESSED_ARSON,
    )
    events, _ = run(tmp_path, pack, 1, GUARD_TALK, "miss.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["knows"] == SOURCE
    assert "drifted_from" not in telling.outcome
    reactions = by_type(events, "suspicion_changed")
    assert {e.actor for e in reactions} == {GUARD}
    assert all(e.target == PLAYER for e in reactions)
    assert all(e.outcome["source"] == "witnessed_steal_failure" for e in reactions)
    assert not any(
        prop.endswith(f"{BARKEEP}.suspicion")
        for prop in (c.prop for c in suspicion_changes(events))
    )


# -- the lint (the closed pack vocabulary) -------------------------------------


def _mutate_committed(tmp_path: Path, name: str, mutate: Any) -> Path:
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate(rules["crime_watch"])
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return target


def test_the_lint_refuses_mode_mixing(tmp_path: Path) -> None:
    """One mode per pack: a string entry beside an object entry refuses
    to load (the flat and per-target homes must never both move — the
    director's aggregate would double-count, the fold would hold two
    homes for one fact)."""
    def mutate(crime: dict[str, Any]) -> None:
        crime["suspicion_from_knowledge"][SOURCE] = {
            "source": "witnessed_steal_failure", "figure": PLAYER,
        }

    with pytest.raises(PackError, match="mixes the flat v0.1 shape"):
        load_pack(_mutate_committed(tmp_path, "mixed", mutate))


def test_the_lint_refuses_an_unknown_figure(tmp_path: Path) -> None:
    """The figure must be an npc of the same pack — a closed vocabulary
    (an id outside the entity list is a typo, never a second world)."""
    def mutate(crime: dict[str, Any]) -> None:
        crime["suspicion_from_knowledge"] = {
            SOURCE: {"source": "witnessed_steal_failure", "figure": "npc_ghost_01"},
        }

    with pytest.raises(PackError, match="is not an npc"):
        load_pack(_mutate_committed(tmp_path, "ghost", mutate))


def test_the_lint_refuses_an_unknown_source_in_object_shape(tmp_path: Path) -> None:
    """The object shape validates its source exactly as the flat shape
    always did — the delta vocabulary stays closed across the mode
    boundary."""
    def mutate(crime: dict[str, Any]) -> None:
        crime["suspicion_from_knowledge"] = {
            SOURCE: {"source": "witnessed_nonsense", "figure": PLAYER},
        }

    with pytest.raises(PackError, match="unknown suspicion source"):
        load_pack(_mutate_committed(tmp_path, "bad_source", mutate))


# -- the aggregate (the director senses the axis, not the storage) --------------


def test_the_director_senses_both_homes() -> None:
    """`_global_suspicion` sums the suspicion axis in either home: the
    flat v0.1 axis and the per-target pair records, never the other
    pair axes, never non-int values. A pack runs one mode and the other
    home never moves (the no-mixing lint), so the two terms never
    double-count one knower."""
    projection = {
        "npc_flat": {"relations.suspicion": 20},
        "npc_pair": {"pair.pc_01.suspicion": 30, "pair.pc_01.trust": 90},
        "npc_other": {"pair.pc_01.trust": 10, "relations.trust": 55},
        "pc_01": {"position": "loc_tavern"},
    }
    assert _global_suspicion(projection) == 50
