"""iter-31 acceptance — the phase-2 parser boundary, mode C
(`brief/parser.py` the pure document layer + `cli/parser.py` the session
door; contract owner `docs/PARSER_SPEC.md`, decision D-062; architecture
owner `docs/blueprint/phases.md` §2).

The parser is EXTERNAL (D-055's pattern applied to the player's free
text): replies arrive as JSON documents, the repo stays LLM-free (INV-4 —
no network, no inference, no runtime dependency landed with this
boundary). The suite pins: the grammar snapshot's closed vocabulary (the
pack's verbs with their derived field constraints plus the addressable
nouns — canon entities and live texture entries; ghost interactivity is
structurally impossible), the call document's bytes (utterance + grammar
+ protocol, pure in (log, ledger, pack)), the reply document's closed
shape gate (off-grammar output is loud and never feeds — the world never
moves on a malformed parse), the pin law (a parsed intent's texture
reference pins its entry; the reference IS the pin, a failed attempt
keeps it live+pinned, a success promotes it — seed-probed like the
narrator-path promotion test), and the door wiring e2e through the real
front door (emit → reply → feed, promotions wired exactly like the
narrator path, attempts are facts).

iter-32 (parse-1 validation beats) adds the phase-2 regression set: the
parse-reply corpus (`fixtures/parse_replies.json`, the narrator-beats
fixture's family) replayed through the REAL session stack — Simulator +
Mediator + ParserDoor over ONE shared ledger (D-049): every off-grammar
probe family caught loudly, both door outcomes, the pin law's live
paths, the fire cascade inside the door's own batch, and the honest
question/no-intent surfaces (the ≥90% evidence, PARSER_SPEC §6).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from brief.ledger import (
    ACTIVE,
    CONTRADICTED,
    PINNED,
    PROMOTED,
    RETIRED,
    SceneLedger,
)
from brief.parser import (
    ParseError,
    grammar_snapshot,
    parse_call,
    parse_reply_from_mapping,
)
from cli.main import main
from cli.mediator import Mediator
from cli.parser import ParserDoor
from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import RunnerError, Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PLAYER = PACK.player_id()

_CANDLES = {
    "scope": "scene:loc_tavern", "slot": "candles", "value": "lit",
    "surface": "A few candles still burned on the tables.",
}
_CANDLES_REF = {
    "entry": "tex_0000", "scope": "scene:loc_tavern",
    "slot": "candles", "value": "lit",
}


def _session(
    tmp_path: Path, seed: int = 42, steps: tuple[dict[str, Any], ...] = ()
) -> tuple[Simulator, SceneLedger, Path]:
    """One opened Simulator plus a ledger, the player inside the main room
    (scene-scoped texture establishes legally there)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}, *steps])
    return sim, SceneLedger(), log


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _establish(ledger: SceneLedger, events: list[Any]) -> None:
    """Narrator-side texture establishment (one scene-scoped entry)."""
    ledger.apply_delta(
        {"source": "turn:1", "established": [_CANDLES]}, events, PACK
    )


# -- the grammar snapshot --------------------------------------------------------


def test_snapshot_verb_grammar_is_derived_from_pack_data(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    snapshot = grammar_snapshot(_events(log), PACK, ledger)
    assert [verb.intent for verb in snapshot.verbs] == [
        action["intent"] for action in PACK.data["actions.json"]["actions"]
    ]
    verbs = {verb.intent: verb for verb in snapshot.verbs}
    wait = verbs["wait"]
    assert wait.fields[0].name == "ticks" and wait.fields[0].positive_int
    assert not wait.target_required and not wait.fields[0].values
    steal = verbs["steal"]
    assert steal.target_required
    assert steal.fields[0].name == "method"
    assert steal.fields[0].values == tuple(PACK.rules["checks"]["methods"])
    take = verbs["take"]
    assert take.fields[0].name == "texture" and take.fields[0].texture
    drop = verbs["drop_break"]
    assert drop.fields[0].name == "near"
    # the player stands in the main room: the ignition layer's spots there
    assert drop.fields[0].values == tuple(PACK.entity("loc_tavern")["fire_spots"])


def test_snapshot_near_enum_tracks_the_actor_position(tmp_path: Path) -> None:
    sim, ledger, log = _session(
        tmp_path, steps=({"intent": "move", "target": "loc_street"},)
    )
    snapshot = grammar_snapshot(_events(log), PACK, ledger)
    drop = {verb.intent: verb for verb in snapshot.verbs}["drop_break"]
    assert drop.fields[0].values == ()  # no spots out on the street


def test_snapshot_nouns_are_entities_plus_live_texture(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    bare = grammar_snapshot(events, PACK, SceneLedger())
    ids = {noun.id for noun in bare.nouns}
    assert len(bare.nouns) == 17  # 5 locations + 6 npcs + 1 ambient + 5 items
    assert {"loc_tavern", "npc_guard_01", "purse_01", "npc_market_crowd_01"} <= ids
    assert all(noun.texture is None for noun in bare.nouns)

    _establish(ledger, events)
    snapshot = grammar_snapshot(events, PACK, ledger)
    texture = [noun for noun in snapshot.nouns if noun.texture is not None]
    assert len(texture) == 1
    assert texture[0].id == "tex_0000" and texture[0].kind == "texture"
    assert texture[0].texture == _CANDLES_REF
    assert texture[0].name == _CANDLES["surface"]


def test_snapshot_is_deterministic(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    other = SceneLedger()
    _establish(other, events)
    assert grammar_snapshot(events, PACK, ledger) == grammar_snapshot(
        events, PACK, other
    )


# -- the call document (PARSER_SPEC §3) ------------------------------------------


def test_call_document_carries_utterance_grammar_and_protocol(
    tmp_path: Path,
) -> None:
    sim, ledger, log = _session(tmp_path)
    document = parse_call("lift the purse", _events(log), PACK, ledger)
    assert document.startswith("## player_input\nlift the purse\n")
    assert "## grammar" in document and "## parse_protocol" in document
    assert 'steal "steal" [target required] method=one of: distraction' in document
    assert 'wait "wait" ticks=<positive integer>' in document
    assert 'take "take" [target required] texture=<a live texture entry>' in document
    assert "npc_guard_01 (npc)" in document
    assert "texture entries:" not in document  # nothing live yet
    assert '{"intent"' in document and '{"question"' in document


def test_call_document_lists_live_texture_entries(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    document = parse_call("snuff the candles", events, PACK, ledger)
    assert "texture entries:" in document
    assert (
        "tex_0000 scene:loc_tavern candles=lit "
        f"\"{_CANDLES['surface']}\"" in document
    )


def test_call_document_bytes_are_deterministic(tmp_path: Path) -> None:
    sim_a, ledger_a, log_a = _session(tmp_path / "a")
    sim_b, ledger_b, log_b = _session(tmp_path / "b")
    for ledger, log in ((ledger_a, log_a), (ledger_b, log_b)):
        _establish(ledger, _events(log))
    doc_a = parse_call("same words", _events(log_a), PACK, ledger_a)
    doc_b = parse_call("same words", _events(log_b), PACK, ledger_b)
    assert doc_a == doc_b


# -- the reply document gate (PARSER_SPEC §4) ------------------------------------


def test_gate_accepts_the_three_alternatives(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    snapshot = grammar_snapshot(events, PACK, ledger)
    intent = parse_reply_from_mapping(
        {"intent": {"kind": "steal", "target": "npc_guard_01",
                    "fields": {"method": "distraction"}}},
        snapshot,
    )
    assert intent.intent is not None
    assert intent.intent.target == "npc_guard_01"
    assert intent.intent.fields == {"method": "distraction"}
    assert intent.question is None and intent.no_intent is None

    question = parse_reply_from_mapping({"question": "take which item?"}, snapshot)
    assert question.question == "take which item?"

    none = parse_reply_from_mapping({"no_intent": "just musing"}, snapshot)
    assert none.no_intent == "just musing"


def test_gate_rejects_malformed_documents(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    snapshot = grammar_snapshot(events, PACK, ledger)
    bad_documents = [
        "not an object",
        {},
        {"intent": {}, "question": "x"},          # two alternatives
        {"intent": {}, "bogus": 1},               # unknown key
        {"intent": "steal"},                      # not an object
        {"intent": {}},                           # missing kind
        {"intent": {"kind": "fly"}},              # off-grammar verb
        {"intent": {"kind": "steal", "target": "npc_ghost_01"}},  # ghost noun
        {"intent": {"kind": "steal", "fields": {"method": "vanish"}}},
        {"intent": {"kind": "steal", "fields": {"surprise": 1}}},
        {"intent": {"kind": "wait", "fields": {"ticks": 0}}},
        {"intent": {"kind": "wait", "fields": {"ticks": "5"}}},
        {"intent": {"kind": "wait", "fields": {"ticks": True}}},
        {"question": ""},                          # empty alternative
        {"no_intent": "   "},
    ]
    for doc in bad_documents:
        with pytest.raises(ParseError):
            parse_reply_from_mapping(doc, snapshot)


def test_gate_texture_reference_must_be_live_and_verbatim(
    tmp_path: Path,
) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    snapshot = grammar_snapshot(events, PACK, ledger)
    fabricated = [
        "candles",
        {"entry": "tex_0000"},                       # missing keys
        {"entry": "tex_0000", "scope": "scene:loc_tavern",
         "slot": "candles", "value": "snuffed"},     # wrong value
        {"entry": "tex_9999", "scope": "scene:loc_tavern",
         "slot": "candles", "value": "lit"},         # not live
        {"entry": "tex_0000", "scope": "scene:loc_tavern",
         "slot": "candles", "value": "lit", "surface": "x"},  # extra key
    ]
    for value in fabricated:
        with pytest.raises(ParseError):
            parse_reply_from_mapping(
                {"intent": {"kind": "take", "fields": {"texture": value}}},
                snapshot,
            )
    good = parse_reply_from_mapping(
        {"intent": {"kind": "take", "fields": {"texture": dict(_CANDLES_REF)}}},
        snapshot,
    )
    assert good.intent is not None and good.intent.target is None


def test_gate_texture_field_only_on_texture_capable_verbs(
    tmp_path: Path,
) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    snapshot = grammar_snapshot(events, PACK, ledger)
    with pytest.raises(ParseError):  # the verb declares no texture field
        parse_reply_from_mapping(
            {"intent": {"kind": "examine", "target": "purse_01",
                        "fields": {"texture": dict(_CANDLES_REF)}}},
            snapshot,
        )


# -- the pin law (SceneLedger.pin — blueprint §1(a)) -----------------------------


def test_pin_flips_active_to_pinned_and_is_idempotent(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    _establish(ledger, _events(log))
    assert ledger.pin("tex_0000") is True
    assert ledger.live()[0].status == PINNED
    assert ledger.pin("tex_0000") is True  # idempotent
    assert ledger.live()[0].status == PINNED


def test_pin_refuses_non_live_and_unknown_entries(tmp_path: Path) -> None:
    sim, ledger, log = _session(tmp_path)
    events = _events(log)
    _establish(ledger, events)
    ledger.apply_delta(
        {"source": "turn:2", "retired": [{"id": "tex_0000"}]}, events, PACK
    )
    assert ledger.pin("tex_0000") is False  # retired: withdraw, never pin
    assert ledger.pin("tex_9999") is False


# -- the session door e2e (the real front door) ----------------------------------


def _door(
    tmp_path: Path, seed: int = 42, steps: tuple[dict[str, Any], ...] = ()
) -> ParserDoor:
    sim, ledger, log = _session(tmp_path, seed=seed, steps=steps)
    return ParserDoor(sim, PACK, SCHEMA, log, ledger, tmp_path / "parser")


def _reply_file(tmp_path: Path, doc: dict[str, Any]) -> Path:
    path = tmp_path / "reply.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def test_emit_then_apply_feeds_the_front_door(tmp_path: Path) -> None:
    door = _door(tmp_path)
    before = len(_events(door._log_path))
    path = door.emit_call("lift the purse quietly")
    assert path.exists() and "## player_input" in path.read_text("utf-8")
    assert door.awaiting_reply is True
    result = door.apply_reply(_reply_file(tmp_path, {
        "intent": {"kind": "steal", "target": "npc_guard_01",
                   "fields": {"method": "distraction"}},
    }))
    assert result.status == "intent" and result.events > 0
    assert result.step == {"intent": "steal", "target": "npc_guard_01",
                           "method": "distraction"}
    assert len(_events(door._log_path)) > before
    assert door.awaiting_reply is False


def test_apply_without_a_call_is_an_error_not_a_crash(tmp_path: Path) -> None:
    door = _door(tmp_path)
    with pytest.raises(ParseError):
        door.apply_reply(_reply_file(tmp_path, {"question": "what?"}))


def test_question_and_no_intent_never_move_the_world(tmp_path: Path) -> None:
    door = _door(tmp_path)
    before = len(_events(door._log_path))
    door.emit_call("hm, what was that noise")
    result = door.apply_reply(_reply_file(tmp_path, {
        "question": "do you want to look around or wait?"}))
    assert (result.status, result.events, result.text) == (
        "question", 0, "do you want to look around or wait?")
    door.emit_call("I hum a tune to myself")
    result = door.apply_reply(
        _reply_file(tmp_path, {"no_intent": "idle chatter"}))
    assert (result.status, result.events) == ("no_intent", 0)
    assert len(_events(door._log_path)) == before  # nothing fed, ever


def test_malformed_reply_never_feeds_and_the_cycle_stays_open(
    tmp_path: Path,
) -> None:
    door = _door(tmp_path)
    before = len(_events(door._log_path))
    door.emit_call("do something impossible to parse cleanly")
    with pytest.raises(ParseError):
        door.apply_reply(_reply_file(tmp_path, {"intent": {"kind": "fly"}}))
    assert len(_events(door._log_path)) == before  # the world never moved
    assert door.awaiting_reply is True  # the operator may fix the reply file
    result = door.apply_reply(_reply_file(tmp_path, {"no_intent": "recovered"}))
    assert result.status == "no_intent"


def test_world_impossible_attempt_is_a_fact_not_a_crash(tmp_path: Path) -> None:
    door = _door(tmp_path)
    before = len(_events(door._log_path))
    door.emit_call("rob the whole market crowd from here")
    result = door.apply_reply(_reply_file(tmp_path, {
        "intent": {"kind": "steal", "target": "npc_market_crowd_01",
                   "fields": {"method": "distraction"}},
    }))
    assert result.status == "intent" and result.events == 1
    fresh = _events(door._log_path)[before:]
    assert [event.type for event in fresh] == ["intent_rejected"]


def test_texture_reference_pins_and_promotes(tmp_path: Path) -> None:
    door = _door(tmp_path, seed=4)  # probed: the take check passes
    events = _events(door._log_path)
    _establish(door._ledger, events)  # the narrator established the candles
    door.emit_call("pocket one of those candles")
    result = door.apply_reply(_reply_file(tmp_path, {
        "intent": {"kind": "take",
                   "fields": {"texture": dict(_CANDLES_REF)}},
    }))
    assert result.status == "intent"
    assert result.pinned == ("tex_0000",)
    assert result.promoted == ("tex_0000",)  # the committed take IS the promotion
    entry = next(e for e in door._ledger.entries if e.id == "tex_0000")
    assert entry.status == PROMOTED
    state = fold(_events(door._log_path), initial_projection(PACK.entities))
    assert state["loc_tavern"].get("candles") == "lit"  # canon birth


def test_texture_pin_survives_a_failed_attempt(tmp_path: Path) -> None:
    """Seed 42 probed: the take check FAILS — a failed attempt promotes
    nothing; the entry stays live+pinned (the reference IS the pin)."""
    door = _door(tmp_path, seed=42)
    _establish(door._ledger, _events(door._log_path))
    door.emit_call("pocket one of those candles")
    result = door.apply_reply(_reply_file(tmp_path, {
        "intent": {"kind": "take",
                   "fields": {"texture": dict(_CANDLES_REF)}},
    }))
    assert result.status == "intent" and result.pinned == ("tex_0000",)
    assert result.promoted == ()  # a failure promotes nothing
    entry = next(e for e in door._ledger.entries if e.id == "tex_0000")
    assert entry.status == PINNED  # live+pinned, not promoted


def test_texture_pin_survives_a_refused_feed(tmp_path: Path) -> None:
    """The door's one-path law (target AND texture is a loud author error,
    INTENT_SCHEMA §3) fires AFTER the pin: un-pinning does not exist."""
    door = _door(tmp_path)
    _establish(door._ledger, _events(door._log_path))
    door.emit_call("take both the purse and a candle, somehow")
    with pytest.raises(RunnerError):
        door.apply_reply(_reply_file(tmp_path, {
            "intent": {"kind": "take", "target": "purse_01",
                       "fields": {"texture": dict(_CANDLES_REF)}},
        }))
    entry = next(e for e in door._ledger.entries if e.id == "tex_0000")
    assert entry.status == PINNED


def test_the_door_shares_the_sessions_ledger_with_the_narrator(
    tmp_path: Path,
) -> None:
    """One session, one ledger (D-049): texture the narrator-side door
    established is addressable by the player's parse call in the same
    session; the scene close retires it and the noun stops being
    addressable — ghost-free by fold."""
    door = _door(tmp_path)
    _establish(door._ledger, _events(door._log_path))
    snapshot = grammar_snapshot(_events(door._log_path), PACK, door._ledger)
    texture = [noun for noun in snapshot.nouns if noun.texture is not None]
    assert [noun.id for noun in texture] == ["tex_0000"]
    # the canon moves the player: the scene closes, the entry retires
    door._sim.run_steps([{"intent": "move", "target": "loc_street"}])
    door._ledger.sync_scene(_events(door._log_path), PACK)
    assert door._ledger.live() == ()
    assert [e.status for e in door._ledger.entries] == [RETIRED]
    fresh = grammar_snapshot(_events(door._log_path), PACK, door._ledger)
    assert all(noun.texture is None for noun in fresh.nouns)


# -- the CLI session wiring (mode C door) ----------------------------------------


def feed(monkeypatch: pytest.MonkeyPatch, commands: list[str]) -> None:
    answers = iter(commands)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_session_say_emits_and_applies_a_reply(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The `say` door drives one full cycle: the utterance emits the parse
    call (utterance + grammar + protocol), `say apply <reply>` feeds the
    front door and prints the world delta — never a silent drop."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    reply = tmp_path / "parser" / "parse_reply_0000.json"
    reply.parent.mkdir(parents=True)
    reply.write_text(json.dumps({
        "intent": {"kind": "move", "target": "loc_tavern"},
    }), "utf-8")
    feed(monkeypatch, [
        "say walk into the tavern",
        f"say apply {reply}",
        "quit",
    ])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    call = tmp_path / "parser" / "parse_0000.md"
    assert call.exists()
    assert "## player_input\nwalk into the tavern" in call.read_text("utf-8")
    assert "## parse_protocol" in call.read_text("utf-8")
    assert "[parser call:" in out
    assert "[parsed intent fed: move" in out
    assert "Three Barrels tavern" in out  # the scene card after the feed


def test_session_say_apply_without_a_call_is_an_error_not_a_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    reply = tmp_path / "reply.json"
    reply.write_text(json.dumps({"question": "what?"}), "utf-8")
    feed(monkeypatch, [f"say apply {reply}", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    assert "no parse call awaits a reply" in capsys.readouterr().out


def test_session_say_question_surfaces_to_the_player(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    reply = tmp_path / "reply.json"
    reply.write_text(json.dumps({
        "question": "do you want to steal or just look?"}), "utf-8")
    feed(monkeypatch, [
        "say get rich quick",
        f"say apply {reply}",
        "quit",
    ])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "[the parser asks: do you want to steal or just look?]" in out
    assert "[parsed intent fed" not in out


# -- the phase-2 parse regression set (iter-32 validation beats) -----------------

_PARSE_CORPUS = json.loads(
    (REPO / "tests" / "fixtures" / "parse_replies.json").read_text(encoding="utf-8")
)

_LEDGER_STATUSES = {
    "active": ACTIVE, "pinned": PINNED, "retired": RETIRED,
    "contradicted": CONTRADICTED, "promoted": PROMOTED,
}


@pytest.mark.parametrize(
    "case", _PARSE_CORPUS["cases"], ids=lambda case: case["name"]
)
def test_phase2_parse_regression_set(
    case: dict[str, Any], tmp_path: Path
) -> None:
    """The parse-reply corpus: full say-cycle documents distilled from the
    six live iter-32 sessions, replayed through the REAL mode-C session
    stack (Simulator + Mediator + ParserDoor over ONE shared ledger — the
    narrator establishes, the player's words reference, D-049). Pins: every
    off-grammar probe family caught loudly at the boundary (the cycle
    stays open, the fixed reply then applies — off-verb, ghost noun,
    non-integer ticks, off-enum method, two alternatives, the CONSUMED
    texture reference, the double apply), both door outcomes
    (committed events + intent_rejected/take_failed as world answers),
    the pin law's live paths (a failed take keeps live+pinned; a
    committed take IS the promotion — canon birth), the one-path
    RunnerError firing AFTER the pin, the fire cascade draining inside
    the door's own run_steps batch (the iter-23 batch-boundary lesson
    through the say door), and the honest question/no-intent surfaces —
    the phase-2 exit criterion's evidence (ROADMAP §2; PARSER_SPEC §6
    owns the measurement procedure)."""
    run = tmp_path / case["name"]
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    door = ParserDoor(
        sim, PACK, SCHEMA, log, mediator.ledger, run / "parser"
    )
    for i, cycle in enumerate(case["cycles"]):
        if "narrator" in cycle:  # the narrator half: texture on the ledger
            mediator.emit_call()
            reply = run / f"narrator_{i}.json"
            reply.write_text(json.dumps(cycle["narrator"]), encoding="utf-8")
            beat = mediator.apply_reply(reply)
            assert beat.status == "accepted"
            assert any(
                "texture: 1 established" in note for note in beat.notes
            )
            continue
        if "double_apply_probe" in cycle:
            probe = run / "double.json"
            probe.write_text(
                json.dumps(cycle["double_apply_probe"]), encoding="utf-8"
            )
            with pytest.raises(ParseError):  # a consumed call, no second reply
                door.apply_reply(probe)
            continue
        door.emit_call(cycle["say"])
        for probe in cycle.get("probes", ()):
            probe_path = run / f"probe_{i}.json"
            probe_path.write_text(json.dumps(probe), encoding="utf-8")
            with pytest.raises(ParseError):  # loud, never a feed
                door.apply_reply(probe_path)
        reply_path = run / f"reply_{i}.json"
        reply_path.write_text(json.dumps(cycle["reply"]), encoding="utf-8")
        if cycle.get("door_error"):
            with pytest.raises(RunnerError):  # one-path law, after the pin
                door.apply_reply(reply_path)
            continue
        result = door.apply_reply(reply_path)
        expect = cycle["expect"]
        assert result.status == expect["status"]
        if result.status == "intent":
            assert result.events > 0
            if "events" in expect:  # the multi-event door batches (findings)
                assert result.events == expect["events"]
            assert result.pinned == tuple(expect.get("pinned", ()))
            assert result.promoted == tuple(expect.get("promoted", ()))
            assert _events(log)[-1].type == expect["last_event"]
        else:
            assert result.text == expect["text"]
    # case-level: the final ledger and the canon state (canon birth or its
    # absence — the failed take leaves no candles in the world)
    expect = case["expect"]
    by_id = {entry.id: entry for entry in mediator.ledger.entries}
    assert set(by_id) == set(expect["ledger"])
    for entry_id, status in expect["ledger"].items():
        assert by_id[entry_id].status == _LEDGER_STATUSES[status]
    state = fold(_events(log), initial_projection(PACK.entities))
    for entity, props in expect.get("state", {}).items():
        for prop, value in props.items():
            assert state[entity].get(prop) == value
