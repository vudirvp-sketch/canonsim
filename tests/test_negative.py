"""negative — the W7 negative/compression witness (iter-283, the
owner's «продолжай работу над задачами класса мирового трека, W7
открывай если больше ничего не осталось» call — the station's first
row: the eight-question battery and the compression test run on the
SAME canonical package, the committed province_pack untouched, zero
core, zero pack change, the LOG untouched, zero corpus price).

The station's law (WORLD_WORKPLAN §9, WORLD_TRACK_AGENT_CONTEXT §9):
for any new major capability, regime or institution ask `why
possible? why not universal? what does it replace? what does it make
harder? who profits? who resists? who remembers? what if it
disappears?` — then run the compression test and remove or merge
decorative material. The first row's scope: the three majors the
world track LANDED with committed consumers and honest deterministic
instruments — the account substrate's fourth verb `settle` (iter-273),
the market's mourning hook `market_mourns` (iter-264/274), and the
secrets/leverage registry (the mystery's substrate). The eight
questions map as follows (the admission evidence — why possible, what
it replaced, what it made harder — is CITED to its owners, never
re-derived, D-024; the measured rows are this witness's own):

- WHY NOT UNIVERSAL — the negative-space census: the closed gate
  vocabulary (exactly one of noun/holder per account gate), the
  no-leak option gate (a standing market never mourns — the option's
  availability gate the SAME prop read as the hook trigger), the
  families' deadband (threshold 50 over trigger 40 — one woken elder
  reads fraction 50, silent), the tale gate (min_importance medium —
  the low-importance moves never enter the tale), the fixed secret
  subjects (the templated-token ineligibility law), the structural
  registry (an empty secrets.tokens refuses at the lint). D-238's
  calendar (surface-only by construction) is cited, never re-measured.
- WHO RESISTS — the lint's own refusals, measured: emptying the
  registry and removing the hook without its seed both refuse at
  load — the capability's structural floor.
- WHAT IF IT DISAPPEARS — the disappearance battery, three arms:
  settle gone -> the calm run BYTE-IDENTICAL (the D-108 both-arms
  law: an unused capability costs nothing) and the buyer's probe
  refused at the GRAMMAR level (RunnerError — the wall returns in
  its hardest form: the world cannot even express the transfer);
  the mourning gone -> the departure never fires, the mistress stays
  at the ashes, the talks stay loud (287 vs 2 — iter-274's measured
  price inverted: the market's social function survives its carrier
  because the carrier never leaves), the feud family and the macro
  arm untouched (vigil 4=4, sourced 4=4) while the social band
  cascades (council 208->1 — the carrier's footprint);
  the word unregistered -> the read STILL mints the knowledge exact
  (the fact survives — the write is the action's own) but zero
  levers and the coerce refused at actor.leverage_over (the door
  dies — the registry IS the leverage authority).
- WHO PROFITS / THE COMPRESSION TEST — the reachability inventory:
  every one of the 76 event templates is producible by construction
  (an action's event type, a structural rules declaration, a group's
  own macro/condense event, or the intent door); every account-kind
  gloss, flow gloss and symbol is declared/referenced; every
  knows-table entry is matchable by a mintable token; the four
  entity ids no other data references each carry their own canonical
  door (the lamp the corpus's arson instrument, the traffic group
  its macro_event arming, the jug its use_effect axis, the sack its
  flammability). VERDICT: no decorative material at the measured
  band — the census's own «0 consumerless» cited (scripts/mechanics
  census, the cov-1 instrument). The UNREALIZED action surface is
  possibility-space (the player's doors — the anti-pattern law: the
  doors exist even unopened), never decoration.

The claim packet (TEST_PLAN §9):

- Claim: the substrate's landed majors survive the negative battery —
  each disappearance kills exactly its own family (the others
  measurable, the disable test's form), each capability has a
  structural floor (the lint), and the committed pack carries ZERO
  decorative material at the reachability-by-construction band.
- Lens(es): the disappearance lens (remove the capability's own rows,
  never a shared driver — the disable test's law); the
  reachability-by-construction lens (a surface is live iff the pack
  declares a canonical path to it — never the fired-count in one
  run, the census's own separate row); the negative-space lens (the
  committed shapes ARE the "why not universal" answers).
- Prism: the crafted pack-data twins (the divergence-probe form —
  the same scripts, one pack-data difference each) plus the static
  inventory scans over the committed pack.
- Oracle: the byte comparison (the calm run), the RunnerError, the
  event-log scans (moves/talks/council/vigil/levers/rejections),
  the projection reads (positions), the producible-union set
  difference, the template/kind/flow/symbol/knows cross-checks.
- Falsifier: the calm run diverging without the capability (a hidden
  price); the buyer's probe landing on the twin (the wall not
  real); the mourning's removal leaving the talks quiet (the
  carrier not the cause); the word unregistering still minting a
  lever (the registry not the authority); ANY template key without
  a producible path, ANY unglossed-decorative surface, ANY entity
  without a canonical door; the golden T1 bytes shifting.
- Expected evidence: the dry-run's own numbers (2269=2269 bytes;
  the wall's RunnerError; 287/2 talks, 4/4 vigil, 208/1 council;
  the word exact with zero levers; the empty missing-set).
- Observed evidence: CONFIRMED at the measured band (seed 2 the
  composition arm, seed 42 the wall/journey arms).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED at the deterministic band — the battery's
  first row expressed. The honest boundaries: (a) the compression
  band is reachability-BY-CONSTRUCTION — a surface that never fired
  in a recorded run is NOT decorative (the possibility-space law);
  (b) the unglossed mintable literals (the_flood_story,
  the_winter_kin, the failure-path tokens) ride the documented dry
  fallback — the honest family law, a READING-side shape never
  touched here; (c) the ungarrisoned window (0 patrols both arms)
  is the composition witness's own recorded limitation, never a
  missing mechanic. No plot written, no machinery promoted, no pack
  change.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.log import read_log
from core.loop import RunnerError, Simulator, load_playscript
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"

MIST = "npc_marketmistress_01"     # the beam's keeper — the departure's carrier
MASTER = "npc_smelter_01"         # the camp's own hand — the word's subject
TALLY = "camp_tally_01"           # the count cut in wood — the read hinge
WORD = "the_camps_word"           # the hidden fact — the registry's third key
MALBY = "loc_malby"               # the beam's town — the market's stage
KEEP = "loc_keep"                 # the artery's node — the departure's roof
CHEST = "loc_malby"               # the guild's chest town (the sale's site)


# -- the twins (the divergence-probe form, one pack-data difference each) --------


def _twin(
    tmp_path: Path, name: str, mutate: Callable[[dict[str, Any]], None],
) -> Path:
    """The committed pack with ONE capability's own rows removed —
    the disappearance probe's twin. `mutate` receives the four-file
    data dict before the write+load (never the committed pack itself)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    data = {
        fname: json.loads((target / f"{fname}.json").read_text(encoding="utf-8"))
        for fname in ("actions", "entities", "rules", "templates")
    }
    mutate(data)
    for fname, payload in data.items():
        (target / f"{fname}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return target


def _no_settle(data: dict[str, Any]) -> None:
    """The fourth verb's own row removed — the capability gone from
    the grammar (the committed consumer sell_bloom with it)."""
    data["actions"]["actions"] = [
        a for a in data["actions"]["actions"] if a["intent"] != "sell_bloom"
    ]


def _no_mourns(data: dict[str, Any]) -> None:
    """The mourning hook's own rows removed together — the director
    entry AND its seeding reference (the wait action's success hooks),
    the two halves of one capability (the seeding law)."""
    del data["rules"]["director"]["hooks"]["market_mourns"]
    for act in data["actions"]["actions"]:
        if act["intent"] == "wait":
            act["hooks"]["success"] = [
                t for t in act["hooks"]["success"] if t != "market_mourns"
            ]


def _no_word(data: dict[str, Any]) -> None:
    """The registry's third key removed — the hidden fact unregistered
    (the read's knowledge write is the action's own and stays)."""
    del data["rules"]["secrets"]["tokens"][WORD]


def _run(
    pack_dir: Path, tmp_path: Path, name: str, script: dict[str, Any],
) -> tuple[list, Simulator]:
    pack = load_pack(pack_dir)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, sim


@pytest.fixture(scope="module")
def composition(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[list, Simulator, bytes]:
    """The committed composition run, once per module (seed 2, the
    iter-261/274 witness's own script — the departure's carrier
    burns the stalls and the cascade is on the record)."""
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_composition.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path_factory.mktemp("negative") / "composition.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, sim, log.read_bytes()


#: the buyer's purchase — the settle class pin's own example (the
#: coin from the actor, the bloom from the location, one atomic door).
#: Against the no-settle twin this is the wall probe: the grammar
#: itself must refuse the expression.
BUYER: dict[str, Any] = {
    "name": "buyer", "seed": 42, "pack": "province_pack@0.1",
    "steps": [
        {"intent": "move", "actor": MASTER, "target": KEEP},
        {"intent": "move", "actor": MASTER, "target": CHEST},
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ],
}

#: the journey's read hinge — the word's own minting path (the
#: iter-185 chain's material, the registry's consumer).
JOURNEY: dict[str, Any] = {
    "name": "journey", "seed": 42, "pack": "province_pack@0.1",
    "steps": [
        {"intent": "move", "target": KEEP},
        {"intent": "move", "target": "loc_crofts"},
        {"intent": "wait", "ticks": 400},
        {"intent": "read_tally", "target": TALLY},
        {"intent": "coerce", "target": MASTER},
        {"intent": "wait", "ticks": 10},
    ],
}


# -- WHY NOT UNIVERSAL: the negative-space census ---------------------------------


def test_the_negative_space_census() -> None:
    """The committed shapes that ARE the "why not universal" answers —
    the capability's deliberate NOT-doings, each pinned where it
    lives: the closed gate vocabulary (an account gate carries a
    holder OR a noun, never both — the endpoint vocabulary stays
    closed); the no-leak option gate (the only world where the
    mourning releases on ANY path is the world where the trigger
    already fires); the families' deadband (the vigil threshold 50
    over the trigger 40 — the same axis two bars apart, a single
    fire waking exactly one elder); the tale gate (medium — the
    low-importance moves never enter the tale); the fixed secret
    subjects (no templated tokens — the literal vocabulary the only
    legal surface). D-238's calendar (removing all 52 turns left
    the projection byte-identical — surface-only BY CONSTRUCTION) is
    cited from its owner, never re-measured here."""
    pack = load_pack(PACK_DIR)
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    # the closed gate vocabulary: exactly one of noun/holder per gate
    sale = actions["sell_bloom"]
    gates = sale["requires"]
    assert gates, "the settle door carries its solvency gates"
    for gate in gates:
        has_noun = "noun" in gate
        has_holder = "holder" in gate
        assert has_noun != has_holder, (
            f"the endpoint vocabulary closed: {gate} carries both/neither"
        )
    assert {"test": "account_at_least", "holder": "loc_crofts",
            "kind": "bloom", "value": 1} in gates
    assert {"test": "account_at_least", "holder": CHEST,
            "kind": "coin", "value": 3} in gates
    # the no-leak option gate: the option's availability gate is the
    # SAME prop read as the hook trigger
    hook = pack.rules["director"]["hooks"]["market_mourns"]
    assert hook["trigger"] == {"kind": "prop", "of": MALBY,
                               "path": "destroyed",
                               "comparator": "equals", "value": True}
    assert hook["options"][0]["trigger"] == hook["trigger"]
    # the families' deadband: threshold 50 over trigger 40
    families = next(
        e for e in pack.rules["factions"]["entries"]
        if e["intent"]["kind"] == "hold_vigil"
    )
    assert families["threshold"] == 50 and families["trigger_value"] == 40
    # the tale gate: the low-importance band never enters the tale
    assert pack.templates["tale_gate"] == {"min_importance": "medium"}
    # the fixed subjects: the literal vocabulary the only legal surface
    subjects = {t["subject"] for t in pack.rules["secrets"]["tokens"].values()}
    assert subjects and all(
        isinstance(s, str) and "{" not in s for s in subjects
    )


def test_the_lint_resists_the_structural_gaps(tmp_path: Path) -> None:
    """WHO RESISTS, measured: the capability's structural floor — the
    load-time lint refuses both half-removals. An EMPTY secrets
    registry is not a world (the leverage authority is structural,
    not optional); a hook removed while its seeding reference stands
    is a silent lie (the seeded consequence would never fire — the
    lint demands the declaration first). The disappearances that
    LOAD are the honest band: the capability's own rows removed
    TOGETHER."""
    def _empty_registry(data: dict[str, Any]) -> None:
        data["rules"]["secrets"]["tokens"] = {}

    def _unseeded_hook(data: dict[str, Any]) -> None:
        del data["rules"]["director"]["hooks"]["market_mourns"]

    for name, mutate in (
        ("empty_registry", _empty_registry),
        ("unseeded_hook", _unseeded_hook),
    ):
        twin = _twin(tmp_path, f"lint_{name}", mutate)
        with pytest.raises(PackError):
            load_pack(twin)


# -- WHAT IF IT DISAPPEARS: the disappearance battery ------------------------------


def test_settle_disappears_the_calm_run_costs_nothing(
    tmp_path: Path, composition: tuple[list, Simulator, bytes],
) -> None:
    """The fourth verb's disappearance over the calm run: the
    composition script never speaks the settle door, and the twin's
    log is BYTE-IDENTICAL — the D-108 both-arms law at the capability
    scale (an unused door costs nothing: no draws, no noise, no
    cascade). The account substrate's presence alone is never a
    price; only its USE moves the world."""
    _, _, base_bytes = composition
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_composition.json"
    )
    twin = _twin(tmp_path, "no_settle", _no_settle)
    log = tmp_path / "calm.jsonl"
    sim = Simulator(load_pack(twin), script["seed"], log, SCHEMA,
                    commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == base_bytes


def test_settle_disappears_the_wall_returns(tmp_path: Path) -> None:
    """The same disappearance at the door's own consumer: the buyer's
    purchase — the class pin's own example — cannot even be EXPRESSED.
    The intent names a verb the grammar no longer carries and the
    runner refuses LOUD (RunnerError), the iter-273 grammar wall
    returned in its hardest form: before the capability the world did
    not merely refuse the transfer, it had no word for it."""
    twin = _twin(tmp_path, "no_settle_wall", _no_settle)
    log = tmp_path / "wall.jsonl"
    sim = Simulator(load_pack(twin), BUYER["seed"], log, SCHEMA,
                    commit="0000000")
    with pytest.raises(RunnerError, match="sell_bloom"):
        sim.run_playscript(BUYER)


def test_the_mourning_disappears_the_market_stays_loud(
    tmp_path: Path, composition: tuple[list, Simulator, bytes],
) -> None:
    """The departure's disappearance — iter-274's measured price
    inverted, arm for arm. With the hook gone the mistress NEVER
    leaves the ashes (zero moves against one; she ends at Malby, not
    the keep's roof) and the market's social surface stays loud: the
    talks 287 against 2, the rumors 22 against 2, the council back to
    its single live sitting against the 208-event catch-up pile — the
    carrier's footprint, the exact shape the departure had paid. The
    OTHER families survive the disable test: the feud's vigils 4=4
    and the macro arm's sourced 4=4, untouched — the mourning was
    never their driver. A living market here is a LOUD one: the
    social function survived its carrier only because the carrier
    never left."""
    base_events, base_sim, _ = composition
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_composition.json"
    )
    twin = _twin(tmp_path, "no_mourns", _no_mourns)
    twin_events, twin_sim = _run(twin, tmp_path, "twin_mourns", script)

    def _count(events: list, *types: str) -> int:
        return sum(1 for e in events if e.type in types)

    def _moves_by(events: list, who: str) -> int:
        return sum(1 for e in events if e.type == "move" and e.actor == who)

    assert _moves_by(base_events, MIST) == 1     # the departure fired
    assert _moves_by(twin_events, MIST) == 0    # the carrier never left
    assert base_sim.projection[MIST]["position"] == KEEP
    assert twin_sim.projection[MIST]["position"] == MALBY
    assert _count(twin_events, "talk", "talk_rebuffed") == 287
    assert _count(base_events, "talk", "talk_rebuffed") == 2
    assert _count(twin_events, "rumor_told") == 22
    assert _count(base_events, "rumor_told") == 2
    assert _count(twin_events, "guild_councils") == 1
    assert _count(base_events, "guild_councils") == 208
    # the other families survive (the disable test's law)
    assert _count(twin_events, "wergeld_vigil") == 4
    assert _count(base_events, "wergeld_vigil") == 4
    assert _count(twin_events, "account_sourced") == 4
    assert _count(base_events, "account_sourced") == 4
    assert (len(twin_events), len(base_events)) == (2372, 2269)


def test_the_word_unregisters_the_door_dies(tmp_path: Path) -> None:
    """The mystery's disappearance shape — the registry's third key
    removed. The read STILL mints the word exact (the knowledge write
    is the action's own: the FACT survives its registry — the log
    keeps what the door once carried) but ZERO levers form and the
    coerce is refused at actor.leverage_over (the DOOR dies — the
    registry IS the leverage authority, the difference between a
    hidden fact and a usable one). The knowledge never becomes
    power without the institution that recognizes it."""
    twin = _twin(tmp_path, "no_word", _no_word)
    events, sim = _run(twin, tmp_path, "twin_word", JOURNEY)
    reads = [e for e in events if e.type == "tally_read"]
    assert len(reads) == 1                       # the hinge itself unharmed
    word = {(r.who, r.fidelity) for e in events for r in e.knowledge
            if r.knows == WORD}
    assert word == {("pc_01", "exact")}          # the fact survives
    assert not [e for e in events if e.type == "leverage_gained"]
    assert not [e for e in events if e.type == "coerce"]
    refusals = [e for e in events if e.type == "intent_rejected"
                and e.outcome["action"] == "coerce"]
    assert len(refusals) == 1
    assert refusals[0].outcome["failed_test"] == "actor.leverage_over"
    assert sim.projection[MASTER].get("pair.pc_01.fear") is None


# -- THE COMPRESSION TEST: the reachability inventory ------------------------------


def _structural_atoms(payload: Any, out: set[str]) -> None:
    """Every string atom of the structural tree (notes stripped —
    prose is never a declaration)."""
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key == "notes":
                continue
            out.add(key)
            _structural_atoms(value, out)
    elif isinstance(payload, list):
        for item in payload:
            _structural_atoms(item, out)
    elif isinstance(payload, str):
        out.add(payload)


def test_the_compression_inventory_events() -> None:
    """The compression test, events leg: every one of the 76 event
    templates is producible BY CONSTRUCTION — it is an action's own
    success/failure event type, a structural rules declaration (the
    systems' event_type fields, the on_action tables, the
    downstream-consumers crosswalk), a group entity's own
    macro/condense arming, or the intent door's rejection. A template
    keyed to a type this pack can never produce would be decorative —
    the missing set is EMPTY. The reverse direction (producible types
    without a template) renders through the fallback line, the
    documented family law, never a defect."""
    pack = load_pack(PACK_DIR)
    producible: set[str] = set()
    for act in pack.data["actions.json"]["actions"]:
        events = act.get("events") or {}
        for outcome in ("success", "failure"):
            if isinstance(events.get(outcome), str):
                producible.add(events[outcome])
    atoms: set[str] = set()
    _structural_atoms(pack.rules, atoms)
    producible |= atoms
    for group in pack.entities.get("groups", []):
        for field in ("macro_event", "condense_event"):
            if group.get(field):
                producible.add(group[field])
    producible.add("intent_rejected")  # the door's own refusal event
    missing = sorted(set(pack.templates["events"]) - producible)
    assert missing == []
    assert len(pack.templates["events"]) == 76


def test_the_compression_inventory_meaning_surfaces() -> None:
    """The compression test, meaning legs: every account-kind gloss
    keys a kind the data actually arms (the accounts' declared kinds);
    every flow gloss keys a flow the economy declares; every symbol
    is referenced by some template through the #name# indirection;
    every knows-table entry is matchable by a token the pack can mint
    (a literal write, a secrets key, or a templated write of the same
    shape). The missing sets are all EMPTY — no decorative glosses.
    The census's own «0 consumerless» (the action-level walk,
    scripts/mechanics census — the cov-1 instrument) is cited, never
    re-derived here."""
    pack = load_pack(PACK_DIR)
    rules_blob = json.dumps(pack.rules)
    entities_blob = json.dumps(pack.entities)

    kinds = set(pack.templates["account_kinds"])
    for kind in kinds:
        assert f'"{kind}"' in rules_blob + entities_blob, (
            f"decorative account-kind gloss: {kind}"
        )
    flows = set(pack.templates["flow_glosses"])
    declared = {f["id"] for f in pack.rules["economy"]["flows"]}
    assert flows <= declared

    all_templates = json.dumps(pack.templates)
    for symbol in pack.templates["symbols"]:
        assert f"#{symbol}#" in all_templates, (
            f"decorative symbol: {symbol}"
        )

    minted: set[str] = set()

    def _collect(payload: Any) -> None:
        if isinstance(payload, dict):
            for key, value in payload.items():
                if key == "knows" and isinstance(value, str):
                    minted.add(value)
                else:
                    _collect(value)
        elif isinstance(payload, list):
            for item in payload:
                _collect(item)

    _collect(pack.data["actions.json"])
    secrets = set(pack.rules["secrets"]["tokens"])

    def _shape(text: str) -> str:
        return re.sub(r"\{[^}]+\}", "*", text)

    minted_shapes = {_shape(m) for m in minted if "{" in m}
    minted_literals = {m for m in minted if "{" not in m} | secrets
    for entry in pack.templates["knows"]:
        if "{" in entry:
            assert _shape(entry) in minted_shapes, (
                f"decorative knows pattern: {entry}"
            )
        else:
            assert entry in minted_literals, (
                f"decorative knows literal: {entry}"
            )
    assert len(pack.templates["knows"]) == 34


def test_the_compression_inventory_entities() -> None:
    """The compression test, entities leg: the four ids no other pack
    data references (the inventory's own flagged rows) each carry
    their canonical door — the lamp is the committed corpus's arson
    instrument (every province playscript's carried fire source), the
    traffic group DECLARES its own arming (the macro/condense events
    the road system reads), the jug carries a use_effect on an axis
    with three named consumers (the perception modifier, the rumor
    teller penalty, the scene-card marker), the sack carries a
    flammability the fire family reads. None is decorative — and the
    anti-pattern law stands: an unopened door is possibility-space,
    never decoration (the UNREALIZED action surface stays)."""
    pack = load_pack(PACK_DIR)
    items = {i["id"]: i for i in pack.entities["items"]}
    groups = {g["id"]: g for g in pack.entities["groups"]}

    corpus = "".join(
        p.read_text(encoding="utf-8")
        for p in (REPO / "tests" / "playscripts").glob("province_*.json")
    )
    assert '"tallow_lamp_01"' in corpus            # the corpus's instrument
    assert items["tallow_lamp_01"]["is_fire_source"] is True

    traffic = groups["grp_road_traffic"]
    assert traffic["macro_event"] == "road_counts"
    assert traffic["condense_event"] == "road_musters"

    jug = items["brew_jug_01"]
    assert jug["use_effect"] == {"status": "intoxication", "delta": 20}
    # the axis's three named consumers (the jug is the vector, not the end)
    skills_blob = json.dumps(pack.rules)
    assert '"per_10_points": -2' in skills_blob   # the perception modifier
    assert '"teller_penalty_axis": "intoxication"' in skills_blob
    assert '"prop": "status.intoxication"' in skills_blob

    assert items["charcoal_sack_01"]["flammability"] == "medium"


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the W7 witness is crafted pairs of
    twins over the committed pack — zero core, zero pack change, the
    golden T1 fixture byte-identical."""
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(load_pack(PACK_DIR), script["seed"], log, SCHEMA,
                    commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == GOLDEN.read_bytes()
