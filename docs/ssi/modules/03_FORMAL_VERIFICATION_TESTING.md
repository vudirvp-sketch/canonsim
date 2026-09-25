## 30. FORMAL SPECIFICATION: КОГДА ТЕСТОВ НЕДОСТАТОЧНО

Для сложных lifecycle/concurrency/authorization/distributed-протоколов сначала задавать допустимое пространство поведения как модель.

```text
intent
→ state machine / temporal relation
→ invariant + liveness assumption
→ model checking
→ implementation
→ conformance / refinement evidence
```

Ключевые конструкции: `safety` · `liveness` · `fairness` · `refinement` · `temporal logic` · `model checking` · `state-space exploration`.

Практический стек высокого уровня: `TLA+ / TLC`, `Alloy`, typestate/refinement types, bounded model checking, symbolic execution.

### 30.1 Safety ≠ Liveness

`Safety`: «плохое никогда не происходит».  
`Liveness`: «хорошее в конце концов происходит при оговорённых progress assumptions».

Нельзя писать:

```text
system eventually processes request
```

без явного условия прогресса: scheduler fairness, доступность dependency, отсутствие perpetual contention и т.п.

**Правило:**

> Любая material liveness-claim обязана назвать progress assumptions; любая material safety-claim — invariant, который запрещает bad state.

---

## 31. STATIC SEMANTIC ANALYSIS: ПРОВЕРЯЙ ПРАВИЛА ДО RUNTIME

Архитектурные правила должны опускаться как можно ближе к машине:

```text
AST / IR
→ control-flow
→ data-flow
→ dependency analysis
→ taint / capability analysis
→ abstract interpretation
→ symbolic execution
→ policy verdict
```

Особенно полезно для:

```text
hidden IO
unauthorized access
forbidden imports
cross-context state access
ambient reads
unbounded recursion / retries
resource leaks
unvalidated trust-boundary crossings
```

### 31.1 Effect surface

Для material функции желательно иметь проверяемое приближение:

```text
READS: DB, env, clock
WRITES: DB, cache
NETWORK: payments.api
AUTHORITY: PaymentService
TIMING: timeout / retry
```

Если runtime-effect не совпадает с declared-effect — это архитектурное нарушение, а не только style issue.

**Правило:**

> Чем сильнее side effect, тем меньше допустима разница между declared semantics и observed effects.

---

## 32. RESOURCE / LIFETIME / STRUCTURED CONCURRENCY

Отдельно различать:

```text
request lifetime
transaction lifetime
resource lifetime
authorization lifetime
task lifetime
cache lifetime
```

Наиболее опасные AI-смеллы:

```text
fire-and-forget
implicit background work
orphaned tasks
uncancelled work
shared mutable state
unbounded queues
retry without budget
```

Предпочитать:

```text
structured concurrency
explicit cancellation
bounded concurrency
scoped resource ownership
RAII / deterministic cleanup
capability-scoped resources
```

**Правило:**

> Resource lifetime должен быть ограничен owner scope; выход за него требует явного handoff, owner и доказанной семантики.

---

## 33. API EVOLUTION, HYRUM'S LAW И SEMANTIC MERGE

### 33.1 Accidental contract

При достаточном числе consumers любое наблюдаемое поведение может стать фактическим контрактом. Поэтому различать:

```text
intended API
explicit contract
observed behavior
accidental dependency
```

Не считать `private` автоматически означает «никому не нужен».

### 33.2 Semantic merge

Git merge проверяет текст. SSI должен дополнительно проверять:

```text
text conflict
structural conflict
dependency conflict
behavioral conflict
invariant conflict
ownership conflict
authority conflict
state-machine conflict
```

**Merge acceptance condition:** изменения могут сосуществовать не только текстуально, но и семантически.

---

## 34. FUZZING + TEST-SUITE ENGINEERING

Добавить к существующей testing ladder:

```text
example
→ boundary
→ property
→ metamorphic
→ fuzzing
→ mutation
→ state/model
→ differential
→ formal
```

### 34.1 Fuzzing contract

```text
generate adversarial input
→ run under bounded resources
→ detect relation violation
→ shrink
→ replay
→ CounterexampleCapsule
```

Использовать: coverage-guided fuzzing · grammar-based fuzzing · protocol fuzzing · schedule fuzzing · fault injection.

### 34.2 Тесты тоже имеют архитектуру

Контролировать:

```text
flakiness
redundancy
staleness
oracle strength
fixture coupling
execution cost
mutation survival
false confidence
```

**Rule:**

> `green suite ≠ healthy suite`; тестовый набор сам подвержен coupling, decay и Goodhart.

---


## 34.3 Deterministic Simulation Testing

Для stateful/distributed систем при material timing/network/disk/fault effects добавлять:

```text
deterministic scheduler + virtual time + seeded faults + controlled I/O
→ replayable witness → shrink → first divergence
```

DST усиливает property/mutation/fuzzing там, где ошибка зависит от взаимодействия state × timing × fault. Цель — reproducible uncertainty reduction, не случайная нагрузка.

## 34.4 Implementation-level proof and synthesis

Model-level спецификация должна, когда risk оправдывает стоимость, доходить до implementation:

```text
specification → refinement/type/contract → verified implementation claim → execution evidence
```

Для synthesis/rewrite циклов допустим:

```text
candidate → verifier → counterexample → refinement → verifier
```

Генератор не является доказательством собственного результата.
