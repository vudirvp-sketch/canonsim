"""The density-envelope pack generator (density-1, iter-345 — the E02
successor row; the unified pack v1.5's ULT §19.3(1) +
SCALE_TESTING_LAW §3.2 shapes, TEST_PLAN §9.1 the claim law).

profile + template → an ORDINARY VALID PACK through the existing
admission lint — never a second execution path, never a second
schema. The template is the committed Tier A fixture
(`content/farstead_pack/`); the settlement is the repeating unit,
copied VERBATIM and namespaced `s<i>` (the scaffold's law: ids are
cross-referenced by rules/hooks/preconditions, so every id moves
with its unit and every cross-reference is rewritten with it —
the measured-not-guessed form, no per-block map inherited).

The knobs (TEST_PLAN §9.1's axes, declared not implied):

  --settlements S   E and L: S copies of the 7-location unit
                    (L = 7·S; E = 1 player + 12·S adults + 3·S groups
                    + 2·S items); K = 0 by construction (no
                    inter-settlement edges — the locality-control
                    baseline; the coupling arm is a later held-out
                    row).
  --talk-links N    R: N extra talk posts per settlement (the
                    declared relation web's degree; deterministic
                    round-robin over the unit's adults).
  --prob-scale X    ρ: multiplier on the SAMPLED post family
                    (probability_per_beat < 100 — the talks, the
                    meal round, the rations, the idle bench); the
                    crossing-certain posts (the p=100 material
                    cycle) stay certain — B6's balance law.

Determinism: the pack is a PURE function of (profile, template) —
no RNG anywhere; same profile → byte-identical files (the
scaffold's own law). The run seed is the labrunner's business.

The output dir is the operator's choice (never inside content/ —
generated packs are disposable runtime artifacts, the gitignored
output family; the fixture-hardcoding law forbids committed herds).
`load_pack` gates the result: a variant the lint refuses never
runs (the `_variant_pack` precedent). PROFILE.md rides beside
the four files as the transparent identity echo (the SCAFFOLD.md
precedent — a non-JSON sidecar the pack glob never sees, not
lint-read).

Usage:
    python -m scripts.densitypack --out output/density_s4 \\
        --settlements 4 --talk-links 8 --prob-scale 1.0
    python scripts/labrunner.py --pack output/density_s4 --years 10 ...
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

from core.pack import PackError, load_pack  # noqa: E402

TEMPLATE_DIR = REPO / "content" / "farstead_pack"
PACK_FILES: tuple[str, ...] = ("actions.json", "entities.json",
                               "rules.json", "templates.json")
PACK_NAME = "density_pack"

#: The settlement unit's local suffixes (the template's own ids).
_LOC_IDS: tuple[str, ...] = ("loc_road", "loc_square", "loc_bank",
                             "loc_copse", "loc_outcrop", "loc_spring",
                             "loc_workshop")
#: The 12-adult roster (the template's ids, the namespace anchor).
_NPC_IDS: tuple[str, ...] = (
    "npc_ashen_elder", "npc_ashen_mate", "npc_ashen_son",
    "npc_ashen_daughter", "npc_bourne_elder", "npc_bourne_mate",
    "npc_bourne_son", "npc_bourne_daughter", "npc_crome_elder",
    "npc_crome_mate", "npc_crome_son", "npc_crome_daughter",
)
#: The template's economy flow ids (namespaced per unit — the
#: lint's unique-id law).
_FLOW_IDS: frozenset[str] = frozenset({
    "the_bank_regrows", "the_copse_regrows",
    "the_outcrop_weathers", "the_spring_runs",
})
#: The template's group and item ids (namespaced per unit).
_GROUP_IDS: frozenset[str] = frozenset({"grp_ashen", "grp_bourne", "grp_crome"})
_ITEM_IDS: frozenset[str] = frozenset({"hammer_01", "pail_01"})
#: The verbs whose posts/holders/legs are settlement-bound (namespaced
#: per unit — the actor-bound serves too: AP-11's clone law keys the
#: (intent, requires) pair, so an unnamed serve would clone across
#: units); the truly generic five (look_around, move, talk, wait)
#: stay shared and verbatim — no urgency post fires them bare.
_BOUND_INTENTS: frozenset[str] = frozenset({
    "haul_food", "haul_timber", "haul_ore", "haul_water",
    "bench_the_bloom", "bench_the_timber", "forge_tool",
    "draw_rations", "serve_the_meal", "serve_the_pail",
})
#: The sampled post family the ρ knob scales (everything the template
#: fires at p<100; the p=100 crossings are the material cycle's own).
_SAMPLED_PROB: int = 1


def _ns(kind: str, i: int, ident: str) -> str:
    """One id's namespaced form: `loc_bank` → `loc_s3_bank` (the
    prefix-insert form keeps every id family recognizable and the
    namespace collision-free by construction)."""
    return f"{kind}_s{i}_{ident[len(kind) + 1:]}"


def _rewrite_ids(obj: object, i: int) -> object:
    """Recursively rewrite every settlement-bound id inside a loaded
    JSON fragment: locations, npcs, groups, items, bound intent
    kinds, flow/recipe ids. Shared surfaces (the player `pc_01`, the
    event kinds, the fact keys) pass through untouched — the
    template's own cross-reference map, measured not guessed."""
    if isinstance(obj, dict):
        out: dict[str, object] = {}
        for key, value in obj.items():
            if key == "intent" and isinstance(value, str):
                # the action's own intent name (actions.json's shape)
                out[key] = (f"{value}_s{i}"
                            if value in _BOUND_INTENTS else value)
            elif key == "intent" and isinstance(value, dict):
                kind = value.get("kind", "")
                new_kind = (f"{kind}_s{i}" if kind in _BOUND_INTENTS
                            else kind)
                new_value: dict[str, object] = dict(value)
                new_value["kind"] = new_kind
                if "target" in new_value:
                    new_value["target"] = _rewrite_target(
                        new_value["target"], i,
                    )
                out[key] = new_value
            elif key in ("id", "npc", "with", "to", "from", "holder",
                         "target", "member", "members", "position",
                         "exits", "recipe"):
                out[key] = _rewrite_value(value, i)
            else:
                out[key] = _rewrite_ids(value, i)
        return out
    if isinstance(obj, list):
        return [_rewrite_ids(item, i) for item in obj]
    return obj


def _rewrite_target(target: object, i: int) -> object:
    """An intent target: locations and npcs namespace; the player
    stays (only settlement 0 carries a player-aimed post — the
    later units retarget it, see `_urgency_entries`)."""
    if not isinstance(target, str):
        return target
    return _rewrite_value(target, i)


def _rewrite_value(value: object, i: int) -> object:
    if isinstance(value, str):
        if value.startswith("loc_") and value in _LOC_IDS:
            return _ns("loc", i, value)
        if value.startswith("npc_") and value in _NPC_IDS:
            return _ns("npc", i, value)
        if value in _FLOW_IDS:
            stem = value[4:]  # strip "the_"
            return f"the_s{i}_{stem}"
        if value in _GROUP_IDS:
            return _ns("grp", i, value)
        if value in _ITEM_IDS:
            stem = value.rsplit("_", 1)[0]
            return f"{stem}_s{i}_01"
        if value == "forge_a_tool":
            return f"forge_a_tool_s{i}"
        return value
    if isinstance(value, list):
        return [_rewrite_value(item, i) for item in value]
    return value


def _settlement_locations(i: int) -> list[dict[str, object]]:
    entities = json.loads(
        (TEMPLATE_DIR / "entities.json").read_text(encoding="utf-8"),
    )
    return [_rewrite_ids(loc, i) for loc in entities["locations"]]


def _settlement_npcs(i: int) -> list[dict[str, object]]:
    entities = json.loads(
        (TEMPLATE_DIR / "entities.json").read_text(encoding="utf-8"),
    )
    adults = [n for n in entities["npcs"] if not n.get("is_player")]
    return [_rewrite_ids(npc, i) for npc in adults]


def _player() -> dict[str, object]:
    entities = json.loads(
        (TEMPLATE_DIR / "entities.json").read_text(encoding="utf-8"),
    )
    player = next(n for n in entities["npcs"] if n.get("is_player"))
    return _rewrite_ids(player, 0)


def _urgency_entries(
    i: int, talk_links: int, prob_scale: float,
) -> list[dict[str, object]]:
    """The unit's urgency posts: the template's fourteen, namespaced,
    plus `talk_links` deterministic extras (the R knob). The ρ knob
    scales the sampled family (p<100); the certain crossings stay
    certain (B6's law). Settlement 0 keeps the player-aimed post;
    later units retarget it to their own son-of-Bourne (the count
    stays uniform — the honest E/R echo, never a quieter unit).

    The extras draw sources from the unit's non-talk adults only —
    the one-goal-per-NPC-per-verb law (engine-2's roll-stream
    content-addressing) caps the relation web at one talk post per
    adult; the profile's honest ceiling is the roster's eight
    non-talk adults (a denser web needs a wider roster — the
    households knob's future row)."""
    rules = json.loads(
        (TEMPLATE_DIR / "rules.json").read_text(encoding="utf-8"),
    )
    entries: list[dict[str, object]] = []
    for entry in rules["urgencies"]["entries"]:
        item = _rewrite_ids(entry, i)
        target = item["intent"].get("target")
        if target == "pc_01" and i > 0:
            item["intent"]["target"] = _ns("npc", i, "npc_bourne_son")
        if entry["probability_per_beat"] < 100:
            scaled = round(entry["probability_per_beat"] * prob_scale)
            item["probability_per_beat"] = max(1, min(100, scaled))
        entries.append(item)
    talkers = {
        str(e["intent"]["target"]) for e in rules["urgencies"]["entries"]
        if e["intent"]["kind"] == "talk"
    } | {
        e["npc"] for e in rules["urgencies"]["entries"]
        if e["intent"]["kind"] == "talk"
    }
    quiet = [npc for npc in _NPC_IDS if npc not in talkers]
    if talk_links > len(quiet):
        raise SystemExit(
            f"densitypack refused — --talk-links {talk_links} exceeds "
            f"the unit's non-talk roster ({len(quiet)}): the "
            "one-goal-per-NPC-per-verb law caps the web at one talk "
            "post per adult; a denser web needs a wider roster (the "
            "households knob's future row)"
        )
    # AP-11: the (kind, target) pair must stay unique too — the extras
    # aim only at adults no base post already targets (the clone law's
    # design-time twin; the lint verifies, the map is measured).
    pool = [npc for npc in _NPC_IDS
            if npc not in talkers and npc not in
            {str(e["intent"]["target"])
             for e in rules["urgencies"]["entries"]
             if e["intent"]["kind"] == "talk"}]
    for k in range(talk_links):
        src = _ns("npc", i, quiet[k])
        dst = _ns("npc", i, pool[(pool.index(quiet[k]) + 1 + k) % len(pool)])
        entries.append({
            "npc": src,
            "probability_per_beat": max(1, min(100,
                round(_SAMPLED_PROB * prob_scale))),
            "intent": {"kind": "talk", "target": dst},
            "requires": [{
                "noun": "target", "test": "same_location",
                "with": "actor",
            }],
            "notes": (
                f"THE DENSITY WEB {k}: the R-knob's extra edge "
                f"(talk-links {k}), {src} to {dst} — the declared "
                "relation degree the profile adds over the unit's "
                "own four."
            ),
        })
    return entries


def build_pack(
    settlements: int, talk_links: int, prob_scale: float,
) -> dict[str, object]:
    """The four pack files' content as a dict (pure: no IO, no RNG —
    the same (knobs, template) always yields the same bytes)."""
    entities_t = json.loads(
        (TEMPLATE_DIR / "entities.json").read_text(encoding="utf-8"),
    )
    actions_t = json.loads(
        (TEMPLATE_DIR / "actions.json").read_text(encoding="utf-8"),
    )
    rules_t = json.loads(
        (TEMPLATE_DIR / "rules.json").read_text(encoding="utf-8"),
    )
    templates_t = json.loads(
        (TEMPLATE_DIR / "templates.json").read_text(encoding="utf-8"),
    )

    locations: list[dict[str, object]] = []
    npcs: list[dict[str, object]] = [_player()]
    groups: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    actions: list[dict[str, object]] = []
    flows: list[dict[str, object]] = []
    recipes: list[dict[str, object]] = []
    urgencies: list[dict[str, object]] = []

    generic = [a for a in actions_t["actions"]
               if a["intent"] not in _BOUND_INTENTS]
    bound = [a for a in actions_t["actions"]
             if a["intent"] in _BOUND_INTENTS]

    for i in range(settlements):
        locations.extend(_settlement_locations(i))
        npcs.extend(_settlement_npcs(i))
        groups.extend(_rewrite_ids(g, i) for g in entities_t["groups"])
        items.extend(_rewrite_ids(it, i) for it in entities_t["items"])
        actions.extend(_rewrite_ids(a, i) for a in bound)
        flows.extend(_rewrite_ids(f, i) for f in rules_t["economy"]["flows"])
        recipes.extend(_rewrite_ids(r, i)
                       for r in rules_t["economy"]["recipes"])
        urgencies.extend(_urgency_entries(i, talk_links, prob_scale))

    actions = generic + actions

    profile_note = (
        f"THE DENSITY-ENVELOPE PACK (density-1, iter-345): "
        f"{settlements} settlement unit(s) of the Tier A template, "
        f"{talk_links} extra talk link(s) per unit, prob-scale "
        f"{prob_scale} on the sampled family. A DISPOSABLE "
        "measurement instrument (TEST_PLAN §9.1's axes; the "
        "fixture-hardcoding law — never committed, regenerated from "
        "the profile). The unit's semantics ride the template "
        "verbatim; the namespace is the only rewrite."
    )

    entities = {
        "meta": {
            "pack": PACK_NAME, "version": "0.1",
            "display": "the density-envelope world (the Lab fixture)",
            "notes": profile_note,
        },
        "locations": locations, "npcs": npcs, "groups": groups,
        "items": items, "ambient_entities": [],
    }
    actions_doc = {
        "meta": {
            "pack": PACK_NAME, "version": "0.1",
            "notes": profile_note,
        },
        "actions": actions,
    }
    rules = dict(rules_t)
    rules["meta"] = {
        "pack": PACK_NAME, "version": "0.1",
        "display": "the density-envelope world (the Lab fixture)",
        "notes": profile_note,
    }
    rules["economy"] = dict(rules_t["economy"])
    rules["economy"]["flows"] = flows
    rules["economy"]["recipes"] = recipes
    rules["urgencies"] = dict(rules_t["urgencies"])
    rules["urgencies"]["entries"] = urgencies
    templates = dict(templates_t)
    templates["meta"] = {
        "pack": PACK_NAME, "version": "0.1",
        "notes": (
            "The Tier A chronicle, verbatim except the flow glosses "
            "(keyed by flow id, so each unit's flows carry their own "
            "gloss — the measured cross-reference map; the event "
            "kinds are shared across the units, the tale surface "
            "needs no per-settlement copies)."
        ),
    }
    glosses: dict[str, object] = {}
    for i in range(settlements):
        for flow_id, gloss in templates_t["flow_glosses"].items():
            glosses[str(_rewrite_value(flow_id, i))] = gloss
    templates["flow_glosses"] = glosses
    return {
        "entities.json": entities, "actions.json": actions_doc,
        "rules.json": rules, "templates.json": templates,
    }


def materialize(out_dir: Path, settlements: int, talk_links: int,
                prob_scale: float) -> str:
    """Write the four files + the PROFILE.md echo, lint-gate the
    result through `load_pack`, return the pack's name@version. A
    variant the lint refuses never survives on disk."""
    if settlements < 1:
        raise SystemExit(
            "densitypack refused — --settlements must be >= 1 "
            "(the E/L axis's unit)"
        )
    if talk_links < 0:
        raise SystemExit(
            "densitypack refused — --talk-links must be >= 0 "
            "(0 = the template's own relation web)"
        )
    if not 0.0 < prob_scale <= 100.0:
        raise SystemExit(
            "densitypack refused — --prob-scale must be in (0, 100] "
            "(the sampled family's multiplier; the certain crossings "
            "stay certain by B6's law)"
        )
    docs = build_pack(settlements, talk_links, prob_scale)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, doc in docs.items():
        (out_dir / name).write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    profile = {
        "generator": "scripts/densitypack.py",
        "template": "content/farstead_pack",
        "settlements": settlements,
        "talk_links": talk_links,
        "prob_scale": prob_scale,
        "axes_echo": {
            "L": 7 * settlements,
            "E_npcs": 1 + 12 * settlements,
            "E_groups": 3 * settlements,
            "E_items": 2 * settlements,
            "R_talk_posts_per_unit": 4 + talk_links,
            "K": 0,
        },
    }
    (out_dir / "PROFILE.md").write_text(
        "```json\n" + json.dumps(profile, indent=2, ensure_ascii=False)
        + "\n```\n",
        encoding="utf-8",
    )
    try:
        pack = load_pack(out_dir)
    except PackError as exc:
        raise SystemExit(
            f"densitypack refused by the pack lint: {exc} — the "
            f"profile (settlements={settlements}, "
            f"talk-links={talk_links}, prob-scale={prob_scale}) "
            "produced an invalid variant; the template's own shapes "
            "must be re-checked against the admission grammar"
        ) from exc
    return pack.name_version


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The density-envelope pack generator (density-1)",
    )
    parser.add_argument(
        "--out", type=Path, required=True,
        help="the output pack directory (never inside content/)",
    )
    parser.add_argument("--settlements", type=int, default=1,
                        help="the settlement units (E and L; default 1)")
    parser.add_argument(
        "--talk-links", type=int, default=0,
        help="extra talk posts per unit (the R knob; default 0)",
    )
    parser.add_argument(
        "--prob-scale", type=float, default=1.0,
        help="the sampled family's probability multiplier (the ρ "
             "knob; default 1.0)",
    )
    args = parser.parse_args(argv)
    resolved = args.out.resolve()
    if REPO / "content" in resolved.parents:
        raise SystemExit(
            "densitypack refused — the output must never live inside "
            "content/ (generated packs are disposable output-family "
            "artifacts, the fixture-hardcoding law)"
        )
    name_version = materialize(
        resolved, args.settlements, args.talk_links, args.prob_scale,
    )
    print(
        f"[densitypack: {resolved} — {name_version}, lint green] "
        f"settlements={args.settlements} talk-links={args.talk_links} "
        f"prob-scale={args.prob_scale}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
