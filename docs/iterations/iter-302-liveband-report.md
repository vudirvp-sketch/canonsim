# Отчёт итерации iter-302 — frontendweb: LIVE BAND CLOSURE
(закрытие объявленных owner-side полос над настоящим llama.cpp в
песочнице: Chat COMPLETED, Models ACTIVE/EVICTED, model.fetch
COMPLETED, S0-4 с живым LLM)

Вызов владельца: «продолжай работу над фронтендом» + «если нужно для
работы - не забывай что ты можешь поставить в песочницу llama.cpp и
любое окружение нужное!» — делегированный вызов того же класса, что
iter-294..301, с явным разрешением окружения. Разблокировка прямая:
iter-298/300 объявили полосы owner-side ровно потому, что в песочнице
не было llama.cpp («a loaded llama.cpp model — declared, never
faked»); разрешение владельца снимает это ограничение — полосы
закрываются агент-стайл, живьём, без единой сфабрикованной строки.
Класс риска: R2 (frontend-local: одна честная правка устаревшего
UI-текста; + один герметичный тест-фикс KI#110 в Python-тестах —
R1-класс внутри R2-итерации; ноль изменений поведения Python, ноль
canon, INV-1..5 не тронуты, LOG нетронут). BASE_COMMIT `1f730ab`.

## A. Что закрыто живьём (полный состав полос)

**Окружение** (вне диффа, gitignored): llama.cpp b11337 (v0.5.0-dev,
commit d775ebf36, ubuntu-x64 CPU) в `workbench/runtime/llama.cpp/` —
положен ровно в документированный drop-folder; гейтвей сам обнаружил
его дискавери-сканом (баннер startup'а назвал полный путь — закон
разрешения exe проверен живьём, а не тестом). Модели приходят ЧЕРЕЗ
собственный `model.fetch` op гейтвея (INV-4's sanctioned outbound
surface): stories15M-q4_0 (19 077 344 байт, 3.0s) и
qwen2.5-0.5b-instruct-q4_k_m (491 400 032 байта, 45.6s, PROGRESS
`downloaded_bytes/total_bytes` наблюдаем в run.get).

**Живой смок** (реальные HTTP POST /op, свежий client_request_id на
каждую попытку — G4; транскрипт в сессии):

- **fetch COMPLETED** ×2 — полоса, которую iter-300 закрыла только
  admission-отказом, теперь закрыта до терминала: реальная сеть,
  живой прогресс, атомарная посадка, honest overwrite-refusal при
  повторе;
- **load → ACTIVE**: run COMPLETED → model.states: активный слот
  заполнен, состояние ACTIVE — полоса iter-300 закрыта;
- **chat.send → COMPLETED**: НАСТОЯЩИЙ ответ модели —
  «"Welcome to the village! Tonight's ale is from our esteemed
  brewmasters. Cheers!"», finish_reason `stop`, backend identity
  `{model: …qwen2.5-0.5b-instruct-q4_k_m.gguf, build:
  b11337-d775ebf36}`, REQUESTED/EFFECTIVE pair (temp запрошен не
  был → effective 0.8 от BASE-профиля) — полоса iter-298 закрыта;
- **одиночный слот**: второй load при ACTIVE → DOMAIN_REJECTED
  дословно («'…' is ACTIVE — unload first (the slot is single this
  row…)»);
- **unload → EVICTED**: run COMPLETED → model.states: EVICTED, слот
  пуст — полоса iter-300 закрыта;
- **ре-селекция**: EVICTED → SELECTED → ACTIVE (stories15M), вторая
  модель честно завершает chat (`finish_reason: length` —
  крошечная модель, честный терминал);
- **финал**: оба EVICTED, слот пуст.

**Живой браузерный closure** (Vite dev server + proxy + headless
Chromium над обслуживаемой композицией; скриншоты приложены к сессии:
`iter-302-models-active.png`, `iter-302-load-probe-with-llm.png`,
`iter-302-chat-completed.png`, `iter-302-models-evicted.png`):

- чипы дискавери до загрузки: оба DISCOVERED (файл ничего не
  доказывает — §20);
- **ACTIVE через собственную кнопку load поверхности Models**: run →
  терминал → ровно ОДНО перечитывание контекста → чип ACTIVE +
  `tag-live` маркер + строка активного слота;
- **S0-4 С ЖИВЫМ LLM**: load probe замерен при загруженной модели —
  50 ops, 0.45-0.49s, **107.8–110.3 ops/s** (attach+get пары) —
  критерий S0-4 «with simulation and/or a local LLM active» впервые
  исполнен буквально;
- **COMPLETED-ход Chat через композер**: ответ модели рендерится +
  полная строка происхождения («run 3ab58bc8… · finish stop ·
  …qwen2.5-0.5b-instruct-q4_k_m.gguf · temp requested (absent — the
  profile's BASE) → effective 0.8 · max_tokens 512»);
- **EVICTED через собственную кнопку unload**;
- **ноль ошибок консоли** на всём драйве.

## B. Кодовые изменения (2 файла, оба — честность, не новые механизмы)

1. **`frontend/src/app/composition/App.tsx`** — устаревшее
   утверждение окружения в UI-тексте Load probe: «no llama.cpp
   model present in this environment (that band is declared, not
   faked)» было верно для песочницы S0, но неверно везде, где модель
   есть (станция владельца с `D:\llama.cpp` — включённо). Заменено на
   честное описание инструмента + измеренная заметка (50 ops ≈108
   ops/s рядом с живым llama-server). Комментарий над драйвером
   синхронизирован: «с загруженной моделью замер идёт рядом с живым
   llama-server; без неё — честный Python-side стенд; проба никогда
   не фабрикует LLM-сторону».
2. **`tests/test_workbench_app.py`** — KI#110: тест
   `test_the_launch_params_merge_cli_over_settings` неявно предполагал
   ПУСТОЙ discovery home: задокументированный поток владельца (drop
   llama.cpp в `workbench/runtime/llama.cpp/`) делал его красным —
   дискавери-скан исправно находил бинарник. Фикс герметичный:
   monkeypatch на пустой tmp-home (сама цепочка разрешения пинируется
   hermetic-тестом `test_the_exe_resolution_order`, который и так
   принимает home явно). Открыт и закрыт в той же итерации (§5).

Отложено по scope-закону (названо, не молча): новые committed-фикстуры
полос COMPLETED/ACTIVE — шейпы уже запинированы существующими
контрактными/интеграционными рядами (Chat-тест выводит COMPLETED-документ
из захваченных форм; validators несут finish_reason: stop), а live-полоса
доказывается транскриптом + скриншотами; фикстуры с недетерминированным
контентом и путями песочницы расширили бы дифф без новой контрактной
глубины.

## C. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped
                                           (с ПРИСУТСТВУЮЩИМ деревом
                                           llama.cpp в runtime/ —
                                           герметичность KI#110
                                           подтверждена живьём)
ruff check .                              → clean
python scripts/docguard.py                → clean
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 221 passed / 12 files
frontend: npm run build                   → dist 15.69kB css / 437.25kB js
```

Живой смок: см. §A (все полосы, транскрипт `/tmp/iter302_transcript.json`
приложен к сессии). Живой браузерный closure: см. §A (4 скриншота +
`iter-302-browser-closure.json`). Повторные прогоны драйва
воспроизводимы (3 полных прогона; идемпотентность fetch — honest
refusal; teardown graceful — SIGTERM гейтвея ретирует его
llama-server-потомка, жёсткий kill сиротит его и валил следующий
спавн EADDRINUSE — оркестратор посылает TERM до KILL).

## D. Границы / следующий шаг

- Полосы закрыты в песочнице; станция владельца закрывает их тем же
  путём (Workbench.bat → Models → load → Chat) — llama.cpp уже
  документирован как drop-folder.
- Следующие ряды фронтенда — вызов владельца (каждый своя итерация):
  streaming admission (SSE — сначала контракт gateway, R3/R4-класс),
  acceptance matrix, коллапс DECISIONS (36→30), оставшиеся строки
  tooling floor (CI wiring, Playwright multi-tab smoke,
  dependency-cruiser), Tauri (нативный пикер импорта), PWA.
- Standing boundaries без изменений: Settings Appearance (нет
  персистентного стора), SSE/WebSocket, Tauri, PWA — каждое своё
  допущение.

## E. Риски

- Ответ модели недетерминирован (seed -1 в профиле по умолчанию) —
  полоса закрывает ФОРМУ (content/finish/backend identity), не
  конкретный текст; фикстуры не коммитятся именно поэтому.
- Драйв измерял ops/s на пустом чате рядом с простой 0.5B-моделью —
  это заметка, не перф-лаб (закон S0-4: rough numbers).
- llama.cpp b11337 — свежий бинарник; повторная сборка владельцем из
  другого релиза меняет только build identity в документах (полоса
  не пинирует номер сборки).

## F. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/app/composition/App.tsx tests/test_workbench_app.py STATUS.md worklog.md docs/TASKS.md frontend/README.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/iterations/iter-302-liveband-report.md
git status --short
git commit -m "iter-302-liveband: the owner-side bands closed live over a real sandbox llama.cpp (chat COMPLETED, models ACTIVE/EVICTED, fetch COMPLETED, S0-4 with a live LLM; the stale probe copy; KI#110 hermetic)"
git push
```

Delta-архив: `canonsim_iter-302-liveband_2026-10-02.zip`
(BASE_COMMIT `1f730ab…`, изменённые пути — ровно 8, создан
`docs/iterations/iter-302-liveband-report.md`, удалений нет),
приложен к сессии + прямая ссылка и md5 в чате.
