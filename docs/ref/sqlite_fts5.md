# SQLite FTS5 · `REFERENCES.md` §6 + §14 · public domain · phase 4 (retrieval candidates)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). SQLite is in the **public domain**
> — verified 2026-08-26 against <https://sqlite.org/copyright.html>
> ("SQLite Is Public Domain … All of the code and documentation in
> SQLite has been dedicated to the public domain by the authors").
> FTS5 is **not a separate library**: per `sqlite.org/fts5.html`
> §2.1, "As of version 3.9.0 (2015-10-14), FTS5 is included as part
> of the SQLite amalgamation" (enabled by the `SQLITE_ENABLE_FTS5`
> pre-processor symbol, on by default in the amalgamation configure
> script). Python's stdlib `sqlite3` ships that amalgamation —
> verified live: `sqlite3.sqlite_version == 3.53.1`; `CREATE
> VIRTUAL TABLE facts USING fts5(subject, body)`, `MATCH`, `bm25(t)`,
> `highlight()`, `snippet()`, `NEAR(...)`, `fts5vocab(...)` all
> execute in a plain `python3 -c` with **zero `pip` installs**. So
> FTS5 is D-012-compliant by construction — it is the zero-runtime-
> dep search layer of record (`TECH_NOTES.md` "Zero-dependency
> default: SQLite FTS5 keyword search over facts and lore"). Catalog
> §6 row reads "SQLite (+FTS5) | public domain | canon index
> (D-003); FTS5 keyword search over facts/lore — the zero-dependency
> search layer (rev v2)"; index §2 row had the matching "public
> domain" license + matching phase 4 — no drift this iteration.

**What it is.** FTS5 is an SQLite **virtual table module** that
builds an inverted full-text index (terms → doclists of `(rowid,
col, offset)` positions) over user-declared text columns, queryable
through the SQL `MATCH` operator with BM25 relevance ranking. The
canonical C source lives in `ext/fts5/` (reduced to `fts5.c`/
`fts5.h`; loadable-extension entry points `sqlite3_fts_init` /
`sqlite3_fts5_init`). FTS5 ships with Python's `sqlite3` module
— no `pip install`, no native wheel, no network; `import sqlite3`
is the entire integration. Verified live against sqlite version
3.53.1.

**Concrete mechanics.**

- **Schema** — `CREATE VIRTUAL TABLE <name> USING fts5(<col1>,
  <col2>, ...)` (the canonical "facts index" shape); no types/
  constraints/`PRIMARY KEY` allowed; the table has an implicit
  `rowid INTEGER PRIMARY KEY` for rowid-binding inserts.
  Tokenizer chosen at create time via `tokenize=`. SQL example:
  `CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
  INSERT INTO email(rowid, sender, title, body) VALUES(14, ...);`.
  Lifted into `core/storage.py` SQLite index — every projected
  fact row gets a row in an FTS5 virtual table; queries go
  through `MATCH`. The `facts` table name in `TECH_NOTES.md`
  is the literal table name FTS5 was always pointing at.
- **Query surface** — three equivalent forms: `WHERE email
  MATCH 'fts5'`, `WHERE email = 'fts5'`, or table-valued
  function `email('fts5')`; relevance order via `ORDER BY
  rank` (`rank` is a virtual column defaulting to `bm25()`).
  The TVF form also takes a rank override as its 2nd arg:
  `email(?, 'bm25(10.0, 5.0)')`. Lifted into `brief/assembler.
  py` — `WHERE facts MATCH ? ORDER BY bm25(facts, w0, w1)` is
  the canonical "find facts matching a query phrase, ranked by
  BM25 with per-column weights" query.
- **Tokenizers** (`tokenize=` option; first arg = name, rest =
  args):
  - `unicode61` (the **default**) — Unicode 6.1 letter/number
    categories (`L* N* Co`) are tokens, all else separators;
    case-folds per Unicode; **removes Latin diacritics** so
    `A`/`a`/`À`/`à`/`Â`/`â` are equivalent. Options:
    `remove_diacritics` `0|1|2` (default `1`), `categories`
    (default `L* N* Co`), `tokenchars`, `separators`. SQL
    example: `tokenize = "unicode61 remove_diacritics 0
    tokenchars '-_'"`. Lifted as the default tokenizer for
    multilingual content packs — `content/tavern_pack/`
    localized names (`azgaar_fmg.md` / `geonames.md`
    alternatenames) fold accents/case by default, so `café`/
    `Café`/`CAFÉ` match. Diacritics-off is opt-in
    (`remove_diacritics 0`), not the default.
  - `ascii` — non-ASCII always token chars, ASCII-only case-
    fold, no `remove_diacritics`. Not lifted (default to
    `unicode61` instead).
  - `porter` — **wrapper** tokenizer applying the Porter
    stemmer to another tokenizer's output (`tokenize = 'porter
    unicode61'`); lets `correction` match `corrected`/
    `correcting`. Lifted as an optional tokenizer for English-
    language content packs where stemming matters.
  - `trigram` — 3-char sliding-window tokens → general
    **substring** matching (not just whole-token). Lifted as
    an optional tokenizer for substring search over names/
    identifiers.
  - **custom tokenizers** via the `fts5_api` struct (methods
    `xCreateTokenizer()` / `xCreateTokenizer_v2()` /
    `xFindTokenizer()` / `xFindTokenizer_v2()`), obtained by
    calling the `fts5()` SQL function with a `sqlite3_bind_
    pointer(..., "fts5_api_ptr")` argument (C only — out of
    scope for our stdlib runtime, but it is the extension seam).
- **`bm25(<table>[, w0, w1, ...])`** — the canonical BM25
  ranking function; returns a real where **lower = better**
  (FTS5 multiplies by −1 so ascending `ORDER BY bm25(ft)`
  returns best first; `k1=1.2`, `b=0.75` hardcoded). Per-column
  weights are positional trailing args (`bm25(email, 10.0,
  5.0)` → sender weight 10, title 5, body defaults to 1.0);
  IDF uses total rows N and rows-containing-phrase n(q). SQL
  example: `SELECT * FROM email WHERE email MATCH ? ORDER BY
  bm25(email, 10.0, 5.0);`. Lifted into `brief/assembler.py`
  as the zero-dep baseline ranker — subject/title weighted
  above body, exactly the `bm25(email, 10.0, 5.0)` pattern.
- **`highlight(<table>, colIdx, before, after)`** — returns
  column text with each phrase match wrapped (`highlight(ft, 0,
  '<b>', '</b>')`; overlapping matches share a single bracket
  pair). Lifted into `render/` for snippet extraction — the
  chronicle scene card and the briefer's quoted evidence both
  need "show the matching span in context".
- **`snippet(<table>, colIdx, before, after, ellipsis,
  maxTokens)`** — auto-selects a short fragment maximizing
  distinct query terms (biased to column starts and to `.`/`:`
  boundaries); `maxTokens` ≤ 64. Lifted into `render/` as the
  off-the-shelf excerpter — `snippet(facts, col, '[', ']',
  '...', 32)` is the chronicle quote-card excerpter, no Python
  tokenization needed.
- **`fts5_get_locale(<table>, colIdx)` / `fts5_insttoken('q')`**
  — locale retrieval (needs `locale=1` table option) / mark a
  query as needing `xInstToken` data for efficient prefix-query
  custom APIs. Deferred (locale support is for non-Latin
  language packs; phase-0 tavern is English; phase-6 content
  packs may revisit).
- **Query operators** (BNF in `fts5.html` §3): `AND` / `OR` /
  `NOT` (precedence `NOT` > `AND` > `OR`, all case-sensitive
  keywords); **`NEAR(p1 p2 [, N])`** proximity (default `N=10`
  tokens between end of first phrase and start of last); `*`
  **prefix token** (`'thr*'`); `^` **initial-token** anchor
  (`'^one'`); `+` phrase concatenation (`'one + two +
  three'`); **column filters** `col:` / `{col1 col2}:` and
  negated `-col:`. SQL example: `SELECT rowid FROM facts WHERE
  facts MATCH 'NEAR(theft arson, 3)' ORDER BY rank; SELECT *
  FROM facts WHERE subject MATCH 'tavern';` (column-scoped
  MATCH). Lifted into the retrieval query DSL — the `NEAR`
  operator is the canonical "find facts where these words
  appear within N tokens of each other" pattern (e.g.
  "theft NEAR/3 arson" — find facts where these words appear
  within 3 tokens of each other).
- **Special INSERT commands** — `INSERT INTO ft(ft, ...)
  VALUES(...)` drives the index lifecycle:
  - `rebuild` — delete the entire FTS index then rebuild from
    the table's own contents (the schema-bump / tokenizer-change
    path). Lifted into the INV-1 path — a schema change or
    tokenizer swap requires a full `rebuild` (FTS5 has no
    in-place tokenizer migration). That is *exactly* INV-1's
    contract: the JSONL log is the only truth, the SQLite/
    FTS5 index is a `fold(log)` projection rebuilt on demand.
    So a schema bump = drop the virtual table, recreate,
    replay the log through `INSERT` — the expected, not
    exceptional, path.
  - `optimize` — merge **all** segment b-trees into one (min
    size, fastest queries; can be slow); `merge` with `N`
    pages does it incrementally (`merge −N` once then `merge
    +N` to completion; no-op detectable via `sqlite3_total_
    changes()` delta < 2). Lifted into the post-rebuild
    housekeeping — `optimize` once after `rebuild`.
  - `automerge` (default 4, max 16, 0=off) / `crisismerge`
    (default 16) / `usermerge` (default 4, min 2, max 16) /
    `deletemerge` (contentless-delete, default 10) — segment-
    merge thresholds. Defaults are good; do not lift the
    knobs.
  - `delete` / `delete-all` (external-content & contentless
    only) — `INSERT INTO ft(ft, rowid, a,b,c) VALUES('delete',
    14, $a,$b,$c)`. Negative for canonsim: brittle on
    contentless tables (the caller must resupply the *exact*
    original column values or the index corrupts — `fts5.html`
    §6.3 "results may be unpredictable"); for our rebuild-from-
    log model we prefer plain tables (with `%_content`) or a
    full `rebuild` over per-row `delete`.
  - `integrity-check` (raises `SQLITE_CORRUPT_VTAB` on
    mismatch); `rank` (set the table's default rank mapping,
    e.g. `VALUES('rank', 'bm25(10.0, 5.0)')`); `pgsz` (default
    4050); `secure-delete`; `insttoken`. Lifted as the
    diagnostic surface — `integrity-check` is the post-rebuild
    smoke test.
- **`fts5vocab` virtual table module** (ships with FTS5) —
  `CREATE VIRTUAL TABLE v USING fts5vocab(ft, 'row'|'col'|
  'instance')` exposes the raw index: `row` = `(term, doc,
  cnt)`; `col` adds `col`; `instance` adds `doc`(rowid)+`col`+
  `offset`. The introspection surface — not the hot path;
  useful for index health checks. Lifted as the introspection
  escape hatch — `fts5vocab` is the sanctioned way to inspect
  the index without touching shadow tables.
- **Shadow tables** (3–5 real tables created beside the
  virtual table; `fts5.html` §9: "They should not be accessed
  directly by the user"):
  - `%_data(id INTEGER PRIMARY KEY, block BLOB)` — bulk of the
    FTS index (structure record id=10, averages record id=1,
    segment b-tree leaves/doclist-index leaves/internal nodes).
  - `%_idx(segid, term, pgno, PRIMARY KEY(segid, term))
    WITHOUT ROWID` — segment b-tree index (the much smaller
    companion to `%_data`).
  - `%_config(k PRIMARY KEY, v) WITHOUT ROWID` — persistent
    options.
  - `%_docsize(id INTEGER PRIMARY KEY, sz BLOB)` — per-row
    column token counts (absent if `columnsize=0`).
  - `%_content(id INTEGER PRIMARY KEY, c0, c1, ...)` — the
    actual inserted text (absent for contentless / external-
    content tables).
  Lifted as a non-goal: never `SELECT` shadow tables directly;
  write to `facts` and read via `MATCH` + `bm25`/`highlight`,
  never `SELECT`ing the shadows directly (the docs forbid it
  and the varint/doclist layout is unstable across versions).
  `fts5vocab` is the sanctioned introspection escape hatch.
- **Segment b-trees** — the index is an ordered key-value
  store (keys = terms/term-prefixes, values = varint-packed
  doclists of `(rowid, col, offset)` triples) stored as a
  series of **immutable, leveled** segment b-trees; each
  commit adds one or more level-0 segments with tombstones for
  deletes; readers query every segment and merge, newer-wins.
  (This is *why* `automerge`/`optimize`/`merge` exist — to
  collapse the pile.) Lifted as the lesson: batch inserts in
  one transaction and `optimize` once at the end, not per
  event — segment b-trees accumulate under write-heavy loads
  and slow reads until `automerge`/`merge`/`optimize` collapse
  them.
- **Content-table variants** (`fts5.html` §4.4): plain,
  **contentless** (`content=''`, no `%_content`, deletes need
  the `delete` command), **contentless-delete** (tombstone
  variant), **external content** (`content='othertable'`,
  index on text stored elsewhere). Lifted as the choice rule:
  plain tables (with `%_content`) for our rebuild-from-log
  model — contentless tables are brittle on `delete`, and we
  want the rebuild path (not per-row delete) anyway.

**What we take.**

- The `CREATE VIRTUAL TABLE facts USING fts5(...)` schema as
  the chronicle facts index (D-003 canon index) — the phase-4
  retrieval layer's primary store: every projected fact row
  gets a row in an FTS5 virtual table; queries go through
  `MATCH`. `facts` is the literal table name in `TECH_NOTES.md`
  — FTS5 is the shape that name was always pointing at.
- The `bm25()` ranking function for relevance-ordered fact
  retrieval when assembling a brief — `brief/assembler.py`
  (per `letta.md` "block layout") needs ranked candidates;
  `ORDER BY bm25(facts, w0, w1)` with positional column weights
  is the zero-dep baseline ranker — subject/title weighted
  above body, exactly the `bm25(email, 10.0, 5.0)` pattern.
- The `highlight()` / `snippet()` for snippet extraction in
  `render/` — the chronicle scene card and the briefer's quoted
  evidence both need "show the matching span in context";
  `snippet(facts, col, '[', ']', '...', 32)` is the off-the-
  shelf excerpter, no Python tokenization.
- The `unicode61` default tokenizer for multilingual content
  packs — `content/tavern_pack/` localized names (`azgaar_fmg.
  md` / `geonames.md` alternatenames) fold accents/case by
  default, so `café`/`Café`/`CAFÉ` match. Diacritics-off is
  opt-in, not the default.
- The `NEAR` operator for proximity queries — the canonical
  "find facts where these words appear within N tokens of each
  other" pattern (e.g. "theft NEAR/3 arson" — find facts where
  these words appear within 3 tokens of each other).
- The `rebuild` command as the INV-1 mechanism — a schema change
  or tokenizer swap requires a full `rebuild` (FTS5 has no
  in-place tokenizer migration). That is *exactly* INV-1's
  contract: the JSONL log is the only truth, the SQLite/FTS5
  index is a `fold(log)` projection rebuilt on demand. So a
  schema bump = drop the virtual table, recreate, replay the
  log through `INSERT` — the expected, not exceptional, path.

**What we adapt.**

- FTS5 is keyword-only, not semantic — phase-4 "find similar
  facts" needs vectors. BM25 matches shared *tokens*, not
  meaning; a paraphrased fact with no term overlap scores 0.
  The retrieval layer therefore composes FTS5 (keyword/phrase
  + `NEAR` proximity, the cheap, always-on path) with **sqlite-
  vec** (`docs/ref/sqlite_vec.md`, ref-11-c) for embedding
  similarity on static lore — the hybrid the catalog already
  encodes (`REFERENCES.md` §6 "FTS5 … zero-dependency search
  layer" + §14 "sqlite-vec … static-lore RAG (phase 4)"). FTS5
  alone is the floor, not the ceiling.
- The index is rebuildable, never the truth — INV-1 path. A
  schema change or tokenizer swap requires a full `rebuild`
  (FTS5 has no in-place tokenizer migration). That is *exactly*
  INV-1's contract: the JSONL log is the only truth, the
  SQLite/FTS5 index is a `fold(log)` projection rebuilt on
  demand. So a schema bump = drop the virtual table, recreate,
  replay the log through `INSERT` — the expected, not
  exceptional, path.
- The shadow tables are storage detail, not query surface.
  `%_data`/`%_idx`/`%_config`/`%_docsize`/`%_content` are
  managed by the virtual-table module; canonsim writes to
  `facts` and reads via `MATCH` + `bm25`/`highlight`, never
  `SELECT`ing the shadows directly (the docs forbid it and the
  varint/doclist layout is unstable across versions).
  `fts5vocab` is the sanctioned introspection escape hatch.

**What inspires us.**

- BM25 is the canonical keyword-relevance baseline — anything
  semantic we build in phase 4 is measured against it (and a
  cross-encoder reranker, per `TECH_NOTES.md` §1, ranks *on top
  of* candidates FTS5/vec retrieve).
- The inverted index as a fold-of-the-log projection — FTS5's
  own `rebuild` command is the mechanism that makes "the index
  is rebuildable" more than a slogan; it is the proof that our
  INV-1 split (log = truth, SQLite = index) has a first-class,
  supported refresh path rather than a hand-rolled reindex.

**Strengths.**

- Ships with Python's `sqlite3` — zero runtime deps, D-012-
  compliant by construction. No `pip install`, no native wheel,
  no network; `import sqlite3` is the entire integration.
  Verified live (3.53.1, FTS5 on by default).
- `bm25()` is the canonical keyword-relevance baseline — battle-
  tested in production search; per-column positional weights give
  us subject-vs-body weighting for free.
- `unicode61` handles Unicode + diacritics by default — fits the
  multilingual content packs (`geonames.md` alternatenames,
  localized tavern names) with no extra config.
- The virtual table abstracts the index. Write `INSERT`, read
  `MATCH`; the shadow tables, segment b-trees, and doclists are
  invisible — and `rebuild`/`optimize`/`merge` give explicit
  control when we want it.
- `NEAR`, prefix `*`, column filters, `fts5vocab` cover the full
  keyword-retrieval surface (proximity, autocomplete, scoped
  search, index health) inside one stdlib module.

**Weaknesses.**

- Keyword-only — no semantic similarity. Phase-4 "find similar
  facts" / paraphrase recall needs sqlite-vec embeddings *in
  addition* to FTS5; FTS5 is the always-on keyword floor, not the
  semantic layer.
- Ranking customization is `bm25` + a custom C function. For
  blended relevance (recency × authority × BM25, the briefer's
  real need) we layer a **Python reranker** over FTS5 candidates
  — there is no built-in recency/authority term to toggle.
- A tokenizer/schema change forces a full `rebuild`. Tokenizer
  choice is fixed at `CREATE VIRTUAL TABLE` time; switching
  `unicode61` → `porter` → `trigram` later = drop + recreate +
  replay. This is the INV-1-expected rebuild path, but it is still
  a full reindex, not incremental — plan the tokenizer at design
  time.
- Segment b-trees accumulate under write-heavy loads. Many small
  commits grow the level-0 pile and slow reads until `automerge`/
  `merge`/`optimize` collapse them; for a fold-the-log rebuild
  we should batch inserts in one transaction and `optimize` once
  at the end, not per event.
- `delete` on contentless tables is brittle — the caller must
  resupply the *exact* original column values or the index
  corrupts (`fts5.html` §6.3 "results may be unpredictable").
  For our rebuild-from-log model we prefer plain tables (with
  `%_content`) or a full `rebuild` over per-row `delete`.

**Verdict.** Phase-4 retrieval-baseline reference (D-012 + D-003)
— the zero-dependency keyword-search layer that underpins `brief/`
candidate retrieval; FTS5 alone is the floor, sqlite-vec is the
semantic ceiling, and `rebuild` is the INV-1 mechanism that keeps
the index a rebuildable projection of the JSONL log rather than a
second source of truth. Public domain license (verified 2026-08-
26 from <https://sqlite.org/copyright.html> — "SQLite Is Public
Domain") — zero friction at intake, and ships inside Python's
`sqlite3` stdlib module so it's D-012-compliant by construction.
The "BM25 is the canonical keyword-relevance baseline" lesson is
the inspiration: anything semantic we build in phase 4 is measured
against it. The "inverted index as a fold-of-the-log projection"
lesson (FTS5's own `rebuild` command) is the proof that our INV-1
split (log = truth, SQLite = index) has a first-class, supported
refresh path.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
