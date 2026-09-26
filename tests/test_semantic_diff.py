"""iter-251 (ssi-7/Phase 6, D-229) — the semantic diff layer's claim
packet (`scripts/semantic_diff.py`, TEST_PLAN §1.4's instrument).

The laws this suite pins (the topology.py/test_topology.py instrument+pin
precedent):

(1) THE LAYER ADDS, NEVER REPLACES — T1's env-pinning (TEST_PLAN §1.1,
    the documented decision) stays the law; the semantic layer is the
    ADDITIONAL cross-environment oracle. The companion arm: a fresh
    run of the golden script is SEMANTICALLY EQUAL to the committed
    golden fixture — the property T1's byte-compare can only check on
    the generating interpreter, checked here at the semantic level.

(2) INDEPENDENCE — the environmental axes the layer must IGNORE by
    design: line endings (CRLF/CR/LF), the header's `python`
    (the generating interpreter), the header's `commit` (the code
    provenance). Each ignored axis stays EQUAL; the report NAMES what
    it ignored (no silent skip, N006).

(3) THE TEETH — every semantic axis the layer must catch: the header's
    semantic fields (schema_version/seed/pack), each enumerated event
    anchor (id/t/type/actor/target/cause), deep field paths
    (outcome.duration), the bool-vs-number kind distinction, stream
    length (a dropped tail event, reported as the append-only prefix
    relation), and the RNG fingerprint (the latent-divergence axis:
    equal events + unequal draw counts = already divergent, RNG-1).
    A checker that cannot fail is decoration (TEST_PLAN §1.3's teeth
    law).

(4) LOUD INPUTS — a missing file, a half-pair of fingerprint flags:
    exit 2 with the reason, never a silent skip.

The instrument itself imports NOTHING from core/ (the independent
re-derivation law, TEST_PLAN §9); this suite imports only the tool.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import semantic_diff  # type: ignore[import-not-found]  # noqa: E402

from core.loop import Simulator, load_playscript  # noqa: E402
from core.pack import load_pack  # noqa: E402

GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")


def _run(tmp_path: Path, name: str) -> tuple[Path, int]:
    """One fresh golden-script run (the T1 helper's shape): the log
    path + the run's RngBank fingerprint."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    sim = Simulator(pack, SCRIPT["seed"], tmp_path / name, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    return tmp_path / name, result.fingerprint


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _write(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _mutate_header(tmp_path: Path, name: str, **changes: object) -> Path:
    lines = _lines(GOLDEN)
    header = json.loads(lines[0])
    header.update(changes)
    return _write(tmp_path / name, [json.dumps(header)] + lines[1:])


def _mutate_event(
    tmp_path: Path, name: str, index: int, **changes: object
) -> Path:
    lines = _lines(GOLDEN)
    events = [json.loads(line) for line in lines[1:]]
    events[index].update(changes)
    return _write(
        tmp_path / name, [lines[0]] + [json.dumps(e) for e in events]
    )


def _drop_tail(tmp_path: Path, name: str, count: int = 1) -> Path:
    lines = _lines(GOLDEN)
    return _write(tmp_path / name, lines[:-count])


# -- (1) the companion arm: the layer ADDS over T1 -----------------------


def test_fresh_run_is_semantically_equal_to_the_committed_golden(
    tmp_path: Path,
) -> None:
    """The phase's headline property: where T1's byte-compare is
    env-pinned (§1.1), the semantic layer proves run↔golden equality at
    the parsed level — the same claim, portable across interpreters."""
    fresh, _ = _run(tmp_path, "fresh.jsonl")
    diff = semantic_diff.compare(GOLDEN, fresh)
    assert diff.equal
    assert "SEMANTICALLY EQUAL" in semantic_diff.format_report(diff)


def test_two_fresh_runs_semantically_equal_with_fingerprints(
    tmp_path: Path,
) -> None:
    """The full oracle over two real runs: equal event streams AND
    equal RngBank fingerprints (the RNG-1 axis joins the verdict only
    when supplied — the run-side pair)."""
    left, fp_l = _run(tmp_path, "a.jsonl")
    right, fp_r = _run(tmp_path, "b.jsonl")
    diff = semantic_diff.compare(
        left, right, fingerprint_left=fp_l, fingerprint_right=fp_r
    )
    assert diff.equal
    assert diff.fingerprints_compared
    assert not diff.fingerprint_delta


# -- (2) the independence arms (GREEN, with the ignored axes named) ------


def test_identical_logs_are_semantically_equal() -> None:
    diff = semantic_diff.compare(GOLDEN, GOLDEN)
    assert diff.equal
    assert semantic_diff.main([str(GOLDEN), str(GOLDEN)]) == 0


def test_line_endings_are_environmental(tmp_path: Path) -> None:
    """CRLF against LF: the same run, different transport — EQUAL."""
    crlf = tmp_path / "golden_crlf.jsonl"
    crlf.write_bytes(GOLDEN.read_bytes().replace(b"\n", b"\r\n"))
    diff = semantic_diff.compare(GOLDEN, crlf)
    assert diff.equal


def test_interpreter_version_is_environmental(tmp_path: Path) -> None:
    """The header's `python` field differs: the report NAMES the ignored
    difference, the verdict stays EQUAL (§1.1's pin is the
    environmental layer, by design)."""
    other = _mutate_header(tmp_path, "py311.jsonl", python="3.11.8")
    diff = semantic_diff.compare(GOLDEN, other)
    assert diff.equal
    report = semantic_diff.format_report(diff)
    assert "python '3.12.14' != '3.11.8'" in report
    assert "ignored by design" in report


def test_commit_is_provenance_not_semantic(tmp_path: Path) -> None:
    other = _mutate_header(tmp_path, "commit.jsonl", commit="deadbeef")
    diff = semantic_diff.compare(GOLDEN, other)
    assert diff.equal


# -- (3) the teeth: every semantic axis goes RED -------------------------


def test_seed_delta_is_semantic(tmp_path: Path) -> None:
    other = _mutate_header(tmp_path, "seed43.jsonl", seed=43)
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert diff.header_semantic == (("seed", 42, 43),)
    assert semantic_diff.main([str(GOLDEN), str(other)]) == 1


def test_schema_version_delta_is_semantic(tmp_path: Path) -> None:
    other = _mutate_header(tmp_path, "schema03.jsonl", schema_version="0.3")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert diff.header_semantic[0][0] == "schema_version"


def test_pack_delta_is_semantic(tmp_path: Path) -> None:
    other = _mutate_header(tmp_path, "pack.jsonl", pack="other@9.9")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert diff.header_semantic[0][0] == "pack"


def test_event_type_mutation_is_a_named_delta(tmp_path: Path) -> None:
    other = _mutate_event(tmp_path, "type.jsonl", 5, type="move_failed")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert diff.event_deltas[0].index == 5
    assert ("type", "move", "move_failed") in diff.event_deltas[0].anchors
    assert "event.type: 'move' != 'move_failed'" in semantic_diff.format_report(diff)


def test_event_actor_mutation_is_a_named_delta(tmp_path: Path) -> None:
    other = _mutate_event(tmp_path, "actor.jsonl", 5, actor="npc_guard_01")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert ("actor", "pc_01", "npc_guard_01") in diff.event_deltas[0].anchors


def test_event_target_mutation_is_a_named_delta(tmp_path: Path) -> None:
    other = _mutate_event(tmp_path, "target.jsonl", 10, target="loc_tavern")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert ("target", "loc_market", "loc_tavern") in diff.event_deltas[0].anchors


def test_event_cause_mutation_is_a_named_delta(tmp_path: Path) -> None:
    other = _mutate_event(tmp_path, "cause.jsonl", 10, cause="ev_0008")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert ("cause", "ev_0009", "ev_0008") in diff.event_deltas[0].anchors


def test_event_id_mutation_is_a_named_delta(tmp_path: Path) -> None:
    other = _mutate_event(tmp_path, "id.jsonl", 5, id="ev_9999")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert ("id", "ev_0005", "ev_9999") in diff.event_deltas[0].anchors


def test_deep_field_mutation_is_reported_at_its_path(
    tmp_path: Path,
) -> None:
    """A field the anchors do not cover: the deep walker names the exact
    path (`outcome.duration`), the report carries the id context."""
    events = [json.loads(line) for line in _lines(GOLDEN)[1:]]
    events[10]["outcome"]["duration"] = 9
    other = _write(
        tmp_path / "deep.jsonl",
        [_lines(GOLDEN)[0]] + [json.dumps(e) for e in events],
    )
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    report = semantic_diff.format_report(diff)
    assert "event.outcome.duration: 4 != 9" in report
    assert "id=ev_0010" in report


def test_bool_vs_number_is_a_kind_delta(tmp_path: Path) -> None:
    """`false` against `0`: numerically equal, semantically DIFFERENT
    kinds — the deep equality is type-strict across the bool/number
    boundary (Python's `False == 0` must not launder a kind change)."""
    events = [json.loads(line) for line in _lines(GOLDEN)[1:]]
    events[0]["outcome"]["near_river"] = 0
    other = _write(
        tmp_path / "boolnum.jsonl",
        [_lines(GOLDEN)[0]] + [json.dumps(e) for e in events],
    )
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert "event.outcome.near_river" in semantic_diff.format_report(diff)


def test_dropped_tail_event_is_a_prefix_delta(tmp_path: Path) -> None:
    """A shorter stream that matches everywhere it exists: the report
    names the append-only prefix relation (the log's own law — any
    prefix is a legal assembly state, TEST_PLAN §1.3)."""
    other = _drop_tail(tmp_path, "shorter.jsonl")
    diff = semantic_diff.compare(GOLDEN, other)
    assert not diff.equal
    assert diff.event_count_left == 11
    assert diff.event_count_right == 10
    assert diff.event_deltas[0].side == "left"
    assert diff.prefix_relation
    assert "strict prefix" in semantic_diff.format_report(diff)


def test_unequal_fingerprints_over_equal_events_go_red() -> None:
    """The latent-divergence axis: identical logs, different supplied
    draw counts — ALREADY divergent (the next substantive draw sits at
    a different entropy position even though no event shows it yet)."""
    diff = semantic_diff.compare(
        GOLDEN, GOLDEN, fingerprint_left=4, fingerprint_right=5
    )
    assert not diff.equal
    assert diff.fingerprint_delta
    assert "latent RNG drift" in semantic_diff.format_report(diff)
    assert (
        semantic_diff.main(
            [str(GOLDEN), str(GOLDEN), "--fingerprint-left", "4",
             "--fingerprint-right", "5"]
        )
        == 1
    )


def test_equal_fingerprints_stay_green() -> None:
    diff = semantic_diff.compare(
        GOLDEN, GOLDEN, fingerprint_left=4, fingerprint_right=4
    )
    assert diff.equal
    assert diff.fingerprints_compared


# -- (4) loud inputs (exit 2, never a silent skip) ------------------------


def test_missing_file_is_loud(tmp_path: Path) -> None:
    assert (
        semantic_diff.main([str(GOLDEN), str(tmp_path / "absent.jsonl")]) == 2
    )


def test_half_pair_fingerprint_flags_are_loud() -> None:
    assert (
        semantic_diff.main([str(GOLDEN), str(GOLDEN), "--fingerprint-left", "4"])
        == 2
    )


def test_non_header_first_line_is_loud(tmp_path: Path) -> None:
    bad = _write(tmp_path / "noheader.jsonl", _lines(GOLDEN)[1:])
    with pytest.raises(semantic_diff.DiffInputError):
        semantic_diff.compare(GOLDEN, bad)
