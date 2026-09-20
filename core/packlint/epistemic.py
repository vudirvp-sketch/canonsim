"""The epistemic lints: the knowledge rules block, the acquisition gate,
the retrieval block (the D-175 split's epistemic family)."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from core.intent import ACQUISITION_CHANNELS
from core.packlint.helpers import PackError, _is_int, _is_number, _require
from core.retrieval import RETRIEVAL_BLOCK_KEYS


class EpistemicLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _knowledge_rules(self) -> None:
        rules = self._data["rules.json"]
        knowledge = rules.get("knowledge", {})
        templates = self._data["templates.json"]["events"]
        relation_axes = set(rules["relations"]["axes"])
        status_axes = set(rules["states"])
        _require(
            knowledge.get("salience") in ("importance_then_recency",),
            f"knowledge.salience must be one of ['importance_then_recency'], "
            f"got {knowledge.get('salience')!r}",
        )
        acceptance = knowledge.get("rumor_acceptance", {})
        _require(
            acceptance.get("trust_axis") in relation_axes,
            f"knowledge.rumor_acceptance.trust_axis {acceptance.get('trust_axis')!r} "
            f"is not a relations axis",
        )
        _require(
            acceptance.get("teller_penalty_axis") in status_axes,
            f"knowledge.rumor_acceptance.teller_penalty_axis "
            f"{acceptance.get('teller_penalty_axis')!r} is not a status axis",
        )
        telling = knowledge.get("telling")
        if telling is not None:
            for key in ("on_event", "event"):
                _require(
                    telling.get(key) in templates,
                    f"knowledge.telling.{key} {telling.get(key)!r} is not in the "
                    f"template vocabulary",
                )
            for key in ("teller", "listener"):
                _require(
                    telling.get(key) in ("actor", "target"),
                    f"knowledge.telling.{key} must be 'actor' or 'target'",
                )
            _require(
                isinstance(telling.get("facts"), int)
                and not isinstance(telling.get("facts"), bool)
                and telling["facts"] >= 1,
                "knowledge.telling.facts must be a positive integer",
            )

    # -- crime_watch (the reacting system, iter-3) ------------------------------


    def _acquisition(self) -> None:
        """The acquisition-conditions contract (depth-1, D-105 — the
        D-096-named phase-5 gap: continuous acquisition CONDITIONS feeding
        birth fidelity; pack data here, mechanics in
        `core/intent.py::acquisition_fidelity`, never a second knowledge
        store). The block is OPTIONAL and lives INSIDE
        `rules.json::position_visibility` (the perception inputs' config
        home, beside `sight`/`hearing`/`smoke_penalty`):
        `position_visibility.acquisition` maps an ambient channel
        (saw | heard — told/inferred have no acquisition surface) to a
        condition list. Each condition is exactly one kind — `when_flag`
        + `is` (the site entity's prop equals the value: smoke, a
        declared layer flag) or `phase_in` (the clock phase at record
        birth, optionally lifted by `unless_flag` — the site's truthy
        flag: the lit room at night) — plus `steps` (an int >= 1 down
        the fidelity chain). A pack without the block answers the base
        fidelity everywhere and runs the v0.1 bytes, byte-identically
        (the pack's own declaration is the arming, the 68a pattern)."""
        rules = self._data["rules.json"]
        config = rules.get("position_visibility", {}).get("acquisition")
        if config is None:
            return
        pv = "position_visibility.acquisition"
        _require(
            isinstance(config, Mapping) and config,
            f"{pv} must be a non-empty object keyed by channel (an empty "
            "block is dead data — omit it for v0.1 bytes)",
        )
        phase_ids = {
            phase["id"] for phase in rules.get("time", {}).get("phases", ())
        }
        for channel, conditions in config.items():
            where = f"{pv}[{channel!r}]"
            _require(
                channel in ACQUISITION_CHANNELS,
                f"{where}: channel must be an ambient channel "
                f"({list(ACQUISITION_CHANNELS)} — told/inferred have no "
                "acquisition surface)",
            )
            _require(
                isinstance(conditions, list) and conditions,
                f"{where} must be a non-empty list of conditions",
            )
            for index, condition in enumerate(conditions):
                spot = f"{where}[{index}]"
                _require(
                    isinstance(condition, Mapping), f"{spot} must be an object"
                )
                kinds = [k for k in ("when_flag", "phase_in") if k in condition]
                _require(
                    len(kinds) == 1,
                    f"{spot}: exactly one condition kind is required "
                    "(when_flag | phase_in)",
                )
                unknown = sorted(
                    set(condition)
                    - {"when_flag", "phase_in", "is", "unless_flag", "steps"}
                )
                if unknown:
                    raise PackError(
                        f"{spot}: unknown keys {unknown} (the closed "
                        "vocabulary: when_flag|phase_in + is|unless_flag "
                        "+ steps)"
                    )
                if "when_flag" in condition:
                    _require(
                        isinstance(condition["when_flag"], str)
                        and condition["when_flag"],
                        f"{spot}.when_flag must be a non-empty site prop "
                        "name (a location-entity prop, e.g. a layer flag)",
                    )
                    _require(
                        "is" in condition,
                        f"{spot}: when_flag requires 'is' (the compared "
                        "value — explicit, no default)",
                    )
                    _require(
                        "unless_flag" not in condition,
                        f"{spot}: unless_flag belongs to phase_in "
                        "conditions only",
                    )
                else:
                    phases = condition["phase_in"]
                    _require(
                        isinstance(phases, list) and phases,
                        f"{spot}.phase_in must be a non-empty list of "
                        "phase ids",
                    )
                    for phase in phases:
                        _require(
                            phase in phase_ids,
                            f"{spot}.phase_in names unknown phase {phase!r} "
                            "(time.phases is the single owner)",
                        )
                    _require(
                        "is" not in condition,
                        f"{spot}: 'is' belongs to when_flag conditions only",
                    )
                if "unless_flag" in condition:
                    _require(
                        isinstance(condition["unless_flag"], str)
                        and condition["unless_flag"],
                        f"{spot}.unless_flag must be a non-empty site prop "
                        "name (truthy on the site lifts the condition)",
                    )
                _require(
                    _is_int(condition.get("steps")) and condition["steps"] >= 1,
                    f"{spot}.steps must be an int >= 1 (0 is a dead "
                    "condition)",
                )


    def _retrieval(self) -> None:
        """The retrieval-ladder contract (`core/retrieval.py` owns the
        vocabulary constants; `phases.md` §4 the ladder's architecture
        — retr-1, STORE-1). The block is OPTIONAL: a pack without it
        builds no index and runs byte-identically (the pack's own
        declaration is the gate, INV-3; the runtime never queries —
        the mediator's keyword query is the consumer, BRIEF_SPEC §9's
        deferral)."""
        rules = self._data["rules.json"]
        config = rules.get("retrieval")
        if config is None:
            return
        where = "retrieval"
        if not isinstance(config, Mapping):
            raise PackError(f"{where} must be an object")
        unknown = sorted(set(config) - set(RETRIEVAL_BLOCK_KEYS))
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed "
                f"vocabulary: {' | '.join(RETRIEVAL_BLOCK_KEYS)})"
            )
        coefficients: list[float] = []
        for key in ("alpha", "beta", "gamma", "delta"):
            value = config.get(key)
            _require(
                _is_number(value) and float(value) >= 0,
                f"{where}.{key} must be a non-negative number (the "
                "re-ranker coefficient — pack data, never a code default)",
            )
            assert _is_number(value)  # the require above
            coefficients.append(float(value))
        _require(
            any(value > 0 for value in coefficients),
            f"{where}: at least one coefficient must be positive (an "
            "all-zero block ranks by construction order alone — dead "
            "data, refused)",
        )
        knn_k = config.get("knn_k")
        _require(
            _is_int(knn_k) and knn_k >= 1,
            f"{where}.knn_k must be an integer >= 1 (the vec rung's "
            "kNN limit — the scan rung's top-k)",
        )
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                f"{where}.notes must be a string (prose)",
            )
        vectors = config.get("vectors")
        if vectors is None:
            return
        _require(
            isinstance(vectors, Mapping) and vectors,
            f"{where}.vectors must be a non-empty object keyed by lore "
            "id (an absent key is the honest no-embeddings state — an "
            "empty table is dead data, refused)",
        )
        lore_ids = {
            entry["id"]
            for entry in rules["brief"].get("lore", ())
            if isinstance(entry, Mapping) and isinstance(entry.get("id"), str)
        }
        dim: int | None = None
        for lore_id, embedding in vectors.items():
            spot = f"{where}.vectors[{lore_id!r}]"
            _require(
                lore_id in lore_ids,
                f"{spot}: no brief.lore entry carries this id (a vector "
                "for a nonexistent lore row is dead data)",
            )
            _require(
                isinstance(embedding, list) and embedding,
                f"{spot}: must be a non-empty list of numbers (the "
                "embedding — the offline embedder's output, pack data)",
            )
            _require(
                all(
                    _is_number(x) and math.isfinite(float(x))
                    for x in embedding
                ),
                f"{spot}: entries must be finite numbers (a NaN or inf "
                "poisons the ranking — refused loudly)",
            )
            if dim is None:
                dim = len(embedding)
            _require(
                len(embedding) == dim,
                f"{spot}: dimension {len(embedding)} differs from {dim} "
                "(one embedder, one dimension — the query side must "
                "match)",
            )
