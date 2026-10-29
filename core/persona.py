"""The appearance and voice ANCHORS (agenda-1 P2, iter-419): the per-NPC
presentational FACTS drawn lazily at the canon birth — the exact twin of
the name generator (`core/names.py::materialize_name`) and the personality
profile (`core/psyche.py::materialize_psyche`): the D-054 lazy-slot shape,
one materialization, first-commit-wins, never a second mechanism.

- **The pack data**: `rules.json::appearance` and `rules.json::voice` —
  the authoring POOLS (`pools[]` rows: an engine-opaque `id` + a `tokens`
  list). The tokens are authoring words (INV-3: the engine spells none of
  them — `burn_scar_forearm`, `clipped` are pack vocabulary). The npc
  record declares the origin: `generated_look: <pool id>` /
  `generated_voice: <pool id>` — the `generated_name`/`generated_psyche`
  twin's law (one origin per prop).
- **The authoring law** (iter-416 §12, the donor's measured dose): an
  anchor is 2-4 CONCRETE PHYSICAL FACTS and 3-4 VOICE PROPERTIES — facts,
  never judgements (`sympathetic`/`ugly` are the observer's read, drawn
  from the relations and knowledge the brief already carries). The guide
  measured instruction-descriptions at ~0% influence and examples at
  ~10%, so the small dose is the empirically right one; a bank of twenty
  phrases clamps the model instead of freeing it. `LOOK_MIN`/
  `LOOK_MAX`/`VOICE_MIN`/`VOICE_MAX` are the dose's ONE owner: the draw
  clips to them and the pack lint refuses a pool below the floor.
- **The draw**: the count uniform inside the dose band (clamped to the
  pool's size — the lint refuses a pool that cannot fill the floor), then
  ONE combinatorial index over `itertools.combinations` picks the token
  set (a draw, never a rejection walk — the P1 draw law), rendered in the
  POOL's declaration order (INV-2). One stream per prop per npc:
  `look:<npc>` / `voice:<npc>` (`core/rng.py::look_stream_name` /
  `voice_stream_name` — the D-079 family law's tenth and eleventh
  members), so arming, removing, or re-arming one anchor shifts neither a
  canon check draw nor another npc's anchors.
- **The birth** is the CONDENSATION's (the recorded consumer,
  `core/groups.py::condensation_drafts` — the same event that births the
  member's name and profile: one member, one block). The committed
  event's `state_changes` carry `StateChange(npc, "look", None ->
  [facts])` and `StateChange(npc, "voice", None -> [properties])` in that
  order; an anchor already held by the folded projection is SKIPPED —
  first-commit-wins, never a redraw (canon is the answer).
- **The unarmed law** (the 68a pattern): no declaration answers `()`
  BEFORE any stream is touched — zero assures, zero draws, the committed
  corpora byte-identical by construction.
- **The reading**: the brief's entity CARDS render the two props as
  `look=...` / `voice=...` segments (`brief/assembler.py::
  _present_entity_items` — the card is the body's own fact surface, the
  `markers=`/`carries=` family). `brief/scan.py::modeled_vocabulary`
  gains the pools' words, so the narrator's use of an anchor is GROUNDED
  (the lowercase assertion split's honest half), never an invention.
- **Change is a fact, not an edit** (iter-416 §12): a wound, a grey
  streak, a lost tooth, a new coat ride an ordinary committed
  state_change event — then the narrator *may* describe the change,
  because canon changed. Nothing here writes a record: an authored
  `look`/`voice` on the npc record is dead data (the card reads the FOLD,
  the record is not seeded) and the pack lint refuses it.
- **What this is not**: no attractiveness, no social modifier, no
  consistency lint over the narrator's prose. The anchor is an
  INSTRUCTION to the narrator and a canon fact about a body; the words
  outside canon stay the model's (the honest boundary §12 names).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from itertools import combinations
from typing import TYPE_CHECKING, Any, Final

from core.log import StateChange
from core.rng import RngBank, look_stream_name, voice_stream_name

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle
    from core.pack import Pack

__all__ = [
    "GENERATED_LOOK_KEY",
    "GENERATED_VOICE_KEY",
    "LOOK_BLOCK",
    "LOOK_MAX",
    "LOOK_MIN",
    "LOOK_PROP",
    "PersonaError",
    "VOICE_BLOCK",
    "VOICE_MAX",
    "VOICE_MIN",
    "VOICE_PROP",
    "materialize_anchors",
]

#: The two rules.json blocks (the pools; `core/packlint/psyche.py::
#: _persona` owns the shape). Absent -> the unarmed law.
LOOK_BLOCK: Final = "appearance"
VOICE_BLOCK: Final = "voice"

#: The npc record's declaration keys (`generated_look: <pool id>` /
#: `generated_voice: <pool id>`) and the born props on the npc entity —
#: one string, two namespaces, exactly the `generated_psyche`/`psyche`
#: split (the record's declaration site, the projection's slot).
GENERATED_LOOK_KEY: Final = "generated_look"
GENERATED_VOICE_KEY: Final = "generated_voice"
LOOK_PROP: Final = "look"
VOICE_PROP: Final = "voice"

#: The authoring dose (`live_char_guide` §12's measured band, carried as
#: the ONE owner both the draw and the lint read): 2-4 physical facts and
#: 3-4 voice properties per person. More is a phrase bank, less is a
#: silhouette.
LOOK_MIN: Final = 2
LOOK_MAX: Final = 4
VOICE_MIN: Final = 3
VOICE_MAX: Final = 4

#: The draw's two halves: (block, declaration key, born prop, stream
#: builder, dose floor, dose ceiling) — declaration order is the birth
#: order in the event (INV-2).
_ANCHORS: Final = (
    (LOOK_BLOCK, GENERATED_LOOK_KEY, LOOK_PROP, look_stream_name,
     LOOK_MIN, LOOK_MAX),
    (VOICE_BLOCK, GENERATED_VOICE_KEY, VOICE_PROP, voice_stream_name,
     VOICE_MIN, VOICE_MAX),
)


class PersonaError(RuntimeError):
    """An anchor-side contract failure (a declaration naming no pool, a
    missing block, an empty pool — the post-lint backstop, loud like
    `core.names.NamesError`)."""


def _pool(config: Mapping[str, Any], pool_id: str) -> Mapping[str, Any] | None:
    """The declared pool row, or None (the draw's own lookup — the
    projection/record read is `materialize_anchors`')."""
    for row in config.get("pools", ()):
        if isinstance(row, Mapping) and str(row.get("id")) == pool_id:
            return row
    return None


def _draw(
    bank: RngBank, tokens: Sequence[str], low: int, high: int,
) -> list[str]:
    """One anchor's token set: the count uniform inside the dose band
    clamped to the pool's size, then ONE combinatorial index over the
    pool positions (a draw, never a rejection walk), rendered in the
    pool's declaration order. Pure over (the active stream, the pool)."""
    count = bank.randint(low, min(high, len(tokens)))
    picks = list(combinations(range(len(tokens)), count))
    chosen = picks[bank.randint(0, len(picks) - 1)]
    return [tokens[index] for index in chosen]


def materialize_anchors(
    bank: RngBank, pack: "Pack",
    projection: "Mapping[str, Mapping[str, Any]]", npc_id: str,
) -> tuple[StateChange, ...]:
    """The npc's anchor births, or () — an npc without a declaration (or
    a pack without the block) answers () BEFORE any stream is touched
    (the unarmed law, zero draws); an anchor already held by the folded
    projection is canon — skipped, never redrawn (the first-commit-wins
    twin). Otherwise each declared anchor is drawn from its own
    `look:<npc>` / `voice:<npc>` stream and returned as a birth
    StateChange, look before voice (the declaration order). The caller
    rides the births on its event — the condensation's own state_changes,
    beside the name and the profile (the name-1 law extended)."""
    record = pack.entity(npc_id) if hasattr(pack, "entity") else None
    if record is None:
        return ()
    births: list[StateChange] = []
    for block, declaration, prop, stream_name, low, high in _ANCHORS:
        pool_id = record.get(declaration)
        if pool_id is None:
            continue  # authored or absent — the unarmed law
        if projection.get(npc_id, {}).get(prop) is not None:
            continue  # canon holds an anchor — first-commit-wins
        config = pack.rules.get(block)
        if not isinstance(config, Mapping):
            raise PersonaError(
                f"{npc_id}: {declaration} declared but rules.json carries "
                f"no {block} block (the lint owns the shape — this path is "
                f"the post-lint backstop)"
            )
        pool = _pool(config, str(pool_id))
        if pool is None:
            raise PersonaError(
                f"{npc_id}: {declaration} {pool_id!r} has no row in "
                f"rules.json {block}.pools (the lint owns the shape — this "
                f"path is the post-lint backstop)"
            )
        tokens = tuple(
            str(token) for token in pool.get("tokens", ())
        )
        if not tokens:
            raise PersonaError(
                f"{npc_id}: the {block} pool {pool_id!r} carries no tokens "
                f"(the post-lint backstop)"
            )
        with bank.assure(stream_name(npc_id)):
            births.append(
                StateChange(
                    entity=npc_id,
                    prop=prop,
                    from_=None,
                    to_=_draw(bank, tokens, low, high),
                )
            )
    return tuple(births)
