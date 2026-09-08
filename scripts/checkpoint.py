"""The fold-checkpoint builder (depth-4, phase 5; `core/checkpoint.py`
owns the mechanism, `docs/blueprint/phases.md` §5 the design).

An offline operator tool over one COMMITTED log (the chronicler family's
derived-artifact law: everything written here is derived, rebuildable,
never truth, never committed — the output dir is gitignored runtime
space). Unlike the mode-F chronicler (which speaks only the log-file
contract, no `core/` imports), this builder imports the engine's own
fold — the checkpoint must snapshot EXACTLY the projection the runtime
would hold, so the single source of the initial projection and the
fold is `core.pack` + `core.fold` (the `balance_harness.py` precedent
for operator tools that import core).

Integrity gates, all fail-loud-write-nothing (the chronicler's
count-gate discipline):

1. the log is read through `core.log.read_log` — the canonical reader
   validates the header and every event line (a malformed log exits 1);
2. the loaded pack's `name_version` must equal the log header's `pack`
   field — a checkpoint folded from the wrong pack's initial projection
   is a lie;
3. every checkpoint is verified by re-fold (`verify_all` — one
   incremental pass) BEFORE any file is written.

Determinism: same log bytes + same pack + same flags = same artifact
bytes and same index bytes (no wall-clock, no absolute paths).

Usage:
    python scripts/checkpoint.py logs/run_123_0.jsonl
    python scripts/checkpoint.py logs/run_123_0.jsonl --every 20
    python scripts/checkpoint.py logs/run_123_0.jsonl --offsets 0,10,55
    python scripts/checkpoint.py logs/run_123_0.jsonl --pack content/tavern_pack --out DIR

Output: `output/checkpoints/<log_stem>/` — `checkpoint_<offset>.json`
per requested offset + `index.json` (the anchor records, sorted by
offset). Default: one checkpoint at the END (the full-log snapshot,
the cheap full-replay point). `--every N`: offsets 0, N, 2N, ... plus
always the end. The resume door (a live session over the log) is
owner-gated and NOT this tool (`phases.md` §7).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.checkpoint import (  # noqa: E402
    CheckpointError,
    CheckpointIndex,
    FoldCheckpoint,
    checkpoint_path,
    prefix_digest,
    save_checkpoint,
    verify_all,
    write_index,
)
from core.fold import Projection, apply_event, initial_projection  # noqa: E402
from core.log import EventRecord, LogError, read_log  # noqa: E402
from core.pack import Pack, PackError, load_pack  # noqa: E402


def resolve_offsets(n_events: int, *, every: int | None, offsets: Sequence[int]) -> list[int]:
    """The deterministic offset set: an explicit sorted-deduped list, or a
    cadence `0, N, 2N, ... ∪ {n_events}` (the end is always a checkpoint —
    it is the cheap full-replay point), or the single end checkpoint by
    default. Empty log: `[0]` — the initial-projection snapshot, the
    uniform zero member (no special cases, L14)."""
    if every is not None and offsets:
        raise CheckpointError("--every and --offsets are mutually exclusive")
    if every is not None:
        if every < 1:
            raise CheckpointError(f"--every must be >= 1, got {every}")
        return sorted(set(range(0, n_events, every)) | {n_events})
    if offsets:
        bad = [o for o in offsets if not isinstance(o, int) or o < 0 or o > n_events]
        if bad:
            raise CheckpointError(
                f"offsets must be ints in 0..{n_events}, got {bad}"
            )
        return sorted(set(offsets))
    return [n_events]


def build_checkpoints(
    pack: Pack,
    header: dict[str, Any],
    events: Sequence[EventRecord],
    *,
    every: int | None = None,
    offsets: Sequence[int] = (),
) -> list[FoldCheckpoint]:
    """Fold the log ONCE, snapshotting at each requested offset (the
    incremental build: O(N) plus one deep copy per checkpoint — never a
    re-fold per offset). Every snapshot is verified by re-fold before it
    leaves this function (the born-verified law)."""
    if header["pack"] != pack.name_version:
        raise CheckpointError(
            f"log header pack {header['pack']!r} != loaded pack "
            f"{pack.name_version!r} — the initial projection would be a lie"
        )
    wanted = resolve_offsets(len(events), every=every, offsets=offsets)
    initial: Projection = initial_projection(pack.entities)
    state: Projection = {entity: dict(props) for entity, props in initial.items()}
    snapshots: dict[int, FoldCheckpoint] = {}
    if 0 in wanted:
        snapshots[0] = FoldCheckpoint.from_state(state, 0)
    for count, event in enumerate(events, start=1):
        apply_event(state, event)
        if count in wanted:
            snapshots[count] = FoldCheckpoint.from_state(state, count)
    checkpoints = [snapshots[offset] for offset in wanted]
    verify_all(checkpoints, events, initial)  # born-verified: loud, write nothing
    return checkpoints


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="checkpoint",
        description="Build fold checkpoints over one committed JSONL run log "
        "(derived artifacts: snapshot + event-index offset + the sha256 "
        "anchor; never truth, never committed).",
    )
    parser.add_argument("log", type=Path, help="path to a run log (.jsonl)")
    parser.add_argument(
        "--pack", type=Path, default=REPO / "content" / "tavern_pack",
        help="pack directory whose initial projection seeds the fold "
        "(default: content/tavern_pack; cross-checked against the log header)",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="output directory (default: output/checkpoints/<log_stem>/)",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--every", type=int, default=None,
        help="cadence: checkpoints at 0, N, 2N, ... plus always the end",
    )
    group.add_argument(
        "--offsets", default="",
        help="explicit comma-separated offset list (e.g. 0,10,55)",
    )
    args = parser.parse_args(argv)

    try:
        schema = json.loads((REPO / "schemas" / "event.schema.json").read_text())
        header, events = read_log(args.log, schema)
        pack = load_pack(args.pack)
        explicit = _parse_offsets(args.offsets)
        checkpoints = build_checkpoints(
            pack, header, events, every=args.every, offsets=explicit
        )
    except (CheckpointError, LogError, PackError, OSError, ValueError) as exc:
        # LogError (malformed log) and PackError (bad pack dir) are
        # RuntimeError subclasses — caught by name; a malformed log or a
        # wrong pack exits loud with nothing written.
        print(f"checkpoint: {exc}", file=sys.stderr)
        return 1

    stem = args.log.name.rsplit(".", 1)[0]
    out_dir = args.out if args.out is not None else REPO / "output" / "checkpoints" / stem
    records = [
        save_checkpoint(cp, out_dir, prefix_digest(args.log, cp.offset))
        for cp in checkpoints
    ]
    index = CheckpointIndex(
        log=args.log.name, pack=pack.name_version, records=tuple(records)
    )
    write_index(index, out_dir)

    print(f"checkpoint: {args.log.name} ({len(events)} events, pack {pack.name_version})")
    for record in index.records:
        print(
            f"  {checkpoint_path(out_dir, record.offset)}  "
            f"offset={record.offset}  snapshot={record.snapshot_sha256[:16]}  "
            f"prefix={record.prefix_sha256[:16]}"
        )
    print(f"  {out_dir / 'index.json'}  ({len(records)} record(s))")
    return 0


def _parse_offsets(text: str) -> list[int]:
    if not text.strip():
        return []
    try:
        return [int(part) for part in text.split(",")]
    except ValueError as exc:
        raise CheckpointError(f"--offsets must be comma-separated ints, got {text!r}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
