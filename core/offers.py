"""The derived offer board (quest-1 v0, A3; iter-435).

The question this module answers, stated so it can be refuted: **what can be
derived, from canonical state alone, as "this person needs X and this act
would close it"?** Nothing here is authored per quest (D-266 — no quest
subsystem, no scripted arcs). A need IS a drive's failing `measure` row; the
closing act IS the drive's own verb (the act the ticker would enqueue); the
terms ARE that verb's declared `account` block; the blocker IS the door's own
`first_failing`; the receipt IS the measure's collapse plus, where the closing
act moves a stock, that stock's change. The board is one read of four existing
owners, it writes nothing, and it invents no term.

Why the read is exact where it claims exactness:

- a row of `ACCOUNT_TEST`/`ACCOUNT_CEILING_TEST` carries `(holder, kind,
  value)`, and the closing verb's declared stock movement on that pair is
  computable from the pack alone — `consume`/`source`/`transfer`/`settle`/
  `convert` (+ the recipe's legs). A floor needs a POSITIVE delta on the
  holder, a ceiling a NEGATIVE one; `payable` is that comparison, never a
  guess. The corpus's own counter-example reproduces by computation: a coin
  floor on a holder no committed verb feeds is `payable=False`.
- a need row may declare `helper_verb` (iter-442, D-288): the act a THIRD
  PARTY performs to close it — the act the card's reader (the player) can
  actually take. The board then offers THAT act, `payable` from the same
  arithmetic with the holder as the act's COUNTERPARTY (a transfer to them, a
  recipe leg to them, a `settle` leg to them), and `blocked` from ITS own
  requirements read on the PLAYER's probe (`pack.player_id()`): the gate the
  reader would meet, never the owner's. A row without the key reads exactly
  as v0 did (every committed pack: zero bytes).
- a row of `STATIC_TESTS` reads the PACK RECORD (`core/intent.py::_Ctx.record`),
  which canon never writes — `payable=False` is a law, not a judgement. The
  pack lint refuses such a row in a `measure` outright (deadmeasure-1,
  iter-439), so this arm is the defensive half of the same law, never a shape
  a loaded pack can still carry.
- any other canon read (position, carrier, spot, the event-driven fold) is
  `payable=None`: v0 does not model a non-account act's effect, and an honest
  "?" beats a guess.

A `CLOCKED_TESTS` row (`leverage_over`, `echo_at_least` — the windowed family's
clock-driven half) is NOT offered: its verdict moves with the clock alone, so
the board would print a need that changes between two reads of the same state.
The card's status law excludes the same pair for the same reason (iter-420).
The windowed family's EVENT-driven half (`trait_held`) IS offered (iter-439,
`drivegoals-1`): the knowledge records are canon, the verdict moves only when
canon commits, and the caller passes the fold read (`traits=`) it took at its
own tick. The board is canon-derived or it says nothing.

Honest limits: the board derives from the DOMINANT drive only — the same
dominance `core.agenda` owns (D-024, no second read); the `need=` phrase is
the narrator's line and never a term, read from the OFFERED DRIVE's own
`need` (`psyche.drives[].need`, needphrase-1, iter-446) and falling back to
the person's `spine.need` when the row declares none — so the sentence
follows the pursuit it stands beside, and a two-pursuit person changes words
when his dominating drive changes (the per-person phrase it replaced is
iter-445 §6's measured defect); a payable need may still be refused at the
door today (`blocked` names that condition); and a single act is modelled,
never a path (earn-then-pay is not a v0 shape).

Non-goals: no schedule, no pressure memory, no commitment object. A promise
paid later by someone else is a different question (the duty family's own
review), and this module deliberately has no opinion about it.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.agenda import agenda_views
from core.drives import DriveSpec, drive_specs
from core.intent import (
    ACCOUNT_CEILING_TEST,
    ACCOUNT_TEST,
    CLOCKED_TESTS,
    STATIC_TESTS,
    IntentData,
    first_failing,
)

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack

__all__ = ["Offer", "act_delta", "offers"]

#: The stock-comparing tests (the two forms the terms law understands).
_ACCOUNT_TESTS: Final = (ACCOUNT_TEST, ACCOUNT_CEILING_TEST)


@dataclass(frozen=True, slots=True)
class Offer:
    """One derived need: the terms, the closing act, and how far the act is.

    - `npc` / `drive`: whose pursuit, and WHICH drive (the dominant one —
      the agenda's own read);
    - `need`: the board's phrase for THIS pursuit — the drive's own authored
      `need` row, falling back to the person's `spine.need` when the row
      declares none (needphrase-1, iter-446: one sentence per PURSUIT, never
      one per person), or None when neither declares one — a phrase for the
      narrator, never a term;
    - `where`: the failing condition as the door names it (`<noun>.<test>`);
    - `kind` / `held` / `required` / `deficit`: the stock terms — present
      only for the account family (None otherwise). `deficit` is what still
      separates the stock from the bar (the floor's `required - held`, the
      ceiling's `held - required`);
    - `verb`: the closing act — the drive's own verb;
    - `payable`: True when that verb's declared stock movement closes this
      test's direction, False when no declared act can (a pack-static read,
      or a stock no verb feeds), None when v0 does not model the act's
      effect (an honest unknown, never a guess);
    - `blocked`: the verb's own static gate that would refuse the act RIGHT
      NOW (`<holder>.<test>`), or None — "closable in principle" and "will
      pass" are two different statements and the board prints both.
    """

    npc: str
    drive: str
    need: str | None
    where: str
    test: str
    kind: str | None
    held: int | None
    required: int | None
    deficit: int | None
    verb: str
    payable: bool | None
    blocked: str | None

    def segments(self) -> tuple[str, ...]:
        """The board's text form — the ONE owner of the sentence the card
        and the `mechanics offers` read both print, so no surface can name
        a different board (the iter-432 §6 asymmetry check)."""
        if self.held is not None and self.required is not None:
            out = [f"offer={self.verb} {self.held}/{self.required}"]
        else:
            out = [f"offer={self.verb}"]
        if self.payable is False:
            out.append("payable=no")
        elif self.payable is None:
            out.append("payable=?")
        if self.blocked is not None:
            out.append(f"blocked={self.blocked}")
        if self.need is not None:
            out.append(f"need={self.need}")
        return tuple(out)


def _spine_need(pack: "Pack", npc: str) -> str | None:
    """The record's `spine.need` — the board's FALLBACK phrase (AP-9's
    field; the drive's own `need` outranks it, needphrase-1, iter-446).
    Absent, empty or non-string answers None (the born person carries no
    dossier, and the card's `want=` already speaks for the role — no second
    truth)."""
    record = pack.entity(npc) if hasattr(pack, "entity") else None
    if not isinstance(record, Mapping):
        return None
    spine = record.get("spine")
    if not isinstance(spine, Mapping):
        return None
    need = spine.get("need")
    return need if isinstance(need, str) and need.strip() else None


def _need(pack: "Pack", spec: DriveSpec) -> str | None:
    """The board's phrase for this offer: the DRIVE's own `need` first, the
    person's recorded `spine.need` when the row declares none (needphrase-1,
    iter-446). The order is the `spine.want` law one slot over
    (`core.agenda`): the most specific authored form wins, the person level
    is the fallback — never the reverse, because a record phrase describes
    the person's whole life while the offer names ONE pursuit."""
    return spec.need if spec.need is not None else _spine_need(pack, spec.npc)


def _holder(
    pack: "Pack", spec: DriveSpec, cond: Mapping[str, Any]
) -> str | None:
    """The entity a measure row's stock belongs to: the explicit `holder`
    form, the `actor` noun (the probe's own actor) or the `target` noun
    (the probe's target — absent answers None: the row names nothing the
    board can read)."""
    holder = cond.get("holder")
    if isinstance(holder, str) and holder:
        return holder
    noun = cond.get("noun")
    if noun == "actor":
        return spec.probe.actor
    if noun == "target" and spec.probe.target is not None:
        return spec.probe.target
    return None


def _recipe(pack: "Pack", recipe_id: str) -> Mapping[str, Any] | None:
    economy = pack.rules.get("economy")
    if not isinstance(economy, Mapping):
        return None
    for row in economy.get("recipes", ()):
        if isinstance(row, Mapping) and row.get("id") == recipe_id:
            return row
    return None


def act_delta(
    pack: "Pack",
    verb: str,
    entity: str,
    kind: str,
    *,
    actor: str | None = None,
    target: str | None = None,
) -> int:
    """The declared stock movement of `verb` on `(entity, kind)` — the pack's
    own terms, read from the `account` block's five forms and (for `convert`)
    the recipe's legs. Never a heuristic: a form v0 does not know answers 0
    (no declared movement), which keeps `payable` conservative.

    The ONE arithmetic the board and the pack lint both read (iter-442,
    D-288): `actor`/`target` are the act's doer and counterparty — the drive
    probe's own pair for the autonomy's act, and the need's HOLDER as the
    target for a helper act (`actor=None`: the movement a third party's act
    delivers TO the holder, so `transfer` targets, `settle` legs and
    `convert` recipe legs all read without inventing a payer)."""
    action = pack.action(verb)
    block = action.get("account") if isinstance(action, Mapping) else None
    if not isinstance(block, Mapping):
        return 0
    form = block.get("verb")
    amount = block.get("amount")
    # the act's own KIND is the first filter of the single-kind forms (iter-442:
    # a `pass_the_seat` gift of paper is not a coin movement — the helper lint
    # exposed the old false credit, which would have printed `payable=True` for
    # a gift of another kind; the multi-kind forms filter per leg already)
    if form in ("consume", "source", "transfer") and block.get("kind") != kind:
        return 0
    if form == "consume":
        return -int(amount) if entity == actor else 0
    if form == "source":
        return int(amount) if entity == actor else 0
    if form == "transfer":
        if entity == actor:
            return -int(amount)
        if target is not None and entity == target:
            return int(amount)
        return 0
    if form == "settle":
        delta = 0
        for leg in block.get("legs", ()):
            if not isinstance(leg, Mapping) or leg.get("kind") != kind:
                continue
            if leg.get("from") == entity:
                delta -= int(leg["amount"])
            if leg.get("to") == entity:
                delta += int(leg["amount"])
        return delta
    if form == "convert":
        recipe = _recipe(pack, str(block.get("recipe")))
        if recipe is None:
            return 0
        delta = 0
        for side, sign in (("inputs", -1), ("outputs", 1)):
            for leg in recipe.get(side, ()):
                if not isinstance(leg, Mapping):
                    continue
                if leg.get("holder") == entity and leg.get("kind") == kind:
                    delta += sign * int(leg["amount"])
        return delta
    return 0


def _payable(
    pack: "Pack",
    spec: DriveSpec,
    verb: str,
    cond: Mapping[str, Any],
    holder: str | None,
    *,
    helper: bool,
) -> bool | None:
    """The terms law: True when the declared stock movement closes the
    test's direction, False when the read can never move (pack-static), None
    when v0 does not model this act's effect (the honest unknown). A helper
    act is read with the need's holder as the act's COUNTERPARTY (the
    movement a third party's act delivers to them, `actor=None`); the
    drive's own act is read with its probe's own actor/target (unchanged,
    byte-identical for every pack without a helper row)."""
    test = cond.get("test")
    if test in STATIC_TESTS:
        return False
    if test not in _ACCOUNT_TESTS or holder is None:
        return None
    kind = cond.get("kind")
    if not isinstance(kind, str) or not kind:
        return None
    if helper:
        delta = act_delta(pack, verb, holder, kind, target=holder)
    else:
        delta = act_delta(
            pack, verb, holder, kind,
            actor=spec.probe.actor, target=spec.probe.target,
        )
    return delta > 0 if test == ACCOUNT_TEST else delta < 0


def _helper(cond: Mapping[str, Any]) -> str | None:
    """The row's declared helper act (`helper_verb`, iter-442/D-288): the act
    a THIRD PARTY — the reader, the player — performs to close the need. The
    lint refuses a helper that walks no stock of the measured kind, so the
    board never prints a helper nobody can carry out."""
    helper = cond.get("helper_verb")
    return helper if isinstance(helper, str) and helper else None


def _blocked(
    pack: "Pack",
    projection: "Projection",
    probe: Any,
    verb: str,
    world: Any,
    traits: Sequence[Any] = (),
) -> str | None:
    """The act's own preconditions, read through the door — a targetless
    probe whose verb demands one cannot even be evaluated, and the board
    says so instead of pretending the act is free. `probe` is the act's
    DOER: the drive's own probe for the autonomy's act, the PLAYER's probe
    for a helper act (the gate the reader would meet, `_offer`). The clocked
    pair is skipped (the caller's tick cannot decide it); the event-driven
    fold reaches the evaluator through `traits`, the same read the bar used."""
    action = pack.action(verb)
    requires = (
        tuple(action.get("requires", ()))
        if isinstance(action, Mapping)
        else ()
    )
    decidable = tuple(
        cond for cond in requires
        if isinstance(cond, Mapping)
        and cond.get("test") not in CLOCKED_TESTS
    )
    try:
        return first_failing(
            pack, projection, probe, decidable, traits=traits,
            world=world,
        )
    except Exception:  # RunnerError: the probe cannot resolve a noun
        return "intent.noun"


def _offer(
    pack: "Pack",
    projection: "Projection",
    spec: DriveSpec,
    cond: Mapping[str, Any],
    world: Any,
    traits: Sequence[Any] = (),
) -> Offer:
    """One row's offer: the numbers only where the terms law reads them."""
    test = str(cond.get("test"))
    kind = (
        str(cond["kind"])
        if test in _ACCOUNT_TESTS and isinstance(cond.get("kind"), str)
        else None
    )
    holder = _holder(pack, spec, cond)
    held: int | None = None
    required: int | None = None
    deficit: int | None = None
    if test in _ACCOUNT_TESTS and kind is not None and holder is not None:
        level = projection.get(holder, {}).get(f"account.{kind}")
        if isinstance(level, int) and not isinstance(level, bool):
            held = level
        value = cond.get("value")
        if isinstance(value, int) and not isinstance(value, bool):
            required = value
        if held is not None and required is not None:
            deficit = (
                required - held if test == ACCOUNT_TEST else held - required
            )
    helper = _helper(cond)
    verb = helper or spec.verb
    if helper is not None and holder is not None:
        # the READER's sentence (iter-442): the helper act is taken by a
        # third party — the player — so its gate is read on the player's own
        # probe at the need's holder (the payer's position and stock decide
        # the `blocked=` token, never the owner's).
        probe = IntentData(
            id=spec.probe.id,
            kind=helper,
            actor=pack.player_id(),
            target=holder,
            fields={},
            based_on_event_seq=0,
        )
        blocked = _blocked(pack, projection, probe, helper, world, traits)
    else:
        blocked = _blocked(pack, projection, spec.probe, verb, world, traits)
    return Offer(
        npc=spec.npc,
        drive=spec.drive,
        need=_need(pack, spec),
        where=f"{cond.get('noun') or cond.get('holder', '?')}.{test}",
        test=test,
        kind=kind,
        held=held,
        required=required,
        deficit=deficit,
        verb=verb,
        payable=_payable(pack, spec, verb, cond, holder, helper=helper is not None),
        blocked=blocked,
    )


def offers(
    pack: "Pack",
    projection: "Projection",
    npc_ids: Collection[str],
    *,
    echoes: Sequence[Any] = (),
    traits: Sequence[Any] = (),
    world: Any = None,
    specs: Sequence[DriveSpec] | None = None,
) -> tuple[Offer, ...]:
    """The board for the given people: one `Offer` per failing CANON measure
    row of each person's DOMINANT drive, in the caller's order and the
    pack's own measure order (INV-2 — declaration order is canon order).

    `specs` is the caller's already-parsed tuple (the brief that needs both
    the views and the board parses ONCE — the E03 memo law). `echoes`/
    `traits`/`world` are the same fold reads `agenda_views` takes, so the
    dominance and the bar are the card's own numbers, never a re-derivation.
    """
    parsed = specs if specs is not None else drive_specs(pack, projection)
    views = agenda_views(
        pack, projection, npc_ids, echoes=echoes, traits=traits, world=world,
        specs=parsed,
    )
    by_key = {(spec.npc, spec.drive): spec for spec in parsed}
    board: list[Offer] = []
    for npc in npc_ids:
        view = views.get(npc)
        if view is None or view.drive is None:
            continue
        spec = by_key.get((npc, view.drive))
        if spec is None:
            continue
        for cond in spec.measure:
            if not isinstance(cond, Mapping):
                continue
            if cond.get("test") in CLOCKED_TESTS:
                continue  # the clock-driven half is not canon-derived (docstring)
            failing = first_failing(
                pack, projection, spec.probe, (cond,), echoes=echoes,
                traits=traits, world=world,
            )
            if failing is None:
                continue
            board.append(_offer(pack, projection, spec, cond, world, traits))
    return tuple(board)
