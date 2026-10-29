"""The role turn (agenda-1 P5, iter-426 — D-279): a person's ROLE can change
when the accumulated price of events crosses a declared bar, while the
TEMPERAMENT stays his own frozen seed.

Why the split (the owner's 2026-10-26 shape, `iter-425` §1-2): the five
numbers are a fact of birth — copying them would break replay (the same log
would answer different numbers depending on WHEN it is read) and turn seed
data into live counters (iter-416 §6.2). The ARCHETYPE is not the
temperament: it is the role — what the person goes after. That is what a
life can turn: the same stubborn, inward smith who loses his daughter walks
into the woods after the wolves. The drives, the `want`, the entity card and
the brief all bind the archetype, so they follow ONE read (`role_of`) and a
turned person can never show two personalities at once.

Pack vocabulary (all optional — the unarmed law, the 68a pattern: a pack
declaring no `psyche.turnings` keeps every byte and every event of its
corpus, INERT-FIRST measured):

- `rules.json::psyche.turnings[]` — one row per ROLE turn:
  `{from, to, when, notes?}`. `from` / `to` are declared archetypes; `when`
  is a NON-EMPTY list of the door's own closed precondition rows, restricted
  to the ACTOR-ONLY subset (a role turn has no target — a condition naming
  another party would silently never fire, so the lint refuses it). A
  `trait_held` condition reads the durable belief ("this changed who he
  is"), an `echo_at_least` condition the decaying residue ("while it has not
  let go") — the pack chooses.
- `rules.json::psyche.turning_event` — the event type a turn emits (a
  template-vocabulary member).

The probe id names the DECLARATION, never its position (`probeids-1`'s law,
iter-436; the turning half is `turnids-1`, iter-437): `turn_<npc>_<from>_<to>`
— the carrier, the role it holds and the role the row makes it. The family is
the ONE probe whose id reaches no observable surface today: a turn is
committed as a canon event, never enqueued (no `cause_intent` in the
provenance, no OCC snapshot entry, and `first_failing` never reads the id), so
the longest, most legible address costs exactly zero bytes — the
readable-vs-log-size tradeoff iter-436 §2 had to weigh does not exist here.
Uniqueness: `(from, to)` is unique by the pack lint (a duplicate row can never
fire — dead data, `core/packlint/psyche.py::_turnings`), so the pair names one
declaration and the npc names one carrier.

The transition is a CANON EVENT, never stored state: one draft per npc per
beat, carrying `StateChange(npc, "archetype", current -> to)`. `current` is
what the projection holds (None while the person still carries the born
role — canon never modeled it, the birth-home law). The cause is the belief's
own source event (the event that last completed the family the condition
names — the honest "what broke him"), or, when the condition is not a
belief, the caller's chain (`cause`, the scheduled-beat convention).

Irreversible by construction: the condition is bound to the `from` role, and
after the turn the person no longer holds it — no yo-yo, no cooldown, no
second state. A back-turn exists only if the pack declares a back-row (that
is content, deliberately authored, not a runtime default).

No entropy: the condition is a threshold over derived reads, not a roll —
the ticker's draw count, its streams and the fingerprint are untouched.
What IS touched is the drive SET (the role's drives), so a pack declaring
turnings parses its drive specs per beat and the quiet-beat skip lands on the
very next beat while a turn is possible (`turning_pending` — the same law
the profile birth follows, `condensation_pending`'s twin).
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.intent import IntentData, first_failing, pack_importance
from core.log import EventDraft, StateChange
from core.psyche import ROLE_PROP, role_of

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.traits import Trait

__all__ = [
    "TURNINGS_KEY",
    "TURNING_EVENT_KEY",
    "TURN_PREFIX",
    "TurningSpec",
    "turning_demand",
    "turning_drafts",
    "turning_pending",
    "turning_specs",
    "turns_declared",
]

#: The psyche block's turning halves (the role layer's one home).
TURNINGS_KEY: Final = "turnings"
TURNING_EVENT_KEY: Final = "turning_event"

TURN_PREFIX: Final = "turn"  # intent ids (turn_<npc>_<from>_<to>)


@dataclass(frozen=True, slots=True)
class TurningSpec:
    """One (npc, declared turn) pair: the person, the role he holds now, the
    role the row would make him, the row's own closed conditions and the
    probe the shared evaluator reads them through."""

    npc: str
    from_role: str
    to_role: str
    when: tuple[Mapping[str, Any], ...]
    probe: IntentData


def _block(pack: "Pack") -> Mapping[str, Any] | None:
    config = pack.rules.get("psyche")
    return config if isinstance(config, Mapping) else None


def turns_declared(pack: "Pack") -> bool:
    """Does the pack declare any turn? The loop's parse-law gate: a pack with
    turns re-parses the drive specs per beat (the drive SET depends on the
    live role — `core.psyche.role_of`)."""
    config = _block(pack)
    if config is None:
        return False
    rows = config.get(TURNINGS_KEY)
    return isinstance(rows, (list, tuple)) and bool(rows)


def turning_demand(pack: "Pack") -> frozenset[str]:
    """The tests the turning rows read — the beat fold's DEMAND twin (the
    E04 law, `core.loop._fold_demand`): the clock computes a derived fold
    only when the pack declares a consumer, so a turning row whose only
    fold reader it is MUST declare itself here — otherwise the price is
    never computed and the turn can never fire (the silent-dead-gate trap
    this twin closes)."""
    config = _block(pack)
    if config is None:
        return frozenset()
    rows = config.get(TURNINGS_KEY)
    if not isinstance(rows, (list, tuple)):
        return frozenset()
    return frozenset(
        str(condition.get("test"))
        for row in rows
        if isinstance(row, Mapping)
        for condition in row.get("when", ())
        if isinstance(condition, Mapping)
    )


def turning_specs(
    pack: "Pack", projection: "Projection | None" = None,
) -> tuple[TurningSpec, ...]:
    """The (npc, turn) pairs alive right now: every declaring npc whose
    CURRENT role is the row's `from`, in row declaration order then npc
    declaration order (INV-2 — the pack's own order is the canon order)."""
    config = _block(pack)
    if config is None:
        return ()
    rows = config.get(TURNINGS_KEY)
    if not isinstance(rows, (list, tuple)) or not rows:
        return ()
    state: Mapping[str, Mapping[str, Any]] = projection or {}
    npcs = [
        str(npc["id"]) for npc in pack.entities.get("npcs", ())
    ]
    specs: list[TurningSpec] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue  # the lint owns the shape — this is the read-side check
        when = tuple(row.get("when", ()))
        from_role = str(row["from"])
        to_role = str(row["to"])
        for npc_id in npcs:
            if role_of(pack, state, npc_id) != from_role:
                continue
            specs.append(
                TurningSpec(
                    npc=npc_id,
                    from_role=from_role,
                    to_role=to_role,
                    when=when,
                    probe=IntentData(
                        # turnids-1 (iter-437): the id names the (carrier,
                        # declaration) pair, never the position — the
                        # `probeids-1`/`roster-2` law family's last member.
                        # The row lint refuses a duplicate (from, to) (dead
                        # data), so the pair names one declaration; a probe's
                        # repeats keep the id (the OCC FIFO's designed case).
                        id=f"{TURN_PREFIX}_{npc_id}_{from_role}_{to_role}",
                        kind=to_role,
                        actor=npc_id,
                        target=None,
                        fields={},
                        based_on_event_seq=0,
                    ),
                )
            )
    return tuple(specs)


def _rolls(
    projection: "Projection",
    npc_id: str,
    locations: Collection[str] | None,
) -> bool:
    """The turning check's rolling predicate — the drive family's own law
    (`core.drives.drive_rolls`): present in the projection, positioned inside
    the ticking zone (None = the unarmed one-scene world) and not caught. A
    diverging copy would desync the quiet-beat skip against the beat walk, so
    both read THIS function."""
    if npc_id not in projection:
        return False
    if locations is not None and projection[npc_id].get("position") not in locations:
        return False
    return projection[npc_id].get("crime_status") != "caught"


def _crossed(
    pack: "Pack",
    projection: "Projection",
    spec: TurningSpec,
    facts: Sequence[Any],
    echoes: Sequence[Any],
    traits: Sequence[Any],
) -> bool:
    """Has the price crossed? The shared evaluator answers the row's own
    closed conditions — an empty `when` would trivially pass, so the lint
    requires it non-empty (this check is the read-side backstop)."""
    if not spec.when:
        return False
    failing = first_failing(
        pack, projection, spec.probe, spec.when,
        facts=facts, echoes=echoes, traits=traits,
    )
    return failing is None


def turning_pending(
    pack: "Pack",
    projection: "Projection",
    *,
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    locations: Collection[str] | None = None,
) -> bool:
    """Would `turning_drafts` answer non-empty here? — the pure EMPTINESS
    TWIN for the quiet-beat skip (zero draws, zero events): any rolling
    npc whose conditions already hold. The skip lands on the very next beat
    when this is true, because a turn changes the DRIVE SET and a skipped
    beat would straddle it."""
    if not turns_declared(pack):
        return False
    for spec in turning_specs(pack, projection):
        if not _rolls(projection, spec.npc, locations):
            continue
        if _crossed(pack, projection, spec, facts, echoes, traits):
            return True
    return False


def _belief_cause(
    traits: Sequence["Trait"], spec: TurningSpec,
) -> str | None:
    """The belief's own source event: the newest record of the family
    condition that fired (the closest honest cause — the event that last
    completed the family, never a guessed one). None when the row's
    conditions name no belief."""
    tokens = {
        str(condition["token"])
        for condition in spec.when
        if isinstance(condition, Mapping)
        and condition.get("test") == "trait_held"
        and isinstance(condition.get("token"), str)
    }
    if not tokens:
        return None
    for trait in traits:
        if trait.who != spec.npc or trait.token not in tokens:
            continue
        if trait.sources:
            return trait.sources[-1]
    return None


def turning_drafts(
    pack: "Pack",
    projection: "Projection",
    *,
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
    traits: Sequence["Trait"] = (),
    cause: str,
    tick: int,
    locations: Collection[str] | None = None,
) -> tuple[EventDraft, ...]:
    """Draft this beat's role turns: at most ONE per npc (the first declared
    row that crossed — INV-2), each an ordinary canon event the caller
    commits through the door so its reactions cascade like any other fact's.

    `cause` is the caller's chronological chain, used when the row's
    conditions name no belief (a turn still needs a cause: the log allows a
    null one on the run-start event only)."""
    config = _block(pack)
    if config is None:
        return ()
    event_type = config.get(TURNING_EVENT_KEY)
    if not isinstance(event_type, str) or not event_type:
        return ()  # no rows or no event type: the unarmed law
    drafts: list[EventDraft] = []
    turned: set[str] = set()
    for spec in turning_specs(pack, projection):
        if spec.npc in turned:
            continue  # one turn per person per beat
        if not _rolls(projection, spec.npc, locations):
            continue
        if not _crossed(pack, projection, spec, facts, echoes, traits):
            continue
        turned.add(spec.npc)
        drafts.append(
            EventDraft(
                t=tick,
                type=event_type,
                actor=spec.npc,
                target=None,
                cause=_belief_cause(traits, spec) or cause,
                outcome={"from": spec.from_role, "to": spec.to_role},
                state_changes=(
                    StateChange(
                        entity=spec.npc,
                        prop=ROLE_PROP,
                        from_=projection.get(spec.npc, {}).get(ROLE_PROP),
                        to_=spec.to_role,
                    ),
                ),
                importance=pack_importance(
                    pack.rules, {spec.npc}, irreversible=0, hooks=0,
                    event_type=event_type,
                ),
            )
        )
    return tuple(drafts)
