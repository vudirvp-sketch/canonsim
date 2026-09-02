"""The psychological echo (social-2, phase 3; `phases.md` §3 P3e — the
CORE_DESIGN_RESEARCH sketch: NPC behavior carries the emotional residue
of past events — a watcher who saw a fire is jittery next morning).
The runtime block is `rules.json::echo` (linted by `core/pack.py::_echo`).

The echo is a READ MODEL, not a reaction (the sketch's law: "not new
data, a behavior modifier computed from the existing log"): a pure fold
over the knowledge view — a record whose token the pack's `echo.tokens`
table values contributes its valence, decaying linearly with the ticks
since it was learned. The module writes NOTHING: no events, no
knowledge, no hooks, no state changes (INV-1 by construction — the
leverage birth minted facts; the echo never even does that). It renders
nothing (templates untouched) and feeds no metric (no events to
classify) — the residue becomes visible only through the behavior it
gates.

The consumer is behavior selection, exactly as the sketch's P2b
dependency names it: the intent door's `echo_at_least` precondition
(`core/intent.py`'s closed test set) — an urgency whose `requires` gate
on it fires only while the residue is high enough, the same
through-the-door discipline as every autonomous intent (D-037). The
fold is read as DATA at each evaluation point, at the CALLER'S OWN
TICK (the iter-45 window law: the door at the entry tick, the urgency
gate at the beat, the OCC re-check at completion — the residue decays
by time, so a tick-windowed gate is never evaluated on stale scores).
Duck-typed (who/axis/score attributes): `core.intent` never imports
`core.echo` (the import direction stays one-way; this module owns the
score type).

The L6 fence: the echo is per-NPC valence over the NPC's OWN records —
never player-adapted, and never an entropy input (the director reads
observable state only, DIRECTOR_SPEC §4; a knowledge-derived score is
not observable state). The director is untouched by construction.

The formula (every number is pack data, INV-3): per record,
contribution = weight * (fades_ticks - age) * fidelity_percent //
(fades_ticks * 100) — integer arithmetic, floored, deterministic
(INV-2); at age 0 the full weight at 100 percent, dead at the boundary
tick (the leverage expiry law's twin), a token learned again renews the
residue (both records sum — heard twice, felt twice). The per-axis sum
clamps to the pack's scale; an axis with no residue for a knower is
absent from the tuple (a missing pair reads as zero — the world's
honest answer, never an error)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:  # pack + view are duck-typed — no runtime imports
    from core.knowledge import KnowledgeView
    from core.pack import Pack

__all__ = [
    "ECHO_BLOCK_KEYS",
    "ECHO_TOKEN_KEYS",
    "EchoScore",
    "echo_scores",
]

ECHO_BLOCK_KEYS: Final = ("scale", "fidelity_weight", "tokens", "notes")
"""The closed `rules.json::echo` key set (an unknown key is a lint
error, never a silent ignore): the score scale, the per-fidelity
percent table, the token valence table, prose."""

ECHO_TOKEN_KEYS: Final = ("fades_ticks", "axes")
"""The closed per-token key set: the decay window in ticks (the
residue's lifetime — dead at the boundary tick itself) and the per-axis
valence weights (the pack's own axis vocabulary; a non-zero integer —
valence has a sign, the pack declares which)."""


@dataclass(frozen=True, slots=True)
class EchoScore:
    """One knower's residue on one axis as derived by the read-side fold
    (`echo_scores`). Zero-residue pairs are absent from the tuple — the
    consumer's missing pair reads as zero (the honest answer)."""

    who: str
    axis: str
    score: int


def echo_scores(
    pack: "Pack",
    view: "KnowledgeView",
    at_tick: int,
) -> tuple[EchoScore, ...]:
    """The read-side fold: every knower's non-zero residue on every
    declared axis, at `at_tick`. Knowers in first-acquisition order,
    axes in token-declaration order (both deterministic); the sums
    themselves are order-free integer arithmetic. A pack without an
    `echo` block folds to the empty tuple (the v0.1 behavior — the
    pack's own declaration is the gate, INV-3). A record born after
    `at_tick` contributes nothing (the read model at that tick — it
    cannot happen inside the loop, where evaluation ticks never precede
    commits; the age check keeps the fold honest for any caller)."""
    config: Mapping[str, Any] | None = pack.rules.get("echo")
    if config is None:
        return ()
    tokens: Mapping[str, Mapping[str, Any]] = config["tokens"]
    lo, hi = config["scale"]
    percents: Mapping[str, int] = config["fidelity_weight"]
    axes: list[str] = []  # declared order, deduped
    declared: set[str] = set()
    for spec in tokens.values():
        for axis in spec["axes"]:
            if axis not in declared:
                declared.add(axis)
                axes.append(axis)
    out: list[EchoScore] = []
    for who in view.knowers():
        sums = dict.fromkeys(axes, 0)
        for record in view.records_of(who):  # acquisition order
            spec = tokens.get(record.knows)
            if spec is None or record.at > at_tick:
                continue
            fades = int(spec["fades_ticks"])
            age = at_tick - record.at
            if age >= fades:
                continue  # dead at the boundary tick (the expiry twin)
            percent = percents[record.fidelity]
            for axis, weight in spec["axes"].items():
                sums[axis] += int(weight) * (fades - age) * percent // (fades * 100)
        for axis in axes:
            score = max(int(lo), min(int(hi), sums[axis]))
            if score:
                out.append(EchoScore(who=who, axis=axis, score=score))
    return tuple(out)
