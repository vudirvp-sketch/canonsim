"""iter-10 acceptance — the session scene ledger (`docs/blueprint/phases.md`
§1 owns the mechanism, D-048/D-049; `docs/BRIEF_SPEC.md` §3.3 owns the
read-side window; `docs/VALIDATION_SPEC.md` §8 owns the protocol clauses).

The ledger is session render state, never canon: the gateway is a pure
function of (delta, events, pack) — no RNG, no wall-clock, writes
nothing to the log (INV-1/2/4; the D-049 determinism quarantine). The
suite pins: scene derivation (PC-location intervals, revisit ordinals),
presence (position + the carried-item closure), the gateway's refusal
vocabulary + the idempotent duplicate rule, the discrete one-way
lifecycle, the beat-pass contradiction retirement (first break wins),
scene-close bulk retirement, the texture-OCC mirror, and the committed
golden delta fixture (`tests/fixtures/texture_deltas.json` — the
VALIDATION_SPEC §9 computed-golden pattern).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from brief import (
    ACTIVE,
    CONTRADICTED,
    PINNED,
    PROMOTED,
    RETIRED,
    DeltaError,
    SceneLedger,
    current_scene,
    present_entities,
    refusal_lines,
    scenes,
)
from brief.ledger import LedgerEntry
from core.fold import initial_projection
from core.log import EventRecord, StateChange, read_log
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
PLAYER = PACK.player_id()


def _ev(
    eid: str,
    t: int,
    etype: str,
    actor: str,
    cause: str | None,
    *,
    changes: tuple[StateChange, ...] = (),
) -> EventRecord:
    return EventRecord(
        id=eid, t=t, type=etype, actor=actor, cause=cause,
        outcome={}, knowledge=(), state_changes=changes, hooks=(),
        importance="low", provenance={"seed": 42}, target=None,
    )


def _establish(
    ledger: SceneLedger,
    events: list[EventRecord],
    scope: str,
    slot: str,
    value: str,
    source: str = "turn:1",
) -> Any:
    """One-establishment delta shorthand for gateway unit tests."""
    return ledger.apply_delta(
        {
            "source": source,
            "established": [
                {"scope": scope, "slot": slot, "value": value, "surface": f"{slot} was {value}."}
            ],
        },
        events,
        PACK,
    )


def _golden_events() -> list[EventRecord]:
    _header, events = read_log(GOLDEN, SCHEMA)
    return events


def _mutated_pack(mutate: Any) -> Pack:
    data = json.loads(json.dumps(dict(PACK.data)))
    mutate(data["rules.json"])
    return Pack(data=data)


# -- scene derivation (PC-location interval; D-049) ------------------------------


def test_scenes_from_the_golden_log() -> None:
    events = _golden_events()
    assert [
        (scene.location_id, scene.ordinal, scene.from_tick, scene.to_tick)
        for scene in scenes(events, PACK)
    ] == [
        ("loc_street", 0, 0, 2),
        ("loc_tavern", 0, 2, 36),
        ("loc_backyard", 0, 36, 54),
        ("loc_street", 1, 54, 58),  # the revisit is a NEW scene
        ("loc_market", 0, 58, None),
    ]


def test_empty_log_is_one_open_scene_at_the_pack_start() -> None:
    scene = current_scene((), PACK)
    assert (scene.location_id, scene.ordinal, scene.from_tick, scene.to_tick) == (
        "loc_street", 0, 0, None,
    )


def test_move_to_same_location_keeps_the_scene_maximal() -> None:
    events = [
        _ev(
            "ev_0000", 5, "move", PLAYER, None,
            changes=(StateChange(PLAYER, "position", "loc_street", "loc_tavern"),),
        ),
        _ev(
            "ev_0001", 9, "move", PLAYER, "ev_0000",
            changes=(StateChange(PLAYER, "position", "loc_tavern", "loc_tavern"),),
        ),
    ]
    derived = scenes(events, PACK)
    assert len(derived) == 2
    assert derived[-1].to_tick is None  # no close: the interval stays maximal


# -- presence (position + the carried-item closure) ------------------------------


def test_present_entities_position_and_carrier_closure() -> None:
    state = initial_projection(PACK.entities)
    present = present_entities(state, "loc_tavern", PACK)
    assert PLAYER not in present  # the pack's START: the PC is still in the street
    assert PLAYER in present_entities(state, "loc_street", PACK)
    assert "npc_guard_01" in present  # positioned there
    assert "npc_guard_02" not in present  # in the guardroom
    assert "purse_01" in present  # carried by the present guard
    assert "rope_01" not in present  # positioned in the backyard


def test_present_entities_item_carried_by_absent_npc_is_absent() -> None:
    state = initial_projection(PACK.entities)
    assert "purse_01" not in present_entities(state, "loc_backyard", PACK)


# -- the gateway: refusals, no-ops, updates (unit; golden-log prefixes) ----------


def test_establishment_stamps_t_from_the_log_never_the_delta() -> None:
    events = _golden_events()[:2]  # last event t=32
    ledger = SceneLedger()
    report = _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    assert [entry.t for entry in report.established] == [32]  # L3: derive-never-store
    assert report.established[0].source == "turn:1"


def test_ids_allocate_in_append_order_gap_free() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    _establish(ledger, events, "scene:loc_tavern", "hearth", "crackling", source="turn:2")
    assert [entry.id for entry in ledger.entries] == ["tex_0000", "tex_0001"]


def test_entity_scope_on_a_location_is_refused() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    report = _establish(ledger, events, "entity:loc_tavern", "shutters", "closed")
    assert report.refused
    assert report.refusals[0].reason == "scope_target"


def test_malformed_scope_prefix_is_refused() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    report = _establish(ledger, events, "zone:loc_tavern", "shutters", "closed")
    assert report.refusals[0].reason == "scope_target"


def test_canon_slot_refusal_for_location_props() -> None:
    events = [
        _ev("ev_0000", 2, "move", PLAYER, None,
            changes=(StateChange(PLAYER, "position", "loc_street", "loc_tavern"),)),
        _ev("ev_0001", 4, "fire_start", "npc_drunk_01", "ev_0000",
            changes=(StateChange("loc_tavern", "burning", None, "smoldering"),)),
    ]
    ledger = SceneLedger()
    report = _establish(ledger, events, "scene:loc_tavern", "burning", "bright")
    assert report.refusals[0].reason == "canon_slot"  # canon outranks texture


def test_canon_slot_refusal_for_item_props() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    report = _establish(ledger, events, "entity:purse_01", "carrier", "the guard")
    assert report.refusals[0].reason == "canon_slot"  # carrier is canon-modeled


def test_unique_slot_refusal_across_scopes() -> None:
    pack = _mutated_pack(
        lambda rules: rules["brief"]["scene_texture"].update(unique_slots=["cloak"])
    )
    events = _golden_events()[:2]
    ledger = SceneLedger()
    first = ledger.apply_delta(
        {
            "source": "turn:1",
            "established": [
                {"scope": "entity:npc_guard_01", "slot": "cloak", "value": "muddy hem",
                 "surface": "A muddy hem."}
            ],
        },
        events,
        pack,
    )
    assert first.established  # entity-scoped cloak established at the tavern
    second = ledger.apply_delta(
        {
            "source": "turn:2",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "cloak", "value": "on a nail",
                 "surface": "A spare cloak on a nail."}
            ],
        },
        events,
        pack,
    )
    assert second.refusals[0].reason == "unique_slot"  # cross-scope re-establishment


def test_unique_slot_allows_live_same_scope_rules() -> None:
    """The unique flag fires ONLY cross-scope: same-scope play stays under
    the duplicate / slot-conflict rules, and a retired entry releases its
    claim (the slot denotes one object, not one lifetime)."""
    pack = _mutated_pack(
        lambda rules: rules["brief"]["scene_texture"].update(unique_slots=["cloak"])
    )
    events = _golden_events()[:2]
    ledger = SceneLedger()
    ledger.apply_delta(
        {
            "source": "turn:1",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "cloak", "value": "on a nail",
                 "surface": "A spare cloak on a nail."}
            ],
        },
        events,
        pack,
    )
    conflict = ledger.apply_delta(
        {
            "source": "turn:2",
            "established": [
                {"scope": "scene:loc_tavern", "slot": "cloak", "value": "on the floor",
                 "surface": "Someone dropped it."}
            ],
        },
        events,
        pack,
    )
    assert conflict.refusals[0].reason == "slot_conflict"  # NOT unique_slot


def test_laundering_refusal_for_contradicted_values() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    (contradicted,) = ledger.retire_contradicted(
        (
            _ev("ev_9000", 40, "gust", "npc_drunk_01", None,
                changes=(StateChange("loc_tavern", "candles", None, "scattered"),)),
        )
    )
    assert contradicted.status == CONTRADICTED and contradicted.cause == "ev_9000"
    report = _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    assert report.refusals[0].reason == "laundering"  # re-asserting the refuted value


def test_laundering_refusal_for_promoted_away_values() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    promoted = ledger.mark_promoted("tex_0000", "ev_0001")
    assert (promoted.status, promoted.cause) == (PROMOTED, "ev_0001")
    report = _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    assert report.refusals[0].reason == "laundering"


def test_new_value_after_contradiction_is_not_laundering() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    ledger.retire_contradicted(
        (_ev("ev_9000", 40, "gust", "npc_drunk_01", None,
             changes=(StateChange("loc_tavern", "candles", None, "scattered"),)),)
    )
    report = _establish(
        ledger, events, "scene:loc_tavern", "candles", "replaced by oil lamps"
    )
    assert report.established  # a different value is fresh texture, not laundering


def test_ref_to_terminal_entry_is_a_stale_refusal() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    ledger.retire_contradicted(
        (_ev("ev_9000", 40, "gust", "npc_drunk_01", None,
             changes=(StateChange("loc_tavern", "candles", None, "scattered"),)),)
    )
    report = ledger.apply_delta(
        {"source": "turn:2", "refs": [{"id": "tex_0000"}]}, events, PACK
    )
    assert report.refusals[0].reason == "stale_ref"


def test_retire_of_not_live_entry_is_an_idempotent_no_op() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    report = ledger.apply_delta(
        {"source": "turn:2", "retired": [{"id": "tex_0000"}, {"id": "tex_0000"}]},
        events,
        PACK,
    )
    assert [entry.id for entry in report.retired] == ["tex_0000"]
    assert len(report.no_ops) == 1  # the second retire: not live anymore


def test_re_establishment_after_narrator_retirement_is_fresh() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    ledger.apply_delta(
        {"source": "turn:2", "retired": [{"id": "tex_0000"}]}, events, PACK
    )
    report = _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    assert [entry.id for entry in report.established] == ["tex_0001"]  # new candles


def test_refusal_lines_shape() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    report = _establish(ledger, events, "scene:loc_backyard", "bonfire", "smoldering")
    assert refusal_lines(report) == (
        "REFUSED establish scene:loc_backyard.bonfire = smoldering (scene_mismatch)",
    )


def test_gateway_is_deterministic_given_its_inputs() -> None:
    events = _golden_events()[:2]
    delta = {
        "source": "turn:1",
        "established": [
            {"scope": "scene:loc_tavern", "slot": "candles", "value": "lit",
             "surface": "Tallow candles."}
        ],
    }
    ledger_a, ledger_b = SceneLedger(), SceneLedger()
    ledger_a.apply_delta(delta, events, PACK)
    ledger_b.apply_delta(delta, events, PACK)
    assert ledger_a.entries == ledger_b.entries  # same inputs → same state


# -- the delta shape gate (loud — emitter bugs crash) ----------------------------


def test_delta_shape_gates() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    scope = {"scope": "scene:loc_tavern", "slot": "candles"}
    bad_deltas = (
        {"source": "turn:1", "unknown_key": []},  # closed document
        {"established": []},  # missing source
        {"source": "  "},  # empty source
        {"source": "turn:1", "established": {"scope": "x"}},  # not a list
        # missing value/surface
        {"source": "turn:1", "established": [dict(scope)]},
        # unknown key — the item document is closed too
        {"source": "turn:1", "established": [dict(scope, value="lit", surface="s", extra=1)]},
        # both selector shapes at once
        {"source": "turn:1", "retired": [dict(id="tex_0000", **scope)]},
        # scope without slot
        {"source": "turn:1", "refs": [{"scope": "scene:loc_tavern"}]},
    )
    for delta in bad_deltas:
        with pytest.raises(DeltaError):
            ledger.apply_delta(delta, events, PACK)


# -- the beat pass: contradiction retirement (canon outranks texture) ------------


def test_retire_contradicted_first_break_wins_the_cause() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    _establish(ledger, events, "entity:npc_guard_01", "cloak", "muddy hem", source="turn:2")
    window = (
        _ev("ev_9000", 40, "gust", "npc_drunk_01", None,
            changes=(StateChange("loc_tavern", "candles", None, "scattered"),)),
        _ev("ev_9001", 44, "gust", "npc_drunk_01", "ev_9000",
            changes=(StateChange("loc_tavern", "candles", "scattered", "gone"),)),
        _ev("ev_9002", 46, "mop", "npc_maid_01", "ev_9001",
            changes=(StateChange("npc_guard_01", "cloak", None, "washed"),)),
    )
    retired = ledger.retire_contradicted(window)
    causes = {entry.scope: entry.cause for entry in retired}
    assert causes == {
        "scene:loc_tavern": "ev_9000",  # first break wins
        "entity:npc_guard_01": "ev_9002",  # entity-scoped target touched too
    }
    statuses = {entry.scope: entry.status for entry in ledger.entries}
    assert set(statuses.values()) == {CONTRADICTED}


def test_retire_contradicted_touches_only_overlapping_props() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    untouched = ledger.retire_contradicted(
        (_ev("ev_9000", 40, "gust", "npc_drunk_01", None,
             changes=(StateChange("loc_tavern", "shutters", None, "banging"),)),)
    )
    assert untouched == ()  # slot/prop overlap only — structural, never semantic


# -- scene close + sync (bulk retirement; entity-scoped survives) ----------------


def test_sync_scene_closes_and_retires_scene_scoped_texture() -> None:
    events = _golden_events()
    ledger = SceneLedger()
    _establish(ledger, events[:2], "scene:loc_tavern", "candles", "lit")
    _establish(ledger, events[:2], "entity:npc_guard_01", "cloak", "muddy hem", source="turn:2")
    sync = ledger.sync_scene(events[:3], PACK)  # the PC moved to the backyard
    assert sync.closed is not None and sync.closed.location_id == "loc_tavern"
    assert [entry.id for entry in sync.retired] == ["tex_0000"]  # scene-scoped only
    assert ledger.entries[1].status == ACTIVE  # entity-scoped survives


def test_sync_scene_is_idempotent_within_a_scene() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    first = ledger.sync_scene(events, PACK)  # adopts the tavern... no — the market
    assert first.closed is None  # first sync adopts, never closes
    second = ledger.sync_scene(events, PACK)
    assert second.closed is None and second.retired == ()  # same scene: no-op


def test_apply_delta_auto_syncs_so_a_close_cannot_be_forgotten() -> None:
    events = _golden_events()
    ledger = SceneLedger()
    _establish(ledger, events[:2], "scene:loc_tavern", "candles", "lit")
    # no explicit sync — apply_delta at the full log must close the tavern
    _establish(ledger, events, "scene:loc_market", "stalls", "half packed up", source="turn:9")
    assert ledger.entries[0].status == RETIRED
    assert ledger.entries[0].cause == "scene_close"


def test_revisit_scene_starts_texture_empty() -> None:
    """Scene-scoped texture from an earlier scene at the same location is
    gone with that scene — both retired (sync) and invisible (window law,
    via the brief suite); a fresh establishment is a new entry."""
    events = _golden_events()
    ledger = SceneLedger()
    _establish(ledger, events[:2], "scene:loc_tavern", "candles", "lit")
    ledger.sync_scene(events, PACK)  # PC now at the market (tavern scene closed)
    # a later prefix that revisits the street is still a different scene;
    # re-establishing the same slot+value after scene_close is FRESH
    report = _establish(ledger, events, "scene:loc_market", "candles", "lit", source="turn:5")
    assert [entry.id for entry in report.established] == ["tex_0001"]


# -- promotion + the texture-OCC mirror ------------------------------------------


def test_mark_promoted_loud_on_unknown_and_terminal() -> None:
    events = _golden_events()[:2]
    ledger = SceneLedger()
    _establish(ledger, events, "scene:loc_tavern", "candles", "lit")
    ledger.retire_contradicted(
        (_ev("ev_9000", 40, "gust", "npc_drunk_01", None,
             changes=(StateChange("loc_tavern", "candles", None, "scattered"),)),)
    )
    with pytest.raises(DeltaError):
        ledger.mark_promoted("tex_9999", "ev_0001")  # unknown id
    with pytest.raises(DeltaError):
        ledger.mark_promoted("tex_0000", "ev_0001")  # terminal (contradicted)
    with pytest.raises(DeltaError):
        ledger.mark_promoted("tex_0000", "")  # no cause event


def test_withdrawals_mirror_pending_texture_intents() -> None:
    events = _golden_events()
    ledger = SceneLedger()
    _establish(ledger, events[:2], "scene:loc_tavern", "candles", "lit")
    _establish(ledger, events[:2], "entity:npc_guard_01", "cloak", "muddy hem", source="turn:2")
    ledger.sync_scene(events, PACK)  # candles retired by scene_close; cloak survives
    withdrawn = ledger.withdrawals(
        {"intent_a": "tex_0000", "intent_b": "tex_0001", "intent_c": "tex_9999"}
    )
    assert withdrawn == ("intent_a", "intent_c")  # not live → withdrawn, not an event
    assert ledger.withdrawals({"intent_d": "tex_0001"}) == ()  # live stays pending


def test_pinned_entry_pins_to_a_terminal_state_or_scene_close() -> None:
    events = _golden_events()
    ledger = SceneLedger()
    _establish(ledger, events[:2], "scene:loc_tavern", "candles", "lit")
    ledger.apply_delta(
        {"source": "turn:2", "refs": [{"id": "tex_0000"}]}, events[:2], PACK
    )
    assert ledger.entries[0].status == PINNED
    ledger.sync_scene(events, PACK)  # the scene closes: even pinned texture retires
    assert (ledger.entries[0].status, ledger.entries[0].cause) == (RETIRED, "scene_close")


# -- the committed golden delta fixture (VALIDATION_SPEC §9 pattern) --------------


def test_texture_delta_golden_fixture_replays() -> None:
    doc = json.loads(
        (REPO / "tests" / "fixtures" / "texture_deltas.json").read_text(encoding="utf-8")
    )
    _header, events = read_log(REPO / doc["log"], SCHEMA)
    ledger = SceneLedger()
    for case in doc["cases"]:
        report = ledger.apply_delta(case["delta"], events[: case["event_seq"]], PACK)
        expect = case["expect"]
        assert [entry.id for entry in report.established] == expect["established"], case["name"]
        assert list(report.pinned) == expect["pinned"], case["name"]
        assert [entry.id for entry in report.retired] == expect["retired"], case["name"]
        assert len(report.no_ops) == expect["no_ops"], case["name"]
        assert refusal_lines(report) == tuple(expect["refusals"]), case["name"]
        assert [
            [entry.id, entry.t, entry.status, entry.cause] for entry in ledger.entries
        ] == expect["ledger"], case["name"]
        # every entry the fixture pins is shape-complete (the entry contract)
        for entry in ledger.entries:
            assert isinstance(entry, LedgerEntry)
            assert entry.surface and entry.source
