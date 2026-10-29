"""density-1/2 — the density-envelope generator's laws (iter-345/347,
the E02 successor row; TEST_PLAN §9.1's axes made checkable, the
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
7. THE HOUSEHOLDS IDENTITY (density-2) — households=3 (the default)
   IS the density-1 form byte-for-byte; the knob only grows, never
   rewrites the template's own surface.
8. THE HOUSEHOLDS AXES (density-2) — H−3 extension households of
   four hearth-voice adults each, resident on the ACTIVE unit's
   square, the Ashen-mirror pair web carried; the PROFILE.md echo
   declares the warm/cold split honestly (warm_adults_unit0 =
   12 + 4·(H−3), cold_npcs = 12·(S−1) — the cold volume the
   template's own).
9. THE EXTENSION RING (density-2) — every extension adult carries
   exactly ONE talk post on the internal 2-step ring (out-degree 1,
   in-degree 1, no self-target, NO template adult targeted — the
   knobs orthogonal by construction, every AP-11 pair unique).
10. THE HOUSEHOLDS RUN LAW (density-2) — a 1y smoke at H=5: T1
    HELD, the extension's talk events PRESENT (the warm population
    alive — the row's point), the census cold volume untouched, and
    the MATERIAL SUBSTREAM (every account_* event's type, actor,
    tick, outcome) IDENTICAL to the H=3 form's run: the cone's
    population density varies, never its material semantics.
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
                 scale: float = 1.0, name: str = "pack",
                 households: int = 3) -> Path:
    out = tmp / name
    materialize(out, settlements, links, scale, households)
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


# -- 7: the households identity (density-2) --------------------------------------

def test_households_three_is_the_density_one_form_byte_for_byte(
    tmp_path: Path,
) -> None:
    # the default (no knob) and the explicit H=3 are the SAME pack —
    # the additive-form law: the extension rides AFTER the template
    # units, so the template's own bytes never move
    base = build_pack(3, 2, 1.0)
    knob = build_pack(3, 2, 1.0, households=3)
    assert base == knob
    # and the knob is real: H=6 is a different pack
    assert build_pack(3, 2, 1.0, households=3) != \
        build_pack(3, 2, 1.0, households=6)
    # determinism at the grown profile (law 1's extension)
    assert build_pack(2, 0, 1.0, households=6) == \
        build_pack(2, 0, 1.0, households=6)


# -- 8: the households axes ------------------------------------------------------

def test_households_axes_declared_not_implied(
    tmp_path: Path,
) -> None:
    s, h = 2, 6  # 3 extension households: dun, elm, fenn
    out = _materialize(tmp_path, s, households=h)
    pack = load_pack(out)  # the SAME admission gate, full lint
    extra = h - 3
    npcs = pack.entities["npcs"]
    assert len(npcs) == 1 + NPC_PER_UNIT * s + 4 * extra
    assert len(pack.entities["groups"]) == GROUPS_PER_UNIT * s + extra
    # the extension adults: unit 0's square, the Ashen-mirror pair web
    ext = [n for n in npcs if str(n["id"]).startswith("npc_s0_")
           and str(n["id"]) not in
           {f"npc_s0_{t}_{r}" for t in ("ashen", "bourne", "crome")
            for r in ("elder", "mate", "son", "daughter")}]
    assert len(ext) == 4 * extra
    assert all(n["position"] == "loc_s0_square" for n in ext)
    by_id = {str(n["id"]): n for n in ext}
    for stem in ("dun", "elm", "fenn"):
        elder, mate = f"npc_s0_{stem}_elder", f"npc_s0_{stem}_mate"
        son, daughter = f"npc_s0_{stem}_son", f"npc_s0_{stem}_daughter"
        assert by_id[elder]["pair_relations"] == \
            [{"with": mate, "trust": 80}]
        assert by_id[mate]["pair_relations"] == \
            [{"with": elder, "trust": 80}]
        assert by_id[son]["pair_relations"] == \
            [{"with": elder, "trust": 70}]
        assert by_id[daughter]["pair_relations"] == \
            [{"with": mate, "trust": 75}]
    # the extension groups: one per household, the four members each
    ext_groups = [g for g in pack.entities["groups"]
                  if str(g["id"]).startswith("grp_s0_")
                  and str(g["id"]) not in
                  {"grp_s0_ashen", "grp_s0_bourne", "grp_s0_crome"}]
    assert len(ext_groups) == extra
    assert all(len(g["members"]) == 4 for g in ext_groups)
    # the PROFILE.md echo declares the warm/cold split honestly
    echo = json.loads(
        (out / "PROFILE.md").read_text(encoding="utf-8")
        .split("```json")[1].split("```")[0],
    )
    assert echo["households"] == h
    assert echo["axes_echo"]["E_npcs"] == 1 + NPC_PER_UNIT * s + 4 * extra
    assert echo["axes_echo"]["warm_adults_unit0"] == 12 + 4 * extra
    assert echo["axes_echo"]["cold_npcs"] == NPC_PER_UNIT * (s - 1)
    assert echo["axes_echo"]["R_talk_posts_unit0"] == 4 + 4 * extra


# -- 9: the extension ring (AP-11's ceiling by construction) ---------------------

def test_the_extension_ring_is_internal_bijective_and_clone_free(
    tmp_path: Path,
) -> None:
    s, h = 2, 5  # 2 extension households: dun, elm (N=8 adults)
    out = _materialize(tmp_path, s, households=h)
    pack = load_pack(out)
    ext_ids = {
        str(n["id"]) for n in pack.entities["npcs"]
        if str(n["id"]).startswith(("npc_s0_dun_", "npc_s0_elm_"))
    }
    assert len(ext_ids) == 8
    entries = pack.rules["urgencies"]["entries"]
    ext_posts = [e for e in entries if str(e["npc"]) in ext_ids]
    assert len(ext_posts) == 8  # exactly one post per extension adult
    # the ring: internal (no template adult targeted), bijective
    # (every extension adult spoken to exactly once), no self-talk
    targets = [str(e["intent"]["target"]) for e in ext_posts]
    assert all(t in ext_ids for t in targets)  # orthogonality
    assert len(set(targets)) == len(targets)   # in-degree exactly 1
    assert all(str(e["intent"]["target"]) != str(e["npc"])
               for e in ext_posts)             # no self-target
    assert all(e["intent"]["kind"] == "talk"
               and e["probability_per_beat"] == 1 for e in ext_posts)
    # AP-11 directly: every LIVE (intent, requires) pair unique across
    # NPCs — the whole pack, the lint's own law verified as the ring's
    # teeth (a verbatim household copy would clone and fail here)
    pairs: dict[tuple[str, str], str] = {}
    for entry in entries:
        if entry["probability_per_beat"] <= 0:
            continue
        pair = (json.dumps(entry["intent"], sort_keys=True),
                json.dumps(entry.get("requires", ()), sort_keys=True))
        assert pair not in pairs or pairs[pair] == entry["npc"], (
            f"AP-11 clone: {pairs.get(pair)!r} and {entry['npc']!r} "
            f"share the pair {entry['intent']['kind']!r}"
        )
        pairs[pair] = str(entry["npc"])
    # the ρ knob scales the extension posts (the sampled family)
    doubled = build_pack(s, 0, 2.0, households=h)
    base_entries = build_pack(s, 0, 1.0, households=h)
    d = [e for e in doubled["rules.json"]["urgencies"]["entries"]
         if str(e["npc"]) in ext_ids]
    b = [e for e in base_entries["rules.json"]["urgencies"]["entries"]
         if str(e["npc"]) in ext_ids]
    assert all(after["probability_per_beat"] == 2 for after in d)
    assert all(before["probability_per_beat"] == 1 for before in b)
    # the refusal arms are loud (the template's own three are the
    # floor; the stem list the honest ceiling)
    with pytest.raises(SystemExit, match="must be >= 3"):
        materialize(tmp_path / "two", 1, 0, 1.0, 2)
    with pytest.raises(SystemExit, match="honest ceiling"):
        materialize(tmp_path / "past", 1, 0, 1.0, 33)


# -- 10: the households run law (the REAL Simulator) ----------------------------

def test_the_households_run_is_alive_cold_invariant_and_material_pure(
    tmp_path: Path,
) -> None:
    # two packs, same (settlements, seed, protocol, horizon): the
    # H=3 form and the H=5 form — the DENSITY-SCALE arm's own A/B
    base_pack = _materialize(tmp_path, 2, name="h3", households=3)
    grown_pack = _materialize(tmp_path, 2, name="h5", households=5)
    logs = {}
    for name, pack_dir in (("h3", base_pack), ("h5", grown_pack)):
        log_dir = tmp_path / f"logs_{name}"
        cmd = [
            sys.executable, str(RUNNER), "--pack", str(pack_dir),
            "--years", "1", "--seeds", "7", "--directors", "off",
            "--anchor", "loc_s0_square", "--out", str(log_dir),
            "--tag", f"density{name}", "--verify-replay",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              check=True)
        assert "T1 byte-identity: HELD" in proc.stdout
        logs[name] = log_dir / "lab_7_loc_s0_square_1y_baseline.jsonl"
    schema = SCHEMA
    _, base_events = read_log(logs["h3"], schema)
    _, grown_events = read_log(logs["h5"], schema)

    def material_substream(events):
        return [
            (e.type, e.actor, e.t, json.dumps(e.outcome, sort_keys=True))
            for e in events if e.type.startswith("account_")
        ]

    # the warm population is ALIVE: the extension's talks are present
    ext_talks = [e for e in grown_events if e.type == "talk"
                 and str(e.actor).startswith(("npc_s0_dun_",
                                              "npc_s0_elm_"))]
    assert len(ext_talks) > 5  # ~10/year per extension adult
    # the cold volume untouched: the census law at the year turn
    turns = [e for e in grown_events if e.type == "year_turns"]
    assert turns and all(t.outcome["cold_npcs"] == NPC_PER_UNIT
                         for t in turns)
    # the witness surface honest: the extension adults react to the
    # served meal (the co-location race is the settlement's attendance)
    eased = [e for e in grown_events if e.type == "meal_eased"]
    assert eased and any(
        str(npc).startswith("npc_s0_dun_")
        for npc in eased[0].outcome["reacting"]
    )
    # THE CONTROL: the material substream IDENTICAL — the cone's
    # population density varies, never its material semantics
    assert material_substream(grown_events) == \
        material_substream(base_events)
