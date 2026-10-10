# iter-364 · restsplit — ОСТАТОЧНЫЙ `rest` РАЗЛОЖЕН ПО ОПЕРАЦИЯМ: 93% — ПУТЬ КОММИТА (`knowledge.add` 8.9% ×6.74 по плотности + `schema.validate` 7.7% плоский), два листа стали членами инструмента, rest 21.5% → 4.8%; таблица роста по оси плотности ПЕРЕРАНЖИРУЕТ следующую стену: бит-семейство (квадратично) > knowledge-фолд > director (сублинеен на душу); решения владельца M2/M3 ЗАПИСАНЫ (§F)

**Вызов владельца (шаги 3–4 плана сессии, дословно):** «Шаг 3.
Принять решения M2/M3 … Моя рекомендация по M3: считать R ведущим
кандидатом для текущего M4-корпуса, но до общего продвижения
сравнить R и H на одном и том же корпусе, с одинаковыми условиями
и метриками. … Моя рекомендация по M2: пока сохранить 0,5 как
консервативный порог по умолчанию. Отдельно проверить 0,4 на
русских сценариях, измерить не только полноту сборки, но и
ошибочно разрешённые действия. … Шаг 4. Вернуться к
производительности — уже на новой базе … сначала нужно разложить
rest на конкретные операции, а затем сравнить ожидаемый эффект и
риск изменения семантики.» + постоянная форма «продолжай работы…
я разрешаю». Явный ввод сессии (D-198) — текущая задача.

**BASE_COMMIT:** `768dfdc7de7ed2258d6e2992e68a768d75cf666c`
(HEAD iter-362; iter-363 этой же сессии — riders-only, кодовая база
та же).

**Класс риска: R2** (локальное изменение поведения инструмента:
расширение карты членов labrunner + расширение двух существующих
законов test_lab; нулевой код ядра, нулевые канон-байты. DECISIONS
на капе 30/30 — запись решений владельца M2/M3 живёт в §F этого
отчёта, прецедент iter-332/362).

## A. Измерение ПЕРЕД кодом (полная атрибуция каллеров)

Пост-362 профиль воспроизведён сначала как есть (labrunner, seed 7,
h32, сегментированные 10y, якорь loc_s0_square, директоры off):
стена 18.2 с, события 25 859, члены точно по записи iter-362
(skip_probes 33.3 / rest 21.5 / beat_rolls 16.2 / decay_walk 15.4 /
director 10.2). Затем пробник сессии (вне репо, Правило 9 — тот же
протокол под cProfile, канон-нейтральность с основной батареей
HELD) слил полный pstats; каллер-атрибуция дала точное дерево
стены:

```
run_steps (51.45 s, профильная)
├── _run_beat 23.45 s (n=7 634)
│     ├── urgency_intents  7.98 s  [член beat_rolls]
│     ├── decay_drafts     7.63 s  [член decay_walk]
│     ├── director.releases 5.09 s ──> entropy 5.05 s [член
│     │     director_global_passes — ВЫЗЫВАЕТСЯ ТОЛЬКО ИЗ releases;
│     │     собственное время обёртки 0.036 s]
│     ├── _snapshot_for    1.28 s  [член projection_snapshot]
│     ├── коммиты бита     1.05 s  (validate/add — будущие члены)
│     └── обёртка          ~0.46 s
├── _skip_quiet_beats 17.03 s (n=7 637)
│     └── urgency_scan 11.10 + next_decay_tick 5.26 + faction_scan
│           0.02 [члены skip_probes] — обёртка 0.03 s
├── _complete 9.96 s (n=13 302) ── ПУТЬ КОММИТА (в rest!)
│     ├── _commit ← _complete  8.89 s
│     │     ├── knowledge.add   4.44 s (n=25 859 — КАЖДЫЙ эвент)
│     │     ├── log.append      4.70 s, внутри schema.validate
│     │     │     3.88 s (780 283 вызова: 25 859 первичных +
│     │     │     рекурсивный спуск $ref/типов)
│     │     └── _react          2.16 s (реакции; сам ре-ентерит
│     │           _commit — 6 115 вложенных коммитов)
│     └── резолверы/прочее     ~1.1 s
├── _execute_intent 0.35 s + _run_macro 0.03 s + ротации/календарь
└── машина очереди (self 0.44 + contextlib 1.5 с на 1.9M входов)
```

**Чтение:** `rest` 21.5% ≈ **93% — путь коммита**: два листа
`knowledge.add` (8.6% профиля) и `schema.validate` (7.5%) плюс
обёртки/очередь/дверь (~4–5%). Оба листа вызваны ТОЛЬКО из
`_commit` (validate — через log.append; add — напрямую; 25 859 =
каждый эвент). Директорного «второго безымянного прохода» НЕТ:
`releases` — обёртка, внутри которой живёт уже-именованный `entropy`.

## B. Закон двойного счёта — кто НЕ стал членом (сознательно)

`_complete`/`_commit`/`log.append`/`_react`/`releases` остаются в
`rest`: их поддеревья СОДЕРЖАТ листья-члены (а `_react` ре-ентерит
`_commit` — 6 115 вложенных коммитов на h32). Ввод любого из них
как entry = двойной счёт нижележащих листьев — та же граница, что
`kind_of` у iter-346, теперь зафиксирована в `_PROFILE_NOTES`.

## C. Изменение (2 файла кода + 2 теста-расширения)

1. **`scripts/labrunner.py`** — `_MEMBER_ENTRIES` + 2 члена:
   `commit_validate` = (core/schema.py, validate) — пер-эвентная
   JSON-схемная валидация писателя (runtime-страховка; рекурсивный
   спуск; пер-колл стоимость ПЛОСКА по населению); и
   `commit_knowledge_fold` = (core/knowledge.py, add) — пер-эвентное
   обновление картины знания (эпистемический фолд; пер-колл
   стоимость растёт с E). `_KEY_FUNCS` + 7 ног таблицы роста
   (validate/add/append/_commit/_complete/_react/releases —
   обёртки как ключи, никогда члены: они несут датум вложенности).
   `_PROFILE_NOTES` + запись (что теперь в rest + экспоненты).
   Докстринг-закон 8 синхронизирован.
2. **`tests/test_lab.py`** — закон аккаунтинга: имена новых членов
   в наборе «существует как ключ» (честный ноль, не отсутствующий
   ключ); закон grown-world: оба листа > 0 на любом мире, где
   коммитятся эвенты (зубы: член, не ловящий вызов, — декорация).

## D. Стена после расширения (один инструмент, один протокол)

| | iter-362 (запись) | iter-364 (этот прогон) | |
|---|---|---|---|
| стена (непрофилированная) | 18.34 с | 18.31 с | неизменна |
| события | 25 859 | 25 859 | идентичны |
| skip_probes | 33.2% | 33.4% | джиттер |
| **rest** | **21.5%** | **4.8%** | **−16.6 пунктов** |
| commit_knowledge_fold | (в rest) | 8.9% | новый член |
| commit_validate | (в rest) | 7.7% | новый член |
| канон-нейтральность | HELD | HELD | |

Остаточный `rest` 4.8% = обёртки пути коммита (≈3.4%:
_complete/_commit/log.append/_react минус листья) + машина
очереди/часы (≈1.0%) + дверь/ротации (≈0.4%) — каждая часть
меньше членов, ни одна не адрес отдельной строкой без нового
измерения.

## E. Таблица роста по оси плотности и РАНЖИРОВАНИЕ следующей стены

Обе ступени: S=4, сегментированные 10y, seed 7, якорь loc_s0_square;
население NPC 49 → 165 (**×3.37**); пер-колл стоимость (мкс/вызов):

| операция | h3 | h32 | рост | класс роста |
|---|---|---|---|---|
| decay_drafts | 84.8 | 997.7 | **×11.76** | ≈ квадрат в населении |
| next_decay_tick | 66.1 | 688.9 | **×10.42** | ≈ квадрат |
| urgency_intents (beat_rolls) | 119.9 | 1044.2 | **×8.71** | ≈ квадрат |
| knowledge.add | 25.5 | 171.8 | **×6.74** | ≈ квадрат |
| urgency_scan | 239.7 | 1452.9 | ×6.06 | ≈ квадрат (блочный ход ×2.11 внутри) |
| _react | 23.9 | 83.4 | ×3.49 | ≈ линейно |
| **entropy (director)** | 265.0 | 661.9 | **×2.50** | **СУБЛИНЕЙ на душу** (×2.50 при ×3.37 населения) |
| _snapshot_for | 43.0 | 84.3 | ×1.96 | ≈ линейно на постановку |
| **schema.validate** | 4.8 | 5.0 | **×1.04** | **ПЛОСКО** (форма документа) |
| log.append (без validate) | ~189 | ~182 | ×0.96 | плоско |
| scene_zones | 21.2 | 23.3 | ×1.10 | L-линейно |

**Эффект-vs-риск (материал решения, ранжировано измерением):**

1. **Бит-семейство** (skip-остаток 33.4% + beat_rolls 16.3% +
   decay_walk 15.5% ≈ 65% стены, рост ×6–12): максимальный
   произведение доля×экспонента. Класс трансформации iter-362
   (коллективные обходы + O(1)-индексы, побайтовая идентичность +
   законы-оракулы) применим напрямую; фальсификаторы существуют
   (scan-vs-walk, T1-под-скипом). Риск: средний (семантика —
   допуск вероятностей: гейты `first_failing`, роллы, decay-оси).
   Кандидаты внутри: `decay_walk` (×11.8, 15.5%) и остаток гейтов
   сканов (`first_failing` 3.85 с по iter-362).
2. **commit_knowledge_fold** (8.9%, ×6.74): вторая строка. Слой
   эпистемический — фальсификаторы T3-законы нулевой утечки; add()
   инкрементален, 2.76 с self = словарная работа (34.6M dict.get).
   Риск: средне-высокий (закон чистоты read-side, D-049/D-088) —
   отдельный допуск.
3. **director_global_passes** (10.2%, ×2.50 — сублинейно на душу):
   кандидат владельца, честно ПЕРЕРАНЖИРОВАН измерением вниз —
   самый мягкий по экспоненте из популяционных проходов (внутренние
   _global_suspicion/_visible_physical_threats мельче сканов),
   ~половина эффекта бит-семейства при ~половине роста. Остаётся
   законной строкой (слой истории глобален ПО ЗАКОНУ, iter-346),
   но третьей по приоритету.
4. **commit_validate** (7.7%, ×1.04): минимальный семантический
   риск (чистая мемоизация скомпилированных проверок per-type),
   но выигрыш ПЛОСКИЙ по плотности — эта строка никогда не станет
   стеной, её доля ОТНОСИТЕЛЬНО падает с ростом населения.

## F. РЕШЕНИЯ ВЛАДЕЛЬЦА M2/M3 — ЗАПИСЬ (DECISIONS на капе 30/30,
прецедент iter-332/362; строка-владелец — эта секция + TASKS)

- **M3 (форма: H / G2 / F / R)**: R — ВЕДУЩИЙ КАНДИДАТ текущего
  M4-корпуса (38.1% full, 0 изобретений, output_tokens=[0], med
  0.556 с, побайтово воспроизводим ×4 — iter-361 §C); НО до общего
  продвижения (runtime-promotion) — СРАВНЕНИЕ R И H НА ОДНОМ КОРПУСЕ,
  одинаковые условия и метрики (H — лидер m3-батареи на другом
  корпусе; like-for-like оговорка iter-361 §G снимается только
  таким прогоном).
- **M2 (block / downgrade / allow + C-tight/C-full)**: порог 0.5
  ОСТАЁТСЯ консервативным дефолтом; 0.4 — ОТДЕЛЬНЫЙ RU-прогон,
  измеряющий НЕ ТОЛЬКО полноту сборки, но и ОШИБОЧНО РАЗРЕШЁННЫЕ
  действия (ложные допуски): рост числа принятых запросов сам по
  себе не доказывает надёжность (слова владельца дословно).
- **Инструментальное следствие**: строка `m5-station` открыта
  (TASKS): M5-пак = база m4 v4.3 + H-рука на том же корпусе +
  RU-0.4-стадия с цензом ложных допусков. Предусловие: зип
  m4-пака от владельца (Rule 9 — пак живёт вне репо; в песочнице
  его нет; восстановление с нуля вместо базы повторило бы
  дорогие уроки iter-352/359/360 — лестница путей, флаги, Verb).
  Станционные прогоны — за владельцем (RTX 3080 Ti; в сэндбоксе
  нет GPU и 4 ГБ RAM).

## G. Верификация

- `PYTHONHASHSEED=0 pytest` на ЗОЛОТОМ интерпретаторе 3.12.14
  (iter-363 — новая точка отсчёта): **2649 passed + 1 skipped,
  zero failed**; на 3.12.15 — 2622 + 27 (известная оговорка
  log-header, набор идентичен iter-362, ноль новых);
- `tests/test_lab.py` — 19 законов зелёные (закон аккаунтинга
  держит расширенную карту: members+rest == total, флаг
  members_disjoint True на обеих фикстурах — малой и grown-world);
- Канон-нейтральность расширенного инструмента: HELD в записи
  (профилированные байты == непрофилированным на [10]y);
- `ruff check .` — clean (0.17.0); `python scripts/docguard.py` —
  clean; `python scripts/topology.py --check` — clean; `python
  scripts/digest.py` — парсит;
- INV-1..5 не тронуты (инструмент + тесты; нулевые канон-байты:
  md5 лога h32 в записи канон-чека HELD).

## H. Гит-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add scripts/labrunner.py tests/test_lab.py docs/TEST_PLAN.md STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-363-py31214-report.md docs/iterations/iter-364-restsplit-report.md
git status --short
git commit -m "iter-363-py31214 + iter-364-restsplit: THE TEST-ENV CAVEAT CLOSED BY FACT + THE POST-362 rest DECOMPOSED - iter-363: the full suite GREEN on the golden interpreter Python 3.12.14 (uv standalone; 2649 passed + 1 skipped, ZERO failed - the 27 3.12.15 failures are EXACTLY and ONLY the log-header python field, closed both directions; 2622+27=2649 reconciled; a fresh cross-iron byte-identity point: Linux x86_64 3.12.14 regenerates the owner's Windows goldens byte-identically) - TEST_PLAN 1.1 carries the measured fact. iter-364 (R2 instrument extension, the iter-346 form): the full-pstats caller attribution found rest 21.5% == 93% THE COMMIT PATH - knowledge.add 8.9% (the per-event epistemic fold, per-call x6.74 along h3->h32, NPC 49->165 x3.37) + schema.validate 7.7% (the writer's per-event schema backstop, x1.04 population-FLAT, 780K calls = 25859 primaries + recursive descent) + wrapper/queue/door residues 4.8%; the two leaves became MEMBERS (commit_validate + commit_knowledge_fold, both called ONLY from _commit; the double-count law keeps _complete/_commit/log.append/_react/releases OUT - their subtrees CONTAIN the leaves, _react re-enters _commit 6115 times) + 7 key-table legs + the notes law; rest 21.5% -> 4.8% on the re-run, the wall unchanged 18.31 s, canon-neutrality HELD; THE DENSITY-AXIS GROWTH TABLE (both S=4/10y/seed 7): decay_drafts x11.76 / next_decay_tick x10.42 / beat_rolls x8.71 / knowledge.add x6.74 / urgency_scan x6.06 / _react x3.49 / entropy x2.50 (SUBLINEAR per capita - the mildest population walk) / validate x1.04 flat - THE NEXT-WALL RANKING the measurement forces: the beat-machinery family (~65% of the wall, quadratic) > commit_knowledge_fold (8.9%, x6.7, T3 leak laws the falsifiers) > director_global_passes (10.2%, x2.5 - the owner's candidate honestly re-ranked THIRD by the exponent) > commit_validate (7.7%, flat - never the wall); test_lab's accounting law name-set + grown-world teeth extended (19 laws green); THE OWNER'S M2/M3 CALLS RECORDED (the report F): M3 R the leading candidate on the m4 corpus with the R-vs-H SAME-CORPUS comparison required before any runtime-promotion; M2 0.5 the conservative default, the 0.4 knob's RU run must measure the FALSELY-ALLOWED actions too - the m5-station row opened (precondition: the owner's m4 pack zip, Rule 9); 2649+1 on 3.12.14, ruff+docguard+topology+digest clean; INV-1..5 untouched"
git push
```

## I. Доставка (§12.2 — оба канала)

Дельта-архив `canonsim_iter-363-364_2026-10-11.zip` против
BASE_COMMIT `768dfdc…` — файлы §H + BASE_COMMIT.txt +
DELETED_PATHS.txt (`None`); self-check по `git status --porcelain
-uall`; md5 + байты + tmpfiles-ссылка — в финальном сообщении
(само-ссылка: хэш архива не может лежать в отчёте, который архив
содержит). Пробники/профили сессии — вне репо (Правило 9),
воспроизводимы из семени.

**Done:** rest разложен на именованные операции (путь коммита —
93% остатка); инструмент расширен (+2 члена, rest 21.5→4.8%);
таблица роста по плотности снята; ранжирование следующей стены
обосновано измерением; решения M2/M3 записаны; оговорка T1
закрыта фактом (iter-363).
**Not done:** сама оптимизация следующей стены (бит-семейство —
своя строка за допуском владельца); M5-пак (ждёт зип m4-пака);
формализованный band-sweep; RU-0.4 прогон (станция).
**Next:** за владельцем — зип m4-пака (открывает m5-station:
R-vs-H один корпус + RU-0.4 с цензом ложных допусков) и/или допуск
строки оптимизации бит-семейства (decay_walk ×11.8 — сильнейший
кандидат по доля×экспонента); стоящие вызовы прежние (replay-UI,
W8, P1/P2/P3, lab-composite-1).
**Active KIs:** KI#113 (test_lab, как в STATUS); KI#117 удалён по
§5 (закрыт iter-360, более двух итераций назад).
