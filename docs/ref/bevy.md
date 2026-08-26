# Bevy · `REFERENCES.md` §7 · MIT OR Apache-2.0 (dual) · phase 5 (ECS patterns, pattern only D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is dual-licensed `MIT OR
> Apache-2.0` (verified 2026-08-26 from the root `Cargo.toml`
> `license = "MIT OR Apache-2.0"` field + `LICENSE-MIT` +
> `LICENSE-APACHE` files + `README.md` §License) — pattern
> lifting is permitted under either; the Rust trait/derive-macro
> code is not useful as a runtime dependency for our Python
> stdlib-only core (D-012). Reference repo: `bevyengine/bevy`
> (active, edition 2024, MSRV 1.95.0). Catalog §7 row reads
> "Bevy | MIT / Apache-2.0 | Rust ECS scheduling model"; index
> §2 row had the matching dual license — no drift this iteration.
> Note on naming: in current `main` (v0.20-dev) Bevy has **renamed
> `Events<T>` → `Messages<M>`** and `EventReader/Writer` →
> `MessageReader/Writer`. The `Event` trait still exists, but it
> now means observer-triggered *immediate* events (via
> `World::trigger`). The double-buffered ring buffer pattern the
> canonsim brief calls "`Events<T>` double buffer" is now
> `Messages<M>` in `crates/bevy_ecs/src/message/`; the pattern is
> unchanged. This is the catalog↔repo drift of the iteration —
> Bevy itself moved; canonsim lifts the *pattern*, not the name.

**What it is.** Bevy ECS (`bevy_ecs` crate) is a data-oriented
registry where the `World` struct owns component-typed `Storages`
(columnar `Table`s + `SparseSet`s), singleton `Resource`s stored
as components on hidden entities, and typed `Query`s are executed
by a dependency-graph `Schedule` of systems that communicate
through `Messages<M>` double-buffered ring buffers, with structural
mutations deferred into a `CommandQueue` flushed at `ApplyDeferred`
sync points. The crate is the canonical Rust ECS reference — the
dual-license is the friendliest Rust crate license, the patterns
(double-buffered ring, build-time ambiguity detection, deferred
commands, declarative FSM) are directly portable to Python
stdlib with INV-1 inversion.

**Concrete mechanics.**

- **`World` struct** (`crates/bevy_ecs/src/world/mod.rs:98`) —
  the central registry; the only mutable root. Fields: `id:
  WorldId` + `entities: Entities` + `entity_allocator:
  EntityAllocator` + `components: Components` + `component_ids:
  ComponentIds` + `resource_entities: ResourceEntities` +
  `archetypes: Archetypes` + `storages: Storages` + `bundles:
  Bundles` + `observers: Observers` + `removed_components:
  RemovedComponentMessages` + `change_tick: AtomicU32` +
  `last_change_tick: Tick` + `last_check_tick: Tick` +
  `last_trigger_id: u32` + `command_queue_start: usize` +
  `command_queue: SyncUnsafeCell<CommandQueue>`. Real methods:
  `spawn<B: Bundle>` (1245), `spawn_empty` (1286), `despawn`
  (1576), `query<D: QueryData>` (1781), `query_filtered<D, F>`
  (1805), `entity(e)` / `entity_mut(e)` (753/879),
  `insert_resource<R: Resource>` (1975), `init_resource<R:
  Resource + FromWorld>` (1962), `get_resource<R>` (2262),
  `resource<R>` / `resource_mut<R>` (2199/2247),
  `remove_resource<R>` (2053), `resource_scope<R, U>` (2793),
  `run_schedule(label)` (3916), `flush()` (3134), `commands()`
  (314). The pattern: **one mutable root owning all state —
  entities, components, resources, archetypes, observers, a
  deferred command queue, and change-tracking ticks**.
  Lifted into `core/store.py` as the central `Store` — but
  INV-1 inversion: the `Store` is *derived* from the JSONL log,
  not the mutable truth.
- **`Component` trait + storage layout** (`crates/bevy_ecs/
  src/component/mod.rs:530`) — `pub trait Component: Send +
  Sync + 'static { const STORAGE_TYPE: StorageType; type
  Mutability: ComponentMutability; fn on_add() -> Option<
  ComponentHook> { None } fn on_insert() -> Option<
  ComponentHook> { None } fn on_discard() -> Option<
  ComponentHook> { None } fn on_remove() -> Option<
  ComponentHook> { None } fn on_despawn() -> Option<
  ComponentHook> { None } fn register_required_components
  (...) {} fn clone_behavior() -> ComponentCloneBehavior {
  ComponentCloneBehavior::Default } fn map_entities<E:
  EntityMapper>(_this: &mut Self, _mapper: &mut E) {} fn
  relationship_accessor() -> Option<ComponentRelationship-
  Accessor<Self>> { None } const HAS_SUMMARY_TICK: bool =
  false; }`. Storage choice enum at `component/mod.rs:763`:
  `pub enum StorageType { #[default] Table, SparseSet }`.
  `Table` storage (`storage/table/mod.rs:204`, with `Column`
  at `table/column.rs:27`, `TableRow(NonMaxU32)` at
  `table/mod.rs:104`): contiguous columnar memory, cache-
  friendly iteration. `SparseSet<I, V>` storage (`storage/
  sparse_set.rs:504`) — the textbook triple `dense: Vec<V>`
  + `indices: Vec<I>` + `sparse: SparseArray<I, NonMaxUsize>`.
  The pattern: **per-component storage layout chosen at
  `#[derive(Component)]` registration via `#[component(storage
  = "SparseSet")]`**. Lifted into `sim/store.py` — negative
  for canonsim: the `SparseSet`/`Table` cache-line rationale
  doesn't survive Python's `dict` overhead; storage collapses
  to `dict[EntityId, dict[ComponentName, dict]]`.
- **`Resource` trait + accessors** (`crates/bevy_ecs/src/
  resource.rs:87`) — `pub trait Resource: Component {}` (a
  marker; a Resource is a singleton Component). Backing:
  `ResourceEntities(SyncUnsafeCell<SparseArray<ComponentId,
  Entity>>)` caches ComponentId→owning-Entity, and
  `IsResource(ComponentId)` marker component (`resource.rs:124`)
  carries `on_insert`/`on_discard`/`on_despawn` hooks that keep
  the cache in sync. System-side accessors: `Res<'w, T: ?
  Sized + Resource>` with `value: &'w T` + `ticks: Component-
  TicksRef<'w>`; `ResMut<'w, T: ? Sized + Resource<Mutability =
  Mutable>>` with `value: &'w mut T` + `ticks: ComponentTicksMut
  <'w>`. The pattern: **a Resource is a Component stored on a
  single hidden entity, so it rides the same archetype/storage
  pipeline as Components**; `Res`/`ResMut` are typed views with
  change-detection ticks attached. Lifted into `core/` per-
  system state — every system closure receives a per-system
  mutable scratch dict (Bevy's `Local<'s, T>` per-system +
  `Res<T>` typed singleton, fused). Fold-rebuildable: scratch
  is regenerated by replaying the log.
- **`Query<'w, 's, D, F>` + filters** (`crates/bevy_ecs/src/
  system/query.rs:487`) — `pub struct Query<'world, 'state, D:
  QueryData, F: QueryFilter = ()> { world: UnsafeWorldCell<
  'world>, state: &'state QueryState<D, F>, last_run: Tick,
  this_run: Tick, }`. Methods: `iter` (678), `iter_mut` (716),
  `par_iter` (1301), `get(entity)` (1722), `get_mut(entity)`
  (1858), `single` (2242), `single_mut` (2271), `as_readonly`
  (547). Filters are zero-sized marker structs in `query/
  filter.rs`: `With<T>` (142), `Without<T>` (253), `Or<T>`
  (370), `Added<T>` (757), `Changed<T>` (996). The trait:
  `pub unsafe trait QueryFilter: WorldQuery { const
  IS_ARCHETYPAL: bool; unsafe fn filter_fetch(state, fetch,
  entity, table_row) -> bool; }`. The pattern: **a typed
  lifetime-tracked view; `init_access` (via `SystemParam`)
  registers a `FilteredAccessSet` per system, and the
  `Schedule` builder cross-checks every pair to flag
  ambiguous (conflicting-access-but-unordered) systems at
  *build* time**. Lifted into `sim/systems/*.py` query helper
  — same shape (typed view, filtered by With/Without/Added/
  Changed), drop the lifetime tracking (Python has no borrow
  checker).
- **`Schedule` + `SystemSet` + `ScheduleLabel`** (`crates/
  bevy_ecs/src/schedule/schedule.rs:391`) — `pub struct
  Schedule { label: InternedScheduleLabel, graph:
  ScheduleGraph, executable: SystemSchedule, executor: Box<
  dyn SystemExecutor>, executor_initialized: bool, }`.
  `ScheduleGraph` (`schedule.rs:757`) carries
  `ambiguous_with: UnGraph<NodeId>` and `ambiguous_with_all:
  HashSet<NodeId>` — the ambiguity-detection edge set.
  Methods: `new(label)` (414), `add_systems(systems)` (439),
  `configure_sets(sets)` (505), `ignore_ambiguity(a,b)` (485),
  `set_apply_final_deferred(bool)` (563), `run(&mut World)`
  (569), `initialize(&mut World)` (610). Ordering combinators
  on `IntoScheduleConfigs`: `.before(...)`, `.after(...)`,
  `.chain()`, `.in_set(...)`, `.ambiguous_with(...)`.
  `SystemSet` and `ScheduleLabel` are label traits generated by
  the `define_label!` macro (`schedule/set.rs:22` and `:62`);
  users write `#[derive(SystemSet)] struct PhysicsSystems;`
  or `#[derive(ScheduleLabel)] struct Update;`. The pattern:
  **declarative dependency graph + automatic build-time
  conflict detection**. Lifted into `sim/systems/__init__.py`
  — systems declare ordering with the same combinator shape;
  `SystemParam::init_access` + `ScheduleGraph::ambiguous_with`
  build-time conflict check is the access-conflict detection
  that guarantees an event-sourced fold has a total,
  deterministic order.
- **`Messages<M>` double-buffered ring** (`crates/bevy_ecs/src/
  message/messages.rs:95`) — `#[derive(Resource)] pub struct
  Messages<M: Message> { pub(crate) messages_a:
  MessageSequence<M>, pub(crate) messages_b: MessageSequence<M>,
  pub(crate) message_count: usize, }`. Methods: `write(M) ->
  MessageId<M>` (125), `write_batch(iter)` (153),
  `write_default()` (168), `get_cursor()` (176),
  `get_cursor_current()` (182), `update()` (193),
  `update_drain()` (208), `oldest_message_count()` (117).
  The double-buffer swap is literally: `pub fn update(&mut
  self) { core::mem::swap(&mut self.messages_a, &mut self.
  messages_b); self.messages_b.clear();
  self.messages_b.start_message_count = self.message_count; }`.
  Writer side (`message/message_writer.rs:62`): `MessageWriter
  <'w, M> { messages: ResMut<'w, Messages<M>> }` with `write`/
  `write_batch`/`write_default`. Reader side (`message/
  message_reader.rs:34`): `pub struct MessageReader<'w, 's,
  M: Message> { pub(super) reader: Local<'s, MessageCursor<M>>,
  #[system_param(validation_message = "Message not
  initialized")] messages: Res<'w, Messages<M>>, }`. Methods:
  `read()` (44), `read_with_id()` (49), `par_read()` (89,
  `multi_threaded`), `len()` (94), `is_empty()` (119), `clear
  ()`. The cursor (`message/message_cursor.rs:54`): `pub
  struct MessageCursor<M: Message> { pub(super)
  last_message_count: usize, pub(super) _marker: PhantomData<M>,
  }`. The pattern: **producers append to buffer B; the per-frame
  `update()` swap A↔B and clears the (now-oldest) B; readers
  carry a per-system `last_message_count` and consume everything
  between their cursor and the global `message_count`, reading
  across both buffers**. Lifted into `core/queue.py` — the
  shape maps 1:1 onto canonsim's `(tick, sub_order, actor_id)`
  queue: the append-only JSONL log IS the producer's buffer
  B; the per-tick `update()` swap is the tick boundary; per-
  system `Local<'s, MessageCursor<M>>` becomes a per-system
  integer-tick cursor. The reader/writer asymmetry (`Res`
  shared read vs `ResMut` exclusive write) is exactly what
  makes a fold deterministic.
- **`Commands` + `CommandQueue` + `Command` trait** — deferred
  mutation. `Command` trait (`system/commands/command.rs:52`):
  `pub trait Command: Send + 'static { type Out:
  CommandOutput; fn apply(self, world: &mut World) -> Self::
  Out; fn handle_error_with(self, eh) -> impl Command<Out = ()>
  where Self: Sized { /* … */ } fn handle_error(self) -> impl
  Command<Out = ()> where Self: Sized { /* … */ } fn
  ignore_error(self) -> impl Command<Out = ()> where Self:
  Sized { /* … */ } }`. `impl<F, Out> Command for F where F:
  FnOnce(&mut World) -> Out + Send + 'static, Out:
  CommandOutput { /* … */ }` — blanket impl for closures.
  `CommandQueue` (`world/command_queue.rs:45`): `pub struct
  CommandQueue { pub(crate) bytes: Vec<MaybeUninit<u8>>,
  pub(crate) caller: MaybeLocation, warn_on_unapplied: bool, }`.
  Methods: `push<C: Command<Out = ()>>(c)` (105), `apply(&mut
  World)` (184). `Commands<'w, 's>` (`system/commands/mod.rs:
  101`): `#[derive(SystemParam)] pub struct Commands<'w, 's>
  { queue: Deferred<'s, CommandQueue>, entities: &'w Entities,
  allocator: &'w EntityAllocator, }`. Methods: `spawn<T:
  Bundle>(bundle)` (267), `entity(e)` (308), `queue(command)`
  (510), `trigger(event)` (1097), `append(other)`,
  `rebound_to(q)`, `reborrow()`. `EntityCommands<'a>` (`mod.rs:
  1232`): `insert(bundle)` (1363), `remove<B>()` (1654),
  `despawn()` (1834), `queue(entity_command)` (1884),
  `trigger(event)` (2286). The flush hook is `SystemParam::
  apply(state, system_meta, world)` (`system/system_param.rs:
  250`) and `SystemBuffer::apply` (`system_param.rs:1053`); the
  `Deferred<'a, T: SystemBuffer>` wrapper (`system_param.rs:
  1185`) is the bridge. The pattern: **parallel systems can't
  hold `&mut World`, so they push `Command` closures into a
  per-system byte-queue; the `Schedule` drains them at
  `ApplyDeferred` sync points** (auto-inserted or explicit
  `.before(ApplyDeferred)`). Adapted into `cli/` Intent →
  Event validation front-door — see "What we adapt" below.
- **`App` + `Plugin` + `States`** — `crates/bevy_app` and
  `crates/bevy_state`. `App` (`bevy_app/src/app.rs:85`): `pub
  struct App { pub(crate) sub_apps: SubApps, pub(crate) runner:
  RunnerFn, fallback_error_handler: Option<ErrorHandler>, }`.
  Methods: `new()` (139), `empty()` (146), `update()` (158),
  `run()` (185), `add_systems(schedule, systems)` (321),
  `configure_sets` (402), `add_message<M: Message>()` (427),
  `insert_resource<R: Resource>` (451), `init_resource<R:
  Resource + FromWorld>` (485), `add_plugins<M>` (655),
  `add_schedule` (1269), `world()` (1181), `world_mut()`
  (1189). `Plugin` trait (`bevy_app/src/plugin.rs:57`): `pub
  trait Plugin: Downcast + Any + Send + Sync { fn build(&self,
  app: &mut App); fn ready(&self, _app: &App) -> bool { true }
  fn finish(&self, _app: &mut App) {} fn cleanup(&self, _app:
  &mut App) {} fn name(&self) -> &str { core::any::type_name::
  <Self>() } fn is_unique(&self) -> bool { true } }`. `impl<T:
  Fn(&mut App) + Send + Sync + 'static> Plugin for T { fn
  build(&self, app) { self(app) } }` — blanket impl for
  closures. `States` trait (`bevy_state/src/state/states.rs:
  64`): `pub trait States: 'static + Send + Sync + Clone +
  PartialEq + Eq + Hash + Debug { const DEPENDENCY_DEPTH:
  usize = 1; }`. Runtime resources (`bevy_state/src/state/
  resources.rs`): `#[derive(Resource)] pub struct State<S:
  States>(pub(crate) S)` with `new(state)` + `get(&self) ->
  &S`; `pub enum NextState<S: FreelyMutableState> {
  #[default] Unchanged, Pending(S), PendingIfDifferent(S), }`
  with `set(&mut self, state: S)` and `set_if_different(&mut
  self, state: S)`. Transitions resolved in a `StateTransition`
  schedule (between `PreUpdate` and `RunFixedMainLoop`), firing
  `OnEnter(variant)` / `OnExit(variant)` schedules. The main
  orchestration schedule is `Main` (`bevy_app/src/main_schedule.
  rs:57`): `Startup → First → PreUpdate → StateTransition →
  RunFixedMainLoop → Update → SpawnScene → PostUpdate → Last`.
  The pattern: **builder-pattern app, pluggable `Plugin::build`,
  and a deferred FSM where state changes are *queued* in
  `NextState<S>` and applied at a known schedule point — never
  mutated mid-system**. Lifted into `sim/systems/` phase
  control (Phase 0 = `tavern`, etc.) — the deferred `set`-then-
  apply-at-schedule-point shape is the correct way for an
  event-sourced sim to switch scenarios mid-fold.
- **`Entity`** (`crates/bevy_ecs/src/entity/mod.rs:424`) —
  `#[repr(C, align(8))] pub struct Entity { index: EntityIndex
  (NonMaxU32), generation: EntityGeneration(u32), }` packs to
  a `u64`; reused indices bump generation. The pattern:
  **generational entity ID — index recycled on despawn,
  generation distinguishes stale references**. Same as entt
  (`entt.md`) — both inherit the same canonical shape;
  canonsim lifts this into `core/ids.py` once.

**What we take.**

- The `Messages<M>` double-buffer (`messages_a` + `messages_b`
  + `message_count` + `update()` swap-clear + per-reader
  `MessageCursor.last_message_count`, messages.rs:95) is the
  precedent for `core/queue.py` — the shape maps 1:1 onto
  canonsim's `(tick, sub_order, actor_id)` queue: the append-
  only JSONL log IS the producer's buffer B; the per-tick
  `update()` swap is the tick boundary; per-system `Local<'s,
  MessageCursor<M>>` becomes a per-system integer-tick cursor.
  The reader/writer asymmetry (`Res` shared read vs `ResMut`
  exclusive write) is exactly what makes a fold deterministic.
- The `Schedule` + `SystemSet` + `before/after/chain/in_set` +
  `ambiguous_with` graph (schedule.rs:391, 757) is the
  precedent for `sim/systems/__init__.py` — systems declare
  ordering with the same combinator shape; `SystemParam::
  init_access` registering a `FilteredAccessSet` and the
  `ScheduleGraph::ambiguous_with` build-time conflict check
  is the access-conflict detection that guarantees an event-
  sourced fold has a total, deterministic order.
- The `Resource` singleton + `Local<'s, T>` per-system state
  (resource.rs:87, system_param.rs) is the precedent for
  `core/` per-system state — every system closure receives a
  per-system mutable scratch dict (Bevy's `Local<'s, T>` fused
  with `Res<T>`). Fold-rebuildable: scratch is regenerated by
  replaying the log.
- The `States` FSM (`State<S>` + `NextState<S>` enum
  `Unchanged/Pending/PendingIfDifferent` + `set(S)` queues,
  `StateTransition` schedule applies + fires `OnEnter`/`OnExit`,
  states.rs:64, resources.rs) is the precedent for `sim/
  systems/` phase control (Phase 0 = `tavern`, etc.) — the
  deferred `set`-then-apply-at-schedule-point shape is the
  correct way for an event-sourced sim to switch scenarios
  mid-fold: queue a transition event, apply at the tick
  boundary, fire enter/exit hooks in deterministic order.

**What we adapt.**

- `Commands` / `CommandQueue` deferred mutation → events-only
  state changes per INV-1. Bevy: a `System` pushes `Command`
  closures into `CommandQueue` (`Vec<MaybeUninit<u8>>`); the
  `Schedule`'s `ApplyDeferred` sync point calls `Command::apply
  (self, &mut World)` to mutate the World. canonsim adaptation:
  there is **no `&mut World`** for systems to touch — INV-1
  forbids direct state mutation. So `Command::apply` becomes
  *"serialize the command to event JSON, append to the JSONL
  log, advance tick"*. The deferred-buffer *shape* survives
  (`Deferred<'s, CommandQueue>` → a per-system append buffer);
  the deferred-target changes from "mutable World" to "append-
  only event log". `schemas/event.schema.json` becomes the
  type-tag + shape validator that `CommandMeta`'s vtable fn-
  pointer used to be.
- Rust traits + derive macros (`#[derive(Component)]`,
  `#[derive(Resource)]`, `#[derive(Message)]`, `#[derive
  (States)]`, `#[derive(SystemSet)]`) → Python plain
  dataclasses + JSON packs. Bevy's compile-time guarantees —
  `Component::STORAGE_TYPE` const, `Component::Mutability`
  sealed-trait, `SystemParam::init_access` panic-on-conflict,
  `QueryFilter::IS_ARCHETYPAL` const-eval — all vanish in
  Python. canonsim replaces them with: plain `@dataclass`
  types in `core/`, a JSON Schema (`schemas/event.schema.
  json`) for message/event shape validation, and the content/
  code split (D-015: no domain words in core code). Domain
  words that Bevy bakes into Rust type names (`Player`,
  `Inventory`, `GameState::InGame`) get pushed into `content/
  packs/*.json` instead — the `Component` trait becomes a
  registry keyed by string name, not by `TypeId`.
- `SparseSet`/`Table` storage layout + `&World`/`&mut World`/
  `UnsafeWorldCell` access discipline → not relevant. Bevy's
  two storage strategies and its entire aliasing discipline
  (`UnsafeWorldCell`, `SyncUnsafeCell`, the `FilteredAccessSet`
  runtime check) exist to satisfy Rust's borrow checker for
  zero-overhead *parallel* iteration. canonsim is single-
  threaded (a fold must be serial to be reproducible) and
  Python has no borrow checker; the storage layer collapses
  to `dict[EntityId, dict[ComponentName, dict]]` with the
  JSONL log as ground truth. The `SparseSet` triple-array trick
  is not lifted — its cache-line rationale doesn't survive
  Python's `dict` overhead.

**What inspires us.**

- Separate the write-half from the read-half. `Messages<M>::
  write` mutates buffer B; `MessageCursor::read` reads both
  A and B without writing — the asymmetry cleanly separates
  "what happened this tick" (the log) from "what does state
  look like now" (the fold), which is exactly canonsim's event-
  log vs derived-state split.
- Declarative ordering beats imperative calls. Systems declare
  `.before(X).after(Y).in_set(Physics)` rather than calling
  each other; the `Schedule` graph + `ambiguous_with` analysis
  tells you at *build* time if two systems would race — the
  design pressure that makes a fold deterministic: if the build
  initializes, the order is total.

**Strengths.**

- Per-component storage strategy choice. `StorageType::Table`
  (default; `Table`+`Column`+`TableRow`, contiguous columnar
  memory for cache-friendly iteration) vs `StorageType::
  SparseSet` (the textbook triple `dense`/`indices`/`sparse`
  for fast insert/remove), selected at the `#[derive(Component)]`
  site via `#[component(storage = "SparseSet")]`.
- Build-time ambiguity detection. `ScheduleGraph` carries
  `ambiguous_with: UnGraph<NodeId>` + `ambiguous_with_all:
  HashSet<NodeId>`; each `SystemParam::init_access` registers
  a `FilteredAccessSet`; the `Schedule::initialize` build
  phase cross-checks every pair of systems and **errors at
  build time** on conflicting access without declared ordering
  — a mis-ordered schedule fails to initialize rather than
  racing.
- Clean producer/consumer split in `Messages<M>`.
  `MessageWriter` = `ResMut` (exclusive write to buffer B);
  `MessageReader` = `Local<MessageCursor>` (per-system
  `last_message_count`) + `Res<Messages<M>>` (shared read
  across both A and B). Multiple readers consume the same
  stream independently and in parallel; the `update()` swap-
  clear is a 4-line O(1) tick boundary.
- Deferred FSM via `State<S>` + `NextState<S>`.
  `next_state.set(X)` queues; the `StateTransition` schedule
  applies at a known point, firing `OnEnter`/`OnExit` sub-
  schedules. No mid-system state thrash; transitions are
  total-ordered with the rest of the schedule.
- Heterogeneous deferred command queue. `CommandQueue` packs
  `CommandMeta`+command-bytes into a single `Vec<MaybeUninit
  <u8>>` with a vtable fn-pointer per command type — zero-
  allocation push, single-pass drain at `ApplyDeferred`. Lets
  parallel systems queue structural mutations without holding
  `&mut World`.

**Weaknesses.**

- Rust-only runtime dependency — forbidden by D-012.
  `bevy_ecs` is a Rust crate (edition 2024, MSRV 1.95.0);
  canonsim is Python ≥3.11 stdlib-only. Bevy enters as
  **patterns only**, never vendored — D-015 pattern-lifting,
  not code-lifting.
- In-place mutable components violate INV-1. Bevy's `ResMut<T>`
  (field `value: &'w mut T`) and `Query<&mut T>` mutate state
  *in place*; canonsim's invariant is that every state change
  is an event appended to the log and state = fold. The borrow-
  checker discipline that makes Bevy's mut safe is precisely
  what we must NOT lift — we lift the *shape* of the deferred-
  mutation queue (`Commands`/`CommandQueue`), not its mutable-
  target (`&mut World`).
- Compile-time trait system + derive macros don't translate
  to Python. `Component::STORAGE_TYPE`, `Component::
  Mutability`, `SystemParam::init_access`, `QueryFilter::
  IS_ARCHETYPAL`, `States::DEPENDENCY_DEPTH` are all const-
  evaluated at compile time and gated by `unsafe impl`s;
  lifting to Python loses the type-safety guarantees (storage
  selection, accessor codegen, ambiguity detection, mutability
  sealing) — they degrade to runtime checks or JSON-Schema
  validation.
- `async_executor` / `multi_threaded` not relevant to phase-0
  single-threaded sim. `MultiThreadedExecutor`,
  `MessageParIter`, `QueryParIter`, `bevy_tasks` thread pool,
  `par_read()` are dead weight for a deterministic fold (a
  reproducible fold must be serial). The default `bevy_ecs`
  features even turn `async_executor` on by default.
- SparseSet/Table memory layout pointless in Python. The
  dense `Vec<V>` + sparse `Vec<Option<V>>` trick and `Table`'s
  columnar `Column`+`TableRow` exist for cache-line locality
  under Rust's allocator; Python's `dict` overhead dominates
  and there's no contiguous-iteration win to capture. Lifting
  them buys nothing.

**Verdict.** Phase-5 ECS pattern-only reference (D-012), the
primary pattern source for canonsim's Phase 5 ECS layer —
specifically its `Messages<M>` double-buffer (→ `core/queue.py`),
its `Schedule`+`SystemSet`+`ambiguous_with` declarative ordering
(→ `sim/systems/`), its `Resource`/`Local` per-system-state
fusion (→ `core/` per-system scratch), and its `States` deferred
FSM (→ `sim/systems/` phase control) — adapted by replacing
`&mut World` mutation with append-only-event-log folding (INV-1)
and Rust derive-macro type-safety with Python dataclasses +
JSON Schema under D-012/D-015. Dual `MIT OR Apache-2.0` license
(verified 2026-08-26 from the root `Cargo.toml` field + both
LICENSE files) — zero friction at intake. The "separate the
write-half from the read-half" lesson (`Messages<M>` asymmetry)
is the inspiration: the JSONL log IS the write-half, the fold
IS the read-half. The "declarative ordering beats imperative
calls" lesson (`Schedule` graph + `ambiguous_with` build-time
conflict detection) shapes `sim/systems/__init__.py` system
registration.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
