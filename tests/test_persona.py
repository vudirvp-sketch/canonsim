"""agenda-1 P2 (iter-419) — the BORN appearance and voice anchors: the
draw's laws, the lazy birth at the canon birth, the brief's read surface,
and the witness with its ablation.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a person's PRESENTATION — 2-4 physical facts and 3-4 voice
  properties — is generated from pack data at the canon birth (never
  hand-written per NPC) and reaches the narrator through the brief's
  entity card, while a pack that arms no anchor keeps every byte.
- Problem: before this row the three road travellers had a born name and
  a born profile but no body and no voice; a narrator meeting them had
  to invent the weather-worn face and could reinvent it every beat
  (iter-416 §12's measured concern: first a stammerer, a year later a
  reciter).
- Lens: "the birth is live, the pool is the cause, and nothing else
  moves" → the born-origin perturbation and the anchor-block ablation
  against ONE committed corpus.
- Prism: BASE (the committed pack: `generated_look`/`generated_voice` on
  the three travellers + the two pools) vs NO-ANCHORS (the declarations
  AND both blocks removed — nothing is born; the lint refuses a pool
  without a consumer, so one cannot be removed alone).
- Scenario + corpus: the province smoke play (seed 42) — the road traffic
  condenses at t=360 on the runner's own road, so the anchors are born
  there. No committed fixture is written by this test: the witness lives
  in tmp twins (PACK_SPEC §8); the committed province golden's own delta
  is `tests/test_t1_province.py`'s pin.
- Oracle: the `road_musters` event's state_changes (the born `look` /
  `voice` props beside the born names and profiles); the brief's entity
  cards (`look=` / `voice=` segments); `modeled_vocabulary` (the anchor
  words become grounded); the scanned/rendered surfaces (the entity view
  never prints a Python list).
- Observed (seed 42, measured): drover — look `freckles_across_nose,
  squint_left`, voice `low, trails_off, dry_laugh, never_raises_voice`;
  peddler — look `chapped_hands, gap_tooth, crooked_nose`, voice
  `dry_laugh, water_slang, never_raises_voice`; carrier — look
  `sun_cracked_lips, chapped_hands`, voice `clipped, flat,
  never_raises_voice, counts_under_breath`. Two draws per stream (the
  count + the combinatorial pick), zero substantive draws
  (`fingerprint == 0`), the born names and profiles unchanged.
- Falsifier: NO-ANCHORS birthing an anchor (the birth is not the switch);
  the briefs differing by anything but the anchor segments (the birth
  moved other canon); the drawn tokens leaving the declared pool or the
  dose band (the draw's shape is broken).
- Epistemic class: measured, deterministic per seed. The narrator's USE
  of the anchor (does the model hold the face?) is a reading measurement,
  never this row's claim — the honest boundary iter-416 §12 names.
- Disposition: CONFIRMED at the measured band (seed 42).
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from brief.assembler import assemble_brief, render_brief
from brief.scan import modeled_vocabulary
from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import PackError, load_pack
from core.persona import (
    GENERATED_LOOK_KEY,
    GENERATED_VOICE_KEY,
    LOOK_BLOCK,
    LOOK_MAX,
    LOOK_MIN,
    LOOK_PROP,
    VOICE_BLOCK,
    VOICE_MAX,
    VOICE_MIN,
    VOICE_PROP,
    PersonaError,
    materialize_anchors,
)
from core.rng import RngBank, look_stream_name, voice_stream_name

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")


# -- the twin ---------------------------------------------------------------


def _twin(
    tmp_path: Path,
    name: str,
    *,
    armed: bool = True,
    mutate: Any = None,
) -> Path:
    """The committed pack copied into tmp and edited — never a committed
    edit (PACK_SPEC §8: the witness lives in the twin). `armed=False`
    removes BOTH halves of each anchor origin (the declarations and the
    blocks — the lint refuses a pool without a consumer, so one cannot be
    removed alone); `mutate` is the malformed forms' hook (raises at load,
    never at run)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if not armed:
        for record in entities["npcs"]:
            record.pop(GENERATED_LOOK_KEY, None)
            record.pop(GENERATED_VOICE_KEY, None)
        rules.pop(LOOK_BLOCK, None)
        rules.pop(VOICE_BLOCK, None)
    if mutate is not None:
        mutate(rules, entities)
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target


def _run(pack_dir: Path, tmp_path: Path, name: str) -> list[Any]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(
        pack, SCRIPT["seed"], log, SCHEMA, commit="0000000"
    )
    sim.run_playscript(SCRIPT)
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events


class _Duck(SimpleNamespace):
    """The draw-law stub: the two pools plus the npc records (duck-typed —
    the materializer never imports pack.py at runtime)."""


def _duck_pack(*npcs: dict[str, Any]) -> _Duck:
    rules = {
        LOOK_BLOCK: {
            "pools": [
                {"id": "faces", "tokens": ["a_fact", "b_fact", "c_fact"]},
            ],
        },
        VOICE_BLOCK: {
            "pools": [
                {
                    "id": "voices",
                    "tokens": ["a_voice", "b_voice", "c_voice", "d_voice"],
                },
            ],
        },
    }
    records = list(npcs)
    return _Duck(
        rules=rules,
        entities={"npcs": records},
        entity=lambda eid: next((r for r in records if r["id"] == eid), None),
    )


# -- the draw's laws --------------------------------------------------------


def test_the_birth_is_lazy_deterministic_and_first_commit_wins() -> None:
    """The birth is TWO draws per prop on the prop's own stream (the count
    inside the dose band, then the combinatorial pick): the same seed
    answers the same anchors, the tokens keep the POOL's declaration
    order (byte determinism), both props are born look-before-voice, and
    an anchor already in the folded projection is canon — skipped, never
    redrawn (the D-054 twin)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    npc = TRAVELLERS[0]
    births = materialize_anchors(RngBank(42), pack, projection, npc)
    assert [birth.entity for birth in births] == [npc, npc]
    assert [birth.prop for birth in births] == [LOOK_PROP, VOICE_PROP]
    assert [birth.from_ for birth in births] == [None, None]
    look, voice = (birth.to_ for birth in births)
    assert look == ["freckles_across_nose", "squint_left"]
    assert voice == ["low", "trails_off", "dry_laugh", "never_raises_voice"]
    pool = {
        row["id"]: row["tokens"]
        for row in pack.rules[LOOK_BLOCK]["pools"]
    }["lowland_road"]
    assert [token for token in pool if token in look] == look  # pool order

    bank = RngBank(42)
    again = materialize_anchors(bank, pack, projection, npc)
    assert again == births  # same seed, same streams, same anchors
    assert bank.count(look_stream_name(npc)) == 2  # the count + the pick
    assert bank.count(voice_stream_name(npc)) == 2
    assert bank.fingerprint == 0  # never a substantive draw

    state = {
        npc: {LOOK_PROP: look, VOICE_PROP: voice},
    }
    assert materialize_anchors(bank, pack, state, npc) == ()  # no redraw


def test_the_unarmed_law_is_total() -> None:
    """No declaration answers () BEFORE any stream is touched — zero
    assures, zero draws, the anchor streams never even registered (the
    68a pattern; the unarmed corpora byte-identical by construction)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    bank = RngBank(42)
    for npc in ("npc_weirkeeper_01", "pc_01", "npc_smelter_01"):
        assert materialize_anchors(bank, pack, projection, npc) == ()
    assert bank.fingerprint == 0
    with pytest.raises(KeyError):
        bank.count(look_stream_name("npc_weirkeeper_01"))  # laziness is total


def test_the_drawn_anchors_obey_the_authoring_shape() -> None:
    """Every born anchor passes the AUTHORED shape by construction: a list
    of UNIQUE tokens drawn from the DECLARED pool, inside the authoring
    dose band (2-4 facts, 3-4 voice properties — `live_char_guide`'s
    measured dose), in the pool's declaration order."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    pools = {
        record["id"]: {
            LOOK_BLOCK: next(
                row["tokens"] for row in pack.rules[LOOK_BLOCK]["pools"]
                if row["id"] == record[GENERATED_LOOK_KEY]
            ),
            VOICE_BLOCK: next(
                row["tokens"] for row in pack.rules[VOICE_BLOCK]["pools"]
                if row["id"] == record[GENERATED_VOICE_KEY]
            ),
        }
        for record in pack.entities["npcs"]
        if record.get(GENERATED_LOOK_KEY) is not None
    }
    assert set(pools) == set(TRAVELLERS)
    for seed in range(1, 21):
        for npc in TRAVELLERS:
            births = materialize_anchors(
                RngBank(seed), pack, projection, npc
            )
            values = {birth.prop: birth.to_ for birth in births}
            for block, prop, low, high in (
                (LOOK_BLOCK, LOOK_PROP, LOOK_MIN, LOOK_MAX),
                (VOICE_BLOCK, VOICE_PROP, VOICE_MIN, VOICE_MAX),
            ):
                tokens = values[prop]
                assert low <= len(tokens) <= high
                assert len(set(tokens)) == len(tokens)  # no repeated fact
                assert set(tokens) <= set(pools[npc][block])
                assert [t for t in pools[npc][block] if t in tokens] == tokens


def test_the_declarations_are_add_safe() -> None:
    """D-079's add-safety at anchor granularity: one stream per prop per
    npc — drawing npc_y's anchors first shifts neither npc_x's anchors
    nor a canon check draw, and the look and voice halves are SEPARATE
    streams of the same npc (arming one cannot move the other)."""
    x = {
        "id": "npc_x",
        GENERATED_LOOK_KEY: "faces",
        GENERATED_VOICE_KEY: "voices",
    }
    y = {
        "id": "npc_y",
        GENERATED_LOOK_KEY: "faces",
        GENERATED_VOICE_KEY: "voices",
    }
    pack = _duck_pack(x, y)
    state: dict[str, dict[str, Any]] = {"npc_x": {}, "npc_y": {}}
    alone = materialize_anchors(RngBank(42), pack, state, "npc_x")
    bank = RngBank(42)
    materialize_anchors(bank, pack, state, "npc_y")
    after = materialize_anchors(bank, pack, state, "npc_x")
    assert after == alone
    assert bank.fingerprint == 0
    assert bank.count(look_stream_name("npc_x")) == 2
    assert bank.count(voice_stream_name("npc_x")) == 2


def test_the_post_lint_backstop_is_loud() -> None:
    """A declaration the lint would refuse cannot pass load — the runtime
    backstop raises loudly anyway (duck-typed packs, the honest path)."""
    npc = {
        "id": "npc_x",
        GENERATED_LOOK_KEY: "faces",
        GENERATED_VOICE_KEY: "voices",
    }
    no_block = _duck_pack(npc)
    no_block.rules.pop(LOOK_BLOCK)
    with pytest.raises(PersonaError, match="no appearance block"):
        materialize_anchors(RngBank(42), no_block, {"npc_x": {}}, "npc_x")

    no_pool = _duck_pack(npc)
    no_pool.rules[LOOK_BLOCK]["pools"] = []
    with pytest.raises(PersonaError, match="no row"):
        materialize_anchors(RngBank(42), no_pool, {"npc_x": {}}, "npc_x")

    empty = _duck_pack(npc)
    empty.rules[LOOK_BLOCK]["pools"] = [{"id": "faces", "tokens": []}]
    with pytest.raises(PersonaError, match="no tokens"):
        materialize_anchors(RngBank(42), empty, {"npc_x": {}}, "npc_x")


# -- the brief's read surface (the witness) ---------------------------------


def _walk_start(events: list[Any]) -> list[Any]:
    """The log prefix the province smoke's runner holds while standing on
    the artery: everything before the walk leaves the river road for the
    keep — the travellers' own road. The cards of that prefix are the
    witness's read surface."""
    cut = next(
        index
        for index, event in enumerate(events)
        if event.type == "move"
        and event.actor == "pc_01"
        and event.target == "loc_keep"
    )
    return events[:cut]


def test_the_brief_card_renders_the_born_anchors(tmp_path: Path) -> None:
    """The consumer law: the born anchors reach the narrator through the
    entity cards (`look=` / `voice=`), the SAME corpus without the born
    origin renders no anchor segment, and the two briefs differ by
    NOTHING ELSE (the birth changed this one event and no other byte)."""
    base_events = _run(_twin(tmp_path, "base"), tmp_path, "base.jsonl")
    none_events = _run(
        _twin(tmp_path, "none", armed=False), tmp_path, "none.jsonl"
    )
    base = render_brief(assemble_brief(_walk_start(base_events), load_pack(PACK_DIR)))
    none = render_brief(
        assemble_brief(_walk_start(none_events), load_pack(PACK_DIR))
    )
    for npc in TRAVELLERS:
        assert f"- {npc} (" in base
    assert "look=" in base and "voice=" in base
    assert "look=" not in none and "voice=" not in none
    anchor_segment = re.compile(r" (?:look|voice)=[^\s]+")
    assert anchor_segment.sub("", base) == none, (
        "the born anchors must be the ONLY difference between the arms"
    )
    assert base.count("look=") == len(TRAVELLERS)
    assert base.count("voice=") == len(TRAVELLERS)


def test_the_scan_vocabulary_grounds_the_anchor_words(tmp_path: Path) -> None:
    """`modeled_vocabulary` reads the anchor POOLS' words (the words the
    birth can ever draw), so a narrator's "the burn scar on his forearm"
    is grounded — and a pack with no anchor block does not hold them (the
    existence law: the manifest is the pack's declared vocabulary, never
    one session's drawn set)."""
    pack = load_pack(PACK_DIR)
    words = modeled_vocabulary(pack)
    for word in ("freckles", "squint", "scar", "forearm", "clipped", "slang"):
        assert word in words
    stripped = load_pack(_twin(tmp_path, "scan", armed=False))
    stripped_words = modeled_vocabulary(stripped)
    assert "freckles" not in stripped_words
    assert "clipped" not in stripped_words


def test_the_birth_is_the_switch_and_nothing_else_moves(tmp_path: Path) -> None:
    """The canonical record: the anchors ride the condensation's OWN event
    (one member, one block: membership, name, profile, look, voice), the
    born names and profiles are IDENTICAL between the arms, and the
    NO-ANCHORS arm births no anchor at all."""
    base_events = _run(_twin(tmp_path, "record"), tmp_path, "record.jsonl")

    def changes(events: list[Any], prop: str) -> list[Any]:
        return [
            change.to_
            for event in events
            if event.type == "road_musters"
            for change in event.state_changes
            if change.prop == prop
        ]

    assert changes(base_events, LOOK_PROP) == [
        ["freckles_across_nose", "squint_left"],
        ["chapped_hands", "gap_tooth", "crooked_nose"],
        ["sun_cracked_lips", "chapped_hands"],
    ]
    assert changes(base_events, VOICE_PROP) == [
        ["low", "trails_off", "dry_laugh", "never_raises_voice"],
        ["dry_laugh", "water_slang", "never_raises_voice"],
        ["clipped", "flat", "never_raises_voice", "counts_under_breath"],
    ]
    per_member = [
        [change.prop for change in event.state_changes
         if change.entity == npc]
        for event in base_events
        if event.type == "road_musters"
        for npc in TRAVELLERS
    ]
    assert per_member == [
        ["member_of", "name", "psyche", LOOK_PROP, VOICE_PROP],
    ] * len(TRAVELLERS)
    none_events = _run(
        _twin(tmp_path, "plain", armed=False), tmp_path, "plain.jsonl"
    )
    assert changes(none_events, LOOK_PROP) == []
    assert changes(none_events, LOOK_PROP + "x") == []
    assert changes(base_events, "name") == changes(none_events, "name")
    assert changes(base_events, "psyche") == changes(none_events, "psyche")


def test_the_state_view_skips_the_anchor_props() -> None:
    """The `state` report renders SCALAR props only: the anchors are token
    LISTS (canon data), so `render_entity_view` never prints a Python list
    repr for them — the log's own state_changes carry the birth, the view
    stays a scalar state line surface."""
    from render.chronicle import render_entity_view

    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    births = materialize_anchors(
        RngBank(42), pack, projection, TRAVELLERS[0],
    )
    for birth in births:
        projection[TRAVELLERS[0]][birth.prop] = birth.to_
    text = render_entity_view(
        (), projection, pack, TRAVELLERS[0], 42,
    )
    assert LOOK_PROP not in text
    assert "freckles" not in text
    assert "voice" not in text
    assert "[" not in text


# -- the lint's refusals ----------------------------------------------------


def test_the_lint_refuses_the_malformed_forms(tmp_path: Path) -> None:
    """Eleven dead shapes, each refused at LOAD (never a silent ignore):
    an unknown block key, an unknown pool key, a duplicate pool id, a pool
    below the dose floor, a duplicate token, a non-snake token, an
    undeclared pool in a declaration, a declaration on a non-condensing
    npc, a pool no npc consumes, a raw anchor on the npc RECORD (the card
    reads the fold), and a declaration left behind by the block's removal
    (the orphan origin — the complete ablation's law)."""

    def unknown_block_key(rules: dict[str, Any], _e: Any) -> None:
        rules[LOOK_BLOCK]["palette"] = []

    def unknown_pool_key(rules: dict[str, Any], _e: Any) -> None:
        rules[LOOK_BLOCK]["pools"][0]["values"] = []

    def duplicate_pool(rules: dict[str, Any], _e: Any) -> None:
        rules[LOOK_BLOCK]["pools"].append(
            dict(rules[LOOK_BLOCK]["pools"][0])
        )

    def below_floor(rules: dict[str, Any], _e: Any) -> None:
        rules[LOOK_BLOCK]["pools"][0]["tokens"] = ["only_one"]

    def duplicate_token(rules: dict[str, Any], _e: Any) -> None:
        tokens = rules[LOOK_BLOCK]["pools"][0]["tokens"]
        tokens[1] = tokens[0]

    def bad_token(rules: dict[str, Any], _e: Any) -> None:
        rules[LOOK_BLOCK]["pools"][0]["tokens"][0] = "Not A Token"

    def undeclared_pool(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record[GENERATED_LOOK_KEY] = "no_such_pool"

    def not_condensing(rules: dict[str, Any], entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record.pop(GENERATED_LOOK_KEY, None)
            if record["id"] == "npc_smelter_01":
                record[GENERATED_LOOK_KEY] = rules[LOOK_BLOCK]["pools"][1]["id"]

    def dead_pool(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[2]:
                record.pop(GENERATED_LOOK_KEY, None)

    def raw_record_prop(_rules: Any, entities: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == "npc_weirkeeper_01":
                record[LOOK_PROP] = ["burn_scar_forearm"]

    def orphan_origin(rules: dict[str, Any], _entities: Any) -> None:
        rules.pop(LOOK_BLOCK, None)

    for name, mutate in (
        ("block-key", unknown_block_key),
        ("pool-key", unknown_pool_key),
        ("duplicate-pool", duplicate_pool),
        ("floor", below_floor),
        ("duplicate-token", duplicate_token),
        ("token", bad_token),
        ("undeclared-pool", undeclared_pool),
        ("condense", not_condensing),
        ("dead-pool", dead_pool),
        ("raw-record", raw_record_prop),
        ("orphan", orphan_origin),
    ):
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate=mutate))
