"""The pack doctor (iter-107, the risk-synthesis §1 rider — the lint's
fix-hint surface; the authoring loop's gate reader).

The lint (`core/pack.py`) is the single admission gate and its errors
already carry the WHERE. The doctor turns a refusal into a diagnosis:
the offending file + block parsed out of the message, the block's
owner doc, the practical fix family (the KI-history shapes), and —
with --trace — the offending block's own data. The green path prints
the pack's health inventory (entities, verbs, systems, hooks, the
armed optional blocks). This closes the autonomous loop's read half:
author JSON → lint → doctor (fix-hint) → patch — the same
self-healing shape the parser boundary gives the reply side.

Periphery (D-046): reads packs, prints, never touches the engine.

Usage:
    python -m scripts.pack_doctor [<dir>]           # default: the tavern
    python -m scripts.pack_doctor <dir> --trace     # + the failing block
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.pack import PACK_FILE_NAMES, PackError, load_pack  # noqa: E402

DEFAULT_DIR = REPO / "content" / "tavern_pack"

#: The block → owner-doc map (FILES, never sections — zero drift risk;
#: the section numbers live in the docs themselves). Blocks without a
#: confident owner fall back to the navigation map (NAV §1).
_DOC_OWNERS: dict[str, str] = {
    "meta": "docs/MVP_SCOPE.md",
    "time": "docs/MVP_SCOPE.md",
    "systems": "docs/blueprint/phase0.md",
    "transitions": "docs/MVP_SCOPE.md",
    "knowledge": "docs/MVP_SCOPE.md",
    "acquisition": "docs/MVP_SCOPE.md",
    "crime_watch": "docs/MVP_SCOPE.md",
    "expectations": "docs/MVP_SCOPE.md",
    "states": "docs/MVP_SCOPE.md",
    "urgencies": "docs/MVP_SCOPE.md",
    "checks": "docs/INTENT_SCHEMA.md",
    "importance": "docs/EVENT_SCHEMA.md",
    "factions": "docs/blueprint/phases.md",
    "names": "docs/blueprint/phases.md",
    "worldgen": "docs/blueprint/phases.md",
    "travel": "docs/blueprint/phases.md",
    "weather": "docs/blueprint/phases.md",
    "scene_detail": "docs/blueprint/phases.md",
    "director": "docs/DIRECTOR_SPEC.md",
    "on_action": "docs/MVP_SCOPE.md",
    "secrets": "docs/MVP_SCOPE.md",
    "brief": "docs/BRIEF_SPEC.md",
    "templates": "docs/EVENT_SCHEMA.md",
    "entities": "docs/MVP_SCOPE.md",
    "actions": "docs/INTENT_SCHEMA.md",
    "metrics": "docs/TEST_PLAN.md",
}

#: The fix families (the KI history's recurring shapes — the practical
#: half of the hint; the message itself carries the specifics).
_FIX_HINTS: dict[str, str] = {
    "urgencies": "urgency entries' preconditions (echo_at_least / "
                 "trait_held / leverage_over) must name declared axes, "
                 "belief tokens or live clusters — declare the axis in the "
                 "owning block or drop the precondition; the lint order "
                 "runs traits before urgencies (the KI#77 family)",
    "transitions": "every layer needs a per-tick systems row, a spot_field, "
                   "events inside the template closure, and non-empty "
                   "follow_ups; actions' ignition configs must name a "
                   "declared layer, and spot_available preconditions too",
    "worldgen": "claims bind slot to a site's field per location; scene-"
                "detail overlap and double-claims refuse; the map geometry "
                "feeds the LOD warm ring",
    "travel": "the pairing law runs both ways: an edge-priced action "
              "declares the travel block, and every exits edge must be "
              "priceable; overrides are real undirected edges only",
    "systems": "write-write conflicts between per-tick systems need "
               "explicit before/after; only per_tick rows enter the "
               "schedule — the rest are annotations",
    "entities": "ids are unique; exactly one npc carries is_player; exits "
                "are the undirected adjacency (no duplicates); locations "
                "declare the fields preconditions read",
    "actions": "the intent grammar (fields, requires, events, knowledge "
               "templates) is INTENT_SCHEMA §9's; success/failure event "
               "types must exist in templates.json first",
    "director": "hook weights resolve as flat int or the multiplier "
                "spec; channels and the climax flag are declared shapes; "
                "pacing's floors are positive ints",
    "templates": "the fallback line is required; the tale gate names an "
                 "importance value; every event type used anywhere must "
                 "be in the events closure",
}

_GENERIC_HINT = (
    "the message names the offender; every closed vocabulary here is pack "
    "data — the information-ownership map: docs/AGENT_NAVIGATION.md §1"
)

#: The optional-block family (the 68a inventory the green path prints).
_OPTIONAL_BLOCKS: tuple[str, ...] = (
    "urgencies", "weather", "worldgen", "travel", "echo", "traits",
    "factions", "secrets", "reflection", "scene_detail", "on_action",
    "drift", "names", "acquisition",
)


def _locate(message: str) -> tuple[str, str]:
    """Parse the offending (file, block) out of a lint message's where
    prefix. The shapes: `rules.json::<block>...`, `action <intent>: ...`,
    `location <id>: ...`, bare `<block>[.path...]: ...`. The block token
    is cut at the first `.`/`[` — the hint keys on the top-level block.
    Unknown shapes fall back to the first word — the parse never
    crashes."""
    if "::" in message:
        head = message.split("::", 1)[0]
        block = message.split("::", 1)[1]
        block = block.split(".", 1)[0].split("[", 1)[0]
        return head, block.strip(": ")
    head = message.split(":", 1)[0]
    first = head.split(" ", 1)
    if first and first[0] in ("action", "item", "npc"):
        return "actions.json" if first[0] == "action" else "entities.json", first[0]
    if first and first[0] == "location":
        return "entities.json", "entities"
    block = (first[0] if first else "pack")
    block = block.split(".", 1)[0].split("[", 1)[0]
    return "rules.json", block.strip(": ")


def _trace_block(pack_dir: Path, file_name: str, block: str) -> str:
    """The offending block's own data (--trace): the file re-read as raw
    JSON and the named block dumped. A file that no longer parses reports
    itself — the doctor never guesses past the data."""
    path = pack_dir / file_name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"    ({file_name} no longer parses: {exc})"
    value = data.get(block) if isinstance(data, dict) else None
    if value is None:
        return f"    ({file_name} carries no block {block!r})"
    text = json.dumps(value, indent=2, ensure_ascii=False)
    lines = text.splitlines()
    if len(lines) > 40:
        lines = lines[:40] + ["    ... (truncated)"]
    return "\n".join(f"    {line}" for line in lines)


def _health(pack_dir: Path) -> int:
    """The green path: the pack's health inventory, derived from the
    loaded data — the surfaces an author edits, the blocks a mechanic
    arms. Exit 0 (the lint's verdict IS the health)."""
    pack = load_pack(pack_dir)
    entities = pack.entities
    rules = pack.rules
    director = rules.get("director", {})
    counts = {
        category: len(entities.get(category, []))
        for category in ("locations", "npcs", "ambient_entities", "items")
    }
    verbs = pack.data["actions.json"]["actions"]
    systems = rules.get("systems", {})
    per_tick = sorted(
        name for name, row in systems.items()
        if isinstance(row, dict) and row.get("per_tick") is True
    )
    optional = {
        block: block in rules for block in _OPTIONAL_BLOCKS
    }
    optional["pacing (director)"] = "pacing" in director
    optional["macro (time)"] = "macro" in rules.get("time", {})
    armed = sorted(k for k, v in optional.items() if v)
    absent = sorted(k for k, v in optional.items() if not v)
    beats = rules.get("urgencies", {}).get("beat_ticks", ())
    print(f"pack doctor — {pack_dir}")
    print("OK — the lint is green (the single admission gate)")
    print(f"  identity: {pack.name_version}")
    print(
        f"  entities: {counts['npcs']} npcs · {counts['locations']} locations "
        f"· {counts['ambient_entities']} ambient · {counts['items']} items"
    )
    print(f"  actions: {len(verbs)} verbs")
    print(f"  templates: {len(pack.templates.get('events', {}))} event types")
    print(f"  systems: {len([k for k in systems if isinstance(systems[k], dict)])} rows"
          + (f" (per-tick: {', '.join(per_tick)})" if per_tick else " (none per-tick)"))
    hooks = sorted(director.get("hooks", {}))
    print(f"  director hooks: {', '.join(hooks) if hooks else '(none)'}")
    if beats:
        print(f"  beat axis: {len(beats)} beats/day "
              f"(@ {', '.join(str(int(b)) for b in sorted(beats))}, "
              f"{int(rules['time']['ticks_per_day'])} ticks/day)")
    else:
        print("  beat axis: (none — no urgencies block)")
    print(f"  optional blocks armed: {', '.join(armed) if armed else '(none)'}")
    print(f"  optional blocks absent: {', '.join(absent) if absent else '(none)'}")
    print(
        "  loop: edit → python -m scripts.pack_doctor "
        f"{pack_dir} (→ --trace on a refusal) → patch"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pack_doctor",
        description="The pack lint's fix-hint surface: a refusal becomes a "
                    "diagnosis (file, block, doc owner, fix family, the "
                    "block's data with --trace); a green pack gets its "
                    "health inventory",
    )
    parser.add_argument("dir", type=Path, nargs="?", default=DEFAULT_DIR,
                        help="the pack directory (default: the committed "
                             "tavern pack)")
    parser.add_argument("--trace", action="store_true",
                        help="include the offending block's own data")
    args = parser.parse_args(argv)
    pack_dir: Path = args.dir

    if not pack_dir.is_dir():
        print(f"error: pack dir not found: {pack_dir}", file=sys.stderr)
        return 1
    present = {path.name for path in pack_dir.glob("*.json")}
    if present != set(PACK_FILE_NAMES):
        print(
            f"FAIL {pack_dir}: expected exactly {list(PACK_FILE_NAMES)}, "
            f"found {sorted(present)} — the pack is its four files",
            file=sys.stderr,
        )
        return 1
    try:
        return _health(pack_dir)
    except PackError as exc:
        message = str(exc)
        file_name, block = _locate(message)
        doc = _DOC_OWNERS.get(block, "docs/AGENT_NAVIGATION.md §1")
        hint = _FIX_HINTS.get(block, _GENERIC_HINT)
        print(f"pack doctor — {pack_dir}")
        print(f"FAIL {file_name} · block: {block}")
        print(f"  rule: {message}")
        print(f"  hint: {hint}")
        print(f"  doc:  {doc}")
        if args.trace:
            print("  data:")
            print(_trace_block(pack_dir, file_name, block))
        return 1
    except json.JSONDecodeError as exc:
        print(f"pack doctor — {pack_dir}")
        print(f"FAIL malformed JSON: {exc}")
        print("  hint: the four files must parse before any lint law runs")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
