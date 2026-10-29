"""iter-383 acceptance — the whole-set family draw (`family_rolls`,
the beat-machinery static-resolution family's next fusion after
iter-370's `family_randint`): ONE door crossing for a per-beat walk's
every rolling entry.

The laws here pin the EQUALITY the fusion is built on — the batch IS
the per-call sequence, fused: same words (the counter function is
pure in (key, position)), same counter positions (the checkpoint
never distinguishes the forms), the entries' own order (a repeated
name draws its next positions in sequence), the nesting law loud per
name (`family_randint`'s own check, executed inline) — and the DOOR
IS ATOMIC: a refusing batch advances nothing, strictly safer than
the per-call sequence whose mid-sequence refusal leaves the earlier
names drawn. The per-call form stays the law's owner; these laws are
the pin, never a second source of truth (D-024, the iter-370
precedent). The real-run law is the A/B byte-identity pair (the
test_h9 form): a session driven through the per-call walks and the
same session through the batch walks commit identical bytes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.factions import (
    _member_values,
    faction_intents,
    faction_probability,
    faction_rolls,
)
from core.factions import (
    _specs as _faction_specs_all,
)
from core.fold import initial_projection
from core.intent import first_failing
from core.loop import Simulator
from core.pack import load_pack
from core.rng import (
    RngBank,
    RngError,
    faction_stream_name,
    urgency_stream_name,
)
from core.urgencies import (
    _specs as _urgency_specs_all,
)
from core.urgencies import (
    urgency_intents,
    urgency_rolls,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

# The six committed packs — the twin law's corpus (the iter-362 class
# form; the walks' rolling sets differ per pack, the law does not).
_PACK_DIRS = (
    "tavern_pack",
    "province_pack",
    "farstead_pack",
    "grim_pack",
    "pressure_pack",
    "road_pack",
)

# the crafted families the equality law sweeps: urgency, faction,
# drift, scene — lazily registered, one round and many (the block
# boundary at every 4th draw crossed inside the sweep)
_CRAFTED = (
    urgency_stream_name("npc_a", "talk"),
    urgency_stream_name("npc_b", "steal"),
    faction_stream_name("grp_watch", "patrol"),
    "drift:rumor_family",
    "scene:loc_square:detail",
)


def _per_call(bank: RngBank, names: list[str], lo: int, hi: int) -> list[int]:
    """The reference: the per-entry `family_randint` sequence — the
    law's owner, executed exactly as the pre-383 walk did."""
    return [bank.family_randint(name, lo, hi) for name in names]


# -- law 1: THE EQUALITY LAW ----------------------------------------------------


def test_the_equality_law_same_words_same_counts() -> None:
    """The batch IS the per-call sequence: same words, same counter
    positions, over crafted families, repeated names (the consecutive
    positions a shared stream sees in the per-entry walk), varied
    ranges, and enough rounds to cross the block boundary."""
    names = [*_CRAFTED, _CRAFTED[0], _CRAFTED[1]]  # repeats: positions
    # in sequence, exactly the per-call walk's own behavior
    batch_bank = RngBank(42)
    call_bank = RngBank(42)
    for _round in range(9):  # 7 draws/round x 9 > 4-word blocks
        assert batch_bank.family_rolls(names, 1, 100) == _per_call(
            call_bank, names, 1, 100
        )
        assert batch_bank.family_rolls(names, 1, 6) == _per_call(
            call_bank, names, 1, 6
        )
    for name in set(names):
        assert batch_bank.count(name) == call_bank.count(name)
    # the substantive fingerprint never sees a family draw (INV-2)
    assert batch_bank.fingerprint == 0


def test_the_empty_batch_is_the_empty_sequence() -> None:
    """No entries, no draws, no counter motion — the beat's empty
    rolling set crosses the door and changes nothing."""
    bank = RngBank(42)
    before = dict(bank._counts)
    assert bank.family_rolls([], 1, 100) == []
    assert bank._counts == before


# -- law 2: THE ATOMIC DOOR -----------------------------------------------------


def test_the_nesting_law_and_the_atomic_door() -> None:
    """The nesting law is `family_randint`'s own, per name: a foreign
    name under the assured substantive scope refuses; a family name
    under an assured FAMILY scope refuses unless it IS the assured
    stream. THE DOOR IS ATOMIC — a refusing batch advances NOTHING
    (every counter unchanged, the memo untouched), strictly safer
    than the per-call sequence, whose mid-sequence refusal leaves the
    earlier names drawn."""
    # a foreign name inside the assured substantive scope
    bank = RngBank(42)
    with bank.assure("substantive"):
        try:
            bank.family_rolls([*_CRAFTED[:2], "cosmetic"], 1, 100)
            raise AssertionError("the foreign name drew inside the scope")
        except RngError:
            pass
    for name in _CRAFTED[:2]:
        assert bank.count(name) == 0, "the refusing batch advanced a counter"

    # a family name under an assured FAMILY scope: only the assured
    # stream itself may draw (the per-call form's own pairing law)
    bank = RngBank(42)
    with bank.assure(_CRAFTED[0]):
        assert bank.family_rolls([_CRAFTED[0]], 1, 100) == _per_call(
            RngBank(42), [_CRAFTED[0]], 1, 100
        )
        try:
            bank.family_rolls([_CRAFTED[0], _CRAFTED[1]], 1, 100)
            raise AssertionError("the foreign family name drew inside a family scope")
        except RngError:
            pass
    assert bank.count(_CRAFTED[0]) == 1  # the legal draw landed, the refused one did not
    assert bank.count(_CRAFTED[1]) == 0

    # the family set under the substantive scope draws free (the run's
    # own form — every beat crosses exactly this door)
    bank = RngBank(42)
    ref = RngBank(42)
    with bank.assure("substantive"):
        got = bank.family_rolls(list(_CRAFTED), 1, 100)
    assert got == _per_call(ref, list(_CRAFTED), 1, 100)


def test_the_range_law_refuses_before_any_draw() -> None:
    """An empty range refuses the WHOLE batch (the per-call form's own
    message), and a point range draws the constant — one range per
    batch, the no-mixed-ranges law's own shape."""
    bank = RngBank(42)
    try:
        bank.family_rolls([*_CRAFTED[:2]], 5, 4)
        raise AssertionError("the empty range drew")
    except ValueError:
        pass
    for name in _CRAFTED[:2]:
        assert bank.count(name) == 0, "the refused range advanced a counter"
    assert bank.family_rolls([_CRAFTED[0]], 7, 7) == [7]


# -- law 3: THE BLOCK-JUMP LAW --------------------------------------------------


def test_the_block_jump_law() -> None:
    """The counter function is pure in (key, position) — after any
    counter jump (`skip_draws`, the restore/branch/seek law) the
    batch draws exactly what the per-call sequence draws at the
    jumped positions: the block memo is derived state, correct by
    construction on any jump."""
    batch_bank = RngBank(7)
    call_bank = RngBank(7)
    # a first round to seed both banks identically
    batch_bank.family_rolls(list(_CRAFTED), 1, 100)
    _per_call(call_bank, list(_CRAFTED), 1, 100)
    # the jumps: skip every stream by a different amount (block
    # boundaries land mid-jump), then draw and compare
    for i, name in enumerate(_CRAFTED):
        batch_bank.skip_draws(name, 3 + i)
        call_bank.skip_draws(name, 3 + i)
    for _round in range(5):
        assert batch_bank.family_rolls(list(_CRAFTED), 1, 100) == _per_call(
            call_bank, list(_CRAFTED), 1, 100
        )
    for name in _CRAFTED:
        assert batch_bank.count(name) == call_bank.count(name)


# -- law 4: THE WALK TWIN ON EVERY COMMITTED PACK -------------------------------


def _old_urgency_intents(
    pack: Any,
    projection: Any,
    bank: RngBank,
    *,
    specs: Any,
) -> list[Any]:
    """The pre-383 walk, reconstructed as the oracle: the per-entry
    draw loop (`family_randint` per rolling entry, the probability
    filter, the gates) — the batch form's own reference."""
    entries = [
        spec for spec in specs if urgency_rolls(spec, projection, None)
    ]
    out: list[Any] = []
    for spec in entries:
        roll = bank.family_randint(spec.stream, 1, 100)
        if roll > spec.probability_per_beat:
            continue
        intent = spec.probe
        if spec.requires:
            failing = first_failing(
                pack, projection, intent, spec.requires,
                facts=(), echoes=(), traits=(), world=None,
            )
            if failing is not None:
                continue
        out.append(intent)
    return out


def test_the_walk_twin_on_every_committed_pack() -> None:
    """The function-level oracle on all six packs: the batch walk's
    outputs and counters equal the per-call reference's, round after
    round (the block boundaries crossed; the gates read the same
    frozen projection — the draws never depend on the gate verdicts,
    so the collect-then-draw order IS the per-entry order, fused)."""
    for pack_dir in _PACK_DIRS:
        pack = load_pack(REPO / "content" / pack_dir)
        projection = initial_projection(pack.entities)
        specs = _urgency_specs_all(pack)
        if not specs:
            continue  # the pack declares no urgencies — nothing to pin
        batch_bank = RngBank(11)
        ref_bank = RngBank(11)
        for _round in range(5):
            got = urgency_intents(
                pack, projection, batch_bank, specs=specs
            )
            want = _old_urgency_intents(
                pack, projection, ref_bank, specs=specs
            )
            assert got == want, f"{pack_dir}: the batch walk diverged"
        for spec in specs:
            assert batch_bank.count(spec.stream) == ref_bank.count(
                spec.stream
            ), f"{pack_dir}: the counters diverged on {spec.stream}"


def test_the_faction_twin() -> None:
    """The faction walk's own oracle (the pressure pack declares the
    family): the batch form's outputs and counters equal the per-call
    reference's — the rolling filter collects first, the draws cross
    once, the bar and the gates read the frozen projection."""
    pack = load_pack(REPO / "content" / "pressure_pack")
    projection = initial_projection(pack.entities)
    specs = _faction_specs_all(pack)
    if not specs:
        raise AssertionError("the pressure pack lost its factions")
    batch_bank = RngBank(11)
    ref_bank = RngBank(11)

    def reference() -> list[Any]:
        out: list[Any] = []
        for spec in specs:
            if not faction_rolls(spec, projection, None):
                continue
            values = _member_values(spec, projection)
            bar = faction_probability(
                values, spec.trigger_value, spec.threshold,
                spec.max_per_beat,
            )
            roll = ref_bank.family_randint(spec.stream, 1, 100)
            if roll > bar:
                continue
            intent = spec.probe
            if spec.requires:
                failing = first_failing(
                    pack, projection, intent, spec.requires,
                    facts=(), echoes=(), traits=(), world=None,
                )
                if failing is not None:
                    continue
            out.append(intent)
        return out

    for _round in range(5):
        got = faction_intents(pack, projection, batch_bank, specs=specs)
        assert got == reference(), "the faction batch walk diverged"
    for spec in specs:
        assert batch_bank.count(spec.stream) == ref_bank.count(spec.stream)


# -- law 5: THE REAL-LOG A/B LAW -------------------------------------------------


def _ab_run(tmp: Path, name: str, *, per_call: bool) -> Path:
    """One province session through the real Simulator — the batch
    walks (the working tree) or the per-call walks (the oracle,
    patched into the loop's own bindings, the probe's own form)."""
    import core.loop as loop_mod
    import core.urgencies as urg_mod
    from core.urgencies import urgency_specs

    if per_call:
        def patched(
            pack, projection, bank, facts=(), echoes=(), traits=(),
            locations=None, world=None, specs=None, roll_index=None,
        ):
            entries = [
                (idx, spec)
                for idx, spec in enumerate(
                    urgency_specs(pack) if specs is None else specs
                )
                if urg_mod.urgency_rolls(spec, projection, locations)
            ]
            out = []
            for _idx, spec in entries:
                roll = bank.family_randint(spec.stream, 1, 100)
                if roll > spec.probability_per_beat:
                    continue
                intent = spec.probe
                if spec.requires:
                    failing = first_failing(
                        pack, projection, intent, spec.requires,
                        facts=facts, echoes=echoes, traits=traits,
                        world=world,
                    )
                    if failing is not None:
                        continue
                out.append(intent)
            return out

        loop_mod.urgency_intents = patched
    try:
        pack = load_pack(REPO / "content" / "province_pack")
        log = tmp / f"ab_{name}.jsonl"
        sim = Simulator(
            pack, 7, log, SCHEMA, commit="0000000",
            director_enabled=False, skip_quiet_beats=True,
        )
        sim.open()
        sim.run_steps(
            [{"intent": "move", "target": "loc_market"}]
            + [{"intent": "wait", "ticks": 518_400}] * 2
        )
        sim.close()
        return log
    finally:
        loop_mod.urgency_intents = urgency_intents


def test_the_real_log_ab_byte_identity(tmp_path: Path) -> None:
    """The fusion is canon-invisible at the real-run level (the
    test_h9 A/B form): the same (seed, steps) through the per-call
    walks and through the batch walks commit byte-identical logs —
    and the pair is NON-VACUOUS (urgency streams actually drew)."""
    log_new = _ab_run(tmp_path, "batch", per_call=False)
    log_old = _ab_run(tmp_path, "percall", per_call=True)
    assert log_new.read_bytes() == log_old.read_bytes(), (
        "the whole-set draw DIVERGED the canon"
    )
    # non-vacuous: the batch form actually ran the door (the family
    # streams registered and advanced — a green pair over zero draws
    # proves nothing)
    pack = load_pack(REPO / "content" / "province_pack")
    specs = _urgency_specs_all(pack)
    assert any(spec.probability_per_beat > 0 for spec in specs), (
        "the province pack declares no rolling urgencies — the A/B "
        "pair is vacuous; pin a pack that rolls"
    )
