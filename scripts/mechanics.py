"""The mechanics introspection CLI (mech-1, iter-84; mech-2, iter-163;
mech-2's impact surface, iter-196; D-046 operator tooling).

Five read-only instruments over the committed pack and committed (or freshly
run) logs, for the per-instance questions the prose specs answer only
generally: "who consumes event type X", "why has hook Y not released by tick
T", "why did event E happen", "what changes if step Z is inserted here",
"what reads pack path P / which sites reference name N". Everything here is
DERIVED, rebuildable, never truth (the checkpoint.py
law): the pack JSON and the engine's public functions are the only sources.
Output is stdout; the blast arms write their logs under the gitignored
output/mech/ dir.

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

The attention budget (mech-2, D-128's effect line): DEFAULTS are bounded
to what a reading agent scans in one screen, and nothing bounded is
dropped silently — every capped view names what was cut and the flag that
shows it (D-148's [truncated:N] law applied to CLI defaults). An
unqualified `trace` shows the last DEFAULT_TRACE_WINDOW_TICKS ticks; an
unqualified `matrix` shows the compact name inventory (`--full` for the
whole); the event postmortem caps its chain/children detail at named
constants. Every explicit flag is the operator's own window or question —
answered in full, never second-guessed.

The impact surface (mech-2's row, iter-196 — intake-37's named consumer,
the agent-edit loop's tool): the static blast radius of an ARBITRARY pack
path, beyond matrix's indexed hook/event/token/prop quadruple. The reader
set is DERIVED from the repo source at run time — an AST scan for
rules-rooted literal accesses (`rules.get("director")`,
`self._data["rules.json"]`, the `*_BLOCK` constants) across core/brief/
render/cli/sim (runtime) and core/packlint + core/pack.py (load-time lint);
scripts/ is excluded (operator tooling, D-046). Derived, never truth
(D-118 extended to the source itself): never a hand table, a new system is
visible the iteration it lands. The reverse query walks the four pack files
for exact-name sites (dict keys, list members, scalar values — the
rename-safety set; substrings are not references). Bounded one-hop
traversal (intake-37's principles, never copied tools): sound at block
level, literal-precise where the source is literal, honest about dynamic
keying; every reader is reported as a minimal witness (file:line + the
source text), never a bare claim.

Usage:
    python scripts/mechanics.py matrix [--pack DIR] [--event TYPE]
        [--hook TAG] [--token TOKEN] [--prop PATH] [--full] [--dag]
    python scripts/mechanics.py impact (--path PACK_PATH | --ref NAME)
        [--pack DIR] [--full]
    python scripts/mechanics.py trace (--log PATH | --script PATH) [--pack DIR]
        [--ticks A:B] [--tail N] [--entity ID] [--hook TAG] [--event TYPE]
    python scripts/mechanics.py why (--hook TAG | --event ID)
        (--log PATH | --script PATH) [--at-tick N] [--pack DIR]
    python scripts/mechanics.py blast --script PATH [--step-json JSON]
        [--at N] [--pack DIR] [--out DIR]

D-012 (stdlib + core only), INV-4 (no LLM/network), INV-5 (never writes
into logs/; blast arms write only gitignored output/mech/).
"""

from __future__ import annotations

import argparse
import ast
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
from core.scheduler import decls_from_rules  # noqa: E402
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
# mech-2 caps (the attention budget, D-128): named constants, one home.
# Measured on the canonical runs at iter-163's HEAD: the last 720 ticks
# render 27 lines (day1_full) / 43 (province_feud) — a screenful of recent
# history, never the O(events) dump (175/277 lines at full width).
DEFAULT_TRACE_WINDOW_TICKS: Final = 720
# The single-event postmortem's detail caps: nearest links/descendants
# shown, the rest counted on the truncation line (anti-silent-drop).
CHAIN_DETAIL_LINKS: Final = 8
CHILD_DETAIL_LINES: Final = 12
# The impact surface's caps (iter-196, the same attention budget): reader
# witnesses and reference sites listed per query; --full uncaps (the
# operator's own window). The value summary shows at most this many keys.
IMPACT_READERS_CAP: Final = 10
IMPACT_REFS_CAP: Final = 16
IMPACT_VALUE_KEYS: Final = 6
IMPACT_EXPR_WIDTH: Final = 72


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


def _matrix_name_inventory(pack: Pack) -> dict[str, list[str]]:
    """The queryable name spaces as sorted lists: hook tags, event types,
    knowledge tokens (the matrix query vocabulary — the compact default
    lists them so the operator never reads rules.json just to ask)."""
    hooks = sorted(pack.rules.get("director", {}).get("hooks", {}))
    events: set[str] = set()
    for action in _action_rows(pack):
        for event_type in (action.get("events") or {}).values():
            if isinstance(event_type, str):
                events.add(event_type)
    events.update(pack.rules.get("on_action", {}))
    tokens = sorted({
        token
        for entries in _event_knowledge_tokens(pack).values()
        for token in entries
    })
    return {"hooks": hooks, "events": sorted(events), "tokens": tokens}


def _render_matrix_compact(pack: Pack) -> list[str]:
    """The bounded default: one (wrapped) line per name space, the read-side
    folds, the unindexed blocks, and the query note. Every fact here is a
    NAME the four narrow flags accept — the wiring itself stays in --full
    or the per-object views."""
    names = _matrix_name_inventory(pack)
    out: list[str] = []
    for label, key in (("hooks", "hooks"), ("events", "events"),
                       ("tokens", "tokens")):
        items = names[key]
        out.append(
            f"{label} ({len(items)}): "
            + (", ".join(items) if items else "-")
        )
    arcs = pack.rules.get("director", {}).get("arcs", {})
    if arcs:
        out.append(
            "arcs: "
            + ", ".join(
                f"{name}[{' > '.join(str(m) for m in arc.get('members', ()))}]"
                if isinstance(arc, Mapping)
                else f"{name}[?]"
                for name, arc in sorted(arcs.items())
            )
        )
    echo = pack.rules.get("echo", {})
    traits = pack.rules.get("traits", {})
    out.append(
        f"read-side folds: echo {len(echo.get('tokens', {}))} valence tokens · "
        f"scale {json.dumps(echo.get('scale'))} · traits threshold "
        f"{traits.get('threshold')} · "
        f"{len(traits.get('beliefs', {}))} belief families (crystallized)"
    )
    unindexed = sorted(
        key
        for key in pack.rules
        if key not in INDEXED_BLOCKS and key != "notes"
    )
    out.append(
        "unindexed rules blocks (shape rules join here, never a rewrite): "
        + (", ".join(unindexed) if unindexed else "-")
    )
    out.append(
        "query: --hook TAG · --event TYPE · --token TOKEN · --prop PATH · "
        "--dag (the systems graph) · --full (the whole inventory)"
    )
    return out


def render_matrix(
    pack: Pack,
    *,
    event: str | None = None,
    hook: str | None = None,
    token: str | None = None,
    prop: str | None = None,
    full_inventory: bool = True,
) -> str:
    """The static wiring matrix: pack-declared producers/consumers/hooks.
    Query flags narrow to one object; without flags the compact name
    inventory prints by default (mech-2's attention budget) and --full
    restores the whole listing. Unknown rules blocks are listed generically
    — the future-layer fallback (visible immediately, indexed when shaped)."""
    narrow = bool(hook or event or token or prop)
    header = "static wiring"
    if not narrow and not full_inventory:
        header += " (compact — the default view)"
    out: list[str] = [f"== MATRIX {pack.name_version} — {header} =="]
    if hook:
        out.extend(_render_matrix_hook(pack, hook))
    if event:
        out.extend(_render_matrix_event(pack, event))
    if token:
        out.extend(_render_matrix_token(pack, token))
    if prop:
        out.extend(_render_matrix_prop(pack, prop))
    if not narrow and not full_inventory:
        out.append("")
        out.extend(_render_matrix_compact(pack))
        return "\n".join(out) + "\n"
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


def trace_window(
    events: Sequence[EventRecord],
    *,
    ticks: str | None = None,
    tail: int | None = None,
    entity: str | None = None,
    hook: str | None = None,
    event_type: str | None = None,
) -> tuple[int | None, int | None, str | None]:
    """The trace window policy (mech-2's cap, D-128): an unqualified trace
    defaults to the last DEFAULT_TRACE_WINDOW_TICKS ticks; every explicit
    flag is the operator's own window or filter — answered in full. Returns
    (lo, hi, note); the note names what was cut and the expansion flags
    (the anti-silent-drop law) and is None whenever nothing was cut."""
    last = events[-1].t if events else 0
    if tail is not None or ticks is not None or entity or hook or event_type:
        if tail is not None:
            return max(0, last - tail + 1), last, None
        lo, hi = _parse_ticks(ticks) if ticks else (None, None)
        return lo, hi, None
    lo = max(0, last - DEFAULT_TRACE_WINDOW_TICKS + 1)
    if lo == 0:
        return None, None, None
    note = (
        f"-- default window: the last {DEFAULT_TRACE_WINDOW_TICKS} of "
        f"{last} ticks (the attention budget); pass --ticks 0: for the "
        "whole run, --tail N for the last N ticks, --ticks A:B for a "
        "window, or --entity/--hook/--event to narrow"
    )
    return lo, last, note


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
    window_note: str | None = None,
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
    if window_note is not None:
        out.append(window_note)
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


# -- why --event: the single-event postmortem (intake-21, mech-2) -------------


def render_why_event(
    pack: Pack,
    events: Sequence[EventRecord],
    *,
    event_id: str,
    source: str = "-",
) -> str:
    """The one-event read (intake-21's form): one event id in — the event's
    own record, the backward cause chain (the log's own `cause` links, one
    parent each), the knowledge it minted joined to the pack's static
    wiring (what those tokens feed), and the forward cascade of
    descendants. Values are log facts; the director attribution is the
    shadow's (D-118); the wiring joins are pack declarations (D-024)."""
    out = [f"== WHY — event {event_id} · {source} =="]
    by_id = {event.id: event for event in events}
    event = by_id.get(event_id)
    if event is None:
        last_id = events[-1].id if events else "ev_0000"
        out.append(
            f"no such event id in this log (ids run ev_0000..{last_id})"
        )
        return "\n".join(out) + "\n"
    replay = shadow_replay(pack, events)
    out.append("event")
    out.extend(_render_event(event, replay.intent_tags))

    # -- the backward chain: exactly one parent per event (the writer's law)
    chain: list[EventRecord] = []
    cursor: str | None = event.cause
    while cursor is not None and cursor in by_id:
        parent = by_id[cursor]
        chain.append(parent)
        cursor = parent.cause
    if cursor is not None:
        out.append(
            f"cause chain  stops at {cursor!r} — a cause naming no event in "
            "this log (cross-log continuation?)"
        )
    elif not chain:
        out.append("cause chain  none — the run-start event (cause null)")
    else:
        root = chain[-1]
        shown = chain[:CHAIN_DETAIL_LINKS]
        out.append(
            f"cause chain  {len(chain)} link(s) back to {root.id} "
            f"({root.type} @ t={root.t})"
        )
        for link in shown:
            out.append(
                f"  [t={link.t}] {link.id} {link.type} · actor={link.actor}"
            )
        hidden = len(chain) - len(shown)
        if hidden > 0:
            out.append(
                f"  (+{hidden} earlier links; walk back with "
                f"why --event {shown[-1].id})"
            )

    # -- the knowledge section: minted tokens joined to their static wiring
    if event.knowledge:
        tokens = sorted({record.knows for record in event.knowledge})
        out.append(
            f"knowledge    {len(event.knowledge)} record(s) minted · "
            f"{len(tokens)} distinct token(s)"
        )
        crime_map = _crime_map(pack)
        echo_tokens = pack.rules.get("echo", {}).get("tokens", {})
        families = pack.rules.get("traits", {}).get("beliefs", {})
        for token in tokens:
            parts = []
            crime = crime_map.get(token)
            if crime:
                parts.append(f"crime {crime[0]} +{crime[1]}")
            valence = echo_tokens.get(token)
            if valence:
                parts.append(f"echo {json.dumps(valence, sort_keys=True)}")
            fed = sorted(
                name
                for name, family in families.items()
                if isinstance(family, Mapping)
                and token in json.dumps(family.get("tokens", family))
            )
            if fed:
                parts.append(f"traits {', '.join(fed)}")
            out.append(
                f"  {token}  ->  "
                + (" · ".join(parts) if parts else "no declared consumer")
            )
    else:
        out.append("knowledge    none minted")

    # -- the forward cascade: every descendant citing this event (BFS)
    children: dict[str, list[EventRecord]] = {}
    for e in events:
        if e.cause is not None:
            children.setdefault(e.cause, []).append(e)
    direct = children.get(event.id, [])
    total = 0
    detail: list[tuple[int, EventRecord]] = []
    frontier: list[EventRecord] = list(direct)
    depth = 1
    while frontier:
        total += len(frontier)
        for child in frontier:
            if len(detail) < CHILD_DETAIL_LINES:
                detail.append((depth, child))
        frontier = [
            child for parent in frontier for child in children.get(parent.id, ())
        ]
        depth += 1
    if total == 0:
        out.append("children     none — no event cites this one as its cause")
    else:
        out.append(
            f"children     {len(direct)} direct · {total} descendant(s) "
            "total (the downstream cascade)"
        )
        for child_depth, child in detail:
            out.append(
                f"  {'  ' * (child_depth - 1)}[t={child.t}] {child.id} "
                f"{child.type} · actor={child.actor}"
            )
        hidden = total - len(detail)
        if hidden > 0:
            out.append(
                f"  (+{hidden} more descendants; zoom with "
                "why --event <id>)"
            )
    out.append(
        "note        the chain and children are the log's own cause links "
        "(EVENT_SCHEMA); the wiring joins are pack declarations; the "
        "release law is DIRECTOR_SPEC's (D-024)"
    )
    return "\n".join(out) + "\n"


# -- matrix --dag: the systems graph export (intake-22, mech-2) ---------------


def render_dag(pack: Pack) -> str:
    """The systems read/write graph as a Mermaid flowchart — the PROJECTION
    of rules.json::systems (intake-22's form): never a runtime, never a
    second truth (D-163). The parse rides the scheduler's own public
    decls (D-118 — display over the real pipeline, never a re-parse).
    Reads are dotted, writes solid, before/after hints thick (a runs
    before b), per_tick systems bold; the per-family blocks (weather,
    travel, economy, ...) declare their own wiring outside this graph —
    the verified asymmetry, stated in the header so the picture never
    overclaims coverage."""
    decls = decls_from_rules(pack.rules)
    out = [
        f"%% MERMAID flowchart — the SCHED-1 systems graph of "
        f"{pack.name_version}",
        "%% derived from rules.json::systems (the projection law — D-163;",
        "%% never truth: the pack JSON is the source, this view rebuilds)",
        "%% the per-family blocks (weather/travel/economy/...) declare their",
        "%% own wiring outside this graph (the verified asymmetry)",
        "flowchart LR",
    ]
    if not decls:
        out.append("  %% no systems declared in this pack")
    namespaces = sorted({
        name
        for decl in decls.values()
        for name in (*decl.reads, *decl.writes)
    })
    for name in sorted(decls):
        marker = ":::per_tick" if decls[name].per_tick else ""
        out.append(f'  sys_{name}["{name}"]{marker}')
    for ns in namespaces:
        out.append(f'  ns_{ns}("{ns}")')
    for name in sorted(decls):
        decl = decls[name]
        for ns in decl.reads:
            out.append(f"  sys_{name} -.-> ns_{ns}")
        for ns in decl.writes:
            out.append(f"  sys_{name} --> ns_{ns}")
    hints: set[tuple[str, str]] = set()
    for decl in decls.values():
        for other in decl.before:
            hints.add((decl.name, other))
        for other in decl.after:
            hints.add((other, decl.name))
    for a, b in sorted(hints):
        out.append(f"  sys_{a} ==>|before| sys_{b}")
    out.append("  classDef per_tick stroke-width:3px")
    out.append(
        "  %% reads -.-> · writes --> · ordering hint ==> (a runs before b)"
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


# -- impact: the agent impact surface (mech-2, iter-196) ----------------------


@dataclass(frozen=True)
class AccessSite:
    """One rules-rooted literal access in the repo source — the minimal
    witness: file, line, the literal key chain, the source line itself."""

    file: str
    line: int
    chain: tuple[str, ...]
    expr: str


@dataclass(frozen=True)
class RefSite:
    """One exact-name reference inside the pack's four files."""

    file: str
    path: str
    role: str


_RULES_ARG_NAMES: Final = frozenset({"rules", "pack_rules"})
_IDENTITY_KEYS: Final = ("id", "intent", "npc", "name")
_FILE_NAMESPACES: Final = ("rules", "actions", "entities", "templates")
_SCAN_ROOTS: Final = ("core", "brief", "render", "cli", "sim")
_ACCESS_SITES: list[AccessSite] | None = None


def _module_string_constants(tree: ast.Module) -> dict[str, str]:
    """Module-level NAME = "literal" bindings (the `*_BLOCK` convention)."""
    consts: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets: list[ast.expr] = node.targets
            value: ast.expr = node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            for target in targets:
                if isinstance(target, ast.Name):
                    consts[target.id] = value.value
    return consts


def _is_rules_root(node: ast.AST) -> bool:
    """The rules-dict roots: a `rules`/`pack_rules` name, any `.rules`
    attribute (pack.rules, self._pack.rules), any `x["rules.json"]`."""
    if isinstance(node, ast.Name):
        return node.id in _RULES_ARG_NAMES
    if isinstance(node, ast.Attribute):
        return node.attr == "rules"
    return isinstance(node, ast.Subscript) and (
        isinstance(node.slice, ast.Constant) and node.slice.value == "rules.json"
    )


def _literal_key(
    node: ast.AST | None, consts: Mapping[str, str]
) -> str | None:
    """A string literal, or a module constant resolving to one."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    return None


def _access_chain(
    node: ast.AST, consts: Mapping[str, str]
) -> tuple[str, ...] | None:
    """The literal key chain of a rules-rooted access expression, or None.
    `rules.get("a", {}).get("b")` -> ("a", "b"); a dynamic key mid-chain
    stops the chain where it goes dynamic (block-level honesty); a dynamic
    key at the ROOT drops the site entirely — an unattributable access is
    never guessed into a block (the honest boundary)."""
    if _is_rules_root(node):
        return ()
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        if node.func.attr != "get":
            return None
        base = _access_chain(node.func.value, consts)
        if base is None:
            return None
        key = _literal_key(node.args[0], consts) if node.args else None
        if key is None:
            return None if not base else base
        return (*base, key)
    if isinstance(node, ast.Subscript):
        base = _access_chain(node.value, consts)
        if base is None:
            return None
        key = _literal_key(node.slice, consts)
        if key is None:
            return None if not base else base
        return (*base, key)
    return None


def _site_class(rel_path: str) -> str:
    """runtime vs load-time lint (the repo's own structure law: packlint +
    pack.py are the admission surface; scripts/ never enters the scan)."""
    if rel_path.startswith("core/packlint/") or rel_path == "core/pack.py":
        return "lint"
    return "runtime"


def block_access_sites() -> list[AccessSite]:
    """The derived reader index: every rules-rooted literal access across
    the runtime modules and the load-time lint (D-118 — derived from the
    source itself, never a hand table; a new system appears here the
    iteration it lands). `*_BLOCK` constants resolve cross-module (the
    importing module sees the defining module's literal — a name mapping
    to one distinct value repo-wide); a bare whole-`rules` argument pass is
    skipped — the callee's own literal access is the precise site;
    same-line nested accesses collapse to the longest chain."""
    global _ACCESS_SITES
    if _ACCESS_SITES is not None:
        return _ACCESS_SITES
    files = sorted(
        {
            path
            for name in _SCAN_ROOTS
            if (REPO / name).is_dir()
            for path in (REPO / name).rglob("*.py")
        }
    )
    parsed: list[tuple[str, ast.Module, list[str]]] = []
    shared_consts: dict[str, str] = {}
    ambiguous: set[str] = set()
    for path in files:
        rel = path.relative_to(REPO).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError, ValueError):
            continue
        parsed.append((rel, tree, source.splitlines()))
        for name, value in _module_string_constants(tree).items():
            if shared_consts.get(name, value) != value:
                ambiguous.add(name)
            shared_consts[name] = value
    for name in ambiguous:
        del shared_consts[name]
    found: list[AccessSite] = []
    for rel, tree, lines in parsed:
        consts = {**shared_consts, **_module_string_constants(tree)}
        by_line: dict[tuple[str, int], AccessSite] = {}
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Call, ast.Subscript)):
                continue
            chain = _access_chain(node, consts)
            if not chain:
                continue
            text = lines[node.lineno - 1].strip()
            if len(text) > IMPACT_EXPR_WIDTH:
                text = text[: IMPACT_EXPR_WIDTH - 1] + "…"
            site = AccessSite(rel, node.lineno, chain, text)
            key = (rel, node.lineno)
            prior = by_line.get(key)
            if prior is None or len(chain) > len(prior.chain):
                by_line[key] = site
        found.extend(by_line.values())
    found.sort(key=lambda site: (site.file, site.line))
    _ACCESS_SITES = found
    return found


def _classify_access(
    chain: tuple[str, ...], query: tuple[str, ...]
) -> str | None:
    """'subtree' (the access touches the queried path's subtree, either
    direction), 'sibling' (same block, different branch), or None."""
    if not query:
        return "subtree"
    if not chain or chain[0] != query[0]:
        return None
    short, long = (
        (chain, query) if len(chain) <= len(query) else (query, chain)
    )
    if long[: len(short)] == short:
        return "subtree"
    return "sibling"


def _list_segment(item: Any, index: int) -> str:
    """The display segment for a list entry: its identity key (id/intent/
    npc/name) when declared, else the index (both are --path-usable)."""
    if isinstance(item, Mapping):
        for key in _IDENTITY_KEYS:
            value = item.get(key)
            if isinstance(value, str):
                return value
    return str(index)


def _step_into(node: Any, segment: str) -> tuple[Any, str | None]:
    """One path segment: dict keys, list indices, and identity-key lookup
    inside lists. Returns (child, error)."""
    if isinstance(node, Mapping):
        if segment in node:
            return node[segment], None
        keys = ", ".join(sorted(str(key) for key in node)[:8]) or "-"
        return None, f"no key {segment!r} (keys: {keys})"
    if isinstance(node, list):
        if segment.lstrip("-").isdigit():
            index = int(segment)
            if -len(node) <= index < len(node):
                return node[index], None
            return None, f"index {segment} out of range (0..{len(node) - 1})"
        for item in node:
            if isinstance(item, Mapping) and any(
                item.get(key) == segment for key in _IDENTITY_KEYS
            ):
                return item, None
        entries = ", ".join(
            _list_segment(item, position) for position, item in enumerate(node[:8])
        )
        return None, f"no entry {segment!r} in list (entries: {entries})"
    return None, f"leaf {node!r} carries no children"


def _resolve_pack_path(
    pack: Pack, dotted: str
) -> tuple[str, tuple[str, ...], Any, str]:
    """Resolve one dotted path against the four files. Namespace grammar:
    a bare first segment addresses rules.json (the default); `rules.` is
    the explicit form; `actions.` addresses the actions list by intent
    (or `actions.meta…`); `entities.`/`templates.` address their top-level
    keys, entity lists by id. Returns (file_name, query_chain, node,
    display_path); a miss fails loud with the deepest resolved position."""
    segments = [seg for seg in dotted.split(".") if seg]
    if not segments:
        raise SystemExit("error: --path is empty")
    if segments[0] in _FILE_NAMESPACES:
        namespace = segments[0]
        rest = segments[1:]
    else:
        namespace = "rules"
        rest = segments
    file_name = f"{namespace}.json"
    root: Any = pack.data[file_name]
    prefix: list[str] = []
    if namespace == "actions" and rest and rest[0] not in root:
        # the dominant list: `actions.steal…` addresses the action record
        # by intent (the top dict only carries meta + the list itself)
        child, err = _step_into(root["actions"], rest[0])
        if err is not None:
            raise SystemExit(
                f"error: --path {dotted!r} does not resolve at "
                f"actions.{rest[0]}: {err}"
            )
        root, rest, prefix = child, rest[1:], [rest[0]]
    node: Any = root
    for position, seg in enumerate(rest):
        child, err = _step_into(node, seg)
        if err is not None:
            where = ".".join([namespace, *prefix, *rest[:position]]) or namespace
            raise SystemExit(
                f"error: --path {dotted!r} does not resolve at {where}: {err}"
            )
        node = child
    display = ".".join([namespace, *prefix, *rest])
    query = tuple(rest) if namespace == "rules" else ()
    return file_name, query, node, display


def _value_summary(node: Any) -> str:
    """A bounded one-line shape of the resolved value (anti-silent-drop:
    the cut names its count)."""
    if isinstance(node, Mapping):
        keys = [str(key) for key in node]
        shown = ", ".join(sorted(keys)[:IMPACT_VALUE_KEYS])
        more = (
            f" (+{len(keys) - IMPACT_VALUE_KEYS} more)"
            if len(keys) > IMPACT_VALUE_KEYS
            else ""
        )
        return f"dict, {len(keys)} key(s): {shown or '-'}{more}"
    if isinstance(node, list):
        return f"list, {len(node)} item(s)"
    text = repr(node)
    if len(text) > IMPACT_EXPR_WIDTH:
        text = text[: IMPACT_EXPR_WIDTH - 1] + "…"
    return text


def _reference_sites(pack: Pack, name: str) -> list[RefSite]:
    """Every exact-name site across the four files: dict keys, list
    members, scalar values — the rename-safety set. Substring matches are
    not references; display paths are --path-usable (the file's own
    namespace-prefix key collapses into the namespace)."""
    out: list[RefSite] = []

    def visit(key: Any, value: Any, path: tuple[str, ...], file: str) -> None:
        skey = str(key)
        if skey == name:
            out.append(RefSite(file, ".".join((*path, skey)), "key"))
        walk(value, (*path, skey), file)

    def walk(node: Any, path: tuple[str, ...], file: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                visit(key, value, path, file)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                if isinstance(item, str):
                    if item == name:
                        out.append(
                            RefSite(file, ".".join((*path, str(index))), "member")
                        )
                    continue
                walk(item, (*path, _list_segment(item, index)), file)
        elif isinstance(node, str) and node == name:
            out.append(RefSite(file, ".".join(path), "value"))

    for file_name in sorted(pack.data):
        namespace = file_name.removesuffix(".json")
        top = pack.data[file_name]
        if isinstance(top, Mapping):
            for key, value in top.items():
                if str(key) == namespace:  # actions.json's list: the ns covers it
                    walk(value, (namespace,), file_name)
                else:
                    visit(key, value, (namespace,), file_name)
        else:
            walk(top, (namespace,), file_name)
    return out


def _name_roles(pack: Pack, name: str) -> list[tuple[str, str]]:
    """(role, matrix pointer) pairs for a name against the pack's own
    vocabularies — the indexed quadruple keeps its single owner (D-024).
    on_action's prose keys (str-valued, e.g. `notes`) are not event types:
    subtracted locally, the matrix inventory itself untouched."""
    roles: list[tuple[str, str]] = []
    names = _matrix_name_inventory(pack)
    prose_keys = {
        key
        for key, value in pack.rules.get("on_action", {}).items()
        if not isinstance(value, list)
    }
    if name in names["hooks"]:
        roles.append(("director hook tag", f"matrix --hook {name}"))
    if (name in names["events"] and name not in prose_keys) or (
        name in pack.event_types()
    ):
        roles.append(("event type", f"matrix --event {name}"))
    if name in names["tokens"]:
        roles.append(("knowledge token", f"matrix --token {name}"))
    if pack.entity(name) is not None:
        roles.append((f"entity id ({pack.kind_of(name) or '?'})", ""))
    return roles


def _render_impact_readers(
    pack: Pack, query: tuple[str, ...], full: bool
) -> list[str]:
    """The derived reader set for a rules query chain: runtime witnesses
    first, then the load-time lint surface (the edit's admission gate)."""
    blocks = set(pack.rules)
    relevant: list[tuple[AccessSite, str]] = []
    siblings = 0
    for site in block_access_sites():
        if site.chain[0] not in blocks:
            continue
        kind = _classify_access(site.chain, query)
        if kind == "subtree":
            relevant.append((site, _site_class(site.file)))
        elif kind == "sibling":
            siblings += 1
    runtime = [site for site, cls in relevant if cls == "runtime"]
    lint = [site for site, cls in relevant if cls == "lint"]
    out: list[str] = []
    scope = (
        "across ALL rules blocks (the whole-file query)"
        if not query
        else f"({len(runtime)} site(s)):"
        if runtime
        else ""
    )
    if runtime:
        cap = len(runtime) if full else IMPACT_READERS_CAP
        out.append(f"readers      runtime {scope}")
        for site in runtime[:cap]:
            out.append(
                f"  {site.file}:{site.line} · {site.expr} "
                f"[reads {'.'.join(site.chain)}]"
            )
        hidden = len(runtime) - cap
        if hidden > 0:
            out.append(f"  (+{hidden} more runtime site(s) — impact --full)")
    else:
        block = ".".join(query[:1]) or "rules"
        out.append(
            f"readers      runtime: none — no rules-rooted literal access "
            f"touches {block} (notes-only, dead data, or dynamic-only; "
            "scripts/ excluded, D-046)"
        )
    if lint:
        modules = sorted({site.file for site in lint})
        cap = len(modules) if full else 6
        shown = ", ".join(modules[:cap])
        hidden = len(modules) - cap
        extra = f" (+{hidden} more)" if hidden > 0 else ""
        out.append(f"             load-time lint: {shown}{extra}")
    if siblings and not full:
        out.append(
            f"             (+{siblings} same-block access(es) outside this "
            "subtree, not listed)"
        )
    return out


def _render_impact_path(pack: Pack, dotted: str, full: bool) -> str:
    """The forward query: one pack path in — the resolved value, the
    derived readers, the leaf name's reference set, the indexed pointers."""
    file_name, query, node, display = _resolve_pack_path(pack, dotted)
    out = [f"== IMPACT {pack.name_version} — path {dotted} =="]
    out.append(f"resolves     {display} — {_value_summary(node)}")
    if file_name == "rules.json":
        out.extend(_render_impact_readers(pack, query, full))
    else:
        out.append(
            "readers      keyed dynamically at runtime (pack.entity()/"
            "action()/event_types()) — the static surface is the reference "
            "set below"
        )
    leaf = display.split(".")[-1]
    refs = _reference_sites(pack, leaf)
    if refs:
        cap = len(refs) if full else IMPACT_REFS_CAP
        out.append(
            f"refs         {leaf!r} — {len(refs)} exact-name site(s) across "
            f"{len({site.file for site in refs})} file(s):"
        )
        for site in refs[:cap]:
            out.append(f"  {site.file:<14} {site.path} [{site.role}]")
        hidden = len(refs) - cap
        if hidden > 0:
            out.append(f"  (+{hidden} more — impact --full)")
    else:
        out.append(f"refs         {leaf!r} — no exact-name site in the four files")
    if isinstance(node, (Mapping, list)) and node:
        out.append(
            f"             {len(node)} name(s) sit under this subtree — "
            "impact --ref <name> each"
        )
    pointers: list[str] = []
    for seg in display.split("."):
        for label, pointer in _name_roles(pack, seg):
            if pointer:
                entry = f"{label} {seg} ({pointer})"
                if entry not in pointers:
                    pointers.append(entry)
    if pointers:
        out.append("indexed      " + " · ".join(pointers[:3]))
    out.append(
        "writers      none at runtime — the pack is read-only after load "
        "(INV-3/INV-1); state writes ride events (matrix --prop / trace the "
        "dynamic half)"
    )
    out.append(
        "note         derived, never truth (D-118): the reader set "
        "re-derives from the repo source at run time; value semantics ride "
        "goldens, path-bound (TEST_PLAN §9)"
    )
    return "\n".join(out) + "\n"


def _render_impact_ref(pack: Pack, name: str, full: bool) -> str:
    """The reverse query: one name in — every exact-name site in the four
    files, with the name's declared role where the pack has one."""
    sites = _reference_sites(pack, name)
    roles = _name_roles(pack, name)
    out = [f"== IMPACT {pack.name_version} — ref {name!r} =="]
    if roles:
        role_text = " · ".join(
            f"{label} ({pointer})" if pointer else label for label, pointer in roles
        )
        out.append(f"role         {role_text}")
    else:
        out.append("role         none in this pack's vocabularies")
    if not sites:
        out.append("sites        none — the name appears nowhere in the four files")
        return "\n".join(out) + "\n"
    by_file: dict[str, list[RefSite]] = {}
    for site in sites:
        by_file.setdefault(site.file, []).append(site)
    out.append(
        f"sites        {len(sites)} exact-name reference(s) across "
        f"{len(by_file)} file(s)"
    )
    cap = len(sites) if full else IMPACT_REFS_CAP
    shown = 0
    for file_name in sorted(by_file):
        for site in by_file[file_name]:
            if shown >= cap:
                break
            out.append(f"  {file_name:<14} {site.path} [{site.role}]")
            shown += 1
    hidden = len(sites) - cap
    if hidden > 0:
        out.append(f"  (+{hidden} more — impact --full)")
    out.append(
        "note         exact-name matching (keys, list members, scalar "
        "values) — substring matches are not references (the "
        "rename-safety set)"
    )
    return "\n".join(out) + "\n"


def render_impact(
    pack: Pack,
    *,
    path: str | None = None,
    ref: str | None = None,
    full: bool = False,
) -> str:
    """The agent impact surface (mech-2's row, intake-37's named consumer):
    `--path` the static blast radius of one pack path (derived readers,
    exact-name cross references, the indexed-matrix pointers); `--ref` the
    reverse query — which sites reference a name. Bounded one-hop
    traversal: sound at block level, literal-precise where the source is
    literal, honest about dynamic keying (D-118 — derived, never truth)."""
    if path is not None:
        return _render_impact_path(pack, path, full)
    if ref is not None:
        return _render_impact_ref(pack, ref, full)
    raise SystemExit("error: exactly one of --path / --ref is required")


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
    m.add_argument(
        "--full",
        action="store_true",
        help="the whole inventory (the default view is the compact one)",
    )
    m.add_argument(
        "--dag",
        action="store_true",
        help="the systems read/write graph as Mermaid (rules.json::systems)",
    )

    i = sub.add_parser(
        "impact",
        help="the agent impact surface: one pack path's derived readers + "
        "references, or the reverse query (which sites reference a name)",
    )
    target = i.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--path",
        help="a dotted pack path: rules.<block>... (bare block name = "
        "rules), actions.<intent>..., entities.<category>.<id>..., "
        "templates.<key>...",
    )
    target.add_argument(
        "--ref", help="the reverse query: every exact-name site in the "
        "four files (the rename-safety set)"
    )
    i.add_argument("--pack", type=Path, default=PACK_DIR)
    i.add_argument(
        "--full",
        action="store_true",
        help="uncap the reader/reference listings (the default caps name "
        "their cuts)",
    )

    t = sub.add_parser("trace", help="per-tick execution view of a log")
    t.add_argument("--log", type=Path, help="a committed log to replay")
    t.add_argument("--script", type=Path, help="a playscript to run fresh")
    t.add_argument("--pack", type=Path, default=PACK_DIR)
    t.add_argument("--ticks", help="tick window, e.g. 700:800 or :800")
    t.add_argument("--tail", type=int, help="the last N ticks only")
    t.add_argument("--entity", help="only events touching this entity")
    t.add_argument("--hook", help="only this hook's seeds/releases")
    t.add_argument("--event", help="only events of this type")

    w = sub.add_parser(
        "why", help="postmortem: why a hook did/didn't release, or one "
        "event's cause chain + knowledge + cascade"
    )
    target = w.add_mutually_exclusive_group(required=True)
    target.add_argument("--hook", help="the hook postmortem")
    target.add_argument(
        "--event", help="the single-event postmortem: one event id in"
    )
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
        if args.dag and (args.full or args.event or args.hook
                         or args.token or args.prop):
            raise SystemExit(
                "error: --dag cannot be combined with --full/--event/"
                "--hook/--token/--prop (it is its own view)"
            )
        if args.dag:
            print(render_dag(pack), end="")
            return 0
        print(
            render_matrix(
                pack,
                event=args.event,
                hook=args.hook,
                token=args.token,
                prop=args.prop,
                full_inventory=args.full,
            ),
            end="",
        )
        return 0
    if args.command == "impact":
        print(
            render_impact(pack, path=args.path, ref=args.ref, full=args.full),
            end="",
        )
        return 0
    if args.command == "trace":
        source, events, header = _events_from_source(
            pack, schema, args.log, args.script
        )
        lo, hi, note = trace_window(
            events,
            ticks=args.ticks,
            tail=args.tail,
            entity=args.entity,
            hook=args.hook,
            event_type=args.event,
        )
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
                window_note=note,
            ),
            end="",
        )
        return 0
    if args.command == "why":
        source, events, header = _events_from_source(
            pack, schema, args.log, args.script
        )
        if args.event is not None:
            if args.at_tick is not None:
                raise SystemExit(
                    "error: --at-tick applies to --hook only "
                    "(the event pins its own tick)"
                )
            print(
                render_why_event(
                    pack, events, event_id=args.event, source=source
                ),
                end="",
            )
            return 0
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
