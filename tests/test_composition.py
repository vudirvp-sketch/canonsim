"""ki114-1-impl acceptance — THE COMPOSITION LAW (KI#114, iter-340; the
owner's 2026-10-08 decision «Принимаем B — закон композиции на чистой
границе drain», the iter-339 packet's landing): a player step enters
the world ONLY at a clean drain boundary — the queue empty, the causal
cascade fully complete — so for the SAME step list, every partitioning
composes:

    run_steps([A,B]) == run_steps([A]); run_steps([B])

and `resume` carries NO separate timing semantics: continuous ==
split == checkpoint/resume, semantically and byte-for-byte, at every
admissible clean boundary. This file is the law's PERMANENT falsifier
(the iter-339 session artifact `scripts/ki114_law.py`, ported): 143
checks — the full cut lattice of a 3-step list (split AND
checkpoint-resume at every cut) x wait / move / zero-duration
(`look_around`) / follow-up-autonomous-drain step kinds x 5 packs
(farstead armed, province, pressure, tavern, grim) x 2 seeds x the
double-run determinism arm, plus the Lab family (`_anchor_steps`
segmented 3y, farstead + province, directors off — the labrunner's
own session form). Under the pre-KI#114 semantics the same battery
could not compose (the mid-drain feed: the iter-339 record measured
44/143 red — the falsifier's teeth); under the landed law it must be
143/143 green forever.

The whole-vs-segmented Lab CONTRACT is a DIFFERENT law and stands
untouched: `partition([A,B,C]) => composition` says the SAME player
sequence composes at every cut; it does NOT say
`run_steps([wait(2y)]) == run_steps([wait(1y), wait(1y)])` — those
are two DIFFERENT player-input sequences, and their divergence (the
deferred-realize law, `scripts/labrunner.py`) is the Lab's own
measured instrument, never erased by KI#114.

The grim battery stays below the year horizon BY DESIGN: the pack's
economy declares two `every:1` flows on one account (`till_settling`
+12 then `license_fee` -4 on `loc_tavern.account.coin`) and
`flow_drafts` computes both drafts against one projection snapshot —
the second flow's `from` is stale the moment the first commits, and
the `_commit` gate refuses LOUD (KI#115, pre-existing: reproduced
with the composition law stripped; no committed corpus script ever
reached a grim year turn, so the latent defect slept until a
year-scale wait). The falsifier falsifies the composition law, not
the pack's economy graph.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from core.cursor import cursor_path, load_cursor, save_cursor
from core.loop import Simulator
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from labrunner import _anchor_steps  # noqa: E402

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

#: The battery table: (pack, name, steps, seeds) rows. b0 is the
#: KI#114 repro family (move + wait + wait — the wait's drain carries
#: the world's autonomous life, the F1 feed-point shift's own shape);
#: b1 adds the zero-duration kind (`look_around`, ticks=1) at the
#: first boundary. Targets are each pack's own smoke-script anchors
#: (valid from the player's start — a rejected move is harness noise,
#: never a world fact). Grim's waits stay day-scale (KI#115's guard).
FARSTEAD = load_pack(REPO / "content" / "farstead_pack")
PROVINCE = load_pack(REPO / "content" / "province_pack")
PRESSURE = load_pack(REPO / "content" / "pressure_pack")
TAVERN = load_pack(REPO / "content" / "tavern_pack")
GRIM = load_pack(REPO / "content" / "grim_pack")

_YEAR = 518400  # the macro cadence (ticks per year), the farstead family
BATTERIES: tuple[
    tuple[Pack, str, str, tuple[dict[str, Any], ...], tuple[int, ...]], ...
] = (
    (FARSTEAD, "farstead", "b0", (
        {"intent": "move", "target": "loc_square"},
        {"intent": "wait", "ticks": _YEAR},
        {"intent": "wait", "ticks": _YEAR},
    ), (7, 11)),
    (FARSTEAD, "farstead", "b1", (
        {"intent": "look_around"},
        {"intent": "move", "target": "loc_square"},
        {"intent": "wait", "ticks": _YEAR},
    ), (7, 11)),
    (PROVINCE, "province", "b0", (
        {"intent": "move", "target": "loc_weirstair"},
        {"intent": "wait", "ticks": 30},
        {"intent": "wait", "ticks": 600},
    ), (2, 42)),
    (PROVINCE, "province", "b1", (
        {"intent": "look_around"},
        {"intent": "move", "target": "loc_weirstair"},
        {"intent": "wait", "ticks": 600},
    ), (2, 42)),
    (PRESSURE, "pressure", "b0", (
        {"intent": "move", "target": "loc_boilerhouse"},
        {"intent": "stoke_hard", "target": "loc_boilerhouse"},
        {"intent": "wait", "ticks": 600},
    ), (39, 2)),
    (PRESSURE, "pressure", "b1", (
        {"intent": "look_around"},
        {"intent": "move", "target": "loc_boilerhouse"},
        {"intent": "wait", "ticks": 600},
    ), (39, 2)),
    (TAVERN, "tavern", "b0", (
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 760},
        {"intent": "wait", "ticks": 760},
    ), (42, 125)),
    (TAVERN, "tavern", "b1", (
        {"intent": "look_around"},
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 760},
    ), (42, 125)),
    (GRIM, "grim", "b0", (
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 30},
        {"intent": "wait", "ticks": 30},
    ), (42, 25)),
    (GRIM, "grim", "b1", (
        {"intent": "look_around"},
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 30},
    ), (42, 25)),
)

#: The non-trivial partitionings of a 3-step list (the full cut
#: lattice minus the whole form): cut tuples over the step indices.
CUTS: tuple[tuple[int, ...], ...] = ((1,), (2,), (1, 2))

#: The check count is the law's own shape: 10 batteries x 2 seeds x
#: (1 double-run + 3 splits + 3 resumes) + 3 Lab checks == 143.
CHECK_COUNT = 143


def _whole(
    pack: Pack, seed: int, steps: list[dict[str, Any]], log: Path,
    *, directors: bool = True,
) -> bytes:
    """The uninterrupted batch: one Simulator, one run_steps call."""
    sim = Simulator(
        pack, seed, log, SCHEMA, commit="0000000", director_enabled=directors,
    )
    sim.open()
    sim.run_steps([dict(step) for step in steps])
    sim.close()
    return log.read_bytes()


def _split(
    pack: Pack, seed: int, steps: list[dict[str, Any]], cuts: tuple[int, ...],
    log: Path, *, directors: bool = True,
) -> bytes:
    """The split form (the session pattern): ONE Simulator, one
    run_steps call per partition cell — the world between calls moves
    only through the queue the cells seed."""
    sim = Simulator(
        pack, seed, log, SCHEMA, commit="0000000", director_enabled=directors,
    )
    sim.open()
    bounds = [0, *cuts, len(steps)]
    # consecutive-pair walk (bounds is one longer than its tail — the
    # partition cells); strict=False is the idiom's own shape
    for lo, hi in zip(bounds, bounds[1:], strict=False):
        sim.run_steps([dict(step) for step in steps[lo:hi]])
    sim.close()
    return log.read_bytes()


def _resume(
    pack: Pack, seed: int, steps: list[dict[str, Any]], cuts: tuple[int, ...],
    log: Path, *, directors: bool = True,
) -> bytes:
    """The checkpoint/resume form: a cursor round-trip AT EVERY cut of
    the partitioning (the test_resume canonical shape — the export
    flag equals the construction flag; interruption is not an input,
    only steps are)."""
    sim = Simulator(
        pack, seed, log, SCHEMA, commit="0000000", director_enabled=directors,
    )
    sim.open()
    bounds = [0, *cuts, len(steps)]
    for index, (lo, hi) in enumerate(
        zip(bounds, bounds[1:], strict=False)  # consecutive-pair cells
    ):
        sim.run_steps([dict(step) for step in steps[lo:hi]])
        if index < len(bounds) - 2:
            cursor = sim.export_cursor(director_enabled=directors)
            sim.close()
            save_cursor(cursor_path(log), cursor)
            sim = Simulator.resume(
                pack, log, SCHEMA, load_cursor(cursor_path(log)),
            )
    sim.close()
    return log.read_bytes()


def _safe(label: str) -> str:
    for old, new in ("(", "_"), (")", ""), (",", "-"), (" ", "_"):
        label = label.replace(old, new)
    return label


# -- THE LAW: 143 checks, zero failures, forever -------------------------------


def test_the_composition_law(tmp_path: Path) -> None:
    """KI#114's permanent falsifier. Every check runs the full real
    Simulator (no mocks, no stripped arms) and byte-compares a
    partitioned form against the uninterrupted reference of the SAME
    step list. A single red check names its label in the failure
    message — the label IS the reproduction (pack, battery, seed,
    form, cuts)."""
    failures: list[str] = []
    checks = 0

    def check(label: str, got: bytes, want: bytes) -> None:
        nonlocal checks
        checks += 1
        if got != want:
            failures.append(
                f"{label}: {len(got)} bytes vs the whole run's {len(want)}"
            )

    for pack, pack_name, battery, steps, seeds in BATTERIES:
        step_list = [dict(step) for step in steps]
        for seed in seeds:
            tag = f"{pack_name}-{battery} seed {seed}"
            ref = _whole(pack, seed, step_list, tmp_path / _safe(f"{tag} whole"))
            # 1. the double-run determinism arm: the whole form twice,
            #    byte-identical (INV-2 at the composition law's own scale).
            check(
                f"{tag} double-run",
                _whole(pack, seed, step_list, tmp_path / _safe(f"{tag} again")),
                ref,
            )
            # 2. the split form at every non-trivial partitioning.
            for cuts in CUTS:
                check(
                    f"{tag} split{cuts}",
                    _split(
                        pack, seed, step_list, cuts,
                        tmp_path / _safe(f"{tag} split{cuts}"),
                    ),
                    ref,
                )
            # 3. the checkpoint/resume form at every non-trivial
            #    partitioning — a cursor round-trip at EVERY cut.
            for cuts in CUTS:
                check(
                    f"{tag} resume{cuts}",
                    _resume(
                        pack, seed, step_list, cuts,
                        tmp_path / _safe(f"{tag} resume{cuts}"),
                    ),
                    ref,
                )

    # the Lab family (the labrunner's own session form): the segmented
    # 3y anchor list, directors off. The whole-vs-segmented CONTRACT is
    # a different law (the module docstring's second paragraph); these
    # checks hold the composition WITHIN the segmented sequence.
    for pack, pack_name, anchor, seed, resume_too in (
        (FARSTEAD, "farstead", "loc_square", 7, True),
        (PROVINCE, "province", "loc_weirstair", 2, False),
    ):
        step_list = [dict(step) for step in _anchor_steps(
            pack, 3, anchor, protocol="segmented",
        )]
        tag = f"lab-{pack_name} seed {seed}"
        ref = _whole(
            pack, seed, step_list, tmp_path / _safe(f"{tag} whole"),
            directors=False,
        )
        every_cut = tuple(range(1, len(step_list)))
        check(
            f"{tag} segmented-split",
            _split(
                pack, seed, step_list, every_cut,
                tmp_path / _safe(f"{tag} split"), directors=False,
            ),
            ref,
        )
        if resume_too:
            check(
                f"{tag} segmented-resume",
                _resume(
                    pack, seed, step_list, every_cut,
                    tmp_path / _safe(f"{tag} resume"), directors=False,
                ),
                ref,
            )

    assert checks == CHECK_COUNT, (
        f"the battery's shape drifted: {checks} checks, the law pins "
        f"{CHECK_COUNT} — a check was added or lost"
    )
    assert not failures, "composition law violations: " + "; ".join(failures)


# -- the historical repro stays closed ------------------------------------------


def test_the_ki114_repro_stays_closed(tmp_path: Path) -> None:
    """The exact KI#114 finding, pinned forever: the farstead
    2-segment split of [move, wait 1y, wait 1y] (seed 7 — the
    occ-1 discovery's own world) is byte-identical to the
    uninterrupted run, split AND checkpoint/resume. Under the
    pre-KI#114 semantics this shape diverged at ev_0210 (+16 ticks —
    the resumed segment's clock pinned the post-drain tick past the
    wait's completion); a regression back to any mid-drain feed point
    is caught HERE, at the historical repro."""
    pack, _name, _battery, steps, _seeds = BATTERIES[0]
    step_list = [dict(step) for step in steps]
    ref = _whole(pack, 7, step_list, tmp_path / "repro_whole.jsonl")
    assert _split(
        pack, 7, step_list, (2,), tmp_path / "repro_split.jsonl",
    ) == ref
    assert _resume(
        pack, 7, step_list, (2,), tmp_path / "repro_resume.jsonl",
    ) == ref


# -- the boundary door: every cell boundary admits the cursor --------------------


def test_every_cell_boundary_admits_the_cursor(tmp_path: Path) -> None:
    """The composition law's structural witness: between two steps of
    ONE run_steps call the queue reaches EMPTY — so every inter-step
    boundary of a batch run is an admissible export_cursor point (the
    cursor is a drain-boundary artifact and refuses mid-drain states
    LOUD). The resumed twin continues from there byte-identically:
    the batch's own internal boundaries ARE clean boundaries."""
    pack, _name, _battery, steps, _seeds = BATTERIES[0]
    step_list = [dict(step) for step in steps]
    log = tmp_path / "boundary.jsonl"
    sim = Simulator(pack, 7, log, SCHEMA, commit="0000000")
    sim.open()
    cursor = sim.export_cursor(director_enabled=True)
    # farstead is unarmed for worldgen: open() wrote the header alone
    # (test_resume's split 0 — the empty boundary admits the cursor too)
    assert cursor["event_count"] == 0
    sim.run_steps([dict(step) for step in step_list[:1]])
    cursor = sim.export_cursor(director_enabled=True)
    assert cursor["event_count"] > 0
    sim.run_steps([dict(step) for step in step_list[1:2]])
    cursor = sim.export_cursor(director_enabled=True)
    assert cursor["event_count"] > 0
    sim.run_steps([dict(step) for step in step_list[2:]])
    sim.close()
    assert log.read_bytes() == _whole(
        pack, 7, step_list, tmp_path / "boundary_whole.jsonl",
    )
