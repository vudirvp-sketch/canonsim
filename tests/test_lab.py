"""lab-1 — the Atomic World Lab Stage A laws (the owner's
CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK v1.5, its 04 §2 the order owner).

The Lab's own falsifiers, pinned at smoke scale (the pack's 03 §12
battery, the E0/F1/F5 subset that is live TODAY):

- E0 player-absent law: over a player-absent horizon the player
  authors NOTHING but the single whole-horizon wait (the anchor
  move only when the player does not already stand at the anchor);
- E0 horizon law: the requested years cross the macro clock exactly
  (year_turns == years, the scheduler's positive-multiple law);
- F1 same-seed replay: the T1 byte-identity double-run at the smoke
  horizon (the same-environment law, AGENTS §10 / replay-1's fence);
- the metric reproducibility law: the same seed yields the SAME
  derived record (the MINIMAL profile is a pure fold over the log —
  no wall-clock, no paths, in the identity fields);
- the E0 honest-baseline law: the mix is maintenance-dominated and
  carries ZERO ecology-closing families — the pack's 01 §11 finding
  («the world ticks; it does not reproduce its own ecology»), now a
  measured law of the current substrate. When Stage B/D lands the
  first endogenous material/demographic mechanism, THIS test flips
  deliberately — it is the gap's canary, not a regression guard.

The runner's own ablation discovery is exercised at one measured
clean block (on_action) and one measured refusal (weather, the
cadence-armed family) — the per-pack re-measurement law.

Horizons stay at 2y in-test (≈0.7 s/run); longer horizons are the
runner's job (100y+), never the suite's (the corpus-price law).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from core.log import read_log
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "province_pack")
PLAYER = PACK.player_id()
PLAYER_START = next(
    str(n["position"])
    for n in PACK.entities["npcs"]
    if n.get("is_player")
)
YEARS = 2

sys.path.insert(0, str(REPO / "scripts"))
from labrunner import (  # noqa: E402
    _anchor_steps,
    _player_start,
    extract_metrics,
    run_world,
)


def _lab_run(tmp_path: Path, seed: int = 42) -> tuple[Path, dict[str, object]]:
    """One player-absent Lab run at the smoke horizon (directors off —
    the E0 baseline form)."""
    log, _wall = run_world(
        PACK, SCHEMA, seed, YEARS, tmp_path,
        anchor=PLAYER_START, directors=False, arm="test",
    )
    metrics = extract_metrics(
        PACK, SCHEMA, log, years=YEARS, wall_s=0.0, directors=False,
    )
    return log, metrics


def test_the_anchor_is_the_players_declared_start() -> None:
    """The default anchor IS the pack's declared player position (the
    03 §3 fixed-observer law: the LOD reads a declared position, the
    harness invents none)."""
    assert _player_start(PACK) == PLAYER_START
    steps = _anchor_steps(PACK, YEARS, PLAYER_START)
    assert steps == [{"intent": "wait", "ticks": 518400 * YEARS}]


def test_player_absent_horizon_authors_one_wait(tmp_path: Path) -> None:
    """E0's player-absent law: the ONLY player-actor events over the
    whole horizon are the single wait completion (the anchor move
    never fires — the player already stands at the declared anchor;
    a rejected move would be harness noise, not a world fact)."""
    log, metrics = _lab_run(tmp_path)
    _, events = read_log(log, SCHEMA)
    player_events = [e for e in events if e.actor == PLAYER]
    assert [e.type for e in player_events] == ["wait"]
    assert metrics["counts"]["player_actor_events"] == 1


def test_horizon_crosses_the_macro_clock_exactly(tmp_path: Path) -> None:
    """The horizon law: year_turns == the requested years (the
    scheduler's positive-multiple law, one turn per crossing —
    maclock-1 held over the whole Lab horizon)."""
    _, metrics = _lab_run(tmp_path)
    assert metrics["horizon"]["year_turns"] == YEARS
    assert metrics["horizon"]["years_requested"] == YEARS


def test_same_seed_byte_identity_at_horizon(tmp_path: Path) -> None:
    """F1/T1 at the smoke horizon: the same seed re-run end-to-end
    produces the IDENTICAL committed byte stream (INV-2's law over a
    player-absent long horizon — the double-run the runner's own
    --verify-replay carries, pinned here at suite scale)."""
    first, _ = _lab_run(tmp_path, seed=42)
    second, _ = _lab_run(tmp_path, seed=42)
    assert first.read_bytes() == second.read_bytes()


def test_metrics_reproducible_per_seed(tmp_path: Path) -> None:
    """The metric-reproducibility law: the derived MINIMAL profile is
    a pure fold over the committed log — the same seed yields the
    same record except the measured cost block (wall seconds)."""
    _, one = _lab_run(tmp_path, seed=7)
    _, two = _lab_run(tmp_path, seed=7)
    one["cost"] = two["cost"] = {}
    assert one == two
    # and the identity block carries the declared environment:
    assert one["identity"]["seed"] == 7
    assert one["identity"]["pack"] == PACK.name_version
    assert one["identity"]["directors"] is False
    assert one["identity"]["horizon_years"] == YEARS


def test_the_e0_mix_is_maintenance_dominant_zero_ecology(
    tmp_path: Path,
) -> None:
    """The honest-baseline canary (the pack's 01 §11 finding as a
    LAW of the current substrate): the player-absent log is carried
    by maintenance + account flows, with ZERO ecology-closing
    families — no birth/death/migration/production/depletion cycle
    exists to fire. This test documents the measured gap; it flips
    only when Stage B/D's first endogenous mechanism lands."""
    _, metrics = _lab_run(tmp_path)
    mix = metrics["mix"]
    assert mix["maintenance"] > 0  # the world ticks (watch/decay/sky)
    assert mix.get("account_flow", 0) > 0  # the authored macro flows
    ecology_families = ("demographic", "production", "ecology")
    for family in ecology_families:
        assert mix.get(family, 0) == 0  # nothing closes a material cycle
    carried = mix["maintenance"] + mix.get("account_flow", 0)
    assert carried / metrics["counts"]["events_total"] > 0.9


def test_ablation_arm_clean_block_runs(tmp_path: Path) -> None:
    """The measured-clean ablation arm: minus:on_action runs the whole
    horizon clean (the 68a law live — the block absent, the primitive
    silent), and the log is SHORTER than the baseline's (the block's
    emission family actually carried events — assignment realized)."""
    variant_dir = tmp_path / "pack_minus_on_action"
    variant_dir.mkdir()
    import shutil

    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(
            REPO / "content" / "province_pack" / name, variant_dir / name,
        )
    rules = json.loads(
        (REPO / "content" / "province_pack" / "rules.json").read_text(
            encoding="utf-8",
        )
    )
    rules.pop("on_action", None)
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # the dead-vocabulary fixpoint's first measured pass (on_action's
    # own emission lines — the lint names them; here the family is
    # small enough to pin: the reaction-table types die with the block)
    from core.pack import PackError
    from core.pack import load_pack as _load

    try:
        variant = _load(variant_dir)
    except PackError:
        templates = json.loads(
            (variant_dir / "templates.json").read_text(encoding="utf-8")
        )
        import re

        dead_re = re.compile(r"templates: '([^']+)' is declared but unused")
        dead = sorted(set(dead_re.findall(str(sys.exc_info()[1]))))
        assert dead, "the refusal is not dead-vocabulary — re-measure"
        for line in dead:
            templates["events"].pop(line, None)
        (variant_dir / "templates.json").write_text(
            json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        variant = _load(variant_dir)

    baseline_log, _ = _lab_run(tmp_path)
    arm_log, _ = run_world(
        variant, SCHEMA, 42, YEARS, tmp_path,
        anchor=PLAYER_START, directors=False, arm="test_minus",
    )
    _, base_events = read_log(baseline_log, SCHEMA)
    _, arm_events = read_log(arm_log, SCHEMA)
    # The MEASURED E0 finding: on_action's reaction family is
    # player-action-armed — over a player-absent horizon it NEVER
    # fires, so the ablation is count-identical to the baseline (the
    # 03 §8 "assignment != realization" law in reverse: the assigned
    # ablation is realized, but its emission family has no consumer
    # in this regime). Pinned as the honest baseline fact; it flips
    # only when an autonomous consumer starts firing on_action.
    assert len(arm_events) == len(base_events)


def test_ablation_arm_cadence_armed_block_refused(tmp_path: Path) -> None:
    """The measured refusal: minus:weather cannot run a long horizon —
    the weather chain is armed by the MACRO CLOCK (time.macro), not
    the weather block; a day-1 harness never crosses the cadence, a
    Lab horizon does. The runner reports the arm's refusal loudly,
    never a stack trace (the honest-ablation law)."""
    variant_dir = tmp_path / "pack_minus_weather"
    variant_dir.mkdir()
    import shutil

    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(
            REPO / "content" / "province_pack" / name, variant_dir / name,
        )
    rules = json.loads(
        (REPO / "content" / "province_pack" / "rules.json").read_text(
            encoding="utf-8",
        )
    )
    rules.pop("weather", None)
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    from core.pack import PackError
    from core.pack import load_pack as _load

    try:
        variant = _load(variant_dir)
    except PackError:
        templates = json.loads(
            (variant_dir / "templates.json").read_text(encoding="utf-8")
        )
        templates["events"].pop("weather_turns", None)
        templates["events"].pop("smoke_washed_away", None)
        (variant_dir / "templates.json").write_text(
            json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        variant = _load(variant_dir)

    with pytest.raises(SystemExit, match="refused at RUNTIME"):
        run_world(
            variant, SCHEMA, 42, YEARS, tmp_path,
            anchor=PLAYER_START, directors=False, arm="test_minus_w",
        )


def test_the_runner_cli_smoke(tmp_path: Path) -> None:
    """The CLI form (the operator's door): one seed, the verify-replay
    flag, the JSON record emitted under the output dir; the process
    exits 0 (the T1 check HELD)."""
    out = tmp_path / "out"
    result = subprocess.run(
        [
            sys.executable, str(REPO / "scripts" / "labrunner.py"),
            "--years", "1", "--seeds", "42", "--verify-replay",
            "--out", str(out), "--tag", "cli_smoke",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(REPO),
        env={"PYTHONHASHSEED": "0", "PATH": "", "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0, result.stderr[-2000:]
    assert "T1 byte-identity: HELD" in result.stdout
    record = json.loads((out / "lab_cli_smoke.json").read_text(encoding="utf-8"))
    assert record["runs"][0]["metrics"]["horizon"]["year_turns"] == 1
