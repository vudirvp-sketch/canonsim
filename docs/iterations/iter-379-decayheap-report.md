# iter-379 · decayheap — ЧЕТВЁРТАЯ ГОЛОВА СТОЯЩЕГО ПРИКАЗА ЗАКРЫТА: ИНДЕКС ПРИЗЕМЛЕНИЯ DECAY (класс iter-362, нуль канон-байт) — стена h32 10y 9.59 → 8.08 с (×1.19), член decay_walk 3.31 → 0.26 проф. с (×12.9), next_decay_tick ×50, ЭКСПОНЕНТА ПЛОТНОСТИ ×8.1 → ×1.85

**Вызов владельца (стоящая директива, дословно):** «продолжай
работы, открывай то что сейчас важнее всего сделать, логичнее и
качественнее на долгосрок. я разрешаю.» — строка STATUS Next называла
четвёртую голову в точности: «the decay landing index FIRST (the
heap form — the (npc,axis)→next-fire walk replacement in
next_decay_tick/decay_drafts, its staleness/veto laws; the decay_walk
member 3.28 profiled s / 12.3%, the density exponent ×8.1 the
strongest residual)».

**BASE_COMMIT:** `26b5fa06bf300c64c758f3e65d080bbca7782149`
(HEAD iter-378, снят до любой правки; вся базовая стена и профиль
этой же сессии).

**Класс риска: R3** (ядро: два модуля поведения + инструмент +
тесты; нулевые канон-байты по закону md5; PCC-строка D-256 — 36/35,
НАД КАПОЙ D-252: второй over-cap прецедент после D-250, оба под
стоящей директивой, называвшей строку; коллапс — исключительный
следующий вызов владельца, D-034/D-185/D-252; строка docguard +
красный guard-тест — честное видимое состояние до его выстрела).

## A. Измерение ПЕРЕД кодом (тот же протокол, что iter-364/375/378)

cProfile h32 (S=4, H=32, seed 7, сегментированные 10y, якорь
loc_s0_square, директоры off, скип on), первозданный HEAD:

- непрофилированная стена **9.59 с** (25 859 событий; записи
  iter-378: 9.57/9.49 — джиттер машины, форма та же);
- профильная стена 26.84 с; **`decay_walk` 3.308 с (12.5%)** —
  `decay_drafts` 7 644 вызова, 224.7 мкс/вызов: обход 165 NPC ×
  таблицу осей НА КАЖДОМ БИТЕ при ~0.84 выстрела на бит (6 386
  status_decayed / 7 634 бита — плотностный пак сам записывает:
  «at the LOD's year cadence it pins at the ceiling between rare
  serves — THE PIN ITSELF THE DATUM»);
- **`next_decay_tick` 2.676 с** внутри skip_probes (9.399 с) — тот
  же обход на каждом стретче скипа (7 637 вызовов);
- **экспонента плотности decay ×8.1** (per-call h3→h32) —
  сильнейший остаток переранжировки iter-378;
- profiled-протокол: labrunner `--profile-depths 10`,
  canon_check HELD (снят ДО правок).

## B. Развилка дизайна (D-198 §2.7 — синтез перед выбором)

Кандидаты, каждый по осям преимуществ/недостатков:

- **(A) Одна глобальная куча + pop-aside по скоупу**: минус,
  внутренний механизму — скоуп НЕ входит в порядок кучи; для
  тёплого вызова все активные ячейки с меньшим next_fire стоят
  перед первой тёплой — худший случай O(n) на вызов, экспонента
  выживает. Артефакт формулировки? Нет — три скоупа (None /
  активная / тёплое кольцо) суть три предиката, один порядок их
  не обслуживает. Отклонён.
- **(C) Словарь живых пар без кучи**: мин на вызове = O(живых) —
  на ЭТОМ инструменте хорошо (пин — большинство), но не
  масштабируется по плотности: цель строки — убить ×8.1, а не
  срезать константу. Отклонён.
- **(B) Кучи ПО ЛОКАЦИЯМ**: скоуп = членство в куче (peek кучи
  активной локации; min по |warm| кучам — выходы одной локации,
  горстка; None — все кучи, ≤7 на паках). Недостаток — ячейки
  переезжают при смене позиции — нейтрализуется фолдом на пути
  коммита (событие позиции перекладывает все пары сущности).
- **Синтез (B)** удовлетворяет объединению преимуществ (O(log)
  мин при всех трёх формах скоупа + масштабируемость по
  плотности), не нарушая ни одного условия избегания
  недостатков. **Эмерджентное свойство, названное и
  проверенное: закон устаревания ЛИЦЕНЗИРОВАН INV-1** — всякая
  причина устаревания ячейки (база/значение/пин/позиция/caught)
  ездит закоммиченным событием, и `_commit` складывает КАЖДОЕ
  state_change ⇒ отброшенная устаревшая ячейка ВСЕГДА имеет
  свежего наследника в пуле или пара легитимно мертва (пин /
  отсутствие значения / caught — собственные вето обходов). Это
  не украшение: без INV-1 ленивое устаревание небезопасно, с
  INV-1 оно — теорема. Свойство переживает родителя по всем
  материальным осям и устраняет материальный недостаток (A).
  Средневзвешенный компромисс — нет; перелицованный родитель —
  нет.

## C. Изменение (4 файла кода/инструмент + 1 новый тест)

1. **`core/states.py` — `DecayIndex`**: min-кучи ПО ЛОКАЦИЯМ из
   ячеек `(next_fire, npc, prop)` над ЖИВЫМИ парами (значение
   int-не-bool, не запинено на клампе в направлении оси, не
   caught, сущность в проекции). Рождение `from_projection`
   (KI#16: целая initial-проекция пака, базы из `last_change`
   вызывающего — при construction пуст, база 0, дефолт самого
   обхода) + штамп идентичности (рождение и штамп одной
   операцией — этот индекс никогда не складывает реплей: резюм
   перевыпускает пул из восстановленного состояния).
2. **Фолд на пути коммита** (`_commit`, после строки
   `last_change`): событие НА ОСИ перекладывает свою пару;
   событие на `position`/`crime_status` — все пары сущности
   (база и значение ездят одним событием — одно перекладывание
   покрывает оба). База читается из связанного `last_change`
   (D-024: один владелец, никогда частная копия).
3. **Валидация НА ВИДУ** (peek/enumeration): ячейка проходит
   СОБСТВЕННЫЕ фильтры обхода против живого связанного состояния
   — сущность в проекции, позиция == ключ кучи (переезд = смерть
   в старой куче), не caught, значение int-не-bool, не запинено,
   свежесть `next_fire == base + elapsed_first` для ТЕКУЩЕЙ базы.
   Невалидные выбрасываются на виду — пул кандидатный, никогда
   истина.
4. **Перечисление НЕ ПОТРЕБЛЯЕТ**: `firing` re-push'ит каждую
   валидную ячейку — вызывающий, бросивший драфты без коммита,
   оставляет пул как был (индекс никогда не предполагает
   дисциплину коммита вызывающего).
5. **Гейт идентичности** (форма ScanGateMemo/SensesIndex):
   `serves` истинен только для штампованных объектов + таблицы
   рождения (свежая резолюция и None НЕ обслуживаются — обход).
   Обходы остаются СЕМАНТИЧЕСКИМИ ВЛАДЕЛЬЦАМИ (D-024): формула
   извлечена в `_axis_change`, обе ветки зовут ровно её;
   clamp `max(…, from_tick)` остаётся собственностью
   `next_decay_tick` (peek отвечает сырой `min(base +
   elapsed_first)`).
6. **`core/loop.py`**: рождение при construction + перевыпуск из
   восстановленной проекции + сложённого `last_change` при resume
   (перестраиваем — в `export_run_state` НЕ входит, закон
   буфера); проводка во все три места вызова (проба скипа, бит,
   макро-дрейф тёплого кольца).

## D. Законы (+8; tests/test_decayidx.py — все зелёные)

1. `test_birth_pool_equals_the_walks_live_set_on_every_committed_pack`
   — пул рождения == множеству живых пар обходов на всех шести
   паках (порядок ответа — порядок декларации NPC пака, INV-2).
2. `test_birth_pool_counts_seeded_values_not_zero` — зубы закона
   рождения: непиненная посевная ось читается через пул, пины
   верха/низа молчат, приземление = base 0 + elapsed_first.
3. `test_the_fold_twin_agrees_after_every_staleness_edge` —
   ГЛАВНЫЙ закон: 17-шаговый краевой сценарий (рождение из None,
   пин верха, распин, bool, str, очистка до None, рождение заново,
   пин низа fear, хоп куч по позиции, caught-вето,
   освобождение, ДВА однотиковых изменения одного пропа —
   совпадение дубликатных ячеек), после КАЖДОГО шага — полный
   свип двойника (оба обхода × 12probe-тиков × 5 скоупов,
   порядок драфтов включён).
4. `test_caught_is_the_total_veto_on_every_axis` — caught:
   приземление None, перечисление пусто, двойник держит.
5. `test_the_enumeration_never_consumes` — драфты взяты и
   брошены без коммита: то же перечисление, то же приземление,
   двойник жив.
6. `test_the_identity_gate_foreign_projection_keeps_the_walk` —
   чужая проекция держит ОБХОД (наблюдаемо через драфты:
   связанный пул пуст — пин, чужая копия живая; с индексом на
   руках драфт есть ⇒ отвечал обход); свежая таблица и None не
   обслуживаются.
7. `test_the_real_log_twin_law` — реальный лог (кража → каскад →
   биты → ротация): двойник mid-run и на дренировании + живой
   пул == СВЕЖЕМУ РОЖДЕНИЮ на той же проекции/`last_change`
   (фолд == скан — сильнейшее производственное равенство).
8. `test_the_resume_law` — резюм: пул перевыпущен, штампован на
   восстановленные объекты, двойник жив и через дальнейшую
   игру.

## E. Стена: до/после (один инструмент, один протокол)

| | до (HEAD 26b5fa0) | после (iter-379) | |
|---|---|---|---|
| стена h32 10y (непроф.) | **9.59 с** | **8.08 / 7.99 с** | **×1.19** |
| профильная стена | 26.84 с | 21.11 с | ×1.27 |
| decay_walk | **3.308 с (12.5%)** | **0.257 с (1.2%)** | **×12.9** |
| decay_drafts per-call | 224.7 мкс | 4.8 мкс | ×47 |
| next_decay_tick (в skip_probes) | **2.676 с** | **0.053 с** | **×50** |
| next_decay_tick per-call | 350 мкс | 1.0 мкс | ×350 |
| skip_probes | 9.399 с | 6.800 с | ×1.38 |
| **экспонента decay (per-call h3→h32)** | **×8.1** | **×1.85** | убита |
| экспонента next_decay_tick | — | ×1.11 | плоско |
| события | 25 859 | 25 859 | идентичны |
| md5 лога h32 | `07e924cb…` | тот же | **байт-в-байт** |

Пары конверта: h3 md5 `796afbe1…` идентичен (стена 0.28 с против
0.30 iter-378); farstead 100y (loc_square, сегментированные)
md5 `4e4f4cf2…` идентичен (13 915 событий, 2.56 с против 2.62).
canon_check HELD в профилированных прогонах ОБЕИХ сторон.

**Экспонента списана:** остаток ×1.85 для decay_drafts — честное
линейное ядро (число ВЫСТРЕЛОВ само растёт с популяцией — это
работа, а не накладные скана; перечисление = O(выстрелов ×
log(живых))). next_decay_tick ×1.11 — плоско.

**Остаточная стена (переранжировка, ×1.19 от ×3.37 iter-362):**
skip_probes 32.8% (urgency_scan 6.73 с — роллинг-фильтр +
сборка ключей) > beat_rolls 19.4% > commit_validate 18.3%
(population-flat — никогда не стена) > projection_snapshot 5.5% >
decay_walk 1.2% (закрыта этой итерацией).

## F. Верификация (claim-пакет, TEST_PLAN §9)

- **Claim:** пул на пути коммита отвечает РОВНО тому, что
  отвечают обходы целой популяции, для связанных живых объектов,
  при всех трёх формах скоупа, без предположения о дисциплине
  коммита вызывающего, через границу процесса резюма.
- **Lens/Prism:** равенство значений и ПОРЯДКА (twin-agreement
  полный свип) / рождение-против-фолда (живой пул == свежему
  рождению).
- **Oracle:** обходы (семантические владельцы) на краевом
  сценарии + реальных логах; законы §D — фальсификаторы.
- **Observed:** 8/8 зелёные; канон-нейтральность: три md5
  байт-в-байт (h32/h3/farstead); canon_check HELD ×2; полная
  батарея **2643 passed + 28 failed** (сбор 2671 = 2663 HEAD + 8
  новых; 27 = известный T1 log-header env-набор, список имён
  сверен поимённо с базлайном ДО правок — ноль новых; +1 строка
  guard-теста docguard `docs/DECISIONS.md: 36 entries` — НАД
  КАПОЙ D-252, очищается коллапсом владельца, прецедент
  D-250/iter-367);
- `ruff check .` clean; `python scripts/topology.py --check`
  clean; `python scripts/digest.py` парсит (tests: 2643 passed +
  28 failed);
- INV-1..5 не тронуты (INV-2: ноль дроу, ноль часов, кортежные
  ячейки, ответы в порядке пакa — закон md5 байт-в-байт).

## G. Гит-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/states.py core/loop.py scripts/labrunner.py tests/test_decayidx.py STATUS.md worklog.md docs/TASKS.md docs/DECISIONS.md docs/iterations/iter-379-decayheap-report.md
git status --short
git commit -m "iter-379-decayheap: THE STANDING ORDER'S FOURTH HEAD LANDED - the decay landing index (D-256, R3, the iter-362 class, ZERO canon bytes) - per-LOCATION min-heaps of (next_fire, npc, prop) candidate cells over the LIVE pairs (valued int-not-bool, unpinned at the clamp bound in the axis's direction, uncaught, present), born from the pack-seeded initial projection (KI#16 - bases from the caller's last_change, base 0 at construction, the walk's own default) + THE STALENESS/VETO LAWS: INV-1 LICENSES STALENESS (every cause - base/value/pin/position/caught - rides a committed event and _commit folds every state change, so a dropped stale cell ALWAYS has a fresher successor or the pair is legitimately dead) + validation ON SIGHT (a popped cell passes the walk's OWN filters against the live bound state - present, positioned at the heap's key, uncaught, valued, unpinned, fresh next_fire == base + elapsed_first; invalid cells dropped on sight - the pool is a candidate set, never truth) + the enumeration NEVER CONSUMES (firing re-pushes every valid popped cell - a caller that drops the drafts leaves the pool exactly as it was) + the identity gate (serves: the stamped objects + the birth table only; every foreign caller keeps the walks - THE WALKS STAY THE SEMANTIC OWNERS, the per-pair formula extracted to _axis_change, both branches call exactly it; the max(..., from_tick) clamp stays next_decay_tick's own) + loop.py: born at construction, re-born from the restored projection + folded last_change on resume (rebuildable - never in export_run_state), wired into all three call sites (the skip probe, the beat, the macro warm-ring drift) + 8 oracle laws (tests/test_decayidx.py: the birth pool == the walks' live set on all six packs + the seeded-values teeth; the fold twin after EVERY one of 17 staleness edges - None birth, top pin, unpin, bool, str, cleared, re-birth, the fear bottom pin, the position heap-hop, the caught veto + release, two same-tick same-prop changes; the caught total veto; the enumeration-never-consumes; the identity gate - the foreign projection drafts through the walk, fresh/None tables unserved; the real-log twin mid-run and at drain + the live pool == a fresh birth; the resume law) + labrunner member comments/note; MEASURED: the wall h32 10y 9.59 -> 8.08/7.99 s (x1.19), the member decay_walk 3.31 -> 0.26 profiled s (12.5% -> 1.2%, x12.9; per-call 224.7 -> 4.8 us), next_decay_tick 2.68 -> 0.05 s (x50, 1.0 us), skip_probes 9.40 -> 6.80 s, the profiled wall 26.84 -> 21.11 s; THE DENSITY EXPONENT x8.1 -> x1.85 (the honest linear core: the firing count itself grows with the population) / x1.11 (flat); the sparse envelope no regression (farstead 100y 2.56 s, h3 0.28 s); ZERO canon bytes: h32 07e924cb../h3 796afbe1../farstead 4e4f4cf2.. identical before/after (canon_check HELD both sides); 2643 passed + 28 failed (27 = the failure set diffed IDENTICAL to the pristine pre-change baseline - the known T1 env set, zero new; +1 the guard test's own DECISIONS 36/35 count line - this row's over-cap record, the D-250 precedent state, clears on the owner's collapse call; the +8 the new laws all green), ruff+topology+digest clean; DECISIONS at 36/35 - OVER the D-252 cap, the collapse the owner's next exclusive call; INV-1..5 untouched"
git push
```

## H. Доставка (§12.2 — оба канала)
Дельта-архив `canonsim_iter-379-decayheap_2026-10-13.zip` против
BASE_COMMIT `26b5fa06…` — файлы §G + BASE_COMMIT.txt +
DELETED_PATHS.txt (`None`); self-check по `git status --porcelain
-uall`; md5 + байты + tmpfiles-ссылка — в финальном сообщении
сессии (само-ссылка: хэш архива не может лежать в отчёте, который
архив содержит).

**Done:** четвёртая голова стоящего приказа закрыта (индекс
приземления decay, класс iter-362, нуль канон-байт; ×1.19 стены,
×12.9/×50 членов, экспонента ×8.1 → ×1.85); 8 законов-оракулов;
D-256 записан (36/35 — над капой, коллапс на владельце);
инструмент синхронизирован.
**Not done:** роллинг-фильтр memo (urgency_rolls ~1.7 проф. с /
2.6M вызовов — следующая строка приказа); сборка ключей скана
(939K pair_values); beat_rolls (19.4%) — кандидат третьей
строки; коллапс DECISIONS — вызов владельца (36/35).
**Next:** стоящий приказ продолжается — роллинг-фильтр первой
строкой переранжировки §E, затем сборка ключей; параллельные
вызовы владельца прежние (runtime-promotion D-250, replay-UI,
W8, P1/P2/P3, lab-composite-1).
**Active KIs:** KI#113 (test_lab, как в STATUS — класс
growth/labels flake; на прогонах этой сессии ноль флейков).
