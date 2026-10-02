# Отчёт итерации iter-305 — SSE-контракт гейтвея
(FRONTEND_WEB_LAW §5, шаг 2 порядка допуска: явный контракт
одностороннего стрима — бэкенд первым)

Вызов владельца: «твоя задача сейчас продолжить работу по
фронтенду, можешь начать работы по SSE-контракту гейтвея и прочему!
помни что мне не нужны костыли и работа ради работы! мне нужен
качественный код и решения на долгосрок! работающий как швейцарские
часы, масштабируемый и изменяемый при желании!» — вызов открывает
строку, которую STATUS держал следующей в очереди фронтенда:
«the streaming admission (SSE — the backend gateway contract
first)». Класс риска: R4 (изменение публичного API — новый внешний
контракт-поверхность гейтвея; D-248 с PCC-записью; INV-4 НЕ
тронут: новый сетевой модуль не появился — SSE-рука едет по
санкционированному inbound-биндингу `transport.py`, ядро осталось
socket-free). BASE_COMMIT `43dd2f1`.

## A. Что было до (и почему именно такой порядок)

FRONTEND_WEB_LAW §5 фиксирует порядок допуска стриминга:

```text
1. POST /op only (landed; S0)
2. explicit gateway contract for a one-way stream + tests   ← ЭТОТ РЯД
3. browser adapter behind the typed gateway client          ← следующий
4. focused-tab / budget policy in UI                        ← едет с 3
```

Закон прямо запрещает реализовать 3–4 раньше 2: браузерный
адаптер без контракта гейтвея — импровизация агента, не механизм.
Поэтому итерация — БЭКЕНД-ФЁРСТ: два модуля, контракт между ними и
24 теста-строки, фиксирующие контракт исполняемо. Семантический
владелец стриминга — WORKBENCH_APP_LAW §13 (строка «live events»,
до сих пор `[CONTRACT]`): её словесные законы — «canonical
execution data is never silently dropped», «overflow is bounded
and observable», «reconnect → replay OR RESYNC_REQUIRED», «a
client disconnect never implicitly cancels unrelated execution»,
«SSE is the default one-way event direction» — стали исполняемыми
инвариантами.

## B. Ядро: подписки в socket-free гейтвее (gateway.py)

`Gateway.subscribe(session_id, since_sequence)` — семантическая
половина, в существующем стиле ядра:

- **Двойственный ответ §13, тот же, что у `session.events`:**
  REPLAY (окно удержанных событий после курсора) или RESYNC
  (снимок текущего состояния, когда курсор выпал из удержания) —
  и в обоих случаях живой хвост дальше. Оба документа-ответа
  побайтово те же формы, что POST-операция уже отдаёт.
- **Gapless-граница replay/live — по построению:** `subscribe`
  выполняется под тем же грубым dispatch-lock, под которым `_emit`
  дописывает события. Replay кончается на `last_sequence`, живая
  очередь начинается с `last_sequence + 1` — ни пропуска, ни
  дубликата, ни гонки. Это проверено тестом на непрерывность
  последовательностей.
- **Ограниченный буфер на подписчика:** `stream_buffer_events`
  (по умолчанию 64) в `GatewayConfig`. Переполнение — наблюдаемое:
  очередь сначала ВЫТОКАЕТ в порядке (потребитель получает своё),
  затем канал закрывается терминалом `StreamOverflow` — ничего не
  молча теряется: удержанный поток (каноническая запись) не
  трогается вообще.
- **Инвариант-закон конфигурации:** `stream_buffer_events <=
  retention_events`, отказ на конструировании (не clamp!). Плата:
  переполнивший потребитель отстаёт не больше буфера, удержание
  хранит не меньше — его реконнект по последнему полученному id
  ВСЕГДА попадает в replay, никогда во второй resync. Это
  проверено тестом на обеих границах (2≤8 и 4==4).
- **`close_subscriptions()`** — поверхность ограниченного
  останова: каждая живая подписка получает терминал SHUTDOWN,
  писатели просыпаются по condition (не по границе heartbeat),
  пишут честный `stream.close` и выходят. Сессии и канон —
  нетронуты.
- **Дисциплина блокировок:** `_push`/`_close` — под блокировкой
  гейтвея, берут только condition (гейтвей → cond, односторонняя
  вложенность); `next_item`/`close` — condition без гейтвей-лока.
  Обратного порядка нет нигде — дедлок невозможен по построению.

## C. Доставка: GET /events (transport.py — санкционированный сокет)

- **Маршрут:** `GET /events?session_id=…&since_sequence=N`, плюс
  заголовок `Last-Event-ID` (стандарт SSE-реконнекта браузера) как
  fallback-курсор; явный параметр выигрывает. Матрица маршрутов
  честная: GET /op → 405, POST /events → 405, неизвестный GET →
  404 (было 405 на всё — размытая семантика, теперь точная).
- **Пре-стримовые guard'ы — транспортные 4xx JSON:** отсутствие
  session_id, мусорный/отрицательный since_sequence,
  продублированный параметр (никакого first-wins) → 400;
  auth_required → 403 `STREAM_AUTH_REQUIRED` — стрим НЕСЁТ
  креденциал некуда (auth-материал никогда в URL — закон), так что
  аутентифицированные exposition-ряды владеют своим будущим
  стрим-контрактом.
- **Семантический отказ едет в стриме:** неизвестная сессия — это
  ОБРАБОТАННЫЙ запрос (ядро ответило DOMAIN_REJECTED) → HTTP 200,
  text/event-stream, ОДИН фрейм `stream.rejected` с вердиктом из
  закрытого словаря, затем закрытие соединения. Раздел
  доставки/семантики §8 держится и на стрим-поверхности: никогда
  не сфабрикованный 4xx для семантического ответа.
- **Фреймы:** `stream.open` (документ режима: mode/session_id/
  last_sequence, RESYNC добавляет resync/retained_from/snapshot —
  те же поля, что POST-ответ); события — `id: <sequence>`, `event:
  <тип>`, `data: <канонический JSON>` — **побайтово тот же
  canonical_json, который `session.events` отдаёт в replay** (D4-
  дисциплина; паритет — доказательство контракта, стрим — это
  ДОСТАВКА того же потока, не второй источник событий);
  heartbeat'ы `: keep-alive` (комментарии, EventSource их
  игнорирует, провод живой); терминалы `stream.overflow` /
  `stream.close` (без id — контрольный фрейм не двигает курсор
  реконнекта).
- **Запись — bounded:** сокет-таймаут на запись
  (`stream_write_seconds`, по умолчанию 30), heartbeat задаёт
  такт пробуждения цикла; писатель — СОБСТВЕННЫЙ handler-тред
  запроса (один тред на стрим, никаких пулов — проверено подсчётом
  тредов).
- **Измеренный факт, честно задокументированный в коде:**
  graceful-close клиента НЕ шлёт RST — записи уходят в буфер ОС
  «в пустоту» без ошибки. Значит, надёжный конец умершего
  потребителя — переполнение его ограниченного буфера (терминал
  OVERFLOW), а не отказ записи. Тест кодирует ровно это: клиент
  исчез → очередь заполнилась → писатель вышел bounded → сессия
  продолжила принимать/эмиссить/реплеить для следующего
  подписчика (закон §13 «disconnect не отменяет чужую работу»).
- **Останов bounded:** `stop()` → сигнал stopping →
  `close_subscriptions()` (все писатели просыпаются, пишут
  честный `stream.close`, выходят) → shutdown → server_close →
  join(5s). Проверено с тремя живыми стримами и heartbeat=30
  (который никогда не тикал): все три получили фрейм + EOF за
  доли секунды.

## D. Тестовый пакет (tests/test_sse_stream.py, 24 строки, NEW)

Слои: словари (закрытость всех множеств) → конфиг-закон → ядро
(rejected-лейн, паритет окна с session.events, resync-документ ==
POST-ответ, gapless-граница, fan-out на N подписчиков, overflow
drain-then-terminal + идемпотентность терминала + неприкосновенность
retained-потока, always-replay-инвариант, idempotent-close,
shutdown-wake ≤ мгновения, disconnect-закон) → провод (200 + тип +
no-store; open-фрейм; replay-фреймы с побайтовой парой canonical
JSON; пустой replay при курсоре за историей; живой push после
открытия; Last-Event-ID fallback + явный параметр побеждает +
мусорный заголовок → 400; вся матрица guard'ов; auth 403 без
открытия канала; heartbeat-комментарий по такту; bounded-stop с
тремя живыми стримами; один-тред-на-стрим + bounded-конец
умершего потребителя). Читатель — настоящий http.client по
настоящему сокету, построчное чтение фреймов: между тестом и
проводом нет моков.

Существующий тест resync получил `stream_buffer_events=1` в
конфиге — новый закон конфигурации сделал старый малый-retention
конфиг неполным; сами assertions не изменены (тест не ослаблен).

## E. Живая проверка над настоящей композицией

`python scripts/workbench_app.py --no-backend` (полный реестр 21
ops) → стрим открыт над реальным гейтвеем → `stream.open` +
replay-фрейм SESSION_CREATED → `session.attach` по другому
соединению → фрейм SESSION_ATTACHED ПРИШЁЛ в стрим (живой push
через настоящую композицию) → chat.send честно REJECTED
DOMAIN_REJECTED (нет бэкенда — закон честного допуска) →
побайтовая пара SSE-данных с `session.events` — OK.

## F. Полный проверочный пакет

| Проверка | Результат |
|---|---|
| `pytest` (PYTHONHASHSEED=0) | **2555 passed + 1 skipped** (было 2531+1; +24) |
| `ruff check .` | clean |
| `python scripts/docguard.py` | clean (caps: worklog 10/10, TASKS-леджер 10/10) |
| `python scripts/topology.py --check` | clean (карта обновлена в той же итерации: transport.py reads += contract.py — закон живой карты) |
| `npm test` (vitest) | 222 passed (фронтенд не тронут) |
| `npm run typecheck` | clean |
| `npm run build` | 1.75s |
| live smoke над реальной композицией | пройден (см. §E) |

## G. Чего здесь НЕТ (границы ряда, по закону о scope)

- **Браузерного адаптера** (шаг 3): EventSource за типизированным
  gateway-клиентом, zod-валидаторы фреймов, политика focused-tab —
  следующий ряд, собственный допуск. Закон порядка допуска — не
  декорация: адаптер без контракта = импровизация.
- **Токен-дельт бэкенда** (§13 «backend stream»): сегодня chat —
  блокирующий вызов порта внутри воркера; дельта-уровень — будущий
  ряд со своим потребителем.
- **Агрегатного cap'а на стримы:** thread-per-strim — собственная
  поза http.server (как и thread-per-connection у POST);
  документировано, а не выдумано политикой без потребителя.
- **Никаких изменений фронтенда** — ноль диффов в frontend/: клиент
  остаётся POST-only до своего ряда адаптера.

## H. Изменённые файлы

```text
workbench/api/gateway.py        — ядро подписок (+~320 строк)
workbench/api/transport.py      — SSE-биндинг (+~320 строк)
tests/test_sse_stream.py        — NEW, 24 строки пакета
tests/test_gateway.py           — конфиг resync-теста дополнен (1 строка)
docs/WORKBENCH_APP_LAW.md       — §13 LANDED + §5 skeleton
docs/FRONTEND_WEB_LAW.md        — §5 шаг 2 LANDED
docs/AGENT_NAVIGATION.md        — §1 строки workbench + frontend
docs/SSI_TOPOLOGY.md            — две api-строки карты (reads+owner)
docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md — stage map
docs/TASKS.md                   — леджер (iter-295 evicted)
docs/DECISIONS.md               — D-248 (R4 + PCC)
STATUS.md                       — шапка + Next step
worklog.md                      — запись iter-305 (iter-295 evicted)
docs/iterations/iter-305-sse-contract-report.md — этот отчёт
```

## I. Риски и откат

Риски: (а) новая публичная поверхность — смягчено закрытыми
словарями + 24 строками контракта + побайтовой парой с
существующим POST-путём; (б) треды-писатели — bounded по
построению (heartbeat / write-timeout / overflow-терминал — три
независимых конца, все проверены); (в) блокировки — односторонняя
вложенность гейтвей→cond, обратного пути нет. Откат: git revert
одного коммита (никаких миграций — хранилищ нет, канон не тронут).

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add workbench/api/gateway.py workbench/api/transport.py tests/test_sse_stream.py tests/test_gateway.py docs/WORKBENCH_APP_LAW.md docs/FRONTEND_WEB_LAW.md docs/AGENT_NAVIGATION.md docs/SSI_TOPOLOGY.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md docs/DECISIONS.md STATUS.md worklog.md docs/iterations/iter-305-sse-contract-report.md
git status --short
git commit -m "iter-305-sse-contract: the SSE gateway contract landed (step 2 of the streaming admission - backend first)"
git push
```
