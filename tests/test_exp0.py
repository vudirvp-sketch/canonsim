"""Experiment 0 — the capability/progression falsifier, executed (iter-183).

The parked capability/progression consult card (intake-34, D-194) carries
its own decision rule: run ONE long scenario, zero implementation — no
quality deficit expressible through status/relations/knowledge/resources/
world state means no progression layer. The intake-35 reframe (D-195)
sharpens the read: the landed folds already implement differential
evidence weighting (knowledge fidelity-weighted, echo/traits
recurrence-weighted), so the null is «growth runs on the landed folds»,
and the discriminating scenario is procedural skill (the corpus's musket
stress case: knowledge records + traits exist, no per-actor resolution
modifier).

`tests/playscripts/exp0_week.json` is that scenario — the apprentice
thief's five days: the purse gambit (steal, the crime-mapped escalation),
then the lift-practice loop (take/drop the ale mug, 25 opposed stealth
checks the room's best observer answers), with rests and waits carrying
the world's rotations, beats and transfers. This file pins the measured
evidence at the canonical seed (32) so any future landing that moves the
falsifier's substrate screams: the world-side arcs (leverage, the
expectation violation, the knowledge transfers, the crystallized trait,
the paranoid scans, the document challenge) are the landed folds
carrying growth; the actor-side resolution inputs stay exactly the
day-one values across the whole week of practice — the flat coin. The
verdict itself lives in `docs/blueprint/phases.md` §6 (the intake-34
card's falsifier record), never here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from core.fold import fold, initial_projection  # noqa: E402
from core.intent import skill_total  # noqa: E402
from core.knowledge import KnowledgeView  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.pack import load_pack  # noqa: E402
from core.traits import crystallized_traits  # noqa: E402
from render.chronicle import chronicle_from_log  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(PACK_DIR)
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "exp0_week.json")

#: the check-carrying event types (the procedural-skill family)
SKILL_EVENTS = ("steal", "pickpocket_failed", "take", "take_failed")


def _run(seed: int, tmp_path: Path) -> tuple[list, dict]:
    """One scenario run at `seed` (the script's seed rides the override —
    the playscript law: one committed fixture, any seed)."""
    script = dict(SCRIPT, seed=seed)
    log = tmp_path / f"exp0_{seed}.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="test",
                    director_enabled=True)
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(PACK.entities))
    return events, projection


def _checks(events) -> list[tuple[str, dict]]:
    """Every opposed-check outcome as (event_type, check), in attempt
    order."""
    out = []
    for e in events:
        if e.type in SKILL_EVENTS:
            check = dict(e.outcome or {}).get("check")
            if isinstance(check, dict) and "attacker_total" in check:
                out.append((e.type, check))
    return out


# -- the canonical run: the world remembers, the hand does not ---------------


def test_exp0_world_side_grows_on_the_landed_folds(tmp_path: Path) -> None:
    """Seed 32, the rich arc: the day-one botch seeds the room's memory
    (four leverage holders + the transferred fifth), the purse lift fires
    the expectation violation, the document challenge is answered, the
    trait crystallizes on BOTH guards (the permanent paranoia) and the
    trait-gated scans keep firing all week. Growth runs on the landed
    folds — the reframe's null, measured."""
    events, projection = _run(32, tmp_path)
    types = [e.type for e in events]
    assert types.count("leverage_gained") == 5  # the botch's social residue
    assert types.count("expectation_violation") == 1  # the purse discovery
    assert types.count("document_check_failed") == 1  # the challenge answered
    assert types.count("knowledge_transfer") == 2  # the watch rotations
    assert types.count("look_around") == 9  # the trait-gated paranoid scans
    # the crystallized trait: both guards, permanent
    traits = crystallized_traits(
        PACK, KnowledgeView.from_events(events), events[-1].t
    )
    assert {(t.who, t.token) for t in traits} == {
        ("npc_guard_01", "paranoid_about_thieves"),
        ("npc_guard_02", "paranoid_about_thieves"),
    }
    # the persistent suspicion axis, below the arrest threshold all week
    assert projection["npc_guard_01"]["pair.pc_01.suspicion"] == 55
    assert projection["npc_guard_02"]["pair.pc_01.suspicion"] == 55
    # the chronicle tells it as a story (the tale-gated read of the same)
    text = chronicle_from_log(
        tmp_path / "exp0_32.jsonl", PACK, SCHEMA
    )
    for line in (
        "the player's hand drifts toward Doren's purse — Doren notices "
        "the movement.",
        "the player lifts the purse unseen.",
        "Doren checks on the purse — it is not where it should be.",
        "Doren demands papers from the player — the answer satisfies.",
        "The room watches the player closely.",
        "the player takes the mug of ale.",
        "the mug of ale breaks with a noise.",
    ):
        assert line in text


def test_exp0_actor_side_stays_the_day_one_coin(tmp_path: Path) -> None:
    """The falsifier's flat half, pinned: 27 opposed checks over the week
    (25 lift attempts, 3 wins; the purse gambit 1-of-2 — the botch, then
    the luck), every attacker total inside base + d20, and the actor's
    effective stealth at the run's END exactly the pack base — after 159
    canonical events of practice, nothing in the folded state feeds the
    thief's resolution. A per-actor mastery term (the card's leading
    candidate) fails this pin the day it lands — by design: the verdict's
    substrate, re-verified at every HEAD."""
    events, projection = _run(32, tmp_path)
    checks = _checks(events)
    assert len(events) == 159
    # the purse race first (2 checks: the botch, then the lift), then 25
    # lift attempts — the one-shot purse law: the script's later steal
    # steps reject once the purse rides the actor (attempts are facts)
    assert [kind for kind, _ in checks[:2]] == [
        "pickpocket_failed", "steal",
    ]
    take_totals = [c["attacker_total"] for kind, c in checks if
                   kind in ("take", "take_failed")]
    assert len(take_totals) == 25
    assert sum(1 for kind, c in checks[2:] if c["passed"]) == 3
    assert all(41 <= t <= 60 for t in take_totals)  # stealth base 40 + d20
    # the tripwire: the day-one resolution inputs, unchanged at the horizon
    assert skill_total(PACK, projection, "pc_01", "stealth") == 40
    # the five dimensions that DO move are the world's, not the actor's:
    # the guard's own status drift (fatigue on duty) is the only lawful
    # difficulty mover in the scenario — asserted present, never actor-side
    assert projection["npc_guard_01"]["status.fatigue"] >= 0
    assert "status.fatigue" in projection["pc_01"]  # the rests landed


def test_exp0_sweep_win_vector_is_the_flat_coin(tmp_path: Path) -> None:
    """The distributional half: across the eight pinned sweep seeds the
    lift-attempt win counts are exactly this vector — the flat coin's
    draws. Any systematic per-actor drift (a mastery term, a draw-order
    change, a pack edit to the stealth table) moves the vector and fires
    the pin; the verdict then needs re-reading, not a test tweak."""
    wins = []
    for seed in range(2000, 2008):
        events, _ = _run(seed, tmp_path)
        checks = _checks(events)
        # the lift-attempt count is seed-stable (25); the purse race's
        # check count is the seed's own draw (1-3 attempts before the
        # lift or the script's end) — the race, never the practice
        takes = [c for kind, c in checks if kind in ("take", "take_failed")]
        assert len(takes) == 25
        wins.append(sum(1 for c in takes if c["passed"]))
    assert wins == [7, 2, 4, 1, 7, 4, 6, 5]
