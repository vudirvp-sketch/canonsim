"""iter-96 acceptance — name-1, the name generator (TASKS name-1; D-116
(12): the Azgaar split — condensation's canon-birth events need names;
`region_00`-style engine ids do not scale to a story).

The laws pinned here:

- **The stream family law** (the D-079 family law's sixth member): one
  content-addressed `name:<npc>` stream per declaring npc
  (`core/rng.py::name_stream_name` — the scene-detail twin: a lazy
  per-entity materialization); npc ids are entity-unique, so the name
  is injective; adding or re-arming a declaration shifts neither a
  canon check draw (the substantive fingerprint untouched — family
  draws never touch it) nor another npc's name.
- **The lazy materialization** (`core/names.py::materialize_name` —
  the D-054 texture-promotion law at npc scale, the scene-detail
  twin): the unborn name draws on the npc's OWN stream, ONE birth
  (StateChange(npc, "name", None -> drawn)); a name already in the
  folded projection is canon — SKIPPED, never redrawn. The unarmed
  law: no declaration, no block — zero assures, zero draws, the
  stream never even registered.
- **The output namespace law** (the TASKS row's lint line): a drawn
  name never collides with the entity namespace — every declared
  entity id, all categories (the render maps id-valued strings to
  display names, so a colliding name would corrupt the mapping). The
  collision walk skips colliding candidates and redraws
  (deterministic), bounded by WALK_MAX before the loud refusal —
  a profile that cannot clear the namespace is a pack design error.
- **The condensation consumer** (depth-7's extension): the
  condensation event carries each member's name birth PAIRED with the
  member's membership birth (one member, one block), the outcome's
  `names` key listing the drawn names (present only when something
  materialized — the drifted_from law); the tier half stays
  draw-free; the unborn population stays counts (the lazy-depth law:
  unnamed until the reader's zone warms).
- **The born-name read surface** (render + brief): the fold's born
  name outranks the pack record (canon is the answer); an authored
  name has no birth event; an unborn generated name renders honestly
  as its dry id.
- **The corpus price** (the 68a pattern + D-108's both-arms law): the
  committed pack unarmed — a crafted pack carrying the INERT
  vocabulary (the names block, the declarations, the group WITHOUT
  `time.macro`) runs the committed corpus scripts BYTE-IDENTICALLY;
  the armed arm's delta is the name births + the `names` key alone
  (carried by the SAME condensation events — the (t, type, actor)
  sequence and the substantive fingerprint EQUAL to the authored
  twin).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

import pytest

from brief.assembler import assemble_brief
from core.fold import fold, initial_projection
from core.groups import (
    MARKER_PROP,
    MEMBER_OF_PROP,
    MEMBERS_KEY,
    NAMES_KEY,
    is_condensed,
)
from core.log import StateChange, read_log
from core.loop import Simulator
from core.names import (
    NAME_PROP,
    WALK_MAX,
    NamesError,
    materialize_name,
)
from core.pack import Pack, PackError, load_pack
from core.rng import (
    FAMILY_PREFIXES,
    NAME_PREFIX,
    SUBSTANTIVE,
    RngBank,
    name_stream_name,
)
from render.chronicle import render_chronicle, render_entity_view

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

GROUP = "grp_road"
GROUP_NAME = "the road traffic"
ANCHOR = "loc_guardroom"  # warm from the street — the PC's load position
MEMBERS = ("npc_guard_01", "npc_guard_02")
PROFILE = "tongue_a"
OTHER_PROFILE = "tongue_b"
AGG_EVENT = "road_counts"
AGG_LINE = "{actor} numbers {population} souls."
COND_EVENT = "road_musters"
# the conditional form: a bare {names} on a nameless condensation is an
# unknown slot (the GrammarError law) — the line branches on the key's
# presence (the drifted_from law's template twin)
COND_LINE = (
    "{names?{actor} brings {names}."
    "|{actor} musters {members} strong at {location}.}"
)
MACRO_EVENT = "year_turns"
MACRO_LINE = "The year turns to {year}."
CADENCE = 40
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]

PROFILES: dict[str, dict[str, Any]] = {
    PROFILE: {
        "onsets": ["b", "br", "d", "g", "m", "n", "r", "s", "t", ""],
        "nuclei": ["a", "e", "i", "o", "u"],
        "codas": ["", "n", "r", "s", "l", "th"],
        "syllables": [1, 2],
    },
    OTHER_PROFILE: {
        "onsets": ["k", "t", "v", "z", ""],
        "nuclei": ["a", "i", "o", "u"],
        "codas": ["", "k", "m", "sh"],
        "syllables": [1, 1],
    },
}


# -- the crafted packs ---------------------------------------------------------


def _group_record(anchor: str = ANCHOR) -> dict[str, Any]:
    return {
        "id": GROUP,
        "name": GROUP_NAME,
        "position": anchor,
        "members": list(MEMBERS),
        "condense_event": COND_EVENT,
        "macro_event": AGG_EVENT,
        "notes": "the acceptance group (name-1): the tier + name vocabulary",
    }


def names_pack(
    tmp_path: Path,
    name: str,
    *,
    groups: list[dict[str, Any]] | None = None,
    generated: dict[str, str] | None = None,
    profiles: dict[str, dict[str, Any]] | None = None,
    macro: Any = False,
) -> tuple[Path, Pack]:
    """A committed-pack copy carrying the name-1 vocabulary: the
    `rules.json::names` block (None = the block REMOVED — the unarmed
    twin), the members' `generated_name` declarations (the authored
    `name` removed — the mutual-exclusion law), the group record with
    the tier keys, the tier template lines, and the optional
    `time.macro` block (False = untouched — the committed pack
    declares none; the inert form carries the whole vocabulary without
    the clock: the one-scene law, no zones, no condensation, zero
    draws). Returns the pack dir (for post-hoc JSON edits) and the
    loaded pack."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)

    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    entities["groups"] = [_group_record()] if groups is None else groups
    declared = PROFILES if generated is None else generated
    for npc in entities["npcs"]:
        if npc["id"] in declared:
            npc.pop("name", None)  # the mutual-exclusion law
            npc["generated_name"] = declared[npc["id"]]
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if profiles is None:
        rules["names"] = {"profiles": PROFILES}
    else:
        rules["names"] = {"profiles": profiles}
    if macro is not False:
        if macro is None:
            rules["time"].pop("macro", None)
        else:
            rules["time"]["macro"] = macro
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates["events"][AGG_EVENT] = AGG_LINE
    templates["events"][COND_EVENT] = COND_LINE
    templates["events"][MACRO_EVENT] = MACRO_LINE
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target, load_pack(target)


def armed(
    tmp_path: Path, name: str, **kwargs: Any
) -> tuple[Path, Pack]:
    """The deterministic armed arm: the macro clock at cadence 40, both
    members declaring the tongue_a profile."""
    kwargs.setdefault(
        "generated", {MEMBERS[0]: PROFILE, MEMBERS[1]: PROFILE}
    )
    kwargs.setdefault(
        "macro", {"cadence_ticks": CADENCE, "event_type": MACRO_EVENT}
    )
    return names_pack(tmp_path, name, **kwargs)


def _mutated(
    tmp_path: Path, name: str, mutate: Callable[[Path], None]
) -> Pack:
    """A crafted pack mutated post-lint-setup (the lint probes)."""
    _base, _pack = armed(tmp_path, f"base_{name}")
    target = tmp_path / name
    shutil.copytree(_base, target)
    mutate(target)
    return load_pack(target)


def _rules_mutate(names_block: Any) -> Callable[[Path], None]:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        rules["names"] = names_block
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


def _npc_mutate(npc_id: str, **field: Any) -> Callable[[Path], None]:
    def mutate(target: Path) -> None:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        npc = next(n for n in entities["npcs"] if n["id"] == npc_id)
        for key, value in field.items():
            if value is None:
                npc.pop(key, None)
            else:
                npc[key] = value
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return mutate


def _profile_mutate(**field: Any) -> Callable[[Path], None]:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        profile = rules["names"]["profiles"][PROFILE]
        for key, value in field.items():
            profile[key] = value
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


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


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return events


# -- the unit level (duck packs) -----------------------------------------------


def _duck_pack(
    profiles: dict[str, Any] | None, *npcs: dict[str, Any]
) -> Any:
    """The unit-test pack stub: the rules' names block + the npc
    records + the entity namespace (duck-typed — the materializer
    never imports pack.py at runtime)."""
    records = list(npcs)
    return SimpleNamespace(
        rules={} if profiles is None else {"names": {"profiles": profiles}},
        entities={"npcs": records},
        entity=lambda eid: next((r for r in records if r["id"] == eid), None),
    )


NPC_X = {"id": "npc_x", "generated_name": PROFILE, "position": "loc_street"}
NPC_Y = {"id": "npc_y", "generated_name": PROFILE, "position": "loc_street"}
_FIXED = {"onsets": ["br"], "nuclei": ["e"], "codas": ["n"], "syllables": [1, 1]}
_TWO = {
    "onsets": ["b", "d"], "nuclei": ["a"], "codas": [""],
    "syllables": [1, 2],
}


def test_the_stream_grammar_and_the_family_law() -> None:
    """The sixth family: `name:<npc>`, content-addressed, lazily
    registered, the scene-detail twin's grammar; the assure-shadow law
    — a name-family stream may nest inside an assured substantive
    scope (the one legal nesting), and the substantive counter NEVER
    sees the name draws (the fingerprint law — family streams are not
    the replay surface)."""
    assert name_stream_name("npc_x") == f"{NAME_PREFIX}npc_x"
    assert NAME_PREFIX in FAMILY_PREFIXES
    bank = RngBank(42)
    with bank.assure(SUBSTANTIVE):
        birth = materialize_name(
            bank, _duck_pack({PROFILE: _FIXED}, NPC_X), {"npc_x": {}}, "npc_x"
        )
    assert birth is not None
    assert bank.fingerprint == 0  # the substantive counter untouched
    assert bank.count(name_stream_name("npc_x")) > 0  # the family stream drew


def test_the_unarmed_law_is_total() -> None:
    """No declaration (or no block): None BEFORE any stream is touched
    — zero assures, zero draws, the stream never even registered (the
    68a pattern; the v0.1 bytes untouched by construction)."""
    bank = RngBank(42)
    unarmed = _duck_pack({PROFILE: _FIXED}, {"id": "npc_plain"})
    assert materialize_name(bank, unarmed, {"npc_plain": {}}, "npc_plain") is None
    undecorated = dict(NPC_X)
    undecorated.pop("generated_name")  # no declaration, the block present
    assert materialize_name(
        bank, _duck_pack({PROFILE: _FIXED}, undecorated), {"npc_x": {}}, "npc_x"
    ) is None
    assert bank.fingerprint == 0
    with pytest.raises(KeyError):
        bank.count(name_stream_name("npc_x"))  # laziness is total


def test_the_draw_shape_and_determinism() -> None:
    """The Azgaar nameBase shape: the syllable count drawn inside the
  bounds, then onset + nucleus + coda per syllable (pool draws), the
    surface capitalized — one draw per component, deterministic per
    (seed, stream). A single-candidate pool pins the exact bytes."""
    bank = RngBank(7)
    birth = materialize_name(
        bank, _duck_pack({PROFILE: _FIXED}, NPC_X), {"npc_x": {}}, "npc_x"
    )
    assert birth == StateChange("npc_x", NAME_PROP, None, "Bren")
    again = materialize_name(
        RngBank(7), _duck_pack({PROFILE: _FIXED}, NPC_X), {"npc_x": {}}, "npc_x"
    )
    assert again == birth  # same seed, same stream, same name
    wide = materialize_name(
        RngBank(7), _duck_pack({PROFILE: _TWO}, NPC_X), {"npc_x": {}}, "npc_x"
    )
    assert wide is not None
    name = str(wide.to_)
    assert name[0].isupper() and name[1:].islower() and name.isalpha()
    syllables = sum(1 for _ in range(1)) if name == "Ba" else 2  # [1, 2]
    assert syllables in (1, 2)


def test_the_isolation_law_per_declaration() -> None:
    """D-079's add-safety at name granularity: one stream per npc —
    drawing npc_y's name first shifts neither npc_x's name nor a canon
    check draw (both banks draw npc_x identically)."""
    pack = _duck_pack({PROFILE: _TWO}, NPC_X, NPC_Y)
    alone = materialize_name(RngBank(42), pack, {"npc_x": {}, "npc_y": {}}, "npc_x")
    bank = RngBank(42)
    materialize_name(bank, pack, {"npc_x": {}, "npc_y": {}}, "npc_y")
    after = materialize_name(bank, pack, {"npc_x": {}, "npc_y": {}}, "npc_x")
    assert after == alone
    assert bank.fingerprint == 0


def test_first_commit_wins_never_redraws() -> None:
    """The D-054 twin: a name already in the folded projection is
    canon — skipped, never redrawn (the stream does not advance)."""
    bank = RngBank(42)
    pack = _duck_pack({PROFILE: _FIXED}, NPC_X)
    birth = materialize_name(bank, pack, {"npc_x": {}}, "npc_x")
    assert birth is not None
    before = bank.count(name_stream_name("npc_x"))
    state = {"npc_x": {NAME_PROP: birth.to_}}
    assert materialize_name(bank, pack, state, "npc_x") is None
    assert bank.count(name_stream_name("npc_x")) == before  # no redraw


def test_the_collision_walk_skips_the_namespace() -> None:
    """The output namespace law: a candidate equal to a declared
    entity id is SKIPPED — the walk redraws (deterministic, the stream
    advancing per attempt) until a clean candidate lands."""
    colliding = dict(NPC_X)
    colliding["id"] = "Ba"  # the [1,2] pool's one-syllable candidate
    pack = _duck_pack({PROFILE: _TWO}, NPC_X, colliding)
    bank = RngBank(42)
    birth = materialize_name(bank, pack, {"npc_x": {}, "Ba": {}}, "npc_x")
    assert birth is not None
    assert str(birth.to_) != "Ba"
    assert str(birth.to_) not in {"npc_x", "Ba"}  # clean of the namespace


def test_the_collision_walk_exhaustion_is_loud() -> None:
    """A profile whose derivable space cannot clear the namespace is a
    pack design error: WALK_MAX candidates tried, then the loud
    refusal naming the fix (widen the pools — the vacuity family)."""
    colliding = dict(NPC_X)
    colliding["id"] = "Bren"  # the fixed pool's ONLY candidate
    pack = _duck_pack({PROFILE: _FIXED}, NPC_X, colliding)
    bank = RngBank(42)
    with pytest.raises(NamesError, match="widen the pools"):
        materialize_name(bank, pack, {"npc_x": {}, "Bren": {}}, "npc_x")
    # bounded: WALK_MAX attempts, each the count draw + 3 component draws
    assert bank.count(name_stream_name("npc_x")) == WALK_MAX * 4


def test_the_post_lint_backstop_is_loud() -> None:
    """A declaration naming an undeclared profile cannot pass the lint
    — the runtime backstop raises loudly anyway (duck-typed packs, the
    honest path)."""
    bank = RngBank(42)
    with pytest.raises(NamesError, match="no profile"):
        materialize_name(
            bank, _duck_pack({}, NPC_X), {"npc_x": {}}, "npc_x"
        )


# -- the pack lint -------------------------------------------------------------


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_rules_mutate(["not", "an", "object"]), "names must be an object"),
        (_rules_mutate({"profiles": PROFILES, "bogus": 1}), "names: unknown keys"),
        (_rules_mutate({"profiles": "nope"}), "names.profiles must be an object"),
        (_profile_mutate(onsets=[]), "onsets must be a non-empty list"),
        (_profile_mutate(nuclei=["a", "9"]), "ASCII letter fragments"),
        (_profile_mutate(nuclei=["a", ""]), "ASCII letter fragments"),
        (_profile_mutate(codas=["n", "th!"]), "ASCII letter fragments"),
        (_profile_mutate(syllables=[0, 2]), "syllables must be"),
        (_profile_mutate(syllables=[3, 2]), "syllables must be"),
        (_npc_mutate(MEMBERS[0], generated_name="no_such_profile"),
         "not a declared profile"),
        (_npc_mutate("npc_barkeep_01", generated_name=PROFILE),
         "mutually exclusive"),
        (_npc_mutate("npc_barkeep_01", name=None, generated_name=PROFILE),
         "dead data"),
    ],
)
def test_the_names_lint(
    tmp_path: Path, mutate: Callable[[Path], None], message: str
) -> None:
    """The closed vocabularies + the mutual-exclusion law + the
    REACHABILITY law (the depth-5b family — an armed declaration names
    at least one LIVE consumer): a generated_name npc must ride a
    group declaring condense_event — the materialization door; the
    names block's shape (pools, bounds) is pack data, the lint owns
    the law."""
    with pytest.raises(PackError, match=message):
        _mutated(tmp_path, "lint_bad", mutate)


def test_the_inert_vocabulary_loads_clean(tmp_path: Path) -> None:
    """The whole name-1 vocabulary (the block, the declarations, the
    group) loads without the macro clock — the inert form the corpus
    price rides (below)."""
    _dir, pack = names_pack(tmp_path, "inert")
    assert pack.rules["names"]["profiles"][PROFILE]["syllables"] == [1, 2]


# -- the condensation consumer (the loop, the zones) ---------------------------


def test_the_condensation_births_the_names(tmp_path: Path) -> None:
    """The recorded consumer: the group warm from load (the PC at the
    street) condenses at the FIRST crossing — ONE event carrying each
    member's membership birth PAIRED with the name birth (one member,
    one block: member_of then the name), the marker LAST, the
    outcome's `names` key listing the drawn names in member order; the
    fold (T2) holds both the memberships and the names."""
    _dir, pack = armed(tmp_path, "cond_names")
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "cond_names")
    events = _events(log)
    condensations = [e for e in events if e.type == COND_EVENT]
    assert len(condensations) == 1
    event = condensations[0]
    changes = event.state_changes
    assert [c.prop for c in changes] == [
        MEMBER_OF_PROP, NAME_PROP, MEMBER_OF_PROP, NAME_PROP, MARKER_PROP,
    ]
    assert [c.entity for c in changes] == [
        MEMBERS[0], MEMBERS[0], MEMBERS[1], MEMBERS[1], GROUP,
    ]
    name0 = next(
        c.to_ for c in changes
        if c.entity == MEMBERS[0] and c.prop == NAME_PROP
    )
    name1 = next(
        c.to_ for c in changes
        if c.entity == MEMBERS[1] and c.prop == NAME_PROP
    )
    assert name0 != name1  # distinct streams, distinct names
    assert event.outcome[MEMBERS_KEY] == 2
    assert event.outcome[NAMES_KEY] == [name0, name1]
    assert isinstance(name0, str) and name0[0].isupper()
    state = fold(events, initial_projection(pack.entities))
    assert state[MEMBERS[0]][MEMBER_OF_PROP] == GROUP
    assert state[MEMBERS[0]][NAME_PROP] == name0
    assert state[MEMBERS[1]][NAME_PROP] == name1
    assert is_condensed(state, GROUP)


def test_the_unborn_population_stays_counts(tmp_path: Path) -> None:
    """The lazy-depth law: the COLD arm (the group at the market, the
    PC inside the tavern) aggregates — the counts ride the turn, NO
    condensation, NO name births (the fold holds no `name` on the
    members — unnamed until the reader's zone warms)."""
    _dir, pack = armed(
        tmp_path, "cold_names", groups=[_group_record(anchor="loc_market")]
    )
    steps = [{"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "cold_names")
    events = _events(log)
    assert not any(e.type == COND_EVENT for e in events)
    assert [e.t for e in events if e.type == AGG_EVENT] == [40, 80]
    state = fold(events, initial_projection(pack.entities))
    assert NAME_PROP not in state[MEMBERS[0]]
    assert NAME_PROP not in state[MEMBERS[1]]


def test_the_condensation_names_a_joined_member(tmp_path: Path) -> None:
    """The skip law's twin: a member who joined at runtime (member_of
    already held) is not re-birthed — but the name it never had still
    materializes on the group's one condensation event."""
    _dir, pack = armed(tmp_path, "joined_names")
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "joined_names")
    events = _events(log)
    event = next(e for e in events if e.type == COND_EVENT)
    # fold a runtime join BEFORE the condensation (the unit-level twin)
    projection = initial_projection(pack.entities)
    projection[MEMBERS[0]][MEMBER_OF_PROP] = GROUP  # the join
    from core.groups import condensation_drafts
    from core.rng import RngBank

    drafts = condensation_drafts(
        RngBank(42), pack, projection, 40, locations=(ANCHOR,)
    )
    assert len(drafts) == 1
    props = [(c.entity, c.prop) for c in drafts[0].state_changes]
    assert props == [
        (MEMBERS[0], NAME_PROP),  # the joined member: the name alone
        (MEMBERS[1], MEMBER_OF_PROP),
        (MEMBERS[1], NAME_PROP),
        (GROUP, MARKER_PROP),
    ]
    assert drafts[0].outcome == event.outcome  # member count 2 either way


# -- the corpus price (the 68a pattern + D-108's both-arms law) -----------------


def test_determinism(tmp_path: Path) -> None:
    """INV-2: same seed + same script -> byte-identical logs (the name
    draws fold from the same seed-derived streams)."""
    _dir, pack = armed(tmp_path, "det")
    log_a, _a = _run(tmp_path, pack, 42, WAIT_100, "det_a")
    log_b, _b = _run(tmp_path, pack, 42, WAIT_100, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_corpus_price_is_the_name_births_alone(tmp_path: Path) -> None:
    """The both-arms measurement: the names arm (the declarations) vs
    the authored twin (plain string names, no names block) — the
    (t, type, actor) sequence IDENTICAL, the event counts EQUAL (the
    name births ride the SAME condensation event), the substantive
    fingerprint EQUAL (the name draws are family draws, never the
    replay surface); the delta is the name births + the `names` key
    alone."""
    _dir_a, pack_a = armed(tmp_path, "price_names")
    steps = [*WAIT_100, {"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log_a, result_a = _run(tmp_path, pack_a, 42, steps, "price_a")
    # the authored twin: the same group + members, authored names
    entities = json.loads((_dir_a / "entities.json").read_text(encoding="utf-8"))
    for npc in entities["npcs"]:
        npc.pop("generated_name", None)
    rules = json.loads((_dir_a / "rules.json").read_text(encoding="utf-8"))
    rules.pop("names", None)
    twin = _dir_a / ".." / "price_authored"
    shutil.copytree(_dir_a, twin.resolve())
    (twin / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (twin / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pack_u = load_pack(twin.resolve())
    log_u, result_u = _run(tmp_path, pack_u, 42, steps, "price_u")
    events_a = _events(log_a)
    events_u = _events(log_u)
    assert result_a.fingerprint == result_u.fingerprint
    assert len(events_a) == len(events_u)  # the births ride the same events
    assert [(e.t, e.type, e.actor) for e in events_a] == [
        (e.t, e.type, e.actor) for e in events_u
    ]
    cond_a = next(e for e in events_a if e.type == COND_EVENT)
    cond_u = next(e for e in events_u if e.type == COND_EVENT)
    assert cond_a.outcome[NAMES_KEY]  # the names arm's delta
    assert NAMES_KEY not in cond_u.outcome
    assert len(cond_a.state_changes) == len(cond_u.state_changes) + 2


def test_the_unarmed_twin_is_the_committed_bytes(tmp_path: Path) -> None:
    """The zero-price proof (the 68a pattern): a crafted pack carrying
    the INERT name-1 vocabulary (the names block, the declarations,
    the group with BOTH tier keys — no `time.macro` block) runs the
    committed corpus scripts BYTE-IDENTICALLY to the committed pack
    itself (the one-gate law: no armed clock, no zones, no
    condensation, no draws — the v0.1 bytes; zero re-pins)."""
    _dir, inert = names_pack(tmp_path, "inert_bytes")
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


# -- the born-name read surface (render + brief) --------------------------------


def test_the_tale_and_views_render_the_born_names(tmp_path: Path) -> None:
    """The read surface: the condensation line renders the names arm
    (the conditional form — the tracery joins the list); the entity
    view's header shows the born name and its state lines carry it;
    the guards' own events render the born name as {actor} (the
    running fold — canon outranks the pack record)."""
    _dir, pack = armed(tmp_path, "render_names")
    rules = json.loads((_dir / "rules.json").read_text(encoding="utf-8"))
    rules["importance"]["story_critical_events"] += [COND_EVENT, AGG_EVENT]
    (_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pack = load_pack(_dir)
    steps = [*WAIT_100, {"intent": "move", "target": "loc_guardroom"}]
    log, _result = _run(tmp_path, pack, 42, steps, "render_names")
    events = _events(log)
    state = fold(events, initial_projection(pack.entities))
    name0 = state[MEMBERS[0]][NAME_PROP]
    name1 = state[MEMBERS[1]][NAME_PROP]
    chronicle = render_chronicle(events, pack, 42)
    assert f"{GROUP_NAME} brings {name0}, {name1}." in chronicle
    view = render_entity_view(events, state, pack, MEMBERS[1], 42)
    assert f"{name1} ({MEMBERS[1]})" in view
    assert f"  {NAME_PROP}: {name1}" in view
    brief = assemble_brief(events, pack)
    cards = next(
        block for block in brief.blocks if block.block_id == "present_entities"
    )
    assert any(f"{MEMBERS[1]} ({name1})" in line for line in cards.lines)
