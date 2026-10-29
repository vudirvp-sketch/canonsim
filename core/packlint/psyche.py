"""The psyche block lint (agenda-1 P0, iter-417 — the drive ticker's
pack half, `core/drives.py` the engine twin), extended by agenda-1 P2
(iter-419) with the born PRESENTATION anchors (`rules.json::appearance`
/ `rules.json::voice`, `core/persona.py` the engine twin).

The block is the personality substrate: the trait AXES (ids the engine
never interprets — INV-3: the words live here, the engine reads the
table), the ARCHETYPES (the profile templates: one value per axis), the
DISTRIBUTIONS (the generative rows of the lazy birth, agenda-1 P1: which
archetypes a born person may carry, the ± jitter, the extra extremes),
the DRIVES (what a profile's carrier pursues, how hard, through which
declared verb, and by which closed-vocabulary measure), and the per-NPC
PROFILE on the entity record (`psyche: {archetype, axes}` — AUTHORED) or
its born twin (`generated_psyche: <distribution id>` — P1).

The anchors are the person's presentation half: two optional blocks, each
a POOL list of engine-opaque tokens (physical facts / voice properties),
and the npc record's born origin (`generated_look` / `generated_voice`) —
the same born-declaration law one slot over.

Every refusal is a SHAPE or a RESOLVABILITY fact — never taste
(AGENTS.md §6.1):
  - the closed key sets (an unknown key is a shape error, never a silent
    ignore — the pack-lint house law);
  - the axes are ids (non-empty, unique, `low < high` inside 0..100);
  - every archetype declares EVERY axis, every value an int in 0..100
    (a half-declared profile template would silently skip a modifier);
  - every drive names a declared archetype, a declared pack action, a
    `base`/`max_per_beat` in 1..100, and a `measure` drawn from the closed
    precondition vocabulary restricted to what CANON can move: the pack-static
    family is refused (a constant verdict is a drive permanently armed or
    permanently silent — dead data) and so is the clocked pair (a bar that
    moves with time alone cannot be evaluated once per stretch), while the
    event-driven fold `trait_held` is LEGAL (it moves only when canon commits;
    `core/intent.py::EVENT_FOLD_TESTS` owns the split — `drivegoals-1`,
    iter-439);
  - a drive MAY declare its own `need` phrase (needphrase-1, iter-446): the
    board's `need=` sentence for THAT pursuit. The shape is the card's own
    (the phrase prints inside one `need=` segment of one card line): a
    non-empty string, no `=` and no line break, the same word budget as the
    archetype's `want`; and it is DEAD DATA on a drive with no `measure`
    (the board offers only a FAILING measure row, so an appetite's sentence
    can never print). And ONE SENTENCE PER PURSUIT: no two OFFERABLE drives a
    person can carry — the role he holds NOW (his authored archetype, or the
    one his born distribution draws) and every role a TURNING can bring him
    through — may resolve to the same phrase (the row's own `need`, else his
    `spine.need`), because the board prints the phrase beside whichever drive
    is dominant and a shared sentence would put one pursuit's words on
    another's offer (iter-445 §6's measured defect; `_need_phrases`);
  - ONE ACT, ONE OWNER (iter-430, D-282): no npc may be armed by a role
    DRIVE and an authored urgency POST for the same (verb, target) — the
    double carrier duplicates the attempt (the loser rejects
    `projection_moved`) and the person-bound post outlives a role turn
    (see `_single_carrier`);
  - the modifier rows name a declared axis and integer per-cents; a row may
    read the ECHO residue instead (`source: echo`, P5-unit-2 iter-427) and
    then declares its own `low`/`high` bands inside the echo block's scale —
    the axis must be one a declared echo token scores (dead data otherwise),
    and a PROFILE row may declare no bands (the axis row is their one owner);
  - every distribution names DECLARED archetypes, each of them carried
    by at least one declared drive (a profile drawn from a driveless
    archetype is inert — dead data); `jitter` is an int 0..100 and
    `extremes` an int 0..`EXTREME_BUDGET` (the archetype's own extremes
    are part of the same budget);
  - every AUTHORED profile names a declared archetype and carries the
    complete axis set as ints 0..100; the guide's EXTREME BUDGET is a
    shape: at most two axes at an extreme band per profile
    (`live_char_guide` §OCEAN: more extremes = unresolved internal
    conflicts; the number is the donor's authoring guidance, carried as
    a lint FLOOR, never a runtime score);
  - every `generated_psyche` declaration names a declared distribution,
    is mutually exclusive with an authored profile (one profile origin
    per npc — the `generated_name` twin's law), rides a group declaring
    `condense_event` (the materialization door — the depth-5b
    reachability law), and every declared distribution is consumed by at
    least one npc (the same reachability law from the other side: a
    distribution nothing draws from is dead data);
  - the anchor pools carry snake_case tokens (the mechanical identifier
    law, the state prop's own pattern), no duplicate token, and enough
    tokens to fill the dose FLOOR (`LOOK_MIN` / `VOICE_MIN`) — a pool
    that cannot fill the authoring band is incomplete authoring; every
    pool is consumed by at least one npc, every declaration names a
    declared pool and rides a condensing npc, and a raw `look`/`voice`
    list on the npc RECORD is refused (the cards read the folded
    projection; a record value is never seeded — dead data).

The blocks are OPTIONAL and the profiles are OPTIONAL independently: a
pack may carry the vocabulary with no armed profile (the inert-first
authoring form — P0's committed anchor did), and the absence of the
block keeps every byte (the 68a law).
"""

from __future__ import annotations

import re
from collections.abc import Collection, Mapping
from typing import Any, Final

from core.agenda import WANT_MAX_WORDS
from core.drives import ECHO_SOURCE, PROFILE_SOURCE
from core.intent import (
    ACCOUNT_CEILING_TEST,
    ACCOUNT_TEST,
    CLOCKED_TESTS,
    ECHO_TEST,
    PRECONDITION_TESTS,
    STATIC_TESTS,
    TRAIT_TEST,
)
from core.offers import act_delta
from core.packlint.helpers import PackError, _is_int, _require
from core.packlint.shared import (
    lint_account_ceiling_cond,
    lint_account_cond,
    lint_direct_keys,
    lint_echo_cond,
    lint_trait_cond,
)
from core.persona import (
    GENERATED_LOOK_KEY,
    GENERATED_VOICE_KEY,
    LOOK_BLOCK,
    LOOK_MIN,
    LOOK_PROP,
    VOICE_BLOCK,
    VOICE_MIN,
    VOICE_PROP,
)
from core.psyche import (
    EXTREME_BUDGET,
    GENERATED_PSYCHE_KEY,
    HIGH_BAND,
    LOW_BAND,
    PSYCHE_PROP,
)

PSYCHE_KEYS: Final = (
    "axes", "archetypes", "distributions", "drives", "turnings",
    "turning_event", "notes",
)
AXIS_KEYS: Final = ("id", "low", "high", "notes")
ARCHETYPE_KEYS: Final = ("id", "defaults", "want", "notes")
DISTRIBUTION_KEYS: Final = ("id", "archetypes", "jitter", "extremes", "notes")
DRIVE_KEYS: Final = (
    "id", "archetypes", "base", "max_per_beat", "verb", "target", "fields",
    "measure", "need", "modifiers", "notes",
)
MODIFIER_KEYS: Final = ("source", "axis", "low", "high", "low_pct", "high_pct")
PROFILE_KEYS: Final = ("archetype", "axes", "notes")
NOUNS: Final = ("actor", "target", "texture")

#: The duty rows (agenda-1 P3, iter-423): the expectations block's
#: generalization — one row per archetype obligation at one post.
DUTY_ROW_KEYS: Final = ("id", "archetypes", "post", "knows", "notes")

#: The turning row's closed keys (agenda-1 P5, iter-426).
TURNING_KEYS: Final = ("from", "to", "when", "notes")

#: The turning condition's allowed shape is the door's own closed precondition
#: vocabulary, restricted to the tests that read the person ALONE (see
#: `_turnings`): a role turn has no target, so a condition naming another
#: party would silently never fire — refused at load instead of dead data.


#: The anchor blocks' shape (agenda-1 P2): the block carries its POOLS
#: (id + tokens) and notes; a pool row carries id + tokens + notes. The
#: token grammar is the mechanical identifier law (the state prop's own
#: pattern family, `schemas/event.schema.json`).
ANCHOR_BLOCK_KEYS: Final = ("pools", "notes")
POOL_KEYS: Final = ("id", "tokens", "notes")
TOKEN_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_]*$")

#: The two anchor halves in declaration order: (block, npc declaration
#: key, born prop, the dose FLOOR the lint enforces).
ANCHOR_SPECS: Final = (
    (LOOK_BLOCK, GENERATED_LOOK_KEY, LOOK_PROP, LOOK_MIN),
    (VOICE_BLOCK, GENERATED_VOICE_KEY, VOICE_PROP, VOICE_MIN),
)


class _PackView:
    """The lint's minimal pack adapter for the declared-terms arithmetic:
    `core.offers.act_delta` (the ONE owner of that law, iter-442/D-288) reads
    exactly two pack surfaces — the action table and `rules` (the recipes)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self.rules = data["rules.json"]
        self._actions = {
            str(row.get("intent")): row
            for row in data["actions.json"]["actions"]
        }

    def action(self, intent: str) -> Mapping[str, Any] | None:
        return self._actions.get(intent)


def _role_closure(
    role: str, edges: Mapping[str, Collection[str]]
) -> set[str]:
    """Every role a person can HOLD after `role`: the role itself plus the
    turning rows' reachable targets. `role_of` rebinds the WHOLE drive set at
    a turn, so a post-turn pursuit is one of the person's — the need-phrase
    law checks the closure (`_need_phrases`), not the origin role alone."""
    seen = {role}
    pending = [role]
    while pending:
        current = pending.pop()
        for target in edges.get(current, ()):
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


class PsycheLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _psyche(self) -> None:
        """The block's own shape + the entity profiles' cross-check.
        Runs in the cross-block late phase (after the actions, the
        entities, the states and the economy — every vocabulary it
        reads is validated by then; the KI#77 order law)."""
        rules = self._data["rules.json"]
        config = rules.get("psyche")
        if config is None:
            self._orphan_origins()
            return  # the unarmed law
        _require(isinstance(config, Mapping), "psyche must be an object")
        unknown = set(config) - set(PSYCHE_KEYS)
        _require(
            not unknown,
            f"psyche: unknown key(s) {sorted(unknown)} "
            f"(closed set {list(PSYCHE_KEYS)})",
        )
        axes = self._axes(config.get("axes"))
        archetypes = self._archetypes(config.get("archetypes"), axes)
        driven = self._drives(config.get("drives"), axes, archetypes)
        distributions = self._distributions(
            config.get("distributions"), archetypes, driven,
        )
        self._profiles(axes, archetypes, distributions)
        self._turnings(config, archetypes, driven)
        self._need_phrases(config, distributions)
        self._single_carrier(config, distributions)

    def _carryable(self, config: Mapping[str, Any]) -> set[str]:
        """Every archetype some npc can actually CARRY: an authored profile's
        archetype, or an archetype of a distribution a `generated_psyche`
        declaration names (the reachability set the duty rows and the turning
        `from` roles are checked against — dead data otherwise)."""
        distributions = {
            str(row["id"]): row
            for row in config.get("distributions", ())
            if isinstance(row, Mapping) and isinstance(row.get("id"), str)
        }
        reachable: set[str] = set()
        for npc in self._data["entities.json"].get("npcs", ()):
            if not isinstance(npc, Mapping):
                continue
            profile = npc.get(PSYCHE_PROP)
            if isinstance(profile, Mapping) and isinstance(
                profile.get("archetype"), str
            ):
                reachable.add(str(profile["archetype"]))
            born = npc.get(GENERATED_PSYCHE_KEY)
            if isinstance(born, str) and born in distributions:
                reachable.update(
                    str(name)
                    for name in distributions[born].get("archetypes", ())
                )
        return reachable

    def _turnings(
        self,
        config: Mapping[str, Any],
        archetypes: Mapping[str, Mapping[str, Any]],
        driven: Collection[str],
    ) -> None:
        """The role-turn rows' shape (agenda-1 P5, iter-426): a person's role
        may be rewritten by a canon event when the accumulated price crosses
        the row's own bar, while the temperament stays his frozen seed.

        The laws: `from` must be an archetype somebody can CARRY (else the
        row is dead data); `to` must declare a `want` and carry at least one
        drive (a turn into a role with nothing to pursue and nothing on the
        card is a dead end); the conditions are the door's closed vocabulary
        restricted to the ACTOR (a turning has no target, so a target-noun
        condition would silently never fire); every condition's PARAMETERS
        are resolvable at load (`turninglint-1`, iter-431: the echo axis and
        its bar inside the declared scale, the belief token in the traits
        table, the `flag` key present — the silent-dead-gate class, where a
        half-written condition loads green and can never fire); and the event
        type is a template-vocabulary member (the admission family's emission
        witness reads the same key); and one `(from, to)` pair may be declared
        ONCE (`turnids-1`, iter-437): the second row can never fire — the first
        takes the carrier, only an explicit back-row returns it, and the first
        row fires again — so it is dead data. The pack-linted pair is also what
        makes the probe id `turn_<npc>_<from>_<to>` name one declaration
        (`core/turning.py::turning_specs`)."""
        rows = config.get("turnings")
        event = config.get("turning_event")
        if rows is None:
            _require(
                event is None,
                "psyche.turning_event declared without psyche.turnings — an "
                "event nothing can emit (the complete ablation drops both)",
            )
            return
        _require(
            isinstance(rows, (list, tuple)) and bool(rows),
            "psyche.turnings must be a non-empty list",
        )
        _require(
            isinstance(event, str) and bool(event),
            "psyche.turnings requires psyche.turning_event (the template a "
            "turn emits)",
        )
        assert isinstance(event, str)  # the require above
        templates = self._data["templates.json"]["events"]
        _require(
            event in templates,
            f"psyche.turning_event {event!r} is not in the template vocabulary",
        )
        carryable = self._carryable(config)
        seen_pairs: set[tuple[str, str]] = set()
        for row in rows:
            _require(isinstance(row, Mapping), "psyche.turnings[] must be objects")
            unknown = set(row) - set(TURNING_KEYS)
            _require(
                not unknown,
                f"psyche.turnings: unknown key(s) {sorted(unknown)} "
                f"(closed set {list(TURNING_KEYS)})",
            )
            from_role = row.get("from")
            to_role = row.get("to")
            where = f"psyche.turnings[{from_role!r} -> {to_role!r}]"
            _require(
                from_role in archetypes,
                f"{where}: from must name a declared archetype",
            )
            _require(
                from_role in carryable,
                f"{where}: from role is dead data — no npc can carry it "
                f"(neither an authored psyche nor a distribution a generated "
                f"declaration names)",
            )
            _require(
                to_role in archetypes,
                f"{where}: to must name a declared archetype",
            )
            _require(
                to_role != from_role,
                f"{where}: a row that turns a role into itself — dead data",
            )
            pair = (str(from_role), str(to_role))
            _require(
                pair not in seen_pairs,
                f"{where}: duplicate turn ({from_role!r} -> {to_role!r}) — the "
                f"second row can never fire (the first takes the carrier, only "
                f"an explicit back-row returns it, and the first row fires "
                f"again): dead data (turnids-1, iter-437)",
            )
            seen_pairs.add(pair)
            _require(
                to_role in driven,
                f"{where}: the target role carries no drive — a turn into a "
                f"role with nothing to pursue is a dead end (declare the "
                f"target's drive rows first)",
            )
            target = archetypes[str(to_role)]
            want = target.get("want")
            _require(
                isinstance(want, str) and bool(want.strip()),
                f"{where}: the target role must declare a `want` — the card "
                f"and the brief show the turned person's pursuit (the "
                f"card-coherence law)",
            )
            when = row.get("when")
            _require(
                isinstance(when, (list, tuple)) and bool(when),
                f"{where}: when must be a non-empty list of the door's "
                f"precondition rows",
            )
            for condition in when:
                _require(
                    isinstance(condition, Mapping),
                    f"{where}.when[] must be objects",
                )
                lint_direct_keys(condition, f"{where}.when")
                test = condition.get("test")
                _require(
                    test in PRECONDITION_TESTS,
                    f"{where}.when: test {test!r} is not in the closed "
                    f"precondition vocabulary",
                )
                _require(
                    condition.get("noun") == "actor",
                    f"{where}.when: every condition's noun must be 'actor' — "
                    f"a role turn reads the PERSON alone (a turning has no "
                    f"target; a target-noun condition would never fire)",
                )
                _require(
                    not ({"with", "who"} & set(condition)),
                    f"{where}.when: no other party is read — 'with'/'who' "
                    f"refused (a turning has no target)",
                )
                if test == ACCOUNT_TEST:
                    lint_account_cond(self._data, condition, f"{where}.when")
                if test == ACCOUNT_CEILING_TEST:
                    lint_account_ceiling_cond(
                        self._data, condition, f"{where}.when"
                    )
                if test == ECHO_TEST:
                    lint_echo_cond(self._data, condition, f"{where}.when")
                if test == TRAIT_TEST:
                    lint_trait_cond(self._data, condition, f"{where}.when")
            if "notes" in row:
                _require(
                    isinstance(row["notes"], str),
                    f"{where}: notes must be a string (prose — never a table "
                    f"key)",
                )

    # -- the block's halves -------------------------------------------------

    def _single_carrier(
        self,
        config: Mapping[str, Any],
        distributions: Mapping[str, Mapping[str, Any]],
    ) -> None:
        """One act, one owner (iter-430, D-282): a person may not carry TWO
        autonomous sources for the same act — a role DRIVE and an authored
        urgency POST naming the same (verb, target). Measured before the law
        (iter-430 §2.2): the pair can enqueue the same craft twice, the loser
        resolves `projection_moved` (a rejected intent in canon) and one tick
        can carry two fires; worse, the person-bound post OUTLIVES a role
        turn — a turned master keeps ordering the craft his role has left,
        while the drive set follows `role_of`. The law is the content twin of
        the drive ticker's own binding: the ROLE owns the act, so a mass
        roster inherits it and no hand-written post can re-arm a person
        against the role he now carries.

        Reads the urgencies block (validated earlier in the run order) and
        the npc origins the profile lint already accepted; compares EXACT
        (verb, target) pairs — a drive and a post naming different targets
        are different acts."""
        by_role: dict[str, list[tuple[str, str | None]]] = {}
        for row in config.get("drives", ()):
            if not isinstance(row, Mapping):
                continue
            act = (str(row.get("verb")), row.get("target"))
            for archetype in row.get("archetypes", ()):
                by_role.setdefault(str(archetype), []).append(act)
        if not by_role:
            return
        posts: dict[str, list[tuple[str, str | None]]] = {}
        for entry in (
            (self._data["rules.json"].get("urgencies") or {}).get("entries", ())
        ):
            if not isinstance(entry, Mapping):
                continue
            npc_id = entry.get("npc")
            intent = entry.get("intent")
            if not isinstance(npc_id, str) or not isinstance(intent, Mapping):
                continue
            posts.setdefault(npc_id, []).append(
                (str(intent.get("kind")), intent.get("target"))
            )
        if not posts:
            return
        for npc in self._data["entities.json"].get("npcs", ()):
            if not isinstance(npc, Mapping):
                continue
            npc_id = npc.get("id")
            if not isinstance(npc_id, str) or npc_id not in posts:
                continue
            roles: list[str] = []
            profile = npc.get(PSYCHE_PROP)
            if isinstance(profile, Mapping) and isinstance(
                profile.get("archetype"), str
            ):
                roles.append(str(profile["archetype"]))
            born = npc.get(GENERATED_PSYCHE_KEY)
            if isinstance(born, str) and isinstance(
                distributions.get(born), Mapping
            ):
                roles.extend(
                    str(name)
                    for name in distributions[born].get("archetypes", ())
                )
            for role in roles:
                for verb, target in by_role.get(role, ()):
                    if (verb, target) not in posts[npc_id]:
                        continue
                    raise PackError(
                        f"npc {npc_id!r}: act {verb!r} -> {target!r} is "
                        f"armed by BOTH the role drive of {role!r} and an "
                        f"authored urgency post — one act, one owner "
                        f"(D-282): the double carrier can enqueue the same "
                        f"act twice (the loser rejects `projection_moved`) "
                        f"and the person-bound post survives a role turn; "
                        f"keep the drive or the post, never both for one "
                        f"(verb, target)"
                    )

    def _orphan_origins(self) -> None:
        """The unarmed law's OTHER side (agenda-1 P1, iter-418): a profile
        origin declared without the block is dead data — nothing reads it,
        and the born one would refuse mid-run at the materializer's own
        backstop. The COMPLETE ablation drops the declarations with the
        block (the four economy twins' law, and P1's own)."""
        for npc in self._data["entities.json"].get("npcs", ()):
            for key in (PSYCHE_PROP, GENERATED_PSYCHE_KEY):
                _require(
                    npc.get(key) is None,
                    f"npc {npc.get('id')!r}: {key} declared but rules.json "
                    f"carries no psyche block — a profile nothing reads (the "
                    f"complete ablation drops the declarations with the block)",
                )

    def _persona(self) -> None:
        """The born presentation anchors' half (agenda-1 P2, iter-419):
        the two blocks' shape and the npc declarations. The same
        reachability law the born profile carries: a declaration must name
        a declared pool and ride a condensing npc (the materialization
        door — otherwise it can never be born), and every declared pool
        must be consumed by at least one npc (a pool nothing draws from is
        dead data). A block absent while declarations name its keys is the
        ORPHAN origin (the complete ablation drops the declarations with
        the block). An authored `look`/`voice` list on the npc RECORD is
        refused: the entity cards read the folded projection, the record's
        value is never seeded — dead data by construction (change a body
        through an event, never through the record)."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        condensing: set[str] = set()
        for group in entities.get("groups", ()):
            if group.get("condense_event") is not None:
                condensing.update(group.get("members", ()))
        for block, declaration, prop, floor in ANCHOR_SPECS:
            config = rules.get(block)
            if config is None:
                for npc in entities.get("npcs", ()):
                    _require(
                        npc.get(declaration) is None,
                        f"npc {npc.get('id')!r}: {declaration} declared but "
                        f"rules.json carries no {block} block — an anchor "
                        f"nothing reads (the complete ablation drops the "
                        f"declarations with the block)",
                    )
                continue  # the unarmed law
            _require(
                isinstance(config, Mapping), f"{block} must be an object"
            )
            unknown = set(config) - set(ANCHOR_BLOCK_KEYS)
            _require(
                not unknown,
                f"{block}: unknown key(s) {sorted(unknown)} "
                f"(closed set {list(ANCHOR_BLOCK_KEYS)})",
            )
            pools = self._anchor_pools(config.get("pools"), block, floor)
            used: set[str] = set()
            for npc in entities.get("npcs", ()):
                authoring = f"npc {npc.get('id')!r}"
                _require(
                    npc.get(prop) is None,
                    f"{authoring}: a raw {prop} on the npc record is dead "
                    f"data — the cards read the FOLDED projection, never "
                    f"the record (declare {declaration} for a born anchor, "
                    f"or assert the fact through an event)",
                )
                pool_id = npc.get(declaration)
                if pool_id is None:
                    continue
                _require(
                    isinstance(pool_id, str) and pool_id in pools,
                    f"{authoring}: {declaration} {pool_id!r} is not a "
                    f"declared {block} pool",
                )
                _require(
                    npc["id"] in condensing,
                    f"{authoring}: {declaration} is dead data — the npc is "
                    f"not a member of any group declaring condense_event "
                    f"(the materialization door; the depth-5b reachability "
                    f"law)",
                )
                used.add(str(pool_id))
            for pool_id in pools:
                _require(
                    pool_id in used,
                    f"{block}.pools[{pool_id!r}]: no npc declares "
                    f"{declaration} on it — dead data (a pool nothing "
                    f"draws from is never consumed; the reachability law)",
                )

    def _anchor_pools(
        self, rows: Any, block: str, floor: int,
    ) -> dict[str, Mapping[str, Any]]:
        """One anchor block's pools: the id vocabulary, the snake_case
        token law (the mechanical identifier pattern), no duplicate token
        (a draw may not repeat a fact), and enough tokens for the dose
        floor (a pool that cannot fill the authoring band is incomplete:
        `core.persona` clips the draw inside it by construction)."""
        _require(
            isinstance(rows, (list, tuple)) and rows,
            f"{block}.pools must be a non-empty list",
        )
        pools: dict[str, Mapping[str, Any]] = {}
        for row in rows:
            _require(
                isinstance(row, Mapping), f"{block}.pools[] must be objects"
            )
            unknown = set(row) - set(POOL_KEYS)
            _require(
                not unknown,
                f"{block}.pools: unknown key(s) {sorted(unknown)}",
            )
            pool_id = row.get("id")
            _require(
                isinstance(pool_id, str) and pool_id,
                f"{block}.pools[].id must be a non-empty string",
            )
            where = f"{block}.pools[{pool_id!r}]"
            _require(pool_id not in pools, f"{where}: duplicate id")
            tokens = row.get("tokens")
            _require(
                isinstance(tokens, (list, tuple)) and tokens,
                f"{where}.tokens must be a non-empty list",
            )
            _require(
                len(tokens) >= floor,
                f"{where}: {len(tokens)} tokens — the authoring dose floor "
                f"is {floor} (the draw clips inside the band; a shorter "
                f"pool cannot fill it)",
            )
            seen: set[str] = set()
            for token in tokens:
                _require(
                    isinstance(token, str) and TOKEN_PATTERN.match(token),
                    f"{where}: token {token!r} must be snake_case "
                    f"(^[a-z][a-z0-9_]*$ — the mechanical identifier law)",
                )
                _require(
                    token not in seen,
                    f"{where}: duplicate token {token!r} — a pool pick must "
                    f"never repeat a fact",
                )
                seen.add(token)
            pools[pool_id] = row
        return pools

    def _axes(
        self, rows: Any
    ) -> dict[str, Mapping[str, Any]]:
        _require(
            isinstance(rows, (list, tuple)) and rows,
            "psyche.axes must be a non-empty list",
        )
        axes: dict[str, Mapping[str, Any]] = {}
        for row in rows:
            _require(isinstance(row, Mapping), "psyche.axes[] must be objects")
            unknown = set(row) - set(AXIS_KEYS)
            _require(
                not unknown,
                f"psyche.axes: unknown key(s) {sorted(unknown)}",
            )
            axis_id = row.get("id")
            _require(
                isinstance(axis_id, str) and axis_id,
                "psyche.axes[].id must be a non-empty string",
            )
            _require(axis_id not in axes, f"psyche.axes: duplicate id {axis_id!r}")
            low = row.get("low", LOW_BAND)
            high = row.get("high", HIGH_BAND)
            _require(
                _is_int(low) and _is_int(high) and 0 <= low < high <= 100,
                f"psyche.axes[{axis_id!r}]: low/high must be ints with "
                f"0 <= low < high <= 100",
            )
            axes[axis_id] = row
        return axes

    def _archetypes(
        self, rows: Any, axes: Mapping[str, Mapping[str, Any]]
    ) -> dict[str, Mapping[str, Any]]:
        _require(
            isinstance(rows, (list, tuple)) and rows,
            "psyche.archetypes must be a non-empty list",
        )
        archetypes: dict[str, Mapping[str, Any]] = {}
        for row in rows:
            _require(
                isinstance(row, Mapping), "psyche.archetypes[] must be objects"
            )
            unknown = set(row) - set(ARCHETYPE_KEYS)
            _require(
                not unknown,
                f"psyche.archetypes: unknown key(s) {sorted(unknown)}",
            )
            archetype_id = row.get("id")
            _require(
                isinstance(archetype_id, str) and archetype_id,
                "psyche.archetypes[].id must be a non-empty string",
            )
            _require(
                archetype_id not in archetypes,
                f"psyche.archetypes: duplicate id {archetype_id!r}",
            )
            defaults = row.get("defaults")
            _require(
                isinstance(defaults, Mapping),
                f"psyche.archetypes[{archetype_id!r}].defaults must be an object",
            )
            _require(
                set(defaults) == set(axes),
                f"psyche.archetypes[{archetype_id!r}].defaults must carry "
                f"EXACTLY the declared axes {sorted(axes)}",
            )
            for axis_id, value in defaults.items():
                _require(
                    _is_int(value) and 0 <= value <= 100,
                    f"psyche.archetypes[{archetype_id!r}].defaults"
                    f"[{axis_id!r}] must be an int 0..100",
                )
            if "want" in row:
                # agenda-1 P2 (iter-420): the derived SPINE's first half —
                # a PHRASE the entity card carries every present beat, so
                # its length is a budget law (the card block's own), not
                # prose taste: an author cannot blow the brief's window
                # with one want line.
                want = row["want"]
                _require(
                    isinstance(want, str) and bool(want.strip()),
                    f"psyche.archetypes[{archetype_id!r}].want must be a "
                    f"non-empty string (the phrase the agenda serves)",
                )
                _require(
                    len(want.split()) <= WANT_MAX_WORDS,
                    f"psyche.archetypes[{archetype_id!r}].want is "
                    f"{len(want.split())} words — the card-budget bound is "
                    f"{WANT_MAX_WORDS} (the want rides EVERY present beat's "
                    f"entity card; the pack's brief window is the loser)",
                )
            archetypes[archetype_id] = row
        return archetypes

    def _drives(
        self,
        rows: Any,
        axes: Mapping[str, Mapping[str, Any]],
        archetypes: Mapping[str, Mapping[str, Any]],
    ) -> set[str]:
        """The drive rows' shape; answers the set of archetypes at least
        one drive is declared on (the distributions' reachability check
        reads it — a drawable archetype with no drive would be inert)."""
        _require(
            isinstance(rows, (list, tuple)) and rows,
            "psyche.drives must be a non-empty list",
        )
        actions = {
            action["intent"]
            for action in self._data["actions.json"]["actions"]
        }
        driven: set[str] = set()
        seen: set[str] = set()
        echo_axes, echo_scale = self._echo_vocabulary()
        for row in rows:
            _require(isinstance(row, Mapping), "psyche.drives[] must be objects")
            unknown = set(row) - set(DRIVE_KEYS)
            _require(
                not unknown,
                f"psyche.drives: unknown key(s) {sorted(unknown)}",
            )
            drive_id = row.get("id")
            _require(
                isinstance(drive_id, str) and drive_id,
                "psyche.drives[].id must be a non-empty string",
            )
            where = f"psyche.drives[{drive_id!r}]"
            _require(drive_id not in seen, f"{where}: duplicate id")
            seen.add(drive_id)
            archetypes_row = row.get("archetypes")
            _require(
                isinstance(archetypes_row, (list, tuple))
                and archetypes_row
                and all(a in archetypes for a in archetypes_row),
                f"{where}: archetypes must be a non-empty list of declared "
                f"archetypes",
            )
            driven.update(str(name) for name in archetypes_row)
            _require(
                _is_int(row.get("base")) and 1 <= row["base"] <= 100,
                f"{where}: base must be an int 1..100",
            )
            _require(
                _is_int(row.get("max_per_beat"))
                and 1 <= row["max_per_beat"] <= 100,
                f"{where}: max_per_beat must be an int 1..100",
            )
            _require(
                row.get("verb") in actions,
                f"{where}: verb must name a declared pack action",
            )
            if "target" in row:
                _require(
                    isinstance(row["target"], str) and row["target"],
                    f"{where}: target must be a non-empty string",
                )
            if "fields" in row:
                _require(
                    isinstance(row["fields"], Mapping),
                    f"{where}: fields must be an object",
                )
            self._need(row, where)
            self._measure(row.get("measure", ()), where)
            for modifier in row.get("modifiers", ()):
                self._modifier(modifier, axes, echo_axes, echo_scale, where)
        return driven

    def _need(self, row: Mapping[str, Any], where: str) -> None:
        """The drive's own phrase for the board's sentence (`need`,
        needphrase-1, iter-446). The shape is the card block's own: a short
        authored line the offer prints VERBATIM, so it carries no `=` (the
        segment grammar) and no line break (the card is one line), and its
        word count rides the same authoring budget as the archetype's `want`
        (both ride a present person's card). A phrase on a drive with no
        `measure` is DEAD DATA: only a failing measure row is ever offered,
        so an appetite's sentence can never print."""
        need = row.get("need")
        if need is None:
            return
        _require(
            isinstance(need, str) and bool(need) and need == need.strip(),
            f"{where}: need must be a non-empty string with no surrounding "
            f"whitespace (the board prints the phrase verbatim)",
        )
        assert isinstance(need, str)  # the require above
        _require(
            "=" not in need and "\n" not in need and "\r" not in need,
            f"{where}: need {need!r} carries '=' or a line break — the board "
            f"prints it inside one `need=` segment of one card line",
        )
        _require(
            len(need.split()) <= WANT_MAX_WORDS,
            f"{where}: need is {len(need.split())} words — the card-budget "
            f"bound is {WANT_MAX_WORDS} (the phrase rides a present person's "
            f"card, the same window the archetype `want` is held to)",
        )
        _require(
            bool(row.get("measure", ())),
            f"{where}: need declared on a drive with no `measure` — dead "
            f"data: the board offers only a FAILING measure row, so an "
            f"appetite's phrase can never print",
        )

    def _distributions(
        self,
        rows: Any,
        archetypes: Mapping[str, Mapping[str, Any]],
        driven: Collection[str],
    ) -> dict[str, Mapping[str, Any]]:
        """The distributions' shape (agenda-1 P1): the born origins a
        `generated_psyche` declaration may name. Absent -> no born origin
        (the inert authoring form, byte-identical corpora)."""
        if rows is None:
            return {}
        _require(
            isinstance(rows, (list, tuple)) and rows,
            "psyche.distributions must be a non-empty list",
        )
        distributions: dict[str, Mapping[str, Any]] = {}
        for row in rows:
            _require(
                isinstance(row, Mapping),
                "psyche.distributions[] must be objects",
            )
            unknown = set(row) - set(DISTRIBUTION_KEYS)
            _require(
                not unknown,
                f"psyche.distributions: unknown key(s) {sorted(unknown)}",
            )
            distribution_id = row.get("id")
            _require(
                isinstance(distribution_id, str) and distribution_id,
                "psyche.distributions[].id must be a non-empty string",
            )
            where = f"psyche.distributions[{distribution_id!r}]"
            _require(
                distribution_id not in distributions,
                f"{where}: duplicate id",
            )
            names = row.get("archetypes")
            _require(
                isinstance(names, (list, tuple)) and bool(names)
                and all(name in archetypes for name in names),
                f"{where}: archetypes must be a non-empty list of declared "
                f"archetypes",
            )
            for name in names:
                _require(
                    name in driven,
                    f"{where}: archetype {name!r} carries no declared drive — "
                    f"a profile drawn from it would never act (the "
                    f"reachability law)",
                )
            _require(
                _is_int(row.get("jitter")) and 0 <= row["jitter"] <= 100,
                f"{where}: jitter must be an int 0..100 (the axis scale)",
            )
            _require(
                _is_int(row.get("extremes"))
                and 0 <= row["extremes"] <= EXTREME_BUDGET,
                f"{where}: extremes must be an int 0..{EXTREME_BUDGET} — the "
                f"authoring budget (the archetype's own extremes are part of "
                f"it, never added on top)",
            )
            distributions[distribution_id] = row
        return distributions

    def _measure(self, rows: Any, where: str) -> None:
        _require(
            isinstance(rows, (list, tuple)),
            f"{where}.measure must be a list",
        )
        for cond in rows:
            _require(
                isinstance(cond, Mapping),
                f"{where}.measure[] must be objects",
            )
            test = cond.get("test")
            _require(
                test in PRECONDITION_TESTS,
                f"{where}.measure: unknown precondition test {test!r}",
            )
            _require(
                test not in STATIC_TESTS,
                f"{where}.measure: static test {test!r} refused — a static "
                f"verdict reads the pack RECORD, which canon never writes, so "
                f"the measure is CONSTANT: the drive is permanently armed or "
                f"permanently silent, never a goal the world can complete "
                f"(deadmeasure-1, iter-439)",
            )
            _require(
                test not in CLOCKED_TESTS,
                f"{where}.measure: clocked test {test!r} refused — its verdict "
                f"moves with the clock ALONE, so the quiet-beat skip could not "
                f"evaluate the bar once per stretch (the event-driven fold "
                f"`{TRAIT_TEST!s}` is legal: it moves only when canon commits)",
            )
            lint_direct_keys(cond, f"{where}.measure")
            if test == ACCOUNT_TEST:
                lint_account_cond(self._data, cond, f"{where}.measure")
            if test == ACCOUNT_CEILING_TEST:
                lint_account_ceiling_cond(self._data, cond, f"{where}.measure")
            for param in ("noun", "with", "who"):
                if param in cond:
                    _require(
                        cond[param] in NOUNS,
                        f"{where}.measure: {param} {cond[param]!r} must be "
                        f"one of {list(NOUNS)}",
                    )
            self._helper(cond, test, f"{where}.measure")

    def _helper(self, cond: Mapping[str, Any], test: Any, where: str) -> None:
        """The helper act (`helper_verb`, iter-442, D-288): the act a THIRD
        PARTY performs to close the need — the card's reader, the player. The
        board offers it in place of the owner's own act, so it owes the same
        resolvability law every figure owes: a declared action, with an
        `account` block whose declared movement on the need's `(holder, kind)`
        closes the test's direction. A helper that walks no stock of that kind
        (a gift of another kind, a `source` at the actor) is DEAD DATA — the
        offer would promise an act that cannot finish the need — refused at
        load, never printed as a promise."""
        helper = cond.get("helper_verb")
        if helper is None:
            return
        _require(
            isinstance(helper, str) and helper,
            f"{where}: helper_verb must be a non-empty string",
        )
        _require(
            test in (ACCOUNT_TEST, ACCOUNT_CEILING_TEST),
            f"{where}: helper_verb closes a STOCK need — {test!r} declares no "
            f"terms, so no third party's act can be its closing act",
        )
        holder = cond.get("holder")
        _require(
            isinstance(holder, str) and holder,
            f"{where}: a helper_verb row names its explicit `holder` (the "
            f"helper act's counterparty) — the `noun` form leaves the delta "
            f"unresolved at load",
        )
        kind = cond.get("kind")
        _require(
            isinstance(kind, str) and kind,
            f"{where}: a helper_verb row names its `kind` (the stock the "
            f"helper act must move)",
        )
        entities = self._data["entities.json"].get("npcs", ())
        _require(
            any(npc.get("is_player") for npc in entities),
            f"{where}: helper_verb reads the READER's gate, and the pack "
            f"declares no is_player entity — the board could not name the "
            f"helper's doer",
        )
        actions = self._data["actions.json"]["actions"]
        declared = next(
            (row for row in actions if row.get("intent") == helper), None,
        )
        _require(
            declared is not None,
            f"{where}: helper_verb {helper!r} is not a declared action",
        )
        delta = act_delta(
            _PackView(self._data), str(helper), str(holder), str(kind),
            target=str(holder),
        )
        _require(
            (delta > 0) if test == ACCOUNT_TEST else (delta < 0),
            f"{where}: helper_verb {helper!r} moves {kind!r} on {holder!r} "
            f"by {delta:+d} — a helper that does not close this need is "
            f"dead data (the offer would promise an act that cannot finish "
            f"it)",
        )

    def _need_phrases(
        self,
        config: Mapping[str, Any],
        distributions: Mapping[str, Mapping[str, Any]],
    ) -> None:
        """One sentence per PURSUIT (needphrase-1, iter-446; the trajectory
        added by needphrase-2, iter-447). The board prints ONE `need=` phrase
        beside the offer of the person's DOMINANT drive, so the phrase must
        belong to THAT drive, never to another of his pursuits. The record's
        `spine.need` is a static person-level line; the drive's own `need` is
        the pursuit's. Where two OFFERABLE drives a person can carry resolve to
        the SAME phrase (the row's `need`, else his `spine.need`), one of them
        is printing the other's words: the defect measured in iter-445 §6,
        where the PAID debt's sentence stood beside the craft's offer. Refused
        at load, because no runtime read can tell the two sentences apart.

        The drives a person can carry are his role's NOW plus, for every
        TURNING row, the role it rebinds him to (`_role_closure` — `role_of`
        swaps the whole drive set at the turn, so the post-turn pursuit is one
        of his own). A born person's distribution declares several archetypes
        but the birth draws ONE, so each candidate origin is checked
        SEPARATELY (two drawn archetypes never stand in one person at once).
        Drives with no `measure` are excluded: they are never offered, so
        neither their phrase nor their fallback can print (`_need` refuses a
        phrase there as dead data)."""
        drives: dict[str, list[Mapping[str, Any]]] = {}
        for row in config.get("drives", ()):
            if not isinstance(row, Mapping) or not row.get("measure"):
                continue
            for archetype in row.get("archetypes", ()):
                drives.setdefault(str(archetype), []).append(row)
        if not drives:
            return
        rows = config.get("turnings")
        edges: dict[str, list[str]] = {}
        for row in rows if isinstance(rows, (list, tuple)) else ():
            if not isinstance(row, Mapping):
                continue
            from_role = row.get("from")
            to_role = row.get("to")
            if isinstance(from_role, str) and isinstance(to_role, str):
                edges.setdefault(from_role, []).append(to_role)
        for npc in self._data["entities.json"].get("npcs", ()):
            if not isinstance(npc, Mapping):
                continue
            spine = npc.get("spine")
            record_need = (
                spine.get("need")
                if isinstance(spine, Mapping)
                and isinstance(spine.get("need"), str)
                and spine["need"].strip()
                else None
            )
            for origin in sorted(self._origins(npc, distributions)):
                seen: dict[str, str] = {}
                for role in sorted(_role_closure(origin, edges)):
                    for row in drives.get(role, ()):
                        phrase = row.get("need") or record_need
                        if phrase is None:
                            continue
                        owner = str(row.get("id"))
                        before = seen.get(phrase)
                        if before is not None and before != owner:
                            raise PackError(
                                f"npc {npc.get('id')!r}: the pursuits "
                                f"{before!r} and {owner!r} both resolve to the "
                                f"need phrase {phrase!r} — one sentence per "
                                f"PURSUIT (needphrase-1, iter-446; the turning "
                                f"trajectory added by needphrase-2, iter-447): "
                                f"the board prints the phrase beside whichever "
                                f"drive is dominant, so a shared sentence would "
                                f"put one pursuit's words on another's offer; "
                                f"declare each drive's own `need` (the record's "
                                f"`spine.need` is the fallback for a person of "
                                f"ONE pursuit)"
                            )
                        seen[phrase] = owner

    def _origins(
        self,
        npc: Mapping[str, Any],
        distributions: Mapping[str, Mapping[str, Any]],
    ) -> set[str]:
        """Every role the person can START in: an AUTHORED profile's
        archetype, or the archetypes his born distribution may draw. One
        draw per person, so two drawn archetypes never stand in one person at
        once — the caller checks each origin separately."""
        roles: set[str] = set()
        profile = npc.get(PSYCHE_PROP)
        if isinstance(profile, Mapping) and isinstance(
            profile.get("archetype"), str
        ):
            roles.add(str(profile["archetype"]))
        born = npc.get(GENERATED_PSYCHE_KEY)
        if isinstance(born, str) and isinstance(
            distributions.get(born), Mapping
        ):
            roles.update(
                str(name) for name in distributions[born].get("archetypes", ())
            )
        return roles

    def _echo_vocabulary(self) -> tuple[set[str], tuple[int, int] | None]:
        """The echo block's declared axis vocabulary and score scale
        (`core.echo` owns the fold, this lint owns the modifier rows'
        resolvability): an echo-sourced modifier naming an axis no declared
        token can ever score — or carrying bands outside the scale — is dead
        data, refused here instead of silently never moving a bar."""
        config = self._data["rules.json"].get("echo")
        if not isinstance(config, Mapping):
            return set(), None
        axes: set[str] = set()
        tokens = config.get("tokens")
        if isinstance(tokens, Mapping):
            for token in tokens.values():
                if isinstance(token, Mapping):
                    axes.update(str(axis) for axis in token.get("axes", ()))
        lo, hi = config["scale"]
        return axes, (int(lo), int(hi))

    def _modifier(
        self,
        modifier: Any,
        axes: Mapping[str, Mapping[str, Any]],
        echo_axes: Collection[str],
        echo_scale: tuple[int, int] | None,
        where: str,
    ) -> None:
        """One drive modifier row (agenda-1 P0; the ECHO source added by
        P5-unit-2, iter-427): a PROFILE row reads the frozen axis (its bands
        live on the axis row — one owner) and declares no bands of its own;
        an ECHO row reads the decaying residue and OWNS its bands (no
        `psyche.axes` row exists for an echo axis), inside the echo block's
        scale and on an axis some declared token can score."""
        _require(
            isinstance(modifier, Mapping),
            f"{where}.modifiers[] must be objects",
        )
        unknown = set(modifier) - set(MODIFIER_KEYS)
        _require(
            not unknown,
            f"{where}.modifiers: unknown key(s) {sorted(unknown)}",
        )
        source = modifier.get("source", PROFILE_SOURCE)
        _require(
            source in (PROFILE_SOURCE, ECHO_SOURCE),
            f"{where}.modifiers: source must be {PROFILE_SOURCE!r} or "
            f"{ECHO_SOURCE!r}",
        )
        if source == ECHO_SOURCE:
            _require(
                echo_scale is not None,
                f"{where}.modifiers: source {ECHO_SOURCE!r} declared but "
                f"rules.json carries no echo block — a modifier reading a "
                f"fold the pack never declares (dead data)",
            )
            _require(
                modifier.get("axis") in echo_axes,
                f"{where}.modifiers: echo axis must be one that a declared "
                f"echo token scores (dead data otherwise)",
            )
            low = modifier.get("low")
            high = modifier.get("high")
            _require(
                _is_int(low) and _is_int(high),
                f"{where}.modifiers: an echo modifier must declare integer "
                f"low/high bands (the row OWNS them — an echo axis has no "
                f"psyche.axes row to read a band from)",
            )
            assert echo_scale is not None and _is_int(low) and _is_int(high)
            scale_lo, scale_hi = echo_scale
            _require(
                scale_lo <= low < high <= scale_hi,
                f"{where}.modifiers: echo bands must satisfy {scale_lo} <= "
                f"low < high <= {scale_hi} (the echo scale — a band outside "
                f"it is dead data)",
            )
        else:
            _require(
                modifier.get("axis") in axes,
                f"{where}.modifiers: axis must name a declared axis",
            )
            _require(
                not ({"low", "high"} & set(modifier)),
                f"{where}.modifiers: a profile modifier declares no bands of "
                f"its own — the axis row owns them (a second band here is a "
                f"second truth; source {ECHO_SOURCE!r} is the row that owns "
                f"its bands)",
            )
        for key in ("low_pct", "high_pct"):
            _require(
                _is_int(modifier.get(key)) and modifier[key] >= 0,
                f"{where}.modifiers: {key} must be a non-negative int "
                f"(per-cent)",
            )

    # -- the duty rows (agenda-1 P3) ----------------------------------------

    def _duties(self) -> None:
        """The duty rows' shape (agenda-1 P3, iter-423): the expectations
        block's generalization from an ITEM rule to a POST row — one
        obligation per archetype at one location, minting one knowledge
        token when the post stands unheld at the block's clock.

        The reachability law is the psyche family's own: a duty bound to an
        archetype NO npc can carry (neither an authored profile nor a
        distribution a born declaration names) is dead data, refused here
        rather than silently never checked. The t=0 law is the expectations
        family's: at least one AUTHORED holder must stand at the post on the
        initial state, because a lapse chains its cause to the event that
        moved the holder (`core.knowledge.last_prop_mover`) — a violation
        with no mover has nothing honest to blame."""
        rules = self._data["rules.json"]
        config = rules.get("expectations")
        if not isinstance(config, Mapping):
            return
        rows = config.get("duties")
        event = config.get("duty_event")
        if rows is None:
            _require(
                event is None,
                "expectations.duty_event declared without expectations.duties "
                "— an event nothing can emit (the complete ablation drops both)",
            )
            return
        _require(
            isinstance(rows, (list, tuple)) and bool(rows),
            "expectations.duties must be a non-empty list",
        )
        _require(
            isinstance(event, str) and bool(event),
            "expectations.duties requires expectations.duty_event (the "
            "template a lapse emits)",
        )
        templates = self._data["templates.json"]["events"]
        _require(
            event in templates,
            f"expectations.duty_event {event!r} is not in the template "
            f"vocabulary",
        )
        psyche = rules.get("psyche")
        _require(
            isinstance(psyche, Mapping),
            "expectations.duties binds a psyche archetype, but rules.json "
            "carries no psyche block — the identity vocabulary owns who a "
            "person is (an obligation nothing can hold)",
        )
        assert isinstance(psyche, Mapping)  # the require above
        archetypes = {
            str(row["id"])
            for row in psyche.get("archetypes", ())
            if isinstance(row, Mapping) and isinstance(row.get("id"), str)
        }
        distributions = {
            str(row["id"]): row
            for row in psyche.get("distributions", ())
            if isinstance(row, Mapping) and isinstance(row.get("id"), str)
        }
        entities = self._data["entities.json"]
        location_ids = {
            str(location["id"])
            for location in entities.get("locations", ())
            if isinstance(location, Mapping) and "id" in location
        }
        npcs = [
            npc for npc in entities.get("npcs", ()) if isinstance(npc, Mapping)
        ]
        # every archetype some npc can actually carry (authored override or
        # a distribution a generated declaration names) — the reachability
        # set, built from the entity records this lint already validates
        reachable: set[str] = set()
        for npc in npcs:
            profile = npc.get(PSYCHE_PROP)
            if isinstance(profile, Mapping) and isinstance(
                profile.get("archetype"), str
            ):
                reachable.add(str(profile["archetype"]))
            born = npc.get(GENERATED_PSYCHE_KEY)
            if isinstance(born, str) and born in distributions:
                reachable.update(
                    str(name)
                    for name in distributions[born].get("archetypes", ())
                )
        seen: set[str] = set()
        for row in rows:
            _require(isinstance(row, Mapping), "expectations.duties[] must be objects")
            unknown = set(row) - set(DUTY_ROW_KEYS)
            _require(
                not unknown,
                f"expectations.duties: unknown key(s) {sorted(unknown)} "
                f"(closed set {list(DUTY_ROW_KEYS)})",
            )
            duty_id = row.get("id")
            _require(
                isinstance(duty_id, str) and bool(duty_id),
                "expectations.duties[].id must be a non-empty string",
            )
            where = f"expectations.duties[{duty_id!r}]"
            _require(duty_id not in seen, f"{where}: duplicate id")
            seen.add(str(duty_id))
            names = row.get("archetypes")
            _require(
                isinstance(names, (list, tuple)) and bool(names),
                f"{where}: archetypes must be a non-empty list",
            )
            for name in names:
                _require(
                    name in archetypes,
                    f"{where}: archetype {name!r} is not a declared psyche "
                    f"archetype",
                )
                _require(
                    name in reachable,
                    f"{where}: archetype {name!r} is dead data — no npc can "
                    f"carry it (neither an authored psyche nor a distribution "
                    f"a generated declaration names)",
                )
            _require(
                row.get("post") in location_ids,
                f"{where}: post must name a declared location",
            )
            _require(
                isinstance(row.get("knows"), str) and bool(row["knows"]),
                f"{where}: knows must be a non-empty string (the token a "
                f"lapse mints — it is the duty's memory)",
            )
            if "notes" in row:
                _require(
                    isinstance(row["notes"], str),
                    f"{where}: notes must be a string (prose — never a table "
                    f"key)",
                )
            holders = [
                npc for npc in npcs
                if isinstance(npc.get(PSYCHE_PROP), Mapping)
                and str(npc[PSYCHE_PROP].get("archetype")) in set(map(str, names))
            ]
            if not holders:
                # a BORN-only archetype: nobody holds the duty yet — the
                # runtime's dormant law, and the lapse's cause-less arm (a
                # born holder never moved; the birth is the only event).
                continue
            _require(
                any(npc.get("position") == row.get("post") for npc in holders),
                f"{where}: violated by the initial pack state — a duty must be "
                f"held at t=0 (the lapse chains its cause to the event that "
                f"moved the holder; the expectations law)",
            )

    # -- the entity profiles ------------------------------------------------

    def _profiles(
        self,
        axes: Mapping[str, Mapping[str, Any]],
        archetypes: Mapping[str, Mapping[str, Any]],
        distributions: Mapping[str, Mapping[str, Any]],
    ) -> None:
        """The per-npc origins: an AUTHORED `psyche` (the author's
        override) or a BORN `generated_psyche` declaration (agenda-1 P1) —
        one origin per npc. The born declaration must name a declared
        distribution and ride a group declaring `condense_event` (the
        materialization door); every declared distribution must be named
        by at least one npc (the reachability law from the other side)."""
        entities = self._data["entities.json"]
        condensing: set[str] = set()
        for group in entities.get("groups", ()):
            if group.get("condense_event") is not None:
                condensing.update(group.get("members", ()))
        used: set[str] = set()
        for npc in entities.get("npcs", ()):
            authoring = f"npc {npc.get('id')!r}"
            generated = npc.get(GENERATED_PSYCHE_KEY)
            profile = npc.get("psyche")
            if generated is not None:
                _require(
                    profile is None,
                    f"{authoring}: authored psyche and generated_psyche are "
                    f"mutually exclusive — one profile origin per npc (the "
                    f"`generated_name` twin's law)",
                )
                _require(
                    isinstance(generated, str) and generated in distributions,
                    f"{authoring}: generated_psyche {generated!r} is not a "
                    f"declared distribution (psyche.distributions owns the "
                    f"vocabulary)",
                )
                _require(
                    npc["id"] in condensing,
                    f"{authoring}: generated_psyche is dead data — the npc is "
                    f"not a member of any group declaring condense_event "
                    f"(the materialization door; the depth-5b reachability "
                    f"law)",
                )
                used.add(str(generated))
                continue
            if profile is None:
                continue  # an unprofiled NPC runs no drive (the inert form)
            where = f"{authoring}: psyche"
            _require(isinstance(profile, Mapping), f"{where} must be an object")
            unknown = set(profile) - set(PROFILE_KEYS)
            _require(
                not unknown, f"{where}: unknown key(s) {sorted(unknown)}"
            )
            _require(
                profile.get("archetype") in archetypes,
                f"{where}: archetype must name a declared archetype",
            )
            values = profile.get("axes")
            _require(
                isinstance(values, Mapping) and set(values) == set(axes),
                f"{where}: axes must carry EXACTLY the declared axes "
                f"{sorted(axes)}",
            )
            extremes = 0
            for axis_id, value in values.items():
                declared = axes[axis_id]
                _require(
                    _is_int(value) and 0 <= value <= 100,
                    f"{where}: axes[{axis_id!r}] must be an int 0..100",
                )
                low = int(declared.get("low", LOW_BAND))
                high = int(declared.get("high", HIGH_BAND))
                if value <= low or value >= high:
                    extremes += 1
            _require(
                extremes <= EXTREME_BUDGET,
                f"{where}: {extremes} extreme axes — the authoring budget is "
                f"at most {EXTREME_BUDGET} (more extremes = unresolved "
                f"internal conflict, `live_char_guide` OCEAN)",
            )
        for distribution_id in distributions:
            _require(
                distribution_id in used,
                f"psyche.distributions[{distribution_id!r}]: no npc declares "
                f"generated_psyche on it — dead data (a distribution nothing "
                f"draws from is never consumed; the reachability law)",
            )
