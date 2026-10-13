"""The goal/urge ticker (P2b, D-021, phase0 §4): NPC goals → occasional
autonomous action through the same queue and tick discipline as
playscript intents. Small-formula dynamics (KeeperRL rebellion): a few
numeric formulas over knowledge and state, not a planner. Full LLM
planning — never (`VISION.md` §6; Generative Agents is the cost
anti-precedent).

Urgencies are pack data: per-NPC goal specs with a probability roll
per beat, an intent template (kind / target / fields), and optional
precondition tests (the closed set in `core/intent.py`). A roll that
hits AND passes the preconditions yields an IntentData enqueued as
`kind="intent"` band `NPC_REACTION` — the front door validates it like
any playscript step. A roll that hits but fails preconditions stays
silent (the NPC tried, the world said no — no rejection event; the
world's noise floor absorbs autonomous attempts that don't fire).
Each entry rolls on its own `urgency:<npc>:<kind>` stream (engine-2,
D-079): canon-relevant, stream-isolated per entry from the checks.
The trait gate (beliefwire, iter-67) never touches that roll — the
belief filters AFTER the roll, a requires-GATE, never a probability
multiplier (D-095's own law).

Through-the-door discipline (D-037): urgencies never write canon
directly. They broadcast objectives through the intent door; the loop
runs the same front-door / OCC / resolver pipeline the player's
intents use. The world's logic is one mechanism, not two — M5
(non-PC event share) becomes non-trivially non-zero by construction.
"""

from __future__ import annotations

from bisect import insort
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Any, Final

from core.ids import sequence_id
from core.intent import (
    WINDOWED_TESTS,
    IntentData,
    ScanGateFold,
    ScanGateMemo,
    first_failing,
    pair_values,
    precondition_read_pairs,
)
from core.rng import urgency_stream_name

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.rng import RngBank
    from core.worldgen import WorldModel

__all__ = [
    "URGENCY_PREFIX",
    "RollIndex",
    "urgency_rolls",
    "urgency_intents",
    "urgency_scan",
    "urgency_specs",
]

URGENCY_PREFIX: Final = "urgency"


@dataclass(frozen=True, slots=True)
class _UrgencySpec:
    """One pack-declared urgency for one NPC (rules.json `urgencies.entries`).

    - `probability_per_beat` (0..100): d100 ≤ probability fires the
      intent attempt this beat.
    - `intent`: template for the IntentData (kind, optional target,
      fields).
    - `requires`: optional preconditions (the closed test set in
      `core/intent.py`). An attempt whose preconditions fail stays
      silent — the NPC tried, the world said no.
    - `stream` / `probe` (iter-370, the static-resolution family): the
      entry's stream NAME and gate PROBE, pre-built at parse time —
      pure over immutable pack data, byte-identical by construction.
      The per-beat walks re-derived both per call: the f-string name
      per rolling entry per beat and a fresh probe IntentData per
      gated entry per stretch (939K probe allocations on one h32
      profile) — the parse-once form is the `urgency_specs` memo's
      own class (E03), extended from the parse to its products. The
      probe IS the walk's intent: same id (`urgency_<seq>`), same
      fields, `based_on_event_seq=0` — the loop stamps the real seq at
      enqueue time via `dataclasses.replace`, so sharing the frozen
      object between the scan's gate evaluation and the walk's hit
      path changes no byte (the sharing law: `IntentData` is frozen
      and slots — no mutation path exists).
    - `pairs` (iter-375, the gate-answer memo): the DECLARED READ SET
      of the entry's `requires` (`precondition_read_pairs` — the occ-1
      read-pairs twin, sorted at parse), or None when the entry is
      ungated OR any require reads a time-dependent fold (the windowed
      family — the skip's fold-demand fence keeps such packs on the
      tick-by-tick path, and `None` keeps the scans exact even under a
      memo-passing caller: never memoized, always evaluated fresh).
      The parse sorts the pairs once — the memo key's order is a parse
      constant (INV-2's construction-order discipline).
    """

    npc: str
    probability_per_beat: int
    intent_kind: str
    intent_target: str | None
    intent_fields: Mapping[str, Any]
    requires: tuple[Mapping[str, Any], ...]
    stream: str
    probe: IntentData
    pairs: tuple[tuple[str, str], ...] | None


def _specs(pack: "Pack") -> tuple[_UrgencySpec, ...]:
    """Parse the pack's `urgencies.entries` (load order: pack-declared;
    the runner respects it as given — INV-2 via sorted() at load). The
    parse also builds each entry's STREAM name and gate PROBE (the
    static-resolution family, iter-370): both are pure functions of
    the entry — `urgency:<npc>:<kind>` and `urgency_<seq>` — so the
    parse-once form serves every later beat and stretch."""
    config = pack.rules.get("urgencies", {})
    entries = config.get("entries", ())
    specs: list[_UrgencySpec] = []
    for seq, entry in enumerate(entries):
        npc = entry["npc"]
        intent_kind = entry["intent"]["kind"]
        fields = dict(entry["intent"].get("fields", {}))
        target = entry["intent"].get("target")
        requires = tuple(entry.get("requires", ()))
        probe = IntentData(
            id=sequence_id(URGENCY_PREFIX, seq),
            kind=intent_kind,
            actor=npc,
            target=target,
            fields=fields,
            based_on_event_seq=0,
        )
        specs.append(
            _UrgencySpec(
                npc=npc,
                probability_per_beat=int(entry["probability_per_beat"]),
                intent_kind=intent_kind,
                intent_target=target,
                intent_fields=fields,
                requires=requires,
                stream=urgency_stream_name(npc, intent_kind),
                probe=probe,
                pairs=(
                    tuple(sorted(precondition_read_pairs(pack, probe, requires)))
                    if requires
                    and not any(
                        cond.get("test") in WINDOWED_TESTS for cond in requires
                    )
                    else None
                ),
            )
        )
    return tuple(specs)


def urgency_specs(pack: "Pack") -> tuple[_UrgencySpec, ...]:
    """The parse-once accessor (scale-1-impl, P0.5-B — the E03 fix):
    the same pure parse `_specs` owns, named for the LOOP's init-time
    memo. The beat machinery re-parsing the pack's rules every beat
    was the measured E03 waste (2.0 parses/beat, iter-328's
    instrument); the parse is pure over immutable pack data, so the
    memo is byte-identical by construction — the same specs, read
    once instead of per beat. iter-370 extends the same class from
    the parse to its PRODUCTS: the stream name and the gate probe
    ride the memoized specs, never re-derived per beat or stretch."""
    return _specs(pack)


class RollIndex:
    """The rolling-set index (iter-381, the standing order's
    rolling-filter row — the iter-362 index class applied to the
    family's per-spec filter walk): per-LOCATION buckets of the
    ``(position, spec)`` pairs whose NPC is present, positioned there,
    and uncaught — `urgency_rolls`'s own answers, pre-folded on the
    commit path. The scans and the beat walk read the bucket instead
    of calling the predicate per spec per call (the measured basis:
    urgency_rolls 1.67 profiled s / 2.63M calls on h32 10y — the
    scan 172 filter calls per stretch, the walk 172 per beat, ~72%
    of them passing).

    THE EXACTNESS LAW (this index's own discipline — the DecayIndex
    twin's staleness laws replaced by exact maintenance):

    - **Every cause of a rolling-verdict change rides a committed
      event's state change** — `position` (the bucket key) and
      `crime_status` (the caught veto). Presence is invariant: the
      commit door's gate raises on any state change to an entity
      outside the seed projection, so a spec NPC (a pack entity,
      seeded) is present for life. The fold re-derives the entity's
      whole membership from the LIVE bound state on every such
      change — remove-if-placed, place-iff-uncaught — so the answer
      after the last fold call of an event equals the predicate's
      answer on the final state, under ANY change order inside the
      event (a position change and a caught flip in one event, both
      orders; repeated same-prop changes — each call is a full
      re-derivation, the last one wins).
    - **The buckets are exact, never candidate.** No staleness, no
      defensive re-filter at read: the bucket IS the predicate's
      answer for the bound objects (the twin law the falsifier —
      tests/test_rollidx.py). A `list.remove` miss fails LOUD — a
      real invariant break, never a silent wrong answer.
    - **The pack order is the canon law.** The buckets hold
      ``(spec_position, spec)`` pairs sorted by the spec's position
      in the birth tuple — the filter form's iteration order (the
      walk's per-beat draw order — the counter words — and the
      scan's dict insertion order ride it); the single-location read
      returns the bucket itself, the None and multi-location reads
      sort the union (disjoint buckets — one spec sits in exactly
      one bucket).

    KI#16's law is the birth constraint (the SensesIndex/DecayIndex
    form): born from the pack-seeded INITIAL projection — the whole
    projection, seeds included. The identity gate (the
    ScanGateMemo/SensesIndex/DecayIndex law): `serves` answers True
    only for the exact projection and specs objects stamped at
    birth — every foreign caller keeps the predicate (the walks
    stay the semantic owners, D-024). Deterministic throughout
    (INV-2): zero draws, zero clock, construction-order birth scan,
    insort-ordered buckets. Rebuildable from the log (the buffer's
    law) — never exported in the run state; a resume re-births it
    from the restored projection."""

    __slots__ = ("_specs", "_spec_idxs", "_buckets", "_where", "_bound")

    def __init__(self, specs: "Sequence[_UrgencySpec]") -> None:
        self._specs = specs
        # npc -> its specs' positions in the birth tuple (ascending —
        # the enumerate order; ≤2 per npc on the committed packs)
        self._spec_idxs: dict[str, list[int]] = {}
        for idx, spec in enumerate(specs):
            self._spec_idxs.setdefault(spec.npc, []).append(idx)
        self._buckets: dict[Any, list[tuple[int, _UrgencySpec]]] = {}
        self._where: dict[str, Any] = {}  # npc -> the bucket key (placed)
        self._bound: "Projection | None" = None

    @classmethod
    def from_projection(
        cls,
        specs: "Sequence[_UrgencySpec]",
        projection: "Projection",
    ) -> "RollIndex":
        """The birth scan AND the identity stamp (the DecayIndex
        collapsed form: this index never folds a replay — a resume
        re-births from the restored state). Scans the specs in pack
        order (INV-2); every present, uncaught NPC's specs land in
        its position's bucket, insort-ordered by the spec position —
        the filter form's own iteration order."""
        index = cls(specs)
        for idx, spec in enumerate(specs):
            props = projection.get(spec.npc)
            if props is None:
                continue  # foreign projections only — see the class law
            if props.get("crime_status") == "caught":
                continue
            insort(
                index._buckets.setdefault(props.get("position"), []),
                (idx, spec),
            )
            index._where[spec.npc] = props.get("position")
        index._bound = projection
        return index

    def serves(
        self, projection: "Projection", specs: "Sequence[_UrgencySpec] | None"
    ) -> bool:
        """The identity gate: the scans' index branch serves ONLY the
        exact projection and specs objects stamped at birth (a None
        or a fresh parse keeps the predicate — the safe fallback for
        every existing caller)."""
        return (
            self._bound is not None
            and self._bound is projection
            and specs is not None
            and specs is self._specs
        )

    def apply_change(self, entity: str, prop: str) -> None:
        """Fold one committed state change (the `apply_event` twin,
        called AFTER the projection apply — the live read is the
        post-change state). Only `position` and `crime_status` can
        move a rolling verdict (the exactness law); everything else
        is a no-op. The re-derivation is exact under any in-event
        change order: remove-if-placed (wherever the index holds the
        entity), then place-iff-uncaught at the live position."""
        if prop != "position" and prop != "crime_status":
            return
        idxs = self._spec_idxs.get(entity)
        if idxs is None or self._bound is None:
            return
        if entity in self._where:
            bucket = self._buckets[self._where.pop(entity)]
            for idx in idxs:
                bucket.remove((idx, self._specs[idx]))  # loud on a break
        props = self._bound.get(entity)
        if props is None or props.get("crime_status") == "caught":
            return  # absent (foreign path) or caught: not placed
        position = props.get("position")
        bucket = self._buckets.setdefault(position, [])
        for idx in idxs:
            insort(bucket, (idx, self._specs[idx]))
        self._where[entity] = position

    def rolling(
        self, locations: "Collection[str] | None"
    ) -> "Sequence[tuple[int, _UrgencySpec]]":
        """The predicate's answers for the scope, in the filter form's
        own iteration order (the pack order). The single-location form
        — the loop's hot path — returns the bucket's own list (zero
        allocation; read-only by contract: the scans never commit
        inside). The None and multi-location forms sort the union of
        the named buckets (disjoint — one spec in exactly one
        bucket)."""
        if locations is None:
            return sorted(chain.from_iterable(self._buckets.values()))
        if len(locations) == 1:
            return self._buckets.get(next(iter(locations)), ())
        out: list[tuple[int, _UrgencySpec]] = []
        for loc in locations:
            out.extend(self._buckets.get(loc, ()))
        out.sort()
        return out


def urgency_rolls(
    spec: "_UrgencySpec",
    projection: "Projection",
    locations: Collection[str] | None,
) -> bool:
    """The rolling predicate — ONE law, TWO consumers (iter-337, H9):
    the entry rolls this walk iff its NPC is present in the projection,
    positioned inside the ticking zone, and not caught. The walk itself
    (`urgency_intents`) and the quiet-beat skip's rolling-set
    computation (the loop's `_quiet_landing`) read the SAME predicate —
    a diverging copy would desync the skip's counter arithmetic against
    the walk's draw pattern, so the filter lives here, extracted, never
    duplicated."""
    if spec.npc not in projection:
        return False
    if (
        locations is not None
        and projection[spec.npc].get("position") not in locations
    ):
        return False
    if projection[spec.npc].get("crime_status") == "caught":
        return False
    return True


def urgency_scan(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[_UrgencySpec] | None" = None,
    limit: int = 0,
    gate_memo: ScanGateMemo | None = None,
    roll_index: "RollIndex | None" = None,
    gate_fold: ScanGateFold | None = None,
) -> tuple[dict[str, int], int | None]:
    """H9's rolling-set + first-hit scan (iter-337): the data the
    loop's quiet-beat skip needs from THIS family, drawn from the same
    predicates and gates the walk itself uses — zero draws, zero
    enqueues. Returns ``(streams, first_fire)``:

    - ``streams`` maps every ROLLING entry's stream name to its
      per-beat draw count (1 — the walk draws once per rolling entry
      per beat, the hit/miss/gate outcome never changes the count);
    - ``first_fire`` is the smallest beat offset in ``[1, limit]`` at
      which the walk would ENQUEUE an intent — a hit whose ``requires``
      gates pass; a gate-failing hit stays silent and its beat stays
      quiet (the noise-floor law). ``None`` when nothing fires within
      the limit; ``1`` answers a probability-100 entry with open gates
      (fires the very first beat). The walk itself is ONE collective
      `RngBank.first_d100_hit` over the gate-open entries (iter-362,
      the walk half of iter-347's named address — the per-stream form
      walked every entry past the collective landing at density).

    All reads are against the FROZEN state the caller pinned: between
    two committed moments the projection, the folds, and the world
    cannot move, so ONE gate evaluation serves the whole stretch (the
    loop's fold-demand fence upstream makes this a law, never an
    approximation — no gate of a skip-capable pack reads a
    time-dependent fold).

    `gate_memo` (iter-375, the measured-wall head): the scan-family
    gate-answer memo — across stretches the frozen halves (pack,
    world, probe, requires) repeat and only the read-pair values
    move, so the verdict is served from the memo when the key (the
    live values at the spec's declared pairs) is unchanged and
    re-evaluated when it moved (the key comparison IS the
    invalidation; `ScanGateMemo`'s own law). None (the default) keeps
    the fresh evaluation — every existing caller unchanged.

    `roll_index` (iter-381, the rolling-filter row): the caller's
    `RollIndex` — the predicate's answers pre-folded on the commit
    path, served ONLY for the exact bound objects (`serves` — the
    identity gate; every other caller keeps the per-spec predicate,
    the semantic owner). The served entries arrive in the filter
    form's own iteration order — the pack order — so the streams/rolls
    dict insertion order and the collective walk's answers are
    identical by construction (the twin law the falsifier).

    `gate_fold` (iter-382, the key-build row): the memo's commit-path
    twin — the caller's `ScanGateFold`, served ONLY for the exact
    bound projection (the identity gate). A confirmed probe skips
    the key build and reads the stored verdict (`answer`); a declared
    pair write pops it (the pop law) and the key-compare path runs —
    THE SERVE LAW: the fast path serves exactly the verdict the key
    compare would, never more. None (the default) keeps the key
    compare — every existing caller unchanged."""
    if gate_memo is not None:
        gate_memo.bind(pack, world)
    fold = (
        gate_fold
        if gate_memo is not None
        and gate_fold is not None
        and gate_fold.serves(projection)
        else None
    )
    if roll_index is not None and roll_index.serves(projection, specs):
        entries: Sequence[tuple[int, _UrgencySpec]] = (
            roll_index.rolling(locations)
        )
    else:
        entries = [
            (idx, spec)
            for idx, spec in enumerate(
                _specs(pack) if specs is None else specs
            )
            if urgency_rolls(spec, projection, locations)
        ]
    streams: dict[str, int] = {}
    rolls: dict[str, int] = {}
    for _idx, spec in entries:
        streams[spec.stream] = 1
        if spec.probability_per_beat <= 0:
            continue  # rolls, never fires
        if spec.requires:
            if gate_memo is not None and spec.pairs is not None:
                open_gate = None
                if fold is not None:
                    entry = gate_memo.entry_at(spec.probe.id)
                    if entry is not None and fold.confirmed(
                        spec.probe.id, spec.pairs, entry
                    ):
                        open_gate = gate_memo.answer(spec.probe.id)
                if open_gate is None:
                    key = pair_values(projection, spec.pairs)
                    open_gate = gate_memo.lookup(spec.probe.id, key)
                    if open_gate is None:
                        open_gate = first_failing(
                            pack, projection, spec.probe, spec.requires,
                            facts=(), echoes=(), traits=(), world=world,
                        ) is None
                        gate_memo.store(spec.probe.id, key, open_gate)
                    if fold is not None:
                        fold.confirm(
                            spec.probe.id, spec.pairs,
                            gate_memo.entry_at(spec.probe.id),
                        )
            else:
                open_gate = first_failing(
                    pack, projection, spec.probe, spec.requires,
                    facts=(), echoes=(), traits=(), world=world,
                ) is None
            if not open_gate:
                continue  # the gates are shut for the whole stretch
        # the duplicate-(npc, kind) fold (iter-362): two entries on one
        # stream walk the same words — the max probability's first hit
        # IS the minimum over the entries' first hits (the monotonicity
        # law, `first_d100_hit`'s contract)
        if spec.probability_per_beat > rolls.get(spec.stream, 0):
            rolls[spec.stream] = spec.probability_per_beat
    first = bank.first_d100_hit(rolls, limit)
    return streams, first


def urgency_intents(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    locations: Collection[str] | None = None,
    world: "WorldModel | None" = None,
    specs: "Sequence[_UrgencySpec] | None" = None,
    roll_index: "RollIndex | None" = None,
) -> list[IntentData]:
    """One beat's worth of autonomous NPC intents (P2b). For each
    pack-declared urgency: roll d100 against `probability_per_beat`; on
    a hit, run the preconditions against the projection; if all pass,
    yield the IntentData. The loop enqueues them through the intent
    door (band NPC_REACTION) at the popped entry's tick, so they
    execute after the player's intents in the same tick (the
    entry-tick enqueue law, D-039).

    `facts` (iter-45, social-1b): the live leverage fold read at the
    BEAT tick — an urgency whose `requires` gate on `leverage_over`
    stays silent until the holder actually holds a live cluster (the
    same silent-skip law as any other world-impossible attempt; the
    front door re-validates at the entry tick with its own facts).
    `echoes` (iter-46, social-2): the residue fold read at the BEAT
    tick — an urgency whose `requires` gate on `echo_at_least` stays
    silent until the residue actually clears the bar (the same law;
    the behavior acts on the echo exactly as the P2b dependency
    names it, and the door re-validates with its own read).
    `traits` (iter-67, beliefwire — the v0.2 refinement family,
    D-095): the crystallized-trait fold read at the BEAT tick — an
    urgency whose `requires` gate on `trait_held` stays silent until
    the belief actually crystallizes (the same law; a GATE, never a
    probability multiplier — the roll already fired on the entry's
    own stream, the belief only filters; the door re-validates with
    its own read at the entry tick).

    `specs` (scale-1-impl, P0.5-B): the caller's PRE-PARSED specs
    (the loop's init-time memo via `urgency_specs`) — None (the
    default) keeps the standalone parse, so every existing caller
    is untouched; the memo is byte-identical (the parse is pure).

    depth-3 (the scene-LOD filter): `locations` scopes the entry walk
    to NPCs positioned there (the active zone at a beat, the warm ring
    at a macro crossing); None (the default) is the one-scene law —
    every entry, the unarmed world's per-beat behavior. roads-1:
    `world` threads the generated model for the adjacent_to gate (the
    ONE shared exits read — an autonomous move along a derived edge
    passes the gate); None is the unarmed default.

    `roll_index` (iter-381): the caller's `RollIndex` — the rolling
    filter's answers pre-folded on the commit path, served ONLY for
    the exact bound objects (the identity gate; every other caller
    keeps the predicate). The served order is the filter form's own
    — the pack order — so the per-beat draw sequence (each entry's
    own stream, the counter words) is identical by construction."""
    if roll_index is not None and roll_index.serves(projection, specs):
        entries: Sequence[tuple[int, _UrgencySpec]] = (
            roll_index.rolling(locations)
        )
    else:
        entries = [
            (idx, spec)
            for idx, spec in enumerate(
                _specs(pack) if specs is None else specs
            )
            if urgency_rolls(spec, projection, locations)
        ]
    out: list[IntentData] = []
    for _idx, spec in entries:
        # the roll: d100 <= probability, on the entry's OWN urgency-family
        # stream `urgency:<npc>:<kind>` (engine-2, D-079) — canon-relevant
        # but stream-isolated PER ENTRY, nested inside the run's assured
        # substantive scope: an added or removed entry shifts neither a
        # later check draw (the iter-49 measurement flipped 3 corpus
        # ladders at one added entry) nor another entry's rolls (the
        # single shared urgency stream was measured and refused — the
        # entries coupled by draw position; the per-entry streams buy
        # permanent add-safety for pack urgency growth). iter-370: the
        # draw rides `family_randint` — the fused assure+randint form
        # (same word, same counter position, same nesting law; the
        # with-scope machinery was the measured per-beat overhead)
        roll = bank.family_randint(spec.stream, 1, 100)
        if roll > spec.probability_per_beat:
            continue
        intent = spec.probe
        if spec.requires:
            failing = first_failing(
                pack, projection, intent, spec.requires,
                facts=facts, echoes=echoes, traits=traits, world=world,
            )
            if failing is not None:
                continue  # the world said no — silent, no rejection event
        out.append(intent)
    return out
