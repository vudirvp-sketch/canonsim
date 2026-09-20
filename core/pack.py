"""Pack loader (PACK-1): fixed 4-file directory, `sorted()` load order
(INV-2), load-then-resolve — name-based references are checked only after
all files load (no forward declarations). The phase-0 minimum lint fails
loudly at load, before any simulation: orphan references (exits, positions,
carriers, carries), closed-enum membership, phase coverage of the day,
pack meta consistency — and, from iter-2, the intent-contract cross-refs:
resolver keys against the registry, precondition tests against the closed
set, action event types against the template vocabulary, check kinds
against `rules.checks`, knowledge audiences/channels/fidelity/slots
against their closed sets, transition layers against the template
vocabulary, the system-pass DAG (an ambiguity fails at load —
`core/scheduler.py`), and — from drama-3 — the on_action reaction
table (closed key sets, the scope/gate/event/state vocabularies, the
one-hop law). `"_"` commentary fields are ignored wherever
references are collected. Full pack JSON-Schemas are a phase-6 rung
(`docs/BLUEPRINT.md` PACK-1); the event-contract enums the pack mirrors
are cross-checked by `tests/test_smoke.py` against the schema.

The D-175 split (riding roads-1, its first pack.py-growing row): THIS
module owns the admission CONTRACT — `load_pack` stays the single
admission gate, the `_Lint` below the one orchestrator holding the
pinned run order (the KI#77 order law: the comments between the calls
are load-bearing) — and `core/packlint/` holds the implementation, one
domain class per family (never a DSL, never a base-class framework).
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from core.packlint.actions import ActionsLint
from core.packlint.actors import ActorsLint
from core.packlint.admission import AdmissionLint
from core.packlint.calendar import CalendarLint
from core.packlint.economy import EconomyLint
from core.packlint.entities import EntitiesLint
from core.packlint.epistemic import EpistemicLint
from core.packlint.helpers import (  # noqa: F401 -- PackError is the compat re-export
    PackError,
    _require,
)
from core.packlint.readside import (
    BRIEF_BLOCK_IDS,  # noqa: F401 -- the compat re-export
    ReadsideLint,
)
from core.packlint.story import StoryLint
from core.packlint.systems import SystemsLint
from core.packlint.travel import TravelLint
from core.packlint.weather import WeatherLint
from core.packlint.worldgen import (  # noqa: F401 -- the compat re-exports
    WORLDGEN_MAP_KEYS,
    WORLDGEN_SUB_BLOCKS,
    WorldgenLint,
)

__all__ = [
    "BRIEF_BLOCK_IDS",
    "PACK_FILE_NAMES",
    "Pack",
    "PackError",
    "load_pack",
]

PACK_FILE_NAMES: Final = ("actions.json", "entities.json", "rules.json", "templates.json")


class _Lint:
    """The admission ORCHESTRATOR (the D-175 split's ownership point): the
    domain classes hold the bodies; this class holds the ORDER — every
    call below keeps its original position and its load-bearing comment
    (the KI#77 order law: a crafted variant must hit the owning block's
    clean PackError, never a KeyError from a later lint)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def run(self) -> None:
        entitieslint = EntitiesLint(self._data)
        actionslint = ActionsLint(self._data)
        systemslint = SystemsLint(self._data)
        epistemiclint = EpistemicLint(self._data)
        actorslint = ActorsLint(self._data)
        storylint = StoryLint(self._data)
        readsidelint = ReadsideLint(self._data)
        worldgenlint = WorldgenLint(self._data)
        travellint = TravelLint(self._data)
        calendarlint = CalendarLint(self._data)
        weatherlint = WeatherLint(self._data)
        economylint = EconomyLint(self._data)
        admissionlint = AdmissionLint(self._data)
        entitieslint._meta()
        # res-1 (the economy substrate): the block's own shape EARLY —
        # before _entities, whose `accounts` cross-check reads the
        # account-kind vocabulary this validates, and before _actions,
        # whose account-block and account_at_least lints read the same
        # vocabulary (the KI#77 order law: a crafted variant with a
        # malformed economy block must hit _economy's clean PackError,
        # never a KeyError downstream). The entity cross-checks live in
        # the LATE phase (_economy_cross, after _weather).
        economylint._economy()
        entitieslint._entities()
        actionslint._actions()
        actionslint._templates()
        systemslint._time_rules()
        systemslint._systems()
        systemslint._transitions()
        epistemiclint._knowledge_rules()
        epistemiclint._acquisition()
        systemslint._crime_watch()
        systemslint._expectations()
        # beliefwire-2 (iter-70, KI#77): the traits block's shape lint
        # runs BEFORE the urgency/action cond lints that read it —
        # _lint_trait_cond reads rules["traits"]["beliefs"], so a crafted
        # variant with a non-object traits block must hit _traits' clean
        # PackError here, never an AttributeError downstream (the order
        # was load-bearing only once the committed pack gained a
        # trait_held consumer).
        storylint._traits()
        actorslint._urgencies()
        # depth-6 (iter-92): after _urgencies — the sibling goal block
        # reads the entities' groups, the states axes, and the actions,
        # all validated before it.
        actorslint._factions()
        # name-1 (iter-96): after _factions — the sibling block reads
        # the entities' npcs + groups (the members' reachability) and
        # the rules' own names block, all validated before it.
        actorslint._names()
        # world-2 L2 slice 2 (iter-119): after _names — the cultures
        # block reads the declared profiles (the culture↔name keying),
        # the npc records' spines and generated_name declarations, and
        # the pack's own text (the vocabulary anti-rot walk), all
        # validated before it.
        actorslint._cultures()
        storylint._director()
        storylint._on_action()
        storylint._secrets()
        storylint._echo()
        systemslint._drift()
        systemslint._reflection()
        systemslint._states_rules()
        systemslint._importance_rules()
        readsidelint._brief()
        epistemiclint._retrieval()
        # depth-2 (iter-75): after _brief — the one-object law reads
        # brief.scene_texture.unique_slots, whose shape _brief validates
        # first (the KI#77 order law: a crafted variant with a malformed
        # brief must hit _brief's clean PackError, never a KeyError
        # downstream).
        readsidelint._scene_detail()
        # depth-5 (iter-81): last but one — the worldgen block's cross-lints
        # read the director hook table, the template vocabulary, the
        # scene_detail block (the overlap refusal), and the entities'
        # modeled-slot law, all validated before it.
        worldgenlint._worldgen()
        # st-6a (iter-97): after _worldgen — the travel block's coverage
        # law reads the claims' declared sites (validated by _worldgen)
        # and the entities' exits graph, all validated before it.
        travellint._travel()
        # the calendar family (the calendar slice): after _travel and
        # before _weather — the sub-year cadences read the macro clock
        # (validated by _time_rules) and the template closure, and the
        # weather block's seasonal layer reads the calendar entries
        # (the ride binding), all validated before it.
        calendarlint._calendar()
        # weather-1 (iter-98): LAST among the block lints — the ambient
        # family's block reads the macro clock (validated by _time_rules),
        # the template closure, the director hook table (the seeded
        # consequences' registry), and the transition layers' follow-up
        # flags (the erosion targets — the promoted canon objects), all
        # validated before it.
        weatherlint._weather()
        # res-1: the economy's flow-endpoint cross-checks — after every
        # block lint and AFTER _entities validated the records (the
        # worldgen lint's own late-phase law: the from/to reads walk
        # entity records, so a malformed entities.json must hit
        # _entities' clean PackError first, never a crash here).
        economylint._economy_cross()
        # pack-ci (iter-117): the cross-block admission families run after
        # EVERY block lint — the teleology gate and the live-char crosswalk
        # read the emission inventory (actions, on_action, transitions,
        # crime_watch, expectations, telling, secrets, reflection, macro,
        # weather, worldgen, groups), the entity reference graph, the
        # urgencies table, the hook channels and the spine records, all
        # validated before them (the KI#77 order law, cross-block edition).
        admissionlint._teleology()
        # pack-1 (iter-148): the fact/belief vocabulary split — after
        # _teleology (the same emission inventory, validated there
        # first; the KI#77 order law, cross-block edition: D-175 (5)'s
        # consent split as the generic disjointness law).
        admissionlint._fact_belief_split()
        admissionlint._live_char()


@dataclass(frozen=True, slots=True)
class Pack:
    """Loaded, linted pack: the setting as read-only data (INV-3)."""

    data: Mapping[str, Mapping[str, Any]]

    @property
    def name(self) -> str:
        return str(self.data["entities.json"]["meta"]["pack"])

    @property
    def version(self) -> str:
        return str(self.data["entities.json"]["meta"]["version"])

    @property
    def name_version(self) -> str:
        return f"{self.name}@{self.version}"

    @property
    def entities(self) -> Mapping[str, Any]:
        return self.data["entities.json"]

    @property
    def rules(self) -> Mapping[str, Any]:
        return self.data["rules.json"]

    @property
    def templates(self) -> Mapping[str, Any]:
        return self.data["templates.json"]

    def entity(self, entity_id: str) -> Mapping[str, Any] | None:
        """The pack record for an entity id, or None (any category)."""
        for category in (
            "locations", "npcs", "ambient_entities", "items", "groups",
        ):
            records: Iterable[Mapping[str, Any]] = self.entities.get(
                category, ()
            )
            for record in records:
                if record["id"] == entity_id:
                    return record
        return None

    def kind_of(self, entity_id: str) -> str | None:
        """The entity category: location | npc | ambient | item | group,
        or None."""
        for category, kind in (
            ("locations", "location"),
            ("npcs", "npc"),
            ("ambient_entities", "ambient"),
            ("items", "item"),
            ("groups", "group"),
        ):
            for record in self.entities.get(category, ()):
                if record["id"] == entity_id:
                    return kind
        return None

    def action(self, intent: str) -> Mapping[str, Any] | None:
        """The action record for an intent type, or None."""
        actions: Iterable[Mapping[str, Any]] = self.data["actions.json"]["actions"]
        for action in actions:
            if action["intent"] == intent:
                return action
        return None

    def event_types(self) -> frozenset[str]:
        """The pack's closed event-type vocabulary (templates own it in
        phase 0 — every type the slice can produce has a chronicle line)."""
        return frozenset(self.templates["events"])

    def player_id(self) -> str:
        """The single is_player entity id."""
        for npc in self.entities["npcs"]:
            if npc.get("is_player", False):
                return str(npc["id"])
        raise PackError("no is_player npc in pack")


def load_pack(pack_dir: Path) -> Pack:
    """Load the fixed 4-file pack directory and run the minimum lint."""
    present = {path.name for path in pack_dir.glob("*.json")}
    _require(
        present == set(PACK_FILE_NAMES),
        f"{pack_dir}: expected exactly {list(PACK_FILE_NAMES)}, found {sorted(present)}",
    )
    data: dict[str, Mapping[str, Any]] = {}
    for name in sorted(PACK_FILE_NAMES):  # INV-2: sorted() load order
        with (pack_dir / name).open(encoding="utf-8") as fh:
            data[name] = json.load(fh)
    _Lint(data).run()
    return Pack(data=data)

