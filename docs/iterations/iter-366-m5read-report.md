# iter-366 · m5read — СТАНЦИОННЫЙ ПРОГОН M5 ПРОЧИТАН: like-for-like закрыт (R против G против H0/H8 на одном корпусе, одной сессии, одном спавне главной — то, что просил iter-361 §G), закон структуры ДОКАЗАН ЖИВЬЁМ: вердикт-слой H0 байт-идентичен G на 42/42 документах — гибрид покупает прозу, не качество вердикта; ручка 0.4 получает полный гроссбух цены на обоих языках (precision на проведённых FLAT: 60.0%→58.8% EN), полосы gate_p перекрываются — разделяющего порога в данных нет

**Владелец прислал:** `m5_20261011_002908.zip` — прогон
`m5_20261011_001111` пака **v5.0** (2026-10-11 00:11, станция
RTX 3080 Ti / 12287 MiB / 11100 free, Kev-4B роутер + Gemma-4-E4B
главная, ОБЕ FULL offload по плану vram, autospawn, порт 50114,
batch 2048/ubatch 512). Прогон **ПОЛНЫЙ И БЕЗ ЕДИНОГО КРАША**:
preflight (6 моделей, вердикты доктора) → reference **10/10** →
R-рука (42) → G-контроль (42) → H0 (42) → H8 (42) → RU-полоса
(12) → RU04 (12) → R04 (42) → det-мини → package — первый
полный m5-прогон серии, все 9 стадий в одном зипе. Явный ввод
сессии (D-198): архив в сессии = открытие чтения (R0/R1
riders-only, нулевой код репо, INV-1..5 не тронуты).

**BASE_COMMIT:** `fd420a3a473ba2dc4947421a8c0641f676f27126`
(HEAD iter-365 — пак m5 доставлен; этот прогон — его станционная
валидация).

## A. Метод чтения и верификация (стандарт iter-361)

Каждое число `m5_report.txt` заново выведено из сырых записей
(скрипт чтения вне репо, Правило 9): цензы всех рук из
`arm_r/arm_g/arm_h0/arm_h8/ru/ru04/arm_r04.jsonl`, латентность из
`r_wall_s`/`parse_wall_s`/`wall_s`, проза-гроссбух из
`prose_len`/`json_bleed`/`protocol_echo`/`eos_held`/
`finish_reason`, det-мини и cuda_gate из одноимённых файлов,
каскад s4 — событие за событием из
`arm_r04/s4_fire_chain/run.jsonl`. Окна подсчёта сверены: RU-стены
отчёта = `r_wall_s` (вызов systemone, med 0.516/mean 0.519);
input med 1531 = окно R+RU (54 вызова; только R = 1529).
Результат: **ВСЕ числа отчёта воспроизведены**, включая
м3-таблицу, обе цензы ложных разрешений, латентность и проза-хвосты.
Независимая классификация false-allow (политика пака,
восстановленная из записи: gate=blocked → blocked; иначе сравнение
kind+объект против золота, targetless-на-текстурном-золоте —
честный класс) даёт **ноль расхождений** с записанными `fa`
на всех 54 строках @0.4 — производная baseline @0.5 той же
политикой достоин доверия.

## B. THE M3 READING — таблица решения, перепроверенная

| метрика | R (роутер 0.5) | G (грамматика) | H0 (гибрид t0) | H8 (гибрид t0.8) |
|---|---|---|---|---|
| full vs gold | **16 (38.1%)** | 9 (21.4%) | 9 (21.4%) | 9 (21.4%) |
| kind+ | 21 (50.0%) | 24 (57.1%) | 26 (61.9%) | 26 (61.9%) |
| refusals | 19 (45.2%) | 12 (28.6%) | 11 (26.2%) | 11 (26.2%) |
| класс target | **1 (2.4%)** | 8 (19.0%) | 10 (23.8%) | 10 (23.8%) |
| parse wall med/max | **0.52 / 0.79 с** | 0.50 / 3.28 с | 7.32 / 32.00 с | 7.51 / 36.30 с |
| out tokens med | **0** | 25 | 84 | 85 |
| проза | — | — | med 275 зн | med 271 зн |
| CLEAN (drift=false) | 15: full 5, kind+ 7 | 10: full 1, kind+ 6 | 10: full 1, kind+ 6 | 10: full 1, kind+ 6 |
| det | **identical**, дайджест 962b30a4… | identical, дайджест c2e33bd9… | identical=False | identical=False |

Три структурных чтения, которых m4 не давал:

**B.1. ВЕРДИКТ-СЛОЙ H0 ≡ G — 42/42 ДОКУМЕНТА БАЙТ-ИДЕНТИЧНЫ.**
Одни и те же (unit, cycle) строки, те же классы цензы, те же
door_outcome, `pinned`-документы совпадают на всех 42 циклах;
CLEAN-подмножества G, H0, H8 — один и тот же список из 10 строк.
Гибрид один-проход НЕ добавляет вердикту ничего: его JSON-голова
проходит через тот же шлюз и даёт ту же цензу. Единственный
продукт лишних ~6.8 с и 84 токенов — проза-хвост (медиана
275 знаков). **H = G + проза при ×14.9 латентности** (7.31 против
0.49 с медиан; на G-Gem max 3.28 с против H 32.0/36.3 с —
генерационный хвост). H8: вердикт-слой неподвижен по температуре
(ценза в точности H0: full 9 / kind 5 / target 10 / no_pin 7 /
not_intent 11), выборка двигает только маргинальные door-исходы
(intent_rejected 8 против 11, take_failed 3 против 1) и поверхность
прозы.

**B.2. R — лидер вердикт-пути по всем осям измерения.** Full-рейт
×1.8 над G/H (16 против 9); точность таргета ×8–10 (класс
target 1 против 8/10 — семейство false_allow_object, см. §C);
латентность med 0.522 с / max 0.789 с — без генерационного
хвоста; **не-генеративность** (output_tokens=[0] ×54 вызовов,
физическая невозможность галлюцинации интента — роутер только
маршрутизирует); **побайтовая воспроизводимость**: det
identical=True, дайджест `962b30a43bdb6363` — ПЯТЫЙ подряд
байт-идентичный R-прогон серии (v4.1 + v4.2 ×2 + m4 + m5), и
RU-полоса 0.5 совпадает с m4 класс-в-класс. Гэп iter-361 «det
g-digest empty» ЗАКРЫТ: `c2e33bd90d353d2b` (g identical=True) —
теперь обе половины инструментально записаны.

**B.3. Закон терминированной прозы ДЕРЖИТ на станции.** Обе H-руки:
41/42 finish=stop — EOS отпускается естественно, форма с пустым
терминатором работает на Gemma-4-E4B FULL offload. Два честных
хвостовых дайджеста: eos_held 1/42 на каждой руке (finish=length,
ctok=416 — ПОТОЛОК max_tokens: h0 s7cy0 длина 581, h8 s8cy2
длина 658; флаг отчёта «check max_tokens» — это вопрос запаса
токенов пака v5.1, не дефект закона); h8 json_bleed 1/42 —
s4_fire_chain cy1: модель вставила в проза-хвост кодовую
ограду с повторной эмиссией вердикта (`##\n\`\`\`json\n{"intent":
…}`) — ДВЕРЬ БЕЗОПАСНА (разрез по первой пустой строке взял
голову; ценза строки full, каскад двинулся), флаг сработал как
положено: дефект поверхности прозы, не канона. protocol_echo 0/42
на обеих руках.

## C. THE M2 READING — гроссбух ручки 0.4 на обоих языках

Ценза ложных разрешений (@0.4 — записана паком, @0.5 — выведена
той же политикой; разбивка blocked на промах/честный отказ —
золото с действием/без):

**EN, n=42:**

| класс | @0.5 | @0.4 | дельта |
|---|---|---|---|
| correct_allow | 15 (35.7%) | 20 (47.6%) | **+5** |
| blocked_miss (золото с действием, гейт отказал) | 10 | 4 | **−6** |
| blocked_honest (золото без действия, гейт отказал — верно) | 7 | 4 | −3 |
| false_allow_nonintent | 4 | 7 | **+3** |
| false_allow_kind | 2 | 3 | +1 |
| false_allow_object | 4 | 4 | **0** |

**RU, n=12:** @0.5 correct 4 / object 1 / blocked 7 (промах 5 +
честный 2); @0.4 correct 6 / object 2 / blocked 4 (промах 2 +
честный 2) — +2 correct, −3 промаха, +1 object; семейство
nonintent на русском ОТСУТСТВУЕТ на обоих порогах (не-интентные
золота лежат ниже обеих линий).

Четыре чтения:

**C.1. Precision на проведённых — FLAT.** EN: 15/25 = 60.0% @0.5
против 20/34 = 58.8% @0.4 (−1.2); RU: 4/5 = 80% против 6/8 = 75%
(малая выборка). Вопрос владельца «прирост принятых сам по себе
не доказывает надёжность» получил измеренный ответ: ручка
конвертирует промахи в correct-ы ПО БАЗОВОЙ СТАВКЕ — надёжность
не отмывается, но и не деградирует; покупается recall.

**C.2. false_allow_object ИНВАРИАНТЕН к порогу** (EN 4 = 4:
ru_05-форма и s8/s10-формы живут выше 0.7 либо в слое сборки).
Ручка двигает ТОЛЬКО гейт; качество сборки двери — порог-инвариант.
Единственная RU-цена — ru_09 (examine без таргета, P=0.410:
маргинальный промах стал маргинальным ложным допуском).

**C.3. Полосы ПЕРЕКРЫВАЮТСЯ — разделяющего порога НЕТ.** Окно
0.4–0.5 EN: correct-ы [0.412, 0.431, 0.461, 0.475, 0.479] против
nonintent-ложных [0.442, 0.442, 0.488] — чередуются; маргинальная
точность окна 5/9 = 55.6% ≈ база. Оставшиеся промахи @0.4 —
[0.239, 0.301, 0.359, 0.377], все НИЖЕ 0.4; мёртвая зона
0.377–0.412 пуста. Структурная цена ручки — nonintent-семейство,
и оно НЕ видно гейту: золото s5/s9 требует «спроси, не угадывай»,
роутер же выдаёт уверенный мирной-действие-вердикт на P 0.44–0.65.
Это ограничение ФОРМЫ R (одна systemone-классификация без
не-интентного зеркала), не порога.

**C.4. Механика ручки — 9 конверсий no_intent→intent на EN.**
Документы: R 25 intent/17 no_intent @0.5 → 34/8 @0.4; RU 5/7 →
8/4. Каждая конверсия — строка, чей gate_p пересёк порог; их
качество (5 correct : 4 ложных) и есть честная цена-выгода окна.

## D. Паритет m4 и приращения серии

- **R ценза байт-в-байт m4-станции** (16/2/1/2/2 + 10/4/5), RU
  классы идентичны (5/5/1/1), det-дайджест роутера идентичен, s7cy0
  door_error «examine requires a target» воспроизведён 1:1 (стоимость
  target-резолюции формы R, дверь отказывает громко, не крашится),
  огненный каскад s4 идентичен событие-за-событием (ev_0008
  drop_break broken=true → ev_0009 fire_started spot=back_wall →
  ev_0010 fire_spread woodpile → ev_0012 location_burned_out t=131
  необратимо → ev_0013 flee t=135) — пятая строка
  воспроизводимости + живое доказательство фокуса Verb вторым
  станционным прогоном.
- **Гроссбух изобретений: 0 на 108 документах m5** (R 42 + R04 42 +
  RU 12 + RU04 12, формы intent/no_intent — все ключи из множеств
  пака); серия: 0/240 живых документов.
- **Латентность GPU-полосы подтверждена**: R systemone med 0.522 с
  (m4: 0.556), max 0.789 с; G med 0.489 с; H med 7.31/7.50 с —
  первая станционная запись H-полосы (×14 против R на одном
  спавне: два резидентных рейтинга генерации против нуля).
- **Honest gaps**: `cuda_gate.bands` по-прежнему `{}` —
  формализованный band sweep флагом пака не выполнялся (строка
  остаётся открытой); drift-флаги R 27/42, G/H 32/42 (статус
  premise-drift, сырой наблюдаемый — без цензы, как в m4); det h
  identical=False — ситтинг-датум движка (записан, финишы
  зафиксированы, не дефект).

## E. Материал решения M2/M3 (за гейтом runtime-promotion — вызов владельца)

**M3 (форма двери) — measured shape.** On one corpus, one session,
one main spawn: R — сильнейшая измеренная строка вердикт-пути
(full ×1.8, target-точность ×8–10, ×14.9 латентность,
не-генеративность, побайтовая воспроизводимость). H не добавляет
вердикту НИЧЕГО (его слой ≡ G, 42/42 байт) — его продукт проза,
ценой ×15 латентности и просадки target-точности (класс target 10
против 1 у R). Числа раскладывают архитектуру так: **R кормит
дверь; проза рассказчика — отдельная поверхность** (H-форма
один-вызов, если одна реплика за ход дорога, или G+narrator
двумя вызовами); H-как-дверь проигрывает по каждой вердикт-метрике.
Лидерство H в батарее m3 РЕШЕНО как корпус-относительное
(Laya zero-shot на корпусе m3; на корпусе m4 при like-for-like
построении H добавляет прозу, не вердикт).

**M2 (порог) — measured shape.** 0.5 честный дефолт (correct
35.7% EN / 33.3% RU; ложные 23.8% / 8.3%); 0.4 измеренная точка
возврата (correct 47.6% / 50.0%; ложные 33.3% / 16.7%) — recall
+11.9/+16.7 при FLAT precision; полосы перекрываются (разделяющего
порога нет — компромисс принципиален); structural цена — только
nonintent-семейство EN (гейт не видит «спроси, не угадывай»);
сборка порог-инвариантна (object 4=4). Порог — Deployment-ручка
с измеренным гроссбухом, не фикс корректности: профиль развёртывания
решает (recall-голодный → 0.4 с цензой nonintent на страже;
precision-голодный → 0.5).

Обе карточки решений теперь имеют полные живые числа на одном
корпусе — то, чего не хватало iter-361 §G. Вызов владельца.

## G. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` (3.12.15 сэндбокса) —
  2622 passed + 27 failed + 1 skipped: все 27 — известный T1
  log-header набор (байт-идентичен записи iter-362/363/365), на
  золотом 3.12.14 сюит зелёный (2649+1, iter-363); riders-only,
  код репо не тронут;
- `ruff check .` — clean; `python scripts/docguard.py` — clean;
  `python scripts/topology.py --check` — clean; `python
  scripts/digest.py` — парсит;
- чтение верифицировано против сырых записей (каждое число отчёта
  пере-выведено; политика false-allow восстановлена и сошлась
  0-расхождений на 54 строках @0.4);
- самопроверка дельты: список путей == `git status --porcelain
  -uall` против BASE (блок Git ниже);
- INV-1..5 не тронуты (R0/R1 riders, нулевой код репо).

Замечание о док-лупе (AGENTS §2.5, превентивно): шестая
riders-only итерация подряд — но это чтение станционного прогона
(функциональный результат: решения M2/M3 получают материал,
проверка инструмента живьём), форма самой серии станции (Rule 9);
нулевая строка TASKS не может двигаться кодом репо, пока решения
владельца за гейтом.

## H. Риски

- чтение опирается на один прогон одной станции (серия: пятый
  байт-идентичный R — риск низкий; H-полоса впервые записана —
  латентность H на других ситтингах может отличаться);
- проза оценивается поверхностями (длина/флаги), не эстетикой —
  эстетический вызов владельца;
- производная @0.5-политика false-allow восстановлена из записей,
  а не прочитана из кода пака — сходство 0-расхождений на 54
  строках @0.4 есть её валидация, но один класс-гранец
  (targetless-на-текстурном-золоте) зафиксирован по наблюдаемым
  классификациям, не по исходнику;
- eos_held 416-токенный потолок — вопрос запаса max_tokens пака:
  если поднять, латентность H-хвостов вырастет; не поднимать —
  две строки на руку не завершают EOS (закон 41/42).

## I. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-366-m5read-report.md
git status --short
git commit -m "iter-366-m5read: THE M5 STATION RUN READ - the owner's m5_20261011_002908.zip (the first FULL m5 run, all 9 stages, zero crashes, pack v5.0 on the 3080 Ti, both models FULL offload): every m5_report number re-derived from the raw jsonl (the census tables, the false-allow censuses, the latency + prose ledgers, the det mini, the s4 event log verbatim - the iter-361 verification standard; the counting windows reconciled: RU walls = r_wall_s, input med 1531 = the R+RU window) + THE M3 LIKE-FOR-LIKE CLOSED (R vs G vs H0/H8 on one corpus, one session, one main spawn - iter-361 §G's ask): R THE VERDICT-PATH LEADER (full 16/38.1% x1.8 over G/H, target class 1 vs 8/10, med 0.52s vs 7.31s x14, output_tokens=[0] x54, det identical digest 962b30a43bdb6363 - the FIFTH byte-identical R run of the series; the iter-361 g-digest gap CLOSED: c2e33bd90d353d2b) + THE STRUCTURAL LAW PROVEN LIVE: H0's verdict layer is BYTE-IDENTICAL to G's on 42/42 documents (same rows, same census classes, same door outcomes, same CLEAN set of 10) - THE HYBRID BUYS PROSE, NOT VERDICT QUALITY (275-ch median tail at x14.9 latency; H8's verdict layer immobile under temp, the sampling moves only marginal door outcomes + the prose surface) + THE TERMINATED-PROSE LAW HELD ON STATION (41/42 stop both arms; the two eos_held rows hit the 416-token max_tokens ceiling - the pack v5.1 headroom question; h8's 1 json_bleed = the fenced protocol echo inside the prose tail on s4 cy1 - THE DOOR SAFE: the split took the head, census full, the flag fired as designed) + THE M2 KNOB'S FULL COST LEDGER (the false-allow censuses + the derived @0.5 baselines, the blocked-miss/blocked-honest split): EN 0.5->0.4 correct 15->20 (+5), misses 10->4 (-6), honest 7->4 (-3), nonintent-false 4->7 (+3), object-false 4=4 INVARIANT (the assembly layer, never the gate); RU correct 4->6, object 1->2, nonintent ABSENT both thresholds; PRECISION ON PASSED FLAT (EN 60.0%->58.8%, RU 80->75 small-n) - the owner's 'the growth of accepted requests does not by itself prove reliability' answered: the knob converts misses into corrects AT THE BASE RATE, no laundering, no degradation, recall bought; THE BANDS OVERLAP (EN recovered-corrects 0.412-0.479 vs nonintent-falses 0.442-0.488 interleaved, the marginal window 5/9 = 55.6% ~ base; the remaining misses all <=0.377, dead zone 0.377-0.412) - NO SEPARATING THRESHOLD EXISTS, the knob is a genuine trade, its only structural cost the nonintent family the gate CANNOT see (the gold's ask-don't-guess demand); the m4 parity (R census byte-identical, RU classes identical, s7cy0 door_error reproduced 1:1, the s4 fire cascade identical event-by-event) + the invention ledger 0/108 m5 docs (0/240 series-wide) + cuda_gate.bands still {} (the honest open row); THE M2/M3 DECISION MATERIAL DELIVERED (R feeds the door, prose is a separate surface - H-as-the-door loses every verdict metric at x15; 0.5 the honest default, 0.4 the measured recovery point with flat precision - a deployment knob, the owner's call behind the runtime-promotion gate); pytest 2622+27(known T1 3.12.15 set)+1, ruff+docguard+topology+digest clean; R0/R1 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## J. Доставка (§12.2 — оба канала)

- **Дельта-архив** (вложение): `canonsim_iter-366-m5read_
  2026-10-11.zip` против BASE_COMMIT `fd420a3a473ba2dc4947421a
  8c0641f676f27126` — STATUS.md, worklog.md, docs/TASKS.md,
  docs/iterations/iter-366-m5read-report.md, BASE_COMMIT.txt,
  DELETED_PATHS.txt (`None`);
- tmpfiles-ссылка, md5 и размер — в финальном сообщении сессии.

**Done:** чтение m5-прогона по стандарту iter-361: каждое число
отчёта пере-выведено из сырых записей (окна подсчёта сверены),
оба гроссбуха ценз ложных разрешений верифицированы
(0-расхождений против записанных fa на 54 строках @04,
@0.5-baseline выведен той же политикой), м3-таблица решения
получила три новых структурных чтения (H0≡G 42/42; R лидер всех
вердикт-осей; закон прозы держит 41/42 с двумя честными
хвостовыми флагами), м2-ручка получила полный гроссбух цены
(precision flat, полосы перекрываются, object инвариантен),
паритет m4 подтверждён (пятый байт-идентичный R + каскад s4 +
s7cy0), гэп det-g-дайджеста iter-361 закрыт; райдеры прошли
ruff + docguard + topology + digest; T1-оговорка процитирована
честно (27 известных, золотой интерпретатор зелёный).
**Not done:** решения M2/M3 (владелец, за гейтом
runtime-promotion); формализованный band sweep (`cuda_gate.bands`
— флаг пака не выполнялся, строка остаётся открытой); эстетка
прозы не оценивалась.
**Next:** вызов владельца M2/M3 по карточкам §E (решения
распаковывают runtime-promotion: форма R у двери + порог
развёртывания); за ними в ранжировании iter-364 — строка
оптимизации бит-семейства (decay_walk ×11.76 / beat_rolls ×8.71,
класс преобразований iter-362: коллективные проходы + O(1)
индексы, байт-идентичность + законы оракула), commit_knowledge_fold
вторым, director_global_passes третьим; стоящие: replay-UI
NOT-EXPOSED, W8, P1/P2/P3, lab-composite-1.
**Active KIs:** KI#113 (test_lab, как в STATUS).
