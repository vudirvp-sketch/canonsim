"""iter-259 (div-1, D-235) — the future-divergence minimal-pair probe's
claim packet (`scripts/divergence_probe.py`, TEST_PLAN §9's first-prism
row's instrument).

The laws this suite pins (the instrument+pin precedent):

(1) THE T8 INSTANCE — the landed minimal pair (day1_full, seed 125,
    directors on/off) re-derives through the probe: the first
    divergence is the director's release chain (the document check),
    the divergence PERSISTS to the horizon, never re-converges, and
    the state-level persistence shows (the suspicion props).

(2) THE NULL CONTROL — identical arms: no first divergence, the
    oracle's EQUAL verdict, exit 0 (a probe that cannot say "equal"
    is not an instrument).

(3) THE ARM FAMILY — the pacing arm (the DIR-2 instance: the release
    timing shifts, the fingerprints stay EQUAL — the timing-only
    change) and the systems-minus arm (the urgencies block carries
    the beat grid — its removal kills the beat machinery, the family
    delta names it); the loud input errors (an unknown block, an
    out-of-family script) exit 2, never a silent skip.

(4) THE RECORDS' OWN LAWS — the causal path walks the divergent
    event's OWN log through real cause ids (bounded), and the probe's
    verdict agrees with the oracle's own compare() on the same arm
    logs (the instrument never overrides its checker).

The probe imports the engine's public Simulator for the arms and the
oracle for the comparison — this suite exercises both through the
probe's own API + CLI.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import divergence_probe  # type: ignore[import-not-found]  # noqa: E402
import semantic_diff  # type: ignore[import-not-found]  # noqa: E402

from core.loop import load_playscript  # noqa: E402
from core.pack import load_pack  # noqa: E402

SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
PACK = load_pack(REPO / "content" / "tavern_pack")


# -- (1) the T8 instance ------------------------------------------------------


def test_t8_minimal_pair_pins_the_first_divergence(
    tmp_path: Path,
) -> None:
    """The landed minimal pair through the probe: the first divergence
    is the director's release (the document check chain — the guard's
    check FAILS on the gate scenario), the divergence persists to the
    horizon and never re-converges, the families delta names the
    release's events, and the state-level persistence shows in the
    suspicion props."""
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=False, out_dir=tmp_path,
    )
    assert not diff.equal
    assert records.first_index is not None
    assert records.first_type == "document_check_failed"
    assert records.first_side == "both"  # the streams shift at the release
    assert records.persists_to_horizon
    assert not records.re_converged
    assert "-1 document_check_failed" in records.family_delta
    assert "-1 crowd_wary" in records.family_delta
    assert any(
        line.startswith("npc_guard_01.pair.pc_01.suspicion")
        or line.startswith("npc_")
        for line in records.projection_delta
    )
    assert records.divergent_positions == records.positions_after + 1
    report = divergence_probe.render_report(
        records, diff, "directors off (the T8 minimal pair)", "day1_full"
    )
    assert "first divergence: event[" in report
    assert "persists to the horizon: yes" in report
    assert "re-converged: no" in report


# -- (2) the null control -----------------------------------------------------


def test_null_control_identical_arms_stay_equal(tmp_path: Path) -> None:
    """Identical packs + identical director flags: no first divergence,
    the oracle's EQUAL verdict, and the report names the null control
    (exit 0's condition)."""
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=True, out_dir=tmp_path,
    )
    assert diff.equal
    assert records.first_index is None
    report = divergence_probe.render_report(records, diff, "none", "day1_full")
    assert "first divergence: NONE" in report
    assert "VERDICT: SEMANTICALLY EQUAL" in report


# -- (3) the arm family -------------------------------------------------------


def test_pacing_arm_is_the_timing_only_shift(tmp_path: Path) -> None:
    """The DIR-2 pacing instance: the release TIMING shifts (the first
    divergence lands at the shifted event), the event counts stay equal,
    and the fingerprints stay EQUAL — the pacing change is timing-only,
    never a draw change (the probe names that distinction)."""
    from balance_harness import _nopacing_pack  # type: ignore[import-not-found]

    pert = _nopacing_pack(tmp_path)
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, pert,
        base_directors=True, pert_directors=True, out_dir=tmp_path,
    )
    assert not diff.equal
    assert records.first_index is not None
    assert records.base_events == records.pert_events
    assert records.base_fingerprint == records.pert_fingerprint
    assert any("ramble" in line for line in records.family_delta)


def test_systems_minus_urgencies_kills_the_beat_machinery(
    tmp_path: Path,
) -> None:
    """The urgencies block carries the beat grid: its removal drops the
    beat machinery wholesale — the family delta names the decay family,
    the projection delta shows the undecayed statuses (the empty-ablation
    rule's exercise half: the arm demonstrably exercises the target)."""
    from balance_harness import _systems_minus_pack  # type: ignore[import-not-found]

    pert = _systems_minus_pack(tmp_path, "urgencies", drop_pacing=False)
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, pert,
        base_directors=True, pert_directors=True, out_dir=tmp_path,
    )
    assert not diff.equal
    assert "-11 status_decayed" in records.family_delta
    assert records.projection_delta_count >= 4


def test_loud_input_errors_exit_two(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unknown systems-minus block and an out-of-family script exit 2
    with the reason — never a silent no-op arm (a dropped-but-unknown
    key would silently run the base twice)."""
    code = divergence_probe.main(
        ["--systems-minus", "fire", "--out-dir", str(tmp_path)]
    )
    captured = capsys.readouterr()
    assert code == 2
    assert "unknown systems-minus block 'fire'" in captured.out
    code = divergence_probe.main(
        [
            "--script", str(REPO / "tests" / "playscripts" / "province_smoke.json"),
            "--pacing-off", "--out-dir", str(tmp_path),
        ]
    )
    captured = capsys.readouterr()
    assert code == 2
    assert "out of family" in captured.out


# -- (4) the records' own laws ------------------------------------------------


def test_causal_path_walks_real_ids_in_one_log(tmp_path: Path) -> None:
    """The causal path is the divergent event's OWN-log ancestry: every
    link's id exists in that arm's parsed log, the chain starts at the
    divergent event, and the walk is bounded."""
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=False, out_dir=tmp_path,
    )
    assert records.first_id is not None
    assert records.causal_path
    # the divergent event itself + at most MAX_CAUSAL_LINKS ancestry links
    assert len(records.causal_path) <= divergence_probe.MAX_CAUSAL_LINKS + 1
    assert records.causal_path[0][0] == records.first_id
    _header, base_events = semantic_diff.parse_log(records.base_log)
    ids = {str(event.get("id")) for event in base_events}
    for event_id, _tick, _type in records.causal_path:
        assert event_id in ids


def test_the_probe_agrees_with_its_oracle(tmp_path: Path) -> None:
    """The instrument never overrides its checker: the probe's diff IS
    the oracle's own compare() over the same arm logs (fingerprints
    supplied) — re-derived here independently, verdict included."""
    records, diff = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=False, out_dir=tmp_path,
    )
    again = semantic_diff.compare(
        records.base_log, records.pert_log,
        fingerprint_left=records.base_fingerprint,
        fingerprint_right=records.pert_fingerprint,
    )
    assert again.equal == diff.equal
    assert again.event_count_left == records.base_events
    assert again.event_count_right == records.pert_events


def test_the_probe_is_deterministic(tmp_path: Path) -> None:
    """Same inputs, same records, same report (INV-2's periphery
    discipline; the arms re-run fresh and land byte-identical)."""
    first, diff_a = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=False, out_dir=tmp_path,
    )
    second, diff_b = divergence_probe.probe(
        SCRIPT, PACK, PACK,
        base_directors=True, pert_directors=False, out_dir=tmp_path,
    )
    assert first == second
    assert diff_a.equal == diff_b.equal
    report_a = divergence_probe.render_report(first, diff_a, "x", "day1_full")
    report_b = divergence_probe.render_report(second, diff_b, "x", "day1_full")
    assert report_a == report_b
