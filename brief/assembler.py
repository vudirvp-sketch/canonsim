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
    events: Sequence[EventRecord], pack: Pack, *, player_id: str
) -> list[str]:
    """What the PC perceived since the last beat, newest first (BRIEF_SPEC
    §3.2): the PC is the actor or holds a record born on the event (the
    blind-NPC law — no record, no delta line)."""
    window_start = last_beat_tick(pack.rules, events[-1].t if events else 0)
    lines: list[str] = []
    for event in reversed(events):  # newest first — recency dominates
        if window_start is not None and event.t <= window_start:
            break  # ticks are log-monotonic: older events are past the window too
        perceived = event.actor == player_id or any(
            record.who == player_id for record in event.knowledge
        )
        if not perceived:
            continue
        line = f"[t {event.t}] {event.type}: {display_name(pack, event.actor)}"
        if event.target is not None:
            line += f" -> {display_name(pack, event.target)}"
        lines.append(line)
    return lines


def _recalled_fact_lines(
    events: Sequence[EventRecord], pack: Pack, *, player_id: str
) -> list[str]:
    """The PC's own knowledge records, ranked by recency + importance
    (the two deterministic signals; relevance arrives with the mediator —
    BRIEF_SPEC §3.5), deduped by token, capped at `max_items`."""
    config = pack.rules["brief"]["recalled_facts"]
    current_tick = events[-1].t if events else 0
    importance_of = {event.id: event.importance for event in events}
    records = KnowledgeView.from_events(events).records_of(player_id)
    recency_weight = float(config["recency_weight"])
    importance_weight = float(config["importance_weight"])

    def score(record: Any) -> float:
        age = current_tick - record.at
        rank = _IMPORTANCE_RANK[importance_of[record.source]]
        return recency_weight / (1 + age) + importance_weight * rank

    ranked = sorted(records, key=score, reverse=True)  # stable: acquisition wins ties
    lines: list[str] = []
    seen: set[str] = set()
    for record in ranked:
        if record.knows in seen:
            continue  # the brief shows what the PC knows, not the learning history
        seen.add(record.knows)
        lines.append(
            f"- [t {record.at}, {record.channel}, {record.fidelity}] {record.knows}"
        )
        if len(lines) >= int(config["max_items"]):
            break
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
    or a present entity, ranked pinned-first then newest-first with
    construction-order tie-break (ids allocate in append order, so the
    index is the tie-break), capped by `max_items`; then tombstone lines
    for contradicted entries in the same scope window, newest-first,
    capped by `tombstone_max_items` (D-049: prevention + enforcement,
    both bounded). The ledger never evicts — ALL boundedness is this
    window; the caps are ranking caps, not budget drops (D-047 law).
    Scene-scoped entries additionally require `t >= scene.from_tick` —
    texture from an earlier scene at the same location is gone with
    that scene (a revisit starts empty), even if a stale ledger still
    holds it live.
    """
    config = pack.rules["brief"]["scene_texture"]
    scene = current_scene(events, pack)
    state = fold(events, initial_projection(pack.entities))
    present = present_entities(state, scene.location_id, pack)
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
    window.sort(key=lambda pair: (pair[1].status != PINNED, -pair[0]))
    tombs.sort(key=lambda pair: -pair[0])
    lines = [
        f"- [t {entry.t}, {entry.status}] {_texture_prefix(entry)}"
        f"{entry.slot} = {entry.value}"
        for _index, entry in window[: int(config["max_items"])]
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
        (str(spec["axis"]), int(spec["min"]), str(spec["marker"]))
        for spec in config["status_markers"]
    ]
    for entity_id in present[: int(config["max_entities"])]:
        props = state[entity_id]
        if pack.kind_of(entity_id) == "item" and props.get("carrier") is not None:
            continue  # carried: the carrier's `carries=` segment renders it
        segments = [f"- {entity_id} ({display_name(pack, entity_id)})"]
        markers = [
            marker
            for axis, threshold, marker in marker_specs
            if (value := props.get(f"status.{axis}")) is not None
            and value >= threshold
        ]
        if markers:
            segments.append(f"status={','.join(markers)}")
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


def assemble_brief(
    events: Sequence[EventRecord], pack: Pack, ledger: SceneLedger | None = None
) -> Brief:
    """Assemble the eight blocks from a log + ledger (pure — BRIEF_SPEC
    §2/§3). `ledger=None` renders an empty scene_texture block (a log
    without a session ledger — the same bytes as an empty one).

    Deterministic by construction: no RNG, no wall-clock, construction
    order or explicit sorts only. The pack's lint guarantees the `brief`
    section shape (`core/pack.py`).
    """
    config = pack.rules["brief"]
    budgets = config["blocks"]
    player_id = pack.player_id()
    beats = beats_crossed(pack.rules, events[-1].t if events else 0)
    texture_ledger = ledger if ledger is not None else SceneLedger()

    items: dict[str, Sequence[str]] = {
        "directives": [str(line) for line in config["directives"]],
        "scene_delta": _scene_delta_lines(events, pack, player_id=player_id),
        "scene_texture": _scene_texture_items(events, pack, texture_ledger),
        "present_entities": _present_entity_items(events, pack),
        "recalled_facts": _recalled_fact_lines(events, pack, player_id=player_id),
        "scheduled_lore": _lore_lines(pack, beats=beats),
        "voice_exemplars": [str(line) for line in config["voice_exemplars"]],
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
) -> str:
    """Read a committed log and render its brief — the golden-fixture
    byte-identity entry point (same (log, ledger) → same brief bytes)."""
    _header, events = read_log(log_path, schema)
    return render_brief(assemble_brief(events, pack, ledger))
