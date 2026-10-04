"""lab-2 — the Tier A synthetic fixture's laws (the owner's Atomic World
Lab agent pack v1.5, its 02 §12 the smallest-world acceptance target; the
TASKS lab-2 row). The pack IS the deliverable: `content/farstead_pack` —
one settlement, four sources + regrowth, one workshop, one road, twelve
adults in three households, four roles — through the SAME admission lint
as every committed pack, zero core change.

The laws these tests pin (each one a measured finding of the fixture's
own development, not a aspiration):

1. THE ADMISSION GATE — the pack lints green (the single gate; the
   doctor's health inventory rides it).
2. THE TIER A SHAPE — 02 §12's counts, as data: 1 road + 1 settlement
   (the green carries storage + exchange) + 4 sources + 1 workshop;
   10-20 adults (12 + the player); 2-4 households (3); 3-4 roles (4);
   small material stocks on declared accounts.
3. THE PLAYER-ABSENT LAW + T1 — the runner's own shape over this pack:
   the player authors the anchor move and ONE wait; same seed twice →
   byte-identical logs (the same-environment law).
4. THE MATERIAL LOOP CLOSES — over a short horizon every L1 edge is
   live: a haul (source → store), a bench delivery (store → workshop),
   a forge (rack → store), a ration draw (store → keeper), a meal
   (the consume sink) and the reply (the witnesses' fatigue eased).
   The 03 §14 minimal-success shape: repeated cycle + persistent
   consequence + downstream consumer — the FIRST test-flip of the
   province canary (the ecology families are no longer zero).
5. CONSERVATION — read-side, over the same log: for every kind,
   initial + minted == final + consumed (02 §5 made executable; the
   flows' mints against the meals' sink, the stocks' remainder).
6. THE ANCHOR PAIR (the LOD datum) — the same seed and horizon, two
   anchors: the square-anchor world runs the material cycle, the
   road-anchor world is the frozen diorama (the sources regrow
   untended, the store untouched). The player-relative scene LOD is
   the gate on autonomous life — measured, not asserted in prose.
7. THE REMOVABLE SET (the per-pack law) — `minus:urgencies` and
   `minus:on_action` both lint AND run clean for THIS pack (the
   province's own verdicts differ — the re-measured, never-inherited
   law; the ablation arm's foundation).
8. THE DEFERRED-REALIZE LAW — under the one-wait protocol every
   autonomous intent discharges at the wait's end (temp-1/D-236 at
   whole-horizon scale): the hauls exist but their every tick sits in
   the horizon's final window. The mid-wait log is the scheduled
   machinery alone — the protocol's own measured shape, the input for
   the segmented-wait row the report names.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.pack import load_pack  # noqa: E402

PACK = REPO / "content" / "farstead_pack"
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
RUNNER = REPO / "scripts" / "labrunner.py"
#: the macro year (the engine's standing shape: 360 days of 1440 ticks)
YEAR = 518_400


def _run(
    tmp: Path, *, years: int, seed: int = 42, anchor: str | None = None,
    arm: str = "baseline",
) -> tuple[Path, list]:
    """One labrunner run over the fixture (the committed protocol; the
    logs land in the pytest tmp dir — zero repo-side runtime residue)."""
    out = tmp / "out"
    cmd = [
        sys.executable, str(RUNNER), "--pack", str(PACK),
        "--years", str(years), "--seeds", str(seed),
        "--arm", arm, "--out", str(out), "--tag", "test",
    ]
    if anchor is not None:
        cmd += ["--anchor", anchor]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert "T1 byte-identity: BROKEN" not in proc.stdout
    # KI#112: the log identity is per-(seed, anchor, horizon, arm,
    # protocol) — the full tuple joins the stem (two battery sessions
    # collided on prefixes: the road pair first, then the 10y/100y
    # pair); the default anchor is the pack's own player position
    resolved_anchor = "loc_road" if anchor is None else anchor
    log = out / (
        f"lab_{seed}_{resolved_anchor}_{years}y_{arm.replace(':', '_')}.jsonl"
    )
    _, events = read_log(log, SCHEMA)
    return log, events


# -- 1: the admission gate ------------------------------------------------------


def test_the_pack_lints_green() -> None:
    """The single admission gate over the Lab's own fixture — the same
    lint every committed pack passes, zero core change (INV-3's
    substance: a pack requires zero engine edits)."""
    pack = load_pack(PACK)
    assert pack.name_version == "farstead_pack@0.1"


def test_the_urgency_table_holds_the_round_laws() -> None:
    """The two structural laws the fixture's development measured, now
    pinned as data invariants: every (npc, intent-kind) pair unique (the
    one-goal-per-verb law — the engine's content-addressed roll streams)
    and every (intent, requires) pair unique across NPCs (AP-11's clone
    law). The haunt model + the direct haul are the honest shapes these
    laws force; the pack carries no move entry at all."""
    rules = json.loads((PACK / "rules.json").read_text(encoding="utf-8"))
    entries = rules["urgencies"]["entries"]
    per_npc = Counter((e["npc"], e["intent"]["kind"]) for e in entries)
    assert set(per_npc.values()) == {1}, per_npc
    pairs = Counter(
        (json.dumps(e["intent"], sort_keys=True), json.dumps(e.get("requires", []), sort_keys=True))
        for e in entries
    )
    assert set(pairs.values()) == {1}, pairs
    assert all(e["intent"]["kind"] != "move" for e in entries)


# -- 2: the Tier A shape --------------------------------------------------------


def test_the_tier_a_shape() -> None:
    """02 §12's smallest-world acceptance target, as pack data: one
    settlement (the green carries the storage and the exchange), four
    sources, one workshop, one road, 10-20 adults in 2-4 households,
    3-4 roles, small stocks on declared accounts."""
    pack = load_pack(PACK)
    entities = pack.entities
    ids = {loc["id"] for loc in entities["locations"]}
    assert len(entities["locations"]) == 7  # road + green + 4 sources + workshop
    assert {"loc_road", "loc_square", "loc_bank", "loc_copse",
            "loc_outcrop", "loc_spring", "loc_workshop"} == ids
    adults = [n for n in entities["npcs"] if not n.get("is_player")]
    assert 10 <= len(adults) <= 20  # the Tier A band (12 here)
    assert len(entities["groups"]) in (2, 3, 4)  # the households (3)
    roles = {r.split(" —")[0].strip() for r in (n["role"] for n in adults)}
    assert 3 <= len(roles) <= 4  # forager / cutter / miner / smith
    # the store and the workshop carry the declared stocks (small, finite)
    square = next(
        loc for loc in entities["locations"] if loc["id"] == "loc_square"
    )
    workshop = next(
        loc for loc in entities["locations"] if loc["id"] == "loc_workshop"
    )
    assert set(square["accounts"]) == {"food", "wood", "ore", "water", "tool"}
    assert workshop["accounts"]["tool"] == 6  # the finite rack
    # the sources: finite stocks + the regrowth flows in the economy block
    economy = pack.rules["economy"]
    assert len(economy["flows"]) == 4
    assert {f["to"] for f in economy["flows"]} == {
        "loc_bank", "loc_copse", "loc_outcrop", "loc_spring"
    }


# -- 3: the player-absent law + T1 ----------------------------------------------


def test_player_absent_and_replay_identity(tmp_path: Path) -> None:
    """The lab-1 protocol over the fixture: the player authors the anchor
    move and ONE wait — nothing else, ever — and the same seed twice is
    byte-identical (the F1/T1 falsifier, the same-environment law)."""
    log1, events = _run(tmp_path / "a", years=2, anchor="loc_square")
    pack = load_pack(PACK)
    player = pack.player_id()
    player_events = [e for e in events if e.actor == player]
    kinds = Counter(e.type for e in player_events)
    assert kinds == {"move": 1, "wait": 1}, kinds
    log2, _ = _run(tmp_path / "b", years=2, anchor="loc_square")
    assert log1.read_bytes() == log2.read_bytes()


# -- 4 + 5: the loop closes and conserves ---------------------------------------


def test_the_material_loop_closes(tmp_path: Path) -> None:
    """Every L1 edge live over one short run (the 03 §14 shape: repeated
    cycle + persistent consequence + downstream consumer) — the first
    test-flip of the province canary: the ecology-carrying families are
    no longer zero."""
    _, events = _run(tmp_path, years=4, anchor="loc_square")
    by_actor = Counter(
        e.actor for e in events if e.type == "account_settled"
    )
    # the four source hauls (source -> store), the bench deliveries
    # (store -> workshop), the forge (rack -> store), the ration draws
    for npc in ("npc_ashen_elder", "npc_ashen_son", "npc_bourne_elder",
                "npc_bourne_mate", "npc_crome_mate", "npc_crome_elder",
                "npc_ashen_mate"):
        assert by_actor[npc] >= 1, (npc, by_actor)
    meals = [e for e in events if e.type == "account_consumed"]
    assert len(meals) >= 2  # the sink (the meal + the pail)
    replies = [e for e in events if e.type == "meal_eased"]
    assert replies and all(
        len(r.state_changes) >= 2 for r in replies
    )  # the downstream consumer: the witnesses' fatigue eased


def test_material_conservation_holds(tmp_path: Path) -> None:
    """02 §5 as an executable read: for every kind, initial + minted ==
    final + consumed — the flows' environmental mints against the meals'
    sink, the stocks' remainder exact (no unexplained creation or
    deletion anywhere in the ledger)."""
    pack = load_pack(PACK)
    _, events = _run(tmp_path, years=4, anchor="loc_square")
    initial = initial_projection(pack.entities)
    final = fold(events, initial)

    def total(state: dict, kind: str) -> int:
        return sum(
            props[f"account.{kind}"] for props in state.values()
            if isinstance(props.get(f"account.{kind}"), int)
        )

    for kind in pack.rules["economy"]["accounts"]:
        minted = sum(
            e.outcome["amount"] for e in events
            if e.type == "account_sourced" and e.outcome.get("kind") == kind
        )
        consumed = sum(
            e.outcome["amount"] for e in events
            if e.type == "account_consumed" and e.outcome.get("kind") == kind
        )
        assert total(initial, kind) + minted == total(final, kind) + consumed, kind


# -- 6: the anchor pair (the LOD datum) ------------------------------------------


def test_the_anchor_pair_measures_the_lod(tmp_path: Path) -> None:
    """The same seed, the same horizon, two anchors: anchored at the
    green the material cycle runs (the star is active-or-warm); anchored
    at the road the world is a frozen diorama (the sources regrow
    untended, the store untouched). The player-relative scene LOD is the
    gate on autonomous life — measured as a count, not asserted in
    prose (the pack's 03 §3 fence, the Stage J input)."""
    _, square = _run(tmp_path / "sq", years=2, anchor="loc_square")
    _, road = _run(tmp_path / "rd", years=2)  # the pack's own position: the road

    def material(events: list) -> int:
        return sum(
            1 for e in events
            if e.type in ("account_settled", "account_consumed")
        )

    assert material(square) >= 20  # the living world's cycle
    assert material(road) == 0  # the frozen diorama: the flows alone
    # the boy's voice is the road-anchor world's one active life
    talks = Counter(
        e.type for e in road if e.actor == "npc_bourne_son"
    )
    assert talks.get("talk", 0) >= 1


# -- 7: the removable set (the per-pack law) -------------------------------------


def test_the_removable_set_is_measured_not_inherited(tmp_path: Path) -> None:
    """The province's own verdicts do NOT transfer: for THIS pack both
    optional blocks come clean out of the pack (the lint green, the run
    green) — the ablation arm's foundation, re-measured per pack as the
    labrunner's own law demands."""
    _, base = _run(tmp_path / "base", years=2, anchor="loc_square")
    _, no_urg = _run(
        tmp_path / "urg", years=2, anchor="loc_square", arm="minus:urgencies"
    )
    # the autonomous engine off: the material cycle dies with it (F3 —
    # the named downstream metric changes; no observed change would be
    # evidence against the mechanism)
    settles = sum(1 for e in no_urg if e.type in ("account_settled", "account_consumed"))
    assert settles == 0
    # the meal's reply off: the serve family still runs, the ease is gone
    _, no_reply = _run(
        tmp_path / "rep", years=2, anchor="loc_square", arm="minus:on_action"
    )
    assert not any(e.type == "meal_eased" for e in no_reply)
    assert any(e.type == "account_consumed" for e in no_reply)


# -- 8: the deferred-realize law --------------------------------------------------


def test_the_deferred_realize_law(tmp_path: Path) -> None:
    """Under the one-wait protocol every autonomous intent discharges at
    the wait's END (temp-1/D-236 at whole-horizon scale): the hauls are
    all real, and they are all late — no material transit fires mid-wait
    (the mid-wait log is the scheduled machinery alone). The protocol's
    own measured shape: the input for the segmented-wait row the report
    names, never a pack-side fix."""
    years = 3
    _, events = _run(tmp_path, years=years, anchor="loc_square")
    hauls = [
        e for e in events
        if e.type == "account_settled"
        and e.actor != "npc_ashen_mate"  # the keeper's draws ride the same law
    ]
    assert hauls, "the hauls must exist for the law to read"
    horizon = years * YEAR
    assert all(e.t >= horizon for e in hauls), (
        "an autonomous material transit fired mid-wait — the deferred-"
        "realize law broke (a protocol change, never a pack fix)"
    )
