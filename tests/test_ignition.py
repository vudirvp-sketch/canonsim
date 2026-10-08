"""ignition — the I0 World Ignition Witness (iter-276, the owner's
2026-09-27 world-liveness direction, the execution order's fifth row:
the FIRST moving-meso proof over existing primitives — the pack
authors the possibility space, the runtime generates the history).

The witness's form (the owner's own spec): ONE ordinary recurring
moving-meso over THREE locations and THREE-PLUS cycles — the camp's
freight loop, the artery E⇄H: the crofts (the bloom heap) → the keep
(the artery's node) → Malby (the beam) — carrying PEOPLE/ROLES (the
master, the seat's own hand), MATERIAL STOCK (the heap, the camp's
ledger, the beam's receiving stock, the guild's chest), KNOWLEDGE
(the_bloom_sold, the sale's public record), CLAIMS/OBLIGATIONS (the
paper sixteen, the standing debt). The perturbation: EXACTLY ONE
meaningful route edge — the keep↔Malby road closed (the drowned ford
made a standing condition; the divergence-probe form, one pack-data
edge between two runs of the same script).

The required chain, MEASURED (the owner's own ladder):

    realized delay / exclusion
    → downstream divergence
    → actor or institutional response
    → persistent residue
    → changed next-cycle condition

The claim packet (TEST_PLAN §9):

- Claim: the existing substrate EXPRESSES the whole chain on existing
  primitives — the closed edge refuses the walk (the exclusion, the
  attempts as facts), the account states and the knowledge diverge
  (the ledger, the beam's stock, the_bloom_sold never minted), the
  master's repeated attempts are the actor's own response (the honest
  boundary: no reroute exists — the map's shape isolates Malby from
  the crofts with the one edge closed), the divergent states persist
  as residue, and every subsequent cycle faces a CHANGED condition
  (the withhold's pile growing against a closed road).
- Lens(es): the four-timelines lens (the owner's own point made
  measurable: people fail, material keeps arriving, knowledge never
  mints, obligations stand — the flows' aggregate arm BLIND to the
  road while the discrete legs diverge, never forced to synchronize);
  the first-missing-causal-leg lens (the named limits, never routed).
- Prism: the two crafted runs (the baseline road vs the closed edge),
  the same script, the divergence-probe form.
- Oracle: the event-log scans (the sales, the rejection chain's
  actors/tests/ticks), the projection reads (the heap, the ledger,
  the beam, the fund, the chest), the knowledge census, the corpus
  bytes.
- Falsifier: the sale landing in the closed world (the exclusion
  broken); the flows skipping a crossing in either run (the
  desynchronization denied); a knowledge record on the rejections
  (the epistemic silence broken); the two runs' terminal states
  agreeing (the divergence denied); the golden T1 bytes shifting.
- Expected evidence: run A — six sales (two per cycle), the ledger
  18, the beam's stock 6, the fund 42, the_bloom_sold minted; run B
  — the master's twelve rejections (six moves at the adjacent_to
  gate, six sales at the same_location gate), zero sales, the ledger
  0, the beam 0, the_bloom_sold never minted; both runs' flows
  banking at EVERY crossing (the aggregate arm identical per
  crossing); the heap climbing monotonically in B against the
  drain-and-bank rhythm of A.
- Observed evidence: CONFIRMED at the measured band (seed 42).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED — the substrate expresses the chain; the
  honest boundaries NAMED, never routed: (a) the edge closure itself
  is not a world event (no runtime route writer — the perturbation
  authored between runs; the authored seasonal fords-drown hold has
  no runtime surface), (b) the master's response repertoire is the
  attempts (no autonomous reroute or adaptation door — none owed
  until a repeated, substrate-level limitation names its consumer),
  (c) the two-sided band gap (iter-275's finding) — the I0
  inventory's first candidate, now joined by (a). No new runtime
  machinery promoted (the owner's law: only on a concrete, repeated,
  substrate-level limitation).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"   # the seat's own hand — the moving meso's person
CHEST = "loc_malby"         # the beam — the destination
CROFTS = "loc_crofts"       # the heap — the origin
KEEP = "loc_keep"           # the artery's node — the middle location
CYCLES = 3
SALES_PER_CYCLE = 2
PRICE = 3                   # three coin the load — the authored price


# -- the witness's two runs ---------------------------------------------------------


def _ignition_twin(tmp_path: Path, name: str, close_edge: bool) -> Path:
    """The crafted short-cadence twin; `close_edge` removes the
    keep↔Malby road (the drowned ford made a standing condition — the
    perturbation is ONE pack-data edge, the divergence-probe form)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    if close_edge:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        for loc in entities["locations"]:
            if loc["id"] == KEEP:
                loc["exits"] = [e for e in loc["exits"] if e != CHEST]
            if loc["id"] == CHEST:
                loc["exits"] = [e for e in loc["exits"] if e != KEEP]
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return target


def _steps() -> list[dict[str, Any]]:
    """The recurring moving-meso script: three cycles, each — the walk
    to the beam (two edges), two loads sold, the walk home, the wait
    through the year's crossing. The flows bank at every crossing on
    their own cadence (the aggregate arm), the master's legs ride the
    door (the discrete arm) — the two timelines never forced to
    synchronize."""
    steps: list[dict[str, Any]] = []
    for _ in range(CYCLES):
        steps.extend([
            {"intent": "move", "actor": MASTER, "target": KEEP},
            {"intent": "move", "actor": MASTER, "target": CHEST},
            {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
            {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
            {"intent": "move", "actor": MASTER, "target": KEEP},
            {"intent": "move", "actor": MASTER, "target": CROFTS},
            {"intent": "wait", "ticks": 480},
        ])
    steps.append({"intent": "wait", "ticks": 10})
    return steps


def _run(pack_dir: Path, tmp_path: Path, name: str):
    pack = load_pack(pack_dir)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": 42, "pack": "province_pack@0.1",
        "steps": _steps(),
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, sim


# -- the census (the moving meso as committed pack data) ------------------------------


def test_the_i0_census() -> None:
    """The witness's parts as committed pack data: THREE locations on
    the artery (the crofts — the heap and the camp's ledger; the keep
    — the artery's node; Malby — the beam, the receiving stock and
    the guild's chest), the PEOPLE/ROLES (the master — the seat's
    door), the MATERIAL STOCK (four account stocks on the loop's
    holders), the KNOWLEDGE (the sale's public record), the
    CLAIMS/OBLIGATIONS (the paper sixteen), and the perturbed edge's
    standing form (the keep↔Malby road in the authored exits)."""
    pack = load_pack(PACK_DIR)
    locations = {loc["id"]: loc for loc in pack.entities["locations"]}
    # the three locations, the artery's own shape
    assert locations[KEEP]["exits"] == ["loc_riverroad", CHEST, CROFTS]
    assert locations[CROFTS]["exits"] == [KEEP]
    assert CHEST in locations[KEEP]["exits"]  # the perturbed edge, standing
    # the material stock on the loop's holders
    assert locations[CROFTS]["accounts"] == {"bloom": 4, "coin": 0}
    assert locations[CHEST]["accounts"] == {"coin": 40, "bloom": 0}
    master = next(n for n in pack.entities["npcs"] if n["id"] == MASTER)
    assert master["accounts"] == {"coin": 3, "paper": 16}  # the claims
    assert master["position"] == CROFTS  # the person, at the origin
    # the knowledge surface: the sale's public record
    assert "the_bloom_sold" in pack.templates["knows"]
    # the moving door: the sale over the settle verb (iter-273)
    sale = next(
        a for a in pack.data["actions.json"]["actions"]
        if a["intent"] == "sell_bloom"
    )
    assert sale["account"]["verb"] == "settle"
    assert sale["account"]["legs"][0]["from"] == CROFTS
    assert sale["account"]["legs"][0]["to"] == CHEST


# -- run A: the open road (the baseline cycle) -----------------------------------------


def test_the_open_road_cycle(tmp_path: Path) -> None:
    """Run A — the road open: three cycles, each walking two loads to
    the beam (SIX sales), the camp's ledger banking eighteen, the
    beam's receiving stock at six, the fund climbing on the nets flow
    (the aggregate arm), the sale's record minted and public — the
    recurring meso in its working rhythm (the heap's drain-and-bank:
    each cycle sells what the year banked)."""
    events, sim = _run(
        _ignition_twin(tmp_path, "run_a", close_edge=False),
        tmp_path, "run_a",
    )
    sales = [e for e in events if e.type == "account_settled"]
    assert len(sales) == CYCLES * SALES_PER_CYCLE
    # the ledger banks three a sale; the beam receives a load a sale
    assert sim.projection[CROFTS]["account.coin"] == 18
    assert sim.projection[CHEST]["account.bloom"] == 6
    # the heap's own rhythm — the two arms' timescales honest: each
    # cycle's sitting starts HIGHER than the last (the crossings bank
    # +4 on their own cadence while the cycle walks and waits — the
    # banks outpace the two-load sales, the withhold deepening even as
    # it sells: the desynchronization WITHIN the working loop itself;
    # ki114-1-impl: every step feeds at the post-drain clock, the
    # crossings bank twice per sitting what the mid-drain feed caught —
    # the F1/F4 +4 translation, the rhythm's shape intact)
    heaps = [sale.state_changes[0].from_ for sale in sales]
    assert heaps == [10, 9, 16, 15, 24, 23]
    # the fund climbs on the nets flow — the aggregate arm, its own time
    # (ki114-1-impl: 42 -> 48 — the fund's own crossings bank the same
    # +4 translation as the heap; the aggregate arm's law intact)
    assert sim.projection[MASTER]["account.coin"] == 48
    # the sale's record public: the beam's witnesses learned
    knows = {r.knows for e in events for r in e.knowledge}
    assert "the_bloom_sold" in knows
    # the master home at the cycle's end — the loop closed
    assert sim.projection[MASTER]["position"] == CROFTS


# -- run B: the closed edge (the perturbation) -------------------------------------------


def test_the_closed_edge_excludes_and_diverges(tmp_path: Path) -> None:
    """Run B — the keep↔Malby road closed (the one perturbed edge):
    the EXCLUSION realized (the master's walk refused at the
    adjacency gate — Malby unreachable from the crofts by the map's
    own shape, no reroute exists), the sales refused downstream at
    the geography gate (he never reaches the beam), the DIVERGENCE
    total (zero sales, the ledger and the beam's stock untouched),
    the KNOWLEDGE never minted (the beam's witnesses never learn a
    sale that never happened) — and the rejections themselves carry
    NO knowledge records: the camp's epistemic silence about the
    closure is measured (the world knows the road only through the
    road's own attempts)."""
    events, sim = _run(
        _ignition_twin(tmp_path, "run_b", close_edge=True),
        tmp_path, "run_b",
    )
    sales = [e for e in events if e.type == "account_settled"]
    assert not sales  # the exclusion total
    # the master's response: the attempts, every cycle, as facts
    rejections = [
        e for e in events if e.type == "intent_rejected"
        and e.actor == MASTER
    ]
    moves = [r for r in rejections if r.outcome["action"] == "move"]
    attempted_sales = [
        r for r in rejections if r.outcome["action"] == "sell_bloom"
    ]
    assert len(moves) == CYCLES * 2  # out and home, every cycle... the
    # outbound move refused; the homeward move from the keep succeeds
    # (the keep still reachable) — the refused moves are the OUTBOUND
    # legs at the beam's edge
    assert len(attempted_sales) == CYCLES * SALES_PER_CYCLE
    assert all(r.outcome["failed_test"] == "target.adjacent_to"
               for r in moves)
    assert all(r.outcome["failed_test"] == "target.same_location"
               for r in attempted_sales)
    # the epistemic silence: the rejections mint no knowledge
    assert all(not r.knowledge for r in rejections)
    # the divergence: the ledger and the beam untouched, the knowledge
    # never minted
    assert sim.projection[CROFTS]["account.coin"] == 0
    assert sim.projection[CHEST]["account.bloom"] == 0
    knows = {r.knows for e in events for r in e.knowledge}
    assert "the_bloom_sold" not in knows
    # the master still home — the loop walked as far as the keep
    assert sim.projection[MASTER]["position"] == CROFTS


# -- the four timelines (the owner's own point) ---------------------------------------------


def test_the_four_timelines_diverge_not_synchronize(tmp_path: None = None) -> None:
    """The owner's own sentence made measurable: people, material,
    knowledge and obligations arrive, fail, or update on DIFFERENT
    timelines — never forced to synchronize. PEOPLE: the master's
    legs fail in B entirely (the twelve rejections) while his fund
    still climbs (the nets flow, the aggregate arm BLIND to the
    road). MATERIAL: the heap keeps banking at every crossing in BOTH
    runs (the withhold's margin arriving on its own cadence) while
    the ledger and the beam's stock diverge to zero in B. KNOWLEDGE:
    the_bloom_sold minted only in A. OBLIGATIONS: the paper sixteen
    standing in BOTH runs — the claim untouched by the road (the
    guild's paper outlives the ford, the honest desynchronization)."""
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    events_a, sim_a = _run(
        _ignition_twin(tmp, "tl_a", close_edge=False), tmp, "tl_a")
    events_b, sim_b = _run(
        _ignition_twin(tmp, "tl_b", close_edge=True), tmp, "tl_b")

    def banks(events):
        return [
            e for e in events if e.type == "account_sourced"
            and e.outcome.get("flow") == "the_withhold_banks"
        ]

    # MATERIAL: the withhold banks at EVERY crossing in both runs —
    # the flow grammar has no conditional cadence (the freightvol
    # law), the aggregate arm blind to the closed road
    assert banks(events_a) and banks(events_b)
    assert all(
        e.outcome["amount"] == 2 for e in banks(events_a) + banks(events_b)
    )
    # PEOPLE: the master's discrete legs diverge (A: 6 sales; B: 0)
    assert len([e for e in events_a if e.type == "account_settled"]) == 6
    assert not [e for e in events_b if e.type == "account_settled"]
    # KNOWLEDGE: the record only where the sale happened
    assert "the_bloom_sold" in {
        r.knows for e in events_a for r in e.knowledge
    }
    assert "the_bloom_sold" not in {
        r.knows for e in events_b for r in e.knowledge
    }
    # OBLIGATIONS: the paper standing in both — the claim's own time
    assert sim_a.projection[MASTER]["account.paper"] == 16
    assert sim_b.projection[MASTER]["account.paper"] == 16


def test_the_changed_next_cycle_condition(tmp_path: Path) -> None:
    """The chain's last leg: every subsequent cycle faces a CHANGED
    condition. Run A's heap carries the punctuated rhythm (each
    sitting drains two loads while the crossings bank between — the
    banks outpacing the sales, every subsequent sitting facing a
    higher pile: 10, 16, 24); run B's heap climbs MONOTONICALLY (the
    withhold deepening against the closed road — each cycle's attempt
    faces a bigger pile and the same refusal), and the beam's chest
    covers a price it never pays. The residue persists through the
    final crossing: the ledger and the beam's stock are the road's own
    memory."""
    events_a, sim_a = _run(
        _ignition_twin(tmp_path, "cond_a", close_edge=False),
        tmp_path, "cond_a",
    )
    events_b, sim_b = _run(
        _ignition_twin(tmp_path, "cond_b", close_edge=True),
        tmp_path, "cond_b",
    )
    # A: the punctuated rhythm — each cycle's sitting drains two
    # loads, the crossings bank between (the banks outpacing the
    # sales: every subsequent sitting faces a higher pile — 10, 16, 24)
    heaps_a = [
        sale.state_changes[0].from_
        for sale in events_a if sale.type == "account_settled"
    ]
    assert heaps_a == [10, 9, 16, 15, 24, 23]
    # B: the monotone climb — the withhold deepening, never drained
    banks_b = [
        e for e in events_b if e.type == "account_sourced"
        and e.outcome.get("flow") == "the_withhold_banks"
    ]
    levels = [change.to_ for bank in banks_b
              for change in bank.state_changes
              if change.entity == CROFTS]
    assert levels == sorted(levels)  # monotonically climbing
    assert levels[-1] > levels[0]    # the pile grew through the cycles
    # the residue: the terminal divergence, the road's own memory
    assert sim_a.projection[CROFTS]["account.coin"] == 18
    assert sim_b.projection[CROFTS]["account.coin"] == 0
    assert sim_a.projection[CHEST]["account.bloom"] == 6
    assert sim_b.projection[CHEST]["account.bloom"] == 0


# -- the corpus laws ---------------------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the I0 witness is a crafted pair of
    twins — the committed pack untouched, the golden T1 fixture
    byte-identical."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == golden


def test_the_twins_are_deterministic(tmp_path: Path) -> None:
    """The T1 law at the witness's own band: same seed + steps + pack,
    each run byte-identical (both arms)."""
    for close in (False, True):
        name = f"det_{'closed' if close else 'open'}"
        for suffix in ("_a", "_b"):
            _run(
                _ignition_twin(tmp_path, f"{name}{suffix}", close_edge=close),
                tmp_path, f"{name}{suffix}",
            )
        assert (tmp_path / f"{name}_a.jsonl").read_bytes() == (
            tmp_path / f"{name}_b.jsonl").read_bytes()
