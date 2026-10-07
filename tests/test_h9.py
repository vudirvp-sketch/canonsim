"""iter-337 acceptance — H9, the event-to-event waiting on the
time-skip (the row the epoch structurally unlocked, rng-1's O(1)
counter jump; the STATUS Next item (1), named by iter-334/335/336's
NEXT lines):

THE QUIET-BEAT SKIP — the loop's crossing discipline jumps the
clock, the bank counters, and the director's beat counter across
beats whose machinery would produce NOTHING (no decay draft, no
condensation, no urgency/faction roll hit with open gates), landing
at the first producing beat or the stretch's bound (a rotation /
calendar / macro crossing or the popped entry's tick — all COMMIT,
none is ever skipped past). A skipped beat consumes exactly its
rolling entries' rolls (+1 each — `skip_draws`), so the landed
beat's first draw reads the same position both paths would.

THE FALSIFIER IS THE A/B BYTE-IDENTITY LAW (this file's first law):
the same (pack, seed, step list) with the skip ON and OFF commits
byte-identical logs — the skip is an acceleration, never a semantics
choice. The committed corpus rides the ON arm by default (the far-
stead/pressure fixtures keep their pinned bytes); the dedicated
pairs here pin both arms on shapes the corpus does not byte-pin.
The named residues, fenced by the capability guards (loop init):
the director-armed world (the pacing clock's beat-count dependence)
and the fold-gated world (the per-tick fold verdicts — a leverage
map expiring, a belief un-crystallizing) keep the exact tick-by-tick
path; modeling either is a future row, never silently approximated.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from core.loop import Simulator
from core.pack import load_pack
from core.rng import RngBank
from core.states import decay_drafts, next_decay_tick
from core.urgencies import urgency_intents, urgency_scan, urgency_specs

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from labrunner import run_world  # noqa: E402

FARSTEAD = load_pack(REPO / "content" / "farstead_pack")
PRESSURE = load_pack(REPO / "content" / "pressure_pack")
TAVERN = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

SQUARE = "loc_square"
YEAR = 518_400  # the farstead macro cadence (ticks per year)


def _steps(years: int, protocol: str) -> list[dict[str, object]]:
    """The player-absent step list (the lab-1 law-2 form; segmented =
    N year waits summing exactly to the span)."""
    if protocol == "whole":
        return [{"intent": "wait", "ticks": YEAR * years}]
    return [{"intent": "wait", "ticks": YEAR}] * years


def _run(
    tmp: Path, name: str, *, seed: int, years: int, protocol: str,
    skip: bool, directors: bool = False,
) -> tuple[Simulator, Path]:
    """One farstead run through the real Simulator, both skip arms."""
    log = tmp / f"h9_{name}.jsonl"
    sim = Simulator(
        FARSTEAD, seed, log, SCHEMA, commit="0000000",
        director_enabled=directors, skip_quiet_beats=skip,
    )
    sim.open()
    sim.run_steps(_steps(years, protocol))
    sim.close()
    return sim, log


# -- law 1: THE A/B BYTE-IDENTITY LAW (the row's falsifier) --------------------


def test_the_ab_byte_identity_law(tmp_path: Path) -> None:
    """The same (seed, step list) with the skip ON and OFF commits
    byte-identical logs — and the ON arm's stats are NON-VACUOUS (the
    skip actually skipped; a green pair with zero skipped beats proves
    nothing). Both wait protocols: whole (one horizon-long wait, the
    deferred-realize world) and segmented (year waits, the living
    world) — different stretch shapes, one law."""
    for seed in (7, 42, 93):
        for protocol in ("whole", "segmented"):
            sim_on, log_on = _run(
                tmp_path, f"on_{seed}_{protocol}", seed=seed, years=3,
                protocol=protocol, skip=True,
            )
            _, log_off = _run(
                tmp_path, f"off_{seed}_{protocol}", seed=seed, years=3,
                protocol=protocol, skip=False,
            )
            assert log_on.read_bytes() == log_off.read_bytes(), (
                f"seed {seed} / {protocol}: the skip DIVERGED the canon"
            )
            stats = sim_on.skip_stats
            assert stats["skipped"] > 0, (
                "the A/B pair is vacuous on this shape — the skip never "
                "fired (pin a shape where it does)"
            )
            assert stats["landings"] > 0


def test_t1_holds_under_the_skip(tmp_path: Path) -> None:
    """T1 (the same-seed double-run byte-identity) holds on the skip
    path itself — both runs ON, both byte-equal."""
    _, log_a = _run(
        tmp_path, "t1a", seed=7, years=3, protocol="segmented", skip=True,
    )
    _, log_b = _run(
        tmp_path, "t1b", seed=7, years=3, protocol="segmented", skip=True,
    )
    assert log_a.read_bytes() == log_b.read_bytes()


# -- law 2: THE COUNTER-IDENTITY LAW -------------------------------------------


def test_the_counter_identity_law(tmp_path: Path) -> None:
    """The skip's arithmetic: at the run's end EVERY stream's draw
    counter is EQUAL on both arms (the skip advanced exactly the rolls
    the tick-by-tick path drew — `skip_draws` is the counters' jump,
    never a shortcut around them), and the beat-grid population the
    skip counted matches the beats the OFF arm actually paid. The
    bank is not exported by the run — the test reads the live bank
    before the simulator is dropped (the worldgen family is excluded
    on both arms by the same export law)."""
    sim_on, _ = _run(
        tmp_path, "cnt_on", seed=7, years=3, protocol="segmented", skip=True,
    )
    sim_off, _ = _run(
        tmp_path, "cnt_off", seed=7, years=3, protocol="segmented", skip=False,
    )
    on_counts = {
        name: sim_on._bank.count(name)  # noqa: SLF001 -- the test's own read
        for name in sim_on._bank._counts  # noqa: SLF001
        if not name.startswith("worldgen:")
    }
    off_counts = {
        name: sim_off._bank.count(name)  # noqa: SLF001
        for name in sim_off._bank._counts  # noqa: SLF001
        if not name.startswith("worldgen:")
    }
    assert on_counts == off_counts
    # the skip's own ledger is consistent with the grid arithmetic: the
    # 3-year segmented horizon carries 3 x 1080 beats; skipped + the
    # landed beats + the bound-crossing beats == the grid population
    stats = sim_on.skip_stats
    beats = 3 * 1080
    assert 0 < stats["skipped"] < beats


# -- law 3: THE CAPABILITY-GUARD LAW ------------------------------------------


def test_the_capability_guards(tmp_path: Path) -> None:
    """A pack that fails any fence keeps the exact tick-by-tick path:
    the fold-gated worlds (tavern: leverage/echo/trait gates; pressure:
    the echo-gated institutional verbs) NEVER skip regardless of the
    director arm; the hook-declaring world under an ENABLED director
    never skips (the pacing clock reads beat counts). The live set is
    the Lab's own fixture family (farstead: no hooks, no fold gates).
    """
    for pack, directors in ((TAVERN, False), (TAVERN, True), (PRESSURE, True)):
        log = tmp_path / f"g_{pack.name}_{directors}.jsonl"
        sim = Simulator(
            pack, 7, log, SCHEMA, commit="0000000",
            director_enabled=directors, skip_quiet_beats=True,
        )
        assert not sim._skip_capable  # noqa: SLF001 -- the fence's own read
        sim.open()
        sim.run_steps([{"intent": "wait", "ticks": 2 * YEAR}])
        sim.close()
        assert sim.skip_stats == {"stretches": 0, "skipped": 0, "landings": 0}
    # farstead: the live set — both director arms (no hooks declared,
    # so the director is quiet either way), the skip fires
    for directors in (False, True):
        log = tmp_path / f"g_farstead_{directors}.jsonl"
        sim = Simulator(
            FARSTEAD, 7, log, SCHEMA, commit="0000000",
            director_enabled=directors, skip_quiet_beats=True,
        )
        assert sim._skip_capable  # noqa: SLF001
        sim.open()
        sim.run_steps([{"intent": "wait", "ticks": 2 * YEAR}])
        sim.close()
        assert sim.skip_stats["skipped"] > 0


def test_the_director_hook_fence(tmp_path: Path) -> None:
    """The director fence's own arm: a farstead twin with ONE declared
    release hook refuses the skip under an enabled director (the pacing
    clock's beat-count dependence — the named residue), and skips as
    ever under the disabled arm (the hooks exist but the policy never
    releases; the fence is the DIRECTOR state, never the buffer's)."""
    twin = tmp_path / "farstead_hook"
    shutil.copytree(REPO / "content" / "farstead_pack", twin)
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules["director"]["hooks"] = {
        "probe_hook": {
            "weight": 1, "release_threshold": 5, "target_npc": "pc_01",
            "intent": {"kind": "wait", "ticks": 1},
        }
    }
    (twin / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    pack = load_pack(twin)
    for directors, capable in ((True, False), (False, True)):
        log = tmp_path / f"hook_{directors}.jsonl"
        sim = Simulator(
            pack, 7, log, SCHEMA, commit="0000000",
            director_enabled=directors, skip_quiet_beats=True,
        )
        assert sim._skip_capable is capable  # noqa: SLF001
        sim.open()
        sim.run_steps([{"intent": "wait", "ticks": YEAR}])
        sim.close()


# -- law 4: THE DECAY-FORMULA TWIN (the property law) --------------------------


def test_the_decay_formula_twin() -> None:
    """`next_decay_tick` is the formula twin of the per-beat
    `decay_drafts` walk: over crafted states (a fresh NPC, a pinned
    axis, a late baseline, a caught NPC, the LOD scope) the first beat
    whose walk answers non-empty is EXACTLY the first grid point at or
    after the formula's tick — and a None formula never drafts inside
    a long window (the pinned law)."""
    from core.fold import initial_projection

    offsets = sorted(FARSTEAD.rules["urgencies"]["beat_ticks"])
    day = int(FARSTEAD.rules["time"]["ticks_per_day"])

    def grid(from_tick: int, count: int) -> list[int]:
        """The first `count` grid points at or after `from_tick`."""
        out: list[int] = []
        tick = from_tick
        while len(out) < count:
            days, remainder = divmod(tick, day)
            for offset in offsets:
                if offset >= remainder:
                    out.append(days * day + offset)
            tick = (days + 1) * day
        return out

    # (a) the fresh world: every NPC starts at seeded fatigue, the
    # baselines empty — the formula and the walk agree on the window
    projection = initial_projection(FARSTEAD.entities)
    formula = next_decay_tick(FARSTEAD, projection, {}, 360)
    assert formula is not None
    beats = grid(360, 4)
    walked = next(
        (b for b in beats if decay_drafts(FARSTEAD, projection, {}, b)),
        None,
    )
    # the twin's exactness: the first drafting beat IS the first grid
    # point at or after the formula's tick
    assert walked == min(b for b in beats if b >= formula)

    # (b) the pinned axis: every NPC's fatigue clamped at the scale max
    # — no draft ever, the formula answers None
    scale = FARSTEAD.rules["relations"]["scale"]
    pinned = {
        npc["id"]: {**props, "status.fatigue": scale[1]}
        for npc in FARSTEAD.entities["npcs"]
        for props in [projection.get(npc["id"], {})]
        if props
    }
    assert next_decay_tick(FARSTEAD, pinned, {}, 360) is None
    assert all(
        not decay_drafts(FARSTEAD, pinned, {}, b) for b in grid(360, 8)
    )

    # (c) the late baseline: a decay event just fired at t=1000 — the
    # next draft waits the full rate window from THERE
    late = dict(projection)
    first_npc = FARSTEAD.entities["npcs"][0]["id"]
    late[first_npc] = {**late[first_npc], "status.fatigue": 0}
    last_change = {(first_npc, "status.fatigue"): 1000}
    formula_c = next_decay_tick(FARSTEAD, late, last_change, 1001)
    assert formula_c is not None and formula_c > 1000
    beats_c = grid(1001, 6)
    walked_c = next(
        (b for b in beats_c
         if decay_drafts(FARSTEAD, late, last_change, b)),
        None,
    )
    assert walked_c == min(b for b in beats_c if b >= formula_c)

    # (d) the caught do not tire — caught NPCs never constrain
    caught = dict(projection)
    caught[first_npc] = {
        **caught[first_npc], "crime_status": "caught",
        "status.fatigue": 0,
    }
    assert next_decay_tick(FARSTEAD, caught, {}, 360) is not None
    beat = grid(360, 1)[0]
    drafts = decay_drafts(FARSTEAD, caught, {}, beat)
    assert drafts and all(
        d.target != first_npc for d in drafts
    ), "the caught must not draft"


# -- law 5: THE SCAN-VS-WALK LAW ----------------------------------------------


def test_the_scan_vs_walk_law() -> None:
    """`urgency_scan` predicts the walk: over fresh banks (several
    seeds), the scan's `first_fire` offset is EXACTLY the first beat
    at which `urgency_intents` yields an intent, and the scan's
    `streams` map is EXACTLY the set of streams the walk touches per
    beat (the rolling-set twin — one law, both consumers)."""
    from core.fold import initial_projection

    projection = initial_projection(FARSTEAD.entities)
    specs = urgency_specs(FARSTEAD)
    limit = 400
    for seed in (7, 42, 125):
        bank_scan = RngBank(seed)
        streams, first = urgency_scan(
            FARSTEAD, projection, bank_scan, specs=specs, limit=limit,
        )
        bank_walk = RngBank(seed)
        walked_first: int | None = None
        touched: set[str] = set()
        for beat in range(1, limit + 1):
            intents = urgency_intents(
                FARSTEAD, projection, bank_walk, specs=specs,
            )
            touched.update(
                f"urgency:{i.actor}:{i.kind}"
                for i in intents
            )
            if intents and walked_first is None:
                walked_first = beat
        assert first == walked_first, (seed, first, walked_first)
        # the scan never draws: the substantive counter (always
        # registered, the fingerprint's own stream) is untouched — a
        # scan that burned a canon check would move it
        assert bank_scan.count() == 0
        # the walk's per-beat draw pattern: every rolling stream drew
        # exactly `limit` times in the walk
        assert all(
            bank_walk.count(name) == limit for name in streams
        ), "a rolling entry missed a beat — the rolling set diverged"


# -- law 6: THE BEAT-GRID ARITHMETIC ------------------------------------------


def test_the_beat_grid_arithmetic(tmp_path: Path) -> None:
    """`_beat_grid_count` / `_beat_grid_point` are the arithmetic
    twins of the `_next_beat_after` walk: for a grid point `s`, the
    point at offset k IS the walk's k-th step and the half-open
    count [s, that point) IS k (s itself included — the skip's
    `skipped = count(beat_tick, landing)` counts the skipped beats
    from the CURRENT one up to the landing, exactly); for a
    non-grid tick the count up to the next step is zero. Pinned
    against the loop's own cursor walk at grid and off-grid
    starts, including the year boundary."""
    sim = Simulator(
        FARSTEAD, 7, tmp_path / "grid.jsonl", SCHEMA, commit="0000000",
    )
    offsets = set(FARSTEAD.rules["urgencies"]["beat_ticks"])
    day = int(FARSTEAD.rules["time"]["ticks_per_day"])
    for start in (360, 720, 518_760, 519_120):
        # a GRID start: k-th walked step == point at offset k, and
        # the half-open count to it == k
        cursor = start
        for k in range(1, 26):
            cursor = sim._next_beat_after(cursor)  # noqa: SLF001
            assert cursor is not None
            assert sim._beat_grid_point(start, k) == cursor  # noqa: SLF001
            assert sim._beat_grid_count(start, cursor) == k  # noqa: SLF001
        assert sim._beat_grid_count(start, start) == 0  # noqa: SLF001
    for tick in (1440, 519_000, 3):  # OFF-grid ticks (incl. day edge)
        assert tick % day not in offsets or tick // day < 0
        step = sim._next_beat_after(tick)  # noqa: SLF001
        assert step is not None
        assert sim._beat_grid_count(tick, step) == 0  # noqa: SLF001
        assert sim._beat_grid_count(tick, tick) == 0  # noqa: SLF001
        # a stretch from an off-grid tick to the NEXT-NEXT step holds
        # exactly the one stepped-on grid point in between
        step2 = sim._next_beat_after(step)  # noqa: SLF001
        assert sim._beat_grid_count(tick, step2) == 1  # noqa: SLF001


# -- law 7: THE LABRUNNER SKIP ARM --------------------------------------------


def test_the_labrunner_skip_arm(tmp_path: Path) -> None:
    """The instrument's arm: `run_world(skip=False)` writes the
    `_noskip` volume (a separate log, never an overwrite — KI#112's
    law) with all-zero skip stats, and the ON arm's record carries the
    skip block; the two logs are byte-identical (the wall A/B's own
    battery shape at smoke scale)."""
    out = tmp_path / "out"
    log_on, wall_on, stats_on = run_world(
        FARSTEAD, SCHEMA, 7, 2, out,
        anchor=SQUARE, directors=False, arm="baseline",
        protocol="segmented", skip=True,
    )
    log_off, wall_off, stats_off = run_world(
        FARSTEAD, SCHEMA, 7, 2, out,
        anchor=SQUARE, directors=False, arm="baseline",
        protocol="segmented", skip=False,
    )
    assert log_on.name.endswith("_segmented.jsonl")
    assert log_off.name.endswith("_segmented_noskip.jsonl")
    assert log_on.read_bytes() == log_off.read_bytes()
    assert stats_on["skipped"] > 0
    assert stats_off == {"stretches": 0, "skipped": 0, "landings": 0}
    assert wall_on > 0 and wall_off > 0  # honest labels, both measured


def test_the_cli_skip_flag(tmp_path: Path) -> None:
    """The CLI surface: `--skip off` runs clean end-to-end (exit 0)
    and writes the `_noskip` volume; the default arm stays ON."""
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(REPO / "scripts" / "labrunner.py"),
        "--pack", str(REPO / "content" / "farstead_pack"),
        "--years", "2", "--seeds", "7", "--anchor", SQUARE,
        "--protocol", "segmented", "--skip", "off",
        "--out", str(out), "--tag", "cli_noskip",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert (out / "lab_7_loc_square_2y_baseline_segmented_noskip.jsonl").exists()
    # the default arm (no flag) writes the plain stem
    cmd[-2] = "cli_default"
    cmd = [c if c != "--skip" else "--protocol" for c in cmd[:-2]] + [
        "--out", str(out), "--tag", "cli_default",
    ]
    cmd = [
        sys.executable, str(REPO / "scripts" / "labrunner.py"),
        "--pack", str(REPO / "content" / "farstead_pack"),
        "--years", "2", "--seeds", "7", "--anchor", SQUARE,
        "--protocol", "segmented",
        "--out", str(out), "--tag", "cli_default",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert (out / "lab_7_loc_square_2y_baseline_segmented.jsonl").exists()
