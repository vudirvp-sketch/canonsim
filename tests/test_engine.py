"""engine-1 acceptance — the adapter contract tests (CONTRACTS §4.3's
test 3, firing at the BUILD; the adapter `cli/engine.py`, iter-177,
D-193; the serializer contract `docs/PRESENTATION_SPEC.md`).

A stub llama-server (stdlib `http.server`, the measured §13/§13.1
surface: `/health`, `/props`, `/v1/chat/completions`) drives every pin
— the tests are INV-4-clean (tests never were the runtime graph; the
network is the loopback stub) and the real backend's own behaviors stay
with the station runs (Layer 2/3, TEST_PLAN §8).

The pins:

- **health/readiness** and the props read (D7's observation boundary);
- **serialization** (§4.3's list, the session-client surface): the
  request bytes are deterministic (the D3 request tier); the GBNF
  grammar rides the parse requests as a TOP-LEVEL param and equals the
  golden grammar fixture over the same snapshot; the narrator requests
  carry NO grammar (unconstrained by design) and split the directives
  block into the system role (BRIEF_SPEC §3.1's note); thinking is off
  on every request (the empty-content trap's recipe); the seed rides
  every request (the seeded-local tier);
- **error mapping** (D1/D7): an HTTP error status is terminal
  ("http"); a malformed body and an empty content are "malformed"
  (once, never retried); a dead endpoint is "unavailable" after the
  tries ladder;
- **the provenance manifest** (§4.3's test 2): the model file's sha256
  from /props, the build, the params, the seed, the first parse call's
  grammar id;
- **the session cycles** (the failure->ladder mapping, D7): the happy
  paths; the off-grammar re-ask (once, the refusal note as the repair
  turn); exhaustion leaving the cycle OPEN with the dev-time door
  standing (a hand-written reply still applies); the engine-unavailable
  rungs (the parse cycle open, the narrator's template rung); the
  door's RunnerError class TERMINAL (the s2c1 lesson: a consumed reply
  the world refused is never re-asked).
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from cli.engine import (
    EngineConfig,
    EngineError,
    LlamaServerClient,
    narrator_messages,
)
from cli.main import main
from core.log import read_log

REPO = Path(__file__).resolve().parents[1]
GOLDEN_GRAMMAR = (
    REPO / "tests" / "fixtures" / "parse_gbnf_seed125.gbnf"
).read_text(encoding="utf-8")

_LOOK_REPLY = '{"intent": {"kind": "look_around", "target": null, "fields": {}}}'
_GOOD_PROSE = (
    "Rain started against the shutters, patient and unhurried."
)


class _StubLlamaServer:
    """The measured llama-server surface, loopback-only: records every
    request body, serves a scripted queue of completions (a content
    string, or a control tuple: ("http500",), ("raw", text),
    ("empty",), ("length", text))."""

    def __init__(
        self, model_file: Path, replies: list[Any] | None = None
    ) -> None:
        self.model_file = model_file
        self.replies: list[Any] = list(replies or [])
        self.requests: list[dict[str, Any]] = []
        self.raw_bodies: list[bytes] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 — http.server's name
                if self.path == "/health":
                    body = json.dumps({"status": "ok"}).encode()
                elif self.path == "/props":
                    body = json.dumps({
                        "role": "server",
                        "model_path": str(outer.model_file),
                        "build_info": "b11064-a894dae93",
                        "total_slots": 1,
                    }).encode()
                else:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self) -> None:  # noqa: N802 — http.server's name
                if self.path != "/v1/chat/completions":
                    self.send_error(404)
                    return
                payload = self.rfile.read(int(self.headers["Content-Length"]))
                outer.raw_bodies.append(payload)
                outer.requests.append(json.loads(payload))
                item = (
                    outer.replies.pop(0) if outer.replies else {"content": ""}
                )
                if isinstance(item, tuple) and item[0] == "http500":
                    self.send_error(500, "stub backend error")
                    return
                if isinstance(item, tuple) and item[0] == "raw":
                    body = item[1].encode()
                elif isinstance(item, tuple) and item[0] == "empty":
                    body = json.dumps({
                        "choices": [{"message": {"role": "assistant",
                                                "content": ""},
                                     "finish_reason": "stop"}],
                    }).encode()
                else:
                    content, finish = (
                        item if isinstance(item, tuple) else (item, "stop")
                    )
                    body = json.dumps({
                        "choices": [{"message": {"role": "assistant",
                                                "content": content},
                                     "finish_reason": finish}],
                    }).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: Any) -> None:
                pass  # silence the stub's stderr

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)


@pytest.fixture()
def stub(tmp_path: Path) -> _StubLlamaServer:
    model = tmp_path / "model.gguf"
    model.write_bytes(b"the stub model bytes")
    server = _StubLlamaServer(model, replies=[])
    server.start()
    yield server
    server.stop()


def _config(url: str, **overrides: Any) -> EngineConfig:
    return EngineConfig(endpoint=url, seed=125, **overrides)


def _feed(monkeypatch: pytest.MonkeyPatch, commands: list[str]) -> None:
    answers = iter(commands)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def _session_argv(stub_url: str, logs_dir: Path) -> list[str]:
    return [
        "--engine", stub_url, "--seed", "125",
        "--logs-dir", str(logs_dir),
    ]


# -- health / props / errors -----------------------------------------------------


def test_health_and_props(stub: _StubLlamaServer) -> None:
    client = LlamaServerClient(_config(stub.url))
    assert client.health() is True
    props = client.props()
    assert props["build_info"] == "b11064-a894dae93"
    assert props["model_path"].endswith("model.gguf")


def test_health_false_on_a_dead_endpoint() -> None:
    client = LlamaServerClient(_config("http://127.0.0.1:1"))
    assert client.health() is False


def test_http_error_is_terminal(stub: _StubLlamaServer) -> None:
    stub.replies.append(("http500",))  
    client = LlamaServerClient(_config(stub.url))
    with pytest.raises(EngineError, match="^\\[http\\]"):
        client.chat([{"role": "user", "content": "x"}],
                    grammar=None, temperature=0.0, max_tokens=8)


def test_malformed_and_empty_responses(stub: _StubLlamaServer) -> None:
    client = LlamaServerClient(_config(stub.url))
    stub.replies.append(("raw", "not json at all"))
    with pytest.raises(EngineError, match="^\\[malformed\\]"):
        client.chat([{"role": "user", "content": "x"}],
                    grammar=None, temperature=0.0, max_tokens=8)
    stub.replies.append(("empty",))
    with pytest.raises(EngineError, match="empty content"):
        client.chat([{"role": "user", "content": "x"}],
                    grammar=None, temperature=0.0, max_tokens=8)


def test_unavailable_after_the_tries_ladder() -> None:
    client = LlamaServerClient(_config("http://127.0.0.1:1", tries=2))
    with pytest.raises(EngineError, match="unreachable after 2 tries"):
        client.chat([{"role": "user", "content": "x"}],
                    grammar=None, temperature=0.0, max_tokens=8)


# -- serialization (the D3 request tier) ------------------------------------------


def test_the_parse_request_shape(stub: _StubLlamaServer) -> None:
    """The measured surface: document-only messages, the grammar as a
    TOP-LEVEL param (the golden grammar over the same snapshot), temp 0,
    thinking off, the seed, the completion budget."""
    client = LlamaServerClient(_config(stub.url))
    stub.replies.append(_LOOK_REPLY)
    content, finish = client.chat(
        [{"role": "user", "content": "## player_input\nhi"}],
        grammar=GOLDEN_GRAMMAR, temperature=0.0, max_tokens=160,
    )
    assert content == _LOOK_REPLY and finish == "stop"
    request = stub.requests[-1]
    assert list(request) == [  # the fixed key order: deterministic bytes
        "messages", "temperature", "max_tokens", "seed",
        "chat_template_kwargs", "grammar",
    ]
    assert request["messages"] == [
        {"role": "user", "content": "## player_input\nhi"}
    ]
    assert request["temperature"] == 0.0
    assert request["max_tokens"] == 160
    assert request["seed"] == 125
    assert request["chat_template_kwargs"] == {"enable_thinking": False}
    assert request["grammar"] == GOLDEN_GRAMMAR


def test_the_narrator_request_shape(stub: _StubLlamaServer) -> None:
    """No grammar (unconstrained by design), temp 0.8, and the §3.1
    mapping: the directives block seeds the system role, the remainder
    rides the user message byte-verbatim."""
    client = LlamaServerClient(_config(stub.url))
    stub.replies.append(_LOOK_REPLY)
    call_text = (
        "## directives\nNarrate only what the brief contains.\n"
        "Facts are immutable.\n\n## scene_delta\n[t 1] look_around: the player"
    )
    client.chat(
        narrator_messages(call_text),
        grammar=None, temperature=0.8, max_tokens=512,
    )
    request = stub.requests[-1]
    assert "grammar" not in request
    assert request["temperature"] == 0.8
    assert request["messages"] == [
        {"role": "system",
         "content": "Narrate only what the brief contains.\nFacts are immutable."},
        {"role": "user",
         "content": "## scene_delta\n[t 1] look_around: the player"},
    ]


def test_request_bytes_are_deterministic(stub: _StubLlamaServer) -> None:
    client = LlamaServerClient(_config(stub.url))
    stub.replies.extend([_LOOK_REPLY, _LOOK_REPLY])
    messages = [{"role": "user", "content": "the same call"}]
    client.chat(messages, grammar=GOLDEN_GRAMMAR,
                temperature=0.0, max_tokens=16)
    client.chat(messages, grammar=GOLDEN_GRAMMAR,
                temperature=0.0, max_tokens=16)
    assert stub.raw_bodies[-1] == stub.raw_bodies[-2]


def test_the_model_field_rides_for_routers(stub: _StubLlamaServer) -> None:
    client = LlamaServerClient(_config(stub.url, model="gemma-e4b"))
    stub.replies.append(_LOOK_REPLY)
    client.chat([{"role": "user", "content": "x"}],
                grammar=None, temperature=0.0, max_tokens=8)
    assert stub.requests[-1]["model"] == "gemma-e4b"


# -- the session cycles (the failure->ladder mapping) ------------------------------


def test_say_via_engine_feeds_the_door(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """The happy path: emit -> the GBNF-constrained answer -> apply; the
    world moves through the SAME door (zero gate edits), the manifest
    carries the model hash + the first parse grammar id, and the request
    rode the golden grammar."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.append(_LOOK_REPLY)
    _feed(monkeypatch, ["say have a good look around", "quit"])
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "[engine reply:" in out
    assert "[parsed intent fed: look_around" in out
    # the request carried the golden grammar over the seed-125 open state
    assert stub.requests[0]["grammar"] == GOLDEN_GRAMMAR
    # the world moved through the door
    log = next((tmp_path / "logs").glob("run_125_*.jsonl"))
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    _header, events = read_log(log, schema)
    assert events[-1].type == "look_around"
    # the manifest: the stub model's hash + the grammar id
    manifest_path = next((tmp_path / "engine").glob("manifest_*.json"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["build"] == "b11064-a894dae93"
    assert manifest["model_sha256"] == hashlib.sha256(
        b"the stub model bytes"
    ).hexdigest()
    assert manifest["seed"] == 125
    assert len(manifest["parse_grammar_id"]) == 16


def test_the_off_grammar_re_ask_rescues(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """The re-ask ladder (1, the heartbeat convention): the degenerate
    empty no_intent refuses at the gate, the repair turn (the refusal
    note riding user/assistant/user) re-asks, the good reply closes the
    cycle through the door."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.clear()
    stub.replies.extend(['{"no_intent": ""}', _LOOK_REPLY])
    _feed(monkeypatch, ["say have a good look around", "quit"])
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "[off-grammar reply (" in out
    assert "re-asking 1/1" in out
    assert "[parsed intent fed: look_around" in out
    # the repair turn: the original call, the bad reply, the note
    repair = stub.requests[1]["messages"]
    assert [m["role"] for m in repair] == ["user", "assistant", "user"]
    assert repair[1]["content"] == '{"no_intent": ""}'
    assert "rejected at the boundary" in repair[2]["content"]
    assert stub.requests[1]["grammar"] == GOLDEN_GRAMMAR  # still constrained


def test_re_ask_exhaustion_leaves_the_dev_time_door_standing(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """Two degenerate replies exhaust the re-ask: the cycle stays OPEN,
    the world never moved — and the dev-time door stands: a hand-written
    reply applies in the same session (engine down == operator absent)."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.clear()
    stub.replies.extend(['{"no_intent": ""}', '{"question": ""}'])
    hand_reply = tmp_path / "parser" / "parse_reply_0000.json"
    step = 0

    def scripted_input(prompt: str = "") -> str:
        # the dev-time operator's own timing: the reply file is fixed
        # BETWEEN commands (the engine's last bad reply stands until then)
        nonlocal step
        step += 1
        if step == 1:
            return "say loiter a while"
        if step == 2:
            hand_reply.write_text(
                json.dumps({"no_intent": "loitering is not world-touching"}),
                encoding="utf-8",
            )
            return f"say apply {hand_reply}"
        return "quit"

    monkeypatch.setattr("builtins.input", scripted_input)
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "[off-grammar after 1 re-ask(s)" in out
    assert "[no intent: loitering is not world-touching" in out


def test_engine_unavailable_keeps_the_parse_cycle_open(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The engine-unavailable rung for the parse door: the cycle stays
    open with the loud hint — the world never moves on silence."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    _feed(monkeypatch, ["say hello there", "quit"])
    assert main(_session_argv("http://127.0.0.1:1", tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "[engine unavailable:" in out
    assert "the cycle stays open" in out
    log = next((tmp_path / "logs").glob("run_125_*.jsonl"))
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    _header, events = read_log(log, schema)
    assert all(event.type != "talk" for event in events)


def test_narrate_via_engine_runs_the_beat(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """The narrator happy path: the engine answers the call (the §3.1
    split — system carries the directives), the beat accepts and closes
    (the empty chorus at the street)."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.clear()
    stub.replies.extend([json.dumps({"prose": _GOOD_PROSE})])
    _feed(monkeypatch, ["narrate", "quit"])
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert _GOOD_PROSE in out
    assert "[engine reply:" in out
    # the directives block seeded the system role (the §3.1 mapping)
    messages = stub.requests[0]["messages"]
    assert messages[0]["role"] == "system"
    assert "Narrate only what the brief contains" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert "## narrator_protocol" in messages[1]["content"]


def test_narrate_via_engine_regens_on_refused_prose(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """The mediator's own ladder maps the engine's failures exactly as
    the human operator's: an invented name refuses the document, the
    regen re-invokes, the clean reply accepts."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.clear()
    stub.replies.extend([
        json.dumps({"prose": "The corner hides Marlbor the miner, waving."}),
        json.dumps({"prose": _GOOD_PROSE}),
    ])
    _feed(monkeypatch, ["narrate", "quit"])
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "refused — regen 1/2" in out
    assert _GOOD_PROSE in out
    # the re-invocation rode the refusal note to the engine
    assert len(stub.requests) == 2
    assert "REFUSED" in stub.requests[1]["messages"][-1]["content"]


def test_narrate_engine_unavailable_falls_to_the_template_rung(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The engine-unavailable rung for the narrator door: dry_close (the
    L12 floor) — never a blocked beat, never a silent drop."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    _feed(monkeypatch, ["narrate", "quit"])
    assert main(_session_argv("http://127.0.0.1:1", tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "[engine unavailable:" in out
    assert "the template rung" in out
    assert "[dry beat — the L12 floor" in out


def test_the_door_runner_error_class_is_terminal(
    stub: _StubLlamaServer, tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """The s2c1 lesson: a gate-valid reply that violates a DOOR-owned
    shape law (a target-required verb with a null target) raises the
    door's loud RunnerError — the cycle is CONSUMED, the world never
    moved, and the engine never re-asks (the ParseError-only re-ask
    law; the world's refusal is an answer, not a parse failure)."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    stub.replies.clear()
    stub.replies.extend([
        '{"intent": {"kind": "examine", "target": null, "fields": {}}}',
    ])
    _feed(monkeypatch, ["say examine that tankard", "quit"])
    assert main(_session_argv(stub.url, tmp_path / "logs")) == 0
    out = capsys.readouterr().out
    assert "error: examine requires a target" in out
    assert len(stub.requests) == 1  # terminal: no re-ask
    log = next((tmp_path / "logs").glob("run_125_*.jsonl"))
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    _header, events = read_log(log, schema)
    assert all(event.type != "examine" for event in events)
