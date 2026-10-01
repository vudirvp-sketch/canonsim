# Отчёт итерации iter-300 — frontendweb: MODELS ENTRY
(Phase 3, шестой ряд: зеркало модельного семейства над существующими
model.list/model.states/model.load/model.unload + тремя model-видами
работ run.start; Models в рейле сразу за Inference)

Вызов владельца: «продолжай работу над фронтендом» — делегированный
вызов того же класса, что открыл iter-294..299 (D-198 intake). Ряд
выбран по собственному порядку следующих рядов STATUS («the next
frontend rows the owner's call: the Models surface (the family's
load/unload/import mirror), the Settings secondary nav…» — Models
назван первым; отчёт iter-299 повторил тот же порядок). Класс риска:
R2 (frontend-local; ноль Python, ноль canon, INV-1..5 не тронуты, LOG
нетронут). BASE_COMMIT `97ba5ed`.

## A. Что высажено (23 кодовых/тестовых пути + 6 доковых — один
когерентный минимальный срез, сверх мягкого лимита 3–5, освоено в
worklog)

- **Контракт-зеркало** (`frontend/src/api/gateway/
  {contracts,validators,client}.ts`) — СЕМЬ существующих операций,
  ни одного нового маршрута (§3):
  - MODEL_WORK_KINDS — потребляемый срез словаря видов работ
    реестра (model.fetch/model.import/model.digest — композиция
    приложения регистрирует digest+import безусловно, fetch с
    инжектированным fetcher); ПОЛНЫЙ словарь реестра — данные
    бэкенда, никогда не перекодируется (runStartResult.work —
    строка, эхо реестра);
  - аргументы run.start ЗАКРЫТЫ ПО ВИДУ на шве (union
    ModelRunStartInput: fetch — url + необязательный logical_name;
    import — список абсолютных путей; digest — logical_name) —
    чужой ключ/неверный тип есть собственный DOMAIN_REJECTED вида
    работы, рендерится дословно;
  - общая форма допуска model.load/model.unload (deadline_seconds/
    execution_id/logical_name/state: STARTING/work — буквальный
    enum двух операций);
  - документы ПРОГРЕССА (fetch: downloaded_bytes/logical_name/
    total_bytes|null — «total неизвестен» честен, никогда не
    угадывается; import: logical_name/file_index/file_count/
    copied_bytes/total_bytes) и ПЯТЬ результатов работ на
    потребительской глубине (fetch: location/logical_name/
    size_bytes/url; import: imported[]+count; digest: chunks/
    content_digest/logical_name/size_bytes; load:
    logical_name/location/reply/state: ACTIVE; unload:
    logical_name/reply/state: EVICTED) — reply остаётся
    z.record(...,unknown), данные бэкенда;
  - клиент modelLoad/modelUnload/runStart — свежий
    client_request_id на каждую явную попытку (G4).
- **Хук** (`frontend/src/features/models/useModels.ts` (новый)) —
  состояние поверхности:
  - два сеанс-свободных чтения на монтирование (model.list +
    model.states) + явный refresh; без поллинга;
  - каждый диспатч — РАБОТА: общий dispatchRun (сторож ОДНА
    работа в моменте → лейн DISPATCHING → четыре честных лейна:
    IN_FLIGHT/REJECTED/TRANSPORT/MISMATCH); лейн возвращается
    вызывающему — форма fetch/import ПОТРЕБЛЯЕТ черновик ТОЛЬКО
    при допуске (REJECTED/TRANSPORT сохраняет черновик: явное
    восстановление пользователя — правка + повторный диспатч,
    никогда не перепечатанный URL);
  - ограниченное наблюдение: ОДИН поллер (фиксированные 700 мс),
    мёртв на терминале/TRANSPORT/размонтировании, re-poll явен
    (G4); прогресс сужается по виду работы (чужая форма — честный
    UNRECOGNIZED, никогда не принуждение);
  - терминал запускает РОВНО ОДНО перечитывание контекста —
    замыкание OBSERVED-базы (приземлившийся файл видит СЛЕДУЮЩИЙ
    скан; лестница покоится в собственной истине), никогда
    поллинг;
  - cancel — правдивый ЗАПРОС (§12.3): свежий ключ, исход дословно,
    поллинг ПРОДОЛЖАЕТСЯ до собственного терминала работы.
- **Поверхность** (`frontend/src/features/models/Models.tsx`
  (новый)) — регионы:
  - **стрип**: models_root (ответ гейтвея, никогда локальная
    догадка — wb-10) · directory_state · счёт · слот ACTIVE
    (ответ владельца состояния загрузок) · явный refresh;
  - **список обнаружения** — закон §20 как хребет: чип ряда —
    СОБСТВЕННЫЙ ответ model.states для ЭТОГО имени (объединение по
    logical_name; DISCOVERED, когда владелец не трогал — файл на
    диске не доказывает НИЧЕГО: discovered ≠ selected ≠ loading ≠
    active), маркер ACTIVE свой канал, сильная идентичность
    («sha256 …» или «not computed» + аффорданс), MISSING ≠ EMPTY ≠
    NO MODELS — три разных честных состояния, никогда пустота;
  - **панель прибытия**: форма fetch (гейт допуска над чистой
    строковой normalize-закономерностью — срабатывает ДО любой
    сети: занятое имя/.part-остаток rejected на допуске, никогда
    посреди полёта) + форма import — честная веб-форма: АБСОЛЮТНЫЕ
    пути текстом, по одному на строку (браузер скрывает локальные
    пути — нативный проводник есть собственная забота Tauri-ряда,
    стоячая граница, названная в примечании, никогда молча
    подделанная);
  - **аффорданс идентичности §9** — digest RUN (честное длинное
    плечо для мульти-ГБ файла: отменяемо, наблюдаемо;
    синхронный model.inspect остаётся бэкенд-поверхностью — один
    HTTP-запрос на минуты был бы замороженным UI, никогда здесь);
  - **ран-лейн** — все стадии отдельны (DISPATCHING/IN_FLIGHT с
    прогрессом дословно/COMPLETED по виду работы/FAILED с
    диагностикой дословно/OTHER_TERMINAL/REJECTED/TRANSPORT/
    MISMATCH + cancel-исход); честные отключённые ворота: FAILED
    терминален (D-203, no re-selection), unload только при ACTIVE,
    всё выключено без сессии при работающих чтениях.
- **Маршрут**: Models в рейле сразу за Inference (голова группы
  RESOURCES — пара AI-семейства converse → control → ресурс) —
  §2.1 каноничное IA-дерево ПОПРАВЛЕНО (закон-владелец
  синхронизирован).
- **Стили**: ряды обнаружения/формы прибытия/ран-лейн; чипы
  лестницы MODEL — STATE-class токен-маппинги (ACTIVE→accent,
  SELECTED/LOADING/LOADED/VALIDATED→config, FAILED→error,
  DISCOVERED/UNLOADING/EVICTED→muted; ноль сырых литералов вне
  :root — V1-скан стража зелёный).

## B. Законы, которые несёт ряд

- **§20 (WORKBENCH_APP_LAW) — лестница Model**: file exists ≠
  valid ≠ selected ≠ loading ≠ loaded ≠ active; discovery — входные
  ворота (model.list прежде model.load/model.digest — захват
  фиксирует NOT_SENT-отклонение «not discovered», сам скрипт
  захвата ударился об это и починился); чип ряда никогда не
  угадывание обнаружением.
- **§9 — дисциплина идентичности**: logical_name + content identity
  (sha256) — материальная идентичность; size/mtime — дешёвый
  экран; location — путь, никогда идентичность. Сильная
  идентичность «вычисляется при необходимости» — в UI это RUN
  (model.digest), не блокирующий READ.
- **§12 — семейство runs**: identity-then-poll; дедлайны видов
  (load 330 с, fetch/import 3600 с, digest 60 с) — эхо на
  проводах, зафиксировано фикстурами; кооперативная отмена —
  запрошенный исход дословен, терминал работы — истина.
- **§8 — замыкание**: REQUESTED (клик/форма) → ACCEPTED
  (execution_id, STARTING) → EFFECTIVE (замороженные входы +
  собственный проход лестницы — SELECTED на допуске load) →
  OBSERVED (терминальный документ + РОВНО ОДНО перечитывание
  контекста) → PRESENTED (этой поверхностью). Запрещённые коллапсы
  названы и фальсифицированы тестами.
- **§16 — закон абсолютных путей**: import отклоняет относительный
  путь дословно («the .git/CWD-independence law (app §16) requires
  absolute paths») — захвачено живым.
- **G4**: никакого авто-ретрая; свежий ключ на каждую явную
  попытку; TRANSPORT после отправки = UNKNOWN; re-poll явен.
- **INV-4 не тронут**: браузер — клиент гейтвея над существующим
  loopback-биндингом; fetch-форма диспатчит run.start — сеть
  остаётся в трёх санкционированных модулях, ноль Python.

## C. §27 transfer records (метод D-246 — донор информирует, закон
CanonSim решает)

1. **Донор: собственный Chat-ряд iter-298** (внутренний прецедент):
   bounded-поллер (700 мс, мёртв на терминале/TRANSPORT/
   размонтировании, явный re-poll), матрица лейнов, правило
   «отмена — не завершение». Перенесено как форма наблюдения
   runs; прогресс-линия — НОВОЕ (Chat не имеет прогресса), её
   форма из собственного закона работ (контекстные отчёты
   context.progress). ДИСПОЗИЦИЯ: KEEP.
2. **Донор: Settings-ряд iter-296** (внутренний прецедент):
   «возвращённый документ — новая OBSERVED-база». Для runs аналог
   — терминал-триггерное РОВНО-ОДНО перечитывание (сам терминал не
   несёт нового discovery-документа; перечитывание и есть
   замыкание). ДИСПОЗИЦИЯ: KEEP.
3. **Донор: отсутствующий — нативный проводник файлов** (внешняя
   рамка wb-10 «просто открывающийся проводник»): НАБЛЮДЕНИЕ —
   браузер скрывает абсолютные пути (File System Access API не
   даёт путей); МЕХАНИЗМ проводника не переносим в чистый веб;
   ГРАНИЦА — импорт-форма берёт АБСОЛЮТНЫЕ ПУТИ ТЕКСТОМ (честная
   веб-форма), нативный пикер — Tauri-ряд (стоячая граница,
   названная); ФАЛЬСИФИКАТОР — относительный путь отклоняется
   дословно (захвачено живым + интеграционный ряд). ДИСПОЗИЦИЯ:
   BOUND (веб-форма сейчас; пикер — своё собственное допущение).

## D. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped (93.9s)
ruff check .                              → clean
python scripts/docguard.py                → clean (caps + state-layer)
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 214 passed / 12 files (=174+40)
frontend: npm run build                   → dist 15.43kB css / 433.26kB js
```

**Живой смок против ОБСЛУЖИВАЕМОЙ композиции** (реальные HTTP POST
по 127.0.0.1:8765, `build_app` + `transport.start()`, throwaway-корни
+ один фиктивный .gguf, managed-бэкенд пробует свободный порт) —
**24/24**:

- app.status OK + пять операций семейства зарегистрированы;
- model.list: пробный файл обнаружен;
- session.create OK;
- model.load: допуск OK (STARTING, deadline 330) → ран FAILED с
  наблюдаемой причиной ДОСЛОВНО («cannot spawn 'llama-server': [Errno 2]
  No such file or directory») → model.states покоится в SELECTED
  (брат §12.1: причина 'unavailable' — наблюдаемый=false, повторная
  загрузка легальна);
- model.unload на не-ACTIVE → DOMAIN_REJECTED дословно («is not
  ACTIVE (state: 'SELECTED') — nothing active to unload»);
- run.start model.digest → COMPLETED с реальным sha256 (сверен с
  hashlib по байтам файла);
- run.start model.import → COMPLETED (1 файл), байты приземлились
  (сверены), СЛЕДУЮЩИЙ model.list видит оба файла + digest едет на
  записи;
- run.start model.fetch с именем существующего файла →
  DOMAIN_REJECTED ДО любой сети (normalize — чистая строковая
  закономерность);
- run.start model.import с относительным путём → DOMAIN_REJECTED
  дословно (§16);
- идемпотентный дубль (тот же client_request_id + материал) →
  duplicate: true, та же execution-идентичность.

**Фикстуры** (11 новых, parity-law byte form, захвачены с реальной
композиции in-process, throwaway-корни models300): model_load_
start_ok, model_load_run_failed (честный FAILED-бенд этой среды),
model_states_selected (лестница SELECTED), model_unload_not_active,
model_digest_start_ok, model_digest_run_completed (реальный sha256),
model_import_start_ok, model_import_run_completed (реальная
локальная копия + живой прогресс в документе), model_list_after_
import (оба файла + digest на записи), model_fetch_exists,
model_import_relative_path. manifest.json синхронизирован.

**Контрактные ряды** (20 новых): формы допуска (shared load/unload
буквальный enum, run.start закрыт — work строка, deadline
присутствует); честный FAILED-бенд (failure_type _ManagedError,
диагностика дословно, §10-заморозка logical_name); лестница
SELECTED; digest (chunks 1, 64-hex); import (прогресс file_count 1,
copied==total, imported+count, заморозка paths как ОДНА
JSON-строка); ре-скан (оба имени, digest на probe, null на втором);
словари (9 состояний MODEL, 3 вида работ); три отклонения дословно;
фальсификаторы закрытого документа: сфабрикованный state, чужое
work-эхо, пропажа deadline, отрицательный downloaded, строковый
total, нулевой file_count, load-результат с state LOADED, чужой
член unload-результата, пропажа url в fetch-результате — все
MISMATCH.

**Интеграционные ряды** (17 новых + 1 Shell): ровно ДВА чтения на
монтирование без аргументов и сессии, никогда поллинг; §20-лестница
(probe SELECTED против second DISCOVERED — ответ владельца на имя,
не угадывание обнаружением; маркер ACTIVE свой канал; «strong
identity not computed» против «sha256 …»); MISSING и EMPTY
различны; поток загрузки (диспатч со свежим ключом + закрытыми
аргументами → поллинг → FAILED дословно → РОВНО ОДНО перечитывание
— listCount==2, statesCount==2, и не больше после паузы);
REJECTED-загрузка дословно (D-203 терминальность названа);
unload-ворота (ACTIVE вооружает, отклонение с наблюдаемым
состоянием дословно; без ACTIVE — disabled); поток import
(прогресс «file 1/1 · 30 B of 67 B» дословно, COMPLETED «1 file(s)
landed», ре-скан приземляет ряд, черновик очищен ТОЛЬКО при
допуске, провода: paths обрезаны/пустые убраны); fetch-отклонение
дословно с СОХРАНЁННЫМ черновиком; относительный путь дословно;
поток digest (sha256 полный, ре-скан сажает его на ряд, провода
закрыты); cancel (исход FAILED_TO_CANCEL дословно, поллинг
продолжается до терминала, execution_id на проводах); полл-TRANSPORT
(STALE в строке in-flight + UNKNOWN в алерте, цикл ОСТАНОВЛЕН,
re-poll ЯВНЫЙ возобновляет); диспатч-TRANSPORT с заметкой UNKNOWN;
без сессии всё отключено при работающих чтениях; ОДНА работа в
моменте (второй диспатч не выходит на провод).

## E. Границы / следующий шаг

- **Владелец-сайд для бендов приземления**: ACTIVE (load COMPLETED
  → маркер + чип accent) и EVICTED (unload COMPLETED) требуют
  загруженной llama.cpp модели; эта среда честно закрывает
  admission → FAILED → SELECTED-rest (снято дословно), import и
  digest закрыты ПОЛНОСТЬЮ живьём. Никогда не сфабриковано.
- **model.inspect не потребляется поверхностью** — названное
  решение (не молчаливое): синхронный READ хеширует весь файл в
  одном HTTP-запросе — минуты на реальной модели; digest RUN —
  честное плечо (отменяемо, наблюдаемо, дедлайн). inspect остаётся
  бэкенд/тестовой поверхностью.
- Следующие ряды фронтенда — вызов владельца: вторичная навигация
  Settings, streaming admission (SSE — сначала контракт gateway),
  acceptance matrix, коллапс DECISIONS; каждый — своя итерация.
- Отложено этим рядом (названо, не молча): нативный проводник
  импорта (Tauri-ряд), переупорядочивание/удаление файлов моделей
  (нет таких ops — будущий бэкенд-ряд, если владелец позовёт),
  контекстная осведомлённость §15 по фактам загруженной модели.

## F. Риски

- Прогресс fetch с total_bytes null («total unknown») — честный
  рендер без процента; при реальной загрузке на стороне владельца
  полоса покажет байты без знаменателя — это закон («never a
  guess»), не дефект.
- Два источника диспатчей (вкладка A и B): каждая вкладка —
  независимый клиент; ОДНА-работа-в-моменте — СТОРОНА ВКЛАДКИ
  (реестр execution допускает параллельные runs по сессиям);
  расхождение — факт представления, перечитывание явное.
- Ряд лестницы FAILED терминален в этой реализации (D-203,
  записанный пробел лестницы) — кнопка load честно отключена с
  подсказкой; разблокировка — будущий бэкенд-ряд, никогда
  молчаливая правка клиента.
- Форма import принимает любой текст — ворота на стороне бэкенда
  (абсолютность/существование/имя/занятость); клиентский «просмотр»
  был бы второй истиной, его нет.

## G. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/api/gateway/contracts.ts frontend/src/api/gateway/validators.ts frontend/src/api/gateway/client.ts frontend/src/features/models/useModels.ts frontend/src/features/models/Models.tsx frontend/src/app/composition/App.tsx frontend/src/app/composition/styles.css frontend/tests/fixtures/model_load_start_ok.json frontend/tests/fixtures/model_load_run_failed.json frontend/tests/fixtures/model_states_selected.json frontend/tests/fixtures/model_unload_not_active.json frontend/tests/fixtures/model_digest_start_ok.json frontend/tests/fixtures/model_digest_run_completed.json frontend/tests/fixtures/model_import_start_ok.json frontend/tests/fixtures/model_import_run_completed.json frontend/tests/fixtures/model_list_after_import.json frontend/tests/fixtures/model_fetch_exists.json frontend/tests/fixtures/model_import_relative_path.json frontend/tests/fixtures/manifest.json frontend/tests/contract/validators.test.ts frontend/tests/integration/Models.test.tsx frontend/tests/integration/Shell.test.tsx frontend/README.md docs/FRONTEND_UIUX_LAW.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-300-frontendweb-report.md
git status --short
git commit -m "iter-300-models: Phase 3 row 6 — the Models entry over the model family (the §20 ladder, the arrival pane, Models behind Inference)"
git push
```

Delta-архив: `canonsim_iter-300-models_2026-10-01.zip`
(BASE_COMMIT `97ba5ed…`, изменённые/созданные пути — ровно 29
(14 изменённых + 15 созданных), удалений нет), приложен к сессии +
прямая ссылка и md5 в чате.
