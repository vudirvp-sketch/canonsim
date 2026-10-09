# iter-352 · m3repoladder — станционный пак M3 v2: ЛЕСТНИЦА РЕПО (второй станционный круг подряд платит за форму запуска: v1 урезал лестницу m2 v2 и умер на раскладке, на которой m2 работал)

**Вызов владельца (2026-10-09, дословно):** «"canonsim_m2_station_pack_v2.7z"
=> это прошлая версия, она работала, а твоя новая не работает! пути
бери с версии canonsim_m2_station_pack_v2.7z.» + инвентарь станции:
модели `Kev-4B-Q8_0.gguf`, `Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-
Q4_K_M.gguf`, `Qwen3.5-9B-Q4_K_M.gguf` в `canonsim\workbench\runtime\
models\`, llama.cpp в `canonsim\workbench\runtime\llama.cpp\`, RTX
3080 Ti + 32 ГБ. Явный ввод сессии (D-198): починить запуск пака M3 —
путями из рабочего m2 v2. BASE_COMMIT: `3580ebc` (iter-351-m3arch).

**Класс риска:** R0/R1 (внутрирепо — только док-райдеры; нулевой код,
нулевые данные пака; INV-1..5 не тронуты, ЛОГ не тронут. Пак живёт
ВНЕ репо — Rule 9 / D-046, форма iter-348/349/351).

## A. Диагноз (что умерло на станции)

`station_m3_probe.py` v1 искал репо по ТРЁМ кандидатам: `pack/canonsim`,
`cwd/canonsim`, `cwd`. Пак, распакованный РЯДОМ с репо (собственная
инструкция README v1: «распакуй папку пака РЯДОМ с canonsim»; форма
Explorer «Extract All» = папка пака рядом с `canonsim/`), не попадает
НИ В ОДИН кандидат: `../canonsim` в лестнице отсутствовал. Зонд умирал
на старте: `SystemExit("the canonsim repo was not found")`. Пак m2 v2
на ТОЙ ЖЕ раскладке работал — его `_find_repo` (iter-349) нёс
`../canonsim` + `../../canonsim` + `../../../canonsim` + восемь
домашних путей (включая `OneDrive/Desktop/repo/canonsim` — реальный
путь владельца) + env `CANONSIM_REPO`. Второй станственный круг
подряд платит за одно и то же: форма запуска, а не измерение
(iter-349 §A — «инструмент, требующий ручной подготовки окружения,
не годится как форма двойного клика»; урок не перенесён из
движковой лестницы в репо-лестницу).

Сопутствующие дефекты того же класса: батник v1 без `cd /d "%~dp0"`
(запуск зависит от cwd — при «Run as administrator» cwd = System32,
`python station_m3_probe.py` не находит даже сам скрипт); `_gguf_models`
регистрозависим по суффиксу (`.GGUF` не матчится); промт экстрактора
не имел выхода без ультралайта — а в инвентаре владельца НЕТ модели
класса ≤1B (Kev-4B / Gemma-4-E4B / Qwen3.5-9B), т.е. чистый двойной
клик упирался в тупик: номер = измерять F не-ультралайтом, Ctrl+C =
всё умерло. `--no-f`/`--extractor-model self` существовали только как
CLI-флаги — недостижимые из двойного клика.

Воспроизведение 1:1 в сэндбоксе (T-R1, §C): v1, пак рядом с репо,
без флагов → exit 1, «the canonsim repo was not found». Ложная тревога
по ходу разбора закрыта: строка `p50 = s[min(...)]` из `m3_analysis.py`
в терминале отображалась как `sin(...)]` — терминал съедал `[m` как
ANSI-эскейп; AST-парс и исполнение подтверждают файл валиден (датум
для будущих сессий: подозрительный синтаксис проверяется исполнением,
не глазом).

## B. Что сделано — пак v2 (5 файлов, вне репо; батарея байт-в-байт)

1. **ЛЕСТНИЦА РЕПО** (порт m2 v2 вербатим, `find_repo` возвращает
   `(repo, tried)`): `--repo` → env `CANONSIM_REPO` → относительно
   папки пака (`canonsim`, `../canonsim`, `../../canonsim`,
   `../../../canonsim`) → относительно cwd (те же четыре) → восемь
   домашних путей (`Desktop/repo/canonsim`,
   `OneDrive/Desktop/repo/canonsim`, …). Валидация — два маркера
   m2 (`brief/gbnf.py` + `core/pack.py`). Отказ — ГРОМКИЙ, со всеми
   проверенными кандидатами и готовыми командами (`--repo`, env);
2. **Батник**: `cd /d "%~dp0"` (привязка к своей папке —Outputs,
   логи и zip всегда рядом с батником), py-3-первая лестница Python,
   шапка с обеими лестницами (репо + движок);
3. **`_gguf_models`**: суффикс `.lower()` (форма m2);
4. **Промт экстрактора: ответы `none`/`self`** — `none` = пропуск
   руки F (эквивалент `--no-f`), `self` = главная модель удваивается
   (форма F-self); при нуле кандидатов не-TTY → честный пропуск с
   записью в gate; не-TTY при нескольких → громкий отказ со строками
   `--extractor-model <путь>` / `--extractor-model self` / `--no-f`.
   Закон iter-349 (самодостаточность двойного клика) применён к
   выбору экстрактора; README переписан под инвентарь владельца;
5. **gate.json**: `repo` + `repo_tried` + `repo_discovery` —
   машиночитаемое станционное доказательство находки.

`m3_analysis.py` и `m3_units.py` — md5-идентичны v1
(`d11f319b…` / `e1f461eb…`); батарея (G/H0/H8/F/G2 + leak + det +
леджер) не тронута. Изменённые поверхности: только запуск и выбор.

## C. Сэндбокс-валидация (класс §13.1: 2 ядра / 4.1 ГБ; llama.cpp
**b11429** CPU + Qwen3-1.7B Q4_K_M + Qwen3-0.6B Q4_K_M — пара iter-351,
билд на шаг старше b11500 — записано честно, пины от билда не зависят)

Раскладка станции воссоздана: exe в `workbench/runtime/llama.cpp/
llama-b11429/` (подпапка — закон лаунчера), GGUF в `workbench/
runtime/models/`, 8080 мёртв, пак — папкой рядом с репо.

- **T-R1** (отказ владельца 1:1): v1, пак рядом с репо, без флагов
  → exit 1, «the canonsim repo was not found» — воспроизведён ДО
  фикса, диагноз подтверждён исполнением, не чтением;
- **T-R2** (фикс): v2, та же раскладка, без флагов → репо найден по
  `../canonsim`, 12+ кандидатов перебрано;
- **T-R3a** (пак «где угодно», без env): громкий отказ с полным
  списком кандидатов (12 путей) и готовыми командами;
- **T-R3b** (пак «где угодно» + `CANONSIM_REPO`): найден;
- **T-M**: `.GGUF` в верхнем регистре матчится, `.part` иммунен,
  посторонние файлы игнорируются;
- **T-E0**: exe-лестница находит бинарь в одной подпапке (закон
  лаунчера, без изменений от v1 — проверено, что не сломано);
- **T-E1/E2/E3** (pty, как iter-349 T-B2): промт экстрактора —
  `none` → «none», `self` → «self», номер → путь модели; главный
  промт не тронут;
- **ФИНАЛ** (полная smoke-батарея из формы двойного клика: cwd =
  папка пака, НИ ОДНОГО флага пути, `--model-file`/`--extractor-model`
  явно — не-TTY сессия): все 10 стадий зелёные за 3 чанка
  `--time-budget` (закон резюме exercised live — каждый чанк
  поднимал серверы заново и продолжал по юнитам), ноль движковых
  отказов, ноль зомби-серверов после (проверено ps), zip собран
  (139 595 байт, md5 `b359cb2a…`).

**Якоря ФИНАЛА:** preflight `pin_g 9fa7e9f4359a9201` =
**кросс-батарейный якорь iter-348/350/351** (пятая точка: m2 CPU,
m2 станция, m3 CPU, m3 v2 CPU), `pin_h b459e25088a4550d` = iter-351,
golden byte-contract TRUE, HEAD `3580ebc`; off_gr 0 на всех руках
(включая 20 гибридных циклов smoke); det-mini: g cold≠warm на
b11429 (того же класса, что b11500 — датум билда, честно записан),
h0/h8/f_ext cold==warm; латентностный порядок CPU ожидаемый
(parse ~9.8 с, hybrid ~17.7 с, extract ~4.9 с — класс iter-351).
Smoke-цензус (s1+s2, 10 циклов) НЕ сравним со строками леджера
(полный корпус 51) — проверялась цепь, не полоса (примечание
iter-349 §E).

## D. Что НЕ сделано (честно)

- **Станционная строка M3 по-прежнему не снята** — владелец запускает
  v2 двойным кликом (при трёх моделях зонд спросит номер главного,
  затем экстрактор: номер / `self` / `none`); латентностный леджер
  GPU («тапки», где обработка промтов доминирует) — предмет прогона;
- **Решение M2 не принято и не тронуто** — формы m3 композируются
  с любой политикой (пакет iter-350 §G);
- `--spawn-server`-форма m2 в m3 отсутствует (была исключена из v1
  сознательно — автоспавн покрывает; не возвращена — минимальное
  вмешательство);
- Ничто из репо-очереди (replay-UI, W8, P1/P2/P3, lab-composite-1)
  не тронуто.

## E. Проверки

- Пак: py_compile ×3; юниты ×5 зелёные; T-R1..T-E3 + ФИНАЛ — все
  зелёные (~90 движковых вызовов на b11429);
- `PYTHONHASHSEED=0 python -m pytest -q` — **2644 passed, 1 skipped**
  (репо не тронуто кодом; счёт = iter-351);
- `ruff check .` — clean; `python scripts/docguard.py` — clean;
  `python scripts/topology.py --check` — clean;
- Самопроверка дельты: список путей == `git status --porcelain -uall`
  против базы `3580ebc` (блок Git ниже).

## F. Риски

- Билд валидации b11429 (не b11500) — пины грамматики от билда не
  зависят (пятая точка совпала), но det-датум cold≠warm — класс
  билда; станция (b11064 в m2-круге) пишет свой вердикт;
- Экстрактор на станции — выбор владельца: ультралайт (лучший
  контраст для F), `self` (F-self), вторая из трёх (измеряет форму,
  не класс) или `none` (G/H/G2 самодостаточны) — README называет
  все четыре;
- OneDrive cold-load GGUF остаётся делом 900-с heartbeat-ожидания
  (закон iter-349) — не менялось;
- Пак — внешний инструмент (Rule 9): страховки — пин G (якорь
  леджера), golden byte-contract, preflight, gate-отчёт (теперь с
  репо-путём и списком кандидатов).

## G. Дальше (по порядку владельца)

1. **Станционный прогон M3 v2** — распаковать пак (куда угодно рядом
   с canonsim — лестница найдёт), двойной клик
   `station_m3_probe.bat`, на двух промтах ответить номером
   (главная) и номером/`self`/`none` (экстрактор); прислать
   `m3_*.zip` обратно. Чтение: census/дельты, латентностный леджер
   («тапки» на GPU), пробы прозы, f6f-эхо, детерминизм.
2. Затем: решение M2 (пакет iter-350 §G + m3-колонки), дальше
   постоянные вызовы — replay-UI NOT-EXPOSED, W8, P1/P2/P3,
   lab-composite-1.

## H. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-352-m3repoladder-report.md
git status --short
git commit -m "iter-352-m3repoladder: THE M3 STATION PACK v2 - the repo ladder (the second station round-trip's launch-form lesson: v1's 3-candidate repo discovery died on the exact beside-the-repo layout the m2 v2 ladder served; the owner's directive - the m2 v2 ladder ported verbatim: --repo > CANONSIM_REPO > pack-relative beside/above > the home paths incl. OneDrive/Desktop/repo/canonsim; cd /d %~dp0 in the bat; the case-insensitive .gguf; the 'none'/'self' answers at the extractor prompt - the owner's three models carry no ultra-light, the double-click stays self-sufficient); the battery byte-untouched; validated 13.1 (T-R1 the owner's failure reproduced 1:1 on v1, T-R2/R3/M/E0..E3 the fix proven, the final full smoke end-to-end - all stages green, the G pin = the cross-battery anchor's fifth point, zero engine failures, zero zombies); zero repo code"
git push
```
