"""The goal/urge ticker (P2b, D-021, phase0 §4): NPC goals → occasional
autonomous action through the same queue and tick discipline as
playscript intents. Small-formula dynamics (KeeperRL rebellion): a few
numeric formulas over knowledge and state, not a planner. Full LLM
planning — never (`VISION.md` §6; Generative Agents is the cost
anti-precedent).

Urgencies are pack data: per-NPC goal specs with a probability roll
per beat, an intent template (kind / target / fields), and optional
precondition tests (the closed set in `core/intent.py`). A roll that
hits AND passes the preconditions yields an IntentData enqueued as
`kind="intent"` band `NPC_REACTION` — the front door validates it like
any playscript step. A roll that hits but fails preconditions stays
silent (the NPC tried, the world said no — no rejection event; the
world's noise floor absorbs autonomous attempts that don't fire).

Through-the-door discipline (D-037): urgencies never write canon
directly. They broadcast objectives through the intent door; the loop
runs the same front-door / OCC / resolver pipeline the player's
intents use. The world's logic is one mechanism, not two — M5
(non-PC event share) becomes non-trivially non-zero by construction.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.ids import sequence_id
from core.intent import IntentData, first_failing

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack
    from core.rng import RngBank

__all__ = ["URGENCY_PREFIX", "urgency_intents"]

URGENCY_PREFIX: Final = "urgency"


@dataclass(frozen=True, slots=True)
class _UrgencySpec:
    """One pack-declared urgency for one NPC (rules.json `urgencies.entries`).

    - `probability_per_beat` (0..100): d100 ≤ probability fires the
      intent attempt this beat.
    - `intent`: template for the IntentData (kind, optional target,
      fields).
    - `requires`: optional preconditions (the closed test set in
      `core/intent.py`). An attempt whose preconditions fail stays
      silent — the NPC tried, the world said no.
    """

    npc: str
    probability_per_beat: int
    intent_kind: str
    intent_target: str | None
    intent_fields: Mapping[str, Any]
    requires: tuple[Mapping[str, Any], ...]


def _specs(pack: "Pack") -> tuple[_UrgencySpec, ...]:
    """Parse the pack's `urgencies.entries` (load order: pack-declared;
    the runner respects it as given — INV-2 via sorted() at load)."""
    config = pack.rules.get("urgencies", {})
    entries = config.get("entries", ())
    specs: list[_UrgencySpec] = []
    for entry in entries:
        specs.append(
            _UrgencySpec(
                npc=entry["npc"],
                probability_per_beat=int(entry["probability_per_beat"]),
                intent_kind=entry["intent"]["kind"],
                intent_target=entry["intent"].get("target"),
                intent_fields=dict(entry["intent"].get("fields", {})),
                requires=tuple(entry.get("requires", ())),
            )
        )
    return tuple(specs)


def _build_intent(spec: _UrgencySpec, seq: int) -> IntentData:
    """Materialize an IntentData from a pack spec; the loop stamps the
    real `based_on_event_seq` at enqueue time."""
    return IntentData(
        id=sequence_id(URGENCY_PREFIX, seq),
        kind=spec.intent_kind,
        actor=spec.npc,
        target=spec.intent_target,
        fields=spec.intent_fields,
        based_on_event_seq=0,
    )


def urgency_intents(
    pack: "Pack",
    projection: "Projection",
    bank: "RngBank",
) -> list[IntentData]:
    """One beat's worth of autonomous NPC intents (P2b). For each
    pack-declared urgency: roll d100 against `probability_per_beat`; on
    a hit, run the preconditions against the projection; if all pass,
    yield the IntentData. The loop enqueues them through the intent
    door (band NPC_REACTION) at the popped entry's tick, so they
    execute after the player's intents in the same tick (the
    entry-tick enqueue law, D-039)."""
    out: list[IntentData] = []
    for seq, spec in enumerate(_specs(pack)):
        # skip actors absent from the projection (arrested, fled, removed)
        if spec.npc not in projection:
            continue
        if projection[spec.npc].get("crime_status") == "caught":
            continue
        # the roll: d100 ≤ probability (substantive stream — canon rolls)
        if bank.randint(1, 100) > spec.probability_per_beat:
            continue
        intent = _build_intent(spec, seq)
        if spec.requires:
            failing = first_failing(pack, projection, intent, list(spec.requires))
            if failing is not None:
                continue  # the world said no — silent, no rejection event
        out.append(intent)
    return out
