"""depth-4 acceptance — fold checkpoints (phase 5; `docs/TASKS.md`
depth-4; design owner `docs/blueprint/phases.md` §5 "Fold checkpoints";
mechanism owner `core/checkpoint.py`; builder `scripts/checkpoint.py`).

The laws under test (the chronicler family's derived-artifact law):

- **Derived, never truth**: no log byte moves; the corpus price is zero
  by construction (nothing in the runtime pipeline is touched).
- **Snapshot + tail replay == full fold** (rollback, phases.md §5) —
  cross-checked against the LIVE runtime projection (the blind-1
  instrument law: the Simulator's incremental state is an evolution
  path the checkpoint code never sees, not a shared fold).
- **Byte-deterministic serialization**: same state -> same canonical
  bytes, any construction path; two builds -> identical artifact and
  index bytes (INV-2's spirit, offline).
- **The re-fold law**: verify/verify_all catch a tampered snapshot, a
  wrong offset, an out-of-bounds offset — a checker that cannot fail
  is decoration.
- **The anchor lives in the index**: load_checkpoint rejects an edited
  artifact (sha mismatch), a missing file, an offset disagreement;
  read_index rejects a hand-edited unsorted index.
- **Append-stability**: the prefix digest of offset K is unchanged when
  the log grows (INV-5 — the checkpoint stays bound to its prefix).
- **The prefix gate**: prefix_digest is loud on a log shorter than the
  offset claims.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import checkpoint as checkpoint_cli  # type: ignore[import-not-found]  # noqa: E402

from core.checkpoint import (  # noqa: E402
    INDEX_NAME,
    CheckpointError,
    CheckpointIndex,
    CheckpointRecord,
    FoldCheckpoint,
    canonical_state_bytes,
    checkpoint_path,
    load_checkpoint,
    prefix_digest,
    read_index,
    save_checkpoint,
    sha256_hex,
    verify,
    verify_all,
    write_index,
)
from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator  # noqa: E402
from core.pack import load_pack  # noqa: E402

PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())
INITIAL = initial_projection(PACK.entities)


def _run_day1(seed: int, tmp_path: Path) -> Path:
    """day1_full on a seed + the LIVE final projection (the runtime's own
    incremental state — the independent evolution path)."""
    log = tmp_path / f"day1_checkpoint_{seed}.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    return log


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return list(events)


_LIVE: dict[str, dict[str, Any]] = {}  # seed -> the runtime's final projection


def _live_projection(seed: int, tmp_path: Path) -> dict[str, Any]:
    if seed not in _LIVE:
        _run_day1(seed, tmp_path)  # the log exists; the live sim re-runs it below
        sim = Simulator(PACK, seed, tmp_path / f"live_{seed}.jsonl", SCHEMA, commit="0000000")
        sim.run_playscript(dict(DAY1, seed=seed))
        _LIVE[seed] = {
            entity: dict(props) for entity, props in sim.projection.items()
        }
        sim.close()
    return _LIVE[seed]


# -- the snapshot + tail replay law (rollback) ---------------------------------


def test_offset_zero_is_the_initial_projection(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cp = FoldCheckpoint.from_events(events, INITIAL, 0)
    assert canonical_state_bytes(cp.state) == canonical_state_bytes(INITIAL)
    verify(cp, events, INITIAL)


def test_end_checkpoint_matches_runtime_projection(tmp_path: Path) -> None:
    """The three-way agreement at the end: the checkpoint's snapshot ==
    the LIVE runtime projection == the fold (the runtime's incremental
    path never touches the checkpoint code — the blind-1 instrument)."""
    log = _run_day1(123, tmp_path)
    events = _events(log)
    live = _live_projection(123, tmp_path)
    cp = FoldCheckpoint.from_events(events, INITIAL, len(events))
    assert canonical_state_bytes(cp.state) == canonical_state_bytes(live)
    assert canonical_state_bytes(cp.state) == canonical_state_bytes(
        fold(events, INITIAL)
    )
    verify(cp, events, INITIAL)


def test_restore_mid_checkpoint_equals_full_fold(tmp_path: Path) -> None:
    """Rollback = snapshot + tail replay: restoring at a mid offset and
    replaying the tail reproduces the full fold, and the LIVE runtime
    projection (the strong cross-check)."""
    log = _run_day1(123, tmp_path)
    events = _events(log)
    live = _live_projection(123, tmp_path)
    for offset in (1, 7, 25, len(events) - 1, len(events)):
        cp = FoldCheckpoint.from_events(events, INITIAL, offset)
        restored = cp.restore(events)
        assert canonical_state_bytes(restored) == canonical_state_bytes(live), offset


def test_restore_loud_on_truncated_log(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cp = FoldCheckpoint.from_events(events, INITIAL, 50)
    with pytest.raises(CheckpointError, match="truncated"):
        cp.restore(events[:30])


def test_restore_loud_on_diverged_snapshot(tmp_path: Path) -> None:
    """A tampered snapshot goes loud on the first tail event touching the
    diverged prop — apply_event's from_-check, INV-1's own net."""
    log = _run_day1(123, tmp_path)
    events = _events(log)
    offset = next(
        i for i, e in enumerate(events) if e.state_changes
    )  # the first state-writing event
    cp = FoldCheckpoint.from_events(events, INITIAL, offset)
    prop = events[offset].state_changes[0].prop
    entity = events[offset].state_changes[0].entity
    tampered = {e: dict(p) for e, p in cp.state.items()}
    tampered[entity][prop] = "tampered"
    bad = FoldCheckpoint(offset=cp.offset, state=tampered)
    with pytest.raises(ValueError, match="expected from"):
        bad.restore(events)


# -- the re-fold law -----------------------------------------------------------


def test_verify_green_on_honest_checkpoints(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cps = [
        FoldCheckpoint.from_events(events, INITIAL, offset)
        for offset in (0, 3, 30, len(events))
    ]
    for cp in cps:
        verify(cp, events, INITIAL)
    verify_all(cps, events, INITIAL)


def test_verify_loud_on_tampered_snapshot(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cp = FoldCheckpoint.from_events(events, INITIAL, 30)
    state = {e: dict(p) for e, p in cp.state.items()}
    first = sorted(state)[0]
    state[first][sorted(state[first])[0]] = "drifted"
    tampered = FoldCheckpoint(offset=30, state=state)
    with pytest.raises(CheckpointError, match="re-fold"):
        verify(tampered, events, INITIAL)
    with pytest.raises(CheckpointError, match="re-fold"):
        verify_all([tampered], events, INITIAL)
    with pytest.raises(CheckpointError, match="duplicate"):
        verify_all([cp, cp], events, INITIAL)


def test_verify_loud_on_wrong_offset(tmp_path: Path) -> None:
    """A snapshot folded to offset 30 but claiming offset 10: the re-fold
    at 10 disagrees — loud."""
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cp = FoldCheckpoint.from_events(events, INITIAL, 30)
    mislabeled = FoldCheckpoint(offset=10, state=cp.state)
    with pytest.raises(CheckpointError, match="re-fold"):
        verify(mislabeled, events, INITIAL)


def test_verify_loud_on_out_of_bounds_offset(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    cp = FoldCheckpoint.from_state(INITIAL, 999)
    with pytest.raises(CheckpointError, match="out of bounds"):
        verify(cp, events, INITIAL)
    with pytest.raises(CheckpointError, match="out of bounds"):
        verify_all([cp], events, INITIAL)


# -- byte-determinism + the canonical serialization ---------------------------


def test_canonical_bytes_exact_and_sorted() -> None:
    state = {"b_entity": {"z_prop": 1, "a_prop": "x"}, "a_entity": {"m": None}}
    expected = (
        b'{"a_entity":{"m":null},"b_entity":{"a_prop":"x","z_prop":1}}'
    )
    assert canonical_state_bytes(state) == expected
    cp = FoldCheckpoint(offset=2, state={"a": {"p": True}})
    assert cp.to_bytes() == b'{"offset":2,"state":{"a":{"p":true}}}\n'
    assert cp.digest == sha256_hex(cp.to_bytes())


def test_determinism_two_builds_identical_bytes(tmp_path: Path) -> None:
    """Same log + same pack + same flags = same artifact and index bytes
    (INV-2's spirit, offline; the manifest law)."""
    log = _run_day1(123, tmp_path)
    out1, out2 = tmp_path / "b1", tmp_path / "b2"
    for out in (out1, out2):
        rc = checkpoint_cli.main([str(log), "--every", "10", "--out", str(out)])
        assert rc == 0
    names = sorted(p.name for p in out1.iterdir())
    assert names == sorted(p.name for p in out2.iterdir())
    for name in names:
        assert (out1 / name).read_bytes() == (out2 / name).read_bytes(), name


# -- the prefix identity (append-stable) ---------------------------------------


def test_prefix_digest_append_stable(tmp_path: Path) -> None:
    """The log only grows (INV-5): a prefix digest computed before an
    append equals the one after — the checkpoint stays bound to its
    log while the run continues. Longer prefixes differ."""
    log = _run_day1(123, tmp_path)
    offset = 20
    before = prefix_digest(log, offset)
    lines = log.read_text().splitlines(keepends=True)
    appended = tmp_path / "grown.jsonl"
    appended.write_text("".join(lines) + "".join(lines[1:6]))  # header + 59 events
    assert prefix_digest(appended, offset) == before
    assert prefix_digest(appended, offset) != prefix_digest(appended, offset + 1)


def test_prefix_digest_loud_on_short_log(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    with pytest.raises(CheckpointError, match="truncated"):
        prefix_digest(log, 100)
    with pytest.raises(CheckpointError, match="non-negative"):
        prefix_digest(log, -1)


def test_prefix_digest_matches_line_prefix_bytes(tmp_path: Path) -> None:
    """The prefix digest is exactly sha256 over the first 1+offset lines'
    raw bytes — the file IS the identity (INV-1)."""
    log = _run_day1(123, tmp_path)
    offset = 12
    raw = log.read_bytes().splitlines(keepends=True)
    expected = hashlib.sha256(b"".join(raw[: offset + 1])).hexdigest()
    assert prefix_digest(log, offset) == expected


# -- copy discipline ------------------------------------------------------------


def test_from_state_and_restore_never_alias_live_state(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    state = fold(events[:30], INITIAL)
    cp = FoldCheckpoint.from_state(state, 30)
    state[sorted(state)[0]][sorted(state[sorted(state)[0]])[0]] = "mutated"
    assert cp.state[sorted(cp.state)[0]][sorted(cp.state[sorted(cp.state)[0]])[0]] != "mutated"
    bytes_before = cp.to_bytes()
    cp.restore(events)
    assert cp.to_bytes() == bytes_before  # restore never mutates the snapshot


# -- the artifact I/O + the anchor teeth ---------------------------------------


def test_save_load_round_trip_and_anchor_teeth(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    out = tmp_path / "cps"
    cp = FoldCheckpoint.from_events(events, INITIAL, 30)
    record = save_checkpoint(cp, out, prefix_digest(log, 30))
    loaded = load_checkpoint(record, out)
    assert canonical_state_bytes(loaded.state) == canonical_state_bytes(cp.state)
    assert loaded.offset == 30

    # the anchor's teeth: an edited artifact file is loud
    path = checkpoint_path(out, 30)
    tampered = json.loads(path.read_text())
    tampered["state"][sorted(tampered["state"])[0]]["drift"] = 1
    path.write_text(json.dumps(tampered, sort_keys=True, separators=(",", ":")) + "\n")
    with pytest.raises(CheckpointError, match="anchor mismatch"):
        load_checkpoint(record, out)

    # a missing artifact is loud
    path.unlink()
    with pytest.raises(CheckpointError, match="missing"):
        load_checkpoint(record, out)


def test_load_loud_on_offset_disagreement(tmp_path: Path) -> None:
    """The file exists at the record's path and its sha matches, but the
    envelope's offset disagrees with the index record — loud (a renamed
    or re-filed artifact)."""
    log = _run_day1(123, tmp_path)
    events = _events(log)
    out = tmp_path / "cps"
    cp = FoldCheckpoint.from_events(events, INITIAL, 30)
    record = save_checkpoint(cp, out, prefix_digest(log, 30))
    refiled = CheckpointRecord(
        offset=31, prefix_sha256=record.prefix_sha256,
        snapshot_sha256=record.snapshot_sha256,
    )
    (out / "checkpoint_000030.json").rename(out / "checkpoint_000031.json")
    with pytest.raises(CheckpointError, match="offset"):
        load_checkpoint(refiled, out)


def test_from_bytes_shape_teeth() -> None:
    good = FoldCheckpoint(offset=1, state={"e": {"p": 2}})
    assert FoldCheckpoint.from_bytes(good.to_bytes()) == good
    for bad in (
        b"not json",
        b'{"offset": 1}',
        b'{"offset": 1, "state": {"e": {"p": 2}}, "extra": 0}',
        b'{"offset": -1, "state": {}}',
        b'{"offset": true, "state": {}}',
        b'{"offset": 1, "state": {"e": 5}}',
    ):
        with pytest.raises(CheckpointError):
            FoldCheckpoint.from_bytes(bad)


def test_index_round_trip_and_hand_edit_teeth(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    events = _events(log)
    out = tmp_path / "cps"
    records = tuple(
        save_checkpoint(
            FoldCheckpoint.from_events(events, INITIAL, o), out, prefix_digest(log, o)
        )
        for o in (0, 10, len(events))
    )
    index = CheckpointIndex(log=log.name, pack=PACK.name_version, records=records)
    path = write_index(index, out)
    assert path.name == INDEX_NAME
    back = read_index(out)
    assert back == index

    # the index bytes: content-derived only, exact envelope
    data = json.loads(path.read_text())
    assert set(data) == {"checkpoints", "log", "pack"}
    assert data["log"] == log.name
    assert data["pack"] == PACK.name_version

    # hand-edit teeth: unsorted offsets / wrong keys / bad digests
    # (each case starts from the pristine index bytes — restored after)
    pristine = path.read_bytes()

    def _rewrite(data: dict[str, Any]) -> None:
        path.write_text(json.dumps(data, indent=2))

    unsorted = json.loads(pristine)
    unsorted["checkpoints"] = list(reversed(unsorted["checkpoints"]))
    _rewrite(unsorted)
    with pytest.raises(CheckpointError, match="sorted"):
        read_index(out)
    path.write_bytes(pristine)

    wrong_keys = json.loads(pristine)
    wrong_keys["extra"] = 1
    _rewrite(wrong_keys)
    with pytest.raises(CheckpointError, match="index keys"):
        read_index(out)
    path.write_bytes(pristine)

    bad_digest = json.loads(pristine)
    bad_digest["checkpoints"][0]["snapshot_sha256"] = "zz"
    _rewrite(bad_digest)
    with pytest.raises(CheckpointError, match="sha256 hex"):
        read_index(out)
    path.write_bytes(pristine)
    assert read_index(out) == index  # pristine again — round-trip intact


def test_save_checkpoint_rejects_bad_prefix_digest(tmp_path: Path) -> None:
    cp = FoldCheckpoint(offset=0, state={})
    with pytest.raises(CheckpointError, match="prefix_sha256"):
        save_checkpoint(cp, tmp_path / "x", "not-a-digest")


# -- the builder CLI ------------------------------------------------------------


def test_cli_default_end_checkpoint(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    out = tmp_path / "out"
    rc = checkpoint_cli.main([str(log), "--out", str(out)])
    assert rc == 0
    n = len(_events(log))
    assert sorted(p.name for p in out.iterdir()) == [
        f"checkpoint_{n:06d}.json", INDEX_NAME,
    ]
    index = read_index(out)
    assert [r.offset for r in index.records] == [n]
    # the loaded artifact restores the full log from nothing (snapshot == fold)
    cp = load_checkpoint(index.records[0], out)
    events = _events(log)
    assert canonical_state_bytes(cp.state) == canonical_state_bytes(fold(events, INITIAL))


def test_cli_every_cadence_offsets(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    n = len(_events(log))
    assert checkpoint_cli.resolve_offsets(n, every=None, offsets=[]) == [n]
    assert checkpoint_cli.resolve_offsets(n, every=20, offsets=[]) == [0, 20, 40, 55]
    assert checkpoint_cli.resolve_offsets(n, every=None, offsets=[55, 0, 20]) == [0, 20, 55]
    assert checkpoint_cli.resolve_offsets(0, every=None, offsets=[]) == [0]
    assert checkpoint_cli.resolve_offsets(0, every=5, offsets=[]) == [0]
    with pytest.raises(CheckpointError, match="mutually exclusive"):
        checkpoint_cli.resolve_offsets(n, every=5, offsets=[1])
    with pytest.raises(CheckpointError, match="0.."):
        checkpoint_cli.resolve_offsets(n, every=None, offsets=[n + 1])

    out = tmp_path / "out"
    rc = checkpoint_cli.main([str(log), "--every", "20", "--out", str(out)])
    assert rc == 0
    index = read_index(out)
    assert [r.offset for r in index.records] == [0, 20, 40, 55]
    # every artifact restores to the same full fold (the tail-replay law)
    events = _events(log)
    for record in index.records:
        cp = load_checkpoint(record, out)
        assert canonical_state_bytes(cp.restore(events)) == canonical_state_bytes(
            fold(events, INITIAL)
        ), record.offset


def test_cli_pack_mismatch_loud_nothing_written(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    lines = log.read_text().splitlines()
    header = json.loads(lines[0])
    header["pack"] = "other_pack@9.9"
    forged = tmp_path / "forged.jsonl"
    forged.write_text(json.dumps(header) + "\n" + "\n".join(lines[1:]) + "\n")
    out = tmp_path / "out"
    rc = checkpoint_cli.main([str(forged), "--out", str(out)])
    assert rc == 1
    assert not out.exists()


def test_cli_malformed_log_loud_nothing_written(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    lines = log.read_text().splitlines()
    lines.insert(5, '{"id": "ev_0099", "t": 99, "typ')
    broken = tmp_path / "broken.jsonl"
    broken.write_text("\n".join(lines) + "\n")
    out = tmp_path / "out"
    rc = checkpoint_cli.main([str(broken), "--out", str(out)])
    assert rc == 1
    assert not out.exists()


def test_cli_explicit_offsets_and_prefix_records(tmp_path: Path) -> None:
    log = _run_day1(123, tmp_path)
    out = tmp_path / "out"
    rc = checkpoint_cli.main([str(log), "--offsets", "0,7,55", "--out", str(out)])
    assert rc == 0
    index = read_index(out)
    assert [r.offset for r in index.records] == [0, 7, 55]
    # each record's prefix digest is the log's own line-prefix digest
    for record in index.records:
        assert record.prefix_sha256 == prefix_digest(log, record.offset)
    # the anchor is the artifact's bytes
    for record in index.records:
        data = checkpoint_path(out, record.offset).read_bytes()
        assert record.snapshot_sha256 == hashlib.sha256(data).hexdigest()
