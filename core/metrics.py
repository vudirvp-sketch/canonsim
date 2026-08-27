"""Phase-0 metrics (M1–M5) + the emergent-chain count — pure functions of
the log + projection (`docs/TEST_PLAN.md` §2, `MVP_SCOPE.md` §15).

Shape: the Mesa `DataCollector` inverted — the metric is a pure function
of `(events, projection)`, no per-event hook into the simulator. The
simulator emits; the metric reads. The simulator never knows a metric
exists (L3 — derive-never-store).

System classification is pack data: `rules.json::metrics.system_of_type`
maps each event type to the systems it touches (a list — an event can
touch several). The state-change prop-prefix map is mechanic vocabulary
(MVP_SCOPE §5 systems are mechanic words, not setting nouns — the
`tests/test_inv3_stoplist.py` FAQ note) and lives here as a constant.

The metrics are deterministic: the same events + projection produce the
same numbers, no RNG, no wall-clock. The balance harness
(`scripts/balance_harness.py`) calls these across 1000 seed-varied runs;
the gate playscript's T8 A/B computes M5 on the OFF run, M2 on the ON
run, M1/M3/M4 on both.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from statistics import mean, median
from typing import Any

from core.fold import Projection
from core.log import EventRecord

__all__ = [
    "MetricReport",
    "emergent_chains",
    "metrics_report",
    "m1_cross_system_share",
    "m2_hooks_fired_ratio",
    "m3_causal_chain_lengths",
    "m4_novelty_repetition",
    "m5_non_pc_share",
    "systems_touched",
]

# Mechanic vocabulary (MVP_SCOPE §5 systems are mechanic words, FAQ note in
# STATUS.md). Pack data owns the event_type → systems map; this map owns
# the state_change prop-prefix → system map (a small closed set).
_PROP_PREFIX_TO_SYSTEM: Mapping[str, str] = {
    "position": "position_visibility",
    "relations": "relations",
    "status": "states",
    "fire": "fire",
    "pair": "relations",
    "crime_status": "crime_watch",
}


@dataclass(frozen=True, slots=True)
class MetricReport:
    """The M1–M5 numbers + the emergent-chain count for one log.

    `m1` is a 0–1 share; `m2` is a 0–N ratio (released / seeded); `m3_mean`
    and `m3_median` are non-negative floats; `m4_repetition_rate` is 0–1
    (lower is better); `m4_distinct_knows_share` is 0–1 (higher is
    better); `m5` is 0–1. `emergent_chains` is the integer count of
    causal paths rooted in a player event with a non-PC, non-director
    tail of length ≥ 2 (`docs/TEST_PLAN.md` §1.2).
    """

    events: int
    m1_cross_system_share: float
    m2_hooks_fired_ratio: float
    m3_mean: float
    m3_median: float
    m4_repetition_rate: float
    m4_distinct_knows_share: float
    m5_non_pc_share: float
    emergent_chains: int
    extra: dict[str, Any] = field(default_factory=dict)


# -- system classification (pack-driven; prop-prefix is mechanic) -------------


def _system_of_type(
    pack_rules: Mapping[str, Any], event_type: str
) -> tuple[str, ...]:
    """The systems an event type inherently touches, from pack data.

    Pack data lives at `rules.json::metrics.system_of_type[type]` (a list
    of system names — an event can touch several). Unknown types return
    an empty tuple (the metric is unaffected; the type is just uncrossed
    by M1's type-side contribution — its state_changes still count).
    """
    table = pack_rules.get("metrics", {}).get("system_of_type", {})
    return tuple(table.get(event_type, ()))


def _system_of_prop(prop: str) -> str | None:
    """The system a `state_change.prop` belongs to, by dotted prefix.

    `position`, `relations.suspicion`, `status.fatigue`, `fire.<spot>`,
    `pair.<id>.<axis>`, `crime_status` — closed set of mechanic prefixes.
    Returns None for props outside this set (the metric just does not
    cross them into a system).
    """
    head = prop.split(".", 1)[0]
    return _PROP_PREFIX_TO_SYSTEM.get(head)


def systems_touched(
    pack_rules: Mapping[str, Any], event: EventRecord
) -> frozenset[str]:
    """The set of systems one event touches (its type + its state_changes).

    M1 counts events where `len(systems_touched) >= 2`.
    """
    systems: set[str] = set(_system_of_type(pack_rules, event.type))
    for change in event.state_changes:
        system = _system_of_prop(change.prop)
        if system is not None:
            systems.add(system)
    return frozenset(systems)


# -- M1 — cross-system share -------------------------------------------------


def m1_cross_system_share(
    pack_rules: Mapping[str, Any], events: Sequence[EventRecord]
) -> float:
    """Share of events touching ≥2 systems (`MVP_SCOPE.md` §15)."""
    if not events:
        return 0.0
    multi = sum(
        1 for event in events if len(systems_touched(pack_rules, event)) >= 2
    )
    return multi / len(events)


# -- M2 — deferred hooks fired -----------------------------------------------


def m2_hooks_fired_ratio(events: Sequence[EventRecord]) -> float:
    """Released director hooks / seeded hooks (the director's seed→release
    ratio). Computed on the ON-run log; the OFF run is 0 by construction.

    Released = events whose `provenance.cause_intent` starts with
    `director_`. Seeded = total hook instances across every event's
    `hooks` array (each tag is one seeded instance — a multi-hook event
    counts as multi-seeded).
    """
    seeded = sum(len(event.hooks) for event in events)
    if seeded == 0:
        return 0.0
    released = sum(
        1
        for event in events
        if str(event.provenance.get("cause_intent", "")).startswith("director_")
    )
    return released / seeded


# -- M3 — causal chain length ------------------------------------------------


def _chain_depth(events: Sequence[EventRecord]) -> list[int]:
    by_id = {event.id: event for event in events}
    depths: list[int] = []
    for event in events:
        depth = 0
        cur = event
        while cur.cause and cur.cause in by_id:
            cur = by_id[cur.cause]
            depth += 1
        depths.append(depth)
    return depths


def m3_causal_chain_lengths(
    events: Sequence[EventRecord]
) -> tuple[float, float]:
    """Mean and median depth of the `cause` chain per event."""
    if not events:
        return 0.0, 0.0
    depths = _chain_depth(events)
    return mean(depths), median(depths)


# -- M4 — novelty / repetition -----------------------------------------------


def m4_novelty_repetition(
    events: Sequence[EventRecord]
) -> tuple[float, float]:
    """Repetition rate of `(type, actor)` bigrams + distinct `knows` share.

    Returns `(repetition_rate, distinct_knows_share)`:
    - `repetition_rate` = share of bigrams that appear more than once
      (lower is better — RimWorld's repetitive-tale problem, measured).
    - `distinct_knows_share` = `len(distinct knows tokens) / len(knowledge
      records)` (higher is better — knowledge vocabulary is not stale).
    """
    if len(events) < 2:
        return 0.0, 0.0
    bigrams = [
        (events[i - 1].type, events[i - 1].actor, events[i].type, events[i].actor)
        for i in range(1, len(events))
    ]
    if not bigrams:
        repetition_rate = 0.0
    else:
        # bigrams that appear more than once / total bigrams
        counts: dict[tuple[str, str, str, str], int] = {}
        for bigram in bigrams:
            counts[bigram] = counts.get(bigram, 0) + 1
        repeated = sum(1 for c in counts.values() if c > 1)
        repetition_rate = repeated / len(counts)
    records = [k for event in events for k in event.knowledge]
    if not records:
        distinct_knows_share = 0.0
    else:
        distinct_knows_share = len({r.knows for r in records}) / len(records)
    return repetition_rate, distinct_knows_share


# -- M5 — non-PC event share -------------------------------------------------


def m5_non_pc_share(
    events: Sequence[EventRecord], player_id: str
) -> float:
    """Share of events whose actor ≠ the player (`MVP_SCOPE.md` §15).

    Computed on the OFF-run log; the director-off gate measures the
    "world not player-centered" Kenshi/RimWorld lesson. `world` counts
    (fire, smoke, burnout are world-actor events that moved without the
    PC's direct action); the run-start event has actor = player and is
    not counted.
    """
    if not events:
        return 0.0
    non_pc = sum(1 for event in events if event.actor != player_id)
    return non_pc / len(events)


# -- emergent chains (T8 operational definition, TEST_PLAN §1.2) -------------


def emergent_chains(
    events: Sequence[EventRecord], player_id: str
) -> list[tuple[str, int, list[str]]]:
    """Maximal causal paths rooted in a player event with a non-PC,
    non-director tail of length ≥ 2.

    Returns `(tail_event_id, chain_length, [type, type, ...])` per chain.
    A chain walks `cause` links from a non-PC, non-director event back to
    the player's own action (the seed); the chain length is the number of
    non-PC, non-director links traversed. A `world`-actor root (a fire
    ignited by the player's drop_break) counts as a chain root.
    """
    by_id = {event.id: event for event in events}
    chains: list[tuple[str, int, list[str]]] = []
    for event in events:
        if event.actor == player_id:
            continue
        if str(event.provenance.get("cause_intent", "")).startswith("director_"):
            continue
        chain: list[EventRecord] = [event]
        cur = event
        root: EventRecord | None = None
        while cur.cause and cur.cause in by_id:
            cur = by_id[cur.cause]
            if cur.actor == player_id:
                root = cur
                break
            if str(cur.provenance.get("cause_intent", "")).startswith("director_"):
                # director-injected link breaks the chain — the director
                # is causally upstream; this is not an emergent chain.
                root = None
                break
            chain.append(cur)
        if root is not None and len(chain) >= 2:
            chains.append(
                (event.id, len(chain), [c.type for c in chain])
            )
    return chains


# -- the one-shot report -----------------------------------------------------


def metrics_report(
    pack_rules: Mapping[str, Any],
    events: Sequence[EventRecord],
    projection: Projection,
    *,
    player_id: str,
    director_on: bool,
) -> MetricReport:
    """All five metrics + the emergent-chain count for one log.

    The `projection` argument is reserved for any future metric that
    needs final-state values (none of M1–M5 do today — they all fold the
    event stream — but the parameter pins the contract: the metric is a
    function of the log, never the simulator's runtime store).
    """
    del projection  # reserved — see docstring
    m3_mean_, m3_median_ = m3_causal_chain_lengths(events)
    rep_rate, distinct_knows = m4_novelty_repetition(events)
    chains = emergent_chains(events, player_id)
    return MetricReport(
        events=len(events),
        m1_cross_system_share=m1_cross_system_share(pack_rules, events),
        m2_hooks_fired_ratio=m2_hooks_fired_ratio(events) if director_on else 0.0,
        m3_mean=m3_mean_,
        m3_median=m3_median_,
        m4_repetition_rate=rep_rate,
        m4_distinct_knows_share=distinct_knows,
        m5_non_pc_share=m5_non_pc_share(events, player_id),
        emergent_chains=len(chains),
    )


def render_report(report: MetricReport, *, director_on: bool) -> str:
    """A one-block text rendering of a MetricReport (for the worklog / the
    balance harness output)."""
    return (
        f"events={report.events} | "
        f"M1={report.m1_cross_system_share:.3f} | "
        f"M2={report.m2_hooks_fired_ratio:.3f}{' (off)' if not director_on else ''} | "
        f"M3 mean={report.m3_mean:.2f} median={report.m3_median:.2f} | "
        f"M4 rep={report.m4_repetition_rate:.3f} "
        f"distinct_knows={report.m4_distinct_knows_share:.3f} | "
        f"M5={report.m5_non_pc_share:.3f} | "
        f"emergent_chains={report.emergent_chains}"
    )
