# Отчёт итерации iter-290 — redot-removal (D-245)

> Ваш приказ: «удаляй redot, архив выше я еще не скачивал и не пушил
> его если что». Вторая половина директивы D-244 («а возможно и вовсе
> отказываемся») исполнена буквально; оговорка про неприменённый архив
> учтена в доставке (см. §E — ОДИН совокупный архив поверх той же базы
> e6789cf, он несёт и iter-289, и замещает его доставку).

## A. Что удалено — 16 путей (карточки SSI-N020 в D-245)

| Цель | Состав | Восстановление |
|---|---|---|
| `workbench/presentation/redot/` | 10 файлов: project.godot, themes/workbench_theme.tres, scenes/{main,shell}.tscn, scripts/{seam_proof,strings,observatory,gateway_client,shell,inference}.gd | git-история (закоммичено вплоть до e6789cf) + вербатим-пак `docs/frontendweb/archive/` (его `legacy-redot-reference/` и REDOT-доки) |
| `docs/REDOT_ENGINE_INDEX.md` | замороженный индекс движка (D-207/D-244) | git-история + `CANONSIM_REDOT_GODOT_AGENT_REFERENCE_INDEX.md` внутри пака |
| `scripts/visual_proof.py` | REDOT_EXE-раннер скриншот-пруфов (wb-1/wb-2) | git-история |
| `tests/test_visual_proof.py`, `tests/test_shell_proof.py` | гейтнутые пруф-пакеты (в CI всегда скипались — 8 из 9 скипов старого прогона) | git-история |
| `tests/test_shell_contract.py` | 23 негейтнутых теста контракта коммиченных .gd-файлов | git-история |
| `Workbench Setup.bat` | выбор папки Redot (--pick-redot) — цели больше нет | git-история |

Каждая цель закрыта карточкой `[GC: target=…; consumer_absence=…;
authority_absence=…; historical=…; recovery=…]` в D-245: потребительское
отсутствие просканировано (потребителями были только лаунчер, пруф-пакеты
и роутинг-доки — все перепривязаны/удалены в этой же итерации), владельцем
решения — ваш зов, история — фриз D-244. Инварианты: INV-1/2/3/5 не
тронуты (нулевое изменение канона, лог не тронут, логи/фикстуры не
удалялись), INV-4 не расширен (браузер ходит через Vite-прокси поверх
СУЩЕСТВУЮЩЕГО loopback-биндинга; лаунчер порождает процессы и не открывает
сокетов).

## B. Лаунчер перепривязан на веб-клиент (wb-10 сохранён)

`scripts/workbench_launch.py` переработан; `Workbench.bat` остался
двойкликом-нулём-команд:

- **ушло**: вся цепочка резолва Redot (скан релизной папки, персист
  launcher.json, автоскан Desktop, tk-пикер, флаги --redot-exe /
  --pick-redot / --no-redot);
- **пришло**: `resolve_npm()` — npm через PATH (паттерн CONTRACTS §5 D1:
  внешний тулчейн, одна точка резолва); при отсутствии
  `frontend/node_modules` лаунчер сам гоняет `npm install` (ваш закон
  «пользователь не должен вводить команды чтобы запустить или скачать
  что-либо!»); наблюдённый URL привязки гейтвея пробрасывается ребёнку
  как `GATEWAY_TARGET` (цель Vite-прокси — `-- --port` больше не
  рассинхронизирует клиент); `--open` поднимает браузер; `--no-frontend`
  — честная форма «только гейтвей» (тестовая/операторская);
- **дефект, найденный и починенный в итерации**: наивный SIGINT в npm
  осиротил его внуков (`sh -c vite` → node vite). Чайлд веба теперь
  стартует в собственной POSIX-сессии, останов групповая (`killpg`):
  живой прогон подтвердил — SIGINT → exit 0, оба ребёнка честно
  остановлены, ноль сирот. Windows ездит на собственной группе консоли;
- npm отсутствует на машине → честная заметка (поставь Node.js LTS с
  nodejs.org, либо руками: `cd frontend && npm install && npm run dev`),
  гейтвей при этом продолжает сервить — никогда фейковый «launched».

## C. Синхронизация роутинга и законов (минимальный по §18/D-244 состав)

`AGENT_NAVIGATION` (§1: строки presentation/redot, REDOT_ENGINE_INDEX,
строка Redot из §2 и §6 удалены; строка scripts/ переписана; §3 — гейт
лаунчера снят), `README.md` (карта репо, zero-command секция, веб-секция),
`FRONTEND_WEB_LAW.md` (scope fence: фриз ЗАКРЫТ удалением; §14 Phase 0 —
DONE; финальное правило), `CONTRACTS.md` §5 (баннер удаления — лендинг-ноты
сохранены как история), баннеры WORKBENCH_APP_LAW (§23.1 помечен DELETED),
LLAMA_CPP/VISUAL_SYSTEM_UI/FRONTEND_UIUX/WORLD_PRESENTATION (указатели на
engine facts сняты), `frontendweb/{README, FRONTEND_WEB_AGENT_CONTEXT}`
(§3/§5/§6: граница фриза закрыта, стадия REDOT DELETED, роут-строка
индекса удалена), `frontend/README.md`, `SSI_TOPOLOGY.md` + докстринг
`topology.py` (границы карты), запись docguard'а, `.gitignore` (строка
`.godot/`), комментарии в 6 модулях (scene_ir, clock, inference/__init__,
llama_process, workbench_app, test_managed_backend).

Глубокий re-homing тел законов (§23.1 и прочие Redot-разделы тел) остаётся
отложенным на фазы 3/4 — по собственному тексту D-244.

## D. Верификация

- `PYTHONHASHSEED=0 pytest -q`: **2529 passed + 1 skipped** (было 2556+9:
  −23 test_shell_contract, −8 гейтнутых скипов, −1 resolve_redot_exe-тест,
  −3 сетка лаунчер-тестов; новых — 10 в переписанном
  test_workbench_launch). junit-подсчёт: 2530 tests, 0 failures, 0 errors.
- `ruff check .` — чисто; `python scripts/docguard.py` — чисто;
  `python scripts/topology.py --check` — чисто.
- **Живой прогон лаунчера** (полный стек на свободном порту):
  bind-строка гейтвея → `GATEWAY_TARGET=http://127.0.0.1:<port>`
  проброшен → Vite ready ~150ms → корень приложения HTTP 200 →
  `POST /gateway/op app.status` через прокси отвечает реальным документом
  гейтвея (полный список операций) → SIGINT → exit 0, строки «the gateway
  stopped» + «the web frontend stopped», ноль сирот. (Шум `xdg-open
  ENOENT` в логе — безголовость песочницы: на вашей машине `--open`
  открывает браузер.)

## E. Доставка — ОДИН совокупный архив

Вы не применяли дельту iter-289 — поэтому этот архив построен от той же
базы **e6789cf** и несёт ОБЕ итерации (frontend-1 S0 + redot-removal).
Он **замещает** доставку iter-289: применяйте только его. Структура по
§12.1: `BASE_COMMIT.txt` (e6789cfb403ef0f6c142ab9fbed2989c891caef0) +
`DELETED_PATHS.txt` (16 путей) + изменённые/созданные файлы.

- Файл: `canonsim_iter-290-redot-removal_2026-09-29.zip`
- Прямая ссылка: <tmpfiles-ссылка подставлена в чате>
- md5 / размер: <в чате>
- Self-check: список путей архива == `git status --porcelain -uall`
  против базы (проверено скриптом сборки).

## F. Риски и честные границы

1. **Node.js на вашей машине**: если не установлен — Workbench.bat
   выведет заметку (гейтвей при этом жив); один раз поставить Node.js LTS
   с nodejs.org, и нуль-командная форма снова полная. Первый запуск после
   установки сам выполнит `npm install` (минуты на холодном кэше).
2. **DECISIONS.md — 36 строк при капе 30**: коллапс по вашему явному зову
   (закон D-034/D-185; прецедент iter-176 «31→30»).
3. **Глубокий re-homing тел законов** (Redot-разделы WORKBENCH_APP_LAW и
   др.) — отложен на фазы 3/4, по тексту D-244.
4. **Визуальный пруф веба** — браузерные скриншоты iter-289 остаются
   действующим доказательством клиента; тулинг-пол пака (Playwright-класс)
   откроется пост-S0.

## G. Дальше — ваши зовы

1. **S0-green ревью** (четыре критерия iter-289) — ваш осмотр скелета.
2. Пост-S0 гейты (по паку): стриминговая политика (SSE/WebSocket),
   тулинг-пол CI, полная acceptance-матрица.
3. Коллапс DECISIONS (36→30) — по вашему зову.
4. Вертикальный срез Workbench (Phase 3 пака).

## Владельческий git-блок (§12.3)

Один коммит (архив несёт обе итерации; примените файлы архива поверх
репозитория в состоянии e6789cf):

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add .gitignore README.md Workbench.bat STATUS.md worklog.md scripts/workbench_launch.py scripts/workbench_app.py scripts/docguard.py scripts/topology.py workbench/scene_ir.py workbench/application/clock.py workbench/application/inference/__init__.py workbench/platform/llama_process.py tests/test_workbench_launch.py tests/test_workbench_app.py tests/test_managed_backend.py docs/DECISIONS.md docs/AGENT_NAVIGATION.md docs/CONTRACTS.md docs/FRONTEND_WEB_LAW.md docs/WORKBENCH_APP_LAW.md docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md docs/VISUAL_SYSTEM_UI.md docs/FRONTEND_UIUX_LAW.md docs/WORLD_PRESENTATION_LAW.md docs/blueprint/phases.md docs/SSI_TOPOLOGY.md docs/TASKS.md docs/frontendweb/README.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/iterations/iter-289-frontendweb-report.md docs/iterations/iter-290-redot-removal-report.md frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/vite.config.ts frontend/index.html frontend/README.md frontend/src/app/composition/main.tsx frontend/src/app/composition/App.tsx frontend/src/app/composition/styles.css frontend/src/api/gateway/contracts.ts frontend/src/api/gateway/validators.ts frontend/src/api/gateway/client.ts frontend/src/features/gateway-status/GatewayStatus.tsx frontend/src/features/trajectory/Trajectory.tsx frontend/src/features/trajectory/useLiveTail.ts frontend/src/features/trajectory/VirtualList.tsx frontend/src/features/trajectory/virtualization.ts frontend/src/state/session/useTabSession.ts frontend/tests/unit/virtualization.test.ts frontend/tests/contract/client.test.ts frontend/tests/contract/validators.test.ts frontend/tests/integration/Trajectory.test.tsx frontend/tests/fixtures/app_status_ok.json frontend/tests/fixtures/manifest.json frontend/tests/fixtures/session_attach_ok.json frontend/tests/fixtures/session_attach_stale_revision.json frontend/tests/fixtures/session_create_duplicate_request.json frontend/tests/fixtures/session_create_ok.json frontend/tests/fixtures/session_events_ok.json frontend/tests/fixtures/session_events_resync_required.json frontend/tests/fixtures/session_events_unknown_argument.json frontend/tests/fixtures/session_get_domain_rejected.json frontend/tests/fixtures/session_get_ok.json
git rm workbench/presentation/redot/project.godot workbench/presentation/redot/themes/workbench_theme.tres workbench/presentation/redot/scenes/main.tscn workbench/presentation/redot/scenes/shell.tscn workbench/presentation/redot/scripts/seam_proof.gd workbench/presentation/redot/scripts/strings.gd workbench/presentation/redot/scripts/observatory.gd workbench/presentation/redot/scripts/gateway_client.gd workbench/presentation/redot/scripts/shell.gd workbench/presentation/redot/scripts/inference.gd docs/REDOT_ENGINE_INDEX.md scripts/visual_proof.py tests/test_visual_proof.py tests/test_shell_proof.py tests/test_shell_contract.py "Workbench Setup.bat"
git status --short
git commit -m "iter-290-redot-removal: D-245 — the Redot presentation layer deleted (16 paths, owner's call), the zero-command launcher re-pointed to the web dev server; carries the unapplied iter-289 frontend-1 S0 build (one cumulative delta over e6789cf)"
git push
```

(Хотите два коммита в истории — примените сначала старый архив iter-289,
закоммитьте его, затем этот; конечное состояние идентично.)
