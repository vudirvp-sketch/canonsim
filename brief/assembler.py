"""The deterministic brief assembler (BRIEF-1, phase 1 — `docs/BRIEF_SPEC.md`
owns the field-level contract; `docs/blueprint/phases.md` §1 owns the donor
design).

The brief is the mediator's input document: eight typed blocks with token
budgets, assembled fresh every beat. This module is the LLM-free half —
**a pure function of (log, ledger)** (the D-042/D-043/D-044 read-side
family, widened iter-10 by the D-049 determinism quarantine): same log +
same ledger + same pack → same brief bytes in any process, any call
order, any `PYTHONHASHSEED`. The ledger is session render state — never
canon, never replayed; canon replay (T1/T2) never touches it. Unlike the
chronicle there is **no randomness at all** — every block iterates
construction order or an explicit sort over deterministic inputs (INV-2);
the brief carries facts as structured tokens, never prose (L2 — voice
lives only in the exemplar block). The assembler writes nothing to the
log (INV-1) and imports no network code (INV-4 — the narrator itself is
a later, owner-gated iteration).

The knower parameter (scene-1, mode B — BRIEF_SPEC §3.9): mode A
(knower=None, the player) is the committed corpus shape, byte-identical
by construction; mode B (knower=<npc>) runs the SAME pipeline for an
actor — its own perception (scene_delta), its own memory
(recalled_facts), its own role text and voice (the pack's
`brief.actors` entry) — the per-NPC brief's leak surface closed by
construction, the chorus served one knower per call
(`brief/scene.py::speaking_queue`).

All setting text and every budget number lives in the pack
(`rules.json::brief`, linted at load — `core/pack.py`); this module knows
block ids and the eviction order, which are architecture (BRIEF_SPEC §5.2),
not balance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from brief.ledger import (
    CONTRADICTED,
    ENTITY_SCOPE_PREFIX,
    LIVE_STATUSES,
    PINNED,
    LedgerEntry,
    SceneLedger,
    current_scene,
    present_entities,
    split_scope,
)
from core.fold import fold, initial_projection, present_in_order
from core.knowledge import KnowledgeView
from core.log import EventRecord, read_log
from core.pack import BRIEF_BLOCK_IDS, Pack
from core.retrieval import word_tokens
from core.traits import Trait, crystallized_traits
from render.chronicle import display_name

__all__ = [
    "Block",
    "Brief",
    "assemble_brief",
    "beats_crossed",
    "brief_from_log",
    "last_beat_tick",
    "render_brief",
    "token_count",
]

# Ascending-priority eviction order for whole-block eviction on total
# overflow (BRIEF_SPEC §5.2). Directives are NOT in it — never evicted;
# scene_texture sits between scene_delta and present_entities (current-scene
# continuity outranks lore; canon-projection structure — the entity cards —
# outranks narrator-invented texture: canon always outranks texture,
# D-049), both below voice/options — st-1.
EVICTABLE_BLOCKS: Final = (
    "scheduled_lore",
    "recalled_facts",
    "scene_delta",
    "scene_texture",
    "present_entities",
    "voice_exemplars",
    "active_options",
)
_TRUNCATED: Final = "[truncated:{n} items dropped]"
_IMPORTANCE_RANK: Final = {"low": 0, "medium": 1, "high": 2}


@dataclass(frozen=True, slots=True)
class Block:
    """One assembled block: the item lines that survived, and how many
    did not (fill law, whole-block eviction — BRIEF_SPEC §5)."""

    block_id: str
    lines: tuple[str, ...]
    dropped: int

    def render(self) -> list[str]:
        """Header + body + the truncation marker when anything dropped."""
        lines = [f"## {self.block_id}"]
        lines.extend(self.lines)
        if self.dropped:
            lines.append(_TRUNCATED.format(n=self.dropped))
        return lines


@dataclass(frozen=True, slots=True)
class Brief:
    """The eight blocks in pipeline order (BRIEF_SPEC §3)."""

    blocks: tuple[Block, ...]


# -- the token model (BRIEF_SPEC §4) ------------------------------------------


def token_count(text: str) -> int:
    """Whitespace tokens — the deterministic, dependency-free proxy.

    The real tokenizer arrives with the LLM circuit and must not change
    committed formats without a spec bump (BRIEF_SPEC §4/§8).
    """
    return len(text.split())


# -- beat arithmetic (the read-side mirror of core/loop.py's forward law) ------


def _beat_offsets(rules: Mapping[str, Any]) -> tuple[int, ...]:
    """Intraday beat offsets, ascending — `urgencies.beat_ticks` is the
    single owner of the beat cycle (one beat, three pieces — D-037)."""
    return tuple(sorted(rules.get("urgencies", {}).get("beat_ticks", ())))


def last_beat_tick(rules: Mapping[str, Any], tick: int) -> int | None:
    """The largest beat tick <= `tick`, or None when no beat crossed yet.

    Beats are the pack's intraday offsets repeated every
    `time.ticks_per_day`; a beat at t=0 never fires (the loop's day-1
    edge, `core/loop.py` `_first_beat`) — this is the backward mirror of
    that forward scheduling law, for the scene-delta window.
    """
    offsets = _beat_offsets(rules)
    day = int(rules["time"]["ticks_per_day"])
    best: int | None = None
    for offset in offsets:
        if offset > 0:
            if tick >= offset:
                candidate = offset + ((tick - offset) // day) * day
                best = candidate if best is None or candidate > best else best
        elif day <= tick:  # offset == 0: fires from day 1 onward only
            candidate = (tick // day) * day
            best = candidate if best is None or candidate > best else best
    return best


def beats_crossed(rules: Mapping[str, Any], tick: int) -> int:
    """How many beat boundaries lie at or before `tick` (the lore schedule
    input, BRIEF_SPEC §3.6) — same beat set as `last_beat_tick`."""
    offsets = _beat_offsets(rules)
    day = int(rules["time"]["ticks_per_day"])
    crossed = 0
    for offset in offsets:
        if offset > 0:
            if tick >= offset:
                crossed += (tick - offset) // day + 1
        else:
            crossed += tick // day  # k >= 1 only: the t=0 beat never fires
    return crossed


# -- per-block assembly --------------------------------------------------------


def _fill(block_id: str, items: Sequence[str], budget: Mapping[str, Any]) -> Block:
    """The fill law (BRIEF_SPEC §5.1): take best-first while below the
    soft target AND the item fits the hard ceiling; everything else
    counts as dropped. Items are never cut mid-line; the marker is
    metadata and always renders (silent drops are forbidden)."""
    soft = int(budget["soft"])
    hard = int(budget["hard"])
    taken: list[str] = []
    tokens = 0
    dropped = 0
    for line in items:
        cost = token_count(line)
        if tokens < soft and tokens + cost <= hard:
            taken.append(line)
            tokens += cost
        else:
            dropped += 1
    return Block(block_id, tuple(taken), dropped)


def _scene_delta_lines(
    events: Sequence[EventRecord], pack: Pack, *, knower: str
) -> list[str]:
    """What the knower perceived since the last beat, newest first
    (BRIEF_SPEC §3.2): the knower is the actor or holds a record born on
    the event (the blind-NPC law — no record, no delta line). Mode A
    passes the player; mode B passes the actor (scene-1 — the same law,
    one knower, never a world dump)."""
    window_start = last_beat_tick(pack.rules, events[-1].t if events else 0)
    lines: list[str] = []
    for event in reversed(events):  # newest first — recency dominates
        if window_start is not None and event.t <= window_start:
            break  # ticks are log-monotonic: older events are past the window too
        perceived = event.actor == knower or any(
            record.who == knower for record in event.knowledge
        )
        if not perceived:
            continue
        line = f"[t {event.t}] {event.type}: {display_name(pack, event.actor)}"
        if event.target is not None:
            line += f" -> {display_name(pack, event.target)}"
        lines.append(line)
    return lines


def _belief_lines(
    traits: Sequence[Trait], events: Sequence[EventRecord]
) -> list[str]:
    """The derived-trait read's item lines (BRIEF_SPEC §3.5, the phase-4
    clause): one line per crystallized belief, declaration order (the
    fold's order for one knower) — the belief carries its provenance
    event ids, the expansion law's demand handle; the cross tick is the
    threshold crossing (the latest source event's t). Dry ids, never
    prose: the line is an address into the log, not a narrative."""
    tick_of = {event.id: event.t for event in events}
    lines: list[str] = []
    for trait in traits:
        cross = max((tick_of.get(sid, 0) for sid in trait.sources), default=0)
        sources = ", ".join(trait.sources)
        lines.append(f"- belief {trait.token} (t {cross}, sources: {sources})")
    return lines


def _recalled_fact_lines(
    events: Sequence[EventRecord], pack: Pack, *, knower: str,
    query: str | None = None,
) -> list[str]:
    """The knower's own knowledge, ranked by the Generative-Agents
    signal shape (BRIEF_SPEC §3.5): recency + importance always, plus
    relevance when the mediator's query rides the assembly (scene-2,
    mode B — the token-overlap match of the query's words against the
    record's `knows` words; `query=None` is mode A's two-signal shape,
    the committed corpus bytes), deduped by token, capped at
    `max_items` — and read through the derived-trait lens (leg-2, the
    phase-4 clause): the knower's crystallized beliefs lead the block
    as belief lines, and the family records that minted them render
    nothing raw — the belief is the derived view, the source records
    stay queryable on demand via the provenance ids (the expansion
    law, `core/traits.py::expand_trait`). Size O(traits + records),
    never O(history). Mode A passes the player; mode B passes the
    actor (scene-1 — the per-NPC brief's leak surface: a record the
    knower does not hold can never render, by construction — the
    records ARE the knower's fold)."""
    config = pack.rules["brief"]["recalled_facts"]
    current_tick = events[-1].t if events else 0
    importance_of = {event.id: event.importance for event in events}
    view = KnowledgeView.from_events(events)
    records = view.records_of(knower)
    recency_weight = float(config["recency_weight"])
    importance_weight = float(config["importance_weight"])
    relevance_weight = float(config["relevance_weight"])
    query_terms = frozenset(word_tokens(query)) if query else frozenset()

    # leg-2: the fold reads as DATA at the assembly tick (the honest
    # read-model law shared with the echo); beliefs in declaration
    # order, the replaced tokens are the crystallized families' own —
    # evidence is evidence, a held family record never survives its
    # belief raw (a below-threshold family still renders raw: no belief,
    # no replacement).
    beliefs = [
        trait
        for trait in crystallized_traits(pack, view, current_tick)
        if trait.who == knower
    ]
    belief_config = pack.rules.get("traits")
    replaced: set[str] = set()
    for trait in beliefs:
        if belief_config is not None:
            replaced.update(belief_config["beliefs"][trait.token]["family"])
    lines = _belief_lines(beliefs, events)

    def score(record: Any) -> float:
        age = current_tick - record.at
        rank = _IMPORTANCE_RANK[importance_of[record.source]]
        relevance = (
            len(query_terms & frozenset(word_tokens(record.knows)))
            / len(query_terms)
            if query_terms
            else 0.0
        )
        return (
            recency_weight / (1 + age)
            + importance_weight * rank
            + relevance_weight * relevance
        )

    ranked = sorted(records, key=score, reverse=True)  # stable: acquisition wins ties
    seen: set[str] = set()
    max_items = int(config["max_items"])
    for record in ranked:
        if len(lines) >= max_items:
            break  # the top-k law: belief lines count against the cap
        if record.knows in seen:
            continue  # the brief shows what the PC knows, not the learning history
        if record.knows in replaced:
            continue  # the belief subsumes its family's raw evidence
        seen.add(record.knows)
        lines.append(
            f"- [t {record.at}, {record.channel}, {record.fidelity}] {record.knows}"
        )
    return lines


def _lore_lines(pack: Pack, *, beats: int) -> list[str]:
    """Eligible lore entries, pack declaration order (BRIEF_SPEC §3.6)."""
    lines: list[str] = []
    for entry in pack.rules["brief"].get("lore", ()):
        if int(entry["from_beat"]) <= beats < int(entry["to_beat"]):
            lines.append(str(entry["text"]))
    return lines


def _option_lines(pack: Pack) -> list[str]:
    """The pack's action grammar as a choice list, pack order (BRIEF_SPEC
    §3.7) — the vocabulary, not a precondition-filtered menu: the intent
    door stays the sole gatekeeper of the possible."""
    lines: list[str] = []
    for action in pack.data["actions.json"]["actions"]:
        fields = [str(field) for field in action.get("fields", ())]
        signature = (
            f"{action['intent']}({', '.join(fields)})" if fields else action["intent"]
        )
        lines.append(f"- {signature}")
    return lines


def _texture_prefix(entry: LedgerEntry) -> str:
    """The entity address prefix for one texture line — empty for
    scene-scoped entries (the scope is the current scene), `<id>: ` for
    entity-scoped ones. Raw ids, never display names: the scope is an
    address, not prose (BRIEF_SPEC §3.3)."""
    split = split_scope(entry.scope)
    if split is not None and split[0] == ENTITY_SCOPE_PREFIX:
        return f"{split[1]}: "
    return ""


def _scene_texture_items(
    events: Sequence[EventRecord], pack: Pack, ledger: SceneLedger
) -> list[str]:
    """The 7th block's item lines (BRIEF_SPEC §3.3 — the window law):
    live (active+pinned) entries whose scope matches the current scene
    or a present entity, ranked by the identity-or-pinned tier — an
    entry whose `slot` is pack-declared `identity_slots` ranks WITH
    `pinned` (tex-1, blueprint §1's identity-persistence resolution:
    identity must not compete with fresh texture on recency), pinned
    above identity within the tier — then newest-first with
    construction-order tie-break (ids allocate in append order, so the
    index is the tie-break; an empty `identity_slots` reduces the key
    to the pinned-only law exactly, the D-048 bytes). The per-entity
    quota walk follows the ranking: at most `per_entity_max_items`
    lines per entity scope (a chatty entity cannot flood the window —
    and the tier already put its identity slots first, "identity slot
    first" by construction), then capped by `max_items`. Both caps are
    ranking caps, not budget drops (the D-047 law: beyond-cap items
    render nothing, never dropped, never marked). Tombstones for
    contradicted entries in the same scope window render newest-first,
    capped by `tombstone_max_items`, AFTER the live lines (prevention +
    enforcement both bounded, D-049; tombstones carry no quota — their
    own cap bounds them, and a refuted identity line is gone).
    Scene-scoped entries additionally require `t >= scene.from_tick` —
    texture from an earlier scene at the same location is gone with
    that scene (a revisit starts empty), even if a stale ledger still
    holds it live.
    """
    config = pack.rules["brief"]["scene_texture"]
    scene = current_scene(events, pack)
    state = fold(events, initial_projection(pack.entities))
    present = present_entities(state, scene.location_id, pack)
    identity_slots = frozenset(config["identity_slots"])
    per_entity_cap = int(config["per_entity_max_items"])
    window: list[tuple[int, LedgerEntry]] = []
    tombs: list[tuple[int, LedgerEntry]] = []
    for index, entry in enumerate(ledger.entries):  # construction order
        split = split_scope(entry.scope)
        if split is None:
            continue
        prefix, target = split
        if prefix == ENTITY_SCOPE_PREFIX:
            if target not in present:
                continue
        elif target != scene.location_id or entry.t < scene.from_tick:
            continue
        if entry.status in LIVE_STATUSES:
            window.append((index, entry))
        elif entry.status == CONTRADICTED:
            tombs.append((index, entry))

    def tier_key(pair: tuple[int, LedgerEntry]) -> tuple[bool, bool, int]:
        # identity-or-pinned -> pinned -> newest -> construction: the
        # tier term first (identity joins pinned), pinned within the
        # tier, then the index descending (newest, the construction
        # tie-break — the pre-tex-1 key when identity_slots is empty).
        pinned = pair[1].status == PINNED
        return (
            not pinned and pair[1].slot not in identity_slots,
            not pinned,
            -pair[0],
        )

    window.sort(key=tier_key)
    tombs.sort(key=lambda pair: -pair[0])
    taken: list[LedgerEntry] = []
    entity_counts: dict[str, int] = {}
    for _index, entry in window:
        split = split_scope(entry.scope)
        if split is not None and split[0] == ENTITY_SCOPE_PREFIX:
            count = entity_counts.get(split[1], 0)
            if count >= per_entity_cap:
                continue  # the quota: beyond-K entity lines render nothing
            entity_counts[split[1]] = count + 1
        taken.append(entry)
        if len(taken) == int(config["max_items"]):
            break
    lines = [
        f"- [t {entry.t}, {entry.status}] {_texture_prefix(entry)}"
        f"{entry.slot} = {entry.value}"
        for entry in taken
    ]
    lines.extend(
        f"- [t {entry.t}, refuted] {_texture_prefix(entry)}"
        f"{entry.slot} (cause: {entry.cause})"
        for _index, entry in tombs[: int(config["tombstone_max_items"])]
    )
    return lines


def _promoted_props(
    events: Sequence[EventRecord],
) -> dict[str, list[tuple[str, Any]]]:
    """Props born by committed promotions (st-1's promoted-prop
    visibility): an event carrying a texture reference whose
    state_changes touch the scope target's slot — the D-054 canon-birth
    shape, the same detection law as `brief/mediator.py::promotions_in`
    (the mediator's marking scan), read-side output shape
    `(entity -> [(prop, value)])` in log order. Machine-condition props
    (`condition`, the `fire.*` layers) are never promotions and never
    appear here."""
    out: dict[str, list[tuple[str, Any]]] = {}
    for event in events:
        reference = event.outcome.get("texture")
        if not isinstance(reference, Mapping) or "entry" not in reference:
            continue
        split = split_scope(str(reference.get("scope", "")))
        target = split[1] if split is not None else None
        for change in event.state_changes:
            if change.entity == target and change.prop == reference.get("slot"):
                out.setdefault(change.entity, []).append(
                    (change.prop, change.to_)
                )
    return out


def _pair_axis_lines(
    pack: Pack, state: Any, present: Sequence[str]
) -> list[str]:
    """Pairwise relation tokens for present pairs (BRIEF_SPEC §3.8):
    one line per directed (holder, other) pair that carries pair-map
    axes — `pair.<other>.<axis>` props on the holder, projection order
    (construction order — seeds in pack order, event-born axes after).
    Directed on purpose: A-fears-B and B-trusts-A are different facts
    (the cross-NPC-consistency home)."""
    lines: list[str] = []
    for holder in present:
        for other in present:
            if holder == other:
                continue
            prefix = f"pair.{other}."
            axes = [
                (prop[len(prefix):], value)
                for prop, value in state[holder].items()
                if prop.startswith(prefix)
            ]
            if not axes:
                continue
            rendered = ",".join(f"{axis}={value}" for axis, value in axes)
            lines.append(f"- pair {holder} -> {other} {rendered}")
    return lines


def _present_entity_items(
    events: Sequence[EventRecord], pack: Pack
) -> list[str]:
    """The 8th block's item lines (BRIEF_SPEC §3.8 — st-1, the entity
    cards): the room's structural answer to "who is here". A read-side
    fold — zero new event types; presence is a projection read, the
    observable surface is pack data. Line order: the scene line (the
    pack-declared `scene_line_fields` of the scene location render
    canon-from-birth, then the promoted props — canon-born texture would
    otherwise vanish from the brief post-promotion: the scene_texture
    window renders live entries only; the card law: static surface
    first, event-born news last), then one dry line per present entity
    in pack declaration order (carried items fold into their carrier's
    `carries=` segment instead of a line of their own — they are the
    carrier's surface, not room fixtures), then the pair lines.
    `max_entities`/`max_pairs` are ranking caps (D-047 law — beyond-cap
    items render nothing, never a budget drop)."""
    config = pack.rules["brief"]["present_entities"]
    scene = current_scene(events, pack)
    state = fold(events, initial_projection(pack.entities))
    present = present_in_order(pack, state, scene.location_id)
    promoted = _promoted_props(events)
    lines: list[str] = []

    location_record = pack.entity(scene.location_id)
    scene_fields = [
        (field, location_record[field])
        for field in config.get("scene_line_fields", ())
        if field in location_record
    ]
    scene_props = (*scene_fields, *promoted.get(scene.location_id, ()))
    if scene_props:
        rendered = " ".join(f"{prop}={value}" for prop, value in scene_props)
        lines.append(
            f"- scene {scene.location_id} "
            f"({display_name(pack, scene.location_id)}) {rendered}"
        )

    marker_specs = [
        (str(spec["prop"]), spec, str(spec["marker"]))
        for spec in config["card_markers"]
    ]
    for entity_id in present[: int(config["max_entities"])]:
        props = state[entity_id]
        if pack.kind_of(entity_id) == "item" and props.get("carrier") is not None:
            continue  # carried: the carrier's `carries=` segment renders it
        segments = [f"- {entity_id} ({display_name(pack, entity_id)})"]
        # tune-2: the marker table is PROP-PATH keyed with two row kinds —
        # threshold rows (numeric `min`) and value rows (string `value`),
        # so `relations.suspicion` and `crime_status` rows are expressible
        # pack data (the card, not the delta window, is the narrator's
        # read surface for standing state; the PC's own perception stays
        # governed by the blind-NPC law in scene_delta).
        markers = []
        for prop, spec, marker in marker_specs:
            value = props.get(prop)
            if "min" in spec:
                if (
                    isinstance(value, int)
                    and not isinstance(value, bool)
                    and value >= int(spec["min"])
                ):
                    markers.append(marker)
            elif value is not None and value == spec["value"]:
                markers.append(marker)
        if markers:
            segments.append(f"markers={','.join(markers)}")
        carries = [
            item["id"]
            for item in pack.entities["items"]
            if state[item["id"]].get("carrier") == entity_id
        ]
        if carries:
            segments.append(f"carries={','.join(carries)}")
        segments.extend(
            f"{prop}={value}" for prop, value in promoted.get(entity_id, ())
        )
        lines.append(" ".join(segments))

    lines.extend(_pair_axis_lines(pack, state, present)[: int(config["max_pairs"])])
    return lines


def _evict_overflow(
    assembled: dict[str, Block], total_hard: int
) -> dict[str, Block]:
    """Whole-block eviction on total overflow (BRIEF_SPEC §5.2): evict in
    ascending priority order, directives never; an evicted block renders
    as its header + marker. Stops as soon as the total fits; an empty
    block frees nothing and is skipped."""
    total = sum(token_count(line) for block in assembled.values() for line in block.render())
    for block_id in EVICTABLE_BLOCKS:
        if total <= total_hard:
            break
        block = assembled[block_id]
        if not block.lines:
            continue
        total -= sum(token_count(line) for line in block.render())
        evicted = Block(block_id, (), dropped=block.dropped + len(block.lines))
        assembled[block_id] = evicted
        total += sum(token_count(line) for line in evicted.render())
    return assembled


def _knower_id(pack: Pack, knower: str | None) -> str:
    """Resolve the brief's knower (scene-1, mode B — BRIEF_SPEC §3.9):
    `None` is the player (mode A's default, byte-identical by
    construction); any other id must name a pack NPC (the chorus knower
    gate — an ambient group holds records but never speaks, an item or
    location is not a knower at all) and carry a `brief.actors` entry
    (the pack's own declaration is the gate — an undeclared NPC has no
    mode-B role text and no brief)."""
    player = pack.player_id()
    if knower is None or knower == player:
        return player
    if pack.kind_of(knower) != "npc":
        raise ValueError(
            f"knower {knower!r} is neither the player nor a pack npc "
            "(the mode-B knower gate — BRIEF_SPEC §3.9)"
        )
    if knower not in pack.rules["brief"].get("actors", {}):
        raise ValueError(
            f"knower {knower!r} carries no brief.actors entry "
            "(the pack's own declaration is the mode-B gate — BRIEF_SPEC §3.9)"
        )
    return knower


def assemble_brief(
    events: Sequence[EventRecord],
    pack: Pack,
    ledger: SceneLedger | None = None,
    *,
    knower: str | None = None,
    query: str | None = None,
) -> Brief:
    """Assemble the eight blocks from a log + ledger (pure — BRIEF_SPEC
    §2/§3). `ledger=None` renders an empty scene_texture block (a log
    without a session ledger — the same bytes as an empty one).
    `knower=None` assembles mode A (the player's brief — the committed
    corpus bytes); `knower=<npc>` assembles mode B (the actor brief:
    scene_delta and recalled_facts read the knower's own perception and
    memory — the blind-NPC law parameterized, the per-NPC brief's leak
    surface; directives and voice exemplars come from the pack's
    `brief.actors` entry — the actor's role and voice, never the
    narrator's; the scene_texture window, the entity cards, the lore,
    and the options stay shared — one scene, one grammar, observables
    only, L6).

    `query` is the mediator's keyword query (scene-2, mode B — §3.5's
    relevance signal): `None` keeps the two-signal ranking (mode A —
    the committed corpus bytes, byte-identical by construction); a
    query string adds the relevance term — the token-overlap match of
    the query's words against each record's `knows` words (the word
    view `core.retrieval.word_tokens` owns; rung-independent — the
    brief's bytes never hinge on a SQLite build's FTS5 presence).

    Deterministic by construction: no RNG, no wall-clock, construction
    order or explicit sorts only. The pack's lint guarantees the `brief`
    section shape (`core/pack.py`).
    """
    config = pack.rules["brief"]
    budgets = config["blocks"]
    knower = _knower_id(pack, knower)
    player_id = pack.player_id()
    if knower == player_id:
        directive_lines = [str(line) for line in config["directives"]]
        exemplar_lines = [str(line) for line in config["voice_exemplars"]]
    else:  # mode B: the actor's own role text and voice (BRIEF_SPEC §3.9)
        entry = config["actors"][knower]
        directive_lines = [str(line) for line in entry["directives"]]
        exemplar_lines = [str(line) for line in entry["voice_exemplars"]]
    beats = beats_crossed(pack.rules, events[-1].t if events else 0)
    texture_ledger = ledger if ledger is not None else SceneLedger()

    items: dict[str, Sequence[str]] = {
        "directives": directive_lines,
        "scene_delta": _scene_delta_lines(events, pack, knower=knower),
        "scene_texture": _scene_texture_items(events, pack, texture_ledger),
        "present_entities": _present_entity_items(events, pack),
        "recalled_facts": _recalled_fact_lines(
            events, pack, knower=knower, query=query
        ),
        "scheduled_lore": _lore_lines(pack, beats=beats),
        "voice_exemplars": exemplar_lines,
        "active_options": _option_lines(pack),
    }
    assembled: dict[str, Block] = {}
    for block_id in BRIEF_BLOCK_IDS:
        if block_id == "directives":
            # Never dropped (BRIEF_SPEC §5.2) — the lint guarantees the
            # lines fit their own hard budget, so no fill law applies.
            assembled[block_id] = Block(block_id, tuple(items[block_id]), 0)
        else:
            assembled[block_id] = _fill(block_id, items[block_id], budgets[block_id])
    assembled = _evict_overflow(assembled, int(config["total_hard"]))
    return Brief(blocks=tuple(assembled[block_id] for block_id in BRIEF_BLOCK_IDS))


def render_brief(brief: Brief) -> str:
    """Render the exact byte format (BRIEF_SPEC §7): `## <block>` headers,
    one blank line between blocks, trailing newline."""
    chunks = ["\n".join(block.render()) for block in brief.blocks]
    return "\n\n".join(chunks) + "\n"


def brief_from_log(
    log_path: Path,
    pack: Pack,
    schema: Mapping[str, Any],
    ledger: SceneLedger | None = None,
    *,
    knower: str | None = None,
    query: str | None = None,
) -> str:
    """Read a committed log and render its brief — the golden-fixture
    byte-identity entry point (same (log, ledger) → same brief bytes);
    `knower`/`query` pass through to `assemble_brief` (mode B)."""
    _header, events = read_log(log_path, schema)
    return render_brief(
        assemble_brief(events, pack, ledger, knower=knower, query=query)
    )
