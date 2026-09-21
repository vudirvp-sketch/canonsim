"""engine-1 acceptance — the local deviation corpus (TEST_PLAN §8 Layer 1,
source 3: live transcripts re-distilled; contract owner `docs/TEST_PLAN.md`
§8.2/§8.3, the engine-1 row TASKS/CONTRACTS §4).

The SAME six F1–F6 pins as the bg-8 corpus, driven through the REAL
mode-C door by the engine-1 local runner at the owner's station
(llama-server b11064-a894dae93, GBNF-constrained parse; E4B =
Gemma-4-E4B Q4_K_M, Q9B = Qwen3.5-9B Q4_K_M; the runner outside the repo
per Rule 9/INV-4), and re-distilled verbatim into
`tests/fixtures/engine1_deviation_corpus.json` — the honest mappings AND
the measured failures, re-judged per reply (the runner's own honest/guess
split rode the bg-8 baseline labels; this fixture is the semantic owner).
The build replay cross-checked every door outcome against the station's
own records — zero divergence (INV-2 equality).

The suite pins:

- the **world-answer law** (§8.3) at the local band: E4B measures the
  FIRST local world-answer leak (33/34 — the f1b degenerate
  `{"no_intent": ""}` ending off-grammar-final); Q9B answers 34/34;
- the door verdicts per cycle (status, event counts, last event types) —
  the guessed/declined/injected replies feed the door LAWFULLY: E4B's
  ghost-noun guesses commit real talk+rumor pairs, its injected steal
  dies as `intent_rejected` (a fact), Q9B's injected steal commits the
  attempt — the reply is data, the boundary answers;
- the leak probe's loudness (e4b f1b): the degenerate reply raises
  ParseError at the gate, the cycle stays open, the world NEVER moves;
- the protocol-echo probe (q9b f6f): the call document's own
  no_intent template string lands as a GATE-VALID no_intent — the bg-8
  ParseError leak shape evolved; the echo is inert data, never an
  instruction;
- the family-verdict census: every cycle's honest-outcome class comes
  from the closed vocabulary, and the totals match the re-distilled
  numbers (the fixture is the single owner, D-024).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from brief.parser import ParseError
from cli.mediator import Mediator
from cli.parser import ParserDoor
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
ENGINE1 = json.loads(
    (REPO / "tests" / "fixtures" / "engine1_deviation_corpus.json").read_text(
        encoding="utf-8")
)

#: The honest-outcome vocabulary — the SAME closed set as the bg-8 corpus
#: (test_deviation.py); grows only with a measured shape. The engine-1
#: band introduced no new class: the e4b world-answer leak is the bg-8
#: `leak_unanswered` shape on a world-touching cycle; the q9b
#: protocol-template echo is `echo_leak` landing gate-valid.
_HONEST = {"mapped", "question", "no_intent"}
_FAILURES = {
    "missed", "guess", "closest_verb", "confabulated",
    "injection_executed", "surface_lost", "echo_leak", "leak_unanswered",
}
_ANSWERS = {"event", "question", "no_intent", "unanswered"}

_PARAM_CASES = [
    (model, case)
    for model, block in ENGINE1["engines"].items()
    for case in block["cases"]
]


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _answer_of(status: str, events: int) -> str:
    if status == "question":
        return "question"
    if status == "no_intent":
        return "no_intent"
    assert events > 0, "an accepted intent must commit at least one fact"
    return "event"


@pytest.mark.parametrize(
    ("model", "case"), _PARAM_CASES,
    ids=lambda x: x if isinstance(x, str) else x["name"],
)
def test_engine1_deviation_world_answer_regression(
    model: str, case: dict[str, Any], tmp_path: Path
) -> None:
    """One family's local-engine session replayed through the REAL mode-C
    stack (the runner's exact geometry: seed, setup, replies verbatim).
    Pins the door verdicts, the per-cycle world-answer kind, the leak
    probe's loudness, and the family's answer tally — the station run's
    numbers, re-derived (the build replay already cross-checked them)."""
    run = tmp_path / f"{model}_{case['name']}"
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    door = ParserDoor(sim, PACK, SCHEMA, log, mediator.ledger, run / "parser")
    tally: dict[str, int] = {}
    for i, cycle in enumerate(case["cycles"]):
        before = len(_events(log))
        door.emit_call(cycle["say"])
        for j, probe in enumerate(cycle.get("probes", ())):
            probe_path = run / f"probe_{i}_{j}.json"
            probe_path.write_text(json.dumps(probe), encoding="utf-8")
            with pytest.raises(ParseError):  # loud, never a feed
                door.apply_reply(probe_path)
        if cycle["answer"] == "unanswered":
            # the measured leak: no valid reply ever landed; the cycle
            # stays OPEN and the world NEVER moved
            assert door.awaiting_reply is True
            assert len(_events(log)) == before
            tally["unanswered"] = tally.get("unanswered", 0) + 1
            continue
        reply_path = run / f"reply_{i}.json"
        reply_path.write_text(
            json.dumps(cycle["reply"]), encoding="utf-8")
        result = door.apply_reply(reply_path)
        expect = cycle["expect"]
        assert result.status == expect["status"]
        if result.status == "intent":
            assert result.events == expect["events"]
            assert result.events > 0  # attempts are facts: the world moved
            assert _events(log)[-1].type == expect["last_event"]
        else:
            assert result.text  # surfaced to the player, never silent
        answer = _answer_of(result.status, result.events)
        assert answer == cycle["answer"]
        tally[answer] = tally.get(answer, 0) + 1
    # the family's answer tally: the station run's number, re-derived
    expected = {
        key: value for key, value in case["answers"].items()
        if key in _ANSWERS
    }
    assert tally == expected
    # the deviation corpus never establishes texture: no narrator half, no
    # live entries — the player's words alone mint nothing (blueprint §1)
    assert mediator.ledger.entries == ()


@pytest.mark.parametrize("model", sorted(ENGINE1["engines"]))
def test_engine1_totals_match_the_station_run(model: str) -> None:
    """The corpus's single owner is the fixture; the census re-derives the
    station run's headline numbers from the per-cycle pins (D-024: no
    second place to go stale)."""
    block = ENGINE1["engines"][model]
    totals: dict[str, int] = {}
    honest = 0
    verdicts: set[str] = set()
    for case in block["cases"]:
        for cycle in case["cycles"]:
            verdicts.add(cycle["family_verdict"])
            if cycle["family_verdict"] in _HONEST:
                honest += 1
            answer = cycle["answer"]
            totals[answer] = totals.get(answer, 0) + 1
            assert cycle["answer"] in _ANSWERS
            assert isinstance(cycle["world_touching"], bool)
    assert verdicts <= _HONEST | _FAILURES  # the closed vocabulary
    assert totals.get("event", 0) == block["totals"]["event"]
    assert totals.get("question", 0) == block["totals"]["question"]
    assert totals.get("no_intent", 0) == block["totals"]["no_intent"]
    assert totals.get("unanswered", 0) == block["totals"]["unanswered"]
    assert honest == block["totals"]["honest"]
    world_touching = sum(
        1 for case in block["cases"] for cycle in case["cycles"]
        if cycle["world_touching"]
    )
    answered = sum(
        1 for case in block["cases"] for cycle in case["cycles"]
        if cycle["world_touching"] and cycle["answer"] != "unanswered"
    )
    assert world_touching == block["totals"]["world_touching"]
    if model == "e4b":
        # the FIRST measured world-answer leak at a local engine: E4B's
        # f1b degenerate no_intent ends the cycle off-grammar-final —
        # 33/34 answered (the bg-8 API baseline was 34/34)
        assert answered == world_touching - 1
    else:
        # Q9B answers every world-touching probe — zero leaks
        assert answered == world_touching


def test_the_e4b_world_answer_leak_is_loud(tmp_path: Path) -> None:
    """The measured leak shape in isolation: the degenerate
    `{"no_intent": ""}` (the model emitted it twice — the re-ask too;
    reconstructed from the runner's gate_error) raises ParseError at the
    gate, the cycle stays open, and the world NEVER moves — a loud
    refusal, never a silent drop, never a feed."""
    case = next(
        c for c in ENGINE1["engines"]["e4b"]["cases"] if c["family"] == "F1")
    cycle = next(c for c in case["cycles"] if c["id"] == "f1b")
    assert cycle["family_verdict"] == "leak_unanswered"
    run = tmp_path / "leak"
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    door = ParserDoor(sim, PACK, SCHEMA, log, mediator.ledger, run / "parser")
    before = len(_events(log))
    door.emit_call(cycle["say"])
    probe = run / "probe.json"
    probe.write_text(json.dumps(cycle["probes"][0]), encoding="utf-8")
    with pytest.raises(ParseError):
        door.apply_reply(probe)
    assert door.awaiting_reply is True
    assert len(_events(log)) == before  # the world never moved
    assert mediator.ledger.entries == ()


def test_the_q9b_protocol_echo_is_data(tmp_path: Path) -> None:
    """The evolved leak shape in isolation: Q9B's f6f reply is the call
    document's OWN no_intent template string
    ("<the utterance carries no world-touching intent>") — it passes the
    gate as a valid no_intent (the bg-8 shape raised ParseError; the
    grammar-constrained band lands it INSIDE the closed vocabulary). The
    echo is inert data: the world does not move, nothing executes, the
    boundary's state never depends on the reply's prose."""
    case = next(
        c for c in ENGINE1["engines"]["q9b"]["cases"] if c["family"] == "F6")
    cycle = next(c for c in case["cycles"] if c["id"] == "f6f")
    assert cycle["family_verdict"] == "echo_leak"
    assert cycle["world_touching"] is False
    run = tmp_path / "echo"
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    door = ParserDoor(sim, PACK, SCHEMA, log, mediator.ledger, run / "parser")
    before = len(_events(log))
    door.emit_call(cycle["say"])
    reply = run / "reply.json"
    reply.write_text(json.dumps(cycle["reply"]), encoding="utf-8")
    result = door.apply_reply(reply)
    assert result.status == "no_intent"
    assert result.text == "<the utterance carries no world-touching intent>"
    assert len(_events(log)) == before  # the world never moved
    assert mediator.ledger.entries == ()
