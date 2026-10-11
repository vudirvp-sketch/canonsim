# iter-365 · m5station — ПАК M5 ПОСТРОЕН И ВАЛИДИРОВАН: H-рука на корпусе m4 (гибрид один-проход, закон терминированной прозы) + ручка 0.4 с цензой ложных разрешений на обоих языках; паритет базы m4 доказан живым прогоном

**Вызов:** строка `m5-station` (docs/TASKS.md, открыта iter-364 по
решениям владельца M2/M3 §F) с выполненным предусловием — zip
m4-пака v4.3 пришёл в сессию. Постоянный приказ сессии:
«продолжай работы, открывай то что сейчас важнее всего сделать,
логичнее и качественнее на долгосрок. я разрешаю.» Явный ввод
сессии (D-198): прибытие зипа = открытие строки.

**BASE_COMMIT:** `709d355fb24caaf87280df79707949344249a7f0`
(HEAD iter-364 — restsplit + py31214).

**Класс риска:** R0/R1 riders-only (внутрирепо — только док-райдеры;
нулевой код, INV-1..5 не тронуты). Пак живёт ВНЕ репо по
Правилу 9 / D-046, форма iter-348..360 — на базе v4.3 ПОСЛОВНО
(предусловие строки: пересборка с нуля повторила бы дорогие уроки
iter-352/359/360 — лестницу репо, флаги, ветку Verb).

## A. Пак M5 v5.0 (10 файлов, вне репо)

`canonsim_m5_station_pack_v5.0.zip` — 70 135 Б, md5
`f7fec7224f855c4ef7cd0bd82183085d`. Состав: station_m5_probe.py
(батарея), m5_analysis.py (отчёт), m5_units.py (юниты),
station_m5_setup.py/.bat + station_m5_doctor.py/.bat (инструменты m4,
переименованные, вердикты/пины пословно), station_m5_probe.bat,
README_RU.txt, m5_sandbox_report.txt (валидационная запись).

**НОВОЕ 1 — H-рука (M3, ядро m5):** гибрид один-проход формы m3 на
корпусе m4 — ОДИН вызов главной модели несёт вердикт И прозу.
Грамматика `root ::= verdict-doc "\n\n" prose` с ЗАКОНОМ
ТЕРМИНИРОВАННОЙ ПРОЗЫ (iter-351 D.1 пословно: тело без пустых строк
+ пустой терминатор → root достигает акцепта, EOS отпускается
естественно; звёздные формы держат генерацию до max_tokens).
Грамматика вердикта — грамматика репо ПОСЛОВНО (root переименован,
каждая другая правила байт-идентична): JSON-голова гибридного ответа
грамматически идентична целому ответу G-руки — ценз like-for-like у
источника. Дверь режет ответ по ПЕРВОЙ пустой строке: JSON → СУЩЕСТВУЮЩИЙ
шлюз (apply_reply, тот же файловый контракт, что у G); проза-хвост →
записанная поверхность (длина, json_bleed, protocol_echo, eos_held;
дословный текст в jsonl). Две половины: H0 (temp 0) и H8
(temp 0.8-seeded), ОБЕ на ТОМ ЖЕ спавне главной, что и G (стены
сравнимы по построению); закон рецикла грамматик распространён на
h0/h8; `--no-h`/`--no-h8` — честные пропуски. Протокольный хвост —
единственная правка протокола (закон m3).

**НОВОЕ 2 — RU-0.4 (M2, русская сторона):** ТЕ ЖЕ 12 строк, сборка на
пороге 0.4. Роутер побайтово воспроизводим (det m4) — свежие
systemone-ответы совпадают с полосой 0.5, порог ЕДИНСТВЕННАЯ
переменная; сборка строк, что 0.5 блокировал, становится измеримой
(честный пробел m4: у заблокированных нет action_top3).
`assemble_intent` получил параметр `gate` (дефолт 0.5 — записанный
дефолт владельца; 0.4 — измеренная iter-361 точка возврата).

**НОВОЕ 3 — ЦЕНЗА ЛОЖНЫХ РАЗРЕШЕНИЙ** (слова владельца: «прирост
принятых запросов сам по себе не доказывает, что система надёжнее»):
`false_allow_class` — чистая функция над (сборка, гейт, золото),
непересекающиеся классы: `correct_allow` (kind И объект совпадают),
`false_allow_kind` (не то действие прошло гейт),
`false_allow_object` (kind тот, закоммичен ДРУГОЙ объект — включая
форму ru_05: золото-текстура закоммичена канон-таргетом),
`false_allow_nonintent` (золото «нет действия» — гейт пропустил
действие; самый тяжёлый класс), `blocked` (гейт отказал — вне счёта
цены; для intent-золот пропуск, для non-intent честный отказ),
`pass_no_action` (невозможно по построению — записано, не выброшено).
Расхождения полей-значений (ticks/method) остаются СВОИМ классом
ценза — никогда не маскируются ни в победу, ни в ложное разрешение.
Сравнение объектов: канон-таргет по id, текстура по slot — ru_05
(золото slot:candles, сборка oil_lamp_01) = false_allow_object,
ровно класс, который m4 назвал бы no_pin-победой прироста.

**НОВОЕ 4 — R04 (M2, английская сторона):** механизм строки,
расширенный на полный корпус — цена ручки измерена там же, где её
польза (sweep 87.1%@0.4 живёт на этом корпусе). Честное расширение
внутри машины строки: +42 router-вызова на станции (~24 с на GPU),
та же ценза ложных разрешений на каждом прошедшем гейт цикле.
Граница sạchо отмечена: RU-0.4 — требование строки; R04 — его
английская половина, выключается `--stages` без r04.

**Прочее:** det-мини + юниты g/h с дайджестами (закрывает
инструментальный пробел iter-361 «det g-digest пуст» одной строкой
на руку); закон соседних паков в `_exe_candidates` — движок
llama.cpp/ из папки m4-пака, лежащей РЯДОМ, находится без докачки
(650 МБ экономии на станции; сетап остаётся честным фолбэком);
STAGES = preflight → reference → r → g → h → ru → ru04 → r04 → det →
package; префиксы m5_/_run-dir/возобновление/always-a-zip — законы m4
пословно.

## B. Живая валидация CPU (полная, §13.1-класс)

Билд b11541 ubuntu-x64 + Laya-Q8_0 (роутер) + Qwen3-0.6B (главная).
Юниты 9/9 (census / вопросы+сборка / RU-форма / **гибридная
грамматика** / **цензa ложных разрешений** / **ручка 0.4** / закон
батча / эскалация 400 / VRAM-звено). Смоук зелёный. **Полный корпус
(10 юнитов / 42 цикла на руку) в 3 бюджетных чанка + упаковка —
машина возобновления валидирована живьём; хил-лестница сработала
живьём один раз (engine failure → restart 1 → прогон продолжен).**

**ПАРИТЕТ С m4 (база пословна — доказана):** R full=6 (14.3%) — ровно
строка m4-валидации; G ценз ПОБАЙТОВО идентичен m4-валидации
(full=4, kind=15, target=10, no_pin=2, not_intent=11); RU@0.5 12
строк — идентичны классы; стены в той же полосе (R med 3.25 c
против 3.30 c, G med 4.58 c против 5.01 c).

**H-рука живьём (84 гибридных цикла):** h0 full=3 / kind+=8; h8
full=3 / kind+=11; ДВЕРЬ приняла каждую JSON-голову через тот же
шлюз, что у G. **Закон терминированной прозы:** h8 41/42 finish=stop
(1 length), h0 34/42 (8 length — жадные петли temp-0 на 0.6B:
повторительные аттракторы «The verdict is that…», грамматика
позволяет продолжать строки; на H8 петель нет) — ЧЕСТНО записано
флагом eos_held per-record, НЕ чинится сэмплером (ломало бы
сравнимость с G; станция снимет свою картину на Gemma-4-E4B).
Стены: h0 med 8.87 c / h8 med 6.86 c против G 4.58 c на том же
спавне (цена проза-хвоста на CPU). json_bleed 1/42 пойман живьём
(проза процитировала документацию поля texture — `{"entry",
"scope"…`), protocol_echo 0/84.

**РУЧКА 0.4 живьём:** RU-0.4 снят (на Laya полоса 0.4–0.5 пуста —
классы @0.4 == @0.5; восстановление покажет Kev-4B станции, его
0.38–0.49 из iter-361); ценза атрибутирована корректно на каждом
классе (RU на Laya: 6 kind + 1 object + 1 nonintent = 8 ложных
против 0 правильных — EN-чекпоинт на кириллице уверенно неверен,
честный датум полосы, не дефект машины). R04: 9 ложных / 2
правильных, ОДНА строка восстановлена на 0.4 неправильным kind —
цена ручки видна в данных.

**det:** роутер identical=True digest `b448cdfe4c14ff41`; g
identical=True digest `30511b5b95a171f7` (пробел iter-361 закрыт);
**h identical=False** (finish length/stop на двух одинаковых вызовах
temp 0 — движковая недетерминированность ситтинга b11541+0.6B с
грамматикой; честно записано финишами, станция даст свой вердикт на
Gemma+GPU — дет-мини фиксирует ситтинг, закон m2).

## C. Дефекты, найденные валидацией (все закрыты в итерации)

1. `run_preflight` не получал `args` (NameError на `h_arms`) —
   передача добавлена; RED→GREEN (краш воспроизведён, всегда-a-zip
   при этом упаковал диагностический зип — закон жив);
2. таблица M3: строка стен шла по неверному ключу («?» вместо стен)
   — диспетч ключей исправлен;
3. отображение P в цензах: 2 знака путали (0.40 при блоке на 0.4) —
   3 знака;
4. det-h: чтение call-документа упрощено на возвращаемый emit_call
   путь.

## D. Что НЕ сделано (честно)

- **СТАНЦИОННЫЕ ПРОГОНЫ — за владельцем** (RTX 3080 Ti / 32 ГБ;
  сэндбокс без GPU): двойной клик station_m5_probe.bat, промты
  моделей (Kev-4B роутер, Gemma-4-E4B главная), прислать m5_*.zip.
  Ожидание ~10–20 мин (H генерирует прозу — самая долгая часть);
- качество прозы на ультралайте телеграфное — эстетика читается
  только на станции (как в m3); дословные образцы едут в jsonl;
- решения M2/M3 — за владельцем (пак даёт материал, не решение);
- formalized band-sweep (`cuda_gate.bands`) — инструментальная
  строка m4, не тронута.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` (3.12.15 сэндбокса) —
  2622 passed + 27 failed + 1 skipped: все 27 — известный T1
  log-header набор (байт-идентичен записи iter-362/363), на золотом
  3.12.14 сюит зелёный (2649+1, закрытие iter-363); райдеры-only,
  код репо не тронут;
- `ruff check .` — clean (ruff 0.17.0); `python scripts/docguard.py`
  — clean; `python scripts/topology.py --check` — clean;
  `python scripts/digest.py` — парсит;
- пак: юниты 9/9, регрессия флагов (все флаги на месте, --stages с
  неизвестным именем — громкий отказ), полный CPU-прогон всех
  стадий end-to-end, упаковка m5_sandbox_full_validation.zip
  (664 401 Б — внутри все jsonl стадий + m5_report.txt + логи);
- самопроверка дельты: список путей == `git status --porcelain
  -uall` против базы (блок Git ниже);
- INV-1..5 не тронуты (R0/R1 райдеры, нулевой код репо).

Замечание о док-лупе (AGENTS §2.5, превентивно): пятая
riders-only итерация подряд подряд в станции серии — не
документ-чёрч: функциональный прогресс — инструмент + валидированное
измерение (новая рука + новая стадия + ценза, полный живой прогон с
доказанным паритетом), Riders-only дифф репо — конструкция самой
строки (Rule 9).

## F. Риски

- H-рука на станции зависит от Gemma-4-E4B: если temp-0 даст петли —
  это ИЗМЕРЯЕТСЯ (eos_held), не чинится молча; H8 —
  производственная форма;
- дет-h на станции может показать свою картину (дет фиксирует
  ситтинг);
- R04/ru04 мерят сборку на новом пороге; события мира могут
  расходиться с 0.5-прогонами после первого коммита — цензы идут
  против золота, не против соседнего прогона (построение);
- движок соседнего пака ищется globo'm `canonsim_m*_station_pack*`
  — имя папки пака при распаковке менять нельзя (README предупреждает).

## G. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-365-m5station-report.md
git status --short
git commit -m "iter-365-m5station: THE M5 STATION PACK delivered + validated (the m5-station row's precondition MET - the owner's m4 pack zip arrived; the m4 v4.3 base VERBATIM per Rule 9): THE H ARM ON THE SAME m4 CORPUS AT LAST (the hybrid single-pass, the m3 form - ONE call carries the verdict AND the prose: the repo's own reply grammar wrapped as root ::= verdict-doc '\n\n' prose with the TERMINATED-PROSE law iter-351 D.1 - the body without empty lines + the blank terminator lets root complete and EOS fire naturally; the door splits at the FIRST blank line: the JSON head through the SAME gate as G (byte-comparable census), the prose tail the recorded surface (length/json_bleed/protocol_echo/eos_held, verbatim in jsonl); H0 temp 0 + H8 temp 0.8-seeded, both on the SAME main spawn as G - the latency like-for-like by construction) + THE RU-0.4 STAGE (the M2 knob's Russian half: the same 12 rows assembled at gate 0.4, the router byte-reproducible so the gate is the ONLY changed variable; the rows 0.5 blocked become measurable) + THE FALSE-ALLOW CENSUS (the owner's recorded call - the growth of accepted requests does not by itself prove reliability: false_allow_kind / false_allow_object (incl. the ru_05 texture-gold-committed-as-target shape) / false_allow_nonintent, field-value divergences never laundered into either side) + R04 (the same machinery on the English corpus - the knob's cost measured where its 87.1%@0.4 benefit was measured) + the det g/h digest lines (the iter-361 instrument gap) + the sibling-pack engine law (the m4 pack's llama.cpp found beside, no 650 MB re-download). VALIDATED LIVE CPU-SIDE FULL CORPUS (b11541 + Laya + Qwen3-0.6B: units 9/9, all stages end-to-end in 3 resume chunks, the heal ladder fired live, THE M4 PARITY PROVEN - R full=6/14.3% exactly the m4 validation row, G census byte-identical, RU classes identical; the H arms: 84 hybrid cycles through the REAL door, the terminated-prose law HELD (h8 41/42 finish=stop; h0 34/42 - the temp-0 greedy repetition loops on a 0.6B honestly recorded as eos_held, never patched with a sampler change that would break G-comparability); the 0.4 knob live (RU-0.4 taken, Laya's 0.4-0.5 band empty - the recovery is Kev's station question; the false-allow classes attributed correctly on every row); det router/g identical=True with digests, h identical=False (the engine-side sitting datum, finishes recorded); four instrument defects found and closed by the validation); THE STATION RUNS ride the owner (double-click station_m5_probe.bat, ~10-20 min, send the m5_*.zip back); pytest 2622+27(known T1 3.12.15 set)+1, ruff+docguard+topology+digest clean; R0/R1 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## H. Доставка (§12.2 — оба канала)

- **Дельта-архив** (вложение): `canonsim_iter-365-m5station_
  2026-10-11.zip` против BASE_COMMIT `709d355fb24caaf87280df7970794
  9344249a7f0` — STATUS.md, worklog.md, docs/TASKS.md,
  docs/iterations/iter-365-m5station-report.md, BASE_COMMIT.txt,
  DELETED_PATHS.txt (`None`);
- **Пак M5** (вложение, вне репо — Правило 9):
  `canonsim_m5_station_pack_v5.0.zip`, 70 135 Б, md5
  `f7fec7224f855c4ef7cd0bd82183085d`; зип полного CPU-прогона
  валидации `m5_sandbox_full_validation.zip` (664 401 Б) едет
  приложением к отчёту сессии — сверка станции с сэндбоксом;
- tmpfiles-ссылки — в финальном сообщении.

**Done:** строка m5-station выполнена в части агента: пак M5 v5.0
построен на базе v4.3 пословно (H-рука с законом терминированной
прозы + RU-0.4 + ценза ложных разрешений + R04 + дайджесты det +
закон соседних паков), юниты 9/9, полный живой CPU-прогон всех
стадий с доказанным паритетом m4 (R/G/RU байт-в-байт), четыре
дефекта инструмента найдены и закрыты валидацией; райдеры прошли
ruff + docguard + topology + digest; T1-оговорка процитирована
честно (27 известных, золотой интерпретатор зелёный).
**Not done:** станционные прогоны (владелец: двойной клик, промты
Kev/Gemma, прислать m5_*.zip); решения M2/M3 за гейтом
runtime-promotion; качество прозы читается только станцией.
**Next:** станционный прогон M5 владельцем → чтение отчёта
(M3-таблица решения + цензы 0.4 обеих полос) → решения M2/M3;
параллельно стоящие вызовы — строка оптимизации бит-семейства
(decay_walk ×11.76, сильнейший кандидат ранжирования iter-364),
replay-UI NOT-EXPOSED, W8, P1/P2/P3, lab-composite-1.
**Active KIs:** KI#113 (test_lab, как в STATUS).
