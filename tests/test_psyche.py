"""agenda-1 P1 (iter-418) — the BORN personality profile: the draw's laws,
the lazy birth at the canon birth, the witness and its two ablations.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a personality profile can be GENERATED from pack data at the
  canon birth (never hand-written per NPC), and the born profile changes
  the NPC's decisions measurably — the three road travellers act under
  the declared weight table, and the same corpus goes silent when the
  born origin is absent or the table is zeroed.
- Problem: before this row the three generated travellers had no
  personality at all and therefore no behaviour (iter-416 §3: three
  travellers, zero urgency rows, `goal`/`mood` prose with no runtime
  reader); the P0 ticker was inert by construction (no profile, no drive).
- Lens: "the birth is live and the drawn numbers are the cause" → the
  born-origin perturbation + the weight-table perturbation, the profile
  and the names of ONE pack.
- Prism: BASE (the committed pack: `generated_psyche` on the three
  travellers + the declared weight table) vs NO-BORN-ORIGIN (the
  declarations AND the distribution removed — nothing is born) vs FLAT
  (the same born profiles, every modifier per-cent zeroed — the table
  says the drive does not matter).
- Scenario + corpus: the province pack, seed 42, the PC waits at the
  river road for 4000 ticks — the road traffic is anchored ON the
  runner's start road, so the group condenses at the first beat and the
  travellers' profiles are born there. No committed fixture is written:
  the witness lives in tmp twins (PACK_SPEC §8's law); the committed
  province golden's own delta is `tests/test_t1_province.py`'s pin.
- Oracle: the canonical events (type/actor/tick of the travellers'
  `look_around` attempts); the `road_musters` event's state_changes (the
  born profiles beside the born names); the drawn profile's shape.
- Observed (seed 42, measured): BASE — the drover 4 attempts, the
  carrier 1, the peddler 0, every attempt on the wait's own entry tick
  (the entry_tick law); the drawn profiles give weights 40 / 20 / 10
  (openness 85 / 67 / 11 against the `scan_the_road` modifier table).
  NO-BORN-ORIGIN — 0 attempts, 0 births. FLAT — 0 attempts, 3 births
  (the profiles are drawn; the table silences them). The drawn names are
  Thimrath / Deathnath / Trogkak in ALL THREE arms — the `name:` and
  `psyche:` families are independent (the D-079 isolation law at
  declaration granularity).
- Falsifier: NO-BORN-ORIGIN or FLAT producing an attempt (the birth or
  the table is not the cause); BASE silent (the drive is dead); the
  names differing between the arms (the families would be entangled).
- Epistemic class: measured, deterministic per seed. The READING of a
  profile (a mood/agenda line for the narrator) is P2's PROPOSAL, never
  this row's claim.
- Disposition: CONFIRMED at the measured band (seed 42).
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core.drives import drive_bar, drive_specs, drive_weight
from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.psyche import (
    EXTREME_BUDGET,
    GENERATED_PSYCHE_KEY,
    HIGH_BAND,
    LOW_BAND,
    PSYCHE_PROP,
    PsycheError,
    materialize_psyche,
)
from core.rng import RngBank, psyche_stream_name

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")
VERB = "look_around"
WAIT = 4000
STEPS: list[dict[str, Any]] = [{"intent": "wait", "ticks": WAIT}]


# -- the twin ---------------------------------------------------------------


def _twin(
    tmp_path: Path,
    name: str,
    *,
    born: bool = True,
    zero_modifiers: bool = False,
    mutate: Any = None,
) -> Path:
    """The committed pack copied into tmp and edited — never a committed
    edit (PACK_SPEC §8: the witness lives in the twin). `born=False`
    removes BOTH halves of the born origin (the declarations and the
    distribution row — the lint refuses a distribution without a
    consumer, so one cannot be removed alone); `zero_modifiers` zeroes
    every psych modifier per-cent (the table's ablation); `mutate` is the
    malformed forms' hook (raises at load, never at run)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if not born:
        for record in entities["npcs"]:
            record.pop(GENERATED_PSYCHE_KEY, None)
        rules["psyche"].pop("distributions", None)
    if zero_modifiers:
        for drive in rules["psyche"]["drives"]:
            for modifier in drive.get("modifiers", ()):
                modifier["low_pct"] = 0
                modifier["high_pct"] = 0
    if mutate is not None:
        mutate(rules, entities)
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    return target


def _run(
    pack_dir: Path, tmp_path: Path, name: str
) -> list[Any]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {
            "name": name,
            "seed": 42,
            "pack": pack.name_version,
            "steps": STEPS,
        }
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events


def _attempts(events: list[Any]) -> list[tuple[str, int]]:
    return [
        (event.actor, event.t)
        for event in events
        if event.type == VERB and event.actor in TRAVELLERS
    ]


def _muster_changes(events: list[Any], prop: str) -> list[Any]:
    return [
        change.to_
        for event in events
        if event.type == "road_musters"
        for change in event.state_changes
        if change.prop == prop
    ]


# -- the draw's laws --------------------------------------------------------


def _duck_pack(*npcs: dict[str, Any], distributions: Any = None) -> Any:
    """The unit-test pack stub: the rules' psyche block (two axes, one
    archetype, one distribution) + the npc records (duck-typed — the
    materializer never imports pack.py at runtime)."""
    psyche = {
        "axes": [
            {"id": "openness", "low": LOW_BAND, "high": HIGH_BAND},
            {"id": "conscientiousness", "low": LOW_BAND, "high": HIGH_BAND},
        ],
        "archetypes": [
            {"id": "arch", "defaults": {"openness": 50, "conscientiousness": 50}},
        ],
        "drives": [],
        "distributions": distributions if distributions is not None else [
            {
                "id": "dist",
                "archetypes": ["arch"],
                "jitter": 10,
                "extremes": EXTREME_BUDGET,
            },
        ],
    }
    records = list(npcs)
    return SimpleNamespace(
        rules={"psyche": psyche},
        entities={"npcs": records},
        entity=lambda eid: next((r for r in records if r["id"] == eid), None),
    )


def test_the_birth_is_lazy_deterministic_and_first_commit_wins() -> None:
    """The birth is ONE draw per npc on `psyche:<npc>`: the same seed
    answers the same profile, the stored axes keep the pack's declaration
    order (byte determinism), the drawn band classes survive, and a
    profile already in the folded projection is canon — skipped, never
    redrawn (the D-054 twin)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    npc = TRAVELLERS[0]
    birth = materialize_psyche(RngBank(42), pack, projection, npc)
    assert birth is not None
    assert (birth.entity, birth.prop, birth.from_) == (npc, PSYCHE_PROP, None)
    again = materialize_psyche(RngBank(42), pack, projection, npc)
    assert again == birth  # same seed, same stream, same profile
    profile = birth.to_
    assert profile["archetype"] == "the_road_wanderer"
    assert list(profile["axes"]) == [
        axis["id"] for axis in pack.rules["psyche"]["axes"]
    ]  # the pack's declaration order is the stored order
    # the archetype's own extreme keeps its band class: the wanderer's
    # conscientiousness default (28) is low-extreme, so every draw stays
    # at or below the band — the birth never turns it mid by accident
    assert profile["axes"]["conscientiousness"] <= LOW_BAND

    bank = RngBank(42)
    drawn = materialize_psyche(bank, pack, projection, npc)
    before = bank.count(psyche_stream_name(npc))
    state = {npc: {PSYCHE_PROP: drawn.to_}}
    assert materialize_psyche(bank, pack, state, npc) is None
    assert bank.count(psyche_stream_name(npc)) == before  # no redraw


def test_the_unarmed_law_is_total() -> None:
    """No declaration answers None BEFORE any stream is touched — zero
    assures, zero draws, the profile stream never even registered (the
    68a pattern; the v0.1 bytes untouched by construction)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    bank = RngBank(42)
    for npc in ("npc_smelter_01", "pc_01"):
        assert materialize_psyche(bank, pack, projection, npc) is None
    assert bank.fingerprint == 0
    with pytest.raises(KeyError):
        bank.count(psyche_stream_name("npc_smelter_01"))  # laziness is total


def test_the_drawn_profile_obeys_the_authoring_shape() -> None:
    """Every born profile passes the AUTHORED profile's own lint shape by
    construction: the profile names a declared archetype, carries EXACTLY
    the declared axes as ints 0..100, and spends at most the authoring
    budget on extremes (`live_char_guide` OCEAN) — the draw cannot author
    a profile the lint would refuse."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    psyche = pack.rules["psyche"]
    axes = {axis["id"]: axis for axis in psyche["axes"]}
    archetypes = {row["id"] for row in psyche["archetypes"]}
    for seed in range(1, 21):
        for npc in TRAVELLERS:
            birth = materialize_psyche(
                RngBank(seed), pack, projection, npc
            )
            assert set(birth.to_) == {"archetype", "axes"}
            assert birth.to_["archetype"] in archetypes
            values = birth.to_["axes"]
            assert set(values) == set(axes)
            extremes = 0
            for axis_id, value in values.items():
                assert isinstance(value, int) and not isinstance(value, bool)
                assert 0 <= value <= 100
                low = int(axes[axis_id].get("low", LOW_BAND))
                high = int(axes[axis_id].get("high", HIGH_BAND))
                if value <= low or value >= high:
                    extremes += 1
            assert 1 <= extremes <= EXTREME_BUDGET


def test_the_declarations_are_add_safe() -> None:
    """D-079's add-safety at profile granularity: one stream per npc —
    drawing npc_y's profile first shifts neither npc_x's profile nor a
    canon check draw."""
    x = {"id": "npc_x", GENERATED_PSYCHE_KEY: "dist"}
    y = {"id": "npc_y", GENERATED_PSYCHE_KEY: "dist"}
    pack = _duck_pack(x, y)
    state: dict[str, dict[str, Any]] = {"npc_x": {}, "npc_y": {}}
    alone = materialize_psyche(RngBank(42), pack, state, "npc_x")
    bank = RngBank(42)
    materialize_psyche(bank, pack, state, "npc_y")
    after = materialize_psyche(bank, pack, state, "npc_x")
    assert after == alone
    assert bank.fingerprint == 0


def test_the_post_lint_backstop_is_loud() -> None:
    """A declaration the lint would refuse cannot pass load — the runtime
    backstop raises loudly anyway (duck-typed packs, the honest path)."""
    npc = {"id": "npc_x", GENERATED_PSYCHE_KEY: "dist"}
    with pytest.raises(PsycheError, match="no row"):
        materialize_psyche(
            RngBank(42), _duck_pack(npc, distributions=[]),
            {"npc_x": {}}, "npc_x",
        )
    empty = _duck_pack(
        npc,
        distributions=[
            {"id": "dist", "archetypes": ["arch"], "jitter": 0, "extremes": 0},
        ],
    )
    empty.rules["psyche"]["archetypes"] = []
    with pytest.raises(PsycheError, match="no declared archetype"):
        materialize_psyche(RngBank(42), empty, {"npc_x": {}}, "npc_x")


# -- the ticker's read ------------------------------------------------------


def test_the_born_profiles_arm_the_ticker() -> None:
    """The projection-free parse is the AUTHORED-only memo, and since
    iter-445 it holds THREE specs in npc declaration order: Ketta
    (`the_weir_keeper`, the content arming of iter-443) and Garrick's two —
    the craft (`fire_the_year_cut`, the first authored origin, iter-429/D-281)
    and the DEBT (`see_the_debt_paid`, the payment stripe's helper carrier).
    Two of the three measures are MET at the seed (`account_at_most wood 1`
    on crofts wood 0, `account_at_most wear 1` on the stair's wear 0), so
    those bars are ZERO and the continuity law silences them; the debt's
    `account_at_least coin 16` on the smith's own 3 coin FAILS, so its bar is
    the weight (base 10 × his diligence's 150 %) — the debt is unpaid, and
    that failing bar is what the offer board reads. The projection-aware
    parse then joins the born profiles in pack order — each with the weight
    its drawn axes give it (`scan_the_road`: base 20, openness at >= 70
    doubles it, at <= 30 halves it)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    assert [(spec.npc, spec.drive) for spec in drive_specs(pack)] == [
        ("npc_weirkeeper_01", "keep_the_crossing"),
        ("npc_smelter_01", "fire_the_year_cut"),
        ("npc_smelter_01", "see_the_debt_paid"),
    ]
    for npc in TRAVELLERS:
        birth = materialize_psyche(RngBank(42), pack, projection, npc)
        projection[npc][PSYCHE_PROP] = birth.to_
    specs = drive_specs(pack, projection)
    assert [(spec.npc, spec.drive) for spec in specs] == [
        ("npc_weirkeeper_01", "keep_the_crossing"),
        ("npc_smelter_01", "fire_the_year_cut"),
        ("npc_smelter_01", "see_the_debt_paid"),
    ] + [(npc, "scan_the_road") for npc in TRAVELLERS]
    assert [spec.stream for spec in specs] == [
        "drive:npc_weirkeeper_01:keep_the_crossing",
        "drive:npc_smelter_01:fire_the_year_cut",
        "drive:npc_smelter_01:see_the_debt_paid",
    ] + [f"drive:{npc}:scan_the_road" for npc in TRAVELLERS]
    assert [drive_weight(spec, pack, projection) for spec in specs] == [
        18, 37, 15, 40, 20, 10,
    ]
    assert [drive_bar(spec, pack, projection) for spec in specs] == [
        0, 0, 15, 40, 20, 10,
    ]


# -- the witness and its two ablations --------------------------------------


def test_the_birth_is_the_switch_and_the_table_the_cause(tmp_path: Path) -> None:
    """BASE (the born origin + the declared table) produces the
    travellers' attempts; NO-BORN-ORIGIN (no declaration, no
    distribution) births nothing and produces none; FLAT (the same born
    profiles, every modifier zeroed) births the same profiles and
    produces none — the BIRTH is the switch, the TABLE is the cause. The
    names are identical in all three arms (the name and psyche families
    never read each other)."""
    base_events = _run(_twin(tmp_path, "base"), tmp_path, "base.jsonl")
    none_events = _run(
        _twin(tmp_path, "none", born=False), tmp_path, "none.jsonl"
    )
    flat_events = _run(
        _twin(tmp_path, "flat", zero_modifiers=True),
        tmp_path,
        "flat.jsonl",
    )
    base = _attempts(base_events)
    assert base, "the born profile must attempt on the horizon"
    assert {tick for _actor, tick in base} == {WAIT + 1}  # the entry_tick law
    # the measured bars: drover 40, peddler 20, carrier 10 over the same
    # beats — the drawn axis is the only difference between them
    assert Counter(actor for actor, _tick in base) == {
        "npc_drover_01": 4, "npc_carrier_01": 1,
    }
    assert _attempts(none_events) == [], (
        "no born origin must birth no profile and run no drive"
    )
    assert _attempts(flat_events) == [], (
        "the zeroed table must silence the born profile"
    )
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    assert _muster_changes(none_events, PSYCHE_PROP) == [], (
        "no born origin must birth no profile"
    )
    assert _muster_changes(base_events, PSYCHE_PROP) == [
        materialize_psyche(RngBank(42), pack, projection, npc).to_
        for npc in TRAVELLERS
    ]
    for events in (base_events, flat_events):
        births = [
            change.entity
            for event in events
            if event.type == "road_musters"
            for change in event.state_changes
            if change.prop == PSYCHE_PROP
        ]
        assert births == list(TRAVELLERS)  # one birth per member, member order
    assert (
        _muster_changes(base_events, "name")
        == _muster_changes(none_events, "name")
        == _muster_changes(flat_events, "name")
        == ["Thimrath", "Deathnath", "Trogkak"]
    )


def test_the_entity_view_skips_the_data_prop() -> None:
    """The `state` report renders SCALAR props only: the born profile is
    a data prop (a nested object), so `render_entity_view` never prints a
    Python dict repr for it — the log's own state_changes carry the birth,
    the view stays a scalar state line surface."""
    from render.chronicle import render_entity_view

    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    birth = materialize_psyche(
        RngBank(42), pack, projection, TRAVELLERS[0],
    )
    projection[TRAVELLERS[0]][PSYCHE_PROP] = birth.to_
    text = render_entity_view((), projection, pack, TRAVELLERS[0], 42)
    assert "psyche" not in text
    assert "archetype" not in text
    assert "the_road_wanderer" not in text


# -- the lint's refusals ----------------------------------------------------


def test_the_lint_refuses_the_malformed_forms(tmp_path: Path) -> None:
    """Nine dead shapes, each refused at LOAD (never a silent ignore):
    an unknown distribution key, an undeclared archetype in a
    distribution, the budget exceeded, an authored profile AND a born
    declaration on one npc, a distribution no npc consumes, an
    undeclared distribution name, a declaration on a non-condensing
    npc, a negative jitter, and a declaration left behind by the
    block's removal (the orphan origin — the complete ablation's law)."""

    def unknown_key(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["distributions"][0]["personality"] = {}

    def undeclared_archetype(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["distributions"][0]["archetypes"] = ["the_ghost"]

    def budget_exceeded(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["distributions"][0]["extremes"] = EXTREME_BUDGET + 1

    def both_origins(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record["psyche"] = {
                    "archetype": "the_road_wanderer",
                    "axes": {
                        "openness": 50, "conscientiousness": 40,
                        "extraversion": 50, "agreeableness": 50,
                        "neuroticism": 50,
                    },
                }

    def dead_distribution(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            record.pop(GENERATED_PSYCHE_KEY, None)

    def undeclared_distribution(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record[GENERATED_PSYCHE_KEY] = "no_such_distribution"

    def not_condensing(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record.pop(GENERATED_PSYCHE_KEY, None)
            if record["id"] == "npc_smelter_01":
                record[GENERATED_PSYCHE_KEY] = "road_folk"

    def negative_jitter(rules: dict[str, Any], _entities: Any) -> None:
        rules["psyche"]["distributions"][0]["jitter"] = -1

    def orphan_origin(rules: dict[str, Any], _entities: Any) -> None:
        rules.pop("psyche", None)
        # the archetype role texts name archetypes, so a psyche-less twin
        # must drop them too — otherwise the brief lint would refuse first
        # and this arm would never reach the ORPHAN-origin law it names
        # (agenda-1 P2c, iter-421).
        rules["brief"].pop("archetype_briefs", None)
        rules["brief"].pop("skeleton_note", None)

    for name, mutate in (
        ("unknown-key", unknown_key),
        ("archetype", undeclared_archetype),
        ("budget", budget_exceeded),
        ("both-origins", both_origins),
        ("dead", dead_distribution),
        ("undeclared", undeclared_distribution),
        ("condense", not_condensing),
        ("jitter", negative_jitter),
        ("orphan", orphan_origin),
    ):
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate=mutate))
