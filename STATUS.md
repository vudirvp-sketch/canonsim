# STATUS — canonsim

Iteration: 0r (owner-requested: ref-10 + ref-11 6-batch — ECS scheduling entt + Bevy, event-sourcing EventStore, storage-layer candidates SQLite FTS5 + DuckDB + sqlite-vec, mostly positive on architecture/shape, some negative on runtime dependencies [D-012]) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0r is the **ref-10 + ref-11 6-batch iteration** — six
open-licensed ECS scheduling + event-sourcing + storage-layer
pattern-only references (per `REFERENCES.md` §6+§7+§14 — pattern
lifting permitted, port the shape not the syntax per §0.7 /
D-015), each in its own per-ref file:
`docs/ref/entt.md` (359 — MIT; C++ ECS sparse-set blueprint:
`basic_sparse_set<Entity, Allocator>` dual-array (`sparse`
page-ptr + `packed` entity) + `deletion_policy` swap_and_pop/
in_place/swap_only enum + `basic_storage<Type, Entity,
Allocator>` paged payload (INV-1 inversion: derived from JSONL
log, not authoritative; `emplace`/`patch` are events) +
`basic_registry<Entity, Allocator>` with `pools` keyed by
`type_hash<Type>::value()` + `basic_view<get_t<Get...>,
exclude_t<Exclude...>>` smallest-pool-leads heuristic +
`basic_group` eagerly maintained intersection (negative:
invalidates on structural change — not adopted; queue
discipline sidesteps) + `basic_organizer<Registry>` task DAG
(`vertex_data{ro_count, rw_count, callback, dependency}` +
`graph()` adjacency list; resource extraction via `internal::
unpack_type` splits function parameters into ro/rw lists;
lifted into `sim/systems/__init__.py` system registration with
declared `reads`/`writes` — INV-3 fix: declared as data from
JSON packs, Python has no const for signature inference) +
`sigh`/`sink`/`connection` RAII hooks + `basic_sigh_mixin`
auto-publishes `construction`/`update`/`destruction` (lifted
into `sim/events.py`: JSONL log IS the signal stream) +
`entt_traits<Entity>` `entity_mask`/`version_mask` id+version
packing (lifted into `core/ids.py`) + `meta_type`/
`meta_factory<T>` runtime reflection (lifted into `content/
packs/*.py` loader — only the registration shape, not the
verbose string-keyed API; `dataclasses` is more ergonomic);
explicitly negative on C++ template-heavy API (D-012 fix: port
to Python plain classes) + mutable in-place storage (INV-1
fix: events-only derived state) + `group` invalidates on
structural change (queue discipline sidesteps, `view` only is
sufficient) + `meta` verbose/string-keyed (only registration
shape lifted); 'storage is the unit; queries are zero-allocation
views over storage' + 'generation bits baked into the
identifier make recycling free' lessons shape `core/store.py`
+ `core/ids.py`; MIT (verified 2026-08-26 from repo LICENSE
header "The MIT License (MIT) — Copyright (c) 2017-2026
Michele Caini, author of EnTT") — no friction at intake; catalog
§7 row reads "entt | MIT | C++ ECS — component / system design";
index §2 row had matching MIT license — no drift this iteration),
`docs/ref/bevy.md` (469 — dual `MIT OR Apache-2.0`; Rust ECS +
scheduler: `World` struct owning `entities` + `storages`
(Table columnar + SparseSet triple `dense`/`indices`/`sparse`)
+ `Component` trait with `const STORAGE_TYPE: StorageType`
(Table/SparseSet enum) + `Resource` singleton (Component on
hidden entity, accessed via `Res<'w, T>` w/ `value: &'w T` +
`ticks: ComponentTicksRef` or `ResMut<'w, T>` w/ `value: &'w
mut T` + `ticks: ComponentTicksMut`) + `Query<'w, 's, D, F>`
with filters `With<T>`/`Without<T>`/`Or<T>`/`Added<T>`/
`Changed<T>` (zero-sized marker structs; `unsafe trait
QueryFilter: WorldQuery { const IS_ARCHETYPAL: bool; unsafe
fn filter_fetch(...) -> bool; }`) + `Schedule` + `SystemSet`
+ `ScheduleLabel` with ordering combinators `.before`/
`.after`/`.chain`/`.in_set`/`.ambiguous_with`; `ScheduleGraph`
carries `ambiguous_with: UnGraph<NodeId>` + `ambiguous_with_
all: HashSet<NodeId>` — the ambiguity-detection edge set;
`SystemParam::init_access` registers a `FilteredAccessSet` per
system; the `Schedule::initialize` build phase cross-checks
every pair and errors at build time on conflicting access
without declared ordering — the access-conflict detection that
guarantees an event-sourced fold has a total, deterministic
order + **`Messages<M>` double-buffered ring** (the catalog
brief calls "`Events<T>` double buffer" — Bevy has RENAMED
`Events<T>` → `Messages<M>` in v0.20-dev; `Event` trait now
means observer-triggered immediate events via `World::
trigger`; the double-buffered ring pattern is unchanged) —
`pub struct Messages<M: Message> { messages_a, messages_b,
message_count: usize, }`; methods `write(M) -> MessageId<M>`,
`write_batch`, `write_default`, `get_cursor`,
`get_cursor_current`, `update()` (swap A↔B + clear B + reset
`start_message_count`), `update_drain`,
`oldest_message_count`; writer side `MessageWriter<'w, M> {
messages: ResMut<'w, Messages<M>> }`; reader side
`MessageReader<'w, 's, M> { reader: Local<'s, MessageCursor<M>>,
messages: Res<'w, Messages<M>> }` with `read`, `read_with_id`,
`par_read`, `len`, `is_empty`, `clear`; cursor `pub struct
MessageCursor<M> { last_message_count: usize, _marker:
PhantomData<M>, }`; lifted into `core/queue.py` — the shape
maps 1:1 onto canonsim's `(tick, sub_order, actor_id)` queue:
the append-only JSONL log IS the producer's buffer B; the
per-tick `update()` swap is the tick boundary; per-system
`Local<'s, MessageCursor<M>>` becomes a per-system integer-tick
cursor; the reader/writer asymmetry (`Res` shared read vs
`ResMut` exclusive write) is exactly what makes a fold
deterministic + `Command` trait with `type Out: CommandOutput;
fn apply(self, world: &mut World) -> Self::Out;` + blanket
impl for closures; `CommandQueue` with `bytes: Vec<MaybeUninit
<u8>>`; `Commands<'w, 's>` with `queue: Deferred<'s,
CommandQueue>`; adapted into `cli/` Intent → Event validation
front-door — there is NO `&mut World` for systems to touch
(INV-1 forbids direct state mutation), so `Command::apply`
becomes "serialize the command to event JSON, append to JSONL
log, advance tick"; the deferred-buffer shape survives, the
deferred-target changes from mutable World to append-only
event log; `schemas/event.schema.json` becomes the type-tag +
shape validator that `CommandMeta`'s vtable fn-pointer used to
be + `App` builder + `Plugin` trait with `build(&self, app:
&mut App)` + blanket impl for closures + `States` trait `pub
trait States: 'static + Send + Sync + Clone + PartialEq + Eq
+ Hash + Debug { const DEPENDENCY_DEPTH: usize = 1; }` +
`State<S: States>` resource + `NextState<S>` enum `Unchanged`
/ `Pending(S)` / `PendingIfDifferent(S)` with `set(S)` and
`set_if_different(S)`; `StateTransition` schedule between
`PreUpdate` and `RunFixedMainLoop`, firing `OnEnter(variant)`
/ `OnExit(variant)` schedules; main schedule `Main`:
`Startup → First → PreUpdate → StateTransition →
RunFixedMainLoop → Update → SpawnScene → PostUpdate → Last`;
lifted into `sim/systems/` phase control — the deferred
`set`-then-apply-at-schedule-point shape is the correct way
for an event-sourced sim to switch scenarios mid-fold: queue
a transition event, apply at the tick boundary, fire enter/
exit hooks in deterministic order + `Entity` struct `index:
EntityIndex(NonMaxU32)`, `generation: EntityGeneration(u32)`
packs to u64 — same as entt's `entity` id+version packing,
both inherit the same canonical shape, canonsim lifts once
into `core/ids.py`; explicitly negative on Rust-only runtime
(D-012 fix: patterns only, never vendored) + in-place mutable
`ResMut<T>` + `Query<&mut T>` (INV-1 fix: lift the deferred-
queue shape, not the `&mut World` target) + trait/derive
macro type-safety (lifted → Python dataclasses + JSON Schema,
type-safety degrades to runtime checks) + SparseSet/Table
cache-line layout (pointless in Python — `dict` overhead
dominates) + `async_executor`/`multi_threaded` not relevant to
phase-0 single-threaded sim (a reproducible fold must be
serial); 'separate the write-half from the read-half' lesson
(Messages<M> asymmetry = JSONL log vs derived-state split) +
'declarative ordering beats imperative calls' lesson (Schedule
graph + `ambiguous_with` build-time conflict detection) shape
`core/queue.py` + `sim/systems/__init__.py`; dual `MIT OR
Apache-2.0` (verified 2026-08-26 from root Cargo.toml `license`
field + LICENSE-MIT + LICENSE-APACHE files + README §License —
the canonical dual-license form) — zero friction at intake;
catalog §7 row reads "Bevy | MIT / Apache-2.0 | Rust ECS
scheduling model"; index §2 row had matching dual license — no
drift this iteration; note on naming: in current `main`
(v0.20-dev) Bevy has RENAMED `Events<T>` → `Messages<M>` and
`EventReader/Writer` → `MessageReader/Writer`; the `Event`
trait still exists but means observer-triggered immediate
events via `World::trigger`; the double-buffered ring buffer
pattern the catalog brief calls "`Events<T>` double buffer" is
now `Messages<M>` in `crates/bevy_ecs/src/message/`; the
pattern is unchanged — this is the catalog↔repo drift of the
iteration; Bevy itself moved; canonsim lifts the *pattern*,
not the name),
`docs/ref/eventstore.md` (534 — BSD-3-Clause [≤23.x] / ESLv2
[24.10+] — pattern only; canonical event-sourcing mechanics:
`EventRecord` with fields `EventId : Guid`, `EventType :
string`, `Data : ReadOnlyMemory<byte>`, `Metadata :
ReadOnlyMemory<byte>`, `EventStreamId : string`, `EventNumber
: long`, `LogPosition : long`, `CorrelationId : Guid`,
`TransactionPosition : long`, `TransactionOffset : int`,
`ExpectedVersion : long`, `TimeStamp : DateTime`, `Flags :
PrepareFlags`; client-facing analog `KurrentDB.Client.
EventData` with `EventId : Uuid`, `Type : string`, `Data`,
`Metadata`, `ContentType : string` (only `application/json`
or `application/octet-stream`); lifted into `schemas/event.
schema.json` as the event record shape — INV-1 inversion:
`EventStreamId` becomes the implicit grouping by `actor_id`
in our global log + `ExpectedVersion` static class with
constants `Any = -2`, `NoStream = -1`, `Invalid = -3`,
`StreamExists = -4`; modern SDK rebrands to `KurrentDB.Client.
StreamState` (readonly struct) with `NoStream`, `Any`,
`StreamExists`, `Deleted = -5`, `Tombstoned = -6`,
`StreamState.StreamRevision(ulong value)` factory for the
exact-version case; every write op carries `ExpectedVersion`,
storage compares to stream's `LastEventNumber`, rejects with
`OperationResult.WrongExpectedVersion` on mismatch; lifted into
`cli/` Intent → Event validation front-door — an Intent
converts to an Event only after the invariant check passes,
mirroring the OCC semantics of `NoStream` (an actor that
should be new) and exact-version writes + `SystemNames`
static constants: `SystemStreams` with `AllStream = "$all"`,
`SettingsStream = "$settings"`,
`PersistentSubscriptionConfig`, `ScavengesStream`,
`ScavengePointsStream`, `MetastreamOf(s) = "$$" + s`,
`IsSystemStream(s) = s[0]=='$'`; `SystemMetadata` with
`MaxAge = "$maxAge"`, `MaxCount = "$maxCount"`,
`TruncateBefore = "$tb"`, `TempStream = "$tmp"`,
`CacheControl = "$cacheControl"`, `Acl = "$acl"` with
sub-keys `"$r"/"$w"/"$d"/"$mr"/"$mw"`; `SystemEventTypes`
with `StreamDeleted = "$streamDeleted"`, `LinkTo = "$>"`,
`StreamMetadata = "$metadata"`, `ScavengePoint`,
`ScavengeStarted/Completed/ChunksCompleted/MergeCompleted/
IndexCompleted`; lifted into canonsim's reserved-namespace
convention — system events use a reserved `event_type` prefix
(`_start`, `_end`, `_seed`, `_correction`); user events use
unprefixed names; the `$all` global stream is the precedent
for the global JSONL log (INV-1) + `StreamMetadata` class with
fields `MaxCount : long?`, `MaxAge : TimeSpan?`,
`TruncateBefore : long?`, `TempStream : bool?`, `CacheControl
: TimeSpan?`, `Acl : StreamAcl`; JSON-serialized via
`ToJsonBytes()` / deserialized via `FromJsonBytes(ReadOnlySpan
<byte>)`; lifted into canonsim's runtime log retention policy
— the three knobs (`MaxAge`, `MaxCount`, `TruncateBefore`)
are exactly the levers canonsim's log-retention policy needs:
per-actor or per-scenario cap on visible event count
(`MaxCount`), tick-age cap (`MaxAge`), logical truncation
point (`TruncateBefore`) + `EventNumber` with `DeletedStream
= long.MaxValue` and `Invalid = int.MinValue`; used as the
`$tb` value when a stream is hard-deleted (tombstoned) via
`ClientMessage.DeleteStream(... bool hardDelete ...)`; tombstone
is the logical deletion; scavenge is the physical compaction;
lifted into INV-5: corrections are new events (the logical-
deletion analog of a tombstone — never mutate, always append),
and the offline scavenge is a separate pass that compacts the
JSONL log + `JintProjectionStateHandler` JS projection engine
using Jint .NET JS interpreter; constructor registers four
global projection functions on the JS realm: `emit`,
`linkTo`, `linkStreamTo`, `copyTo`; state via `_state :
JsValue`, `_sharedState : JsValue`; methods `Load(string?
state)`, `GetSourceDefinition()` returning `IQuerySources`
via `SourceDefinitionBuilder`; `_emitted : List<Emitted-
EventEnvelope>` accumulator; user-supplied projection script
defines `init`/`state` (fold function) and calls
`emit(streamId, eventName, body, metadata)` or `linkTo
(streamId, event, metadata)`; adapted into `sim/systems/`
Python folds (and the `render/` fold) — each "projection" is
a `def fold(state, event) -> state` Python callable, and
"emit" is just `yield` or a returned list of derived events;
the conceptual shape — fold-from-stream producing derived
state/events — is preserved, the scripting runtime is dropped
+ `PersistentSubscription` + `PersistentSubscriptionCheck-
pointWriter` writes the checkpoint to stream
`$persistentsubscription-<id>-checkpoint` as a
`SubscriptionCheckpoint` event with `ExpectedVersion.Any` first
write then exact-version thereafter, uses metastream
`$$<...>-checkpoint` with `StreamMetadata(maxCount: 2)` so only
the latest checkpoint survives; adapted into canonsim's SQLite
incremental projection — the SQLite index IS the projection
checkpoint (the row count / max `event_seq` in the SQLite
table is the position; on restart, the projection resumes from
`SELECT MAX(event_seq) FROM projection_state`); no separate
subscription store is needed + `VNodeState` enum with 16 values
`Initializing`, `DiscoverLeader`, `Unknown`, `PreReplica`,
`CatchingUp`, `Clone`, `Follower`, `PreLeader`, `Leader`,
`Manager`, `ShuttingDown`, `Shutdown`, `ReadOnlyLeaderless`,
`PreReadOnlyReplica`, `ReadOnlyReplica`, `ResigningLeader`;
negative for canonsim: irrelevant overhead for single-process
phase-0 sim + `Scavenger<TStreamId>` + `ScavengePoint` +
`ScavengeCheckpoint` (abstract base) — the offline compaction
engine; `ScavengeAsync(CancellationToken)` runs as a pipeline
of stages: `Accumulate` → `Calculate` → `Execute(Chunks)` →
`MergeChunks` → `Execute(Index)` → `Clean`, each restartable
from a `ScavengeCheckpoint.{Accumulating, Calculating,
ExecutingChunks, MergingChunks, ExecutingIndex, Cleaning,
Done}` with a `ScavengePoint { position, eventNumber,
effectiveNow, threshold }` as the cutoff; lifted into
canonsim's offline JSONL-compaction pass + `ResolvedEvent`
struct with `Event : EventRecord`, `Link : EventRecord`,
`OriginalEvent = Link ?? Event`, `OriginalStreamId`,
`OriginalEventNumber`, `OriginalPosition : TFPos?`;
`ReadStreamResult` enum `Success`, `NoStream`,
`StreamDeleted`, `NotModified`, `Error`, `AccessDenied`,
`Expired`; `OperationResult` enum `Success`, `PrepareTimeout`,
`CommitTimeout`, `ForwardTimeout`, `WrongExpectedVersion`,
`StreamDeleted`, `InvalidTransaction`, `AccessDenied`;
negative for canonsim: link-to events not lifted (our global
JSONL log doesn't need a separate link-to event type;
`actor_id` field is the link) + `WriteEventsCompleted` with
`CorrelationId`, `Result : OperationResult`, `Message`,
`FirstEventNumber`, `LastEventNumber`, `PreparePosition`,
`CommitPosition`, `CurrentVersion`; lifted into `cli/`
write-result shape — the `Intent → Event` validation front-
door returns the post-write `event_seq` so the caller can
chain an Intent with the exact expected `event_seq` for the
next write (the OCC chain); explicitly negative on JS
projection engine Jint (D-012 fix: Python fold functions in
`sim/systems/`, "emit" is `yield`) + cluster gossip +
leader election (irrelevant overhead for single-process
phase-0 sim) + ESLv2 license friction at 24.10+ (no-hosted-
service clause — pattern-only intake is the only path, but
none of the C# code is useful to us anyway — wrong language,
wrong runtime) + persistent subscriptions need a backing
store for checkpoints (canonsim: SQLite IS the projection
checkpoint, separate stream would be double-bookkeeping) +
`$all` TFPos opaque ordering (INV-2 fix: explicit domain-
meaningful `(tick, sub_order, actor_id)` queue key —
EventStoreDB's TFPos is unsuitable because it leaks storage-
layer mechanics into the simulation's notion of time);
'every event has a stream it belongs to; the stream is the
unit of ordering; `ExpectedVersion` is the unit of concurrency
on that stream' lesson + 'logical deletion and physical
compaction are different operations on different timelines'
lesson (INV-5's ancestor — the same separation applied to
corrections as well as deletions) shape the canonsim event-
sourcing contract; license history verified 2026-08-26 from
the repo LICENSE.md file at multiple tags + the commit log:
tag `oss-v23.10.0` opens "EventStoreDB License / Copyright
(c) 2011-2023, Event Store Ltd" with the verbatim 3-clause
BSD body and self-declares "Event Store is permissively
licensed under the 3-clause BSD license"; commit
`7c85c2944234` 2024-09-27 "Apply Event Store License v2"
replaces BSD on master; commit `88f4ff37532f` 2025-02-11
"[KDB-598] Update copyright notice ... Update license to
kurrent license v1" renames ESLv2 to "Kurrent License v1"
(Event Store Ltd rebranded to Kurrent, Inc.; the
`EventStore/EventStore` repo auto-redirects to
`kurrent-io/EventStore`); catalog §6 row reads "EventStore
(EventStoreDB) | BSD-3-Clause (≤23.x); ESLv2 from 24.10 —
pattern only"; index §2 row said "MIT" — standing pre-flip
check (KI#6-class pitfall) caught the drift in the same §2
edit that flips ref-10-c todo→done with the corrected
"BSD-3-Clause (≤23.x); ESLv2/Kurrent-License-v1 from 24.10 —
pattern only" annotation; the "pattern only" intake is the
correct and safer choice: ESLv2 §Limitations says "You may
not provide the software to third parties as a hosted or
managed service" — canonsim does not host EventStoreDB, so
the clause never bites; and none of EventStoreDB's actual
code is useful to us anyway — it is C#/gRPC/Jint/Javascript,
while canonsim is Python ≥3.11 stdlib-only (D-012); what we
want is the architectural pattern: streams as ordered event
sub-sequences, `ExpectedVersion` optimistic concurrency,
projections as fold-from-stream, `$maxAge`/`$maxCount`
retention, tombstone+scavenge separating logical deletion
from physical compaction; none of these concepts is
copyrightable subject matter — they are ideas/mechanics,
not expression),
`docs/ref/sqlite_fts5.md` (368 — public domain; zero-
dependency keyword search in stdlib SQLite: FTS5 is an
SQLite **virtual table module** that builds an inverted
full-text index (terms → doclists of `(rowid, col, offset)`
positions) over user-declared text columns, queryable through
the SQL `MATCH` operator with BM25 relevance ranking; the
canonical C source lives in `ext/fts5/` (reduced to `fts5.c`/
`fts5.h`; loadable-extension entry points `sqlite3_fts_init`/
`sqlite3_fts5_init`); FTS5 ships with Python's `sqlite3`
module — no `pip install`, no native wheel, no network;
`import sqlite3` is the entire integration; verified live
against sqlite version 3.53.1; lifted as the chronicle facts
index (D-003 canon index); **Schema** — `CREATE VIRTUAL TABLE
<name> USING fts5(<col1>, <col2>, ...)` (no types/constraints/
`PRIMARY KEY` allowed; the table has an implicit `rowid
INTEGER PRIMARY KEY` for rowid-binding inserts; tokenizer
chosen at create time via `tokenize=`); lifted into `core/
storage.py` SQLite index — every projected fact row gets a
row in an FTS5 virtual table; queries go through `MATCH` +
**Query surface** — three equivalent forms: `WHERE email
MATCH 'fts5'`, `WHERE email = 'fts5'`, or table-valued
function `email('fts5')`; relevance order via `ORDER BY
rank` (`rank` is a virtual column defaulting to `bm25()`); the
TVF form also takes a rank override as its 2nd arg: `email(?,
'bm25(10.0, 5.0)')` + **Tokenizers** (`tokenize=` option):
`unicode61` (the default — Unicode 6.1 letter/number
categories `L* N* Co` are tokens, all else separators;
case-folds per Unicode; removes Latin diacritics so `A`/`a`/
`À`/`à`/`Â`/`â` are equivalent; options `remove_diacritics`
`0|1|2` (default `1`), `categories`, `tokenchars`,
`separators`; lifted as the default tokenizer for
multilingual content packs), `ascii` (non-ASCII always token
chars, ASCII-only case-fold, no `remove_diacritics` — not
lifted, default to `unicode61` instead), `porter` (wrapper
applying the Porter stemmer to another tokenizer's output,
lets `correction` match `corrected`/`correcting` — lifted as
an optional tokenizer for English-language content packs),
`trigram` (3-char sliding-window tokens → general substring
matching — lifted as an optional tokenizer for substring
search over names/identifiers), custom via the `fts5_api`
struct (out of scope for stdlib runtime) + **`bm25(<table>[,
w0, w1, ...])`** — the canonical BM25 ranking function;
returns a real where lower = better (FTS5 multiplies by −1 so
ascending `ORDER BY bm25(ft)` returns best first; `k1=1.2`,
`b=0.75` hardcoded; per-column weights are positional trailing
args; lifted into `brief/assembler.py` as the zero-dep baseline
ranker — subject/title weighted above body + **`highlight(<-
table>, colIdx, before, after)`** — returns column text with
each phrase match wrapped; lifted into `render/` for snippet
extraction + **`snippet(<table>, colIdx, before, after,
ellipsis, maxTokens)`** — auto-selects a short fragment
maximizing distinct query terms (biased to column starts and
to `.`/`:` boundaries); `maxTokens` ≤ 64; lifted into
`render/` as the off-the-shelf excerpter + **Query operators**
(BNF in `fts5.html` §3): `AND`/`OR`/`NOT` (precedence `NOT` >
`AND` > `OR`, all case-sensitive keywords); `NEAR(p1 p2 [, N])
` proximity (default `N=10` tokens between end of first phrase
and start of last); `*` prefix token; `^` initial-token
anchor; `+` phrase concatenation; column filters `col:` /
`{col1 col2}:` and negated `-col:`; lifted into the retrieval
query DSL — the `NEAR` operator is the canonical "find facts
where these words appear within N tokens of each other"
pattern (e.g. "theft NEAR/3 arson") + **Special INSERT
commands** — `INSERT INTO ft(ft, ...) VALUES(...)` drives the
index lifecycle: `rebuild` (full reindex — the schema-bump /
tokenizer-change path; lifted into the INV-1 path — a schema
change or tokenizer swap requires a full `rebuild`), `optimize`
(merge all segment b-trees into one), `merge ±N` (incremental),
`automerge`/`crisismerge`/`usermerge`/`deletemerge` (segment-
merge thresholds — defaults are good), `delete`/`delete-all`
(brittle on contentless tables — caller must resupply exact
original column values or index corrupts; prefer plain tables
+ full rebuild), `integrity-check` (raises `SQLITE_CORRUPT_
VTAB` on mismatch — lifted as post-rebuild smoke test), `rank`
(set the table's default rank mapping), `pgsz`, `secure-delete`,
`insttoken` + **`fts5vocab` virtual table module** —
`CREATE VIRTUAL TABLE v USING fts5vocab(ft, 'row'|'col'|
'instance')` exposes the raw index: `row` = `(term, doc, cnt)`,
`col` adds `col`, `instance` adds `doc`(rowid)+`col`+`offset`;
lifted as the introspection escape hatch + **Shadow tables**
(3–5 real tables created beside the virtual table; `fts5.html`
§9: "They should not be accessed directly by the user"): `%_
data(id INTEGER PRIMARY KEY, block BLOB)`, `%_idx(segid, term,
pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID`, `%_config(k
PRIMARY KEY, v) WITHOUT ROWID`, `%_docsize(id INTEGER PRIMARY
KEY, sz BLOB)`, `%_content(id INTEGER PRIMARY KEY, c0, c1,
...)`; lifted as a non-goal: never `SELECT` shadow tables
directly; `fts5vocab` is the sanctioned introspection escape
hatch + **Segment b-trees** — the index is an ordered key-
value store (keys = terms/term-prefixes, values = varint-
packed doclists of `(rowid, col, offset)` triples) stored as a
series of immutable, leveled segment b-trees; each commit adds
one or more level-0 segments with tombstones for deletes;
readers query every segment and merge, newer-wins; lifted as
the lesson: batch inserts in one transaction and `optimize`
once at the end, not per event + **Content-table variants**:
plain, contentless (`content=''`, no `%_content`, deletes
need the `delete` command), contentless-delete (tombstone
variant), external content (`content='othertable'`, index on
text stored elsewhere); lifted as the choice rule: plain
tables (with `%_content`) for our rebuild-from-log model —
contentless tables are brittle on `delete`; explicitly
negative on keyword-only (need sqlite-vec for semantic) +
ranking customization is bm25 + custom C function only
(recency×authority×BM25 blend needs Python reranker) +
tokenizer fixed at CREATE TABLE (switch forces full rebuild
— INV-1-expected path but plan at design time) + segment
b-trees accumulate under write-heavy loads (batch inserts +
optimize once at end, not per event) + `delete` on
contentless tables brittle (prefer plain tables + full
rebuild); 'BM25 is the canonical keyword-relevance baseline —
anything semantic compares against it' lesson + 'inverted
index as a fold-of-the-log projection' lesson (FTS5's
`rebuild` is the proof INV-1's log=truth/SQLite=index split
has a first-class supported refresh path) shape phase-4
retrieval; public domain (verified 2026-08-26 against
https://sqlite.org/copyright.html — "SQLite Is Public
Domain … All of the code and documentation in SQLite has
been dedicated to the public domain by the authors"; FTS5 is
not a separate library: per `fts5.html` §2.1, "As of version
3.9.0 (2015-10-14), FTS5 is included as part of the SQLite
amalgamation"; Python's stdlib `sqlite3` ships that
amalgamation — verified live; FTS5 is D-012-compliant by
construction — it is the zero-runtime-dep search layer of
record (`TECH_NOTES.md` "Zero-dependency default: SQLite
FTS5 keyword search over facts and lore"); catalog §6 row
reads "SQLite (+FTS5) | public domain | canon index (D-003);
FTS5 keyword search over facts/lore — the zero-dependency
search layer (rev v2)"; index §2 row had matching "public
domain" license + matching phase 4 — no drift this iteration),
`docs/ref/duckdb.md` (458 — MIT; in-process columnar OLAP SQL
database engine implemented as a C++17 library — the
analytical analogue of SQLite; catalog describes DuckDB as
"analytics over the log, chronicle rebuilds (rev v2: offline
'chronicler' compression)"; the role is OFFLINE analytics /
offline compression, not in-process runtime — DuckDB is a C++
runtime dependency, NOT shippable as a vendored runtime dep
under D-012; the intake is "offline chronicler compression" —
read JSONL → run SQL analytics → write parquet archive +
summary SQLite; for phase-0 + phase-1, DuckDB is not needed
at all — the JSONL log is small; the runtime SQLite projection
is sufficient; DuckDB enters at phase-3+ when analytics over
100k+ events become a real workflow (D-022); `DuckDB` class
(database handle; constructor `DuckDB(const char *path =
nullptr, DBConfig *config = nullptr)`; `nullptr` = in-memory,
path = persistent; owns `shared_ptr<DatabaseInstance> instance`
aggregating `BufferManager`, `DatabaseManager`, `TaskScheduler`,
`ObjectCache`, `ExtensionManager`, `LogManager`; static helpers
`LibraryVersion`, `StandardVectorSize`, `Platform`) +
`Connection` class (per-client query surface; methods `Query`
→ `MaterializedQueryResult`, `SendQuery` → streamable
`QueryResult`, `Prepare` → `PreparedStatement`, `PendingQuery`
for async/interruptible, `Interrupt`, `GetQueryProgress`;
relation builders `Table`, `ReadCSV`, `ReadParquet`,
`TableFunction`; `EnableProfiling`/`DisableProfiling` toggle
the query profiler) + **Vectorized execution — `STANDARD_
VECTOR_SIZE = 2048`** — every operator pushes data through
`DataChunk`s of 2048 rows at a time (`vector<Vector> data` in
`DataChunk`; morsel-driven parallelism without using the word
"morsel" — the chunk IS the morsel); the `PipelineExecutor`
pulls through the operator tree; lifted as the lesson —
columnar layout makes "scan all `suspicion` values across 1M
events" a single sequential pass; SQLite's row-store page
model makes the same query a full-table scan +
`PhysicalOperator` family keyed by `enum class
PhysicalOperatorType` — real members: `FILTER`, `PROJECTION`,
`HASH_GROUP_BY`, `PERFECT_HASH_GROUP_BY`, `PARTITIONED_
AGGREGATE`, `WINDOW`, `HASH_JOIN`, `NESTED_LOOP_JOIN`,
`CROSS_PRODUCT`, `PIECEWISE_MERGE_JOIN`, `ASOF_JOIN`, `TOP_N`,
`ORDER_BY`, `TABLE_SCAN`, `INSERT`, `BATCH_INSERT`,
`COPY_TO_FILE`, `BATCH_COPY_TO_FILE`, `ATTACH`, `DETACH`,
`CREATE_SEQUENCE`, `EXPLAIN_ANALYZE`; each operator implements
`Execute`/`GetData`/`Sink` returning `OperatorResultType`/
`SourceResultType`/`SinkResultType`; closed family keyed by
enum + **`read_json_auto()` table-valued function**
(`extension/json/json_functions/read_json.cpp:384`) —
`JSONFunctions::GetReadJSONAutoFunction()` creates a
`TableFunctionSet` named `"read_json_auto"`; sibling functions
`read_json`, `read_ndjson`, `read_ndjson_auto`, `read_json_
objects`, `read_ndjson_objects`, `read_json_objects_auto`; the
`auto` variant auto-detects schema from the JSON; NDJSON mode
reads newline-delimited JSON — the canonical JSONL ingestion
path; lifted into the chronicler — `SELECT * FROM read_ndjson_
auto('log/events.jsonl')` is the entire intake step; the
*pattern* — that the log file is directly queryable as a
table — is the inheritance + **`COPY TO` parquet via
`CopyFunction("parquet")`** (`extension/parquet/parquet_
extension.cpp:1040`) — parquet registered as `CopyFunction`
with `copy_to_sink = ParquetWriteSink`, `copy_to_finalize =
ParquetWriteFinalize`, `execution_mode = ParquetWriteExecu-
tionMode` (returns `PARALLEL_COPY_TO_FILE` / `BATCH_COPY_TO_
FILE` / `REGULAR_COPY_TO_FILE`); same function object carries
`copy_from_function` so `COPY FROM 'x.parquet'` and `COPY
(SELECT…) TO 'x.parquet'` are both first-class; lifted as the
chronicler output path + **`Appender` API** (`src/include/
duckdb/main/appender.hpp:30`) — high-throughput bulk-insert
path bypassing per-row SQL parsing; concrete API:
`BaseAppender::BeginRow`, `EndRow`, template `Append<T>
(value)` with explicit instantiations for `bool, int8_t …
uint64_t, float, double, date_t, timestamp_t, string_t,
Value, nullptr_t`; `Flush` commits, `Close` flushes +
invalidates; flushes internal `ColumnDataCollection` every
`DEFAULT_FLUSH_COUNT = STANDARD_VECTOR_SIZE * 100` (=
204,800 rows); three concrete classes `Appender` (for a real
table), `QueryAppender` (inserts via a custom query),
`InternalAppender` (internal system tables); lifted as the
canonical bulk-load pattern when `read_json_auto` is too slow +
**Composite column types** (`enum class LogicalTypeId :
uint8_t`): `STRUCT = 100`, `LIST = 101`, `MAP = 102`, `UNION
= 107`, `ARRAY = 108`, `TUPLE = 110`; constructors on
`LogicalType`: `LogicalType::STRUCT(child_list_t<Logical-
Type>)`, `LogicalType::LIST`, `LogicalType::ARRAY`,
`LogicalType::MAP`; SQL surface: `STRUCT(name VARCHAR,
value INTEGER)`, `LIST(INTEGER)[1,2,3]`, `INTEGER[4]` (fixed-
size ARRAY); lifted as the auto-detection contract — `read_
json_auto()` infers these for us; nested `data` and `metadata`
objects in JSONL map directly to `STRUCT(...)` columns +
**Window functions** (`enum`): `WINDOW_RANK = 120`,
`WINDOW_RANK_DENSE = 121`, `WINDOW_NTILE = 122`,
`WINDOW_PERCENT_RANK = 123`, `WINDOW_ROW_NUMBER = 125`,
`WINDOW_FIRST_VALUE = 130`, `WINDOW_LAST_VALUE = 131`,
`WINDOW_LEAD = 132`, `WINDOW_LAG = 133`; bound in
`BoundWindowExpression` with `WindowBoundary start` /
`WindowBoundary end`; lifted as the canonical "diff consecutive
per-actor state" pattern — `LAG(suspicion) OVER (PARTITION BY
actor_id ORDER BY tick)` + **Extension mechanism** (`INSTALL`/
`LOAD`/`AutoLoadExtension`) — built-in core extensions live
under `extension/`: `parquet`, `json`, `icu`, `core_functions`,
`autocomplete`, `tpcds`, `demo_capi`; SQL: `INSTALL json;
LOAD json;`; extensions can be statically linked via `DuckDB::
LoadStaticExtension<T>`; lifted as a negative: extensions fetch
from DuckDB's extension repository by default — in an air-
gapped or stdlib-purist context this is a network dependency;
canonsim's chronicler must either bundle the extension
binaries or rely on auto-loaded core extensions + **`ATTACH`
external databases + `CREATE SEQUENCE`** — `PhysicalAttach`
wires `AttachInfo` so a second database file can be queried
read-only as `att_db.tablename`; lifted as the chronicler
output path: `ATTACH 'chronicle.sqlite'; INSERT INTO
chronicle.sqlite.facts_summary SELECT … FROM read_ndjson_
auto('log/events.jsonl') GROUP BY actor_id;` + **`PRAGMA`
system + `EXPLAIN`** — `enable_verification` (deprecated
no-op), `enable_profiling`/`disable_profiling`,
`enable_progress_bar`/`disable_progress_bar`,
`enable_object_cache`, `enable_optimizer`/`disable_optimizer`,
`force_checkpoint`, `verify_parallelism`; `EXPLAIN` operator
is `LogicalExplain`/`PhysicalExplainAnalyze` producing a plan
tree via `ProfilerPrintFormat`; lifted as the diagnostic
surface for the chronicler + **Columnar storage + compression**
— pluggable per-column compression with concrete
implementations: `Bitpacking`, `Dictionary`, `FSST`, `ALP`/
`ALPRD`, `Chimp128`, `Patas`, `Roaring`, `Zstd`; each has
parallel `analyze`/`compression`/`decompression`/`scan`/`fetch`
modules; lifted as the lesson: columnar layout + per-column
compression makes "scan all `suspicion` values across 1M
events" a single sequential pass; explicitly negative on C++
runtime dependency (D-012 fix: NOT in the runtime path —
chronicler is `scripts/chronicle.py` outside the runtime
module graph) + phase-0 log too small (SQLite wins on
simplicity below ~100k events — DuckDB's analytical advantage
wasted) + single-writer OLAP model (cannot live-ingest during
simulation — chronicler runs after tick-batch seal) + another
tool in the chain (only justified at phase-3+ scale per D-022)
+ extensions fetch from network by default (must bundle
binaries or rely on auto-loaded core extensions in air-gapped
contexts); 'columnar layout is the canonical shape for event-
log analytics; row-store SQLite is the wrong shape for full-
log rollups' lesson (runtime index = row-store SQLite for
point lookups; offline analytics = columnar DuckDB for rollups;
boundary is the chronicler) + 'point at the file and start
querying' lesson (the log is already queryable — chronicler is
optional, never required) shape phase-4 offline analytics;
MIT (verified 2026-08-26 from repo LICENSE header "Copyright
2018-2026 Stichting DuckDB Foundation" — "Permission is hereby
granted, free of charge, to any person obtaining a copy of
this software … to deal in the Software without restriction");
catalog §6 row reads "DuckDB | MIT | analytics over the log,
chronicle rebuilds (rev v2: offline 'chronicler' compression)";
index §2 row had matching MIT license — no drift this iteration),
`docs/ref/sqlite_vec.md` (383 — dual `MIT OR Apache-2.0`;
local-first vector index in SQLite — single-file, dependency-
free loadable SQLite extension written in pure C that adds a
`vec0` virtual-table module plus a suite of SQL scalar
functions for storing, querying, and compressing `float32` /
`int8` / `bit` vectors inside an ordinary SQLite database —
i.e. "FTS5, but for embeddings"; the canonical local-first
vector store — no qdrant server, no lancedb extra dep, just a
SQLite loadable extension; for phase 4 retrieval, sqlite-vec
is the canonical local-first vector store; the `vec0` shape
(`CREATE VIRTUAL TABLE … MATCH … ORDER BY distance LIMIT k`)
mirrors FTS5 (`docs/ref/sqlite_fts5.md`) — same ergonomics
for keyword and vector search, both in the same SQLite
database file; **critical phase-0 intake rule:** sqlite-vec
is a C `.so`/`.dll`/`.dylib` loadable extension — does NOT
ship with Python's stdlib `sqlite3` module (macOS system
Python even lacks `enable_load_extension` entirely); phase 0
cannot rely on it; phase 4 treats it as opt-in: the retriever
probes `db.enable_load_extension(True)` + `sqlite_vec.load
(db)` inside a `try/except`; if unavailable, it silently
degrades to pure-Python brute-force `cosine_sim()` over the
same embeddings cached in SQLite; **`vec0` virtual-table
module** registered at `sqlite-vec.c:10688` via
`sqlite3_create_module_v2`; DDL shape `CREATE VIRTUAL TABLE
<name> USING vec0(<col> <type>[N] [pk] [partition key]
[distance_metric=L2|cosine], <other_col> <type>[M], +<aux_col>
<type>, ...)`; lifted into the canonical "vector index over
facts" pattern for `core/storage.py` — `CREATE VIRTUAL TABLE
lore_vec USING vec0(embedding float[D], +fact_text text,
scenario_id integer partition key)` gives canonsim's phase-4
retrieval layer the same ergonomics as its FTS5 keyword index:
`WHERE embedding MATCH :q ORDER BY distance LIMIT k`; the
auxiliary `+fact_text` column means retrieval returns the
fact payload with no JOIN; the `scenario_id integer
partition key` column maps onto phase-0 tavern scope (one
partition per scenario; pre-filters kNN to in-scope facts) +
**`rowid` PK + MATCH kNN query** — every `vec0` table has an
implicit `rowid`; the kNN pattern: `select rowid, distance
from vec_examples where sample_embedding match '[0.89,
0.54, ...]' order by distance limit 2;`; the `k` constraint
(`and k = 10`) is the pre-3.41 form; `LIMIT k` works on
SQLite ≥ 3.41; the C source validates this at `sqlite-vec.
c:6101`: "A LIMIT or 'k = ?' constraint is required on vec0
knn queries."; lifted into the retrieval query DSL alongside
FTS5 + **`vec_distance_cosine(a, b)`** registered at
`sqlite-vec.c:10665`; C impl `static void vec_distance_
cosine(...)` at line 1423; computes cosine *distance* (not
similarity; `1 - cos`) between two float32 or int8 vectors;
**note:** the canonical SQL name is `vec_distance_cosine`,
**not** `vec_distance_cos`; lifted as the canonical
similarity metric — for static-lore RAG; cosine is the right
default for normalized embedding models + **`vec_distance_L2
(a, b)` / `vec_distance_L1(a, b)` / `vec_distance_hamming
(a, b)`** registered at lines 10662–10664; L2 = Euclidean
(float32/int8); Hamming = bit-vectors only; the `vec0`
default distance metric is L2; cosine is opt-in per-column
via `distance_metric=cosine` in the DDL (parsed at `sqlite-
vec.c:3066`, stored on `VectorColumnDefinition.distance_
metric` at line 2688); lifted as the distance-metric choice
rule — cosine for normalized embeddings (the canonsim
default), L2 for non-normalized, Hamming for binary-quantized
vectors + **`vec_f32(v)` / `vec_int8(v)` / `vec_bit(v)`
constructors** registered at lines 10673–10675; return a
BLOB with a `sqlite3_result_subtype` of `223` (float32), `225`
(int8), or `224` (bit); this subtype byte is how sqlite-vec
tags vector type on an otherwise-undifferentiated BLOB; the
pattern: vectors over the wire are just `struct.pack`-ed
`float32` BLOBs — `bindings/python/extra_init.py` ships a
4-line pure-Python `struct.pack("%sf" % len(v), *v)` serializer;
lifted into `core/storage.py` pure-Python fallback — same BLOB
format, same `cosine_sim(a: bytes, b: bytes) -> float` signature
as `vec_distance_cosine` + **`vec_to_json(v)`** registered at
line 10668; `static void vec_to_json(...)` at line 1965;
renders a vector BLOB as a JSON array string; the constructors
accept JSON input the other way; JSON input is tagged with
`#define JSON_SUBTYPE 74` (line 865); lifted as the vector-
serialization contract — vectors go over the wire as JSON
arrays, the BLOB form is for storage + compute +
**`vec_quantize_binary(v)` / `vec_quantize_int8(v, 'unit')`**
registered at lines 10676–10677; `vec_quantize_binary` (line
1618) reduces each float element to a single bit (1 =
positive, 0 = negative), packing 8 dims per byte → 32×
storage reduction for float32; used to build a coarse index
that's re-scored against full vectors (`site/guides/binary-
quant.md` shows the two-pass `coarse_matches` CTE pattern
with `vec_distance_L2` rescore); lifted as the compression
fallback before reaching for an ANN index: build a coarse
`bit[D]` column alongside the `float[D]` column, kNN-filter
on the bit index at high k, then re-rank the survivors with
`vec_distance_L2`; this is the canonsim "scale-up without
adding a server" ladder rung + **`vec_slice(v, start, end)` +
`vec_normalize(v)`** — the **matryoshka embeddings** primitives;
`vec_slice` (line 1849, registered line 10671) extracts dims
`[start, end)` from a vector; `vec_normalize` (line 2015,
registered line 10672) L2-normalizes a float32 vector; the
matryoshka pattern: train at 1024-d, store/query at 256-d →
~4× index shrink with minimal quality loss on matryoshka-
trained models (`mxbai-embed-large-v1`, `nomic-embed-text-
v1.5`, `text-embedding-3-large`); lifted as the matryoshka
pattern — train embeddings at high dim, store at low dim →
~4× smaller lore index for the tavern scenario's static-fact
corpus + **`vec0` shadow tables** declared on the `vec0_vtab`
struct (`sqlite-vec.c:3528–3576`): `_rowids`, `_chunks`,
per-vector `_vector_chunks00`, per-vector `_rescore_chunks00`/
`_rescore_vectors00`, per-metadata `_metadatachunks00`; the
vec0 module also supports partition-key columns
(`Vec0PartitionColumnDefinition`, struct at line 2697 —
internally shards the index) and auxiliary columns (`+`-prefixed,
`Vec0AuxiliaryColumnDefinition` at line 2703 — stored in a
separate table, not in kNN `WHERE`, no JOIN needed for SELECT);
max 16 metadata + 16 auxiliary + 4 partition keys; lifted as
shadow-table separation as an architectural metaphor, not a
literal copy — canonsim adapts by storing event-log-derived
fact embeddings in a separate `fact_embeddings(fact_id,
embedding BLOB)` table alongside the main `facts` table, same
separation-of-PK-from-payload discipline, expressed as
ordinary (non-virtual) SQLite tables so it works without the
extension loaded + **`vec_each(v)` table function** registered
at line 10689 via `vec_eachModule` struct at line 3365;
returns one row per vector element (`rowid`, `value`); mirrors
FTS5's `fts5vocab` pattern; lifted as the introspection escape
hatch + **`vec_version()` / `vec_debug()`** registered at
lines 10641 / 10647; runtime introspection (`vec_debug()`
returns version + build flags + commit); useful for the
canonsim "is the extension actually loaded?" probe + **Loadable-
extension entrypoint + Python `sqlite_vec.load(db)`** — the C
extension is loaded into the SQLite runtime via
`sqlite3_load_extension` (Python: `db.enable_load_extension
(True); sqlite_vec.load(db); db.enable_load_extension(False)`);
the CLI flag for the `sqlite3` shell is `.load ./vec0`;
**crucially, this is NOT in Python's stdlib** — `sqlite-vec`
ships as a `.so`/`.dll`/`.dylib` downloaded from GitHub Releases
(or `pip install sqlite-vec` which bundles the precompiled
binary); the macOS system Python lacks `enable_load_extension`
entirely (`AttributeError: 'sqlite3.Connection' object has no
attribute 'enable_load_extension'` — Homebrew Python is the
documented workaround); lifted as the intake contract:
conditional loadable extension, NOT a phase-0 runtime
dependency (D-012 compliance) + **`serialize_float32()` /
`serialize_int8()` Python helpers** — `bindings/python/
extra_init.py` ships a 4-line pure-Python `struct.pack("%sf"
% len(v), *v)` serializer; this is the exact pattern canonsim's
fallback needs: vectors over the wire are just `struct.pack`-ed
`float32` BLOBs, no extension required to produce them;
explicitly negative on C extension not in Python stdlib (D-012
fix: conditional loadable extension at phase 4 — phase 0 stays
stdlib-only with pure-Python `cosine_sim()` brute-force fallback
over the same BLOB format) + pure-Python fallback O(N·D) per
query (viable for phase-0 small N < 10⁴ facts, painful past
10⁴ at 768-d) + pre-v1 with breaking changes expected (README
IMPORTANT banner — pin a version, treat SQL contract as the
stable interface not C ABI) + no approximate search in stable
path (HNSW/IVF/DiskANN live in separate experimental C files,
not the default — at very large corpora qdrant/lancedb would
be needed) + brute-force only for the core `vec0` path (README
states "brute-force only and meant to run on small devices");
'vectors are just another typed column on the same SQLite
index' lesson (no separate vector server — embedding column
is just another rebuildable projection of the event log, INV-1
extends to RAG layer) + 'loadable extension keeps the runtime
minimal — if you don't load it, the runtime is still stdlib-
only' lesson (pattern at intake, dep only at opt-in) shape
phase-4 retrieval; catalog "verify" license status RESOLVED
to dual `MIT OR Apache-2.0` (verified 2026-08-26 from repo
LICENSE-MIT file header "Copyright (c) 2024 Alex Garcia" +
LICENSE-APACHE file present + `sqlite-dist.toml` manifest
declares `license = "MIT OR Apache-2.0"`); since MIT is one of
the two offered licenses, canonsim may take it under plain
MIT terms; catalog §6 row read "sqlite-vec (asg017) | verify
| vector search inside SQLite for static-lore RAG (phase 4;
§14)" — `verify` status now resolved to "MIT OR Apache-2.0
(dual)"; index §2 row had "MIT" — standing pre-flip check
(KI#6-class pitfall) caught the dual-vs-MIT drift in the same
§2 edit that flips ref-11-c todo→done with the corrected
"MIT OR Apache-2.0 (dual)" annotation.
§2 of `docs/REFERENCES_DEEP.md` flips ref-10-a/b/c + ref-11-a/
b/c todo → done with rich one-line verdicts + fixes license
drift on ref-10-c [index "MIT" → "BSD-3-Clause (≤23.x);
ESLv2/Kurrent-License-v1 from 24.10 — pattern only" — pre-flip
caught, KI#6-class pitfall avoided] + resolves ref-11-c
"verify" catalog license status to dual "MIT OR Apache-2.0"
+ fixes the matching index drift [index "MIT" → "MIT OR
Apache-2.0 (dual)"]. `docs/AGENT_NAVIGATION.md` §1 adds the
six new files to the `docs/ref/` list. `docs/TASKS.md` flips
ref-10 + ref-11 backlog entries done in-place with rich
per-source verdicts + adds a one-line Done collapse entry at
the bottom. Per AGENTS §2.5 this is the **seventeenth** docs
iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k,
0l, 0m, 0n, 0o, 0p, 0q, 0r; iter-0d was infra) — the doc-loop
alarm has fired again; the owner explicitly asked to continue
reference work, so the D-022 exception applies. iter-1 is still
the next functional step; no further docs iterations without
a fresh owner request. All references in the backlog are now
done — ref-1 through ref-11 complete (plus the iter-0h
cousins: Neighborly + Mesa + DF Legends XML); the next
functional step is iter-1 core plumbing (seed, RNG instance,
clock, event queue, JSONL log with header, playscript runner,
pack loader for the drafted `content/tavern_pack/` v0.1).
KI#3, KI#4, KI#5 unchanged.
AGENTS, ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas,
TECH_NOTES, SPECS_BACKLOG, CORE_DESIGN_RESEARCH, VISION,
DECISIONS — untouched.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Doc-loop alarm vs owner-requested research.** Seventeen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0r is the seventeenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n,
  0o, 0p, 0q, 0r; iter-0d was infra). All ref-N backlog items are now
  complete (ref-1 through ref-11, plus the iter-0h cousins: Neighborly +
  Mesa + DF Legends XML); no further ref-N iterations remain.
- **Substance over line count (D-025) + per-ref split (D-026).** The
  400-line cap was a crutch — iter-0i trimmed real depth (XML element
  lists, event-type enumerations, Mesa pseudo-code, DataCollector
  details) to fit. AGENTS §6 cap is 600, but §6.1 is the real law — filler /
  restatements / linker chains / decorative prose are cut always; named
  systems, real field lists, type enumerations, pseudo-code, per-source
  verdicts are never cut to fit the cap. Over cap after a real cruft pass:
  keep, document in worklog. At iter-0j the single-file
  `docs/REFERENCES_DEEP.md` was 737 lines — 4 deep dives with concrete
  field names and type enumerations justified the breach. At iter-0k the
  same content was split into 5 per-ref files in `docs/ref/` (D-026);
  each is 101–244 lines — under the cap by construction. At iter-0l
  `paradox_scripting.md` is 605 lines — 5 over the cap, justified per
  §6.1 (three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names and ~150+ on_action IDs). At
  iter-0m three proprietary §10 source files (`rimworld.md` 253,
  `l4d_director.md` 245, `alien_isolation.md` 296) — all under
  cap by construction (the closed-source constraint forces
  field-shape-from-public-talks only, not full enumeration). At
  iter-0n four open-licensed event/narrative grammar family files
  (`wesnoth_wml.md` 244, `endless_sky_dsl.md` 228, `ink.md` 212,
  `tracery.md` 217) — all under cap by construction (the pattern-
  not-content rule §0.7 + the JSON/grammar shape lift keeps each
  file to the mechanics layer only). At iter-0o three open-
  licensed roguelike emergence + micro-sim files
  (`brogue.md` 326, `dcss.md` 360, `keeperrl.md` 444) — all
  under cap by construction (the pattern-not-content rule §0.7
  + the shape-lift keeps each file to the mechanics layer
  only; the larger line counts vs iter-0n reflect the deeper
  RNG/scheduler/queue mechanics these three sources carry —
  the §6.1 substance filter protects the depth). At iter-0p
  three open-licensed LLM-agent precedent files
  (`generative_agents.md` 371, `ai_town.md` 345,
  `letta.md` 353) — all under cap by construction (the
  pattern-not-content rule §0.7 + the shape-lift keeps each
  file to the mechanics layer only; the larger line counts
  vs iter-0n reflect the deeper memory hierarchy + retrieval
  + context-window block manager mechanics these three
  sources carry — the §6.1 substance filter protects the depth). At iter-0q
  six open-licensed worldgen data donor + grid math pattern-only files
  (`azgaar_fmg.md` 280, `natural_earth.md` 250, `geonames.md` 345,
  `libtcod.md` 279, `rot_js.md` 347, `red_blob_games.md` 312) — all
  under cap by construction (the pattern-not-content rule §0.7 + the
  shape-lift keeps each file to the mechanics layer only; the larger
  line counts vs iter-0n reflect the deeper worldgen donor + FOV /
  pathfinding / grid math mechanics these six sources carry — the
  §6.1 substance filter protects the depth). At iter-0r six open-
  licensed ECS + event-sourcing + storage-layer pattern-only files
  (`entt.md` 359, `bevy.md` 469, `eventstore.md` 534, `sqlite_fts5.md`
  368, `duckdb.md` 458, `sqlite_vec.md` 383) — all under cap by
  construction (the pattern-not-content rule §0.7 + the shape-lift
  keeps each file to the mechanics layer only; the larger line counts
  vs iter-0q reflect the deeper ECS sparse-set + scheduler +
  event-sourcing + storage-layer mechanics these six sources carry —
  the §6.1 substance filter protects the depth). The STATUS.md
  opening block at iter-0r is 803 lines (over the 600 cap) —
  substance-justified per §6.1 (named systems + real field names +
  type enumerations + per-source verdicts are all substance, never
  cut); documented in worklog.
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. The index
  restates the license as a one-line convenience column; if the two
  disagree, the catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. iter-0o
  verified the three new ref-6 rows (AGPL/GPL/GPL shorthand) against
  catalog §2 (AGPL-3.0 (CE) / GPL-2.0+ / GPL-2.0) — no drift this
  iteration. iter-0p caught one drift on ref-7-a (index said
  "(paper)", misleading — the catalog §5 says Apache-2.0 for the
  `joonspk-research/generative_agents` repo; the paper is the academic
  companion, not the license-bearing artefact); fixed in the same §2
  edit that flipped ref-7-a/b/c todo→done with the corrected
  "Apache-2.0 (repo) + paper" annotation. The diagnostic: before
  flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index
  entry. Same pattern as the catalog ↔ synthesis ↔ deep-dive
  anti-drift rule (D-024/D-026): a fact restated in two places
  drifts; the catalog is the owner. Standing pre-flip check added
  to the iter-0o workflow, exercised again in iter-0p, exercised
  again in iter-0q (ref-9-a + ref-9-b "BSD" shorthand → "BSD-3-Clause"
  to match catalog §3 explicit value; ref-9-c Red Blob Games marked as
  "CC-BY (treat as)" — catalog §8 has no license column for knowledge-
  base sources, so this is not catalog↔index drift; the convention is
  documented honestly in the per-ref file, with Amit Patel's explicit
  attribution-request in academic contexts as the basis). iter-0r
  caught TWO drifts in the same §2 edit that flipped ref-10-a/b/c +
  ref-11-a/b/c todo→done: ref-10-c EventStore index said "MIT" vs
  catalog §6 "BSD-3-Clause (≤23.x); ESLv2 from 24.10 — pattern only"
  — fixed in the same §2 edit with the corrected "BSD-3-Clause (≤23.x);
  ESLv2/Kurrent-License-v1 from 24.10 — pattern only" annotation (the
  license history was verified by reading the LICENSE.md commit log on
  master: BSD-3-Clause at tag oss-v23.10.0, ESLv2 from commit 7c85c2944234
  on 2024-09-27, renamed Kurrent License v1 at commit 88f4ff37532f on
  2025-02-11); ref-11-c sqlite-vec catalog said "verify" (the only
  unresolved license in the catalog) + index said "MIT" — verified by
  reading LICENSE-MIT + LICENSE-APACHE + sqlite-dist.toml manifest as
  dual "MIT OR Apache-2.0"; the catalog "verify" status is now RESOLVED
  to dual "MIT OR Apache-2.0", and the matching index drift (index
  "MIT" vs verified dual) was fixed in the same §2 edit. Both drifts
  are KI#6-class pre-flip catches; the standing pre-flip check is now
  exercised across iter-0o/0p/0q/0r — every ref-N batch iteration.
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source). Per-source
  **deep dives** live in `docs/ref/<source>.md` (one file per source,
  indexed by `docs/REFERENCES_DEEP.md` §2 — D-026; the single-file
  arrangement from D-024 did not scale). Drift rule (AGENTS §3): never
  restate across these three — link only. A future reference detail
  belongs in a per-ref file under `docs/ref/`, not in the catalog or the
  synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
The ref-6 deep dives (Brogue two-stream RNG, DCSS multi-stream RNG +
energy-based scheduler, KeeperRL continuous-time queue + Collective tick
order) are the direct precedents for iter-1 core plumbing. The ref-7 deep
dives (Generative Agents memory stream + retrieval function + reflection
pattern, ai-town reactive-database anti-pattern, letta block-manager +
three-tier memory hierarchy) are the precedents for the phase-1+ brief
layer (track B only, behind the phase-0 gate). The ref-8 deep dives
(Azgaar FMG four-layer architecture + ordered generator pipeline +
`State`/`Campaign` interface shapes, Natural Earth three-scale LOD
ladder + `featurecla` closed enum + semantic versioning, GeoNames
9-class/684-code feature enum + `geoname` table per-feature record +
admin-hierarchy code chain + `alternatenames` table + daily delta
files) are the precedents for phase-5 worldgen + `entities.json` +
`relations.json` P2a + `templates.json` localized name sets + chronicle
rename events. The ref-9 deep dives (libtcod FOV algorithm closed
enum + `TCOD_MapCell` per-tile state + A*/Dijkstra pathfinder +
heightmap pipeline + Mersenne Twister RNG, rot.js `EventQueue`
min-heap + scheduler family [simple/speed/action] + FOV family +
path family + Alea RNG + engine game loop, Red Blob Games hex grid
coordinate algebra + A* pseudo-code + polygon map generation
pipeline [Voronoi + Lloyd + Perlin + watershed + Whittaker biomes +
noisy edges] + relational grid abstraction + Floyd-Warshall pre-
compute) are the precedents for `core/queue.py` + `core/rng.py` +
`core/runner.py` iter-1 plumbing + `sim/systems/perception.py` +
`sim/systems/movement.py` iter-2/iter-3 systems. The ref-10 deep
dives (entt C++ ECS sparse-set blueprint + `basic_organizer` task
DAG + `sigh`/`sink`/`connection` RAII hooks + `meta_type`/
`meta_factory` reflection, Bevy Rust ECS + scheduler + `Messages<M>`
double-buffered ring [renamed from `Events<T>` in v0.20-dev] +
`Command`/`CommandQueue`/`Commands` deferred mutation + `States`
FSM, EventStoreDB canonical event-sourcing mechanics +
`ExpectedVersion` OCC constants + `SystemNames.SystemStreams`
`$all` + `StreamMetadata` retention knobs + tombstone + `Scavenger`
offline compaction) are the precedents for `core/store.py` +
`core/queue.py` + `cli/` Intent → Event validation front-door +
INV-5 corrections-as-new-events + offline scavenge + `sim/systems/
__init__.py` Schedule + `ambiguous_with` build-time conflict detection
+ `sim/systems/` phase control (States deferred FSM). The ref-11
deep dives (SQLite FTS5 `CREATE VIRTUAL TABLE USING fts5` + `bm25`
+ `highlight`/`snippet` + `NEAR`/`*`/`^`/`+` query operators +
`rebuild` INV-1 mechanism + segment b-trees + `fts5vocab`
introspection + 5 shadow tables, DuckDB `STANDARD_VECTOR_SIZE =
2048` DataChunk + `read_json_auto()`/`read_ndjson_auto()` TVF +
`CopyFunction("parquet")` + `Appender` API + `WINDOW_LAG`/
`WINDOW_LEAD` window functions + per-column compression [offline
chronicler pipeline; NOT runtime — D-012], sqlite-vec `vec0`
virtual-table module + `vec_distance_cosine` + matryoshka
`vec_slice`/`vec_normalize` + `vec_quantize_binary` 32× compression
+ loadable C extension [phase 4 only, conditionally-loaded — phase
0 stays stdlib-only with pure-Python `cosine_sim()` fallback]) are
the precedents for `core/storage.py` SQLite index + `brief/
assembler.py` bm25 ranking + `render/` highlight/snippet + the
offline `chronicler` pipeline (phase-3+ scale) + phase-4 retrieval
layer (FTS5 + sqlite-vec hybrid). **All ref-N backlog items are now
complete** — ref-1 through ref-11, plus the iter-0h cousins
(Neighborly + Mesa + DF Legends XML). The doc-loop alarm (17th
consecutive docs iteration) requires the next iteration to be
iter-1 (functional code, not docs); no further ref-N iterations
remain unless a fresh external source enters the catalog.
