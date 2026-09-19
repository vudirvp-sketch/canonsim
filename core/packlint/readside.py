"""The read-side lints: the brief block, scene detail, retrieval (the
D-175 split's readside family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.detail import SCENE_DETAIL_BLOCK
from core.packlint.helpers import PackError, _armed_claim_slots, _ids, _require

# The brief pipeline's closed block vocabulary (BRIEF_SPEC §3). Mechanic
# words, not setting nouns (INV-3); owned here so the lint and the
# assembler (`brief/assembler.py`) share one source of truth.
# `present_entities` sits after scene_texture (st-1: the entity-card block
# — canon-projection structure closes the quiet-beat hole; it outranks
# texture in the eviction order, BRIEF_SPEC §5.2).
BRIEF_BLOCK_IDS: Final = (
    "directives",
    "scene_delta",
    "scene_texture",
    "present_entities",
    "recalled_facts",
    "scheduled_lore",
    "voice_exemplars",
    "active_options",
)


class ReadsideLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _brief(self) -> None:
        config = self._data["rules.json"].get("brief")
        if config is None:
            raise PackError(
                "rules.json: the brief section is required (phase-1 contract, "
                "BRIEF_SPEC §6)"
            )
        where = "rules.json::brief"
        npc_ids = _ids(self._data["entities.json"]["npcs"])
        blocks = config.get("blocks")
        _require(isinstance(blocks, Mapping), f"{where}: 'blocks' must be an object")
        _require(
            set(blocks) == set(BRIEF_BLOCK_IDS),
            f"{where}: blocks must be exactly {list(BRIEF_BLOCK_IDS)}, "
            f"got {sorted(blocks)}",
        )
        for block_id, budget in blocks.items():
            _require(
                isinstance(budget, Mapping),
                f"{where}.blocks[{block_id!r}]: budget must be an object",
            )
            for key in ("soft", "hard"):
                value = budget.get(key)
                _require(
                    isinstance(value, int) and not isinstance(value, bool) and value > 0,
                    f"{where}.blocks[{block_id!r}]: {key} must be a positive integer",
                )
            _require(
                budget["soft"] <= budget["hard"],
                f"{where}.blocks[{block_id!r}]: soft must be <= hard",
            )
        total = config.get("total_hard")
        _require(
            isinstance(total, int) and not isinstance(total, bool) and total > 0,
            f"{where}: total_hard must be a positive integer",
        )
        directives = config.get("directives")
        _require(
            isinstance(directives, list)
            and directives
            and all(isinstance(line, str) and line.strip() for line in directives),
            f"{where}: directives must be a non-empty list of non-empty strings",
        )
        # Never-dropped data must fit by construction (BRIEF_SPEC §6):
        # the fill law never applies to directives, so their own hard
        # budget is the only ceiling they have.
        directives_tokens = sum(len(line.split()) for line in directives)
        _require(
            directives_tokens <= blocks["directives"]["hard"],
            f"{where}: directives ({directives_tokens} tokens) exceed their own "
            f"hard budget {blocks['directives']['hard']}",
        )
        lore = config.get("lore")
        _require(isinstance(lore, list), f"{where}: lore must be a list")
        seen_ids: set[str] = set()
        for entry in lore:
            _require(isinstance(entry, Mapping), f"{where}.lore: entries must be objects")
            entry_id = entry.get("id")
            _require(
                isinstance(entry_id, str) and entry_id.strip() and entry_id not in seen_ids,
                f"{where}.lore: ids must be unique non-empty strings, got {entry_id!r}",
            )
            seen_ids.add(entry_id)
            where_entry = f"{where}.lore[{entry_id!r}]"
            _require(
                isinstance(entry.get("text"), str) and entry["text"].strip(),
                f"{where_entry}: text must be a non-empty string",
            )
            for key in ("from_beat", "to_beat"):
                value = entry.get(key)
                _require(
                    isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                    f"{where_entry}: {key} must be a non-negative integer",
                )
            _require(
                entry["from_beat"] < entry["to_beat"],
                f"{where_entry}: from_beat must be < to_beat",
            )
        exemplars = config.get("voice_exemplars")
        _require(
            isinstance(exemplars, list)
            and all(isinstance(line, str) and line.strip() for line in exemplars),
            f"{where}: voice_exemplars must be a list of non-empty strings",
        )
        recalled = config.get("recalled_facts")
        _require(
            isinstance(recalled, Mapping),
            f"{where}: recalled_facts must be an object",
        )
        for key in ("recency_weight", "importance_weight", "relevance_weight"):
            value = recalled.get(key)
            _require(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and value >= 0,
                f"{where}.recalled_facts: {key} must be a non-negative number",
            )
        max_items = recalled.get("max_items")
        _require(
            isinstance(max_items, int) and not isinstance(max_items, bool) and max_items >= 1,
            f"{where}.recalled_facts: max_items must be an integer >= 1",
        )
        # iter-10: the 7th block's ranking caps + the unique-slot flag set
        # (BRIEF_SPEC §3.3/§6 — the scene-texture window law, D-049).
        # tex-1 (iter-62): the identity-tier slot set + the per-entity
        # quota — both required, closed vocabulary (empty identity_slots
        # = no tier beyond pinned; a quota >= max_items is the documented
        # inert state).
        texture = config.get("scene_texture")
        _require(isinstance(texture, Mapping), f"{where}: scene_texture must be an object")
        for key in ("max_items", "tombstone_max_items", "per_entity_max_items"):
            value = texture.get(key)
            _require(
                isinstance(value, int) and not isinstance(value, bool) and value >= 1,
                f"{where}.scene_texture: {key} must be an integer >= 1",
            )
        unique_slots = texture.get("unique_slots")
        _require(
            isinstance(unique_slots, list)
            and all(
                isinstance(slot, str) and slot.strip() and slot not in unique_slots[: index]
                for index, slot in enumerate(unique_slots)
            ),
            f"{where}.scene_texture: unique_slots must be unique non-empty strings",
        )
        identity_slots = texture.get("identity_slots")
        _require(
            isinstance(identity_slots, list)
            and all(
                isinstance(slot, str) and slot.strip() and slot not in identity_slots[: index]
                for index, slot in enumerate(identity_slots)
            ),
            f"{where}.scene_texture: identity_slots must be unique non-empty strings",
        )
        # st-1: the 8th block's ranking caps + the observable-marker table
        # (BRIEF_SPEC §3.8/§6 — the entity-card block). Marker names are
        # pack vocabulary (INV-3); the axis must be a known status axis of
        # the pack's states section.
        present = config.get("present_entities")
        _require(
            isinstance(present, Mapping),
            f"{where}: present_entities must be an object",
        )
        for key in ("max_entities", "max_pairs"):
            value = present.get(key)
            _require(
                isinstance(value, int) and not isinstance(value, bool) and value >= 1,
                f"{where}.present_entities: {key} must be an integer >= 1",
            )
        markers = present.get("card_markers")
        _require(
            isinstance(markers, list),
            f"{where}.present_entities: card_markers must be a list",
        )
        state_axes = set(self._data["rules.json"].get("states", {})) - {"notes"}
        relation_axes = set(self._data["rules.json"].get("relations", {}).get(
            "axes", ()
        ))
        for marker in markers:
            _require(
                isinstance(marker, Mapping),
                f"{where}.present_entities.card_markers: entries must be objects",
            )
            where_marker = (
                f"{where}.present_entities.card_markers[{marker.get('prop')!r}]"
            )
            # tune-2 (D-060): prop-path keyed, two row kinds. The closed
            # prefix set keeps the table honest — a typo'd prop is dead
            # data (the marker silently never renders), the KI#15 family.
            prop = marker.get("prop")
            _require(isinstance(prop, str) and prop.strip(),
                     f"{where_marker}: prop must be a non-empty string")
            if prop.startswith("status."):
                _require(
                    prop[len("status."):] in state_axes,
                    f"{where_marker}: status axis "
                    f"{prop[len('status.'):]!r} is not one of the pack's "
                    f"states axes {sorted(state_axes)}",
                )
            elif prop.startswith("relations."):
                _require(
                    prop[len("relations."):] in relation_axes,
                    f"{where_marker}: relations axis "
                    f"{prop[len('relations.'):]!r} is not one of the pack's "
                    f"relations axes {sorted(relation_axes)}",
                )
            elif prop.startswith("pair."):
                # suspectaxis-2 (iter-69b): the directed-axis home — a marker
                # may key `pair.<npc>.<axis>` (the wary marker followed the
                # suspicion axis to its new address). The marker fires on the
                # HOLDER of the pair record; the named npc is the figure.
                parts = prop.split(".")
                _require(
                    len(parts) == 3 and parts[1] in npc_ids
                    and parts[2] in relation_axes,
                    f"{where_marker}: pair marker path {prop!r} must be "
                    f"pair.<npc>.<axis> — the npc one of {sorted(npc_ids)}, "
                    f"the axis one of {sorted(relation_axes)}",
                )
            else:
                _require(
                    prop == "crime_status",
                    f"{where_marker}: prop must be status.<axis>, "
                    f"relations.<axis>, pair.<npc>.<axis>, or crime_status "
                    f"(the closed marker surface; grow it only with a real "
                    f"need, L13)",
                )
            has_min, has_value = "min" in marker, "value" in marker
            _require(
                has_min != has_value,
                f"{where_marker}: exactly one of min (threshold row) or "
                f"value (value row) is required",
            )
            if has_min:
                threshold = marker["min"]
                _require(
                    isinstance(threshold, int)
                    and not isinstance(threshold, bool) and threshold >= 0,
                    f"{where_marker}: min must be a non-negative integer",
                )
            else:
                _require(
                    isinstance(marker["value"], str) and marker["value"].strip(),
                    f"{where_marker}: value must be a non-empty string",
                )
            _require(
                isinstance(marker.get("marker"), str) and marker["marker"].strip(),
                f"{where_marker}: marker must be a non-empty string",
            )
        # iter-20/D-057: pack-declared location fields the scene line
        # renders canon-from-birth (the st-6 layout answer — no projection
        # seeding; canon_slot already guards pack-modeled fields).
        # bridge-1 (D-116 (1)): the field source is the FOLDED PROJECTION
        # — a scene field may also name an ARMED claim's slot (the claims'
        # first brief-side consumer); the pack record stays the fallback
        # for unclaimed fields.
        scene_fields = present.get("scene_line_fields")
        _require(
            isinstance(scene_fields, list)
            and all(
                isinstance(field, str) and field.strip() for field in scene_fields
            ),
            f"{where}.present_entities: scene_line_fields must be a list of "
            f"non-empty strings",
        )
        _require(
            len(set(scene_fields)) == len(scene_fields),
            f"{where}.present_entities: scene_line_fields must be unique",
        )
        location_fields = {
            key
            for location in self._data["entities.json"]["locations"]
            for key in location
        }
        legal_fields = location_fields | _armed_claim_slots(
            self._data["rules.json"]
        )
        _require(
            all(field in legal_fields for field in scene_fields),
            f"{where}.present_entities: scene_line_fields must reference "
            f"location fields of the pack or armed claim slots "
            f"(a field neither the pack models nor a claim claims "
            "renders nothing — dead data)",
        )
        # scene-1 (iter-60): the chorus budget + the mode-B actor table
        # (BRIEF_SPEC §3.9/§6 — one NPC per call, the pack's own
        # declaration the gate; mode A's static text stays the block's
        # own, so the player never appears in `actors`).
        chorus = config.get("chorus")
        if chorus is not None:
            unknown_chorus = sorted(set(chorus) - {"max_actor_calls", "notes"})
            _require(
                not unknown_chorus,
                f"{where}.chorus: unknown keys {unknown_chorus} (the closed "
                "vocabulary: max_actor_calls | notes)",
            )
            cap = chorus.get("max_actor_calls")
            _require(
                isinstance(cap, int) and not isinstance(cap, bool) and cap >= 1,
                f"{where}.chorus.max_actor_calls must be an integer >= 1 (a "
                "zero cap is a block-less pack — declare nothing instead)",
            )
            if "notes" in chorus:
                _require(
                    isinstance(chorus["notes"], str),
                    f"{where}.chorus: notes must be a string (prose)",
                )
        actors = config.get("actors")
        if actors is not None:
            _require(
                isinstance(actors, Mapping) and actors,
                f"{where}.actors must be a non-empty object keyed by npc id "
                "(an empty actor table is dead data — declare nothing)",
            )
            npc_ids = {
                record["id"]
                for record in self._data["entities.json"]["npcs"]
            }
            player_ids = {
                record["id"]
                for record in self._data["entities.json"]["npcs"]
                if record.get("is_player", False)
            }
            for actor_id, entry in actors.items():
                spot = f"{where}.actors[{actor_id!r}]"
                _require(
                    actor_id in npc_ids,
                    f"{spot}: no pack npc carries this id (an actor entry for "
                    "a nonexistent entity is dead vocabulary)",
                )
                _require(
                    actor_id not in player_ids,
                    f"{spot}: the player never carries an actor entry (mode A "
                    "owns its directives — the two tables are disjoint by law)",
                )
                _require(
                    isinstance(entry, Mapping),
                    f"{spot}: the entry must be an object",
                )
                unknown_actor = sorted(set(entry) - {
                    "directives", "voice_exemplars", "notes"
                })
                _require(
                    not unknown_actor,
                    f"{spot}: unknown keys {unknown_actor} (the closed "
                    "vocabulary: directives | voice_exemplars | notes)",
                )
                directives = entry.get("directives")
                _require(
                    isinstance(directives, list)
                    and directives
                    and all(
                        isinstance(line, str) and line.strip()
                        for line in directives
                    ),
                    f"{spot}: directives must be a non-empty list of "
                    "non-empty strings (never-dropped data — the mode-B "
                    "call is roleless without them)",
                )
                # Same construction-fit law as the block's own directives
                # (BRIEF_SPEC §6): the fill law never applies to them.
                actor_tokens = sum(len(line.split()) for line in directives)
                _require(
                    actor_tokens <= blocks["directives"]["hard"],
                    f"{spot}: directives ({actor_tokens} tokens) exceed the "
                    f"directives hard budget {blocks['directives']['hard']}",
                )
                exemplars = entry.get("voice_exemplars")
                _require(
                    isinstance(exemplars, list)
                    and all(
                        isinstance(line, str) and line.strip()
                        for line in exemplars
                    ),
                    f"{spot}: voice_exemplars must be a list of non-empty "
                    "strings (L2 — the only place the actor's style lives)",
                )
                if "notes" in entry:
                    _require(
                        isinstance(entry["notes"], str),
                        f"{spot}: notes must be a string (prose)",
                    )

    # -- pack-ci (iter-117): the teleology gate (PACK_SPEC §5) -----------------


    def _scene_detail(self) -> None:
        """The lazy scene-detail contract (depth-2, `phases.md` §5 — the
        D-054 texture-promotion law at scene scale; mechanics in
        `core/detail.py::materialize_scene_detail`, wired into the
        observe resolver; the claim gate `detail_claim`; the stream
        `core/rng.py::scene_detail_stream_name`). The block is OPTIONAL
        and lives at rules.json top level (`scene_detail` — the system
        config home, the position_visibility.acquisition precedent: a
        rules block keyed by world ids): `location_id -> slot list`.
        Each slot entry is exactly `{slot, values}` — `slot` a
        non-empty string unique within the location, `values` a list
        of unique non-empty strings (the closed draw vocabulary;
        `empty` is just a value — first-commit-wins makes a
        materialized empty reject later gold, no special casing).
        The double-claim law: a scene_detail slot must NOT be modeled
        by the location entity (any record key or declared flag —
        lazy detail occupies only slots canon does not model, the
        texture law's twin; the fold seeds flags as raw site props,
        so a pre-claimed slot could never birth). The one-object law:
        the slot must not appear in brief.scene_texture.unique_slots
        (a unique slot denotes one cross-scope object — a lazy pool
        on it would declare the same object twice). Location ids name
        the detail streams (`scene:<id>:detail`, D-079's family law)
        — map keys, injective by construction. A pack without the
        block materializes nothing and runs the v0.1 bytes,
        byte-identically (the pack's own declaration is the arming,
        depth-2b — the 68a pattern)."""
        rules = self._data["rules.json"]
        config = rules.get(SCENE_DETAIL_BLOCK)
        if config is None:
            return
        where = f"rules.json::{SCENE_DETAIL_BLOCK}"
        _require(
            isinstance(config, Mapping) and config,
            f"{where} must be a non-empty object keyed by location id "
            "(an empty block is dead data — omit it for v0.1 bytes)",
        )
        unique_slots = set(
            rules.get("brief", {}).get("scene_texture", {}).get("unique_slots", ())
        )
        locations = {
            record["id"]: record
            for record in self._data["entities.json"]["locations"]
        }
        for location_id, slots in config.items():
            spot = f"{where}[{location_id!r}]"
            record = locations.get(location_id)
            _require(
                record is not None,
                f"{spot}: unknown location id (entities.json locations "
                "is the single owner — the id also names the detail "
                "stream `scene:<id>:detail`)",
            )
            assert record is not None  # _require above is the protection
            _require(
                isinstance(slots, list) and slots,
                f"{spot}: must be a non-empty list of slot entries (an "
                "empty list is dead data — omit the location)",
            )
            seen: set[str] = set()
            modeled = set(record) | set(record.get("flags", {}))
            for index, entry in enumerate(slots):
                entry_spot = f"{spot}[{index}]"
                _require(
                    isinstance(entry, Mapping),
                    f"{entry_spot}: must be an object",
                )
                unknown = sorted(set(entry) - {"slot", "values"})
                if unknown:
                    raise PackError(
                        f"{entry_spot}: unknown keys {unknown} (the "
                        "closed vocabulary: slot | values)"
                    )
                slot = entry.get("slot")
                _require(
                    isinstance(slot, str) and slot.strip(),
                    f"{entry_spot}.slot must be a non-empty string",
                )
                _require(
                    slot not in seen,
                    f"{entry_spot}.slot {slot!r} is declared twice in "
                    "the location (one slot, one draw, one birth — a "
                    "duplicate would couple the stream positions)",
                )
                seen.add(slot)
                _require(
                    slot not in modeled,
                    f"{entry_spot}.slot {slot!r} is already modeled by "
                    "the location entity (a record key or declared flag) "
                    "— lazy detail occupies only slots canon does not "
                    "model (the texture law's twin)",
                )
                _require(
                    slot not in unique_slots,
                    f"{entry_spot}.slot {slot!r} is a "
                    "brief.scene_texture unique slot (one object, one "
                    "vocabulary — the double-declaration refusal)",
                )
                values = entry.get("values")
                _require(
                    isinstance(values, list)
                    and values
                    and all(
                        isinstance(value, str) and value.strip()
                        for value in values
                    ),
                    f"{entry_spot}.values must be a non-empty list of "
                    "non-empty strings (the closed draw vocabulary)",
                )
                _require(
                    len(set(values)) == len(values),
                    f"{entry_spot}.values contains duplicates (a "
                    "duplicate member is dead draw vocabulary — weighting "
                    "would be an explicit feature, never an accident)",
                )
