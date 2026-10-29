"""iter-423 acceptance — the duty memory (agenda-1 P3, D-278).

The claim the laws below pin: a pack-declared duty, bound to a psyche
archetype and a post, becomes a RECORDED fact of the world when it goes
unkept at its clock —

- a held duty records nothing (the crossing passes silently);
- a lapsed duty records ONCE per witness standing at the post (the
  perception law the at-location expectations already carry), as an
  `inferred`-channel knowledge record of the row's token, cause-chained
  to the event that moved the holder off the post;
- the same lapse is never re-recorded while a witness still holds the
  token (a memory, not a drumbeat);
- a duty whose archetype no one carries yet is DORMANT: the born holders
  arm it from their birth, and the first lapse of a born holder carries
  no cause (the birth is the only event — the log moved nobody);
- the complete ablation (rows, event type, template, archetype and its
  authored profile) leaves every other event of the corpus intact — the
  mechanism prices nothing outside its own rows (INERT-FIRST).

The witness corpus is the committed province pack plus ONE crafted twin:
an authored `psyche` on the crossing's second hand (the archetype
`the_crossing_hand`) and a duty owed at the weirstair post. His own
committed road-leg urgency (a `move` to the artery when the runner stands
with him) is what removes him from the post — no test may hand-place an
actor (the world's own logic is the mover).

Seeds are pinned (T1 discipline); the committed corpora stay untouched —
the whole twin rides `tmp_path`.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.log import read_log
from core.loop import Simulator
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
SOURCE = REPO / "content" / "province_pack"

SECONDHAND = "npc_secondhand_01"
WEIRKEEPER = "npc_weirkeeper_01"
PLAYER = "pc_01"
STAIR = "loc_weirstair"
ROAD = "loc_riverroad"
SERGEANT = "npc_sergeant_01"
MARKET = "npc_marketmistress_01"

#: The crafted identity the twin arms on the second hand — one authored
#: profile (the author's override, five numbers, no extremes) bound to a
#: NEW archetype declared beside the committed vocabulary.
CROSSING_HAND = "the_crossing_hand"
CROSSING_PROFILE = {
    "openness": 44,
    "conscientiousness": 52,
    "extraversion": 58,
    "agreeableness": 61,
    "neuroticism": 40,
}
DUTY_EVENT = "duty_lapsed"
DUTY_LINE = (
    "the post stands unheld — {actor} finds no one where the duty would "
    "have them."
)
TOKEN = "the_crossing_unheld"
DUTY = "the_crossing_held"

SEED = 42
#: The world's own script: the runner walks to the crossing and waits out
#: several rotations. The second hand's committed urgency takes him onto
#: the artery once the runner stands with him (the beat fires at the next
#: step boundary — hence TWO waits), and every rotation after that finds
#: the stair unheld.
STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": STAIR},
    {"intent": "wait", "ticks": 1200},
    {"intent": "wait", "ticks": 1500},
]


def _twin(
    tmp_path: Path,
    name: str = "duty_pack",
    *,
    arm_profile: bool = True,
    arm_archetype: bool = True,
    arm_duty: bool = True,
    arm_event: bool = True,
    mutate: str | None = None,
) -> Path:
    """The committed province pack plus the named pieces of the P3 delta —
    each piece switchable so a law can ablate exactly what it claims."""
    twin = tmp_path / name
    twin.mkdir()
    for file_name in ("rules.json", "entities.json", "actions.json", "templates.json"):
        shutil.copy(SOURCE / file_name, twin / file_name)
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    entities = json.loads((twin / "entities.json").read_text(encoding="utf-8"))
    templates = json.loads((twin / "templates.json").read_text(encoding="utf-8"))

    if arm_archetype:
        rules["psyche"]["archetypes"].append(
            {
                "id": CROSSING_HAND,
                "defaults": dict(CROSSING_PROFILE),
                "want": "the rope side kept under the hand",
            }
        )
    if arm_profile:
        for npc in entities["npcs"]:
            if npc["id"] == SECONDHAND:
                npc["psyche"] = {
                    "archetype": CROSSING_HAND,
                    "axes": dict(CROSSING_PROFILE),
                }
    if arm_duty:
        rules["expectations"]["duties"] = [
            {
                "id": DUTY,
                "archetypes": [CROSSING_HAND],
                "post": STAIR,
                "knows": TOKEN,
            }
        ]
    if arm_event:
        rules["expectations"]["duty_event"] = DUTY_EVENT
        templates["events"][DUTY_EVENT] = DUTY_LINE

    if mutate is not None:
        _mutate(rules, entity_records=entities["npcs"], twin=mutate)

    (twin / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    (twin / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    (twin / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    return twin


def _mutate(
    rules: dict[str, Any],
    *,
    entity_records: list[dict[str, Any]],
    twin: str,
) -> None:
    """The refused shapes — one per call, so each law names ONE dead form."""
    rows = rules["expectations"].get("duties", [])
    if twin == "unknown key":
        rows[0]["post_id"] = STAIR
    elif twin == "undeclared archetype":
        rows[0]["archetypes"] = ["the_unwritten_hand"]
    elif twin == "undeclared post":
        rows[0]["post"] = "loc_nowhere"
    elif twin == "no event":
        rules["expectations"].pop("duty_event", None)
    elif twin == "no rows":
        rules["expectations"].pop("duties", None)
    elif twin == "event not declared":
        rules["expectations"]["duty_event"] = "duty_unwritten"
    elif twin == "unreachable archetype":
        # a DECLARED archetype nobody can carry: the row's obligation has
        # no possible holder (the reachability law)
        rules["psyche"]["archetypes"].append(
            {
                "id": "the_unheld_hand",
                "defaults": dict(CROSSING_PROFILE),
                "want": "a post no one can hold",
            }
        )
        rows[0]["archetypes"] = ["the_unheld_hand"]
    elif twin == "violated at t=0":
        rows[0]["post"] = ROAD  # the second hand stands at the stair at t=0
    elif twin == "empty knows":
        rows[0]["knows"] = ""
    else:  # pragma: no cover - the test's own guard
        raise AssertionError(f"unknown mutation {twin!r}")


def _run(tmp_path: Path, pack_path: Path, name: str = "duty.jsonl"):
    pack = load_pack(pack_path)
    log = tmp_path / name
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "duty", "seed": SEED, "pack": "province_pack@0.1", "steps": STEPS}
    )
    _, events = read_log(log, SCHEMA)
    return events, sim


def _by_type(events: list[Any], event_type: str) -> list[Any]:
    return [event for event in events if event.type == event_type]


# -- the witness ----------------------------------------------------------------


def test_a_lapsed_duty_is_recorded_once_per_witness_at_the_post(
    tmp_path: Path,
) -> None:
    """The world's own move removes the holder; the witnesses standing at
    the post infer the lapse ONCE, cause-chained to that move."""
    events, sim = _run(tmp_path, _twin(tmp_path))

    moves = [
        event for event in _by_type(events, "move")
        if event.actor == SECONDHAND and event.target == ROAD
    ]
    assert len(moves) == 1, "the world's own road-leg urgency is the mover"
    mover = moves[0]

    lapses = _by_type(events, DUTY_EVENT)
    witnesses = {event.actor for event in lapses}
    # the two entities standing at the stair when the clock crosses: the
    # keeper and the runner — never the lapsed holder, never the road
    assert witnesses == {WEIRKEEPER, PLAYER}
    assert SECONDHAND not in witnesses
    for event in lapses:
        assert event.outcome["duty"] == DUTY
        assert event.outcome["expected"] == {"held_at": STAIR}
        assert event.outcome["observed"] == {"held_by": []}
        assert event.cause == mover.id, "the lapse blames the honest mover"
        record = event.knowledge[0]
        assert (record.who, record.channel, record.fidelity, record.knows) == (
            event.actor, "inferred", "exact", TOKEN
        )
    # the projection answers the same story the event does
    assert sim.projection[SECONDHAND]["position"] == ROAD
    assert sim.projection[WEIRKEEPER]["position"] == STAIR


def test_the_lapse_is_not_re_recorded_at_later_rotations(tmp_path: Path) -> None:
    """Four rotations cross after the move; the memory holds ONE record per
    witness (the expectations dedup law)."""
    events, _ = _run(tmp_path, _twin(tmp_path))
    rotations = [
        event for event in _by_type(events, "watch_change") if event.t > 2400
    ]
    assert len(rotations) >= 2, "the script crosses the lapse and a later clock"
    assert len(_by_type(events, DUTY_EVENT)) == 2  # two witnesses, once


def test_a_held_duty_records_nothing(tmp_path: Path) -> None:
    """The discriminator: the SAME twin with the holder never leaving the
    post — the world's urgency cannot fire because the runner's script
    ends before he stands with the second hand. Nothing is recorded, and
    the duty is not an always-armed row."""
    pack_path = _twin(tmp_path)
    pack = load_pack(pack_path)
    log = tmp_path / "held.jsonl"
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {
            "name": "held",
            "seed": SEED,
            "pack": "province_pack@0.1",
            "steps": [{"intent": "wait", "ticks": 1100}],
        }
    )
    _, events = read_log(log, SCHEMA)
    assert _by_type(events, "watch_change"), "the clock crossed"
    assert _by_type(events, DUTY_EVENT) == []
    assert sim.projection[SECONDHAND]["position"] == STAIR


def test_a_born_only_duty_is_dormant_until_the_birth(tmp_path: Path) -> None:
    """The generative half: an obligation bound to an archetype only a BORN
    distribution can draw arms nobody at t=0 (the dormant law), then the
    birth makes it owed — and the first lapse of a born holder has no mover
    to blame (his only event is the birth), so the draft carries no
    cause rather than an invented one."""
    twin = _twin(tmp_path, name="born_duty", arm_profile=False, arm_archetype=False)
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules["expectations"]["duties"] = [
        {
            "id": "the_artery_watched",
            "archetypes": ["the_road_wanderer"],
            "post": "loc_malby",  # the born travellers stand on the artery
            "knows": "the_artery_unwatched",
        }
    ]
    (twin / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")

    events, _ = _run(tmp_path, twin, name="born.jsonl")
    lapses = _by_type(events, DUTY_EVENT)
    assert lapses, "the birth arms the duty and the post stands unheld"
    assert {event.outcome["duty"] for event in lapses} == {"the_artery_watched"}
    # the born holder never moved (his only event is the birth), so the
    # lapse chains to the CLOCK that opened the check, never to a null
    # cause (the log's run-start law) and never to an invented mover
    clocks = {
        event.t: event.id for event in _by_type(events, "watch_change")
    }
    for event in lapses:
        assert event.cause == clocks[event.t]
    # the witnesses are the people standing at Malby's post, never a
    # traveller (they hold the duty, they are not its observers)
    travellers = {"npc_drover_01", "npc_peddler_01", "npc_carrier_01"}
    assert {event.actor for event in lapses}.isdisjoint(travellers)
    assert {event.actor for event in lapses} <= {
        SERGEANT, MARKET, PLAYER, "npc_corporal_01",
    }


def test_the_complete_ablation_leaves_every_other_event(tmp_path: Path) -> None:
    """INERT-FIRST's other side: dropping the whole delta (rows, event
    type, template, archetype, profile) removes exactly the duty events
    and nothing else — the same seed, the same world, byte-for-byte the
    same facts."""
    armed, _ = _run(tmp_path, _twin(tmp_path, name="armed"), name="armed.jsonl")
    ablated, _ = _run(
        tmp_path,
        _twin(
            tmp_path,
            name="ablated",
            arm_profile=False,
            arm_archetype=False,
            arm_duty=False,
            arm_event=False,
        ),
        name="ablated.jsonl",
    )
    assert _by_type(armed, DUTY_EVENT), "the armed arm recorded the lapse"
    assert _by_type(ablated, DUTY_EVENT) == []

    def shape(event: Any) -> tuple[Any, ...]:
        return (event.type, event.actor, event.target, event.outcome)

    assert [shape(e) for e in armed if e.type != DUTY_EVENT] == [
        shape(e) for e in ablated
    ]


# -- the refusals ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("unknown key", "unknown key"),
        ("undeclared archetype", "not a declared psyche archetype"),
        ("unreachable archetype", "dead data"),
        ("undeclared post", "post must name a declared location"),
        ("no event", "requires expectations.duty_event"),
        ("no rows", "declared without expectations.duties"),
        ("event not declared", "not in the template vocabulary"),
        ("violated at t=0", "held at t=0"),
        ("empty knows", "knows must be a non-empty string"),
    ],
)
def test_dead_duty_shapes_are_refused_at_load(
    tmp_path: Path, mutation: str, message: str
) -> None:
    twin = _twin(tmp_path, name="refused", mutate=mutation)
    with pytest.raises(PackError, match=message):
        load_pack(twin)
