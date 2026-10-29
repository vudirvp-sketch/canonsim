"""agenda-1 P2 (iter-421) — mode B for a RUNTIME-BORN character: the
archetype role text, the pack's skeleton note, the actor's own anchors, and
the ensemble that makes one archetype-mate sound unlike the other.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: an NPC the pack never wrote a line for can SPEAK — the mode-B
  gate resolves an authored entry OR a profile-archetype entry, the born
  actor's own anchors ride one line above the shared skeletons, the pack's
  note declares the skeletons a support rather than a script, and a pack
  without the generative table keeps today's behaviour byte-for-byte
  (authored entries unchanged, mode A untouched, unresolvable NPCs mute).
- Problem: before this row a born traveller had a name, a profile, a
  drive and a persona line — and no `brief.actors` entry, so the chorus
  could never queue it: the most alive characters in the world were mute
  (measured: 3 born travellers, 0 of them speakable; 7 authored entries).
- Lens: "the gate is the declaration, and the declaration can be
  archetype-keyed" — the same resolution law for the chorus and the
  assembly, one function.
- Prism: BASE (the pack's `brief.archetype_briefs` + `skeleton_note`) vs
  MUTE (both removed — the identical pack minus the generative table).
- Scenario + corpus: the province smoke play (seed 42), the prefix the
  runner holds on the artery — the travellers are born at t=360 and stand
  in the same scene.
- Oracle: `actor_entry`'s origin; the assembled mode-B document's
  directives/voice blocks; `speaking_queue` membership; the mode-A bytes.
- Observed (seed 42): queue `npc_drover_01`, `npc_peddler_01` (cap 2,
  declaration order); the drover's call carries 2 archetype directives +
  the pack's note, then
  `voice: low, trails_off, dry_laugh, never_raises_voice; look:
  freckles_across_nose, squint_left; want: the road's own sign read`, then
  the two fact-free skeletons; the authored Ketta call is byte-identical
  to before (no note, no anchor line); the MUTE arm refuses the same
  call with the gate's ValueError.
- Falsifier: a born actor assembling without the anchor line (the
  individuation channel would be absent); an authored entry gaining the
  note or the anchor line (the authored path would be polluted); mode A
  moving (the generative table must never touch the player's brief).
- Epistemic class: the GATE and the DOCUMENT are FACT (the engine bytes);
  whether a small model then performs a distinct voice is the pilot's
  measurement (`docs/analysis/voice-exemplars-brief-2026-10.md` §6) — this
  row does not claim it.
- Disposition: CONFIRMED on the engine side (seed 42).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from brief.assembler import actor_entry, assemble_brief, render_brief, token_count
from brief.scene import speaking_queue
from core.fold import fold, initial_projection
from core.log import read_log
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
WANDERER = "the_road_wanderer"
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")


def _events() -> list[Any]:
    _, events = read_log(GOLDEN, SCHEMA)
    return events


def _walk_start(events: list[Any]) -> list[Any]:
    cut = next(
        index
        for index, event in enumerate(events)
        if event.type == "move"
        and event.actor == "pc_01"
        and event.target == "loc_keep"
    )
    return events[:cut]


def _blocks(text: str, block_id: str) -> list[str]:
    body = text.split(f"## {block_id}", 1)[1].split("## ", 1)[0]
    return body.strip().splitlines()


def _twin(tmp_path: Path, name: str, mutate: Any) -> Path:
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    entities = json.loads(
        (target / "entities.json").read_text(encoding="utf-8")
    )
    mutate(rules, entities)
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target


# -- the resolution and the document ----------------------------------------


def test_a_born_npc_resolves_to_the_archetype_role_text() -> None:
    """The mode-B gate resolves a runtime-born npc through its PROFILE's
    archetype: `actor_entry` answers ('archetype', row) — the one authored
    set every carrier of the archetype rides. The assembled document then
    carries the archetype's directives, the pack's skeleton note (the
    no-clamp statement), the actor's OWN anchors as one line at generation
    distance, and the two fact-free skeletons in declaration order."""
    pack = load_pack(PACK_DIR)
    events = _walk_start(_events())
    state = fold(events, initial_projection(pack.entities))
    origin, entry = actor_entry(pack, state, "npc_drover_01")
    assert origin == "archetype"
    assert entry is pack.rules["brief"]["archetype_briefs"][WANDERER]

    text = render_brief(
        assemble_brief(events, pack, knower="npc_drover_01")
    )
    directives = _blocks(text, "directives")
    assert directives[:2] == entry["directives"]
    assert directives[2] == pack.rules["brief"]["skeleton_note"]  # last
    voice = _blocks(text, "voice_exemplars")
    assert voice[0] == (
        "voice: low, trails_off, dry_laugh, never_raises_voice; "
        "look: freckles_across_nose, squint_left; "
        "want: the road's own sign read"
    )
    assert voice[1:] == entry["voice_exemplars"]
    # the never-dropped system role fits its own hard budget by construction
    hard = pack.rules["brief"]["blocks"]["directives"]["hard"]
    assert sum(token_count(line) for line in directives) <= hard


def test_the_authored_entry_outranks_the_archetype(tmp_path: Path) -> None:
    """The two tiers REPLACE, never merge: an npc with both an authored
    `brief.actors` row and a resolving archetype gets the authored text
    alone — no pack note, no anchor line (the hand-written entry already
    carries the voice)."""
    def authored(rules: Any, _entities: Any) -> None:
        rules["brief"]["actors"]["npc_drover_01"] = {
            "directives": ["Speak as yourself, one utterance; the log is the canon."],
            "voice_exemplars": ["\"The herd knows the road.\""],
        }

    pack = load_pack(_twin(tmp_path, "authored", authored))
    events = _walk_start(_events())
    state = fold(events, initial_projection(pack.entities))
    origin, entry = actor_entry(pack, state, "npc_drover_01")
    assert origin == "authored"
    assert entry["voice_exemplars"] == ["\"The herd knows the road.\""]
    text = render_brief(
        assemble_brief(events, pack, knower="npc_drover_01")
    )
    directives = _blocks(text, "directives")
    assert directives == entry["directives"]  # no skeleton note
    assert _blocks(text, "voice_exemplars") == entry["voice_exemplars"]


def test_the_chorus_queues_a_born_npc(tmp_path: Path) -> None:
    """The chorus gate reads the SAME resolution law: the born travellers
    enter the queue (declaration order, capped by `max_actor_calls`), and
    with the generative table removed the identical scene queues nobody —
    mute stays the honest default."""
    events = _walk_start(_events())
    pack = load_pack(PACK_DIR)
    queue = speaking_queue(events, pack)
    assert queue == ("npc_drover_01", "npc_peddler_01")  # cap 2, pack order
    assert set(queue) <= set(TRAVELLERS)

    def no_table(rules: Any, _entities: Any) -> None:
        rules["brief"].pop("archetype_briefs", None)
        rules["brief"].pop("skeleton_note", None)

    muted = load_pack(_twin(tmp_path, "mute", no_table))
    assert speaking_queue(events, muted) == ()
    with pytest.raises(ValueError, match="resolves to no role text"):
        assemble_brief(events, muted, knower="npc_drover_01")


def test_mode_a_is_byte_identical_without_the_table(tmp_path: Path) -> None:
    """INERT-FIRST at the brief's bytes: the generative table is a mode-B
    surface only — the player's brief is byte-identical with it and
    without it, and the authored mode-B calls are untouched (Ketta carries
    no note and no anchor line)."""
    events = _walk_start(_events())
    base = load_pack(PACK_DIR)

    def no_table(rules: Any, _entities: Any) -> None:
        rules["brief"].pop("archetype_briefs", None)
        rules["brief"].pop("skeleton_note", None)

    stripped = load_pack(_twin(tmp_path, "inert", no_table))
    assert render_brief(assemble_brief(events, base)) == render_brief(
        assemble_brief(events, stripped)
    )
    assert render_brief(
        assemble_brief(events, base, knower="npc_weirkeeper_01")
    ) == render_brief(
        assemble_brief(events, stripped, knower="npc_weirkeeper_01")
    )
    ketta = _blocks(
        render_brief(assemble_brief(events, base, knower="npc_weirkeeper_01")),
        "voice_exemplars",
    )
    assert ketta[0].startswith('"')  # the authored exemplars, no anchor line


def test_an_unresolvable_npc_stays_mute() -> None:
    """Neither an authored entry nor a profile: the gate refuses (the pack's
    own declaration is the gate — no generic default profile is invented,
    because a default produces wallpaper and hides the missing content)."""
    pack = load_pack(PACK_DIR)
    events = _walk_start(_events())
    state = fold(events, initial_projection(pack.entities))
    assert actor_entry(pack, state, "npc_winterkin_01") is None
    with pytest.raises(ValueError, match="resolves to no role text"):
        assemble_brief(events, pack, knower="npc_winterkin_01")


# -- the lint's refusals ----------------------------------------------------


def test_the_lint_refuses_the_malformed_forms(tmp_path: Path) -> None:
    """Nine dead shapes, each refused at LOAD: an entry for an undeclared
    archetype, an unknown entry key, empty directives, directives over the
    hard budget, directives + note over the budget (the assembled system
    role never drops a line), the table without a psyche block, an empty
    skeleton note, a note with no table to serve (dead data), and an empty
    table."""

    wanderer = "the_road_wanderer"

    def unknown_archetype(rules: Any, _e: Any) -> None:
        rules["brief"]["archetype_briefs"]["the_ghost"] = {
            "directives": ["Speak as yourself."],
            "voice_exemplars": [],
        }

    def unknown_key(rules: Any, _e: Any) -> None:
        rules["brief"]["archetype_briefs"][wanderer]["style"] = "clipped"

    def empty_directives(rules: Any, _e: Any) -> None:
        rules["brief"]["archetype_briefs"][wanderer]["directives"] = []

    def over_budget(rules: Any, _e: Any) -> None:
        hard = rules["brief"]["blocks"]["directives"]["hard"]
        rules["brief"]["archetype_briefs"][wanderer]["directives"] = [
            "word " * (hard + 1)
        ]

    def note_overflows(rules: Any, _e: Any) -> None:
        rules["brief"]["skeleton_note"] = "word " * 80

    def no_psyche(rules: Any, _e: Any) -> None:
        rules.pop("psyche", None)

    def empty_note(rules: Any, _e: Any) -> None:
        rules["brief"]["skeleton_note"] = "   "

    def note_without_table(rules: Any, _e: Any) -> None:
        rules["brief"].pop("archetype_briefs")

    def empty_table(rules: Any, _e: Any) -> None:
        rules["brief"]["archetype_briefs"] = {}

    for name, mutate in (
        ("archetype", unknown_archetype),
        ("key", unknown_key),
        ("directives", empty_directives),
        ("budget", over_budget),
        ("note", note_overflows),
        ("psyche", no_psyche),
        ("note-empty", empty_note),
        ("note-orphan", note_without_table),
        ("table-empty", empty_table),
    ):
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate))
