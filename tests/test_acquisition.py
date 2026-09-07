"""iter-73 acceptance — depth-1, the acquisition gate (phase 5's first
row, D-105/TASKS: the D-096-named real gap — continuous acquisition
CONDITIONS feeding birth fidelity — pack data in rules.json, mechanics
in the perception path, never a second knowledge store). Mechanics only
(iter-73): the committed pack declares NO block — the arming is depth-1b
(the 68a→68b pattern: the pack's own declaration is the arming).

The laws pinned here:

- **The gate law**: each armed condition that fails at the event's site
  steps the born record down the fidelity chain — `when_flag` + `is`
  (the site entity's prop equals the value: a layer's smoke flag) or
  `phase_in` (the clock phase at record birth, lifted by a truthy
  `unless_flag` — the lit room at night); `steps` >= 1 per condition,
  accumulating. The walk floor-sticks exactly as `decay_fidelity` does
  (D-007's ladder — the transfer law stays the ladder's single owner;
  the gate is its documented birth-side twin).
- **The emission-site law**: conditions read the EVENT SITE (the origin
  for actor/target/same/adjacent audiences, the destination for
  destination_location and present_at expansions), never the observer's
  own state — the observer's state rides the perception checks' status
  modifiers, the existing single owner.
- **The channel law**: only the ambient channels saw/heard have an
  acquisition surface — told rides the transfer decay, inferred is
  internal; the gate answers the base fidelity for any other channel
  (the lint refuses arming them; the mechanics stay defensive).
- **The unarmed law (v0.1 bytes)**: a pack without the block answers
  the base fidelity everywhere — zero gate cost, zero draws (the gate
  consumes no RNG stream EVER, so the fingerprint law holds by
  construction), byte-identical logs.
- **The corpus-price law (both arms)**: a crafted pack armed with a
  condition that never fires on the DAY1_TALK geometry (no fire) vs the
  committed pack — ten seeds, byte-identical.
- **The liveness law**: a geometry whose site IS degraded (the day1
  arson prefix, then a return into the smoke) — the arrival-snapshot
  records born partial in the armed arm, exact in the committed twin,
  and the bytes differ: the arming is measurable, never silent.
- **The lint laws**: the closed condition vocabulary (exactly one kind
  per condition; when_flag requires `is`; unless_flag belongs to
  phase_in only); ambient channels only; `phase_in` names real
  `time.phases` ids; `steps` is an int >= 1 (a dead condition is
  refused, never silently legal); unknown keys are loud.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core.fold import initial_projection
from core.intent import acquisition_fidelity, resolve_knowledge
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

DAY1_TALK: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01"},
    {"intent": "talk", "target": "npc_guard_01"},
]
# The day1_theft_and_arson prefix (seed 8: the lamp ignites), then leave
# the fire and RETURN into the smoke — the final arrival's snapshot is
# born at a degraded site.
SMOKE_RETURN: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "take", "target": "oil_lamp_01"},
    {"intent": "move", "target": "loc_backyard"},
    {"intent": "drop_break", "target": "oil_lamp_01", "near": "back_wall"},
    {"intent": "wait", "ticks": 12},  # the smoke flag lands at +10
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "move", "target": "loc_backyard"},  # arrival in the smoke
]
# The real flag convention: a layer's follow-up flags land RAW on the
# location entity (transitions.py writes prop=spec["flag"]) — the smoke
# follow-up is "smoke", the spots are layer-prefixed ("fire.back_wall").
SMOKE_ARM: dict[str, Any] = {
    "saw": [{"when_flag": "smoke", "is": True, "steps": 1}],
}


def _duck_pack(acquisition: Any) -> Any:
    """The unit-test pack stub: rules only, the shape the gate reads
    (duck-typed — the gate never imports pack.py at runtime)."""
    return SimpleNamespace(
        rules={
            "time": {
                "ticks_per_day": 1440,
                "phases": [
                    {"id": "morning", "from": 0, "to": 360},
                    {"id": "afternoon", "from": 360, "to": 720},
                    {"id": "evening", "from": 720, "to": 1080},
                    {"id": "night", "from": 1080, "to": 1440},
                ],
            },
            "knowledge": {"fidelity_chain": ["exact", "partial", "vague"]},
            "position_visibility": {"acquisition": acquisition},
        }
    )


def crafted_pack(tmp_path: Path, name: str, acquisition: Any) -> Pack:
    """A committed-pack copy with `position_visibility.acquisition` set
    (or REMOVED when None — the v0.1 twin: the committed pack is unarmed,
    so the unarmed arm of every A/B pin is this crafted block-popped
    copy or the committed pack itself)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if acquisition is None:
        rules["position_visibility"].pop("acquisition", None)
    else:
        rules["position_visibility"]["acquisition"] = acquisition
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


def run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> Path:
    """One playscript run; answers the log path (bytes are the pin)."""
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    return log


def born_knowledges(log: Path) -> list[Any]:
    """Every knowledge record in the log, in birth order."""
    _, events = read_log(log, SCHEMA)
    return [record for event in events for record in event.knowledge]


# -- the gate (unit) -----------------------------------------------------------


def test_the_absent_block_answers_the_base_fidelity() -> None:
    """The unarmed law: no block, an empty object, or an empty condition
    list — all answer the declared fidelity (v0.1 bytes; the pack's own
    declaration is the arming)."""
    for acquisition in (None, {}, {"saw": []}):
        pack = _duck_pack(acquisition)
        assert (
            acquisition_fidelity(
                pack, {"loc_a": {}}, "saw", "loc_a", 5, "exact"
            )
            == "exact"
        )


def test_when_flag_fires_only_on_the_matching_site_state() -> None:
    """The flag condition: steps accrue when the site's prop EQUALS the
    declared value — a mismatch, an absent prop, or another value never
    fires (deterministic read of committed state, never a roll)."""
    pack = _duck_pack({"saw": [{"when_flag": "smoke", "is": True, "steps": 1}]})
    smoking = acquisition_fidelity(
        pack, {"loc_a": {"smoke": True}}, "saw", "loc_a", 5, "exact"
    )
    burning = acquisition_fidelity(
        pack, {"loc_a": {"smoke": "burning"}}, "saw", "loc_a", 5, "exact"
    )
    clear = acquisition_fidelity(
        pack, {"loc_a": {}}, "saw", "loc_a", 5, "exact"
    )
    assert (smoking, burning, clear) == ("partial", "exact", "exact")


def test_phase_in_fires_by_clock_phase_and_the_unless_flag_lifts() -> None:
    """The light condition: the clock phase at record birth (the pure
    rules-level twin `phase_of_tick`), lifted by a truthy site flag —
    the lit room at night keeps its fidelity; an unflagged site steps."""
    pack = _duck_pack(
        {"saw": [{"phase_in": ["night"], "unless_flag": "lit", "steps": 1}]}
    )
    night_lit = acquisition_fidelity(
        pack, {"loc_a": {"lit": True}}, "saw", "loc_a", 1200, "exact"
    )
    night_dark = acquisition_fidelity(
        pack, {"loc_a": {}}, "saw", "loc_a", 1200, "exact"
    )
    morning_dark = acquisition_fidelity(
        pack, {"loc_a": {}}, "saw", "loc_a", 5, "exact"
    )
    assert (night_lit, night_dark, morning_dark) == ("exact", "partial", "exact")


def test_steps_accumulate_and_the_floor_sticks() -> None:
    """The ladder law: failing conditions accumulate their steps, and the
    walk floor-sticks at the chain's end exactly as the transfer decay
    does (D-007's ladder — the documented twin)."""
    pack = _duck_pack(
        {
            "saw": [
                {"when_flag": "smoke", "is": True, "steps": 1},
                {"phase_in": ["night"], "steps": 1},
            ]
        }
    )
    both = acquisition_fidelity(
        pack, {"loc_a": {"smoke": True}}, "saw", "loc_a", 1200, "exact"
    )
    runaway = acquisition_fidelity(
        pack, {"loc_a": {"smoke": True}}, "saw", "loc_a", 1200, "partial"
    )
    assert both == "vague"
    assert runaway == "vague"  # partial + 2 steps floors at vague


def test_told_and_inferred_have_no_acquisition_surface() -> None:
    """The channel law: a non-ambient channel in the block answers the
    base fidelity — the gate is defensive (the lint owns the refusal of
    arming told/inferred)."""
    pack = _duck_pack(
        {"told": [{"when_flag": "smoke", "is": True, "steps": 1}]}
    )
    assert (
        acquisition_fidelity(
            pack, {"loc_a": {"smoke": True}}, "told", "loc_a", 5, "exact"
        )
        == "exact"
    )


# -- the wiring (resolve_knowledge rides the gate on both branches) --------------


def test_audience_branch_wiring(tmp_path: Path) -> None:
    """A same_location template born at a smoking origin: saw exact →
    partial in the armed arm, exact in the committed pack."""
    armed = crafted_pack(tmp_path, "armed_audience", SMOKE_ARM)
    state = initial_projection(PACK.entities)
    state["loc_tavern"]["smoke"] = True
    template = {
        "who": "same_location", "except": ["actor"],
        "channel": "saw", "fidelity": "exact", "knows": "figure_at_{location}",
    }
    ctx = {"actor": "pc_01", "target": None, "location": "loc_tavern"}
    stepped = resolve_knowledge([template], armed, state, ctx, tick=5)
    base = resolve_knowledge([template], PACK, state, ctx, tick=5)
    assert all(r.fidelity == "partial" for r in stepped)
    assert all(r.fidelity == "exact" for r in base)
    assert [r.knows for r in stepped] == [r.knows for r in base]


def test_the_expansion_branch_rides_the_gate(tmp_path: Path) -> None:
    """The emission-site law, expansion side: the arrival-snapshot
    template (present_at) born at a smoking destination steps every
    per-present record identically."""
    armed = crafted_pack(tmp_path, "armed_expansion", SMOKE_ARM)
    state = initial_projection(PACK.entities)
    state["loc_backyard"]["smoke"] = True
    state["pc_01"]["position"] = "loc_tavern"
    template = {
        "who": "actor", "present_at": "destination_location",
        "channel": "saw", "fidelity": "exact", "knows": "{present}_present",
    }
    ctx = {
        "actor": "pc_01", "target": "loc_backyard", "location": "loc_tavern",
    }
    stepped = resolve_knowledge([template], armed, state, ctx, tick=5)
    base = resolve_knowledge([template], PACK, state, ctx, tick=5)
    assert stepped and all(r.fidelity == "partial" for r in stepped)
    assert base and all(r.fidelity == "exact" for r in base)
    assert [r.who for r in stepped] == [r.who for r in base]


def test_a_clean_site_never_steps_even_when_armed(tmp_path: Path) -> None:
    """The zero-price mechanics pin: the armed pack at a clean site
    answers exactly the committed pack's records (same knows, same
    fidelity, same order)."""
    armed = crafted_pack(tmp_path, "armed_clean", SMOKE_ARM)
    state = initial_projection(PACK.entities)
    template = {
        "who": "same_location", "channel": "saw", "fidelity": "exact",
        "knows": "figure_at_{location}",
    }
    ctx = {"actor": "pc_01", "target": None, "location": "loc_tavern"}
    stepped = resolve_knowledge([template], armed, state, ctx, tick=5)
    base = resolve_knowledge([template], PACK, state, ctx, tick=5)
    assert stepped == base


# -- the corpus-price law (both arms, bytes) -------------------------------------


def test_the_armed_never_firing_condition_costs_zero_bytes(tmp_path: Path) -> None:
    """The corpus-price law: a crafted pack armed with the smoke
    condition vs the committed pack, over the DAY1_TALK geometry (no
    fire, so the condition never fires) — ten seeds, byte-identical
    logs: the gate consumes no draws, so even the fingerprint cannot
    see an armed-but-silent pack."""
    armed = crafted_pack(tmp_path, "armed_price", SMOKE_ARM)
    for seed in range(10):
        armed_log = run(tmp_path, armed, seed, DAY1_TALK, f"armed_{seed}")
        base_log = run(tmp_path, PACK, seed, DAY1_TALK, f"base_{seed}")
        assert armed_log.read_bytes() == base_log.read_bytes()


def test_the_liveness_law_a_degraded_site_steps_the_born_records(
    tmp_path: Path,
) -> None:
    """The liveness law: the day1 arson prefix, then a return into the
    smoke — the armed arm's arrival-snapshot records are born PARTIAL
    where the committed twin births them EXACT, and the bytes differ
    (the arming is measurable, never silent)."""
    armed = crafted_pack(tmp_path, "armed_live", SMOKE_ARM)
    armed_log = run(tmp_path, armed, 8, SMOKE_RETURN, "live_armed")
    base_log = run(tmp_path, PACK, 8, SMOKE_RETURN, "live_base")
    armed_records = [
        r
        for r in born_knowledges(armed_log)
        if r.knows.endswith("_present") and r.channel == "saw"
    ]
    base_records = [
        r
        for r in born_knowledges(base_log)
        if r.knows.endswith("_present") and r.channel == "saw"
    ]
    assert base_records and all(r.fidelity == "exact" for r in base_records)
    assert any(r.fidelity == "partial" for r in armed_records)
    assert armed_log.read_bytes() != base_log.read_bytes()


# -- the lint (the closed vocabulary is loud) ------------------------------------


def _armed(tmp_path: Path, block: Any) -> Pack:
    return crafted_pack(tmp_path, f"lint_{abs(id(block)) % 10**8}", block)


def test_the_lint_accepts_the_canonical_arming(tmp_path: Path) -> None:
    """The full vocabulary loads: a flag condition and a phase condition
    with an exemption, both channels armed."""
    pack = _armed(
        tmp_path,
        {
            "saw": [
                {"when_flag": "fire.smoke", "is": True, "steps": 1},
                {"phase_in": ["night"], "unless_flag": "lit", "steps": 1},
            ],
            "heard": [{"phase_in": ["night"], "steps": 1}],
        },
    )
    assert pack.rules["position_visibility"]["acquisition"]["saw"][0]["steps"] == 1


def test_the_lint_refuses_a_non_ambient_channel(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="ambient channel"):
        _armed(tmp_path, {"told": [{"when_flag": "x", "is": True, "steps": 1}]})


def test_the_lint_refuses_a_dead_condition(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="steps must be an int >= 1"):
        _armed(
            tmp_path,
            {"saw": [{"when_flag": "smoke", "is": True, "steps": 0}]},
        )


def test_the_lint_refuses_two_condition_kinds_in_one_entry(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="exactly one condition kind"):
        _armed(
            tmp_path,
            {
                "saw": [
                    {
                        "when_flag": "x", "is": True,
                        "phase_in": ["night"], "steps": 1,
                    }
                ]
            },
        )


def test_the_lint_refuses_when_flag_without_is(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="requires 'is'"):
        _armed(tmp_path, {"saw": [{"when_flag": "x", "steps": 1}]})


def test_the_lint_refuses_an_unknown_phase(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="unknown phase"):
        _armed(tmp_path, {"saw": [{"phase_in": ["brunch"], "steps": 1}]})


def test_the_lint_refuses_unless_flag_on_a_flag_condition(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="belongs to phase_in"):
        _armed(
            tmp_path,
            {
                "saw": [
                    {
                        "when_flag": "x", "is": True,
                        "unless_flag": "y", "steps": 1,
                    }
                ]
            },
        )


def test_the_lint_refuses_is_on_a_phase_condition(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="'is' belongs to when_flag"):
        _armed(
            tmp_path, {"saw": [{"phase_in": ["night"], "is": True, "steps": 1}]}
        )


def test_the_lint_refuses_unknown_keys(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="unknown keys"):
        _armed(
            tmp_path,
            {"saw": [{"when_flag": "x", "is": True, "steps": 1, "chance": 5}]},
        )


def test_the_lint_refuses_an_empty_condition_list(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="non-empty list"):
        _armed(tmp_path, {"saw": []})
