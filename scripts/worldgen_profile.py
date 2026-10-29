"""geo-1: the worldgen timing profile (`docs/TECH_NOTES.md` §12 owns the
numbers) — the perf-1 precedent mapped to the map side.

Per invocation, each scale of the ladder runs the FULL genesis door
(`core/worldgen.py::genesis` — generate_world + the claim gate + the
chronicle + the drafts) over the committed pack's own `worldgen` block
with the map extent scaled to the site target (extent = spacing·side,
so the lattice count lands exactly on side²; every other value the
pack's own — the probe config is TOOLING, never a second config
surface), TWICE: once clean (the headline wall-clock) and once under
cProfile (the per-pass hot-spot table for the largest scale). The two
runs' (model, drafts, parents) fingerprints are sha256-compared — a
free determinism probe at the scale target, same process (T1 remains
the owner of the cross-environment guarantee). The committed scale
(target 36 — the extent 48 map) reproduces the corpus digests
byte-for-byte: the ladder's anchor row.

Timing is wall-clock BY DESIGN: a measurement harness is operator
tooling, not canon (INV-2 bans wall-clock in the log; the
profile_harness precedent). Output:
`output/worldgen_perf_<seed>.txt` — gitignored runtime artifact; the
harness is committed, the distilled numbers live in TECH_NOTES §12.

Usage:
    PYTHONHASHSEED=0 python -m scripts.worldgen_profile
    PYTHONHASHSEED=0 python -m scripts.worldgen_profile --sites 10000
    PYTHONHASHSEED=0 python -m scripts.worldgen_profile --sites 36,2500 --seed 42
"""

from __future__ import annotations

import argparse
import cProfile
import hashlib
import math
import pstats
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

# Allow `python scripts/worldgen_profile.py` and `python -m scripts.worldgen_profile`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.pack import load_pack  # noqa: E402
from core.rng import RngBank  # noqa: E402
from core.worldgen import genesis  # noqa: E402

#: The committed pack's own map spacing — the ladder's scale unit (the
#: probe scales extent alone; spacing stays the pack's).
SPACING = 8

#: The default ladder: the committed scale (36 sites — extent 48, the
#: corpus anchor) then five synthetic scales to the 10k-site exit
#: evidence.
DEFAULT_LADDER = "36,100,400,900,2500,4900,10000"

#: The hot-spot filter: the worldgen module and the stream bank (the
#: passes and their draws — everything else is scaffolding).
PROBE_FILES = ("/core/worldgen.py", "/core/rng.py")
HOTSPOT_ROWS = 12


def probe_rules(rules: Any, sites_target: int) -> dict[str, Any]:
    """The committed block with the extent scaled to the target: the
    lattice count lands exactly on isqrt(target)^2 sites (row 36 = the
    committed extent 48 map verbatim)."""
    side = math.isqrt(sites_target)
    extent = SPACING * side
    block = dict(rules["worldgen"])
    block["map"] = {**block["map"], "extent": extent}
    return {**rules, "worldgen": block}


def fingerprint(seed: int, rules: Any) -> tuple[str, int]:
    """The genesis door's answer, digested: sha256 over the model, the
    drafts, and the parent map (repr — deterministic under
    PYTHONHASHSEED=0; derived, never truth)."""
    model, drafts, parents = genesis(RngBank(seed), rules, (), seed)
    blob = repr((model, drafts, parents))
    digest = hashlib.sha256(blob.encode()).hexdigest()[:16]
    return digest, len(model.sites)


def scale_row(seed: int, rules: Any) -> dict[str, Any]:
    """One ladder run: the clean wall-clock, the profiled twin, and the
    fingerprint compare (the in-run determinism probe)."""
    t0 = time.perf_counter()
    digest, sites = fingerprint(seed, rules)
    clean_s = time.perf_counter() - t0
    profiler = cProfile.Profile()
    profiler.enable()
    profiled_digest, _ = fingerprint(seed, rules)
    profiler.disable()
    return {
        "sites": sites,
        "clean_s": clean_s,
        "identical": digest == profiled_digest,
        "digest": digest,
        "profiler": profiler,
    }


def hotspots(profiler: cProfile.Profile) -> list[dict[str, Any]]:
    """Top worldgen-side functions by cumulative time (the triage
    table — the per-pass cost split, instrumented)."""
    stats = pstats.Stats(profiler).stats
    rows: list[tuple[float, int, str, str]] = []
    for (filename, _lineno, funcname), (
        _cc, nc, _tt, ct, _callers,
    ) in stats.items():
        if not any(part in filename for part in PROBE_FILES):
            continue
        rows.append((ct, nc, funcname, Path(filename).name))
    rows.sort(key=lambda r: (-r[0], r[2]))
    return [
        {"cum_s": round(ct, 4), "calls": nc, "func": func, "file": fname}
        for ct, nc, func, fname in rows[:HOTSPOT_ROWS]
    ]


def report(seed: int, rows: list[dict[str, Any]]) -> str:
    """The distilled run record (stdout + the output/ artifact)."""
    lines: list[str] = []
    lines.append(f"worldgen profile (geo-1) · seed {seed} · ladder:")
    lines.append(
        f"{'sites':>6} {'extent':>7} {'clean_s':>9} {'sites/s':>10} "
        "fingerprint"
    )
    for row in rows:
        extent = SPACING * math.isqrt(row["sites"])
        rate = row["sites"] / row["clean_s"] if row["clean_s"] else 0.0
        lines.append(
            f"{row['sites']:>6} {extent:>7} {row['clean_s']:>9.2f} "
            f"{rate:>10,.0f} {row['digest']} "
            f"{'(identical twin)' if row['identical'] else 'DIVERGED'}"
        )
    lines.append("-" * 64)
    biggest = rows[-1]
    lines.append(
        f"hot spots (cumulative, top {HOTSPOT_ROWS}, the "
        f"{biggest['sites']}-site scale):"
    )
    for i, spot in enumerate(hotspots(biggest["profiler"]), start=1):
        lines.append(
            f"  {i:>2}. {spot['cum_s']:>8.3f}s  {spot['calls']:>9,d}x  "
            f"{spot['func']}  [{spot['file']}]"
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="worldgen_profile",
        description="geo-1: the worldgen timing profile (TECH_NOTES §12)",
    )
    parser.add_argument(
        "--sites", default=DEFAULT_LADDER,
        help=f"comma-separated site targets (default: {DEFAULT_LADDER})",
    )
    parser.add_argument(
        "--seed", type=int, default=125,
        help="seed (default: 125 — the corpus probe family)",
    )
    args = parser.parse_args(argv)
    targets = [int(value) for value in args.sites.split(",")]
    pack = load_pack(REPO / "content" / "tavern_pack")
    rows = [
        scale_row(args.seed, probe_rules(pack.rules, target))
        for target in targets
    ]
    if not all(row["identical"] for row in rows):
        print("the clean and profiled twins diverged — INV-2 probe failed",
              file=sys.stderr)
        return 1
    text = report(args.seed, rows)
    out_dir = REPO / "output"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"worldgen_perf_{args.seed}.txt").write_text(text,
                                                            encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
