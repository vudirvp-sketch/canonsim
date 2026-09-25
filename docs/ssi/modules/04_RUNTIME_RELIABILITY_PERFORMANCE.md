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


## 40.1 Work amplification budget

Отдельно наблюдать:

```text
1 semantic action
→ fanout
→ duplicate work
→ retry work
→ timeout/recovery work
```

Reliability/performance control должен ограничивать не только latency/CPU, но и amplification. Для material action нужен budget, bound или explicit stop rule.

## 40.2 Progressive delivery / burn-rate control

Material rollout:

```text
baseline → canary/staged exposure → SLI comparison → stop rule → rollback/containment
```

Error-budget burn-rate — operational control; delivery metrics — delivery health indicators. Ни один из них не является единственным архитектурным truth metric.

## 40.3 Controlled failure injection

Chaos/game-day сценарий оформлять тем же Experiment Contract:

```text
hypothesis → intervention → realized delta → discriminant → spillover → disposition
```
