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
A. PROBLEM MODE
B. INTENT
C. CURRENT SUBSTRATE
D. CLAIMS + EVIDENCE
E. INVARIANTS
F. CHANGE RISK / REVERSIBILITY
G. OWNER / AUTHORITY / CAPABILITY
H. BOUNDARY / TOPOLOGY / FOOTPRINT
I. STATE / LIFETIME
J. REPRESENTATION / COMPLEXITY / WORK
K. EXISTING PRIMITIVES
L. SEMANTIC TYPES / CONTRACTS
M. IMPLEMENTATION / EFFECTS
N. STATIC POLICY
O. COMPOSITIONAL REASONING
P. TESTING / FUZZ / MUTATION / SIMULATION
Q. SEMANTIC DIFF
R. ADVERSARIAL VERIFICATION
S. BUILD / PROVENANCE
T. RUNTIME / ROLLOUT / STOP RULE
U. PROOF-CARRYING CHANGE
V. DISPOSITION
W. DURABLE RESIDUE / GC
```

Нельзя переходить к `M. IMPLEMENTATION`, если не заполнены `A–L`, кроме R0-изменений.

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
