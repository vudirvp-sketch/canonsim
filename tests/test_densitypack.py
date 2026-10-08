"""density-1 — the density-envelope generator's laws (iter-345, the
E02 successor row; TEST_PLAN §9.1's axes made checkable, the
fixture-hardcoding law's instrument side).

The generator (`scripts/densitypack.py`) is the row's only new
mechanism: profile → an ORDINARY VALID PACK through the existing
admission lint (the SCALE_TESTING_LAW §15 boundary — no second
runner, no second schema; the packs are disposable output-family
artifacts, never committed herds).

The laws these tests pin (each one the generator's own contract,
measured in its development, not aspiration):

1. DETERMINISM — the pack is a pure function of (profile, template):
   two materializations of the same profile are byte-identical
   (the scaffold's law; no RNG anywhere in the generator).
2. LINT + AXES — the generated pack loads through the SAME admission
   gate as every committed pack, and the axes are real: L = 7·S,
   E_npcs = 1 + 13·S, groups = 3·S, items = 2·S, actions = 4 + 10·S,
   urgency posts = 14·S + links·S (TEST_PLAN §9.1's declared-not-
   implied requirement).
3. ISOLATION (K=0) — no cross-unit reference anywhere: each unit's
   urgency posts, flows and exits stay inside its own namespace (the
   locality-control baseline; the coupling arm is a later held-out
   row). The player rides unit 0 alone.
4. THE KNOBS — talk_links adds exactly links·S unique-source talk
   posts (AP-11's one-goal-per-NPC-per-verb ceiling enforced loud);
   prob_scale scales the SAMPLED family only (the p=100 crossings
   stay certain — B6's law); the refusal arms are loud SystemExits.
5. THE RUN LAW — a 1y smoke run over the generated pack commits
   events and the T1 double-run is byte-identical: the pack is a
   REAL pack on the real Simulator (the Lab's own F1 form).
6. THE TEMPLATE ECONOMY — templates.json stays the template's tale
   surface verbatim except the flow glosses (keyed by flow id, so
   each unit's flows carry their own): no per-unit chronicle bloat.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from core.log import read_log  # noqa: E402
from core.pack import load_pack  # noqa: E402
from scripts.densitypack import build_pack, materialize  # noqa: E402

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"),
)
RUNNER = REPO / "scripts" / "labrunner.py"
GEN = REPO / "scripts" / "densitypack.py"
#: the unit's own constants (the template's measured shape: 12 adults
#: per unit — the player rides unit 0 alone)
LOC_PER_UNIT, NPC_PER_UNIT, GROUPS_PER_UNIT, ITEMS_PER_UNIT = 7, 12, 3, 2
BOUND_VERBS_PER_UNIT, GENERIC_VERBS = 10, 4
POSTS_PER_UNIT = 14


def _materialize(tmp: Path, settlements: int, links: int = 0,
                 scale: float = 1.0, name: str = "pack") -> Path:
    out = tmp / name
    materialize(out, settlements, links, scale)
    return out


# -- 1: determinism ------------------------------------------------------------

def test_the_pack_is_a_pure_function_of_the_profile(
    tmp_path: Path,
) -> None:
    first = build_pack(3, 2, 1.0)
    second = build_pack(3, 2, 1.0)
    assert first == second
    for name, doc in first.items():
        assert (json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
                == json.dumps(second[name], indent=2,
                              ensure_ascii=False) + "\n")
    # and a different profile is a different pack (the knob is real)
    assert build_pack(3, 2, 1.0) != build_pack(3, 3, 1.0)


# -- 2: lint + the axes are real -----------------------------------------------

def test_the_pack_lints_green_and_the_axes_declared_not_implied(
    tmp_path: Path,
) -> None:
    s, links = 3, 2
    out = _materialize(tmp_path, s, links)
    pack = load_pack(out)  # the SAME admission gate, full lint
    assert pack.name_version == "density_pack@0.1"
    entities = pack.entities
    assert len(entities["locations"]) == LOC_PER_UNIT * s
    assert len(entities["npcs"]) == 1 + NPC_PER_UNIT * s
    assert len(entities["groups"]) == GROUPS_PER_UNIT * s
    assert len(entities["items"]) == ITEMS_PER_UNIT * s
    assert len(pack.data["actions.json"]["actions"]) == \
        GENERIC_VERBS + BOUND_VERBS_PER_UNIT * s
    entries = pack.rules["urgencies"]["entries"]
    assert len(entries) == POSTS_PER_UNIT * s + links * s
    # the PROFILE.md echo carries the same axes (the transparent
    # identity — the record never guesses what the pack declares)
    echo = json.loads(
        (out / "PROFILE.md").read_text(encoding="utf-8")
        .split("```json")[1].split("```")[0],
    )
    assert echo["axes_echo"]["L"] == LOC_PER_UNIT * s
    assert echo["axes_echo"]["E_npcs"] == 1 + NPC_PER_UNIT * s


# -- 3: isolation (K=0) ---------------------------------------------------------

def test_no_cross_unit_reference_and_the_player_rides_unit_0(
    tmp_path: Path,
) -> None:
    s = 3
    out = _materialize(tmp_path, s, links=4)
    pack = load_pack(out)
    units = [f"s{i}" for i in range(s)]
    # the exits graph: every edge stays inside one unit
    for loc in pack.entities["locations"]:
        stem = str(loc["id"]).split("_")[1]
        assert stem in units, f"unnamespaced location {loc['id']}"
        for exit_id in loc["exits"]:
            assert str(exit_id).split("_")[1] == stem, (
                f"cross-unit exit {loc['id']} -> {exit_id} (K must "
                "stay 0 in the locality baseline; the coupling arm "
                "is a later held-out row)"
            )
    # every urgency post: the npc, the target and any holder stay in
    # one unit (the player excepted — unit 0's own road)
    for entry in pack.rules["urgencies"]["entries"]:
        stem = str(entry["npc"]).split("_")[1]
        target = entry["intent"].get("target")
        if isinstance(target, str) and target != "pc_01":
            assert str(target).split("_")[1] == stem
        for req in entry.get("requires", ()):
            holder = req.get("holder")
            if holder:
                assert str(holder).split("_")[1] == stem
    # the economy flows: one namespace each, no shared holder
    stems = {str(f["to"]).split("_")[1]
             for f in pack.rules["economy"]["flows"]}
    assert stems == set(units)
    # the player: exactly one, declared inside unit 0's star
    players = [n for n in pack.entities["npcs"] if n.get("is_player")]
    assert len(players) == 1
    assert players[0]["position"] == "loc_s0_road"


# -- 4: the knobs ---------------------------------------------------------------

def test_the_r_knob_adds_unique_talk_posts_and_refuses_past_the_ceiling(
    tmp_path: Path,
) -> None:
    s, links = 2, 4
    out = _materialize(tmp_path, s, links=links)
    pack = load_pack(out)
    talks = [e for e in pack.rules["urgencies"]["entries"]
             if e["intent"]["kind"] == "talk"]
    # the unit's own four + the knob's four, per unit
    assert len(talks) == (4 + links) * s
    sources = [e["npc"] for e in talks]
    assert len(set(sources)) == len(sources)  # one goal per npc/verb
    # the ceiling: more links than the non-talk roster → loud refusal
    with pytest.raises(SystemExit, match="non-talk roster"):
        materialize(tmp_path / "refused", 1, 9, 1.0)


def test_the_rho_knob_scales_the_sampled_family_never_the_crossings(
    tmp_path: Path,
) -> None:
    base = build_pack(1, 0, 1.0)
    doubled = build_pack(1, 0, 2.0)
    base_entries = base["rules.json"]["urgencies"]["entries"]
    doubled_entries = doubled["rules.json"]["urgencies"]["entries"]
    for before, after in zip(base_entries, doubled_entries, strict=True):
        if before["probability_per_beat"] < 100:
            assert after["probability_per_beat"] == \
                before["probability_per_beat"] * 2
        else:
            assert after["probability_per_beat"] == 100  # B6's law
    with pytest.raises(SystemExit, match="prob-scale"):
        materialize(tmp_path / "zero", 1, 0, 0.0)
    with pytest.raises(SystemExit, match="settlements"):
        materialize(tmp_path / "empty", 0, 0, 1.0)


# -- 5: the run law (a REAL pack on the real Simulator) -------------------------

def test_the_smoke_run_commits_events_and_t1_holds(
    tmp_path: Path,
) -> None:
    out = _materialize(tmp_path, 2, links=2)
    log_dir = tmp_path / "logs"
    cmd = [
        sys.executable, str(RUNNER), "--pack", str(out),
        "--years", "1", "--seeds", "7", "--directors", "off",
        "--anchor", "loc_s0_square", "--out", str(log_dir),
        "--tag", "densitytest", "--verify-replay",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert "T1 byte-identity: HELD" in proc.stdout
    log = log_dir / "lab_7_loc_s0_square_1y_baseline.jsonl"
    _, events = read_log(log, SCHEMA)
    assert len(events) > 50  # the living unit's material cycle + talk
    assert any(e.type == "year_turns" for e in events)
    # the LOD's cold census rides the year turn (D-112: counts for
    # populations) — the cold unit's ONLY event-surface footprint
    turns = [e for e in events if e.type == "year_turns"]
    assert all("cold_npcs" in e.outcome for e in turns)
    assert turns[0].outcome["cold_npcs"] == NPC_PER_UNIT  # unit 1


# -- 6: the template economy ----------------------------------------------------

def test_the_tale_surface_stays_the_templates_own(
    tmp_path: Path,
) -> None:
    template = json.loads(
        (REPO / "content" / "farstead_pack" / "templates.json")
        .read_text(encoding="utf-8"),
    )
    out = _materialize(tmp_path, 2, links=0)
    generated = json.loads(
        (out / "templates.json").read_text(encoding="utf-8"),
    )
    for key in ("events", "knows", "account_kinds", "tale_gate",
                "day_header", "scene_card", "fallback", "symbols"):
        assert generated[key] == template[key]
    # the flow glosses: rebuilt per unit (keyed by flow id), the
    # values verbatim — each unit's flows carry their own gloss
    assert set(generated["flow_glosses"]) == {
        f"the_s{i}_{stem}"
        for i in range(2)
        for stem in ("bank_regrows", "copse_regrows",
                     "outcrop_weathers", "spring_runs")
    }
    assert set(generated["flow_glosses"].values()) == \
        set(template["flow_glosses"].values())
