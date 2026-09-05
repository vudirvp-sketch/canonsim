"""iter-60 acceptance — the scene manager + mode B (scene-1, phase 4;
TASKS.md's row: "the scene manager + mode B (one NPC per call — the
chorus is a queue, not a convention; the per-NPC brief's leak
surface)"). The contract owner is `docs/BRIEF_SPEC.md` §3.9; the
architecture owner is `docs/blueprint/phases.md` §1/§4.

The laws pinned here:

- **The queue law**: the chorus is a deterministic fold over (log,
  pack), never a convention — presence-gated at the current scene
  (projection read), pack-gated (an NPC without a `brief.actors` entry
  is not chorus-eligible — the DORMANT family precedent), kind-gated
  (the player never: mode A owns its call; ambient groups never: they
  hold records but do not speak), pack declaration order (INV-2), and
  capped by the per-beat actor-call budget (beyond-cap NPCs fall to the
  L12 template rung — their beats already render through the chronicle).
- **The knower-parameterized assembly**: mode A (`knower=None`, the
  player) is the committed corpus shape, byte-identical by construction;
  mode B (`knower=<npc>`) runs the SAME pipeline — the actor's own
  perception (scene_delta), own memory (recalled_facts, beliefs
  included), own role text and voice (the `brief.actors` entry, never
  the narrator's). The shared blocks (scene_texture, present_entities,
  lore, options) stay shared — one scene, one ledger, one grammar,
  observables only (L6).
- **The leak surface** (the blind-NPC law, T3's extension — the
  phase-4 exit criterion's instrument core): a mode-B brief contains
  ONLY what its knower perceived and holds — every scene_delta line
  maps to an event the knower perceived, every recalled_facts line maps
  to a record (or belief) the knower owns; a record held by another
  knower can never render, by construction.
- **The knower gate**: an unknown id, an item, a location, an ambient
  group, or a present-but-undeclared NPC is a loud ValueError, never a
  wrong brief.
- **The actor call document**: mode B carries the `actor:` protocol
  line (whose beat-projection the call is); mode A's bytes are unchanged
  (the committed corpus shape, the zero-regen landing).
- **The corpus price is zero**: mode A over the committed pack (which
  now carries `chorus` + `actors`) is byte-identical to a block-less
  copy — the pack's own declaration is the gate (INV-3).
- **The lint family**: closed vocabularies for both blocks; the
  directives construction-fit law (never-dropped data); the player
  never carries an actor entry; dead vocabulary refused.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from brief import SceneLedger, assemble_brief, render_brief, speaking_queue
from brief.mediator import narrator_call
from brief.scene import present_at_scene, recall_query
from cli.mediator import Mediator
from core.knowledge import KnowledgeView
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import RunnerError, Simulator
from core.pack import Pack, PackError, load_pack
from core.retrieval import RetrievalIndex

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())
PLAYER = PACK.player_id()
GUARD = "npc_guard_01"
RELIEF = "npc_guard_02"
BARKEEP = "npc_barkeep_01"
DRUNK = "npc_drunk_01"
MAID = "npc_maid_01"


def _blocks(text: str) -> dict[str, list[str]]:
    """Rendered brief → block bodies (headers stripped, marker kept)."""
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            out[current] = []
        elif current is not None and line:
            out[current].append(line)
    return out


def _block(text: str, block_id: str) -> list[str]:
    return _blocks(text)[block_id]


def _mutated_pack(mutate: Callable[[dict[str, Any]], None]) -> Pack:
    """A deep-copied pack with mutated brief rules (the test_brief
    pattern)."""
    data = json.loads(json.dumps(dict(PACK.data)))
    mutate(data["rules.json"])
    return Pack(data=data)


def _golden_events() -> list[Any]:
    _header, events = read_log(GOLDEN, SCHEMA)
    return list(events)


def run_day1(tmp_path: Path, seed: int) -> list[Any]:
    """The committed pack's live fire: day1_full on a seed (the
    reflection-arming precedent — seeds 123/125 carry the measured
    recurrences)."""
    log = tmp_path / f"day1_scene_{seed}.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _raised_cap(pack: Pack, cap: int) -> Pack:
    data = json.loads(json.dumps(dict(pack.data)))
    data["rules.json"]["brief"]["chorus"]["max_actor_calls"] = cap
    return Pack(data=data)


# -- the queue law (the scene manager) ---------------------------------------


def test_queue_is_presence_pack_order_and_cap(tmp_path: Path) -> None:
    """The chorus is a queue, not a convention (live fire, day1 seed
    123): the tavern scene's queue is the present, actors-declared NPCs
    in pack declaration order, clipped to the per-beat cap; the watch
    change swaps the guard by PRESENCE (the fold reads the projection,
    never a convention about who talked); the PC's departure empties
    the chorus (no declared actor remains at the backyard)."""
    events = run_day1(tmp_path, 123)
    assert speaking_queue(events[:10], pack=PACK) == (GUARD, BARKEEP)
    assert speaking_queue(events[:25], pack=PACK) == (RELIEF, BARKEEP)
    assert speaking_queue(events, pack=PACK) == ()


def test_the_player_and_ambients_are_never_queued(tmp_path: Path) -> None:
    """The kind gate: the player is never queued (mode A owns its call —
    the chorus is mode B's) and an ambient group is never queued (it
    holds records but does not speak, the knower-gate law); a
    cap-raised queue over the tavern scene holds only kind-npc ids."""
    events = run_day1(tmp_path, 123)
    open_cap = _raised_cap(PACK, 9)
    queue = speaking_queue(events[:10], pack=open_cap)
    assert queue == (GUARD, BARKEEP, DRUNK, MAID)
    assert PLAYER not in queue
    assert all(open_cap.kind_of(entity_id) == "npc" for entity_id in queue)
    # the golden fixture's market scene: the crowd is ambient — present
    # in the projection, absent from the chorus by kind.
    assert speaking_queue(_golden_events(), pack=open_cap) == ()


def test_no_chorus_block_is_the_empty_chorus(tmp_path: Path) -> None:
    """The DORMANT gate: a pack without the chorus block runs mode B
    off — the queue is empty, the runs byte-identical (the pack's own
    declaration is the gate, INV-3)."""
    events = run_day1(tmp_path, 123)
    blockless = _mutated_pack(lambda rules: rules["brief"].pop("chorus"))
    assert speaking_queue(events[:25], pack=blockless) == ()


def test_the_actors_entry_is_the_eligibility_gate(tmp_path: Path) -> None:
    """A present NPC without a `brief.actors` entry is not
    chorus-eligible (the pack declares WHO may speak — dropping the
    drunk's entry silences him, the others unaffected; silence is not
    an error)."""
    events = run_day1(tmp_path, 123)
    open_cap = _raised_cap(PACK, 9)
    silenced = _mutated_pack(
        lambda rules: (
            rules["brief"]["chorus"].__setitem__("max_actor_calls", 9),
            rules["brief"]["actors"].pop(DRUNK),
        )
    )
    assert speaking_queue(events[:10], pack=open_cap) == (GUARD, BARKEEP, DRUNK, MAID)
    assert speaking_queue(events[:10], pack=silenced) == (GUARD, BARKEEP, MAID)


def test_the_cap_clips_head_first(tmp_path: Path) -> None:
    """The per-beat actor-call budget: the queue drains head-first —
    `max_actor_calls` clips the declared order, the beyond-cap NPCs
    fall to the L12 template rung (never a blocked beat: the chronicle
    already renders their beats)."""
    events = run_day1(tmp_path, 123)
    one = _raised_cap(PACK, 1)
    assert speaking_queue(events[:10], pack=one) == (GUARD,)


def test_queue_is_a_pure_fold(tmp_path: Path) -> None:
    """Same (log, pack) prefix → same queue: a pure fold, no RNG, no
    wall-clock (INV-2); the queue moves only when the projection moves
    (the watch-change swap)."""
    events = run_day1(tmp_path, 123)
    assert speaking_queue(events[:10], pack=PACK) == speaking_queue(events[:10], pack=PACK)
    assert speaking_queue(events[:10], pack=PACK) != speaking_queue(
        events[:25], pack=PACK
    )


# -- mode B: the knower-parameterized assembly --------------------------------


def test_mode_a_default_is_the_player_byte_identical() -> None:
    """The default law: `knower=None` is mode A (the committed corpus
    bytes) — explicitly passing the player id changes nothing (the
    golden fixture's brief, the zero-regen witness)."""
    events = _golden_events()
    default = render_brief(assemble_brief(events, PACK))
    explicit = render_brief(assemble_brief(events, PACK, knower=PLAYER))
    assert default == explicit


def test_mode_b_renders_the_actors_own_role_and_voice() -> None:
    """The actor's static half: a mode-B brief carries the actor's own
    directives and voice exemplars (the `brief.actors` entry) — never
    the narrator's (mode A's); the drunk's voice is not the guard's."""
    events = _golden_events()
    guard = _block(render_brief(assemble_brief(events, PACK, knower=GUARD)), "directives")
    assert guard == [
        str(line) for line in PACK.rules["brief"]["actors"][GUARD]["directives"]
    ]
    narrator = _block(render_brief(assemble_brief(events, PACK)), "directives")
    assert guard != narrator
    drunk_lines = _block(
        render_brief(assemble_brief(events, PACK, knower=DRUNK)), "voice_exemplars"
    )
    guard_lines = _block(
        render_brief(assemble_brief(events, PACK, knower=GUARD)), "voice_exemplars"
    )
    assert drunk_lines != guard_lines
    assert guard_lines == [
        str(line) for line in PACK.rules["brief"]["actors"][GUARD]["voice_exemplars"]
    ]


def test_mode_b_shared_blocks_stay_shared() -> None:
    """One scene, one ledger, one grammar (L6): the scene_texture
    window, the entity cards, the lore, and the options are the SAME
    bytes for mode A and mode B over the same (log, ledger) — the
    chorus reads the same texture block; the cards are observables, not
    knowledge; the grammar is the door's, not the knower's."""
    events = _golden_events()
    ledger = SceneLedger()
    mode_a = render_brief(assemble_brief(events, PACK, ledger))
    mode_b = render_brief(assemble_brief(events, PACK, ledger, knower=GUARD))
    for block_id in (
        "scene_texture", "present_entities", "scheduled_lore", "active_options",
    ):
        assert _block(mode_a, block_id) == _block(mode_b, block_id)


def _delta_tick(line: str) -> int:
    """The tick of one scene_delta line (`[t <tick>] ...`)."""
    return int(line.split("]", 1)[0].removeprefix("[t ").strip())


def _delta_type(line: str) -> str:
    """The event type of one scene_delta line."""
    return line.split("]", 1)[1].strip().split(":", 1)[0]


def _run_delta_is_leak_free(events: list[Any], knower: str, brief: str) -> None:
    perceived = {
        (event.t, event.type)
        for event in events
        if event.actor == knower
        or any(record.who == knower for record in event.knowledge)
    }
    for line in _block(brief, "scene_delta"):
        assert (_delta_tick(line), _delta_type(line)) in perceived


def test_mode_b_scene_delta_is_the_knowers_perception(tmp_path: Path) -> None:
    """The blind-NPC law, parameterized: every scene_delta line in a
    mode-B brief maps to an event the knower perceived (the actor or a
    knowledge-record holder) — an event nobody told this knower about
    never renders for him. Checked at EVERY beat window the day holds
    (mid-run beats included — the guard's window at the theft beats,
    the empty window after his departure: silence is the honest
    answer, never a leak)."""
    events = run_day1(tmp_path, 123)
    for cut in (13, 16, 20, 25, 30, len(events)):
        brief = render_brief(assemble_brief(events[:cut], knower=GUARD, pack=PACK))
        _run_delta_is_leak_free(events[:cut], GUARD, brief)
    mid = render_brief(assemble_brief(events[:16], knower=GUARD, pack=PACK))
    assert _block(mid, "scene_delta")  # the guard saw the theft beats
    late = render_brief(assemble_brief(events, knower=GUARD, pack=PACK))
    assert _block(late, "scene_delta") == []  # departed: the window is not his


def test_mode_b_recalled_facts_are_the_knowers_own(tmp_path: Path) -> None:
    """The leak surface, closed by construction: every recalled_facts
    line (raw or belief) maps to the knower's own fold — and a token
    held ONLY by the guard never renders in the maid's brief (what you
    do not hold, you do not say)."""
    events = run_day1(tmp_path, 123)
    view = KnowledgeView.from_events(events)
    held_by = {
        knower: {record.knows for record in view.records_of(knower)}
        for knower in (GUARD, BARKEEP, DRUNK, MAID, RELIEF)
    }
    for knower, held in held_by.items():
        brief = render_brief(assemble_brief(events, knower=knower, pack=PACK))
        for line in _block(brief, "recalled_facts"):
            token = (
                line.split()[2] if line.startswith("- belief ")
                else line.split("] ", 1)[1]
            )
            assert token in held
    others = held_by[BARKEEP] | held_by[DRUNK] | held_by[MAID]
    guard_only = held_by[GUARD] - others
    assert guard_only  # the guard's own sighting, unheard by the room
    maid_brief = render_brief(assemble_brief(events, knower=MAID, pack=PACK))
    maid_facts = "\n".join(_block(maid_brief, "recalled_facts"))
    for token in guard_only:
        assert token not in maid_facts


def test_mode_b_beliefs_are_the_knowers_own(tmp_path: Path) -> None:
    """The per-knower traits fold: seed 125's guard crystallizes
    `paranoid_about_thieves` (the iter-55 canonical pin) — the belief
    line leads HIS brief with his own provenance; the relief's brief
    carries his own (the hearsay mint, one source); the maid holds no
    family and renders no belief line at all."""
    events = run_day1(tmp_path, 125)
    guard = _block(
        render_brief(assemble_brief(events, knower=GUARD, pack=PACK)),
        "recalled_facts",
    )
    relief = _block(
        render_brief(assemble_brief(events, knower=RELIEF, pack=PACK)),
        "recalled_facts",
    )
    assert guard[0] == (
        "- belief paranoid_about_thieves (t 360, sources: ev_0002, ev_0017)"
    )
    assert any(
        line.startswith("- belief paranoid_about_thieves (t ") for line in relief
    )
    maid = _block(
        render_brief(assemble_brief(events, knower=MAID, pack=PACK)),
        "recalled_facts",
    )
    assert not [line for line in maid if line.startswith("- belief ")]


def test_mode_b_knower_gate() -> None:
    """The gate: an unknown id, an item, a location, an ambient group,
    or a present-but-undeclared NPC is a loud ValueError — never a
    wrong brief; the player (explicit or default) passes."""
    events = _golden_events()
    for bad in ("npc_nobody_99", "purse_01", "loc_tavern", "npc_market_crowd_01"):
        with pytest.raises(ValueError, match="knower"):
            assemble_brief(events, PACK, knower=bad)
    undeclared = _mutated_pack(lambda rules: rules["brief"]["actors"].pop(GUARD))
    with pytest.raises(ValueError, match="brief.actors"):
        assemble_brief(events, undeclared, knower=GUARD)
    assemble_brief(events, PACK, knower=PLAYER)  # passes: mode A


def test_mode_b_is_deterministic(tmp_path: Path) -> None:
    """Same (log, pack, knower) → same bytes: the knower parameter adds
    no randomness, no wall-clock (INV-2) — the fold is pure."""
    events = run_day1(tmp_path, 123)
    first = render_brief(assemble_brief(events, knower=GUARD, pack=PACK))
    second = render_brief(assemble_brief(events, knower=GUARD, pack=PACK))
    assert first == second


def test_mode_a_corpus_price_is_zero(tmp_path: Path) -> None:
    """The zero-regen landing: mode A over the committed pack (which
    now carries `chorus` + `actors`) is byte-identical to a block-less
    copy — the new pack data is inert on the mode-A path (the pack's
    own declaration is the gate, INV-3; the A/B witness)."""
    events = run_day1(tmp_path, 123)
    blockless = _mutated_pack(
        lambda rules: (
            rules["brief"].pop("chorus"),
            rules["brief"].pop("actors"),
        )
    )
    assert render_brief(assemble_brief(events, PACK)) == render_brief(
        assemble_brief(events, blockless)
    )


# -- the actor call document ---------------------------------------------------


def test_actor_call_carries_the_actor_line() -> None:
    """Mode B's own protocol field: the actor call names whose
    beat-projection it carries (`actor: <id>`, the protocol section's
    first line) — the operator knows whose voice to speak; mode A's
    bytes carry no actor line (the player is the narrator's subject by
    construction — the committed corpus shape)."""
    events = _golden_events()
    actor_doc = narrator_call(events, PACK, SceneLedger(), knower=GUARD)
    tail = actor_doc.splitlines()[-4:]
    assert tail == [
        "## narrator_protocol",
        f"actor: {GUARD}",
        f"anchor: {len(events)}",
        "regen: 0/2",
    ]
    narrator_doc = narrator_call(events, PACK, SceneLedger())
    assert "actor:" not in narrator_doc


def test_actor_call_mode_a_passes_through_unchanged() -> None:
    """The narrator call's mode-A bytes are the committed shape: an
    explicit `knower=<player>` still omits the actor line (mode A is
    mode A however it is spelled)."""
    events = _golden_events()
    default_doc = narrator_call(events, PACK, SceneLedger())
    player_doc = narrator_call(events, PACK, SceneLedger(), knower=PLAYER)
    assert default_doc == player_doc


# -- the leak surface over every declared actor (blind-1's core) ---------------


def test_zero_leaks_on_the_canonical_run(tmp_path: Path) -> None:
    """The phase-4 exit criterion's instrument core: over the canonical
    run (day1, the armed pack), EVERY declared actor's brief is
    leak-free at EVERY beat window — every scene_delta line maps to a
    perceived event, every recalled_facts line maps to a held record
    or belief. The suite the `blind-1` row will extend to the session
    wiring."""
    events = run_day1(tmp_path, 123)
    view = KnowledgeView.from_events(events)
    for knower in sorted(PACK.rules["brief"]["actors"]):
        held = {record.knows for record in view.records_of(knower)}
        for cut in (13, 16, 20, 25, 30, len(events)):
            brief = render_brief(
                assemble_brief(events[:cut], knower=knower, pack=PACK)
            )
            _run_delta_is_leak_free(events[:cut], knower, brief)
            for line in _block(brief, "recalled_facts"):
                token = (
                    line.split()[2] if line.startswith("- belief ")
                    else line.split("] ", 1)[1]
                )
                assert token in held


# -- the lint family ------------------------------------------------------------


def _broken_pack(tmp_path: Path, mutate: Callable[[dict[str, Any]], None]) -> Path:
    target = tmp_path / "broken_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return target


@pytest.mark.parametrize(
    ("label", "mutate"),
    [
        (
            "unknown chorus key",
            lambda r: r["brief"]["chorus"].__setitem__("cadence", 3),
        ),
        (
            "zero cap",
            lambda r: r["brief"]["chorus"].__setitem__("max_actor_calls", 0),
        ),
        (
            "cap not an int",
            lambda r: r["brief"]["chorus"].__setitem__("max_actor_calls", "2"),
        ),
        (
            "empty actors table",
            lambda r: r["brief"].__setitem__("actors", {}),
        ),
        (
            "actor key is not an npc",
            lambda r: r["brief"]["actors"].__setitem__("purse_01", {
                "directives": ["Speak."], "voice_exemplars": [],
            }),
        ),
        (
            "the player carries an actor entry",
            lambda r: r["brief"]["actors"].__setitem__(PLAYER, {
                "directives": ["Speak."], "voice_exemplars": [],
            }),
        ),
        (
            "unknown actor key",
            lambda r: r["brief"]["actors"][GUARD].__setitem__("mood", "dark"),
        ),
        (
            "empty directives",
            lambda r: r["brief"]["actors"][GUARD].__setitem__("directives", []),
        ),
        (
            "directives bust the hard budget",
            lambda r: r["brief"]["actors"][GUARD].__setitem__(
                "directives", ["word " * 90]
            ),
        ),
        (
            "exemplars not strings",
            lambda r: r["brief"]["actors"][GUARD].__setitem__(
                "voice_exemplars", [3]
            ),
        ),
        (
            "notes not a string",
            lambda r: r["brief"]["actors"][GUARD].__setitem__("notes", 7),
        ),
    ],
)
def test_lint_refuses_broken_blocks(
    tmp_path: Path, label: str, mutate: Callable[[dict[str, Any]], None]
) -> None:
    """The closed-vocabulary family: both blocks fail loudly at load —
    dead vocabulary, the player in the actor table, roleless calls,
    budget-busting never-dropped data (the KI#15 family: a typo is a
    load error, never a silent never-rendering entry)."""
    with pytest.raises(PackError):
        load_pack(_broken_pack(tmp_path, mutate))


def test_lint_accepts_the_committed_pack() -> None:
    """The committed pack carries both blocks and loads clean — the
    arming witness."""
    assert "chorus" in PACK.rules["brief"]
    assert sorted(PACK.rules["brief"]["actors"]) == [
        BARKEEP, DRUNK, GUARD, RELIEF, MAID,
    ]


# -- scene-2: the session wiring (the drain, the actor door, the query) -------


def _mediator_session(
    tmp_path: Path, seed: int = 42
) -> tuple[Simulator, Mediator]:
    """A live session at the tavern (the test_mediator pattern): the
    chorus queue over the fresh arrival is (guard, barkeep) — the cap
    clips the tavern's four declared actors to the pack-order head."""
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}])
    mediator = Mediator(sim, PACK, SCHEMA, log, tmp_path / "mediator")
    return sim, mediator


def _reply(tmp_path: Path, name: str, doc: dict[str, Any]) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def test_actor_step_feeds_the_door_as_the_npc(tmp_path: Path) -> None:
    """The actor reply door: a step carrying `actor=<npc>` goes through
    the SAME front door — the committed event's actor IS the NPC
    (INTENT_SCHEMA §9's actor key, mode B's reply path; the player's
    default needs no key — mode A unchanged)."""
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "look_around", "actor": GUARD}])
    sim.close()
    _header, events = read_log(log, SCHEMA)
    assert any(event.actor == GUARD for event in events)


@pytest.mark.parametrize("bad", ["purse_01", "loc_tavern", "npc_unknown", 7])
def test_bad_step_actor_is_a_loud_author_error(
    tmp_path: Path, bad: Any
) -> None:
    """The actor key is an author error when it names anything but a
    pack NPC (an item, a location, an unknown id, a non-string) — the
    loud/soft front-door line (INTENT_SCHEMA §9), never a silent
    player-substitution."""
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000")
    sim.open()
    with pytest.raises(RunnerError, match="actor must be a pack npc id"):
        sim.run_steps([{"intent": "look_around", "actor": bad}])
    sim.close()


def test_actor_steps_chain_like_player_steps(tmp_path: Path) -> None:
    """KI#17's generalization: the runner feeds the next step when the
    CURRENT step's own intent ends — actor steps chain exactly like
    player steps (the mode-B reply lists), and autonomous intents
    (different intent ids) never advance the script."""
    log = tmp_path / "run.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([
        {"intent": "look_around"},
        {"intent": "look_around", "actor": GUARD},
        {"intent": "look_around", "actor": BARKEEP},
    ])
    sim.close()
    _header, events = read_log(log, SCHEMA)
    actors = [event.actor for event in events if event.type == "look_around"]
    assert actors == [PLAYER, GUARD, BARKEEP]


def test_the_drain_hands_actor_calls_after_the_players_beat(
    tmp_path: Path,
) -> None:
    """The wiring: an accepted player beat hands the chorus's calls one
    per queued NPC (head-first, pack order — guard then barkeep at the
    cap-2 tavern); each actor's accept advances the drain; the LAST
    accept closes the beat. The actor calls ride the same files, the
    same reply flow, the same ladder."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))
    assert result.status == "accepted" and result.actor is None
    assert result.call_path is not None  # the chorus's first actor call
    guard_call = result.call_path.read_text(encoding="utf-8")
    assert f"actor: {GUARD}" in guard_call
    result2 = mediator.apply_reply(_reply(tmp_path, "r2.json", {
        "prose": "Easy now. Hands where I can see them.",
    }))
    assert result2.status == "accepted" and result2.actor == GUARD
    assert f"actor: {BARKEEP}" in result2.call_path.read_text(encoding="utf-8")
    result3 = mediator.apply_reply(_reply(tmp_path, "r3.json", {
        "prose": "Ale's on the house.",
    }))
    assert result3.status == "accepted" and result3.actor == BARKEEP
    assert result3.call_path is None  # the drain emptied
    assert not mediator.beat_open
    sim.close()


def test_the_player_dry_closes_the_whole_beat(tmp_path: Path) -> None:
    """Declining the PLAYER's call declines the beat: the chorus never
    starts (the beat's head is its subject — the template rung renders
    the whole beat; no actor call is ever emitted)."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    result = mediator.dry_close()
    assert result.status == "dry" and result.actor is None
    assert not mediator.beat_open
    assert sorted(p.name for p in (tmp_path / "mediator").glob("call_*.md")) == [
        "call_0000.md"
    ]
    sim.close()


def test_actor_dry_skips_and_advances(tmp_path: Path) -> None:
    """`narrate dry` on an ACTOR's call skips that actor (the template
    rung — its beats already render through the chronicle) and hands
    the next queued NPC's call; the last skip closes the beat."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))  # the accept hands the guard's call
    skip = mediator.dry_close()
    assert skip.status == "dry" and skip.actor == GUARD
    assert skip.call_path is not None
    assert f"actor: {BARKEEP}" in skip.call_path.read_text(encoding="utf-8")
    skip2 = mediator.dry_close()
    assert skip2.status == "dry" and skip2.actor == BARKEEP
    assert skip2.call_path is None
    assert not mediator.beat_open
    sim.close()


def test_a_bare_narrate_drops_the_pending_drain_and_the_notes_wait(
    tmp_path: Path,
) -> None:
    """The drop law: a bare `narrate` (emit_call) DROPS a pending drain
    — the unanswered actor calls fall to the template rung (the operator
    moved on; never a blocked beat). The withdrawal notes minted by the
    player's reply wait through the chorus and ride the player's NEXT
    call (BRIEF_SPEC §7.1's subject-scoped note law — the actor calls
    never consume them)."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    _header, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    anchor = len(events)
    result = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The barkeep fidgeted.",
        "proposal": {"expected_event_seq": anchor, "intents": [
            {"kind": "look_around", "actor": BARKEEP,
             "based_on_event_seq": anchor},
        ]},
    }))
    assert result.status == "accepted"  # the barkeep proposal: withdrawn
    guard_call = result.call_path.read_text(encoding="utf-8")
    assert "WITHDRAWN" not in guard_call  # the actor call does not consume
    next_call = mediator.emit_call()  # the drop + the player's next beat
    text = next_call.read_text(encoding="utf-8")
    assert "actor:" not in text  # the player's call, not an actor's
    assert "WITHDRAWN intent look_around" in text  # the notes arrived home
    sim.close()


def test_mid_drain_departure_skips_the_absent_actor(tmp_path: Path) -> None:
    """The live presence re-verification: the world may move between an
    actor's call and its reply (the corpus's own `between` pattern) —
    an NPC no longer present at the current scene is SKIPPED (the
    template rung), never called for a scene it stands outside of."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    accepted = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))
    assert accepted.call_path is not None  # the guard's call is open
    sim.run_steps([{"intent": "move", "target": "loc_backyard"}])  # mid-drain
    skip = mediator.dry_close()  # the guard declines — the scene moved
    assert skip.actor == GUARD
    assert skip.call_path is None  # the barkeep: not present, skipped
    assert not mediator.beat_open
    sim.close()


def test_actor_refusals_regen_then_fall_to_the_template_rung(
    tmp_path: Path,
) -> None:
    """The actor's own L12 ladder: refusals spend the actor exchange's
    budget (a FRESH budget per exchange — the player's spend never
    leaks in), the re-emit carries the actor's own refusal notes, and
    exhaustion drops the actor to the template rung with the notes on
    the result — the drain lives on (the next actor's call awaits)."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    mediator.apply_reply(_reply(tmp_path, "r.json", {"prose": "Warm."}))
    refused = {  # `exits` is pack-modeled — the canon_slot refusal family
        "prose": "A door stood to the north.",
        "texture_delta": {"source": "turn:1", "established": [{
            "scope": "scene:loc_tavern", "slot": "exits", "value": "north",
            "surface": "A door stood to the north.",
        }]},
    }
    first = mediator.apply_reply(_reply(tmp_path, "r1.json", refused))
    assert first.status == "regen" and first.regens_used == 1
    assert first.actor == GUARD  # the fresh budget: 1, not 1 + the player's
    assert "REFUSED" in first.call_path.read_text(encoding="utf-8")
    second = mediator.apply_reply(_reply(tmp_path, "r2.json", refused))
    assert second.status == "regen" and second.regens_used == 2
    third = mediator.apply_reply(_reply(tmp_path, "r3.json", refused))
    assert third.status == "dry" and third.actor == GUARD
    assert any("REFUSED" in note for note in third.notes)  # why it fell
    assert third.call_path is not None  # the barkeep's call: drain lives
    assert mediator.beat_open
    sim.close()


def test_the_actor_reply_feeds_the_callers_intents(tmp_path: Path) -> None:
    """The caller law end-to-end: an actor call's reply feeds the
    ACTOR's proposals through the door (the committed event's actor is
    the NPC — mode B's write path), and the summary counts the feed."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))
    actor_call = result.call_path.read_text(encoding="utf-8")
    anchor = int(
        next(line.split()[1] for line in actor_call.splitlines()
             if line.startswith("anchor:"))
    )
    _header, before = read_log(tmp_path / "run.jsonl", SCHEMA)
    result2 = mediator.apply_reply(_reply(tmp_path, "r2.json", {
        "prose": "Easy now. Hands where I can see them.",
        "proposal": {"expected_event_seq": anchor, "intents": [
            {"kind": "look_around", "actor": GUARD,
             "based_on_event_seq": anchor},
        ]},
    }))
    assert result2.status == "accepted" and result2.actor == GUARD
    _header, after = read_log(tmp_path / "run.jsonl", SCHEMA)
    fresh = after[len(before):]
    assert any(event.actor == GUARD for event in fresh)  # THE DOOR
    assert "BEAT intents: 1 fed, 0 withdrawn" in result2.notes
    sim.close()


# -- scene-2: the keyword query (§3.5's relevance signal) ----------------------


def test_recall_query_is_the_fresh_window_tokens(tmp_path: Path) -> None:
    """The query derivation: the knows tokens the beat window minted
    for the knower, first-seen order, space-joined — leak-free by
    construction (the tokens ARE the knower's own fresh records; the
    pre-first-beat window is the whole log)."""
    events = run_day1(tmp_path, 123)
    assert recall_query(events[:10], PACK, GUARD) == (
        "pc_01_arrived pc_01_reaching_for_oil_lamp_01 noise_in_loc_tavern "
        "figure_reaching_for_purse noise_by_the_bar"
    )
    # the maid's own fresh tokens — never the guard's
    assert "purse_missing" not in recall_query(events[:10], PACK, MAID)


def test_recall_query_empty_when_the_window_mints_nothing(
    tmp_path: Path,
) -> None:
    """The honest empty query: a window that mints nothing for the
    knower yields the empty string (no fabricated signal — the
    two-signal ranking stands; the late-day window is quiet for the
    rotated-out guard)."""
    events = run_day1(tmp_path, 123)
    assert recall_query(events, PACK, GUARD) == ""


def test_present_at_scene_reads_the_live_projection(tmp_path: Path) -> None:
    """The drain's re-verification fold: presence is read from the
    projection at the CURRENT scene — the guard mid-tavern, gone after
    the watch change (the rotation moved him; the fold reads the world,
    never a convention about who talked)."""
    events = run_day1(tmp_path, 123)
    assert present_at_scene(events[:10], PACK, GUARD)
    assert not present_at_scene(events[:25], PACK, GUARD)


def test_the_relevance_term_reranks_the_actors_memory() -> None:
    """§3.5's third signal: with a query, an OLD record sharing words
    with the fresh ones rides UP (the token overlap over the word view
    — rung-independent, pure); without a query the two-signal shape
    stands (mode A's committed bytes). Synthetic records: the fresh
    `ale_order_shouted` query pulls `ale_spilled` above
    `song_by_the_hearth` (recency alone ranks them the other way)."""
    records = (
        ("ev_0000", 2, "ale_spilled"),
        ("ev_0001", 4, "song_by_the_hearth"),
        ("ev_0002", 50, "ale_order_shouted"),
    )
    events = [
        EventRecord(
            id=eid, t=t, type="rumor_told", actor=BARKEEP, cause=None,
            outcome={}, knowledge=(LoggedKnowledgeRecord(
                who=GUARD, channel="told", fidelity="partial",
                knows=knows, at=t, source=eid,
            ),), state_changes=(), hooks=(),
            importance="low", provenance={}, target=None,
        )
        for eid, t, knows in records
    ]
    without = _block(render_brief(assemble_brief(events, PACK, knower=GUARD)), "recalled_facts")
    with_query = _block(render_brief(
        assemble_brief(events, PACK, knower=GUARD, query="ale_order_shouted")
    ), "recalled_facts")
    assert without == [
        "- [t 50, told, partial] ale_order_shouted",
        "- [t 4, told, partial] song_by_the_hearth",
        "- [t 2, told, partial] ale_spilled",
    ]
    assert with_query[:1] == without[:1]  # the fresh record still leads
    assert with_query[1:] == [  # the flip: the old ale record rides up
        "- [t 2, told, partial] ale_spilled",
        "- [t 4, told, partial] song_by_the_hearth",
    ]


def test_mode_a_bytes_ignore_the_relevance_weight(tmp_path: Path) -> None:
    """The corpus price: `relevance_weight` is inert on the mode-A path
    — no query ever arrives there, any weight renders the same bytes
    (the pack-data gate; the zero-regen landing)."""
    events = run_day1(tmp_path, 123)
    zeroed = _mutated_pack(
        lambda rules: rules["brief"]["recalled_facts"].__setitem__(
            "relevance_weight", 0.0
        )
    )
    assert render_brief(assemble_brief(events, PACK)) == render_brief(
        assemble_brief(events, zeroed)
    )


# -- scene-2: the retrieval ladder's first runtime query ----------------------


def test_the_actor_call_carries_query_and_retrieval_lines(
    tmp_path: Path,
) -> None:
    """The actor call's protocol extension (BRIEF_SPEC §7.1): the
    `query:` line (the relevance signal made visible) and the ladder's
    top `retrieval:` rows — dry demand handles with the fidelity and
    the minting event id inline; mode A carries neither."""
    events = run_day1(tmp_path, 123)
    window = events[:10]
    query = recall_query(window, PACK, GUARD)
    index = RetrievalIndex.build(PACK, window)
    assert index is not None  # the committed pack declares the block
    try:
        rows = index.query(query, knower=GUARD)
    finally:
        index.close()
    document = narrator_call(
        window, PACK, SceneLedger(), knower=GUARD, query=query, retrieval=rows,
    )
    tail = document.splitlines()[-8:]
    assert tail == [
        "## narrator_protocol",
        f"actor: {GUARD}",
        "anchor: 10",
        "regen: 0/2",
        "query: pc_01_arrived pc_01_reaching_for_oil_lamp_01 "
        "noise_in_loc_tavern figure_reaching_for_purse noise_by_the_bar",
        "retrieval: fact figure_reaching_for_purse (saw/partial, ev_0002)",
        "retrieval: fact noise_by_the_bar (heard/vague, ev_0002)",
        "retrieval: fact pc_01_reaching_for_oil_lamp_01 (saw/partial, ev_0001)",
    ]
    mode_a = narrator_call(window, PACK, SceneLedger())
    assert "query:" not in mode_a and "retrieval:" not in mode_a


def test_the_mediator_queries_the_ladder_per_actor_call(
    tmp_path: Path,
) -> None:
    """retr-1's DORMANT gate opened: the live drain builds the index and
    queries it per actor call (the mode-B path pays it; mode A never
    does) — the auto-emitted guard call carries the query and the
    ladder's top row for it (the session's own arrival record)."""
    sim, mediator = _mediator_session(tmp_path)
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))
    call = result.call_path.read_text(encoding="utf-8")
    assert "query: pc_01_arrived" in call
    assert "retrieval: fact pc_01_arrived (saw/partial, ev_0000)" in call
    sim.close()


def test_a_blockless_pack_runs_the_ladder_off(tmp_path: Path) -> None:
    """The DORMANT family: a pack without the `retrieval` block keeps
    the query line (the relevance signal is pack-independent — the
    assembler's own overlap) but serves no retrieval rows; the ladder
    is the pack's own declaration, INV-3."""
    blockless = _mutated_pack(lambda rules: rules.pop("retrieval"))
    log = tmp_path / "run.jsonl"
    sim = Simulator(blockless, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}])
    _header, events = read_log(log, SCHEMA)
    query = recall_query(list(events), blockless, GUARD)
    index = RetrievalIndex.build(blockless, list(events))
    assert index is None
    document = narrator_call(
        list(events), blockless, SceneLedger(), knower=GUARD, query=query,
    )
    assert "query: pc_01_arrived" in document
    assert "retrieval:" not in document
    # and the live drain over the blockless pack: the same law
    mediator = Mediator(sim, blockless, SCHEMA, log, tmp_path / "mediator")
    mediator.emit_call()
    result = mediator.apply_reply(_reply(tmp_path, "r.json", {
        "prose": "The common room was warm.",
    }))
    call = result.call_path.read_text(encoding="utf-8")
    assert "query: pc_01_arrived" in call
    assert "retrieval:" not in call
    sim.close()


@pytest.mark.parametrize("seed", range(120, 130))
def test_scene_2_corpus_price_is_zero(seed: int, tmp_path: Path) -> None:
    """The 10-seed day1_full A/B (the retr-1 witness pattern): the
    committed pack (chorus + actors + retrieval + relevance_weight)
    vs the block-less copy — the playscript path never touches the
    mediator, every run byte-identical; the mode-A corpus (the narrator
    corpus 105 + the parse corpus 10 + the T1 golden) replays green in
    the same suite."""
    baseline = tmp_path / "baseline.jsonl"
    sim = Simulator(PACK, seed, baseline, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    blockless = _mutated_pack(
        lambda rules: (
            rules["brief"].pop("chorus"),
            rules["brief"].pop("actors"),
            rules.pop("retrieval"),
            rules["brief"]["recalled_facts"].__setitem__(
                "relevance_weight", 0.0
            ),
        )
    )
    stripped = tmp_path / "stripped.jsonl"
    sim2 = Simulator(blockless, seed, stripped, SCHEMA, commit="0000000")
    sim2.run_playscript(dict(DAY1, seed=seed))
    sim2.close()
    assert baseline.read_bytes() == stripped.read_bytes()


def test_the_actor_call_bytes_are_deterministic(tmp_path: Path) -> None:
    """The D-049 quarantine extends to the actor call: two sessions over
    the same seed assemble the same actor call bytes (the ladder's
    answer is same-environment deterministic — the call document is
    session render state, never canon, never committed)."""
    documents = []
    for run in ("a", "b"):
        target = tmp_path / run
        target.mkdir()
        sim, mediator = _mediator_session(target)
        mediator.emit_call()
        result = mediator.apply_reply(_reply(target, "r.json", {
            "prose": "The common room was warm.",
        }))
        documents.append(result.call_path.read_text(encoding="utf-8"))
        sim.close()
    assert documents[0] == documents[1]
