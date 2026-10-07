"""RngBank: the single point of randomness control (INV-2, RNG-1, D-028).

One master seed; named streams deterministically derived via
`stable_hash(f"{seed}:{stream}")` — sha256-based, environment-independent
(never relies on PYTHONHASHSEED). THE EPOCH (rng-1, the owner's C-13
call): the value at a stream's draw position `k` is a PURE COUNTER
FUNCTION — `U(stream, k) = word (k mod 4) of sha256(f"{key}:{k div 4})`
where `key = stable_hash(f"{seed}:{stream}")` — read in 64-bit
big-endian words, so O(1) access to the k-th draw, a checkpoint state
of COUNTERS ONLY (never generator internals), and branch isolation: an
added or removed draw anywhere shifts no later draw's index (each
position's value is fixed by construction). The Mersenne Twister named
streams (the pre-epoch bank) could serve none of these without O(k)
replay; their canonical bytes die at the epoch boundary (rng-1's
recorded price — the corpus regeneration, never a silent read).

Registered streams: `substantive` (canon checks) and `cosmetic`
(render-only); plus seven CONTENT-ADDRESSED FAMILIES of lazily
registered streams, whose names are built by the owning module and
pack-linted before any draw — `urgency:<npc>:<kind>` (engine-2,
D-079, `urgency_stream_name`), `drift:<family>` (rumordrift, A2''/
D-099, `drift_stream_name`), `scene:<id>:detail` (lazy detail
materialization, depth-2, `scene_detail_stream_name`),
`worldgen:<pass>` (the ordered worldgen passes, depth-5,
`worldgen_stream_name`), `faction:<group>:<kind>` (the faction
goal rolls, depth-6, `faction_stream_name`), `name:<npc>` (the
generated names, name-1, `name_stream_name`), and `weather:chain`
(weather-1, `weather_stream_name`). All draws flow through the bank,
which counts them per stream; the substantive counter is the replay
fingerprint T1 compares. The draw forms: `randint(lo, hi)` = `lo +
U mod (hi - lo + 1)` (the modulo bias over a 64-bit draw is <=
span/2**64 — negligible at every real range); `random()` =
`(U >> 11) / 2**53` (the [0, 1) 53-bit form). A per-stream BLOCK
MEMO (the sha256 of the current 4-draw block) is derived state —
pure function of (key, block index), recomputed on any counter jump,
never exported (the checkpoint carries counters only).

Guards (donor discipline, `docs/blueprint/phase0.md` §1):

- `assure(name)` — run a scope with `name` as the active stream (Brogue
  `assureCosmeticRNG`). Nesting a *different* stream inside an assured
  scope raises immediately — EXCEPT the seven content-addressed
  families: an urgency-, drift-, scene-, worldgen-, faction-, name-, or
  weather-family stream may shadow the assured `substantive` run scope
  (engine-2, rumordrift + lazy detail (depth-2), worldgen (depth-5),
  factions (depth-6), names (name-1), weather (weather-1)): all are
  canon-relevant but stream-isolated per declared entry, so an added,
  removed, or re-armed pack entry shifts neither a later canon check
  draw nor another entry's roll — the single shared stream was measured
  and refused for urgencies (the entries coupled by draw position;
  D-079); drift, scene detail, the worldgen passes, the generated
  names, and the weather chain inherit the same isolation law
  (D-095: "isolation is law"; at pass granularity a re-tuned map
  config shifts neither a canon check draw nor another pass's draws).
  Under the epoch the isolation law is structural: a stream's draw at
  position k is fixed by (seed, stream, k) alone, so a re-armed
  neighbor entry cannot move it even in principle. A wrong-stream draw
  is loud, never silent.
- `audit(name)` — assert zero draws on `name` inside the scope (DCSS
  `ASSERT_stable`); the test-side assertion.
- `peek(name)` — non-advancing read of the next float (tests only).

A draw outside any `assure` scope goes to the default active stream:
`substantive` (canon is the default; render paths must assure cosmetic).
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import Any, Final

__all__ = [
    "COSMETIC",
    "DRIFT_PREFIX",
    "FACTION_PREFIX",
    "FAMILY_PREFIXES",
    "NAME_PREFIX",
    "PHASE0_STREAMS",
    "SCENE_PREFIX",
    "SUBSTANTIVE",
    "URGENCY_PREFIX",
    "WEATHER_PREFIX",
    "WORLDGEN_PREFIX",
    "RngBank",
    "RngError",
    "drift_stream_name",
    "faction_stream_name",
    "name_stream_name",
    "scene_detail_stream_name",
    "stable_hash",
    "urgency_stream_name",
    "weather_stream_name",
    "worldgen_stream_name",
]

SUBSTANTIVE: Final = "substantive"
COSMETIC: Final = "cosmetic"
URGENCY_PREFIX: Final = "urgency:"
DRIFT_PREFIX: Final = "drift:"
SCENE_PREFIX: Final = "scene:"
WORLDGEN_PREFIX: Final = "worldgen:"
FACTION_PREFIX: Final = "faction:"
NAME_PREFIX: Final = "name:"
WEATHER_PREFIX: Final = "weather:"
PHASE0_STREAMS: Final = (SUBSTANTIVE, COSMETIC)

# The seven lazily registered content-addressed families (D-079's law,
# extended by drift, scene detail, the worldgen passes, the faction
# goal rolls, the generated names, and the weather chain): the
# name-building functions are the single owners of each grammar, and the
# pack lint validates the ids inside before any draw.
FAMILY_PREFIXES: Final = (
    URGENCY_PREFIX,
    DRIFT_PREFIX,
    SCENE_PREFIX,
    WORLDGEN_PREFIX,
    FACTION_PREFIX,
    NAME_PREFIX,
    WEATHER_PREFIX,
)

# The counter block: one sha256 digest serves BLOCK draws (four
# 64-bit big-endian words); the block index of draw position k is
# k >> BLOCK_SHIFT, the word index is k & (BLOCK_SIZE - 1).
_BLOCK_SHIFT: Final = 2
_BLOCK_SIZE: Final = 1 << _BLOCK_SHIFT
_WORD_MASK: Final = _BLOCK_SIZE - 1


def urgency_stream_name(npc: str, intent_kind: str) -> str:
    """The per-entry urgency roll stream: content-addressed
    `urgency:<npc>:<kind>` (engine-2, D-079). One stream per pack urgency
    entry — the (npc, kind) pair is pack-linted unique, so the name is
    injective; adding an entry adds a NEW stream and never shifts another
    entry's draws (the add-safety law)."""
    return f"{URGENCY_PREFIX}{npc}:{intent_kind}"


def drift_stream_name(family: str) -> str:
    """The per-family rumor-drift stream: content-addressed
    `drift:<family>` (rumordrift, A2''/D-099). One stream per pack-declared
    `knowledge.drift` family — family ids are map keys, so the name is
    injective; arming, adding, or removing a family shifts neither a canon
    check draw nor another family's rolls (the isolation law, D-095)."""
    return f"{DRIFT_PREFIX}{family}"


def scene_detail_stream_name(location_id: str) -> str:
    """The per-scene lazy-detail stream: content-addressed
    `scene:<id>:detail` (depth-2, `phases.md` §5 — the D-079 family law's
    third member). One stream per pack-declared `scene_detail` location —
    location ids are entities.json map keys, so the name is injective;
    arming a scene's detail block draws from that scene's OWN stream, so
    it shifts neither a canon check draw nor another scene's details
    (the isolation law at stream-address granularity; the within-scene
    slot list is one pack unit — a slot-list edit is a content change,
    D-079's content-landing protocol, its corpus price paid at arming)."""
    return f"{SCENE_PREFIX}{location_id}:detail"


def worldgen_stream_name(pass_name: str) -> str:
    """The per-pass worldgen stream: content-addressed
    `worldgen:<pass>` (depth-5, `phases.md` §5 — the D-079 family law's
    fourth member; the pass names are the closed `PASS_ORDER` vocabulary
    of `core/worldgen.py`, ":"-free and unique, so the name is injective).
    One stream per ordered pass — re-tuning, adding, or removing a pass
    shifts neither a canon check draw nor another pass's draws (the
    isolation law at pass granularity; the corpus price of arming
    worldgen is the genesis events alone, never a moved canon check)."""
    return f"{WORLDGEN_PREFIX}{pass_name}"


def faction_stream_name(group_id: str, intent_kind: str) -> str:
    """The per-entry faction goal-roll stream: content-addressed
    `faction:<group>:<kind>` (depth-6, `phases.md` §5 P3b — the D-079
    family law's fifth member). One stream per pack-declared faction
    entry — the (group, kind) pair is pack-linted unique and group ids
    are entity-unique across categories, so the name is injective;
    adding, removing, or re-tuning a faction shifts neither a canon
    check draw nor another entry's rolls (the isolation law at faction
    granularity — the KeeperRL small formula's odds are the world's own
    derived number, never another stream's draw positions)."""
    return f"{FACTION_PREFIX}{group_id}:{intent_kind}"


def name_stream_name(npc: str) -> str:
    """The per-npc generated-name stream: content-addressed `name:<npc>`
    (name-1, `phases.md` §5 — the D-079 family law's sixth member; the
    scene-detail twin: a lazy per-entity materialization). One stream
    per npc declaring a generated name — npc ids are entity-unique
    across categories, so the name is injective; arming, adding, or
    removing a declaration shifts neither a canon check draw nor
    another npc's name (the isolation law at declaration granularity;
    the birth is first-commit-wins, so a re-tuned profile pays its
    corpus price only on the unborn — canon names are never redrawn)."""
    return f"{NAME_PREFIX}{npc}"


def weather_stream_name() -> str:
    """The weather chain's own stream: content-addressed `weather:chain`
    (weather-1, `phases.md` §5 — the D-079 family law's seventh member;
    SINGLETON: the world's one weather chain, the block's own
    granularity — one stream, nothing else draws from it). Arming or
    re-tuning the weather block shifts neither a canon check draw nor
    any other family's rolls (the isolation law at world granularity —
    the ambient family's draws never touch the substantive
    fingerprint, so the armed twin's corpus price is the weather events
    alone, never a moved canon check)."""
    return f"{WEATHER_PREFIX}chain"


class RngError(RuntimeError):
    """INV-2 violation: wrong-stream draw, an audit-scope draw leak, or
    a bank state from another epoch."""


def stable_hash(text: str) -> int:
    """Environment-independent 64-bit hash: sha256, first 8 bytes, big-endian."""
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def _draw_word(key: int, position: int, memo: dict[str, tuple[int, bytes]], name: str) -> int:
    """The 64-bit word at a stream's draw position: the epoch's counter
    function. Pure in (key, position); the block memo is derived state —
    recomputed whenever the position's block differs, correct by
    construction on any counter jump (restore, branch, seek)."""
    block_index = position >> _BLOCK_SHIFT
    cached = memo.get(name)
    if cached is None or cached[0] != block_index:
        digest = hashlib.sha256(f"{key}:{block_index}".encode()).digest()
        cached = (block_index, digest)
        memo[name] = cached
    word = position & _WORD_MASK
    return int.from_bytes(cached[1][8 * word:8 * word + 8], "big")


class RngBank:
    """Holds every named stream; the only door to entropy (L5). The
    epoch (rng-1): a stream's draws are its counter positions — the
    checkpoint is the counts, nothing else."""

    def __init__(self, seed: int, streams: Iterable[str] = PHASE0_STREAMS) -> None:
        self._seed = int(seed)
        self._keys: dict[str, int] = {}
        self._counts: dict[str, int] = {}
        self._memo: dict[str, tuple[int, bytes]] = {}
        self._active: str = SUBSTANTIVE
        self._assured: str | None = None
        for name in streams:
            self._register(name)

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def active(self) -> str:
        """The stream draws currently route to."""
        return self._active

    def _register(self, name: str) -> None:
        if name in self._counts:
            raise RngError(f"duplicate stream {name!r}")
        self._keys[name] = stable_hash(f"{self._seed}:{name}")
        self._counts[name] = 0

    def _ensure(self, name: str) -> None:
        """Register `name` if the family law admits it; loud otherwise."""
        if name not in self._counts:
            if name.startswith(FAMILY_PREFIXES):
                # engine-2 + rumordrift + lazy detail (depth-2) + the
                # worldgen passes (depth-5) + the faction goal rolls
                # (depth-6) + the generated names (name-1) + the weather
                # chain (weather-1): the seven content-addressed stream
                # families register lazily — names built by
                # `urgency_stream_name`
                # / `drift_stream_name` / `scene_detail_stream_name` /
                # `worldgen_stream_name` / `faction_stream_name` /
                # `name_stream_name` / `weather_stream_name`,
                # pack-linted before any draw; the closed-set tripwire
                # survives for every non-family name (a typo stays
                # loud).
                self._register(name)
            else:
                raise RngError(
                    f"unknown stream {name!r} (known: {sorted(self._counts)})"
                )

    def count(self, name: str = SUBSTANTIVE) -> int:
        """Draws taken from `name` so far (the counter positions)."""
        return self._counts[name]

    @property
    def fingerprint(self) -> int:
        """Replay fingerprint: the substantive draw count (RNG-1)."""
        return self._counts[SUBSTANTIVE]

    @contextmanager
    def assure(self, name: str) -> Iterator[None]:
        """Scope with `name` active; nesting a foreign stream is an error
        unless the pairing is the content-addressed family law: an
        urgency-, drift-, scene-, worldgen-, faction-, name-, or
        weather-family stream may shadow the assured substantive run
        scope — and nothing else may nest anywhere."""
        self._ensure(name)
        if (
            self._assured is not None
            and self._assured != name
            and not (
                name.startswith(FAMILY_PREFIXES)
                and self._assured == SUBSTANTIVE
            )
        ):
            raise RngError(
                f"cannot assure {name!r} inside an assured {self._assured!r} scope"
            )
        prev_active, prev_assured = self._active, self._assured
        self._active, self._assured = name, name
        try:
            yield
        finally:
            self._active, self._assured = prev_active, prev_assured

    @contextmanager
    def audit(self, name: str = SUBSTANTIVE) -> Iterator[None]:
        """Assert zero draws on `name` inside the scope (DCSS ASSERT_stable)."""
        self._ensure(name)  # fail fast on unknown stream names
        before = self._counts[name]
        try:
            yield
        except BaseException:
            raise
        else:
            drawn = self._counts[name] - before
            if drawn:
                raise RngError(f"{drawn} draw(s) on stream {name!r} inside audit scope")

    def peek(self, name: str = SUBSTANTIVE) -> float:
        """Next float of `name` without advancing it (tests only)."""
        self._ensure(name)
        word = _draw_word(self._keys[name], self._counts[name], self._memo, name)
        return (word >> 11) / 2**53

    def next_d100_hit(
        self, name: str, probability: int, limit: int
    ) -> int | None:
        """The smallest offset j in [1, limit] such that the d100 roll
        the stream would draw at position ``count + j - 1`` HITS
        (``1 + U mod 100 <= probability``) — H9's quiet-beat scan
        primitive (iter-337). Pure: never advances the counter, never
        touches the block memo (the scan walks its own digests — the
        landed draw recomputes them through the normal path, exactly as
        the tick-by-tick run would). ``None`` when no draw within the
        limit hits; ``probability >= 100`` answers 1 (every draw hits);
        ``probability <= 0`` answers None (none ever does — the
        probability-0 entry's roll is still consumed by the walk, but
        never fires, so it never constrains a landing). The offset is
        in BEATS-from-now: the caller maps it onto the beat grid."""
        self._ensure(name)
        if limit <= 0 or probability <= 0:
            return None
        if probability >= 100:
            return 1
        key = self._keys[name]
        base = self._counts[name]
        pos = base
        remaining = limit
        while remaining > 0:
            block_index = pos >> _BLOCK_SHIFT
            digest = hashlib.sha256(f"{key}:{block_index}".encode()).digest()
            start_word = pos & _WORD_MASK
            take = min(_BLOCK_SIZE - start_word, remaining)
            for word_index in range(start_word, start_word + take):
                word = int.from_bytes(
                    digest[8 * word_index:8 * word_index + 8], "big"
                )
                if word % 100 < probability:
                    return pos - base + (word_index - start_word) + 1
            pos += take
            remaining -= take
        return None

    def skip_draws(self, name: str, count: int) -> None:
        """Advance ``name``'s counter by ``count`` positions WITHOUT
        drawing — H9's counter jump across quiet beats (iter-337). The
        quiet-beat skip's own law: a skipped beat consumes exactly the
        rolls its rolling entries would have drawn (one per entry per
        beat, the values unconsumed by anything — the beat committed
        nothing, so no check, duration, or pick ever read them); the
        jump is therefore the tick-by-tick counters advanced in one
        arithmetic step, and the landed beat's first draw reads the
        same position both paths would. The only caller is the loop's
        ``_apply_skip``; the A/B byte-identity law (tests/test_h9.py)
        is the operation's falsifier — a wrong jump is a wrong canon,
        never a wrong speed."""
        if count < 0:
            raise RngError(f"skip_draws count must be >= 0, got {count}")
        self._ensure(name)
        self._counts[name] += count

    # -- draw surface (the only advancing operations) -----------------------

    def randint(self, lo: int, hi: int) -> int:
        """Inclusive integer draw from the active stream: `lo + U mod span`
        (one counter position per call, uniform at every real range —
        the modulo bias over a 64-bit word is <= span/2**64)."""
        if hi < lo:
            raise ValueError(f"empty range for randint: [{lo}, {hi}]")
        name = self._active
        word = _draw_word(self._keys[name], self._counts[name], self._memo, name)
        self._counts[name] += 1
        return lo + word % (hi - lo + 1)

    def random(self) -> float:
        """Float draw from the active stream: `(U >> 11) / 2**53`, the
        [0, 1) 53-bit form (one counter position per call)."""
        name = self._active
        word = _draw_word(self._keys[name], self._counts[name], self._memo, name)
        self._counts[name] += 1
        return (word >> 11) / 2**53

    # -- the resume door (iter-106, D-139): entropy positions ----------

    def export_state(self) -> dict[str, Any]:
        """The bank's full entropy position, JSON-ready: every registered
        stream's draw COUNTER — the epoch's tiny checkpoint (rng-1: the
        pre-epoch form carried each stream's 624-word Mersenne Twister
        state; the counter form is the whole position). EXCEPT the
        worldgen family (their positions are genesis-scoped —
        `generate_world` re-derives them from the fresh seed at resume,
        so a cursor must never carry them; under the epoch the
        re-derivation recomputes the same pure values by construction).
        Sorted stream names; the same run state serializes to the same
        bytes in any process (INV-2's spirit — `core/cursor.py` owns the
        artifact around this payload)."""
        counts: dict[str, int] = {}
        for name in sorted(self._counts):
            if name.startswith(WORLDGEN_PREFIX):
                continue  # genesis-scoped: rebuilt, never restored
            counts[name] = self._counts[name]
        return {"counts": counts}

    def restore_state(self, mapping: Mapping[str, Any]) -> None:
        """Restore draw counters (the resume door's bank half —
        `Simulator.resume` is the only caller). The payload is counts
        ONLY: a mapping carrying `streams` (Mersenne Twister states) is
        a cursor from the pre-epoch bank — refused LOUD, never silently
        drifted across the epoch boundary (rng-1's recorded price: the
        run restarts from its log; the log itself stays replayable and
        foldable — INV-1/INV-5 untouched). The worldgen family is
        REFUSED loudly as ever: a cursor carrying `worldgen:<pass>`
        positions claims a state `generate_world` is about to re-derive
        differently. The always-registered pair (`substantive`,
        `cosmetic`) must be present: an export without the
        fingerprint's own stream is a lie about the run. Unknown
        non-family stream names stay loud (the closed-set tripwire)."""
        if "streams" in mapping or set(mapping) != {"counts"}:
            raise RngError(
                "bank state must carry exactly the draw counters "
                "{'counts'} — a payload with 'streams' (or any other "
                "shape) is a cursor from the pre-epoch MT bank: the "
                "counter epoch cannot restore it; restart the run from "
                "its log (rng-1's recorded price)"
            )
        counts = mapping["counts"]
        if not isinstance(counts, Mapping):
            raise RngError("bank 'counts' must be a mapping")
        for name in counts:
            if name.startswith(WORLDGEN_PREFIX):
                raise RngError(
                    f"bank state carries the genesis-scoped stream {name!r} — "
                    "worldgen positions are re-derived at resume, never "
                    "restored"
                )
        for required in PHASE0_STREAMS:
            if required not in counts:
                raise RngError(
                    f"bank state lacks the always-registered stream "
                    f"{required!r} — an export without it is a lie"
                )
        for name, raw in counts.items():
            self._ensure(name)  # registers family streams lazily; loud otherwise
            if not isinstance(raw, int) or isinstance(raw, bool) or raw < 0:
                raise RngError(
                    f"bank count for {name!r} must be a non-negative int, "
                    f"got {raw!r}"
                )
            self._counts[name] = raw
