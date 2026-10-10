# iter-362 · skipprobe — АДРЕС ИЗ iter-347 ЗАКРЫТ: стена плотности ×3.37 (61.87 → 18.34 с на h32), ни один канон-байт не двинут (md5 07e924cb… ×2), ход «beat-outer» + O(1) индекс kind

**Повод:** директива владельца «продолжай работы, открывай то что
сейчас важнее всего сделать, логичнее и качественнее на долгосрок. я
разрешаю» — постоянная форма, открывшая h9-1/occ-1/density-1/2.
M2/M3-решения остаются за владельцем (материал доставлен iter-350 §G
+ iter-361 §G — это развилки продукта, не мои); стоящие вызовы
пересмотрены по критерию «важнейшее на долгосрок»: **адрес
оптимизации skip_probes, названный в iter-347** («спек-фильтр + O(E)
kind_of обходы внутри его поддерева — будущая строка "id→kind индекс
в pack.py" получает измеренное обоснование плотности») — единственная
ИЗМЕРЕННАЯ стена ядра: 75.0% профиля на глубоком конце density-лестницы
(H=32, ×211 абсолютного роста, КВАДРАТИЧНА в населении конуса).
Допуск строки — вызов владельца; явное «я разрешаю» его покрывает.

**BASE_COMMIT:** `ef65551b4a994147216092f4d14b56f2bc86fb0e`
(HEAD iter-361).

**Класс риска: R3** (кросс-модульное изменение ядра: pack + rng +
urgencies + factions + инструмент; PCC-запись — §G этого отчёта,
DECISIONS на капе 30/30, прецедент iter-332).

## A. Что было измерено до кода (профиль, тот же протокол, что в iter-347)

cProfile h32 (S=4, H=32, seed 7, сегментированные 10y, якорь
loc_s0_square, директоры off), первозданный HEAD:

- профильная стена **137.78 с**; `_skip_quiet_beats` cum **101.93 с**
  (74%); внутри него `urgency_scan` **95.89 с**;
- **`next_d100_hit` 73.30 с** — 933 261 вызов (≈122 роллинг-спека ×
  7 637 стретчей), **88.6M блочных слов, 22.17M sha256-дайджестов**:
  посерийная форма гуляла КАЖДЫЙ поток до его СОБСТВЕННОГО первого
  попадания — вся популяция проходила мимо коллективного лендинга
  (5 386 из 7 637 вызовов лендятся на бит 1: плотный конус никогда
  не тих);
- **`kind_of` 13.94 с** — 1.92M вызовов, каждый ЛИНЕЙНЫЙ обход всех
  записей (гейты `first_failing` → `_test_same_location` →
  `location_of` → `kind_of`); `first_failing` целиком 17.63 с.

## B. Изменение (7 файлов: 5 код + 2 тест)

1. **`core/pack.py` — id→kind / id→record индекс** («id→kind индекс»
   из адреса iter-347): `__post_init__` строит два словаря
   (first-wins в порядке категорий — точная семантика старого
   обхода, кросс-категорный дубль отвечает тем же); `kind_of`/
   `entity` становятся O(1). Производное состояние от `data`, не
   вторая истина; замороженный dataclass со slots — индексные поля
   `init=False, compare=False`.
2. **`core/rng.py` — `first_d100_hit(rolls, limit)`** (спек-фильтр из
   адреса iter-347, его коллективная посадка): beat-outer обход —
   на каждом сдвиге бита читается слово КАЖДОГО потока (то же слово,
   что посерийный обход прочитал бы на этой позиции — функция
   счётчика чиста в (key, position)), стоп на первом бите, где
   ХОТЯ БЫ один поток попадает; per-call блочный мемо; чистота
   сохранена (счётчики не двинуты, банк-мемо не тронут).
   **`next_d100_hit` удалён** (его единственные продакшн-потребители
   — два скана; блочная точность живёт в законе-оракуле).
   Контракт дубликатов: два входа на одном имени сворачиваются в
   МАКСИМАЛЬНУЮ вероятность — {j: word_j % 100 < p} растёт с p,
   значит первый хит максимума РАВЕН минимуму первых хитов входов
   (закон монотонности).
3. **`core/urgencies.py`** — `urgency_scan`: проход гейтов не тронут;
   вместо посерийных прогулок ОДИН коллективный вызов + max-свёртка
   на имя; ранний возврат p≥100 убран (частичная карта потоков была
   ненаблюдаема в вызывающем — при first=1 ни один бит не
   пропускается; теперь карта всегда полная, законы это крепят).
4. **`core/factions.py`** — `faction_scan`: тот же рестракт (max по
   бару на имя).
5. **`scripts/labrunner.py`** — синхронизация инструмента: запись
   `_KEY_FUNCS`/карты членов `next_d100_hit` → `first_d100_hit`.
6-7. **Законы** (см. §D).

## C. Стена: до/после, один инструмент, один протокол

Labrunner (НЕпрофилированная стена, seed 7, h32, сегментированные
10y, профильная рука `--profile-depths 10`, канон-нейтральность
HELD в обоих):

| | до (HEAD ef65551) | после (iter-362) | |
|---|---|---|---|
| стена | **61.87 с** | **18.34 с** | **×3.37** |
| доля skip_probes | 74.9% | 33.2% | член ×6.0 по cum |
| события | 25 859 | 25 859 | идентичны |
| md5 лога | `07e924cbe6a3f05e9991e083ed004610` | тот же | **байт-в-байт** |

Профильный механизм (cProfile, тот же протокол; инструмент-артефакт,
только доли): `_skip_quiet_beats` 101.93 → 17.10 с; `urgency_scan`
95.89 → 11.12 с; **обход 73.30 → 2.22 с (×33)**; `kind_of` 13.94 с →
вне топ-40 (O(1)); `first_failing` 17.63 → 3.85 с; всего вызовов
функций 297.1M → 123.7M. **skip_stats и occ_stats идентичны
посимвольно** (`{stretches: 2251, skipped: 3166, landings: 2248}`;
`{calls: 231, window: 99354, inspected: 752, attributed: 231}`) —
лендинг-паттерн скипа сохранён точно.

Разреженный конверт (farstead 100y сегментированные, seed 7 —
kiloyear-форма): 4.48 → 3.28 с (×1.37, **регрессии нет** — None-случай
обхода не дороже прежнего, индекс помогает дверям/гейту везде);
события 13 915 идентичны. Остаточные члены после (честные, будущие
строки): rest 21.5%, beat_rolls 16.2%, decay_walk 15.4%,
director_global_passes 10.2%, skip-остаток (гейты+роллс+next_decay_tick)
33.2%.

## D. Законы (+5; все 13 h9-законов зелёные)

- **`test_core.py` (индекс):** (1) `test_pack_kind_index_matches_
  the_linear_scan` — на ВСЕХ шести коммитнутых паках kind_of/entity
  отвечают в точности линейному обходу (референс пере-выведен в
  тесте) по каждому id + None на неизвестном; (2)
  `test_pack_kind_index_first_wins_on_cross_category_duplicate` —
  (линт-запрещённый) кросс-категорный дубль отвечает ПЕРВОЙ
  категорией.
- **`test_h9.py` (коллективный обход):** (3)
  `test_the_collective_first_hit_law` — `first_d100_hit` ==
  минимуму посерийных блочных обходов (оракул iter-337 пере-выведен в
  тесте), 4 семени × 5 лимитов × 2 семейства вероятностей
  (попадающее и промахивающееся — не-вакуальность оба знака),
  пред-продвинутые счётчики, чистота (счётчики на месте); (4)
  `test_the_collective_duplicate_fold_law` — свёртка max на одном
  имени теряет ничего против прогулки обоих входов; (5)
  `test_the_p100_full_streams_map_law` — карта потоков ВСЕГДА полная
  (все 14 роллинг-записей farstead), first=1 на p=100 старце.
- Существующие законы — главные фальсификаторы, не тронуты: A/B
  побайтовая идентичность (закон 1), T1-под-скипом, контр-тождество,
  **scan-vs-walk** (теперь на коллективном пути — стал СТРОЖЕ: карта
  полная значит все 14 потоков проверяются), grid-арифметика.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2622 passed + 27 failed
  + 1 skipped**: 27 = известная оговорка T1 (поле `python`
  log-header, 3.12.15 сэндбокс против 3.12.14 golden);
  **набор падений побайтово идентичен базовой линии первозданного
  кода, снятой в этой же сессии до изменения** — ноль новых;
- A/B побайтовая идентичность h32: md5 `07e924cb…` до и после
  (оба прогона на одном инструменте; хэш до снят ДО перезаписи
  лога);
- smoke эквивалентности 30/30 триалов (коллективный против
  посерийного референса, случайные семейства);
- `ruff check .` — clean (0.17.0); `python scripts/docguard.py` —
  clean; `python scripts/topology.py --check` — clean;
  `python scripts/digest.py` — парсит;
- INV-1..5 не тронуты (INV-2: обход читает те же чистые слова
  функции счётчика; индекс — чистая функция данных пака).

## G. PCC (R3 — компактная запись, AGENTS §2.9; DECISIONS на капе
30/30, прецедент iter-332 — строка не добавляется, запись живёт
здесь)

- **intent:** разрушить измеренную стену плотности (адрес iter-347)
  без движения единого канон-байта;
- **invariants:** INV-2 держится (обход читает те же чистые слова
  функции счётчика — она чиста в (key, position); индекс — чистая
  функция данных пака); INV-1/3/4/5 не тронуты (механика
  read-side-сканов + производное lookup-состояние, без изменений
  схемы/лога/очереди);
- **delta:** core/pack.py, core/rng.py (first_d100_hit добавлен,
  next_d100_hit удалён — два скана были его единственными
  продакшн-потребителями), core/urgencies.py, core/factions.py
  (коллективный обход + max-свёртка), scripts/labrunner.py
  (синхронизация _KEY_FUNCS), tests/test_core.py, tests/test_h9.py
  (+5 законов);
- **verification:** md5 h32-лога 07e924cbe6a3f05e9991e083ed004610
  ИДЕНТИЧЕН до/после (labrunner, seed 7, сегментированные 10y);
  skip_stats {2251, 3166, 2248} + occ_stats идентичны дословно;
  стена 61.87→18.34 с ×3.37; farstead 100y 4.48→3.28 с без
  регрессии; 2622 passed + 27 failed (известная оговорка T1
  log-header, набор падений идентичен базовой линии первозданного
  кода, снятой в этой же сессии) + 1 skipped; ruff/docguard/
  topology/digest clean; законы A/B побайтовой идентичности и
  scan-vs-walk зелёные (scan-vs-walk теперь СТРОЖЕ: проверяется
  полная карта потоков);
- **provenance:** lab_h32_before/after.json + farstead-пара (вне
  репо, Rule 9) + этот отчёт; записи воспроизводимы из семени;
- **runtime:** PYTHONHASHSEED=0, Python 3.12.15 (документированная
  оговорка окружения).

## H. Гит-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/pack.py core/rng.py core/urgencies.py core/factions.py scripts/labrunner.py tests/test_core.py tests/test_h9.py STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-362-skipprobe-report.md
git status --short
git commit -m "iter-362-skipprobe: THE MEASURED DENSITY WALL COLLAPSED - iter-347's named skip_probes address landed (the spec filter as the collective beat-outer first-hit walk + the O(1) id->kind/id->record index in pack.py): the h32 wall 61.87->18.34 s (x3.37, skip_probes 74.9->33.2%), the walk member x33 (73.30->2.22 s profiled), kind_of O(E) walks gone; ZERO canon bytes moved (the h32 log md5 07e924cb.. identical before/after, skip_stats/occ_stats identical verbatim, the farthest envelope farstead 100y 4.48->3.28 s no regression); +5 laws (the index-vs-linear-scan over all six packs + first-wins duplicate; the collective-vs-per-stream reference oracle + the max-fold monotonicity + the p100 full-map law); the scans' p>=100 early return dropped (unobservable in the caller, the streams map now always full); next_d100_hit removed (its two scans were the only production consumers; the block-walk exactness lives in the test-local reference oracle); labrunner _KEY_FUNCS synced; 2622 passed + 27 failed (the known T1 log-header env caveat, the failure set identical to the pristine baseline) + 1 skipped, ruff+docguard+topology+digest clean; R3 (the PCC record rides this report's section G - DECISIONS at cap 30/30, the iter-332 precedent)"
git push
```

## I. Доставка (§12.2 — оба канала)

- Дельта-архив (вложение): `canonsim_iter-362-skipprobe_
  2026-10-11.zip` против BASE_COMMIT `ef65551b4a994147216092f4d14b5
  6f2bc86fb0e` — 11 файлов (5 код + 2 теста + 4 райдера) +
  BASE_COMMIT.txt + DELETED_PATHS.txt (`None`); self-check: список
  путей == `git diff --name-only` против базы; **md5 + байты +
  tmpfiles-ссылка — в финальном сообщении** (само-ссылка: хэш архива
  не может лежать в отчёте, который архив содержит);
- labrunner-записи (`lab_h32_before/after.json`, farstead-пара) и
  pstats-дампы — вне репо (Rule 9), воспроизводимы из семени.

**Done:** адрес iter-347 закрыт целиком (обе половины); стена h32
×3.37 без движения канон-байта; +5 законов; полный батт-верификатор
зелёный (с известной оговоркой T1).
**Not done:** остаточные члены стены (rest/beat_rolls/decay_walk/
director_global_passes ≈ 63% профиля после) — каждое своя будущая
строка, допуск за владельцем; M2/M3-решения остаются за владельцем
(материал готов).
**Next:** стоящие вызовы владельца в порядке: M2/M3 за гейтом
runtime-promotion, replay-UI NOT-EXPOSED, W8, фронтенд P1/P2/P3,
lab-composite-1; из новых названных строк — обход гейтов скана
(`first_failing` 3.85 с остаток) и director_global_passes как
следующие кандидаты measured-wall семейства.
**Active KIs:** KI#113 (test_lab), KI#117 (закрыт iter-360;
удаляется по §5 на iter-363).
