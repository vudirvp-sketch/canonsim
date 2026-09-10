"""iter-92 acceptance — depth-6, factions with goals (phases.md §5 P3b,
the STATUS queue's W2 row after depth-3: small-formula dynamics, the
KeeperRL rebellion precedent — a ratio and a threshold, never a
psychology engine).

The laws pinned here:

- **The small formula** (`core/factions.py::faction_probability`): the
  affected fraction of the membership (per-cent, floored) against the
  pack-declared threshold, ramping linearly to `max_per_beat` — pure
  integer arithmetic, INV-2-clean; zero on the deadband (at-or-below
  the bar) and the vacuity law (no values — a memberless or valueless
  faction never acts).
- **D-006 holds — axes are per-entity data**: the walk reads each
  member's `status.<axis>` from the LIVE fold, never a stored group
  score; a member with no value on the axis sits the ratio out (the
  decay pass's read family).
- **The one-id law** (D-112): a faction is a pack entity (kind
  `group`) acting through the SAME intent door — the intent's actor
  IS the group id, band NPC_REACTION at the entry tick (D-039), the
  event's `provenance.cause_intent` the `faction_NNNN` handle; the
  group never appears in presence views (it acts, it does not appear).
- **The stream law** (engine-2's twin, D-079): the roll draws on the
  entry's own `faction:<group>:<kind>` stream — one draw per walk per
  entry (the cadence law — p=0 still consumes the roll), zero
  substantive draws, and the armed arm's event delta is the faction
  family ALONE (the both-arms corpus price, D-108).
- **The scene-LOD scoping** (depth-3's one-gate law): under an armed
  macro clock the faction's ANCHOR scopes it — the active zone's
  beats, the warm ring's crossings, the cold zone silent; under the
  unarmed clock the one-scene law (every beat, `locations=None`).
- **The unarmed law** (the 68a pattern): the committed pack declares
  no groups and no factions — the walk returns nothing, zero draws,
  and a crafted pack carrying the inert vocabulary (groups + action +
  template, no `factions` block) runs the committed corpus scripts
  BYTE-IDENTICALLY (zero corpus price by construction, zero re-pins).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.factions import faction_intents, faction_probability
from core.fold import initial_projection, present_in_order
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import RngBank, faction_stream_name
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

GROUP = "grp_watch"
GROUP_NAME = "the watch"
ANCHOR = "loc_guardroom"
EVENT_TYPE = "muster_call"
TEMPLATE_LINE = "The {actor} musters at the {location}."
MACRO_EVENT = "year_turns"
MACRO_LINE = "The year turns to {year}."
MEMBERS = ("npc_guard_01", "npc_guard_02")
#: fears (80, 70) over trigger 50, threshold 30, max 100: fraction 100,
#: bar 100 — every roll fires (the deterministic armed arm).
ARMED_ENTRY: dict[str, Any] = {
    "group": GROUP,
    "axis": "fear",
    "trigger_value": 50,
    "threshold": 30,
    "max_per_beat": 100,
    "intent": {"kind": "muster"},
    "notes": "the watch's flinch — the acceptance arm (bar 100)",
}
WAIT_400: list[dict[str, Any]] = [{"intent": "wait", "ticks": 400}]
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]


def crafted_pack(
    tmp_path: Path,
    name: str,
    *,
    entries: list[dict[str, Any]] | None = None,
    fears: tuple[int, int] | None = None,
    anchor: str = ANCHOR,
    macro: Any = False,
) -> tuple[Path, Pack]:
    """A committed-pack copy carrying the depth-6 INERT vocabulary (the
    group entity + the muster action + the template line — bytes that
    cost an unarmed pack nothing) plus the armed knobs: the `factions`
    entries, the guards' seeded `status.fear`, the group's anchor, and
    the optional `time.macro` block (False = untouched — the committed
    pack declares none). Returns the pack dir (for post-hoc JSON edits)
    and the loaded pack."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)

    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    entities["groups"] = [
        {
            "id": GROUP,
            "name": GROUP_NAME,
            "position": anchor,
            "members": list(MEMBERS),
            "notes": "the acceptance faction (depth-6): the two watchmen",
        }
    ]
    if fears is not None:
        for npc, fear in zip(MEMBERS, fears, strict=True):
            record = next(n for n in entities["npcs"] if n["id"] == npc)
            record["status"]["fear"] = fear
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if entries is not None:
        rules["factions"] = {"entries": entries}
    if macro is not False:
        if macro is None or macro == "v01":
            # the v0.1 one-scene twin: both blocks dropped together
            # (the pairing law; weather-1's arming re-pin)
            rules["time"].pop("macro", None)
            rules.pop("weather", None)
        else:
            rules["time"]["macro"] = macro
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    actions["actions"].append(
        {
            "intent": "muster",
            "label": "muster",
            "resolver": "wait",
            "ticks": 2,
            "check": None,
            "on_failure": None,
            "events": {"success": EVENT_TYPE},
            "requires": [],
            "fields": [],
            "knowledge": {"success": [], "failure": []},
            "hooks": {"success": [], "failure": []},
            "notes": "the faction's goal verb (depth-6 acceptance vocabulary)",
        }
    )
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates["events"][EVENT_TYPE] = TEMPLATE_LINE
    templates["events"][MACRO_EVENT] = MACRO_LINE
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target, load_pack(target)


def armed(tmp_path: Path, name: str, **kwargs: Any) -> tuple[Path, Pack]:
    """The deterministic armed arm: fears (80, 70), bar 100."""
    kwargs.setdefault("entries", [dict(ARMED_ENTRY)])
    kwargs.setdefault("fears", (80, 70))
    return crafted_pack(tmp_path, name, **kwargs)


def _mutated(
    tmp_path: Path, name: str, mutate: Callable[[Path], None], **kwargs: Any
) -> Pack:
    """A crafted pack mutated post-lint-setup (the lint probes): the
    base is crafted with the kwargs, then `mutate` edits the JSON in
    place before the final load runs the lint."""
    _base, _pack = crafted_pack(tmp_path, f"base_{name}", **kwargs)
    target = tmp_path / name
    shutil.copytree(_base, target)
    mutate(target)
    return load_pack(target)


def _entry_mutate(**field: Any) -> Callable[[Path], None]:
    """A rules.json mutator: overwrite one field of the factions entry
    (or drop it when the value is DEL)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        entry = rules["factions"]["entries"][0]
        for key, value in field.items():
            if value is DEL:
                entry.pop(key, None)
            else:
                entry[key] = value
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


def _group_mutate(**field: Any) -> Callable[[Path], None]:
    """An entities.json mutator: overwrite one field of the group
    record (or drop it when the value is DEL)."""
    def mutate(target: Path) -> None:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        group = entities["groups"][0]
        for key, value in field.items():
            if value is DEL:
                group.pop(key, None)
            else:
                group[key] = value
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return mutate


DEL = object()


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[Path, Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(
        {"name": name, "seed": seed, "pack": pack.name_version, "steps": steps}
    )
    sim.close()
    return log, result


# -- the small formula --------------------------------------------------------


def test_the_formula_deadband_and_ramp() -> None:
    """The KeeperRL shape, pinned at the integers: the affected fraction
    (floored per-cent) against the threshold — at-or-below never fires;
    above it the bar ramps linearly to `max_per_beat` at fraction 100."""
    assert faction_probability((), 50, 30, 100) == 0  # the vacuity law
    assert faction_probability((10, 10), 50, 30, 100) == 0  # fraction 0
    # the boundary itself: fraction == threshold -> at-the-bar, never fires
    assert faction_probability((80, 10), 50, 50, 100) == 0
    # fraction 100 -> the ceiling
    assert faction_probability((80, 70), 50, 30, 100) == 100
    # the ramp: 3 of 4 affected -> fraction 75; (75-30)*60//70 = 38
    assert faction_probability((80, 80, 80, 10), 50, 30, 60) == 38
    # the floor: 1 of 3 affected -> fraction 33; (33-30)*100//70 = 4
    assert faction_probability((80, 10, 10), 50, 30, 100) == 4
    # monotone in the values (the emergent-dynamics law: more axis,
    # never less goal)
    bars = [
        faction_probability(values, 50, 30, 100)
        for values in ((0, 0), (10, 80), (80, 80), (80, 90))
    ]
    assert bars == sorted(bars)
    assert bars[0] == 0 and bars[-1] == 100


def test_the_formula_reads_only_integers() -> None:
    """The trigger compares against axis VALUES — the status family is
    integers; the same values always yield the same bar (INV-2)."""
    assert faction_probability((50, 50), 50, 0, 100) == 100  # at the trigger
    assert faction_probability((49, 49), 50, 0, 100) == 0


# -- the pack lint ------------------------------------------------------------


def test_the_groups_category_lints(tmp_path: Path) -> None:
    """The one-id law's pack side: the group is an entity (kind
    `group`, found by `entity()`/`kind_of()`), its anchor a declared
    location seeded into the projection, its members declared npcs;
    presence views never list it (the group acts, it does not appear)."""
    _dir, pack = armed(tmp_path, "groups_ok")
    assert pack.kind_of(GROUP) == "group"
    assert pack.entity(GROUP)["name"] == GROUP_NAME
    projection = initial_projection(pack.entities)
    assert projection[GROUP]["position"] == ANCHOR
    assert GROUP not in present_in_order(pack, projection, ANCHOR)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_group_mutate(position="loc_none"), "unknown position"),
        (
            _group_mutate(members=["npc_guard_01", "npc_guard_01"]),
            "duplicate member",
        ),
        (_group_mutate(members=["npc_pc_none"]), "is not a declared npc"),
        (_group_mutate(crew=[]), "unknown keys"),
        (_group_mutate(members=DEL), "members must be a list"),
        (_group_mutate(id="npc_guard_01"), "not unique across categories"),
    ],
)
def test_the_groups_lint_refusals(
    tmp_path: Path, mutate: Callable[[Path], None], message: str
) -> None:
    """A crafted group record that breaks the contract dies naming it
    (the pred-contract family — a PackError, never the host's
    exception)."""
    with pytest.raises(PackError, match=message):
        _mutated(tmp_path, "grp_bad", mutate, entries=None, fears=None)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_entry_mutate(group="grp_none"), "unknown group"),
        (_entry_mutate(axis="morale"), "not a rules.states axis"),
        (_entry_mutate(trigger_value=-1), "trigger_value"),
        (_entry_mutate(threshold=100), "threshold"),
        (_entry_mutate(max_per_beat=0), "max_per_beat"),
        (_entry_mutate(maxim=5), "unknown keys"),
    ],
)
def test_the_factions_lint_refusals(
    tmp_path: Path, mutate: Callable[[Path], None], message: str
) -> None:
    """A crafted faction entry that breaks the closed vocabulary or the
    ranges dies naming the field (dead data refused: threshold 100 and
    max 0 can never fire)."""
    with pytest.raises(PackError, match=message):
        _mutated(
            tmp_path, "fct_bad", mutate,
            entries=[dict(ARMED_ENTRY)], fears=(80, 70),
        )


def test_the_duplicate_pair_is_refused(tmp_path: Path) -> None:
    """Engine-2's twin: two entries on one (group, kind) pair would put
    two rolls on one stream and couple their draws — refused."""
    entries = [dict(ARMED_ENTRY), dict(ARMED_ENTRY)]
    with pytest.raises(PackError, match="duplicate faction"):
        crafted_pack(tmp_path, "dup", entries=entries, fears=(80, 70))


def test_the_unknown_block_key_is_refused(tmp_path: Path) -> None:
    """The closed vocabulary at the block level too (the future-layer
    law's own lifecycle: the block is real now, its shape owned)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        rules["factions"]["houses"] = {}
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    with pytest.raises(PackError, match="unknown keys.*entries \\| notes"):
        _mutated(
            tmp_path, "blk_bad", mutate,
            entries=[dict(ARMED_ENTRY)], fears=(80, 70),
        )


def test_the_requires_cond_lint_reuses_the_closed_set(tmp_path: Path) -> None:
    """The faction's `requires` ride the SAME closed precondition set
    as the urgencies — an unknown test dies naming it."""
    entries = [dict(ARMED_ENTRY)]
    entries[0]["requires"] = [{"noun": "actor", "test": "mind_read"}]
    with pytest.raises(PackError, match="unknown precondition test"):
        crafted_pack(tmp_path, "req_bad", entries=entries, fears=(80, 70))


# -- the walk (unit) ----------------------------------------------------------


def test_the_unarmed_committed_pack_walks_nothing() -> None:
    """The 68a law: no `factions` block -> no specs, no draws, no
    intents — the committed pack pays the mechanism zero."""
    bank = RngBank(42)
    assert faction_intents(PACK, initial_projection(PACK.entities), bank) == []
    # the stream never drew — the registry is draw-driven
    with pytest.raises(KeyError):
        bank.count(faction_stream_name(GROUP, "muster"))
    assert bank.fingerprint == 0


def test_the_walk_returns_the_group_intent(tmp_path: Path) -> None:
    """The one-id law: the intent's actor IS the group id, the id
    handle `faction_0000` — through the same door as an urgency."""
    _dir, pack = armed(tmp_path, "walk_ok")
    intents = faction_intents(pack, initial_projection(pack.entities), RngBank(42))
    assert len(intents) == 1
    intent = intents[0]
    assert intent.actor == GROUP
    assert intent.kind == "muster"
    assert intent.id == "faction_0000"
    assert intent.target is None


def test_the_roll_rides_the_isolated_faction_stream(tmp_path: Path) -> None:
    """Engine-2's twin: the draw lands on `faction:<group>:<kind>` —
    one per walk, the substantive fingerprint untouched (an added
    faction shifts neither a canon check draw nor another entry's
    rolls)."""
    _dir, pack = armed(tmp_path, "stream_ok")
    stream = faction_stream_name(GROUP, "muster")
    bank = RngBank(42)
    faction_intents(pack, initial_projection(pack.entities), bank)
    assert bank.count(stream) == 1
    assert bank.fingerprint == 0
    faction_intents(pack, initial_projection(pack.entities), bank)
    assert bank.count(stream) == 2


def test_the_cadence_law_draws_even_at_bar_zero(tmp_path: Path) -> None:
    """The roll is the cadence's own cost: p=0 still consumes the draw
    (the stream advances uniformly — the formula only shapes the
    comparison bar, exactly like a probability-0 urgency entry)."""
    _dir, pack = crafted_pack(
        tmp_path, "bar0", entries=[dict(ARMED_ENTRY)], fears=(0, 0)
    )
    stream = faction_stream_name(GROUP, "muster")
    bank = RngBank(42)
    assert faction_intents(pack, initial_projection(pack.entities), bank) == []
    assert bank.count(stream) == 1


def test_the_deadband_silences_the_goal(tmp_path: Path) -> None:
    """Fears below the trigger: fraction 0, at-or-below the bar — the
    goal never fires (the deadband is the pack's own number)."""
    _dir, pack = crafted_pack(
        tmp_path, "dead", entries=[dict(ARMED_ENTRY)], fears=(10, 20)
    )
    assert faction_intents(pack, initial_projection(pack.entities), RngBank(42)) == []


def test_the_nonholder_member_sits_the_ratio_out(tmp_path: Path) -> None:
    """The decay family's read law: a member with no value on the axis
    does not count — the ratio is over the membership that HOLDS the
    data (here: one holder at 80 -> fraction 100 -> bar 100)."""

    def drop_fear(target: Path) -> None:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        record = next(n for n in entities["npcs"] if n["id"] == MEMBERS[1])
        del record["status"]["fear"]
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    pack = _mutated(
        tmp_path, "sit_out", drop_fear,
        entries=[dict(ARMED_ENTRY)], fears=(80, 0),
    )
    intents = faction_intents(pack, initial_projection(pack.entities), RngBank(42))
    assert len(intents) == 1


def test_the_lod_filter_scopes_by_the_anchor(tmp_path: Path) -> None:
    """depth-3's one-gate law at the walk: `locations` scopes the walk
    to factions ANCHORED there — a guardroom faction does not roll for
    the street's zone (None is the one-scene law, every entry)."""
    _dir, pack = armed(tmp_path, "lod_unit")
    projection = initial_projection(pack.entities)
    bank = RngBank(42)
    stream = faction_stream_name(GROUP, "muster")
    assert faction_intents(pack, projection, bank, locations=("loc_street",)) == []
    # the excluded faction's stream never drew — the registry is
    # draw-driven (the skip precedes the roll)
    with pytest.raises(KeyError):
        bank.count(stream)
    assert faction_intents(pack, projection, bank, locations=(ANCHOR,)) != []
    assert bank.count(stream) == 1
    assert faction_intents(pack, projection, bank) != []  # None: one-scene


def test_the_requires_gate_stays_silent_when_the_world_says_no(
    tmp_path: Path,
) -> None:
    """The urgency family's noise-floor law: a hit that fails the gates
    produces NO intent (silent — no rejection from the walk; the door
    re-validates at its own tick)."""
    entries = [dict(ARMED_ENTRY)]
    entries[0]["requires"] = [
        {"noun": "actor", "test": "flagged_accessible", "flag": "no_such_flag"}
    ]
    _dir, pack = crafted_pack(tmp_path, "gate", entries=entries, fears=(80, 70))
    assert faction_intents(pack, initial_projection(pack.entities), RngBank(42)) == []


# -- the integration (the door, the LOD, the price) ---------------------------


def test_the_goal_fires_through_the_door(tmp_path: Path) -> None:
    """The full pipeline: the beat's walk -> the intent (band
    NPC_REACTION) -> the door -> the completion -> ONE canon event
    with actor = the group id, cause-chained to the previous event
    (the chronological-chain law), the faction handle in provenance."""
    _dir, pack = armed(tmp_path, "door", macro="v01")
    log, _result = _run(tmp_path, pack, 42, WAIT_400, "door")
    _header, events = read_log(log, SCHEMA)
    musters = [e for e in events if e.type == EVENT_TYPE]
    assert len(musters) >= 1  # the beat at 360 arms it
    muster = musters[0]
    assert muster.actor == GROUP
    assert muster.provenance["cause_intent"] == "faction_0000"
    index = events.index(muster)
    assert index > 0 and muster.cause == events[index - 1].id


def test_the_run_is_deterministic(tmp_path: Path) -> None:
    """INV-2: same seed + same script -> byte-identical logs (the
    formula, the stream, the door all fold from the same inputs)."""
    _dir, pack = armed(tmp_path, "det")
    log_a, _a = _run(tmp_path, pack, 42, WAIT_400, "det_a")
    log_b, _b = _run(tmp_path, pack, 42, WAIT_400, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_cold_zone_faction_is_silent_under_an_armed_clock(
    tmp_path: Path,
) -> None:
    """The one-gate law's cold arm: with the macro clock armed and the
    PC INSIDE the tavern, a faction anchored at the market (COLD — the
    street is the hub, its exits cover the whole map, so the cold zone
    only exists once the PC steps off it) never rolls — not at the
    beats, not at the crossings (its population ride is depth-7's
    aggregate machinery, never this walk's)."""
    _dir, pack = armed(
        tmp_path, "cold", anchor="loc_market",
        macro={"cadence_ticks": 40, "event_type": MACRO_EVENT},
    )
    steps = [{"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "cold")
    _header, events = read_log(log, SCHEMA)
    assert not any(e.actor == GROUP for e in events)


def test_the_warm_ring_faction_rolls_at_the_crossings(tmp_path: Path) -> None:
    """The warm arm: the PC at the street, the faction anchored at the
    tavern (WARM — the street's exit) — its goal rides the macro
    crossings (the beat at 360 never comes in the 100-tick window),
    and only there: the muster lands, the cold arm above does not."""
    _dir, pack = armed(
        tmp_path, "warm", anchor="loc_tavern",
        macro={"cadence_ticks": 40, "event_type": MACRO_EVENT},
    )
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "warm")
    _header, events = read_log(log, SCHEMA)
    musters = [e for e in events if e.type == EVENT_TYPE]
    assert len(musters) >= 1
    for muster in musters:
        assert muster.t > 100  # after the crossings' entry tick — never at 360


def test_the_active_zone_faction_rolls_at_the_beats(tmp_path: Path) -> None:
    """The active arm: the faction anchored at the PC's own street —
    the beats carry it (t=360 inside a 400-tick wait), the armed clock
    keeping the crossings to the warm ring."""
    _dir, pack = armed(
        tmp_path, "active", anchor="loc_street",
        macro={"cadence_ticks": 40, "event_type": MACRO_EVENT},
    )
    log, _result = _run(tmp_path, pack, 42, WAIT_400, "active")
    _header, events = read_log(log, SCHEMA)
    musters = [e for e in events if e.type == EVENT_TYPE]
    assert len(musters) >= 1


def test_the_corpus_price_is_the_faction_family_alone(
    tmp_path: Path,
) -> None:
    """The both-arms measurement (D-108): the armed arm vs the unarmed
    twin (the `factions` block's PRESENCE alone differs — the world,
    the groups, the action, the template stay: same fears, same decay)
    — the substantive fingerprint EQUAL (the roll rides the isolated
    faction stream; the fixed-tick no-check action draws nothing
    through the door), the event delta the muster family ALONE, the
    shared events byte-equal ids."""
    _dir_a, armed_pack_v = armed(tmp_path, "price_armed", macro="v01")
    _dir_u, unarmed_pack_v = crafted_pack(
        tmp_path, "price_unarmed", entries=None, fears=(80, 70), macro="v01"
    )
    log_a, result_a = _run(tmp_path, armed_pack_v, 42, WAIT_400, "price_a")
    log_u, result_u = _run(tmp_path, unarmed_pack_v, 42, WAIT_400, "price_u")
    _header, events_a = read_log(log_a, SCHEMA)
    _header, events_u = read_log(log_u, SCHEMA)
    assert result_a.fingerprint == result_u.fingerprint
    musters = [e for e in events_a if e.type == EVENT_TYPE]
    assert len(musters) >= 1
    assert all(e.actor == GROUP for e in musters)
    assert len(events_a) == len(events_u) + len(musters)
    # the shared events: the same sequence (t, type, actor) — the muster
    # family interleaves chronologically, so the ids renumber; the bytes
    # of every other event are untouched (the cause chains stay honest)
    shared = [
        (e.t, e.type, e.actor) for e in events_a if e.type != EVENT_TYPE
    ]
    unarmed = [(e.t, e.type, e.actor) for e in events_u]
    assert shared == unarmed


def test_the_unarmed_twin_is_the_committed_bytes(tmp_path: Path) -> None:
    """The zero-price proof (the 68a pattern): a crafted pack carrying
    the INERT depth-6 vocabulary (the group entity, the muster action,
    the template line — no `factions` block, committed fears) runs the
    committed corpus scripts BYTE-IDENTICALLY to the committed pack
    itself (the T1 golden + every corpus fixture untouched — zero
    re-pins)."""
    _dir, inert = crafted_pack(tmp_path, "inert", entries=None, fears=None)
    for script in ("plumbing_smoke", "day1_full"):
        playscript = json.loads(
            (REPO / "tests" / "playscripts" / f"{script}.json").read_text(
                encoding="utf-8"
            )
        )
        _log_c, _r_c = _run(tmp_path, PACK, 42, playscript["steps"], f"c_{script}")
        _log_u, _r_u = _run(
            tmp_path, inert, 42, playscript["steps"], f"u_{script}",
        )
        assert _log_c.read_bytes() == _log_u.read_bytes()


def test_the_tale_renders_the_faction_line(tmp_path: Path) -> None:
    """The render arm: the group's display name + anchor resolve in the
    chronicle line (the group is a pack entity — `display_name` and
    the position fold read it like any actor's; the pack's
    story-critical listing decides the muster's visibility, the tune-1
    split)."""
    target, _pack = armed(tmp_path, "render", macro="v01")
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["importance"]["story_critical_events"].append(EVENT_TYPE)
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pack = load_pack(target)
    log, _result = _run(tmp_path, pack, 42, WAIT_400, "render")
    _header, events = read_log(log, SCHEMA)
    chronicle = render_chronicle(events, pack, 42)
    assert GROUP_NAME in chronicle
    assert "the guard room" in chronicle  # the anchor renders as {location}
