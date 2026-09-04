"""iter-37 acceptance — the DIR-2 balance-harness pacing A/B (the
phase-3 exit criterion's measurement, `docs/TEST_PLAN.md` §6).

The clock-off arm is a PACK VARIANT: the committed pack minus
`director.pacing`, materialized once per invocation under the
gitignored output dir and linted on load (a pack without the block
runs the v0.1 minimal pair — the pack's own declaration is the gate,
INV-3). The instrument itself (`core.metrics.eventless_beat_stretches`)
is tested in `tests/test_metrics.py`; this file pins the harness's
arm machinery, the stretch block in the table, and the D-065 record
(seed 125: all beats in PEAK — the two arms run byte-identically).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import balance_harness  # type: ignore[import-not-found]  # noqa: E402

from core.director import pacing_from_rules  # noqa: E402
from core.pack import load_pack  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(PACK_DIR)


# -- the clock-off arm's pack variant ----------------------------------------


def test_nopacing_pack_loads_and_drops_only_pacing(tmp_path: Path) -> None:
    """The variant is the committed pack minus `director.pacing` and
    nothing else: every other rules key, and the whole of the other
    three files, are deep-equal; the lint passes (the block is
    optional); `pacing_from_rules` reads None — the v0.1 minimal pair."""
    variant = balance_harness._nopacing_pack(tmp_path)
    assert pacing_from_rules(variant.rules) is None
    assert pacing_from_rules(PACK.rules) is not None  # the committed arm
    expected = {
        key: value
        for key, value in dict(PACK.rules).items()
    }
    expected["director"] = {
        key: value
        for key, value in dict(PACK.rules["director"]).items()
        if key != "pacing"
    }
    assert dict(variant.rules) == expected
    for name in ("entities.json", "actions.json", "templates.json"):
        assert dict(variant.data[name]) == dict(PACK.data[name])


def test_nopacing_pack_is_idempotent(tmp_path: Path) -> None:
    """A second invocation rewrites the variant dir cleanly — the A/B
    never inherits a stale variant."""
    first = balance_harness._nopacing_pack(tmp_path)
    second = balance_harness._nopacing_pack(tmp_path)
    assert dict(first.rules) == dict(second.rules)


# -- the arm guard ------------------------------------------------------------


def test_pacing_off_requires_directors_on() -> None:
    """A disabled director never consults the clock — the combination
    would measure nothing; the harness fails fast at the parser."""
    with pytest.raises(SystemExit):
        balance_harness.main(
            [
                "--runs", "1", "--directors", "off", "--pacing", "off",
                "--out-dir", str(PACK_DIR.parent.parent / "output"),
            ]
        )


# -- the end-to-end arms ------------------------------------------------------


def _run_arm(tmp_path: Path, pacing: str) -> Path:
    argv = [
        "--runs", "2", "--seed-base", "300", "--directors", "on",
        "--pacing", pacing, "--out-dir", str(tmp_path),
    ]
    assert balance_harness.main(argv) == 0
    suffix = "" if pacing == "on" else "_nopacing"
    return tmp_path / f"balance_2_seed300_on{suffix}.txt"


def test_harness_emits_the_stretch_block(tmp_path: Path) -> None:
    """The table carries the DIR-2 block: the arm label, the max-stretch
    row, the quiet-run share, and the length histogram."""
    table_path = _run_arm(tmp_path, "on")
    table = table_path.read_text(encoding="utf-8")
    assert "pacing: clock on" in table
    assert "eventless_max_stretch" in table
    assert "eventless beat-stretches (gate=medium)" in table
    assert "stretch histogram (length:count)" in table
    assert "runs quiet at least once" in table
    # determinism: the same seeds → the same table bytes
    again = _run_arm(tmp_path, "on")
    assert again.read_text(encoding="utf-8") == table


def test_harness_nopacing_arm_labels_and_file(tmp_path: Path) -> None:
    """The clock-off arm names itself in the table and lands in the
    `_nopacing` output file — the two arms never overwrite each other."""
    on_path = _run_arm(tmp_path, "on")
    off_path = _run_arm(tmp_path, "off")
    off_table = off_path.read_text(encoding="utf-8")
    assert "pacing: clock off (v0.1 minimal pair)" in off_table
    assert "eventless_max_stretch" in off_table
    assert on_path.exists() and off_path != on_path


def test_seed_125_arms_agree_the_d065_record(tmp_path: Path) -> None:
    """D-065 pinned, superseded in part at iter-52 (D-081), re-pinned at
    iter-53 (D-082, content-3): the day1_full seed-125 ON run keeps all
    three beats in PEAK — the clock's PEAK/REST bands still gate no
    quiet release — and the day's closing beat rides the CLIMAX PATH
    (the barkeep's sweep: trigger-less, climax-flagged). The nopacing
    arm (the pack minus `director.pacing` — no climax_floor, a flagged
    hook dies with no trigger AND no clock) now closes on the AMBIENT
    beat instead: without the pacing clock there is no PEAK suppression
    of the quiet path, and the ambient channel's own floor (0 < 2) is
    the only gate left — the drunkard's ramble rides the channel gate
    at the last beat. Both arms share their 52-line prefix; the ON arm
    appends the sweep (t=1456), the OFF arm appends the ramble
    (t=1458) — the clock's presence swaps WHICH director beat closes
    the day, and the structure rows (chains, M5, destroyed locations,
    the stretch block, the suspicion peaks) agree."""
    argv = [
        "--runs", "1", "--seed-base", "125", "--directors", "on",
        "--out-dir", str(tmp_path),
    ]
    assert balance_harness.main(argv + ["--pacing", "on"]) == 0
    assert balance_harness.main(argv + ["--pacing", "off"]) == 0
    on_table = (tmp_path / "balance_1_seed125_on.txt").read_text(encoding="utf-8")
    off_table = (
        tmp_path / "balance_1_seed125_on_nopacing.txt"
    ).read_text(encoding="utf-8")
    # the structure the D-065 record was about: the clock's own bands
    # changed nothing — chains, M5, the destroyed world, the stretches
    for row_start in (
        "M5", "emergent_chains", "destroyed_locations",
        "eventless_max_stretch",
    ):
        on_row = next(
            ln for ln in on_table.splitlines() if ln.startswith(row_start)
        )
        off_row = next(
            ln for ln in off_table.splitlines() if ln.startswith(row_start)
        )
        assert on_row == off_row, row_start
    # and the A/B's per-run logs: the arms share their whole prefix
    # (zero id shifts); each appends exactly its own closing beat
    on_log = (tmp_path / "balance_125_on.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    off_log = (
        tmp_path / "balance_125_on_nopacing.jsonl"
    ).read_text(encoding="utf-8").splitlines()
    assert on_log[:-1] == off_log[:-1]
    sweep = on_log[-1]
    assert '"type": "look_around"' in sweep
    assert '"cause_intent": "director_0001"' in sweep
    assert '"t": 1456' in sweep
    ramble = off_log[-1]
    assert '"type": "ramble"' in ramble
    assert '"actor": "npc_drunk_01"' in ramble
    assert '"t": 1458' in ramble
