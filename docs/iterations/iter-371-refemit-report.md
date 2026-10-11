# iter-371 — refemit: KI#120 ЗАКРЫТ ФИКСОМ В ПАКЕ v6.1 — РЕФЕРЕНС КОММИТИТ ЗОЛОТУЮ ТРАЕКТОРИЮ + СТАНЦИОННЫЙ ПРОГОН ПОДГОТОВЛЕН

**Task ID:** iter-371-refemit · **Дата:** 2026-10-12 ·
**Класс:** R0/R1 райдеры + R2 вне репо (пак-инструмент, Правило 9;
в репо — только райдеры и архив) · **BASE_COMMIT:**
`25f6ea84871483abdb8d60a8b9c34d276d111cf4` (iter-370).

## A. Что сделано (в двух словах)

Вызов владельца «готовь прогон или ki закрывай» (2026-10-12)
исполнен **в обе половины сразу**: KI#120 закрыт фиксом, и этот же
фикс есть подготовка станционного прогона — станция теперь гоняет
**v6.1**, и её drift-колонка с первого же прогона читается в
честном смысле. Дефект (живший с самого m3): `run_reference`
применял закреплённые золотые ответы через `door.apply_reply` **БЕЗ
`door.emit_call`** — контракт двери «один вызов ждёт один ответ»
отклонял каждый (`ParseError: no parse call awaits a reply`), который
глотал толерантный `except`. Референс-логи всей серии = setup +
narrator-биты: **золотая траектория корпуса никогда не выполнялась**
(цепочка огня s4 — включая GREEN-доказанный каскад iter-360 — в
референсе не существовала), а drift-отпечатки мерили «рука сдвинула
мир от нетронутой premise», НЕ «разошлась с золотом». Фикс — одна
строка в форме **собственного теста парсера репо**
(`test_phase2_parse_regression_set`, tests/test_parser.py:629 —
эталон честной формы, который был рядом всё время): `emit_call` в
say-циклах референса.

## B. Живое доказательство (до/после, scripts/ki120_proof.py вне репо)

- **Сломанная форма (v6.0):** все 5 золотых ответов s4 отклонены
  (`ParseError: no parse call awaits a reply — say <text> first`),
  лог = **6 событий** (setup + narrator), цепочка огня **ОТСУТСТВУЕТ**.
- **Исправленная форма (v6.1):** применены 5/5, лог = **15 событий**:
  `take → move → drop_break → fire_started → fire_spread →
  smoke_rising → location_burned_out → flee → intent_rejected`
  (последний — честный отказ мира на arson по loc_street, оба исхода
  двери по закону теста парсера). Ровно запись KI#120, дословно.

## C. Устройство v6.1 (дельта над v6.0; руки r/g/ru — m5 ПОСЛОВНО)

1. **run_reference**: `door.emit_call(cycle["say"])` перед
   `apply_reply` (голый вызов, как в руках g/r и в тесте парсера);
   докстринг фикс-закона; **закон пропуска probe-циклов НЕ ТРОНУТ** —
   руки и референс пропускают одни и те же циклы (проверено: все 9
   probe-циклов корпуса — s6×6, s7×1, s8×1, s10×1 — ездят НА
   say-циклах), сравнение drift остаётся apples-to-apples.
2. **DRIFT-КОЛОНКА — новый смысл**: флаг = «состояние руки на старте
   цикла разошлось с ЗОЛОТОЙ траекторией». Числа m4/m5 (R 27/42 /
   G 32/42 на станции) остаются в узком чтении «от нетронутой
   premise» — оба смысла задокументированы (README пака + примечание
   CLEAN в отчёте + эпилог --help). Ограничение (записано в
   оговорках README): числа v6.1 нельзя сравнивать с m4/m5 подряд —
   только внутри одного прогона.
3. **Юнит 13/13** (+`test_reference_commits_gold`): референс
   коммитит золото — s4 цепочка событие-за-событием, отпечатки
   растут и monotone, intent_rejected на месте; регрессия
   невозможна.
4. Райдеры пака: PACK_VERSION v6.1 + история версий, шапка модуля,
   CLEAN-примечание в m6_analysis, README_RU.txt (что нового, смысл
   drift, оговорка сравнимости), заголовок bat.

## D. Живая валидация (сэндбокс; окружение установлено по разрешению
владельца «можешь устанавливать llama.cpp для работы и прочее
окружение»: движок b11541 ubuntu sha256-pinned через setup пака,
модели Laya-Q8_0 + Qwen3-0.6B-Q4_K_M md5-pinned доктором; движок
найден законом соседних паков — v6.0 лежит рядом, перекачки нет)

- **Юниты 13/13** (12 m6-пословно + 1 новый).
- **Смоук** (s1+s2, все стадии): зелёный; RU-ценза на каждой строке;
  gold:s1 = 7 строк (золото коммитится) при r:s1 = 6 — дрейф стал
  виден В ПОВЕРХНОСТИ ПРОЗЫ.
- **ПОЛНЫЙ КОРПУС одним чанком** (все стадии done, finished=True):
  - **ПАРИТЕТ m4/m5/v6.0 ТОЧНЫЙ** (руки не тронуты): R full=6
    (14.3%) ровно строка валидации; G full=4, kind+=16 (38.1%),
    refusals=11; RU kind=6/blocked=3/fp=1/not_intent=1/target=1;
    output_tokens=[0]×42; inventions 0/42; вход med 841; R systemone
    med 3.332 с / G parse med 4.394 с (полоса CPU, честно
    помечена). Каждое число перепроверено из сырья (arm_*.jsonl,
    ru.jsonl) — стандарт iter-361.
  - **РЕФЕРЕНС (эффект фикса)**: отпечатки растут с золотом (s4
    6→7→8→13→14; s7 6→…→24 — батч распада wait-720 внутри
    run_steps двери; s1 5→…→9); леджеры несут пины (1–2 записи);
    gold:s4 = **13 строк прозы С КАСКАДОМ** (r:s4 = 14 —
    поверхности прозы теперь сравнимы, в v6.0 у gold:s4 было 6
    строк «ничего не случилось»); gold:s2 == r:s2 байт-в-байт
    (дайджест 44ff4d405225e47e — рука повторила золото точно).
  - **DRIFT нового смысла**: R 28/42, G 29/42 (CLEAN R 14 / G 13 —
    «ещё на золотой траектории»). Первые honest числа колонки.
  - narrate 20/20 детерминирован; det router identical
    (b448cdfe4c14ff41) / g identical (30511b5b95a171f7);
    бенд-вердикт ГРОМКИЙ: «Qwen3-0.6B, Laya ran the CPU band (no
    ggml_cuda_init in the log). No CUDA was visible at all — the
    CPU band is the honest band for this machine» — прибор KI#119
    работает вживую.
  - Пакет: m6_20261011_223843.zip (349 776 б полного прогона).

## E. Риски

- drift-числа v6.1 — НОВОЙ колонки: сравнение с m4/m5 подряд
  запрещено (записано в README и отчёте пака);
- референс теперь коммитит и мировые отказы (intent_rejected) —
  отпечаток считает события, не «успехи»; это честно (мир отвечал),
  но чтение отпечатка = «длина золотого пути с отказами»;
- станционный Kev-4B даст свои drift-числа (роутер сильнее Laya —
  CLEAN, вероятно, больше; измерится, не спекуляция);
- позитивный вердикт бенда «cuda» ещё не виден вживую (сэндбокс без
  CUDA; юнит-форма покрыта, станция скажет фактом).

## F. Проверки

- **База ДО правок** (нетронутый HEAD 25f6ea8, эта сессия):
  2626 passed + 27 failed + 1 skipped — набор идентичен записи
  iter-370 (все 27 — известный T1-набор байт-сравнений золотых
  логов, патч-символ 3.12.15 в заголовке лога; golden 3.12.14 весь
  зелёный по iter-363); ноль флейков test_lab на обоих прогонах;
  ruff clean, docguard clean, topology clean, digest parses.
- **После райдеров**: те же проверки (см. §H) — правки только в
  райдерах и архиве, код репо нулевой, INV-1..5 не тронуты.
- Самопроверка дельты: список путей == `git status --porcelain
  -uall` против BASE (§I).

## G. Поставка (обе половины вызова)

- **Прогон подготовлен**: пак v6.1 — вложение +
  docs/station/archive/canonsim_m6_station_pack_v6.1.zip (76 897 б,
  md5 2370f9fcffe01af616d99a11f3c93442). Инструкция владельца —
  README_RU.txt (распаковать, сетап, doctor, двойной клик
  station_m6_probe.bat, вернуть m6_*.zip + вердикт бенда из хвоста
  консоли).
- **KI закрыт**: STATUS KI#120 → CLOSED iter-371 (KI#119 удалён по
  §5 — закрыт iter-368, прошло три итерации).

## H. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-371-refemit-report.md docs/station/archive/canonsim_m6_station_pack_v6.1.zip
git status --short
git commit -m "iter-371-refemit: KI#120 CLOSED BY THE v6.1 FIX - the reference's say-cycles honor the door's contract (emit_call -> apply_reply, the parser test's own form; the bug lived since m3: every pinned gold reply died a swallowed ParseError, the reference logs were setup+narrator beats, the gold trajectory NEVER ran) - THE M6 STATION PACK v6.1: the reference COMMITS the gold trajectory (proven live: s4 = 6 events without the fire chain -> 15 events with take->move->drop_break->fire_started->fire_spread->smoke_rising->location_burned_out->flee->intent_rejected); THE DRIFT COLUMN reads gold-path divergence now (the m4/m5 numbers keep their narrowed pristine-premise reading, both documented; the probe-cycle skip law untouched - arms and reference skip the same cycles); VALIDATED LIVE FULL-CORPUS (b11541 + Laya + Qwen3-0.6B, md5-pinned): units 13/13 (+1 new: the reference commits gold), smoke green, the full corpus in ONE chunk - all stages done, THE m4/m5/v6.0 PARITY EXACT (R full=6/14.3%, G full=4/kind+=16/38.1%/refusals=11, RU classes identical, output_tokens=[0]x42, inventions 0/42, every number re-derived from the raw records); the reference fingerprints grow with gold (s4 6->7->8->13->14, s7 to 24), gold:s4 = 13 lines of prose WITH the cascade, the new-meaning drift R 28/42 / G 29/42 (CLEAN 14/13), narrate 20/20, det identical, the band verdict loud (CPU, honest); the v6.1 zip archived in docs/station/archive/ (the m5/m6.0 pattern - the station source at every future clone); THE STATION RUN now rides v6.1 (the owner's call 'готовь прогон или ki закрывай' - both halves executed); riders-only, zero repo code; pytest 2626+27(the known T1 set, identical to the pre-change baseline taken this session; zero flakes)+1, ruff clean, docguard clean, topology clean, digest parses; INV-1..5 untouched"
git push
```

## I. Доставка (§12.2 — оба канала)

- **Дельта-архив** (вложение): `canonsim_iter-371-refemit_
  2026-10-12.zip` против BASE_COMMIT `25f6ea84871483abdb8d60a8b
  9c34d276d111cf4` — STATUS.md, worklog.md, docs/TASKS.md,
  docs/iterations/iter-371-refemit-report.md,
  docs/station/archive/canonsim_m6_station_pack_v6.1.zip,
  BASE_COMMIT.txt, DELETED_PATHS.txt (`None`);
- **Пак станции** (вложение, для двойного клика):
  `canonsim_m6_station_pack_v6.1.zip` (76 897 б, md5
  2370f9fcffe01af616d99a11f3c93442) — распаковать рядом с репо
  (или куда угодно — лестница найдёт; движок наследуется законом
  соседних паков от m5/m4/m6.0);
- tmpfiles-ссылка, md5 и размеры — в финальном сообщении сессии.

**Done:** KI#120 закрыт фиксом в v6.1 (emit_call в say-циклах
референса — форма собственного теста парсера репо; баг
воспроизведён живьём до/после; паритет рук точный; юниты 13/13);
drift-колонка переведена в честный смысл «расхождение с золотом»
(оба чтения задокументированы); пак v6.1 собран, валидирован на
полном корпусе живьём, заархивирован в репо и подготовлен как
следующий станционный прогон (готовь прогон — исполнено).
**Not done:** сам станционный прогон (владелец: двойной клик
station_m6_probe.bat из v6.1, вернуть m6_*.zip + вердикт бенда);
DECISIONS-коллапс (кап 33/35, вызов на breached).
**Next:** станционный прогон v6.1 (бенд-вердикт + продакшн-батарея
на 3080 Ti + ПЕРВЫЕ honest drift-числа станционного класса); за
ним — голова ранжирования iter-364: first_falling's gate reads
(7.45 с, форма: мемо ответа гейта над замороженным состоянием,
закон инвалидации вперёд), commit_knowledge_fold (T3-фальсификаторы),
director_global_passes.
**Active KIs:** KI#113 (test_lab-класс, как в STATUS); KI#120
закрыт этой итерацией; KI#119 удалён по §5.
