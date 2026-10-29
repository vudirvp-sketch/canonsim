"""The agenda view (agenda-1 P2, iter-420): one NPC's pursuit as a READ —
the dominant drive, the want it serves, and whether the world would let it
act NOW. Pure: no entropy, no state, no write; the same (pack, projection)
answers the same view.

The three inputs are the ones the engine already owns, never a second
copy (D-024):

- **the drive** comes from the ticker's own parse (`core/drives.py::
  drive_specs` — the pack's declared drive rows joined with the NPC's
  profile) and its own bar (`drive_bar`: weight x the unmet share of the
  goal measure). The DOMINANT drive is the strongest CURRENT bar, ties
  keeping the declaration order (the pack's own order is the law, INV-2).
- **the want** is authored prose: the NPC record's `spine.want` (the
  author's override — AP-9's field, whose first RUNTIME reader this is)
  first, the archetype's own `want` second (the derived SPINE's first
  half — the born person's want comes from the drawn archetype, never
  from a hand-written dossier).
- **the status** is the DOOR's own evaluator, read-only
  (`core/intent.py::first_failing` — the one evaluator, never a second):
  `SATISFIED` when the drive's measure is fully met (the continuity law:
  a met goal stops pushing), `BLOCKED` when a STATIC precondition of the
  drive's verb fails against the frozen projection, `OPEN` otherwise.
  Only the CLOCKED tests (`CLOCKED_TESTS` — leverage / echo) are EXCLUDED
  from the read: their answer moves with the clock alone, so a status
  written at one tick is stale at the next. The EVENT-DRIVEN fold
  (`EVENT_FOLD_TESTS` — `trait_held`) is legal here (iter-439,
  `drivegoals-1`): its verdict moves only when canon commits, and the
  caller passes the fold read it took at its own tick (`traits=`), the
  same triple the beat walk used. A condition the projection alone cannot
  decide never turns the status into a false BLOCKED — the door
  re-validates at its own tick and a failure there is an ATTEMPT, canon
  like any other).

Consumers: the brief's entity cards (`brief/assembler.py::
_present_entity_items` — `drive=<id>:<STATUS>` and `want=<phrase>`, the
person's intent surface beside the body's `look=`/`voice=`). The card is
the one surface: the model has NO memory across beats (PRESENTATION_SPEC
§4: no transcript tail, each call document stands alone), so a fact not in
THIS beat's document does not exist for the narrator — which is why the
persona line is a per-beat card fact, not a sometimes-shown bonus.

The honest boundaries: no priorities, no scheduler, no retention (a drive
does not remember yesterday's failure — the accumulation of pressure is a
separate mechanism, P0-§7's named gap); `BLOCKED` names the FIRST failing
static condition only; and the view is a READING — the ticker still rolls
its own bar against the same measure, so a `SATISFIED` goal is a goal the
roll will not fire this beat either (one measure, one owner).
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.drives import DriveSpec, drive_bar, drive_specs
from core.intent import CLOCKED_TESTS, first_failing
from core.psyche import ROLE_PROP, role_of

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.worldgen import WorldModel

__all__ = [
    "BLOCKED",
    "OPEN",
    "SATISFIED",
    "WANT_MAX_WORDS",
    "AgendaView",
    "agenda_view",
    "agenda_views",
]

#: The status vocabulary (closed, THREE values — the design's own set):
#: the goal is met, the world would let him act now, the world would not.
OPEN: Final = "OPEN"
SATISFIED: Final = "SATISFIED"
BLOCKED: Final = "BLOCKED"

#: The want phrase's authoring bound (the card-budget law): the want is a
#: PHRASE the entity card carries on every beat the person is present, so
#: it is capped at eight words — the pack lint enforces the shape, the
#: brief's `present_entities` budget stays the beneficiary. One owner for
#: the number (the read and the lint), the D-024 law.
WANT_MAX_WORDS: Final = 8


@dataclass(frozen=True, slots=True)
class AgendaView:
    """One NPC's agenda as the brief reads it.

    - `want`: the authored phrase the agenda serves (None when neither the
      record's spine nor the archetype declares one — the line then omits
      the segment, never renders an empty one);
    - `drive` / `status`: the dominant drive's id and its `OPEN` /
      `SATISFIED` / `BLOCKED` read (None together when the NPC carries no
      drive — an authored-spine-only person has a want and no pursuit);
    - `failing`: the first failing static condition (`<noun>.<test>`), or
      None — the reader's dry provenance for a `BLOCKED`;
    - `bar`: the dominant drive's current bar (0 for a satisfied goal).
    """

    npc: str
    want: str | None
    drive: str | None
    status: str | None
    failing: str | None
    bar: int


def _authored_want(pack: "Pack", npc_id: str) -> str | None:
    """The record's `spine.want` — the author's override (AP-9's field)."""
    record = pack.entity(npc_id) if hasattr(pack, "entity") else None
    if not isinstance(record, Mapping):
        return None
    spine = record.get("spine")
    if not isinstance(spine, Mapping):
        return None
    want = spine.get("want")
    return want if isinstance(want, str) and want.strip() else None


def _derived_want(pack: "Pack", archetype_id: str | None) -> str | None:
    """The archetype's `want` — the derived SPINE's first half (a born
    person's want comes from the drawn archetype, never a dossier). Read by
    ROLE (agenda-1 P5): after a turning the role is the new archetype, so
    the card shows what the person is after NOW, not what the author wrote
    about his previous life."""
    config = pack.rules.get("psyche")
    if not isinstance(config, Mapping) or archetype_id is None:
        return None
    for row in config.get("archetypes", ()):
        if isinstance(row, Mapping) and row.get("id") == archetype_id:
            want = row.get("want")
            return want if isinstance(want, str) and want.strip() else None
    return None


def _status(
    pack: "Pack",
    projection: "Projection",
    spec: DriveSpec,
    bar: int,
    world: "WorldModel | None",
    traits: Sequence[Any] = (),
) -> tuple[str, str | None]:
    """The drive's read of the door: SATISFIED when its measure is fully
    met (the continuity law), else BLOCKED when a precondition of its verb
    fails now, else OPEN. The CLOCKED tests are excluded (a clock-driven
    verdict is stale at the caller's tick — see the module docstring); the
    event-driven fold reaches the evaluator through `traits`, which is the
    same read the bar came from."""
    if spec.measure and bar == 0:
        return SATISFIED, None
    action = pack.action(spec.verb)
    requires = (
        tuple(action.get("requires", ()))
        if isinstance(action, Mapping) else ()
    )
    decidable = tuple(
        condition for condition in requires
        if isinstance(condition, Mapping)
        and condition.get("test") not in CLOCKED_TESTS
    )
    failing = first_failing(
        pack, projection, spec.probe, decidable, traits=traits, world=world,
    )
    if failing is not None:
        return BLOCKED, failing
    return OPEN, None


def _view(
    pack: "Pack",
    projection: "Projection",
    npc_id: str,
    specs: Sequence[DriveSpec],
    world: "WorldModel | None",
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
) -> AgendaView | None:
    """One NPC's view from its parsed specs (the shared body of the
    batched and the single read). `echoes` is the caller's fold read —
    the bar's echo-sourced modifiers read it (`core.drives.drive_weight`);
    `traits` is the event-driven fold the measure's `trait_held` rows read
    and the status's door read shares. Passing the walk's own triple is
    what keeps the card honest."""
    role = role_of(pack, projection, npc_id)
    # agenda-1 P5's SUPERSEDE law: a canon turning outranks the authored
    # spine — the author's `want` describes the person BEFORE the turn, and
    # canon says who he is now (the fold-first display-name precedent, the
    # same canon-over-record principle). While no turn exists the authored
    # want keeps D-274's precedence.
    turned = projection.get(npc_id, {}).get(ROLE_PROP) is not None
    want = None if turned else _authored_want(pack, npc_id)
    if want is None:
        want = _derived_want(pack, role)
    if not specs:
        if want is None:
            return None  # neither a want nor a drive: no line at all
        return AgendaView(npc_id, want, None, None, None, 0)
    bars = [
        drive_bar(
            spec, pack, projection, echoes=echoes, traits=traits, world=world,
        )
        for spec in specs
    ]
    best = 0
    for position in range(1, len(specs)):
        if bars[position] > bars[best]:
            best = position  # ties keep the declaration order (INV-2)
    spec = specs[best]
    status, failing = _status(
        pack, projection, spec, bars[best], world, traits,
    )
    return AgendaView(
        npc=npc_id,
        want=want,
        drive=spec.drive,
        status=status,
        failing=failing,
        bar=bars[best],
    )


def agenda_view(
    pack: "Pack",
    projection: "Projection",
    npc_id: str,
    *,
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    world: "WorldModel | None" = None,
) -> AgendaView | None:
    """One NPC's agenda view, or None (no want, no drive). The single-NPC
    form of `agenda_views`: parses the pack's drives and keeps this NPC's.
    `echoes` and `traits` are the caller's fold reads at its own tick (an
    echo-sourced drive modifier moves the bar; a `trait_held` measure reads
    the belief) — the walk, the card and the brief pass the SAME triple, so
    no surface can name a different dominant drive."""
    specs = tuple(
        spec for spec in drive_specs(pack, projection)
        if spec.npc == npc_id
    )
    return _view(pack, projection, npc_id, specs, world, echoes, traits)


def agenda_views(
    pack: "Pack",
    projection: "Projection",
    npc_ids: Collection[str],
    *,
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    world: "WorldModel | None" = None,
    specs: Sequence[DriveSpec] | None = None,
) -> dict[str, AgendaView]:
    """The batched read (the brief's own call): ONE drive parse for the
    whole present set, then each NPC's view — the cost law (the brief's
    per-beat assembly must not re-parse the pack once per card). Order:
    the caller's order is irrelevant (a dict), the parse's declaration
    order is the law. `specs` is the caller's already-parsed tuple: the
    surfaces that need BOTH these views and another drive read (quest-1's
    offer board) parse once and pass the same tuple, so no second parse
    can ever name a different set (the E03 memo law)."""
    by_npc: dict[str, list[DriveSpec]] = {}
    for spec in (specs if specs is not None else drive_specs(pack, projection)):
        by_npc.setdefault(spec.npc, []).append(spec)
    views: dict[str, AgendaView] = {}
    for npc_id in npc_ids:
        view = _view(
            pack, projection, npc_id, by_npc.get(npc_id, ()), world, echoes,
            traits,
        )
        if view is not None:
            views[npc_id] = view
    return views
