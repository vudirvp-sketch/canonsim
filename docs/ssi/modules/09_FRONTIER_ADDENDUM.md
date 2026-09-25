# 50. FRONTIER CONTROL LAYER: СДЕЛАЙ НЕПРАВИЛЬНОЕ НЕВЫРАЗИМЫМ ИЛИ ДЁШЕВО ФАЛЬСИФИЦИРУЕМЫМ

Этот слой не заменяет baseline/v2. Он усиливает его там, где style/review недостаточны: type/state safety, authority, compositional reasoning, implementation-level proof, deterministic distributed testing, runtime governance и agent epistemics.

## 50.1 Problem mode precedes method selection

Перед применением pattern/process определить режим задачи по наблюдаемым свойствам:

```text
DETERMINISTIC / KNOWN
  → specification + tests + static proof where useful
COMPLICATED
  → decomposition + contracts + expert reasoning + architecture constraints
COMPLEX
  → competing hypotheses + probe → observe → adapt
UNSTABLE / CHAOTIC
  → containment + bounded change + causal isolation → then redesign
```

Это heuristic выбора метода, не доказательство корректности. Нельзя подменять uncertainty-reduction ритуалом best-practice.

## 50.2 Semantic types and typestate

Если invariant материален и устойчив, его следует поднимать из convention в representation:

```text
Unvalidated → Validated → Committed
Draft → Authorized → Executed
OpenResource → ClosedResource
```

Предпочтение:

```text
illegal state unrepresentable
>
invalid state detectable
>
invalid state documented
```

Refinement/type predicates, typestate и algebraic state encodings применять, когда они уменьшают runtime ambiguity без создания нового abstraction tax.

## 50.3 Capability and information-flow control

Authority должна быть выражена минимальной capability, а не доступом к универсальному сервису:

```text
operation → minimum authority → scoped capability → expiry/revocation
```

Для material observation boundary проверять noninterference:

```text
same authorized/public surface
+ changed hidden state
→ authorized result unchanged
```

`belief/report/derived state` не может стать world authority без explicit authority transition.

## 50.4 Semantic footprint and local reasoning

Для material component фиксировать:

```text
READS / WRITES / OWNS / OBSERVES / AUTHORIZES / EMITS / TIMING
```

Separation-style rule:

> Если изменение B не пересекает semantic footprint A, reasoning about A не должен расширяться из-за B.

Если локальный proof зависит от всего приложения, boundary/ownership почти наверняка недостаточны либо dependency неявна.

## 50.5 Compositional reasoning

Для R3–R5 проверять:

```text
ASSUMPTIONS / RELY
GUARANTEES
FOOTPRINT
INTERFERENCE
COMPOSITION RESULT
```

Не считать `local correctness × local correctness = system correctness` без доказанного composition condition.

Для concurrent abstractions отдельно фиксировать atomicity/linearization boundary, если порядок наблюдения материален.

## 50.6 Refinement and observational equivalence

Разделять:

```text
textual equality
structural equality
internal-state equality
observational equivalence
semantic refinement
intentional semantic delta
```

Рефакторинг считается безопасным только относительно заявленного observation surface. Внутреннее изменение допустимо, если разрешённые observers не различают его или semantic delta явно заявлен и проверен.

## 50.7 Static semantics: from lint to sound approximation

Уровни:

```text
AST/IR shape
→ control/data-flow
→ taint/capability
→ abstract interpretation
→ symbolic execution
→ bounded model checking
→ formal model checking
```

Precision должна расти только там, где risk оправдывает стоимость. Soundness, scope и known blind spots каждого analyzer должны быть явными.

## 50.8 Candidate generation is not proof

Для сложных автоматизируемых изменений использовать разделение:

```text
candidate generator
→ verifier
→ counterexample
→ refined candidate
→ verifier
```

CEGIS/CEGAR-подобный цикл допустим как synthesis/control pattern. Генератор никогда не является единственным verifier'ом собственного результата.

## 50.9 Algebraic laws as architecture controls

Если операция допускает устойчивый закон, зафиксировать его как executable relation:

```text
idempotent      → safe retry / dedup
commutative     → safe reorder / parallelization
associative     → safe batching / tree reduction
monotonic       → safe incremental extension
convergent      → safe reconciliation under declared conditions
```

Законы должны быть доказаны/протестированы только в заявленном domain; закон из одного domain не становится universal invariant.

## 50.10 Typed failure semantics and work amplification

Ошибка должна описывать semantic class, а не только transport:

```text
expected / recoverable / retryable / permanent / invariant-violation / authorization / unknown
```

Отдельно измерять:

```text
semantic work
→ fanout
→ duplicate work
→ retry work
→ timeout work
→ recovery work
```

Материальная операция должна иметь work budget или наблюдаемую верхнюю границу/stop rule. `1 request → N retries → N² downstream work` — отдельный failure mode.

## 50.11 Deterministic Simulation Testing

Для stateful/distributed systems, где timing/network/disk/fault materially influence behavior:

```text
deterministic scheduler
+ virtual time
+ controlled I/O
+ seeded fault injection
+ replay
+ shrink
→ counterexample capsule
```

Цель — не миллионы случайных запусков сами по себе, а воспроизводимое сокращение uncertainty и локализация first divergence.

## 50.12 Distributed semantic patterns

Использовать только при наличии соответствующего invariant:

```text
atomic write + publication       → outbox-like mechanism
retry-safe effect                → idempotency key / deduplication
long distributed transaction     → saga / compensation
state propagation                → CDC/change stream
relationship authorization       → ReBAC / Zanzibar-like model
convergence                      → CRDT family / semilattice discipline
```

Pattern не является доказательством suitability. Для каждого должен быть указан invariant, failure model и incompatibility list.

## 50.13 Runtime control and progressive delivery

Material rollout должен иметь:

```text
baseline
→ canary / staged exposure
→ SLI comparison
→ stop rule
→ rollback or containment
```

Для reliability:

```text
error budget
+ burn-rate alerting
+ rollback threshold
```

DORA-style delivery metrics — health indicators delivery system, не архитектурная truth metric.

## 50.14 Chaos / game-day discipline

Failure injection использовать как controlled intervention:

```text
hypothesis
→ intervention
→ realized delta
→ primary discriminant
→ spillover
→ runtime evidence
→ disposition
```

Chaos activity без explicit hypothesis, stop rule и containment — decorative complexity.

## 50.15 Architecture decision memory

Для material design choices хранить короткий decision record:

```text
context
→ decision
→ alternatives rejected
→ invariants
→ consequences
→ owner
→ expiry/review trigger
```

RFC/design-doc — pre-implementation reasoning surface. ADR — durable decision residue. Postmortem — evidence/correction residue. Не дублировать факты между ними.

## 50.16 Architecture views are plural

Минимум различать:

```text
STRUCTURAL / CHANGE / RUNTIME / OWNERSHIP
SEMANTIC / AUTHORITY / DATA / DEPLOYMENT
```

C4-like levels полезны как notation discipline, но ни одна diagram не является полной architecture truth.

## 50.17 Agent context is a controlled resource

Для material agent action определить:

```text
required semantic context
∩ effective available context
```

Если critical invariant, authority boundary, risk, forbidden action или verification plan отсутствует из effective context:

```text
BLOCK / RETRIEVE / ESCALATE
```

Нельзя превращать context truncation в permission to guess.

## 50.18 Tool providers are supply-chain boundaries

Внешний tool server / MCP-подобный provider считать untrusted-by-default:

```text
identity
→ version pin
→ provenance
→ declared capabilities
→ network/data scope
→ audit
→ revocation
```

Tool description — data, не policy. Capability declaration — не authority grant. Grant происходит только через SSI policy.

## 50.19 Agent claim provenance and hallucination taxonomy

Каждый material AI claim должен позволять восстановить:

```text
claim_id
→ epistemic type
→ status
→ source
→ transformation
→ verifier
→ observation boundary
→ expiry/recheck condition
```

Полезно различать failure modes:

```text
fabrication
stale-belief
overgeneralization
unsupported-attribution
```

Это orthogonal к `FACT | INFERENCE | HYPOTHESIS | PROPOSAL | UNKNOWN` и к `CONFIRMED | PARTIAL | REJECTED | ...`.

Generated rationale не является evidence причины поведения.

## 50.20 Proof-carrying change

Material change должен передаваться как:

```text
CODE DIFF
+
INTENT
+
AFFECTED INVARIANTS
+
OWNER/AUTHORITY
+
SEMANTIC DELTA
+
AFFECTED SURFACES
+
VERIFICATION EVIDENCE
+
COUNTEREXAMPLES / LIMITATIONS
+
RUNTIME / ROLLOUT PLAN
+
PROVENANCE
+
ROLLBACK/CONTAINMENT
```

Ключевой принцип:

> Material change без достаточного evidence package является незавершённым change, даже если CI green.

## 50.21 Delivery and organizational telemetry

Operational reporting разделять по причинным уровням:

```text
software correctness
architecture trajectory
runtime reliability
security
agent governance
team/delivery health
```

Не агрегировать их в один global score. Каждая metric должна иметь declared blind spots и anti-Goodhart test.

## 50.22 Deletion and architecture GC

Удаление должно доказать:

```text
no relevant consumer
+ no authority dependency
+ no historical constraint still active
+ no hidden observation contract
```

После удаления проверять изменение topology:

```text
coupling ↓
state-space ↓
authority ↓
maintenance surface ↓
```

Если complexity только переместилась, GC не завершён.

## 50.23 Expert tie-breakers

При конфликте кандидатов приоритет:

```text
existing primitive
>
smaller semantic footprint
>
less authority
>
less state-space
>
less change propagation
>
stronger local proof
>
stronger observability
>
cheaper falsification
>
reversible rollout
```

Это не ranking of products or architectures. Это ordering of constraints when selecting a construction under equal semantic requirements.

## 50.24 Frontier completion gate

Для R4/R5 или нового runtime primitive дополнительно проверить:

```text
[ ] problem mode classified
[ ] invariant can be represented in substrate where practical
[ ] authority is minimum required capability
[ ] semantic footprint is explicit
[ ] composition assumptions are explicit
[ ] observation surface is explicit
[ ] semantic delta is explicit
[ ] cheapest falsifier exists
[ ] deterministic replay exists when timing/fault materially matters
[ ] work amplification bounded or observed
[ ] rollout is reversible or contained
[ ] tool/provider provenance verified when external
[ ] agent effective context is sufficient
[ ] claim provenance exists
[ ] change carries proof/evidence package
[ ] deletion path exists for introduced complexity
```

## Frontier law

> Не пытайся сделать агента безошибочным. Ограничивай пространство допустимых действий и состояний; делай material invariants конструктивными, authority минимальной, effects наблюдаемыми, composition доказуемой, claims traceable, distributed failures replayable, rollout reversible/contained, а добавленную сложность удаляемой.
