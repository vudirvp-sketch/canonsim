"""The parser session door (phase 2, mode C — D-062; contract owner
`docs/PARSER_SPEC.md`).

The parser is EXTERNAL at dev-time, exactly like the narrator (D-055): an
operator reading a parse call file and writing a parse reply file — the
repo itself stays LLM-free and network-free (INV-4 unchanged; the runtime
inference engine stays the owner-gated decision). Files are the contract,
both gitignored runtime artifacts under `output/parser/`:

    parse_<NNNN>.md          the parser's input: the utterance + the grammar snapshot + the protocol
    parse_reply_<NNNN>.json  the parser's output: {intent} | {question} | {no_intent}

One cycle: `say <text>` emits the call (ledger hygiene first — the
contradiction window and the scene sync, the same idempotent folds the
narrator door runs); `say apply <reply.json>` gates the reply at the
boundary, pins any live texture entry the parsed intent references
(blueprint §1(a) — the reference IS the pin; a door-rejected attempt
still pins), feeds the intent through the door as ONE step, and wires
committed promotions exactly like the narrator path. Off-grammar replies
are loud ParseErrors — the session prints them and nothing feeds: the
world never moves on a malformed parse (the runtime re-ask ladder is
deferred with the runtime engine decision, PARSER_SPEC §7). A question
surfaces to the player — uncertainty is asked, never guessed.

This module is periphery (D-046): files, the Simulator handle, cycle
state — never engine mechanics. The engine-side work is `brief/parser.py`
pure functions; the ledger is the session's SHARED SceneLedger (the
narrator establishes texture; the player's words reference it — one
ledger, D-049).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from brief.ledger import SceneLedger
from brief.mediator import promotions_in
from brief.parser import (
    ParsedIntent,
    ParseError,
    grammar_snapshot,
    parse_call,
    parse_reply_from_mapping,
)
from core.log import EventRecord, read_log
from core.loop import Simulator
from core.pack import Pack

__all__ = ["ParseError", "ParseResult", "ParserDoor"]


@dataclass(frozen=True, slots=True)
class ParseResult:
    """One completed parse cycle. `status`:

    - `intent` — a boundary-accepted intent went through the door; the
      world moved, or the door rejected it as a world fact
      (`intent_rejected` — attempts are facts); `events` counts the fresh
      log records, `pinned` the entries the reference pinned, `promoted`
      the entries committed events flipped;
    - `question` — the parser asks the player; nothing fed (`text` is
      the question);
    - `no_intent` — the utterance carries no world-touching intent
      (`text` is the parser's note).
    """

    status: str
    text: str = ""
    step: Mapping[str, Any] | None = None
    events: int = 0
    pinned: tuple[str, ...] = ()
    promoted: tuple[str, ...] = ()


class ParserDoor:
    """One session's mode-C door over an opened Simulator plus the shared
    scene ledger. `say <text>` → `emit_call`; `say apply <reply>` →
    `apply_reply`. One call awaits one reply; the door dies with the
    session (the D-049 death law — texture is never persisted)."""

    def __init__(
        self,
        sim: Simulator,
        pack: Pack,
        schema: Mapping[str, Any],
        log_path: Path,
        ledger: SceneLedger,
        out_dir: Path,
    ) -> None:
        self._sim = sim
        self._pack = pack
        self._schema = schema
        self._log_path = log_path
        self._ledger = ledger
        self._out_dir = Path(out_dir)
        self._out_dir.mkdir(parents=True, exist_ok=True)
        self._call_seq = 0
        self._call_events = 0  # the log length at the last emit (retire window edge)
        self._awaiting_reply = False

    @property
    def awaiting_reply(self) -> bool:
        return self._awaiting_reply

    def emit_call(self, text: str) -> Path:
        """Emit the parse call for one utterance: retire texture
        contradicted by the window's new canon, sync the scene, then
        assemble the document (utterance + grammar + protocol)."""
        if not isinstance(text, str) or not text.strip():
            raise ParseError("the utterance must be a non-empty string")
        events = self._events()
        self._ledger.retire_contradicted(events[self._call_events :])
        self._ledger.sync_scene(events, self._pack)
        document = parse_call(text, events, self._pack, self._ledger)
        path = self._out_dir / f"parse_{self._call_seq:04d}.md"
        path.write_text(document, encoding="utf-8")
        self._call_seq += 1
        self._call_events = len(events)
        self._awaiting_reply = True
        return path

    def apply_reply(self, reply_path: Path) -> ParseResult:
        """Ingest the parser's reply and close the cycle: shape gate
        against the CURRENT grammar (recomputed — a reply naming texture
        that died mid-cycle is off-grammar), then either surface the
        question/no-intent verdict or feed the intent through the door
        (pin the referenced entry, run the step, wire promotions)."""
        if not self._awaiting_reply:
            raise ParseError("no parse call awaits a reply — say <text> first")
        try:
            doc = json.loads(reply_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ParseError(f"cannot read reply {reply_path}: {exc}") from exc
        events = self._events()
        snapshot = grammar_snapshot(events, self._pack, self._ledger)
        reply = parse_reply_from_mapping(doc, snapshot)
        self._awaiting_reply = False
        if reply.question is not None:
            return ParseResult(status="question", text=reply.question)
        if reply.no_intent is not None:
            return ParseResult(status="no_intent", text=reply.no_intent)

        assert reply.intent is not None  # the gate's exactly-one law
        intent = reply.intent
        pinned: tuple[str, ...] = ()
        reference = intent.fields.get("texture")
        if isinstance(reference, Mapping) and "entry" in reference:
            entry_id = str(reference["entry"])
            if self._ledger.pin(entry_id):
                pinned = (entry_id,)
        step = _step(intent)
        before = len(events)
        self._sim.run_steps([step])
        fresh = self._events()
        promotions = promotions_in(fresh[before:])
        for entry_id, event_id in promotions:
            self._ledger.mark_promoted(entry_id, event_id)
        return ParseResult(
            status="intent",
            step=step,
            events=len(fresh) - before,
            pinned=pinned,
            promoted=tuple(entry_id for entry_id, _ in promotions),
        )

    def _events(self) -> list[EventRecord]:
        _header, events = read_log(self._log_path, self._schema)
        return list(events)


def _step(intent: ParsedIntent) -> dict[str, Any]:
    """ParsedIntent → the step grammar the door already owns
    (INTENT_SCHEMA §9) — the same conversion the narrator path performs
    (`cli/mediator.py::_step`); the door anchors the intent at feed time."""
    step: dict[str, Any] = {"intent": intent.kind}
    if intent.target is not None:
        step["target"] = intent.target
    step.update(intent.fields)
    return step
