"""The actor-side lints: urgencies, factions, names, cultures (the
D-175 split's actors family)."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from core.intent import (
    ACCOUNT_TEST,
    ECHO_TEST,
    PRECONDITION_TESTS,
    TRAIT_TEST,
)
from core.packlint.helpers import _NOUNS, PackError, _ids, _is_int, _require
from core.packlint.shared import lint_account_cond, lint_echo_cond, lint_trait_cond


class ActorsLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _urgencies(self) -> None:
        rules = self._data["rules.json"]
        config = rules.get("urgencies")
        if config is None:
            return
        entities = self._data["entities.json"]
        npc_ids = _ids(entities["npcs"])
        actions = {a["intent"]: a for a in self._data["actions.json"]["actions"]}
        ticks_per_day = rules["time"]["ticks_per_day"]
        seen_pairs: set[tuple[str | None, str | None]] = set()
        _require(
            isinstance(config.get("beat_ticks"), list)
            and all(
                isinstance(t, int) and not isinstance(t, bool)
                and 0 <= t < ticks_per_day
                for t in config["beat_ticks"]
            ),
            "urgencies.beat_ticks must be intraday tick offsets",
        )
        for entry in config.get("entries", ()):
            where = f"urgencies.entries[{entry.get('npc')!r}]"
            _require(entry.get("npc") in npc_ids, f"{where}: unknown npc")
            _require(
                isinstance(entry.get("probability_per_beat"), int)
                and not isinstance(entry.get("probability_per_beat"), bool)
                and 0 <= entry["probability_per_beat"] <= 100,
                f"{where}: probability_per_beat must be 0..100",
            )
            intent = entry.get("intent", {})
            _require(
                isinstance(intent, Mapping)
                and intent.get("kind") in actions,
                f"{where}: intent.kind must name a pack action",
            )
            # engine-2 (D-079): the (npc, kind) pair addresses the entry's
            # roll stream `urgency:<npc>:<kind>` — a duplicate pair would
            # put two entries on one stream and couple their draws
            # (exactly what the per-entry split exists to prevent)
            pair = (entry.get("npc"), intent.get("kind"))
            _require(
                pair not in seen_pairs,
                f"{where}: duplicate urgency (npc, intent.kind) {pair} — "
                f"one goal per NPC per verb (the roll stream is "
                f"content-addressed, engine-2)",
            )
            seen_pairs.add(pair)
            for key in ("target", "fields"):
                if key in intent:
                    if key == "target" and not isinstance(intent[key], str):
                        raise PackError(
                            f"{where}: intent.target must be a string, "
                            f"got {intent.get('target')!r}"
                        )
                    if key == "fields" and not isinstance(intent[key], Mapping):
                        raise PackError(
                            f"{where}: intent.fields must be a mapping, "
                            f"got {intent.get('fields')!r}"
                        )
            for cond in entry.get("requires", ()):
                _require(
                    cond.get("test") in PRECONDITION_TESTS,
                    f"{where}: unknown precondition test {cond.get('test')!r}",
                )
                if cond.get("test") == ECHO_TEST:
                    lint_echo_cond(self._data, cond, where)
                if cond.get("test") == TRAIT_TEST:
                    lint_trait_cond(self._data, cond, where)
                if cond.get("test") == ACCOUNT_TEST:
                    lint_account_cond(self._data, cond, where)
                for param in ("noun", "with", "who"):
                    if param in cond:
                        _require(
                            cond[param] in _NOUNS,
                            f"{where}: precondition {param} {cond[param]!r} "
                            f"must be one of {list(_NOUNS)}",
                        )

    # -- factions (depth-6: small-formula goal dynamics, P3b) ---------------


    def _factions(self) -> None:
        rules = self._data["rules.json"]
        config = rules.get("factions")
        if config is None:
            return  # the unarmed law (the 68a pattern: zero entries, zero draws)
        entities = self._data["entities.json"]
        groups = entities.get("groups", ())
        group_ids = _ids(groups)
        status_axes = {
            axis for axis in rules.get("states", {}) if axis != "notes"
        }
        actions = {a["intent"]: a for a in self._data["actions.json"]["actions"]}
        seen_pairs: set[tuple[str | None, str | None]] = set()
        _require(
            isinstance(config, Mapping),
            "factions must be an object",
        )
        unknown = sorted(set(config) - {"entries", "notes"})
        _require(
            not unknown,
            f"factions: unknown keys {unknown} (the closed vocabulary: "
            "entries | notes)",
        )
        _require(
            isinstance(config.get("entries", ()), list),
            "factions.entries must be a list",
        )
        for entry in config.get("entries", ()):
            _require(
                isinstance(entry, Mapping),
                f"factions.entries: each entry must be an object, got {entry!r}",
            )
            where = f"factions.entries[{entry.get('group')!r}]"
            unknown = sorted(
                set(entry)
                - {
                    "group", "axis", "trigger_value", "threshold",
                    "max_per_beat", "intent", "requires", "notes",
                }
            )
            _require(
                not unknown,
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "group | axis | trigger_value | threshold | max_per_beat "
                "| intent | requires | notes)",
            )
            _require(
                entry.get("group") in group_ids,
                f"{where}: unknown group {entry.get('group')!r} (declare it "
                "in entities.json groups first)",
            )
            _require(
                entry.get("axis") in status_axes,
                f"{where}: axis {entry.get('axis')!r} is not a rules.states "
                "axis (D-006 — the formula reads per-entity status axes)",
            )
            _require(
                _is_int(entry.get("trigger_value"))
                and entry["trigger_value"] >= 0,
                f"{where}: trigger_value must be an integer >= 0 "
                f"(the status family is non-negative), got "
                f"{entry.get('trigger_value')!r}",
            )
            _require(
                _is_int(entry.get("threshold"))
                and 0 <= entry["threshold"] <= 99,
                f"{where}: threshold must be an integer 0..99 (per-cent of "
                "the membership; 100 is dead data — the fraction never "
                "exceeds it)",
            )
            _require(
                _is_int(entry.get("max_per_beat"))
                and 1 <= entry["max_per_beat"] <= 100,
                f"{where}: max_per_beat must be an integer 1..100 (the ramp's "
                "endpoint — 0 is dead data, never a goal)",
            )
            intent = entry.get("intent", {})
            _require(
                isinstance(intent, Mapping)
                and intent.get("kind") in actions,
                f"{where}: intent.kind must name a pack action",
            )
            # D-079 (engine-2's twin): the (group, kind) pair addresses
            # the entry's roll stream `faction:<group>:<kind>` — a
            # duplicate pair puts two entries on one stream and couples
            # their draws (exactly what the per-entry split prevents)
            pair = (entry.get("group"), intent.get("kind"))
            _require(
                pair not in seen_pairs,
                f"{where}: duplicate faction (group, intent.kind) {pair} — "
                f"one goal per group per verb (the roll stream is "
                "content-addressed, engine-2's twin)",
            )
            seen_pairs.add(pair)
            for key in ("target", "fields"):
                if key in intent:
                    if key == "target" and not isinstance(intent[key], str):
                        raise PackError(
                            f"{where}: intent.target must be a string, "
                            f"got {intent.get('target')!r}"
                        )
                    if key == "fields" and not isinstance(intent[key], Mapping):
                        raise PackError(
                            f"{where}: intent.fields must be a mapping, "
                            f"got {intent.get('fields')!r}"
                        )
            for cond in entry.get("requires", ()):
                _require(
                    cond.get("test") in PRECONDITION_TESTS,
                    f"{where}: unknown precondition test {cond.get('test')!r}",
                )
                if cond.get("test") == ECHO_TEST:
                    lint_echo_cond(self._data, cond, where)
                if cond.get("test") == TRAIT_TEST:
                    lint_trait_cond(self._data, cond, where)
                if cond.get("test") == ACCOUNT_TEST:
                    lint_account_cond(self._data, cond, where)
                for param in ("noun", "with", "who"):
                    if param in cond:
                        _require(
                            cond[param] in _NOUNS,
                            f"{where}: precondition {param} {cond[param]!r} "
                            f"must be one of {list(_NOUNS)}",
                        )

    # -- names (name-1, iter-96: the phonotactic profiles + the
    # declarations' reachability) --------------------------------------------


    def _names(self) -> None:
        """The name generator's pack contract (name-1, TASKS; D-116
        (12)): `rules.json::names` — the phonotactic PROFILES,
        culture-keyed n-gram pools (the closed vocabulary: onsets |
        nuclei | codas | syllables | notes; the pools' entries ASCII
        letter fragments, the empty fragment legal in onsets/codas —
        vowel initials and open syllables — never in nuclei, a
        syllable needs its vowel; the bounds a 2-int [min, max] with
        min >= 1 — a zero-syllable name is dead data, the vacuity
        family; no upper ceiling, the bounds are pack tuning). The
        npc record's `generated_name` key names a DECLARED profile,
        mutually exclusive with an authored `name` (one name origin
        per npc — `name` stays the pure string surface every reader
        already knows). The REACHABILITY law (the depth-5b family:
        an armed declaration names at least one LIVE consumer): a
        generated_name npc must ride a group declaring
        `condense_event` — the materialization door; a declaration
        nothing can materialize is dead data, refused."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        config = rules.get("names")
        profiles: Mapping[str, Any] = {}
        if config is not None:
            _require(
                isinstance(config, Mapping),
                "names must be an object",
            )
            unknown = sorted(set(config) - {"profiles", "notes"})
            _require(
                not unknown,
                f"names: unknown keys {unknown} (the closed vocabulary: "
                "profiles | notes)",
            )
            _require(
                isinstance(config.get("profiles", {}), Mapping),
                "names.profiles must be an object (profile id -> the "
                "phonotactic record)",
            )
            profiles = config.get("profiles", {})
        for profile_id, record in profiles.items():
            where = f"names.profiles[{profile_id!r}]"
            _require(
                isinstance(profile_id, str) and profile_id.strip(),
                f"{where}: profile ids must be non-empty strings",
            )
            _require(
                isinstance(record, Mapping),
                f"{where}: the profile must be an object, got {record!r}",
            )
            unknown = sorted(
                set(record) - {"onsets", "nuclei", "codas", "syllables", "notes"}
            )
            _require(
                not unknown,
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "onsets | nuclei | codas | syllables | notes)",
            )
            for key in ("onsets", "nuclei", "codas"):
                pool = record.get(key)
                _require(
                    isinstance(pool, list) and bool(pool),
                    f"{where}: {key} must be a non-empty list",
                )
                for entry in pool:
                    # nuclei: non-empty ASCII letters (a syllable needs
                    # its vowel); onsets/codas: the same, or the empty
                    # fragment (vowel initials, open syllables)
                    legal = (
                        isinstance(entry, str)
                        and (
                            entry.isascii() and entry.isalpha()
                            or (key != "nuclei" and entry == "")
                        )
                    )
                    _require(
                        legal,
                        f"{where}: {key} entries must be ASCII letter "
                        "fragments"
                        + ("" if key == "nuclei" else " (the empty fragment legal)")
                        + f", got {entry!r}",
                    )
            bounds = record.get("syllables")
            _require(
                isinstance(bounds, list) and len(bounds) == 2
                and _is_int(bounds[0]) and _is_int(bounds[1])
                and bounds[0] >= 1 and bounds[0] <= bounds[1],
                f"{where}: syllables must be [min, max] integers with "
                f"min >= 1 and min <= max (a zero-syllable name is dead "
                f"data; no upper ceiling — the bounds are pack tuning), "
                f"got {bounds!r}",
            )
        # the declarations: the npc walk (the only legal site — the
        # members' reachability below reads the groups)
        condensing: set[str] = set()
        for group in entities.get("groups", ()):
            if group.get("condense_event") is not None:
                condensing.update(group.get("members", ()))
        for npc in entities["npcs"]:
            declaration = npc.get("generated_name")
            if declaration is None:
                continue
            where = f"npc {npc['id']}"
            _require(
                isinstance(declaration, str) and declaration in profiles,
                f"{where}: generated_name {declaration!r} is not a declared "
                "profile (names.profiles owns the vocabulary)",
            )
            _require(
                "name" not in npc,
                f"{where}: authored name and generated_name are mutually "
                "exclusive — one name origin per npc (name stays the pure "
                "string surface)",
            )
            _require(
                npc["id"] in condensing,
                f"{where}: generated_name is dead data — the npc is not a "
                "member of any group declaring condense_event (the "
                "materialization door; the depth-5b reachability law)",
            )

    # -- the cultures block (iter-119: the estrangement metadata) --------


    def _pack_text_without(self, block: str) -> str:
        """Every string the pack's data carries — keys, values and notes
        prose (the raw-text family the stoplist self-check searches),
        MINUS one rules block: the vocabulary check below must never
        find its own declaration (the self-reference exclusion)."""
        chunks: list[str] = []

        def walk(node: Any) -> None:
            if isinstance(node, Mapping):
                for key, value in node.items():
                    if isinstance(key, str):
                        chunks.append(key)
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
            elif isinstance(node, str):
                chunks.append(node)

        for name, data in self._data.items():
            if name == "rules.json" and isinstance(data.get(block), Mapping):
                data = {key: value for key, value in data.items() if key != block}
            walk(data)
        return "\n".join(chunks)


    def _cultures(self) -> None:
        """The cultures block's pack contract (world-2 L2 slice 2, the
        cultures half — D-130's sketch, D-154): the ESTRANGEMENT
        METADATA, the budget-block precedent — load-time lint, ZERO
        runtime surface ("prohibitions as pack metadata, never bonuses",
        REFERENCES §10; enforced as log asserts at gate review,
        PACK_SPEC §5). One record per culture (the CK3 culture keying:
        pillars + domain-token lists): `name_profile` — the profile the
        culture's names draw from, must be a declared `names.profiles`
        id; `custom_vocabulary` — the culture's own words, each must
        occur in the pack data OUTSIDE this block as a full segment (the
        anti-rot twin of the stoplist self-check — a word nothing in the
        pack carries is dead vocabulary, the depth-5b reachability
        family); `prohibitions` — the culture's laws (what it CANNOT
        do, the WH40k grammar): each entry carries a non-empty `law`
        and the OPTIONAL `flaw` — when present it must name a MEMBER's
        declared spine flaw (AP-8's prohibition surface, the culture's
        limit over the flaw; the consumption union lives in
        `_live_char`); `members` — the declared-npc cast, one culture
        each (a member of two cultures is an ambiguity), and a member
        declaring a generated name must name THIS culture's profile
        (the culture↔name keying made executable — the CK3
        culture↔name-pool binding, `docs/ref/ck3.md`)."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        config = rules.get("cultures")
        if config is None:
            return  # the unarmed law (the 68a pattern — the other packs)
        _require(
            isinstance(config, Mapping),
            "cultures must be an object (culture id -> the record)",
        )
        profiles = (
            rules.get("names", {}).get("profiles", {})
            if isinstance(rules.get("names"), Mapping) and
            isinstance(rules.get("names", {}).get("profiles"), Mapping)
            else {}
        )
        npc_records = {npc["id"]: npc for npc in entities["npcs"]}
        spines = {
            npc_id: record.get("spine", {}).get("flaw")
            for npc_id, record in npc_records.items()
            if isinstance(record.get("spine"), Mapping)
        }
        # the anti-rot corpus: the whole pack's strings, this block
        # excluded (computed once — the walk below is the only reader)
        pack_text = self._pack_text_without("cultures")
        claimed: dict[str, str] = {}  # npc id -> the culture that claimed them
        for culture_id, record in config.items():
            if culture_id == "notes":
                continue  # the block-level commentary field
            where = f"cultures[{culture_id!r}]"
            _require(
                isinstance(culture_id, str) and culture_id.strip(),
                f"{where}: culture ids must be non-empty strings",
            )
            _require(
                isinstance(record, Mapping),
                f"{where}: the culture must be an object, got {record!r}",
            )
            required = ("name_profile", "custom_vocabulary", "prohibitions", "members")
            unknown = sorted(
                set(record) - set(required) - {"notes"}
            )
            _require(
                not unknown,
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "name_profile | custom_vocabulary | prohibitions | members "
                "| notes)",
            )
            for key in required:
                _require(
                    key in record,
                    f"{where}.{key} is required — a half-declared culture is "
                    "a broken culture (all-or-nothing, the spine's own law)",
                )
            # the profile binding (the culture↔name keying)
            profile = record["name_profile"]
            _require(
                isinstance(profile, str) and profile in profiles,
                f"{where}.name_profile {profile!r} is not a declared "
                "profile (rules.json names.profiles owns the vocabulary)",
            )
            # the custom vocabulary (the anti-rot walk)
            vocabulary = record["custom_vocabulary"]
            _require(
                isinstance(vocabulary, list) and bool(vocabulary),
                f"{where}.custom_vocabulary must be a non-empty list "
                "(a culture with no words of its own is dead data)",
            )
            for word in vocabulary:
                _require(
                    isinstance(word, str) and bool(word.strip()),
                    f"{where}.custom_vocabulary: words must be non-empty "
                    f"strings, got {word!r}",
                )
                pattern = re.compile(
                    rf"(?<![a-zA-Z0-9]){re.escape(word)}(?![a-zA-Z0-9])",
                    re.IGNORECASE,
                )
                _require(
                    pattern.search(pack_text) is not None,
                    f"{where}.custom_vocabulary: {word!r} occurs nowhere in "
                    "the pack data outside the cultures block (dead "
                    "vocabulary — the word must belong to the pack, the "
                    "reachability law)",
                )
            # the member cast (one culture each, the keying check) —
            # validated BEFORE the prohibition set reads it (the
            # member-flaw binding below walks the same list)
            members = record["members"]
            _require(
                isinstance(members, list) and bool(members),
                f"{where}.members must be a non-empty list (a culture of "
                "nobody is dead data, the vacuity family)",
            )
            for member in members:
                _require(
                    member in npc_records,
                    f"{where}.members: {member!r} is not a declared npc",
                )
                other = claimed.get(member)
                _require(
                    other is None,
                    f"{where}.members: {member!r} already belongs to "
                    f"{other!r} (one culture per npc — two is an "
                    "ambiguity)",
                )
                claimed[member] = str(culture_id)
                declaration = npc_records[member].get("generated_name")
                if declaration is not None:
                    _require(
                        declaration == profile,
                        f"{where}.members: {member!r} declares "
                        f"generated_name {declaration!r} but the culture's "
                        f"profile is {profile!r} (the culture↔name keying — "
                        "a member's drawn name comes from the culture's own "
                        "tongue)",
                    )
            # the prohibition set (the culture's laws)
            prohibitions = record["prohibitions"]
            _require(
                isinstance(prohibitions, list) and bool(prohibitions),
                f"{where}.prohibitions must be a non-empty list (a culture "
                "with no law is dead data — two prohibition sets minimum "
                "per the estrangement family)",
            )
            member_flaws = {
                flaw
                for flaw in (spines.get(member) for member in members)
                if isinstance(flaw, str)
            }
            for entry in prohibitions:
                entry_where = f"{where}.prohibitions"
                _require(
                    isinstance(entry, Mapping),
                    f"{entry_where}: entries must be objects "
                    "(law | flaw | notes), got {entry!r}",
                )
                unknown_entry = sorted(set(entry) - {"law", "flaw", "notes"})
                _require(
                    not unknown_entry,
                    f"{entry_where}: unknown keys {unknown_entry} (the "
                    "closed vocabulary: law | flaw | notes)",
                )
                _require(
                    isinstance(entry.get("law"), str)
                    and bool(entry["law"].strip()),
                    f"{entry_where}.law is required and must be a non-empty "
                    "string (the law names itself)",
                )
                flaw = entry.get("flaw")
                if flaw is None:
                    continue  # a pure culture law, no member flaw root
                _require(
                    isinstance(flaw, str) and flaw in member_flaws,
                    f"{entry_where}: flaw {flaw!r} names no declared spine "
                    f"flaw of a member of {culture_id!r} (AP-8: the "
                    "prohibition is the culture's limit over a member's "
                    "flaw — the law roots in the cast it bounds)",
                )

    # -- director (iter-4: consequence buffer + triggers + stagnation) --------
