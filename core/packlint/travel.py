"""The travel block lint (st-6a; the price law's pack half — the D-175
split's travel family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.intent import EDGE_TICKS
from core.packlint.helpers import PackError, _require
from core.travel import EDGE_OVERRIDES_KEY, TRAVEL_BLOCK, TRAVEL_KEYS
from core.worldgen import WORLDGEN_BLOCK


class TravelLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _travel(self) -> None:
        """The travel price law's pack half (st-6a, D-116 (5); runs after
        `_worldgen` — the coverage law reads the claims' declared sites,
        whose shape `_worldgen` validates first, and the exits graph,
        whose symmetry `_entities` guarantees). THE PAIRING LAW: the
        `travel` block exists exactly when an edge-priced action does —
        an action without the block is dead vocabulary (no price
        source), a block without an action is dead data (the
        status_effects family, both directions refused). THE WEIGHTS:
        `step_ticks` >= 1 (zero would make same-cell edges free),
        `climb_ticks`/`river_ticks` >= 0 (an off modifier is policy,
        never dead data). THE OVERRIDES: one entry per undirected exits
        edge — the pair must be a REAL edge (an override for a
        non-edge prices a road that does not exist), `ticks` >= 1
        (a zero-duration edge is degenerate), no duplicate pairs (the
        claims' double-declaration family). THE COVERAGE LAW: when an
        edge-priced action is declared, EVERY exits edge is priceable —
        an override or two claimed endpoints (an unpriceable edge is a
        travel verb that hard-fails mid-run: dead vocabulary, refused
        at load; claim the endpoints or price the edge)."""
        rules = self._data["rules.json"]
        travel = rules.get(TRAVEL_BLOCK)
        actions = self._data["actions.json"]["actions"]
        edge_priced = [
            action for action in actions if action.get("ticks") == EDGE_TICKS
        ]
        where = f"rules.json {TRAVEL_BLOCK}"
        if travel is None:
            if edge_priced:
                raise PackError(
                    f"rules.json: the action "
                    f"{edge_priced[0]['intent']!r} declares ticks "
                    f"'{EDGE_TICKS}' but the rules declare no "
                    f"{TRAVEL_BLOCK!r} block — the weights are the "
                    "price's source (dead vocabulary, refused at load)"
                )
            return  # the unarmed law: no block, no edge-priced action
        if not isinstance(travel, Mapping):
            raise PackError(f"{where}: must be an object")
        if not edge_priced:
            raise PackError(
                f"{where}: the travel block without an edge-priced "
                "action is dead data (no action declares ticks "
                f"'{EDGE_TICKS}' — the pairing law, both directions)"
            )
        unknown = sorted(set(travel) - set(TRAVEL_KEYS))
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed "
                f"vocabulary: {' | '.join(TRAVEL_KEYS)})"
            )
        step_ticks = travel.get("step_ticks")
        if (
            not isinstance(step_ticks, int)
            or isinstance(step_ticks, bool)
            or step_ticks < 1
        ):
            raise PackError(
                f"{where}.step_ticks must be an integer >= 1, got "
                f"{step_ticks!r} (the derived price's base unit — zero "
                "would make same-cell edges free)"
            )
        for key in ("climb_ticks", "river_ticks"):
            value = travel.get(key, 0)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise PackError(
                    f"{where}.{key} must be an integer >= 0, got "
                    f"{value!r} (an off modifier is policy, never dead "
                    "data — declare 0 or omit the key)"
                )
        locations = {
            record["id"]: record
            for record in self._data["entities.json"]["locations"]
        }
        edges: set[tuple[str, str]] = set()
        for record in self._data["entities.json"]["locations"]:
            for exit_id in record["exits"]:
                left, right = sorted((str(record["id"]), str(exit_id)))
                edges.add((left, right))
        overrides: dict[tuple[str, str], int] = {}
        entries = travel.get(EDGE_OVERRIDES_KEY)
        if entries is not None:
            if not isinstance(entries, list):
                raise PackError(
                    f"{where}.{EDGE_OVERRIDES_KEY} must be a list of edge "
                    "entries"
                )
            if not entries:
                # an empty list is dead data — omit the key (the claims
                # law); the derived law alone prices every edge
                raise PackError(
                    f"{where}.{EDGE_OVERRIDES_KEY}: an empty list is dead "
                    "data — omit the key"
                )
        for index, entry in enumerate(entries or ()):  # None = key omitted
            spot = f"{where}.{EDGE_OVERRIDES_KEY}[{index}]"
            _require(isinstance(entry, Mapping), f"{spot}: must be an object")
            unknown = sorted(set(entry) - {"from", "to", "ticks"})
            if unknown:
                raise PackError(
                    f"{spot}: unknown keys {unknown} (the closed "
                    "vocabulary: from | to | ticks)"
                )
            origin = entry.get("from")
            destination = entry.get("to")
            for side, value in (("from", origin), ("to", destination)):
                if value not in locations:
                    raise PackError(
                        f"{spot}.{side} {value!r}: unknown location id "
                        "(entities.json locations is the single owner)"
                    )
            pair = tuple(sorted((str(origin), str(destination))))
            if pair not in edges:
                raise PackError(
                    f"{spot}: {origin!r} <-> {destination!r} is not an "
                    "exits edge (an override prices a road that does "
                    "not exist — dead data, refused at load)"
                )
            ticks = entry.get("ticks")
            if not isinstance(ticks, int) or isinstance(ticks, bool) or ticks < 1:
                raise PackError(
                    f"{spot}.ticks must be an integer >= 1, got "
                    f"{ticks!r} (a zero-duration edge is degenerate)"
                )
            if pair in overrides:
                raise PackError(
                    f"{spot}: the edge {pair[0]!r} <-> {pair[1]!r} is "
                    "overridden twice (the double-declaration family — "
                    "one price per road)"
                )
            overrides[pair] = ticks
        # THE COVERAGE LAW: with an edge-priced action declared, every
        # exits edge is priceable — an override, or two claimed
        # endpoints (the derived law; an unarmed worldgen makes the
        # derived law unavailable, so EVERY edge needs an override).
        sites_by_location: dict[str, list[int]] = {}
        for entry in self._data["rules.json"].get(WORLDGEN_BLOCK, {}).get(
            "claims", ()
        ):
            sites_by_location.setdefault(
                str(entry["location"]), []
            ).append(int(entry["site"]))
        for left, right in sorted(edges):
            if (left, right) in overrides:
                continue
            if sites_by_location.get(left) and sites_by_location.get(right):
                continue
            raise PackError(
                f"{where}: the exits edge {left!r} <-> {right!r} carries "
                "no override and an endpoint is unclaimed (or the "
                "worldgen is unarmed) — the travel verb would hard-fail "
                "on it mid-run (an edge-local price needs edge-local "
                "sites, D-116 (5); price the edge or claim both "
                "endpoints)"
            )
