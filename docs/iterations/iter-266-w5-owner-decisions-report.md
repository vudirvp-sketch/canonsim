# Отчёт итерации iter-266 — W5-решения владельца: развилки закрыты по disposition

> Владельческий call 2026-09-27 (чат, поверх аудита станции W5):
> «Здесь я бы принял решения сейчас». Ноль кода, ноль пак-данных,
> ноль канона — итерация приземляет сами решения в доки-владельцы и
> чинит ориентацию world track: её W5-строка больше не читается как
> один недифференцированный «finish owner decisions».

## A. Главный ответ (коротко)

Все четыре стоящие W5-развилки получили явный disposition. Выбор — не
«открыть всё» и не «оставить всё»:

```text
FAIL-THEN-PASS   → CLOSE AS RESIDUE
40/80            → CLOSE AS RESIDUE
RUNNER GRUDGE    → ADD DISCOVERY SURFACE
SHAVE TIMING     → ADD TEMPORAL SURFACE
```

Два residue — осознанные нерешённые discovery-остатки (deliberate,
не техдолг); две поверхности — будущие строки в зафиксированной
владельцем последовательности (см. §D).

## B. Решения и их обоснования

| Развилка | Решение | Почему |
|---|---|---|
| fail-then-pass | RESIDUE | Attempt 1 → fail, attempt 2 → pass может быть честной частью discovery path. Отдельная поверхность обязана была бы доказать, что читателю нужно знать о первом провале, чтобы правильно понять какое-то важное настоящее состояние. Такого доказательства на записи нет. |
| 40/80 | RESIDUE | Его 40 / её 80 — тонкая асимметрия kin-отношений. Специально выведенная на поверхность (табличка, глосса) она рискует стать авторской загадкой / puzzle clue, а не живым социальным механизмом. Остаётся канонически присутствующей, доступной downstream-потребителям, не форсируется в читательский путь. |
| runner grudge | DISCOVERY SURFACE | Есть actor-specific motive, живой человеческий конфликт и observed reader recognition: живой читатель (iter-208) сам заметил standing обиды, но причины и последствия не проходили через доступную поверхность. Канон содержит причинную дугу, а перенос standing → history → consequence на поверхности теряется — это настоящий кандидат DISCOVERY_PATH_GAP, не «читатель не заметил деталь». Поверхность минимальная причинная: standing → remembered incident → why the grudge exists. НЕ биография раннера. |
| shave timing | TEMPORAL SURFACE | Проблема не в красоте арки, а в потере временной позиции причинно важного события: без неё рвётся event → residue → later consequence — один из главных законов world track. Маршрут чтения должен уметь восстановить earlier season → hunger winter → event → present consequence. Разрешение: dated-memory поверхность / исторический маркер. |

Политика двух residue: **DO NOT DELETE, DO NOT EXPLAIN BY DEFAULT**.
Для 40/80: canonically present → available to downstream consumers →
not forced into reader path.

## C. Стандарт решения (закон вперёд)

Поверхность не открывается лишь потому, что два LLM-чтения и один
живой читатель не собрали связь. Решающими стали два разных
дополнительных признака:

- **runner**: живой читатель уже зацепился за standing — поверхность
  «почти» работает; маленькое добавление превращает unresolved
  residue в читаемую человеческую историю;
- **shave**: теряется временная позиция самой причинной цепи — потеря
  исторической структуры, а не эстетики.

Обратная сторона зафиксирована как ценность Canonsim: **мир может
быть причинно связным, не будучи полностью разгаданным**. Разные
знания порождают разные законные решения; не каждый существующий
causal relation обязан быть reader-visible.

## D. Fill-list: §6.3 закрыт, порядок работ зафиксирован

§6.3 **удалён из fill-list** — «прожитый возврат» уже исполнен
(iter-204..210: прогон зонда, рендер-фикс, ресубъективация,
человеческая полоса, конфаунд снят). В документации остаётся только:

```text
§6.3 original probe = COMPLETED (iter-204..210)
remaining material  = W5 residue dispositions (landed iter-266)
                     + the live band's return
```

Строка ANCHOR_REGION §6.3 синхронизирована — док-дрифт закрыт (строка
не обновлялась после iter-204).

Последовательность работ (владельческая):

```text
W5 OWNER DECISIONS          ← закрыты этой итерацией
    ↓
RUNNER DISCOVERY SURFACE    (минимальная причинная поверхность)
    ↓
SHAVE TEMPORAL MEMORY       (dated-memory поверхность)
    ↓
LIVE RETURN / HEARTBREAK RECHECK
    (живая полоса не отделяется от только что внесённых изменений)
    ↓
§6.4 FACTOR NEGOTIATION + SALE + GUILD ROLES + TAG TRANSFER
    (первый настоящий fill-ряд: negotiation + economic state +
     knowledge + role structure + ownership/tag + debt residue —
     один ordinary mechanism, несколько downstream histories)
    ↓
§6.1 PAPER DEBT / PUNT BUYOUT / DEBT INHERITANCE
    (усилить carrier: paper representation → holder → inherited
     obligation → later settlement; НЕ новый debt-примитив)
    ↓
§6.5 MOVE-RELEASE           (agency / state-space / pacing)
    ↓
§6.2 PRESENT / HATCH / NOTCH
    (последним: два риск-слоя — present-state persistence + verb
     gate; wattle = prose, у runtime action нет writer'а для
     location flags — наивысший шанс преждевременно удариться в
     substrate gap)
    ↓
W6
```

## E. Ориентация world track: P0 расщеплён

Прежняя строка ориентации читалась как один пункт — «Finish owner
decisions for open W5 discovery/arc items» — и агент мог воспринять
весь список как технический fill. Теперь P0 несёт три явных класса
disposition'ов:

```text
CLOSE AS RESIDUE       fail-then-pass, 40/80     (сделано, iter-266)
ADD DISCOVERY SURFACE  runner grudge             (будущая строка №1)
ADD TEMPORAL SURFACE   shave timing              (будущая строка №2)
```

Репо-сторона расщепления: WORLD_WORKPLAN §7 (запись решений),
WORLD_TESTS §9 (запись в W5-entry), STATUS Next step (порядок работ),
этот отчёт §B. В отчёт iter-265 §D.1 добавлена купирующая пометка
(развилки закрыты, §6.3 из fill-list удалён).

## F. Честные границы

- Это решения, не работа: поверхности runner/shave ещё не написаны —
  каждая входит своей итерацией по зову владельца (новые ряды входят
  только по его зову — закон очереди).
- D-строка в DECISIONS не заведена: файл стоит на капитции 30/30,
  коллапс — только по явному зову владельца (D-034/D-185). Решение
  живёт в своих док-владельцах (WORKPLAN §7 / WORLD_TESTS §9), как и
  все записи станции W5.
- Верификация итерации механическая (ноль кода — тесты не могли
  измениться), но полный прогон обязателен по закону итерации; см. §G.

## G. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2461 passed + 9 skipped
✓ ruff check . — clean
✓ python scripts/docguard.py — clean (worklog 10, ledger 10, DECISIONS 30)
✓ python scripts/topology.py --check — clean
✓ ноль изменений core/, render/, content/, tests/ — LOG нетронут
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

Изменённые пути (9): docs/worldbuild/WORLD_WORKPLAN.md,
docs/worldbuild/WORLD_TESTS.md, docs/worldbuild/ANCHOR_REGION.md,
docs/iterations/iter-266-w5-owner-decisions-report.md (новый),
docs/iterations/iter-265-render-conditional-report.md,
docs/blueprint/phases.md, docs/TASKS.md, STATUS.md, worklog.md.
