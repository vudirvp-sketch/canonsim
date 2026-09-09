"""iter-75 acceptance — depth-2, lazy detail materialization (phase 5's
second row, TASKS/phases.md §5 — the D-096 research-intake design: seed
materialization over the D-054/ledger-OCC law with `scene:<id>:detail`
streams). Mechanics (iter-75) + the ARMING (iter-76, depth-2b — the
68b pattern): the committed pack carries the block (the tavern's two
slots + the guardroom's cot), so the unarmed arm of every A/B pin
below is the crafted v0.1 twin (the block-popped copy) or a scene
the committed arming does not list.

The laws pinned here:

- **The stream law (the D-079 family's third member)**:
  `scene:<id>:detail`, content-addressed via
  `core/rng.py::scene_detail_stream_name` (injective — location ids are
  map keys); lazily registered on first use; the closed-set tripwire
  survives for every non-family name; the ONE legal nesting is inside
  the assured substantive run scope (the family law — a scene stream
  may shadow `substantive`, never the reverse).
- **The laziness law**: the draws fire only on the first meaningful
  observation of an ARMED scene — a pack without the block (or a scene
  never observed) answers an empty tuple BEFORE touching the bank:
  zero assures, zero draws, the fingerprint and the v0.1 bytes
  untouched by construction.
- **The draw law**: one draw per pack-declared slot, pack declaration
  order, on the scene's OWN stream — canon checks and other scenes'
  details never shift (stream isolation at the address granularity;
  the within-scene slot list is one pack unit, D-079's content-landing
  protocol).
- **The first-commit-wins law**: a slot already present in the folded
  projection is SKIPPED — no redraw, no second change; re-observation
  reproduces the same detail by reading canon. `empty` is just a value:
  a materialized empty rejects later gold with no special casing.
- **The claim law (the slot_conflict mirror — the ledger's texture-OCC
  twin)**: `detail_claim` validates a declared claim against the
  committed log: `commit` (unclaimed), `no_op` (canon holds the same
  value — the idempotent duplicate), or `slot_conflict` with the cause
  chain — the LAST write on the slot, the authority the claim
  conflicts with. A written-then-emptied slot still refuses (the
  sentinel law: written is not the value).
- **The wiring law**: the materialization surface is the scene-snapshot
  resolver family — the observation event's `state_changes` carry the
  births (`StateChange(location, slot, None -> value)`, the promotion
  shape) and its outcome names them under `materialized` (present only
  when something materialized — the drifted_from law, so unarmed
  events never move); the fold rebuilds the projection from the log
  (INV-1's truth test). Since iter-76 the committed arming is live:
  the knowledge surface of the materialized detail is the event's OWN
  payload + the folded canon — ZERO new knowledge tokens (the
  observation's `knows` templates stay the pack's declared
  `scene_{location}` / `rambling_by_{actor}` — detail tokens never
  ride the knowledge records, D-108 — so the corpus claim surface
  never moves).
- **The lint laws**: the closed entry vocabulary `{slot | values}`;
  location ids must be real locations; slots unique within a location
  (a duplicate would couple stream positions); the double-claim law
  (a slot the location already models — record key or flag — can never
  birth); the one-object law (a `brief.scene_texture.unique_slots`
  overlap is a double declaration); values are unique non-empty
  strings.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core.detail import (
    COMMIT,
    NO_OP,
    SLOT_CONFLICT,
    detail_claim,
    materialize_scene_detail,
    materialized_fields,
)
from core.fold import fold, initial_projection
from core.log import EventRecord, StateChange, read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import (
    COSMETIC,
    SUBSTANTIVE,
    RngBank,
    RngError,
    scene_detail_stream_name,
)

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"

ARMED: dict[str, Any] = {
    "loc_tavern": [
        {"slot": "under_bench", "values": ["empty", "old_cloak", "purse_coins"]},
        {"slot": "behind_barrel", "values": ["empty", "lost_ring"]},
    ]
}

# The player STARTS on loc_street (entities.json) — the first
# look_around of a fresh run observes the street, so the integration
# pins arm the start scene.
ARMED_STREET: dict[str, Any] = {
    "loc_street": [
        {"slot": "under_cobbles", "values": ["empty", "rat_nest", "lost_ring"]},
        {"slot": "doorway_crack", "values": ["empty", "folded_note"]},
    ]
}


def _duck_pack(scene_detail: Any) -> Any:
    """The unit-test pack stub: rules only, the shape the gate reads
    (duck-typed — the gate never imports pack.py at runtime). `None`
    builds the v0.1 shape: no `scene_detail` key at all."""
    rules = {} if scene_detail is None else {"scene_detail": scene_detail}
    return SimpleNamespace(rules=rules)


def crafted_pack(
    tmp_path: Path, name: str, scene_detail: Any
) -> Pack:
    """A committed-pack copy with the `scene_detail` block set (or
    REMOVED when None — the v0.1 twin: the committed pack is unarmed,
    so the unarmed arm of every A/B pin is this copy or the committed
    pack itself)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if scene_detail is None:
        rules.pop("scene_detail", None)
    else:
        rules["scene_detail"] = scene_detail
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


def run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> Path:
    """One playscript run; answers the log path (bytes are the pin)."""
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    return log


def look_events(log: Path) -> list[Any]:
    """Every look_around event, in log order."""
    _header, events = read_log(log, SCHEMA)
    return [event for event in events if event.type == "look_around"]


# -- the stream family (unit) -------------------------------------------------


def test_the_name_grammar_is_content_addressed() -> None:
    """`scene_detail_stream_name` is the single owner of the naming
    grammar `scene:<id>:detail` — injective over location ids (map
    keys), never hand-written."""
    assert scene_detail_stream_name("loc_tavern") == "scene:loc_tavern:detail"
    assert scene_detail_stream_name("a") != scene_detail_stream_name("b")
    assert scene_detail_stream_name("a") != scene_detail_stream_name("a:detail")


def test_the_stream_registers_lazily_and_derives_per_seed() -> None:
    """The family registers on first use, derives per (seed, name) —
    the standard stream law (INV-2) — and a scene-LOOKING non-family
    name stays loud (the closed-set tripwire)."""
    stream = scene_detail_stream_name("loc_tavern")
    bank = RngBank(42)
    assert bank.peek(stream) != bank.peek(SUBSTANTIVE)
    assert bank.peek(stream) != bank.peek(COSMETIC)
    assert RngBank(42).peek(stream) == RngBank(42).peek(stream)
    assert RngBank(42).peek(stream) != RngBank(43).peek(stream)
    with pytest.raises(RngError, match="unknown stream"):
        bank.peek("scenee:loc_tavern:detail")  # outside the family


def test_the_family_nests_inside_the_substantive_scope() -> None:
    """The one legal nesting: a scene-family stream may shadow the
    assured substantive run scope (the draw is canon-relevant but
    stream-isolated); the reverse nesting is a bug, not a feature."""
    stream = scene_detail_stream_name("loc_tavern")
    bank = RngBank(42)
    with bank.assure(SUBSTANTIVE):
        bank.randint(1, 6)  # a canon check draws
        with bank.assure(stream):
            assert bank.active == stream
            bank.randint(1, 100)
        assert bank.active == SUBSTANTIVE
        bank.randint(1, 6)
    assert bank.count(stream) == 1
    assert bank.fingerprint == 2  # only the two check draws
    with pytest.raises(RngError, match="cannot assure"):
        with bank.assure(stream):
            with bank.assure(SUBSTANTIVE):
                pass


# -- the draw gate (unit) -----------------------------------------------------


def test_the_unarmed_pack_draws_nothing_and_touches_no_stream() -> None:
    """The unarmed law: no block (the v0.1 twin's rules — the committed
    pack is armed since depth-2b), an unlisted location, or an empty
    slot list answers an empty tuple BEFORE any assure or draw — the
    fingerprint law holds by construction (v0.1 bytes)."""
    bank = RngBank(42)
    projection: dict[str, dict[str, Any]] = {"loc_tavern": {}}
    assert materialize_scene_detail(
        bank, _duck_pack(None), projection, "loc_tavern"
    ) == ()
    assert materialize_scene_detail(
        bank, _duck_pack({}), projection, "loc_tavern"
    ) == ()
    assert materialize_scene_detail(
        bank, _duck_pack({"loc_tavern": []}), projection, "loc_tavern"
    ) == ()
    assert bank.fingerprint == 0
    # laziness is total: the stream was never even registered
    with pytest.raises(KeyError):
        bank.count(scene_detail_stream_name("loc_tavern"))


def test_the_first_observation_draws_pack_order_and_commits_births() -> None:
    """One draw per slot, pack declaration order, each value from the
    declared pool, each birth the promotion shape: from_ None (canon
    never modeled it — the lint guarantees), to_ the drawn value."""
    bank = RngBank(42)
    projection: dict[str, dict[str, Any]] = {"loc_tavern": {}}
    changes = materialize_scene_detail(
        bank, _duck_pack(ARMED), projection, "loc_tavern"
    )
    assert [change.prop for change in changes] == ["under_bench", "behind_barrel"]
    assert all(change.entity == "loc_tavern" for change in changes)
    assert all(change.from_ is None for change in changes)
    assert changes[0].to_ in ARMED["loc_tavern"][0]["values"]
    assert changes[1].to_ in ARMED["loc_tavern"][1]["values"]
    assert bank.count(scene_detail_stream_name("loc_tavern")) == 2
    assert bank.fingerprint == 0  # the draws never touch canon checks


def test_re_observation_skips_canon_slots_and_never_redraws() -> None:
    """First-commit-wins: a slot in the folded projection is skipped —
    no redraw, no second change (canon is the answer); the stream
    advances only on an actual birth."""
    bank = RngBank(42)
    projection: dict[str, dict[str, Any]] = {
        "loc_tavern": {"under_bench": "old_cloak"}  # canon already holds one
    }
    changes = materialize_scene_detail(
        bank, _duck_pack(ARMED), projection, "loc_tavern"
    )
    assert [change.prop for change in changes] == ["behind_barrel"]
    assert bank.count(scene_detail_stream_name("loc_tavern")) == 1
    # the full-canon re-observation: nothing at all
    projection["loc_tavern"]["behind_barrel"] = changes[0].to_
    assert materialize_scene_detail(
        bank, _duck_pack(ARMED), projection, "loc_tavern"
    ) == ()
    assert bank.count(scene_detail_stream_name("loc_tavern")) == 1


def test_the_draw_is_deterministic_and_reproducible() -> None:
    """Same seed, same slot list, same projection state — byte-equal
    births (INV-2; the lazy detail is replay-stable)."""
    first = materialize_scene_detail(
        RngBank(7), _duck_pack(ARMED), {"loc_tavern": {}}, "loc_tavern"
    )
    second = materialize_scene_detail(
        RngBank(7), _duck_pack(ARMED), {"loc_tavern": {}}, "loc_tavern"
    )
    assert first == second
    other_seed = materialize_scene_detail(
        RngBank(8), _duck_pack(ARMED), {"loc_tavern": {}}, "loc_tavern"
    )
    assert [c.to_ for c in first] != [c.to_ for c in other_seed]


def test_arming_a_second_scene_shifts_nothing_measured() -> None:
    """The scene-granular add-safety (the isolation law at stream
    address granularity): arming a second scene shifts neither the
    first scene's materialized values nor any canon-check draw — each
    scene draws from its own stream."""
    armed_one = _duck_pack({"loc_tavern": ARMED["loc_tavern"]})
    armed_two = _duck_pack({
        "loc_tavern": ARMED["loc_tavern"],
        "loc_backyard": [{"slot": "wood_pile", "values": ["empty", "rat_nest"]}],
    })
    bank_a, bank_b = RngBank(42), RngBank(42)
    with bank_a.assure(SUBSTANTIVE), bank_b.assure(SUBSTANTIVE):
        bank_a.randint(1, 6)
        bank_b.randint(1, 6)
        a = materialize_scene_detail(bank_a, armed_one, {"loc_tavern": {}}, "loc_tavern")
        b = materialize_scene_detail(bank_b, armed_two, {"loc_tavern": {}}, "loc_tavern")
    assert a == b  # the first scene's details are byte-equal
    assert bank_a.fingerprint == bank_b.fingerprint == 1


# -- the claim gate (unit — the slot_conflict mirror) --------------------------


def _record(
    event_id: str, changes: tuple[StateChange, ...]
) -> EventRecord:
    return EventRecord(
        id=event_id, t=0, type="look_around", actor=PLAYER, cause=None,
        outcome={}, knowledge=(), state_changes=changes, hooks=(),
        importance="low", provenance={"seed": 42}, target=None,
    )


def test_an_unclaimed_slot_commits() -> None:
    """An empty log (or an untouched slot) answers commit — the claimer
    is the first committer, the law's winner."""
    verdict = detail_claim([], "loc_tavern", "under_bench", "gold")
    assert verdict.outcome == COMMIT and verdict.cause is None
    assert not verdict.refused


def test_a_slot_already_described_empty_rejects_the_later_gold() -> None:
    """The phases.md §5 law verbatim: canon holds `empty`, the later
    gold claim is refused with `slot_conflict`, cause-chained to the
    winning event — no special casing of the empty value."""
    events = [
        _record("ev_0003", (StateChange("loc_tavern", "under_bench", None, "empty"),))
    ]
    verdict = detail_claim(events, "loc_tavern", "under_bench", "gold")
    assert verdict.outcome == SLOT_CONFLICT
    assert verdict.cause == "ev_0003"
    assert verdict.refused


def test_a_claim_matching_canon_is_the_idempotent_no_op() -> None:
    """The ledger's duplicate rule twin: canon holds the SAME value —
    a recorded non-event, never a refusal (re-observation reproduces
    the same detail)."""
    events = [
        _record("ev_0003", (StateChange("loc_tavern", "under_bench", None, "old_cloak"),))
    ]
    verdict = detail_claim(events, "loc_tavern", "under_bench", "old_cloak")
    assert verdict.outcome == NO_OP and not verdict.refused


def test_the_cause_names_the_last_write_the_current_authority() -> None:
    """The cause chain links the LAST write on the slot — the authority
    the claim conflicts with now (a legitimate later canon move
    re-anchors the cause, the occ_breaking_cause semantic)."""
    events = [
        _record("ev_0003", (StateChange("loc_tavern", "under_bench", None, "empty"),)),
        _record(
            "ev_0010",
            (StateChange("loc_tavern", "under_bench", "empty", "moved_on"),),
        ),
    ]
    verdict = detail_claim(events, "loc_tavern", "under_bench", "gold")
    assert verdict.outcome == SLOT_CONFLICT and verdict.cause == "ev_0010"


def test_a_written_then_emptied_slot_still_refuses() -> None:
    """The sentinel law: `written` is not the value — a slot canon
    emptied by a later event is still claimed territory; a new birth
    claim on it is a conflict, never a re-birth."""
    events = [
        _record("ev_0003", (StateChange("loc_tavern", "under_bench", None, "gold"),)),
        _record(
            "ev_0010",
            (StateChange("loc_tavern", "under_bench", "gold", None),),
        ),
    ]
    verdict = detail_claim(events, "loc_tavern", "under_bench", "gold")
    assert verdict.outcome == SLOT_CONFLICT and verdict.cause == "ev_0010"


# -- the wiring (integration) -------------------------------------------------


def test_the_unarmed_v01_twin_observes_without_materializing(
    tmp_path: Path,
) -> None:
    """The unarmed law, integration arm: the v0.1 twin (the committed
    pack with the block popped — the committed arming is live since
    depth-2b) runs look_around as v0.1: no state_changes, no
    `materialized` key on the event — the outcome decoration is present
    only when something materialized (the drifted_from law), so the
    unarmed bytes never move."""
    v01 = crafted_pack(tmp_path, "v01_look", None)
    log = run(
        tmp_path, v01, 42,
        [{"intent": "look_around"}, {"intent": "look_around"}],
        "unarmed_look",
    )
    events = look_events(log)
    assert len(events) == 2
    for event in events:
        assert event.state_changes == ()
        assert "materialized" not in event.outcome


def test_the_armed_observation_materializes_into_the_log(
    tmp_path: Path,
) -> None:
    """The armed twin: the first look_around's state_changes carry the
    births (the promotion shape), its outcome names them under
    `materialized`, and the fold rebuilds the projection from the log
    alone — INV-1's truth test on the materialization events."""
    pack = crafted_pack(tmp_path, "armed", ARMED_STREET)
    log = run(
        tmp_path, pack, 42, [{"intent": "look_around"}], "armed_look"
    )
    event = look_events(log)[0]
    assert [change.prop for change in event.state_changes] == [
        "under_cobbles", "doorway_crack",
    ]
    assert all(
        change.entity == "loc_street" and change.from_ is None
        for change in event.state_changes
    )
    assert event.outcome["materialized"] == materialized_fields(
        event.state_changes
    )
    _header, events = read_log(log, SCHEMA)
    state = fold(events, initial_projection(pack.entities))
    assert state["loc_street"]["under_cobbles"] == event.state_changes[0].to_
    assert state["loc_street"]["doorway_crack"] == event.state_changes[1].to_


def test_re_observation_in_run_is_byte_stable(
    tmp_path: Path,
) -> None:
    """The second look_around in the same run: no new births, no
    `materialized` key — the stream never advances twice for one slot
    (re-observation reads canon)."""
    pack = crafted_pack(tmp_path, "armed2", ARMED_STREET)
    log = run(
        tmp_path, pack, 42,
        [{"intent": "look_around"}, {"intent": "look_around"}],
        "armed_look2",
    )
    first, second = look_events(log)
    assert first.state_changes != ()
    assert second.state_changes == ()
    assert "materialized" not in second.outcome
    assert second.outcome["location"] == first.outcome["location"]


def test_the_laziness_law_an_unobserved_scene_costs_zero_bytes(
    tmp_path: Path,
) -> None:
    """The corpus pin on the committed arming: the armed block's scenes
    are dead until observed — the run (backyard look only) is
    byte-identical to the v0.1 twin's. The arming's corpus price is
    paid only where observation actually fires (the day1 ten's price
    is the guard-scan seed's own pin below)."""
    steps = [
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "look_around"},
        {"intent": "wait", "ticks": 3},
    ]
    v01 = crafted_pack(tmp_path, "v01_lazy", None)
    baseline = run(tmp_path, v01, 42, steps, "baseline")
    lazy = run(tmp_path, PACK, 42, steps, "lazy")
    assert baseline.read_bytes() == lazy.read_bytes()


def test_the_armed_run_differs_only_where_observation_fires(
    tmp_path: Path,
) -> None:
    """The arming is measurable, never silent: the armed run's
    look_around event differs exactly by the births and the outcome
    decoration — the event COUNT and the event TYPES are unchanged (no
    id shifts beyond the materializing event, no appended events: the
    fidelity-only family law, paid in the event's own payload)."""
    steps = [{"intent": "look_around"}]
    pack = crafted_pack(tmp_path, "armed3", ARMED_STREET)
    v01 = crafted_pack(tmp_path, "v01_diff", None)
    baseline = run(tmp_path, v01, 42, steps, "baseline2")
    armed = run(tmp_path, pack, 42, steps, "armed_run")
    base_events = look_events(baseline)
    armed_events = look_events(armed)
    assert len(base_events) == len(armed_events) == 1
    assert base_events[0].type == armed_events[0].type
    assert armed_events[0].state_changes != ()
    assert base_events[0].state_changes == ()
    assert base_events[0].outcome["location"] == armed_events[0].outcome["location"]


# -- the committed arming (depth-2b, iter-76 — the 68b pattern) ----------------

DAY1 = json.loads(
    (REPO / "tests" / "playscripts" / "day1_full.json").read_text(encoding="utf-8")
)


def run_day1(tmp_path: Path, pack: Pack, seed: int, name: str) -> Path:
    """One day1_full playscript run; answers the log path (bytes are the pin)."""
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    return log


def test_the_committed_arming_is_the_declared_block() -> None:
    """The committed pack carries the block (depth-2b, iter-76): exactly
    the two scenes the committed corpus observes — the tavern (the
    narrator looks + the guard's scans + the murmur's room) and the
    guardroom (the rotation scans). The lint accepts it at load."""
    assert PACK.rules["scene_detail"] == {
        "loc_tavern": [
            {"slot": "under_bench", "values": ["empty", "old_cloak"]},
            {"slot": "behind_barrel", "values": ["empty", "lost_ring"]},
        ],
        "loc_guardroom": [
            {"slot": "under_cot", "values": ["empty", "spare_boots"]},
        ],
    }


def test_the_live_arming_materializes_the_committed_pools(
    tmp_path: Path,
) -> None:
    """The live arming: the committed pack's first tavern observation
    materializes the declared slots from the declared pools, in pack
    order, the births riding the event — and the fold rebuilds the
    projection from the log alone (INV-1's truth test, live)."""
    log = run(
        tmp_path, PACK, 42,
        [{"intent": "move", "target": "loc_tavern"}, {"intent": "look_around"}],
        "live_arming",
    )
    event = look_events(log)[0]
    assert [(c.entity, c.prop, c.from_) for c in event.state_changes] == [
        ("loc_tavern", "under_bench", None),
        ("loc_tavern", "behind_barrel", None),
    ]
    pools = {
        entry["slot"]: entry["values"]
        for entry in PACK.rules["scene_detail"]["loc_tavern"]
    }
    assert all(c.to_ in pools[c.prop] for c in event.state_changes)
    assert [m["slot"] for m in event.outcome["materialized"]] == [
        "under_bench", "behind_barrel",
    ]
    _header, events = read_log(log, SCHEMA)
    state = fold(events, initial_projection(PACK.entities))
    assert state["loc_tavern"]["under_bench"] == event.state_changes[0].to_
    assert state["loc_tavern"]["behind_barrel"] == event.state_changes[1].to_


def test_the_knowledge_surface_stays_the_declared_templates(
    tmp_path: Path,
) -> None:
    """The arming-time decision (D-108): the materialized detail's
    knowledge surface is the event's own payload + the folded canon —
    ZERO new knowledge tokens. The observation's knowledge records are
    identical to the v0.1 twin's (`scene_{location}` unchanged: detail
    tokens never ride the records), so the corpus claim surface never
    moves — the measured both-arms law, pinned."""
    steps = [{"intent": "move", "target": "loc_tavern"}, {"intent": "look_around"}]
    v01 = crafted_pack(tmp_path, "v01_knows", None)
    armed = run(tmp_path, PACK, 42, steps, "knows_armed")
    base = run(tmp_path, v01, 42, steps, "knows_base")
    armed_event = look_events(armed)[0]
    base_event = look_events(base)[0]
    assert armed_event.state_changes != ()
    assert armed_event.knowledge == base_event.knowledge
    assert [(k.who, k.channel, k.fidelity, k.knows) for k in armed_event.knowledge] == [
        (PLAYER, "saw", "exact", "scene_loc_tavern"),
    ]


def test_the_paid_day1_price_is_two_scan_payloads(tmp_path: Path) -> None:
    """The corpus-price law's paid half (measured both arms, iter-76):
    over the day1 ten's scan seed (125 — the guard's belief-gated
    scans, the beliefwire-2 arming's own price row; director ON, the
    Simulator default) the scene-detail arming costs exactly TWO event
    payloads — the guard's first tavern scan (the second reads canon:
    one draw per slot ever; the barkeep's later director look reads it
    too) and the guardroom rotation scan — and NOTHING else: same
    event count, same ids, same types, same knowledge, same
    importance, same t/cause; the price is the births + the outcome
    key on the materializing events themselves (the fidelity-only
    family law)."""
    v01 = crafted_pack(tmp_path, "v01_day1", None)
    base = run_day1(tmp_path, v01, 125, "paid_base")
    armed = run_day1(tmp_path, PACK, 125, "paid_armed")
    base_lines = base.read_text().splitlines()
    armed_lines = armed.read_text().splitlines()
    assert len(base_lines) == len(armed_lines)
    diffed = [
        (json.loads(a), json.loads(b))
        for a, b in zip(armed_lines, base_lines, strict=True)
        if a != b
    ]
    assert len(diffed) == 2
    for armed_event, base_event in diffed:
        assert armed_event["type"] == "look_around"
        assert armed_event["actor"] == "npc_guard_02"
        assert set(armed_event) == set(base_event)
        changed = {
            key for key in armed_event
            if armed_event[key] != base_event[key]
        }
        assert changed <= {"state_changes", "outcome"}
        assert armed_event["knowledge"] == base_event["knowledge"]
        assert armed_event["importance"] == base_event["importance"]
        assert armed_event["t"] == base_event["t"]
        assert armed_event["cause"] == base_event["cause"]
    scans = [event for event, _ in diffed]
    assert scans[0]["id"] == "ev_0042"  # the first tavern scan materializes
    assert scans[0]["outcome"]["materialized"] == [
        {"slot": "under_bench", "value": "old_cloak"},
        {"slot": "behind_barrel", "value": "lost_ring"},
    ]
    assert scans[1]["id"] == "ev_0060"  # the guardroom rotation scan
    assert scans[1]["outcome"]["materialized"] == [
        {"slot": "under_cot", "value": "empty"},
    ]


def test_the_day1_ten_pays_only_the_observing_seeds(tmp_path: Path) -> None:
    """The corpus-price law's shape (measured both arms, iter-76):
    the day1 ten (director ON — the Simulator default) pays ONLY where
    an observation of an armed scene actually fires. Four seeds carry
    no observation at all (121, 122, 126, 129 — zero bytes); five
    seeds pay exactly ONE payload — the director-released barkeep look,
    the run's FIRST tavern observation (120, 123, 124, 127, 128); the
    scan seed (125) pays two — its own pin above. Every paid line is
    fidelity-only: fields <= {state_changes, outcome}, the knowledge,
    importance, t and cause untouched."""
    v01 = crafted_pack(tmp_path, "v01_ten", None)
    zero_seeds = (121, 122, 126, 129)
    look_seeds = (120, 123, 124, 127, 128)
    for seed in zero_seeds:
        base = run_day1(tmp_path, v01, seed, f"ten_base_{seed}")
        armed = run_day1(tmp_path, PACK, seed, f"ten_armed_{seed}")
        assert base.read_bytes() == armed.read_bytes(), f"seed {seed}"
    for seed in look_seeds:
        base = run_day1(tmp_path, v01, seed, f"ten_base_{seed}")
        armed = run_day1(tmp_path, PACK, seed, f"ten_armed_{seed}")
        base_lines = base.read_text().splitlines()
        armed_lines = armed.read_text().splitlines()
        assert len(base_lines) == len(armed_lines), f"seed {seed}"
        diffed = [
            (json.loads(a), json.loads(b))
            for a, b in zip(armed_lines, base_lines, strict=True)
            if a != b
        ]
        assert len(diffed) == 1, f"seed {seed}: {len(diffed)} lines paid"
        armed_event, base_event = diffed[0]
        assert armed_event["type"] == "look_around", f"seed {seed}"
        assert armed_event["actor"] == "npc_barkeep_01", f"seed {seed}"
        changed = {
            key for key in armed_event
            if armed_event[key] != base_event[key]
        }
        assert changed <= {"state_changes", "outcome"}, f"seed {seed}"
        assert armed_event["knowledge"] == base_event["knowledge"]


def test_the_armed_day1_seed_replays_byte_identically(
    tmp_path: Path,
) -> None:
    """The T1 discipline on the armed pack: the committed arming is
    deterministic — the same seed replays the same births, byte for
    byte (the lazy detail is replay-stable, INV-2)."""
    first = run_day1(tmp_path, PACK, 125, "replay_a")
    second = run_day1(tmp_path, PACK, 125, "replay_b")
    assert first.read_bytes() == second.read_bytes()


# -- the lint (crafted packs) --------------------------------------------------


def test_the_lint_accepts_the_canonical_arming(tmp_path: Path) -> None:
    """The committed pack's shape with the block set: clean load (the
    arming row's own shape — this is the depth-2b candidate)."""
    pack = crafted_pack(tmp_path, "ok", ARMED)
    assert pack.rules["scene_detail"] == ARMED


def test_the_lint_refuses_an_unknown_location(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="unknown location id"):
        crafted_pack(tmp_path, "bad_loc", {"loc_nowhere": ARMED["loc_tavern"]})


def test_the_lint_refuses_a_non_location_id(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="unknown location id"):
        crafted_pack(
            tmp_path, "bad_kind",
            {"npc_guard_01": ARMED["loc_tavern"]},
        )


def test_the_lint_refuses_an_empty_or_non_object_block(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="non-empty object keyed by location"):
        crafted_pack(tmp_path, "empty_block", {})
    with pytest.raises(PackError, match="non-empty object keyed by location"):
        crafted_pack(tmp_path, "list_block", ["loc_tavern"])


def test_the_lint_refuses_an_empty_slot_list(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="non-empty list of slot entries"):
        crafted_pack(tmp_path, "empty_slots", {"loc_tavern": []})


def test_the_lint_refuses_unknown_entry_keys(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="unknown keys"):
        crafted_pack(
            tmp_path, "unknown_keys",
            {"loc_tavern": [
                {"slot": "under_bench", "values": ["empty"], "weight": 2},
            ]},
        )


def test_the_lint_refuses_a_malformed_slot_or_values(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="slot must be a non-empty string"):
        crafted_pack(
            tmp_path, "blank_slot",
            {"loc_tavern": [{"slot": "  ", "values": ["empty"]}]},
        )
    with pytest.raises(PackError, match="values must be a non-empty list"):
        crafted_pack(
            tmp_path, "empty_values",
            {"loc_tavern": [{"slot": "under_bench", "values": []}]},
        )
    with pytest.raises(PackError, match="values must be a non-empty list"):
        crafted_pack(
            tmp_path, "bad_values",
            {"loc_tavern": [{"slot": "under_bench", "values": ["empty", 7]}]},
        )


def test_the_lint_refuses_duplicate_slots_or_values(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="declared twice in the location"):
        crafted_pack(
            tmp_path, "dup_slot",
            {"loc_tavern": [
                {"slot": "under_bench", "values": ["empty"]},
                {"slot": "under_bench", "values": ["gold"]},
            ]},
        )
    with pytest.raises(PackError, match="values contains duplicates"):
        crafted_pack(
            tmp_path, "dup_value",
            {"loc_tavern": [{"slot": "under_bench", "values": ["empty", "empty"]}]},
        )


def test_the_lint_refuses_a_slot_the_location_models(tmp_path: Path) -> None:
    """The double-claim law: a record key (exits) or a declared flag
    (lit) is canon territory — lazy detail occupies only unmodeled
    slots (the texture law's twin; the fold seeds flags as props)."""
    with pytest.raises(PackError, match="already modeled by the location"):
        crafted_pack(
            tmp_path, "modeled_key",
            {"loc_tavern": [{"slot": "exits", "values": ["empty"]}]},
        )
    with pytest.raises(PackError, match="already modeled by the location"):
        crafted_pack(
            tmp_path, "modeled_flag",
            {"loc_tavern": [{"slot": "lit", "values": ["empty"]}]},
        )


def test_the_lint_refuses_a_unique_slot_overlap(tmp_path: Path) -> None:
    """The one-object law: `hearth` is a brief.scene_texture unique
    slot — one object, one vocabulary; a lazy pool on it double-declares."""
    with pytest.raises(PackError, match="unique slot"):
        crafted_pack(
            tmp_path, "unique",
            {"loc_tavern": [{"slot": "hearth", "values": ["empty", "gold"]}]},
        )
