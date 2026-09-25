# SOFTWARE SEMANTIC INTEGRITY & ENGINEERING CONTROL
### Единая доктрина против спагетти-кода, God Object и «ИИ-кода» — синтез двух источников

> **Хороший код — это локальная, наблюдаемая и проверяемая реализация устойчивых семантических инвариантов при контролируемой изменчивости.**
> Абстракция — не эстетика, а управление будущим изменением. Архитектура должна не только разрешать правильное поведение, но делать неправильное — трудным или невозможным. Правило существует, только если у него есть owner и falsifier.

Главный объект инженерии — не класс/функция/файл, а **отношения**:
`intent↔behavior · invariant↔variation · authority↔derivation · state↔transition · specification↔implementation · claim↔evidence · change↔blast radius · capability↔permission · observation↔inference · artifact↔provenance`

---

## 0. МЕТА-ПРИНЦИП: СИСТЕМА ПРИМЕНЯЕТ СЕБЯ К СЕБЕ

Любой каталог правил (включая этот) обязан пройти **Material Verdict Test**:
1. Есть ли реальный consumer и failure, которые принцип предотвращает?
2. Существует ли уже примитив, покрывающий то же самое?
3. Даёт ли правило causal leverage, а не декоративную структуру?
4. Переносится ли оно на другую подсистему?
5. Можно ли синтезировать его сильнее, чем просто сложить пункты?

Без этого фильтра сама anti-god-object система рискует стать god-process. Metric hygiene (§9) применяется и к архитектурным метрикам: `fitness function зелёный ≠ архитектура чистая` — можно формально соблюсти «domain не импортирует infra», продублировав доменную логику в infra-слое (синтаксическая чистота при семантической утечке).

---

## 1. ЧЕТЫРЕ БАЗОВЫХ РАЗДЕЛЕНИЯ (фундамент всей системы)

### 1.1 Stable ↔ Variable — ядро CVA (Commonality/Variability Analysis, J. Coplien)
- Два вопроса: **что общее** (стабильный контракт) / **что варьируется** (delegируется в strategy/factory/composition).
- Абстрагировать по **usage context**, не по синтаксическому сходству или форме хранения: «что обязано меняться одинаково — удерживаем вместе; что меняется независимо — разделяем».
- Триггер: ≥3 похожих сущности → мини-CVA перед реализацией третьей.
- `ABSTRACTION_JUSTIFICATION`: абстрагируй только если это снижает стоимость будущих изменений. Низкая частота изменений → explicit procedural code лучше карты стратегий.
- Источник концепции — **Parnas (1972)**: модуль скрывает **решение** (secret), а не данные → абстракция = information hiding с границами по вероятной точке изменения.
- **Expression Problem (Wadler)**: нельзя одновременно дёшево расширять и по типам, и по операциям — выбор структурного паттерна математически ограничен этим trade-off, а не предпочтением.

### 1.2 Claim ↔ Evidence
- `observed behavior ≠ intended behavior ≠ possible implementation ≠ warranted implementation`.
- Статус утверждения: `FACT / INFERENCE / HYPOTHESIS / PROPOSAL / UNKNOWN`.
- Результат исследования: `CONFIRMED / PARTIALLY CONFIRMED / REJECTED / UNRESOLVED / DEFERRED`.
- Главный закон: **CLAIM STRENGTH ≤ WEAKEST MATERIAL EVIDENCE CONDITION** — сила вывода ограничена самым слабым существенным условием доказательности. Красивая гипотеза не становится requirement только потому, что хорошо объясняет наблюдение.

### 1.3 Authority ↔ Derivation
```
canonical authority → state/event/effect → derived representation → diagnostic/cache/projection/approximation
```
- Производное состояние не должно незаметно становиться ground truth; диагностика не должна менять семантику; belief/report не должен превращаться в authority.
- Approximation допустима в derived/read/search/assurance-слоях, но canonical state обязан быть exact, deterministic, replayable, inspectable.
- Смежная триада для AI-контекста: `world state → stored state → authorized state → observer knowledge → interpretation → behavior → narration`. Запрещено: `belief→truth`, `report→authority`, `diagnostic→state`, `projection→source of truth`, `stale cache→current fact`, `partial observation→completeness claim` — один из сильнейших anti-hallucination принципов не только для AI, но и для distributed-систем.

### 1.4 State ↔ Transition
`state × event → next state`. Для каждого существенного объекта нужны ответы: какие состояния существуют / какие переходы разрешены и невозможны / кто вправе их инициировать / какой semantic effect создаёт переход / что происходит при retry, timeout, concurrency, failure. Большинство сложных production-багов рождается не из неправильного состояния, а из неправильной **траектории** между состояниями.

---

## 2. СЕМАНТИЧЕСКОЕ МОДУЛИРОВАНИЕ: ГДЕ РОЖДАЕТСЯ GOD OBJECT

Классическая ошибка — декомпозировать по таблицам/DTO/экранам/файлам/техническим слоям/синтаксическому сходству. Граница должна проходить там, где находится **независимо изменяемое решение**.

| Принцип | Против чего | Операционное правило |
|---|---|---|
| Information Hiding (Parnas) | утечка реализации | модуль скрывает design decision, которое может измениться независимо, а не файл |
| Deep Modules (Ousterhout) | shallow-module epidemic — типичный AI-код | маленький публичный интерфейс + большая скрытая сложность = deep module; большая публичная поверхность ≈ вся реализация = shallow, опасен даже при идеальной файловой структуре |
| Connascence (Page-Jones) | скрытая связанность | искать не coupling, а «что обязано меняться вместе»; иерархия силы: `name→type→meaning→algorithm→order→timing→identity`; сильно связанное нельзя искусственно разносить на большие архитектурные расстояния |
| Cohesion by responsibility | God Object | объект = один устойчивый кластер решений |
| Bounded Context / Ubiquitous Language (DDD) | semantic drift | одно слово ≠ одна модель во всех контекстах; имена — из бизнес-языка |
| Functional Core / Imperative Shell | spaghetti из side-effects | чистая логика в центре, IO по краю |
| Stable Dependencies Principle | хаотичный граф | зависимость → к более стабильному слою |
| Law of Demeter | «не разговаривай с незнакомцами» | первый количественный фильтр против God Object |
| Simple vs Easy (Rich Hickey) | привычный ≠ простой | LLM оптимизирует под *easy* (знакомые паттерны обучения), не под *simple* (unbraided, объективно меньше сплетённых concerns) — источник «ИИ-код-смелла» |

**Надстройка**: оптимизируй не строки, а **locality of reasoning** — чтобы понять `X`, не нужно загружать полсистемы в голову: ограниченная глубина переходов, явные owner boundaries, минимум ambient state, короткий путь intent→effect.

### 2.1 God Object и spaghetti — это не размер
Настоящий критерий: **сколько независимых change dimensions, ownership boundaries и семантических решений сходятся в одной точке.** God Object возникает, когда один объект владеет данными, решениями, координацией, policy, IO, validation, security, state transitions, diagnostics, integration — и любое изменение начинает затрагивать чужие concerns. Spaghetti — система, где control flow, dependency flow и responsibility flow перестали совпадать с semantic boundaries.

Правильные вопросы: *что это потребляет? почему? что меняется независимо? кто владеет этой изменчивостью? какие решения объект реально владеет?* — не *сколько методов/строк/интерфейсов?*

---

## 3. СВЯЗАННОСТЬ: ОТ «КТО ВЫЗЫВАЕТ» К «ЧТО ОБЯЗАНО МЕНЯТЬСЯ ВМЕСТЕ»

Зрелость code review возрастает по шкале: *кто вызывает? → что сломается при изменении? → какие изменения обязаны распространяться совместно?*

Ключевые формы: **temporal coupling** (порядок вызовов важен, но API этого не показывает) · **hidden state coupling** (независимые по API модули делят mutable state) · **data vs semantic coupling** (общий DTO ≠ общая семантика) · **blast radius** (не «сколько строк», а сколько независимых решений может быть нарушено). Стыкуется с диагностической цепочкой §7.

### 3.1 Change surface и границы
Измерять нужно не только complexity, но: dependency surface / change surface / failure surface / observation surface / authority surface. **Change Surface** — какие независимые решения потенциально затрагиваются одним изменением. **Good boundary** — локальное изменение имеет локальный blast radius; если маленькая правка регулярно распространяется через множество owner boundaries — граница, скорее всего, проведена неверно.

---

## 4. AI-CODE: ДИАГНОСТИКА И СЛОВАРЬ АНТИПАТТЕРНОВ

«AI-code» нельзя надёжно определить по визуальному стилю. Его характерный дефект: **локально правдоподобная реализация, которая глобально плохо интегрирована в систему инвариантов, ownership boundaries и evidence.**

AI-агенты структурно склонны к циклу:
```
error → add if → new error → add fallback → new error → helper → manager → God Object
```
Локально каждый шаг выглядит рациональным; глобально создаётся новый слой/owner/dependency/abstraction без прироста capability — **decorative complexity**.

### Словарь антипаттернов (объединённый, без дублей)
`Large Class` · `Feature Envy` · `Shotgun Surgery` · `Divergent Change` · `Primitive Obsession` · `Anemic Domain Model` · `Temporal Coupling` · `Hidden State Coupling` · `Abstraction Inflation` (BaseService/AbstractManager/FactoryFactory без прироста capability) · `Boundary Laundering` (нарушение границы маскируется wrapper'ом) · `Conditional Accretion` (каждый edge case = новый if вместо локализации variation) · `Responsibility Drift` (класс копит «логически рядом лежащее» → будущий God Object) · `Semantic Duplication` (две реализации похожи синтаксически, но разная бизнес-семантика — опаснее обычного дублирования) · `Exception-driven Architecture` (fallback становится основной веткой) · `Utility Gravity` (`utils/` как кладбище архитектуры) · `DTO Ossification` (внутренняя модель продиктована транспортным DTO) · `Context Laundering` (новый слой маскирует нехватку контекста вместо устранения источника неоднозначности) · `Patch Accretion` (локальные заплатки съедают исходную структуру) · `copy-paste variation` · `excessive defensive code` · `semantic naming drift` · `silent behavior changes` · `overfitted tests` · `unsupported assumptions` · `local optimization`.

**Postel's Law как ловушка**: «be liberal in what you accept» в LLM-реализации превращается буквально в try/except на всё — прямое попадание в `Exception-driven Architecture`. Современная позиция: **strict-in/strict-out по умолчанию**; liberal accept — только explicit решение с owner, не default. Согласуется с §11 «Fail Closed» в security.

Главный антидот — не «писать меньше AI-кода», а **делать систему устойчивой к плохим локальным решениям агента**.

---

## 5. ПАТТЕРН — НЕ ПЕРВЫЙ ВЫБОР

Правильный порядок: `problem → invariant → variation → boundary → constraints → mechanism → pattern`, а не сразу «Strategy? Factory? Observer? CQRS? Event Sourcing? CRDT?». Паттерн — форма реализации механизма; если механизм не нужен, паттерн — декоративная архитектура. Структурный паттерн выбирается по **constraint topology** (см. Expression Problem, §1.1), не по preference.

### 5.1 Refinement: от спецификации к реализации
```
intent → specification → invariants/contracts → abstract state/behavior → refinement → representation → implementation
```
Главный вопрос рефакторинга: **изменилась реализация или изменилась семантика?** Representation Independence требует, чтобы internal representation менялась без изменения externally observable semantics: `semantic equivalence ≠ structural similarity` — две реализации могут быть устроены радикально по-разному и удовлетворять одному контракту.

---

## 6. CONTRACT-DRIVEN DESIGN И КОНСТРУКТИВНАЯ КОРРЕКТНОСТЬ

**Design by Contract (Meyer)**: precondition / postcondition / invariant переводят скрытые assumptions в проверяемые контракты. Для AI-кода вместо задачи «сделай оплату» — явный контракт:
```
PRE:  order is payable · actor has permission · amount > 0
POST: exactly one semantic charge exists · retry cannot duplicate charge ·
      persisted state matches canonical effect
INVARIANT: diagnostic/logging changes cannot alter outcome
```
LLM перестаёт проектировать «по ощущению» — контракт заменяет неявное намерение явным.

### 6.1 Illegal states should be unrepresentable
Если invariant можно выразить структурой типов/состояния/capabilities — лучше сделать его **конструктивным ограничением**, а не договорённостью, а не отфильтровывать булевой проверкой постфактум (**Parse, don't validate**, A. King). Пример: `Order{status, paid, cancelled, fulfilled}` допускает бессмысленные комбинации — вместо этого представление, где invalid state физически недостижимо без обхода системы.
Type-level invariants выражаются цепочкой: `RawInput → ValidatedInput → AuthorizedCommand → ResolvedCommand → PersistedEffect`.
Полезные конструкции: Algebraic Data Types · Sum Types · Typestate · Refinement Types · Capability Types · Effect Types.
Принцип: **чем больше correctness закодировано representation, тем меньше correctness приходится держать в голове человека или LLM.**

### 6.2 Effects должны быть видимы
IO, network, filesystem, mutation, transaction, security-sensitive action, external side effect не должны прятаться внутри `processEverything(...)`. Чем скрытее effect, тем сложнее testability, reasoning, replay, causal diagnosis, dependency analysis. Предпочтительно: pure calculation + explicit effect boundary. **Algebraic Effects / Effect Systems** дают более формальное средство выражать variability и effects, чем глубокие иерархии наследования; снижают hidden dependencies и hallucinated assumptions у LLM.

### 6.3 State и concurrency
Для concurrent/distributed систем отдельно проверять: atomicity, ordering, visibility, isolation, identity, idempotence, causality, progress. Понятия: happens-before, linearizability, serializability, causal consistency, idempotency, commutativity, monotonicity.
**Semantic algebra операции** — знать: associative? commutative? idempotent? invertible? deterministic? monotonic? — это определяет безопасность retry, batching, parallelization, reordering, deduplication, caching, replay, merge, incremental recomputation. Свойства операции — часть её architecture contract.

### 6.4 Existing substrate first
Перед новой абстракцией: выражает ли это уже существующий примитив? содержит ли substrate нужное состояние? можно ли расширить существующее отношение? действительно ли это отсутствующий примитив? Новый primitive — **architectural finding**, а не рефлекс. Запрещены по умолчанию: второй canonical store, общий provenance graph, generic workflow engine, self-adjusting runtime и т.п. без material failure и evidence.

---

## 7. ТЕСТИРОВАНИЕ: ОТ COVERAGE К SEMANTIC ADEQUACY

Иерархия зрелости (единая для обоих источников):
```
Example → Boundary → Property-based → Metamorphic → Mutation →
Model/State-based → Differential → Formal invariants/verification
```
- **Property-based** — не «пример работает», а «отношение R выполняется для класса входов».
- **Metamorphic** — безопасное преобразование входа сохраняет заявленное отношение; незаменимо там, где нет oracle (типично для ML/LLM-компонентов).
- **Mutation testing** — намеренно ломаем смысл, проверяем, замечает ли suite; тест **чувствительности**, не просто покрытия строк.
- **Contract testing** (consumer-driven) — операционализация «stable contract» на границах сервисов, независимо от внутренней реализации.
- **Golden/Characterization** — фиксирует поведение legacy перед рефакторингом.
- **Stateful/Model-based** — проверяет допустимость последовательностей переходов.
- **Differential testing / формальные инварианты** — верхняя граница строгости.
- **CEGAR-style refinement** — грубая гипотеза → cheap test → counterexample → добавить только недостающую грань → повтор; стратегия против over-engineering.
- **Testing Trophy** (Kent C. Dodds) — для сильно композиционного AI-кода integration-тесты честнее, чем пирамида unit-тестов, легко проходящих по отдельности, но ломающихся в композиции.

### 7.1 Многомерное покрытие
Вместо одного числа `80%`: line · branch · path · state-transition · boundary · failure-mode · interaction · invariant coverage · mutation adequacy · **held-out transfer**. Формулы дисциплины: `coverage ≠ correctness` · `test count ≠ evidence strength` · `green build ≠ semantic equivalence`. Главный вопрос mutation testing: если намеренно внести meaningful semantic defect, suite его обнаружит? Held-out transfer — главная защита от иллюзии обобщения: тест прошёл в сценарии A ≠ механизм доказан вне A.

---

## 8. FALSIFICATION И ДИАГНОСТИКА ВМЕСТО СИМПТОМ-ПАТЧИНГА

Надёжный исследовательский цикл (research-control loop):
```
QUESTION → competing explanations → distinguishing assumptions →
cheapest discriminating test → controls/nuisance plan → realized intervention →
primary discriminant → counterexample → held-out/scope test → disposition
```
Перед redesign: реальна ли проблема? что уже объясняет текущий substrate? какое конкурирующее объяснение сильнейшее? какой falsifier дешевле всего? Типовые альтернативы: missing primitive / missing data / missing dependency / wrong observation surface / wrong resolution rule / measurement blind spot / harness defect.

### 8.1 Diagnose before redesign — causal slicing
```
Failure → First Divergence → Influence Region / Causal Slice → Minimal Sufficient Cause →
Responsible Boundary → Minimal Replayable Witness / Counterexample → Repair → Regression Witness
```
Диагностические артефакты: `CausalSlice` (что могло повлиять?) · `FailureCore` (что достаточно для объяснения?) · `BoundaryBlame` (чья граница ответственна?) · `CounterexampleCapsule` (минимальный воспроизводимый свидетель). Это лучший антидот против AI-цикла `error → if → fallback → helper → manager → God Object` (§4).

---

## 9. SEMANTIC DIFF ВМЕСТО TEXT DIFF

Ревьюировать нужно не «что написал агент», а **какая семантика системы изменилась**. Четыре слоя diff: `TEXTUAL → STRUCTURAL → BEHAVIORAL → INVARIANT`.
```
Changed: authority path / retry implementation / cache representation / internal topology
Preserved: retry invariant, transaction boundary / exactly-one-effect invariant /
           freshness ≤ contract / public semantic contract
Added: idempotency constraint
Affected: Order, Payment
Unchanged: read model, notification path
```
Размер patch (`+17/-8 строк`), число новых файлов и «красота» архитектуры сами по себе ничего не доказывают — важны затронутые инварианты.

---

## 10. АРХИТЕКТУРА КАК ИСПОЛНЯЕМЫЙ ИНВАРИАНТ

Правило в README не работает — оно не «помнит»себя, ни человеком, ни LLM. Доктрина, которую CI не проверяет, со временем превращается в пожелание. Нужны:

- **Architecture Fitness Functions** (Fowler) — CI падает при нарушении: `domain не импортирует infra` · `нет циклов зависимостей` · `writes идут только через canonical authority` · `нет cross-context DB access` · `restricted API имеют named owner` · `public API ≤ N` · `complexity ≤ budget` · `новый primitive требует gate`.
- **Policy-as-code** — правило + автопроверка + owner + причина нарушения + explicit exception с expiry.
- **CODEOWNERS / ownership gates** — архитектурное изменение проходит через owner boundary.
- **Negative design / Verification Grammar** — явно фиксировать, чего система **никогда** не делает (полный список — §14).
- **Negative capability**: хорошая архитектура не только разрешает нужное, но делает ненужное трудным или невозможным. `correctness by construction` > `correctness by convention`.

---

## 11. OBSERVABILITY, PROVENANCE, ДИАГНОСТИКА

**Observability ≠ logging.** Телеметрия — семантический интерфейс системы (OpenTelemetry semantic conventions), не склад сообщений:
```
operation = reserve_resource · resource.id · request.id · trace.id ·
decision = rejected · reason = capacity_exceeded · authority = InventoryService
```
Для каждой значимой операции должно быть восстановимо: что произошло / кто вызвал / какая authority решила / какие inputs повлияли / что изменилось / что не изменилось / какое evidence осталось / можно ли реплеить. Distributed tracing нужен потому, что причинная цепочка пересекает границы, и без trace невозможно восстановить first divergence.

**Диагностика не должна менять семантику**: `change diagnostics ≠ change result` · `add tracing ≠ alter execution semantics` · `increase logging ≠ introduce hidden state`. Диагностическая инфраструктура по умолчанию transient; становится permanent primitive только при устойчивом потребителе и доказанной потребности (No permanent diagnostics without durable consumer).

**Provenance/traceability**: `Requirement → Scenario → Invariant → Design decision → Code change → Test → Build artifact → Deployment → Runtime evidence`. Обязаны иметь машиночитаемый ответ вопросы «почему этот код существует» и обратный «что сломается, если его удалить» (направление, близкое к SLSA в supply-chain security). Для AI-среды provenance расширяется: model / context / tool / dependency / build / artifact / deployment provenance.

### 11.1 Metric hygiene (anti-Goodhart)
Для любой метрики: можно ли улучшить метрику без улучшения реальности, и наоборот? Какое gaming-поведение она провоцирует? Какой у неё blind spot?
`coverage ≠ test quality/correctness` · `LOC↓ ≠ complexity↓` · `abstraction↑ ≠ design quality↑` · `types↑ ≠ correctness/safety↑` · `tests↑ ≠ confidence↑` · `observability/logging↑ ≠ понимание↑` · `documentation↑ ≠ transparency↑` · `performance↑ ≠ efficiency↑` · **`fitness function green ≠ architecture clean`**. Метрика — detector, не verdict.

---

## 12. SECURITY — ТА ЖЕ МОДЕЛЬ, ПРИМЕНЁННАЯ К AUTHORITY

- **Least Authority** — компонент получает минимально необходимое право.
- **Capability Security** — permission представляется capability, а не скрытым global privilege.
- **Confused Deputy** — компонент не использует свои полномочия для действия, которое инициатор не имел права совершить.
- **TOCTOU** (`check → state changes → use`) не считается безопасной схемой без сохранения нужного invariant.
- **Fail Closed**: `unknown → deny/downgrade/explicit fallback`, а не `unknown → assume safe`.
- Security boundaries должны быть такими же executable, как architecture boundaries (§10).

---

## 13. DATA И SCHEMA EVOLUTION

Runtime architecture учитывает не только code evolution, но и data evolution. Цикл: `expand → migrate → verify → contract`. Проверять backward/forward compatibility, ownership, freshness, schema semantics, canonicalization, identity. Нельзя приравнивать `same bytes = same structure = same semantic value = same identity = same derivation` — **Layered Identity** прямо требует отличать равенство содержимого от identity derivation/reuse.

---

## 14. PERFORMANCE, RELIABILITY, CONTROL THEORY

### 14.1 Производительность — причинная цепочка, не интуиция
```
symptom → measurement → bottleneck → causal mechanism → intervention → regression proof/evidence
```
Не «выглядит медленно → переписать». Ключевые инструменты: алгоритмическая сложность (`O(n²)` часто важнее микрооптимизаций) · критический путь · **Amdahl's Law** · **tail latency** (`p95/p99`, не среднее) · contention/allocation/IO/cache locality · batching · **backpressure** · **bounded concurrency** · **incremental computation** · memoization/caching только при одновременном определении `identity + invalidation + freshness + ownership` (иначе cache = скрытое состояние). Performance optimization без доказанного bottleneck — потенциально decorative complexity.

### 14.2 Reliability = contract + failure model + control loop
```
failure mode → expected degradation → detection → containment → recovery → evidence
```
SLO / SLI / Error Budget / DORA — не путать с code quality: `DORA = delivery-system health` · `SLO = reliability target` · `Error Budget = operational control mechanism`. Метрика без действия (`measurement → threshold → policy → allowed/forbidden action`) — reporting, не control.

### 14.3 Control theory для software
Эксплуатация — feedback control: `desired state → system → observation → deviation → diagnosis → correction → new observation`. Полезны: feedback, hysteresis, deadband, stability, gain, oscillation. Плохая автоматизация создаёт oscillating system (например: медленно → добавить concurrency → перегрузка → выше latency → throttle → снова медленно). Corrective action должно быть bounded, observable, reversible, proportional.

### 14.4 Reversibility влияет на доказательство
Для каждого существенного решения: reversible? cost of reversal? observability of reversal? irreversible state создаётся? data/API/ownership последствия? Принцип: **чем выше irreversibility × blast radius, тем выше должен быть evidence threshold.** Необратимые решения (schema change, public API, external contract, persistent representation, authority boundary, ownership transfer, distributed topology) требуют существенно более сильного evidence, чем локальный reversible refactor.

### 14.5 Representation-first
Иногда правильное решение — не новый алгоритм, а смена representation: `change representation → make operation tractable → exact canonical verification`. Формы: candidate generation→filtering→exact validation; derived representation→search→exact verification; semantic addressing→local variation control→deterministic replay. Approximation не становится truth только потому, что ускоряет поиск.

---

## 15. CHANGE MANAGEMENT ДЛЯ LEGACY / МУСОРНОГО КОДА

Не rewrite, а контролируемое вытеснение: `characterization tests → seam → isolate variation → strangler boundary → branch by abstraction → migrate → verify → remove obsolete path`.

- **Mikado Method** — target change → обнаруженные зависимости → подцели → минимальные refactor nodes → повтор (граф препятствий, не «переписать всё сразу»).
- **Strangler Fig** — постепенное вытеснение старого поведения новой границей.
- **Seam-Oriented Refactoring** — сначала точка замены поведения, потом изменение.
- **Anti-Corruption Layer (DDD)** — интеграция с чужим/legacy доменом без семантической утечки.
- **Feature Flags / Progressive Delivery** — old/new параллельно в проде, не только в коде.
- **Broken Windows** — одно необработанное нарушение стандарта резко повышает вероятность следующих; объясняет самоускорение Patch Accretion.
- **Chesterton's Fence** — перед удалением непонятного кода сначала понять, какое историческое constraint он обслуживает. Особенно важно для LLM: агент не должен считать необъяснимый код автоматически мусором.

---

## 16. СОЦИОТЕХНИЧЕСКИЙ СЛОЙ

Архитектура — слепок коммуникационной структуры (Conway's Law / inverse Conway maneuver). Team Topologies формализует **cognitive load** как центральный организационный фактор. `owner boundary = architectural boundary`: если модуль требует пяти команд для изменения — проблема в boundary design, не в коде. **Bus factor** — симметричная owner-boundary метрика риска исчезновения знания.

---

## 17. CROSS-DOMAIN TRANSFER

Дисциплина переноса решений между доменами:
```
foreign domain → mechanism → invariant → remove cargo → target adaptation →
competing explanation → cheapest discriminating test → consequence →
counterexample → scope check → durable residue
```
Переносится не название, не метафора и не структура, а **operation that causes the effect**. Антипаттерны: surface analogy · cargo cult · hidden assumption · arbitrary transfer · decorative complexity · threshold leakage · terminology leakage · false independence. Если нет observable consequence — это не established transfer.

---

## 18. АДВЕРСАРИАЛЬНЫЙ SEMANTIC REVIEW (ключевое усиление)

Карточка ревью, заполненная тем же агентом, что писал код, эпистемически слаба (нарушает evidence-independence: тот же контекст не может быть независимым подтверждением). Нужна двухагентная схема:
```
generator agent → код + review card (INTENT/INVARIANTS/VARIATIONS/OWNER/
                  BOUNDARY/DEPENDENCIES/SEMANTIC DELTA/NON-CHANGES/EVIDENCE)
critic agent (независимый контекст) → пытается фальсифицировать:
    - вход, нарушающий заявленный инвариант
    - blast radius шире заявленного
    - скрытый эффект, не упомянутый в карточке
adjudication → CONFIRMED / PARTIALLY CONFIRMED / REJECTED
```

---

## 19. ЗАПРЕТНОЕ ВАЖНЕЕ ИНСТРУКЦИЙ: NEGATIVE RULES

Запрещённые состояния и действия сильнее длинных инструкций. Сводный список (дубли исходников устранены):

```
Domain NEVER импортирует infrastructure.
Diagnostic objects/data NEVER становятся authority или не меняют семантику.
Derived state NEVER незаметно становится truth/authority.
Retry NEVER дублирует semantic effect.
Unauthorized actors NEVER могут сконструировать authorized action.
Unknown input NEVER оправдывает completeness claim.
Private data NEVER утекает через authorized-поверхности.
Изменение диагностики NEVER меняет семантику результата.
Новый primitive NEVER появляется без promotion gate.
Паттерн/метрика/зелёный тест сами по себе NEVER являются доказательством (causal claim, correctness, quality).
Локальное синтаксическое сходство NEVER оправдывает абстракцию.
Исторический хак NEVER удаляется без понимания обслуживаемого им constraint.
```

### Глобальные анти-AI-code правила
1. No abstraction without stable commonality.
2. No primitive without real consumer (real failure + material gap + owner + falsifier).
3. No hidden effect — IO, mutation, authorization, timing, внешние эффекты наблюдаемы.
4. No silent semantic drift — рефакторинг доказывает сохранность объявленных relations.
5. No ownership ambiguity — у каждого решения есть owner.
6. No evidence laundering — зелёный тест не становится автоматически proof.
7. No local patch without boundary check — каждый новый if/fallback/helper проверяется на вопрос «не локализую ли я symptom вместо responsible variation?».
8. No duplicate semantic authority — две competing truths — одна из самых дорогих форм complexity.
9. No architecture by accumulation — каждый новый layer имеет capability justification.
10. No permanent diagnostics without durable consumer.
11. No irreversible change without elevated evidence.
12. No architectural rule without executable enforcement, где это осуществимо.

---

## 20. ЕДИНЫЙ ПРОЦЕСС ИЗМЕНЕНИЯ КОДА

Объединяет CVA, research-control loop, diagnostic pipeline, material verdict test и runtime promotion gate:
```
1. INTENT — что должно измениться?
2. CURRENT SUBSTRATE — что уже умеет система?
3. INVARIANTS — что обязано остаться истинным?
4. VARIATIONS — что именно изменяется?
5. OWNER — кто владеет решением?
6. BOUNDARY — где проходит responsibility boundary?
7. COMPETING EXPLANATIONS — почему проблема вообще существует?
8. CHEAPEST FALSIFIER — что дешевле всего может опровергнуть гипотезу?
9. DESIGN — какая минимальная representation поддерживает invariant?
10. IMPLEMENT — минимальная sufficient structure.
11. VERIFY — contract + property + mutation + regression + relevant architecture checks.
12. OBSERVE — как доказать поведение в runtime?
13. SEMANTIC DIFF — что изменилось и что сохранено?
14. COUNTEREXAMPLE — чем пытались сломать решение?
15. DISPOSITION — Confirmed / Partial / Rejected / Unresolved.
16. PERSIST — сохранить только durable residue.
```

---

## 21. МОДЕЛЬ АРХИТЕКТУРНОЙ ЦЕННОСТИ И ГЕЙТ НОВЫХ ПРИМИТИВОВ

Новая структура имеет право существовать, если она хотя бы одно из следующего: локализует variation · усиливает invariant · уменьшает change surface · уменьшает blast radius · делает authority явной · делает effect явным · улучшает observability · усиливает testability · уменьшает cognitive load · снижает failure class · делает forbidden state недостижимым · улучшает reversibility · увеличивает доказательность. Если ничего из этого не выполняется — вероятно, decorative complexity.

Единственный жёсткий гейт на добавление:
```
NO NEW PRIMITIVE unless:
REAL CONSUMER + REAL FAILURE + MATERIAL GAP + NATIVE LIMIT +
REPEATED SHAPE + OWNER + FALSIFIER + PROMOTION GATE
```
и симметрично на удаление:
```
NO DELETION unless: понята причина существования (Chesterton's Fence) +
доказано отсутствие скрытого потребителя +
подтверждено снижение (не перенос) connascence
```
LLM-агенты по умолчанию аддитивно смещены (добавить if дешевле, чем удалить путь) — симметричное требование к удалению единственное, что этому прямо противодействует.

---

## 22. ИТОГОВАЯ МОДЕЛЬ ПОТОКА

```
DOMAIN INTENT
   ↓
SCENARIOS / CONTEXT
   ↓
INVARIANTS / CONTRACTS
   ↓
CVA: BOUNDARIES · OWNERS · VARIATIONS  ←── Expression Problem constraint
   ↓
IMPLEMENTATION (small / local / explicit effects / typed invariants)
   ↓
┌──────────────┬──────────────┬──────────────────┐
CONTRACT TESTS   PROPERTY TESTS   ARCH FITNESS FUNCTIONS
MUTATION TESTS   METAMORPHIC      DEPENDENCY / NEGATIVE RULES
└──────────────┴──────────────┴──────────────────┘
   ↓
OBSERVABILITY (semantic telemetry, not logs)
   ↓
PROVENANCE / EVIDENCE (независимый, adversarial review)
   ↓
DECISION / DURABLE RESIDUE
   ↓
[ deletion loop: та же evidence bar, что и addition ] ──▶ обратно к INVARIANTS
```

---

## 23. ФИНАЛЬНАЯ МАТРИЦА УРОВНЕЙ

| Уровень | Главный вопрос |
|---|---|
| Semantic | Что система означает? |
| Domain | Что реально существует в предметной области? |
| Abstraction | Что invariant, а что variable? |
| Modularity | Что может меняться независимо? |
| Dependency | Кто должен что знать? |
| Ownership | Кто имеет право принимать решение? |
| State | Какие состояния допустимы? |
| Transition | Какие переходы разрешены? |
| Concurrency | Что может происходить одновременно? |
| Authority | Что является источником истины? |
| Derivation | Что является производным? |
| Contract | Что обещано на границе? |
| Representation | Как сделать корректное поведение конструктивным? |
| Effects | Какие действия система реально выполняет? |
| Testing | Как мы можем доказать и опровергнуть claim? |
| Diagnostics | Где первая divergence? |
| Observability | Как восстановить causal chain? |
| Security | Что запрещено и кому? |
| Reliability | Как система деградирует и восстанавливается? |
| Performance | Где доказанная стоимость? |
| Evolution | Как менять representation без semantic break? |
| Provenance | Откуда взялось это решение и этот artifact? |
| Governance | Кто контролирует изменение? |
| Organization | Где проходят ownership/communication boundaries? |
| AI | Как сделать систему устойчивой к локально правдоподобным ошибкам агента? |

---

## 24. ФИНАЛЬНЫЕ ГЛОБАЛЬНЫЕ ПРАВИЛА (сведены в 13 пунктов)

1. **Intent before implementation** — сначала semantic effect, потом код.
2. **Invariant before abstraction** — сначала stable core, потом абстракция.
3. **Variation must have an owner** — у каждой ветвящейся изменчивости — локальный владелец.
4. **Boundaries are executable** — архитектурные границы проверяются автоматикой, не памятью.
5. **Prefer existing primitives** — новая сущность требует отдельного доказательства необходимости (§21 gate).
6. **Effects must be visible** — IO/state/authority/timing/retries не скрыты внутри функций.
7. **Claims require discriminating evidence** — не «тест прошёл», а «альтернативная гипотеза отвергнута».
8. **Diagnose before redesign** — сначала first divergence/causal slice/minimal witness.
9. **Semantic diff over textual diff** — ревью поведения, не строк.
10. **Metrics are evidence, not truth** — каждая метрика проходит anti-Goodhart check, включая метрики самой архитектуры.
11. **Persist durable residue only** — сохранять то, что изменит будущее решение, не факт, что работа была проделана.
12. **Architecture must resist its future authors** — корректность сохраняется, даже если следующий автор — человек, другой агент или LLM.
13. **Subtraction requires the same evidence bar as addition** — удаление проходит Chesterton's Fence → Material Verdict Test в обратную сторону → обязано снижать, а не переносить connascence.

---

## 25. УЛЬТИМАТИВНЫЕ ТЕЗИСЫ (дайджест, без повторов с §24)

1. Абстракция — управление будущим изменением, не сокращение кода.
2. Модульность определяется независимостью изменения, а не размером файла.
3. God Object — концентрация независимых решений и ownership, а не просто большой класс.
4. Spaghetti возникает, когда semantic boundaries перестают совпадать с dependency/control boundaries.
5. Паттерн без доказанной потребности — decorative complexity.
6. Производное не должно становиться authority.
7. Invalid state лучше запрещать представлением, чем ловить тестами.
8. Тесты проверяют свойства и отношения, а не только примеры; falsification сильнее подтверждения красивым примером.
9. Observability — способность восстановить causal story системы.
10. Чем выше blast radius и irreversibility, тем выше должен быть evidence threshold.
11. Security, testing, architecture и observability используют одну и ту же идею: ограничивать недопустимые переходы, делать допустимые отношения наблюдаемыми.
12. AI не должен быть архитектором по умолчанию — он работает внутри явных contracts, invariants, boundaries и gates (LLM как drafter, не как источник domain-valid architectural judgment).
13. Лучшая защита от плохого AI-code — не лучший prompt, а substrate, в котором неправильное решение дорого, заметно и структурно ограничено.

---

## 26. ГЛАВНОЕ ПРАВИЛО СИСТЕМЫ

> **Не добавляй структуру, если она не локализует изменчивость, не защищает инвариант, не уменьшает change surface, не ограничивает authority, не делает effect наблюдаемым, не снижает failure class и не усиливает доказательность.**

И симметрично:

> **Если правило можно сделать конструктивным — сделай его конструктивным. Если архитектурное ограничение можно проверить машиной — проверяй машиной. Если claim можно сфальсифицировать дешёвым тестом — сначала сфальсифицируй. Если invariant можно выразить типом или representation — не оставляй его только в документации. Если изменение можно сделать обратимым — не делай его необратимым без необходимости.**

### Финальная формула
```
INTENT → SEMANTICS → INVARIANTS → VARIATIONS → OWNERSHIP → BOUNDARIES →
REPRESENTATION → EFFECTS → IMPLEMENTATION → VERIFICATION → OBSERVATION →
EVIDENCE → CONTROL → EVOLUTION
```
```
QUALITY ≈ semantic correctness × boundary integrity × evidence strength ×
          observability × reversibility × maintainability
```
Failure modes (`AI-code, spaghetti, God Object, architecture erosion, semantic drift, test illusion, metric gaming, hidden coupling, authority confusion, state corruption, diagnostic pollution, security leakage, irreversible mistakes`) — не случайности, а проявления одного дефекта: **система перестала ясно различать семантику, ответственность, изменчивость, authority, state transition и evidence — и попыталась компенсировать это дополнительным кодом.**

Ultimate engineering goal — не сделать код «умным», а сделать систему такой, чтобы правильные отношения были явными, неправильные — труднодостижимыми, изменения — локальными, эффекты — наблюдаемыми, утверждения — проверяемыми, а архитектурная деградация — обнаруживаемой и исправимой до того, как станет системным долгом.

**Главная единица хорошей архитектуры — не `class`, не `function` и не `pattern`, а доказанный invariant с ясным owner, boundary, transition и способом его проверки.**

---

## 27. ЧТО ДЕЛАЕТ ЭТУ СИСТЕМУ ОТЛИЧНОЙ ОТ «ГАЙДА ПО ЧИСТОМУ КОДУ»

1. Information hiding + connascence + change propagation — предотвращает связанность до появления God Object, не после.
2. Contract/property/metamorphic/mutation/stateful testing — тестирует отношения, а не примеры.
3. Architecture fitness functions + policy-as-code — правило не зависит от памяти человека или LLM.
4. Semantic provenance + observability contracts + adversarial review — для любого поведения есть ответ: почему существует → что меняет → чем доказано независимо → кто владеет → как наблюдать → как воспроизвести → на каких условиях можно удалить.

Комбинация этих направлений с симметрией addition/deletion (§21, §24.13) превращает набор правил в **самоконтролируемую инженерную среду**, где плохому коду структурно трудно возникнуть — и легко раствориться, если он всё же возник.

---

## ТАБЛИЦА: РАСХОЖДЕНИЯ И НЕСТЫКОВКИ МЕЖДУ ИСТОЧНИКАМИ

Содержательных логических противоречий между документами не найдено — это два изложения одной доктрины разной степени детализации. Ниже — структурные и терминологические расхождения, которые стоит иметь в виду при использовании объединённого документа.

| № | Тема | Источник 1 (code-integrity) | Источник 2 (SSI Framework) | Характер расхождения / как снято в этом документе |
|---|---|---|---|---|
| 1 | Число «финальных» правил | §15: ровно «13, не 12» глобальных правил | §34: отдельный список из 12 «Global Anti-AI-Code Rules» (другое содержание) + §38: 20 «ультимативных тезисов» | Не противоречие, а **две параллельные системы нумерации** с разным охватом (общие принципы vs. AI-специфичные негативные правила vs. тезисы-дайджест). В объединённом документе разведены по §19 (негативные правила), §24 (13 правил) и §25 (тезисы-дайджест), с явной пометкой, что это разные срезы одной доктрины. |
| 2 | Полнота словаря антипаттернов | §13: 10 терминов, включая `Context Laundering`, без классических smells (Feature Envy, Shotgun Surgery и т.д.) | §4: 17 терминов, включает классические smells, но не называет `Context Laundering` отдельно | Не противоречие — разная степень детализации. Объединено в единый словарь §4 без потерь. |
| 3 | Testing Trophy (Kent C. Dodds) | Упоминается явно (§6) | Не упоминается | Дополнение, не конфликт. Сохранено как есть в §7. |
| 4 | Postel's Law как ловушка | Разбирается явно с выводом «strict-in/strict-out by default» (§13) | Не упоминается напрямую, но косвенно согласуется через «Fail Closed» (§22) | Направления совпадают (оба требуют строгого поведения по умолчанию); прямого конфликта нет — терминологическое дополнение сохранено в §4. |
| 5 | Metric anti-Goodhart: набор пар | `documentation↑≠transparency↑`, `fitness function green≠architecture clean`, но без `performance↑≠efficiency↑` | Есть `performance↑≠efficiency↑`, но нет явной пары про fitness function (хотя есть эквивалент в §0 меты) | Не конфликт — объединены в один список без потерь (§11.1). |
| 6 | Runtime-Promotion Gate: терминология полей | `OWNER`, `PROMOTION GATE` (§16) | `semantic owner`, `phase/gate` (§3) | Синонимия, не противоречие — унифицировано как `OWNER` и `PROMOTION GATE` в §21. |
| 7 | Степень детализации разделов Security / Data evolution / Control theory / Reliability | Кратко или отсутствует (§12 — только производительность, без отдельных Security/Reliability/Control theory разделов) | Разворачивает в отдельные §22–26 подробно | Источник 1 не противоречит, а просто не покрывает эти темы на таком уровне детализации — включено из источника 2 без изменений (§12–14 объединённого документа). |
| 8 | Мета-принцип «система применяет себя к себе» | Есть явный §0 с 5-пунктовым Material Verdict Test как отдельная секция верхнего уровня | Тот же тест упомянут по частям (Runtime-Promotion Gate, Architectural Value Model §36), но не выделен в отдельный «мета-раздел 0» | Не конфликт — источник 1 даёт более сильную формулировку. Сохранена как раздел §0 целиком. |

**Вывод по расхождениям**: оба документа взаимно непротиворечивы на уровне принципов; расхождения касаются исключительно (а) глубины детализации отдельных тем и (б) параллельных, слегка различных схем нумерации «финальных списков правил», которые в этом документе сведены к единой иерархии: **негативные правила (§19) → 13 глобальных принципов (§24) → тезисы-дайджест (§25) → главное правило (§26)**.
