"""The pack scaffold generator (iter-107, the risk-synthesis §1 rider:
"tavern as template inventory" — the authoring loop's first rung).

scaffold → author JSON → lint (pack_doctor, fix-hints) → patch → lint
→ A/B self-check (balance_harness, mechanics.py): the closed loop a
human author or an autonomous LLM can run without ever reading core
code. This tool emits the first artifact: a COMPLETE, lint-clean copy
of the committed tavern pack with the identity renamed — not a blank
page. The level-1 reskin experiment (world-2, phases.md §6) edits
names and prose over exactly this skeleton: ids STAY (every id is
cross-referenced by rules/hooks/preconditions), surfaces are free.

The output dir is the operator's choice (never inside content/ —
scaffolded packs are runtime authoring artifacts, gitignored output
family); SCAFFOLD.md rides beside the four files as the editing map
(derived from the pack's own data — counts and noun surfaces, no
timestamps, same pack → same scaffold bytes).

Usage:
    python -m scripts.pack_scaffold --out <dir> [--name <pack-name>]
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

from core.pack import load_pack  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"
PACK_FILES: tuple[str, ...] = ("actions.json", "entities.json",
                               "rules.json", "templates.json")
SOURCE_NAME = "tavern_pack"


def _rewrite_identity(text: str, name: str) -> str:
    """Rename the pack identity in one file's bytes: the four files share
    one meta formatting, so the targeted `"pack": "<old>"` swap preserves
    every other byte (formatting, notes, key order — the diff the author
    makes later stays surgical). Loud when the anchor is missing — a
    format change upstream must be faced, not silently absorbed."""
    anchor = f'"pack": "{SOURCE_NAME}"'
    if anchor not in text:
        raise ValueError(
            f"the identity anchor {anchor!r} is missing — the source pack's "
            "meta formatting changed; update the scaffold's anchor law"
        )
    return text.replace(anchor, f'"pack": "{name}"')


def _noun_surfaces(entities: dict) -> list[tuple[str, int, list[str]]]:
    """The editable noun surfaces per category: (kind, count, names) —
    display names are the reskin's main lever; ids are pinned."""
    out: list[tuple[str, int, list[str]]] = []
    for category in ("locations", "npcs", "ambient_entities", "items"):
        records = entities.get(category, [])
        out.append((category, len(records),
                    [str(r.get("name", r["id"])) for r in records]))
    return out


def _scaffold_md(name: str, rules: dict, entities: dict,
                 actions: dict, templates: dict) -> str:
    """The editing map, derived from the pack's own data (deterministic —
    same pack, same bytes; no wall-clock ever lands in a repo artifact)."""
    optional_blocks = (
        "pacing (director)", "weather", "worldgen", "travel", "echo",
        "traits", "factions", "secrets", "reflection", "scene_detail",
        "urgencies", "on_action", "drift", "names", "macro (time)",
    )
    present = []
    director = rules.get("director", {})
    if "pacing" in director:
        present.append("pacing (director)")
    for block in ("weather", "worldgen", "travel", "echo", "traits",
                  "factions", "secrets", "reflection", "scene_detail",
                  "urgencies", "on_action", "drift", "names"):
        if block in rules:
            present.append(block)
    if "macro" in rules.get("time", {}):
        present.append("macro (time)")
    absent = [block for block in optional_blocks if block not in present]

    lines = [
        f"# SCAFFOLD.md — the editing map for {name}",
        "",
        "This is a complete, lint-clean copy of the committed tavern pack,",
        "identity renamed. The lint (`core/pack.py`) is the single admission",
        "gate — every edit loops through it:",
        "",
        "    python -m scripts.pack_doctor <this-dir>          # after every edit",
        "    python -m scripts.pack_doctor <this-dir> --trace  # + the failing",
        "                                                  block's data",
        "",
        "## The reskin law (ids stay, surfaces are free)",
        "",
        "Every id is cross-referenced: rules hooks target npcs, urgencies",
        "key by npc id, preconditions name fields, templates bind slots.",
        "Rename NAMES, ROLES, PROSE freely; rename an ID only with a",
        "repo-wide search of all four files. The stoplist test",
        "(tests/test_inv3_stoplist.py) guards the engine side; pack nouns",
        "are yours.",
        "",
        "## The noun surfaces (entities.json)",
        "",
    ]
    for kind, count, names in _noun_surfaces(entities):
        lines.append(f"- {kind} ({count}): " + ", ".join(names))
    lines.extend([
        "",
        "## The verb labels (actions.json — the parser's display words)",
        "",
    ])
    verbs = [f"{a['intent']} (\"{a.get('label', a['intent'])}\")"
             for a in actions.get("actions", [])]
    lines.append(f"- {len(verbs)} verbs: " + ", ".join(verbs))
    lines.extend([
        "",
        "## The prose (templates.json)",
        "",
        f"- {len(templates.get('events', {}))} event-type lines; the tracery",
        "  symbols and the tale gate (`tale_gate.min_importance`) live here.",
        "",
        "## The rules inventory (rules.json)",
        "",
        f"- armed optional blocks: {', '.join(present) if present else '(none)'}",
        "- absent (the 68a family — silence a mechanic by REMOVING its",
        f"  block): {', '.join(absent) if absent else '(none)'}",
        "- director hooks: "
        + (", ".join(sorted(director.get("hooks", {}))) or "(none)"),
        "",
        "## The self-check instruments (the A/B half of the loop)",
        "",
        "    python -m scripts.balance_harness --script <a-playscript> \\",
        "        --runs 50 --directors on            # the distribution table",
        "    python -m scripts.balance_harness --runs 50 --directors on \\",
        "        --systems-minus <name>              # world-without-X arm",
        "    python -m scripts.mechanics matrix|blast|trace|why  # wiring views",
        "",
        "A playscript binds to this pack as `" + name
        + "@<version>` (`pack` field) — write steps against the verbs above.",
    ])
    return "\n".join(lines) + "\n"


def scaffold(out_dir: Path, name: str) -> Path:
    """Materialize the scaffold: four files copied (identity renamed) +
    SCAFFOLD.md. Refuses a non-empty out dir — never clobbers author
    work. Returns the dir (the caller prints the loop's next steps)."""
    if out_dir.exists() and any(out_dir.iterdir()):
        raise ValueError(
            f"scaffold refuses to overwrite: {out_dir} exists and is not "
            "empty (point --out at a fresh dir)"
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    for file_name in PACK_FILES:
        text = (PACK_DIR / file_name).read_text(encoding="utf-8")
        (out_dir / file_name).write_text(
            _rewrite_identity(text, name), encoding="utf-8"
        )
    data = {
        file_name: json.loads((out_dir / file_name).read_text(encoding="utf-8"))
        for file_name in PACK_FILES
    }
    (out_dir / "SCAFFOLD.md").write_text(
        _scaffold_md(
            name, data["rules.json"], data["entities.json"],
            data["actions.json"], data["templates.json"],
        ),
        encoding="utf-8",
    )
    load_pack(out_dir)  # the gate: a scaffold that does not lint is a bug
    return out_dir


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pack_scaffold",
        description="Generate a lint-clean pack skeleton from the committed "
                    "tavern pack (the authoring loop's first rung): four "
                    "files, identity renamed, SCAFFOLD.md the editing map",
    )
    parser.add_argument("--out", type=Path, required=True,
                        help="the output pack dir (must be empty or absent)")
    parser.add_argument("--name", default="scaffold_pack",
                        help="the new pack identity (default: scaffold_pack)")
    args = parser.parse_args(argv)
    try:
        out_dir = scaffold(args.out, args.name)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    pack = load_pack(out_dir)
    print(f"[scaffold: {out_dir} — {pack.name_version}, lint green]")
    print(
        "[next: edit the noun surfaces (SCAFFOLD.md maps them), then "
        "python -m scripts.pack_doctor "
        f"{out_dir} after every edit]"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
