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
  --households H    the ACTIVE unit's households (density-2, the
                    DENSITY-SCALE arm): H−3 extension households of
                    four hearth-voice adults each, resident on the
                    active unit's square, every adult one talk post
                    (the sampled family) on the extension's own
                    directed ring — the warm ring's population the
                    varied axis while the cold volume stays the
                    template's own (12·(S−1) cold adults, the census
                    law untouched). The material web stays the
                    template's verbatim (no extension post touches
                    an account): the cone's POPULATION density
                    varies, never its material semantics. AP-11's
                    unique-(intent, requires) ceiling is why this
                    is its own arm — a verbatim household copy would
                    clone; the ring keeps every pair unique.

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
    python -m scripts.densitypack --out output/density_h12 \\
        --settlements 4 --households 12
    python scripts/labrunner.py --pack output/density_h12 --years 10 ...
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
#: The extension households' plain-noun stems (the template's own
#: "every noun deliberately plain" law); the knob's honest ceiling —
#: past the list the generator refuses LOUD (the talk-links roster
#: precedent: a named ceiling, never a silent truncation).
_EXT_STEMS: tuple[str, ...] = (
    "dun", "elm", "fenn", "gale", "hale", "iris", "joss", "kern",
    "lyle", "moss", "nix", "orra", "peat", "quill", "reed", "sedge",
    "torr", "ursa", "vail", "wick", "yate", "zeph", "brack", "croft",
    "dell", "flint", "gorse", "hesp", "kale",
)
#: The extension adult's four roles (the template household's own
#: shape: elder, mate, son, daughter).
_EXT_ROLES: tuple[str, ...] = ("elder", "mate", "son", "daughter")
#: The template's own household count (the knob's floor and identity:
#: H = 3 is the density-1 form byte-for-byte).
_TEMPLATE_HOUSEHOLDS: int = 3


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


def _extension_households(
    households: int, prob_scale: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]],
           list[dict[str, object]]]:
    """The ACTIVE unit's extension households (density-2, the
    DENSITY-SCALE arm): `households` − 3 new households of four
    hearth-voice adults, resident on unit 0's square (the anchor's
    active location — the population the cone actually exercises
    per-beat), every adult ONE talk post on the extension's own
    directed 2-step ring (`npc_j → npc_{(j+2) mod N}` — two
    interleaved rings through the households, the elders-and-heirs
    and the keepers-and-daughters). The ring is deliberately
    INTERNAL: no extension post targets a template adult, so the
    knobs stay ORTHOGONAL (the talk-links pool and the daughters'
    cycle untouched — no AP-11 collision by construction, measured
    not merely lint-hoped). The pair web mirrors the Ashen
    household's own shape (elder↔mate 80, son→elder 70,
    daughter→mate 75) — the household's semantics carried as
    projection-side data, never a material post: the extension
    touches NO account anywhere (the warm material web stays the
    template's verbatim — the row's control)."""
    extra = households - _TEMPLATE_HOUSEHOLDS
    ids = [f"npc_s0_{stem}_{role}"
           for stem in _EXT_STEMS[:extra] for role in _EXT_ROLES]
    npcs: list[dict[str, object]] = []
    groups: list[dict[str, object]] = []
    entries: list[dict[str, object]] = []
    for e, stem in enumerate(_EXT_STEMS[:extra]):
        titled = stem.capitalize()
        members = [f"npc_s0_{stem}_{role}" for role in _EXT_ROLES]
        elder, mate, son, daughter = members
        pairs: dict[str, list[dict[str, object]]] = {
            elder: [{"with": mate, "trust": 80}],
            mate: [{"with": elder, "trust": 80}],
            son: [{"with": elder, "trust": 70}],
            daughter: [{"with": mate, "trust": 75}],
        }
        names: dict[str, str] = {
            "elder": f"{titled}, the elder voice",
            "mate": f"the {stem} hearth-keeper",
            "son": f"the {stem} boy",
            "daughter": f"{titled}'s daughter",
        }
        roles: dict[str, str] = {
            "elder": "hearth-voice — the household's head, the green's ear",
            "mate": "hearth-voice — the household's hands, the square's round",
            "son": "hearth-voice — the household's legs, the square's watch",
            "daughter": "hearth-voice — the household's young ear",
        }
        for role in _EXT_ROLES:
            npc_id = f"npc_s0_{stem}_{role}"
            npcs.append({
                "id": npc_id,
                "name": names[role],
                "role": roles[role],
                "position": "loc_s0_square",
                "status": {"fatigue": 10},
                "relations": {"trust": 50},
                "knowledge": [],
                "mood": "easy",
                "goal": "the green's life heard and kept",
                "pair_relations": pairs[npc_id],
                "notes": (
                    f"THE DENSITY HOUSEHOLD {e} ({titled}): a "
                    "measurement instrument's hearth-voice (density-2, "
                    "the DENSITY-SCALE arm) — resident on the active "
                    "unit's square so the cone's own population rolls "
                    "per-beat; the talk post the extension ring's own "
                    "edge; NO material post (the warm material web is "
                    "the template's verbatim, the row's control)."
                ),
            })
        groups.append({
            "id": f"grp_s0_{stem}",
            "name": f"the {titled} household",
            "position": "loc_s0_square",
            "members": members,
            "notes": (
                f"THE DENSITY HOUSEHOLD {e}: the extension arm's "
                "social unit — four voices at the green, the warm "
                "ring's population the varied axis (TEST_PLAN §9.1's "
                "DENSITY-SCALE class, the first promotion candidate)."
            ),
        })
    for j, npc_id in enumerate(ids):
        target = ids[(j + 2) % len(ids)]
        entries.append({
            "npc": npc_id,
            "probability_per_beat": max(1, min(100,
                round(_SAMPLED_PROB * prob_scale))),
            "intent": {"kind": "talk", "target": target},
            "requires": [{
                "noun": "target", "test": "same_location",
                "with": "actor",
            }],
            "notes": (
                f"THE DENSITY WEB (households): the extension ring's "
                f"own edge — {npc_id} to {target}, the 2-step ring "
                "internal to the extension (no template adult "
                "targeted: the knobs orthogonal, every AP-11 pair "
                "unique by construction)."
            ),
        })
    return npcs, groups, entries


def build_pack(
    settlements: int, talk_links: int, prob_scale: float,
    households: int = _TEMPLATE_HOUSEHOLDS,
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

    # density-2 (the DENSITY-SCALE arm): the ACTIVE unit's extension
    # households ride AFTER every template unit — the additive form,
    # so households = 3 (the template's own) is the density-1 form
    # byte-for-byte (the identity law) and the extension is visibly
    # its own surface in the file order too.
    if households > _TEMPLATE_HOUSEHOLDS:
        ext_npcs, ext_groups, ext_entries = _extension_households(
            households, prob_scale,
        )
        npcs.extend(ext_npcs)
        groups.extend(ext_groups)
        urgencies.extend(ext_entries)

    actions = generic + actions

    extra_households = households - _TEMPLATE_HOUSEHOLDS
    profile_note = (
        f"THE DENSITY-ENVELOPE PACK (density-1/2, iter-345/347): "
        f"{settlements} settlement unit(s) of the Tier A template, "
        f"{talk_links} extra talk link(s) per unit, prob-scale "
        f"{prob_scale} on the sampled family, {households} household(s) "
        f"in the ACTIVE unit ({extra_households} extension hearth-voice "
        "households — the DENSITY-SCALE arm: the warm ring's population "
        "the varied axis, the cold volume the template's own). A "
        "DISPOSABLE measurement instrument (TEST_PLAN §9.1's axes; the "
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
                prob_scale: float,
                households: int = _TEMPLATE_HOUSEHOLDS) -> str:
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
    if households < _TEMPLATE_HOUSEHOLDS:
        raise SystemExit(
            "densitypack refused — --households must be >= 3 (the "
            "template's own three households are the base, copied "
            "verbatim; the knob only GROWS the active unit — a "
            "smaller roster is not this instrument's surface)"
        )
    if households > _TEMPLATE_HOUSEHOLDS + len(_EXT_STEMS):
        raise SystemExit(
            f"densitypack refused — --households {households} exceeds "
            f"the stem list's honest ceiling "
            f"({_TEMPLATE_HOUSEHOLDS + len(_EXT_STEMS)}): every "
            "extension household needs its own plain-noun stem (the "
            "template's every-noun-plain law), never a synthesized id"
        )
    docs = build_pack(settlements, talk_links, prob_scale, households)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, doc in docs.items():
        (out_dir / name).write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    extra_households = households - _TEMPLATE_HOUSEHOLDS
    profile = {
        "generator": "scripts/densitypack.py",
        "template": "content/farstead_pack",
        "settlements": settlements,
        "talk_links": talk_links,
        "prob_scale": prob_scale,
        "households": households,
        "axes_echo": {
            "L": 7 * settlements,
            "E_npcs": 1 + 12 * settlements + 4 * extra_households,
            "E_groups": 3 * settlements + extra_households,
            "E_items": 2 * settlements,
            "warm_adults_unit0": 12 + 4 * extra_households,
            "cold_npcs": 12 * (settlements - 1),
            "R_talk_posts_unit0": 4 + talk_links + 4 * extra_households,
            "R_talk_posts_per_cold_unit": 4 + talk_links,
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
            f"talk-links={talk_links}, prob-scale={prob_scale}, "
            f"households={households}) produced an invalid variant; "
            "the template's own shapes must be re-checked against "
            "the admission grammar"
        ) from exc
    return pack.name_version


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The density-envelope pack generator (density-1/2)",
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
        "--households", type=int, default=_TEMPLATE_HOUSEHOLDS,
        help="the ACTIVE unit's households (the DENSITY-SCALE arm; "
             "default 3 = the template's own, byte-identical to "
             "the density-1 form)",
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
        args.households,
    )
    print(
        f"[densitypack: {resolved} — {name_version}, lint green] "
        f"settlements={args.settlements} talk-links={args.talk_links} "
        f"prob-scale={args.prob_scale} households={args.households}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
