# iter-383 · batchrolls — СЕДЬМАЯ ГОЛОВА СТОЯЩЕГО ПРИКАЗА ЗАКРЫТА: БАТЧ-ДРОУ ЦЕЛОГО МНОЖЕСТВА (класс iter-362, нуль канон-байт) — beat_rolls 2.860 → 2.168 проф. с (×1.32), family_randint 939 052 → 0 в обходе, стена ×1.03 перемеченным A/B; НАХОДКА ИНСТРУМЕНТА: профильный остаток завышал цену стены ~×5

**Класс риска:** R3 core (rng + urgencies + factions + тесты).
**PCC-строка:** D-259 — 36/35, НАД КАПОЙ D-252 (форма прецедента
D-256: строка посажена под стоящей директивой, коллапс —
ЭКСКЛЮЗИВНЫЙ вызов владельца, D-034/D-185; docguard RED — честное
видимое состояние, строка счёта гварда — сама запись, уходит в
зелёный на коллапсе).

**Вызов владельца:** стоящая директива «продолжай работы, открывай
то что сейчас важнее всего сделать, логичнее и качественнее на
долгосрок. я разрешаю» (открыла головы 362/370/375/378/379/381/382)
+ «продолжай работу» (эта сессия); строка STATUS Next называла
дроу-остаток beat_rolls ПЕРВОЙ оставшейся строкой (2.79 проф. с —
сам обход family_randint, 939K вызовов; форма-кандидат:
слитный батч-дроу — следующий шаг фузии после iter-370).

## A. Измерение ПЕРЕД кодом (тот же протокол, что 364/375/378/379/381/382)

cProfile h32 (S=4, H=32, seed 7, сегментированные 10y, якорь
loc_s0_square, директоры off, скип on), первозданный HEAD (82ab6df,
после iter-382):

- непрофилированная стена **7.05 с** (25 859 событий — точно якорь
  iter-382; его же 6.99/7.20); md5 лога `07e924cb…` — якорь
  воспроизведён до байта;
- профильная стена 17.85 с; **`beat_rolls` 2.860 с (16.3%)** —
  `urgency_intents` cum 2.857 / 7 644 вызова; внутри него
  **`family_randint` cum 2.434 с / 939 052 вызовов** (87% члена —
  сам обход дроу: Python-вызов + _ensure + закон вложенности +
  вызов _draw_word на каждый вход каждого бита) + `answer`
  0.330 / 939K (фаст-путь гейтов) + `first_failing` 0.326 / 41K;
  `faction_intents` 0.003 с (семейство пусто на этом паке);
- члены вокруг: skip_probes 4.548 с (внутри first_d100_hit 2.18 —
  уже оптимален по iter-362), commit_validate 3.897 (плоский),
  rest 4.12;
- конверт: h3 10y 0.27 с; farstead 100y (loc_square) 2.58 с,
  md5 `4e4f4cf2…`;
- профильный протокол: labrunner `--profile-depths 10`,
  canon_check HELD (снят ДО правок).

## B. Развилка дизайна (D-198 §2.7 — синтез перед выбором)

Кандидаты:

- **(A) Батч-дроу на банке — `family_rolls(names, lo, hi)`**: один
  проход двери на весь обход, дроу инлайн. Убивает 939K внешних
  вызовов; банк остаётся единственной дверью энтропии (L5); закон
  вложенности — по имени, как у per-call формы.
- **(B) Ужимка per-call** (специализация d100, пропуск проверок):
  коэффициент, а не срез — цена вызова (сама стена) остаётся.
  Отклонена как полумера.
- **(C) Прямые вызовы _draw_word из обходов** (минуя банк):
  нарушение L5 — счётчики/мемо приватны банку. Отклонена законом.
- **(D) Вердикты вместо значений** (`family_d100_hits`): банк
  узнал бы о вероятностях — семантическое наслоение; экономии ноль
  (слово вычисляется либо way). Отклонена.
- **(E) Предвычисление на стретч вперёд**: невозможно —
  роллинг-множество читается свежо на каждом бите (события между
  битами меняют его). Отклонена по построению.
- **Синтез (A)** с ДВУМЯ проходами: дверь (регистрация +
  вложенность + диапазон, порядок проверок per-call формы, нуль
  дроу) и дроу (закон `_draw_word` инлайн — прецедент iter-370:
  `family_randint` сам инлайнил проверку `assure`; оракулы пинуют
  равенство, D-024 не нарушен). **Эмерджентное свойство, названное
  и проверенное: ЗАКОН АТОМАРНОЙ ДВЕРИ** — отказывающий батч не
  двинул НИ ОДНОГО счётчика (строже per-call последовательности,
  чей отказ посередине оставляет ранние имена нарисованными);
  отказ и там и там убивает прогон — чистое состояние делает закон
  тестируемым.

## C. Изменение (4 файла кода + 1 новый тест)

1. **`core/rng.py` — `RngBank.family_rolls(names, lo, hi)`** (рядом
   с `family_randint`): ДВА ПРОХОДА. Дверь: ленивая регистрация
   (`_ensure`), закон вложенности ПО ИМЕНИ (проверка
   `family_randint`'а, исполненная инлайн — чужое имя под
   substantive-скоупом отказывает; семейное имя под чужим семейным
   скоупом отказывает; свой имя под своим — проходит), диапазон
   (`hi < lo` — ValueError, сообщение per-call формы); всё в
   порядке per-call формы, НУЛЬ дроу до полного прохода. Дроу:
   локальные переменные банка подняты; на имя — позиция,
   block_index, мемо-гет (пересборка sha256-блока при смене),
   слайс слова, `int.from_bytes`, `% span`, запись счётчика,
   append. Один диапазон на батч (оба бит-вызывателя дроу d100;
   смешанных диапазонов потребитель нет — AGENTS §2.7).
2. **`core/urgencies.py` — `urgency_intents`**: collect-then-draw —
   роллинг-множество как было (RollIndex-бакет или фильтр), ОДИН
   `family_rolls` на бит, затем фильтр вероятности + гейты по
   входу (`zip(strict=True)` — длины равны по построению). Гейты
   ничего не дроу — перепорядочивание ЕСТЬ пер-входовой порядок,
   слитый.
3. **`core/factions.py` — `faction_intents`**: фильтр собирает
   спеки первым (фильтр и бар — чистые чтения замороженной
   проекции), ОДИН `family_rolls`, затем бар + гейты по входу.
   Пустой `rolling` — ранний возврат, ноль дроу (закон каданса
   цел: дроу только у роллящих).
4. **`scripts/labrunner.py`**: комментарий члена beat_rolls +
   **ЗАМЕТКА ИНСТРУМЕНТА** (см. E).

## D. Законы-оракулы (tests/test_batchrolls.py — 8, все зелёные)

1. **Закон равенства**: тот же слова, те же счётчики — crafted
   семейства (urgency/faction/drift/scene) + ПОВТОРЫ имён
   (последовательные позиции одного стрима — поведение
   per-входового обхода) + разные диапазоны + 9 раундов
   (блок-граница в 4 слова пересечена); отпечаток substantive не
   тронут.
2. **Пустой батч** = пустая последовательность (нуль движения).
3. **Закон вложенности + атомарная дверь**: чужое имя под
   assured-substantive отказывает, НОЛЬ двинутых счётчиков;
   семейное имя под чужим семейным скоупом отказывает, своё под
   своим проходит; семейное множество под substantive проходит
   свободно (форма прогона).
4. **Закон диапазона**: `hi < lo` отказывает весь батч до любого
   дроу; точечный диапазон рисует константу.
5. **Закон блок-прыжка**: skip_draws посреди последовательности
   (разные смещения на стрим, блок-границы внутри прыжков) —
   батч рисует ровно то, что per-call форма на прыгнутых позициях
   (мемо — производное состояние, чисто на любом прыжке: закон
   restore/branch/seek).
6. **Обход-двойник на ВСЕХ ШЕСТИ коммитнутых паках**: выходы
   `urgency_intents` (батч) == реконструированному per-call
   обходу (оракул в тесте), 5 раундов, + построчное равенство
   счётчиков каждого стрима.
7. **Фракционный двойник** (pressure — пак с фракциями): выходы и
   счётчики `faction_intents` == per-call референсу.
8. **Реальный лог — A/B байт-идентичность** (форма test_h9): та же
   сессия провинции (seed 7, move + 2 годовых wait) через per-call
   обходы (патч в биндинги лупа — форма зонда) и через батч-обходы
   — байты ИДЕНТИЧНЫ; пара невернакуумна (пак роллит).

## E. Измерения

| Метрика | До | После | Дельта |
|---|---|---|---|
| член `beat_rolls` (проф.) | 2.860 с / 16.3% | **2.168 с / 13.2%** | **×1.32** |
| `family_randint` в обходе | 2.434 с / 939 052 вызова | **0.000 с / 0** | честное отсутствие |
| `family_rolls` | — | 1.933 с / 7 644 вызова | сама энтропийная работа |
| профильная стена | 17.85 с | **16.76 с** | ×1.07 |
| стена h32 10y (перемеч. A/B) | мед **7.38 с** | мед **7.18 с** | **×1.03** |
| микробенчмарк чистой цены дроу | 0.740 с | **0.542 с** | ×1.36 (−0.20 с) |
| конверт h3 / farstead 100y | 0.27 / 2.58 с | 0.27 / 2.59 с | без регрессии |

**НАХОДКА ИНСТРУМЕНТА (второй датум строки)**: профильный остаток
ряда (2.79 с) завышал истинную цену стены ~×5 — cProfile берёт
налог на каждый из 939K вызовов; перемеченный A/B (один процесс,
дрейф-компенсированный, 4 раунда на руку) меряет истинный срез
0.2 с, и микробенчмарк чистой цены дроу объясняет его в точности.
Две серии по 5 прогонов БЕЗ перемешивания дали ПЛОСКУЮ картину
(7.14 против 7.15 мед) — дрейф машины глотает 0.2 с; перемеченная
форма — честный инструмент. Закон 8 лаба («профильная стена —
артефакт прибора: доли и отношения — датумы, никогда абсолют»)
теперь с измеренным зубом: **пер-вызовный остаток в профильной
таблице НИКОГДА не заявление о стене** — заметка посажена в
labrunner рядом с членом.

Остаточный рейтинг стены (после 383): skip_probes 27.0%
(first_d100_hit 2.1 с — оптимальный коллективный обход iter-362 +
цикл скана) > commit_validate 22.8% (популяционно-плоский —
никогда не стена) > **beat_rolls 13.2% — НА ЭНТРОПИЙНОМ ПОЛУ**
(sha256-блоки + слайсы слов + записи счётчиков — сама работа) >
фаст-путь подачи (уже срезан ×2.2). **Очередь производительности
стоящего приказа исчерпана**: каждый остаток на документированном
полу; новая строка — только по свежему непрофилированному
A/B-датуму.

## F. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` → **2670 passed + 28
  failed** (2663 + 8 новых законов − 1 строка гварда; 28 = 27
  известных T1 env-сет (множество продиффено имя-в-имя против
  первозданного базлайна ДО правок — ИДЕНТИЧНО, ноль новых) + 1
  строка гварда docguard 36/35 — честная запись состояния над
  капом, уходит в зелёный на коллапсе владельца);
- `ruff check .` → чист; `topology.py --check` → чист;
  `digest.py` → парсит; `docguard.py` → **RED 36/35 — честное
  состояние над капом** (форма прецедента D-256/iter-379: строка
  счёта гварда — видимая запись, уходит в зелёный на коллапсе
  владельца);
- **НУЛЬ КАНОН-БАЙТ**: md5 h32 10y `07e924cbe6a3f05e9991e083ed004610`
  / h3 `796afbe131a1057482eb1a5c82b8527a` / farstead 100y
  `4e4f4cf209d5a0a3bb83db7ef06bd155` — все идентичны до/после
  (ШЕСТЬ независимых сравнений, включая каждое промежуточное
  состояние кода; canon_check HELD — профильный ==
  непрофильный);
- INV-1..5 не тронуты (INV-2: те же стримы, те же позиции
  счётчиков, тот же порядок — отпечаток не тронут, чекпоинт не
  различает формы; законы равенства/блок-прыжка/A/B пинуют).

## G. Изменённые пути (10: 8 изменено + 2 создано)

core/rng.py; core/urgencies.py; core/factions.py;
scripts/labrunner.py; STATUS.md; worklog.md (iter-371 вытеснен);
docs/TASKS.md (леджер, iter-371 вытеснен); docs/DECISIONS.md
(D-259, 36/35); tests/test_batchrolls.py (новый, 8 законов);
docs/iterations/iter-383-batchrolls-report.md (новый).

Превышение soft-cap 3–5 файлов — класс iter-375/378/379/381/382
(код + законы + обязательные райдеры протокола); отмечено в
worklog.

## H. Риски

- **Инлайн закона `_draw_word`**: второй носитель формулы слова —
  дрейф-риск, закрытый оракулом (закон равенства + блок-прыжок
  пинуют к per-call форме; прецедент iter-370 — инлайн проверки
  `assure` той же формы).
- **Атомарность двери**: поведение при отказе ОТЛИЧАЕТСЯ от
  per-call последовательности (та оставляет частично продвинутые
  счётчики) — намеренно, строже, безопаснее; отказ убивает прогон
  в обеих формах, чистое состояние — тестируемый закон (#3).
- **Чужие вызывающие**: публичные сигнатуры обходов НЕ тронуты
  (фузия внутренняя); `family_randint` остаётся владельцем закона
  одиночного дроу (все прочие потребители — scene detail, name,
  weather — не тронуты).

## I. Дальше

**Первый вызов владельца — коллапс DECISIONS 36/35 → 35**
(кандидаты слияния: семейные строки стоящего приказа D-257/D-258/
D-259 в строку-семью D-253 — три головы одного класса под одной
директивой, форма iter-380). Затем — стоящие вызовы владельца по
порядку: промоушен рантайма (D-250, базис полон), станционный
хаускипинг (m6-v6.2-зип в docs/station/archive/), строки
playbook'а (replay-UI, W8, P1/P2/P3, lab-composite-1). Новая
строка производительности — только по свежему непрофилированному
A/B-датуму (находка инструмента этой итерации).

## J. Git-блок владельца

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/rng.py core/urgencies.py core/factions.py scripts/labrunner.py tests/test_batchrolls.py STATUS.md worklog.md docs/TASKS.md docs/DECISIONS.md docs/iterations/iter-383-batchrolls-report.md
git status --short
git commit -m "iter-383-batchrolls: THE STANDING ORDER'S SEVENTH HEAD LANDED - the whole-set family draw (D-259, R3, the iter-362 class, ZERO canon bytes; DECISIONS at 36/35 OVER the D-252 cap - the D-256 precedent form, the collapse the owner's next exclusive call) - RngBank.family_rolls (core/rng.py, beside family_randint): TWO PASSES - the DOOR (lazy registration + the nesting law per name + the range, the per-call form's own check order, ZERO draws) then the DRAWS (_draw_word's law executed INLINE - the call overhead was the measured body; the iter-370 precedent, the oracle laws the pin, never a second source of truth) + THE ATOMIC-DOOR LAW (a refusing batch advances NOTHING - strictly safer than the per-call sequence whose mid-sequence refusal leaves the earlier names drawn) + one range per batch (both beat callers draw d100; a mixed-range batch has no consumer) + both walks collect-then-draw (urgency_intents: the rolling set unchanged, ONE batch draw, then the probability filter and the gates per entry; faction_intents: the filter collects first - the bar and the gates read the frozen projection, the reordering IS the per-entry order fused; zip strict=True) + 8 oracle laws (tests/test_batchrolls.py: the equality law over crafted families + repeats + block-crossing rounds; the empty batch; the nesting/atomic-door battery; the range law; the block-jump law; the walk twin on ALL SIX committed packs; the faction twin; the real-log A/B byte-identity - the same province session through the per-call walks and the batch walks commits IDENTICAL bytes); MEASURED: the member beat_rolls 2.860 -> 2.168 profiled s (x1.32, share 16.3->13.2%), family_randint 939,052 calls -> 0 in the walk (family_rolls 7,644 calls cum 1.933 s - the entropy work itself), the profiled wall 17.85 -> 16.76 s, THE WALL (the interleaved drift-cancelled A/B, 4 rounds per arm): old med 7.38 / new med 7.18 s (x1.03), the pure-draw micro-benchmark 0.740 -> 0.542 s explaining the cut exactly; THE INSTRUMENT FINDING: the row's profiled residue overstated its wall price ~5x - cProfile's per-call tax over 939K calls; a per-call residue in a profiled table is NEVER a wall claim (lab law 8 now with a measured bite, the labrunner note); the envelope h3 flat / farstead 100y 2.59 s; ZERO canon bytes: h32 07e924cb../h3 796afbe1../farstead 4e4f4cf2.. identical across SIX independent comparisons (canon_check HELD); 2670 passed + 28 failed (28 = 27 the known T1 env set diffed IDENTICAL to the pristine baseline - zero new + 1 the guard's own DECISIONS 36/35 count line, the D-256 precedent state clearing on the owner's collapse call; the +8 laws all green), ruff+topology+digest clean, docguard RED at 36/35 - the honest over-cap state (the D-256 precedent, clears on the owner's collapse call); THE STANDING ORDER'S PERFORMANCE QUEUE DRAINED - every residual at its documented floor (first_d100_hit optimal, commit_validate population-flat, beat_rolls at the entropy floor); a new performance row opens only on a fresh unprofiled A/B datum; INV-1..5 untouched"
git push
```
