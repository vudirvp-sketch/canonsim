"""iter-426 acceptance — the role turn (agenda-1 P5, D-279).

The claim the laws below pin: a person's ROLE can change from what happened
to him, while the five numbers of temperament stay his own frozen seed —

- a declared turn fires ONCE, as a canon event, when the row's own closed
  conditions cross; its cause is the belief's own source event (the news
  that broke him), never a guess;
- the drives, the want, the entity card and the brief follow the NEW role
  through the ONE `core.psyche.role_of` read: the old role's drives fall
  silent, the new role's arm, and the card can never mix two roles;
- the TEMPERAMENT is untouched (the profile's five numbers are the same
  after the turn);
- the complete ablation (rows, event type, template, target archetype and
  its drive, the authored source profile) leaves every other event
  identical — the mechanism prices nothing outside its own rows;
- the quiet-beat skip lands on the very next beat while a turn is possible
  (a turn rewrites the DRIVE SET — a skipped beat would straddle it);
- the probe id names the (carrier, declaration) pair, never the position
  (`turnids-1`, iter-437): a row inserted FIRST renumbers nothing, and two
  declarations that share their target role stay distinct probes;
- ten dead shapes are refused at load (the duplicate `(from, to)` row is the
  tenth: its second row can never fire).

The witness corpus is the committed province pack plus ONE crafted twin:
the smith gets the authored `the_smelter_master` profile (the archetype the
committed drive rows already bind, which the committed pack leaves
unarmed), a `the_wolf_hunter` role with its own drive and want, a turn row
keyed on the belief `wolves_took_the_child`, and the talk action mints that
belief's token to its listener. The world's own mover is the player's news:
he walks to the crofts and tells the smith what the wolves did.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.agenda import agenda_view
from core.drives import drive_specs
from core.log import read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.psyche import profile_of
from core.turning import turning_specs

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
SOURCE = REPO / "content" / "province_pack"

SMITH = "npc_smelter_01"
WEIR = "npc_weirkeeper_01"
PLAYER = "pc_01"
HUNTER = "the_wolf_hunter"
SMELTER_ROLE = "the_smelter_master"
TOKENS = [
    "wolves_took_the_child",
    "wolves_came_down_the_hill",
    "the_childs_name_on_the_stone",
]
HUNT = "the_hunt"
TURN_EVENT = "role_turned"
WANT = "the wolves' account settled"

SMELTER_AXES = {
    "openness": 40,
    "conscientiousness": 78,
    "extraversion": 35,
    "agreeableness": 42,
    "neuroticism": 38,
}

SEED = 42
STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "talk", "target": SMITH},
    # the beat grid runs 360/720/1080 a day: the news lands ~t=1183, so the
    # wait must cross the NEXT day's first beat (1800)
    {"intent": "wait", "ticks": 900},
]


def _twin(
    tmp_path: Path,
    name: str = "turn_pack",
    *,
    arm: bool = True,
    mutate: str | None = None,
) -> Path:
    """The committed province pack plus the P5 delta, each piece switchable
    so the ablation removes exactly what the law claims."""
    twin = tmp_path / name
    twin.mkdir()
    for file_name in ("rules.json", "entities.json", "actions.json", "templates.json"):
        shutil.copy(SOURCE / file_name, twin / file_name)

    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    entities = json.loads((twin / "entities.json").read_text(encoding="utf-8"))
    actions = json.loads((twin / "actions.json").read_text(encoding="utf-8"))
    templates = json.loads((twin / "templates.json").read_text(encoding="utf-8"))

    # the news the player carries: the talk action mints the belief's token
    # to its LISTENER (the smith) — the price arrives by an ordinary event
    for action in actions["actions"]:
        if action["intent"] == "talk":
            for token in TOKENS:
                action["knowledge"]["success"].append(
                    {
                        "who": "target",
                        "channel": "told",
                        "fidelity": "exact",
                        "knows": token,
                    }
                )
    # the belief the turn reads: its own family of the news' tokens, at the
    # pack's OWN global threshold (the committed belief keeps its table)
    traits = rules.get("traits") or {"threshold": 3, "beliefs": {}}
    traits["beliefs"] = dict(traits.get("beliefs") or {})
    traits["beliefs"]["the_price_paid"] = {"family": list(TOKENS)}
    rules["traits"] = traits

    if arm:
        await_turning_pieces(rules, entities, templates)

    if mutate is not None:
        _mutate(rules, entities, templates, mutate)

    (twin / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    (twin / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    (twin / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    (twin / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    return twin


def await_turning_pieces(
    rules: dict[str, Any],
    entities: dict[str, Any],
    templates: dict[str, Any],
) -> None:
    """The armed half: the smith's authored profile, the hunter role (a want +
    its own drive), the turn row, its event type and template line."""
    for npc in entities["npcs"]:
        if npc["id"] == SMITH:
            npc["psyche"] = {
                "archetype": SMELTER_ROLE,
                "axes": dict(SMELTER_AXES),
            }
    rules["psyche"]["archetypes"].append(
        {
            "id": HUNTER,
            "defaults": dict(SMELTER_AXES),
            "want": WANT,
        }
    )
    rules["psyche"]["drives"].append(
        {
            "id": HUNT,
            "archetypes": [HUNTER],
            "base": 100,
            "max_per_beat": 100,
            "verb": "look_around",
        }
    )
    rules["psyche"]["turnings"] = [
        {
            "from": SMELTER_ROLE,
            "to": HUNTER,
            "when": [
                {"noun": "actor", "test": "trait_held", "token": "the_price_paid"}
            ],
        }
    ]
    rules["psyche"]["turning_event"] = TURN_EVENT
    templates["events"][TURN_EVENT] = (
        "the man who was {from} is {to} now — the price settled."
    )


def _row(from_role: str, to_role: str) -> dict[str, Any]:
    """One legal turn row: the twin's own belief condition, a declared pair."""
    return {
        "from": from_role,
        "to": to_role,
        "when": [{"noun": "actor", "test": "trait_held",
                  "token": "the_price_paid"}],
    }


def _carry(
    rules: dict[str, Any],
    entities: dict[str, Any],
    npc_id: str,
    archetype: str,
) -> None:
    """Give one npc an AUTHORED profile of a declared archetype — the second
    carrier a probe-id stability law needs (the row binds the role, never
    the person)."""
    defaults = next(
        row["defaults"]
        for row in rules["psyche"]["archetypes"]
        if row["id"] == archetype
    )
    for npc in entities["npcs"]:
        if npc["id"] == npc_id:
            npc["psyche"] = {"archetype": archetype, "axes": dict(defaults)}


def _mutate(
    rules: dict[str, Any],
    entities: dict[str, Any],
    templates: dict[str, Any],
    twin: str,
) -> None:
    """The refused shapes — one per call, each naming ONE dead form."""
    turns = rules["psyche"].get("turnings")
    if twin == "unknown key":
        turns[0]["when_policy"] = "any"
    elif twin == "from undeclared":
        turns[0]["from"] = "the_unwritten_role"
    elif twin == "from uncarryable":
        rules["psyche"]["archetypes"].append(
            {"id": "the_unheld_role", "defaults": dict(SMELTER_AXES),
             "want": "a post no one can hold"}
        )
        turns[0]["from"] = "the_unheld_role"
    elif twin == "to undeclared":
        turns[0]["to"] = "the_unwritten_hunter"
    elif twin == "to without want":
        for row in rules["psyche"]["archetypes"]:
            if row["id"] == HUNTER:
                row.pop("want", None)
    elif twin == "to without drive":
        rules["psyche"]["drives"] = [
            row for row in rules["psyche"]["drives"] if row["id"] != HUNT
        ]
    elif twin == "self turn":
        turns[0]["to"] = SMELTER_ROLE
    elif twin == "empty when":
        turns[0]["when"] = []
    elif twin == "target noun":
        turns[0]["when"] = [
            {"noun": "target", "test": "same_location", "with": "actor"}
        ]
    elif twin == "other party":
        turns[0]["when"] = [
            {"noun": "actor", "test": "relation_at_least", "axis": "trust",
             "with": "pc_01", "value": 20}
        ]
    elif twin == "no event":
        rules["psyche"].pop("turning_event", None)
    elif twin == "event not declared":
        rules["psyche"]["turning_event"] = "role_unwritten"
    elif twin == "event without rows":
        rules["psyche"].pop("turnings", None)
    elif twin == "echo axis undeclared":
        turns[0]["when"] = [
            {"noun": "actor", "test": "echo_at_least",
             "axis": "the_unscored_axis", "value": 50}
        ]
    elif twin == "echo bar outside the scale":
        turns[0]["when"] = [
            {"noun": "actor", "test": "echo_at_least", "axis": "dread",
             "value": 0}
        ]
    elif twin == "trait token undeclared":
        turns[0]["when"] = [
            {"noun": "actor", "test": "trait_held", "token": "no_such_belief"}
        ]
    elif twin == "flag without parameter":
        turns[0]["when"] = [{"noun": "actor", "test": "flag"}]
    elif twin == "duplicate row":
        turns.append(dict(turns[0]))
    elif twin == "row inserted first":
        _carry(rules, entities, WEIR, "the_road_wanderer")
        turns.insert(0, _row("the_road_wanderer", HUNTER))
    elif twin == "shared target row":
        turns.append(_row("the_road_wanderer", HUNTER))
    else:  # pragma: no cover - the test's own guard
        raise AssertionError(f"unknown mutation {twin!r}")


def _run(tmp_path: Path, pack_path: Path, name: str = "turn.jsonl"):
    pack = load_pack(pack_path)
    log = tmp_path / name
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "turn", "seed": SEED, "pack": "province_pack@0.1", "steps": STEPS}
    )
    _, events = read_log(log, SCHEMA)
    return events, sim, pack


def _by_type(events: list[Any], event_type: str) -> list[Any]:
    return [event for event in events if event.type == event_type]


# -- the witness ----------------------------------------------------------------


def test_the_news_turns_the_smith_and_his_drives_follow(tmp_path: Path) -> None:
    """One canon turn, caused by the talk that carried the news; from the
    next beat the smith pursues the hunter's goal and the smith's own old
    drive is no longer armed."""
    events, sim, pack = _run(tmp_path, _twin(tmp_path))

    talks = [event for event in _by_type(events, "talk")
             if event.target == SMITH]
    assert len(talks) == 1, "the news arrives once, as the player's own act"
    turned = _by_type(events, TURN_EVENT)
    assert len(turned) == 1, "one role turn"
    event = turned[0]
    assert event.actor == SMITH
    assert event.outcome == {"from": SMELTER_ROLE, "to": HUNTER}
    assert event.cause == talks[0].id, "the belief's own source event"
    change = event.state_changes[0]
    assert (change.entity, change.prop, change.from_, change.to_) == (
        SMITH, "archetype", None, HUNTER,
    )
    assert event.t % 360 == 0, "a turn lands on a beat"

    # the drive SET follows the role: the smith now owns the hunter's drive
    specs = [spec for spec in drive_specs(pack, sim.projection) if spec.npc == SMITH]
    assert [spec.drive for spec in specs] == [HUNT]
    # and the world shows it: he looks around after the turn, never before
    looks = [event for event in _by_type(events, "look_around")
             if event.actor == SMITH]
    assert looks, "the new role's drive acts"
    assert all(event.t > turned[0].t for event in looks)

    # the one read law: the card shows the NEW role's pursuit, the authored
    # spine's want is superseded by canon (the pre-turn life is history)
    view = agenda_view(pack, sim.projection, SMITH)
    assert view is not None
    assert (view.drive, view.want) == (HUNT, WANT)


def test_the_temperament_is_untouched_by_the_turn(tmp_path: Path) -> None:
    """Q3's law: the five numbers are the frozen seed — the hunter who was
    the smith keeps his own temperament (two men turning the same way stay
    distinguishable)."""
    _, sim, pack = _run(tmp_path, _twin(tmp_path))
    profile = profile_of(pack, sim.projection, SMITH)
    assert profile is not None
    assert profile["axes"] == SMELTER_AXES
    assert profile["archetype"] == SMELTER_ROLE, "the seed stays the birth's"
    assert sim.projection[SMITH]["archetype"] == HUNTER, "the role is canon"


def test_the_complete_ablation_leaves_every_other_event(tmp_path: Path) -> None:
    """INERT-FIRST's other side: without the delta the smith never turns and
    the rest of the corpus is byte-identical in (type, actor, target,
    outcome)."""
    armed, _, _ = _run(tmp_path, _twin(tmp_path, name="armed"), name="armed.jsonl")
    ablated, _, _ = _run(
        tmp_path, _twin(tmp_path, name="ablated", arm=False), name="ablated.jsonl"
    )
    turned = _by_type(armed, TURN_EVENT)
    assert turned, "the armed arm turned the smith"
    assert _by_type(ablated, TURN_EVENT) == []
    assert all(
        event.actor != SMITH for event in _by_type(ablated, "look_around")
    ), "without the delta the hunter's drive does not exist"

    def shape(event: Any) -> tuple[Any, ...]:
        return (event.type, event.actor, event.target, event.outcome)

    # the world is identical UP TO the turn; after it the divergence IS the
    # point (the new role acts) — the ablation law compares the prefix
    horizon = turned[0].t
    assert [shape(e) for e in armed if e.t < horizon] == [
        shape(e) for e in ablated if e.t < horizon
    ], "before the turn the two arms are the same world"


def test_the_skip_lands_on_the_turn(tmp_path: Path) -> None:
    """The quiet-beat skip may not walk past a possible turn (it rewrites the
    drive set): the beat right after the news evaluates the condition."""
    events, _, _ = _run(tmp_path, _twin(tmp_path))
    talk = [event for event in _by_type(events, "talk") if event.target == SMITH][0]
    turned = _by_type(events, TURN_EVENT)[0]
    beats_between = (turned.t - talk.t) // 360
    assert beats_between <= 2, (
        f"the turn waits at most the next beat (talk {talk.t} -> turn "
        f"{turned.t}) — a skip that walked further would have straddled the "
        f"role change"
    )


# -- the probe id (turnids-1, iter-437) -----------------------------------------


def test_the_probe_id_names_the_declaration_never_its_position(
    tmp_path: Path,
) -> None:
    """The id is the (carrier, from, to) triple — the pack's own names, no
    ordinal."""
    pack = load_pack(_twin(tmp_path, name="one"))
    assert [(spec.npc, spec.probe.id) for spec in turning_specs(pack)] == [
        (SMITH, f"turn_{SMITH}_{SMELTER_ROLE}_{HUNTER}")
    ]


def test_an_inserted_row_never_renumbers_another_probe(tmp_path: Path) -> None:
    """THE stability law (the `roster-2`/`probeids-1` pattern): a row declared
    FIRST — arming a second carrier — leaves every existing probe id
    unchanged. The positional form gave the smith `turn_0001` here (measured,
    iter-437 §2)."""
    one = load_pack(_twin(tmp_path, name="one"))
    two = load_pack(_twin(tmp_path, name="two", mutate="row inserted first"))
    before = {spec.npc: spec.probe.id for spec in turning_specs(one)}
    after = {spec.npc: spec.probe.id for spec in turning_specs(two)}
    assert after[SMITH] == before[SMITH], "a row declared first renumbered it"
    assert after[WEIR] == f"turn_{WEIR}_the_road_wanderer_{HUNTER}"
    assert len(set(after.values())) == len(after), "distinct probes, distinct ids"


def test_two_declarations_sharing_their_target_are_distinct_probes(
    tmp_path: Path,
) -> None:
    """Why `from` rides the id: `A -> X` and `B -> X` are different
    declarations one life can fire in sequence, so `turn_<npc>_<to>` would
    name both. Here the smith is read as master and as wanderer — two
    probes, two ids."""
    pack = load_pack(_twin(tmp_path, name="shared", mutate="shared target row"))
    as_master = {
        spec.probe.id for spec in turning_specs(pack) if spec.npc == SMITH
    }
    as_wanderer = {
        spec.probe.id
        for spec in turning_specs(
            pack, {SMITH: {"archetype": "the_road_wanderer"}}
        )
        if spec.npc == SMITH
    }
    assert as_master == {f"turn_{SMITH}_{SMELTER_ROLE}_{HUNTER}"}
    assert as_wanderer == {f"turn_{SMITH}_the_road_wanderer_{HUNTER}"}


# -- the refusals ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("unknown key", "unknown key"),
        ("from undeclared", "from must name a declared archetype"),
        ("from uncarryable", "dead data"),
        ("to undeclared", "to must name a declared archetype"),
        ("to without want", "must declare a `want`"),
        ("to without drive", "carries no drive"),
        ("self turn", "turns a role into itself"),
        ("empty when", "when must be a non-empty list"),
        ("target noun", "noun must be 'actor'"),
        ("other party", "no other party is read"),
        ("no event", "requires psyche.turning_event"),
        ("event not declared", "not in the template vocabulary"),
        ("event without rows", "declared without psyche.turnings"),
        # turninglint-1 (iter-431): the condition's PARAMETERS resolve at
        # load — a half-written condition can never fire (the dead-gate class)
        ("echo axis undeclared", "declared echo axis"),
        ("echo bar outside the scale", "value must be an integer"),
        ("trait token undeclared", "declared traits.beliefs belief"),
        ("flag without parameter", "requires 'flag'"),
        # turnids-1 (iter-437): the pair the probe id is built from must name
        # ONE declaration — a duplicate can never fire (dead data)
        ("duplicate row", "duplicate turn"),
    ],
)
def test_dead_turn_shapes_are_refused_at_load(
    tmp_path: Path, mutation: str, message: str
) -> None:
    twin = _twin(tmp_path, name="refused", mutate=mutation)
    with pytest.raises(PackError, match=message):
        load_pack(twin)
