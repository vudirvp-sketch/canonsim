# iter-385 · composite1 — первая голова lab-composite-1: boundary surgery исполнена

**Класс риска:** R2 local-add (новый тестовый файл + реестр §9.2 +
райдеры; нуль строк рантайма, нуль строк гварда, DECISIONS не тронут —
33/35, R0–R2 не требуют записи класса, AGENTS §2.9).

**Вызов владельца:** стоящая директива «продолжай работы, открывай то
что сейчас важнее всего сделать, логичнее и качественнее на долгосрок.
я разрешаю» (2026-10-14). После iter-384 (коллапс) очередь владельца
состоит из его эксклюзивных вызовов; единственная OPEN-строка бэклога
— `lab-composite-1` (TASKS), единственная строка, открываемая
агентом без отдельных разрешений. Строку STATUS Next и называл.

## A. Что сделано

### A.1 Диагноз: что нового против уже приземлённого

§9.2 — карта композитных паттернов с двусторонней честностью: паттерн
с живым владельцем цитируется им (никогда не строится заново);
паттерн без владельца — только словарь. **Boundary surgery была
vocabulary-only** («возмущение сразу-за / сразу-внутри объявленной
границы зависимости — снаружи не может изменить результат»). Ближайший
родственник — мутации read-пар OCC (test_occidx) и поп-законы фолда
(test_gatefold) — но оба проверяют свои структуры на
ручных/стартовых состояниях.

Новая поверхность этой посадки (то, что НЕ было приземлено):
- **манифест** — граница зависимости, перечисляемая из СОБСТВЕННЫХ
  объявлений структур (фолд гейтов: объявленные ПАКОМ пары чтения —
  единственная буквально паковая граница; роллинг-индекс: движки
  вердикта position/crime_status; индекс распада: оси пака) —
  тестовая сторона никогда не строит вторую истину (D-024);
- **нагрузка** — собственные оси конверта плотности: три
  материализованных профиля (density-1 форма S=3/links=2/ρ=1.0/H=3;
  households S=2/H=6 — тёплое кольцо; cold-R-ρ S=4/links=4/ρ=0.5),
  каждый — РЕАЛЬНЫЙ годовой прогон на живом Симуляторе (138+
  событий: material cycle, talks, decay, rumors) — структуры
  сфолджены production-путём коммита ДО всякой хирургии;
- **кросс-структурная дискриминация** — хирургия внутри границы ОДНОЙ
  структуры не движет ответы ДРУГИХ (пер-структурная точность
  границы сразу по трём);
- **кросс-юнитовая локальность** — хирургия в юните i не движет
  скоупированные ответы юнита j (пересечение двух
  первых-именованных паттернов строки: locality injection ×
  boundary surgery);
- **порядок хирургии** — точный отрывок порядка фолдов `_commit`
  (apply_event → _last_change → decay → roll → gate), с явно
  не-управляемыми половинами (писатель/OCC/знание/реакции — у своих
  законов), канон-путь не тронут (INV-1).

### A.2 Пять законов (tests/test_labcomposite.py, все зелёные, ~0.25 с)

1. **THE MANIFEST LAW** — таблица `_declared` фолда РАВНА собственному
   перечислению спеков (нулевая вторая истина); каждая объявленная
   пара юнит-именована (закон скаффолда); классы хирургии
   не-вакуозны (вне-манифестные и гейт-онли пары существуют —
   батарея с зубами); профили реально разнообразны (7·S локаций).
2. **THE JUST-OUTSIDE LAW** — свёртка шести вне-манифестных хирургий
   (включая юнит 1 и игрока): ноль поп фолда, бакеты роллов
   неизменны, ответы распада неизменны (оба юнита), свёрнутый скан ==
   свежий == до-хирургии — МАНИФЕСТ НЕОБХОДИМ (снаружи не может
   изменить результат — слова §9.2).
3. **THE JUST-INSIDE GATE LAW** — объявленная пара чтения пинает
   РОВНО своих читателей (`_readers`-инверсия: popped ==
   readers ∩ confirmed), ре-дерирует == fresh, бакеты/распад юнита 1
   неизменны, скоупированный скан юнита 1 неизменен, полный скоуп
   ре-подтверждает — граница пер-структурная и юнит-локальная.
4. **THE VERDICT-MOVER LAW** — позиция NPC юнита 0: точные двойники
   (живое == свежее рождение — roll и decay, оба скоупа), юнит 1
   нетронут (бакеты, распад, скан), поп фолда == читатели пары
   позиции (манифест решает — p=100 муверы объявляют её).
5. **THE AXIS-MOVER LAW** — axis-prop NPC юнита 1 (локальность в обе
   стороны — роли юнитов меняются): пул распада ре-дерирует (живое ==
   свежее рождение, оба скоупа), бакеты роллов неизменны, фолд пинает
   iff манифест объявил пару (fatigue НЕ объявлена в шаблоне —
   дискриминация управляется данными, не хардкодом).

### A.3 Реестр §9.2 — живой владелец назван той же итерацией

Строка boundary surgery: vocabulary-only →
**`tests/test_labcomposite.py`** (полная форма посадки в колонке
владельца). Закон карты соблюдён: ближайший родственник (OCC
мутации) процитирован, не перестроен.

### A.4 Что осталось в строке (честный underdeliver)

Остальные головы ждут ПОТРЕБИТЕЛЕЙ (закон строки «WHERE a consumer
names itself»): observer noninterference (CONS-сторона), капсульная
половина causal debugging closure, specialized-kernel differential
(нативная строка ULT S8). Promotion ping-pong / adaptive sufficient
state — припаркованы до мезо/мировых строк. Строка остаётся OPEN.

## B. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` → **2676 passed + 27 failed +
  1 skipped** (прогон 127.8 с): множество провалов ИДЕНТИЧНО
  базлайну ДО правок имя-в-имя (`diff` пуст), +5 новых законов все
  зелёные (каждый ~0.25 с, тайминги сняты `--durations=5`);
- `ruff check .` → чист; `python scripts/docguard.py` → **ЧИСТ**
  (TASKS.md вернулся к 600/600 тремя круфт-пасами моей строки —
  повторы законов срезаны по D-024, владельцы: докстринг теста +
  этот отчёт; E31-заметка — владелец отчёт iter-344 §D, повтор
  срезан);
- `python scripts/topology.py --check` → чист;
  `python scripts/digest.py` → парсит;
- INV-1..5 не тронуты: нуль строк рантайма; хирургия — read-side
  верификация на слитых одноразовых прогонах (писатель не
  вызывается);
- Дизайн проверен ЗОНДОМ до написания законов (проба на живом
  материализованном паке: двойники и вне-хирургия подтверждены
  эмпирически до фиксации формы).

## C. Изменённые пути (6: 5 изменено + 1 создано)

tests/test_labcomposite.py (новый, 5 законов);
docs/TEST_PLAN.md (§9.2: boundary surgery → живой владелец);
STATUS.md (заголовок + Next); worklog.md (iter-385, iter-375
вытеснен); docs/TASKS.md (строка lab-composite-1 + леджер, iter-375
вытеснен, круфт-пас до 600/600); docs/iterations/
iter-385-composite1-report.md (новый).

Превышение soft-cap §2.3 (3–5) на одну позицию — класс
lab-строк (код законов + обязательные райдеры протокола);
отмечено в worklog.

## D. Риски

- **Хирургия на живых объектах** мутирует состояние сессии — батарея
  работает на слитом (drained) прогоне, дальше прогона нет; лог
  одноразовый (tmp), писатель не вызывается — INV-1 канон-пути не
  тронут.
- **_last_change управляется хирургией** — иначе двойник распада
  читал бы устаревшую базу (найдено пробой ДО законов; порядок
  `apply_event → _last_change → фолды` — это собственный порядок
  `_commit`, сверено с core/loop.py).
- **Пер-граничные двойники уже имели владельцев** (test_gatefold /
  test_rollidx / test_decayidx) — батарея НЕ перестраивает их
  (закон карты §9.2): она строит новую КОМПОЗИТНУЮ поверхность
  (манифест + конверт + дискриминация + локальность). Риск
  дублирования закрыт различием поверхностей.

## E. Дальше

`lab-composite-1` остаётся OPEN — головы ждут потребителей.
Очередь владельца после этой посадки: промоушен рантайма (D-250,
базис полон — отдельное разрешение), станционный хаускипинг
(m6-v6.2-зип), H-проза-фоллоу-апы (416-токенный вопрос + эстетический
вызов), replay-UI строка, W8, P1/P2/P3. Новая строка
производительности — только по свежему непрофильному A/B-датуму.

## F. Git-блок владельца

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add tests/test_labcomposite.py docs/TEST_PLAN.md STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-385-composite1-report.md
git status --short
git commit -m "iter-385-composite1: THE COMPOSITE BATTERY'S FIRST HEAD LANDED (lab-composite-1, R2 local-add, zero runtime change) - boundary surgery made executable, the TEST_PLAN 9.2 vocabulary-only row's live owner named the same iteration: tests/test_labcomposite.py (NEW, 5 laws, ~0.25 s each) over REAL 1y runs on three materialized density-envelope profiles (density-1 / households / cold-R-rho - the row's declared workload) - THE MANIFEST LAW (the dependency boundary enumerated from the structures' own declarations: the gate fold's pack-declared read pairs + the verdict movers + the decay axes, never a test-side second truth), the surgery riding the exact _commit fold-order excerpt (apply_event -> _last_change -> decay/roll/gate folds; the writer/OCC/knowledge/reaction halves owned by their own laws, INV-1 untouched), THE JUST-OUTSIDE LAW (surgeries outside every declared boundary move NOTHING - no pop, the buckets, the decay answers, the folded scan == fresh == pre-surgery: the manifest necessary), THE JUST-INSIDE GATE LAW (a declared pair pops EXACTLY its readers, re-derives == fresh, the other structures + the other unit untouched), THE VERDICT-MOVER LAW (a position move re-derives roll + decay, live == fresh birth, the other unit untouched), THE AXIS-MOVER LAW (the decay pool re-derives alone; the fold pops iff the manifest declares the pair - data-driven) - the cross-structure discrimination + the cross-unit locality composing the row's two first-named patterns; 2676 passed + 27 failed (the known T1 env set IDENTICAL name-by-name, zero new; the +5 laws all green), ruff+docguard+topology+digest clean, TASKS back at 600/600 after three D-024 cruft passes on the row; DECISIONS untouched at 33/35; INV-1..5 untouched"
git push
```
