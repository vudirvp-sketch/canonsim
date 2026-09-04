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
from core.knowledge import KnowledgeView
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack

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
