"""The cross-domain shared lints (the D-175 split): the action
knowledge-entry walker (read by the actions and the transitions lints)
and the echo/trait cond linters (read by the actions, urgencies and
factions lints) — the only _Lint methods with callers in more than one
family, hoisted here as plain functions over the loaded pack data."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.intent import AUDIENCES, KNOWLEDGE_SLOTS, PRESENT_SITES
from core.packlint.helpers import _EXCEPT_TOKENS, _SLOT, _is_int, _require


def knowledge_entry(
    data: dict[str, Mapping[str, Any]], action_intent: str, record: Mapping[str, Any],
    requires: tuple[Mapping[str, Any], ...] = (),
) -> None:
    knowledge = data["rules.json"]["knowledge"]
    where = f"action {action_intent!r} knowledge"
    _require(record["who"] in AUDIENCES, f"{where}: unknown audience {record['who']!r}")
    _require(
        record["channel"] in knowledge["channels"],
        f"{where}: unknown channel {record['channel']!r}",
    )
    _require(
        record["fidelity"] in knowledge["fidelity_chain"],
        f"{where}: unknown fidelity {record['fidelity']!r}",
    )
    if record["who"] == "destination_location":
        # resolves against the target location: the action must pin the
        # target's kind to location (movement sighting audiences)
        _require(
            any(
                cond.get("noun") == "target"
                and cond.get("test") == "kind"
                and cond.get("is") == "location"
                for cond in requires
            ),
            f"{where}: audience 'destination_location' requires a "
            f"target-kind-location precondition",
        )
    if "present_at" in record:
        # The per-present-target expansion (st-1, INTENT_SCHEMA §7): the
        # audience stays `actor` (KI#43's law — this is a `knows`
        # expansion, NOT an audience kind), the site is a closed set,
        # and the {present} slot must actually be used — a site without
        # the slot would emit N identical records.
        _require(
            record["who"] == "actor",
            f"{where}: a 'present_at' expansion requires who == 'actor' "
            f"(the audience stays actor — INTENT_SCHEMA §7)",
        )
        _require(
            record["present_at"] in PRESENT_SITES,
            f"{where}: unknown present_at site {record['present_at']!r} "
            f"(must be one of {list(PRESENT_SITES)})",
        )
        _require(
            not record.get("except"),
            f"{where}: 'except' has no meaning on a 'present_at' "
            f"expansion (the audience is the actor alone)",
        )
        _require(
            "present" in _SLOT.findall(record["knows"]),
            f"{where}: 'present_at' declared but the knows template "
            f"{record['knows']!r} lacks the {{present}} slot",
        )
        if record["present_at"] == "destination_location":
            _require(
                any(
                    cond.get("noun") == "target"
                    and cond.get("test") == "kind"
                    and cond.get("is") == "location"
                    for cond in requires
                ),
                f"{where}: 'present_at=destination_location' requires a "
                f"target-kind-location precondition",
            )
    elif "present" in _SLOT.findall(record["knows"]):
        # the mirror: the {present} slot has no semantics without a
        # site — the closed-slot lint alone would pass it
        _require(
            False,
            f"{where}: the {{present}} slot requires a 'present_at' "
            f"expansion site on the record",
        )
    for token in record.get("except", ()):
        _require(
            token in _EXCEPT_TOKENS,
            f"{where}: unknown except token {token!r}",
        )
    for slot in _SLOT.findall(record["knows"]):
        _require(
            slot in KNOWLEDGE_SLOTS,
            f"{where}: unknown slot {{{slot}}} in {record['knows']!r}",
        )


def literal_knows_tokens(data: Mapping[str, Mapping[str, Any]]) -> set[str]:
    """Every knowledge token the pack can mint as a literal string:
    the `knows` values declared without slot braces across the three
    birth sites — action knowledge templates (all branches + the
    texture path), expectation rules, and transition-layer knowledge
    entries. The reaction systems (telling, crime) only transfer
    existing tokens, so this IS the birth vocabulary; templated
    values (containing `{`) are excluded — a secret's subject is a
    fixed entity, and a templated token's subject varies with the
    world."""
    tokens: set[str] = set()

    def _take(entry: Any) -> None:
        knows = entry.get("knows") if isinstance(entry, Mapping) else None
        if isinstance(knows, str) and "{" not in knows:
            tokens.add(knows)

    for action in data["actions.json"]["actions"]:
        knowledge = action.get("knowledge", {})
        if isinstance(knowledge, Mapping):
            for branch in knowledge.values():
                if isinstance(branch, list):
                    for entry in branch:
                        _take(entry)
        texture = action.get("texture", {})
        if isinstance(texture, Mapping):
            for branch in texture.get("knowledge", {}).values():
                if isinstance(branch, list):
                    for entry in branch:
                        _take(entry)
    rules = data["rules.json"]
    for rule in rules.get("expectations", {}).get("rules", ()):
        if isinstance(rule, Mapping):
            _take(rule)
    for config in rules.get("transitions", {}).values():
        if isinstance(config, Mapping):
            for entry in config.get("knowledge", {}).values():
                _take(entry)
    return tokens


def lint_echo_cond(data: dict[str, Mapping[str, Any]], cond: Mapping[str, Any], where: str) -> None:
    """The echo_at_least precondition contract, shared by the action
    and urgency `requires` lints: `axis` must name a declared echo
    axis and `value` must sit strictly above the scale floor and at
    or below the ceiling — outside those bounds the gate can never
    pass (score clamps into the scale) or never fails (always above
    the floor), dead vocabulary either way, refused at load."""
    echo_cfg = data["rules.json"].get("echo")
    axes: set[str] = set()
    if isinstance(echo_cfg, Mapping):
        for spec in echo_cfg.get("tokens", {}).values():
            if isinstance(spec, Mapping):
                axes.update(spec.get("axes", ()))
    _require(
        bool(axes) and cond.get("axis") in axes,
        f"{where}: precondition echo_at_least requires 'axis' naming "
        "a declared echo axis (the fold scores only the declared "
        "vocabulary — anything else is dead data)",
    )
    assert isinstance(echo_cfg, Mapping)  # non-empty axes imply the block
    lo, hi = echo_cfg["scale"]
    _require(
        _is_int(cond.get("value")) and lo < cond["value"] <= hi,
        f"{where}: precondition echo_at_least value must be an "
        f"integer in {lo + 1}..{hi} (the score clamps to the scale — "
        "outside it the gate is dead vocabulary)",
    )


def lint_trait_cond(
    data: dict[str, Mapping[str, Any]], cond: Mapping[str, Any], where: str
) -> None:
    """The trait_held precondition contract (beliefwire, iter-67),
    shared by the action and urgency `requires` lints: `token` must
    name a declared belief in `rules.json::traits.beliefs` — the
    fold only answers tokens the block declares, anything else is a
    dead gate (the echo_at_least axis family: dead vocabulary is
    refused at load, never silently always-False). A pack without a
    traits block carrying a trait gate is the same refusal — the
    gate names vocabulary nobody minted."""
    beliefs = data["rules.json"].get("traits", {}).get("beliefs", {})
    _require(
        cond.get("token") in beliefs,
        f"{where}: precondition trait_held requires 'token' naming a "
        "declared traits.beliefs belief (the fold answers only the "
        "declared vocabulary — anything else is dead data)",
    )


def lint_account_cond(
    data: dict[str, Mapping[str, Any]], cond: Mapping[str, Any], where: str
) -> None:
    """The account_at_least precondition contract (res-1, the economy
    substrate), shared by the action, urgency, faction and texture
    `requires` lints: `kind` must name a declared economy.accounts kind
    and `value` a non-negative integer — the door reads only declared
    stocks, a kind outside the vocabulary is a dead gate (the
    echo_at_least axis family: dead vocabulary is refused at load,
    never silently always-False)."""
    economy = data["rules.json"].get("economy")
    vocabulary = (
        economy.get("accounts") if isinstance(economy, Mapping) else None
    )
    _require(
        isinstance(vocabulary, list) and cond.get("kind") in vocabulary,
        f"{where}: precondition account_at_least requires 'kind' naming "
        "a declared economy.accounts kind (the door reads only the "
        "declared stocks — anything else is dead data)",
    )
    _require(
        _is_int(cond.get("value")) and cond["value"] >= 0,
        f"{where}: precondition account_at_least value must be a "
        "non-negative integer",
    )


_DIRECT_INDEXED_KEYS: Final[Mapping[str, Mapping[str, str]]] = {
    "carries_flagged": {"flag": "string"},
    "flagged_accessible": {"flag": "string"},
    "field_in": {"field": "string", "values": "list"},
    "field_nonempty": {"field": "string"},
    "has_field": {"field": "string"},
}
"""The directly-indexed cond keys (KI#89, closed iter-169): the five
record-reading tests whose parameters the door subscripts (`cond[key]`,
never `.get`) — the key is a lint-required parameter, presence plus the
type the door consumes. The lint family's single table: the same cond
shape is refused identically wherever a `requires` list is declared."""


def lint_direct_keys(cond: Mapping[str, Any], where: str) -> None:
    """The directly-indexed key rows (KI#89, closed iter-169), shared by
    the action, urgency, faction and texture `requires` lints (the
    lint_echo_cond family): the five record-reading tests read their
    named parameters by subscript — a cond that loads without one
    KeyErrors mid-run at the door or the beat gate (the iter-45
    leverage `who` family: refuse at load what would crash at
    completion). Non-emptiness rides the same row: an empty flag or
    field name, or an empty `values` set, is dead vocabulary (the gate
    can never pass — the echo bounds family's own law)."""
    test = cond.get("test")
    if not isinstance(test, str):
        return  # the caller's unknown-test row owns the refusal
    spec = _DIRECT_INDEXED_KEYS.get(test)
    if spec is None:
        return
    for key, kind in spec.items():
        value = cond.get(key)
        if kind == "string":
            _require(
                isinstance(value, str) and value,
                f"{where}: precondition {test} requires '{key}' — a "
                f"non-empty string the door indexes directly (a missing "
                f"or empty key is a load-time refusal, never a mid-run "
                f"KeyError)",
            )
        else:
            _require(
                isinstance(value, list) and value,
                f"{where}: precondition {test} requires '{key}' — a "
                f"non-empty list (an empty one is dead vocabulary: the "
                f"gate can never pass)",
            )
