"""iter-64 acceptance — the mode F offline chronicler (leg-4, phase 4;
`docs/TASKS.md` leg-4; contract owner: `docs/TEST_PLAN.md` §7;
architecture: `docs/blueprint/phases.md` §4 "Choricler mode F offline";
the donor pattern set: `docs/ref/duckdb.md` "what we take").

The law under test (D-093): DuckDB never enters the runtime import graph
(D-012 executable in `tests/test_architecture.py`); the chronicler speaks
only the log-file contract; every artifact is derived, rebuildable, and
byte-deterministic per environment; the count gate makes a silent intake
drop an integrity failure, never a partial archive.

The instrument (the blind-1 law: pure test-side folds, never the
engine's paths in the checked pipeline): the chronicler reads the log
through DuckDB's `read_ndjson_auto` — these tests cross-check every
output against an independent stdlib fold of the SAME log via
`core.log.read_log` (the engine's canonical reader). A checker that
shares the checked code cannot catch its bugs.

The suite is green with and without duckdb installed
(`pytest.importorskip` — the retr-1 sqlite-vec probe philosophy): the
pure-dev env (`pip install -e ".[dev]"`) skips; the chronicler env
(`pip install -e ".[dev,chronicler]"`) runs everything.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

pytest.importorskip("duckdb")  # the [chronicler] extra: skip cleanly without it

import chronicle  # type: ignore[import-not-found]  # noqa: E402
import duckdb  # noqa: E402

from core.log import read_log  # noqa: E402
from core.loop import Simulator  # noqa: E402
from core.pack import load_pack  # noqa: E402

PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

#: The manifest's exact key set — the deterministic contract (no
#: wall-clock, no absolute paths, no environment-variant keys beyond the
#: recorded duckdb_version, mirroring the log header's own python field).
_MANIFEST_KEYS = {
    "log", "log_sha256", "n_lines", "n_events", "schema_version", "seed",
    "python", "commit", "pack", "duckdb_version", "write_mode", "artifacts",
}
_ARTIFACTS = ("events.parquet", "state_diffs.parquet", "chronicle.sqlite")


def _run_day1(seed: int, tmp_path: Path) -> Path:
    """day1_full on a seed (the 10-seed family witness pattern)."""
    log = tmp_path / f"day1_chronicle_{seed}.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    return log


def _read_events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _sqlite_rows(path: Path, table: str) -> list[tuple[Any, ...]]:
    cx = sqlite3.connect(path)
    try:
        return cx.execute(f'SELECT * FROM "{table}"').fetchall()
    finally:
        cx.close()


def _norm(rows: list[tuple[Any, ...]]) -> list[tuple[str, ...]]:
    return [tuple(str(v) for v in row) for row in rows]


def _json_text(value: Any) -> str:
    """The chronicler's value encoding: CAST(JSON AS VARCHAR) == json.dumps."""
    return json.dumps(value)


def _scanner_available() -> bool:
    con = duckdb.connect()
    try:
        row = con.execute(
            "SELECT installed OR loaded FROM duckdb_extensions() "
            "WHERE extension_name = 'sqlite_scanner'"
        ).fetchone()
        return bool(row and row[0])
    finally:
        con.close()


# -- the pipeline artifacts ------------------------------------------------------


def test_artifacts_and_manifest_contract(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    out = tmp_path / "chron"
    manifest = chronicle.run_chronicler(log, out)
    assert manifest is not None
    assert sorted(p.name for p in out.iterdir()) == sorted(
        _ARTIFACTS + ("manifest.json",)
    )
    on_disk = json.loads((out / "manifest.json").read_text())
    assert on_disk == manifest  # the file is the dict, byte-for-byte semantics
    assert set(manifest) == _MANIFEST_KEYS
    assert manifest["n_events"] == len(_read_events(log)) == 55
    assert manifest["n_lines"] == manifest["n_events"] + 1
    assert manifest["log"] == log.name
    assert manifest["log_sha256"] == hashlib.sha256(log.read_bytes()).hexdigest()
    assert manifest["seed"] == 123
    assert manifest["commit"] == "0000000"
    for name, info in manifest["artifacts"].items():
        assert info["sha256"] == hashlib.sha256((out / name).read_bytes()).hexdigest()
    assert manifest["write_mode"] in ("attach", "stdlib")


def test_events_archive_is_the_log(tmp_path: Path) -> None:
    """The cold archive: one row per event, canonical order, the header
    line dropped (the count gate's standing law)."""
    log = _run_day1(123, tmp_path)
    out = tmp_path / "chron"
    chronicle.run_chronicler(log, out)
    con = duckdb.connect()
    try:
        ids = [r[0] for r in con.execute(
            f"SELECT id FROM read_parquet('{out / 'events.parquet'}') ORDER BY id"
        ).fetchall()]
        types = {r[0] for r in con.execute(
            f"DESCRIBE SELECT * FROM read_parquet('{out / 'events.parquet'}')"
        ).fetchall()}
    finally:
        con.close()
    events = _read_events(log)
    assert ids == [e.id for e in events]
    assert len(ids) == 55
    # the uniform archive schema: always the twelve canonical fields
    # (EVENT_SCHEMA §2) — the header keys never enter the archive
    assert types == set(chronicle.EVENT_FIELDS)


def test_state_diffs_lag_law(tmp_path: Path) -> None:
    """The window-diff law, cross-checked against a pure Python fold:
    per (entity, prop) ordered by (t, event_id), prev_to is the previous
    change's to; continuous is NULL on the first change (no previous),
    then from == prev_to."""
    log = _run_day1(123, tmp_path)
    out = tmp_path / "chron"
    manifest = chronicle.run_chronicler(log, out)
    con = duckdb.connect()
    try:
        got = con.execute(
            f"SELECT event_id, t, actor, type, entity, prop, from_value, "
            f"to_value, irreversible, prev_to, continuous "
            f"FROM read_parquet('{out / 'state_diffs.parquet'}')"
        ).fetchall()
    finally:
        con.close()

    fold: list[tuple[str, int, str, str, str, str, str, str, bool, str | None, bool | None]] = []
    last: dict[tuple[str, str], Any] = {}
    for e in _read_events(log):
        for c in e.state_changes:
            key = (c.entity, c.prop)
            prev = last.get(key)
            fold.append((
                e.id, e.t, e.actor, e.type, c.entity, c.prop,
                _json_text(c.from_), _json_text(c.to_), c.irreversible,
                None if prev is None else _json_text(prev),
                None if prev is None else _json_text(c.from_) == _json_text(prev),
            ))
            last[key] = c.to_
    fold.sort(key=lambda r: (r[4], r[5], r[1], r[0]))
    assert _norm(got) == _norm(fold)
    # a concrete witness: the PC's position chain is continuous
    pc_rows = [r for r in got if r[4] == "pc_01" and r[5] == "position"]
    assert len(pc_rows) >= 2
    assert all(r[10] is True for r in pc_rows[1:])
    assert manifest is not None
    assert manifest["artifacts"]["state_diffs.parquet"]["rows"] == len(fold) == 44


def test_summary_sqlite_matches_python_fold(tmp_path: Path) -> None:
    """Every summary table, cross-checked against the stdlib fold."""
    log = _run_day1(123, tmp_path)
    out = tmp_path / "chron"
    manifest = chronicle.run_chronicler(log, out)
    assert manifest is not None
    sq = out / "chronicle.sqlite"
    events = _read_events(log)

    # facts_summary: per actor
    fold_actors = {}
    for e in events:
        a = fold_actors.setdefault(
            e.actor,
            {"event_count": 0, "first_tick": e.t, "last_tick": e.t,
             "state_changes": 0, "knowledge_out": 0},
        )
        a["event_count"] += 1
        a["first_tick"] = min(a["first_tick"], e.t)
        a["last_tick"] = max(a["last_tick"], e.t)
        a["state_changes"] += len(e.state_changes)
        a["knowledge_out"] += len(e.knowledge)
    got = _sqlite_rows(sq, "facts_summary")
    assert _norm(got) == _norm(
        (actor, v["event_count"], v["first_tick"], v["last_tick"],
         v["state_changes"], v["knowledge_out"])
        for actor, v in sorted(fold_actors.items())
    )

    # type_histogram
    hist = Counter(e.type for e in events)
    got = _sqlite_rows(sq, "type_histogram")
    assert _norm(got) == _norm([(t, n) for t, n in sorted(hist.items())])

    # knowledge_summary: per knower, by channel
    know: Counter = Counter()
    chans: Counter = Counter()
    for e in events:
        for k in e.knowledge:
            know[k.who] += 1
            chans[(k.who, k.channel)] += 1
    got = _sqlite_rows(sq, "knowledge_summary")
    expected = [
        (who, know[who], chans[(who, "saw")], chans[(who, "heard")],
         chans[(who, "told")], chans[(who, "inferred")])
        for who in sorted(know)
    ]
    assert _norm(got) == _norm(expected)

    # state_current: the (entity, prop) fold snapshot
    current: dict[tuple[str, str], tuple[str, str, int, int]] = {}
    counts: Counter = Counter()
    for e in events:
        for c in e.state_changes:
            key = (c.entity, c.prop)
            counts[key] += 1
            current[key] = (_json_text(c.to_), e.id, e.t)
    got = _sqlite_rows(sq, "state_current")
    expected = [
        (entity, prop, v[0], v[1], v[2], counts[(entity, prop)])
        for (entity, prop), v in sorted(current.items())
    ]
    assert _norm(got) == _norm(expected)

    # chronicle_meta: the artifact's own identity
    meta = dict(_sqlite_rows(sq, "chronicle_meta"))
    assert meta["log"] == log.name
    assert meta["log_sha256"] == manifest["log_sha256"]
    assert meta["n_events"] == "55"
    assert meta["write_mode"] == manifest["write_mode"]
    assert meta["seed"] == "123"
    assert meta["schema_version"] == manifest["schema_version"]


def test_chronicler_determinism(tmp_path: Path) -> None:
    """Same log bytes + same environment = same artifact bytes (INV-2's
    spirit, offline): two full runs, every artifact sha256 equal."""
    log = _run_day1(123, tmp_path)
    out1, out2 = tmp_path / "run1", tmp_path / "run2"
    m1 = chronicle.run_chronicler(log, out1)
    m2 = chronicle.run_chronicler(log, out2)
    assert m1 is not None and m2 is not None
    assert m1["write_mode"] == m2["write_mode"]
    for name in _ARTIFACTS + ("manifest.json",):
        assert (out1 / name).read_bytes() == (out2 / name).read_bytes(), name


def test_write_ladder_equivalence(tmp_path: Path) -> None:
    """The L12 ladder: attach (when locally available) and stdlib write
    logically identical summaries — the lifted pattern and the floor are
    the same artifact, only the bytes differ."""
    log = _run_day1(123, tmp_path)
    out_a, out_s = tmp_path / "via_attach", tmp_path / "via_stdlib"
    m_std = chronicle.run_chronicler(log, out_s, sqlite_via="stdlib")
    assert m_std is not None and m_std["write_mode"] == "stdlib"
    if not _scanner_available():
        pytest.skip("sqlite_scanner not locally available (offline env)")
    m_att = chronicle.run_chronicler(log, out_a, sqlite_via="attach")
    assert m_att is not None and m_att["write_mode"] == "attach"
    assert m_att["log_sha256"] == m_std["log_sha256"]
    for table in ("facts_summary", "state_current", "type_histogram",
                  "knowledge_summary"):
        a = _sqlite_rows(out_a / "chronicle.sqlite", table)
        s = _sqlite_rows(out_s / "chronicle.sqlite", table)
        assert _norm(a) == _norm(s), table
    meta_a = dict(_sqlite_rows(out_a / "chronicle.sqlite", "chronicle_meta"))
    meta_s = dict(_sqlite_rows(out_s / "chronicle.sqlite", "chronicle_meta"))
    assert {k: v for k, v in meta_a.items() if k != "write_mode"} == {
        k: v for k, v in meta_s.items() if k != "write_mode"
    }


def test_scale_gate_noop(tmp_path: Path) -> None:
    """Below --min-events: a clean no-op — no artifacts, no output dir."""
    log = _run_day1(123, tmp_path)
    out = tmp_path / "gated"
    result = chronicle.run_chronicler(log, out, min_events=1000)
    assert result is None
    assert not out.exists()


def test_count_gate_rejects_silent_drop(tmp_path: Path) -> None:
    """A line DuckDB cannot serve (truncated JSON) but the file holds:
    integrity failure — exit loud, write nothing."""
    log = _run_day1(123, tmp_path)
    lines = log.read_text().splitlines()
    lines.insert(5, '{"id": "ev_0099", "t": 99, "typ')
    broken = tmp_path / "broken.jsonl"
    broken.write_text("\n".join(lines) + "\n")
    out = tmp_path / "gated"
    with pytest.raises(chronicle.ChronicleError, match="count gate"):
        chronicle.run_chronicler(broken, out)
    assert not out.exists() or not any(out.iterdir())


def test_count_gate_accepts_line_prefix(tmp_path: Path) -> None:
    """Any line-aligned prefix is a legal log (append-only): the chronicler
    archives the prefix, not the future."""
    log = _run_day1(123, tmp_path)
    lines = log.read_text().splitlines()
    prefix = tmp_path / "prefix.jsonl"
    prefix.write_text("\n".join(lines[:30]) + "\n")
    out = tmp_path / "prefix_out"
    manifest = chronicle.run_chronicler(prefix, out)
    assert manifest is not None
    assert manifest["n_events"] == 29
    assert manifest["n_lines"] == 30


def test_header_only_log_is_uniform(tmp_path: Path) -> None:
    """A header-only log (a crash between header and run-start) is handled
    uniformly: zero-event artifacts, gate 0 == 1 - 1."""
    log = _run_day1(123, tmp_path)
    header = log.read_text().splitlines()[0]
    empty = tmp_path / "empty.jsonl"
    empty.write_text(header + "\n")
    out = tmp_path / "empty_out"
    manifest = chronicle.run_chronicler(empty, out)
    assert manifest is not None
    assert manifest["n_events"] == 0
    assert manifest["artifacts"]["events.parquet"]["rows"] == 0
    assert _norm(_sqlite_rows(out / "chronicle.sqlite", "facts_summary")) == []
