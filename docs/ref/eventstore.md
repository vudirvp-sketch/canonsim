# EventStoreDB · `REFERENCES.md` §6 · BSD-3-Clause (≤23.x) / ESLv2 (24.10+) — pattern only · phase 5 (event-sourcing, T2 reference)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). License history verified 2026-08-26
> from the repo `LICENSE.md` file at multiple tags + the commit
> log: tag `oss-v23.10.0` opens "EventStoreDB License / Copyright
> (c) 2011-2023, Event Store Ltd" with the verbatim 3-clause BSD
> body and self-declares "Event Store is permissively licensed
> under the 3-clause BSD license"; commit `7c85c2944234` 2024-09-27
> "Apply Event Store License v2" replaces BSD on master; commit
> `88f4ff37532f` 2025-02-11 "[KDB-598] Update copyright notice ...
> Update license to kurrent license v1" renames ESLv2 to "Kurrent
> License v1" (Event Store Ltd rebranded to Kurrent, Inc.; the
> `EventStore/EventStore` repo auto-redirects to `kurrent-io/
> EventStore`). Catalog §6 row reads "EventStore (EventStoreDB) |
> BSD-3-Clause (≤23.x); ESLv2 from 24.10 — pattern only"; index §2
> row said `MIT` — standing pre-flip check (KI#6-class pitfall)
> caught the drift in the same §2 edit that flips ref-10-c todo
> → done with the corrected "BSD-3-Clause (≤23.x); ESLv2/Kurrent-
> License-v1 from 24.10 — pattern only" annotation. The "pattern
> only" intake is the correct and safer choice for two reasons:
> (1) ESLv2 §Limitations says "You may not provide the software to
> third parties as a hosted or managed service" — canonsim does not
> host EventStoreDB, so the clause never bites; (2) none of
> EventStoreDB's actual code is useful to us anyway — it is C#/
> gRPC/Jint/Javascript, while canonsim is Python ≥3.11 stdlib-only
> (D-012). What we want is the *architectural pattern*: streams as
> ordered event sub-sequences, `ExpectedVersion` optimistic
> concurrency, projections as fold-from-stream, `$maxAge`/`$maxCount`
> retention, tombstone+scavenge separating logical deletion from
> physical compaction. None of these concepts is copyrightable
> subject matter — they are ideas/mechanics, not expression.

**What it is.** EventStoreDB is an append-only, log-structured
event store where every write targets a named **stream**, every
event carries an `EventId`/`EventType`/`Data`/`Metadata` shape,
every write is gated by an **`ExpectedVersion`** for optimistic
concurrency, and a global ordered **`$all`** stream plus a
JavaScript **projection engine** let you fold events into per-
stream/per-category derived state, with logical deletion by
tombstone and physical compaction by a periodic **scavenge** pass.
The store is the canonical reference implementation of the event-
sourcing mechanics canonsim needs at phase 5 — but every concept
we lift is rendered in Python stdlib, none of the C#/Jint/gRPC/
cluster-gossip code comes with us, and the `(tick, sub_order,
actor_id)` queue key replaces EventStoreDB's opaque TFPos as the
explicit total order for deterministic single-process simulation.

**Concrete mechanics.**

- **`EventRecord`** (`EventStore.Core.Data.EventRecord`,
  server-side event record) — fields: `EventId : Guid`,
  `EventType : string`, `Data : ReadOnlyMemory<byte>`,
  `Metadata : ReadOnlyMemory<byte>`, `EventStreamId : string`,
  `EventNumber : long`, `LogPosition : long`, `CorrelationId :
  Guid`, `TransactionPosition : long`, `TransactionOffset :
  int`, `ExpectedVersion : long`, `TimeStamp : DateTime`,
  `Flags : PrepareFlags`. The constructor copies these from
  an `IPrepareLogRecord` (`EventRecord(long eventNumber,
  IPrepareLogRecord prepare, string eventStreamId, string
  eventType)`). The client-facing analog is `KurrentDB.Client.
  EventData` with `EventId : Uuid`, `Type : string`, `Data :
  ReadOnlyMemory<byte>`, `Metadata : ReadOnlyMemory<byte>`,
  `ContentType : string` — the JSON-vs-binary discriminator is
  `ContentType`, with the only two legal values `application/
  json` and `application/octet-stream`. The pattern: **the
  canonical event tuple that lives in the transaction file —
  four payloads (`EventId`, `EventType`, `Data`, `Metadata`)
  plus bookkeeping for ordering, stream identity, and the
  expected-version at write time**. Lifted into `schemas/
  event.schema.json` as the event record shape — `event_id`
  UUID, `event_type` string enum, `data` JSON object, `meta-
  data` JSON object; INV-1 inversion: `EventStreamId` becomes
  the implicit grouping by `actor_id` in our global log (no
  separate stream-id field).
- **`ExpectedVersion`** (`EventStore.Core.Data.ExpectedVersion`,
  static class, constants) — the optimistic-concurrency
  primitive for writes: `public static class ExpectedVersion
  { public const long Any = -2; public const long NoStream =
  -1; public const long Invalid = -3; public const long
  StreamExists = -4; }`. The modern client SDK rebrands this
  as `KurrentDB.Client.StreamState` (a `readonly struct`)
  with `NoStream = -1`, `Any = -2`, `StreamExists = -4`,
  plus internal `Deleted = -5` and `Tombstoned = -6`, and a
  `StreamState.StreamRevision(ulong value)` factory for the
  exact-version case. Mechanically: every write op (TCP
  `ClientMessage.WriteEvents` / gRPC `Append`) carries an
  `ExpectedVersion`; the storage layer compares it to the
  stream's current `LastEventNumber` and rejects with
  `OperationResult.WrongExpectedVersion` on mismatch. The
  pattern: **the canonical OCC front-door for event-sourced
  writes** — four constants (`Any`, `NoStream`, `Invalid`,
  `StreamExists`) plus the exact-positive-version case cover
  the entire OCC state space for a single-writer-to-a-stream,
  and the write result (`WriteEventsCompleted` with
  `LastEventNumber` + `CurrentVersion`) gives the client the
  next expected version for free. Lifted into `cli/` Intent →
  Event validation front-door — an Intent (proposed write)
  is converted to an Event only after the invariant check
  passes, mirroring the OCC semantics of `ExpectedVersion.
  NoStream` (an actor that should be new) and exact-version
  writes (a known next event number for an actor).
- **`SystemNames`** (`EventStore.Core.Services.SystemNames`,
  static constants for the wire protocol) — three nested
  static classes: `SystemStreams`: `AllStream = "$all"`,
  `SettingsStream = "$settings"`, `PersistentSubscription-
  Config = "$persistentSubscriptionConfig"`, `Scavenges-
  Stream = "$scavenges"`, `ScavengePointsStream = "$scavenge-
  Points"`, `MetastreamOf(s) = "$$" + s`, `IsSystemStream(s)
  = s[0]=='$'`; `SystemMetadata`: `MaxAge = "$maxAge"`,
  `MaxCount = "$maxCount"`, `TruncateBefore = "$tb"`,
  `TempStream = "$tmp"`, `CacheControl = "$cacheControl"`,
  `Acl = "$acl"` with sub-keys `"$r"/"$w"/"$d"/"$mr"/"$mw"`;
  `SystemEventTypes`: `StreamDeleted = "$streamDeleted"`,
  `LinkTo = "$>"`, `StreamMetadata = "$metadata"`,
  `ScavengePoint = "$scavengePoint"`, `ScavengeStarted/
  Completed/ChunksCompleted/MergeCompleted/IndexCompleted`.
  The pattern: **the `$`-prefix is the namespace convention
  for everything not user data; `$all` is the global ordered
  stream (one event-position ordering for the whole DB),
  `$$<stream>` is the metadata side-stream for `<stream>`,
  and `$tb`/`$maxCount`/`$maxAge` are the retention policy
  knobs**. Lifted into canonsim's reserved-namespace convention
  — system events use a reserved `event_type` prefix (`_start`,
  `_end`, `_seed`, `_correction`); user events use unprefixed
  names. The `$all` global stream is the precedent for the
  global JSONL log (INV-1).
- **`StreamMetadata`** (`EventStore.Core.Data.StreamMetadata`)
  — fields: `MaxCount : long?`, `MaxAge : TimeSpan?`,
  `TruncateBefore : long?`, `TempStream : bool?`,
  `CacheControl : TimeSpan?`, `Acl : StreamAcl`. JSON-
  serialized via `ToJsonBytes()` / deserialized via
  `FromJsonBytes(ReadOnlySpan<byte>)` using the `SystemMetadata`
  string keys. Has a static `Empty` and an upgrade path
  `UpgradeMetadata(prepareVersion, metadata)` that maps
  `int.MaxValue` TruncateBefore (V0 sentinel) to `EventNumber.
  DeletedStream`. The pattern: **the per-stream retention
  policy document, stored as a `$metadata` event in the
  metastream `$$<stream>`**; `MaxCount` keeps only the last
  N events visible, `MaxAge` expires events older than T,
  `TruncateBefore` makes events before event number N
  invisible without physical deletion. Soft delete of a
  stream = set `$tb` high; hard delete (tombstone) = set
  `$tb = long.MaxValue`. Lifted into canonsim's runtime log
  retention policy — the three knobs (`MaxAge`, `MaxCount`,
  `TruncateBefore`) are exactly the levers canonsim's log-
  retention policy needs: a per-actor or per-scenario cap on
  visible event count (`MaxCount`), a tick-age cap
  (`MaxAge`), and a logical truncation point (`TruncateBefore`).
- **`EventNumber`** (`EventStore.Core.Data.EventNumber`) —
  `public const long DeletedStream = long.MaxValue; public
  const long Invalid = int.MinValue;`. Used as the `$tb`
  value when a stream is hard-deleted (tombstoned) via
  `ClientMessage.DeleteStream(... bool hardDelete ...)`.
  The pattern: **a tombstone is just a sentinel value of
  `$tb`; the events are still physically in the chunk file
  but reads return `ReadStreamResult.StreamDeleted` because
  the read index sees `$tb == MaxValue` and skips**. The
  tombstone is the logical deletion; **scavenge** is the
  physical compaction. Lifted into INV-5: corrections are
  new events (the logical-deletion analog of a tombstone —
  never mutate, always append), and the offline scavenge is
  a separate pass that compacts the JSONL log into a smaller
  form when the retention policy allows.
- **`PersistentSubscription` + `PersistentSubscriptionCheck-
  pointWriter`** — fields: `SubscriptionId`, `EventSource`
  (an `IPersistentSubscriptionEventSource` — either single-
  stream or `$all`), `GroupName`, `ResolveLinkTos`, plus
  internal `_lastCheckpointedSequenceNumber`,
  `_lastKnownSequenceNumber`, `_nextSequenceNumber`,
  `_outstandingMessages : OutstandingMessageCache`,
  `_pushClients : PersistentSubscriptionClientCollection`.
  `PersistentSubscriptionParams` carries `_checkPointAfter :
  TimeSpan`, `_minCheckPointCount`, `_maxCheckPointCount`,
  `_liveBufferSize`, `_bufferSize`, `_readBatchSize`,
  `_consumerStrategy`, `_streamReader`, `_checkpointReader`,
  `_checkpointWriter`, `_messageParker`, and a derived
  `ParkedMessageStream = "$persistentsubscription-" + event-
  Source + "::" + groupName + "-parked"`. The `Persistent-
  SubscriptionCheckpointWriter` writes the checkpoint to
  stream `"$persistentsubscription-" + subscriptionId +
  "-checkpoint"` as a `SubscriptionCheckpoint` event, with
  `ExpectedVersion.Any` first write then exact-version
  thereafter, and uses a metastream `$$<...>-checkpoint`
  with `StreamMetadata(maxCount: 2)` so only the latest
  checkpoint survives. The pattern: **persistent
  subscriptions are the canonical "fold a stream into a
  downstream consumer with a recoverable position" pattern
  — the checkpoint is itself a tiny event-sourced stream
  with `maxCount=2` so it can only ever hold the latest
  position**. Adapted into canonsim's SQLite incremental
  projection: the SQLite index IS the projection checkpoint
  (the row count / max `event_seq` in the SQLite table is the
  position; on restart, the projection resumes from
  `(SELECT MAX(event_seq) FROM projection_state)`). No
  separate subscription store is needed because INV-1 says
  SQLite is a rebuildable index over the JSONL log — the
  index is the checkpoint.
- **`JintProjectionStateHandler`** — the JS projection
  engine. Uses the **Jint** .NET JS interpreter (`Engine`
  from `Jint`). Constructor registers the four global
  projection functions on the JS realm: `_engine.Realm.
  GlobalObject.FastAddProperty("emit", new ClrFunction-
  Instance(_engine, "emit", Emit, 4), ...);` and similarly
  for `linkTo`, `linkStreamTo`, `copyTo`. State via
  `_state : JsValue`, `_sharedState : JsValue`; methods
  `Load(string? state)`, `GetSourceDefinition()` (returns
  `IQuerySources` via `SourceDefinitionBuilder`), and an
  `_emitted : List<EmittedEventEnvelope>` accumulator.
  The user-supplied projection script defines `init`/
  `state` (fold function) and calls `emit(streamId,
  eventName, body, metadata)` or `linkTo(streamId, event,
  metadata)` to write derived events into output streams.
  The pattern: **a projection is a JavaScript fold-from-
  stream that emits derived events (or link-to references)
  into output streams; the projection engine maintains its
  own `CheckpointTag` so it is restartable**. Adapted into
  `sim/systems/` Python folds (and the `render/` fold) —
  each "projection" is a `def fold(state, event) -> state`
  Python callable, and "emit" is just `yield` or a
  returned list of derived events. The conceptual shape —
  fold-from-stream producing derived state/events — is
  preserved; the scripting runtime is dropped because we
  already live in the host language.
- **`VNodeState`** (`EventStore.Core.Data.VNodeState`,
  enum, the cluster gossip node-state machine): `Initializing
  = 0, DiscoverLeader = 1, Unknown = 2, PreReplica = 3,
  CatchingUp = 4, Clone = 5, Follower = 6, PreLeader = 7,
  Leader = 8, Manager = 9, ShuttingDown = 10, Shutdown =
  11, ReadOnlyLeaderless = 12, PreReadOnlyReplica = 13,
  ReadOnlyReplica = 14, ResigningLeader = 15`. `IsReplica
  (state)` extension covers `CatchingUp|Clone|Follower|
  ReadOnlyReplica`. The gRPC gossip wire type is `Member-
  Info.VNodeState` in `src/Protos/Grpc/gossip.proto`,
  served by `EventStore.Core.Services.Gossip.NodeGossip-
  Service` and seeded via `ClusterVNodeOptionsExtensions.
  WithGossipSeeds(EndPoint[])`. The pattern: **nodes gossip
  `MemberInfo { VNodeState state; bool is_alive; EndPoint
  http_end_point; ... }` to converge on who is `Leader`
  (writes) vs `Follower`/`ReadOnlyReplica` (reads); writes
  are rejected unless the node is `Leader`** — the cluster-
  discovery + leader-election layer. Negative for canonsim:
  irrelevant overhead for a single-process phase-0 sim.
- **`Scavenger<TStreamId>` + `ScavengePoint` + `Scavenge-
  Checkpoint`** (abstract base) — the offline compaction
  engine. `Scavenger` constructor takes `IScavengeState<
  TStreamId>`, `IAccumulator<TStreamId>`, `ICalculator<
  TStreamId>`, `IChunkExecutor<TStreamId>`, `IChunkMerger`,
  `IIndexExecutor<TStreamId>`, `ICleaner`,
  `IScavengePointSource`, plus `_thresholdForNewScavenge :
  int` and `_syncOnly : bool`. `ScavengeAsync(Cancellation-
  Token)` runs as a pipeline of stages: `Accumulate` →
  `Calculate` → `Execute(Chunks)` → `MergeChunks` →
  `Execute(Index)` → `Clean`, each restartable from a
  `ScavengeCheckpoint.{Accumulating, Calculating, Execut-
  ingChunks, MergingChunks, ExecutingIndex, Cleaning,
  Done}` with a `ScavengePoint { position, eventNumber,
  effectiveNow, threshold }` as the cutoff. The driving
  message is `ClientMessage.ScavengeDatabase`, handled by
  `EventStore.Core.Services.Storage.StorageScavenger`,
  which gates the whole thing behind a `_switchChunksLock`.
  The pattern: **scavenge is the physical compaction pass
  that rewrites chunk files to drop tombstoned/expired
  events and rewrites the PTable indexes — strictly offline
  with respect to the live log, restartable from a
  checkpoint, and only runs on `Leader` or `Follower`**.
  Lifted into canonsim's offline JSONL-compaction pass —
  same two-stage Accumulate→Execute pipeline with
  restartable `ScavengeCheckpoint` variants per stage.
- **`ResolvedEvent` + `ReadStreamResult`/`ReadAllResult` +
  `OperationResult`** — the read-side shapes. `ResolvedEvent`
  is a struct with `Event : EventRecord`, `Link :
  EventRecord` (the `$>` link-to event, when present),
  `OriginalEvent = Link ?? Event`, `OriginalStreamId`,
  `OriginalEventNumber`, `OriginalPosition : TFPos?`,
  and factories `ForUnresolvedEvent`, `ForResolvedLink`,
  `ForFailedResolvedLink`. `ReadStreamResult` is `Success=0,
  NoStream=1, StreamDeleted=2, NotModified=3, Error=4,
  AccessDenied=5, Expired=6`. `ReadAllResult` is `Success=0,
  NotModified=1, Error=2, AccessDenied=3, Expired=4`.
  `OperationResult` (write side) is `Success=0, Prepare-
  Timeout=1, CommitTimeout=2, ForwardTimeout=3, Wrong-
  ExpectedVersion=4, StreamDeleted=5, InvalidTransaction=6,
  AccessDenied=7`. The pattern: **link-to events (`$>`)
  let projections reference events in other streams by
  `"<eventNumber>@<streamId>"` (parsed by `SystemEvent-
  Types.EventLinkToEventNumber`), so a "category" projection
  is just a stream of link-to events into the original
  events — `ResolvedEvent` rehydrates the link into the
  original `EventRecord` for the consumer**. Negative for
  canonsim: the link-to event pattern is not lifted (our
  global JSONL log doesn't need a separate link-to event
  type; the `actor_id` field is the link).
- **`WriteEventsCompleted` + `ReadStreamEventsForward-
  Completed`** — the wire result shapes. `WriteEventsCom-
  pleted` fields: `CorrelationId`, `Result : Operation-
  Result`, `Message`, `FirstEventNumber`, `LastEventNumber`,
  `PreparePosition`, `CommitPosition`, `CurrentVersion`.
  `ReadStreamEventsForwardCompleted` fields: `Correlation-
  Id`, `EventStreamId`, `FromEventNumber`, `MaxCount`,
  `Result : ReadStreamResult`, `Events : ResolvedEvent[]`,
  `StreamMetadata`, `NextEventNumber`, `LastEventNumber`,
  `TfLastCommitPosition`, `ReadDirection`, `IsCacheMiss`,
  `LongPollRequest`, `LongPollTimeout`. The pattern: **every
  write returns the post-write `LastEventNumber` and
  `CurrentVersion` (so the client can chain a follow-up write
  with the exact `ExpectedVersion`); reads return the
  resolved events plus the `NextEventNumber` to start the
  next page from — the cursor pattern**. Lifted into `cli/`
  write-result shape — the `Intent → Event` validation
  front-door returns the post-write `event_seq` so the
  caller can chain an Intent with the exact expected
  `event_seq` for the next write (the OCC chain).

**What we take.**

- The `$all` global ordered stream (`SystemStreams.AllStream =
  "$all"`, the single global position-ordered log of every
  event in the DB) is the precedent for `core/queue.py` + the
  global JSONL log — canonsim lifts this into its single
  append-only JSONL event log (the global `state = fold(log)`
  truth per INV-1), with the `(tick, sub_order, actor_id)`
  queue key in `core/queue.py` providing the explicit total
  order that EventStoreDB expresses only as `LogPosition`/
  `CommitPosition` (TFPos).
- The `ExpectedVersion` optimistic-concurrency primitive
  (four constants `Any = -2`, `NoStream = -1`, `Invalid =
  -3`, `StreamExists = -4` plus the exact-positive-version
  case, the `OperationResult.WrongExpectedVersion` rejection,
  the `WriteEventsCompleted` post-write `LastEventNumber` +
  `CurrentVersion`) is the precedent for `cli/` Intent →
  Event validation front-door + `schemas/event.schema.json`
  — an Intent (proposed write) is converted to an Event only
  after the invariant check passes, mirroring the OCC
  semantics of `ExpectedVersion.NoStream` (an actor that
  should be new) and exact-version writes (a known next event
  number for an actor).
- The `StreamMetadata` retention policy (`$maxAge`/`$maxCount`/
  `$tb`, the per-stream retention policy document stored as a
  `$metadata` event in the metastream `$$<stream>`) is the
  precedent for canonsim's runtime log retention policy — the
  three knobs (`MaxAge : TimeSpan?`, `MaxCount : long?`,
  `TruncateBefore : long?`) are exactly the levers canonsim's
  log-retention policy needs: a per-actor or per-scenario cap
  on visible event count (`MaxCount`), a tick-age cap
  (`MaxAge`), and a logical truncation point (`TruncateBefore`).
  These map directly to a runtime retention config object
  keyed off the JSONL log path.
- The tombstone + scavenge pattern (`EventNumber.DeletedStream
  = long.MaxValue` tombstone = logical deletion via `$tb`,
  `Scavenger.ScavengeAsync` Accumulate→Calculate→Chunks→Merge→
  Index→Clean pipeline offline from the live log with
  restartable `ScavengeCheckpoint` variants per stage) is the
  precedent for INV-5 (corrections are new events) + offline
  scavenge — canonsim lifts the exact two-layer separation:
  per INV-5, committed logs are never edited, so a *correction*
  is a new event (the logical-deletion analog of a tombstone —
  never mutate, always append), and the *scavenge* is a
  separate offline pass that compacts the JSONL log into a
  smaller form when the retention policy allows.

**What we adapt.**

- JS projection engine (Jint + `emit`/`linkTo`/`state` globals)
  → Python fold functions in `sim/systems/` (and the `render/`
  fold). EventStoreDB's `JintProjectionStateHandler` runs user-
  supplied JavaScript with `init`/`state` callbacks and four
  global side-effecting functions (`emit`, `linkTo`, `linkStream-
  To`, `copyTo`) that accumulate into `_emitted : List<Emitted-
  EventEnvelope>`. canonsim adapts this by replacing the entire
  Jint/JS layer with native Python fold functions in `sim/
  systems/` (per D-012 stdlib-only): each "projection" is a
  `def fold(state, event) -> state` Python callable, and "emit"
  is just `yield` or a returned list of derived events. The
  conceptual shape — fold-from-stream producing derived state/
  events — is preserved; the scripting runtime is dropped
  because we already live in the host language.
- Persistent subscriptions with checkpoints → SQLite-based
  incremental projection (the SQLite index IS the checkpoint).
  EventStoreDB's `PersistentSubscriptionCheckpointWriter`
  persists the consumer position to a tiny event-sourced stream
  `$persistentsubscription-<id>-checkpoint` with `maxCount=2`,
  restarted via `PersistentSubscriptionCheckpointReader.Begin-
  LoadState`. canonsim adapts this by collapsing the
  subscription + checkpoint into one thing: the SQLite
  incremental-projection index *is* the projection checkpoint
  (the row count / max `event_seq` in the SQLite table is the
  position; on restart, the projection resumes from `(SELECT
  MAX(event_seq) FROM projection_state)`). No separate
  subscription store is needed because INV-1 says SQLite is a
  rebuildable index over the JSONL log — the index is the
  checkpoint.
- C#/gRPC wire protocol + cluster gossip + leader election →
  not applicable (phase 0) / replaced by JSONL file + `random.
  Random(seed)`. EventStoreDB's `NodeGossipService`,
  `VNodeState` enum (Leader/Follower/...), `ExpectedVersion`-
  over-the-wire via gRPC `Append`, and `ClusterVNodeOptions.
  WithGossipSeeds` are all multi-process coordination machinery.
  In canonsim phase 0 there is one process, one `random.Random
  (seed)`, one JSONL file — so the entire wire/cluster layer is
  replaced by direct in-process function calls and a JSONL file
  as the "wire". The single-process determinism (one PRNG,
  integer ticks) makes optimistic concurrency trivial: there is
  no concurrent writer to conflict with, so the `ExpectedVersion`
  check reduces to a schema/invariant check at Intent-validation
  time.

**What inspires us.**

- Every event has a stream it belongs to; the stream is the unit
  of ordering, and `ExpectedVersion` is the unit of concurrency
  on that stream. A global log gives you total order, but per-
  stream `ExpectedVersion` is what makes writes composable and
  idempotent — canonsim's per-actor-id event sub-sequence within
  the global log is the same idea.
- Logical deletion and physical compaction are different
  operations on different timelines. EventStoreDB never edits the
  log to delete; it writes a tombstone (a new event) and runs
  scavenge offline later. This is exactly INV-5's "committed logs
  are never edited; corrections are new events" — the same
  separation, applied to corrections as well as deletions.

**Strengths.**

- `ExpectedVersion` is the canonical optimistic-concurrency
  primitive for event-sourced writes — the four constants
  (`Any = -2`, `NoStream = -1`, `Invalid = -3`, `StreamExists
  = -4`) plus the exact-positive-version case cover the entire
  OCC state space for a single-writer-to-a-stream, and the
  write result (`WriteEventsCompleted` with `LastEventNumber`
  + `CurrentVersion`) gives the client the next expected
  version for free. This is the right primitive to lift into
  `cli/` Intent validation.
- Projections are a declarative fold-from-stream pattern. The
  `JintProjectionStateHandler` shape — `Load(state)`, fold
  over events, `emit` derived events, checkpoint via
  `CheckpointTag` — maps cleanly onto canonsim's `sim/
  systems/` Python folds and the `render/` fold. The
  checkpoint-and-restart pattern is exactly what an
  incremental SQLite projection needs.
- Tombstone + scavenge cleanly separates logical deletion from
  physical compaction — a fit for canonsim's log retention. The
  two-stage Accumulate→Execute pipeline with restartable
  `ScavengeCheckpoint` variants per stage is the right shape
  for an offline JSONL-compaction pass.
- `StreamMetadata` is a small, complete retention vocabulary
  — `MaxAge`/`MaxCount`/`TruncateBefore`/`CacheControl`/
  `TempStream`/`Acl` is enough knobs to express any retention
  policy without inventing new vocabulary. canonsim's runtime
  retention config can be a strict subset of these.
- `$all` + per-stream `$$<stream>` metastream convention — the
  `$`-prefix-as-namespace + `$$`-prefix-as-metastream
  convention is a clean way to separate system data from user
  data and per-stream metadata from per-stream events. canonsim's
  content/code split (content in `content/packs/`, code in
  `sim/`) can reuse the same idea: a reserved namespace prefix
  for system events vs scenario events.

**Weaknesses.**

- The JS projection engine (Jint) is a runtime scripting layer
  — canonsim folds in Python, not JS. Vendoring Jint or writing
  JS projections would violate D-012 (stdlib-only). The pattern
  is portable; the implementation is not. This is the single
  biggest reason "pattern only" is the correct intake.
- Cluster gossip + leader election is irrelevant overhead for a
  single-process phase-0 sim. `VNodeState` (16 enum values),
  `NodeGossipService`, `WithGossipSeeds`, the `Leader`-only-writes
  rule — all of this exists to coordinate multiple processes.
  canonsim has one process and one PRNG; there is no leader to
  elect and no concurrency to serialize. Lifting any of it would
  be cargo-cult.
- ESLv2 license friction at 24.10+ means we cannot vendor the
  source; pattern-only intake is the only path. The no-hosted-
  service clause plus the no-license-key-circumvention clause
  mean that even if we wanted to vendor the C# code (we don't —
  wrong language, wrong runtime), we'd be carrying license-key-
  auditing machinery we don't want. BSD-3-Clause at `oss-v23.10.
  0`/`oss-v24.6.0` would be vendor-safe, but there's nothing in
  the source we need that isn't already expressible as a pattern.
- Persistent subscriptions need a backing store for checkpoints
  — for canonsim, the SQLite index IS the projection checkpoint,
  so a separate subscription store would be redundant.
  EventStoreDB's `PersistentSubscriptionCheckpointWriter`
  writes to a stream `$persistentsubscription-<id>-checkpoint`
  with `maxCount=2` because EventStoreDB doesn't have a separate
  "projection index" concept — the projection emits into output
  streams and the subscription is a separate consumer. canonsim
  collapses these: the SQLite incremental projection is *both*
  the derived state *and* the checkpoint (max row id = position).
  Adding a separate checkpoint stream would be double-bookkeeping.
- The `$all` stream is a global ordered stream — canonsim's
  JSONL log is the equivalent, but our `(tick, sub_order,
  actor_id)` queue key is the explicit tiebreaker EventStoreDB
  doesn't expose. EventStoreDB's `$all` ordering is by `TFPos`
  (commit position + prepare position), an opaque internal
  counter. canonsim needs deterministic reproducibility (INV-2:
  one `random.Random(seed)`, integer ticks), so the queue key
  in `core/queue.py` is an explicit, domain-meaningful total
  order — EventStoreDB's TFPos is unsuitable for that role
  because it leaks storage-layer mechanics into the simulation's
  notion of time.

**Verdict.** Phase-5 event-sourcing pattern-only reference (the
T2 reference — replay tests), the canonical reference
implementation of the event-sourcing mechanics canonsim needs at
phase 5 — `ExpectedVersion` OCC, `$all` global stream,
`StreamMetadata` retention, projections-as-fold, tombstone+
scavenge — but it is a *pattern-only* intake (BSD-3-Clause at
≤23.x is vendor-safe but useless to us; ESLv2/Kurrent-License-v1
at 24.10+ would block vendoring even if we wanted to): every
concept we lift is rendered in Python stdlib, none of the C#/
Jint/gRPC/cluster-gossip code comes with us, and the `(tick,
sub_order, actor_id)` queue key replaces EventStoreDB's opaque
TFPos as the explicit total order for deterministic single-
process simulation. License drift (KI#6-class: catalog said
"BSD-3-Clause (≤23.x); ESLv2 from 24.10 — pattern only"; index
§2 said "MIT") caught pre-flip in the same §2 edit that flips
ref-10-c todo→done. The "every event has a stream it belongs to;
the stream is the unit of ordering; `ExpectedVersion` is the
unit of concurrency on that stream" lesson is the inspiration:
canonsim's per-actor-id event sub-sequence within the global
log is the same idea. The "logical deletion and physical
compaction are different operations on different timelines"
lesson is INV-5's ancestor — the same separation, applied to
corrections as well as deletions.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
