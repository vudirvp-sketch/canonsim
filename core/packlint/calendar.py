"""The calendar block lint (maclock-1's middle granularities — the
D-175 split's calendar family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.packlint.helpers import PackError, _is_int, _require


class CalendarLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _calendar(self) -> None:
        """The sub-year cadence family's pack half (maclock-1's middle
        granularities, the calendar slice — `core/calendar.py` the
        engine twin). Runs after `_time_rules` (the pairing reads the
        macro block) and before `_weather` (the seasonal layer's ride
        binding reads the entries validated here).

        THE PAIRING LAW (the L4 one-authority family): a calendar
        without the macro clock is dead data — the middle
        granularities hang from the same authority's head block (a
        sub-year clock in a pack that declares no year clock has no
        calendar to sit inside). The other direction is legal: the
        clock may run calendar-less (the year granularity alone, the
        68a pattern — the committed pack's arming rides with the
        slice's own content).

        THE SUB-YEAR LAW: every entry's `every_ticks` is an integer
        in [1, macro.cadence_ticks) — the year clock owns the year
        turns, a second year-scale clock is a duplicate declaration
        ("one clock, one cadence"; the calendar never re-declares
        what the macro block already owns).

        THE IDENTITY LAW: the entries' event types are unique across
        the block (a cycled entry's phases included) and differ from
        the macro turn's and the weather change's — the fold scans by
        event type; a shared type would mix two families' outcome
        shapes (the weather lint's own law, extended to the whole
        clock family).

        THE CYCLE LAW (the vacuity family): a declared `cycle` is a
        list of at least TWO phase pairs `{phase, event_type}` — the
        phases unique non-empty strings, the event types in the
        template closure under the same identity laws; one phase is
        a constant, never a cycle (dead data). A cycled entry
        declares NO `event_type` of its own and a plain one MUST —
        the both-or-neither refusal (an ambiguous emission surface
        is a drift the fold cannot diagnose). The phases are the
        entry's own vocabulary, consumed by the weather family's
        seasonal weights (the ride's binding law)."""
        time_rules = self._data["rules.json"]["time"]
        calendar = time_rules.get("calendar")
        if calendar is None:
            return  # the unarmed law: no block, no family, zero crossings
        where = "time.calendar"
        _require(
            isinstance(calendar, Mapping) and calendar,
            f"{where}: must be a non-empty object (a mapping of named "
            "sub-year cadence entries)",
        )
        macro = time_rules.get("macro")
        if macro is None:
            raise PackError(
                f"{where}: the sub-year cadences hang from the same "
                "authority's head block — declare time.macro (a calendar "
                "without the year clock is dead data: the middle "
                "granularities have no calendar to sit inside; the "
                "pairing law — the other direction is legal, the clock "
                "may run calendar-less)"
            )
        cadence = macro["cadence_ticks"]
        templates = self._data["templates.json"]["events"]
        weather = self._data["rules.json"].get("weather")
        weather_event = (
            weather.get("event_type")
            if isinstance(weather, Mapping) else None
        )
        seen_types: set[str] = set()

        def _check_event_type(
            entry_where: str, event_type: object,
        ) -> None:
            """One emission surface's identity checks (the shared law:
            the template closure, the macro/weather identities, the
            block-unique types — the clock family's own names)."""
            if not (isinstance(event_type, str) and event_type in templates):
                raise PackError(
                    f"{entry_where} {event_type!r} is not in the template "
                    "vocabulary (EVENT_SCHEMA §11 — closed per pack)"
                )
            if event_type == macro.get("event_type"):
                raise PackError(
                    f"{entry_where} {event_type!r} is the macro turn's own "
                    "event type — two families, two identities (the fold "
                    "scans by event type; a shared type would mix the "
                    "year's counter with the calendar's day)"
                )
            if event_type == weather_event:
                raise PackError(
                    f"{entry_where} {event_type!r} is the weather change's "
                    "own event type — two families, two identities (the "
                    "fold scans by event type; a shared type would mix "
                    "the sky's state with the calendar's day)"
                )
            if event_type in seen_types:
                raise PackError(
                    f"{entry_where} {event_type!r} is already declared "
                    "by another calendar emission — one entry, one "
                    "identity (the fold scans by event type)"
                )
            seen_types.add(str(event_type))

        for entry_id, entry in calendar.items():
            entry_where = f"{where}[{entry_id!r}]"
            _require(
                isinstance(entry, Mapping),
                f"{entry_where}: must be an object",
            )
            unknown = sorted(set(entry) - {"every_ticks", "event_type",
                                          "cycle", "notes"})
            if unknown:
                raise PackError(
                    f"{entry_where}: unknown keys {unknown} (the closed "
                    "vocabulary: every_ticks | event_type | cycle | notes)"
                )
            every = entry.get("every_ticks")
            if not (_is_int(every) and 1 <= every < cadence):
                raise PackError(
                    f"{entry_where}.every_ticks must be an integer in "
                    f"[1, {cadence}) — the sub-year law: the year clock "
                    f"(time.macro.cadence_ticks = {cadence}) owns the "
                    "year turns; a second year-scale clock is a duplicate "
                    "declaration, never a calendar"
                )
            cycle = entry.get("cycle")
            has_own_type = "event_type" in entry
            if has_own_type == (cycle is not None):
                raise PackError(
                    f"{entry_where}: exactly one of event_type or cycle — "
                    "a plain entry declares its own turn's type, a cycled "
                    "entry's phases own the types (an ambiguous emission "
                    "surface is a drift the fold cannot diagnose)"
                )
            if has_own_type:
                _check_event_type(
                    f"{entry_where}.event_type", entry.get("event_type")
                )
            else:
                if (
                    not isinstance(cycle, list)
                    or len(cycle) < 2
                    or not all(isinstance(pair, Mapping) for pair in cycle)
                ):
                    raise PackError(
                        f"{entry_where}.cycle must be a list of at least "
                        "two phase pairs {{phase, event_type}} (one phase "
                        "is a constant, never a cycle — the vacuity "
                        f"family; got {cycle!r})"
                    )
                phases: list[str] = []
                for pair in cycle:
                    pair_where = f"{entry_where}.cycle[{pair.get('phase')!r}]"
                    unknown = sorted(set(pair) - {"phase", "event_type"})
                    if unknown:
                        raise PackError(
                            f"{pair_where}: unknown keys {unknown} (the "
                            "closed vocabulary: phase | event_type)"
                        )
                    phase = pair.get("phase")
                    if not isinstance(phase, str) or not phase:
                        raise PackError(
                            f"{pair_where}.phase must be a non-empty "
                            "string (the phase is the entry's own "
                            "vocabulary — the weather family's seasonal "
                            "weights key on it)"
                        )
                    if phase in phases:
                        raise PackError(
                            f"{pair_where}: the phase {phase!r} repeats — "
                            "the cycle's phases are unique (a repeated "
                            "phase is a clock that cannot tell its own "
                            "position)"
                        )
                    phases.append(phase)
                    _check_event_type(
                        f"{pair_where}.event_type", pair.get("event_type")
                    )
            if "notes" in entry and not isinstance(entry["notes"], str):
                raise PackError(
                    f"{entry_where}.notes must be a string (the pack's "
                    "commentary convention)"
                )
