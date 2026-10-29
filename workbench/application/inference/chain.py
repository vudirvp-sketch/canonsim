"""The sampler chain's membership/order semantics (the law's §11 —
ssi-4 step 1, extracted verbatim): ChainItem, the default 9-member
document (the reviewed runtime's own order), the inf-1 -> inf-2 load
upgrade. Membership is a FAMILY concern — the chain id -> value-
control mapping (CHAIN_FAMILIES) lives in the library; the ids are
the runtime's own `--samplers` names, two vocabularies one mapping.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from workbench.application.inference.library import SAMPLER_CHAIN_IDS

# ---------------------------------------------------------------- the chain


@dataclass(frozen=True)
class ChainItem:
    """One sampler chain member's profile state (the law's §11): a
    sampler chain is an ORDERED semantic object — membership +
    position are first-class, never a favorites grid. `enabled`
    decides whether the member is emitted into `--samplers`."""

    id: str
    enabled: bool


#: The chain's default document (the reviewed runtime's own order,
#: every member enabled).
DEFAULT_CHAIN: tuple[ChainItem, ...] = tuple(
    ChainItem(member, True) for member in SAMPLER_CHAIN_IDS
)


def _upgrade_chain(loaded: Mapping[str, bool]) -> tuple[ChainItem, ...]:
    """The inf-1 → inf-2 chain upgrade (the load-time normalization):
    a 5-member profile's chain grows to the library's 9-member set —
    the MISSING members insert at their canonical positions (each
    before the first present member that follows it canonically),
    the present members keep their loaded order and enabled state.
    Non-destructive: never reorders what the operator already set."""
    order: list[str] = [
        member for member in loaded if member in SAMPLER_CHAIN_IDS
    ]
    for member in SAMPLER_CHAIN_IDS:
        if member in loaded:
            continue
        canonical = SAMPLER_CHAIN_IDS.index(member)
        insert_at = len(order)
        for position, present in enumerate(order):
            if SAMPLER_CHAIN_IDS.index(present) > canonical:
                insert_at = position
                break
        order.insert(insert_at, member)
    return tuple(ChainItem(member, bool(loaded.get(member, True))) for member in order)
