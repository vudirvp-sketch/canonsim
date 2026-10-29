"""render-conditional — the §6.5 embodiment row's LAST leg (iter-265,
the owner's «можешь закрыть "рендер-условную строку (последняя нога
§6.5)"» call over the iter-263 verdict's ONE remaining owner-gated
row): the tale contradiction on the ashes — the calendar's market day
still reading "the stalls from the weir stair to the bank" after the
burnout took them — closed READ-SIDE, never a runtime primitive (the
iter-263 §D.1 boundary: the calendar line's consumer routes are closed
by law, C1/C2 measured twice; the honest medicine is the renderer's
own fold).

The mechanism (render/chronicle.py, zero core): the renderer's running
fold now carries each LOCATION's prop state — seeded from the pack's
declared flags + accounts (initial_projection's own location seeding,
the honest mirror) and advanced by every event's state_changes
targeting a location, tolerant last-write-wins (the renderer is a
READER, never the truth test — a foreign log renders dry; T2's replay
owns the from-checks). The event context exposes the tracked props as
DOTTED conditional keys `<location_id>.<prop>`, values raw — an
authored `{cond?...|...}` binds the world's own state: the market
line's {loc_malby.destroyed?...|...}, the day still counted (the
calendar's legibility, the surface BY LAW), the tale never
contradicting the projection.

The claim packet (TEST_PLAN §9):

- Claim: the read-side conditional closes the tale contradiction —
  the SAME log renders the standing line before the burnout and the
  ashes line after it, the render staying a pure function of
  (log, pack, seed); zero runtime change — the LOG layer is untouched
  by a template (the committed fixtures and the composition counts
  prove that layer separately).
- Lens(es): the changed-next-decision unit (a tale reader now reads
  the world's own state on the calendar line — the legibility of time
  kept, the contradiction dead); the boundary lens (read-side only —
  the calendar grammar stays closed, the location fold a reader never
  a truth test).
- Prism: the mechanism census below (the seeded flags/accounts, the
  advance on location writes, the tolerance over foreign/desynced
  writes — a scratch pack copy through the REAL load_pack, the
  iter-263 instrument's own law); the two integration arms (the
  standing market and the burned market, real Simulator runs crossing
  the SAME first market day at t=14400 — one day, two worlds).
- Oracle: the rendered tale text itself (the branch words), the
  projection reads (destroyed is / is not True), the byte-identical
  re-render.
- Falsifier: the standing prose on the ashes (the contradiction
  surviving); the ashes prose on a standing market (the fold seeing a
  burnout that never happened); the fold crashing over a foreign or
  desynced write (the reader turned truth-test).
- Expected evidence: the arms below over the seed-2 runs; the
  composition chronicle's 36 market lines all reading the ashes branch
  (the measured surface, WORLD_TESTS §9's run record).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, StateChange, read_log
from core.loop import Simulator
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

#: the market's own site (the chest at the weighbeam)
CHEST = "loc_malby"

#: the two branch texts — the falsifier is their swap (the standing
#: prose on the ashes, the ashes prose on a standing market)
STANDING = "the river market opens at Malby — the stalls from the weir stair to the bank"
ASHES = "the market day passes at Malby — the stall row burned from the weir stair to the bank"

#: the standing arm — the calendar witness's own shape (no fire in the
#: route), the long wait crossing the FIRST market day at t=14400
STANDING_STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": CHEST},
    {"intent": "wait", "ticks": 15000},
]

#: the burned arm — the §6.5 family's own route (test_marketlegs.py's
#: witness: the lamp, the keep's hearth, the walk to Malby, the
#: accepted trade, the stall row's arson with the burnout 120 ticks
#: on, the rejected re-trade on the ashes), the SAME long wait crossing
#: the SAME first market day
BURNED_STEPS: list[dict[str, Any]] = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_keep"},
    {"intent": "arson", "target": "loc_keep"},
    {"intent": "move", "target": CHEST},
    {"intent": "trade_at_market", "target": CHEST},
    {"intent": "arson", "target": CHEST},
    {"intent": "wait", "ticks": 1440},
    {"intent": "trade_at_market", "target": CHEST},
    {"intent": "move", "target": "loc_thornmill"},
    {"intent": "wait", "ticks": 15000},
]


def _run_and_render(
    tmp_path: Path, name: str, steps: list[dict[str, Any]], seed: int = 2,
) -> tuple[list[EventRecord], str]:
    """One real run + its chronicle (the seed from the log header —
    the same log always renders to the same bytes)."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    sim.close()
    header, events = read_log(log, SCHEMA)
    return events, render_chronicle(events, pack, seed=int(header["seed"]))


@pytest.fixture(scope="module")
def standing(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[list[EventRecord], str]:
    return _run_and_render(
        tmp_path_factory.mktemp("render_cond_standing"), "standing.jsonl",
        STANDING_STEPS,
    )


@pytest.fixture(scope="module")
def burned(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[list[EventRecord], str]:
    return _run_and_render(
        tmp_path_factory.mktemp("render_cond_burned"), "burned.jsonl",
        BURNED_STEPS,
    )


# -- the mechanism census (a scratch pack through the real load_pack) ---------


def _probe_pack(tmp_path: Path) -> Any:
    """A scratch copy of the province pack through the REAL load_pack
    (the iter-263 instrument's own law: the lint is part of the tool —
    a NEW probe event type is dead vocabulary the lint refuses, so the
    probe RE-VOICES one existing line instead: `wait`, the murmur
    family's own site), every location-fold claim readable through the
    public render surface."""
    pack_dir = tmp_path / "probe_pack"
    pack_dir.mkdir()
    for name in ("entities.json", "rules.json", "actions.json"):
        shutil.copy(PACK_DIR / name, pack_dir / name)
    templates = json.loads(
        (PACK_DIR / "templates.json").read_text(encoding="utf-8")
    )
    templates["events"]["wait"] = (
        "lit:{loc_malby.lit?LIT|DARK} "
        "smoke:{loc_malby.smoke?SMOKE|CLEAR} "
        "chest:{loc_malby.account.coin?CHEST|EMPTY} "
        "market:{loc_malby.destroyed?ASHES|STANDING} "
        "foreign:{loc_foreign.burned?FOREIGN|HOME}"
    )
    (pack_dir / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return load_pack(pack_dir)


def _crafted(
    event_id: str, t: int, changes: tuple[StateChange, ...] = (),
) -> EventRecord:
    """A minimal valid probe event (the scratch pack's re-voiced wait
    line) — the fold advances on EVERY event (the tale gate reads
    importance, never the fold)."""
    return EventRecord(
        id=event_id, t=t, type="wait", actor="world", cause=None,
        outcome={"probe": True}, knowledge=(), state_changes=changes,
        hooks=(), importance="high", provenance={}, target=None,
    )


def test_the_fold_seeds_the_declared_site_state(tmp_path: Path) -> None:
    """The seed — the honest mirror of initial_projection's own
    location seeding: the pack-declared flag (lit) and the pack-declared
    account level (the chest's coin) both surface as dotted conditional
    keys, raw; an undeclared prop (smoke, destroyed before any fire)
    reads falsy — the standing market's own context."""
    pack = _probe_pack(tmp_path)
    tale = render_chronicle([_crafted("e1", 1)], pack, seed=2)
    assert "lit:LIT smoke:CLEAR chest:CHEST market:STANDING foreign:HOME" in tale


def test_the_fold_advances_on_location_writes(tmp_path: Path) -> None:
    """The advance: every state_change targeting a location lands in
    the fold — the smoke flag, the chest's level (its own truthiness
    at zero) and the burnout's destroyed all read at the LATER event's
    line, and at the WRITING event's own line too (the at-tick
    inclusive law, the projection fold's own shape)."""
    pack = _probe_pack(tmp_path)
    fire = _crafted("e1", 1, changes=(
        StateChange(CHEST, "smoke", False, True),
        StateChange(CHEST, "account.coin", 40, 0),
        StateChange(CHEST, "destroyed", False, True, irreversible=True),
    ))
    tale = render_chronicle([fire, _crafted("e2", 2)], pack, seed=2)
    assert tale.count("lit:LIT smoke:SMOKE chest:EMPTY market:ASHES") == 2


def test_the_fold_is_a_reader_never_the_truth_test(tmp_path: Path) -> None:
    """The tolerance law: the renderer folds WITHOUT from-checks (T2's
    replay owns those) — a desynced `from` lands its `to` value, and a
    write to an entity the pack never declared is ignored with the
    conditional reading absent-falsy (a foreign log renders dry and
    honest, never a crash): the reader stays a reader."""
    pack = _probe_pack(tmp_path)
    foreign = _crafted("e1", 1, changes=(
        StateChange("loc_foreign", "burned", None, True),
        StateChange(CHEST, "destroyed", "garbage", True),
    ))
    tale = render_chronicle([foreign, _crafted("e2", 2)], pack, seed=2)
    assert "market:ASHES" in tale  # the `to` lands; the from is never checked
    assert "foreign:HOME" in tale  # the unknown entity never enters the fold


# -- the integration arms (one day, two worlds) --------------------------------


def test_the_standing_market_keeps_its_line(
    standing: tuple[list[EventRecord], str],
) -> None:
    """The no-leak arm: with no fire in the route the fold never sees a
    burnout — the market day renders the STANDING branch, the ashes
    prose absent, the projection honest (destroyed is not True)."""
    events, tale = standing
    markets = [e for e in events if e.type == "market_opens"]
    assert len(markets) == 1 and markets[0].t == 14400
    assert "Day 10: " + STANDING in tale
    assert ASHES not in tale
    projection = fold(events, initial_projection(load_pack(PACK_DIR).entities))
    assert projection[CHEST].get("destroyed") is not True


def test_the_burned_market_reads_the_ashes(
    burned: tuple[list[EventRecord], str],
) -> None:
    """THE row's own witness: the burnout precedes the first market day
    (the fire's 120-tick follow-up, the route's own arson), and the
    calendar line renders the ASHES branch — the same Day 10, the
    standing prose DEAD on the burned stalls (the falsifier: the
    contradiction must not survive), the day still counted (the
    calendar's legibility, the surface BY LAW)."""
    events, tale = burned
    markets = [e for e in events if e.type == "market_opens"]
    assert len(markets) == 1 and markets[0].t == 14400
    burnouts = [
        e for e in events
        if e.type == "location_burned_out" and e.target == CHEST
    ]
    assert len(burnouts) == 1 and burnouts[0].t < 14400
    assert "Day 10: " + ASHES in tale
    assert STANDING not in tale


def test_the_render_stays_a_pure_function_of_the_log(
    burned: tuple[list[EventRecord], str],
) -> None:
    """T1's own law over the conditional: a fresh render of the same
    events (a fresh fold, a fresh Engine, the same seed) is
    byte-identical — the render is a pure function of (log, pack,
    seed), the location fold stateless per pass."""
    events, tale = burned
    again = render_chronicle(events, load_pack(PACK_DIR), seed=2)
    assert again == tale
    assert render_chronicle(events, load_pack(PACK_DIR), seed=2) == again
