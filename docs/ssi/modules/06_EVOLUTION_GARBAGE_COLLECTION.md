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


## 38.1 Decision memory and proof-carrying change

Material design decision сохранять как:

```text
context → decision → rejected alternatives → invariants → consequences → owner → expiry/review trigger
```

Material change передаётся вместе с evidence package, а не только code diff:

```text
intent + invariants + semantic delta + verification + provenance + runtime/rollback plan
```

ADR/RFC/decision-record не заменяют proof; они сохраняют rationale и future constraints.
