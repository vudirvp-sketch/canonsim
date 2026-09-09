"""The macro-clock primitive (maclock-1, L4 layered clocks — phases.md
§5): micro-time (ticks) and macro-time (years) are layered clocks, one
authority, two granularities. The macro-year is the macro-clock's
COUNTER — derived, never stored (L3: the year is a pure function of
the tick and the pack-declared cadence); each turn is recorded as ONE
event through the canon door (INV-1 — the calendar's increments are
canon, not ambient truth). The cadence is PACK-DECLARED under
`rules.json::time.macro` (D-116 (4): neither a global tick-year
constant — TIME-1's three primitives + the AGENTS §8 tick-semantics
fence — nor forever-decorative years); an absent block is the unarmed
law (zero crossings, zero events, the v0.1 bytes untouched — the 68a
pattern; the committed pack's arming rides with the primitive's first
consumer).

The scheduler cadence rule (INV-2-clean, the depth-3 "scheduler rule"
family): crossings are the positive multiples of the declared cadence
— tick-derived integer arithmetic, never entropy; the loop fires them
in the crossing discipline (tick order, coarsest clock first at a
co-occurring tick: the year turns before the day's rotation, the
rotation before the beat).

The aggregate-event emission surface (D-112's shape — one event with
cardinality): `macro_turn_draft` builds the single event a consumer's
counts ride (the D-112 `band_raid {caravans: 3, losses: 1}` form —
log growth O(consumers x macrobeats), never O(members x ticks)); the
count keys are the consumers' own future vocabulary (pack-side through
their declarations), the surface is shape-only and refuses a key
colliding with the counter's own (`year` — the branch-fake family:
the chron-2 line's conditional branches on the outcome shape, a count
named `year` would flip it). The primitive's own run-path event carries
no counts — depth-3 (warm ring), depth-7 (group ticks), st-6a (travel)
and weather-1 (ambient) land after, each calling the surface at the
crossing (one primitive, one row, first — the scheduler blast-radius
insurance, D-116 (6)).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.intent import pack_importance
from core.log import EventDraft
from core.transitions import WORLD

__all__ = [
    "MACRO_KEYS",
    "MacroError",
    "macro_year",
    "macro_year_start",
    "macro_turn_draft",
    "next_macro_tick",
]

#: The closed vocabulary of the `time.macro` sub-block (the lint owns
#: the load-time contract; this is the engine-side mirror the raw-read
#: guards and the docs cite — one owner per shape, the lint the
#: authority).
MACRO_KEYS: Final = ("cadence_ticks", "event_type")

#: The counter's reserved outcome key. A count named `year` is a branch
#: fake (the RESERVED_CLAIM_SLOTS family: the history line's
#: `{year?...}` conditional branches on the outcome shape — a cardinality
#: key named `year` would collide with the calendar's own coordinate).
RESERVED_COUNT_KEYS: Final = ("year",)


class MacroError(ValueError):
    """A macro-clock contract failure (raw-read surfaces fail loud,
    never with a KeyError — the pred-contract family law, D-111)."""


def _cadence(macro_rules: Mapping[str, Any] | None) -> int | None:
    """The declared cadence, validated loud (the runtime backstop: the
    lint owns the load-time contract; a hand-built runtime config that
    skips it fails here with the block named)."""
    if macro_rules is None:
        return None
    cadence = macro_rules.get("cadence_ticks")
    if not isinstance(cadence, int) or isinstance(cadence, bool) or cadence < 1:
        raise MacroError(
            f"time.macro.cadence_ticks must be an integer >= 1, got "
            f"{cadence!r} (zero or negative is an infinite crossing "
            "loop, never a clock)"
        )
    return cadence


def next_macro_tick(
    macro_rules: Mapping[str, Any] | None, after: int
) -> int | None:
    """The smallest macro-crossing strictly after `after`: the positive
    multiples of the declared cadence. None when the pack declares no
    macro block (the unarmed law). Pure tick arithmetic — the rotation
    and beat cadences' sibling, the depth-3 "scheduler rule" family
    (INV-2-clean: tick-derived, never entropy)."""
    cadence = _cadence(macro_rules)
    if cadence is None:
        return None
    return (after // cadence + 1) * cadence


def macro_year_start(rules: Mapping[str, Any]) -> int:
    """The macro-year counter's value at tick 0 — the calendar binding
    (D-116 (4)): a worldgen-armed pack's genesis years are the world's
    history BEFORE the run, so the live counter continues from the
    chronicle horizon (`worldgen.chronicle.years` — the pack's own
    number); an unarmed pack counts from 0. One rule, both ends
    pack-declared — never a global tick-year constant."""
    worldgen = rules.get("worldgen")
    if not isinstance(worldgen, Mapping):
        return 0
    years = worldgen.get("chronicle", {}).get("years", 0)
    if not isinstance(years, int) or isinstance(years, bool) or years < 0:
        raise MacroError(
            f"worldgen.chronicle.years must be an integer >= 0 for the "
            f"macro-year binding, got {years!r}"
        )
    return years


def macro_year(rules: Mapping[str, Any], t: int) -> int:
    """The macro-year of a tick: `start + t // cadence` — the counter
    law (L3: derived, never stored; each turn's event records the value,
    INV-1). The genesis years and the live years are ONE timeline: the
    crossing at `k * cadence` turns the year to `start + k`."""
    cadence = _cadence(rules.get("time", {}).get("macro"))
    if cadence is None:
        raise MacroError(
            "macro_year reads an armed macro clock — the pack declares "
            "no time.macro block (call only on the armed path)"
        )
    return macro_year_start(rules) + t // cadence


def macro_turn_draft(
    rules: Mapping[str, Any],
    t: int,
    counts: Mapping[str, int] | None = None,
) -> EventDraft:
    """The aggregate-event emission surface (D-112's shape — one event
    with cardinality): the macro turn's draft at tick `t`. The outcome
    carries the year (the counter's value — the calendar coordinate)
    plus the consumer's counts as FLAT integer keys (the flat-keys
    family: written after the fixed key, the template binding surface).
    The count keys are the future consumers' vocabulary (pack-side,
    their rows own the lints); this surface is shape-only and refuses a
    key colliding with `year` (the branch-fake family) or a non-count
    value. Actor WORLD, no knowledge (a world event), no state_changes
    (the year is derived, never stored — L3), no hooks (the director
    boundary is the consumers' own rows, never the clock's); importance
    rides the pack's own rule (the story-critical listing decides
    visibility — the tune-1 split)."""
    macro_rules = rules.get("time", {}).get("macro")
    cadence = _cadence(macro_rules)
    if cadence is None:
        raise MacroError(
            "macro_turn_draft reads an armed macro clock — the pack "
            "declares no time.macro block"
        )
    event_type = macro_rules.get("event_type")
    if not isinstance(event_type, str) or not event_type:
        raise MacroError(
            f"time.macro.event_type must be a non-empty string, got "
            f"{event_type!r}"
        )
    outcome: dict[str, Any] = {"year": macro_year(rules, t)}
    for key, value in (counts or {}).items():
        if key in RESERVED_COUNT_KEYS:
            raise MacroError(
                f"macro count key {key!r} is reserved for the counter — "
                "a cardinality key named for the calendar's own "
                "coordinate would flip the {year?...} template branch "
                "(the branch-fake family, RESERVED_CLAIM_SLOTS' twin)"
            )
        if not isinstance(key, str) or not key.strip():
            raise MacroError(
                f"macro count keys must be non-empty strings, got {key!r}"
            )
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise MacroError(
                f"macro count {key!r} must be a non-negative integer "
                f"(cardinality), got {value!r}"
            )
        if key in outcome:
            raise MacroError(
                f"macro count key {key!r} duplicates an outcome key"
            )
        outcome[key] = value
    return EventDraft(
        t=t,
        type=event_type,
        actor=WORLD,
        cause=None,  # the loop chains to the writer's last id (the
        # chronological-chain law, the rotation's precedent)
        outcome=outcome,
        knowledge=(),
        state_changes=(),
        hooks=(),
        importance=pack_importance(
            rules, set(), irreversible=0, hooks=0, event_type=event_type,
        ),
        provenance={},  # the loop stamps seed at commit (the family law)
    )
