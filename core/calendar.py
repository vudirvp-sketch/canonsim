"""The sub-year cadence family (maclock-1's middle granularities, the
calendar slice — L4's layered clocks grown to three tiers: micro-time
(ticks), the SUB-YEAR calendar cadences, macro-time (years), ONE
authority). `rules.json::time.calendar` — a mapping of named entries,
each a recurring clock at a pack-declared period:

- THE CROSSING LAW (the depth-3 "scheduler rule" family, INV-2-clean):
  crossings are the positive multiples of the entry's `every_ticks` —
  tick-derived integer arithmetic, never entropy. At a co-occurring
  tick the COARSEST clock fires first (the year turns before the
  season, the season before the fair, the fair before the week's
  turn, the week's turn before the day's rotation, the rotation
  before the beat); within the calendar the order is `every_ticks` DESCENDING
  then the entry id — deterministic, pinned.
- THE SUB-YEAR LAW: every entry's `every_ticks` is strictly below the
  macro cadence — the year clock owns the year turns (a second
  year-scale clock is a duplicate declaration, the "one clock, one
  cadence" family law; the calendar never re-declares what the macro
  block already owns). A calendar without the macro clock is dead
  data (the pairing law's own direction: the middle granularities
  hang from the same authority's head block).
- THE TURN (INV-1 — the calendar's increments are canon, never ambient
  truth): each crossing commits ONE event through the canon door —
  actor `world`, cause chained by the loop to the previous canon id
  (the chronological-chain law), the outcome carrying the entry id
  (`calendar`), the day coordinate (`day` — derived, L3: the macro
  turn's `year` twin), and — for a CYCLED entry — the phase
  (`phase`: the k-th crossing carries `cycle[k % len(cycle)]`, pure
  arithmetic again). No knowledge (a world event), no state_changes
  (the day and the phase are derived, L3), no hooks (the director
  boundary is the consumers' own rows, never the clock's); importance
  rides the pack's own rule (the story-critical listing decides tale
  visibility — the tune-1 split).
- THE CYCLE (the seasons' form): an optional list of PHASE PAIRS on
  the entry — `{phase, event_type}`, at least two, the phases unique
  — the recurring clock's OWN vocabulary; the k-th crossing carries
  the k-th pair's phase and renders its event type (each season's
  turn is its own tale line, never a shared template keyed on a raw
  id), and the phase rotates deterministically (the seasons turn by
  arithmetic, never by draw — the snowmelt comes when it comes). A
  cycled entry declares no `event_type` of its own (the pairs own the
  types — the lint refuses both-or-neither). The current phase is a
  PURE READ (`calendar_phase`) — never stored, so the fold never
  needs it and no consumer pays a corpus price for a phase it does
  not read (the unborn-stay-counts law, L13).
- THE UNARMED LAW (the 68a pattern): an absent `time.calendar` block
  is zero crossings, zero events, the committed bytes untouched — the
  clock family runs at the year granularity alone. The committed
  pack's arming rides with the slice's own content (the recurring
  trade turns, the great fair, the river's seasonal rise).

The aggregate surface stays the macro turn's own (`core/macro.py` —
the counts ride the YEAR's outcome, never the calendar's): the
calendar's consumers land as pack data over the event types (the tale
lines, the importance listing, the weather family's seasonal ride —
`core/weather.py` reads a cycled entry's phase at its roll).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.intent import pack_importance
from core.log import EventDraft
from core.transitions import WORLD

__all__ = [
    "CALENDAR_ENTRY_KEYS",
    "CalendarError",
    "calendar_entries",
    "calendar_order",
    "calendar_phase",
    "calendar_turn_draft",
    "next_calendar_tick",
]

#: The closed vocabulary of one `time.calendar` entry (the lint owns
#: the load-time contract; this is the engine-side mirror the raw-read
#: guards and the docs cite — one owner per shape, the lint the
#: authority). `cycle` and `notes` are optional; a CYCLED entry carries
#: no `event_type` of its own — the cycle's pairs own the types.
CALENDAR_ENTRY_KEYS: Final = ("every_ticks", "event_type", "cycle", "notes")

#: The closed vocabulary of one cycle pair (the phases' own emission
#: surface: the k-th crossing renders the k-th phase's event type —
#: the season's turn is the phase's own tale line, never a shared
#: template keyed on a raw id).
CYCLE_PAIR_KEYS: Final = ("phase", "event_type")


class CalendarError(ValueError):
    """A calendar-family contract failure (raw-read surfaces fail loud,
    never with a KeyError — the pred-contract family law, D-111)."""


def calendar_entries(
    rules: Mapping[str, Any],
) -> Mapping[str, Mapping[str, Any]]:
    """The declared calendar block, validated loud (the runtime
    backstop: the lint owns the load-time contract; a hand-built
    runtime config that skips it fails here with the block named).
    An absent block is the unarmed law — an EMPTY mapping, never
    None (the callers iterate; the 68a pattern)."""
    time_rules = rules.get("time")
    if not isinstance(time_rules, Mapping):
        raise CalendarError(
            "the calendar family reads the pack's time rules — the "
            "rules declare none (the lint guarantees time is an "
            "object; this is the runtime backstop)"
        )
    calendar = time_rules.get("calendar")
    if calendar is None:
        return {}
    if not isinstance(calendar, Mapping):
        raise CalendarError(
            "time.calendar must be an object (a mapping of named "
            "sub-year cadence entries)"
        )
    return calendar


def next_calendar_tick(entry: Mapping[str, Any], after: int) -> int:
    """The entry's smallest crossing strictly after `after`: the
    positive multiples of the declared period. Pure tick arithmetic
    (the scheduler rule — INV-2-clean, the macro clock's twin)."""
    every = entry.get("every_ticks")
    if not isinstance(every, int) or isinstance(every, bool) or every < 1:
        raise CalendarError(
            f"calendar entry every_ticks must be an integer >= 1, got "
            f"{every!r} (zero or negative is an infinite crossing loop, "
            "never a clock)"
        )
    return (after // every + 1) * every


def calendar_order(
    rules: Mapping[str, Any],
) -> tuple[str, ...]:
    """The deterministic crossing order of the declared entries:
    `every_ticks` DESCENDING (the coarsest calendar clock first — the
    family's own crossing discipline), then the entry id (the pinned
    tiebreak). A stable total order over the entries, so a
    co-occurring tick's commits are byte-identical across runs and
    environments (INV-2's construction-order discipline)."""
    entries = calendar_entries(rules)
    return tuple(
        sorted(entries, key=lambda eid: (-entries[eid]["every_ticks"], eid))
    )


def calendar_phase(
    rules: Mapping[str, Any], entry_id: str, t: int,
) -> str | None:
    """The entry's phase at tick `t` — None for a plain (uncycled)
    entry, else the k-th pair's `phase` (`cycle[t // every_ticks %
    len(cycle)]`, pure arithmetic, L3: derived, never stored — the
    macro-year's own law). The weather family's seasonal layer reads
    this at its roll; the fold never needs it."""
    entry = calendar_entries(rules).get(entry_id)
    if entry is None:
        raise CalendarError(
            f"calendar_phase read the entry {entry_id!r} — time.calendar "
            "declares no such entry (the lint guarantees the binding; "
            "this is the runtime backstop)"
        )
    cycle = entry.get("cycle")
    if cycle is None:
        return None
    every = entry["every_ticks"]
    return str(cycle[t // every % len(cycle)]["phase"])


def calendar_turn_draft(
    rules: Mapping[str, Any], entry_id: str, t: int,
) -> EventDraft:
    """The crossing's ONE event (INV-1 — the calendar's increments are
    canon): the outcome carries the entry id (`calendar`), the day
    coordinate (`day` — derived, L3, the macro turn's `year` twin) and,
    for a cycled entry, the phase (`phase` — the template binding
    surface). A CYCLED entry's event type is the CURRENT phase's own
    (`cycle[k].event_type` — each phase's turn renders its own tale
    line); a plain entry's is its declared `event_type`. Actor WORLD,
    no knowledge (the ambient law — a world event, the macro turn's own
    shape), no state_changes, no hooks (the director boundary is the
    consumers' rows, never the clock's); importance rides the pack's
    own rule."""
    entry = calendar_entries(rules).get(entry_id)
    if entry is None:
        raise CalendarError(
            f"calendar_turn_draft read the entry {entry_id!r} — "
            "time.calendar declares no such entry"
        )
    cycle = entry.get("cycle")
    if cycle is None:
        event_type = entry.get("event_type")
    else:
        every = entry["every_ticks"]
        event_type = cycle[t // every % len(cycle)].get("event_type")
    if not isinstance(event_type, str) or not event_type:
        raise CalendarError(
            f"calendar entry {entry_id!r} event_type must be a "
            f"non-empty string, got {event_type!r}"
        )
    time_rules = rules["time"]
    ticks_per_day = time_rules["ticks_per_day"]
    outcome: dict[str, Any] = {
        "calendar": entry_id,
        "day": t // int(ticks_per_day),
    }
    phase = calendar_phase(rules, entry_id, t)
    if phase is not None:
        outcome["phase"] = phase
    return EventDraft(
        t=t,
        type=event_type,
        actor=WORLD,
        cause=None,  # the loop chains to the writer's last id (the
        # chronological-chain law, the macro turn's precedent)
        outcome=outcome,
        knowledge=(),
        state_changes=(),
        hooks=(),
        importance=pack_importance(
            rules, {WORLD}, irreversible=0, hooks=0, event_type=event_type,
        ),
        provenance={},  # the loop stamps seed at commit (the family law)
    )
