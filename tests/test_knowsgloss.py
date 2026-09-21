"""rs-1 — the told-fact gloss boundary (iter-188, the owner's W5
decomposition call, finding 3: raw machine IDs in the reader surface
are an engineering presentation bug, fixed at the boundary/mapping
only — never a worldbuilding task).

The bug (the owner's observed surface, the annual calendar run): the
knowledge machinery mints COMPOSITE TOKENS from the action knowledge
blocks' patterns — `{present}_present`, `rambling_by_{actor}`,
`conversation_with_{target}` — whose slot values are ENTITY IDS. When
such a token rides a telling (the `rumor_told` line's `{knows}` slot),
the reader saw the raw machine string: "the factor's runner tells
Maren: npc_corporal_01_present." The fix: one boundary — the pack
declares a `knows` gloss table in templates.json (the mint pattern →
the reader prose), the renderer maps the token through it with display
names, and an unmatched token renders dry and honest (the foreign-log
fallback). The LOG is untouched (the tokens are canon; the gloss is
read-side only) — zero corpus price by construction.

The claim packet (TEST_PLAN §9):

- Claim: no raw entity id reaches the tale through the knowledge
  surface; every templated mint shape carries a pack-declared gloss.
- Lens(es): the reader-surface boundary (the tale lines); the
  coverage lens (every pack's mint vocabulary vs its gloss table).
- Prism: the renderer-level unit over hand-built rumor events; the
  committed calendar run (the owner's observed surface); the
  five-pack census walk.
- Oracle: the rendered tale text (no id-shaped token; the glossed
  prose present).
- Falsifier: any `npc_*`/`loc_*`/`pc_*`/item-id substring in a
  rendered tale line; a templated knows shape with no table entry.
- Expected evidence: the glossed rumor lines; the census green.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  calendar run renders "Ferra is there." where the raw
  `npc_corporal_01_present` stood).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residue recorded in TASKS rs-1:
  LITERAL fact tokens — `purse_missing`, the read-hinge secrets —
  render dry as-is by design; they carry no entity ids, and their
  rendering quality is the probe's boundary to name, never a
  preemptive renderer feature).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import (
    _Positions,  # the matcher's own fold surface
    compile_glosses,
    gloss_knows,
    render_chronicle,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
PACKS = (
    "tavern_pack",
    "road_pack",
    "province_pack",
    "grim_pack",
    "pressure_pack",
)

#: The composite tokens the owner's observed tale carried raw (the
#: calendar run, seed 42 — the W5 feedback's named leak class).
_OBSERVED_TOKENS = (
    "npc_corporal_01_present",
    "npc_marketmistress_01_present",
    "npc_malby_crowd_01_present",
    "tally_staff_01_present",
    "pay_tin_01_present",
    "npc_sergeant_01_present",
    "rambling_by_npc_marketmistress_01",
    "conversation_with_npc_marketmistress_01",
)

_ID_SHAPE = re.compile(r"\b(?:npc|loc|pc|grp|ambient)_[a-z0-9_]+")


def _rumor(token: str, t: int = 100) -> EventRecord:
    """One medium-importance rumor event carrying the token — the
    exact surface the owner observed (the told fact renders in the
    `{knows}` slot)."""
    return EventRecord(
        id=f"ev_{t:04d}", t=t, type="rumor_told", actor="pc_01",
        target="npc_marketmistress_01", cause=None,
        outcome={"accepted": True, "score": 60, "knows": token,
                 "fidelity": "partial"},
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": 42},
    )


# -- the renderer-level boundary (the unit arm) ----------------------------------


def test_the_observed_tokens_render_glossed() -> None:
    """Every composite token from the owner's observed tale maps to
    reader prose with DISPLAY NAMES — no machine shape survives the
    boundary, the entity ids re-rendered through the fold-aware
    display (the pack's authored names)."""
    pack = load_pack(PACK_DIR)
    glosses = compile_glosses(pack.templates)
    positions = _Positions(pack)
    rendered = {
        token: gloss_knows(glosses, pack, positions, token)
        for token in _OBSERVED_TOKENS
    }
    assert rendered["npc_corporal_01_present"] == "Ferra is there"
    assert rendered["tally_staff_01_present"] == "the tally staff is there"
    assert rendered["pay_tin_01_present"] == "the garrison pay tin is there"
    assert rendered["npc_malby_crowd_01_present"] == "the market queue is there"
    assert (
        rendered["rambling_by_npc_marketmistress_01"] == "rambling from Maren"
    )
    assert rendered["conversation_with_npc_marketmistress_01"] == (
        "a conversation with Maren"
    )
    for token, prose in rendered.items():
        assert _ID_SHAPE.search(prose) is None, (token, prose)


def test_the_rumor_line_renders_the_gloss_in_the_tale() -> None:
    """The line itself: the `{knows}` slot carries the glossed prose —
    the template consumes it with no other change (the boundary is the
    slot's own mapping, never a template rewrite)."""
    pack = load_pack(PACK_DIR)
    tale = render_chronicle([_rumor("npc_corporal_01_present")], pack, seed=42)
    assert "the factor's runner tells Maren: Ferra is there." in tale
    assert "npc_corporal_01" not in tale


def test_the_foreign_token_falls_back_dry() -> None:
    """A token no table entry matches renders UNCHANGED — the dry
    honest fallback (a foreign log's fact names are not the renderer's
    to invent), never an error mid-render."""
    pack = load_pack(PACK_DIR)
    glosses = compile_glosses(pack.templates)
    positions = _Positions(pack)
    assert gloss_knows(
        glosses, pack, positions, "some_foreign_fact"
    ) == "some_foreign_fact"
    assert gloss_knows(glosses, pack, positions, "") == ""
    assert gloss_knows(glosses, pack, positions, None) is None


def test_the_matcher_shapes() -> None:
    """The pattern arithmetic, pinned per shape: the suffix form
    (`{present}_present`), the prefix form (`conversation_with_...`),
    the infix form (`{actor}_left_toward_{target}`), the literal form,
    and the refusals (trailing content past the last anchor; a
    non-entity texture noun passing through raw)."""
    pack = load_pack(PACK_DIR)
    glosses = compile_glosses(pack.templates)
    positions = _Positions(pack)
    g = lambda token: gloss_knows(glosses, pack, positions, token)  # noqa: E731
    assert g("pc_01_left_toward_loc_malby") == (
        "the factor's runner left toward Malby, the market town"
    )
    assert g("scene_loc_crofts") == "the lay of the smelt crofts"
    assert g("details_pay_tin_01") == "the details of the garrison pay tin"
    assert g("pc_01_holds_the_purse") == "the factor's runner holds the purse"
    # the refusals: trailing content, a missing anchor
    assert g("npc_corporal_01_present_extra") == "npc_corporal_01_present_extra"
    assert g("no_anchor_here") == "no_anchor_here"


# -- the committed calendar run (the owner's observed surface) --------------------


def test_the_calendar_tale_carries_no_raw_ids(tmp_path: Path) -> None:
    """The regression on the exact observed surface: the annual run
    (seed 42, the long-horizon chronicle) renders its told facts as
    prose — the raw composite tokens gone, the glossed lines standing
    in their place, and no id-shaped substring anywhere in the tale."""
    pack = load_pack(PACK_DIR)
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_calendar.json"
    )
    log = tmp_path / "year.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _, events = read_log(log, SCHEMA)
    tale = render_chronicle(events, pack, seed=42)
    assert _ID_SHAPE.search(tale) is None
    for token in _OBSERVED_TOKENS:
        assert token not in tale
    assert "the factor's runner tells Maren: Ferra is there." in tale
    assert "the factor's runner tells Maren: a conversation with Maren." in tale


def test_the_log_bytes_are_untouched_by_the_gloss(tmp_path: Path) -> None:
    """The zero-corpus-price law: the gloss is read-side only — the
    committed smoke fixture regenerates byte-identically under the
    glossed pack (the tokens are canon, the table is not)."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == golden


# -- the coverage census (every pack's mint vocabulary) ---------------------------


def _templated_knows_shapes(data: dict[str, Any]) -> set[str]:
    """Every templated `knows` pattern the pack can mint, normalized
    to a slot-shape (each `{slot}` → `{*}` — `conversation_with_{actor}`
    and `conversation_with_{target}` are ONE shape): the action
    knowledge blocks (all branches + the texture path), the
    expectation rules, the transition-layer entries — the same walk
    `literal_knows_tokens` owns, restricted to the templated half."""
    shapes: set[str] = set()

    def take(entry: Any) -> None:
        knows = entry.get("knows") if isinstance(entry, dict) else None
        if isinstance(knows, str) and "{" in knows:
            shapes.add(re.sub(r"\{[a-z_]+\}", "{*}", knows))

    actions = data["actions.json"]["actions"]
    for action in actions:
        knowledge = action.get("knowledge", {})
        if isinstance(knowledge, dict):
            for records in knowledge.values():
                if isinstance(records, list):
                    for entry in records:
                        take(entry)
        texture = action.get("texture", {})
        if isinstance(texture, dict):
            for records in texture.get("knowledge", {}).values():
                if isinstance(records, list):
                    for entry in records:
                        take(entry)
    rules = data["rules.json"]
    for rule in rules.get("expectations", {}).get("rules", ()):
        if isinstance(rule, dict):
            take(rule)
    for config in rules.get("transitions", {}).values():
        if isinstance(config, dict):
            for records in config.get("knowledge", {}).values():
                if isinstance(records, list):
                    for entry in records:
                        take(entry)
    return shapes


def test_every_packs_mint_shapes_carry_a_gloss() -> None:
    """The coverage law: every templated knows shape a pack mints has
    a table entry — a future pattern without a gloss would leak raw
    ids again, so the census refuses the gap at test time."""
    for pack_name in PACKS:
        pack = load_pack(REPO / "content" / pack_name)
        shapes = _templated_knows_shapes(pack.data)
        table = pack.templates.get("knows", {})
        assert isinstance(table, dict), f"{pack_name}: no knows table"
        glossed = {
            re.sub(r"\{[a-z_]+\}", "{*}", pattern) for pattern in table
        }
        missing = shapes - glossed
        assert not missing, (
            f"{pack_name}: templated knows shapes without a gloss — "
            f"{sorted(missing)} (a raw-id leak class; author the table row)"
        )
