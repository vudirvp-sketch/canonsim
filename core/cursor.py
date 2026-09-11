"""The run cursor (iter-106, `--resume`; the resume door `phases.md` §7
marked owner-gated, opened by the owner's call — D-139).

The log is the truth of the PAST (INV-1): the fold rebuilds the world
from it, and so does a resumed session — for everything the log can
carry. One piece of run state is NOT a function of the log: the
entropy position. Silent draws — an urgency roll that misses, a
weather self-roll that keeps the sky, a faction goal that fails its
bar — consume stream positions WITHOUT committing events, so no fold
can recover them (INV-2's RngBank is stateful per stream by design,
D-028). The cursor is that missing record: the run's bank positions,
director run marks, clock and crossing cursors, pinned by the session
at every CLEAN DRAIN boundary (the queue empty — a mid-drain state is
not resume-able and is never saved; `Simulator.export_cursor` owns
that law).

Artifact laws (the checkpoint family, `core/checkpoint.py`):

- **Derived of the RUN, never of the log, never canon.** A fold
  checkpoint is a pure function of the log prefix; a cursor is a pure
  function of the live run that wrote it. It writes NOTHING to the
  log, and its loss costs only resume-exactness — a log without its
  cursor is still complete, replayable, foldable (INV-1 untouched);
  the resumed continuation simply restarts the entropy streams, which
  is why a lost cursor is not rebuilt silently but refused loudly.
- **Bound to its log.** `event_count` + `prefix_sha256`
  (`core.checkpoint.prefix_digest` — the append-stable prefix
  identity) pin the exact log bytes the cursor was saved against. A
  log that moved past the cursor (a mid-drain crash, a manual append)
  refuses LOUD at resume: the entropy consumed by the extra events is
  unrecoverable, and guessing it would be save-scumming dressed as
  determinism.
- **Byte-deterministic serialization** — sorted keys, compact JSON,
  no wall-clock (INV-2's spirit: same run state, same bytes, any
  process, any PYTHONHASHSEED).
- **Exact envelope** — a closed key set, the log header's own law
  (`core.log.validate_header`): a field that must not appear cannot
  appear.

The resume law itself (D-139): **resume is invisible to the log.** A
session interrupted at a drain boundary and resumed with the same
remaining steps produces byte-identical bytes to the uninterrupted
run — interruption is not an input, only steps are. T1's guarantee
extended across process boundaries; `tests/test_resume.py` pins it at
every split point. What the cursor deliberately does NOT carry: the
projection, the knowledge index, the seeded-hook buffer, the
last-change index (all rebuild from the log at resume), the
WorldModel (a pure function of seed + pack config, re-derived by
`core.worldgen.generate_world`), and the scene ledger (session-scoped
by law, D-049 — it dies with its session, promoted texture rode
events).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

__all__ = [
    "CURSOR_KEYS",
    "CURSOR_SUFFIX",
    "CursorError",
    "cursor_path",
    "load_cursor",
    "save_cursor",
]

CURSOR_SUFFIX: Final = ".cursor.json"
CURSOR_KEYS: Final = frozenset({
    "seed",
    "pack",
    "event_count",
    "prefix_sha256",
    "tick",
    "next_rotation",
    "next_beat",
    "next_macro",
    "intent_seq",
    "director_enabled",
    "bank",
    "director",
})
_BANK_KEYS: Final = frozenset({"streams", "counts"})


class CursorError(RuntimeError):
    """Cursor shape or binding failure (envelope, digest, staleness)."""


def cursor_path(log_path: Path) -> Path:
    """The cursor file for a run log: `<stem>.cursor.json` beside it —
    `run_42_0.jsonl` → `run_42_0.cursor.json`. Sibling of the log (both
    live under the gitignored runtime dirs; never committed)."""
    return log_path.with_suffix(CURSOR_SUFFIX)


def save_cursor(path: Path, cursor: Mapping[str, Any]) -> None:
    """Validate the envelope, then write the artifact — byte-deterministic
    (sorted keys, compact separators, one trailing newline; no wall-clock,
    no absolute paths). A wrong-shape cursor is a caller bug: loud before
    anything reaches disk (the count-gate spirit)."""
    _validate(cursor)
    data = json.dumps(cursor, sort_keys=True, separators=(",", ":"))
    path.write_text(data + "\n", encoding="utf-8")


def load_cursor(path: Path) -> dict[str, Any]:
    """Read a cursor back — loud on any drift: unreadable file, bad JSON,
    wrong envelope, wrong scalar types (CursorError names the path). The
    bank and director sub-shapes are validated by their own restore doors
    (`RngBank.restore_state`, `Director.restore_run_state`) — one owner
    per law (D-024)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CursorError(f"{path}: cannot read the run cursor: {exc}") from exc
    if not isinstance(data, dict):
        raise CursorError(f"{path}: the run cursor must be a JSON object")
    _validate(data)
    return data


def _validate(cursor: Mapping[str, Any]) -> None:
    """The envelope gate: exact key set, scalar types, the two sub-mappings
    present. Everything deeper belongs to the consuming modules."""
    keys = set(cursor)
    if keys != CURSOR_KEYS:
        raise CursorError(
            f"cursor keys must be exactly {sorted(CURSOR_KEYS)}, got "
            f"{sorted(keys)}"
        )
    _require_int(cursor, "seed")
    _require_int(cursor, "event_count", minimum=0)
    _require_int(cursor, "tick", minimum=0)
    _require_int(cursor, "intent_seq", minimum=0)
    if not isinstance(cursor["pack"], str):
        raise CursorError(f"cursor 'pack' must be a string, got {cursor['pack']!r}")
    digest = cursor["prefix_sha256"]
    if not _is_sha256_hex(digest):
        raise CursorError(
            "cursor 'prefix_sha256' must be sha256 hex (64 lowercase "
            f"chars), got {digest!r}"
        )
    if not isinstance(cursor["director_enabled"], bool):
        raise CursorError(
            f"cursor 'director_enabled' must be a bool, got "
            f"{cursor['director_enabled']!r}"
        )
    for key in ("next_rotation", "next_beat", "next_macro"):
        value = cursor[key]
        if value is None:
            continue
        if (
            not isinstance(value, int) or isinstance(value, bool) or value < 0
        ):
            raise CursorError(
                f"cursor {key!r} must be a non-negative int or null, got {value!r}"
            )
    bank = cursor["bank"]
    if not isinstance(bank, Mapping) or set(bank) != _BANK_KEYS:
        raise CursorError(
            f"cursor 'bank' must be a mapping with keys {sorted(_BANK_KEYS)}, "
            f"got {bank!r}"
        )
    if not isinstance(cursor["director"], Mapping):
        raise CursorError(
            f"cursor 'director' must be a mapping, got {cursor['director']!r}"
        )


def _require_int(cursor: Mapping[str, Any], key: str, *, minimum: int | None = None) -> None:
    """One scalar's type gate (bools are not ints here, as ever)."""
    value = cursor[key]
    if not isinstance(value, int) or isinstance(value, bool):
        raise CursorError(f"cursor {key!r} must be an int, got {value!r}")
    if minimum is not None and value < minimum:
        raise CursorError(f"cursor {key!r} must be >= {minimum}, got {value!r}")


def _is_sha256_hex(text: object) -> bool:
    """The digest form (sha256, lowercase hex, 64 chars) — the shape
    `core.checkpoint` established for every anchor in this family."""
    return (
        isinstance(text, str)
        and len(text) == 64
        and all(c in "0123456789abcdef" for c in text)
    )
