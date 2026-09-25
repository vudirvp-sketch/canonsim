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

---

## 28. ARCHITECTURE TOPOLOGY: СМОТРИ НЕ ТОЛЬКО НА DEPENDENCY GRAPH

Static imports, calls и inheritance показывают **структурную связанность**, но не всю реальную связанность системы. Production-архитектура имеет минимум четыре графа:

```text
STRUCTURAL   = кто кого импортирует / вызывает
CHANGE       = что фактически меняется вместе
RUNTIME      = кто реально влияет на кого
OWNERSHIP    = кто имеет право менять / решать
```

Главный объект контроля:

```text
ARCHITECTURE HEALTH = structural topology
                    + change topology
                    + runtime topology
                    + ownership topology
```

### 28.1 Hidden coupling

Если `A` и `B` не имеют прямой зависимости, но почти каждое изменение `A` требует изменения `B`, это **logical/co-change coupling**. Если изменение маленького узла регулярно распространяется через много boundary/owner edges — это архитектурный сигнал, даже когда static dependency graph выглядит «чисто».

Инструменты/методы: `Design Structure Matrix (DSM)` · dependency matrix · co-change analysis · change propagation graph · architecture recovery.

**Правило:**

> `low import coupling ≠ low change coupling`.

### 28.2 Architecture Drift

Контролировать нужно не snapshot, а траекторию:

```text
baseline → observed architecture → delta → erosion rate → budget → correction
```

Architecture Fitness Function должна проверять не только `violation == 0`, но и:

```text
cycle growth
boundary-crossing growth
public-surface growth
primitive growth
semantic duplication growth
ownership spread
orphan abstraction growth
```

`green today` не означает `healthy trajectory`.

---

## 29. COMPLEXITY ENGINEERING: СЧИТАЙ ПРОСТРАНСТВО ВОЗМОЖНОСТЕЙ

LOC, class count и cyclomatic complexity — только частичные proxies. Для semantic engineering считать нужно **сколько различий должен удерживать в голове человек/агент и сколько вариантов должна различать система**.

```text
essential complexity
accidental complexity
state-space complexity
interaction complexity
dependency complexity
change complexity
cognitive complexity
operational complexity
```

### 29.1 State-space complexity

Приближённо:

```text
state space ≈ states × transitions × actors × permissions × timing × retry × concurrency modes
```

Это не универсальная формула метрики, а reminder: увеличение независимых измерений быстро создаёт combinatorial explosion.

### 29.2 Complexity budget

У каждого material subsystem должны быть budgets хотя бы для:

```text
states
transition classes
public entry points
independent variation axes
boundary crossings
authority crossings
ambient dependencies
failure modes
retry paths
concurrency paths
```

**Правило:**

> Оптимизируй не размер кода, а число независимых семантических различий, которое требуется различать для безопасного изменения.

---

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

## 35. REPRODUCIBLE ENGINEERING & SUPPLY-CHAIN CONTROL

Traceability должна переходить в воспроизводимость:

```text
source
→ declared inputs
→ hermetic build
→ deterministic artifact
→ attestation
→ deployment provenance
→ runtime provenance
```

Ключевые свойства: `hermeticity` · dependency pinning · immutable artifacts · reproducible builds · SBOM · signed/verified attestations · source/build provenance.

SLSA v1.2 формализует provenance как проверяемую информацию о том, где, когда и как был произведён software artifact, и расширяет supply-chain control на source track.

**Правило:**

> Нельзя считать artifact «доказанным», если нельзя восстановить критический путь `source → inputs → build → artifact`.

---

## 36. AI AGENT = PRIVILEGED RUNTIME

AI coding agent не считать «текстовым помощником». Современные agentic coding tools могут читать проект, запускать команды, устанавливать пакеты, редактировать файлы, работать с сетью и изменять build/CI/deployment поверхности. Поэтому capability model относится к агенту так же, как к любому privileged runtime.

### 36.1 Agent Capability Model

```text
agent identity
→ task scope
→ tool capability
→ resource scope
→ operation scope
→ data classification
→ approval gate
→ audit trail
→ revocation
```

По умолчанию:

```text
least privilege
read-only where possible
sandboxed runtime
restricted filesystem
restricted network egress
ephemeral credentials
bounded CPU/memory/processes
tool allowlist
explicit high-impact approval
```

Практика OWASP для agentic coding включает sandboxing, tool allowlists, egress controls, ephemeral credentials и защиту чувствительных файлов/секретов.

### 36.2 Untrusted context

Repository text, issue bodies, PR descriptions, comments, logs, fetched pages и tool descriptions могут быть **instruction-bearing input**, а не trusted policy. Поэтому:

```text
DATA ≠ INSTRUCTION
OBSERVATION ≠ AUTHORITY
TOOL DESCRIPTION ≠ POLICY
REPOSITORY FILE ≠ TRUSTED AGENT RULE
```

### 36.3 High-impact surfaces

Повышенный gate для AI-изменений:

```text
CI/CD
build scripts
package scripts
Dockerfiles
deployment config
permissions/auth
secrets
schema migrations
lockfiles/dependency resolution
agent rules / tool configuration
```

**Правило:**

> Агенту запрещено одновременно быть генератором, единственным verifier'ом и владельцем irreversible action.

---

## 37. CHANGE RISK CLASSIFICATION

Одинаковый процесс проверки для всех изменений создаёт либо bureaucratic drag, либо недостаток контроля. Ввести risk classes:

```text
R0  text/style only
R1  local pure refactor
R2  local behavior change
R3  cross-boundary / dependency change
R4  state / authority / schema / public API change
R5  security / distributed / irreversible / external-contract change
```

Минимально обязательное доказательство растёт вместе с:

```text
blast radius × irreversibility × privilege × uncertainty
```

Для R4/R5 автоматически повышать:

```text
review independence
contract tests
migration/rollback plan
runtime observation
semantic diff
counterexample path
provenance
progressive rollout
```

---

## 38. ARCHITECTURE GARBAGE COLLECTION

Архитектура деградирует не только через addition, но и через **accumulation of obsolete residue**:

```text
dead code
dead flags
obsolete adapters
unused capabilities
duplicate primitives
stale telemetry
compatibility branches
orphan abstractions
orphan docs
obsolete schemas
```

Цикл:

```text
detect orphan
→ recover historical constraint
→ prove consumer absence
→ prove authority absence
→ remove
→ verify blast/coupling reduction
→ record durable residue
```

Это симметрично promotion gate:

> **Deletion требует не меньшего evidence bar, чем addition, но её результат должен измеряться как уменьшение сложности/connascence, а не перенос проблемы.**

---

## 39. BOUNDARY CALCULUS

Граница — не только модуль/папка/API. Для каждой material boundary оценивать:

```text
semantic cohesion
independent change frequency
coupling strength
change propagation
failure propagation
authority crossing
data crossing
latency cost
owner count
cognitive load
```

Хорошая граница приблизительно имеет:

```text
high semantic cohesion
+ low independent-change coupling
+ low blast propagation
+ clear authority
+ small cognitive surface
```

**Не применять автоматически:** SRP → more classes, microservices → better boundaries, interface → decoupling. Форма не доказывает границу.

---

## 40. RESOURCE / RELIABILITY BUDGETS

Ресурсы reliability должны быть ограничиваемы так же, как CPU:

```text
retry budget
concurrency budget
queue budget
timeout budget
latency budget
memory budget
dependency-call budget
blast-radius budget
error budget
```

Плохая автоматизация часто образует положительную обратную связь:

```text
slow
→ increase concurrency
→ overload
→ latency increases
→ timeout
→ more retry
→ more load
→ collapse
```

Поэтому corrective action должен быть:

```text
bounded
observable
reversible
proportional
```

---

## 41. SPECIFICATION MINING & ARCHITECTURE RECOVERY

Legacy система часто не имеет надёжной документации. Не переписывать «из головы», а извлекать observed specification:

```text
runtime traces
+ call patterns
+ state transitions
+ co-change
+ dependency graph
+ ownership history
+ exception behavior
→ inferred contracts
→ characterization
→ explicit specification
→ controlled refactor
```

Различать:

```text
intended architecture
implemented architecture
runtime architecture
ownership architecture
```

Их расхождение — самостоятельный diagnostic signal.

**Rule:**

> Для legacy сначала восстанавливай фактическую семантику; только потом объявляй отклонение архитектурой.

---

## 42. EVIDENCE INDEPENDENCE

Подтверждения нельзя автоматически считать независимыми, если они используют один источник ошибки:

```text
same agent
same model
same prompt
same implementation
same tests
same oracle
same metric
same observation boundary
```

Сильнее:

```text
generator
≠ verifier
≠ oracle
≠ runtime witness
```

Практическая цепочка:

```text
AI proposes
→ compiler/static policy
→ tests
→ mutation/fuzz
→ independent critic
→ runtime evidence
→ disposition
```

Независимость — не формальность: два разных инструмента с общей blind spot не являются двумя доказательствами.

---

## 43. CONTROL LOOP ДЛЯ АРХИТЕКТУРНОЙ ЭНТРОПИИ

Операционная модель всей доктрины:

```text
TARGET ARCHITECTURE
        ↓
OBSERVE topology / complexity / failures / drift / provenance
        ↓
DETECT deviation
        ↓
DIAGNOSE causal slice
        ↓
CHOOSE minimum corrective intervention
        ↓
VERIFY semantic + architectural consequences
        ↓
ROLL OUT reversibly where possible
        ↓
RE-OBSERVE
        ↓
GC obsolete residue
```

Это делает архитектуру **closed-loop control system**, а не статическим набором правил.

---

## 44. AGENT NAVIGATION CONTRACT: НЕ ПРОПУСКАЙ БЛОКИ

При работе AI-агента с системой этот документ читать не линейно «по вдохновению», а как protocol.

### 44.1 Mandatory traversal

```text
A. INTENT
B. CURRENT SUBSTRATE
C. INVARIANTS
D. CHANGE RISK
E. OWNER / AUTHORITY
F. BOUNDARY / TOPOLOGY
G. COMPLEXITY / STATE SPACE
H. EXISTING PRIMITIVES
I. IMPLEMENTATION / EFFECTS
J. STATIC POLICY
K. TESTING / FUZZ / MUTATION
L. SEMANTIC DIFF
M. ADVERSARIAL VERIFICATION
N. BUILD / PROVENANCE
O. RUNTIME OBSERVATION
P. DISPOSITION
Q. DURABLE RESIDUE / GC
```

Нельзя переходить к `I. IMPLEMENTATION`, если не заполнены `A–H`, кроме R0-изменений.

### 44.2 Block completion state

Каждый material block должен иметь:

```text
NOT_APPLICABLE
OPEN
PARTIAL
VERIFIED
WAIVED
```

`WAIVED` требует `owner + reason + expiry + blast assessment`.

### 44.3 No silent skip

Если агент не применяет блок:

```text
BLOCK = NOT_APPLICABLE
WHY = ...
EVIDENCE = ...
```

Запрет: молча пропускать архитектурный/verification block.

---

## 45. MACHINE-READABLE GOVERNANCE

Для repository-level внедрения держать рядом с кодом минимум:

```text
ssi/
  README.md
  manifest.yaml
  controls/
    architecture.yaml
    boundaries.yaml
    risk-classes.yaml
    agent-capabilities.yaml
    negative-rules.yaml
  templates/
    change-record.md
    semantic-diff.md
    counterexample.md
    review-card.md
    deletion-card.md
    experiment-contract.md
```

Каждое правило по возможности имеет поля:

```yaml
id:
name:
scope:
intent:
forbidden:
required_evidence:
falsifier:
enforcement:
owner:
risk_classes:
exception:
expiry:
```

**Rule:** documentation-only control = advisory; executable control = enforced; отсутствующий `owner/falsifier` = незрелое правило.

---

## 46. EXPANDED CHANGE PROTOCOL

Материализовать единый процесс как карточку изменения:

```text
01 INTENT
02 CURRENT SUBSTRATE
03 CLAIMS + EVIDENCE STATUS
04 INVARIANTS / CONTRACTS
05 RISK CLASS
06 AUTHORITY / OWNER
07 CHANGE TOPOLOGY
08 BOUNDARY DECISION
09 STATE / TRANSITION IMPACT
10 COMPLEXITY / BUDGET IMPACT
11 EXISTING PRIMITIVES CHECK
12 COMPETING EXPLANATIONS
13 CHEAPEST FALSIFIER
14 MINIMUM DESIGN
15 IMPLEMENTATION + EFFECT SURFACE
16 STATIC POLICY CHECKS
17 CONTRACT / PROPERTY / METAMORPHIC / MUTATION / FUZZ / MODEL TESTS
18 SEMANTIC DIFF
19 ADVERSARIAL REVIEW
20 BUILD / PROVENANCE
21 RUNTIME OBSERVATION
22 ROLLOUT / REVERSIBILITY
23 DISPOSITION
24 DURABLE RESIDUE
25 GARBAGE COLLECTION OPPORTUNITY
```

---

## 47. CONSOLIDATED ANTI-AI-CODE LAWS

Добавление к §19 и §24. Эти правила сильнее stylistic guidance:

```text
NO CODE WITHOUT SEMANTIC OWNER.
NO ABSTRACTION WITHOUT STABLE COMMONALITY.
NO NEW PRIMITIVE WITHOUT MATERIAL GAP.
NO HIDDEN EFFECT.
NO UNBOUNDED LIFETIME.
NO UNBOUNDED RETRY / CONCURRENCY / QUEUE.
NO TRUSTED INTERPRETATION OF UNTRUSTED AGENT CONTEXT.
NO IRREVERSIBLE AGENT ACTION WITHOUT INDEPENDENT GATE.
NO ARCHITECTURE HEALTH CLAIM FROM SNAPSHOT METRICS ALONE.
NO DEPENDENCY GRAPH CLAIM WITHOUT CHANGE-TOPOLOGY CHECK.
NO GREEN TEST SUITE WITHOUT SEMANTIC SENSITIVITY EVIDENCE.
NO ARTIFACT TRUST WITHOUT PROVENANCE.
NO LIVENESS CLAIM WITHOUT PROGRESS ASSUMPTION.
NO DELETION WITHOUT HISTORICAL-CONSTRAINT CHECK.
NO SILENT BLOCK SKIP.
NO SINGLE-ACTOR / SINGLE-ORACLE / SINGLE-METRIC EVIDENCE FOR MATERIAL CLAIMS.
NO NEW COMPLEXITY WITHOUT MEASURED CAPABILITY LEVERAGE.
```

---

## 48. UPDATED ULTIMATE MODEL

```text
DOMAIN INTENT
    ↓
SPECIFICATION / SCENARIOS
    ↓
INVARIANTS / CONTRACTS
    ↓
RISK + REVERSIBILITY
    ↓
OWNERSHIP / AUTHORITY
    ↓
BOUNDARY + CHANGE TOPOLOGY
    ↓
STATE / TRANSITIONS / LIFETIME
    ↓
REPRESENTATION + COMPLEXITY BUDGET
    ↓
MINIMUM EXISTING SUBSTRATE
    ↓
IMPLEMENTATION + EXPLICIT EFFECTS
    ↓
STATIC SEMANTIC ENFORCEMENT
    ↓
CONTRACT / PROPERTY / FUZZ / MUTATION / MODEL VERIFICATION
    ↓
SEMANTIC DIFF + ADVERSARIAL REVIEW
    ↓
HERMETIC BUILD + PROVENANCE
    ↓
PROGRESSIVE RUNTIME OBSERVATION
    ↓
DISPOSITION + DURABLE RESIDUE
    ↓
ARCHITECTURE DRIFT / GARBAGE COLLECTION
    ↺
```

### Final law

> **Не пытайся заставить агента никогда ошибаться. Строй substrate, где ошибка локализуема, capability ограничена, invariant конструктивен, effect наблюдаем, claim фальсифицируем, artifact воспроизводим, irreversible action gated, архитектурная деградация измеряется во времени, а obsolete complexity систематически удаляется.**

---

## 49. CURRENT EXTERNAL ANCHORS

Это не новые правила доктрины, а reference anchors для отдельных расширений:

- `TLA+ / TLC` — formal specification, temporal reasoning, model checking для concurrent/distributed systems. 
- `SLSA v1.2` — source/build supply-chain security и provenance.
- `OWASP Secure Coding with AI` — agentic coding security, sandboxing, tool scoping, untrusted repository context, CI/build/deployment gates.
- `OWASP AI Agent Security` — excessive autonomy, high-impact actions, least-privilege tool security, approval boundaries.

При использовании этих anchors требования должны проходить тот же Material Verdict Test, что и любой внешний transfer.

---

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


## 51. CANONICAL V3 MODEL

```text
PROBLEM MODE
    ↓
DOMAIN INTENT / SCENARIOS
    ↓
CLAIMS / EVIDENCE STATUS
    ↓
INVARIANTS / CONTRACTS
    ↓
RISK / REVERSIBILITY / BLAST RADIUS
    ↓
OWNER / AUTHORITY / CAPABILITY
    ↓
BOUNDARY / TOPOLOGY / SEMANTIC FOOTPRINT
    ↓
STATE / TRANSITIONS / LIFETIME
    ↓
REPRESENTATION / TYPESTATE / COMPLEXITY / WORK BUDGET
    ↓
EXISTING SUBSTRATE / MINIMUM PRIMITIVE
    ↓
IMPLEMENTATION / EXPLICIT EFFECTS
    ↓
STATIC POLICY / ABSTRACT ANALYSIS
    ↓
COMPOSITIONAL REASONING / REFINEMENT
    ↓
PROPERTY / METAMORPHIC / MUTATION / FUZZ / DETERMINISTIC SIMULATION / MODEL PROOF
    ↓
SEMANTIC DIFF / OBSERVATIONAL EQUIVALENCE / ADVERSARIAL REVIEW
    ↓
HERMETIC BUILD / PROVENANCE / CLAIM TRACE
    ↓
CANARY / RUNTIME OBSERVATION / BURN-RATE / STOP RULE
    ↓
PROOF-CARRYING CHANGE
    ↓
DISPOSITION / DURABLE RESIDUE
    ↓
ARCHITECTURE DRIFT / GARBAGE COLLECTION
    ↺
```

## 52. ULTIMATE V3 LAWS

```text
NO UNOWNED SEMANTICS.
NO UNREPRESENTED MATERIAL INVARIANTS WHEN THE SUBSTRATE CAN REPRESENT THEM.
NO UNBOUNDED AUTHORITY.
NO HIDDEN EFFECT.
NO INVALID STATE WHEN INVALID STATE CAN BE MADE UNREPRESENTABLE.
NO UNPROVEN COMPOSITION.
NO MATERIAL SEMANTIC DELTA HIDDEN BY TEXTUAL REFACTOR.
NO UNBOUNDED LIFETIME / RETRY / CONCURRENCY / QUEUE / WORK AMPLIFICATION.
NO MATERIAL CLAIM WITHOUT SOURCE, STATUS, VERIFIER AND OBSERVATION SCOPE.
NO SINGLE ORACLE / METRIC / AGENT AS SOLE EVIDENCE FOR MATERIAL CLAIMS.
NO TRUST OF TOOL PROVIDER FROM DESCRIPTION ALONE.
NO MATERIAL AGENT ACTION WITH INSUFFICIENT EFFECTIVE CONTEXT.
NO IRREVERSIBLE CHANGE WITHOUT INDEPENDENT GATE OR EXPLICIT CONTAINMENT.
NO GREEN CI AS A SUBSTITUTE FOR SEMANTIC ADEQUACY.
NO ARCHITECTURE HEALTH CLAIM FROM SNAPSHOT METRICS ALONE.
NO ARTIFACT TRUST WITHOUT PROVENANCE.
NO LIVENESS CLAIM WITHOUT PROGRESS ASSUMPTIONS.
NO DELETION WITHOUT CONSTRAINT RECOVERY.
NO NEW COMPLEXITY WITHOUT MATERIAL CAPABILITY LEVERAGE.
EVERY MATERIAL CHANGE CARRIES ITS OWN EVIDENCE PACKAGE.
```

### Final V3 law

> **Не пытайся сделать агента безошибочным. Ограничивай пространство допустимых программ и действий; делай material invariants конструктивными, authority минимальной, effects наблюдаемыми, composition доказуемой, claims traceable, distributed failures replayable, rollout reversible/contained, а добавленную сложность удаляемой.**
