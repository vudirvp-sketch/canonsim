"""iter-427 acceptance — the intensity half of character change (agenda-1
P5-unit-2, D-280): the accumulated price moves HOW HARD a person goes, not
only where.

The claim the laws below pin:

- a drive `modifiers` row may read the ECHO residue (`source: echo`) at the
  caller's own tick instead of a frozen profile axis, and then owns its
  bands (`low`/`high` — no `psyche.axes` row exists for an echo axis);
- the weighted bar moves the DECISION: an NPC whose history left no residue
  never fires that drive, the same NPC after the news acts on every beat;
  the corpus diverges against its own no-news twin exactly at the residue,
  and is identical before it (the row adds no draw — the fingerprint law);
- the ROW is the cause: with the echo row removed the news cannot move the
  bar, and the NPC acts the same whether or not he heard it;
- the CARD and the brief read the SAME weight: the present-entity line is
  the walk's own bar, never a second fold;
- the quiet-beat skip is fenced off by the pack's declared demand (a bar
  that decays between events cannot be evaluated once per stretch) while
  every committed pack — no echo row — keeps its skip exactly;
- seven dead shapes are refused at load.

The witness corpus is the committed province pack plus in-tmp twins: the
winter kin gets the authored `the_road_wanderer` profile (the archetype the
committed `scan_the_road` row already binds), a SECOND drive whose bar is
zero until the echo residue arrives, and the talk action mints one echo
token (`figure_firing_the_barn`, `wariness`) to its listener. The world's own
mover is the player's news: he walks to the crofts and tells the kin what he
saw. No committed fixture is written (PACK_SPEC §8's twin law), so the
canonical corpora stay byte-identical (the T1 laws remain the oracle).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from brief.assembler import assemble_brief, render_brief
from core.agenda import OPEN, agenda_view
from core.drives import (
    ECHO_SOURCE,
    PROFILE_SOURCE,
    drive_bar,
    drive_specs,
    drive_weight,
    echo_modifiers_declared,
)
from core.echo import EchoScore, echo_scores
from core.fold import fold, initial_projection
from core.knowledge import KnowledgeView
from core.log import read_log
from core.loop import Simulator
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
KIN = "npc_winterkin_01"
PLAYER = "pc_01"
NEWS = "figure_firing_the_barn"  # fades 1440 ticks, wariness 30 at exact
WATCH = "hold_the_watch"
LOOK = "scan_the_road"
SEED = 42
SEED_COUNT = 3  # the beats the residue stays above the row's high band

PROFILE: dict[str, Any] = {
    "archetype": "the_road_wanderer",
    "axes": {
        "openness": 20,
        "conscientiousness": 28,
        "extraversion": 45,
        "agreeableness": 50,
        "neuroticism": 55,
    },
}

#: The row the twin arms: zero while the kin carries no residue, a full bar
#: while it does — the decision flips on the news alone.
ECHO_ROW: dict[str, Any] = {
    "source": ECHO_SOURCE,
    "axis": "wariness",
    "low": 0,
    "high": 4,
    "low_pct": 0,
    "high_pct": 10_000,
}

STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "talk", "target": KIN},
    {"intent": "wait", "ticks": 900},
]


# -- the twin ---------------------------------------------------------------


def _twin(
    tmp_path: Path,
    name: str,
    *,
    news: bool = True,
    echo_row: bool = True,
    mutate: Any = None,
) -> Path:
    """The committed pack plus the P5-unit-2 delta, each piece switchable so
    the ablation removes exactly what the law claims: `news` (the talk mints
    the echo token to its listener), `echo_row` (the drive reads the
    residue). `mutate` is the malformed forms' hook (raises at load)."""
    target = tmp_path / name
    target.mkdir()
    for file_name in (
        "rules.json", "entities.json", "actions.json", "templates.json",
    ):
        shutil.copy(PACK_DIR / file_name, target / file_name)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))

    for npc in entities["npcs"]:
        if npc["id"] == KIN:
            npc["psyche"] = json.loads(json.dumps(PROFILE))
    if news:
        for action in actions["actions"]:
            if action["intent"] == "talk":
                action["knowledge"]["success"].append(
                    {
                        "who": "target",
                        "channel": "saw",
                        "fidelity": "exact",
                        "knows": NEWS,
                    }
                )
    # the watch drive: no measure (an appetite — the bar IS the weight), so
    # the echo row is the only thing that can move it
    drive: dict[str, Any] = {
        "id": WATCH,
        "archetypes": ["the_road_wanderer"],
        "base": 25,
        "max_per_beat": 100,
        "verb": "wait",
        "fields": {"ticks": 1},
        "modifiers": [dict(ECHO_ROW)] if echo_row else [],
    }
    rules["psyche"]["drives"].append(drive)
    if mutate is not None:
        mutate(rules, drive)

    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2), encoding="utf-8"
    )
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    return target


def _run(tmp_path: Path, pack_path: Path, name: str):
    pack = load_pack(pack_path)
    log = tmp_path / name
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {
            "name": name,
            "seed": SEED,
            "pack": "province_pack@0.1",
            "steps": STEPS,
        }
    )
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events, sim, pack


def _events_of(events: list[Any], event_type: str) -> list[Any]:
    return [event for event in events if event.type == event_type]


def _talk_tick(events: list[Any]) -> int:
    talks = [event for event in _events_of(events, "talk") if event.target == KIN]
    assert len(talks) == 1, "the news arrives once, as the player's own act"
    return talks[0].t


def _shape(event: Any) -> tuple[Any, ...]:
    return (event.type, event.actor, event.target, event.outcome)


# -- the inert law ----------------------------------------------------------


def test_the_committed_packs_declare_no_echo_modifier() -> None:
    """The unarmed law (INERT-FIRST): the committed province block declares
    the modifier vocabulary with the PROFILE source only — the loop's fence
    predicate answers False, so the ticker, the skip, the card and the brief
    keep every byte."""
    pack = load_pack(PACK_DIR)
    assert echo_modifiers_declared(pack) is False
    rows = [
        modifier
        for drive in pack.rules["psyche"]["drives"]
        for modifier in drive.get("modifiers", ())
    ]
    assert rows, "the committed block carries the v0.1 profile rows"
    assert all(
        modifier.get("source", PROFILE_SOURCE) == PROFILE_SOURCE
        for modifier in rows
    )


def test_the_source_defaults_to_the_profile_and_the_weight_is_unchanged(
    tmp_path: Path,
) -> None:
    """A row without `source` is a PROFILE row (byte-identical v0.1
    behaviour): `scan_the_road` at openness 20 reads the low band — 20 * 50
    // 100 = 10 — exactly the pre-P5 formula. An echo row declares itself and
    owns its bands (the axis has no `psyche.axes` row)."""
    twin = _twin(tmp_path, "profile_only", echo_row=False, news=False)
    pack = load_pack(twin)
    projection = initial_projection(pack.entities)
    specs = [spec for spec in drive_specs(pack) if spec.npc == KIN]
    assert [spec.drive for spec in specs] == [LOOK, WATCH]
    scan = specs[0]
    assert [row.source for row in scan.modifiers] == [PROFILE_SOURCE]
    assert drive_weight(scan, pack, projection) == 10  # 20 * 50 // 100
    assert specs[1].modifiers == ()  # the unarmed twin declares no row

    armed = load_pack(_twin(tmp_path, "armed_only", news=False))
    watch = [
        spec for spec in drive_specs(armed)
        if spec.drive == WATCH and spec.npc == KIN
    ][0]
    assert [(row.source, row.low, row.high) for row in watch.modifiers] == [
        (ECHO_SOURCE, 0, 4)
    ]


# -- the weight's two sources ------------------------------------------------


def test_the_echo_row_reads_the_residue_at_the_callers_tick(
    tmp_path: Path,
) -> None:
    """One arithmetic law, read three ways: no residue reads ZERO (the fold
    omits the pair — the world's honest answer) and the low band zeroes the
    weight; a residue inside the band leaves it alone; a residue at the high
    band multiplies it. Another NPC's residue can never move this one's
    bar (the L6 fence: the echo is per-NPC)."""
    twin = _twin(tmp_path, "echo_reads", news=False)
    pack = load_pack(twin)
    projection = initial_projection(pack.entities)
    watch = [
        spec for spec in drive_specs(pack)
        if spec.drive == WATCH and spec.npc == KIN
    ][0]

    assert drive_weight(watch, pack, projection) == 0  # no residue: the low band
    assert drive_bar(watch, pack, projection) == 0

    inside = (EchoScore(who=KIN, axis="wariness", score=2),)
    assert drive_weight(watch, pack, projection, inside) == 25  # between the bands

    other = (EchoScore(who="npc_weirkeeper_01", axis="wariness", score=40),)
    assert drive_weight(watch, pack, projection, other) == 0  # not this NPC

    high = (EchoScore(who=KIN, axis="wariness", score=24),)
    assert drive_weight(watch, pack, projection, high) == 25 * 10_000 // 100
    assert drive_bar(watch, pack, projection, echoes=high) == 25 * 10_000 // 100
    # (an appetite with no measure pushes at its full weight — the v0.1 law;
    # `max_per_beat` clamps the bar only when a measure multiplies it)


def test_the_residue_decays_and_the_bar_falls_with_it(tmp_path: Path) -> None:
    """The fold at the caller's tick, not a stored number: `echo_scores`
    answers the decaying score, so the same person's bar is 100 while the
    residue is fresh, 0 after the token's `fades_ticks` — the row moves the
    bar, the fold owns the time."""
    events, _, pack = _run(tmp_path, _twin(tmp_path, "decay"), "decay.jsonl")
    talk = _talk_tick(events)
    view = KnowledgeView.from_events(events)

    def residue(tick: int) -> tuple[Any, ...]:
        return echo_scores(pack, view, tick)

    def watch_bar(tick: int) -> int:
        projection = fold(events, initial_projection(pack.entities))
        watch = [
            spec for spec in drive_specs(pack, projection)
            if spec.drive == WATCH and spec.npc == KIN
        ][0]
        return drive_bar(watch, pack, projection, echoes=residue(tick))

    assert watch_bar(talk) == 25 * 10_000 // 100, "fresh news: the high band"
    assert watch_bar(talk + 720) == 25 * 10_000 // 100, "still the high band"
    assert watch_bar(talk + 1300) == 25, "inside the fade, between the bands"
    assert watch_bar(talk + 1440) == 0, "past fades_ticks the fold holds nothing"


# -- the witness and its two ablations --------------------------------------


def test_the_news_moves_the_bar_and_the_corpus_follows(tmp_path: Path) -> None:
    """BASE (news + the echo row) stays silent until the news lands, then
    acts on the residue; NO-NEWS (the row present, nobody told him) never
    acts; the two corpora are identical up to the news — the row adds no
    draw (the fingerprint law). The first divergent event is the watch."""
    base_events, _, _ = _run(tmp_path, _twin(tmp_path, "base"), "base.jsonl")
    quiet_events, _, _ = _run(
        tmp_path, _twin(tmp_path, "quiet", news=False), "quiet.jsonl"
    )
    talk = _talk_tick(base_events)
    watched = [
        event for event in _events_of(base_events, "wait")
        if event.actor == KIN
    ]
    assert watched, (
        "the armed arm must act on the horizon (empty-ablation rule)"
    )
    assert all(event.t > talk for event in watched), (
        "the kin acts only after the residue arrives — the bar was zero"
    )
    assert [
        event for event in _events_of(quiet_events, "wait")
        if event.actor == KIN
    ] == [], "an untold kin carries no residue and never acts"
    assert [_shape(event) for event in base_events if event.t <= talk] == [
        _shape(event) for event in quiet_events if event.t <= talk
    ], "up to the news the two arms are the same world — the row adds no draw"


def test_the_echo_row_is_the_cause(tmp_path: Path) -> None:
    """The ROW, not the news, is the binding: with the row removed the same
    fresh residue leaves the weight and the bar untouched (25 — the plain
    appetite), and the pack declares no echo consumer at all; with the row
    the same residue drives the bar to the ceiling. Same arithmetic, same
    projection, one declared row apart."""
    fresh = (EchoScore(who=KIN, axis="wariness", score=24),)
    ablated = load_pack(_twin(tmp_path, "ablated", echo_row=False))
    ablated_projection = initial_projection(ablated.entities)
    watch = [
        spec for spec in drive_specs(ablated)
        if spec.drive == WATCH and spec.npc == KIN
    ][0]
    assert echo_modifiers_declared(ablated) is False
    assert drive_weight(watch, ablated, ablated_projection, fresh) == 25
    assert drive_bar(watch, ablated, ablated_projection, echoes=fresh) == 25

    armed = load_pack(_twin(tmp_path, "armed", news=False))
    armed_projection = initial_projection(armed.entities)
    armed_watch = [
        spec for spec in drive_specs(armed)
        if spec.drive == WATCH and spec.npc == KIN
    ][0]
    assert drive_bar(armed_watch, armed, armed_projection, echoes=fresh) == (
        25 * 10_000 // 100
    )


def test_the_card_and_the_brief_read_the_same_bar(tmp_path: Path) -> None:
    """ONE reading (D-024): the present-entity line's `drive=` is the walk's
    own fold — the boosted drive on the card is the drive the ticker rolls,
    and an untold kin's card names the plain drive. The card is assembled
    from the committed log alone (the brief takes no external fold)."""
    events, sim, pack = _run(tmp_path, _twin(tmp_path, "card"), "card.jsonl")
    talk = _talk_tick(events)
    last = events[-1].t
    assert last - talk < 1440, "the residue is still alive on the last beat"
    view = agenda_view(
        pack, sim.projection, KIN,
        echoes=echo_scores(pack, KnowledgeView.from_events(events), last),
    )
    assert view is not None
    assert (view.drive, view.status) == (WATCH, OPEN)
    text = render_brief(assemble_brief(events, pack))
    assert f"drive={WATCH}:{OPEN}" in text

    quiet_events, quiet_sim, quiet_pack = _run(
        tmp_path, _twin(tmp_path, "card_quiet", news=False), "card_quiet.jsonl"
    )
    quiet_view = agenda_view(quiet_pack, quiet_sim.projection, KIN)
    assert quiet_view is not None
    assert quiet_view.drive == LOOK
    quiet_text = render_brief(assemble_brief(quiet_events, quiet_pack))
    assert f"drive={WATCH}" not in quiet_text


# -- the skip's fence -------------------------------------------------------


def test_the_echo_row_fences_off_the_quiet_beat_skip(tmp_path: Path) -> None:
    """A bar that decays between events cannot be evaluated once per
    stretch: the pack's declared demand includes the echo test, so the loop
    refuses the skip — and a pack WITHOUT the row keeps it exactly (the
    fence is the declared reader, never the ticker's presence)."""
    twin = load_pack(_twin(tmp_path, "fenced", news=False))
    fenced = Simulator(twin, SEED, tmp_path / "f.jsonl", SCHEMA, commit="0000000")
    assert fenced._skip_capable is False  # noqa: SLF001 -- the fence's own read

    # the control: a committed pack that declares no such consumer keeps the
    # skip exactly (the floor the fence is measured against)
    control_pack = load_pack(REPO / "content" / "farstead_pack")
    assert echo_modifiers_declared(control_pack) is False
    control = Simulator(
        control_pack, SEED, tmp_path / "c.jsonl", SCHEMA, commit="0000000",
    )
    assert control._skip_capable is True  # noqa: SLF001


# -- the refusals -----------------------------------------------------------


def _strip_echo_readers(node: Any) -> None:
    """Remove every `echo_at_least` condition (the mutation helper: a twin
    without the echo block must not leave the pack's OTHER consumers gating
    on a fold nothing declares — the lint would refuse them first, and this
    test pins the MODIFIER's own refusal)."""
    if isinstance(node, dict):
        for value in node.values():
            _strip_echo_readers(value)
    elif isinstance(node, list):
        node[:] = [
            item for item in node
            if not (
                isinstance(item, dict)
                and item.get("test") == "echo_at_least"
            )
        ]
        for item in node:
            _strip_echo_readers(item)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("unknown key", "unknown key"),
        ("unknown source", "source must be"),
        ("no echo block", "carries no echo block"),
        ("undeclared axis", "a declared echo token scores"),
        ("without bands", "must declare integer"),
        ("low above high", "low < high"),
        ("outside the scale", "the echo scale"),
        ("profile row with bands", "declares no bands of its own"),
    ],
)
def test_dead_modifier_shapes_are_refused_at_load(
    tmp_path: Path, mutation: str, message: str
) -> None:
    def mutate(rules: dict[str, Any], drive: dict[str, Any]) -> None:
        row = drive["modifiers"][0]
        if mutation == "unknown key":
            row["because"] = "the mood"
        elif mutation == "unknown source":
            row["source"] = "belief"
        elif mutation == "no echo block":
            rules.pop("echo", None)
            _strip_echo_readers(rules)
        elif mutation == "undeclared axis":
            row["axis"] = "hunger"
        elif mutation == "without bands":
            row.pop("low")
        elif mutation == "low above high":
            row["low"], row["high"] = 40, 5
        elif mutation == "outside the scale":
            row["high"] = 200
        elif mutation == "profile row with bands":
            row["source"] = PROFILE_SOURCE
            row["axis"] = "openness"
        else:  # pragma: no cover - the test's own guard
            raise AssertionError(f"unknown mutation {mutation!r}")

    with pytest.raises(PackError, match=message):
        load_pack(_twin(tmp_path, name="refused", mutate=mutate))
