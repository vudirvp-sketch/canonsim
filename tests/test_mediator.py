"""iter-12 acceptance — the mediator session loop, agent-in-the-loop
(`cli/mediator.py` + the pure document layer `brief/mediator.py`;
protocol owner `docs/VALIDATION_SPEC.md` §7.1, call format
`docs/BRIEF_SPEC.md` §7.1, decision D-055).

The narrator is EXTERNAL: replies arrive as JSON documents, the repo
stays LLM-free (INV-4 — no network, no inference, no runtime dependency
landed with this boundary). The suite pins: the call document's bytes
(brief + protocol, pure in (log, ledger, pack)), the response document's
closed shape gate (malformed = degradation, never a crash — the gates
never see it), the refusal → regen → dry ladder (≤2 regens, L12), the
accepted path (delta through the real gateway, intents through the real
door, `mark_promoted` live wiring, canon birth in the projection), the
withdrawal mirror (a retired entry's intent never feeds), and the
call-bytes determinism (the D-049 quarantine). Since iter-13 also the
phase-1 regression set: the narrator-beat corpus (fixtures/
narrator_beats.json, distilled from the live validation-beats session)
replayed through the real cycle, plus the accepted-beat `BEAT` summary
lines (KI#44 — verdict visibility for the phase-1 exit numbers).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from brief.assembler import brief_from_log
from brief.ledger import PROMOTED, RETIRED, DeltaError, SceneLedger
from brief.mediator import (
    NarratorError,
    feedable_intents,
    narrator_call,
    narrator_response_from_mapping,
    promotions_in,
)
from brief.validator import IntentProposal, ProposalError
from cli.mediator import BeatResult, Mediator, MediatorError
from core.log import EventRecord, StateChange, read_log
from core.loop import Simulator
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


def _session(tmp_path: Path, seed: int = 42) -> tuple[Simulator, Mediator]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}])
    mediator = Mediator(sim, PACK, SCHEMA, log, tmp_path / "mediator")
    return sim, mediator


def _reply(tmp_path: Path, name: str, doc: dict[str, Any]) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _events(log: Path) -> list[EventRecord]:
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _anchor(mediator: Mediator) -> int:
    """The anchor the last emitted call advertised (from the protocol line)."""
    call = mediator._out_dir / f"call_{mediator._call_seq - 1:04d}.md"
    for line in call.read_text(encoding="utf-8").splitlines():
        if line.startswith("anchor:"):
            return int(line.split()[1])
    raise AssertionError("no anchor line in the call document")


# -- the call document (BRIEF_SPEC §7.1) -----------------------------------------


def test_call_document_is_brief_plus_protocol(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    path = mediator.emit_call()
    document = path.read_text(encoding="utf-8")
    events = _events(tmp_path / "run.jsonl")
    brief = brief_from_log(
        tmp_path / "run.jsonl", PACK, SCHEMA, ledger=mediator.ledger
    )
    assert document == (
        f"{brief}\n## narrator_protocol\nanchor: {len(events)}\nregen: 0/2\n"
    )
    assert "## directives" in document  # the brief rides unchanged


def test_notes_ride_the_call_and_are_consumed(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    mediator._pending_notes.append("REFUSED establish x (canon_slot)")
    first = mediator.emit_call()
    assert "REFUSED establish x (canon_slot)" in first.read_text(encoding="utf-8")
    second = mediator.emit_call()
    assert "REFUSED" not in second.read_text(encoding="utf-8")  # consumed


def test_call_bytes_are_deterministic(tmp_path: Path) -> None:
    _sim_a, mediator_a = _session(tmp_path / "a")
    _sim_b, mediator_b = _session(tmp_path / "b")
    doc_a = mediator_a.emit_call().read_text(encoding="utf-8")
    doc_b = mediator_b.emit_call().read_text(encoding="utf-8")
    assert doc_a == doc_b


# -- the response document gate (VALIDATION_SPEC §7.1) ---------------------------


def test_response_gate_accepts_prose_only_and_full_documents() -> None:
    bare = narrator_response_from_mapping({"prose": "The room was warm."})
    assert bare.prose == "The room was warm."
    assert bare.texture_delta is None and bare.proposal is None
    full = narrator_response_from_mapping({
        "prose": "She took the candles.",
        "texture_delta": {"source": "turn:1"},
        "proposal": {"expected_event_seq": 3},
    })
    assert full.texture_delta == {"source": "turn:1"}
    assert full.proposal is not None and full.proposal.expected_event_seq == 3


@pytest.mark.parametrize("doc", [
    {"prose": "x", "bogus": 1},          # unknown key — the document is closed
    {},                                   # prose missing
    {"prose": "   "},                     # prose empty
    {"prose": 7},                         # prose not a string
    {"prose": "x", "texture_delta": []},  # delta not an object
])
def test_response_gate_is_loud_on_outer_shape(doc: dict[str, Any]) -> None:
    with pytest.raises(NarratorError):
        narrator_response_from_mapping(doc)


def test_response_gate_runs_the_deep_gates_at_the_boundary() -> None:
    with pytest.raises(DeltaError):  # malformed delta item — before the gateway
        narrator_response_from_mapping({
            "prose": "x",
            "texture_delta": {"source": "t", "established": [{"scope": "s"}]},
        })
    with pytest.raises(ProposalError):  # malformed proposal
        narrator_response_from_mapping({
            "prose": "x", "proposal": {"claims": []},
        })


# -- feedable intents (noun resolution + the withdrawal mirror) ------------------


def _intent(kind: str = "take", actor: str = PLAYER, **fields: Any) -> IntentProposal:
    return IntentProposal(
        kind=kind, actor=actor, based_on_event_seq=0, fields=dict(fields)
    )


def test_feedable_intents_filters_for_the_door(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    mediator.ledger.apply_delta(
        {"source": "turn:1", "established": [dict(_CANDLES)]},
        _events(tmp_path / "run.jsonl"), PACK,
    )
    plain = _intent("look_around")
    texture = _intent(texture=dict(_CANDLES_REF))
    feedable, withdrawn = feedable_intents(
        [plain, texture, _intent(actor="npc_guard_01"),
         _intent(texture=dict(_CANDLES_REF, entry="tex_9999")),
         _intent(texture=dict(_CANDLES_REF)),  # duplicate entry
        ],
        mediator.ledger, PLAYER,
    )
    assert feedable == (plain, texture)
    assert withdrawn == (
        "WITHDRAWN intent take (actor 'npc_guard_01' is not the player "
        "— mode A proposes player actions only)",
        "WITHDRAWN intent take (texture entry not live: tex_9999)",
        "WITHDRAWN intent take (duplicate texture entry in one document: tex_0000)",
    )


def test_promotions_scan_matches_only_canon_births() -> None:
    def event(eid: str, etype: str, *, changes: tuple[StateChange, ...],
              outcome: dict[str, Any] | None = None) -> EventRecord:
        return EventRecord(
            id=eid, t=1, type=etype, actor=PLAYER, cause=None,
            outcome=outcome or {}, knowledge=(), state_changes=changes,
            hooks=(), importance="low", provenance={}, target=None,
        )

    birth = event(
        "ev_0001", "take",
        changes=(StateChange("loc_tavern", "candles", None, "lit"),),
        outcome={"texture": dict(_CANDLES_REF)},
    )
    failure = event("ev_0002", "take_failed", changes=(), outcome={"texture": dict(_CANDLES_REF)})
    unrelated = event("ev_0003", "move", changes=(StateChange(PLAYER, "position", "a", "b"),))
    assert promotions_in([birth, failure, unrelated]) == (("tex_0000", "ev_0001"),)


# -- the beat cycle (refusals → regen → dry; accept → door + promotion) ----------


def test_accepted_delta_establishes_texture_for_the_next_call(
    tmp_path: Path,
) -> None:
    _sim, mediator = _session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r1.json", {
        "prose": "The common room smelled of spilled ale.",
        "texture_delta": {"source": "turn:1", "established": [dict(_CANDLES)]},
    }))
    assert result.status == "accepted"
    assert [entry.id for entry in mediator.ledger.live()] == ["tex_0000"]
    call = mediator.emit_call().read_text(encoding="utf-8")
    assert "candles = lit" in call  # the brief's scene_texture window


def test_refusals_regen_then_fall_dry(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    mediator.emit_call()
    refused = {  # `exits` is pack-modeled on loc_tavern → canon_slot
        "prose": "A door stood to the north.",
        "texture_delta": {"source": "turn:1", "established": [{
            "scope": "scene:loc_tavern", "slot": "exits", "value": "north",
            "surface": "A door stood to the north.",
        }]},
    }
    first = mediator.apply_reply(_reply(tmp_path, "r1.json", refused))
    assert first.status == "regen" and first.regens_used == 1
    assert "REFUSED establish scene:loc_tavern.exits = north (canon_slot)" in first.notes
    assert "REFUSED establish scene:loc_tavern.exits = north (canon_slot)" in (
        first.call_path.read_text(encoding="utf-8")
    )  # the note rides the re-invocation's protocol section
    second = mediator.apply_reply(_reply(tmp_path, "r2.json", refused))
    assert second.status == "regen" and second.regens_used == 2
    third = mediator.apply_reply(_reply(tmp_path, "r3.json", refused))
    assert third.status == "dry"  # the budget is spent — the L12 floor
    assert not mediator.beat_open
    assert third.prose  # template prose, never a blocked beat


def test_malformed_reply_is_degradation_not_crash(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r1.json", {"prose": "x", "bogus": 1}))
    assert result.status == "regen"
    assert result.notes[0].startswith("MALFORMED")
    assert "MALFORMED" in result.call_path.read_text(encoding="utf-8")


def test_contradicted_claims_refuse_the_document(tmp_path: Path) -> None:
    _sim, mediator = _session(tmp_path)
    mediator.emit_call()
    anchor = _anchor(mediator)
    result = mediator.apply_reply(_reply(tmp_path, "r1.json", {
        "prose": "The purse lay on the table.",
        "proposal": {
            "expected_event_seq": anchor,
            "claims": [{"kind": "state", "entity": PLAYER,
                        "prop": "position", "value": "loc_moon"}],
        },
    }))
    assert result.status == "regen"
    assert any("CONTRADICTED" in note for note in result.notes)


def test_texture_intent_feeds_the_door_and_promotes(tmp_path: Path) -> None:
    sim, mediator = _session(tmp_path, seed=4)  # probed: the take check passes
    mediator.emit_call()
    mediator.apply_reply(_reply(tmp_path, "r1.json", {
        "prose": "The tables stood in candlelight.",
        "texture_delta": {"source": "turn:1", "established": [dict(_CANDLES)]},
    }))
    mediator.emit_call()
    anchor = _anchor(mediator)
    result = mediator.apply_reply(_reply(tmp_path, "r2.json", {
        "prose": "She palmed the candles before anyone looked.",
        "proposal": {
            "expected_event_seq": anchor,
            "intents": [{
                "kind": "take", "actor": PLAYER, "based_on_event_seq": anchor,
                "fields": {"texture": dict(_CANDLES_REF)},
            }],
        },
    }))
    assert result.status == "accepted"
    entry = mediator.ledger.entries[0]
    assert entry.status == PROMOTED
    take = _events(tmp_path / "run.jsonl")[-1]
    assert take.type == "take"
    assert entry.cause == take.id  # the committed take event is the promotion cause
    assert sim.projection["loc_tavern"]["candles"] == "lit"  # canon birth
    assert not mediator.beat_open


def test_retired_entry_intent_is_withdrawn_not_fed(tmp_path: Path) -> None:
    sim, mediator = _session(tmp_path)
    mediator.emit_call()
    mediator.apply_reply(_reply(tmp_path, "r1.json", {
        "prose": "The tables stood in candlelight.",
        "texture_delta": {"source": "turn:1", "established": [dict(_CANDLES)]},
    }))
    mediator.emit_call()
    anchor = _anchor(mediator)
    before = len(_events(tmp_path / "run.jsonl"))
    result = mediator.apply_reply(_reply(tmp_path, "r2.json", {
        "prose": "The candles were gone by morning.",
        "texture_delta": {"source": "turn:2", "retired": [{"id": "tex_0000"}]},
        "proposal": {
            "expected_event_seq": anchor,
            "intents": [{
                "kind": "take", "actor": PLAYER, "based_on_event_seq": anchor,
                "fields": {"texture": dict(_CANDLES_REF)},
            }],
        },
    }))
    assert result.status == "accepted"  # the retirement itself is legal
    assert len(_events(tmp_path / "run.jsonl")) == before  # nothing fed
    assert mediator.ledger.entries[0].status == RETIRED
    call = mediator.emit_call().read_text(encoding="utf-8")
    assert "WITHDRAWN intent take (texture entry not live: tex_0000)" in call


def test_dry_close_renders_the_beat_chronicle_lines(tmp_path: Path) -> None:
    sim, mediator = _session(tmp_path)
    mediator.emit_call()
    sim.run_steps([{"intent": "look_around"}])  # canon moves after the call
    result = mediator.dry_close()
    assert result.status == "dry"
    assert result.prose  # the beat's fresh chronicle lines (template rung)
    assert not mediator.beat_open


def test_apply_reply_without_an_open_beat_is_an_operator_error(
    tmp_path: Path,
) -> None:
    _sim, mediator = _session(tmp_path)
    with pytest.raises(MediatorError, match="no open narrator beat"):
        mediator.apply_reply(_reply(tmp_path, "r1.json", {"prose": "x"}))


# -- the call document, pure (narrator_call) --------------------------------------


def test_narrator_call_carries_regen_counter_and_notes() -> None:
    _header, events = read_log(
        REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl", SCHEMA
    )
    document = narrator_call(
        events, PACK, SceneLedger(), notes=("REFUSED x (canon_slot)",),
        regens_used=1,
    )
    assert document.endswith(
        f"## narrator_protocol\nanchor: {len(events)}\n"
        "regen: 1/2\nREFUSED x (canon_slot)\n"
    )


# -- the phase-1 regression set (iter-13 validation beats) ------------------------

_CORPUS = json.loads(
    (REPO / "tests" / "fixtures" / "narrator_beats.json").read_text(encoding="utf-8")
)


def _anchor_of(call_path: Path) -> int:
    """The anchor the emitted call advertised (the narrator's contract —
    BRIEF_SPEC §7.1; the corpus never hardcodes event counts)."""
    for line in call_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("anchor:"):
            return int(line.split()[1])
    raise AssertionError(f"no anchor line in {call_path}")


def _resolve_anchors(doc: Any, anchor: int) -> Any:
    """Substitute the corpus's `'anchor'` placeholders with the advertised
    anchor — exactly what the external narrator does when replying."""
    if isinstance(doc, dict):
        return {
            key: anchor if value == "anchor" else _resolve_anchors(value, anchor)
            for key, value in doc.items()
        }
    if isinstance(doc, list):
        return [_resolve_anchors(item, anchor) for item in doc]
    return doc


@pytest.mark.parametrize("case", _CORPUS["cases"], ids=lambda case: case["name"])
def test_phase1_regression_set(case: dict[str, Any], tmp_path: Path) -> None:
    """The narrator-beat corpus: full response documents from the live
    iter-13 agent-in-the-loop session, replayed through the REAL mediator
    cycle (Simulator + Mediator + SceneLedger). Every refusal family and
    every accept path at the beat level — the phase-1 exit criterion's
    regression set (0 canon violations per 100 beats, ROADMAP §2)."""
    run = tmp_path / case["name"]
    run.mkdir()
    log = run / "run.jsonl"
    sim = Simulator(PACK, case["seed"], log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(case["setup"])
    mediator = Mediator(sim, PACK, SCHEMA, log, run / "mediator")
    result: BeatResult | None = None
    pre_reply = post_reply = 0
    for beat in case["beats"]:
        anchor = _anchor_of(mediator.emit_call())
        sim.run_steps(beat.get("between", []))
        pre_reply = len(_events(log))
        reply = run / "reply.json"
        reply.write_text(
            json.dumps(_resolve_anchors(beat["reply"], anchor)), encoding="utf-8"
        )
        result = mediator.apply_reply(reply)
        post_reply = len(_events(log))
    assert result is not None
    expect = case["expect"]
    assert result.status == expect["status"]
    for needle in expect.get("notes_contains", []):
        assert any(needle in note for note in result.notes), result.notes
    if expect.get("log_unchanged"):
        assert post_reply == pre_reply  # withdrawn intents never touch canon
    if "last_event_type" in expect:
        assert _events(log)[-1].type == expect["last_event_type"]
    if "call_contains" in expect:
        final_call = mediator.emit_call().read_text(encoding="utf-8")
        assert expect["call_contains"] in final_call


def test_prose_only_beat_has_no_summary_lines(tmp_path: Path) -> None:
    """A prose-only accepted beat summarizes nothing (KI#44: the BEAT
    lines carry verdict counts, not noise)."""
    _sim, mediator = _session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(
        _reply(tmp_path, "r1.json", {"prose": "The room was warm."})
    )
    assert result.status == "accepted"
    assert result.notes == ()
