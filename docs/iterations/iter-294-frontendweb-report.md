# Отчёт итерации iter-294 — frontendweb: Phase 3, первый ряд
# (shell/nav + session lifecycle)

> Ваш приказ: «продолжай работы по фронтенду, над теми частями что
> логичнее всего сейчас провести а не откладывать». Развилка из
> отчёта iter-293 имела три ветки: стриминговое допуск (SSE —
> сначала бэкенд-ряд и отдельный допуск), тулинг-поле CI-строки
> (§8 — трогать CI только с вашим звонком) и Phase 3 вертикальный
> срез. Выбран срез: из его строк (shell/nav, connection state,
> Chat/Inference, Settings, Observatory entry, lifecycle/error/
> reconnect) ровно ДВЕ не требуют ни новых gateway-контрактов, ни
> бэкенд-рядов — shell/nav и жизненный цикл сессии. Они и
> высажены: это фундамент, на который смонтируется каждая
> следующая поверхность Phase 3.

## A. Сначала: KI#109 — зеркало GitHub было в наполовину применённом
## состоянии

Свежий клон HEAD `6c614ce` (коммит «iter-291..293») дал 2 красных
теста: docguard красный на 1462-строчном REDOT_ENGINE_INDEX.md и
старый test_shell_contract, проверяющий redot-бинарь в лаунчере.
Диагноз — тот же класс, что KI#108, но на зеркале: коммит внёс
доки iter-291..293, а 16 записанных удалений D-245 в коммит не
попали (последний коммит, трогавший индекс — iter-237). Ваше
локальное дерево их имеет (iter-291 верифицировал 2529+1);
GitHub — нет. По §5 (баг → KI → фикс) открыт KI#109 и закрыт в
ту же итерацию: 16 путей переисполнены в песочнице, сьюта
восстановлена до заявленных **2529 passed + 1 skipped**, ruff /
docguard / topology --check чисты. Дельта несёт их в
DELETED_PATHS.txt; в git-блоке §12.3 они перечислены отдельной
секцией (для зеркала — обязательны, для вашего локального дерева
— уже применены, пропустите).

## B. Что высажено (7 кодовых путей, все — только по существующим
## швам)

| Путь | Что это |
|---|---|
| `features/shell/Shell.tsx` | навигационная поверхность (§7 «Shell/navigation»): реестр панелей, переключение, **монтируется только активная панель** — boundedness; переключение сбрасывает локальное presentation-состояние панели (gateway остаётся единственной истиной) |
| `features/session-lifecycle/useSessionLease.ts` | hook lease-цикла: attach под CAS- guard'ом ревизии, detach под lease-guard'ом; **G4 — ноль автоповторов**: каждый явный try минает свежий `client_request_id` |
| `features/session-lifecycle/SessionLifecycle.tsx` | поверхность: честное замыкание REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED (§8), вердикт-лейн рендерит имя отказа сервера дословно |
| `app/composition/App.tsx` + `styles.css` | корень монтирует Shell с 4 панелями: Session (новая), Gateway, Load probe (S0-4 инструмент), Trajectory |
| `tests/integration/SessionLifecycle.test.tsx` | 5 интеграционных тестов (по живым фикстурам session_get_ok / session_attach_ok / session_attach_stale_revision) |

Запрещённые коллапсы, которых здесь нет: `click !== success`
(вердикт-лейн называет исход дословно); `selected !== loaded`
(OBSERVED-карта — ре-рид корня, не оптимистичное эхо; рассинхрон
карты и вердикта до ре-рида — это и есть UI); lease живёт только
в памяти таба (никакого storage); TRANSPORT никогда не
рендерится как «rejected».

## C. Проверка

- **Фронтенд**: tsc чисто; **vitest 59/59** (54 + 5 новых);
  production build собран; все 8 правил architecture guard зелёные
  (новые файлы под их юрисдикцией: Shell не импортирует ни одной
  фичи — панели приходят пропсами из корня; SessionLifecycle
  касается gateway только через типизированный клиент).
- **Python**: 2529 passed + 1 skipped (после KI#109-фикса),
  ruff / docguard / topology --check чисты. Ноль изменений
  Python-кода.
- **Живой прогон против настоящего gateway** (скрипт вне репо,
  Rule 9): `session.attach` OK (конверт rev 1, lease 30.0, токен),
  OBSERVED ре-рид `attached=true`, устаревший писатель →
  `REJECTED STALE_REVISION` с точной причиной, `session.detach`
  OK (конверт rev 2), повторный detach с освобождённым lease →
  `REJECTED LEASE_EXPIRED`. Каждая ветка, которую рендерит
  поверхность, подтверждена живым проводом.

## D. Открытие для следующих рядов

`app.status` на живом app-gateway перечисляет СЛОВАРЬ ОПЕРАЦИЙ
шире сид-шестёрки: `model.load/list/inspect/unload/states`,
`inference.read/update`, `chat.send`, `observatory.read/runs`,
`run.start/get/cancel`, `backend.settings[.update]`. Значит
оставшиеся поверхности Phase 3 (Chat/Inference, Settings,
Observatory entry) **не заблокированы бэкендом** — их итерации
это зеркало контрактов (contracts.ts + validators.ts по живым
фикстурам) + поверхность + тесты.

## E. Границы / следующий шаг

- SSE/стриминговое допуск — по-прежнему за отдельным допуском:
  сначала gateway-контракт (бэкенд-ряд), потом адаптер за
  типизированным клиентом (§5 admission order).
- CI-строки тулинг-поля и Playwright мульти-таб smoke —
  запаркованные строки, ваш звонок.
- Композиция «монтируется только активная панель» — осознанный
  boundedness-выбор: повторный вход в панель Trajectory
  перечитывает хвост (возможно через RESYNC) — честно, никогда
  молча.
