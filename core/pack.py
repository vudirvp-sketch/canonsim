"""Pack loader (PACK-1): fixed 4-file directory, `sorted()` load order
(INV-2), load-then-resolve — name-based references are checked only after
all files load (no forward declarations). The phase-0 minimum lint fails
loudly at load, before any simulation: orphan references (exits, positions,
carriers, carries), closed-enum membership (status axes, relation axes —
both declared by the pack's own `rules.json`), phase coverage of the day,
and pack meta consistency. `"_"` commentary fields are ignored wherever
references are collected. Full pack JSON-Schemas are a phase-6 rung
(`docs/BLUEPRINT.md` PACK-1); the event-contract enums the pack mirrors
are cross-checked by `tests/test_smoke.py` against the schema.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from core.clock import Clock

__all__ = ["PACK_FILE_NAMES", "Pack", "PackError", "load_pack"]

PACK_FILE_NAMES: Final = ("actions.json", "entities.json", "rules.json", "templates.json")

_SNAKE_CASE: Final = re.compile(r"^[a-z][a-z0-9_]*$")


class PackError(RuntimeError):
    """Load-time lint failure — the pack never reaches the simulation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PackError(message)


def _ids(records: list[Mapping[str, Any]]) -> set[str]:
    return {record["id"] for record in records}


class _Lint:
    """Phase-0 minimum lint: one pass over the loaded pack data."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def run(self) -> None:
        self._meta()
        self._entities()
        self._actions()
        self._templates()
        self._time_rules()

    def _meta(self) -> None:
        names = {name: d["meta"]["pack"] for name, d in self._data.items()}
        versions = {name: d["meta"]["version"] for name, d in self._data.items()}
        _require(
            len(set(names.values())) == 1 and len(set(versions.values())) == 1,
            f"pack meta disagrees across files: {names} / {versions}",
        )

    def _entities(self) -> None:
        entities = self._data["entities.json"]
        rules = self._data["rules.json"]
        locations = entities["locations"]
        npcs = entities["npcs"]
        ambients = entities["ambient_entities"]
        items = entities["items"]

        all_ids = _ids(locations) | _ids(npcs) | _ids(ambients) | _ids(items)
        total = sum(map(len, (locations, npcs, ambients, items)))
        _require(len(all_ids) == total, "entity ids are not unique across categories")

        location_ids = _ids(locations)
        by_location = {loc["id"]: loc for loc in locations}
        for loc in locations:
            for exit_id in loc["exits"]:
                _require(exit_id in location_ids, f"location {loc['id']}: orphan exit {exit_id}")
                _require(
                    loc["id"] in by_location[exit_id]["exits"],
                    f"exit graph asymmetric: {loc['id']} -> {exit_id}",
                )

        status_axes = set(rules["states"])
        relation_axes = set(rules["relations"]["axes"])
        item_ids = _ids(items)
        npc_ids = _ids(npcs)
        for npc in npcs:
            _require(npc["position"] in location_ids, f"npc {npc['id']}: unknown position")
            for carried in npc.get("carries", []):
                _require(carried in item_ids, f"npc {npc['id']}: carries unknown item {carried}")
            unknown_status = set(npc.get("status", {})) - status_axes
            _require(not unknown_status, f"npc {npc['id']}: unknown status axes {unknown_status}")
            unknown_axes = set(npc.get("relations", {})) - relation_axes
            _require(not unknown_axes, f"npc {npc['id']}: unknown relation axes {unknown_axes}")

        players = [npc["id"] for npc in npcs if npc.get("is_player", False)]
        _require(len(players) == 1, f"exactly one is_player npc required, got {players}")

        for ambient in ambients:
            _require(
                ambient["position"] in location_ids,
                f"ambient {ambient['id']}: unknown position",
            )

        for item in items:
            _require(item["position"] in location_ids, f"item {item['id']}: unknown position")
            carrier = item.get("carrier")
            if carrier is not None:
                _require(carrier in npc_ids, f"item {item['id']}: unknown carrier {carrier}")
                owner = next(npc for npc in npcs if npc["id"] == carrier)
                _require(
                    item["id"] in owner.get("carries", []),
                    f"item {item['id']}: carrier {carrier} does not carry it",
                )
        for npc in npcs:
            for carried in npc.get("carries", []):
                item = next(i for i in items if i["id"] == carried)
                _require(
                    item.get("carrier") == npc["id"],
                    f"npc {npc['id']} carries {carried} but the item names "
                    f"{item.get('carrier')!r}",
                )

    def _actions(self) -> None:
        actions = self._data["actions.json"]["actions"]
        intents = [action["intent"] for action in actions]
        _require(len(intents) == len(set(intents)), "action intents are not unique")
        for action in actions:
            _require(
                bool(_SNAKE_CASE.match(action["intent"])),
                f"action intent {action['intent']!r} is not snake_case",
            )
            ticks = action["ticks"]
            if isinstance(ticks, Mapping):
                _require(
                    isinstance(ticks.get("min"), int) and isinstance(ticks.get("max"), int)
                    and ticks["min"] <= ticks["max"],
                    f"action {action['intent']}: ticks range malformed: {ticks}",
                )
            else:
                _require(
                    isinstance(ticks, int) or ticks == "N",
                    f"action {action['intent']}: ticks must be int, {{min,max}} or 'N'",
                )
            resolver = action.get("resolver")
            _require(
                resolver is None or isinstance(resolver, str),
                f"action {action['intent']}: resolver must be a string",
            )

    def _templates(self) -> None:
        templates = self._data["templates.json"]
        _require("fallback" in templates, "templates: missing fallback line")
        for event_type in templates["events"]:
            _require(
                bool(_SNAKE_CASE.match(event_type)),
                f"template event type {event_type!r} is not snake_case",
            )

    def _time_rules(self) -> None:
        time_rules = self._data["rules.json"]["time"]
        try:
            Clock.from_rules(time_rules)
        except ValueError as exc:
            raise PackError(f"time rules invalid: {exc}") from exc


@dataclass(frozen=True, slots=True)
class Pack:
    """Loaded, linted pack: the setting as read-only data (INV-3)."""

    data: Mapping[str, Mapping[str, Any]]

    @property
    def name(self) -> str:
        return self.data["entities.json"]["meta"]["pack"]

    @property
    def version(self) -> str:
        return self.data["entities.json"]["meta"]["version"]

    @property
    def name_version(self) -> str:
        return f"{self.name}@{self.version}"

    @property
    def entities(self) -> Mapping[str, Any]:
        return self.data["entities.json"]

    @property
    def rules(self) -> Mapping[str, Any]:
        return self.data["rules.json"]

    @property
    def templates(self) -> Mapping[str, Any]:
        return self.data["templates.json"]

    def action(self, intent: str) -> Mapping[str, Any] | None:
        """The action record for an intent type, or None."""
        for action in self.data["actions.json"]["actions"]:
            if action["intent"] == intent:
                return action
        return None

    def event_types(self) -> frozenset[str]:
        """The pack's closed event-type vocabulary (templates own it in
        phase 0 — every type the slice can produce has a chronicle line)."""
        return frozenset(self.templates["events"])

    def player_id(self) -> str:
        """The single is_player entity id."""
        for npc in self.entities["npcs"]:
            if npc.get("is_player", False):
                return npc["id"]
        raise PackError("no is_player npc in pack")


def load_pack(pack_dir: Path) -> Pack:
    """Load the fixed 4-file pack directory and run the minimum lint."""
    present = {path.name for path in pack_dir.glob("*.json")}
    _require(
        present == set(PACK_FILE_NAMES),
        f"{pack_dir}: expected exactly {list(PACK_FILE_NAMES)}, found {sorted(present)}",
    )
    data: dict[str, Mapping[str, Any]] = {}
    for name in sorted(PACK_FILE_NAMES):  # INV-2: sorted() load order
        with (pack_dir / name).open(encoding="utf-8") as fh:
            data[name] = json.load(fh)
    _Lint(data).run()
    return Pack(data=data)
