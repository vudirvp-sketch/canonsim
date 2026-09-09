"""The mechanics introspection CLI (mech-1, iter-84; D-046 operator tooling).

Four read-only instruments over the committed pack and committed (or freshly
run) logs, for the per-instance questions the prose specs answer only
generally: "who consumes event type X", "why has hook Y not released by tick
T", "what changes if step Z is inserted here". Everything here is DERIVED,
rebuildable, never truth (the checkpoint.py law): the pack JSON and the
engine's public functions are the only sources. Output is stdout; the blast
arms write their logs under the gitignored output/mech/ dir.

The shadow-replay principle (D-118): the runtime is never instrumented — no
observer hooks, no core edits, no reimplementation of fold logic. `trace` and
`why` re-derive the director's decisions by replaying the log through the
REAL public pipeline (`fold.apply_event`, `Director.seed/next_beat/releases`,
`predicates.evaluate`, `director.entropy/channel_entropies`). INV-2
determinism makes the shadow equal the runtime's own decisions on the same
log; tests/test_mechanics.py pins that equality on the canonical day1_full
run (the shadow's release ids must equal the log's director-intent events).

Beat-grid derivation: beats are pack data (`urgencies.beat_ticks`, intraday
offsets repeated daily — DIRECTOR_SPEC §7 owns the axis). The tool re-derives
the grid with core/loop.py's arithmetic (_first_beat/_next_beat_after) and
fires beats up to the last event tick (a run ends when its queue drains).
Each beat's input is the projection of all events with t < B plus the
leading t == B events whose provenance carries no cause_intent (the
crossing-committed family: rotations and status decay — the loop's in-beat
order is decay first, then urgencies, then the director, core/loop.py
_run_beat). Known approximation: a transition-layer pass landing at a beat
tick before any intent event is fed to the shadow's beat input as well; the
release-equality pin guards drift on the canonical corpus.

Future layers are additive, never a rewrite: the dynamic half replays the
engine, so new systems and folds appear in traces automatically; the static
half (`matrix`) walks the known pack shapes (director.hooks, on_action,
crime_watch, urgencies, echo, traits, actions) and lists every other rules
block generically as unindexed — a new layer is visible the iteration it
lands and joins the wiring matrix when its shape rule is added.

Usage:
    python scripts/mechanics.py matrix [--pack DIR] [--event TYPE]
        [--hook TAG] [--token TOKEN] [--prop PATH]
    python scripts/mechanics.py trace (--log PATH | --script PATH) [--pack DIR]
        [--ticks A:B] [--tail N] [--entity ID] [--hook TAG] [--event TYPE]
    python scripts/mechanics.py why --hook TAG (--log PATH | --script PATH)
        [--at-tick N] [--pack DIR]
    python scripts/mechanics.py blast --script PATH [--step-json JSON]
        [--at N] [--pack DIR] [--out DIR]

D-012 (stdlib + core only), INV-4 (no LLM/network), INV-5 (never writes
into logs/; blast arms write only gitignored output/mech/).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

# Allow `python scripts/mechanics.py` and `python -m scripts.mechanics`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.clock import Clock  # noqa: E402
from core.director import (  # noqa: E402
    HOOK_PREFIX,
    Director,
    channel_entropies,
    channels_from_rules,
    entropy,
    policy_from_rules,
)
from core.fold import Projection, apply_event, fold, initial_projection  # noqa: E402
from core.log import EventRecord, read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.pack import Pack, load_pack  # noqa: E402
from core.predicates import evaluate  # noqa: E402
from core.states import DECAY_EVENT  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"
SCHEMA_PATH = REPO / "schemas" / "event.schema.json"
MECH_OUT = REPO / "output" / "mech"

INDEXED_BLOCKS: Final = (
    "director", "on_action", "crime_watch", "urgencies", "echo", "traits",
)
_COMPARATORS: Final = {
    "at_least": ">=", "at_most": "<=", "equals": "==", "not_equals": "!=",
}


# -- loading ------------------------------------------------------------------


def _load(pack_dir: Path) -> tuple[Pack, dict[str, Any]]:
    return load_pack(pack_dir), json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _events_from_source(
    pack: Pack,
    schema: Mapping[str, Any],
    log_path: Path | None,
    script_path: Path | None,
) -> tuple[str, list[EventRecord], dict[str, Any]]:
    """Events for trace/why: a committed log read canonically, or a fresh
    run of a playscript into the gitignored output dir. The log's pack must
    equal the loaded pack (the checkpoint.py provenance gate)."""
    if log_path is None and script_path is None:
        raise SystemExit("error: exactly one of --log / --script is required")
    if log_path is not None:
        header, events = read_log(log_path, schema)
        if header.get("pack") != pack.name_version:
            raise SystemExit(
                f"error: log pack {header.get('pack')!r} != loaded pack "
                f"{pack.name_version!r} (the checkpoint provenance law)"
            )
        return str(log_path), list(events), header
    script = load_playscript(script_path)
    MECH_OUT.mkdir(parents=True, exist_ok=True)
    log = MECH_OUT / f"{script['name']}_{script['seed']}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(pack, script["seed"], log, schema, commit="0000000")
    sim.run_playscript(script)
    header, events = read_log(log, schema)
    return str(log), list(events), header


# -- the beat grid ------------------------------------------------------------


def beat_grid(rules: Mapping[str, Any], last_tick: int) -> list[int]:
    """Beat ticks a run fires whose last event lands at `last_tick` (the
    queue-drain law). Mirrors core/loop.py _first_beat/_next_beat_after
    (DIRECTOR_SPEC §7 owns the axis); pinned by the release-equality test."""
    offsets = sorted(rules.get("urgencies", {}).get("beat_ticks", ()))
    if not offsets:
        return []
    day = Clock.from_rules(dict(rules["time"])).ticks_per_day
    beats: list[int] = []
    tick = next((o for o in offsets if o > 0), day + offsets[0])
    while tick <= last_tick:
        beats.append(tick)
        day_idx = tick // day
        tick = min(
            c
            for c in (d * day + o for d in (day_idx, day_idx + 1) for o in offsets)
            if c > tick
        )
    return beats


# -- the shadow replay (trace / why) ------------------------------------------


@dataclass(frozen=True)
class ReleaseLine:
    intent_id: str
    tags: tuple[str, ...]
    kind: str
    actor: str
    trigger_armed: bool | None


@dataclass(frozen=True)
class BeatLine:
    tick: int
    index: int
    pacing: str | None
    entropy: int | None
    channels: tuple[tuple[str, int], ...]
    decay: tuple[str, ...]
    releases: tuple[ReleaseLine, ...]


@dataclass
class Replay:
    beats: list[BeatLine] = field(default_factory=list)
    seeded: dict[str, list[tuple[str, int]]] = field(default_factory=dict)
    intent_tags: dict[str, tuple[str, ...]] = field(default_factory=dict)
    projection: Projection = field(default_factory=dict)
    last_tick: int = 0


def _payload_tags(pack: Pack) -> dict[tuple[str, str], tuple[str, ...]]:
    """(intent kind, actor) -> hook tags, option payloads included. The
    release-attribution heuristic: releases() hides its source hook; payload
    matching against the pack's own declarations recovers it. An ambiguous
    payload lists every candidate tag."""
    table: dict[tuple[str, str], list[str]] = {}
    hooks = pack.rules.get("director", {}).get("hooks", {})
    for tag, spec in hooks.items():
        actor = spec.get("target_npc")
        kinds = [spec.get("intent", {}).get("kind")]
        for option in _option_items(spec):
            kinds.append(option.get("intent", {}).get("kind"))
        for kind in (k for k in kinds if k):
            if actor:
                table.setdefault((kind, actor), []).append(tag)
    return {key: tuple(tags) for key, tags in table.items()}


def _is_intent_driven(event: EventRecord) -> bool:
    return isinstance(event.provenance.get("cause_intent"), str)


def shadow_replay(
    pack: Pack, events: Sequence[EventRecord], upto_tick: int | None = None
) -> Replay:
    """Re-derive the run's director state from the log: fold the projection
    and drive a real Director over the same events and beats (the design
    law — the real pipeline, INV-2-equal to the runtime on the same log)."""
    replay = Replay()
    if not events:
        return replay
    last_tick = events[-1].t if upto_tick is None else min(upto_tick, events[-1].t)
    replay.last_tick = last_tick
    director = Director(pack=pack, policy=policy_from_rules(pack.rules, True))
    channels_cfg = channels_from_rules(pack.rules) or {}
    payload = _payload_tags(pack)
    proj: Projection = initial_projection(pack.entities)
    released_tags: set[str] = set()

    def absorb(event: EventRecord) -> None:
        apply_event(proj, event)
        director.seed(event)
        for tag in event.hooks:
            replay.seeded.setdefault(tag, []).append((event.id, event.t))

    i = 0
    for beat_tick in beat_grid(pack.rules, last_tick):
        while i < len(events) and events[i].t < beat_tick:
            absorb(events[i])
            i += 1
        decay_ids: list[str] = []
        while (
            i < len(events)
            and events[i].t == beat_tick
            and not _is_intent_driven(events[i])
        ):
            if events[i].type == DECAY_EVENT:
                decay_ids.append(events[i].id)
            absorb(events[i])
            i += 1
        director.next_beat()
        intents = director.releases(proj, beat_tick)
        lines: list[ReleaseLine] = []
        for intent in intents:
            tags = payload.get((intent.kind, intent.actor), ())
            armed = None
            for tag in tags:
                spec = pack.rules.get("director", {}).get("hooks", {}).get(tag, {})
                trigger = spec.get("trigger")
                if trigger is not None:
                    armed = bool(evaluate(trigger, proj, beat_tick))
                    break
            lines.append(
                ReleaseLine(intent.id, tags, intent.kind, intent.actor, armed)
            )
            released_tags.update(tags)
            replay.intent_tags[intent.id] = tags
        tension = [
            hook for hook in director.hooks if hook.tag not in released_tags
        ]
        ent = entropy(proj, iter(tension), pack.rules, beat_tick)
        channel_map = channel_entropies(
            channels_cfg, proj, iter(tension), pack.rules, beat_tick
        )
        pacing = director.pacing.state if director.pacing is not None else None
        replay.beats.append(
            BeatLine(
                tick=beat_tick,
                index=director.beat_count,
                pacing=pacing,
                entropy=ent,
                channels=tuple(sorted(channel_map.items())),
                decay=tuple(decay_ids),
                releases=tuple(lines),
            )
        )
    while i < len(events) and events[i].t <= last_tick:
        absorb(events[i])
        i += 1
    replay.projection = proj
    return replay


# -- predicate rendering ------------------------------------------------------


def _render_predicate(spec: Any) -> str:
    """A compact one-line rendering of a predicate spec (the grammar's
    single owner is core/predicates.py; this is display, not semantics)."""
    if isinstance(spec, Sequence) and not isinstance(spec, (str, bytes)):
        return " & ".join(_render_predicate(item) for item in spec)
    if not isinstance(spec, Mapping) or not spec:
        return repr(spec)
    for key in ("all", "any", "not"):
        if key in spec:
            inner = _render_predicate(spec[key])
            return f"{key}({inner})" if key != "not" else f"not({inner})"
    kind = spec.get("kind")
    if kind == "time":
        return f"tick >= {spec.get('tick')}"
    if kind == "place":
        return f"{spec.get('target_npc')} at {spec.get('location')}"
    if kind == "threshold":
        op = _COMPARATORS.get(str(spec.get("comparator")), ">=")
        return (
            f"{spec.get('target_npc')}.relations.{spec.get('axis')} "
            f"{op} {spec.get('value')}"
        )
    if kind == "prop":
        op = _COMPARATORS.get(str(spec.get("comparator")), ">=")
        owner = f"{spec.get('of')}." if spec.get("of") else ""
        return f"{owner}{spec.get('path')} {op} {spec.get('value')}"
    return json.dumps(spec, sort_keys=True)


def _annotate_predicate(
    spec: Any, projection: Mapping[str, Mapping[str, Any]], tick: int
) -> str:
    """The rendered spec with a per-leaf verdict (the REAL evaluator's
    answer per leaf — display only, semantics stay core/predicates.py)."""
    if isinstance(spec, Sequence) and not isinstance(spec, (str, bytes)):
        parts = [
            _annotate_predicate(item, projection, tick) for item in spec
        ]
        return " & ".join(parts)
    if isinstance(spec, Mapping):
        for key in ("all", "any"):
            if key in spec:
                return f"{key}(" + _annotate_predicate(
                    spec[key], projection, tick
                ) + ")"
        if "not" in spec:
            return "not(" + _annotate_predicate(spec["not"], projection, tick) + ")"
    try:
        verdict = "T" if evaluate(spec, projection, tick) else "F"
    except (ValueError, TypeError):
        verdict = "?"
    return f"{_render_predicate(spec)} [{verdict}]"


def _explain_trigger(
    spec: Any, projection: Mapping[str, Mapping[str, Any]], tick: int
) -> str:
    """Render + verdict: the rendered spec with the armed/blocked answer of
    the REAL evaluator (predicates.evaluate) against the projection."""
    try:
        verdict = "ARMED" if evaluate(spec, projection, tick) else "BLOCKED"
    except (ValueError, TypeError):
        verdict = "UNEVALUABLE"
    return f"{_render_predicate(spec)} -> {verdict}"


def _trigger_hold(
    spec: Any, projection: Mapping[str, Mapping[str, Any]]
) -> str | None:
    """The current value a prop/threshold leaf reads (the BLOCKED reason)."""
    if not isinstance(spec, Mapping):
        return None
    if "kind" not in spec:
        for key in ("all", "any", "not"):
            if key in spec:
                return _trigger_hold(spec[key], projection)
        return None
    if spec.get("kind") == "prop":
        owner = spec.get("of")
        props = projection.get(str(owner), {}) if owner else {}
        value = props.get(str(spec.get("path")))
        return f"holds {value!r}" if value is not None else "holds nothing yet"
    if spec.get("kind") == "threshold":
        props = projection.get(str(spec.get("target_npc")), {})
        value = props.get(f"relations.{spec.get('axis')}")
        return f"holds {value!r}" if value is not None else "holds nothing yet"
    return None


# -- matrix: the static wiring -----------------------------------------------


def _action_rows(pack: Pack) -> list[dict[str, Any]]:
    actions = pack.data.get("actions.json", {}).get("actions", [])
    return [a for a in actions if isinstance(a, Mapping)]


def _action_outcome_knowledge(
    action: Mapping[str, Any]
) -> dict[str, list[Mapping[str, Any]]]:
    """Outcome -> knowledge entries an action declares (the block is keyed
    by the action's own outcome names; a flat list is tolerated)."""
    block = action.get("knowledge") or {}
    if isinstance(block, Mapping):
        return {
            str(outcome): [
                entry for entry in entries if isinstance(entry, Mapping)
            ]
            for outcome, entries in block.items()
            if isinstance(entries, list)
        }
    if isinstance(block, list):
        return {"flat": [entry for entry in block if isinstance(entry, Mapping)]}
    return {}


def _crime_map(pack: Pack) -> dict[str, tuple[str, int]]:
    """Knowledge token -> (crime source label, suspicion delta), composed
    from the pack's own two tables (suspicion_from_knowledge +
    suspicion_sources — the single owners of the mapping and the numbers)."""
    from_knowledge = (
        pack.rules.get("crime_watch", {}).get("suspicion_from_knowledge", {})
    )
    sources = pack.rules.get("crime_watch", {}).get("suspicion_sources", {})
    out: dict[str, tuple[str, int]] = {}
    for token, entry in from_knowledge.items():
        if not isinstance(entry, Mapping):
            continue
        source = entry.get("source")
        delta = sources.get(str(source))
        out[str(token)] = (str(source), int(delta) if isinstance(delta, int) else 0)
    return out


def _option_items(spec: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """A hook spec's declared options (list or dict form, both legal)."""
    raw = spec.get("options", ())
    items = list(raw.values()) if isinstance(raw, Mapping) else list(raw)
    return [item for item in items if isinstance(item, Mapping)]


def _render_matrix_hook(pack: Pack, tag: str) -> list[str]:
    spec = pack.rules.get("director", {}).get("hooks", {}).get(tag)
    if spec is None:
        return [f"hook {tag}", "  declared   no (unknown tag in this pack)"]
    lines = [f"hook {tag}"]
    trigger = spec.get("trigger")
    lines.append(
        f"  trigger    "
        f"{_render_predicate(trigger) if trigger is not None else 'none (quiet-only)'}"
    )
    weight = spec.get("weight")
    weight_text = (
        json.dumps(weight, sort_keys=True) if not isinstance(weight, int)
        else str(weight)
    )
    lines.append(
        f"  weight     {weight_text} · release_threshold "
        f"{spec.get('release_threshold')}"
    )
    flags = []
    if spec.get("channel"):
        flags.append(f"channel {spec.get('channel')}")
    if spec.get("climax"):
        flags.append("climax")
    if spec.get("first_time_only"):
        flags.append("first_time_only")
    lines.append(f"  gates      {' · '.join(flags) if flags else '-'}")
    intent = spec.get("intent", {})
    lines.append(
        f"  payload    {intent.get('kind')} -> {intent.get('target')} "
        f"by {spec.get('target_npc')}"
    )
    raw_options = spec.get("options", ())
    option_count = len(raw_options) if hasattr(raw_options, "__len__") else 0
    lines.append(f"  options    {option_count}")
    seeded_by = [
        f"{action.get('intent')}.{outcome}"
        for action in _action_rows(pack)
        for outcome in ("success", "failure")
        if tag in (action.get("hooks", {}).get(outcome) or ())
    ]
    lines.append(
        f"  seeded_by  {', '.join(seeded_by) if seeded_by else '-'}"
    )
    for name, arc in pack.rules.get("director", {}).get("arcs", {}).items():
        members = arc.get("members", []) if isinstance(arc, Mapping) else []
        if tag in members:
            lines.append(
                f"  arc        {name} (member {members.index(tag) + 1} "
                f"of {len(members)})"
            )
    return lines


def _event_knowledge_tokens(pack: Pack) -> dict[str, list[str]]:
    """Event type -> knowledge tokens its producing actions mint (templates
    included, marked with braces)."""
    table: dict[str, list[str]] = {}
    for action in _action_rows(pack):
        events = action.get("events") or {}
        for outcome, event_type in events.items():
            if not isinstance(event_type, str):
                continue
            for entry in _action_outcome_knowledge(action).get(str(outcome), []):
                knows = entry.get("knows")
                if isinstance(knows, str) and knows not in table.setdefault(
                    event_type, []
                ):
                    table[event_type].append(knows)
    return table


def _render_matrix_event(pack: Pack, event_type: str) -> list[str]:
    lines = [f"event {event_type}"]
    producers = [
        f"{action.get('intent')}.{outcome}"
        for action in _action_rows(pack)
        for outcome, event_type_ in (action.get("events") or {}).items()
        if event_type_ == event_type
    ]
    lines.append(f"  produced_by  {', '.join(producers) if producers else '?'}")
    reactions = pack.rules.get("on_action", {}).get(event_type)
    lines.append(
        f"  on_action    {len(reactions) if isinstance(reactions, list) else '-'}"
    )
    crime_map = _crime_map(pack)
    crime_parts = [
        f"{token} -> {crime_map[token][0]} +{crime_map[token][1]}"
        for token in sorted(_event_knowledge_tokens(pack).get(event_type, ()))
        if token in crime_map
    ]
    lines.append(
        "  crime        "
        + ("; ".join(crime_parts) if crime_parts else "-")
    )
    seeders = [
        tag
        for action in _action_rows(pack)
        for outcome in ("success", "failure")
        if (action.get("events") or {}).get(outcome) == event_type
        for tag in (action.get("hooks", {}).get(outcome) or ())
    ]
    lines.append(
        f"  seeds        {', '.join(sorted(set(seeders))) if seeders else '-'}"
    )
    tokens = _event_knowledge_tokens(pack).get(event_type, [])
    if tokens:
        lines.append(f"  knowledge    {', '.join(tokens[:6])}")
    return lines


def _render_matrix_token(pack: Pack, token: str) -> list[str]:
    lines = [f"token {token}"]
    minted = [
        f"{action.get('intent')} ({entry.get('channel')}/{entry.get('fidelity')})"
        for action in _action_rows(pack)
        for entries in _action_outcome_knowledge(action).values()
        for entry in entries
        if entry.get("knows") == token
    ]
    lines.append(f"  minted_by    {', '.join(minted) if minted else '-'}")
    crime_map = _crime_map(pack)
    crime_entry = crime_map.get(token)
    lines.append(
        "  crime        "
        + (
            f"source {crime_entry[0]} · delta +{crime_entry[1]}"
            if crime_entry
            else "-"
        )
    )
    valence = pack.rules.get("echo", {}).get("tokens", {}).get(token)
    lines.append(
        "  echo         "
        + (json.dumps(valence, sort_keys=True) if valence else "-")
    )
    families = [
        name
        for name, family in pack.rules.get("traits", {}).get("beliefs", {}).items()
        if isinstance(family, Mapping)
        and token in json.dumps(family.get("tokens", family))
    ]
    lines.append(
        f"  traits       {', '.join(families) if families else '-'}"
    )
    return lines


def _predicate_prop_paths(spec: Any) -> list[str]:
    """Every prop/threshold leaf path a predicate spec reads (recursive)."""
    if isinstance(spec, Sequence) and not isinstance(spec, (str, bytes)):
        out: list[str] = []
        for item in spec:
            out.extend(_predicate_prop_paths(item))
        return out
    if not isinstance(spec, Mapping):
        return []
    out: list[str] = []
    for key in ("all", "any", "not"):
        if key in spec:
            out.extend(_predicate_prop_paths(spec[key]))
    kind = spec.get("kind")
    if kind == "prop":
        owner = f"{spec.get('of')}." if spec.get("of") else ""
        out.append(f"{owner}{spec.get('path')}")
    elif kind == "threshold":
        out.append(f"{spec.get('target_npc')}.relations.{spec.get('axis')}")
    return out


def _render_matrix_prop(pack: Pack, prop: str) -> list[str]:
    lines = [f"prop {prop}"]

    def _reads(qualified: str) -> bool:
        return qualified == prop or qualified.endswith(f".{prop}")

    readers: list[str] = []
    for tag, spec in pack.rules.get("director", {}).get("hooks", {}).items():
        paths = _predicate_prop_paths(spec.get("trigger"))
        for option in _option_items(spec):
            paths.extend(_predicate_prop_paths(option.get("trigger")))
        weight = spec.get("weight")
        if isinstance(weight, Mapping):
            for modifier in weight.get("modifiers", ()):
                if isinstance(modifier, Mapping):
                    paths.extend(_predicate_prop_paths(modifier.get("when")))
        if any(_reads(path) for path in paths):
            readers.append(f"hook {tag} (trigger/gate/modifier)")
    for event_type, entries in pack.rules.get("on_action", {}).items():
        for entry in entries if isinstance(entries, list) else ():
            if isinstance(entry, Mapping) and prop in json.dumps(
                entry.get("state", {})
            ):
                readers.append(f"on_action {event_type} (state)")
    for entry in pack.rules.get("urgencies", {}).get("entries", ()):
        if isinstance(entry, Mapping) and any(
            _reads(path) for path in _predicate_prop_paths(entry.get("requires"))
        ):
            readers.append(f"urgency {entry.get('npc', '?')} (requires)")
    lines.append(f"  read_by    {', '.join(readers) if readers else '-'}")
    return lines


def render_matrix(
    pack: Pack,
    *,
    event: str | None = None,
    hook: str | None = None,
    token: str | None = None,
    prop: str | None = None,
) -> str:
    """The static wiring matrix: pack-declared producers/consumers/hooks.
    Query flags narrow to one object; without flags the full (compact)
    inventory prints. Unknown rules blocks are listed generically — the
    future-layer fallback (visible immediately, indexed when shaped)."""
    out: list[str] = [f"== MATRIX {pack.name_version} — static wiring =="]
    if hook:
        out.extend(_render_matrix_hook(pack, hook))
    if event:
        out.extend(_render_matrix_event(pack, event))
    if token:
        out.extend(_render_matrix_token(pack, token))
    if prop:
        out.extend(_render_matrix_prop(pack, prop))
    if not (hook or event or token or prop):
        out.append("")
        out.append("-- hooks (director.hooks) --")
        for tag in sorted(pack.rules.get("director", {}).get("hooks", {})):
            out.extend(_render_matrix_hook(pack, tag))
            out.append("")
        out.append("-- events (actions.json wiring) --")
        known: set[str] = set()
        for action in _action_rows(pack):
            for event_type in (action.get("events") or {}).values():
                if isinstance(event_type, str):
                    known.add(event_type)
        known.update(pack.rules.get("on_action", {}))
        for event_type in sorted(known):
            out.extend(_render_matrix_event(pack, event_type))
            out.append("")
        out.append("-- read-side folds (code-owned, generic rows) --")
        echo = pack.rules.get("echo", {})
        out.append(
            f"  echo: {len(echo.get('tokens', {}))} valence tokens · "
            f"scale {json.dumps(echo.get('scale'))} · decay linear in ticks"
        )
        traits = pack.rules.get("traits", {})
        out.append(
            f"  traits: threshold {traits.get('threshold')} · "
            f"{len(traits.get('beliefs', {}))} belief families "
            "(distinct-token count, no decay on crystallized beliefs)"
        )
        out.append("")
    unindexed = [
        key
        for key in sorted(pack.rules)
        if key not in INDEXED_BLOCKS and key != "notes"
    ]
    out.append(
        "-- unindexed rules blocks (generic listing; shape rules join here, "
        "never a rewrite) --"
    )
    for key in unindexed:
        block = pack.rules[key]
        if isinstance(block, Mapping):
            out.append(f"  {key} ({len(block)} keys)")
        else:
            out.append(f"  {key} ({type(block).__name__})")
    out.append(
        "note: the pack lint (core/pack.py, load-time) validates every "
        "reference; this matrix only displays the wiring."
    )
    return "\n".join(out) + "\n"


# -- trace --------------------------------------------------------------------


def _event_touches(event: EventRecord, entity: str) -> bool:
    if event.actor == entity or event.target == entity:
        return True
    if any(change.entity == entity for change in event.state_changes):
        return True
    return any(record.who == entity for record in event.knowledge)


def _render_event(
    event: EventRecord, intent_tags: Mapping[str, tuple[str, ...]]
) -> list[str]:
    parts = [f"[t={event.t}] {event.id} {event.type}", f"actor={event.actor}"]
    if event.target:
        parts.append(f"target={event.target}")
    if event.cause:
        parts.append(f"cause={event.cause}")
    lines = ["  " + " · ".join(parts)]
    for change in event.state_changes:
        arrow = f"{change.from_!r} -> {change.to_!r}"
        flag = " [irreversible]" if change.irreversible else ""
        lines.append(
            f"    state  {change.entity}.{change.prop}: {arrow}{flag}"
        )
    for record in event.knowledge:
        lines.append(
            f"    knows  {record.who} · {record.knows} "
            f"({record.channel}/{record.fidelity})"
        )
    if event.hooks:
        lines.append(f"    seeds  {', '.join(event.hooks)}")
    ci = event.provenance.get("cause_intent")
    if isinstance(ci, str) and ci.startswith(f"{HOOK_PREFIX}_"):
        tags = intent_tags.get(ci) or ("?",)
        lines.append(f"    via    {ci} -> {', '.join(tags)} (director release)")
    return lines


def render_trace(
    pack: Pack,
    events: Sequence[EventRecord],
    *,
    source: str,
    seed: Any,
    tick_from: int | None = None,
    tick_to: int | None = None,
    entity: str | None = None,
    hook: str | None = None,
    event_type: str | None = None,
) -> str:
    """The dynamic half: a per-tick execution view of one log — events with
    their fold deltas, knowledge mints, hook seeds, and the director's beat
    decisions (entropy, pacing, releases) re-derived by the shadow."""
    replay = shadow_replay(pack, events)
    last_tick = events[-1].t if events else 0
    lo = tick_from if tick_from is not None else 0
    hi = tick_to if tick_to is not None else last_tick
    out = [
        f"== TRACE {source} ==",
        f"pack {pack.name_version} · seed {seed} · {len(events)} events · "
        f"ticks 0..{last_tick} · beats {len(replay.beats)}",
    ]
    for beat in replay.beats:
        if not (lo <= beat.tick <= hi):
            continue
        if entity and not any(
            line.actor == entity for line in beat.releases
        ):
            continue
        if hook and not any(hook in line.tags for line in beat.releases):
            continue
        if event_type:
            continue
        channels = " · ".join(f"{name} {value}" for name, value in beat.channels)
        pacing = beat.pacing if beat.pacing is not None else "no pacing block"
        out.append(
            f"[t={beat.tick}] -- BEAT {beat.index} · pacing {pacing} · "
            f"entropy {beat.entropy}"
            + (f" · {channels}" if channels else "")
        )
        if beat.decay:
            out.append(f"    decay  {', '.join(beat.decay)}")
        for line in beat.releases:
            tags = ", ".join(line.tags) if line.tags else "?"
            armed = ""
            if line.trigger_armed is not None:
                armed = " · trigger " + ("armed" if line.trigger_armed else "blocked")
            out.append(
                f"    release {line.intent_id} -> {tags} · {line.kind} "
                f"by {line.actor}{armed}"
            )
    for event in events:
        if not (lo <= event.t <= hi):
            continue
        if entity and not _event_touches(event, entity):
            continue
        if event_type and event.type != event_type:
            continue
        if hook and hook not in event.hooks and not (
            isinstance(event.provenance.get("cause_intent"), str)
            and hook in replay.intent_tags.get(
                str(event.provenance.get("cause_intent")), ()
            )
        ):
            continue
        out.extend(_render_event(event, replay.intent_tags))
    if hook:
        instances = replay.seeded.get(hook, [])
        released_beats = [
            beat.tick
            for beat in replay.beats
            if any(hook in line.tags for line in beat.releases)
        ]
        out.append(
            f"hook {hook}: seeded {len(instances)} "
            f"({', '.join(f'{eid}@t={tick}' for eid, tick in instances) or 'never'})"
            f" · released at beat(s) "
            f"{', '.join(str(t) for t in released_beats) or 'never'}"
        )
    return "\n".join(out) + "\n"


# -- why ----------------------------------------------------------------------


def render_why(
    pack: Pack,
    events: Sequence[EventRecord],
    *,
    tag: str,
    at_tick: int | None = None,
    source: str = "-",
) -> str:
    """The postmortem: one hook's full causal status at a tick — seeded,
    armed, gate inputs (entropy/pacing/channels), release record. The
    VALUES come from the shadow; the decision LAW is DIRECTOR_SPEC's
    (values here, law there — D-024)."""
    tick = events[-1].t if at_tick is None else at_tick
    replay = shadow_replay(pack, events, upto_tick=tick)
    spec = pack.rules.get("director", {}).get("hooks", {}).get(tag)
    out = [f"== WHY — {tag} @ t={tick} · {source} =="]
    if spec is None:
        out.append("declared    no such hook in director.hooks (dead tag?)")
        return "\n".join(out) + "\n"
    weight = spec.get("weight")
    weight_text = (
        json.dumps(weight, sort_keys=True)
        if not isinstance(weight, int)
        else str(weight)
    )
    flags = []
    if spec.get("channel"):
        flags.append(f"channel {spec.get('channel')}")
    if spec.get("climax"):
        flags.append("climax")
    if spec.get("first_time_only"):
        flags.append("first_time_only")
    out.append(
        f"declared    weight {weight_text} · release_threshold "
        f"{spec.get('release_threshold')}"
        + (f" · {' · '.join(flags)}" if flags else "")
    )
    intent = spec.get("intent", {})
    out.append(
        f"payload     {intent.get('kind')} -> {intent.get('target')} "
        f"by {spec.get('target_npc')}"
    )
    trigger = spec.get("trigger")
    if trigger is not None:
        explain = _explain_trigger(trigger, replay.projection, tick)
        hold = _trigger_hold(trigger, replay.projection)
        out.append(f"trigger     {explain}" + (f" ({hold})" if hold else ""))
    else:
        out.append("trigger     none — quiet/climax paths only")
    option_items = _option_items(spec)
    if option_items:
        out.append(
            f"options     {len(option_items)} declared — the option layer "
            "(drama-2): an all-closed hook WAITS (no door attempt, no budget)"
        )
        for index, option in enumerate(option_items, start=1):
            if not isinstance(option, Mapping):
                continue
            gate = option.get("trigger")
            if gate is None:
                out.append(f"  [{index}] always open (no gate)")
                continue
            annotated = _annotate_predicate(gate, replay.projection, tick)
            try:
                open_ = evaluate(gate, replay.projection, tick)
            except (ValueError, TypeError):
                open_ = None
            verdict = "OPEN" if open_ else ("CLOSED" if open_ is not None else "?")
            out.append(f"  [{index}] {annotated} -> {verdict}")
    instances = replay.seeded.get(tag, [])
    out.append(
        f"seeded      {len(instances)} instance(s): "
        + (", ".join(f"{eid}@t={t}" for eid, t in instances) or "never")
    )
    release_beats = [
        beat for beat in replay.beats
        if any(tag in line.tags for line in beat.releases)
    ]
    if release_beats:
        beat = release_beats[0]
        line = next(ln for ln in beat.releases if tag in ln.tags)
        event_ids = [
            event.id
            for event in events
            if event.provenance.get("cause_intent") == line.intent_id
        ]
        out.append(
            f"released    YES — beat t={beat.tick} · {line.intent_id}"
            + (f" -> event(s) {', '.join(event_ids)}" if event_ids else "")
        )
        return "\n".join(out) + "\n"
    out.append(f"released    NO — no director intent matched this payload by t={tick}")
    tension_total = None
    for beat in reversed(replay.beats):
        tension_total = beat.entropy
        break
    channels_cfg = channels_from_rules(pack.rules) or {}
    last_beat = replay.beats[-1] if replay.beats else None
    if last_beat is not None:
        channel_text = " · ".join(
            f"{name} {value} (floor {channels_cfg[name].entropy_floor})"
            for name, value in last_beat.channels
        )
        out.append(
            f"entropy     total {tension_total}"
            + (f" · {channel_text}" if channel_text else "")
            + " (the last beat's shadow view)"
        )
        if last_beat.pacing is not None:
            out.append(
                f"pacing      {last_beat.pacing} at the last beat — "
                "PEAK/REST suppress the quiet path; explicit triggers are "
                "never paced"
            )
        else:
            out.append("pacing      no pacing block (the v0.1 minimal pair)")
    else:
        out.append("entropy     no beat fired by t=" + str(tick))
    cooldown = pack.rules.get("director", {}).get("stagnation", {}).get(
        "per_npc_cooldown_beats"
    )
    target = str(spec.get("target_npc"))
    last_release = [
        beat.tick
        for beat in replay.beats
        if any(line.actor == target for line in beat.releases)
    ]
    out.append(
        f"cooldown    per_npc_cooldown_beats {cooldown} · {target} last "
        f"released at beat "
        + (f"t={last_release[-1]}" if last_release else "never (no release on "
           "record)")
    )
    for name, arc in pack.rules.get("director", {}).get("arcs", {}).items():
        members = arc.get("members", []) if isinstance(arc, Mapping) else []
        if tag in members:
            out.append(
                f"arc         {name} — member {members.index(tag) + 1} of "
                f"{len(members)} (the order law gates candidacy)"
            )
    out.append(
        "note        the values above are gate INPUTS; the release law is "
        "docs/DIRECTOR_SPEC.md §3-§5 (never restated here — D-024)"
    )
    return "\n".join(out) + "\n"


# -- blast --------------------------------------------------------------------


def _counter(events: Sequence[EventRecord], key: str) -> Counter[str]:
    out: Counter[str] = Counter()
    for event in events:
        if key == "type":
            out[event.type] += 1
        elif key == "hooks":
            out.update(event.hooks)
        elif key == "director":
            ci = event.provenance.get("cause_intent")
            if isinstance(ci, str) and ci.startswith(f"{HOOK_PREFIX}_"):
                out[ci] += 1
    return out


def run_blast(
    pack: Pack,
    schema: Mapping[str, Any],
    script: Mapping[str, Any],
    step: Mapping[str, Any] | None,
    at: int | None,
    out_dir: Path,
) -> str:
    """The two-arm A/B (the corpus-price pattern): the same seed, the base
    script and the modified script, folded and diffed. No state fork — both
    arms replay from t=0 (the resume door stays owner-gated)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    if step is not None:
        steps = list(script["steps"])
        position = len(steps) if at is None else max(0, min(at, len(steps)))
        steps.insert(position, dict(step))
        script_b = dict(script, steps=steps)
    else:
        script_b = script
    arms: dict[str, tuple[Any, list[EventRecord], Projection]] = {}
    for label, arm_script in (("A", script), ("B", script_b)):
        log = out_dir / f"blast_{script['name']}_{label.lower()}.jsonl"
        if log.exists():
            log.unlink()
        sim = Simulator(pack, script["seed"], log, schema, commit="0000000")
        result = sim.run_playscript(dict(arm_script))
        _, events = read_log(log, schema)
        projection = fold(events, initial_projection(pack.entities))
        arms[label] = (result, events, projection)
    result_a, events_a, proj_a = arms["A"]
    result_b, events_b, proj_b = arms["B"]
    step_text = json.dumps(step, sort_keys=True) if step is not None else "none"
    out = [
        f"== BLAST {script['name']} (seed {script['seed']}) — "
        f"step {step_text} ==",
        f"arm A (base)     : {len(events_a)} events · ticks "
        f"0..{events_a[-1].t if events_a else 0} · fingerprint "
        f"0x{result_a.fingerprint:016x} · last {events_a[-1].id if events_a else '-'}",
        f"arm B (modified) : {len(events_b)} events · ticks "
        f"0..{events_b[-1].t if events_b else 0} · fingerprint "
        f"0x{result_b.fingerprint:016x} · last {events_b[-1].id if events_b else '-'}",
    ]
    same = result_a.fingerprint == result_b.fingerprint
    out.append(
        "fingerprints     "
        + ("EQUAL (no RNG divergence)" if same else "DIVERGED (the RNG price)")
    )
    types_a, types_b = _counter(events_a, "type"), _counter(events_b, "type")
    delta = types_b - types_a
    drops = types_a - types_b
    parts = [f"+{name} x{n}" for name, n in sorted(delta.items())]
    parts.extend(f"-{name} x{n}" for name, n in sorted(drops.items()))
    out.append("event delta      " + (", ".join(parts) if parts else "none"))
    proj_delta: list[str] = []
    for entity in sorted(set(proj_a) | set(proj_b)):
        props_a = proj_a.get(entity, {})
        props_b = proj_b.get(entity, {})
        for prop in sorted(set(props_a) | set(props_b)):
            if props_a.get(prop) != props_b.get(prop):
                proj_delta.append(
                    f"{entity}.{prop}: {props_a.get(prop)!r} -> "
                    f"{props_b.get(prop)!r}"
                )
    out.append(
        "projection delta "
        + (", ".join(proj_delta[:12]) if proj_delta else "none")
        + (f" (+{len(proj_delta) - 12} more)" if len(proj_delta) > 12 else "")
    )
    seeds_a, seeds_b = _counter(events_a, "hooks"), _counter(events_b, "hooks")
    seed_delta = seeds_b - seeds_a
    seed_drop = seeds_a - seeds_b
    seed_parts = [f"+{name} x{n}" for name, n in sorted(seed_delta.items())]
    seed_parts.extend(f"-{name} x{n}" for name, n in sorted(seed_drop.items()))
    out.append("seed delta       " + (", ".join(seed_parts) if seed_parts else "none"))
    dir_a, dir_b = _counter(events_a, "director"), _counter(events_b, "director")
    out.append(
        "director events  "
        + (f"A {sum(dir_a.values())} -> B {sum(dir_b.values())}")
    )
    out.append(
        "note: both arms ran the same seed from t=0 (the corpus-price "
        "pattern); arm logs live under the gitignored output dir"
    )
    return "\n".join(out) + "\n"


# -- CLI ----------------------------------------------------------------------


def _parse_ticks(text: str) -> tuple[int | None, int | None]:
    left, _, right = text.partition(":")
    lo = int(left) if left else None
    hi = int(right) if right else None
    return lo, hi


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mechanics",
        description=(
            "Mechanics introspection for canonsim: static wiring (matrix), "
            "shadow-replay trace, hook postmortems (why), two-arm blast."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    m = sub.add_parser("matrix", help="static wiring off the loaded pack")
    m.add_argument("--pack", type=Path, default=PACK_DIR)
    m.add_argument("--event", help="narrow to one event type")
    m.add_argument("--hook", help="narrow to one director hook tag")
    m.add_argument("--token", help="narrow to one knowledge token")
    m.add_argument("--prop", help="narrow to one projection prop path")

    t = sub.add_parser("trace", help="per-tick execution view of a log")
    t.add_argument("--log", type=Path, help="a committed log to replay")
    t.add_argument("--script", type=Path, help="a playscript to run fresh")
    t.add_argument("--pack", type=Path, default=PACK_DIR)
    t.add_argument("--ticks", help="tick window, e.g. 700:800 or :800")
    t.add_argument("--tail", type=int, help="the last N ticks only")
    t.add_argument("--entity", help="only events touching this entity")
    t.add_argument("--hook", help="only this hook's seeds/releases")
    t.add_argument("--event", help="only events of this type")

    w = sub.add_parser("why", help="postmortem: why a hook did/didn't release")
    w.add_argument("--hook", required=True)
    w.add_argument("--log", type=Path)
    w.add_argument("--script", type=Path)
    w.add_argument("--at-tick", type=int, default=None)
    w.add_argument("--pack", type=Path, default=PACK_DIR)

    b = sub.add_parser("blast", help="two-arm same-seed A/B over a script")
    b.add_argument("--script", type=Path, required=True)
    b.add_argument(
        "--step-json", help="a playscript step to insert (JSON text)"
    )
    b.add_argument(
        "--at", type=int, default=None, help="insert position (default: append)"
    )
    b.add_argument("--pack", type=Path, default=PACK_DIR)
    b.add_argument("--out", type=Path, default=MECH_OUT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    pack, schema = _load(args.pack)
    if args.command == "matrix":
        print(
            render_matrix(
                pack,
                event=args.event,
                hook=args.hook,
                token=args.token,
                prop=args.prop,
            ),
            end="",
        )
        return 0
    if args.command == "trace":
        source, events, header = _events_from_source(
            pack, schema, args.log, args.script
        )
        lo, hi = _parse_ticks(args.ticks) if args.ticks else (None, None)
        if args.tail is not None:
            last = events[-1].t if events else 0
            lo, hi = max(0, last - args.tail + 1), last
        print(
            render_trace(
                pack,
                events,
                source=source,
                seed=header.get("seed", "-"),
                tick_from=lo,
                tick_to=hi,
                entity=args.entity,
                hook=args.hook,
                event_type=args.event,
            ),
            end="",
        )
        return 0
    if args.command == "why":
        source, events, header = _events_from_source(
            pack, schema, args.log, args.script
        )
        print(
            render_why(
                pack, events, tag=args.hook, at_tick=args.at_tick, source=source
            ),
            end="",
        )
        return 0
    script = load_playscript(args.script)
    step = json.loads(args.step_json) if args.step_json else None
    if step is not None and not isinstance(step, Mapping):
        raise SystemExit("error: --step-json must be a JSON object (a step)")
    print(
        run_blast(pack, schema, script, step, args.at, args.out),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
