"""The retrieval ladder (retr-1, phase 4, STORE-1; `phases.md` §4 the
architecture owner — the re-ranker formula and the precedence chain;
`docs/LEGEND_SPEC.md` §4/§5 fix the two contract points the ladder must
honor). A pure READ-SIDE service over (pack, events): an in-memory,
fully rebuildable SQLite index (INV-1 — a derived store, never canon;
"rebuild is the mechanism: drop, replay, re-index") plus a
deterministic query ranker. Nothing in the runtime calls it — the
consumer is the mediator's keyword query (mode B, BRIEF_SPEC §9's
deferral); the committed block is declarative-only, so the corpus
price is zero by construction (the 10-seed witness in
tests/test_retrieval.py).

The ladder (phases.md §4's precedence chain, L12 — a rung failure
never breaks the ladder, only degrades it):

1. **FTS5 BM25 always runs first** — the zero-dependency default
   (`sqlite3` is stdlib; the unicode61 tokenizer splits underscored
   dry tokens into words, so a `knows` token is word-retrievable as
   its compound words — no normalization pass, the tokens' own
   shape). Probed at build; a SQLite build lacking FTS5 falls to the
   pure-Python keyword floor (any-term token containment, no bm25
   signal — γ contributes 0), which keeps matching alive.
2. **The vec rung, static lore only** — the sqlite-vec extension is
   PROBED (the pip loader, then the plain extension name; its absence
   is normal operation, never an error — D-012 holds: no runtime
   dependency, the extension is optional environment capability). When
   the probe succeeds AND the pack ships lore vectors, a `vec0` kNN
   table answers `MATCH … ORDER BY distance LIMIT k` (cosine distance,
   `cos = 1 − distance`). When the probe fails but vectors exist, the
   pure-Python cosine scan computes the SAME top-k (rung equivalence:
   the scan is the semantic definition — ties by rowid; the kNN is an
   acceleration that must preserve it, verified wherever the extension
   exists). No vectors, or no query vector → the rung is off.
3. **Never an empty result from a rung failure**: the candidate set is
   the UNION of FTS5 matches and the cosine top-k; whichever rungs are
   available contribute. With vectors live the top-k nearest always
   ride (the RAG shape — a query is never empty-handed). Without them,
   a query that matches nothing returns the honest empty — that is an
   answer, not a ladder failure.

The hard boundary (VISION §5, TECH_NOTES §6): dynamic world state is
served as SQL + `known_by`, NEVER as vectors. Structurally: vectors
live only on lore rows (the pack's `retrieval.vectors` maps lore ids),
and FACT candidates enter the index only through the knowledge fold —
the `knower` query parameter IS the known_by filter. `knower=None`
retrieves lore only; no fact row can ever be reached without naming
the knower whose memory holds it. RAG never touches dynamic facts.

The deterministic re-ranker (coefficients are pack data,
`rules.json::retrieval`, lint `core/pack.py::_retrieval`):
`score = α·recency + β·authority + γ·bm25 + δ·cosine` over the union,
sorted descending, ties by construction order (rowid: lore in pack
declaration order, then facts in event order — INV-2). Per-kind signal
sources (the formula uniform, the sources honest per kind): recency is
a fact-side signal (age at the build snapshot, `1/(1+tick−at)`; static
lore is timeless — 0); authority is evidential quality (authored lore
1.0; a fact's fidelity rank in the pack's chain — an exact sighting
outranks a vague murmur, a told record decays with its fidelity);
bm25 is the normalized keyword score (`goodness/(1+goodness)`,
goodness = −bm25 ≥ 0); cosine is the raw similarity of the top-k only
(δ·0 outside it — rung equivalence preserved).

The two LEGEND_SPEC contract points, formalized deterministically:

- **The stale law (§5)**: the build consults `stale_reflections` — a
  reflection whose provenance does not resolve within the given event
  universe (the derived-store-after-scavenge shape; impossible on a
  whole log, INV-1) has its minted record EXCLUDED from the index.
  Serving a stale reflection as fact is the derived-store lie.
- **The source-outranks law (§4)**: when a query retrieves a
  reflection AND one or more of its provenance-source records, the
  sources outrank the reflection's recency — the reflection is ordered
  below every retrieved source of its own. The spec words it as the
  contradiction case ("the source record outranks the reflection's
  recency"); a deterministic ranker cannot judge semantic
  contradiction, so it enforces the precedence that makes the
  contradiction harmless: the derived view never shadows its own
  evidence in a shared candidate list (the expansion law's ranking
  twin — the source is always queryable, the reflection never a
  replacement).

Determinism (INV-2): no RNG anywhere; the union is iterated in rowid
order; the cosine top-k tie-breaks by rowid; the sort is stable over
construction order; no set-order iteration on any ranking path. The
floats are same-environment deterministic (TECH_NOTES §4 — the
byte-identity guarantee's standing scope)."""

from __future__ import annotations

import json
import math
import re
import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.reflection import stale_reflections

if TYPE_CHECKING:  # pack + events are duck-typed — no runtime cycle
    from core.log import EventRecord
    from core.pack import Pack

__all__ = [
    "RETRIEVAL_BLOCK_KEYS",
    "Retrieved",
    "RetrievalIndex",
    "cosine_sim",
]

RETRIEVAL_BLOCK_KEYS: Final = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "knn_k",
    "vectors",
    "notes",
)
"""The closed `rules.json::retrieval` key set (an unknown key is a lint
error, never a silent ignore): the four re-ranker coefficients
(recency, authority, bm25, cosine), the vec rung's kNN limit, the
optional static-lore vector table (lore id → embedding), prose."""

_TOKEN_RE: Final = re.compile(r"[^\W_]+", re.UNICODE)
"""The floor tokenizer (FTS5's unicode61 approximation: alphanumeric
runs, underscore a separator — the dry tokens' own word shape)."""

_KIND_LORE: Final = "lore"
_KIND_FACT: Final = "fact"


@dataclass(frozen=True, slots=True)
class _Row:
    """One indexed candidate (the corpus in construction order — lore
    rows first in pack declaration order, then fact rows in event
    order; rowid = position + 1, the INV-2 tie-break)."""

    kind: str
    ref: str
    text: str
    knower: str | None  # facts only — lore is knower-free
    source: str | None  # the minting event id, facts only
    at: int | None  # the learning tick, facts only
    channel: str | None
    fidelity: str | None


@dataclass(frozen=True, slots=True)
class Retrieved:
    """One ranked retrieval result: the row plus its final score. `ref`
    is the lore entry id (lore) or the `knows` token (fact) — the dry
    address; `source` is the record's minting event id (facts) — the
    demand handle every consumer (the expansion law) reads."""

    kind: str
    ref: str
    text: str
    score: float
    knower: str | None = None
    source: str | None = None
    at: int | None = None
    channel: str | None = None
    fidelity: str | None = None


def cosine_sim(a: Sequence[float], b: Sequence[float]) -> float:
    """The pure-Python cosine similarity (the vec rung's fallback
    engine — the scan that defines the rung's semantics). A zero
    vector has no direction: 0.0, the honest neutral, never an error.
    Deterministic; `zip(strict=True)` — a dimension mismatch is the
    caller's bug, loud by construction."""
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _tokens(text: str) -> list[str]:
    """The alphanumeric token runs, casefolded (the floor's word view)."""
    return [match.group(0).casefold() for match in _TOKEN_RE.finditer(text)]


def _match_string(query: str) -> str:
    """The safe FTS5 MATCH expression: every whitespace term quoted
    (inner quotes doubled — FTS5 syntax can never crash the ladder),
    terms without tokens dropped, OR-joined — retrieval is recall
    first, the re-ranker sorts (bm25 sums the per-term contributions a
    row actually matched)."""
    terms = [term for term in query.split() if _tokens(term)]
    return " OR ".join(
        f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms
    )


def _fts5_available(db: sqlite3.Connection) -> bool:
    """The FTS5 probe: one throwaway virtual table (a build lacking the
    module answers loudly here, once — never per query)."""
    try:
        db.execute("CREATE VIRTUAL TABLE _fts_probe USING fts5(x)")
    except sqlite3.Error:
        return False
    db.execute("DROP TABLE _fts_probe")
    return True


def _probe_vec(db: sqlite3.Connection) -> bool:
    """The sqlite-vec probe (the ref intake rule): the optional pip
    loader first, then the plain extension name. Failure is normal
    operation — the scan rung answers instead (D-012: the extension is
    environmental capability, probed, never a dependency)."""
    try:
        db.enable_load_extension(True)
    except (AttributeError, sqlite3.Error):
        return False
    try:
        try:
            import sqlite_vec  # type: ignore[import-not-found]

            sqlite_vec.load(db)
            return True
        except ImportError:
            db.load_extension("vec0")
            return True
    except (sqlite3.Error, OSError):
        return False
    finally:
        try:
            db.enable_load_extension(False)
        except (AttributeError, sqlite3.Error):
            pass


def _provenance_map(
    pack: "Pack", events: Sequence["EventRecord"]
) -> dict[str, tuple[str, ...]]:
    """The reflection-event id → provenance ids map (the
    source-precedence law's lookup; a malformed outcome is validation's
    loud business — skipped here exactly as the stale fold skips it)."""
    config: Mapping[str, Any] | None = pack.rules.get("reflection")
    if config is None:
        return {}
    event_type = config["event"]
    out: dict[str, tuple[str, ...]] = {}
    for event in events:
        if event.type != event_type:
            continue
        provenance = event.outcome.get("provenance")
        if isinstance(provenance, list) and all(
            isinstance(item, str) for item in provenance
        ):
            out[event.id] = tuple(provenance)
    return out


def _apply_source_precedence(
    ranked: list[Retrieved],
    provenance: Mapping[str, tuple[str, ...]],
) -> list[Retrieved]:
    """LEGEND_SPEC §4's contract, formalized: every reflection candidate
    orders below ALL of its retrieved provenance-source candidates —
    the derived view never shadows its own evidence (the source
    outranks the reflection's recency; on contradiction the ground
    truth wins). Deterministic: reflections visited in rowid order; a
    demotion moves the reflection to just after its lowest-ranked
    retrieved source. Identity-based throughout — duplicate rows are
    legal evidence (the ladder never dedups: the consumer reads the
    learning history's addresses)."""
    reflections = [item for item in ranked if item.source in provenance]
    for reflection in reflections:
        sources_here = [
            item
            for item in ranked
            if item is not reflection
            and item.source in provenance[reflection.source or ""]
        ]
        if not sources_here:
            continue
        last = sources_here[-1]
        reflection_at = next(
            i for i, item in enumerate(ranked) if item is reflection
        )
        last_at = next(i for i, item in enumerate(ranked) if item is last)
        if reflection_at < last_at:
            ranked.pop(reflection_at)
            last_at = next(i for i, item in enumerate(ranked) if item is last)
            ranked.insert(last_at + 1, reflection)
    return ranked


def _create_vec_table(
    db: sqlite3.Connection,
    vectors: Mapping[int, tuple[float, ...]],
) -> bool:
    """Create and fill the vec0 kNN table (dimension from the
    uniform-linted vectors; cosine distance — `cos = 1 − d`). Returns
    the capability: a creation failure degrades to the scan rung —
    never a break."""
    dim = len(next(iter(vectors.values())))
    try:
        db.execute(
            f"CREATE VIRTUAL TABLE vec_index USING "
            f"vec0(embedding float[{dim}] distance_metric=cosine)"
        )
        db.executemany(
            "INSERT INTO vec_index(rowid, embedding) VALUES (?, ?)",
            [(rowid, json.dumps(list(vec))) for rowid, vec in vectors.items()],
        )
    except sqlite3.Error:
        return False
    return True


class RetrievalIndex:
    """The rebuildable retrieval index over (pack, events): static lore
    (pack data, optionally vectorized) plus every knowledge record the
    log holds (the known_by fold — facts are per-knower by
    construction). Built once, queried many times; `build` returns None
    for a pack without a `retrieval` block (the pack's own declaration
    is the gate, INV-3 — the ladder's DORMANT law: nothing in the
    runtime queries, the mediator's keyword query is the consumer)."""

    __slots__ = (
        "_alpha",
        "_beta",
        "_gamma",
        "_delta",
        "_knn_k",
        "_rows",
        "_db",
        "_fts_ok",
        "_vectors",
        "_vec_sql",
        "_provenance",
        "_authority",
        "_tick",
        "_closed",
    )

    def __init__(self) -> None:
        raise NotImplementedError(
            "use RetrievalIndex.build(pack, events) — the index is a "
            "derived store, never hand-assembled"
        )

    @classmethod
    def build(
        cls,
        pack: "Pack",
        events: Sequence["EventRecord"],
    ) -> "RetrievalIndex | None":
        """Index (pack, events) and return the queryable ladder — or
        None when the pack declares no `retrieval` block. Pure: reads
        its inputs, writes nothing (INV-1); the stale fold (LEGEND_SPEC
        §5) is consulted HERE — a stale reflection's minted records are
        excluded from the corpus at insert, so no query can ever serve
        them."""
        config: Mapping[str, Any] | None = pack.rules.get("retrieval")
        if config is None:
            return None
        index = cls.__new__(cls)
        index._alpha = float(config["alpha"])
        index._beta = float(config["beta"])
        index._gamma = float(config["gamma"])
        index._delta = float(config["delta"])
        index._knn_k = int(config["knn_k"])
        index._closed = False
        index._tick = events[-1].t if events else 0
        index._provenance = _provenance_map(pack, events)
        stale = stale_reflections(pack, events)
        chain = pack.rules["knowledge"]["fidelity_chain"]
        span = max(len(chain) - 1, 1)
        index._authority = {
            fidelity: (len(chain) - 1 - rank) / span
            for rank, fidelity in enumerate(chain)
        }

        rows: list[_Row] = []
        for entry in pack.rules["brief"]["lore"]:  # pack declaration order
            rows.append(
                _Row(
                    kind=_KIND_LORE,
                    ref=str(entry["id"]),
                    text=str(entry["text"]),
                    knower=None,
                    source=None,
                    at=None,
                    channel=None,
                    fidelity=None,
                )
            )
        for event in events:  # event order — construction order
            if event.id in stale:
                continue  # the stale law: a stale reflection never serves
            for record in event.knowledge:  # acquisition order
                rows.append(
                    _Row(
                        kind=_KIND_FACT,
                        ref=record.knows,
                        text=record.knows,
                        knower=record.who,
                        source=record.source,
                        at=record.at,
                        channel=record.channel,
                        fidelity=record.fidelity,
                    )
                )
        index._rows = tuple(rows)

        vectors: Mapping[str, Sequence[float]] = config.get("vectors") or {}
        index._vectors = {
            rowid: tuple(float(x) for x in vectors[row.ref])
            for rowid, row in enumerate(rows, start=1)
            if row.kind == _KIND_LORE and row.ref in vectors
        }
        db = sqlite3.connect(":memory:")
        index._db = db
        index._fts_ok = _fts5_available(db)
        index._vec_sql = False
        if index._fts_ok:
            db.execute("CREATE VIRTUAL TABLE corpus USING fts5(text)")
            db.executemany(
                "INSERT INTO corpus(rowid, text) VALUES (?, ?)",
                [(rowid, row.text) for rowid, row in enumerate(rows, start=1)],
            )
        if index._vectors and _probe_vec(db):
            index._vec_sql = _create_vec_table(db, index._vectors)
        return index

    # -- the query ------------------------------------------------------

    def query(
        self,
        text: str,
        *,
        knower: str | None = None,
        vector: Sequence[float] | None = None,
    ) -> tuple[Retrieved, ...]:
        """Retrieve ranked candidates for `text`. `knower` IS the
        known_by filter: None retrieves lore only (facts are reachable
        solely through a knower's own memory — the hard boundary,
        structurally unbreakable); a knower id retrieves lore plus that
        knower's records. `vector` (the caller's embedded query — the
        embedder never enters the runtime) engages the cosine rung on a
        vectorized corpus; a dimension or finiteness mismatch is a loud
        caller bug, never a silent skip."""
        self._ensure_open()
        bm25_of = self._bm25_candidates(text, knower)
        cosine_of = self._cosine_candidates(vector)
        scored: list[Retrieved] = []
        for rowid in sorted(set(bm25_of) | set(cosine_of)):
            row = self._rows[rowid - 1]
            recency = (
                0.0 if row.at is None else 1.0 / (1 + self._tick - row.at)
            )
            authority = (
                1.0
                if row.fidelity is None
                else self._authority.get(row.fidelity, 0.0)
            )
            score = (
                self._alpha * recency
                + self._beta * authority
                + self._gamma * bm25_of.get(rowid, 0.0)
                + self._delta * cosine_of.get(rowid, 0.0)
            )
            scored.append(
                Retrieved(
                    kind=row.kind,
                    ref=row.ref,
                    text=row.text,
                    score=score,
                    knower=row.knower,
                    source=row.source,
                    at=row.at,
                    channel=row.channel,
                    fidelity=row.fidelity,
                )
            )
        scored.sort(key=lambda item: item.score, reverse=True)  # stable
        return tuple(_apply_source_precedence(scored, self._provenance))

    @property
    def vec_loaded(self) -> bool:
        """Whether the sqlite-vec extension answered the probe AND the
        kNN table lives (the capability flag — the scan rung answers
        either way, rung equivalence)."""
        return self._vec_sql

    def close(self) -> None:
        """Release the in-memory SQLite handle (the derived store dies
        whole; the canon it was built from is untouched)."""
        self._ensure_open()
        self._closed = True
        self._db.close()

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("the retrieval index is closed")

    # -- the rungs ------------------------------------------------------

    def _bm25_candidates(
        self, text: str, knower: str | None
    ) -> dict[int, float]:
        """Rung 1 (and its floor): the FTS5 matches for the query terms,
        knower-filtered (facts only the named knower's; lore always),
        normalized `goodness/(1+goodness)` with goodness = −bm25 ≥ 0
        (FTS5 scores better matches more negative). The floor (no FTS5
        in the environment): any-term token containment, no bm25 signal
        — γ·0, the L12 degradation, never a break."""
        match = _match_string(text)
        if not match:
            return {}
        raw: dict[int, float] = {}
        if self._fts_ok:
            for rowid, value in self._db.execute(
                "SELECT rowid, bm25(corpus) FROM corpus WHERE corpus MATCH ?",
                (match,),
            ):
                raw[int(rowid)] = float(value)
        else:
            terms = frozenset(_tokens(text))
            for rowid, row in enumerate(self._rows, start=1):
                if terms & frozenset(_tokens(row.text)):
                    raw[rowid] = 0.0
        out: dict[int, float] = {}
        for rowid, value in raw.items():
            row = self._rows[rowid - 1]
            if row.knower is None or (knower is not None and row.knower == knower):
                goodness = max(0.0, -value)
                out[rowid] = goodness / (1.0 + goodness)
        return out

    def _cosine_candidates(
        self, vector: Sequence[float] | None
    ) -> dict[int, float]:
        """Rung 2: the cosine top-k over the vectorized lore rows — the
        kNN path when the extension probed, the pure-Python scan
        otherwise (rung equivalence: the same top-k, ties by rowid).
        Never returns a fact row — vectors live on lore only (the hard
        boundary)."""
        if not self._vectors or vector is None:
            return {}
        values = [float(x) for x in vector]
        if not all(math.isfinite(x) for x in values):
            raise ValueError("the query vector carries non-finite values")
        dim = len(next(iter(self._vectors.values())))
        if len(values) != dim:
            raise ValueError(
                f"the query vector is {len(values)}-d; the pack's lore "
                f"vectors are {dim}-d (one embedder must produce both)"
            )
        if self._vec_sql:
            try:
                rows = self._db.execute(
                    "SELECT rowid, distance FROM vec_index "
                    "WHERE embedding MATCH ? ORDER BY distance LIMIT ?",
                    (json.dumps(values), self._knn_k),
                ).fetchall()
                return {int(rowid): 1.0 - float(distance) for rowid, distance in rows}
            except sqlite3.Error:  # never break — the scan answers
                pass
        scored = sorted(
            (
                (rowid, cosine_sim(vec, values))
                for rowid, vec in self._vectors.items()
            ),
            key=lambda pair: (-pair[1], pair[0]),
        )
        return {rowid: cos for rowid, cos in scored[: self._knn_k]}
