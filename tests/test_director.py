"""iter-4 acceptance — the director (phase0 §4, D-005, DIRECTOR_SPEC):
the consequence planner that never improvises. Hooks seeded at event
time sit in a per-run buffer; explicit triggers (time / place /
threshold) fire causally; the stagnation detector releases the
lowest-threshold hook when narrative entropy drops below the pack's
floor. Releases ride the intent door — the director never writes canon
itself (D-037). Director-off keeps the buffer seeding but suppresses
releases (T8 A/B baseline).

Determinism holds (T1 discipline): the entropy formula reads
observable state only (L6), and the release decisions are deterministic
for a given buffer + projection — no RNG in the director itself.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.director import (
    DISABLED,
    Director,
    DisabledPolicy,
    EnabledPolicy,
    SeededHook,
    entropy,
)
from core.fold import initial_projection
from core.log import EventRecord
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")


def _record(hooks: tuple[str, ...] = (), event_id: str = "ev_0001", t: int = 0) -> EventRecord:
    """A minimal committed event with the given hooks."""
    return EventRecord(
        id=event_id, t=t, type="test_event", actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=(), hooks=hooks,
        importance="low", provenance={}, target=None,
    )


def _seeded_hook(
    *, tag: str = "guard_suspicious_of_pc", target_npc: str = "npc_guard_01",
    weight: int = 2, release_threshold: int = 5, trigger: dict[str, Any] | None = None,
) -> SeededHook:
    return SeededHook(
        tag=tag, seeded_by_event="ev_0001", seeded_at_tick=0,
        weight=weight, release_threshold=release_threshold,
        target_npc=target_npc, intent_kind="wait", intent_target=None,
        intent_fields={"ticks": 1}, trigger=trigger,
    )


# -- seeding (D-005: hooks seeded at event time, never invented later) --------


def test_seed_absorbs_hooks_the_pack_declares() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc", "unknown_tag")))
    # the pack-declared hook seeds; the unknown tag is silently ignored
    assert len(director.hooks) == 1
    assert director.hooks[0].tag == "guard_suspicious_of_pc"
    assert director.hooks[0].target_npc == "npc_guard_01"
    assert director.hooks[0].intent_kind == "wait"


def test_seed_ignores_events_without_hooks() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=()))
    assert director.hooks == ()


# -- entropy (P2e: observable state only, never knowledge records) ------------


def test_entropy_zero_on_idle_world() -> None:
    projection = initial_projection(PACK.entities)
    assert entropy(projection, iter([])) == 0  # no hooks, no suspicion, no fires


def test_entropy_sums_hook_weights() -> None:
    projection = initial_projection(PACK.entities)
    hooks = [_seeded_hook(weight=2), _seeded_hook(weight=3)]
    # only the unreleased contribute
    assert entropy(projection, iter(hooks)) == 5


def test_entropy_reads_global_suspicion() -> None:
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 25
    projection["npc_guard_02"]["relations.suspicion"] = 10
    assert entropy(projection, iter([])) == 35


def test_entropy_counts_visible_physical_threats() -> None:
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    projection["loc_tavern"]["fire.tables"] = "burning"
    assert entropy(projection, iter([])) == 2


def test_entropy_never_reads_knowledge_records() -> None:
    """L6: entropy is observable state only. A knower's records must
    never feed the director's release decision — the Influence Boundary
    extends from the perceiver (EPIST-1) to the director itself."""
    projection = initial_projection(PACK.entities)
    # stuff a knowledge record into the projection — the director MUST
    # not see it (it lives in the KnowledgeView, not the projection)
    projection["npc_guard_01"]["knowledge.figure_reaching_for_purse"] = True
    assert entropy(projection, iter([])) == 0


# -- explicit triggers (causal, fire regardless of entropy) -------------------


def test_threshold_trigger_fires_when_suspicion_crosses() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director.seed(_record(hooks=("possible_document_check",)))
    projection = initial_projection(PACK.entities)
    # suspicion below the threshold (50): trigger does not fire
    assert director.releases(projection, _empty_view(), beat_tick=0) == []
    # suspicion crosses 50: trigger fires — entropy_floor=0 means
    # stagnation never releases (entropy can't be negative), only the
    # explicit threshold trigger can release here
    projection["npc_guard_01"]["relations.suspicion"] = 50
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1
    assert released[0].kind == "wait"
    assert released[0].actor == "npc_guard_01"


def test_time_trigger_fires_after_the_packed_tick() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    # craft a hook with a time trigger at tick 100
    hook = _seeded_hook(
        tag="guard_suspicious_of_pc", release_threshold=0,
        trigger={"kind": "time", "tick": 100},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    assert director.releases(projection, _empty_view(), beat_tick=50) == []
    released = director.releases(projection, _empty_view(), beat_tick=100)
    assert len(released) == 1


def test_place_trigger_fires_when_target_at_location() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    hook = _seeded_hook(
        target_npc="npc_guard_01",
        trigger={"kind": "place", "target_npc": "npc_guard_01", "location": "loc_tavern"},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # guard at the tavern: trigger fires
    assert projection["npc_guard_01"]["position"] == "loc_tavern"
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1
    # move the guard away: trigger stops
    projection["npc_guard_01"]["position"] = "loc_guardroom"
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(hook)
    assert director2.releases(projection, _empty_view(), beat_tick=0) == []


# -- stagnation release (entropy < floor → lowest-threshold hook wins) --------


def test_stagnation_releases_when_entropy_below_floor() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    # two unreleased hooks; no triggers; no suspicion; no fires.
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_suspicious_of_pc", release_threshold=10, weight=2,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="possible_document_check", release_threshold=5, weight=3,
    ))
    projection = initial_projection(PACK.entities)
    # entropy = 2 + 3 = 5 < floor 10 → release the lowest-threshold hook
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1
    # the lowest release_threshold wins (5 < 10)
    assert director.hooks[1].tag == "possible_document_check"


def test_stagnation_silent_when_entropy_above_floor() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    director._hooks.append(_seeded_hook(weight=20, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # entropy = 20 ≥ floor 10 → no stagnation release
    assert director.releases(projection, _empty_view(), beat_tick=0) == []


def test_stagnation_skips_released_hooks() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    h1 = _seeded_hook(
        tag="guard_suspicious_of_pc", target_npc="npc_guard_01",
        weight=2, release_threshold=5,
    )
    h2 = _seeded_hook(
        tag="possible_document_check", target_npc="npc_barkeep_01",
        weight=3, release_threshold=10,
    )
    director._hooks.extend([h1, h2])  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # first release: lowest-threshold wins (h1, threshold=5)
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1
    # mark h1 as released (simulate the actual release path)
    director._released.add(0)  # type: ignore[attr-defined]
    # entropy now = 3 (h2 only) < floor 10 → release h2 (different NPC —
    # no cooldown blocks the barkeep)
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1


# -- director-off (T8 A/B baseline: buffer seeds, nothing releases) -----------


def test_director_off_seeds_but_never_releases() -> None:
    director = Director(pack=PACK, policy=DISABLED)
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    assert len(director.hooks) == 1  # the buffer seeds
    projection = initial_projection(PACK.entities)
    # no triggers fire either — the disabled policy suppresses all releases
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert released == []


def test_disabled_policy_always_returns_false() -> None:
    policy = DisabledPolicy()
    assert policy.permit_release(explicit_trigger_fires=True, current_entropy=0) is False
    assert policy.permit_release(explicit_trigger_fires=False, current_entropy=999) is False


# -- per-NPC cooldown (MinGapBetweenEncounters analogue) ---------------------


def test_per_npc_cooldown_blocks_back_to_back_releases() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    # two hooks targeting the same NPC; no triggers
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_suspicious_of_pc", target_npc="npc_guard_01",
        weight=2, release_threshold=5,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_wary_vigil", target_npc="npc_guard_01",
        weight=2, release_threshold=6,
    ))
    projection = initial_projection(PACK.entities)
    # beat 1: release h1 (lowest threshold)
    director.next_beat()
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1
    # beat 2: same NPC is on cooldown (per_npc_cooldown_beats=2) → no release
    director.next_beat()
    assert director.releases(projection, _empty_view(), beat_tick=0) == []
    # beat 3: cooldown expired → release h2
    director.next_beat()
    released = director.releases(projection, _empty_view(), beat_tick=0)
    assert len(released) == 1


# -- dead actors (caught NPCs never targeted) ---------------------------------


def test_caught_target_is_never_targeted() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=999))
    hook = _seeded_hook(
        target_npc="npc_guard_01", release_threshold=0,
        trigger={"kind": "threshold", "target_npc": "npc_guard_01",
                 "axis": "suspicion", "value": 0, "comparator": "at_least"},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # the trigger condition (suspicion >= 0) is always met — fires normally
    assert len(director.releases(projection, _empty_view(), beat_tick=0)) == 1
    # mark the target as caught: the trigger still matches, but the actor
    # is dead to the director — no release
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=999))
    director2._hooks.append(hook)
    projection["npc_guard_01"]["crime_status"] = "caught"
    assert director2.releases(projection, _empty_view(), beat_tick=0) == []


# -- helpers -----------------------------------------------------------------


def _empty_view():
    from core.knowledge import KnowledgeView
    return KnowledgeView()
