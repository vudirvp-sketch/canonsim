"""The knowledge system (phase0 §3): per-knower memory as a DERIVED index
over the log (L3 — `known_by` is never stored; the fold of knowledge
records IS the memory, Generative Agents' append-only stream with the
channel axis they lacked). The runtime keeps the index incrementally
(`KnowledgeView.add` per committed event); `from_events` rebuilds it from
any log — the T2 truth-test applies to it exactly as to the projection.

Mechanics (every name and number that is not a mechanic lives in the pack):

- **Salience** (P2c, D-033): a teller's most important, then most recent,
  record — knowledge *used*, not just stored. Records born on the
  triggering conversation never count (the teller shares what they knew
  before it).
- **Transfer** (D-007): fidelity decays one step down the pack's chain,
  channel `told`, never further than the chain floor — distortion from
  source incompleteness, not a rumor system.
- **Telling reaction**: a conversation whose event type matches the pack's
  `telling.on_event` makes the teller share their most salient facts the
  listener does not already hold; acceptance rolls d100 against
  base + trust weight − teller status penalty (all pack numbers). Trust is
  read from the pair map first (P2a), then the toward-the-player axis,
  else the pack neutral — the Influence Boundary holds (EPIST-1): only
  the listener's own trust and the teller's own status feed the roll.
- **Rumor drift** (A2'', rumordrift, iter-68a): a told fact whose token
  rides a pack-declared `knowledge.drift` family may mutate to a sibling
  token — the family's fidelity-ladder profile gives the chance at the
  RECEIVED fidelity (the vaguer the record, the likelier the drift). The
  roll rides the family's own `drift:<family>` stream (isolation is law,
  D-095: arming a family shifts neither a canon check draw nor another
  family's rolls); the outcome's `drifted_from` names the pre-drift token
  (EVENT_SCHEMA §11: an outcome payload addition, no bump). An undeclared
  block drifts nothing — v0.1 bytes (the pack's own declaration is the
  arming, INV-3; the pack arming is 68b). The official watch briefing
  (crime_watch, D-006) never drifts — handovers transfer verbatim.
- **Expectation checks** (P2d, KI#3): pack behaviour rules generate
  per-NPC expectations (an item carried by someone / lying at a location);
  a mismatch at check time emits an `inferred` record cause-chained to the
  event that moved the item on the violated axis — the only legal route
  to suspicion-from-absence: an absence is knowable only as a violated
  expectation, never as "not seen".
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.intent import pack_importance
from core.log import (
    EventDraft,
    EventRecord,
    Fidelity,
    KnowledgeRecord,
    LoggedKnowledgeRecord,
)
from core.rng import RngBank, drift_stream_name

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "DriftFamily",
    "KnowledgeView",
    "acceptance_score",
    "decay_fidelity",
    "drift_families",
    "drifted_knows",
    "expectation_drafts",
    "telling_reaction",
    "trust_toward",
]

_IMPORTANCE_RANK: Final[Mapping[str, int]] = {"low": 0, "medium": 1, "high": 2}
TOLD: Final = "told"  # channel for transfers (EVENT_SCHEMA §3)
INFERRED: Final = "inferred"  # channel for expectation violations (P2d)
SALIENCE_RULES: Final = ("importance_then_recency",)  # closed set, v0.1


@dataclass(frozen=True, slots=True)
class _Row:
    """One knowledge row plus its source event's importance (salience input)."""

    record: LoggedKnowledgeRecord
    importance: str


class KnowledgeView:
    """The derived per-knower memory index (L3). Rebuildable from any log;
    the runtime updates it inside the commit door, one event at a time.

    scale-1-impl P1b (the wall fix's second member): the ranked
    iteration rides the RANK-BUCKET index (`_runs`) — per knower,
    per importance rank, an ordered list of TIE-RUNS (maximal groups
    of rows sharing one event tick) — so `_ranked` walks the exact
    stable-sort order (rank DESC, then tick DESC, ties in arrival
    order) with ZERO comparisons; the per-beat re-sort was the
    measured quadratic member (`_ranked` per-call ×10.02,
    `list.sort` ×8.61 at 100y, iter-327/328). The order is exact
    because event ticks never regress (the writer's own law,
    `core/log.py`'s tick-regression refusal) — a new row either
    extends the last tie-run of its rank or starts a new one.
    The (teller, listener) NOVELTY COUNT (`_novelty`, maintained
    with `add` over the inverted token-holder index) answers the
    saturated teller in O(1): zero novel rows → no walk at all
    (the whole-knowledge re-ranking per talk was the measured
    cost, ×9.17 per-call growth)."""

    def __init__(self) -> None:
        self._rows: dict[str, list[_Row]] = {}
        # Token novelty index (who -> token -> source event ids), derived
        # with `add` as its only writer — `holds` is O(1) instead of a row
        # scan; the same funnel feeds it on replay (`from_events`).
        self._sources: dict[str, dict[str, set[str]]] = {}
        # P1b: per knower, per rank, the ordered tie-runs (the ranked
        # order without the sort — see the class docstring).
        self._runs: dict[str, dict[int, list[list[_Row]]]] = {}
        # P1b: token -> the knowers holding it (the inverted holder
        # index the novelty bookkeeping walks).
        self._token_holders: dict[str, set[str]] = {}
        # P1b: teller -> listener -> the count of the teller's rows
        # whose token the listener does NOT hold (the O(1) saturated
        # answer; maintained by `add`, born-correct for late knowers).
        self._novelty: dict[str, dict[str, int]] = {}
        # P1b: knower -> token -> how many rows of that token they
        # hold (the decrement weights for the novelty count).
        self._rows_by_token: dict[str, dict[str, int]] = {}

    def add(self, event: EventRecord) -> None:
        """Absorb one committed event's records (acquisition order)."""
        for record in event.knowledge:
            who = record.who
            # P1b: a knower's FIRST row initializes their novelty
            # column for every existing teller — the newborn holds
            # nothing, so every teller's rows count as unheld (the
            # incremental counts would otherwise miss pre-birth rows)
            if who not in self._rows:
                for teller, rows in self._rows.items():
                    self._novelty.setdefault(teller, {})[who] = len(rows)
            held_before = (
                record.knows in self._sources.get(who, {})
            )
            row = _Row(record=record, importance=event.importance)
            self._rows.setdefault(who, []).append(row)
            self._sources.setdefault(who, {}).setdefault(
                record.knows, set()
            ).add(record.source)
            # P1b: the bucket append — `at` never regresses (the
            # writer's tick-regression law), so the row either
            # extends the rank's last tie-run or starts a new one;
            # the iteration order is then exactly the stable sort's
            runs = (
                self._runs.setdefault(who, {})
                .setdefault(_IMPORTANCE_RANK[event.importance], [])
            )
            if runs and runs[-1][0].record.at == record.at:
                runs[-1].append(row)
            else:
                runs.append([row])
            self._rows_by_token.setdefault(who, {}).setdefault(
                record.knows, 0
            )
            self._rows_by_token[who][record.knows] += 1
            # P1b: the row is novel to every knower who does not hold
            # its token
            for listener in self._rows:
                if listener == who:
                    continue
                if record.knows not in self._sources.get(listener, {}):
                    counts = self._novelty.setdefault(who, {})
                    counts[listener] = counts.get(listener, 0) + 1
            # P1b: `who` newly holds the token — every teller's rows
            # of it leave their novelty counts for `who`
            if not held_before:
                for teller in self._token_holders.get(record.knows, ()):
                    if teller == who:
                        continue
                    weight = self._rows_by_token.get(teller, {}).get(
                        record.knows, 0
                    )
                    if weight:
                        counts = self._novelty.setdefault(teller, {})
                        counts[who] = counts.get(who, 0) - weight
            self._token_holders.setdefault(record.knows, set()).add(who)

    @classmethod
    def from_events(cls, events: Sequence[EventRecord]) -> KnowledgeView:
        """Rebuild from a log (the T2 truth-test path)."""
        view = cls()
        for event in events:
            view.add(event)
        return view

    def knowers(self) -> tuple[str, ...]:
        """Who holds anything, in first-acquisition order."""
        return tuple(self._rows)

    def records_of(self, who: str) -> tuple[LoggedKnowledgeRecord, ...]:
        """Everything `who` knows, in acquisition order (their memory)."""
        return tuple(row.record for row in self._rows.get(who, ()))

    def holds(self, who: str, token: str, *, before_source: str | None = None) -> bool:
        """Whether `who` holds `token` — optionally only from events other
        than `before_source` (the novelty test for reactions: a record does
        not count as old knowledge merely because it just got written).
        O(1) through the token index: a token learned only from the
        excluded source is NOT held."""
        sources = self._sources.get(who, {}).get(token)
        if not sources:
            return False
        if before_source is None:
            return True
        return any(source != before_source for source in sources)

    def _ranked(
        self, who: str, *, exclude_source: str | None
    ) -> Iterator[LoggedKnowledgeRecord]:
        """The knower's records, best salience first (importance, then
        recency; the newest of equals wins) — the RANK-BUCKET
        iteration (P1b): ranks DESC, tie-runs newest-first, arrival
        order within a run — EXACTLY the stable sort's order, with
        zero comparisons (the per-call re-sort was the measured
        quadratic member; the structure is maintained by `add`)."""
        runs_by_rank = self._runs.get(who)
        if not runs_by_rank:
            return iter(())

        def generate() -> Iterator[LoggedKnowledgeRecord]:
            for rank in sorted(runs_by_rank, reverse=True):
                for run in reversed(runs_by_rank[rank]):
                    for row in run:
                        if (
                            exclude_source is not None
                            and row.record.source == exclude_source
                        ):
                            continue
                        yield row.record

        return generate()

    def salient(
        self, who: str, *, exclude_source: str | None = None
    ) -> LoggedKnowledgeRecord | None:
        """The most salient record (P2c) — or None for a blind knower.
        Top-1 of the `_ranked` order (importance, then recency); `max`
        returns the first of equals, exactly what the stable reverse sort
        put at index 0 — so the O(K log K) sort is not paid for one pick."""
        rows = [
            row
            for row in self._rows.get(who, ())
            if exclude_source is None or row.record.source != exclude_source
        ]
        if not rows:
            return None
        best = max(
            rows, key=lambda row: (_IMPORTANCE_RANK[row.importance], row.record.at)
        )
        return best.record


# -- transfer (one-step fidelity decay, D-007) --------------------------------


def decay_fidelity(fidelity: Fidelity, chain: Sequence[Fidelity], steps: int = 1) -> Fidelity:
    """`steps` down the pack's fidelity chain; the chain floor sticks."""
    if fidelity not in chain:
        raise ValueError(f"unknown fidelity {fidelity!r} (chain: {list(chain)})")
    index = min(chain.index(fidelity) + max(steps, 0), len(chain) - 1)
    return chain[index]


# -- rumor drift (A2'', rumordrift iter-68a) ----------------------------------


DRIFT_SPEC_KEYS: Final = ("tokens", "ladder", "notes")  # closed set, pack-linted


@dataclass(frozen=True, slots=True)
class DriftFamily:
    """One pack-declared drift family: the orbit of tokens the rumor path
    may substitute (pack order — the target pick is deterministic), plus
    the fidelity-ladder chance profile (received fidelity → d100 chance).
    Built by `drift_families` from `rules.json::knowledge.drift`."""

    family: str
    tokens: tuple[str, ...]
    ladder: Mapping[str, int]


def drift_families(pack: Pack) -> dict[str, DriftFamily]:
    """The token → family index over `rules.json::knowledge.drift` (the
    lint's one-sided membership law makes it a function, never a
    one-to-many). An absent or empty block answers the empty index — the
    telling path then never rolls, byte-identical v0.1 (the pack's own
    declaration is the arming; the committed pack declares none until 68b)."""
    config = pack.rules.get("knowledge", {}).get("drift")
    if not config:
        return {}
    index: dict[str, DriftFamily] = {}
    for family, spec in config.items():  # pack order — deterministic
        entry = DriftFamily(
            family=family,
            tokens=tuple(spec["tokens"]),
            ladder=spec["ladder"],
        )
        for token in entry.tokens:
            index[token] = entry
    return index


def drifted_knows(
    bank: RngBank,
    families: Mapping[str, DriftFamily],
    token: str,
    fidelity: str,
) -> str:
    """The token a transferred record carries after the drift gate: a
    family member rolls d100 at the RECEIVED fidelity's ladder chance — a
    miss keeps the token (the roll still consumed its draw: the urgency
    law, the count never depends on the ladder's numbers); a hit picks
    one uniform OTHER member (one draw). Both draws ride the family's own
    `drift:<family>` stream, nested inside the run's assured substantive
    scope — isolation is law (D-095): the drift never shifts a canon
    check draw or another family's rolls, and the fingerprint never sees
    it. A token outside every family answers itself — no roll, no stream."""
    entry = families.get(token)
    if entry is None:
        return token
    with bank.assure(drift_stream_name(entry.family)):
        if bank.randint(1, 100) > entry.ladder[fidelity]:
            return token
        source = entry.tokens.index(token)
        pick = bank.randint(0, len(entry.tokens) - 2)
    return entry.tokens[pick] if pick < source else entry.tokens[pick + 1]


def trust_toward(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    listener: str,
    teller: str,
    axis: str,
) -> int:
    """The listener's trust in the teller: the pair map first (P2a), then
    the toward-the-player relations axis (v0.1 semantics), else neutral."""
    value = projection.get(listener, {}).get(f"pair.{teller}.{axis}")
    if value is None and teller == pack.player_id():
        value = projection.get(listener, {}).get(f"relations.{axis}")
    if value is None:
        value = pack.rules["relations"]["neutral"]
    return int(value)


def acceptance_score(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    teller: str,
    listener: str,
) -> int:
    """Base + trust weight − teller status penalty; every number is pack
    data (`rules.knowledge.rumor_acceptance`)."""
    config = pack.rules["knowledge"]["rumor_acceptance"]
    score = int(config["base"])
    score += int(
        float(config["trust_weight"])
        * trust_toward(pack, projection, listener, teller, config["trust_axis"])
    )
    penalty_value = projection.get(teller, {}).get(
        f"status.{config['teller_penalty_axis']}"
    )
    if isinstance(penalty_value, (int, float)) and not isinstance(penalty_value, bool):
        score += int(config["teller_penalty_per_10"]) * (int(penalty_value) // 10)
    return score


# -- the telling reaction (P2c: talk topic = the teller's most salient fact) ---


def _novel_facts(
    view: KnowledgeView,
    teller: str,
    listener: str,
    exclude_source: str,
    limit: int,
) -> list[LoggedKnowledgeRecord]:
    """The teller's salient facts the listener does not already hold,
    best first, at most `limit` (dedup by token — a listener never re-learns).

    P1b: the O(1) saturated answer — the (teller, listener) novelty
    count says ZERO unheld rows, so the walk (a subset of the rows —
    it additionally excludes one source) can pick nothing; sound
    because `holds` is monotone (knowledge is append-only, the
    forgetting vocabulary absent by P7's law) and the count is
    maintained on the same `add` funnel."""
    if view._novelty.get(teller, {}).get(listener, 0) == 0:
        return []
    picks: list[LoggedKnowledgeRecord] = []
    taken: set[str] = set()
    for record in view._ranked(teller, exclude_source=exclude_source):
        if record.knows in taken or view.holds(listener, record.knows):
            continue
        picks.append(record)
        taken.add(record.knows)
        if len(picks) >= limit:
            break
    return picks


def telling_reaction(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    view: KnowledgeView,
    bank: RngBank,
    record: EventRecord,
) -> EventDraft | None:
    """Draft the transfer a successful conversation triggers (P2c): the
    teller shares their most salient novel fact; the listener receives it
    told, one fidelity step down (D-007). None when the pack declares no
    telling, the event type does not match, or the teller has nothing new
    to say — a blind NPC cannot say anything (T3)."""
    config = pack.rules["knowledge"].get("telling")
    if config is None or record.type != config["on_event"]:
        return None
    teller = record.target if config["teller"] == "target" else record.actor
    listener = record.actor if config["listener"] == "actor" else record.target
    if teller is None or listener is None or teller == listener:
        return None
    picks = _novel_facts(
        view, teller, listener, exclude_source=record.id, limit=int(config["facts"])
    )
    if not picks:
        return None
    chain = pack.rules["knowledge"]["fidelity_chain"]
    score = acceptance_score(pack, projection, teller, listener)
    accepted = bank.randint(1, 100) <= score
    # the drift gate runs only on ACCEPTED records — a refused telling
    # transfers nothing, so nothing mutates (the drift draw count is a
    # function of the log's acceptances, never of the ladder's numbers)
    families = drift_families(pack)
    records: list[KnowledgeRecord] = []
    drifted_from: str | None = None
    if accepted:
        for index, pick in enumerate(picks):
            received = decay_fidelity(pick.fidelity, chain)
            knows = drifted_knows(bank, families, pick.knows, received)
            if index == 0 and knows != pick.knows:
                drifted_from = pick.knows
            records.append(
                KnowledgeRecord(
                    who=listener,
                    channel=TOLD,
                    fidelity=received,
                    knows=knows,
                    at=record.t,
                )
            )
    outcome: dict[str, Any] = {
        "accepted": accepted,
        "score": score,
        "knows": records[0].knows if records else picks[0].knows,
        "fidelity": (
            records[0].fidelity
            if records
            else decay_fidelity(picks[0].fidelity, chain)
        ),
    }
    if drifted_from is not None:
        outcome["drifted_from"] = drifted_from
    return EventDraft(
        t=record.t,
        type=config["event"],
        actor=teller,
        target=listener,
        cause=None,  # the loop chains the cause to the triggering event
        outcome=outcome,
        knowledge=tuple(records),
        importance=pack_importance(
            pack.rules, {teller, listener}, irreversible=0, hooks=0,
            event_type=config["event"],
        ),
    )


# -- expectation checks (P2d, KI#3) -------------------------------------------


def _rule_holds(
    projection: Mapping[str, Mapping[str, Any]], rule: Mapping[str, Any]
) -> bool:
    item = projection[rule["item"]]
    if "carried_by" in rule:
        return bool(item.get("carrier") == rule["carried_by"])
    return bool(item.get("position") == rule["at_location"])


def _last_moving_event(
    events: Sequence[EventRecord], rule: Mapping[str, Any]
) -> EventRecord:
    """The latest event that moved the item on the rule's axis (carrier for
    carried-by expectations, position for at-location ones) — the violation
    chains its cause there (the honest originating event, not the last
    thing that merely touched the item)."""
    prop = "carrier" if "carried_by" in rule else "position"
    for event in reversed(events):
        if any(
            change.entity == rule["item"] and change.prop == prop
            for change in event.state_changes
        ):
            return event
    raise ValueError(
        f"expectation {rule.get('knows')!r} is broken but no event ever moved "
        f"{rule['item']!r}.{prop} — the pack lint guarantees rules hold at t=0, "
        f"so a violation without a mover is a simulator bug"
    )


def expectation_drafts(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    view: KnowledgeView,
    events: Sequence[EventRecord],
    tick: int,
) -> tuple[EventDraft, ...]:
    """P2d: compare each pack-declared expectation against the projection;
    a mismatch the NPC does not already know about emits an
    `inferred`-channel record cause-chained to the event that moved the
    item. Location-bound expectations require the NPC on site (perception);
    carried-by expectations check anywhere (their own pocket)."""
    config = pack.rules.get("expectations")
    if config is None:
        return ()
    drafts: list[EventDraft] = []
    for rule in config.get("rules", ()):  # pack order — deterministic
        npc = rule["npc"]
        if "at_location" in rule and projection[npc]["position"] != rule["at_location"]:
            continue  # not on site: the absence stays unobserved
        if _rule_holds(projection, rule):
            continue
        if view.holds(npc, rule["knows"]):
            continue  # already noticed — no duplicate violations
        expected = (
            {"carried_by": rule["carried_by"]}
            if "carried_by" in rule
            else {"at_location": rule["at_location"]}
        )
        observed_prop = "carrier" if "carried_by" in rule else "position"
        observed = {observed_prop: projection[rule["item"]].get(observed_prop)}
        cause = _last_moving_event(events, rule)
        drafts.append(
            EventDraft(
                t=tick,
                type=config["event"],
                actor=npc,
                target=rule["item"],
                cause=cause.id,  # chained to the originating event (P2d)
                outcome={"expected": expected, "observed": observed},
                knowledge=(
                    KnowledgeRecord(
                        who=npc,
                        channel=INFERRED,
                        fidelity="exact",
                        knows=rule["knows"],
                        at=tick,
                    ),
                ),
                importance=pack_importance(
                    pack.rules, {npc, rule["item"]}, irreversible=0, hooks=0,
                    event_type=config["event"],
                ),
            )
        )
    return tuple(drafts)
