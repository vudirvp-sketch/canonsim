"""Smoke tests: pack data integrity and event-contract shape (iter-0d).

Guards the iter-0c data draft and the two-place event contract
(docs/EVENT_SCHEMA.md <-> schemas/event.schema.json) until the real suite
(T0-T8, docs/MVP_SCOPE.md §14) lands with iter-1+. Structural checks only:
log-line validation against the schema is T0 and arrives with iter-1.
"""

import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "content" / "tavern_pack"
SCHEMA = REPO / "schemas" / "event.schema.json"

# The action intents pinned by docs/MVP_SCOPE.md §7 (12 phase-0 + rest, tune-1).
MVP_INTENTS = frozenset(
    {
        "look_around",
        "examine",
        "move",
        "talk",
        "wait",
        "take",
        "drop_break",
        "use",
        "steal",
        "distract",
        "arson",
        "rest",  # tune-1 (iter-27): the fatigue counter-play, pack data
        "flee",
        "document_check",  # iter-43: the crime ladder's public rung (D-072)
    }
)

# Status axes pinned by docs/MVP_SCOPE.md §4.2.
STATUS_KEYS = frozenset({"fatigue", "intoxication", "fear", "injury"})


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def entities() -> dict[str, Any]:
    return load(PACK / "entities.json")


def rules() -> dict[str, Any]:
    return load(PACK / "rules.json")


def test_pack_files_parse() -> None:
    for name in ("entities", "actions", "rules", "templates"):
        assert isinstance(load(PACK / f"{name}.json"), dict)


def test_entity_counts_match_mvp_scope() -> None:
    data = entities()
    assert len(data["locations"]) == 5  # MVP_SCOPE §4.1
    assert len(data["npcs"]) == 6  # MVP_SCOPE §4.2
    assert len(data["ambient_entities"]) == 1  # MVP_SCOPE §4.2 ambient group
    assert len(data["items"]) == 5  # MVP_SCOPE §4.3


def test_entity_ids_are_unique() -> None:
    data = entities()
    ids = [
        e["id"]
        for key in ("locations", "npcs", "ambient_entities", "items")
        for e in data[key]
    ]
    assert len(ids) == len(set(ids))


def test_location_graph_is_symmetric_and_closed() -> None:
    data = entities()
    by_id = {loc["id"]: loc for loc in data["locations"]}
    for loc in data["locations"]:
        for exit_id in loc["exits"]:
            assert exit_id in by_id, f"unknown exit {exit_id}"
            assert loc["id"] in by_id[exit_id]["exits"], f"asymmetric {loc['id']}->{exit_id}"


def test_npcs_are_well_formed() -> None:
    data = entities()
    location_ids = {loc["id"] for loc in data["locations"]}
    axes = set(rules()["relations"]["axes"])
    players = 0
    for npc in data["npcs"]:
        assert npc["position"] in location_ids, npc["id"]
        assert set(npc["status"]) <= STATUS_KEYS, npc["id"]
        assert set(npc["relations"]) <= axes, npc["id"]
        players += int(npc.get("is_player", False))
    assert players == 1


def test_items_are_well_formed() -> None:
    data = entities()
    location_ids = {loc["id"] for loc in data["locations"]}
    npc_ids = {npc["id"] for npc in data["npcs"]}
    for item in data["items"]:
        assert item["position"] in location_ids, item["id"]
        assert item["carrier"] is None or item["carrier"] in npc_ids, item["id"]
        assert isinstance(item["is_fire_source"], bool), item["id"]


def test_time_rules_cover_the_day_exactly() -> None:
    time = rules()["time"]
    assert time["ticks_per_day"] == 1440  # MVP_SCOPE §8
    cursor = 0
    for phase in time["phases"]:
        assert phase["from"] == cursor, phase["id"]
        cursor = phase["to"]
    assert cursor == time["ticks_per_day"]


def test_knowledge_enums_match_event_schema() -> None:
    knowledge = rules()["knowledge"]
    assert knowledge["channels"] == ["saw", "heard", "told", "inferred"]  # EVENT_SCHEMA §3
    assert knowledge["fidelity_chain"] == ["exact", "partial", "vague"]  # EVENT_SCHEMA §3


def test_suspicion_thresholds_escalate() -> None:
    # status flip (relations thresholds) < document check (the director
    # hook's threshold trigger — single owner since the iter-4a cleanup)
    # < arrest (crime_watch.arrest)
    thresholds = rules()["relations"]["suspicion_thresholds"]
    doc_check = rules()["director"]["hooks"]["possible_document_check"]["trigger"]
    assert doc_check["kind"] == "threshold" and doc_check["axis"] == "suspicion"
    arrest_at = rules()["crime_watch"]["arrest"]["requires_suspicion"]
    assert thresholds["status_suspect_at"] < doc_check["value"]
    assert doc_check["value"] < arrest_at


def test_watch_rotation_ticks_are_inside_the_day() -> None:
    day = rules()["time"]["ticks_per_day"]
    ticks = rules()["crime_watch"]["watch_rotation_ticks"]
    assert all(0 <= tick < day for tick in ticks)


def test_actions_match_mvp_scope() -> None:
    data = load(PACK / "actions.json")
    # MVP_SCOPE §7: 12 phase-0 + rest (tune-1) + document_check (iter-43)
    assert len(data["actions"]) == 14
    intents = [a["intent"] for a in data["actions"]]
    assert len(intents) == len(set(intents))
    assert frozenset(intents) == MVP_INTENTS


def test_templates_have_fallback_and_snake_case_types() -> None:
    data = load(PACK / "templates.json")
    assert "fallback" in data
    assert "events" in data
    pattern = re.compile(r"^[a-z][a-z0-9_]*$")
    for event_type in data["events"]:
        assert pattern.match(event_type), event_type


def test_event_schema_shape_matches_event_schema_doc() -> None:
    schema = load(SCHEMA)
    assert schema["$id"] == "canonsim/event/0.1"
    assert set(schema["required"]) == {
        "id",
        "t",
        "type",
        "actor",
        "cause",
        "outcome",
        "knowledge",
        "state_changes",
        "hooks",
        "importance",
        "provenance",
    }  # EVENT_SCHEMA §2
    defs = schema["$defs"]
    assert set(defs["knowledge_record"]["required"]) == {
        "who",
        "channel",
        "fidelity",
        "knows",
        "at",
        "source",
    }  # EVENT_SCHEMA §3
    assert defs["knowledge_record"]["properties"]["channel"]["enum"] == [
        "saw",
        "heard",
        "told",
        "inferred",
    ]
    assert defs["knowledge_record"]["properties"]["fidelity"]["enum"] == [
        "exact",
        "partial",
        "vague",
    ]
    assert schema["properties"]["importance"]["enum"] == ["low", "medium", "high"]
    assert schema["properties"]["id"]["pattern"] == "^ev_[0-9]{4,}$"
