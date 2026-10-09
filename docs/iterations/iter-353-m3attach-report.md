# iter-353 · m3attach — станционный пак M3 v3: ПОЛЕ `model` + живучесть экстрактора + краш-zip (третий станционный круг: первый, где отказ случился НЕ до измерения, а ВО ВРЕМЯ него — и оба раза прогресс владельца остановил не корпус, а транспорт)

**Вызов владельца (2026-10-09, дословно):** «фигня какая-то, нет?» +
два трейсбека станционных прогонов v2: **run 1** (экстрактор
Qwen3.5-9B): attach к `http://127.0.0.1:8080` (билд владельца
**b11490-9c2e0e491**, свежее репо-бинаря b11064), префлят-пины все
зелёные, s1..s10 референс done — и на ПЕРВОМ движковом вызове руки g:
`ServerDown: HTTP 400: {"message":"model name is missing from the
request"}`; **run 2** (экстрактор Kev-4B-Q8_0): `[spawn] …llama-server
-m Kev-4B-Q8_0.gguf --port 53402 …` → `llama-server died rc=1 (see
m3_llama_extract.log)` ДО префлайта — весь прогон умер, не начавшись.
+ «исправь все и пришли ссылку на правленный архив, ало!». Явный ввод
сессии (D-198). BASE_COMMIT: `f27c2a3` (= HEAD прогона владельца —
префлят его run 1 показывает тот же хеш).

**Класс риска:** R0/R1 (внутрирепо — только док-райдеры; нулевой код,
нулевые данные пака; INV-1..5 не тронуты, ЛОГ не тронут. Пак живёт
ВНЕ репо — Rule 9 / D-046, форма iter-348/349/351/352).

## A. Диагноз (оба отказа — исполнением, не чтением)

**Баг A — OAI-поле `model`.** Клиент v1/v2 не слал `model` в теле
`/v1/chat/completions`. Билд-ОКНО строгости: b11064 (репо-бинарь,
автоспавн) / b11429 / b11500 / b11538 — принимают тело без поля;
**b11490 владельца — отвергает** (точный текст 400 совпадает с
llama.cpp-формой `invalid_request_error`). Почему m2 v2 «работал», а
m3 v2 умер на том же железе: (а) m2 v2 СЛАЛ поле, когда задан
`--model` (station_m2_probe.py:327 `body["model"] = self.model` —
механизм был, у m3 v1 при переписывании клиента он выпал); (б) на
станции m2 v2 вообще АВТОСПАВНИЛ b11064 (8080 был мёртв) — а m3 v2
приаттачился к живому серверу владельца b11490. Attach-форма m3
впервые ударилась в строгий билд. T1 (строгий мок, дословный ответ
b11490) воспроизводит отказ v1 1:1 — диагноз исполнением.

**Баг B — смерть экстрактора убила прогон.** rc=1 спавна Kev-4B:
лог лежал в папке пака, В ZIP не ехал (упаковщик ходил только по
run-dir), причина владельцу не видна. Классы причин (лог не получен,
владелец его не прислал): архитектура GGUF не поддержана билдом
b11064 (Kev на станции ни разу не грузился — в m2-круге выбор был
Gemma), OneDrive-заглушка в папке моделей, VRAM-двое-резидентности
(12 ГБ: главная ~5-6 ГБ + Q8 4.5 ГБ). Главный дефект — не сам rc=1,
а ДИЗАЙН: стартовый проб экстрактора (props-only, ничего не
измеряет) валил ВЕСЬ прогон до первого измерения.

**Ещё три скрытых краша v1 — найдены чтением, закрыты моками**
(формы, которые CPU-валидация iter-351 не доезжала — там был
автоспавн + отдельный экстрактор 0.6B): (1) `run_det` звал
`main_server.stop()` без None-гарда — attach-форма упала бы на
стадии det ПОСЛЕ моего фикса бага A; (2) F-self: `extract_lazy`
None → `.ensure()`/`.stop()` без гарда в трёх местах (run_arm,
run_leak, run_det) — форма, задокументированная в README, была
сломана вся; (3) attach + ни одного exe-кандидата → `IndexError` в
`_exe_candidates(repo)[0]`.

## B. Что сделано — пак v3 (5 файлов, вне репо; батарея байт-в-байт)

Сборка: v3 = v1 (md5-эталон) + пять пунктов §B отчёта iter-352
перенесены по спецификации (исходник v2 утерян вместе с обрывом
сессии: лестница репо verbatim из m2 v2 + `cd /d "%~dp0"` +
`.gguf` case-insensitive + `none`/`self` в промте экстрактора +
repo/repo_tried в gate) + новые законы:

1. **ПОЛЕ `model` ВСЕГДА** — id берётся из `/v1/models` САМОГО
   сервера (кэш по endpoint: респавн = новый порт = новый проб;
   attach и спавн детектят заранее, chat() — ленивый страховочный
   путь); fallback `default`. Старые билды игнорируют лишнее поле,
   строгим оно обязательно — отправка безопасна на любом классе;
2. **GGUF ПРЕ-ЧЕК** перед спавном: магия `GGUF`, размер, читаемость
   — OneDrive-заглушка и битый файл ловятся ДО спавна с внятной
   формулировкой (то, чего run 2 не показал вовсе);
3. **ХВОСТ ЛОГА В КАЖДОМ ОТКАЗЕ СПАВНА** (25 строк) — причина едет в
   сообщении об ошибке и в консоль, не в файл, который надо искать;
4. **GPU-ЛЕСТНИЦА СПАВНА**: default → `--n-gpu-layers 24` → `8` →
   `0`, свежий порт на каждой попытке; явный `-ngl` в `--server-arg`
   выключает лестницу (слово оператора выше);
5. **ДЕГРАДАЦИЯ ЭКСТРАКТОРА** (`ExtractorDown(ServerDown)`,
   поднимается только LazyServer-путями): стартовый проб с TTY
   РЕ-ПРОМТОМ — `s` скип F / `u` self / номер-путь другая модель
   (точный путь владельца для Kev); не-TTY — честный авто-скип с
   записью причины в gate; смерть mid-run — рука помечается
   скипом, G/H0/H8/G2 едут дальше; `_stage_done` и leak-need
   считают мёртвый экстрактор как `--no-f`;
6. **КРАШ-ZIP ЗАКОН**: любой упавший прогон всё равно пакует
   диагностический m3_*.zip (порядок finally: summary → zip с
   summary внутри → summary с строкой package); сервер-логи
   `m3_llama_*.log` копируются в `run/logs/` и едут ВНУТРИ zip;
7. **ремонты attach/F-self**: гард det-рестарта (attach пишет честную
   `attach_note`-запись, тег намеренно НЕ `restart_cold` — заметка не
   вердикт), `_lazy_stop()` None-safe на четырёх местах, гард
   «attach без exe» → честная деградация, а не IndexError;
8. preflight `main_model`/`extract_model` теперь с fallback-цепочкой
   `model_path → model → model_id (/v1/models) → model_alias`
   (датум run 1: `"main_model": "none"` — /props билда владельца не
   отдал путь); gate несёт `pack_version`, `attach_model_id`,
   `extractor_error`.

`m3_analysis.py`/`m3_units.py` — md5-идентичны v1
(`d11f319b…`/`e1f461eb…`). Изменённые поверхности: транспорт,
спавн, выбор/деградация, упаковка. Батарея (руки/циклы/цензус)
не тронута.

## C. Валидация (§13.1-класс; 2 ядра / 4 ГБ; + llama.cpp **b11538** CPU + Qwen3-0.6B-Q4_K_M)

- **СТРОГИЙ МОК b11490** (дословный 400 без `model`, `/health`,
  `/props`, `/v1/models`, гибридная форма ответа) — **9/9**:
  T1 репро отказа v1 1:1 (до фикса), T2 фикс проходит, T3 ПОЛНАЯ
  smoke-батарея в attach-форме (все стадии зелёные, zip, gate с
  model_id), T4 битый GGUF → деградация (F скип, остальное done,
  причина в gate), T5 F-self end-to-end (три краша v1 закрыты),
  T6a мёртвый exe — 4 ступени, хвосты в ошибке, T6b выживание на
  ngl-0 + чат со строгим model-полем, T6c явный `-ngl` проходит
  насквозь, T7 сервер умер mid-run → прогон упал И диагностический
  zip собран (summary внутри);
- **PTY ×3**: промт экстрактора `none` (F скип) / `self` (F-self
  done) / **мёртвый экстрактор → ре-промт → `u`** — точный путь
  Kev владельца: батарея выжила, gate записал деградацию честно;
- **РЕАЛЬНЫЙ b11538** (свежее b11490 владельца): полная smoke-батарея
  в ОБОИХ формах — **attach** (10/10 стадий за 3 чанка с резюме,
  `[engine] attach … (model id …)` — поле шлётся, пин G
  `9fa7e9f4359a9201` = **ШЕСТАЯ точка кросс-батарейного якоря**,
  golden byte-contract true, zip 141 КБ) и **автоспавн** (10/10 за
  2 чанка, exe найден в подпапке по закону лаунчера, рецикл
  grammar-growth жив, ноль зомби);
- **ДАТУМ БИЛДА**: b11538 отвечает 200 и БЕЗ `model`, и с чужим id —
  строгость поля не монотонна по версиям, это свойство ОКНА билдов;
  у владельца строгость b11490 — эмпирический факт его прогона,
  фикс корректен и безвреден на обоих классах;
- юниты ×5 зелёные; чистые законы (лестница репо 11 кандидатов,
  `.GGUF`/`.part`, пре-чек магики) — зелёные.

## D. Что НЕ сделано (честно)

- **Станционная строка M3 по-прежнему не снята** — владелец запускает
  v3 (двойной клик; два промта; при смерти экстрактора — выбор в
  окне);
- **Точная причина rc=1 Kev-4B не установлена** — лог run 2 не
  получен; все три класса-кандидата закрыты КОНКРЕТНО (пре-чек /
  лестница / деградация), а хвост лога теперь сам приедет и в окно,
  и в zip;
- `--spawn-server`-форма m2 в m3 не возвращена (сознательно, iter-352
  §D);
- Ничто из репо-очереди (replay-UI, W8, P1/P2/P3, lab-composite-1,
  skip_probes-адрес iter-347) не тронуто.

## E. Проверки

- Пак: py_compile ×3; юниты ×5; мок 9/9; pty 3/3; реальный smoke
  ×2 формы (10/10 стадий каждая); батарея md5 = v1;
- `PYTHONHASHSEED=0 python -m pytest -q` — **rc=0, 2644 зелёных
  индикатора** (счёт этой среды; строка итога подавлена конфигом —
  класс примечания iter-343 о средо-зависимости счёта);
- `ruff check .` — clean; `python scripts/docguard.py` — clean;
  `python scripts/topology.py --check` — clean;
- Самопроверка дельты: список путей == `git status --porcelain
  -uall` против базы `f27c2a3` (блок Git ниже).

## F. Риски

- `/v1/models` на b11490 не снят напрямую (билд недоступен
  отсюда): это стандартный OAI-эндпоинт llama.cpp, /props тот же
  сервер ответил; если вдруг эндпоинта нет — fallback `default`
  (билды, требующие поле, обычно требуют Имя, а не любое значение —
  риск назван, закроется первым же прогоном владельца: префлят
  теперь пишет model_id в gate);
- Поле `grammar` на b11490 не проверяемо отсюда (окно
  b11429…b11500 принимает; тест на него — off_gr-полоса прогона
  владельца: у фиксированного G-пина off_gr должен остаться 0);
- Чанковый budget-выход по-прежнему НЕ пакует zip (закон резюме
  iter-352 сохранён намеренно) — пакует только краш и финиш;
- Пак — внешний инструмент (Rule 9): страховки — пин G (якорь),
  golden byte-contract, префлят, gate-отчёт с pack_version.

## G. Дальше (по порядку владельца)

1. **Станционный прогон M3 v3** — распаковать куда угодно рядом с
   canonsim (лестница та же), двойной клик
   `station_m3_probe.bat`; если сервер 8080 поднят — зонд
   приаттачится к нему (поле `model` шлётся сам); промт
   экстрактора: номер / `self` / `none`; если Kev опять не
   поднимется — в окне будет ХВОСТ ЛОГА и выбор `s`/`u`/модель.
   Прислать `m3_*.zip` (даже из упавшего прогона zip теперь есть).
   Чтение: цензус/дельты, латентностный леджер («тапки» на GPU),
   пробы прозы, f6f-эхо, детерминизм.
2. Затем: решение M2 (пакет iter-350 §G + m3-колонки), дальше
   постоянные вызовы — replay-UI NOT-EXPOSED, W8, P1/P2/P3,
   lab-composite-1.

## H. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-353-m3attach-report.md
git status --short
git commit -m "iter-353-m3attach: THE M3 STATION PACK v3 - the OAI model field + the extractor resilience + the crash zip (the third station round-trip: both owner failures diagnosed by execution - the strict-mock 400 repro 1:1 on v1 (the b11490 attach build REQUIRES the chat body's model field; the field now always sent, the id from the server's own /v1/models) + the dead-extractor law (a broken extractor model skipped the F arm and offered skip/self/another at the TTY - never again a whole run dead before its first measurement; the GGUF pre-check, the spawn GPU ladder, the log tail in every failure, the server logs INSIDE the zip, the crash always packages its diagnostic zip) + three latent v1 crashes in the never-exercised attach/F-self forms closed (the det restart None-guard, the F-self ensure/stop guards, the attach-no-exe IndexError); the battery byte-untouched; validated: strict mock 9/9 (the repro, the fix, the attach battery, the degrade, F-self, the ladder, the crash zip), pty 3/3 (none/self/the dead-extractor re-prompt - the owner's Kev path), REAL b11538 + Qwen3-0.6B in BOTH forms (attach 10/10 stages chunked-with-resume, the G pin = the cross-battery anchor's SIXTH point; autospawn 10/10, zero zombies); the b11538 leniency datum recorded - the strictness is a build-window property, the owner's b11490 the authority; zero repo code)"
git push
```
