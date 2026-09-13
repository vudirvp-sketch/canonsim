"""iter-119 acceptance — the cultures block (world-2 L2 slice 2, the
cultures half; TASKS world-2, D-153's wave plan / D-154): the
estrangement metadata — the custom vocabularies + the prohibition sets,
belief-as-rules data (the Disco Elysium shape).

The laws pinned here:

- **The budget-block precedent** (zero runtime surface): the block is
  LOAD-TIME metadata — "prohibitions as pack metadata, never bonuses"
  (REFERENCES §10, the WH40k grammar), enforced as log asserts at gate
  review (PACK_SPEC §5), never a core system. A pack without the block
  is the primitive silent (the 68a pattern — the tavern and the road
  load untouched).
- **The culture record** (the CK3 culture keying): one record per
  culture — the `name_profile` (a declared `names.profiles` id), the
  `custom_vocabulary` (the culture's own words), the `prohibitions`
  (the laws: what the culture CANNOT do), the `members` (the declared
  cast). All-or-nothing: a half-declared culture is a broken culture.
- **The anti-rot walk** (the reachability family): every custom word
  occurs in the pack data OUTSIDE the cultures block, as a full
  segment — a word nothing in the pack carries is dead vocabulary
  (the stoplist self-check's twin, enforced at load for any pack that
  declares cultures).
- **The AP-8 prohibition surface** (the consuming union): a
  prohibition's optional `flaw` must name a MEMBER's declared spine
  flaw (the culture's limit over the flaw — the law roots in the cast
  it bounds), and it JOINS the consumed set: a flaw consumed by the
  culture's law alone (no urgency entry names it) is anchored, never
  GHOST — the third consuming surface, after the urgency entry's own
  `flaw` key (iter-117) and beside the still-future hook-weight and
  on_action surfaces.
- **The member laws**: one culture per npc (two is an ambiguity), and
  a member declaring a generated name names the culture's OWN profile
  (the culture↔name keying made executable — the CK3
  culture↔name-pool binding).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PROFILE = "tongue_a"
OTHER_PROFILE = "tongue_b"
GUARD = "npc_guard_01"
OTHER_MEMBER = "npc_guard_02"
FLAW = "the house answers no coin after dark"
CULTURE = "the_house"
AGG_EVENT = "road_counts"
AGG_LINE = "{actor} numbers {population} souls."
COND_EVENT = "road_musters"
COND_LINE = (
    "{names?{actor} brings {names}."
    "|{actor} musters {members} strong at {location}.}"
)
MACRO_EVENT = "year_turns"
MACRO_LINE = "The year turns to {year}."

PROFILES: dict[str, dict[str, Any]] = {
    PROFILE: {
        "onsets": ["b", "d", "m", "n", "r", "s", "t", ""],
        "nuclei": ["a", "e", "i", "o", "u"],
        "codas": ["", "n", "r", "s", "l"],
        "syllables": [1, 2],
    },
    OTHER_PROFILE: {
        "onsets": ["k", "v", "z", ""],
        "nuclei": ["a", "i", "o", "u"],
        "codas": ["", "k", "sh"],
        "syllables": [1, 1],
    },
}

CULTURES: dict[str, dict[str, Any]] = {
    CULTURE: {
        "name_profile": PROFILE,
        "custom_vocabulary": ["purse", "mug", "ale"],
        "prohibitions": [
            {
                "law": "the house's dark-hour law",
                "flaw": FLAW,
                "notes": "the crafted culture law (AP-8's third surface)",
            }
        ],
        "members": [GUARD, OTHER_MEMBER],
        "notes": "the acceptance culture (the crafted twin)",
    }
}


def cultures_pack(
    tmp_path: Path,
    name: str,
    *,
    cultures: dict[str, Any] | None = None,
) -> tuple[Path, Any]:
    """A committed-tavern copy carrying the cultures vocabulary: the
    names block (two profiles), guard_02's `generated_name` declaration
    (the authored name removed — the mutual-exclusion law) riding a
    condensing group (the reachability law), guard_01's crafted SPINE
    (consumed by the prohibition ALONE — no urgency entry names the
    flaw: the AP-8 union's own proof), and the cultures block. Returns
    the pack dir (for post-hoc JSON edits) and the loaded pack."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)

    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    entities["groups"] = [{
        "id": "grp_road",
        "name": "the road traffic",
        "position": "loc_guardroom",
        "members": [OTHER_MEMBER],
        "condense_event": COND_EVENT,
        "macro_event": AGG_EVENT,
        "notes": "the acceptance group (the names reachability door)",
    }]
    for npc in entities["npcs"]:
        if npc["id"] == OTHER_MEMBER:
            npc.pop("name", None)
            npc["generated_name"] = PROFILE
        if npc["id"] == GUARD:
            npc["spine"] = {
                "want": "the house kept",
                "need": "the debt cleared",
                "flaw": FLAW,
                "cause": "the bad winter emptied the cellar",
            }
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["names"] = {"profiles": PROFILES}
    rules["cultures"] = CULTURES if cultures is None else cultures
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


def _rules_mutate(cultures: Any) -> Callable[[Path], None]:
    """A rules.json mutator: overwrite the whole cultures block."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        rules["cultures"] = cultures
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


def _culture_mutate(**field: Any) -> Callable[[Path], None]:
    """A rules.json mutator: overwrite one field of the first culture
    record (DEL drops the key)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        record = rules["cultures"][CULTURE]
        for key, value in field.items():
            if value is DEL:
                record.pop(key, None)
            else:
                record[key] = value
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


def _prohibition_mutate(**field: Any) -> Callable[[Path], None]:
    """A rules.json mutator: overwrite one field of the first
    prohibition entry (DEL drops the key)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        entry = rules["cultures"][CULTURE]["prohibitions"][0]
        for key, value in field.items():
            if value is DEL:
                entry.pop(key, None)
            else:
                entry[key] = value
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return mutate


DEL = object()


def _mutated(
    tmp_path: Path, name: str, mutate: Callable[[Path], None]
) -> None:
    """A crafted pack mutated post-lint-setup (the lint probes)."""
    base, _pack = cultures_pack(tmp_path, f"base_{name}")
    target = tmp_path / name
    shutil.copytree(base, target)
    mutate(target)
    with pytest.raises(PackError, match=match_for(name)):
        load_pack(target)


# the per-probe expected message (name -> the regex the refusal must
# match — the parametrize table below pairs each mutator with one)
MATCHES: dict[str, str] = {
    "not_an_object": r"cultures must be an object",
    "unknown_keys": r"unknown keys",
    "half_declared": r"prohibitions is required",
    "bad_profile": r"not a declared profile",
    "dead_word": r"occurs nowhere in the pack data",
    "empty_vocabulary": r"custom_vocabulary must be a non-empty list",
    "foreign_flaw": r"names no declared spine flaw",
    "unknown_member": r"is not a declared npc",
    "two_cultures": r"already belongs to",
    "keying": r"the culture\u2194name keying",
    "memberless": r"members must be a non-empty list",
    "lawless": r"prohibitions must be a non-empty list",
    "lawless_entry": r"law is required",
}


def match_for(name: str) -> str:
    return MATCHES[name]


# -- the green pins -------------------------------------------------------------


def test_the_green_twin_loads_and_the_union_holds(tmp_path: Path) -> None:
    """The AP-8 consuming UNION, proven by load: guard_01's crafted
    spine flaw is consumed by the prohibition ALONE (no urgency entry
    names it — the tavern's urgency table is untouched) — the load
    would refuse it as GHOST if the prohibition's flaw did not join
    the consumed set. The metadata block's own 68a law: nothing at
    runtime reads it, the whole vocabulary rides load-time."""
    _dir, pack = cultures_pack(tmp_path, "green")
    culture = pack.rules["cultures"][CULTURE]
    assert culture["name_profile"] == PROFILE
    assert culture["members"] == [GUARD, OTHER_MEMBER]


def test_the_unarmed_law_the_other_packs_load_untouched() -> None:
    """A pack without the block is the primitive silent (the 68a
    pattern): the tavern and the road load byte-untouched through the
    new lint — the block is optional per pack, zero assured surface."""
    assert load_pack(REPO / "content" / "tavern_pack").name_version == "tavern_pack@0.1"
    assert load_pack(REPO / "content" / "road_pack").name_version == "road_pack@0.1"


# -- the lint ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "mutate"),
    [
        ("not_an_object", _rules_mutate(["not", "an", "object"])),
        ("unknown_keys", _culture_mutate(bogus=1)),
        ("half_declared", _culture_mutate(prohibitions=DEL)),
        ("bad_profile", _culture_mutate(name_profile="no_such_profile")),
        ("dead_word", _culture_mutate(custom_vocabulary=["purse", "noguchword"])),
        ("empty_vocabulary", _culture_mutate(custom_vocabulary=[])),
        ("foreign_flaw", _prohibition_mutate(flaw="a flaw nobody declared")),
        ("unknown_member", _culture_mutate(members=[GUARD, "npc_nobody"])),
        ("two_cultures", _rules_mutate({
            CULTURE: CULTURES[CULTURE],
            "the_other": {
                "name_profile": OTHER_PROFILE,
                "custom_vocabulary": ["mug"],
                "prohibitions": [{"law": "a law", "flaw": None}],
                "members": [GUARD],
            },
        })),
        ("keying", _culture_mutate(name_profile=OTHER_PROFILE)),
        ("memberless", _culture_mutate(members=[])),
        ("lawless", _culture_mutate(prohibitions=[])),
        ("lawless_entry", _prohibition_mutate(law="")),
    ],
)
def test_the_cultures_lint(
    tmp_path: Path, name: str, mutate: Callable[[Path], None]
) -> None:
    """The closed vocabularies, the all-or-nothing shape, the
    anti-rot walk, the AP-8 member binding, the one-culture law and
    the culture↔name keying — the block's whole contract, refused
    loudly at load (PACK_SPEC §6's prohibition surface)."""
    _mutated(tmp_path, name, mutate)
