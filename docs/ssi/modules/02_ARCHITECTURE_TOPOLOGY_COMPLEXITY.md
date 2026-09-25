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


## 29.3 Multi-layer topology

Для material architecture различать:

```text
STRUCTURAL / CHANGE / RUNTIME / OWNERSHIP
SEMANTIC / AUTHORITY / DATA / DEPLOYMENT
```

Архитектурное здоровье — это согласованность этих views и их trajectory, а не snapshot dependency graph.

## 29.4 Semantic footprint and change locality

Для boundary фиксировать `READS / WRITES / OWNS / OBSERVES / AUTHORIZES / EMITS / TIMING`. Если локальное изменение систематически требует reasoning за пределами footprint, boundary или ownership подозрительно. Проверять change propagation empirically.
