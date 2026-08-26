# entt · `REFERENCES.md` §7 · MIT · phase 5 (ECS patterns, pattern only D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is MIT (verified 2026-08-26
> from the repo `LICENSE` file header: "The MIT License (MIT) —
> Copyright (c) 2017-2026 Michele Caini, author of EnTT") —
> pattern lifting is permitted per §0.4; the C++ template code
> is not useful as a runtime dependency for our Python stdlib-only
> core (D-012), but the ECS shape (sparse-set storage, view/
> group queries, organizer DAG, sigh hooks, meta reflection) is
> the canonical structural blueprint. Reference repo:
> `skypjack/entt` (active, C++20). Catalog §7 row reads "entt |
> MIT | C++ ECS — component / system design"; index §2 row had
> the matching license — no drift this iteration. Documentation
> is CC-BY 4.0, logos are CC-BY-SA 4.0 — neither relevant to
> code use.

**What it is.** entt is a header-only modern-C++ (C++20)
entity-component-system library providing `registry`/`storage`/
`view`/`group`/`organizer` plus RTTI (`meta`), signals
(`sigh`/`delegate`/`sink`), and process/resource/graph utilities
for game programming. The library is the canonical reference for
the sparse-set ECS storage layout: components are stored in
per-type paged sparse-set arrays indexed by entity id, queries
are zero-allocation views over the smallest pool, system ordering
is a build-time DAG built from declared `ro`/`rw` access sets,
and reactive hooks (`on_construct`/`on_update`/`on_destroy`) are
sigh-based listeners attached to storage mixin.

**Concrete mechanics.**

- **`entity` id + version packing** (`entity/entity.hpp:15`).
  `enum class entity : id_type` (opaque 32-bit integral).
  `entt_traits<Entity>` exposes `entity_mask = 0xFFFFF` (20 bits
  for the entity index) + `version_mask = 0xFFF` (12 bits for
  the recycling generation) + `page_size = ENTT_SPARSE_PAGE`
  (default 4096). Methods: `to_integral`, `to_entity`,
  `to_version`, `construct(entity, version)`, `next(value)`,
  `combine(lhs, rhs)`. The pattern: **pack an id + a generation
  in one int so recycled handles are distinguishable** — a stale
  reference to a recycled entity fails `==` against the new
  entity at the same index. Lifted into `core/ids.py` actor id
  type: a stable `(id, generation)` so recycled actor handles
  are detectable in the `(tick, sub_order, actor_id)` queue key
  without a lookup.
- **`null` / `tombstone` sentinels** (`entity/entity.hpp:218,
  253`). `inline constexpr null null{}` and `inline constexpr
  tombstone tombstone{}`. Each has `template<entity_like Entity>
  operator Entity() const noexcept` returning `traits_type::
  construct(entity_mask, version_mask)` (all-ones). The
  pattern: **type-safe sentinels for "no entity" and "empty
  slot"** — convertible to any entity-like type, distinguishable
  from real entities by value. Lifted into `core/ids.py` as
  `NULL_ACTOR` / `TOMBSTONED_ACTOR` sentinels (no Python
  equivalent of constexpr, plain class-level constants).
- **`basic_sparse_set<Entity, Allocator>`** (`entity/sparse_
  set.hpp:139`) — fields: `sparse_container_type sparse`
  (vector of page pointers) + `packed_container_type packed`
  (vector of `Entity`) + `const type_info* descriptor` +
  `deletion_policy mode` + `size_type head` (free-list cursor).
  Methods: `try_emplace(entt, force_back, value=nullptr)`,
  `swap_and_pop(entt)`, `in_place_pop(entt)`, `swap_only(entt)`,
  `pop(first,last)`, `extent()`, `free_list()`, `policy()`,
  `index(entt)`, `contains(entt)`. The dual-array indirection:
  `sparse[page][offset]` holds a packed index; `packed[packed_
  index]` holds the entity. O(1) membership/lookup + linear
  iteration over `packed`. The pattern: **a sparse array (id →
  packed index) + a packed array (packed index → entity) for
  O(1) membership + linear iteration** — the canonical sparse-
  set layout. Lifted into `core/store.py` (or `sim/store.py`)
  as `dict[actor_id → int]` sparse + `list[actor_id]` packed;
  Python drops the page optimization (a plain dict beats paged
  4096-pointer arrays in CPython) but preserves the dual-array
  shape.
- **`deletion_policy` enum** (`entity/fwd.hpp:18`) — `swap_and_
  pop = 0` (reorders; fast, unstable iteration), `in_place = 1`
  (writes a tombstone; stable iteration, free-list via `head`),
  `swap_only = 2` (stable refs + version bumps), `unspecified =
  swap_and_pop`. The pattern: **per-storage choice of how `pop`
  recycles slots** — trade iteration stability vs write speed
  per-component. `in_place` is what makes `view` iteration safe
  during structural changes (via the tombstone check).
- **`basic_storage<Type, Entity, Allocator>`** (`entity/storage.
  hpp:208`) — public `basic_sparse_set<Entity,...>`; adds
  `container_type payload` (vector of page pointers to `Type`,
  parallel to `packed`). Methods: `emplace(entt, args...)`,
  `get(entt)`, `get_as_tuple(entt)`, `insert(first, last,
  value)`, `patch(entt, func...)`, `each()`, `raw()`. The
  payload is paged: `payload[pos / page_size][fast_mod(pos,
  page_size)]`. The pattern: **a typed component pool laid out
  as paged arrays indexed by the sparse set's packed slot** —
  the canonical component storage. `swap_or_move` keeps
  `payload` and `packed` in sync on swap. Lifted into `sim/
  store.py` as a per-component `dict[actor_id → @dataclass T]`
  — INV-1 inversion: the `Storage` is *derived* (a fold over
  the JSONL log), not authoritative; `emplace`/`patch` are
  events, not in-place mutations.
- **`basic_registry<Entity, Allocator>`** (`entity/registry.
  hpp:211`) — fields: `pool_container_type pools` (dense_map
  <id_type, shared_ptr<base_type>>) + `group_container_type
  groups` + `base_type entities` (the registry IS-A sparse_set
  for entity ids) + `context vars` (dense_map<id_type,
  basic_any>). Methods: `create()`, `destroy(entt)`, `valid
  (entt)`, `current(entt)`, `emplace<Type>(entt, args...)`,
  `get<Type...>(entt)`, `get_or_emplace<Type>`, `try_get`,
  `view<Type..., Exclude...>()`, `group<Owned, Get, Exclude>
  ()`, `on_construct<Type>()`, `on_destroy<Type>()`, `clear
  ()`, `compact()`, `storage()`. `assure<Type>()` lazily creates
  a `storage_for_type<Type>` keyed by `type_hash<Type>::value
  ()` and binds it to the registry via `cpool->bind(*this)`.
  The pattern: **a registry IS-A sparse_set of entity ids +
  a dense map of typed component pools + a context map for
  untyped singletons**. Lifted into `core/store.py` as the
  store owner — every component type gets a `Storage` keyed
  by string name (from `content/packs/*.json`), not by C++
  `type_hash`.
- **`basic_view<get_t<Get...>, exclude_t<Exclude...>>`**
  (`entity/view.hpp:410`) — inherits `basic_common_view`
  (holding `std::array<const Type*, Get> pools` + `std::array
  <const Type*, Exclude> filter` + `size_type index`).
  Methods: `each(func)`, `size_hint()`, `contains(entt)`,
  `get(entt)`, `use<Index>()`, `storage<Index>()`, `refresh
  ()`. The "smallest pool leads" heuristic: `unchecked_refresh
  ()` picks the smallest pool as the lead; `view_iterator::
  valid` filters via `all_of(pools, entt) && none_of(filter,
  entt)`. The pattern: **a zero-allocation view over N pools
  with a smallest-pool-leads optimization for multi-component
  queries** — iterate the smallest pool, filter membership in
  the others. Lifted into `sim/systems/*.py` query helper:
  `View(lead: Storage, included: tuple[Storage,...], excluded:
  tuple[Storage,...])` with `__iter__` filtering by membership.
- **`basic_group<owned_t<Owned...>, get_t<Get...>, exclude_t
  <Exclude...>>`** (`entity/group.hpp:687`) backed by
  `class group_handler` (group.hpp:96) — fields: `std::array
  <common_type*, Owned+Get> pools` + `std::array<common_type*,
  Exclude> filter` + `size_t len`. Methods: `push_on_construct
  (entt)`, `push_on_destroy(entt)`, `remove_if(entt)`,
  `swap_elements(pos, entt)`, `length()`, `storage<Index>()`,
  `owned(id)`. The pattern: **an eagerly maintained intersection
  of N owned storages** — the handler connects `on_construct`/
  `on_destroy` of each owned pool and swaps offending entities
  to the back so the first `len` slots of every owned pool are
  the group. O(1) iteration; *invalidates* on structural change
  during iteration. Negative for canonsim: not lifted directly
  (queue-based tick discipline sidesteps invalidation, but
  `group` requires a deferred-mutation rule).
- **`basic_organizer<Registry>`** (`entity/organizer.hpp:120`)
  — fields: `std::vector<vertex_data> vertices` + `flow
  builder`. `vertex_data` (organizer.hpp:125): `size_t
  ro_count`, `rw_count`, `const char* name`, `const void*
  payload`, `callback_type* callback`, `dependency_type*
  dependency`, `prepare_type* prepare`, `const type_info*
  info`. Methods: `emplace<Candidate, Req...>(name)`,
  `emplace<Candidate, Req..., Type>(instance, name)`,
  `emplace(func, payload, name)`, `graph()` returning `std::
  vector<vertex>` with `in_edges()`/`out_edges()`/`top_level
  ()`. Resource extraction via `internal::unpack_type`
  (organizer.hpp:39-80) splits each function parameter into
  `ro`/`rw` lists; `sync_point` flag is set when a parameter is
  `Registry&` itself. The pattern: **a static task graph
  builder that topologically orders systems by declared read/
  write component sets**. Lifted into `sim/systems/__init__.py`
  (or `core/scheduler.py`): register each system with declared
  `reads`/`writes` component sets, build a DAG, topologically
  order so writers of component C run after readers.
- **`sigh<Ret(Args...)>` + `sink` + `connection`** (`signal/
  sigh.hpp:54, 23, 227`) — `sigh` holds `container_type calls`
  (a `std::vector<delegate<Ret(Args...)>>`). Methods:
  `publish(args...)` (iterates `calls` in reverse),
  `collect(func, args...)` (short-circuit collection), `size
  ()`, `empty()`. `sink` is a builder RAII that inserts/removes
  delegates; `connection`/`scoped_connection` are release
  handles. `class basic_sigh_mixin final: public Type`
  (`entity/mixin.hpp:60`) wraps a storage and publishes
  `construction`/`update`/`destruction` signals in
  `try_emplace`, `pop`, `pop_all`. The pattern: **a single-
  target type-erased callable list + RAII builder + scoped
  connections + a storage mixin that auto-publishes lifecycle
  hooks**. Lifted into `sim/events.py` (or `sim/systems/hooks.
  py`): the *shape* (subscribe to a category, get a release
  handle) is preserved, but the source of truth inverts — the
  JSONL event log *is* the signal stream, and a system
  subscribes to event types it cares about (event types, not
  component lifecycle).
- **`meta_type` / `meta_factory` / `meta_any`** (`meta/meta.
  hpp:1026, fwd.hpp:30`) — runtime reflection. `meta_factory<T>`
  (factory.hpp) registers `data<...>`, `func<...>`, `base<
  ...>`, `conv<...>`, `ctor<...>` against a `meta_ctx`.
  `meta_type` exposes `data(id, recursive=true)`, `func(id,
  recursive=true)`, `base()`, `construct(args...)`, `invoke
  (id, instance, args...)`, `is_class()`/`is_enum()`/
  `is_arithmetic()`, `from_void(elem)`. The pattern: **a
  separately-built symbol table over C++ types, so JSON/script
  code can drive entity/component mutation at runtime**.
  Registration is opt-in and keyed by `id_type`. Lifted into
  `content/packs/*.py` loader: register component schemas
  (fields + types) at startup from JSON packs, then materialize
  typed dataclasses. Negative for canonsim: do NOT port `meta`
  verbatim — `dataclasses` + `getattr`/`setattr` is more
  ergonomic in Python; only the *registration shape* is lifted.

**What we take.**

- The sparse-set two-array layout (`sparse` + `packed`,
  sparse_set.hpp:142-143) is the precedent for `core/store.py`
  — a `dict[actor_id → int]` sparse + a `list[actor_id]`
  packed gives O(1) membership/iteration. Python drops the
  page optimization but preserves the dual-array shape.
- The view-based query (`basic_view`'s smallest-pool-leads +
  `all_of`/`none_of` filter, view.hpp:410, 221-231, 68) is the
  precedent for `sim/systems/*.py` query helper — `View(lead:
  Storage, included: tuple[Storage,...], excluded: tuple[
  Storage,...])` with `__iter__` filtering by membership.
- The `organizer` DAG (`vertex_data{ro_count, rw_count,
  callback, dependency}` + `graph()` returning an adjacency
  list, organizer.hpp:120-310) is the precedent for `sim/
  systems/__init__.py` (or `core/scheduler.py`) — register
  each system with declared `reads`/`writes` component sets,
  build a DAG, topologically order so writers of C run after
  readers.
- The `sigh` + `sink` + `connection` + `basic_sigh_mixin`
  pattern (sigh.hpp:54, mixin.hpp:60-119) is the precedent for
  `sim/events.py` / `sim/systems/hooks.py` — subscribe to a
  category, get a release handle; INV-1 inversion: the JSONL
  event log is the signal stream, not the in-place mutation
  callbacks.
- The `entity` id+version packing (`entt_traits::entity_mask`/
  `version_mask`/`construct`/`next`, entity.hpp:38-170) is the
  precedent for `core/ids.py` actor id type — a stable `(id,
  generation)` so recycled actor handles are distinguishable
  in the queue key.
- The `meta_factory<T>` registration shape (meta/meta.hpp:1026,
  factory.hpp) is the precedent for `content/packs/*.py` loader
  — register component schemas (fields + types) at startup
  from JSON packs, then materialize typed dataclasses.

**What we adapt.**

- C++ templates → Python plain classes. `template<typename
  Type> basic_storage<Type,...>` (storage.hpp:208) becomes
  `class Storage[T]` keyed by `type[T]` (or a string name from
  JSON). The storage *shape* (sparse + packed + payload) is
  preserved, but the payload is a `list[T]` of `@dataclass`es,
  not `void*` paged arrays. We lose compile-time type checks
  (every `get` returns `T`, unchecked at runtime); we gain
  stdlib-only compliance and content-driven component types.
- Mutable component storage → events-only state changes
  (INV-1). entt's `storage.emplace/erase/patch` mutate
  `payload` in place (storage.hpp:243, 319-338); `sigh_mixin::
  pop` publishes `destruction` *during* the mutation
  (mixin.hpp:82). In canonsim the `Storage` is *derived* — a
  fold over the JSONL event log; writes go through `core.
  event_log.append(event)`, and the `sigh` `on_construct`/
  `on_destroy` callbacks become *event handlers* invoked
  during log replay, not mutation callbacks. Same query API
  (`view.each`), inverted authority.
- `organizer` signature-inferred `ro`/`rw` → declared data.
  entt's `unpack_type` (organizer.hpp:39-91) inspects C++
  function parameter constness to infer read-only vs read-
  write resource sets. canonsim cannot do this in Python (no
  const); each system dataclass declares `reads: tuple[str,
  ...]` / `writes: tuple[str, ...]` *as data loaded from JSON
  packs*. Loses signature inference, gains D-012 compliance
  (the access spec is content, not code).
- The `group` (eagerly maintained intersection, invalidates
  on structural change) is not adopted — queue-based tick
  discipline sidesteps the invalidation; the `view` pattern
  (lazy, smallest-pool-leads) is sufficient.

**What inspires us.**

- Storage is the unit; queries are zero-allocation views over
  storage. canonsim keeps per-component stores as the only
  stateful objects; systems receive ephemeral query objects
  and never own a slice of state.
- Generation bits baked into the identifier make recycling
  free — actor ids carry a generation so stale queue entries
  referencing a destroyed actor are detectable without a lookup.

**Strengths.**

- Header-only, zero ABI/link friction — `single_include/entt/
  entt.hpp` is the entire library; matches canonsim's D-012
  "patterns not packages" stance perfectly.
- Sparse-set gives O(1) `contains`/`index`/`erase` + cache-
  friendly linear iteration over `packed`; paged `sparse`
  (4096-entry pages) bounds memory for sparse entity-id
  spaces.
- Three deletion policies (`swap_and_pop`/`in_place`/
  `swap_only`, fwd.hpp:18) let callers trade iteration
  stability vs write speed per-component — `in_place` is
  what makes `view` iteration safe during structural changes
  via the tombstone check (view.hpp:69).
- View's "smallest pool leads" heuristic (view.hpp:221-231)
  gives near-optimal multi-component query iteration for
  free, no planner.
- `sigh`+`sink`+scoped `connection` give RAII lifecycle for
  per-component hooks, and `basic_sigh_mixin` (mixin.hpp:60)
  auto-publishes `on_construct`/`on_update`/`on_destroy` on
  any storage — the ECS "reactive system" pattern in <300
  lines.
- `organizer` builds a task DAG from declared `ro`/`rw`
  resources and returns a topologically-sorted adjacency list
  (`graph()`, organizer.hpp:402) — solves system ordering
  without a runtime scheduler.

**Weaknesses.**

- C++ only — runtime dependency forbidden by D-012. Even the
  single header is C++20 template code; cannot be imported by
  Python. Only the *shape* is portable under D-015.
- No event sourcing — components are mutable. `basic_storage::
  emplace`/`erase`/`patch` (storage.hpp:668, 319, 686) write
  `payload` in place; INV-1 inverts this: every canonsim state
  change must be an appended JSONL event, and the storage is
  derived, not authoritative.
- Template-heavy API surface — `basic_view<get_t<storage_for
  <const T>...>, exclude_t<...>>` (fwd.hpp:278), `entt_traits`,
  `type_list_transform_t`, `connect_arg_t`, `unpack_type` —
  relies on C++20 concepts and template metaprogramming that
  have no direct Python port; the compile-time type safety is
  precisely what gets lost.
- Group iteration invalidates on structural change —
  `group_handler::push_on_construct` reorders owned storage
  (group.hpp:99-110); mutating during iteration corrupts the
  contiguous prefix. canonsim's queue-based tick discipline
  sidesteps this, but `group` cannot be adopted directly
  without a deferred-mutation rule.
- `meta` reflection is verbose and string-keyed at the
  boundary — `meta_type::data(id, recursive)` / `invoke(id,
  instance, args...)` (meta.hpp:1313, 1386) lose C++ type
  safety and depend on a registered `meta_ctx`. For a stdlib-
  only Python project, `dataclasses` + `getattr`/`setattr`
  is *more* ergonomic, so porting `meta` verbatim is a net
  negative — only the *registration shape* is worth taking.

**Verdict.** Phase-5 ECS pattern-only reference (D-012),
the canonical structural blueprint for the ECS *shape* (sparse-
set storage, view queries, organizer DAG, sigh hooks, meta
reflection registration) that canonsim ports as Python stdlib
patterns under D-012/D-015 — never as a dependency, always as a
structural reference — with the single largest inversion being
that its mutable in-place storage becomes event-sourced derived
state per INV-1. MIT license (verified 2026-08-26 from the repo
`LICENSE` file header) — no friction at intake. The "storage is
the unit; queries are zero-allocation views over storage"
lesson is the inspiration: canonsim keeps per-component stores
as the only stateful objects, systems receive ephemeral query
objects. The `organizer` DAG pattern (topologically order
systems by declared `ro`/`rw` access sets) is the precedent for
`sim/systems/__init__.py` system registration.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
