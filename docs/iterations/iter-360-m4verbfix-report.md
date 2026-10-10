# iter-360 · m4verbfix — краш drop_break починен: у Verb нет атрибута name (одна строка, c.name → c.intent); оба твоих прогона v4.2 умерли на ней, и «аномалия s4» из iter-358 закрыта настоящей причиной — тот же краш; RED-воспроизведение 1:1 + GREEN-доказательство насквозь (fire cascade дрейнирует) в сэндбоксе

**Владелец прислал:** два диагностических зипа упавших прогонов
v4.2 — `m4_20261010_150710.zip` (87 759 Б) и `m4_20261010_150805.zip`
(89 377 Б) — оба вызова (`--g --ru --det --full-corpus` и
`--full-corpus`) прошли флаги (фикс iter-359 работает), подняли обе
модели (Kev-4B роутер + Gemma-4-E4B главная, FULL offload), прогнали
preflight + reference (10/10 юнитов) + R-руку s1..s3 — и умерли
ОДНОЙ ошибкой на s4:

```
AttributeError: 'Verb' object has no attribute 'name'
  station_m4_probe.py, line 1131, in assemble_intent
    if c.name == kind:
```

Явный ввод сессии (D-198): пункт STATUS Next — «THE OWNER'S RERUN
WITH v4.2» — ВЫПОЛНЕН владельцем, оба зипа получены; «продолжай
работы… я разрешаю» даёт право ввести итерацию чтения + фикса.

**Класс риска:** R2 (локальная правка паковочного скрипта, вне репо
по Rule 9 / D-046 — нулевой код репо, INV-1..5 не тронуты). Изменение
поведения ровно одно: раньше любой live-выбор drop_break убивал
скрипт; теперь ветка читает правильный атрибут и собирает документ
(фиксированная политика полей — near = первое место двора, класс
census=fields, расходимость честно считается).

**BASE_COMMIT:** `d94d1cc6ebc659fe56f885ded984c326e5f3cd7f` (HEAD
двинулся — владелец закоммитил райдеры iter-358+359 одним коммитом;
iter-360 сидит на новом HEAD).

## A. Первопричина — одна строка, жившая с рождения пака

Спец-ветка поля `near` для drop_break (строки 1128–1135
`station_m4_probe.py`, фиксированная политика полей R-формы: дефолт
`near` = «первое огнеопасное место позиции» — в отличие от
wait/ticks и steal/method, у near нет константы, значение derives
из грамматики) перебирает `snapshot.verbs` и сравнивает… `c.name`.
У датакласса `Verb` (`brief/parser.py`, строки 153–162) поле
называется **`intent`**: `intent, label, target_required, fields` —
и называлось так С МОМЕНТА СОЗДАНИЯ в iter-31 (проверено по git:
`git show 718d079:brief/parser.py` — `name` у Verb не было никогда).
`c.fields`/`fc.name`/`fc.values` в той же ветке корректны
(`FieldConstraint.name/.values` существуют) — баг ровно один,
подтверждено полным сканом атрибутных доступов по скрипту.

## B. Почему стреляло только теперь — и что это закрывает задним числом

Ветка исполняется ТОЛЬКО когда живой роутер выбирает `drop_break`
верхним действием. До прогона владельца это не случалось НИ РАЗУ:
в CPU-валидации iter-357 Laya ни разу не выбрала drop_break (42
документа — все take/talk/steal/move/wait/look_around). Твой
v4.1-прогон (140427) выбрал — и умер: «аномалия упаковки s4» из
iter-358 §F (2 reply + 3 parse, нет end-события) — ЭТОТ ЖЕ КРАШ,
сигнатуры совпадают один в один, включая третий парс «I smash the
lamp down against the woodpile». Доказательство детерминизма: оба
v4.2-прогона побайтово идентичны в собранных документах, census,
gate_p и input-токенах (см. §C) — роутер ВСЕГДА выбирает drop_break
на этом цикле, значит v4.1 умер той же строкой. Уточняю честно: моя
формулировка в v4.2 «это НЕ баг скрипта — Ctrl-C/окно/бюджет» была
НЕПРАВИЛЬНОЙ; в README_RU v4.3 записано извинение и исправление.

## C. Что упавшие прогоны всё равно дали (полезный вынос — данные целы)

Оба зипа несут полный preflight + reference 10/10 + R-рука s1..s3
(12 say-циклов в каждом), и это НЕ повторы — это новые датаумы:

1. **КРОСС-ПРОГОНОВАЯ ВОСПРОИЗВОДИМОСТЬ R-РУКИ:** run 150710 ≡
   run 150805 побайтово — assembled docs, census (s1: full 4 /
   gate_blocked 2 / gate_fp 1; s2: kind 1 / not_intent 1 /
   gate_blocked 1; s3: full 2), gate_p (одни и те же 12 значений:
   0.7082, 0.4605, …, 0.7091), input-токены (1259, 1515, 1539,
   1579, 1539, 1555, 1531, …) — различаются только wall-времена
   (0.597 vs 0.561 и т.п.). И их census ПОБАЙТОВО совпадает с
   v4.1-прогоном (full 6, kind 1, gate_blocked 3, gate_fp 1,
   not_intent 1 из iter-358 §D). ТРИ прогона, одна машина, одна
   модель — R-рука на Kev-4B воспроизводима до байта (расширяет
   кросс-рановый датаум iter-314 на R-форму станции).
2. **24 новых доказательства R-формы:** 0 изобретений на 24
   собранных документах (12 × 2) + output_tokens=[0] на каждом
   вызове — теперь 36 live-документов суммарно с v4.1 (0/36).
3. **Латентность подтверждена:** med 0.519 s / min 0.508 / max
   0.730 / mean 0.575 (n=12; паттерн прогрева: первые циклы
   0.60–0.73, потом устойчиво ~0.51) — против 3.30 s CPU iter-357.
4. **Gate sweep стабилен:** gate>=0.5 → 66.7% (6/9), gate>=0.4 →
   100% (9/9) — те же числа, что в v4.1-прогоне (ручка
   подтверждена вторым прогоном).
5. Reference-корпус 10/10, вердикты доктора по 6 моделям,
   cuda_gate с FULL offload планом — всё на месте, докатке не
   нужно перегонять.

## D. Фикс (минимальный, без изменения дизайна)

`station_m4_probe.py`: `c.name == kind` → `c.intent == kind`
(+ комментарий с датой и причиной). PACK_VERSION → `v4.3 (iter-360:
the Verb attribute fix — …)`. Файл 98 582 → 99 199 Б. README_RU.txt:
заголовок v4.3; секция «ДОБАВЛЕНО В v4.3» (что случилось, почему,
доказательство); ПЕРЕПИСАНА секция про обрыв s4 (честное
исправление моей ошибки v4.2 + доказательство тремя прогонами);
докатка-рецепт обновлён: `--run-dir m4_20261010_150805` (R
доиграет s4..s10 — упавший юнит перезапустится чисто, s1..s3
пропустятся как done; затем G, RU, det, package). Остальные 8
файлов пака не тронуты.

## E. RED/GREEN доказательство в сэндбокке (настоящие двери репо)

Воспроизводящий скрипт (сэндбокс, вне репо по Rule 9): поднимает
РЕАЛЬНУЮ батарею — Simulator + Mediator + ParserDoor на общем
SceneLedger, юнит s4_fire_chain (seed 8, setup move loc_tavern),
пять say-циклов; роутер заменён скриптованными ответами ТОЙ ЖЕ
формы, что возвращал Kev живьём (take/move из твоего прогона,
затем drop_break) — всё остальное (build_state, build_questions,
assemble_intent, invention_check, настоящая ParserDoor, census)
исполняется дословно.

- **RED (нетронутый v4.2):** циклы 0–1 проходят (take oil_lamp_01
  census=full, move loc_backyard census=full — ровно как в твоём
  прогоне), цикл 2 умирает `AttributeError: 'Verb' object has no
  attribute 'name'` — воспроизведение 1:1.
- **GREEN (v4.3):** все 5 циклов: take full → move full →
  **drop_break census=fields** (near=back_wall — первое место
  двора по фиксированной политике; золото ждёт woodpile —
  расходимость УЧТЕНА классом fields, это задокументированная
  честная цена R-формы, не баг; G-рука сгенерирует woodpile
  правильно) → **fire cascade дрейнирует внутри двери: drop_break
  → fire_started → fire_spread → smoke_rising →
  location_burned_out** (ровно expect корпуса: 5 событий) → flee
  full (коммит) → arson full → дверь честно отвечает
  intent_rejected (expect корпуса). Изобретения 0 на всех пяти.
- **Регрессия флагов v4.2 — 7/7:** --help (epilog на месте),
  --g --ru --det, --full-corpus, все четыре, --xyz → чёткое
  «unrecognized», --stages r,foo → громкий отказ со списком,
  --stages ru,det → принято. Ни один вызов не изменился.
- **Самодостаточность архива:** GREEN повторён из РАСПАКОВАННОГО
  7z — архив несёт фикс.

## F. Пак v4.3

10 файлов под `canonsim_m4_station_pack/` (тот же верхний уровень):
station_m4_probe.py v4.3 (99 199 Б) + README_RU.txt (21 471 Б)
изменены; m4_analysis.py, m4_units.py, sandbox_report.txt,
station_m4_doctor.{bat,py}, station_m4_probe.bat,
station_m4_setup.{bat,py} — нетронуты (те же, что v4.2). Размер
50 211 Б, md5 `270018c458a436a2c344528b6aa31444`. Runtime-мусор
(папки прогонов от смоука) исключён — чистые инструменты.

## G. Тебе делать (докатка — самое дешёвое)

1. Распакуй `canonsim_m4_station_pack_v4.3.7z` ПОВЕРХ текущего
   пака (структура та же);
2. **Докатка:** `station_m4_probe.bat --run-dir m4_20261010_150805`
   — preflight/reference пропустятся (done), R-рука доиграет
   s4..s10 (s1..s3 уже done, s4 перезапустится чисто), затем
   G-рука на Gemma-4-E4B, RU-полоса (12 строк — главный вопрос
   доверия Kev), det-мини, package. Промты моделей — как обычно;
3. ИЛИ свежий прогон: просто `station_m4_probe.bat` (без флагов)
   — то же самое, только R-рука перегонит s1..s3 (~15 с на GPU);
4. m4_*.zip обратно — закрывает RU-полосу + G-контроль + det,
   затем решения M2/M3 за гейтом runtime-promotion.

## H. Верификация

- RED/GREEN/флаги/архив — §E, все зелёные;
- `python scripts/docguard.py` — clean; `python scripts/topology.py
  --check` — clean (нулевая дельта кода репо); `python
  scripts/digest.py` — парсит (заголовок iter-360 в STATUS.md);
- `PYTHONHASHSEED=0 python -m pytest -q` — 2616 passed + 28 failed
  + 1 skipped: все 28 — известные T1 byte-identical сбои на
  `python`-строке log-header (3.12.15 sandbox vs 3.12.14 golden),
  воспроизведённые 1:1 на чистом клоне ещё в iter-358 —
  riders-only, код репо не тронут;
- INV-1..5 не тронуты (R2, паковый скрипт вне репо, нулевой код).

## I. Что это значит для долгосрочного трека

Краш был НЕ в архитектуре R-формы — ни один инвариант не задет:
собранные документы всех трёх прогонов так и остались без единого
изобретения, дверь продолжала бы коммитить по канону. Это был
инструментальный долг пака (never-exercised ветка), закрытый тем
самым методом, который уже стал законом серии: воспроизведи красным
в сэндбокке ДО отправки владельцу (урок iter-353 «strict mock
воспроизвёл 400 1:1 ДО фикса» — теперь расширен: воспроизводи не
только транспорт, но и never-exercised ветки кода на реальных
данных владельца). Датаум детерминизма (§C.1) — самостоятельная
ценность: R-рука на Kev-4B побайтово воспроизводима, а значит
RU-полосу можно будет доверять как измерению, а не как выборке.

## J. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-360-m4verbfix-report.md
git status --short
git commit -m "iter-360-m4verbfix: THE VERB ATTRIBUTE FIX - both v4.2 station runs (m4_20261010_150710/150805) died one error deep in arm r s4_fire_chain: AttributeError 'Verb' object has no attribute 'name' at station_m4_probe.py:1131 - the drop_break/near special case (the fixed field policy's position-derived branch) read c.name on brief/parser.py's Verb dataclass whose field is intent (since iter-31, never name; c.fields/fc.name/fc.values in the same branch are correct - one bug, confirmed by a full attribute scan). The branch executes ONLY when a live router picks drop_break top - never happened before (CPU Laya validation never picked it), which RETROACTIVELY EXPLAINS iter-358's 's4 packaging anomaly': the v4.1 run died the same line (identical artifact signature 2 replies + 3 parses + no end-event; the router is deterministic - both v4.2 runs are byte-identical in assembled docs/census/gate_p/itok, and their census matches the v4.1 run exactly - THREE runs, one byte pattern; my v4.2 README claim 'NOT a script bug' honestly retracted). THE CRASHED RUNS STILL DELIVERED: cross-run reproducibility of the R-arm on Kev-4B (byte-identical across runs, extends iter-314's datum), 24 more invention-free docs (0/36 live total with v4.1), output_tokens=[0] x24, latency re-confirmed med 0.519 s (warmup 0.60-0.73 then ~0.51 steady), gate sweep re-confirmed 66.7%@0.5 / 100%@0.4, reference 10/10 + doctor verdicts + cuda_gate FULL-offload plan all intact - the docatka needs no rerun of what is done. THE FIX: one line c.name -> c.intent + PACK_VERSION v4.3 + README (the v4.3 section, the honest s4 correction, the docatka recipe --run-dir m4_20261010_150805). PROVEN in sandbox on the REAL repo doors: RED - pristine v4.2 dies the exact AttributeError at s4 cycle 2 (1:1 with the owner's crash); GREEN - v4.3 runs all five s4 cycles: take/move full, drop_break census=fields (near=back_wall the fixed-policy default vs gold woodpile - the counted honest divergence, the designed cost), the fire cascade drains inside the door (drop_break -> fire_started -> fire_spread -> smoke_rising -> location_burned_out, exactly the corpus expect), flee commits, arson lands intent_rejected, inventions 0 everywhere; flag regression 7/7; GREEN re-run from the extracted 7z (the archive carries the fix). Pack v4.3: 10 files, 50 211 bytes, md5 270018c458a436a2c344528b6aa31444, outside the repo per Rule 9. KI#117 opened+closed in-iteration. R2 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## K. Доставка (§12.2 — оба канала)

- **Пак v4.3** (вложение): `canonsim_m4_station_pack_v4.3.7z`
  сохранён в сессии — едет через чат как вложение; tmpfiles-ссылка
  и md5 (`270018c458a436a2c344528b6aa31444`, 50 211 Б) — в
  финальном сообщении;
- **Дельта-архив** (вложение): `canonsim_iter-360-m4verbfix_
  2026-10-11.zip` против BASE_COMMIT `d94d1cc` — STATUS.md,
  worklog.md, docs/TASKS.md, docs/iterations/iter-360-m4verbfix-
  report.md, BASE_COMMIT.txt, DELETED_PATHS.txt (`None`); md5 и
  ссылка — в финальном сообщении.

**Done:** первопричина краша найдена и закрыта одной строкой
(c.name → c.intent); RED-воспроизведение 1:1 + GREEN-доказательство
s4 насквозь (fire cascade, flee, arson-rejected, 0 изобретений) +
регрессия флагов 7/7 + проверка из распакованного архива; «аномалия
s4» iter-358 закрыта настоящей причиной (тот же краш, три прогона
одной сигнатуры); пак v4.3 собран (10 файлов, 50 211 Б, md5
270018c458a436a2c344528b6aa31444); KI#117 открыт и закрыт в
итерации; райдеры прошли docguard + topology + digest; из упавших
прогонов извлечены новые датаумы (кросс-рановая воспроизводимость
R-руки, 0/36 изобретений, латентность, gate sweep).
**Not done:** полная батарея (G-рука, RU-полоса, det, band sweep) —
за владельцем: докатка `--run-dir m4_20261010_150805` (или свежий
прогон) с паком v4.3.
**Next:** чтение вернувшегося m4_*.zip (RU-полоса на Kev —
заголовочный вопрос доверия; G-контроль на Gemma-4-E4B; det);
затем решения M2 (block/downgrade/allow + C-tight/C-full) и M3
(H/G2/F/R) за гейтом runtime-promotion.
**Active KIs:** KI#113 (test_lab, как в STATUS); KI#117 CLOSED
iter-360 (открыт и закрыт в этой итерации).
