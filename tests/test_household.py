"""household — the crossing's year measured and its larder realized
(wt-fill-1's U1, iter-404; the consuming household, iter-412).

The anchor's `ANCHOR_REGION.md` §8 row "full household economics" asked for
the household as a COUNTABLE surface (stores, labour, consumption through
one year). This witness first landed the countable half with zero pack
change and named what it refused; both walls are now addressed, and the
CONSUMPTION half is committed pack data (iter-412):

- WALL 1 — the co-due fold law — CLOSED at the engine by substrate-1's
  first unit (iter-409) and REALIZED on the anchor (iter-412). A `consume`
  FLOW on the same stock that a `source` FLOW mints at the same crossing
  used to desync the commit gate: both drafts were built against the
  crossing's single snapshot, so the drain's `from_` disagreed with the
  mint's `to_` (`core/loop.py`'s own check). `flow_drafts` is a GENERATOR
  reading the projection at each yield now, and the loop commits before
  asking for the next — the crossing is a sequence (the mechanism witness:
  `tests/test_codueflows.py`). The household's own larder is the first
  committed co-due pair (`the_garden_yields` +3 bounded at four,
  `the_hearth_eats` −2 declared after it), and the old refusal is kept as
  a LAW, inverted (`test_the_larder_cycle_commits_as_a_sequence` below).
  The second form still stands as measured: a certain beat POST over a
  consume DOOR logs `intent_rejected` noise — under the deferred-realization
  law a long wait mints every beat's intent against the pre-wait
  projection, and all but the first then refuse (FOUR rejections on a
  1500-tick twin).
- WALL 2 — no distress axis. There is no hunger/scarcity representation and
  the consume verb may never underflow (D3's floor), so "the household went
  hungry" has nowhere to sit: the committed larder eats its own ground and
  never empties. A distress surface is the OWNER'S canon call (the iter-404
  report carries it).

What IS observable at the committed band, and what this witness measures:
the household's year as a closed ARITHMETIC — the toll's net surplus at
every macro crossing climbing to the AUTHORED twelve (`ANCHOR_REGION.md`
§6.1's own fund), the punt's purchase taking it at Malby, and the flood
paper's twenty still standing behind it: ONE COIN, TWO CLAIMS as a live
trace, the order the thin surplus decides. Driven through the household's
OWN door set (`buy_punt`, `pass_paper`, `render_toll`, `settle_paper` — the
account resolver's player-scaled arm, iter-272's fills) by actor steps: an
NPC's agency is a legal playscript actor (`core/loop.py::_intent_from_step`),
so the household can be walked without the player impersonating it.

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the crossing household's year is a closed, lawfully ordered
  arithmetic over the COMMITTED surfaces — the fund reaches the authored
  twelve at the fifth crossing, the punt takes it, the paper stands — with
  zero pack change, zero core, and the canonical corpus byte-untouched.
- Lens(es): the changed-next-decision unit (which claim the surplus pays,
  and in what order); the boundary lens (the two walls above: what the
  substrate REFUSES is measured, never faked).
- Prism: the macro-year band (`province_household`, five crossings) plus the
  canonical day-scale corpus as the inertness oracle.
- Oracle: the account events' own state changes (from → to), never a
  recomputed projection; the fixture's bytes for the corpus law.
- Falsifier: a coin trail that does not reach twelve at the fifth crossing,
  a punt purchase the gate refuses at that fund, an account write to the
  flood paper, or one byte of movement in the canonical corpus refutes it.
- Epistemic class: FACT at the measured band (the deterministic half).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
KETTA = "npc_weirkeeper_01"
MALBY = "loc_malby"
TRAIL = ("loc_riverroad", "loc_keep", "loc_malby")
CROSSINGS = 5
TICK_YEAR = 518_400
TWELVE = 12
PAPER = 20


def _run_committed(tmp_path: Path, log_name: str) -> list:
    script = load_playscript(REPO / "tests" / "playscripts" / "province_household.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / log_name
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events


def _level_trail(events: list, entity: str, kind: str) -> list:
    """Every state change on `entity`'s `kind`: (t, type, from, to) — the
    log's own arithmetic, never a recomputed projection. The entity filter
    is the whole point: the world carries other holders of the same kind."""
    return [
        (e.t, e.type, ch.from_, ch.to_)
        for e in events
        for ch in e.state_changes
        if ch.entity == entity and ch.prop.endswith(kind)
    ]


# -- (1) the committed surfaces the year rides ------------------------------------


def test_the_year_rides_the_committed_door_set() -> None:
    """The arithmetic's inputs as committed pack data: the household's
    stocks, the toll's net surplus, and the four lifecycle doors that
    compete for the same coin (settle_paper's twenty, buy_punt's twelve,
    render_toll's twenty, pass_paper's inherited paper)."""
    pack = load_pack(PACK_DIR)
    ketta = next(n for n in pack.entities["npcs"] if n["id"] == KETTA)
    assert ketta["accounts"] == {
        "coin": 2, "floodpaper": PAPER, "step": 3, "stores": 0}
    toll = next(f for f in pack.rules["economy"]["flows"]
                if f["id"] == "the_toll_nets")
    assert (toll["verb"], toll["kind"], toll["to"], toll["amount"]) == (
        "source", "coin", KETTA, 2)
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    # the punt's door: twelve on the actor, the destination the market town
    punt = actions["buy_punt"]
    gates = [(c.get("kind"), c.get("value")) for c in punt["requires"]
             if c.get("test") == "account_at_least"]
    assert gates == [("coin", TWELVE)]
    assert punt["account"] == {"verb": "transfer", "kind": "coin", "amount": TWELVE}
    # the purchase is public to the co-present (the household's word)
    assert [k["knows"] for k in punt["knowledge"]["success"]] == ["the_punt_bought"]
    # the paper's doors: the fall needs the fund that covers it
    settle = actions["settle_paper"]
    assert [(c.get("kind"), c.get("value")) for c in settle["requires"]
            if c.get("test") == "account_at_least"] == [
        ("floodpaper", PAPER), ("coin", PAPER)]
    assert actions["render_toll"]["account"] == {
        "verb": "transfer", "kind": "coin", "amount": PAPER}
    assert actions["pass_paper"]["account"] == {
        "verb": "transfer", "kind": "floodpaper", "amount": PAPER}


# -- (2) the year's arithmetic ---------------------------------------------------


def test_the_coin_climbs_to_the_authored_twelve(tmp_path: Path) -> None:
    """The toll's net surplus at every crossing, measured leg by leg: the
    household's coin reaches the AUTHORED fund — twelve — at exactly the
    fifth crossing (`ANCHOR_REGION.md` §6.1's own number, the fund the
    pack's notes describe: "the punt fund's climb toward the authored
    twelve")."""
    events = _run_committed(tmp_path, "household.jsonl")
    trail = _level_trail(events, KETTA, "coin")
    mints = [(t, before, after) for t, kind, before, after in trail
             if kind == "account_sourced"]
    assert len(mints) == CROSSINGS
    assert [after - before for _t, before, after in mints] == [2] * CROSSINGS
    assert [after for _t, _b, after in mints] == [4, 6, 8, 10, TWELVE]
    assert [t for t, _b, _a in mints] == [
        TICK_YEAR * (n + 1) for n in range(CROSSINGS)]


def test_the_punt_is_bought_and_the_paper_still_stands(tmp_path: Path) -> None:
    """ONE COIN, TWO CLAIMS as a live trace: the punt's purchase takes the
    twelve at Malby's market (the household walks the committed road, one
    legal hop at a time), and the flood paper's twenty is untouched behind
    it — the order the household's thin surplus decides."""
    events = _run_committed(tmp_path, "household.jsonl")
    moves = [e.target for e in events if e.type == "move" and e.actor == KETTA]
    assert moves == list(TRAIL), "the household walks the committed road"
    punt = next(
        e for e in events
        if e.type == "account_transferred" and e.actor == KETTA
        and e.outcome.get("kind") == "coin"
    )
    assert punt.target == MALBY
    assert punt.outcome["amount"] == TWELVE
    assert [(ch.from_, ch.to_) for ch in punt.state_changes
            if ch.entity == KETTA] == [(TWELVE, 0)]
    assert not [e for e in events if e.type == "account_consumed"
                and e.outcome.get("kind") == "floodpaper"], "the paper stands"
    assert _level_trail(events, KETTA, "floodpaper") == []
    # the coin's whole trail: the toll's five mints and the one purchase,
    # nothing else — the household's year is exactly its declared flows
    # plus the one door the surplus pays
    assert [row[1] for row in _level_trail(events, KETTA, "coin")] == (
        ["account_sourced"] * CROSSINGS + ["account_transferred"])


def test_the_larder_cycle_commits_as_a_sequence(tmp_path: Path) -> None:
    """WALL 1 CLOSED, then REALIZED (substrate-1's first unit, iter-409;
    the consuming household, iter-412). The wall: a garden minting
    `stores` and a hearth draining them at the same crossing desynced the
    commit gate, so the household's consumption leg could not be pack
    data. The crossing is a SEQUENCE now (`flow_drafts` yields each draft
    after the predecessor's commit), and the household's OWN larder is the
    committed pair — the garden's three, then the hearth's two out of the
    just-minted level, at every year of the household's script."""
    events = _run_committed(tmp_path, "larder.jsonl")
    trail = _level_trail(events, KETTA, "stores")
    # the first year: the empty larder → the garden's three → the hearth's two
    assert trail[:2] == [
        (TICK_YEAR, "account_sourced", 0, 3),
        (TICK_YEAR, "account_consumed", 3, 1),
    ]
    # every year: the drain reads the minted level (never the year's
    # opening one), and the pair alternates mint→drain over the whole run
    assert len(trail) == CROSSINGS * 2
    for position, row in enumerate(trail):
        assert row[1] == ("account_sourced" if position % 2 == 0
                          else "account_consumed")
        if position:
            assert row[2] == trail[position - 1][3]
    # the larder never fills (the cap of four) and never empties (the floor)
    levels = [to for _t, _kind, _from, to in trail]
    assert max(levels) == 4 and min(levels) == 1


# -- (3) the corpus law and the fingerprint --------------------------------------


def test_the_canonical_corpus_is_untouched(tmp_path: Path) -> None:
    """INERT-FIRST (`PACK_SPEC` §9.1) with zero pack change to defend: a
    fresh day-scale run of the smoke script is byte-identical to the
    committed golden."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    Simulator(pack, script["seed"], log, SCHEMA, commit="0000000").run_playscript(script)
    fresh = log.read_bytes()
    golden = (REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl").read_bytes()
    assert fresh == golden, "the corpus price is zero — never paid silently"


def test_the_walk_is_byte_identical_and_the_fingerprints_agree(tmp_path: Path) -> None:
    """INV-2: the same script twice, the same bytes; the two arms' RngBank
    fingerprints equal."""
    script = load_playscript(REPO / "tests" / "playscripts" / "province_household.json")
    pack = load_pack(PACK_DIR)
    arms = []
    for name in ("twin_a.jsonl", "twin_b.jsonl"):
        log = tmp_path / name
        sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
        result = sim.run_playscript(script)
        arms.append((result.fingerprint, log.read_bytes()))
    assert arms[0][1] == arms[1][1]
    assert arms[0][0] == arms[1][0]
