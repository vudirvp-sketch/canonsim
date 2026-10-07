# iter-337 · h9 — ТИХИЙ БИТОВЫЙ СКИП ПОСАЖЕН: мир ждёт от события к событию на скипе времени — crossing-дисциплина прыгает через биты, которые ничего не производят; закон A/B побайтово на КАЖДОЙ измеренной форме, килогод = канон iter-335 побайтово, стена сегментированного килогода 102.54 → 46.44 с (2.21×, скипнуто 93.5% битов)

**Вызов владельца:** действующая директива «продолжай работы, открывай
то что сейчас важнее всего сделать, логичнее и качественнее на
долгосрок» — строка STATUS Next п.(1), названная первой в NEXT-линиях
iter-334/335/336: «H9 — event-to-event waiting на скипе времени,
структурно разблокирована эпохой (O(1)-прыжок счётчика)».
BASE_COMMIT: `836a743` (iter-336, чистое дерево — база 2606+1 green).
Задача ID: `iter-337-h9`. **R3** (кросс-граничное: rng + states +
urgencies/factions/groups + loop; PCC-запись §G этого отчёта —
DECISIONS на капе 30/30, прецедент iter-332).

**llama.cpp не устанавливался** — строка LLM-free: детерминированный
движок, чистая инженерия счётчиков эпохи.

## A. Что сделано

### A.1 Закон скипа (механизм)

Бит ТИХ ⟺ его машина ничего не производит: нет драфта распада, нет
конденсации, ни один качающийся urgency/faction-розыгрыш не попадает
с открытым гейтом, нет релиза директора. Тихий бит потребляет РОВНО
+1 розыгрыш на каждый качающийся поток (исход не меняет счёта —
закон семейства) и не пишет ни байта. Значит:

1. **Счётчики прыгают арифметически** — `RngBank.skip_draws(name, m)`:
   m скипнутых битов × качающееся множество; бит-лейдинг читает ту же
   позицию, что прочитал бы тик-за-тиком путь.
2. **Часы прыгают на лендинг** — первый производящий бит (или граница
   стретча: rotation/calendar/macro-crossing — они ВСЕ коммитят,
   скип никогда не переходит их; тик входа — граница очереди).
3. **Лендинг считает по замороженному состоянию** — между двумя
   материализованными моментами проекция/фолды/мир неподвижны,
   вердикты гейтов не меняются, ОДНА оценка на весь стретч.

Три чистых двойника кормят лендинг (всё — рядом с механизмами,
которым они двойники, никогда вторая истина):

| двойник | владелец | закон |
|---|---|---|
| `next_decay_tick` | core/states.py | формула первого тика драфта: `last + ceil(360/rate)`; интервальная пропорциональность ⇒ скип бита не меняет значения (следующий дельта покрывает весь промежуток); пиннинг на границе клэмпа ⇒ ось молчит всегда (монотонность) |
| `condensation_pending` | core/groups.py | предикат пустоты драфтов БЕЗ розыгрышей (сами драфты жгут name-потоки — вызывать их для проверки пустоты нельзя) |
| `urgency_scan` / `faction_scan` | core/urgencies.py / factions.py | качающееся множество (ОБЩИЙ предикат `urgency_rolls`/`faction_rolls` — один закон, два потребителя) + один `first_failing` на стретч + `next_d100_hit` |

`RngBank.next_d100_hit(name, p, limit)` — скан первого попадания
d100 в потоке: тайт-луп по блокам эпохи (один sha256 на 4 позиции),
чистый, без продвижения счётчика — структурный дивиденд rng-1
(до эпохи каждый скипнутый бит стоил бы O(k) реплея).

### A.2 Фенсисы способности (гварды, init-once)

Пак, не прошедший любой фенс, держит ТОЧНЫЙ тик-за-тиковый путь —
нулевая поверхность расхождения по построению:

1. **Запрошенная рука** — `skip_quiet_beats` (конструктор, дефолт
   ON): офф-выключатель фальсификатора, никогда выбор семантики.
2. **Директор тих** — выключен ИЛИ пак не объявляет хуков релиза:
   `releases()` тогда отвечает [] навсегда, пейсинг-часы инертны.
   Хуковый мир под включённым директором — старый путь (пейсинг
   читает счётчик битов — именованный остаток, никогда не
   аппроксимируется молча).
3. **Fold-demand пуст** — ни один гейт не читает времязависимые
   фолды (leverage/echo/trait): вердикты заморожены между событиями
   ПО ПОСТРОЕНИЮ. Гейтовый мир (карта истекающего рычага,
   рас-кристаллизующееся убеждение) — старый путь; моделирование
   брейкпоинтов фолдов — будущая строка.

Живое множество: семейство лабораторных фикстур — **farstead в обеих
руках директора** (хуков нет); **pressure ОТКАЗАН** (echo-гейт
институциональных глаголов), **tavern ОТКАЗАН** (фолд-гейты) —
коммитнутый корпус истории-паков едет по старому пути, их
байтовые пины тривиально целы.

### A.3 Закон A/B — фальсификатор строки

`tests/test_h9.py`, закон 1: тот же (пак, сид, список шагов) со
скипом ON и OFF → **логи побайтово идентичны**, и статистика ON-руки
НЕВАКУУМНА (скип реально скипал; зелёная пара с нулём скипов не
доказывает ничего). Обе руки протокола — whole (мир отложенной
реализации) и segmented (живой мир): разные формы стретчей, один
закон.

## B. Измерено

| форма | ON | OFF | закон |
|---|---|---|---|
| 10y segmented ×3 сида | — | — | **IDENTICAL** ×3 (md5 пары) |
| 10y whole ×3 сида | — | — | **IDENTICAL** ×3 |
| 100y segmented seed 7 | 4.78 с | 10.34 с | **IDENTICAL**, md5 `ee8459fa…` = канон iter-335 |
| **1000y segmented seed 7** | **46.44 с** | 102.54 с (iter-335) | **IDENTICAL, md5 `a1d8f05b…` = КАНОН iter-335; T1 HELD 76,951,399 × 2** |
| 50y whole seed 7 | 13.61 с | 16.27 с | **IDENTICAL** (1.20× — occ-остаток = строка B7) |
| 2606-й корпус (дефолт ON) | — | — | **2616+1 green** (10 новых законов; ни один не удалён/ослаблен) |

- **Килогод**: скип съел **1,009,806 из 1,080,000 битов (93.5%)** за
  60,039 стретчей, 59,091 лендинг; события 130,327 — каноническое
  число; глагольная линейность (sourced 3,996 / converted 1,000 /
  settled 8,013) и жизнь 74,322 в 1000/1001 спанов — числа iter-335.
- **Стена**: сегментированный килогод **2.21×**; 100y **2.16×**; 10y
  **2.15×**; 10,000y теперь ≈ 8 мин одним сидом (было ≈ 17) —
  глубокие горизонты открываются.
- **Whole-рука 1.20×** — по анализу iter-335/336 её стена занята
  occ-рефолдом (68.8→81.7% на глубине); скип срезает битовую часть,
  occ-остаток — отдельная строка за гейтом (буква B7).
- **2616 passed + 1 skipped**, ruff clean, docguard clean,
  topology --check clean (Python 3.12.14, env pin).

## C. Файлы

core/rng.py (next_d100_hit + skip_draws), core/states.py
(next_decay_tick), core/urgencies.py + core/factions.py (общие
предикаты rolls + сканы + faction_bar), core/groups.py
(condensation_pending), core/loop.py (скип: _skip_quiet_beats +
грид-арифметика + фенсисы + статистика + вставка в crossing-loop),
scripts/labrunner.py (--skip on|off, том _noskip, cost.skip),
tests/test_lab.py (механический re-pin под 3-tuple), tests/test_h9.py
(новый, 10 законов), docs/TASKS.md (строка h9-1 + леджер, iter-327
evicted), STATUS.md, worklog.md (iter-326/327 evicted), этот отчёт —
13 changed/created (6 код + 1 инструмент + 2 тест + 4 райдера).
NO test deleted or weakened — 10 добавлено, 1 механический re-pin
(распаковка возвращаемого кортежа).

## D. Чего НЕ сделано (намеренно)

- **Фолдовое расширение** (скип на гейтовых мирах: leverage/echo/
  trait-брейкпоинты) — именованный остаток, будущая строка за
  вызовом владельца; гвард держит эти миры на старом пути.
- **Директорское расширение** (пейсинг-часы на скип-пути) — второй
  именованный остаток; та же ограда.
- **Фикс occ-окна whole-руки** (B7) — своя строка; здесь только
  измерение 1.20×.
- **Станционный кросс-чек скипа** — станция едет по вызову владельца;
  скип побайтово прозрачен, кросс-железный закон (iter-336) переносит
  идентичность автоматически (контент не меняется — меняется только
  время его вычисления).

## E. NEXT

1. **Фикс occ-окна whole-протокола** (индексная атрибуция дренажа,
   буква B7) — первая строка STATUS Next, по вызову владельца.
2. Стоящие вызовы в порядке: Lab E02/E31, M2, replay-UI, W8,
   фронтовые P1/P2/P3.
3. Фолдовое/директорское расширение скипа — при появлении
   потребителя (гейтовый мир глубоких горизонтов).

## F. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/rng.py core/states.py core/urgencies.py core/factions.py core/groups.py core/loop.py scripts/labrunner.py tests/test_lab.py tests/test_h9.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-337-h9-report.md
git status --short
git commit -m "iter-337-h9: THE QUIET-BEAT SKIP — the world waits event-to-event on the time-skip (H9): the crossing discipline jumps the clock/counters/director-beat across beats that would produce nothing (the decay/condensation/scan pure twins + the epoch's O(1) next_d100_hit); THE A/B BYTE-IDENTITY LAW held on every measured shape — the kiloyear md5 = the iter-335 canon, T1 HELD 77MB x2; the segmented wall 102.54->46.44s (2.21x, 93.5% of beats skipped), the whole arm 1.20x (the occ residue stays B7's row); the fences: skip arm / quiet director / empty fold demand (pressure, tavern keep the old path); +10 laws + the labrunner --skip arm"
git push
```

## G. PCC (R3 — the compact record, AGENTS §2.9)

- **intent**: collect the epoch's structural dividend — the H9
  event-to-event waiting: jump the quiet beats whose machinery
  produces nothing, keeping the canon byte-identical (an
  acceleration, never a semantics choice); unblock the deep-horizon
  worlds (10,000y ≈ 8 min single-seed now).
- **invariants**: INV-1 (a skipped beat commits nothing — the log
  never sees the skip; every landed beat runs the REAL machinery
  through the one canon door); INV-2 (the skip advances the SAME
  named-stream counters the tick-by-tick path draws — `skip_draws`
  is arithmetic over the epoch's counter positions, no new stream,
  no wall-clock, the queue key untouched); INV-3 (zero domain words —
  the INV-3 stoplist caught one «guard» in a docstring, fixed);
  INV-4 (untouched — no network surface); INV-5 (old logs never
  edited; the skip writes only new events identical to the old
  path's).
- **delta**: core/rng.py (+next_d100_hit, +skip_draws), core/states.py
  (+next_decay_tick), core/urgencies.py (+urgency_rolls,
  +urgency_scan; the walk's filter extracted), core/factions.py
  (+faction_rolls, +faction_bar, +faction_scan; the same
  extraction), core/groups.py (+condensation_pending), core/loop.py
  (the skip + the fences + the stats + the skip_quiet_beats arm),
  scripts/labrunner.py (the --skip arm, cost.skip), tests/test_h9.py
  (+10 laws), tests/test_lab.py (mechanical 3-tuple re-pin).
- **verification**: the A/B byte-identity law (ON vs OFF, stats
  non-vacuous) on 3 seeds × 2 protocols at 10y, 100y, whole 50y, and
  the kiloyear (md5 = the iter-335 canonical log; T1 HELD
  76,951,399 × 2); the counter-identity law (every stream's count
  equal at the run's end); the fence laws (pressure/tavern refused,
  the farstead hook-twin refused under an enabled director); the
  decay-formula and scan-vs-walk property laws; the grid-arithmetic
  law; the full corpus 2616+1 green, ruff/docguard/topology clean.
- **provenance**: the STATUS Next item (1) — the row named first by
  iter-334/335/336's NEXT lines; the owner's standing «продолжай
  работы, открывай важнейшее на долгосрок» directive; the H9
  definition reconstructed from the three in-repo references (the
  external Lab pack's H-family not committed).
- **runtime**: the skip is ON by default (the corpus rides it — the
  farstead/pressure fixtures stay byte-pinned); the fences keep every
  director-armed or fold-gated pack on the exact old path; resume is
  skip-transparent (the cursor carries the counters, which the skip
  advances identically; no new persisted state).
