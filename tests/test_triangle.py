"""iter-135 acceptance — world-2 L2 slice 3, the triangle (phases.md §6,
D-130's FNV shape; TASKS world-2's wave plan, D-153/D-154): depth-6's
FIRST COMMITTED ARMING — three factions over the settlement cast's live
axes — plus the deep feud history (the cause-tree chronicle + the
wergeld claims seeding the director's buffer).

The laws pinned here:

- **The triangle is pack data** (the D-160 probe pattern at province
  scale): three group entities + three `factions` entries + one new
  status axis (`grievance`, decay 0 — the wergeld law) + three goal
  verbs (bare story beats, the attribution rows their witnesses) + the
  tale lines + the story-critical listing. ZERO core edits for the
  arming itself (the one forced core edit is KI#85's, below).
- **The player tips ratios, never script gates**: the fire family is
  the lever — the alarm spikes fear (the guild's axis), the grief
  reaction wakes grievance (the families' axis). One verb (arson),
  many roads: burning the market tips the GUILD; burning the keep
  tips the GARRISON; both fires tip the FAMILIES (the deadband: one
  woken elder reads fraction 50 at threshold 50 — silent).
- **The escalation ladder**: the guild reads fear at trigger 30 (the
  trade flinches first), the garrison at 40 (the trained bar) — the
  same axis, two thresholds, the FNV cascade.
- **The grief-wake's numeric-home law**: only the seeded elders carry
  a grievance value; the crowd hears the alarm and never wakes (the
  on_action ripple's own filter, now the alarm spike's too — KI#85).
- **The deep feud history**: events_max 5 -> 9, the third collection
  tier (exodus), the wergeld claim joins the hook draw list — the
  cause TREE lands in the log (the member chains to its nearest
  lower tier), the render is the tier clause + the year chain.
- **The corpus price**: the base script on the committed pack vs the
  factions-block-removed twin runs BYTE-IDENTICALLY (the D-108
  both-arms law: the rolls ride the isolated faction streams, zero
  events in the calm vale — the deadband is the designed rest state).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from core.factions import faction_probability
from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "content" / "province_pack"
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"

#: the committed roads (the experiment's arms — same route shape as
#: province_smoke, the fire family inserted): the market tip, the keep
#: tip (a long stay — the runner trapped by the smoke), and the total
#: war. Every leg a legal exits edge; the lamp is the carried source.
ROAD_MARKET = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 30},
    {"intent": "move", "target": "loc_riverroad"},
    {"intent": "wait", "ticks": 15},
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_malby"},
    {"intent": "arson", "target": "loc_malby"},
    {"intent": "wait", "ticks": 600},
    {"intent": "move", "target": "loc_thornmill"},
    {"intent": "wait", "ticks": 400},
]
ROAD_KEEP = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 30},
    {"intent": "move", "target": "loc_riverroad"},
    {"intent": "wait", "ticks": 15},
    {"intent": "move", "target": "loc_keep"},
    {"intent": "arson", "target": "loc_keep"},
    {"intent": "wait", "ticks": 2000},
]
ROAD_BOTH = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 30},
    {"intent": "move", "target": "loc_riverroad"},
    {"intent": "wait", "ticks": 15},
    {"intent": "move", "target": "loc_keep"},
    {"intent": "arson", "target": "loc_keep"},
    {"intent": "wait", "ticks": 600},
    {"intent": "move", "target": "loc_malby"},
    {"intent": "arson", "target": "loc_malby"},
    {"intent": "wait", "ticks": 600},
    {"intent": "move", "target": "loc_thornmill"},
    {"intent": "wait", "ticks": 900},
]


def _run(
    tmp_path: Path, name: str, steps: list[dict], seed: int,
) -> tuple[list, dict]:
    pack = load_pack(PACK_DIR)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": pack.name_version,
         "steps": steps}
    )
    sim.close()
    _header, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))
    return events, projection


def _events_of(records: list, *types: str) -> list:
    return [e for e in records if e.type in types]


# -- the committed instance ---------------------------------------------------


def test_the_triangle_is_committed_pack_data() -> None:
    """The arming's shape: three groups over the settlement cast (the
    budget's own prediction — the cast stays 10), three entries reading
    two axes at two thresholds (the ladder), the grievance axis declared
    with decay 0 (the wergeld law — a man-price once named stays
    named), the elders' seeded simmer below the bar, the grief reaction
    on the alarm family, the wergeld claim hook, and the goal verbs'
    full tale surface (template + story-critical + attribution)."""
    pack = load_pack(PACK_DIR)
    groups = {g["id"]: g for g in pack.entities["groups"]}
    assert set(groups) == {
        "grp_road_traffic", "grp_river_guild", "grp_old_families",
        "grp_garrison",
    }
    assert groups["grp_river_guild"]["members"] == [
        "npc_marketmistress_01", "npc_weirkeeper_01",
    ]
    assert groups["grp_old_families"]["members"] == [
        "npc_steward_01", "npc_smelter_01",
    ]
    assert groups["grp_garrison"]["members"] == [
        "npc_sergeant_01", "npc_corporal_01",
    ]
    assert groups["grp_river_guild"]["position"] == "loc_malby"
    assert groups["grp_old_families"]["position"] == "loc_thornmill"
    assert groups["grp_garrison"]["position"] == "loc_keep"

    entries = pack.rules["factions"]["entries"]
    by_group = {entry["group"]: entry for entry in entries}
    assert set(by_group) == {
        "grp_river_guild", "grp_old_families", "grp_garrison",
    }
    # the escalation ladder: the same fear axis read at two thresholds
    assert by_group["grp_river_guild"]["axis"] == "fear"
    assert by_group["grp_river_guild"]["trigger_value"] == 30
    assert by_group["grp_garrison"]["axis"] == "fear"
    assert by_group["grp_garrison"]["trigger_value"] == 40
    # the deep-history arm: grievance at the deliberate deadband
    assert by_group["grp_old_families"]["axis"] == "grievance"
    assert by_group["grp_old_families"]["trigger_value"] == 40
    assert by_group["grp_old_families"]["threshold"] == 50
    # the goal verbs ride the wait resolver (the bare story beat)
    assert by_group["grp_river_guild"]["intent"] == {"kind": "council"}
    assert by_group["grp_old_families"]["intent"] == {"kind": "hold_vigil"}
    assert by_group["grp_garrison"]["intent"] == {"kind": "patrol"}

    # the grievance axis: decay 0 (the wergeld law), the seeded simmer
    # below the bar
    assert pack.rules["states"]["grievance"]["decay_per_360_ticks"] == 0
    npcs = {n["id"]: n for n in pack.entities["npcs"]}
    assert npcs["npc_steward_01"]["status"]["grievance"] == 35
    assert npcs["npc_smelter_01"]["status"]["grievance"] == 30
    # the elders alone: no other entity carries a grievance home
    assert not any(
        "grievance" in n.get("status", {})
        for n in pack.entities["npcs"]
        if n["id"] not in ("npc_steward_01", "npc_smelter_01")
    )

    # the grief reaction joins the alarm family (the numeric-home law
    # filters the candidates at runtime)
    alarm_reactions = pack.rules["on_action"]["alarm_raised"]
    grief = [r for r in alarm_reactions if r["event"] == "grief_wakes"]
    assert len(grief) == 1
    assert grief[0]["state"] == {
        "prop": "status.grievance", "add": 20,
    }

    # the wergeld claim: the third story-critical hook + the draw list
    assert "garrick_wergeld_count" in pack.rules["director"]["hooks"]
    assert pack.rules["worldgen"]["chronicle"]["hooks"] == [
        "maren_feud_sweep", "wilmot_grief_ramble", "garrick_wergeld_count",
    ]
    # the goal verbs' tale surface
    for event in ("guild_councils", "wergeld_vigil", "garrison_patrols",
                  "grief_wakes"):
        assert event in pack.templates["events"]
        assert event in pack.rules["importance"]["story_critical_events"]
    for event in ("guild_councils", "wergeld_vigil", "garrison_patrols"):
        assert pack.rules["metrics"]["system_of_type"][event] == ["director"]


def test_the_bars_over_the_committed_shapes() -> None:
    """The small formula over the triangle's own numbers: one spooked
    guild post reads fraction 50 -> bar 20 (1-in-5 per beat); the
    garrison's split watch reads bar 15 (the crown answers slower); the
    families' deadband holds at fraction 50 (one woken elder) and opens
    at 100 (both elders -> bar 60)."""
    assert faction_probability([50, 0], 30, 0, 40) == 20
    assert faction_probability([50, 10], 40, 0, 30) == 15
    assert faction_probability([55, 30], 40, 50, 60) == 0  # the deadband
    assert faction_probability([55, 50], 40, 50, 60) == 60  # both elders
    assert faction_probability([], 40, 0, 30) == 0  # the vacuity law


# -- the market road: the guild councils, one elder wakes ---------------------


def test_the_market_fire_tips_the_guild(tmp_path: Path) -> None:
    """The committed experiment arm (province_feud.json, seed 53): the
    runner takes his own lamp, walks the artery, burns the market row —
    the alarm spikes Maren past the guild's bar, and the GUILD
    COUNCILS through the front door (actor = the group id, the
    faction_NNNN handle in the provenance — D-112's one-id law live at
    province scale, the census's only zero-consumer family armed)."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_feud.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / "feud.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))

    councils = _events_of(events, "guild_councils")
    assert len(councils) == 1
    assert councils[0].actor == "grp_river_guild"
    assert councils[0].provenance["cause_intent"] == "faction_0000"
    # the tip: Maren's fear crossed the guild's bar (the alarm family)
    assert projection["npc_marketmistress_01"]["status.fear"] >= 30
    # the crime chain went live too (the arson's own cascade)
    assert _events_of(events, "fire_started", "alarm_raised",
                      "location_burned_out")
    assert any(e.type == "suspicion_changed" for e in events)


def test_the_market_fire_wakes_one_elder_only(tmp_path: Path) -> None:
    """The grief reaction + the deadband on the market road: the alarm
    is heard at Thornmill (adjacent) — Wilmot's grief wakes (35 -> 55,
    the KI#85-consistent write) — but Garrick at the crofts hears
    nothing: the families read fraction 50 at threshold 50 and the
    VIGIL STAYS SILENT (the old blood moves together, by design)."""
    events, projection = _run(tmp_path, "market_elder", ROAD_MARKET, 53)
    grief = _events_of(events, "grief_wakes")
    assert len(grief) == 1
    changes = {c.entity: (c.from_, c.to_)
               for c in grief[0].state_changes}
    assert changes == {"npc_steward_01": (35, 55)}
    # the numeric-home law: the crowd never wakes (no grievance home)
    assert not any(
        c.entity == "npc_malby_crowd_01" for e in grief for c in e.state_changes
    )
    assert projection["npc_smelter_01"]["status.grievance"] == 30
    assert _events_of(events, "wergeld_vigil") == []
    # KI#85: the alarm's spike skips the crowd's absent fear home —
    # the alarm fired, Maren spiked, the crowd holds no status write
    alarm = _events_of(events, "alarm_raised")
    assert len(alarm) == 1
    spiked = {c.entity for c in alarm[0].state_changes}
    assert "npc_malby_crowd_01" not in spiked
    assert "npc_marketmistress_01" in spiked


# -- the keep road: the garrison patrols, the other elder wakes ---------------


def test_the_keep_fire_tips_the_garrison(tmp_path: Path) -> None:
    """The watch road (seed 139, the long stay at the burning keep):
    the hearth fire spikes the keep's occupant past the trained bar —
    the GARRISON PATROLS through the door (the anchor is the keep, the
    PC lingers there: the active zone rolls the walk). The crown's
    answer is the rare one by design: the split rotation reads
    fraction 50, bar 15 — the escalation ladder's honest shape."""
    events, _projection = _run(tmp_path, "keep_road", ROAD_KEEP, 139)
    patrols = _events_of(events, "garrison_patrols")
    assert len(patrols) == 1
    assert patrols[0].actor == "grp_garrison"
    assert patrols[0].provenance["cause_intent"].startswith("faction_")
    assert _events_of(events, "guild_councils") == []  # the market whole


def test_the_keep_fire_wakes_the_other_elder(tmp_path: Path) -> None:
    """The crofts hear the keep's alarm (adjacent): Garrick's grief
    wakes (30 -> 50) — the SECOND road's elder. The families still
    hold the deadband (Wilmot asleep at 35): the vigil needs both
    houses, and each fire wakes exactly one — the many roads made
    mechanical."""
    events, projection = _run(tmp_path, "keep_elder", ROAD_KEEP, 139)
    grief = _events_of(events, "grief_wakes")
    assert len(grief) == 1
    changes = {c.entity: (c.from_, c.to_)
               for c in grief[0].state_changes}
    assert changes == {"npc_smelter_01": (30, 50)}
    assert projection["npc_steward_01"]["status.grievance"] == 35
    assert _events_of(events, "wergeld_vigil") == []


# -- the total war: the vigil -------------------------------------------------


def test_both_fires_tip_the_families(tmp_path: Path) -> None:
    """The total war (seed 2, both posts burned): BOTH elders grieve
    past the bar — the fraction reads 100, the deadband opens, and the
    OLD FAMILIES HOLD THE WERGELD VIGIL at the burned mill (twice on
    this seed — the bar reads 60, both beats hit; the blood price
    spoken aloud again — the deep feud's runtime consummation, the
    claim/legitimacy first consumer)."""
    events, projection = _run(tmp_path, "both_fires", ROAD_BOTH, 2)
    vigils = _events_of(events, "wergeld_vigil")
    assert len(vigils) == 2
    assert all(v.actor == "grp_old_families" for v in vigils)
    assert all(
        v.provenance["cause_intent"].startswith("faction_")
        for v in vigils
    )
    assert projection["npc_steward_01"]["status.grievance"] >= 40
    assert projection["npc_smelter_01"]["status.grievance"] >= 40
    # both fires, both grief wakes — the two roads composed
    assert len(_events_of(events, "grief_wakes")) == 2
    assert len(_events_of(events, "fire_started")) == 2


# -- the tale -----------------------------------------------------------------


def test_the_tale_renders_the_triangle(tmp_path: Path) -> None:
    """The story-critical listing decides visibility (the tune-1
    split): the guild's line and the grief's line render in the
    chronicle with the group's display name and the anchor resolved
    through the position fold — the triangle reads as story, never as
    mechanics."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_feud.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / "tale.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    tale = render_chronicle(events, pack, script["seed"])
    assert "the river guild bars the stalls" in tale
    assert "The old grief wakes" in tale
    assert "Malby, the market town" in tale


def test_the_deep_feud_tree_renders_its_tiers() -> None:
    """The cause-tree render (the D-130 history half): the golden
    corpus's eight history lines read the tree through the tier
    clauses — the feud roots, the quarrel under them, the exodus at
    the leaves — and the drawn claim tags (the sweep, the murmur, the
    count) ride the events that seed the director's buffer."""
    pack = load_pack(PACK_DIR)
    text = GOLDEN.read_text(encoding="utf-8")
    events = [
        json.loads(line) for line in text.splitlines()
        if "schema_version" not in line
    ]
    history = [
        e for e in events
        if e["type"] == "world_history" and "year" in e["outcome"]
    ]
    assert len(history) == 8
    collections = [
        e["outcome"].get("collection") for e in history
    ]
    # the seed-42 tree: two blood-ending feud roots with quarrel and
    # exodus members, a first independent, the war chained last
    assert collections == [
        None, "feud", "quarrel", "exodus", "feud", "exodus", "exodus",
        "feud",
    ]
    # the cause chains: the members chain to their nearest lower tier,
    # the roots to the previous TOP-LEVEL event (the sagas chain —
    # never the episodes: the second root chains to the FIRST root,
    # the war to the second)
    causes = [e["cause"] for e in history]
    assert causes == [
        "ev_0000",  # the first independent -> world_formed
        "ev_0001",  # the first feud root -> the independent (last top)
        "ev_0002",  # the quarrel -> its feud root
        "ev_0003",  # the exodus -> the quarrel (nearest lower tier)
        "ev_0002",  # the second feud root -> the FIRST root (top-level)
        "ev_0005",  # the second exodus -> its feud root
        "ev_0005",  # the third exodus -> its feud root
        "ev_0005",  # the war -> the second root (the latest saga)
    ]
    # the claim tags drawn onto the tree: all three ride
    tags = {t for e in history for t in e["hooks"]}
    assert tags == {
        "maren_feud_sweep", "wilmot_grief_ramble", "garrick_wergeld_count",
    }
    # the render: the tier clauses and the years make the tree readable
    lines = render_chronicle(
        _records(GOLDEN), pack, 42,
    ).splitlines()
    joined = "\n".join(lines)
    assert "in the feud." in joined
    assert "in the quarrel." in joined
    assert "in the exodus." in joined


def _records(path: Path) -> list:
    from core.log import read_log as _read
    _header, events = _read(path, SCHEMA)
    return events


# -- the corpus price ---------------------------------------------------------


def test_the_calm_vale_is_byte_identical_without_the_entries(
    tmp_path: Path,
) -> None:
    """The D-108 both-arms law at province scale: the base script on
    the committed pack vs the factions-block-removed twin runs
    BYTE-IDENTICALLY — the rolls ride the isolated faction streams
    (zero substantive draws), and the calm vale's deadband means zero
    faction events: the arming's presence alone costs nothing (the
    census's DORMANT -> ARMED flip is data, never noise)."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
    twin_dir = tmp_path / "twin"
    shutil.copytree(PACK_DIR, twin_dir)
    rules = json.loads((twin_dir / "rules.json").read_text(encoding="utf-8"))
    del rules["factions"]
    (twin_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    twin = load_pack(twin_dir)

    log_a = tmp_path / "armed.jsonl"
    log_b = tmp_path / "unarmed.jsonl"
    pack = load_pack(PACK_DIR)
    for target, the_pack in ((log_a, pack), (log_b, twin)):
        sim = Simulator(the_pack, script["seed"], target, SCHEMA,
                        commit="0000000")
        sim.run_playscript(script)
        sim.close()
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_lod_scoping_reads_the_anchors() -> None:
    """The committed anchors scope the walks (depth-3's one-gate law):
    each faction rolls only where it is anchored — the guild at the
    market, the families at the manor, the garrison at the keep; the
    road traffic (depth-7's group) carries no faction entry and never
    walks."""
    from core.factions import faction_intents
    from core.rng import RngBank

    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    # seed the fold past the bars: everyone afraid, everyone grieving
    for npc_id in ("npc_marketmistress_01", "npc_weirkeeper_01",
                   "npc_sergeant_01", "npc_corporal_01"):
        projection[npc_id]["status.fear"] = 80
    for npc_id in ("npc_steward_01", "npc_smelter_01"):
        projection[npc_id]["status.grievance"] = 80
    # bank seed 1: all three first-draws hit their bars (deterministic)
    walked = {
        zone: sorted(i.actor for i in faction_intents(
            pack, projection, RngBank(1), locations=(zone,)
        ))
        for zone in ("loc_malby", "loc_thornmill", "loc_keep",
                     "loc_riverroad")
    }
    assert walked["loc_malby"] == ["grp_river_guild"]
    assert walked["loc_thornmill"] == ["grp_old_families"]
    assert walked["loc_keep"] == ["grp_garrison"]
    assert walked["loc_riverroad"] == []  # the traffic carries no entry
    # the one-scene law: no scoping, every entry walks
    assert sorted(i.actor for i in faction_intents(
        pack, projection, RngBank(1)
    )) == ["grp_garrison", "grp_old_families", "grp_river_guild"]
