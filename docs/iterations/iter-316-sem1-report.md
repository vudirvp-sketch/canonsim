# iter-316 · sem1 — контракт семантической валидности и авторитета событий (голова подтверждённой очереди, review-C1/D1)

**Вызов владельца (2026-10-03, дословно):** «продолжай работу прошлой
итерации, sem1 открывай и так далее» — продолжение
подтверждённой на iter-315 очереди контрактов; разрешение на
llama.cpp/окружение получено, но строка R0/R1 (определение) —
llama.cpp не нужен, право остаётся зарезервированным для живых
inference-рядов (прецедент iter-315 §C).

## A. Что сделано

- **Контракт sem-1 ПРИЗЕМЛЁН** в `docs/CONTRACTS.md` §6 — форма файла
  (пинированные решения + инварианты + фальсификатор + минимальный
  тест-сет), семь решений, каждое привязано к живому коду или закону:
  - **S1 один семантический владелец** — резолверный контур
    (`core/intent.py` + `core/resolvers.py` + механики loop) остаётся
    единственным, кто решает, что событие ЗНАЧИТ; гейт никогда не
    пере-выводит смысл, не перезапускает прекондишены/чеки, не
    правит драфт.
  - **S2 декларированная поверхность эффектов** — на тип события:
    легальные классы акторов + семейство state-change (или NONE для
    knowledge-only/no-op типов) + каналы knowledge + словарь hooks +
    постусловия (чистые предикаты над projection+draft+pack).
    Декларация живёт в pack-данных (`events`-ветви, `status_effects`/
    `balance`/`ignition`, закрытый словарь `Pack.event_types()`) +
    именованных константах механик (`STATE_MUTATING`,
    `REJECTION_EVENT`, глаголы экономики, типы clock-семейства с
    актором `world`) — НИКОГДА per-draft, никогда не выводится из
    вывода продюсера в рантайме (статический двойник — packlint
    admission, D-152).
  - **S3 словарь авторитета (emit-side)** — классы акторов, которые
    продюсеры уже подразумевают (player/npc/`world`/group-ids);
    `year_turns` → только `world` (собственная декларация
    `core/macro.py`); входная сторона конвейера — территория auth-1
    (D9), забор закреплён.
  - **S4 гейт** — чистый, non-resolving:
    `admit(draft, declaration, projection) → ADMIT | REJECT`; место —
    ВНУТРИ `_commit`, после дельта-гейта, до `writer.append`: одна
    дверь, ещё одна проверка (продление формы D-035, не вторая дверь).
  - **S5 две полосы RED** — внутреннее нарушение продюсера падает
    ГРОМКО до записи (форма дельта-гейта, KI#13); внешний кандидат
    (медиатор/движок) отказывается МЯГКО — кандидат умирает у двери,
    логируется факт-попытка по словарю медиатора.
  - **S6 запрет тавтологии** — референс гейта это ДЕКЛАРАЦИЯ,
    независимая от экземпляра драфта; «валиден, потому что резолвер
    его произвёл» запрещено; фальсификатор — исполняемое опровержение.
  - **S7 проба `_commit` — контрактный разрыв, не production-эксплойт** —
    переподтверждена фальсификатором; ни один production-путь не
    скармливает рукодельные драфты приватной двери.
- **Дешёвый фальсификатор ПРОГОНЁН ВЖИВУЮ** (скрипт вне репо, Rule 9;
  seed 42, plumbing_smoke): обе руки СЕГОДНЯ ПРОХОДЯТ — разрыв
  продемонстрирован (см. §D).
- **Минимальный тест-сет будущей строки имплементации закреплён**:
  две руки RED→GREEN без аппенда; позитивный контроль — весь корпус
  плейскриптов admitting 100%, golden T1-фикстуры байт-в-байт;
  тавтология-гард (флип ДЕКЛАРАЦИИ, не драфта, переворачивает
  вердикт); две полосы; INV-2 replay.
- **Кап-проход §5 CONTRACTS.md** (576→338 строк): приземлённые
  wb-заметки свёрнуты в указатели по собственному закону файла +
  D-024 (дословные заметки — в git); протухший роутинг
  `REDOT_ENGINE_INDEX` починен на форму D-245.

## B. Что НЕ сделано (честно)

- **Ни строчки кода** — ни гейта, ни изменения схемы, ни нового поля
  драфта (закон строки: «Do NOT implement a semantic checker or
  change schemas in the definition task»). Имплементация — НЕ строка:
  владелец открывает её после приёмки контракта (гейт
  runtime-promotion: named consumer + measured native limit +
  фальсификатор).
- **DECISIONS.md не тронут** (кап 30/30, docguard) — sem-1 исполняет
  уже подтверждённую очередь (review-D1 принят на iter-315), нового
  решения нет; запись живёт в CONTRACTS §6 + TASKS + этом отчёте.
- **llama.cpp не устанавливался** — R0/R1 doc+probe строка;
  зарезервировано для живых рядов.

## C. Связь с соседними строками (заборы)

- review-C1 ≠ TASKS::core-1-C4 (граница LLM при необычном
  взаимодействии) — неймспейс-забор пакета, закреплён в §6.
- auth-1 владеет входным конвейером (интерпретация → классификация →
  авторизация); sem-1 — только emit-side проверка у канонической
  двери; словари не должны противоречить друг другу.
- speech-1 владеет типизированными речевыми актами; sem-1 не трогает
  каналную изоляцию.

## D. Фальсификатор — живой прогон (исполняемое доказательство разрыва)

Захват живых producer-outputs (обёртка над `EventLogWriter.append`),
мутация, подача через приватную `Simulator._commit`:

```
[capture] 11 events committed; 11 producer outputs captured
[capture] base producer output: type='wait' actor='pc_01' t=51 state_changes=()
[control] the unmutated log is clean: 11 events, all types within the pack vocabulary
[Arm A] schema-valid + delta-consistent `wait` carrying a position teleport
        loc_market->loc_tavern (non-adjacent): APPENDED as ev_0011 — NO declared-surface check fired
[Arm B] schema-valid `year_turns` (declared actor `world`) emitted by actor pc_01:
        APPENDED as ev_0012 — NO authority check fired
[result] the committed log now holds 13 events — the writer's schema/chain/tick gates passed both
[T2]    fold(polluted log): pc_01.position == 'loc_tavern' — the log absorbs unauthorized
        semantic effects SELF-CONSISTENTLY
```

Артефакт: `sem1_run_42.jsonl`, md5
`228ea08bff9b87afc9761d34bb704071`; скрипт пробы вне репо (Rule 9).
Смысл: событие, schema-валидное + дельта-консистентное +
chain-валидное, но неавторизованное/недекларированное, сегодня
ПОПАДАЕТ В ЛОГ и сворачивается без противоречий — в точности риск
review-C1 («Schema-valid log may encode an unauthorized semantic
effect»). Будущий гейт обязан дать RED на обеих руках без аппенда.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2556 passed + 1 skipped**
  (до и после идентично: ноль изменений кода);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (ledger 10 строк: iter-316 вошёл,
  iter-306 выселен; worklog 10 записей: iter-306 выселен; DECISIONS
  30/30 — не тронут);
- `python scripts/topology.py --check` — clean;
- CONTRACTS.md 338 строк (кап 600), TASKS.md 599 (кап 600).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/CONTRACTS.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-316-sem1-report.md
git status --short
git commit -m "iter-316-sem1: the sem-1 contract landed (CONTRACTS §6 — the seven pinned decisions + the live falsifier demonstrating the C1 gap; the §5 cap pass riding, the wb landing notes collapsed to pointers)"
git push
```

## G. Риски и следующее

- Риск: свёртка §5 удаляет из репо развёрнутые wb-landing-заметки —
  компенсировано: substance живёт в TASKS-строках wb-семейства + git;
  указатели сохраняют навигацию; работа свёртки записана в worklog.
- Риск: контракт объявляет, но не исполняет — это форма строки
  (definition-first), а не дыра: фальсификатор исполняем, тест-сет
  закреплён, строка имплементации откроется по вызову владельца.
- Следующее — **caus-1** (каузальная достаточность, review-C2/D2,
  естественная пара T1+T2): `primary_cause + necessary_supports[] +
  provenance` без причинного графа, поверх приземлённого примитива
  temp-1 (`provenance.assignment_tick`, D-236); абляционная проба
  «убери поддержку X → исход недостижим» как дешёвый фальсификатор.
