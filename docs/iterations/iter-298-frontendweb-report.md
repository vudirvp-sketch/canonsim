# Отчёт итерации iter-298 — frontendweb: CHAT ENTRY
(Phase 3, четвёртый ряд: мир диалога над существующим семейством
run-операций; Chat во главе рейла)

Вызов владельца: «продолжай работу над фронтендом» — делегированный
вызов того же класса, что открыл iter-294/295/296 (D-198 intake).
Ряд выбран по собственному Next итерации iter-297: «Chat lands as its
own surface row at the rail's head — СЛЕДУЮЩИЙ ряд (iter-298):
контракт-зеркало model.*/inference.*/chat.send по образцу Settings +
поверхность (header/viewport/composer/status) с §27 transfer record».
Класс риска: R2 (frontend-local; ноль Python, ноль canon, INV-1..5 не
тронуты, LOG нетронут). BASE_COMMIT `d40c1df`.

## A. Что высажено (21 кодовый/тестовый путь + 6 доковых — один
когерентный минимальный срез, сверх мягкого лимита 3–5, освоено в
worklog)

- **Контракт-зеркало** (`frontend/src/api/gateway/{contracts,validators,client}.ts`)
  — семь СУЩЕСТВУЮЩИХ операций, ни одного нового маршрута (§3):
  - `chat.send` — ADMISSION: закрытый набор аргументов
    (messages/temperature/max_tokens/deadline), результат —
    идентичность исполнения (`state: "STARTING"` как ЛИТЕРАЛ —
    допущение никогда не выдаёт себя за завершение) + `execution_id`;
    клиент посылает переопределения ТОЛЬКО когда они явно заданы;
  - `run.get` / `run.cancel` — путь наблюдения/останова: строгий
    конверт прогона (enum EXECUTION-лестницы из 10 состояний, пары
    frozen_inputs `[ключ, значение]`, блок deadline, progress/result/
    failure_type/diagnostics/artifact); `result` остаётся generic-
    record'ом — чат-вид результата сужается на потребителе своим
    СТРОГИМ схемой (content/finish_reason/backend-identity/
    requested-vs-effective pair); закрытый словарь исходов отмены
    (CANCEL_REQUESTED/CANCELED/FAILED_TO_CANCEL — §12.3);
  - `model.list` / `model.states` — линия модели в шапке:
    классификация каталога (OK|MISSING), записи §20-скана (mtime_ns —
    ЧИСЛО, не int: наносекундная эпоха вне safe-integer — честное
    зеркало, задокументировано) + лестница MODEL из 9 состояний и
    ACTIVE-слот;
  - `inference.read` — КОМПАКТНАЯ контекстная проекция §21.2:
    потребляемый срез (profile_name/controls/applies/managed_live/
    pinned) валидируется ЗАКРЫТО, непотребляемая глубина (profile,
    presets, categories, sampler chain, compiled preview) едет по
    проводу НЕПОТРЕБЛЕННОЙ — `looseObject` это сознательная форма
    закона data-driven («UI никогда не перекодирует словарь
    контролов»); `projectInference` на шве не пускает index-сигнатуру
    в поверхности.
- **Поверхность** (`frontend/src/features/chat/{useChat.ts, Chat.tsx}`
  (новые)) — четыре региона по названной iter-297 форме:
  - **header** — стрип: линия модели (истина состояний загрузки, не
    догадка обнаружения) + компактная проекция inference («temp 0.8
    (EFFECTIVE · profile) · managed down · applies next-spawn»); три
    чтения на монтирование, каждое со СВОИМ лейном отказа;
  - **viewport** — транскрипт как presentation-state поверхности:
    per-exchange идентичность (execution_id), строка провенанса
    REQUESTED/EFFECTIVE на каждый ответ, near-bottom follow law;
  - **composer** — черновик владеет REQUEST'ом: Enter отправляет,
    Shift+Enter переносит, call-local переопределения (temperature/
    max_tokens) ЯВНО на поверхности (пусто = BASE-резолюция профиля,
    показанная в стрипе — скрытых сэмплер-настроек нет по §21.2),
    нелегальное явное значение честно дизейблит отправку;
  - **status** — §8-замыкание как стадии: REQUESTED (черновик) →
    ACCEPTED (admission) → EFFECTIVE (frozen inputs прогона, §10) →
    OBSERVED (терминальный документ, ДОСЛОВНО) → PRESENTED (ряды).
    BOUNDED poll-цикл: 700мс константа, один на активный прогон,
    мёртв на терминале/TRANSPORT/размонтировании, re-poll — явное
    действие пользователя (G4); правило контекста сообщений — в
    следующий send едут ТОЛЬКО допущенные ходы пользователя и
    завершённые ответы (возможно-не-отправленный ход — вне контекста).
- **Композиция** (`frontend/src/app/composition/{App.tsx, styles.css}`)
  — Chat во главе рейла (§2.1 каноническое IA-дерево; pin в
  Shell-тестах), стили — только нейтральные токены (второго акцента
  нет: канальные оттенки — STATE-класс dual-read пары).
- **Fixtures** — 10 живых захваченных документов (in-process parity
  над реальной композицией, throwaway-корни + один настоящий файл
  .gguf для §20-скана): честный FAILED-бенд (EngineError, connection
  refused) захвачен ДОСЛОВНО — сфабрикованного завершения нет.
- **Тесты** — 18 контрактных рядов (испорченные варианты отклоняются:
  чужое EXECUTION-состояние, не-кортеж frozen input, отсутствие
  deadline, неизвестный член завершения, сфабрикованный admission-
  state, чужой directory_state/MODEL-ступень, пропавший controls,
  чужой исход отмены) + 12 интеграционных (Chat.test.tsx: три
  чтения без polling'а; полный closure до FAILED с дословными
  диагностика­ми и мёртвым циклом; COMPLETED-бенд с провенансом и
  правилом контекста [user, assistant, user]; переопределения на
  проводе только явные; REJECTED дословно без автоповтора; TRANSPORT
  с UNKNOWN и выключением хода из контекста; stop с fresh-key и
  дословным исходом; STALE + явный re-poll; каденция с реальным
  временем; без сессии честный дизейбл) + пин рейла в Shell-тестах.
- **Доки**: stage map (контекст агента), ledger TASKS (iter-287
  выселен), STATUS (шапка), worklog (iter-288 выселен), README
  фронтенда, этот отчёт.

## B. Законы, которые несёт ряд

- **FRONTEND_WEB_LAW §8** — замыкание по стадиям, запреты
  коллапсов названы в докстринге хука: `textarea.value !== EFFECTIVE`,
  `click !== success`, `cancel click !== canceled` (ответ отмены —
  наблюдаемый исход REQUEST'а; терминальная истина прогона — сам
  прогон: опрос продолжается ПОСЛЕ отмены), `HTTP 200 !== semantic
  success`.
- **§3 (Execution seam)** — длительная работа: идентичность
  немедленно, наблюдение отдельным чтением; неоднозначный результат
  остаётся UNKNOWN; G4 — ни одного автоповтора (ни отправки, ни
  опроса: TRANSPORT на run.get останавливает цикл, STALE-лейн,
  re-poll руками).
- **§6 (boundedness)** — «passive on evidence, never a polling
  storm»: один поллер на один прогон, фиксированная каденция,
  смерть на терминале/TRANSPORT/unmount; транскрипт — волатильный
  буфер поверхности (чат-история НЕ канон, §21 persistence split) —
  размонтирование её честно роняет, как и буфер live-tail.
- **§21.1/§21.2 (UIUX)** — эргономика чата: per-message identity,
  провенанс run/model, чёткие ошибки; компактная проекция inference
  + ссылка (поверхность Inference — позже), никаких скрытых
  сэмплер-настроек; requested ≠ accepted ≠ effective ≠ observed ≠
  presented.
- **§15** — task-aware focus entry (Chat → composer), Enter как
  default action, Escape-free (нет транзиентных панелей), reduced-
  motion: follow — прямой прыжок (статический эквивалент по
  построению, твин не вводился).
- **VISUAL_SYSTEM_UI §2/§3** — только токены, ноль сырых литералов
  (guard V1 зелёный на новых стилях).

## C. §27 transfer records (метод D-246 — донор информирует, закон
решает; компактная форма протокола)

### C.1 Composer-механика LM Studio / Jan (внешние доноры)

- TASK: механика composer'а чата — владение черновиком, отправка,
  останов, следование за контентом.
- OWNER: FRONTEND_UIUX_LAW §15/§21.1 (закон); поверхность — носитель.
- SOURCE: LM Studio и Jan (desktop LLM-клиенты класса «чат с локальной
  моделью») — донорские паттерны composer'а.
- OBSERVATION (механика, не вид): (1) черновик живёт в composer'е и
  очищается на отправке; (2) Enter = отправка, Shift+Enter = перенос;
  (3) пока генерация идёт — affordance остановки; (4) вьюпорт
  следует за контентом ТОЛЬКО когда читатель у нижней кромки.
- MECHANISM: разделение REQUEST (локальный черновик) и OBSERVED
  (серверный документ); ключевые действия — явные; позиция чтения
  пользователя выигрывает у авто-скролла.
- FUNCTION: пользователь никогда не теряет позицию чтения и никогда
  не ждёт «молчащего» UI — каждое состояние visibly named.
- TRANSFER BOUNDARY: НЕ переносятся — иконки/темы/лейблы/раскладка
  доноров, их streaming-SSE (у нас POST-only mandate), их история
  чата в localStorage (у нас — волатильность по закону).
- CANONSIM INVARIANT: §8 (closure-стадии), §5 (POST-only), §6
  (нет browser-storage как истины).
- NATIVE CARRIER: features/chat/{useChat.ts (черновик/стадии/каденция),
  Chat.tsx (composer/follow)}.
- ADAPTATION: останов = run.cancel (§12.3 — REQUEST с наблюдаемым
  исходом, не «completed»); отправка = один dispatch с fresh-key;
  follow = прямой прыжок после кадра (rAF).
- TARGET ENVELOPE: MUST PRESERVE — иерархию (composer подчинён
  транскрипту), видимость состояний, фокус-вход в composer; MAY VARY —
  текст лейблов, число полей переопределений, геометрия.
- COST: ~60 строк follow+composer-механики.
- FALSIFIER: (а) скролл дёргается при чтении истории — механизм
  сломан; (б) после терминала цикл продолжает слать run.get — G4
  сломан; (в) composer дизейблится навсегда после отказа — re-arm
  сломан.
- PROOF: интеграционные ряды (каденция/мёртвый цикл/re-arm/stop) +
  живой браузерный closure (2 живые отправки, follow, фокус, ноль
  ошибок консоли) — RUNTIME_VERIFIED в jsdom-бенде + живой бенд;
  COMPLETED-бенд — DEFERRED owner-side (нужна загруженная модель).
- DISPOSITION: KEEP.
- DURABLE RESIDUE ROUTING: закон уже в §15/§21.1; переносимых
  NEW-механик сверх существующего закона нет — запись закрывает
  обязательство протокола.

### C.2 Chat-follow из собственной Redot-эры (внутренний донор)

- TASK: near-bottom follow + late-layout read.
- OWNER: FRONTEND_UIUX_LAW §21.1 (ссылка на iter-230 паттерн).
- SOURCE: собственный Redot-код (удалён D-245; STATUS FAQ: «the chat
  follow law (scrollbar max read AFTER a frame, the near-bottom gate)
  — carried forward as PRINCIPLES for the web client»).
- OBSERVATION: чтение максимума скроллбара ПОСЛЕ кадра (late-layout),
  гейт нижней кромки.
- MECHANISM: величины раскладки недостоверны в момент мутации DOM —
  читать/писать их после кадра (rAF); следовать только из near-bottom.
- FUNCTION: отсутствие «прыжка под рукой» при чтении истории.
- TRANSFER BOUNDARY: GDScript/Node-механика НЕ переносится — только
  принцип (гейт + позднее чтение).
- CANONSIM INVARIANT: §15 reduced-motion (прямой прыжок — уже
  статический эквивалент).
- NATIVE CARRIER: Chat.tsx (onViewportScroll + rAF-effect).
- ADAPTATION: rAF вместо await frame; порог 80px — константа.
- TARGET ENVELOPE: MUST PRESERVE — гейт; MAY VARY — порог, метод
  чтения.
- COST: ~20 строк.
- FALSIFIER: viewport скроллит при reading-above — гейт сломан.
- PROOF: код + живой браузерный бенд (follow сработал на обеих
  живых отправках); jsdom не меряет раскладку — бенд живой.
- DISPOSITION: KEEP.
- DURABLE RESIDUE ROUTING: §21.1 уже владеет; запись подтверждает
  перенос принципа в web-клиент.

## D. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped (92.6s)
ruff check .                              → clean
python scripts/docguard.py                → clean (caps + state-layer)
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 139 passed / 10 files (108 + 31)
frontend: npm run build                   → dist 9.99kB css / 387.94kB js
```

**Живой смок против реального gateway** (HTTP, путь браузера;
`scripts/workbench_app.py`, throwaway-корни) — **16/16**:
- шесть операций выставлены (chat.send/run.get/run.cancel/model.list/
  model.states/inference.read);
- model.list: 1 обнаружен (настоящий файл на диске), directory OK;
  model.states: честное «none ACTIVE»;
- inference.read: Baseline, temperature 0.8 EFFECTIVE·profile,
  applies next-spawn;
- chat.send → OK, STARTING + execution_id (никогда не завершение);
- run.get → терминальный FAILED (EngineError, `[unavailable] …
  Connection refused` — ДОСЛОВНО), frozen_inputs наблюдаемы (§10);
- run.cancel на терминальном → FAILED_TO_CANCEL (дословно);
- DOMAIN_REJECTED-лейны дословно (unknown argument; no session).

**Живой браузерный closure** (Vite-прокси + headless-браузер, снимки
приложены: `iter-298-chat-ia-rail.png`,
`iter-298-chat-failed-band.png`, `iter-298-chat-second-turn.png`):
- рейл = ровно [Chat, Trajectory, Observatory, Settings,
  Diagnostics] — Chat во главе (§2.1);
- стрип: «model none ACTIVE · discovered 1 · profile Baseline ·
  temp 0.8 (EFFECTIVE · profile) · managed down · applies
  next-spawn» — вся честная линия;
- две живые отправки → оба прогона закрылись FAILED с дословными
  диагностиками (честный бенд среды без llama-server); провенанс и
  follow сработали; фокус в composer; Enter отправил второй ход;
- уход на Trajectory → транскрипт размонтировался (0 рядов —
  волатильность по закону), возврат — поверхность перечиталась;
- консоль: ноль ошибок.

**Мутационная честность fixtures**: захвачены с реальной композиции
in-process (parity-law byte form); «COMPLETED»-варианты в
интеграционных тестах — ПРОИЗВОДНЫЕ формы (structuredClone от
захваченного конверта), явно помечены в тесте — закоммиченные
fixtures остаются живым захваченным множеством.

## E. Границы / следующий шаг

- **COMPLETED-бенд — owner-side**: для живого ответа модели нужен
  загруженный llama-server (model.load — ряд поверхности Models).
  В этой среде честно закрыты admission/FAILED/REJECTED-лейны —
  захвачены дословно, завершение НЕ сфабриковано.
- Следующие ряды фронтенда — вызов владельца: поверхность
  **Inference** (inf-2: пресеты/поиск/категории/advanced —
  data-driven над полным документом), поверхность **Models**
  (load/unload/import — оставшееся зеркало семейства), вторичная
  навигация Settings, streaming admission (SSE — сначала контракт
  gateway), acceptance matrix, коллапс DECISIONS (36→30).
- Прочие границы без изменений: SSE/WebSocket, Tauri, PWA — каждое
  своё admission.

## F. Риски

- Транскрипт умирает с поверхностью (переключение вкладки рейла
  теряет диалог) — волатильность по закону §6/§7, как у live-tail;
  персистентность чат-истории — отдельный будущий ряд (§21
  persistence split), не молчаливое расширение этого.
- Поллер живёт до терминала: при недостижимом терминале (deadline
  120с сервера) цикл продолжается до него — каденция 700мс, один
  прогон, один tab; серверный deadline — верхняя граница.
- `inference.read` loose-форма: непотребляемая глубина не
  валидируется — ГИБКОСТЬ по закону data-driven; потребляемый срез
  закрыт и покрыт тестами (пропажа controls/identity — MISMATCH).
- Мульти-вкладка: каждая вкладка — независимый клиент со своей
  сессией (закон); два параллельных чата двух вкладок — это два
  честных прогона двух сессий, не конфликт.

## G. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/api/gateway/contracts.ts frontend/src/api/gateway/validators.ts frontend/src/api/gateway/client.ts frontend/src/features/chat/useChat.ts frontend/src/features/chat/Chat.tsx frontend/src/app/composition/App.tsx frontend/src/app/composition/styles.css frontend/tests/fixtures/chat_send_ok.json frontend/tests/fixtures/chat_send_unknown_argument.json frontend/tests/fixtures/chat_send_bad_messages.json frontend/tests/fixtures/chat_send_no_session.json frontend/tests/fixtures/run_get_failed.json frontend/tests/fixtures/run_get_no_match.json frontend/tests/fixtures/run_cancel_terminal.json frontend/tests/fixtures/model_list_ok.json frontend/tests/fixtures/model_states_ok.json frontend/tests/fixtures/inference_read_ok.json frontend/tests/fixtures/manifest.json frontend/tests/contract/validators.test.ts frontend/tests/integration/Chat.test.tsx frontend/tests/integration/Shell.test.tsx frontend/README.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-298-frontendweb-report.md
git status --short
git commit -m "iter-298-chat: Phase 3 row 4 — the Chat entry over the run family (the bounded observation, the compact inference projection, Chat at the rail's head)"
git push
```

Delta-архив: `canonsim_iter-298-chat_2026-10-01.zip` (BASE_COMMIT
`d40c1df…`, изменённые/созданные пути — ровно 27 (13 изменённых + 14 созданных), удалений нет),
приложен к сессии + прямая ссылка и md5 в чате. Снимки живого
closure приложены к сессии (3 PNG).
