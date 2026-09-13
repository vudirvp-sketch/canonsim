"""iter-117 — the pack-ci admission rungs (PACK_SPEC §5/§6 landing as
enforcement in `core/pack.py`).

The teleology gate (§5): dead action types, orphan entities, empty
intersection-matrix rows, declared-but-unused templates — the UAP audit's
"every event type must produce a state delta or a hook" as deterministic
lint. The live-char crosswalk (§6): the AP rows (spine shape, flaw
consumption, clone pairs, contradictory reactions, predicate atomicity,
size budgets) plus the price-marker lint (AP-2's design-time half).

The suite's law: the two committed packs (the tavern + the road — the
reskin pack is the first pack the new rows run against, PACK_SPEC §12)
and the scaffold's output all lint GREEN under every new row, and every
crafted-broken twin dies naming the offender (the crafted-twin pattern,
the pack-tools/travel suites' family).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from core.pack import PackError, load_pack  # noqa: E402

TAVERN = REPO / "content" / "tavern_pack"
ROAD = REPO / "content" / "road_pack"
PACK_FILES = ("entities.json", "actions.json", "rules.json", "templates.json")

# the weather family's template lines — the v0.1 twin's ablation strips
# them with the blocks (the dead-vocabulary law), the twin-compliance
# shape every crafted helper in this suite follows
WEATHER_DEAD_LINES = ("year_turns", "weather_turns", "smoke_washed_away")


def crafted(
    tmp_path: Path,
    name: str,
    *,
    rules: Callable[[dict[str, Any]], None] | None = None,
    actions: Callable[[list[dict[str, Any]]], None] | None = None,
    entities: Callable[[dict[str, Any]], None] | None = None,
    templates: Callable[[dict[str, Any]], None] | None = None,
    v01: bool = False,
) -> Path:
    """A committed tavern copy with the four files mutated; the caller
    reads the refusal off `load_pack(target)` itself (the single
    admission gate — the helper never pre-lints)."""
    target = tmp_path / name
    shutil.copytree(TAVERN, target)
    data: dict[str, Any] = {
        path.name: json.loads(path.read_text(encoding="utf-8"))
        for path in target.glob("*.json")
    }
    if v01:
        data["rules.json"]["time"].pop("macro", None)
        data["rules.json"].pop("weather", None)
        for line in WEATHER_DEAD_LINES:
            data["templates.json"]["events"].pop(line, None)
    if rules is not None:
        rules(data["rules.json"])
    if actions is not None:
        actions(data["actions.json"]["actions"])
    if entities is not None:
        entities(data["entities.json"])
    if templates is not None:
        templates(data["templates.json"])
    for file_name, payload in data.items():
        (target / file_name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return target


def refuses(target: Path, match: str) -> None:
    with pytest.raises(PackError, match=match):
        load_pack(target)


def _action(intent: str, resolver: str, event_type: str) -> dict[str, Any]:
    """The minimal legal action record — no declared effect of its own
    (the dead-action probe's base shape)."""
    return {
        "intent": intent,
        "label": intent,
        "resolver": resolver,
        "ticks": 1,
        "check": None,
        "on_failure": None,
        "events": {"success": event_type},
        "requires": [],
        "fields": [],
        "knowledge": {"success": [], "failure": []},
        "hooks": {"success": [], "failure": []},
        "notes": "the pack-ci probe verb",
    }


# -- the green pins -------------------------------------------------------------


def test_the_committed_packs_pass_every_new_row() -> None:
    """The admission gate stays green on the two committed packs — the
    tavern and the road (the reskin pack is the first pack the new rows
    run against, PACK_SPEC §12): zero dead actions, zero orphans, zero
    empty rows, zero unused templates across 16 verbs and 46 lines."""
    for pack_dir in (TAVERN, ROAD):
        pack = load_pack(pack_dir)
        assert pack.templates["events"]


def test_the_scaffold_output_lints_green(tmp_path: Path) -> None:
    """The authoring loop's first rung holds under the new rows: a
    lint-clean tavern copy with the identity renamed is still lint-clean
    (a scaffold that does not lint is a bug — the §9 law)."""
    import pack_scaffold  # type: ignore[import-not-found]

    out = tmp_path / "skeleton"
    pack_scaffold.scaffold(out, "probe_pack")
    assert load_pack(out).name_version == "probe_pack@0.1"


def test_the_v01_twin_lints_green_when_complete(tmp_path: Path) -> None:
    """The 68a law intact: the v0.1 twin (macro + weather dropped
    TOGETHER with their template lines) is a legal pack — the ablation
    is complete when the family's vocabulary goes with the blocks."""
    assert load_pack(crafted(tmp_path, "v01", v01=True))


# -- §5 row 1: dead action types ------------------------------------------------


def test_dead_action_type_is_refused(tmp_path: Path) -> None:
    """A verb whose events carry no state change, no knowledge, no seed
    and no on_action reaction is dead content — refused at load, the
    UAP gate's deterministic form."""
    target = crafted(
        tmp_path, "dead_verb",
        actions=lambda acts: acts.append(_action("lurk", "observe", "lurk")),
        templates=lambda tpl: tpl["events"].update({"lurk": "{actor} lurks."}),
    )
    refuses(target, r"action lurk: dead action type")


def test_state_mutating_resolver_keeps_a_bare_verb_alive(tmp_path: Path) -> None:
    """The resolver family is the state-change witness: a bare movement
    verb (no declared effect of its own) is alive — its events carry the
    position change by construction (STATE_MUTATING)."""
    target = crafted(
        tmp_path, "bare_move",
        actions=lambda acts: acts.append(_action("slip_out", "movement", "move")),
    )
    assert load_pack(target)


def test_system_attribution_keeps_a_story_beat_verb_alive(tmp_path: Path) -> None:
    """The metrics attribution row is the witness the goal-verbs use
    (the factions muster family): a system reacts to the event type —
    the pack's own declaration that the beat matters."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["metrics"]["system_of_type"]["lurk"] = ["director"]

    target = crafted(
        tmp_path, "attributed_verb",
        rules=rules,
        actions=lambda acts: acts.append(_action("lurk", "observe", "lurk")),
        templates=lambda tpl: tpl["events"].update({"lurk": "{actor} lurks."}),
    )
    assert load_pack(target)


# -- §5 row 2: orphan entities ---------------------------------------------------


def test_an_unaddressable_item_is_an_orphan(tmp_path: Path) -> None:
    """The target grammar misses an item nothing can address: the orb
    sits in the sealed cellar — the hermit's position touches the room
    (and his two-sided pair relation wires him into the world), but no
    exits edge leads there, so no co-location verb can ever reach the
    orb — dead weight, refused."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["locations"].append({
            "id": "loc_cellar", "name": "the sealed cellar", "exits": [],
            "flammability": "none", "fire_spots": [],
            "notes": "the hermit stands here; no doors, no verbs reach in",
        })
        entities_data["npcs"].append({
            "id": "npc_hermit_01", "name": "the hermit",
            "position": "loc_cellar", "status": {}, "relations": {},
            "pair_relations": [{"with": "npc_barkeep_01", "trust": 40}],
            "knowledge": [], "mood": "quiet", "goal": "be left alone",
            "notes": "wired to the barkeep by a two-sided relation",
        })
        barkeep = next(
            n for n in entities_data["npcs"] if n["id"] == "npc_barkeep_01"
        )
        barkeep.setdefault("pair_relations", []).append(
            {"with": "npc_hermit_01", "trust": 40}
        )
        entities_data["items"].append({
            "id": "orb_01", "name": "the glass orb", "position": "loc_cellar",
            "carrier": None, "is_fire_source": False, "breakable": False,
            "flammability": "none",
            "notes": "declared, pretty, and untouchable by any verb",
        })

    target = crafted(tmp_path, "orphan_item", entities=entities)
    refuses(target, r"entity orb_01: orphan")


def test_an_isolated_location_is_an_orphan(tmp_path: Path) -> None:
    """The position-read half: a location with no exits edge and no name
    reference is reachable by nothing — dead weight, refused."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["locations"].append({
            "id": "loc_cellar", "name": "the sealed cellar", "exits": [],
            "flammability": "none", "fire_spots": [],
            "notes": "no doors, no windows, no references, no occupants",
        })

    target = crafted(tmp_path, "orphan_cellar", entities=entities)
    refuses(target, r"entity loc_cellar: orphan")


def test_a_stranded_occupant_is_an_orphan(tmp_path: Path) -> None:
    """The knower half: an npc at an isolated location is unreachable
    by any positional audience (the reference walk missed them by name,
    the exits graph has no edge to their room) — the hermit is touched
    by nothing, refused. The cellar itself is touched by the hermit's
    own position declaration (the fold reads it — a position read)."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["locations"].append({
            "id": "loc_cellar", "name": "the sealed cellar", "exits": [],
            "flammability": "none", "fire_spots": [],
            "notes": "no doors, no windows — but the hermit stands here",
        })
        entities_data["npcs"].append({
            "id": "npc_hermit_01", "name": "the hermit",
            "position": "loc_cellar", "status": {}, "relations": {},
            "knowledge": [], "mood": "quiet", "goal": "be left alone",
            "notes": "stranded with the cellar",
        })

    target = crafted(tmp_path, "orphan_hermit", entities=entities)
    refuses(target, r"entity npc_hermit_01: orphan")


def test_a_takeable_item_is_not_an_orphan(tmp_path: Path) -> None:
    """The grammar-reachable reading pinned: an unreferenced, unflagged
    item at a walked location is addressable by the take family — the
    event grammar touches it, the orphan check passes it."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["items"].append({
            "id": "candle_01", "name": "the stub of candle",
            "position": "loc_tavern", "carrier": None,
            "notes": "nothing references it — the take verb still can",
        })

    target = crafted(tmp_path, "takeable", entities=entities)
    assert load_pack(target)


# -- §5 row 3: empty intersection-matrix rows ------------------------------------


def test_an_unexercised_npc_row_is_refused(tmp_path: Path) -> None:
    """An npc the dynamic grammar can reach (co-located, talkable) but
    no authored surface ever wires — no urgency, no watch slot, no
    expectation, no hook, no pair relation, no carried item — is an
    empty matrix row: dead design space, refused."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["npcs"].append({
            "id": "npc_loafer_01", "name": "the loafer",
            "position": "loc_tavern", "status": {}, "relations": {},
            "knowledge": [], "mood": "idle", "goal": "loiter",
            "notes": "stands in the taproom, wired into nothing",
        })

    target = crafted(tmp_path, "empty_row", entities=entities)
    refuses(target, r"npc npc_loafer_01: the intersection-matrix row is empty")


def test_a_pair_relation_exercises_both_sides(tmp_path: Path) -> None:
    """The authored-surface inventory read: a pair relation is an
    authored exercise of BOTH sides — an npc whose only wiring is a
    declared relationship is a non-empty row (the committed maid's
    own shape)."""
    def entities(entities_data: dict[str, Any]) -> None:
        entities_data["npcs"].append({
            "id": "npc_twin_01", "name": "the quiet twin",
            "position": "loc_tavern", "status": {}, "relations": {},
            "pair_relations": [{"with": "npc_barkeep_01", "trust": 40}],
            "knowledge": [], "mood": "calm", "goal": "keep company",
            "notes": "wired by the relation alone",
        })

    target = crafted(tmp_path, "related_row", entities=entities)
    assert load_pack(target)


# -- §5 row 4: declared-but-unused templates -------------------------------------


def test_a_declared_but_unused_template_is_refused(tmp_path: Path) -> None:
    """A template line no emission site, core constant or story-critical
    listing renders is dead vocabulary — the reverse walk over the same
    closed set the forward closure validates."""
    def templates(tpl: dict[str, Any]) -> None:
        tpl["events"]["ghost_bell"] = "A bell no one ever rings."

    target = crafted(tmp_path, "ghost_bell", templates=templates)
    refuses(target, r"templates: 'ghost_bell' is declared but unused")


def test_the_story_critical_listing_is_the_dormancy_witness(tmp_path: Path) -> None:
    """A template the tale's own listing carries is deliberately kept
    vocabulary — the authored-intent witness: the on_action block
    stripped, the crowd_wary line kept, the pack still lints (the 68a
    twin's dormant lines ride the listing)."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data.pop("on_action", None)

    target = crafted(tmp_path, "dormant_lines", rules=rules)
    assert load_pack(target)


# -- §6: the live-char crosswalk ---------------------------------------------------


def test_a_partial_spine_is_refused(tmp_path: Path) -> None:
    """AP-9: the spine is all-or-nothing — want/need tension and flaw
    rooted in a cause are four load-bearing fields; a half-declared
    spine is a broken spine."""
    def entities(entities_data: dict[str, Any]) -> None:
        npc = next(n for n in entities_data["npcs"] if n["id"] == "npc_drunk_01")
        npc["spine"] = {
            "want": "forget the war", "need": "stay upright till dark",
            "flaw": "the drink always wins",
        }

    target = crafted(tmp_path, "broken_spine", entities=entities)
    refuses(target, r"npc npc_drunk_01: spine.cause is required")


def test_a_full_spine_with_a_consumed_flaw_lints_green(tmp_path: Path) -> None:
    """AP-8's positive pin: the drunkard's spine declared whole, his
    coerce entry carrying the flaw token — GHOST with anchors, the
    behavior rule consuming the flaw, the pack green."""
    def entities(entities_data: dict[str, Any]) -> None:
        npc = next(n for n in entities_data["npcs"] if n["id"] == "npc_drunk_01")
        npc["spine"] = {
            "want": "forget the war", "need": "stay upright till dark",
            "flaw": "the drink always wins", "cause": "the siege took his sons",
        }

    def rules(rules_data: dict[str, Any]) -> None:
        entry = next(
            e for e in rules_data["urgencies"]["entries"]
            if e["npc"] == "npc_drunk_01"
        )
        entry["flaw"] = "the drink always wins"

    target = crafted(
        tmp_path, "anchored_spine", entities=entities, rules=rules,
    )
    assert load_pack(target)


def test_an_unconsumed_flaw_is_refused(tmp_path: Path) -> None:
    """AP-8: GHOST without anchors is dead pack data — a declared flaw
    no behavior rule consumes is refused (the spine exists, the drink
    never drives anything)."""
    def entities(entities_data: dict[str, Any]) -> None:
        npc = next(n for n in entities_data["npcs"] if n["id"] == "npc_drunk_01")
        npc["spine"] = {
            "want": "forget the war", "need": "stay upright till dark",
            "flaw": "the drink always wins", "cause": "the siege took his sons",
        }

    target = crafted(tmp_path, "unconsumed_flaw", entities=entities)
    refuses(target, r"spine flaw 'the drink always wins' is unconsumed")


def test_an_urgency_flaw_token_must_name_a_declared_flaw(tmp_path: Path) -> None:
    """The forward direction: a consuming rule's flaw token that names
    no declared spine is dead vocabulary — refused like every other
    dangling reference."""
    def rules(rules_data: dict[str, Any]) -> None:
        entry = next(
            e for e in rules_data["urgencies"]["entries"]
            if e["npc"] == "npc_drunk_01"
        )
        entry["flaw"] = "no such flaw anywhere"

    target = crafted(tmp_path, "phantom_flaw", rules=rules)
    refuses(target, r"flaw 'no such flaw anywhere' names no declared spine flaw")


def test_clone_npcs_sharing_a_trigger_action_pair_are_refused(tmp_path: Path) -> None:
    """AP-11: two LIVE entries from different NPCs with the identical
    (intent, requires) pair are clones — the design-time twin of M4
    novelty, refused at admission."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["urgencies"]["entries"].append({
            "npc": "npc_barkeep_01", "probability_per_beat": 30,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
            "requires": [],
        })

    target = crafted(tmp_path, "clone_pair", rules=rules)
    refuses(target, r"clone NPCs.*npc_maid_01.*npc_barkeep_01.*'wait'")


def test_a_zero_weight_slot_is_not_a_clone(tmp_path: Path) -> None:
    """The stream-placeholder exemption: a probability-0 slot never
    fires — it is a roll-position probe, not a behavior, so sharing its
    pair with a live entry clones nothing (the add-safety law's own
    crafted shape, kept legal)."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["urgencies"]["entries"].append({
            "npc": "npc_barkeep_01", "probability_per_beat": 0,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
        })

    target = crafted(tmp_path, "quiet_slot", rules=rules)
    assert load_pack(target)


def test_a_nested_predicate_is_refused(tmp_path: Path) -> None:
    """AP-15: a compound's members must be leaves — the conditional
    chain ("if X and if Y before that") is refused; split it into
    separate rules instead."""
    def rules(rules_data: dict[str, Any]) -> None:
        hook = rules_data["director"]["hooks"]["guard_suspicious_of_pc"]
        hook["weight"]["modifiers"][0]["when"] = {
            "all": [
                {"kind": "prop", "of": "npc_guard_01",
                 "path": "pair.pc_01.suspicion", "value": 50,
                 "comparator": "at_least"},
                {"any": [
                    {"kind": "time", "tick": 360},
                    {"kind": "time", "tick": 720},
                ]},
            ],
        }

    target = crafted(tmp_path, "nested_cond", rules=rules)
    refuses(target, r"nested compound — one condition per rule")


def test_a_flat_compound_predicate_lints_green(tmp_path: Path) -> None:
    """The atomic compound is legal: `all` over leaves is one flat
    condition, the split law's own permitted shape."""
    def rules(rules_data: dict[str, Any]) -> None:
        hook = rules_data["director"]["hooks"]["guard_suspicious_of_pc"]
        hook["weight"]["modifiers"][0]["when"] = {
            "all": [
                {"kind": "prop", "of": "npc_guard_01",
                 "path": "pair.pc_01.suspicion", "value": 50,
                 "comparator": "at_least"},
                {"kind": "time", "tick": 360},
            ],
        }

    target = crafted(tmp_path, "flat_cond", rules=rules)
    assert load_pack(target)


def test_contradictory_ungated_reactions_are_refused(tmp_path: Path) -> None:
    """AP-13: two ungated reactions to the same event asserting the same
    prop in opposite directions cancel out — the gate vocabulary exists
    to separate them, and the lint demands it."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["on_action"]["alarm_raised"].append({
            "scope": "witnesses", "event": "panic_ripple",
            "state": {"prop": "status.fear", "add": -10},
        })

    target = crafted(tmp_path, "contradiction", rules=rules)
    refuses(target, r"contradictory rules.*status.fear")


def test_a_gated_opposing_reaction_is_legal(tmp_path: Path) -> None:
    """The gate separates them: the same opposing add with a gate key
    is a deliberate conditional rule, not a cancellation."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["on_action"]["alarm_raised"].append({
            "scope": "witnesses", "event": "panic_ripple",
            "gate": [{"prop": "status.intoxication", "comparator": "at_least",
                      "value": 40}],
            "state": {"prop": "status.fear", "add": -10},
        })

    target = crafted(tmp_path, "gated_opposition", rules=rules)
    assert load_pack(target)


def test_a_budget_violation_is_refused(tmp_path: Path) -> None:
    """AP-1: the pack's own declared bounds are enforced — six npcs
    against a declared 2..3 is a pack that outgrew its shape."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["budget"] = {"npcs": {"min": 2, "max": 3}}

    target = crafted(tmp_path, "over_budget", rules=rules)
    refuses(target, r"budget.npcs: count 6 is outside the declared bounds")


def test_a_satisfied_budget_lints_green(tmp_path: Path) -> None:
    """The declared-bounds positive pin: the counts inside their budget,
    the metadata block silent when satisfied."""
    def rules(rules_data: dict[str, Any]) -> None:
        rules_data["budget"] = {
            "npcs": {"min": 6, "max": 8},
            "items": {"min": 5, "max": 5},
            "hooks": {"min": 1, "max": 20},
            "templates": {"min": 40, "max": 60},
        }

    target = crafted(tmp_path, "in_budget", rules=rules)
    assert load_pack(target)


# -- §6: the price-marker lint (AP-2's design-time half) -------------------------


def test_deferred_hooks_without_an_immediate_price_marker_are_refused(
    tmp_path: Path,
) -> None:
    """AP-2: a socially meaningful behavior must be observable
    in-scene. The wait verb's ambient murmur re-pointed at a SOCIAL
    hook — deferred consequence, no knowledge record, no state token on
    the branch — is socially invisible, refused."""
    def actions(acts: list[dict[str, Any]]) -> None:
        wait = next(a for a in acts if a["intent"] == "wait")
        wait["hooks"]["success"] = ["guard_suspicious_of_pc"]

    target = crafted(tmp_path, "invisible_price", actions=actions)
    refuses(target, r"action wait: the success hooks seed deferred "
                    r"consequences with no immediate price marker")


def test_ambient_hooks_need_no_price_marker(tmp_path: Path) -> None:
    """The ambient channel's exemption pinned: the committed wait verb
    (its murmur ride is texture, weight 0 — the noise floor) needs no
    immediate marker; the committed pack's own shape, held green."""
    assert load_pack(TAVERN)
