"""since-1 acceptance — the re-encounter delta (CONTRACTS §3, D-180):
the per-entity encounter-epoch fold and the cards' since-segments.

The contract's minimal test set, in order:
(1) the epoch fold — meet/part/remeet boundaries exactly at the
    co-presence interval edges, both arrival directions opening epochs
    (independent re-derivation: the expected reunions below are
    hand-derived literals over the crafted event lists, never fold
    output — the blind suite's own law);
(2) the window content — apart-window changes surface, during-
    co-presence changes do not (scene_delta's own territory),
    unperceived changes stay silent (a born prop, another knower's
    records, intermediate position hops);
(3) the surface separation — the segments ride the entity cards,
    never scene_delta; the budget family applies (the fill law counts
    the whole card, the truncation marker marks drops, max_segments is
    the D-047 ranking cap);
(4) zero canon writes + zero corpus price — the fold is a pure query
    (the log file untouched), the same-seed armed/unarmed fork produces
    byte-identical logs, the committed packs land unarmed;
(5) the multi-reader parameterization — an NPC reader's delta differs
    from the PC's on the same log, the mode-B assembly carries the
    knower's own segments, and the leak law holds (another knower's
    records never render).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from brief.assembler import assemble_brief, render_brief
from brief.since import (
    HeardDelta,
    PropDelta,
    Reunion,
    ReunionFold,
    since_config,
)
from core.log import (
    EventDraft,
    EventLogWriter,
    KnowledgeRecord,
    StateChange,
    read_log,
)
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
PACK = load_pack(REPO / "content" / "province_pack")

READER = "pc_01"
KEEPER = "npc_weirkeeper_01"
SERGEANT = "npc_sergeant_01"
STEWARD = "npc_steward_01"

# the armed vocabulary (the sandbox driver's own, distilled)
SINCE_LINES: dict[str, Any] = {
    "props": [
        {"prop": "status.fatigue", "label": "fatigue"},
        {"prop": "status.grievance", "label": "grievance"},
    ],
    "templates": {
        "prop": "{label} {from}->{to}",
        "position": "last seen at {from}",
        "heard": "heard {token} ({channel}, {fidelity})",
    },
    "max_segments": 4,
}


# -- the crafted-log harness --------------------------------------------------


def craft(
    tmp_path: Path,
    changes: list[dict[str, Any]],
    name: str = "crafted.jsonl",
) -> list[Any]:
    """Write a crafted event list through the REAL writer (ids assigned,
    schema-validated, cause-chained) and return the records."""
    writer = EventLogWriter(tmp_path / name, SCHEMA)
    writer.write_header(seed=42, commit="0000000", pack="province_pack@0.1")
    records = []
    cause = None
    for spec in changes:
        draft = EventDraft(
            t=spec["t"],
            type=spec["type"],
            actor=spec["actor"],
            cause=cause,
            outcome={},
            provenance={"seed": 42},
            target=spec.get("target"),
            state_changes=[
                StateChange(*triplet) for triplet in spec.get("state_changes", ())
            ],
            knowledge=[
                KnowledgeRecord(*quad) for quad in spec.get("knowledge", ())
            ],
        )
        record = writer.append(draft)
        records.append(record)
        cause = record.id
    writer.close()
    return records


def fold_of(records: list[Any], reader: str = READER) -> ReunionFold:
    return ReunionFold(
        records, PACK, reader, props=["status.fatigue", "status.grievance"]
    )


def armed_pack(
    tmp_path: Path,
    name: str = "armed",
    since: Any = "default",
) -> Pack:
    """A committed-pack copy with the since vocabulary armed (None
    removes it — the unarmed twin; a dict sets it verbatim — the lint
    refusal tests' injection point)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "province_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if since == "default":
        rules["brief"]["present_entities"]["since_lines"] = SINCE_LINES
    elif since is not None:
        rules["brief"]["present_entities"]["since_lines"] = since
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def pe_block(text: str) -> list[str]:
    """The rendered present_entities block's body lines."""
    lines = text.splitlines()
    start = lines.index("## present_entities")
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.strip():
            body.append(line)
    return body


# the canonical crafted sequence: the reader meets the keeper at the
# stair (fatigue decays DURING co-presence 10->30), departs, the decay
# continues while apart (30->40), a grievance is born while apart (no
# perceived before — silent), the reader hears a rumor about the
# keeper, the keeper MOVES while apart (weirstair -> malby), the
# reader reunites at her new location, then one more decay fires
# during the new epoch (40->50 — never surfaces)
MEET_PART_REMEET: list[dict[str, Any]] = [
    {"t": 10, "type": "probe_move", "actor": READER, "target": "loc_weirstair",
     "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
    {"t": 20, "type": "probe_decay", "actor": "world",
     "state_changes": [(KEEPER, "status.fatigue", 10, 30)]},
    {"t": 30, "type": "probe_move", "actor": READER, "target": "loc_riverroad",
     "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
    {"t": 40, "type": "probe_decay", "actor": "world",
     "state_changes": [(KEEPER, "status.fatigue", 30, 40)]},
    {"t": 41, "type": "probe_birth", "actor": "world",
     "state_changes": [(KEEPER, "status.grievance", None, 5)]},
    {"t": 50, "type": "probe_talk", "actor": "npc_smelter_01",
     "knowledge": [(READER, "told", "partial", f"{KEEPER}_flooded_the_stair", 50)]},
    {"t": 51, "type": "probe_talk", "actor": "npc_smelter_01",
     "knowledge": [("npc_steward_01", "told", "partial", f"{KEEPER}_lied", 51)]},
    {"t": 55, "type": "probe_move", "actor": KEEPER, "target": "loc_malby",
     "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_malby")]},
    {"t": 60, "type": "probe_move", "actor": READER, "target": "loc_malby",
     "state_changes": [(READER, "position", "loc_riverroad", "loc_malby")]},
    {"t": 70, "type": "probe_decay", "actor": "world",
     "state_changes": [(KEEPER, "status.fatigue", 40, 50)]},
]


# -- (1) the epoch fold -------------------------------------------------------


def test_remeet_boundaries_at_the_co_presence_edges(tmp_path: Path) -> None:
    """Hand-derived expectation over MEET_PART_REMEET: the reader and
    the keeper are together over events [t10, t30), apart [t30, t60),
    together again from t60 — so the reunion compares the state before
    the t30 departure (fatigue 30 — the t20 decay happened DURING
    co-presence and is baked into the end view) against the state at
    the t60 reunion (fatigue 40, position loc_malby), and carries the
    apart-born record."""
    records = craft(tmp_path, MEET_PART_REMEET)
    reunion = fold_of(records).reunion(KEEPER)
    assert reunion == Reunion(
        props=(PropDelta("status.fatigue", 30, 40),),
        position=("loc_weirstair", "loc_malby"),
        heard=(HeardDelta(f"{KEEPER}_flooded_the_stair", "told", "partial", 50),),
    )


def test_a_first_meeting_has_no_reunion(tmp_path: Path) -> None:
    records = craft(tmp_path, MEET_PART_REMEET)
    fold = fold_of(records)
    # the sergeant stands at malby the whole log: the reader's first
    # epoch with him opens at t60 — no previous epoch, no delta
    assert fold.reunion(SERGEANT) is None
    # the reader never met the smelter at crofts at all
    assert fold.reunion("npc_smelter_01") is None
    # the reader's own self-pair never breaks co-presence
    assert fold.reunion(READER) is None


def test_the_scene_location_rides_the_readers_intervals(
    tmp_path: Path,
) -> None:
    """The scene card's entity is the location: its epochs are the
    reader's own intervals AT it. The reader visits the stair (the
    weir_water claim born during the visit), leaves, the claim flips
    while away, and the return opens the LOCATION's reunion."""
    records = craft(tmp_path, [
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 15, "type": "probe_claim", "actor": "world",
         "state_changes": [("loc_weirstair", "weir_water", None, True)]},
        {"t": 20, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
        {"t": 30, "type": "probe_claim", "actor": "world",
         "state_changes": [("loc_weirstair", "weir_water", True, False)]},
        {"t": 40, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
    ])
    fold = ReunionFold(records, PACK, READER, props=["weir_water"])
    assert fold.reunion("loc_weirstair") == Reunion(
        props=(PropDelta("weir_water", True, False),),
        position=None,
        heard=(),
    )


def test_both_arrival_directions_open_epochs(tmp_path: Path) -> None:
    """Direction A — the reader arrives at the entity's location (the
    t60 arrival in MEET_PART_REMEET, proven above); direction B — the
    entity arrives at the reader's location. The sergeant comes to the
    riverroad twice; the second arrival opens the reunion whose apart
    window holds the t30 fatigue decay."""
    records = craft(tmp_path, [
        # direction B first contact: the sergeant arrives at riverroad
        {"t": 10, "type": "probe_move", "actor": SERGEANT,
         "target": "loc_riverroad",
         "state_changes": [
             (SERGEANT, "position", "loc_malby", "loc_riverroad"),
             ("pay_tin_01", "position", "loc_malby", "loc_riverroad"),
         ]},
        # he leaves with the tin: co-presence breaks for both
        {"t": 20, "type": "probe_move", "actor": SERGEANT,
         "target": "loc_keep",
         "state_changes": [
             (SERGEANT, "position", "loc_riverroad", "loc_keep"),
             ("pay_tin_01", "position", "loc_riverroad", "loc_keep"),
         ]},
        # his fatigue decays while apart (the pack seeds 10)
        {"t": 30, "type": "probe_decay", "actor": "world",
         "state_changes": [(SERGEANT, "status.fatigue", 10, 15)]},
        # he returns to the reader's location: direction B again
        {"t": 40, "type": "probe_move", "actor": SERGEANT,
         "target": "loc_riverroad",
         "state_changes": [
             (SERGEANT, "position", "loc_keep", "loc_riverroad"),
             ("pay_tin_01", "position", "loc_keep", "loc_riverroad"),
         ]},
    ])
    fold = fold_of(records)
    assert fold.reunion(SERGEANT) == Reunion(
        props=(PropDelta("status.fatigue", 10, 15),),
        position=None,  # riverroad at both boundaries — unmoved
        heard=(),
    )
    # the tin rode the sergeant's moves: its epoch reopened too (its
    # only modeled surface is silent — a born prop has no before)
    assert fold.reunion("pay_tin_01") == Reunion(props=(), position=None, heard=())


def test_the_carried_item_closure_breaks_when_carried_off(
    tmp_path: Path,
) -> None:
    """D1's item law, under the engine's own position contract (a
    carried item's position == its carrier's, `movement_changes` the
    single owner): carried by a present non-item the lamp stays
    co-present; carried OFF it breaks; carried back it reopens; dropped
    at the reader's feet (carrier released at the reader's location)
    it stays co-present."""
    records = craft(tmp_path, [
        # the steward walks to riverroad (his pack home is thornmill)
        {"t": 5, "type": "probe_move", "actor": STEWARD,
         "target": "loc_riverroad",
         "state_changes": [
             (STEWARD, "position", "loc_thornmill", "loc_riverroad"),
         ]},
        # he picks the lamp up: still co-present (carried by present)
        {"t": 10, "type": "probe_take", "actor": STEWARD,
         "target": "tallow_lamp_01",
         "state_changes": [("tallow_lamp_01", "carrier", None, STEWARD)]},
        # a modeled surface is born while still co-present (baked in)
        {"t": 15, "type": "probe_birth", "actor": "world",
         "state_changes": [("tallow_lamp_01", "status.grievance", None, 3)]},
        # he carries it away (the mover's law: the item travels with
        # him): the closure breaks for the lamp
        {"t": 20, "type": "probe_move", "actor": STEWARD,
         "target": "loc_thornmill",
         "state_changes": [
             (STEWARD, "position", "loc_riverroad", "loc_thornmill"),
             ("tallow_lamp_01", "position", "loc_riverroad", "loc_thornmill"),
         ]},
        # he brings it back: the lamp's epoch reopens (empty reunion —
        # the grievance was born during co-presence, nothing changed)
        {"t": 30, "type": "probe_move", "actor": STEWARD,
         "target": "loc_riverroad",
         "state_changes": [
             (STEWARD, "position", "loc_thornmill", "loc_riverroad"),
             ("tallow_lamp_01", "position", "loc_thornmill", "loc_riverroad"),
         ]},
        # he drops it at the reader's feet: still co-present (position)
        {"t": 40, "type": "probe_drop", "actor": STEWARD,
         "target": "loc_riverroad",
         "state_changes": [("tallow_lamp_01", "carrier", STEWARD, None)]},
    ])
    fold = ReunionFold(
        records, PACK, READER, props=["status.fatigue", "status.grievance"]
    )
    assert fold.reunion("tallow_lamp_01") == Reunion(
        props=(), position=None, heard=()
    )


# -- (2) the window content ---------------------------------------------------


def test_apart_window_changes_surface_co_presence_changes_do_not(
    tmp_path: Path,
) -> None:
    records = craft(tmp_path, MEET_PART_REMEET)
    reunion = fold_of(records).reunion(KEEPER)
    # t20 (10->30, during epoch 1) and t70 (40->50, during epoch 2)
    # never surface; only the apart-window t40 (30->40) does
    assert [delta.prop for delta in reunion.props] == ["status.fatigue"]
    assert (reunion.props[0].from_, reunion.props[0].to_) == (30, 40)


def test_unperceived_changes_stay_silent(tmp_path: Path) -> None:
    records = craft(tmp_path, MEET_PART_REMEET)
    reunion = fold_of(records).reunion(KEEPER)
    # the t41 grievance birth: the reader never knew a before-value
    assert "status.grievance" not in [d.prop for d in reunion.props]
    # the t51 record belongs to the steward, not the reader
    assert "lied" not in [h.token for h in reunion.heard]


def test_intermediate_position_hops_never_render(tmp_path: Path) -> None:
    """The keeper hops weirstair -> crofts -> malby while apart: the
    reader compares only the endpoints (where we parted vs here); the
    crofts leg is invisible (D3 — never raw state)."""
    records = craft(tmp_path, [
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 20, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
        {"t": 30, "type": "probe_move", "actor": KEEPER,
         "target": "loc_crofts",
         "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_crofts")]},
        {"t": 40, "type": "probe_move", "actor": KEEPER,
         "target": "loc_malby",
         "state_changes": [(KEEPER, "position", "loc_crofts", "loc_malby")]},
        {"t": 50, "type": "probe_move", "actor": READER,
         "target": "loc_malby",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_malby")]},
    ])
    reunion = fold_of(records).reunion(KEEPER)
    assert reunion is not None
    assert reunion.position == ("loc_weirstair", "loc_malby")
    # the crofts leg is invisible: only the endpoints the reader
    # perceived ever render (D3 — never raw state)
    assert reunion.position[0] != "loc_crofts"
    assert reunion.position[1] != "loc_crofts"


def test_the_boundary_events_own_records_never_ride_the_window(
    tmp_path: Path,
) -> None:
    """The break and reunion events' own records are the boundary
    sightings (the beat window's territory): the departure sighting and
    the arrival snapshot never render as since-segments."""
    records = craft(tmp_path, [
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 20, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")],
         "knowledge": [(READER, "saw", "exact", f"{KEEPER}_left_toward_x", 20)]},
        {"t": 30, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")],
         "knowledge": [(READER, "saw", "exact", f"{KEEPER}_present", 30)]},
    ])
    reunion = fold_of(records).reunion(KEEPER)
    assert reunion is not None
    assert reunion.heard == ()


# -- (3) the surface separation + the budgets --------------------------------


def test_segments_ride_the_cards_never_scene_delta(tmp_path: Path) -> None:
    pack = armed_pack(tmp_path)
    records = craft(tmp_path, MEET_PART_REMEET)
    text = render_brief(assemble_brief(records, pack))
    keeper_line = next(
        line for line in pe_block(text) if line.startswith(f"- {KEEPER}")
    )
    assert "since=" in keeper_line
    assert "fatigue 30->40" in keeper_line
    assert "last seen at loc_weirstair" in keeper_line
    assert "flooded_the_stair" in keeper_line
    # the scene_delta block never carries since content
    lines = text.splitlines()
    start = lines.index("## scene_delta")
    body = []
    for line in lines[start + 1:]:
        if line.startswith("## ") or not line.strip():
            break
        body.append(line)
    assert all("since=" not in line for line in body)


def test_the_scene_card_carries_its_own_segment(tmp_path: Path) -> None:
    """The location's since-segment rides the scene line (the row's
    '+ the scene card'): weir_water flipped while the reader was away."""
    records = craft(tmp_path, [
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 15, "type": "probe_claim", "actor": "world",
         "state_changes": [("loc_weirstair", "weir_water", None, True)]},
        {"t": 20, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
        {"t": 30, "type": "probe_claim", "actor": "world",
         "state_changes": [("loc_weirstair", "weir_water", True, False)]},
        {"t": 40, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
    ])
    pack = armed_pack(tmp_path, since={
        "props": [{"prop": "weir_water", "label": "weir"}],
        "templates": {"prop": "{label} {from}->{to}"},
        "max_segments": 2,
    })
    text = render_brief(assemble_brief(records, pack))
    scene_line = next(
        line for line in pe_block(text) if line.startswith("- scene ")
    )
    assert "since=" in scene_line
    assert "weir true->false" in scene_line


def test_max_segments_is_the_ranking_cap(tmp_path: Path) -> None:
    """Beyond-cap segments render nothing (the D-047 law) — the tail
    drops silently, never into the truncation marker."""
    pack = armed_pack(tmp_path, since={
        "props": [
            {"prop": "status.fatigue", "label": "fatigue"},
            {"prop": "status.grievance", "label": "grievance"},
        ],
        "templates": {
            "prop": "{label} {from}->{to}",
            "position": "last seen at {from}",
            "heard": "heard {token}",
        },
        "max_segments": 2,
    })
    records = craft(tmp_path, MEET_PART_REMEET)
    text = render_brief(assemble_brief(records, pack))
    keeper_line = next(
        line for line in pe_block(text) if line.startswith(f"- {KEEPER}")
    )
    # position first, then the fatigue delta — the heard tail is capped
    assert "last seen at loc_weirstair" in keeper_line
    assert "fatigue 30->40" in keeper_line
    assert "flooded_the_stair" not in keeper_line


def test_the_fill_law_counts_the_whole_card(tmp_path: Path) -> None:
    """The since-segments ride the card line atomically: a budget too
    small for the fat card drops the WHOLE line with the truncation
    marker (never a silent drop, never a dangling since-only line)."""
    armed_pack(tmp_path, name="tiny", since=SINCE_LINES)
    rules = json.loads(
        (tmp_path / "tiny" / "rules.json").read_text(encoding="utf-8")
    )
    rules["brief"]["blocks"]["present_entities"] = {"soft": 1, "hard": 2}
    (tmp_path / "tiny" / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    tiny = load_pack(tmp_path / "tiny")
    records = craft(tmp_path, MEET_PART_REMEET)
    text = render_brief(assemble_brief(records, tiny))
    pe = pe_block(text)
    assert not any(KEEPER in line for line in pe)  # the card dropped whole
    assert any(  # the marker: the drop is never silent
        line.startswith("[truncated:") for line in pe
    )
    assert not any("since=" in line for line in pe)  # no dangling tail


# -- (4) zero canon writes + zero corpus price --------------------------------


def test_the_fold_never_touches_the_log_bytes(tmp_path: Path) -> None:
    records = craft(tmp_path, MEET_PART_REMEET)
    log_path = tmp_path / "crafted.jsonl"
    before = log_path.read_bytes()
    fold_of(records).reunion(KEEPER)
    pack = armed_pack(tmp_path)
    render_brief(assemble_brief(records, pack))
    assert log_path.read_bytes() == before


def test_same_seed_armed_and_unarmed_logs_byte_identical(
    tmp_path: Path,
) -> None:
    """The §9 fork's zero-price arm: the vocabulary is read-side — the
    same playscript over the armed variant and the committed pack
    produces byte-identical canon (the province smoke corpus)."""
    steps = json.loads(
        (REPO / "tests" / "playscripts" / "province_smoke.json").read_text(
            encoding="utf-8"
        )
    )["steps"]
    logs = []
    for name, pack in (("unarmed", PACK), ("armed", armed_pack(tmp_path))):
        log = tmp_path / f"{name}.jsonl"
        sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
        sim.run_playscript({
            "name": "fork", "seed": 42,
            "pack": "province_pack@0.1", "steps": steps,
        })
        sim.close()
        logs.append(log.read_bytes())
    assert logs[0] == logs[1]


def test_the_committed_packs_land_unarmed() -> None:
    for name in ("tavern_pack", "road_pack", "province_pack"):
        assert since_config(load_pack(REPO / "content" / name)) is None
    # the committed golden log's brief carries no since segment
    golden = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
    tavern = load_pack(REPO / "content" / "tavern_pack")
    _header, events = read_log(golden, SCHEMA)
    text = render_brief(assemble_brief(events, tavern))
    assert "since=" not in text


# -- (5) the multi-reader parameterization -----------------------------------


def test_an_npc_readers_delta_differs_from_the_pcs(tmp_path: Path) -> None:
    """The same log, two readers: the sergeant stands at malby the whole
    time — his epochs with the keeper are hers at malby, the reader's
    are hers at the stair; the apart windows differ and so do the
    reunions (the knower boundary honored)."""
    records = craft(tmp_path, [
        # the reader's epoch with the keeper (the stair)
        {"t": 5, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
        # the keeper visits malby: the sergeant's FIRST epoch (no reunion)
        {"t": 15, "type": "probe_move", "actor": KEEPER,
         "target": "loc_malby",
         "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_malby")]},
        # she returns to the stair: the sergeant's epoch closes (fatigue 10)
        {"t": 20, "type": "probe_move", "actor": KEEPER,
         "target": "loc_weirstair",
         "state_changes": [(KEEPER, "position", "loc_malby", "loc_weirstair")]},
        # her fatigue decays at the stair: apart from BOTH readers
        {"t": 30, "type": "probe_decay", "actor": "world",
         "state_changes": [(KEEPER, "status.fatigue", 10, 25)]},
        # the SERGEANT hears a rumor about her: HIS record, his alone
        {"t": 40, "type": "probe_talk", "actor": READER,
         "knowledge": [(SERGEANT, "told", "partial",
                        f"{KEEPER}_swore_at_the_toll", 40)]},
        # she returns to malby: the sergeant's reunion
        {"t": 50, "type": "probe_move", "actor": KEEPER,
         "target": "loc_malby",
         "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_malby")]},
        # the reader follows to malby: his reunion
        {"t": 60, "type": "probe_move", "actor": READER,
         "target": "loc_malby",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_malby")]},
    ])
    # the reader's reunion: fatigue 10->25, the position transfer
    # (they parted at the stair), no records (the toll rumor is the
    # sergeant's, never the reader's)
    assert fold_of(records, READER).reunion(KEEPER) == Reunion(
        props=(PropDelta("status.fatigue", 10, 25),),
        position=("loc_weirstair", "loc_malby"),
        heard=(),
    )
    # the sergeant's reunion: no position transfer (malby at both his
    # boundaries) but HIS OWN heard record — different knowledge, the
    # same log (the knower boundary honored)
    assert fold_of(records, SERGEANT).reunion(KEEPER) == Reunion(
        props=(PropDelta("status.fatigue", 10, 25),),
        position=None,
        heard=(HeardDelta(f"{KEEPER}_swore_at_the_toll", "told", "partial", 40),),
    )


def test_mode_b_assembly_carries_the_knower_own_segments(
    tmp_path: Path,
) -> None:
    """The §3.9 amendment executable: the same armed log assembles the
    sergeant's brief — his cards carry HIS since-segments (the leak law:
    the reader's apart-window record never renders for him)."""
    records = craft(tmp_path, [
        # the reader's epoch with the keeper (the stair)
        {"t": 5, "type": "probe_move", "actor": READER,
         "target": "loc_weirstair",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_weirstair")]},
        {"t": 10, "type": "probe_move", "actor": READER,
         "target": "loc_riverroad",
         "state_changes": [(READER, "position", "loc_weirstair", "loc_riverroad")]},
        # the keeper visits malby (the sergeant's first epoch), leaves
        {"t": 15, "type": "probe_move", "actor": KEEPER,
         "target": "loc_malby",
         "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_malby")]},
        {"t": 20, "type": "probe_move", "actor": KEEPER,
         "target": "loc_weirstair",
         "state_changes": [(KEEPER, "position", "loc_malby", "loc_weirstair")]},
        {"t": 30, "type": "probe_decay", "actor": "world",
         "state_changes": [(KEEPER, "status.fatigue", 10, 25)]},
        # the READER holds this record about the keeper (apart-born) —
        # the sergeant must never see it (the leak law)
        {"t": 40, "type": "probe_talk", "actor": "npc_smelter_01",
         "knowledge": [(READER, "told", "partial",
                        f"{KEEPER}_flooded_the_stair", 40)]},
        # the keeper returns to malby (the sergeant's reunion)
        {"t": 50, "type": "probe_move", "actor": KEEPER,
         "target": "loc_malby",
         "state_changes": [(KEEPER, "position", "loc_weirstair", "loc_malby")]},
        # the reader follows (his reunion, at the log's end)
        {"t": 60, "type": "probe_move", "actor": READER,
         "target": "loc_malby",
         "state_changes": [(READER, "position", "loc_riverroad", "loc_malby")]},
    ])
    pack = armed_pack(tmp_path)
    mode_a = render_brief(assemble_brief(records, pack))
    mode_b = render_brief(
        assemble_brief(records, pack, knower=SERGEANT)
    )
    # mode A (the reader, now at malby): his reunion with the keeper
    a_line = next(
        line for line in pe_block(mode_a) if line.startswith(f"- {KEEPER}")
    )
    assert "fatigue 10->25" in a_line
    assert "last seen at loc_weirstair" in a_line
    assert "flooded_the_stair" in a_line  # HIS apart-born record
    # mode B (the sergeant, at malby): his reunion — the same fatigue
    # window, no position transfer (malby at both his boundaries), and
    # never the reader's record (the leak law)
    b_line = next(
        line for line in pe_block(mode_b) if line.startswith(f"- {KEEPER}")
    )
    assert "fatigue 10->25" in b_line
    assert "last seen at" not in b_line
    assert "flooded_the_stair" not in b_line
    assert "heard" not in b_line


# -- determinism + the unarmed landing ---------------------------------------


def test_repeated_assembly_is_byte_identical(tmp_path: Path) -> None:
    pack = armed_pack(tmp_path)
    records = craft(tmp_path, MEET_PART_REMEET)
    first = render_brief(assemble_brief(records, pack))
    second = render_brief(assemble_brief(records, pack))
    assert first == second


def test_the_unarmed_twin_renders_no_segments(tmp_path: Path) -> None:
    records = craft(tmp_path, MEET_PART_REMEET)
    text = render_brief(assemble_brief(records, PACK))
    assert "since=" not in text


# -- the lint (the pack's own declaration is the arming) ---------------------


def _lint(tmp_path: Path, since: Any) -> None:
    with pytest.raises(PackError):
        armed_pack(tmp_path, name="refused", since=since)


def test_lint_unknown_key_refused(tmp_path: Path) -> None:
    _lint(tmp_path, {**SINCE_LINES, "unknown_key": 1})


def test_lint_zero_cap_refused(tmp_path: Path) -> None:
    _lint(tmp_path, {**SINCE_LINES, "max_segments": 0})


def test_lint_unknown_placeholder_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["templates"]["prop"] = "{label} {from} -> {too}"
    _lint(tmp_path, broken)


def test_lint_constant_template_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["templates"]["heard"] = "a constant with no slot"
    _lint(tmp_path, broken)


def test_lint_dead_vocabulary_refused(tmp_path: Path) -> None:
    """No props, no templates: the section renders nothing — dead data."""
    _lint(tmp_path, {"max_segments": 4})


def test_lint_props_without_the_prop_template_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["templates"].pop("prop")
    _lint(tmp_path, broken)


def test_lint_position_row_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["props"].append({"prop": "position", "label": "where"})
    _lint(tmp_path, broken)


def test_lint_bogus_prop_surface_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["props"].append({"prop": "status.bogus_axis", "label": "x"})
    _lint(tmp_path, broken)


def test_lint_duplicate_prop_refused(tmp_path: Path) -> None:
    broken = json.loads(json.dumps(SINCE_LINES))
    broken["props"].append({"prop": "status.fatigue", "label": "again"})
    _lint(tmp_path, broken)


def test_lint_a_location_field_prop_is_legal(tmp_path: Path) -> None:
    """The scene card's surface: location fields / armed claim slots are
    legal since-props (weir_water is a world_formed claim slot)."""
    pack = armed_pack(tmp_path, name="locfield", since={
        "props": [{"prop": "weir_water", "label": "weir"}],
        "templates": {"prop": "{label} {from}->{to}"},
        "max_segments": 2,
    })
    assert pack is not None
