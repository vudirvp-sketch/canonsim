"""codueflows — the co-due crossing (substrate-1's FIRST wall, iter-409).

The wall, as measured at iter-404/405: `core/economy.py::flow_drafts`
built EVERY due flow's draft against the crossing's SINGLE projection
snapshot, so two flows touching one stock at one crossing desynced the
`_commit` gate — the second draft's `from_` was stale (`expected from 2
but projection holds 4`), and the run died LOUD. The province pack
folded its year around the limit (debt-1, D-182: the gross toll splits
as two SOURCES instead of a source plus a drain), and the household's
consumptive half was refused by measurement, not by authorship.

The fix is the law this witness measures: the crossing is a SEQUENCE.
`flow_drafts` is a GENERATOR whose every draft reads the projection AT
YIELD TIME, and `core/loop.py` commits each draft before asking for the
next — KI#13's live-read law, extended from the intent door to the
aggregate family. No pack byte changes: the committed corpora stay
inert by construction (the wall's witness lives in an in-tmp twin).

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a drain co-due with a mint on the same stock at one macro
  crossing now commits as an ORDERED sequence — each event's `from_` is
  the level its predecessor just wrote — while a drain declared BEFORE
  its mint still dies LOUD at the `_commit` floor (declaration order is
  the pack's own law, never silently reordered).
- Lens(es): the arithmetic unit (the `from_`/`to_` chain, never a
  recomputed projection); the boundary lens (the loud refusal of a
  graph order that empties a stock — a refusal, not a skip).
- Prism: the crafted short-cadence twin (macro 480, the calendar inside
  the sub-year law) over the committed province pack, flows replaced by
  the two-element graph under test; plus the generator-level read law.
- Oracle: the log's own `state_changes` of `npc_weirkeeper_01.account.coin`.
- Falsifier: a stale `from_` (2 where the mint already wrote 4), a
  silently skipped drain, a negative stock landing in the log, or the
  snapshot form returning (two drafts sharing one read).
- Epistemic class: FACT at the measured band (deterministic, seed 42).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.economy import flow_drafts
from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
KETTA = "npc_weirkeeper_01"
WAIT = 1500  # three crossings at the twin's 480-tick macro year

SOURCE = "account_sourced"
CONSUME = "account_consumed"


def _twin(tmp_path: Path, name: str, flows: list[dict[str, Any]]) -> Path:
    """The crafted short-cadence twin: the committed province pack with
    the macro year shrunk to 480 ticks (the calendar scaled inside the
    sub-year law, the test_debt1 form) and the economy's flow list
    REPLACED by the graph under test. Zero bytes of the committed pack
    change — the twin is a copy."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    rules["economy"]["flows"] = flows
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    # The committed flow-gloss table names the pack's own flow ids; the
    # twin's graph is different, so the table goes with it (the gloss
    # table is OPTIONAL — an unglossed flow renders nothing, rs-4's dry
    # fallback law; a gloss for an undeclared id is dead data and the
    # lint refuses it).
    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates.pop("flow_glosses", None)
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    return target


def _run(pack_dir: Path, tmp_path: Path, name: str, seed: int = 42) -> list:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": [{"actor": KETTA, "intent": "wait", "ticks": WAIT}],
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events


def _coin_trail(events: list) -> list[tuple[int, str, Any, int, int]]:
    """The toll-taker's coin arithmetic as the LOG owns it: (t, type,
    flow id, from, to) — never a recomputed projection."""
    return [
        (e.t, e.type, e.outcome.get("flow"), ch.from_, ch.to_)
        for e in events
        for ch in e.state_changes
        if ch.entity == KETTA and ch.prop == "account.coin"
    ]


# -- (1) the crossing as a sequence ---------------------------------------------


def test_a_drain_co_due_with_a_mint_commits_in_declaration_order(
    tmp_path: Path,
) -> None:
    """The wall's closing witness: the source mints 2, the drain takes 1
    on the SAME stock at the SAME crossing — both events land, and the
    second's `from_` is the first's `to_` (the sequence, not the
    snapshot). Three crossings, six events, exact arithmetic: the
    toll-taker's coin climbs 2→4→3→5→4→6→5."""
    pack_dir = _twin(tmp_path, "codue", [
        {"id": "toll_mints", "verb": "source", "to": KETTA,
         "kind": "coin", "amount": 2},
        {"id": "year_eats", "verb": "consume", "from": KETTA,
         "kind": "coin", "amount": 1},
    ])
    trail = _coin_trail(_run(pack_dir, tmp_path, "codue.log"))

    assert trail[:6] == [
        (480, SOURCE, "toll_mints", 2, 4),
        (480, CONSUME, "year_eats", 4, 3),
        (960, SOURCE, "toll_mints", 3, 5),
        (960, CONSUME, "year_eats", 5, 4),
        (1440, SOURCE, "toll_mints", 4, 6),
        (1440, CONSUME, "year_eats", 6, 5),
    ]
    # The falsifier named in the packet: the snapshot form would have
    # built the drain against the pre-mint level (from_ 2, not 4).
    assert [entry[3] for entry in trail[:6]] == [2, 4, 3, 5, 4, 6]
    # The law holds at every crossing the run reached, not only the
    # measured three: the trail alternates mint→drain and every event's
    # `from_` IS its predecessor's `to_` (the sequence, byte-exact).
    assert len(trail) % 2 == 0
    for position, entry in enumerate(trail):
        assert entry[1] == (SOURCE if position % 2 == 0 else CONSUME)
        if position:
            assert entry[3] == trail[position - 1][4]


def test_the_declaration_order_is_the_packs_own_law(tmp_path: Path) -> None:
    """A drain declared BEFORE its mint reads the pre-mint level. The
    law now has TWO arms: the LOAD-time guard (`core/packlint/economy.py
    ::_flow_order`, iter-413 — the crossing is simulated from the seeds
    and refused before the world ever runs) and the runtime `_commit`
    floor for later crossings (`tests/test_economy.py`'s underflow
    witness). This test pins the first arm: the misordered graph cannot
    load at all."""
    pack_dir = _twin(tmp_path, "wrong_order", [
        {"id": "year_eats", "verb": "consume", "from": KETTA,
         "kind": "coin", "amount": 5},
        {"id": "toll_mints", "verb": "source", "to": KETTA,
         "kind": "coin", "amount": 2},
    ])
    from core.packlint.helpers import PackError

    with pytest.raises(PackError, match="declaration order drives"):
        load_pack(pack_dir)


# -- (2) the generator-level read law ------------------------------------------


def test_every_draft_reads_the_projection_at_yield_time() -> None:
    """The mechanism at its smallest band: two consecutive `next()`s on
    one flow stream answer different `from_` values once the projection
    between them holds the first draft's `to_` — laziness IS the live
    read, and a caller that commits in between is exactly the loop."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    assert projection[KETTA]["account.coin"] == 2

    rules = dict(pack.rules)
    economy = dict(rules["economy"])
    economy["flows"] = (
        {"id": "toll_mints", "verb": "source", "to": KETTA,
         "kind": "coin", "amount": 2},
        {"id": "year_eats", "verb": "consume", "from": KETTA,
         "kind": "coin", "amount": 1},
    )
    rules["economy"] = economy

    drafts = flow_drafts(rules, projection, 480)
    first = next(drafts)
    (change,) = first.state_changes
    assert (change.from_, change.to_) == (2, 4)

    # The caller's commit: the projection now holds the mint's result.
    projection[KETTA]["account.coin"] = change.to_
    second = next(drafts)
    (drain,) = second.state_changes
    assert (drain.from_, drain.to_) == (4, 3)
