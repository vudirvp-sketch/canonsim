# iter-368 — m6promotion: THE R-PROMOTION — THE M6 STATION PACK v6.0 (R AT THE DOOR + THE L12 TEMPLATE RUNG) + THE BAND FINDING (KI#119) + THE M5 ZIP ARCHIVED IN THE REPO

**Task ID:** iter-368-m6promotion · **Дата:** 2026-10-11 ·
**Класс:** R0/R1 riders-only + R2 (пак-инструмент вне репо, Правило 9;
в репо — только райдеры и архив) · **BASE_COMMIT:**
`7c9c654113d54a31efee9109000ead72c097a1ee` (iter-367).

## A. Что сделано (в двух словах)

Приказ владельца «разрешаю promotion R» (2026-10-11, сессия
continuation) ИСПОЛНЕН: решение D-250 M3 получило свой рантайм —
**THE M6 STATION PACK v6.0**, пак продвижения. Батарея по умолчанию
ТЕПЕРЬ САМА ПРОДАКШН-ФОРМА: R у двери (роутер = оператор
вердикт-пути, гейт профиля `--gate 0.5|0.4` по D-250 M2) + **narrate
— НОВАЯ СТАДИЯ, L12-ШАБЛОН** (проза как ОТДЕЛЬНАЯ поверхность:
каждый лог R-юнита через `render/chronicle.py`, каждый тейл
рендерится дважды с дайджестом — доказательство детерминированности
L12-звена вживую; золотые юниты рендерятся рядом) + G-якорь + RU +
det. H исключён из дефолта НАВСЕГДА (`--stages h` — опциональный
инструмент эстетического вызова), ru04/r04 убраны (ручка `--gate`
заменила стадии измерения). ЦЕНЗА ЛОЖНЫХ РАЗРЕШЕНИЙ повышена до
ПОСТОЯННОГО СТРАЖА: каждая прошедшая гейт строка R и RU (на любом
профиле) сверена с золотом. Пак валидирован живьём на полном корпусе
(b11541 ubuntu + Laya + Qwen3-0.6B): **все стадии зелёные,
ПАРИТЕТ m4/m5 воспроизведён точно** (R full=6/14.3% — ровно строка
m4-валидации; классы G и RU идентичны), **narrate 20/20
детерминирован**, det identical, resume-машина зелёная. Параллельно
НАЙДЕН И ЗАКРЫТ ИНСТРУМЕНТОМ серьёзный дефект серии — **KI#119, БЕНД
m5-прогона: логи обоих серверов владельца несут НОЛЬ строк CUDA**
(см. §C), и записан честный дейтум о референсе — **KI#120** (§D).
По прямому указанию владельца **m5-зип заархивирован в репо**
(`docs/station/archive/`), вместе с m6-зипом — исходник станции при
каждом будущем клоне (§F).

## B. Устройство батареи v6.0 (дельта над m5 v5.0, руки r/g/ru пословно)

1. **STAGES = (preflight, reference, r, g, ru, narrate, det,
   package)** — дефолт ЭТО продакшн-форма D-250 M3. OPT_IN_STAGES =
   ("h",): гибридные половины (h0+h8) запускаются ТОЛЬКО явным
   `--stages h` (H не продвинут; эстетический вызов открыт);
   `--no-h`/`--no-h8` стали no-op (m5-мышечная память, не ошибка).
   ru04/r04 СТАДИИ УДАЛЕНЫ: их роль измерения выполнена (решение
   M2 записано в D-250), форма развёртывания — ручка `--gate`.
2. **--gate 0.5|0.4** — ПРОФИЛЬ (choices ровно два значения, отказ
   громкий на любое иное): 0.5 дефолт; 0.4 явный recall-oriented
   deployment override, НИКОГДА «более надёжный режим» — цена D-250
   дословно в help и в отчёте (EN correct 15→20, blocked_miss 10→4,
   nonintent 4→7, precision 60.0→58.8%; разделяющего порога нет).
   Гейт применяется к r-руке и RU-полосе; `gate.json` несёт
   `profile_gate`.
3. **narrate — L12-ШАБЛОН** (главное новое): `RepoNS` импортирует
   `render.chronicle.chronicle_from_log`; стадия рендерит каждый
   `arm_r/<case>/run.jsonl` и каждый золотой
   `reference/<case>/run.jsonl`; тейл рендерится ДВАЖДЫ — дайджесты
   (sha256-16) сравниваются; полный текст пишется в
   `narrate/<tag>_<case>.txt`; записи в narrate.jsonl: строки, знаки,
   дайджест, флаг детерминированности, head/tail-строки. Рендер НЕ
   пишет в лог (INV-1) — проверено юнит-тестом (md5 лога до/после).
4. **СТОЯЩИЙ СТРАЖ**: overlay `rec["fa"] = false_allow_class(...)` —
   в m5 он был только у r04/ru04-стадий; теперь на КАЖДОЙ строке r
   (42) и ru (12) на любом профиле. m6_analysis выводит обе цензы
   (EN/RU) как «THE STANDING WATCH».
5. **БЕНД-ПРИБОР (KI#119)**: `DeviceGate.observe` теперь записывает
   и НЕГАТИВНЫЙ вердикт («cpu (no ggml_cuda_init in log)» — лог без
   строк CUDA = бенд CPU по доказательству, молчание больше
   невозможно); `finalize()` в finally-блоке перечитывает оба лога,
   печатает ГРОМКИЙ вердикт в конце прогона, cuda_gate.json
   перезаписывается финально (в m5 писался один раз до старта);
   `doc()` несёт `band_note` с объяснением; отчёт — строку бенда с
   выводом. Дедупликация имён: один канонический ключ на лог
   (`_log_names`), «router»/«main» не дублируют имена моделей.
6. **m6_analysis.py**: отчёт переименован в THE PROMOTION PACK
   REPORT — шапка с профилем и вердиктом бенда, THE PRODUCTION
   TABLE (R на профиле против G; H-колонки n/a в дефолте), секция
   NARRATE (N/N детерминированность, строки/знаки/дайджесты,
   head/tail-цитаты), цензы EN/RU как страж, H-секции помечены
   OPT-IN.
7. **README_RU.txt** переписан под v6.0: блок про бенд m5 (с
   рецептом починки — перезапустить setup, искать строку «CUDA
   runtime in place»), запуск, флаги, чтение отчёта, честные
   оговорки, включая запись об m5-зипе в репо. Батники — новые
   заголовки. Юнит-чеки m6_units.py: 12/12 (три новых —
   детерминированность narrate, форма дефолт-батареи, прибор бенда).

## C. KI#119 — БЕНД m5-прогона: логи несут НОЛЬ строк CUDA (открыт-закрыт этой итерацией)

Факт (воспроизведён по возвращённому владельцем zip, файлы
`m5_llama_main.log` 140 КБ и `m5_llama_router.log` 138 КБ):
`grep -ci "cuda|vram|nvml"` = **0 в обоих логах**; нет
`ggml_cuda_init`, нет offload-строк; `n_threads = 8` в обоих;
Gemma-4-E4B грузится за 3.1 с, Kev-4B за 2.9 с. Серверы владельца
**НИКОГДА не инициализировали CUDA-бэкенд** — m5-прогон шёл на
**CPU-бенде**, при этом `cuda_gate.bands` честно стоял `{}` весь
прогон (прибор молчал ровно там, где должен был кричать — тот же
класс, что KI#118: утверждение без инструментальной проверки).
Тайминги согласуются с CPU-полосой процессора владельца (prefill
4400 ток/с на 8 потоках для 4B-Q4; Kev 825 ток/префилл ≈ 0.52 с).

**Что снято/пересмотрено:** чтение iter-358 §D «GPU BAND OPENED BY
MEASUREMENT, ×6.3» и iter-361 «Kev-4B + Gemma-4-E4B FULL offload on
3080 Ti» — утверждения с предположением, не с прибора; бендовая
метка чисел латентности (0.52 с / 7.31 с) снята до «wall-times без
верифицированной метки бенда, консистентны с CPU-полосой станции»
(сами числа — настоящие измерения, не тронуты). **Что НЕ меняется:**
решения D-250 M2/M3 — сравнение R-vs-H шло like-for-like в ОДНОЙ
полосе одного спавна (бенд-независимо); выводы о лидерстве R по
full-rate/не-генеративности/воспроизводимости не опираются на метку
бенда. Механизм (гипотеза, валидируется следующим станционным
прогоном): `--list-devices` видит CUDA (драйвер), но спавн не
инициализирует бэкенд — вероятна неразрешённая загрузка
cudart64_12/cublas64_12/cublasLt64_12; сетап распаковывает компаньон
рядом с exe, но подтверждения строки «CUDA runtime in place» в
консоли владельца нет. Зуб: v6.0 прибора — вердикт ВЫВОДИТСЯ из
логов и произносится громко; рецепт починки в README. Следующий
прогон станции скажет свой бенд данными.

## D. KI#120 — референс никогда не коммитит закреплённые say-ответы (открыт, НЕ чинится в v6.0 — вызов владельца)

Найдено при валидации narrate: у золотого s4 лог = 6 событий
(setup-эпики + move), fire-цепочка ОТСУТСТВУЕТ, у r:s4 — 19 событий
с полной цепочкой (fire_started → fire_spread ×2 → smoke_rising →
location_burned_out). Причина воспроизведена напрямую:
`run_reference` (m4/m5-пословно, подтверждено diff) применяет
закреплённые ответы через `door.apply_reply` БЕЗ `door.emit_call`
— контракт двери «один вызов ждёт один ответ» отклоняет каждый
ParseError'ом, который глотает толерантный `except`. Следствие для
всей серии: референс-логи = только setup + narrator-биты;
premise-drift отпечатки мерили «рука сдвинула мир от нетронутой
premise», а НЕ «разошлась с золотой траекторией» (числа m5
R 27/42 / G 32/42 стоят как измеренные сырые наблюдения, их чтение
сужено честно); золотая траектория корпуса (например, s4-цепочка по
iter-360 GREEN) никогда не выполнялась в референсе. РЕШЕНИЕ НЕ
ПРИНЯТО В v6.0 осознанно: (а) закон сравнимости — руки m5-пословно,
паритет воспроизведён именно на неизменной машине; (б) фикс (добавить
emit_call в say-циклы референса) меняет смысл drift-колонки по всей
серии — это исключительный вызов владельца, не тихое исправление
(§11: никогда молча не сводить). KI#120 открыт в STATUS.

## E. Живая валидация (сэндбокс, b11541 ubuntu CPU + Laya-Q8_0 + Qwen3-0.6B-Q4_K_M, md5-пinned доктором)

- **Юниты 12/12**: 9 m5-пословно + 3 новых (narrate: тейл-в-тейл,
  md5 лога неизменен — INV-1; батарея по умолчанию: narrate в STAGES,
  h только в OPT_IN, ru04/r04 нет; прибор бенда: негативный вердикт
  записан, дубли имён исключены).
- **Смоук (2 юнита, все стадии)**: зелёный; narrate r:s1 дайджест ==
  gold:s1 (3243beeaca31fa97), r:s2 == gold:s2 — проза-поверхность
  like-for-like на смоук-корпусе; ценза-страж на каждой строке RU.
- **--stages h (опциональные половины)**: только h0+h8 выполняются,
  остальное честно «skipped (--stages)», пакет всегда.
- **--gate 0.4**: профиль записан в gate.json; полоса Laya
  0.4–0.5 пуста (RU-классы @0.4 == @0.5) — ровно ожидание m5
  («восстановление покажет Kev-4B на станции»).
- **ПОЛНЫЙ КОРПУС (10 юнитов / 42 say-цикла, один бюджетный чанк
  560 с)**: все стадии done, finished=True. **ПАРИТЕТ: R full=6
  (14.3%) — ровно строка m4/m5-валидации; G full=4, kind+ 16
  (38.1%), refusals 11 — побайтово цензус m4/m5; RU 12 строк:
  kind=6, blocked=3, fp=1, not_intent=1, target=1 — идентичны
  классы m4/m5.** Латентность: R systemone med 3.271 с, G parse med
  4.479 с, output_tokens=[0] ×42 (доказательство не-генеративности
  в каждой записи); вход med 841 ток. **narrate: 20/20 тейлов
  (10 R + 10 золотых), детерминированность 20/20**; r:s4 = 14 строк
  («Three Barrels tavern burns out…» — каскад в прозе), gold:s4 =
  6 (KI#120, §D — честное расхождение поверхности прозы). det:
  router identical=True, g identical=True. Бенд-вердикт вживую:
  «CPU band (no ggml_cuda_init in log)» — честная строка сэндбокса
  (CUDA не виден вовсе). Пакет: m6_*.zip всегда (304 676 байт
  полного прогона).
- **Resume**: повторный прогон с `--run-dir` — все стадии
  «done (resumed)», package done; машина возобновления m5-пословно
  зелёная.
- **Дефекты, найденные и закрытые валидацией**: (1) подпись run_arm
  с переносом стрелки возвращаемого типа (синтаксис); (2) дубли
  ключей бенда (модель + роль) — закрыто реестром лог→имя; (3)
  KI#120 найден (оставлен открытым — вызов владельца); (4) KI#119
  закрыт зубом прибора.

## F. m5-зип в репо — прямое указание владельца (запись закона)

Владелец: «вероятно стоит canonsim_m5_station_pack_v5.0.zip в
репозитории оставить, чтобы у тебя был исходник станции и ты мог с
ним работать». Исполнено: `docs/station/archive/
canonsim_m5_station_pack_v5.0.zip` (возврат владельца: инструменты +
его логи + отчёт сэндбокса; 102 671 байт, md5 8faedf1cd581abb8
a99449c4fcf8b205) и рядом `canonsim_m6_station_pack_v6.0.zip`
(чистые инструменты, 74 194 байта, md5 22da4f4087b859330a
555b736cbad679) — тот же паттерн, что docs/frontendweb/archive/ и
docs/worldbuild/archive/ (агентские паки тех дорожек живут в репо).
Конфликт с Правилом 9 («паки вне репо», D-046) разрешён ВЛАДЕЛЬЦЕМ
явной инструкцией — записано здесь, в worklog и строке TASKS, без
молчаливого сведения (§11). Замечание по INV-5: в m5-зипе лежат
ЛОГИ станции владельца — INV-5 governs собственные runtime-логи
репо (logs/, *.jsonl вне fixtures); возвращённый станционный прогон
— доказательные данные владельца, заархивированные по его прямой
инструкции под именем, которое он назвал. Рантайм-артефакты работы
m6 (run-папки, doctor.json, логи, __pycache__) в репо НЕ попали.

## G. Риски

- инструмент бенда закрывает НЕГАТИВ, но позитивный вердикт «cuda»
  на станции ещё не виден вживую (сэндбокс без CUDA) — юнит-тест
  покрыл форму, станция скажет факт;
- KI#120 открыт: drift-колонка следующего прогона будет читаться в
  старом смысле (от нетронутой premise) — до вызова владельца;
- профиль 0.4 мерился на Laya (пустая полоса 0.4–0.5): станционный
  Kev-4B даст свою картину — записано, не спекуляция;
- длинный m6-прогон на станции мог бы упереться в бюджет —
  машина чанков m5 наследуется, смоук и полный в один чанк здесь;
- m6-зип в репо = второй бинарный артефакт станции: рост ~176 КБ,
  паттерн archive-каталога уже существовал.

## H. Проверки

- pytest: 2621 passed + 28 failed (27 = известный T1-набор
  3.12.15-сэндбокса, байт-в-байт как в iter-362..367; golden 3.12.14
  полностью зелёный по iter-363) + 1 skipped; ПЛЮС
  test_guard_clean_on_the_real_repo красный НА ТОЙ ЖЕ строке D-250
  (31-я запись над капом — ожидаемое видимое состояние до коллапса,
  вызов владельца, KI-carry iter-367) — ноль новых;
- ruff clean; docguard: та же одна строка счёта DECISIONS
  (31/30, D-250) — ничего нового от этой итерации; topology clean;
  digest parses;
- самопроверка дельты: список путей == `git status --porcelain
  -uall` против BASE `7c9c654` (см. блок Git);
- INV-1..5 не тронуты (код репо нулевой; narrate-рендер
  INV-1-чист по юнит-тесту; архив — по §F).

## I. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-368-m6promotion-report.md docs/station/archive/canonsim_m5_station_pack_v5.0.zip docs/station/archive/canonsim_m6_station_pack_v6.0.zip
git status --short
git commit -m "iter-368-m6promotion: THE R-PROMOTION EXECUTED - the owner's permission + D-250 M3 -> THE M6 STATION PACK v6.0 (R AT THE DOOR: the default battery IS the production form; narrate = the L12 TEMPLATE RUNG as the prose surface, a SEPARATE surface per D-250 - every R unit's log through the repo's own chronicle renderer, each tale rendered twice with digests, the gold units beside; --gate 0.5|0.4 the profile knob per D-250 M2 with the measured cost verbatim; the false-allow census promoted to the STANDING WATCH on every R/RU row at any profile; H opt-in only via --stages h, never in the default - H not promoted, the aesthetic call open; ru04/r04 retired - the knob replaced the stages) + THE BAND FINDING KI#119 (the owner's m5 logs carry ZERO CUDA lines in BOTH server logs - no ggml_cuda_init, no offload, n_threads=8: the servers never initialized CUDA, the run was the CPU band while cuda_gate.bands honestly read {} - the GPU-band readings of iter-358 x6.3 and iter-361 FULL-offload WITHDRAWN as assumption-carried, the latency numbers stand as wall-times with the band label removed; the D-250 decisions unaffected - R-vs-H was like-for-like in one band; the v6.0 device gate DERIVES the band from the logs, records the negative verdict, says it LOUD at run end, rewrites cuda_gate.json finally) + KI#120 OPEN (the reference never commits the pinned say-replies: run_reference applies them without emit_call, the door's one-call-awaits-one-reply contract refuses each, the tolerant except swallows - the reference logs are setup+narrator only, the drift fingerprints measure pristine-premise divergence, never gold-path divergence; the fix is the owner's call, it changes the drift column series-wide) + the m5 zip archived IN the repo at docs/station/archive/ per the owner's explicit instruction (the station source for every future clone; Rule 9 yielded to the owner's direct call, recorded; the m6 zip beside it) - validated live full-corpus CPU-side (b11541+Laya+Qwen3-0.6B): ALL stages green, THE M4/M5 PARITY REPRODUCED EXACTLY (R full=6/14.3%, G byte-identical census, RU identical classes), narrate 20/20 deterministic, det identical, the band verdict live, the resume machine green, units 12/12; riders-only, zero repo code; pytest 2621+28(known T1)+1, ruff clean, docguard 1 line (the D-250 count, unchanged), topology clean, digest parses; INV-1..5 untouched"
git push
```

## J. Доставка (§12.2 — оба канала)

- **Дельта-архив** (вложение): `canonsim_iter-368-m6promotion_
  2026-10-11.zip` против BASE_COMMIT `7c9c654113d54a31efee9109
  00ead72c097a1ee` — STATUS.md, worklog.md, docs/TASKS.md,
  docs/iterations/iter-368-m6promotion-report.md,
  docs/station/archive/canonsim_m5_station_pack_v5.0.zip,
  docs/station/archive/canonsim_m6_station_pack_v6.0.zip,
  BASE_COMMIT.txt, DELETED_PATHS.txt (`None`);
- **Пак станции** (вложение, для двойного клика):
  `canonsim_m6_station_pack_v6.0.zip` (74 194 байта, md5
  22da4f4087b859330a555b736cbad679) — распаковать рядом с репо
  (или куда угодно — лестница найдёт);
- tmpfiles-ссылка, md5 и размеры — в финальном сообщении сессии.

**Done:** promotion R исполнен (M6 v6.0 собран и валидирован живьём
на полном корпусе, паритет m4/m5 точный, L12-звено доказано вживую);
KI#119 найден и закрыт прибором (бенд m5 = CPU по логам, чтения
сняты, зуб в паке); KI#120 открыт (референс не коммитит
закреплённые ответы — вызов владельца); m5-зип заархивирован в репо
по указанию; проверки пройдены.
**Not done:** станционный прогон m6 (владелец: двойной клик, вернуть
m6_*.zip + вердикт бенда из консоли); коллапс DECISIONS 31→30
(исключительный вызов); фикс KI#120 (меняет смысл drift-колонки);
эстетика H (опциональный вызов).
**Next:** станционный прогон m6 (вердикт бенда + продакшн-батарея
на 3080 Ti); за ним — голова ранжирования iter-364: бит-семейство
(decay_walk ×11.76 / beat_rolls ×8.71, класс iter-362 — коллективные
проходы + O(1)-индексы, байт-идентичность + законы-оракулы),
commit_knowledge_fold вторым, director_global_passes третьим;
стоящие: вызов KI#120, replay-UI, W8, P1/P2/P3, lab-composite-1.
**Active KIs:** KI#113 (test_lab, как в STATUS); KI#119 закрыт этой
итерацией; KI#120 ОТКРЫТ (референс/дрифт — вызов владельца).
