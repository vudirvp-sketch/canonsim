# Отчёт итерации iter-309 — frontendweb: CI + E2E + BOOT-SYNC

(три ряда одним заездом по прямому вызову владельца — «можешь все
сразу»; два OPEN-ряда матрицы iter-308 и её §C-кандидат закрыты)

Вызов владельца: «твоя задача: взять CI-ряд (additive-ветка для
ci.yml с vitest+tsc+build), или Playwright multi-tab smoke на основе
сегодняшнего драйва, или крошечный ряд boot-time OBSERVED-sync (один
session.get после create). можешь все сразу если позволит
контекстное окно и за 1 итерацию качественно сможешь провести все».
Класс риска: **R2 frontend-local + один R3-класс CI-ряд (D-249,
PCC-запись)**; §8 stop&confirm по CI-файлам погашен самим вызовом
(D-198: явный запрос владельца в активной сессии ЕСТЬ задача).
Совмещённый объём — санкция владельца (та же фраза), §2.3
зафиксирован в worklog. BASE_COMMIT `bca81ad`.

## A. Что исполнено

**(1) Аддитивный CI-ряд.** `.github/workflows/ci.yml`: новый job
`frontend` — checkout + setup-node 24 (LTS-линия, на которой
проверено; npm-кэш по `frontend/package-lock.json`) + `npm ci`
(lockfile — корень воспроизводимости) + `npm run typecheck`
(tsc --noEmit) + `npm test` (vitest, 256 рядов) + `npm run build`.
Python-job `test` **байт-идентичен** — аддитивный закон §11
(FRONTEND_WEB_LAW) исполнен буквально: ruff + pytest остаются
семантической верификацией, веб-проверки — новый слой, не замена.
Playwright-смок в CI **не** входит — спецификация ряда владельцем
(«vitest+tsc+build»); смок — owner-side/sandbox запуск.

**(2) Playwright multi-tab smoke** — `frontend/tests/e2e/
multitab.smoke.spec.ts` (4 ряда) + `frontend/playwright.config.ts`:
сьюит сам поднимает РЕАЛЬНУЮ композицию — гейтвей
(`scripts/workbench_app.py --no-backend`, выделенный порт 8788;
честный admission-закон: без llama.cpp бэкенд-опы не
зарегистрированы, и смок их не трогает) и Vite dev-сервер с
`GATEWAY_TARGET` на него. Готовность — TCP-уровнем (`port`, не
`url`): единственный 2xx-GET гейтвея — сам SSE-стрим (GET /op —
405 по построению), опрашивать его — фейковый маршрут, открывать —
фантомная подписка. `workers: 1` — один браузер, одно «переднее
кресло»: политика focused-tab и есть предмет теста. Ноль артефактов
(trace/screenshot off; каталоги раннера в .gitignore).

Ряды (все — над живым гейтвеем, 4/4 зелёные, ноль ошибок консоли
приложения):

- **два таба — независимые клиенты**: две сессии (различные 64-hex
  id), обе полосы **LIVE при буте** — живое замыкание бут-синка
  (create-только бут оставался DISCONNECTED — наблюдение §C
  iter-308, before-состояние ряда); rev/seq — из ПРОЧИТАННОГО
  документа;
- **focused-tab политика по живому проводу**: размытый таб —
  соединение РЕАЛЬНО закрывается (PAUSED/STALE, EventSource
  закрыт), рефокус — передозвон от курсора; симметрично для второго
  таба, стрим первого не тронут. Честная форма для headless:
  Chromium никогда не размывает фоновую страницу (обе всегда
  visible+focus — измерено), поэтому драйв диспатчит СОБСТВЕННЫЕ
  слушатели политики (window blur/focus + hasFocus) — тот же бэнд,
  что пинит jsdom-сьют (Trajectory.test.tsx), но здесь teardown и
  re-dial — настоящие, над живым стримом;
- **live push без рефреша**: три attach-опы через CAS-цикл (get
  ревизии → attach со свежим idempotency-ключом) прямо в гейтвей —
  строки приезжают в хвост фокус-таба по уже открытому стриму;
- **UNKNOWN-полоса**: кат сети убивает ТОЛЬКО attach в полёте (get
  перед ним проходит — запрос доказуемо отправлен, исход честно
  неизвестен): вердикт TRANSPORT с «outcome is UNKNOWN (no blind
  retry)» дословно; затем провод цел — явный retry ПОЛЬЗОВАТЕЛЯ
  (новая request identity внутри поверхности) → ACCEPTED →
  EFFECTIVE: ATTACHED.

Два закреплённых в конфиге факта об окружении (честные находки,
не дефекты продукта): Vite гасится по stdin-close, если CI ≠
"true" (собственный interop-флаг Vite — без него dev-сервер умирает
сразу после «available»); без `--host 127.0.0.1` Vite биндит
только ::1 — браузер на 127.0.0.1 получает connection refused
(IPv6/IPv4-сплит).

**(3) Boot-time OBSERVED-sync** — `frontend/src/state/session/
useTabSession.ts`: ровно ОДИН `session.get` сразу после успешного
create. Это первое наблюдение, НЕ ретрай (create уже ответил OK —
G4) и НЕ поллинг (ровно один read). Ланы чтения вынесены в одного
владельца (`readInto`) — бут-синк и явный refresh делят одни
семантики: TRANSPORT-провал → DISCONNECTED (успешных чтений нет —
никогда не фейковый LIVE, и create-баннер не переписывается),
доставленный отказ → STALE-with-reason. Побочные хуки: testid
`session-freshness`/`session-rev`/`session-seq` (полоса) и
`tail-seq`/`tail-rows` (хвост) — именованный потребитель — сам
e2e-ряд.

## B. Проверка (claim-пакеты, TEST_PLAN §9)

```
PYTHONHASHSEED=0 python -m pytest -q      → 2555 passed + 1 skipped
ruff check .                              → clean
python scripts/docguard.py                → clean
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 256 passed / 14 файлов
                                           (=252 + 4 новых BootSync)
frontend: npm run build (×2)              → 18.89 kB css / 446.04 kB js
                                           (байт-идентичные хэши;
                                           css-хэш = iter-308 — стили
                                           не тронуты, js = дельта
                                           бут-синка)
frontend: npm run e2e                     → 4 passed (5.0s) над
                                           живым гейтвеем + Vite +
                                           headless Chromium
```

Claim-пакеты:

1. **Бут-синк**: claim «после успешного create полоса сходится LIVE
   одним чтением». Оракул: текст полосы + ровно один POST
   session.get с id созданной сессии; фальсификатор: ноль
   session.get (RED до правки — проверено живьём в before-состоянии
   iter-308) или больше одного (поллинг — запрещён). Epistemic
   class: FACT (jsdom-ряд 4/4 + e2e-ряд 1 живьём).
2. **Смок**: claim «два таба независимы; focused-tab политика
   держит один стрим; live push доезжает без рефреша; UNKNOWN
   рендерится честно и закрывается явным retry». Оракул: DOM-платежи
   над реальным гейтвеем; фальсификатор: одинаковые id сессий,
   отсутствие STALE-полосы, не приехавшие строки, сфабрикованный
   вердикт. FACT (4/4).
3. **CI-ряд**: claim «веб-проверки зелёны из чистого npm ci в
   аддитивном job». Оракул: локальные эквиваленты (тот же набор
   команд) + YAML-форма job; честная граница: сам прогон GitHub
   Actions наступит на push владельца — записано как ожидаемое
   событие, не как исполненное доказательство. INFERENCE → станет
   FACT первым пушем в main.

## C. Границы / следующий шаг

- Playwright-смок НЕ в CI (спецификация ряда владельцем); если
  позже захочется CI-форму — отдельный ряд (браузер + Python в
  раннере, другая цена).
- Форма focused-tab-полосы в смоке — диспатч собственных слушателей
  политики (headless-ограничение, задокументировано в спеке);
  headed-прогон у владельца даст то же поведение средствами самого
  браузера.
- Ряды, оставшиеся в tooling floor: pixel-diff visual regression
  (последний). Прочие вызовы владельца без изменений: коллапс
  DECISIONS (37→30), B1/C4 из iter-303, replay-UI NOT-EXPOSED.
- Standing boundaries без изменений: SharedWorker, Tauri, PWA,
  Settings Appearance.

## D. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add .github/workflows/ci.yml .gitignore frontend/package.json frontend/package-lock.json frontend/playwright.config.ts frontend/src/app/composition/App.tsx frontend/src/features/trajectory/Trajectory.tsx frontend/src/state/session/useTabSession.ts frontend/tests/e2e/multitab.smoke.spec.ts frontend/tests/integration/BootSync.test.tsx frontend/tests/integration/Shell.test.tsx frontend/README.md docs/DECISIONS.md docs/FRONTEND_WEB_LAW.md docs/AGENT_NAVIGATION.md docs/TASKS.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/iterations/iter-309-cie2e-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-309-cie2e: the additive frontend CI job + the committed Playwright multi-tab smoke + the boot-time OBSERVED-sync (one session.get after create) - iter-308's two OPEN rows and the §C candidate closed in one owner-called sweep"
git push
```

Delta-архив: `canonsim_iter-309-cie2e_2026-10-03.zip` (BASE_COMMIT
`bca81ad…`, ровно 20 изменённых/созданных путей репозитория — все
перечислены в §D, плюс BASE_COMMIT.txt и DELETED_PATHS.txt (None)
внутри архива), приложен к сессии + прямая ссылка и md5 в чате.
