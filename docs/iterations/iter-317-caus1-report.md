# iter-317 · caus1 — контракт каузальной достаточности (T1+T2-пара с sem-1, review-C2/D2)

**Вызов владельца (2026-10-03, дословно):** «продолжай работу прошлой
итерации, sem1 открывай и так далее» — продолжение по подтверждённой
очереди; caus-1 — естественная пара sem-1 (собственная
последовательность T1+T2 пакета concept-review).

## A. Что сделано

- **Контракт caus-1 ПРИЗЕМЛЁН** в `docs/CONTRACTS.md` §7 — шесть
  пинированных решений, каждое привязано к живому коду:
  - **K1 причинный хребет, три части, без графа**:
    `primary_cause + necessary_supports[] + provenance`. Сегодняшний
    `cause` — слот primary-cause (писатель-принуждаемая цепочка;
    `core/loop.py` ставит `writer.last_id` — хронологический закон;
    `cause_hook` (D-140) и `based_on_event_seq` (OCC) —
    посемейные атрибуции, которые хребет сохраняет).
    `necessary_supports[]` — НОВАЯ декларируемая заявка: события, БЕЗ
    КАЖДОГО из которых исход недостижим. `provenance` остаётся
    блоком родословной (seed / cause_intent / cause_hook /
    assignment_tick, D-236) — НИКОГДА не причинная заявка.
  - **K2 контрфактическая необходимость** — поддержка X необходима ⟺
    same-seed абляция X делает заявленный исход НЕДОСТИЖИМЫМ (нет
    события с идентичностью исхода: тип + актор + материальное
    семейство эффектов; замены вида `intent_rejected` не считаются).
  - **K3 раскол необходимость/свидетельство** — опциональное
    свидетельство (восприятие, амбиент, даунстрим) живёт там, где
    живёт (knowledge/проекция/payload), НИКОГДА в supports.
    Дискриминирующий тест — абляционная пара: удаление свидетельства
    оставляет исход достижимым (возможно со сдвигом тика/ветви),
    удаление поддержки убивает.
  - **K4 абляционная батарея — только OFF-LINE** — инструмент
    приземлённой формы BASE/PERTURBED (`scripts/divergence_probe.py`,
    D-235); никогда внутри тик-цикла — рантаймного пере-вывода
    необходимости нет (близнец S1: запрет второго резолвера держит и
    для причинных заявок).
  - **K5 продюсер декларирует, батарея верифицирует** —
    necessary_supports это заявка ПРОДЮСЕРА (резолвер называет
    события, установившие факты, которые его резолюция материально
    использовала — read-set × устанавливающие события; индекс
    `_last_change` (L3, D-050) — существующее зерно вывода).
    Декларация, переживающая абляцию, — ОПРОВЕРГНУТА (RED).
  - **K6 совместимость + запрет DAG** — аддитивное
    provenance-семейное поле (любой schema-бамп — дело строки
    имплементации через AGENTS §8 stop&confirm); INV-5: ссылки на
    закоммиченные id, append-only; потребители (divergence_probe,
    observatory, hook-семейство, brief/validator, census) — только
    аддитивно. ЗАПРЕЩЕНО: DAG-хранилище, обход графа, provenance-движки.
- **Абляционный фальсификатор ПРОГОНЁН ВЖИВУЮ** (скрипт вне репо,
  Rule 9; seed 8, шаги day1-кражи + одна вставленная перцепция) —
  см. §D.
- **Минимальный тест-сет будущей строки имплементации закреплён.**

## B. Что НЕ сделано (честно)

- **Ни строчки кода** — ни поля, ни schema-изменения, ни
  DAG/движка (закон строки). Имплементация — НЕ строка: владелец
  открывает после приёмки контракта.
- **DECISIONS.md не тронут** (кап 30/30) — исполняется
  подтверждённая очередь (review-D2 принят iter-315); запись —
  CONTRACTS §7 + TASKS + этот отчёт.
- **llama.cpp не устанавливался** — R0/R1 строка (как iter-316).

## C. Связь с соседями

- sem-1 (§6): та же дисциплина «продюсер декларирует — проверка не
  пере-выводит»; K4 — emit-близнец S1/S4.
- replay-1 (следующая строка): identity-кортеж replay опирается на
  ту же самость прогона, что и абляционная пара (same-seed,
  same-prefix); контракты не перекрываются: caus-1 — о причинной
  достаточности записей, replay-1 — о тождестве продолжения.
- core-1-C3 (история/масштаб): батарея работает поверх логов —
  цена батарей на больших логах это measured-native-limit-вопрос
  core-1, не этот контракт.

## D. Аblation-проба — живой прогон

```
[BASE] 16 events; the steal outcome: ev_0007 type='steal' cause='ev_0006'
       state_changes=['purse_01.carrier']
[BASE] the outcome's `cause` names ev_0006 ('look_around') — the CHRONOLOGICAL
       predecessor (writer.last_id at build), never the materially-required move
[BASE] the materially-REQUIRED ev_0005 (move->loc_tavern) and the
       correlated-but-not-required ev_0006 (look_around) are INDISTINGUISHABLE
       in the outcome's own fields — the necessity is unrecorded (review-C2's gap)
[ABLATE-MOVE] steal-family outcomes: 0; intent_rejected: 3 — the BASE outcome
       is UNREACHABLE (necessity of the move shown)
[ABLATE-LOOK] steal-family outcomes: 1 ('steal' at t=6) — the outcome REMAINS
       REACHABLE (correlation is not necessity)
```

Артефакты (md5): base `947adfb5358984f76e21f5feb4208789`,
ablate-move `ce05d72bb60ef4e94c5bf1d50ba59349`,
ablate-look `26d5e6a11c0ec032d0d2d1a0a0052a10`; скрипт вне репо
(Rule 9).

**Смысл:** необходимость РЕАЛЬНА и измерима (абляция Move убивает
исход; абляция Look — нет), но текущий хребет НЕ МОЖЕТ её записать:
`cause` исхода-кражи указывает на `look_around` (хронологического
предшественника — каузально инертного для кражи!), а материально
необходимый `move` неотличим от любого другого события. Риск
review-C2 («tree-like reduction can erase conditions required for
the outcome») продемонстрирован вживую.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2556 passed + 1 skipped**
  (до/после идентично);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (ledger 10: iter-317 вошёл,
  iter-307 выселен; worklog 10: iter-307 выселен);
- `python scripts/topology.py --check` — clean;
- CONTRACTS.md 441 строк (кап 600), TASKS.md 599 (кап 600).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/CONTRACTS.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-317-caus1-report.md
git status --short
git commit -m "iter-317-caus1: the caus-1 contract landed (CONTRACTS §7 — the causal spine K1..K6 + the live ablation falsifier demonstrating review-C2's gap: the outcome's chronological cause vs the unrecorded necessity)"
git push
```

## G. Риски и следующее

- Риск: определение «необходимости» операционально (абляция), а не
  метафизично — это сознательный выбор: фальсифицируемость вместо
  онтологии (D0/D11 формы пакета); батарея детерминирована same-seed.
- Риск: декларация supports — будущая нагрузка на продюсеров; запись
  K5 фиксирует зерно вывода (`_last_change`), так что строка
  имплементации не начнёт с нуля.
- Следующее — **replay-1** (identity-кортеж replay + durability,
  review-C4/C7/C13/D4): `log_prefix_digest + engine_semantic_version
  + schema_identity + pack_semantic_digest + execution_config_digest
  + seed`; пробелы живого курсора названы триажем (pack-имя без
  контентного дайджеста, без execution-config дайджеста, движок неявен
  через commit заголовка); `flush == durable` явно отвергнуть.
