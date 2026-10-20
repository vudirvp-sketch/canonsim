"""ironcycle — the iron scarcity cycle's measured legs (iter-394, the
owner's standing directive «давай то что логично и способствует качеству
в долгосрок… оно потом должно работать глобально и само по себе без
прописывания точечно»: the ANCHOR_REGION §3/§8 row — "bloom, iron,
charcoal as measured scarcity" — over the STANDING primitives, ALL PACK
DATA, ZERO CORE (the stageb-1 B2/B4 patterns landed in the anchor, the
farstead fixture the family precedent).

The row's arming (the production's input ledger): THREE working kinds
on the crofts — wood (the cut's yield), ore (the seam's weathering),
charcoal (the stacks' fuel), all seeded EMPTY at the weighing aftermath
— plus TWO bounded sources (`the_coppice_grows` +2 wood a year,
CAPACITY 8; `the_seam_yields` +5 ore a year, CAPACITY 10 — CONTRACTS
§12 B4, the every-miss silence at full) and ONE recipe (`the_burn`:
wood 2 → charcoal 2 at the crofts — the cut fired to the stacks, ONE
atomic account_converted event, conservation per recipe per kind) fired
by ONE gated post (the master's burn — the farmland forge precedent:
the material's arrival the pacing, the soft refusal the perturbation
safety, the scene-LOD beat walk the observation law).

THE COMMITTED RHYTHM UNTOUCHED: the burn's annual five loads keep
their armed dispositions (the withheld two the banking flow's, the
sold three the sale door's) — the smelt's TRANSFORMATION stays the
authored aggregate.

THE SMELT'S FEED WALLED — the row's own measured findings, three
first-exposure substrate gaps recorded, never routed (the
separate-track law, the stepbench two-sided-band gap's own class):
(1) the CONSUME verb's actor-side grammar (a consume always drains
the intent actor — loc_crofts' stocks unreachable); (2) the SETTLE
line's byte-pinned trade reading (any two-kind draw renders a false
exchange); (3) the RECIPE double-mint (a smelt recipe minting bloom
would double-mint the freightvol-pinned heap). The walls' resolutions
each an owner-gated fork — the I0 inventory's fourth candidate class.

The claim packet (TEST_PLAN §9):

- Claim: the iron scarcity cycle's input half is one pack-data arming
  — the yard's yields as live bounded stocks, the cut fired to the
  stacks as ONE atomic craft event at the master's gated post, the
  committed rhythm's flows and doors byte-untouched, zero core.
- Lens(es): the changed-next-decision unit (the reader of the year's
  tale sees the craft's lines beside the reckoning; the designer reads
  the seam's silence at the cap — the walled consumer's own face); the
  boundary lens (the feed walled three ways — the honest residue, the
  walls' falsifiers pinned here); the disable-test lens (the burn post
  ablated: the wood piles to the coppice's cap and the mint goes
  silent — the perturbation SAFE, the committed loops untouched).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480, the SEGMENTED year protocol — lab-3's own law: the
  one-wait whole protocol defers the beats to the final tick, the
  segmented waits drain them yearly, the honest annual band) walking
  the player to the crofts (the scene-LOD beat walk's observation
  law); the lint-level wall probes (the consume grammar, the
  bloom-mint guard).
- Oracle: the event log scans (the flows' outcomes, the converted
  events' legs, the caps' silences), the projection reads, the tale
  render, the fingerprint + the both-arms strip compare.
- Falsifier: a corpus byte shifting outside the documented env header
  (a corpus price); the burn post firing in the committed day-scale
  band; the wood crossing the coppice's cap; the committed four flows'
  events moving (the rhythm's bytes); a bloom-minting recipe landing
  (the freightvol double-mint).
- Expected evidence: the census pins; the twin's exact laws (the
  seam's two mints then silence — the ore at its cap; every burn's
  legs; the charcoal's monotone climb; the withhold's climb
  unchanged); the disable arm's bounded pile; the walls' lint
  refusals; the T1 double-run byte-identical.
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED at the measured band (seed 42: the twin + the
  disable arm + the wall probes), the honest residues carried in the
  pack's own notes (the charcoal's uncapped accumulation — the fire
  trap's own deepening; the beam's off-region terminus; the feed's
  walls).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from core.packlint.helpers import PackError
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

CROFTS = "loc_crofts"
MASTER = "npc_smelter_01"
SOURCE_EVENT = "account_sourced"
CONVERT_EVENT = "account_converted"

#: The yard's two bounded yields (ironcycle's own declarations).
COPPICE_CAP = 8
SEAM_CAP = 10

#: The twin's segmented steps: the player walks to the crofts (the
#: scene-LOD beat walk's observation law — the master's post rolls at
#: the beats of the zone he stands in), then ONE WAIT PER MACRO YEAR
#: (the SEGMENTED protocol, lab-3's own measured law: the one-wait
#: whole protocol defers every beat intent to the final tick — the
#: deferred-realize discharge — while the year-segmented waits drain
#: them yearly; the craft's annual rhythm the honest measured band).
CRAFT_STEPS = [
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": CROFTS},
] + [{"intent": "wait", "ticks": 480} for _ in range(5)]


# -- the twin helpers (the freightvol family's own form) ------------------------


def _twin(
    tmp_path: Path, name: str, *, armed: bool = True, drop_post: bool = False
) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the
    sub-year law (market 40, fair 120, seasons 120 — every entry < the
    year). The ablated twin is the COMPLETE ablation (the freightvol
    form, the post going with the door — an urgency entry naming a
    removed action is dead data, the admission lint's own refusal).
    The `drop_post` arm is the DISABLE test's own form: the burn POST
    alone removed (the door stays lawful — the player may still fire
    the craft; only the autonomous driver is gone)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    if drop_post:
        rules["urgencies"]["entries"] = [
            e for e in rules["urgencies"]["entries"]
            if (e.get("intent") or {}).get("kind") != "burn_the_stacks"
        ]
    if not armed:
        removed = {
            a["intent"] for a in json.loads(
                (target / "actions.json").read_text(encoding="utf-8")
            )["actions"] if "account" in a
        }
        entries = rules["urgencies"]["entries"]
        rules["urgencies"]["entries"] = [
            e for e in entries
            if (e.get("intent") or {}).get("kind") not in removed
        ]
        del rules["economy"]
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    if not armed:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        for category in ("locations", "npcs"):
            for record in entities[category]:
                record.pop("accounts", None)
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2), encoding="utf-8"
        )
        actions = json.loads(
            (target / "actions.json").read_text(encoding="utf-8")
        )
        actions["actions"] = [
            a for a in actions["actions"] if "account" not in a
        ]
        (target / "actions.json").write_text(
            json.dumps(actions, indent=2), encoding="utf-8"
        )
        templates = json.loads(
            (target / "templates.json").read_text(encoding="utf-8")
        )
        templates.pop("account_kinds", None)
        templates.pop("flow_glosses", None)
        (target / "templates.json").write_text(
            json.dumps(templates, indent=2), encoding="utf-8"
        )
    return target


def _run_pack(
    pack_dir: Path, tmp_path: Path, log_name: str, seed: int, steps: list
) -> tuple[list[EventRecord], Simulator, object]:
    pack = load_pack(pack_dir)
    log = tmp_path / log_name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript({
        "name": log_name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, sim, result


def _run_script(
    tmp_path: Path, log_name: str, seed: int, script_path: Path
) -> tuple[list[EventRecord], object]:
    log = tmp_path / log_name
    script = load_playscript(script_path)
    pack = load_pack(PACK_DIR)
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events, pack


# -- (1) the armed census ---------------------------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the three
    working kinds (all seeded EMPTY — the weighing aftermath band),
    the two bounded sources (the capacities declared — the hills' own
    bounds), the recipe (the cut fired to the stacks), the door (the
    convert form binding the recipe, the input-leg solvency gate the
    lint's own law), the post (the master's, the material's arrival
    the pacing), the template line + the glosses + the story-critical
    listing (the tale's own surfaces)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    # the kinds — the production's input ledger beside the committed six
    assert economy["accounts"] == [
        "coin", "bloom", "paper", "floodpaper", "step", "notch",
        "wood", "ore", "charcoal",
    ]
    crofts = next(
        loc for loc in pack.entities["locations"] if loc["id"] == CROFTS
    )
    # all three seeded EMPTY — the genesis the weighing aftermath
    assert crofts["accounts"] == {
        "bloom": 4, "coin": 0, "wood": 0, "ore": 0, "charcoal": 0,
    }
    # the two bounded sources — the capacities the hills' own bounds
    assert [
        (f["id"], f["kind"], f["to"], f["amount"], f["capacity"])
        for f in economy["flows"]
        if f["id"] in ("the_coppice_grows", "the_seam_yields")
    ] == [
        ("the_coppice_grows", "wood", CROFTS, 2, COPPICE_CAP),
        ("the_seam_yields", "ore", CROFTS, 5, SEAM_CAP),
    ]
    # the recipe — the cut fired to the stacks, conservation per kind
    assert economy["recipes"] == [{
        "id": "the_burn",
        "inputs": [{"holder": CROFTS, "kind": "wood", "amount": 2}],
        "outputs": [{"holder": CROFTS, "kind": "charcoal", "amount": 2}],
    }]
    # the door — the convert form, the recipe bound, the input gate
    door = next(
        a for a in pack.data["actions.json"]["actions"]
        if a["intent"] == "burn_the_stacks"
    )
    assert door["account"] == {"verb": "convert", "recipe": "the_burn"}
    assert door["events"]["success"] == CONVERT_EVENT
    assert {"holder": CROFTS, "test": "account_at_least", "kind": "wood",
            "value": 2} in door["requires"]
    # the post — the master's, certain at the beat, the material gated
    post = next(
        e for e in pack.rules["urgencies"]["entries"]
        if (e.get("intent") or {}).get("kind") == "burn_the_stacks"
    )
    assert post["npc"] == MASTER and post["probability_per_beat"] == 100
    assert post["intent"]["target"] == CROFTS
    assert post["requires"] == [
        {"holder": CROFTS, "test": "account_at_least",
         "kind": "wood", "value": 2},
    ]
    # the read surfaces — the craft's own lines and glosses
    assert pack.templates["events"][CONVERT_EVENT] == (
        "{actor} fires the year's cut at {target}: {input_0_amount} "
        "{input_0_kind} becomes {output_0_amount} {output_0_kind}."
    )
    assert pack.templates["account_kinds"]["wood"] == (
        "cut timber in the crofts' yard — the coppice's yearly yield, "
        "the hills' own gift to the burn"
    )
    assert "the_coppice_grows" in pack.templates["flow_glosses"]
    assert "the_seam_yields" in pack.templates["flow_glosses"]
    assert pack.templates["knows"]["the_burn_set"] == (
        "the year's cut fired — the crews' craft done under the "
        "master's rule, the stacks built against the smelt's year"
    )
    # the tale's story listing carries the craft's line (the
    # account_sourced law's own family — the year's story beats)
    assert CONVERT_EVENT in pack.rules["importance"]["story_critical_events"]


# -- (2) the zero corpus price ----------------------------------------------------


def test_the_committed_corpus_pays_nothing(tmp_path: Path) -> None:
    """The zero-corpus-price law BY CONSTRUCTION: the flows ride the
    macro year (518400 — beyond the day-scale smoke script's horizon)
    and the post's requires fail in-band (the wood seeds EMPTY) — the
    committed corpus's event stream byte-identical, the burn NEVER
    firing in the day-scale band. The header's env pin (the python
    meta, the documented family caveat) rides OUTSIDE the stream — the
    stream compare the honest instrument that holds on any env."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(load_pack(PACK_DIR), script["seed"], log, SCHEMA,
                    commit="0000000")
    sim.run_playscript(script)
    sim.close()
    fresh = log.read_bytes()
    # the event stream (everything after the header line) — identical
    assert fresh.split(b"\n", 1)[1] == golden.split(b"\n", 1)[1]
    # the burn never fires in the committed day-scale band
    _, events = read_log(log, SCHEMA)
    assert not [
        e for e in events
        if e.type in (CONVERT_EVENT,) or (
            e.type == SOURCE_EVENT and e.outcome.get("flow") in (
                "the_coppice_grows", "the_seam_yields",
            )
        )
    ]
    # the yard's stocks stand EMPTY through the whole band — the
    # genesis aftermath holding (the posts' requires fail softly)
    assert sim.projection[CROFTS]["account.wood"] == 0
    assert sim.projection[CROFTS]["account.ore"] == 0
    assert sim.projection[CROFTS]["account.charcoal"] == 0
    sim.close()


# -- (3) the twin: the craft runs itself ------------------------------------------


def test_the_twin_runs_the_craft(tmp_path: Path) -> None:
    """The world's own year, measured at the segmented band: every
    crossing carries the committed four + the yard's yields, the SEAM
    mints exactly TWICE then goes SILENT (the ore at its cap 10 — the
    every-miss law measured, the walled consumer's own face), every
    BURN's legs exact (the wood drained two, the charcoal built two —
    conservation per recipe per kind), the charcoal climbing monotonely
    (the fire trap's own deepening), the wood NEVER crossing the
    coppice's cap (the craft keeps the yard below the bound), and the
    committed rhythm UNTOUCHED beside it all (the withhold's +2 every
    crossing, the coin funds' exact reckonings)."""
    events, sim, _result = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "craft.jsonl", 42, CRAFT_STEPS,
    )
    # the seam: exactly two mints, then the every-miss silence at the cap
    ore = [
        (e.t, e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events
        if e.type == SOURCE_EVENT
        and e.outcome["flow"] == "the_seam_yields"
    ]
    assert ore == [(480, 0, 5), (960, 5, SEAM_CAP)]
    # the burns: every leg exact, the actor the master, the recipe bound
    burns = [e for e in events if e.type == CONVERT_EVENT]
    assert burns, "the craft must fire at the segmented band"
    for burn in burns:
        assert burn.actor == MASTER
        assert burn.outcome["recipe"] == "the_burn"
        # the exact conservation pair: two wood out, two charcoal in
        wood_leg, coal_leg = burn.state_changes
        assert wood_leg.entity == coal_leg.entity == CROFTS
        assert wood_leg.prop == "account.wood"
        assert coal_leg.prop == "account.charcoal"
        assert wood_leg.from_ >= 2 and wood_leg.to_ == wood_leg.from_ - 2
        assert coal_leg.to_ == coal_leg.from_ + 2
        # the master's own year-craft record rides the event
        assert burn.knowledge and all(
            k.knows == "the_burn_set" for k in burn.knowledge
        )
    # the charcoal: monotone, +2 per burn (the trap deepening)
    coal_levels = [e.state_changes[1].to_ for e in burns]
    assert coal_levels == sorted(coal_levels)
    assert len(set(coal_levels)) == len(coal_levels)
    # the wood NEVER crosses the coppice's cap — the craft keeps it low
    assert all(
        e.state_changes[0].to_ <= 4
        for e in events
        if e.type == SOURCE_EVENT and e.outcome["flow"] == "the_coppice_grows"
    )
    # the committed rhythm UNTOUCHED: the withhold +2 every crossing
    banks = [
        (e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events
        if e.type == SOURCE_EVENT and e.outcome["flow"] == "the_withhold_banks"
    ]
    assert banks[0] == (4, 6)
    assert all(b[1] == b[0] + 2 for b in banks)
    # the coin funds' reckonings unchanged — the kinds never cross
    coin = [
        (e.outcome["flow"], e.state_changes[0].entity,
         e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events
        if e.type == SOURCE_EVENT and e.outcome["kind"] == "coin"
    ][:6]
    assert coin == [
        ("the_toll_nets", "npc_weirkeeper_01", 2, 4),
        ("the_guild_collects", "loc_malby", 40, 44),
        ("the_bloom_nets", MASTER, 3, 6),
        ("the_toll_nets", "npc_weirkeeper_01", 4, 6),
        ("the_guild_collects", "loc_malby", 44, 48),
        ("the_bloom_nets", MASTER, 6, 9),
    ]
    sim.close()


def test_the_tale_carries_the_crafts_line(tmp_path: Path) -> None:
    """The reader's surface, measured at the observed band (the player
    at the crofts — the scene-LOD law: the master's post fires where
    the world is watched; the committed calendar script never reaches
    the crofts, the burn's line absent from THAT tale by the same
    law): the year's tale carries the craft's own lines — the yard's
    two yields beside the committed reckoning lines (the world-scale
    half, firing at every crossing regardless), the burn's line with
    the kind glosses riding (rs-2's boundary — the meaning on every
    account line)."""
    events, sim, _result = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "year.jsonl", 42, CRAFT_STEPS,
    )
    pack = load_pack(_twin(tmp_path, "armed_reread"))
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "comes by 2 cut timber in the crofts' yard — the coppice's"
        " yearly yield, the hills' own gift to the burn at the year's"
        " reckoning — the hills' yearly cut — the coppice gives its"
        " two timber to the yard, the burn's own feed." in tale
    )
    assert (
        "comes by 5 ironstone weathered from the seam — the smelt's"
        " raw feed, the yard's waiting iron at the year's reckoning"
        " — the seam weathers loose its ironstone — five to the"
        " smelt's yard, the hills' own iron." in tale
    )
    assert (
        "Garrick fires the year's cut at the smelt crofts: 2 cut"
        " timber in the crofts' yard — the coppice's yearly yield,"
        " the hills' own gift to the burn becomes 2 the stacks'"
        " charcoal — the crews' craft, the smelt's fire, the crofts'"
        " own making." in tale
    )
    sim.close()


# -- (4) the disable test: the perturbation safety -------------------------------


def test_the_disable_arm_is_perturbation_safe(tmp_path: Path) -> None:
    """The doctrine's own probe (WORLD_AUTHORING §8): the burn POST
    removed — the wood PILES to the coppice's cap and the mint goes
    SILENT (the every-miss form, the bounded world's honest face),
    NOTHING CRASHES (the soft-gated form's own law — an unconditional
    eat flow would have died at the loud floor; the gated post only
    goes quiet), the committed loops UNTOUCHED (the heap still climbs
    every crossing), and the DOOR stays lawful (the craft still
    player-scalable — only the autonomous driver gone)."""
    steps = [
        {"intent": "move", "target": "loc_keep"},
        {"intent": "move", "target": CROFTS},
    ] + [{"intent": "wait", "ticks": 480} for _ in range(6)]
    events, sim, _result = _run_pack(
        _twin(tmp_path, "no_post", drop_post=True), tmp_path,
        "nopost.jsonl", 42, steps,
    )
    # the wood: four mints to the cap, then the SILENCE
    mints = [
        (e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events
        if e.type == SOURCE_EVENT
        and e.outcome["flow"] == "the_coppice_grows"
    ]
    assert mints == [(0, 2), (2, 4), (4, 6), (6, COPPICE_CAP)]
    # the ore: two mints to its cap, then the seam's silence
    ore = [
        (e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events
        if e.type == SOURCE_EVENT
        and e.outcome["flow"] == "the_seam_yields"
    ]
    assert ore == [(0, 5), (5, SEAM_CAP)]
    # no burn ever fires — the craft silent, NO CRASH anywhere
    assert not [e for e in events if e.type == CONVERT_EVENT]
    # the committed rhythm untouched: the heap climbs every crossing
    banks = [
        e for e in events
        if e.type == SOURCE_EVENT
        and e.outcome["flow"] == "the_withhold_banks"
    ]
    assert len(banks) >= 6
    assert sim.projection[CROFTS]["account.bloom"] == 4 + 2 * len(banks)
    # the yard's honest standing: the caps held, the stacks never built
    assert sim.projection[CROFTS]["account.wood"] == COPPICE_CAP
    assert sim.projection[CROFTS]["account.ore"] == SEAM_CAP
    assert sim.projection[CROFTS]["account.charcoal"] == 0
    sim.close()


# -- (5) the walls: the row's measured findings -----------------------------------


def test_the_consume_grammar_wall_is_real(tmp_path: Path) -> None:
    """Wall (1), measured at the lint: the consume verb's closed form
    carries NO endpoint keys — a crafted drain-with-holder door is
    REFUSED at load (the actor-side grammar the iter-273 wall's own
    consume form; the smelt's feed over the crofts' stocks not
    authorable as pack data — the finding recorded, never routed)."""
    target = _twin(tmp_path, "wall_consume")
    actions = json.loads(
        (target / "actions.json").read_text(encoding="utf-8")
    )
    actions["actions"].append({
        "intent": "feed_the_smelt",
        "label": "feed the smelt",
        "resolver": "account",
        "ticks": 2,
        "events": {"success": "account_consumed"},
        "requires": [
            {"holder": CROFTS, "test": "account_at_least",
             "kind": "charcoal", "value": 2},
        ],
        "account": {"verb": "consume", "kind": "charcoal",
                    "amount": 2, "holder": CROFTS},
        "notes": "the crafted wall probe — the holder key is not in the"
                 " closed vocabulary",
    })
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    with pytest.raises(PackError, match="unknown keys.*holder"):
        load_pack(target)


def test_the_bloom_mint_guard_holds() -> None:
    """Wall (3), pinned as the pack's own law: NO recipe's output kind
    is bloom — the banking flow OWNS the heap's mint (the freightvol
    pin's own guard; a smelt recipe minting bloom would double-mint the
    pinned climb, the wall recorded in the pack's notes, never
    silently resolved)."""
    pack = load_pack(PACK_DIR)
    for recipe in pack.rules["economy"].get("recipes", ()):
        for leg in recipe.get("outputs", ()):
            assert leg["kind"] != "bloom", (
                "a bloom-minting recipe double-mints the withhold's"
                " ledger — the freightvol law (iter-187's pinned"
                " climb), never re-seated by a recipe"
            )
    # the heap's ONLY declared writer stays the banking flow
    assert [
        f for f in pack.rules["economy"]["flows"]
        if f["kind"] == "bloom"
    ] == [
        {"id": "the_withhold_banks", "verb": "source", "kind": "bloom",
         "to": CROFTS, "amount": 2, "every": 1},
    ]


# -- (6) INV-2: the craft draws nothing -------------------------------------------


def test_the_fingerprint_never_sees_the_craft(tmp_path: Path) -> None:
    """INV-2's both-arms proof, the ironcycle form: the fingerprints
    EQUAL across all arms (the post's rolls ride their own isolated
    streams, the craft's door processing draws nothing substantive)
    and the event lists IDENTICAL up to the craft's first door tick
    — the queue's own arithmetic beyond it (the post's intents join
    the NPC_REACTION band; the later intents' sub-orders shift by the
    craft's processing) the door-participation residue, the honest
    measured boundary: the freightvol strip law's world-scale form
    held for FLOWS alone (draw-free drafts, no queue); a DOOR-side
    post carries the queue's own cost — recorded here, the account
    family alone carrying the row's own events."""
    armed_events, _sim, armed = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "a.jsonl", 42, CRAFT_STEPS,
    )
    ablated_events, _sim2, ablated = _run_pack(
        _twin(tmp_path, "ablated", armed=False), tmp_path, "u.jsonl", 42,
        CRAFT_STEPS,
    )
    # INV-2's substantive law: the craft draws NOTHING from the canon
    assert armed.fingerprint == ablated.fingerprint
    # the prefix law: identical up to the craft's first door tick
    burns = [e for e in armed_events if e.type == CONVERT_EVENT]
    assert burns, "the craft must fire at the segmented band"
    first_burn = min(e.t for e in burns)

    def prefix(es: list) -> list:
        return [
            (e.t, e.type) for e in es
            if e.type not in (SOURCE_EVENT, CONVERT_EVENT)
            and e.t < first_burn
        ]

    assert prefix(armed_events) == prefix(ablated_events)
    # the door itself stays lawful in the drop-post arm — only the
    # autonomous driver gone (the disable test's own law below)
    nopost_events, _sim3, nopost = _run_pack(
        _twin(tmp_path, "no_post", drop_post=True), tmp_path, "n.jsonl",
        42, CRAFT_STEPS,
    )
    assert armed.fingerprint == nopost.fingerprint
    assert not [e for e in nopost_events if e.type == CONVERT_EVENT]


def test_the_twin_is_deterministic(tmp_path: Path) -> None:
    """The T1 law at the twin's own band: same seed + steps +
    environment, byte-identical logs — the craft's annual cycle a
    deterministic world rhythm, never a clock."""
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42,
            CRAFT_STEPS,
        )
    first = (tmp_path / "det_a.jsonl").read_bytes()
    second = (tmp_path / "det_b.jsonl").read_bytes()
    assert first == second
