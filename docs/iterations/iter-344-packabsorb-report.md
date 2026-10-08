# iter-344 · packabsorb — проработка unified-пака v1.5: полезное впитано, долгоживущие законы припаркованы к их репо-потребителям, строки очереди открыты

**Вызов владельца (2026-10-08, дословно):** «перед началом
работ по: "E02/E31 → M2 → replay-UI → W8 → P1/P2/P3" я хочу
чтобы ты проработал архив canonsim_unified_agent_pack_v1_5.zip,
"впитал полезное", поставил задачи соответственные и "припарковал"
куда нужно законы, паттерны и всякое прочее что должно жить долго
и всегда (если должно)» — явный запрос сессии (D-198), вторая
половина того же сообщения: «твоя задача продолжить работу по
планам, можешь открывать любые задачи, наиболее логичные сейчас
и правильный для качества в долгосрок». BASE_COMMIT этой
итерации: `e183c64` (iter-343-doc4-lawrehome).

**llama.cpp не устанавливался** — проработка пака и парковка
законов это doc-строка; M2 (первая строка очереди, где живой
движок нужен) — станционная батарея, своя строка.

## A. Что сделано

### A.1 Пак прочитан целиком (12/12 файлов)

ROUTER → INDEX → QUICKSTART → CURRENT_STATE → MANIFEST → ULT
(1332 строки) → SCALE_TESTING_LAW (401) → CONS (431) → CDMT
(574) → TEXT2_DISPOSITION (186) → AUDIT_SOURCES → PACK_INTEGRITY.
Маршрут по собственному закону пака (ROUTER §0: не грузить всё
по умолчанию) был НАРУШЕН сознательно и один раз: задача владельца
именно «проработать архив» — полный проход и есть deliverable,
обычная работа дальше идёт по роутеру (один документ + нужная
секция).

### A.2 Свежесть проверена (закон пака §12: LIVE OWNER > PACK SNAPSHOT)

Пак снапшотирован на iter-337 / HEAD `2e54d39`; живой HEAD на
момент начала — `e183c64` (iter-343). Снапшот исторический;
устаревшие строки пака — таблица §B ниже. Закон работает: живой
владелец перечитан до любых действий (STATUS/TASKS/CONTRACTS/
TEST_PLAN), ни одна строка пака не перенесена в репо как текущая
истина.

### A.3 Припарковано (3 закона, каждый — к именованному репо-потребителю)

1. **Закон достаточности масштабных утверждений → TEST_PLAN §9.1.**
   Оси `E/L/R/F/ρ/K/H/Q (+B)`, пять классов достаточности
   (`UNEXERCISED / SEMANTIC-ONLY / LOCAL-SCALE / DENSITY-SCALE /
   TARGET-SCALE`, продвижение вверх — никогда молча), ядро
   «TEST PASS ≠ SCALE PROOF», три яруса оракулов (малый =
   byte-golden, средний = семантика+счётчики, большой =
   регенерированный дифференциал — никогда два независимо
   выдуманных приближения), минимальный scale-claim пакет (поверх
   §9's claim packet), семь именованных профилей нагрузки
   (locality-control … mixed-density), запрет fixture-hardcoding
   как механизма общности, метрическая валидность (чувствительность
   + приманка). Плюс СТОЯЩАЯ классификация: семейство farstead
   kiloyear (iter-335/336/337/338) = **SEMANTIC-ONLY** —
   горизонтное доказательство на разреженном авторском мире;
   ни одна строка репо не заработала LOCAL-SCALE и выше (это
   цель density-1). Потребители: density-1 (открытая голова
   очереди), мировой трек (плотные миры), любая будущая строка
   с «N×» в заявлении.

2. **Карта композитных proof-тест паттернов → TEST_PLAN §9.2.**
   14 паттернов (v1.5 ULT §17.4.1/§17.5), каждый с живым
   владельцем ГДЕ ОН ЕСТЬ: certificate quiescence = test_h9
   закон 1 (A/B байт-идентичность + заборы), derived-index
   poisoning = test_occidx (twin-agreement + resume rebuild),
   schedule permutation = test_composition (143-check решётка),
   mutation adequacy = mutation probe + census, workload-
   sufficiency gate = §9.1, reference/replay equivalence =
   T2 + OCC A/B + snapshot-vs-fold. Честно помечены
   vocabulary-only: locality injection, boundary surgery,
   promotion ping-pong, observer noninterference, adaptive
   sufficient state, specialized-kernel differential (+ половина
   causal debugging closure — capsule minimization). Правило
   карты двунаправленное: паттерн с владельцем цитируется, никогда
   не перестраивается; сказать «implemented» без имени живого
   теста — doc-drift баг. Плюс карта спаривания профиль→паттерн
   для будущих исполнимых. Потребитель: lab-composite-1 + §9's
   собственная задача «какой инструмент фальсифицирует ЭТО
   утверждение».

3. **Определение 8-частного runtime-promotion гейта → CONTRACTS.md
   (преамбула).** В CONTRACTS на гейт 10+ ссылок («behind the
   runtime-promotion gate» в §6..§12), в TASKS — в каждой строке
   имплементаций sem-1..auth-1, но САМОГО ОПРЕДЕЛЕНИЯ в репо не
   было — жило только в паке (ROUTER §9). Теперь определение
   там, где ссылки: восемь требований (REAL CONSUMER / REAL
   FAILURE / MATERIAL QUALITY GAP / NATIVE LIMIT / REPEATED
   SHAPE / FALSIFIER / INFORMATION-SEMANTIC OWNER / PHASE-GATE),
   все восемь обязательны, «применимой подмножества» нет; отсутствие
   любого → research vocabulary / proposal (TEST_PLAN §9's
   эпистемические классы), никогда билд. Отграничено от AGENTS
   §2.8 (инструментальный admission — своя, шестичастная форма).

### A.4 Строки очереди открыты (TASKS, композиция — владелец ордера уже вызвал)

- **`density-1`** (голова очереди) — форма-преемник старой E02:
  density-конверт батарея. Детерминированный параметризованный
  профиль (profile + seed → ОБЫЧНЫЙ ВАЛИДНЫЙ пак через существующий
  admission lint), минимум `E`, `L` и один из `R/F` — явные ручки
  (`ρ` производное, `K` — позже отдельной held-out рукой, требование
  ULT §19.3); потребление через `load_pack`/`Simulator`/
  `labrunner`, ноль нового пути исполнения (граница
  SCALE_TESTING_LAW §15: строится только недостающий кусок —
  материализатор profile→pack; никакого второго раннера, никакой
  второй схемы). Первая батарея — разделение H1/H2: при
  контролируемом росте мира и горизонта какая доля стены/
  inspected-счётчиков — нелокальные проходы по истории (H1) против
  per-beat опроса/реинтерпретации (H2). Класс достаточности
  объявляется по §9.1. Паки одноразовые под gitignored `output/`.
- **`lab-composite-1`** (за density-1) — форма-преемник старой
  E31 + «метаморфические семейства §26»: vocabulary-only паттерны
  §9.2 делаются исполнимыми ГДЕ потребитель сам себя называет
  (первыми locality injection + boundary surgery — их нагрузка
  это собственные оси density-конверта); каждый приземлённый
  паттерн в той же итерации называет владельца в §9.2.

### A.5 НЕ припарковано (сознательно — «если должно» фильтр владельца)

| Кандидат | Решение | Причина |
|---|---|---|
| CONS T1–T7 | не парковать | уже поглощены: CONTRACTS §6..§11 (sem-1/caus-1/replay-1/scale-1/speech-1/auth-1, S1–S7+K1–K6+E1–E6+Q1–Q7+P1–P7+A1–A7, owner-accepted 2026-10-03/04); вторая копия = вторая истина |
| CONS §4.1 verification grammar (~30 отношений) | не парковать | §9's claim packet + lens/prism каталог (phases.md §6) уже несут форму; отдельная таблица — дублирование D-024 |
| CDMT v2 (метод) | не парковать | пак — единственный владелец метода; доктрина синтеза уже репо-закон (AGENTS §2.7, D-231/D-232) |
| TEXT2 disposition | не парковать | память пака против повторного открытия; репо-строк-потребителей нет |
| M-регистр (M-1..M-24) целиком | не парковать | реестр — владелец пак; приземлённые факты уже в git + DONE-строках (rng-1, P0.5-B, h9-сертификаты); см. §B.2 |
| ULT §19.1 S0–S8 лестница | не парковать | ROADMAP §2 владелец фазовой лестницы; S-порядок — исследование [SYN], ордер фиксирует владелец |
| 8-частный гейт в AGENTS.md | отклонено | AGENTS §2.8 уже несёт инструментальную форму; runtime-гейт принадлежит CONTRACTS (где ссылки), не вторая запись в AGENTS |

## B. Свежесть: снапшот пака vs живой HEAD

### B.1 Строки пака, устаревшие к моменту проработки (все — по закону свежести, репо перечитан первым)

| Строка пака (v1.5) | Состояние в паке | Живая истина на HEAD |
|---|---|---|
| ULT §11 B7 «named next fix, owner-gated» | гипотеза, S1b | **LANDED** iter-338 (occ-1): write index + twin table, whole kiloyear 3818→43.5 s, α 1.89→0.997 |
| ULT §2.1A h9 «the whole-path OCC residue remains the B7 target» | открытый хвост | B7 закрыл; хвост теперь per-call ×1.02 |
| M-2 counter RNG «DEFERRED, [C-13]» | отложено | **LANDED** iter-334 (rng-1): эпоха, корпусная цена уплачена (228 re-pins) |
| M-7/M-8 memo/compiled specs «PROPOSAL, S1a» | предложение | **LANDED** iter-330 (P0.5-B): parse-once memo, E03 2.0→0.0/бит |
| M-16..M-18 lazy/fusion/pruning «PROPOSAL» | предложение | частично: P0.5-A (derived folds on declared demand), h9-сертификаты (next_decay_tick, condensation_pending, next_d100_hit — BI-форма сертификатного wake-up) |
| CONS §6 «OPEN P0: C1..C5» | открытые | **CLOSED как закон**: CONTRACTS §6..§11 owner-accepted |
| CURRENT_STATE «iter-337» | снапшот | HEAD iter-343 (+6 итераций: occ-1, ki114dec/impl, ki115-1, ki114-recraft, doc-4) |

### B.2 М-регистр: что уже приземлено (для будущего роутинга, не вторая копия реестра)

M-2 → rng-1 (эпоха); M-7/M-8 → P0.5-B (memo) + частично farstead-
инструмент; M-1 (timing wheel) → BI-формой h9-сертификаты + остаток
S2; M-23 (certificate wake-up) → h9 (three twins + next_d100_hit);
M-3 (Gillespie) → BI-форма h9 family scans, EPOCH-форма не нужна
(эпоха уже даёт O(1) jump); M-4 (witness) → не приземлено (S2-строка
будущего); M-9 (zone maps) → не приземлено (S2); M-5/M-6 (addressable
worldgen) → DEFERRED, владелец-гейт (C-14) — мировой трек первый
потребитель.

## C. Что НЕ сделано (честно)

- **density-1 НЕ начата** — строка открыта, материалайзер не
  построен: одна строка = одна итерация (AGENTS §2), проработка
  пака и парковка — эта итерация; батарея — следующая.
- **M2/replay-UI/W8/P1-P3 не тронуты** — за density-1 по ордеру
  владельца.
- **Кап TEST_PLAN**: файл 769→889 строк (припаркованные §9.1/§9.2,
  +120) — allowlist-запись уже стоит (substance-dense, крус-проход
  сделан iter-334-эпохой); докguard зелёный, переполнение
  задокументировано здесь (§6.1 форма: субстанция — законы и
  карты, не нарратив).
- Две doc-only итерации подряд (iter-343 + iter-344) — исключение
  D-022 применено (свежий запрос владельца = явная задача), сигнал
  зафиксирован: следующая итерация ФУНКЦИОНАЛЬНАЯ (density-1 — код).

## D. Честное неизвестное: старые метки E02/E31

Реестр E-нумерации умер вместе с удалённым ULTIMATE-паком (iter-328
§C: «пак вне репо и удалён владельцем»). Восстановимо из репо:
E0 = baseline (lab-1), E1 = horizon ladder (lab-4), E03/E04 =
per-beat счётчики (приземлены lab-5 в labrunner), «E02 в полной
форме» + «E31» + «метаморфические семейства §26» — остаток
батареи (lab-5 §E.3). Форма-преемники v1.5: density-конверт
(ULT §19.3(1) + SCALE_TESTING_LAW §3.2 — контекст iter-328 сам
вёл к нему: E03/E04 это счётчики именно этой батареи) и
композитно-метаморфическое семейство (ULT §17.4.1 + §17.5).
Старое определение E31 невосстановимо из репо — если у владельца
сохранён старый пак и его E31 отличается от выведенной формы,
строка lab-composite-1 перекраивается по вызову (запись в строке
TASKS). Ни одна строка не открыта «как новая» по одному только
старому имени — правило no-rediscovery (TEXT2 §7.3) применено
к собственным меткам репо.

## E. Проверки

- `PYTHONHASHSEED=0 python -m pytest -q` — **2632 passed + 1
  skipped** (коллекция IDENTICAL to BASE e183c64: док-изменения
  не тронули ни один тест; счёт совпадает с iter-343 в этой же
  среде);
- `ruff check .` — clean; `python scripts/docguard.py` — clean
  (TASKS ledger 10/10, worklog 10/10, TEST_PLAN allowlist);
- `python scripts/topology.py --check` — clean (нуль кодовых
  изменений — тривиально).
- INV-1..5 не тронуты, ЛОГ не тронут, корпус не тронут, нуль
  pack data, нуль corpus price.

## F. Риски

- R1 doc-only: изменены только док-райдеры; единственный
  содержательный риск — §9.1/§9.2 сформулированы уже́ более
  жёстко, чем репо жил до сих пор (классификация farstead =
  SEMANTIC-ONLY стоя́щая, не разовая оговорка). Это намеренно:
  до сих пор каждая итерация формулировала это руками (iter-335
  §«не разрешение на оптимизацию», iter-337 «interpretation
  boundary»); теперь закон один.
- Форма-преемственность E02/E31 — вывод, не перенос: если
  старый реестр владельца скажет иное, плотность строк не меняется
  (density-1 в любом случае первый потребитель и §9.1, и §9.2) —
  перекраивается только lab-composite-1.
- TEST_PLAN +120 строк: allowlist уже стоял; если владелец
  предпочтёт отдельный файл (SCALE_TESTING_LAW.md в docs/) —
  перенос одной секцией, ордер владельца.

## G. Дальше (по порядку владельца)

1. **density-1** — материалайзер profile→pack + первая батарея
   H1/H2 + первый классифицированный датум (§9.1 пакет);
2. M2 (станционная A/B surface→canonical-ID);
3. replay-UI NOT-EXPOSED; 4. W8; 5. P1/P2/P3;
6. lab-composite-1 за density-1.

## H. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/TEST_PLAN.md docs/CONTRACTS.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-344-packabsorb-report.md
git status --short
git commit -m "iter-344-packabsorb: THE UNIFIED-PACK v1.5 ABSORPTION — the scale-claim sufficiency law parked at TEST_PLAN 9.1 (the E/L/R/F/K/H/Q axes, the five sufficiency classes, the oracle tiers, the farstead family = SEMANTIC-ONLY standing) + the composite proof-test pattern map at 9.2 (14 patterns, live owners named) + the 8-part runtime-promotion gate definition at CONTRACTS' preamble + the queue rows opened (density-1 the E02 successor, lab-composite-1 the E31 successor)"
git push
```
