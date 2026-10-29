"""bg-8 acceptance — the deviation corpus (TEST_PLAN §8 Layer 1, source 3:
live transcripts re-distilled; contract owner `docs/TEST_PLAN.md` §8.2/§8.3,
decision D-109).

The F1–F6 families authored to break the boundary's comfort (the owner's
2026-09-07 living-world clarification), driven through the REAL mode-C door
by the bg-8 live runner (the sandbox API engine, glm-4-plus; the runner
outside the repo per Rule 9/INV-4), and re-distilled verbatim into
`tests/fixtures/deviation_corpus.json` — the honest mappings AND the
measured failures (the F3/F4 guessed mappings, the F6 executed injections,
the f6f protocol echo), so Layer 1's scripted repliers are calibrated from
the real loop, never imagined (the anti-tautology law).

The suite pins:

- the **world-answer law** (§8.3) as regression teeth: every world-touching
  utterance ends in exactly one of — a committed event (attempts included:
  `intent_rejected` is a fact), a surfaced disambiguation question, or a
  `no_intent` verdict. A boundary change that turns an answered case silent
  (a drop, a crash, an off-grammar leak feeding the door) FAILS here. The
  first live number: 34/34 coverage at this engine class — the failures
  live in mapping quality, never in answer coverage;
- the door verdicts per cycle (status, event counts, last event types) —
  the guessed/paraphrased/injected replies feed the door LAWFULLY: the
  F3 guesses commit real talk+rumor pairs, the F6 injected steal commits a
  world fact, the F4 closest-verb moves die as `intent_rejected` — the
  reply is data, the boundary answers;
- the leak probe's loudness (f6f): the protocol-echo replies raise
  ParseError at the gate, the cycle stays open, the world NEVER moves —
  the measured failure class pinned verbatim;
- the family-verdict census: every cycle's honest-outcome class comes from
  the closed vocabulary, and the totals match the live run's numbers
  (the fixture is the single owner, D-024).
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
DEVIATION = json.loads(
    (REPO / "tests" / "fixtures" / "deviation_corpus.json").read_text(
        encoding="utf-8")
)

#: The honest-outcome vocabulary (the metric definitions' semantic side,
#: TEST_PLAN §8.2): the honest classes and the measured-failure classes
#: the live run named. Closed by D-109; grows only with a measured shape.
_HONEST = {"mapped", "question", "no_intent"}
_FAILURES = {
    "missed", "guess", "closest_verb", "confabulated",
    "injection_executed", "surface_lost", "echo_leak", "leak_unanswered",
}
_ANSWERS = {"event", "question", "no_intent", "unanswered"}


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
    "case", DEVIATION["cases"], ids=lambda case: case["name"]
)
def test_deviation_corpus_world_answer_regression(
    case: dict[str, Any], tmp_path: Path
) -> None:
    """One family's live session replayed through the REAL mode-C stack
    (the runner's exact geometry: seed, setup, replies verbatim). Pins the
    door verdicts, the per-cycle world-answer kind, the leak probe's
    loudness, and the family's answer tally — the live run's number."""
    run = tmp_path / case["name"]
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
            # the leak probe: no valid reply ever arrived; the cycle stays
            # OPEN and the world NEVER moved — the honest measured failure
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
    # the family's answer tally: the live run's number, re-derived
    expected = {
        key: value for key, value in case["answers"].items()
        if key in _ANSWERS
    }
    assert tally == expected
    # the deviation corpus never establishes texture: no narrator half, no
    # live entries — the player's words alone mint nothing (blueprint §1)
    assert mediator.ledger.entries == ()


def test_deviation_totals_match_the_live_run() -> None:
    """The corpus's single owner is the fixture; the census re-derives the
    live run's headline numbers from the per-cycle pins (D-024: no second
    place to go stale)."""
    totals: dict[str, int] = {}
    honest = 0
    verdicts: set[str] = set()
    for case in DEVIATION["cases"]:
        for cycle in case["cycles"]:
            verdicts.add(cycle["family_verdict"])
            if cycle["family_verdict"] in _HONEST:
                honest += 1
            answer = cycle["answer"]
            totals[answer] = totals.get(answer, 0) + 1
            assert cycle["answer"] in _ANSWERS
            assert isinstance(cycle["world_touching"], bool)
    assert verdicts <= _HONEST | _FAILURES  # the closed vocabulary
    assert totals["event"] == DEVIATION["totals"]["event"]
    assert totals["question"] == DEVIATION["totals"]["question"]
    assert totals["no_intent"] == DEVIATION["totals"]["no_intent"]
    assert totals["unanswered"] == DEVIATION["totals"]["unanswered"]
    assert honest == DEVIATION["totals"]["honest"]
    # the world-answer law's first live number: every world-touching probe
    # answered (34/34) — the one unanswered cycle is the non-world-touching
    # leak probe f6f
    world_touching = sum(
        1 for case in DEVIATION["cases"] for cycle in case["cycles"]
        if cycle["world_touching"]
    )
    answered = sum(
        1 for case in DEVIATION["cases"] for cycle in case["cycles"]
        if cycle["world_touching"] and cycle["answer"] != "unanswered"
    )
    assert world_touching == DEVIATION["totals"]["world_touching"]
    assert answered == world_touching  # 34/34 coverage, pinned


def test_the_injected_replies_are_data_not_instructions(
    tmp_path: Path,
) -> None:
    """F6's worst case replayed in isolation: the injection-compliant reply
    (the engine executed the payload — a gate-valid steal) feeds the door
    LAWFULLY: the gate checks it, the world answers with a fact, nothing
    crashes, and the payload never reaches any instruction channel (the
    boundary's own state never depends on the reply's prose). The
    protocol-echo probe stays off-grammar — loud, never a feed."""
    case = next(c for c in DEVIATION["cases"] if c["family"] == "F6")
    run = tmp_path / "f6"
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    door = ParserDoor(sim, PACK, SCHEMA, log, mediator.ledger, run / "parser")
    injected = [c for c in case["cycles"]
                if c["family_verdict"] == "injection_executed"]
    assert len(injected) == 2  # f6a and f6c, the measured executions
    for cycle in injected:
        door.emit_call(cycle["say"])
        reply = run / "reply.json"
        reply.write_text(json.dumps(cycle["reply"]), encoding="utf-8")
        result = door.apply_reply(reply)
        assert result.status == "intent" and result.events == 1
        # the world answered the injected intent as a FACT (an attempt —
        # never an instruction-side effect): f6a's item-target steal dies
        # as intent_rejected, f6c's guard steal commits the attempt
        assert _events(log)[-1].type in ("intent_rejected", "steal")
