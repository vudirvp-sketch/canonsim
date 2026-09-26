# Отчёт итерации iter-261 — composition witness + cov-1 + P1-10

> Владелецский отчёт по запросу «следующая итерация после iter-260»
> (композиционный вопрос: **что делает temporal semantics в уже
> существующем интегрированном мире и где настоящий bottleneck**).
> Рабочая база: `iter-260-temp1-a2b3` (HEAD `0218070`). Язык отчёта —
> русский по прямому указанию владельца (исключение из AGENTS §1 для
> ЭТОГО артефакта; все сопутствующие state-доки — по-английски, как
> обычно). Формат статусов — семейный словарь репо (CONFIRMED /
> PARTIALLY CONFIRMED / REJECTED / UNRESOLVED / DEFERRED) и
> FACT / INFERENCE / HYPOTHESIS / PROPOSAL / UNKNOWN.
> Полный код проверки: `tests/test_p1_composition.py` (16 тестов),
> `scripts/mechanics.py` (`census --log`, `timing`),scratch-замеры
> зафиксированы ниже с воспроизводимыми командами.

---

## A. Existing composition surface (что уже есть)

**FACT.** Sarrow Vale (`content/province_pack`, `ANCHOR_REGION.md`) —
самый сильный композиционный субстрат репо: 12 NPC / 6 локаций /
7 предметов / 4 группы; 9 urgency-записей, 3 faction-записи, 6
director-хуков; полный `crime_watch` (suspicion-источники, статусная
лестница unknown→suspect→caught, arrest при 75 + co-location);
календарный год (маркеты 14400, ярмарки 43200, сезоны 129600,
макро-год 518400 + сезонный weather-райд); экономические потоки
(debt-1: accounts + flows на макро-пересечении); watch-ротация с
`knowledge_transfer`; leverage-экономика (4 секрета); scene LOD
(depth-3: активная зона на битах, тёплое кольцо на макро-пересечениях).

**FACT.** Причинная сеть (`ANCHOR_REGION.md` §5): 8 петель. A (пожар →
институт) и B (фьюд → вигилия) — COMMITTED; C (сезон → погода →
социальный сигнал) и D (маршрут → конденсация → культура) — COMMITTED;
E (кредитная петля) — биты committed, поток вооружён (debt-1); F/G/H —
AUTHORED (не runtime). 13 межпетельных рёбер задокументированы.

**FACT.** Существующие интеграционные тесты — по-петельные, изолированные:
`test_triangle` (пожары, seed 53/139/2), `test_calendar` (год, seed 42),
`test_t1_province` (T1 + travel + конденсация), `test_poleseed` /
`test_stepread` / `test_tallyread` / `test_winterkin` (read-хинжи),
`test_debt1` / `test_campaccount` / `test_freightvol` (экономика).
**Единого интегрированного прогона в записях не было** — до этой
итерации.

**FACT (provenance исторического witness'а, §3 брифа).**
`province_calendar.json` = `province_pack@0.1`, seed 42, **три шага**
(move keep, move malby, **wait 519000**). Это узкий **temporal stress
тест**: PC год простаивает на Малби; все 265 разговоров — одна запись
`urgency_0004` (npc_marketmistress_01 → talk → pc_01, гейты
same_location + trust≥20); ни одна авторская причинная цепочка не
запускается; пожарной/криминальной/фракционной механики в прогоне нет.
**Вывод: кластеризацию 265/265 нельзя читать как доказательство на
«полном интегрированном мире» — это стресс-witness узкой формы.**
P1-1 обязан дать композиционный witness с явным provenance — что и
сделано (раздел B).

---

## B. P1-1: Province integrated witness (композиционный результат)

**Deliverable:** `tests/playscripts/province_composition.json`
(province_pack@0.1, seed 2, 13 шагов, только существующие глаголы:
take лампы → arson камина в keep → кража жестяной коробки сержанта
(провал) → ожидание → arson рыночного ряда на Малби → ожидание →
переходы → **годовое ожидание 519000**) +
`tests/test_p1_composition.py` — 16 тестов, оракулы — ОТНОШЕНИЯ
(§12 брифа: без giant golden log), поверх одного прогона 2371 события.

**FACT.** Один прогон проходит **шесть взаимодействующих цепочек
end-to-end**:

1. **Криминальная семья** (механизм-семейство петли A по
   anti-double-count решению): провал кражи → knowledge-mint
   (`figure_reaching_for_tin`, свидетели — сержант и торговка) →
   leverage-кластеры над PC (3: у сержанта, у торговки, у корпорала
   через брифинг) → suspicion 30→55→65 + статус `suspect` →
   **ротация передаёт ВЕСЬ стек корпоралу одним тиком**
   (knowledge_transfer, 0→30→55→65; корпорал никогда не был
   co-located с преступлениями PC — его знание чисто институционально)
   → институциональный `document_check` (urgency_0001 сержанта,
   «лицо, кормящее сбор») → waybill 65→90 (пересечение arrest-бара 75
   при co-location) → `arrest_attempt` → `arrest_resolved`: **caught,
   irreversible**. Плюс вторая рука: relief-хук директора
   (possible_manifest_check_relief) даёт корпоралу собственную
   проверку (65→90).
2. **Петля A, гильдейская рука**: arson рынка → fire → alarm
   (fear 0→40 у торговки) → panic_ripple (+10 сквозь стены) →
   `guild_councils` через front door (actor = grp_river_guild,
   faction_0000).
3. **Петля B**: пожар keep будит Гаррика (grief 30→50), пожар рынка —
   Вилмота (35→55) → deadband открыт (100%) → `wergeld_vigil` ×4 —
   **включая тик 525335, через год**: grievance decay=0, пережиток
   кормит фракционное событие год спустя (оракул
   residue→future-option).
4. **Петля C**: год прокручивает весь календарь — 36 маркетов, 12
   ярмарок, 4 сезона в цикловом порядке, year_turns 151, weather-райд
   (3 броска; no-op-roll подавил один; на оттепели — storm).
5. **Макро-экономика (вооружённая половина E/H)**: на пересечении года
   — 4 аккаунт-потока (the_toll_nets 2, the_guild_collects 4,
   the_bloom_nets 3, the_withhold_banks 2).
6. **Петля D + амбиент**: конденсация дороги на первом бите (имена
   рождены), 730 ротаций, 5 брифингов, 287 разговоров (urgency_0004),
   22 слуха, 7 crowd_wary.

**FACT (честные границы witness'а).** Рука гарнизона
(fear→`garrison_patrols`) и шторм-мурмор (weather→hook→ramble) на
окнах этого seed не выпали — обе COMMITTED-доказаны своими witness'ами
(`test_triangle` seed 139; `test_weather` — семейство
storm-seeds-the-director's-buffer). Это ограничение witness-окон
(вероятностные окна p=15/p=20), **не отсутствующая механика**.
Классификация по §14: MISSING MECHANIC — нет; MISSING TEST — нет;
ограничение формы witness'а — да.

**FACT (LOD-структура).** Scene LOD ограничивает битовую механику
активной зоной (тёплое кольцо — только на макро-пересечениях): NPC
weirstair/crofts на этом маршруте не тикают вообще (см. census,
раздел C). «Интегрированный мир» = активная сцена + глобальные
поверхности (директор, календарь, макро, ротация, криминальная
система) — by design (depth-3/D-186).

**Вердикт B: CONFIRMED** — композиция доказана на существующем
субстрате: несколько подсистем, реальные end-to-end цепочки, реальные
взаимодействия (knowledge → институт → криминал → фракция → календарь)
в ОДНОМ прогоне, детерминированно (twin byte-identical).

---

## C. cov-1 census (где находятся потери)

**Deliverable:** расширение `scripts/mechanics.py` — `census --log
<run>` (runtime-ценз, словарь потерь A–H по §5 брифа; read-side,
derived, regenerable; НЕ вторая canonical truth). Класс называет
**первый отсутствующий ногу** конвейера
`давление → urgency → intent → реализация → событие → residue →
потребитель`.

**FACT (census по композиционному прогону, seed 2):**

```text
классы: A 1 · B 3 · C 5 · D 1 · E 2 · F 0 · G 0 · H 10
```

| Потеря | Кто | Причина (из лога+пака) |
|---|---|---|
| **A** (нет давления) | urgency_0003 (корпорал, look_around) | трейт `wary_of_the_tin_drifter` никогда не кристаллизовался — самого давления нет |
| **B** (давление без urgency) | npc_drover/peddler/carrier_01 | их fear двигался (panic_ripple), но urgency-записей у дорожных нет вообще — pack-shape факт |
| **C** (urgency без intent) | urgency_0000 (Кетта, coerce) — гейт: кластер lever'а у неё не чеканился + вне зоны; urgency_0005/0007/0008 — **LOD: носитель никогда не входит в тикающую зону**; faction_0002 (гарнизон) — rolled, never hit (p=15 на доступных битах) |
| **D** (intent без реализации) | director_0001 (possible_manifest_check) — дверь отвергла релиз: окно (2520→3449, 929 тиков) — ротация увела сержанта |
| **E** (реализация без канонического последствия) | faction_0000 (guild_councils), faction_0001 (wergeld_vigil) — тихие события: без state_changes/knowledge/hooks; их потребитель — story-critical рендер (tale), не проекция |
| **F** (последствие без персистентности) | 0 семей — и alarm-fear (decay 5/360) и fatigue гаснут, но у каждой семьи есть и персистентные ноги (grief decay=0, caught irreversible, knowledge append-only) |
| **G** (residue без потребителя) | **0** — каждый персистентный residue имеет декларированного потребителя (static census + runtime согласованы) |
| **H** (полный путь) | urgency_0001 (86 проверок → арест), urgency_0002, urgency_0004 (287 разговоров), urgency_0006, director_0000, 5 player-глаголов |

**FACT (статический censус, не изменился):** province 29 действий /
10 realized / **19 UNREALIZED** (вся authored-мезо-поверхность:
read_pole/read_stair/read_tally/steal(до этой итерации)/council/
hold_vigil/reckon_paper/…); 0 consumerless. Новым скриптом `steal`
перешёл в authored (10→11 realized, 19→18 UNREALIZED) — законная
пере-фиксация с объясняющим изменением.

**Ключевые выводы (INFERENCE):** потери концентрируются в
**assignment** (C: 5 из 12 автономных семей — 3 структурно LOD, 1
гейт, 1 бросок) и в **consequence** (E: институциональные ответы —
тихие канонические факты, их замыкание живёт на read-стороне). Потерь
в **realization** почти нет (1 OCC-miss), в **residue/consumer** —
ноль. Узкое место композиции — не планировщик, а плотность давления
и потребителей в off-stage зонах (B/C) и отсутствие state-ног у
институциональных ответов (E).

---

## D. P1-10: autonomous timing witness

**Deliverable:** `scripts/mechanics.py timing --log/--script` —
двухвременная таблица по каждому автономному resolution:
assignment_tick / event.t / latency / cause / каноническое событие /
deltas+knowledge+hooks / OCC-миссы / компрессия. **Первый именованный
потребитель `assignment_tick` за пределами contract-теста.**

**FACT (композиционный прогон, seed 2, 2371 событие):**

```text
autonomous resolutions: 383 (382 accepted + 1 rejected)
B3 discipline: 383/383 carry assignment_tick, all origin<=realization
latency: min 7 · max 518861 · mean 247897.6 · zero-latency 0
buckets: 0 0 · 1-99 1 · 100-999 8 · 1k-10k 12 · >10k 362
OCC misses: 1 — director_0001 at 2520 -> t 3449 (latency 929)
compression: assignment span [360,523440] vs realization span [605,525341]
```

Разрез по окнам: **раннее окно** (до годового ожидания, t<6333) — 11
автономных событий, max latency **1656** (короткие окна: цепочки
криминал→арест→совет→вигилия замыкаются при малых задержках);
**позднее окно** (год) — 372 события, min latency 1901, все — в
последних тиках ожидания.

**FACT (эмпирическая H1/H2-пара, season-scale, seed 2).** Композиционный
сценарий с ожиданием 129600: span vs полностью нарезанный
(129600×wait 1, temp-1 трансформация), semantic_diff + семейные
дельты + финальные проекции:

- **Материальные исходы цепочек ИДЕНТИЧНЫ**: arrest=True, caught=True,
  council=1, vigil=3, burnout=2, suspicion=11, leverage=3 в обоих
  рукавах.
- **Пересекающиеся семейства инвариантны** (закон A2, провинциальное
  подтверждение): status_decayed 300/300, watch_change 189/189,
  knowledge_transfer 5/5, market_opens 9/9, fair_opens 3/3,
  high_water_rises 1/1, weather_turns 1/1.
- **Дельты только в door-трафике**: `intent_rejected` **20 → 0**;
  `document_check(+failed)` **1(+0) → 11(+10)**; crowd_wary 1→7;
  rumor_told 25→20. Финальные проекции различаются ровно **двумя**
  пропами: pair-suspicion торговки (70 vs 100) и сержанта (95 vs 100).
- Механизм дельт: в span-рукаве чеки сержанта, отчеканенные на битах
  годового окна, приземляются на ОДИН тик лендинга — и 19 из них
  отвергаются (ротация увела сержанта с Малби к моменту лендинга);
  в нарезанном рукаве дверь приземляется на бите — сержант на месте,
  проверки проходят и рассыпаются по году. В годовом (519000) witness
  фаза ротации на лендинге обратная: **86 проверок принимаются одним
  тиком**. Судьба целого года minted-интентов решается состоянием мира
  в ОДНОМ тике — наблюдаемо странно (B2), материально пока benign
  (см. E).
- Команда воспроизведения (scratch, не коммитится): пара
  `pair_span`/`pair_sliced` из этой итерации; инструмент:
  `python scripts/semantic_diff.py A B`.

**Вердикт D: CONFIRMED** — задержка измерена и по величине, и по
последствию: она реально меняет door-исходы (OCC-миссы, масштаб
пропорционален окну), но на этом субстрате не меняет материальную
траекторию композиции.

---

## E. Competing explanations (H1–H4)

| Гипотеза | Статус | Класс | Evidence |
|---|---|---|---|
| **H1** temporal semantics material gap: deferred realization меняет причинную траекторию | **PARTIALLY CONFIRMED** с названной границей | FACT+INFERENCE | FACT: единственный измеренный МАТЕРИАЛЬНЫЙ флип — tavern seed-125 (leverage-карта истекла в 12-тик окне: `intent_rejected` vs `coerce`+relation-mint) — уже зафиксирован в temp-1/D-236. На провинциальной композиции (сезон-пара) материальная траектория ИНВАРИАНТНА (D). INFERENCE: деферал становится материальным ровно тогда, когда есть **истекающий гейт** (leverage-карты) или **mid-window потребитель**; на province-субстрате таких в позднем окне нет |
| **H2** наблюдаемо странно, но материально мало: B2 допустимая fast-forward semantics | **CONFIRMED на измеренной полосе** | FACT+INFERENCE | FACT: pile-up реален (372 события позднего окна в последних тиках; 86 проверок одним тиком), материальные исходы инвариантны (D). Граница честности: это свойство СУБСТРАТА на этой полосе, не свойство семантики как таковой |
| **H3** проблема в substrate/content: не хватает давления/urgency/потребителей/механик | **CONFIRMED как решающий фактор материальности** | INFERENCE | Census (C): 5 из 12 семей не доходят до intent (LOD/гейты), 3 NPC с давлением без urgency, 2 фракционных ответа без state-последствия; экономика позднего окна не имеет mid-window читателей suspicion/разговоров. Материальность деферала определяется плотностью субстрата, не планировщиком |
| **H4** проблема в integration boundary (urgency→intent, realization→residue, residue→consumer) | **CONFIRMED в своей полосе** | FACT | FACT: 19→0 rejected / 1→11 checks — стык urgency→дверь реально теряет назначения (масштаб с окном); `destroyed` рынка не гейтит ни маркет-дни (36/36 открылись на пепелище), ни разговоры торговки (285/287) — стык residue→consumer отсутствует; фракционные ответы без state-записи — стык realization→residue читается только рендером |

**Сводный ответ на главный вопрос итерации** (INFERENCE): temporal
semantics делает реальную работу на стыке intent→дверь (OCC-окна,
масштабирующиеся с размахом ожидания), но **настоящий bottleneck
композиции — не планировщик (B1), а плотность субстрата**: давление
off-stage зон (B/C-классы), отсутствие state-ног у институциональных
ответов (E-класс) и непрокинутые residue→consumer стыки (H4).

---

## F. B3 status (есть ли реальный consumer `assignment_tick`)

**FACT (аудит потребителей на BASE):** писатель — один
(`core/loop.py`, дверь enqueue + `_provenance`). Именованный читатель
на BASE — **один: `tests/test_temp1_contract.py`**. `observatory_read`
и `chronicle` несут provenance сквозным проходом (без интерпретации).
Ни render/, ни cli/, ни workbench/, ни scripts/ не читали поле.

**FACT (что изменила эта итерация):** `mechanics.py timing` становится
**первым диагностическим (read-side) потребителем** поля — census `--log`
тоже читает его (окна A/C/D классифицируются по двухвременной записи).
Это диагностический, не продакшн-потребитель.

**Вердикт: consumer status = UNRESOLVED → частично закрыт этой
итерацией** (диагностический потребитель есть; runtime/narrative — нет).
**PROPOSAL (owner-gated, без churn сейчас):** демоция поля из
постоянной схемы в research-only представление НЕ предлагается до
появления либо (а) продакшн-потребителя (хроника/observatory, читающие
деферал), либо (б) двух итераций без новых потребителей; schema 0.3
остаётся как есть. Обратный schema churn без evidence-based причины
не делается (§9 брифа).

---

## G. A2 status (family-level contract)

**FACT:** контракт остаётся **семейным инвариантом количества**, нигде
не расширен до tuple-equivalence: `test_temp1_contract.py`
(`EXPECTED_CROSSING_COUNTS` — счёт по семействам, проекция+фингерпринт
только на минимальной паре); `phases.md` §6 record явно фиксирует
границу «family counts are the contract, payloads are inside the free
surface» и называет измеренный случай `knowledge_transfer` seed 1001
(count 2 vs 3) как внутри свободной поверхности. Документация и тесты
объясняют это однозначно.

**FACT (новое):** сезон-пара (D) независимо подтверждает семейную
инвариантность на province-масштабе (9 семейств crossing/календаря —
все INVARIANT), включая `knowledge_transfer` 5/5.

**Вердикт: CONFIRMED** — семейство-уровень; расширения до
tuple-equivalence не произошло и не нужно.

---

## H. World-level invariant gaps (инвентаризация)

Кандидаты §13 брифа против `WORLD_TESTS.md` + нового witness'а:

| Кандидат | Статус | Где |
|---|---|---|
| мир не становится причинно безмолвным при объявленном незакрытом давлении | **EXISTS (теперь)** | `test_p1_composition.py::test_the_world_stays_causally_loud_through_the_year` — 2371 событие за год простоя; LOD-молчание off-stage зон — честная граница, задокументирована |
| персистентный residue влияет на будущие валидные опции | **EXISTS (юнит-уровень) → PARTIAL (мир-уровень)** | Юниты: pole/steal_target (test_poleseed), leverage-гейты (test_coerce), kin-claim (test_winterkin), аккаунт-двери (test_charcoalpaper). Мир-уровень: ВИГИЛИЯ ЧЕРЕЗ ГОД на том же grievance — новый тест закрывает |
| мёртвые агенты не порождают новых автономных интентов | **PARTIAL** | Механизм существует и читается: `crime_status==caught` вычёркивает NPC из urgency-обхода (`core/urgencies.py`) и из целей директора; death-механики в провинции нет → как world-level тест NOT APPLICABLE на этом субстрате; предложение — см. J |
| знание не появляется без объявленного источника/передачи | **EXISTS** | knowledge-mint'ы едут на событиях (source-поля), слепые NPC — phase-4 gate (0 leaks, test_blind); брифинг ротации — институциональная передача (новый тест) |
| долгие ожидания не стирают объявленные персистентные последствия | **EXISTS (теперь)** | `test_p1_composition.py::test_the_final_projection_carries_the_persistent_deltas` + vigiliya-через-год: caught/destroyed/grief/suspicion пережили 519000 тиков |
| рутинная текучка не топит навсегда причинно-значимые события | **PARTIAL** | story-critical листинг + tale gate (tune-1) решают рендер-половину; метрики важности выделают семейство; прямого world-level отношения «churn не поглощает causal-change» нет — минимальный кандидат в новые тесты (см. ниже) |

**Минимальный набор предложений (PROPOSAL, owner-gated):** (1)
world-level тест «churn не поглощает» — на композиционном прогоне:
все story-critical события присутствуют в tale-рендере несмотря на
1112 decay + 730 ротаций (дешёвый, готов к следующей итерации);
(2) при появлении death-механики — тест мёртвого агента (сейчас
NOT APPLICABLE). Новых механик ради тестов не добавлять (§14).

---

## I. B1 disposition

**DEFERRED — без изменений.** Условия переоткрытия (phases.md §6,
пять пунктов) на этой итерации **не приобрели evidence**: именованного
runtime-потребителя generate-at-T нет (F); повторяемого МАТЕРИАЛЬНОГО
провала deferred realization на интегрированном мире нет — сезон-пара
показала инвариантность материальных исходов (D); измеренный
продукт-уровневый разрыв не показан; собственное ограничение
планировщика не показано (потери назначений — свойство окон и
LOD-скоупинга, не закона очереди). Единственный материальный флип
(seed-125, tavern) остаётся классом истекающих гейтов — лечится
субстратом (сроки кластеров), не законом тиков. **B1 has NOT acquired
promotion evidence.**

---

## J. Missing mechanics/content (только доказанные прогоном пробелы)

Формат §14 брифа: наблюдённый провал → первая дивергенция →
отсутствующее звено → существующий примитив, почти решающий →
минимальное отсутствие → наблюдаемое последствие.

**J-1. Выгоревший рынок не гейтит рынок.**
Провал: 36/36 `market_opens` и 285/287 разговоров на `destroyed=True`
локации. Первая дивергенция: t=3573 (burnout) → t=14400 (первый
маркет-день) без реакции. Отсутствующее звено: residue→consumer на
стыке календарь/экономика. Примитив-кандидат: предикат
`prop(loc_malby.destroyed)` уже в закрытом наборе (`core/predicates`),
календарные записи уже несут notes-гейты. Минимальное отсутствие:
гейт (или альтернативный сценарий) у календарной записи
`market_days` + необязательный флейвор у talk-urgency. Последствие:
после пожара рынок реально пустеет — экономический отклик на
институциональное насилие, новый causal-контур A→(экономика).
Классификация: **MISSING INTEGRATION/CONSUMER** (не механика, не
контент-объём).

**J-2. Институциональные ответы без state-последствия.**
Провал: `guild_councils`/`wergeld_vigil` — тихие события (E-класс);
петля A документирована как state-closing («the changed world state:
barred stalls, the watch on the road»), но записей состояния нет.
Отсутствующее звено: realization→residue у фракционных резолверов.
Примитив-кандидат: `state_changes` на действии `council` ( resolver
`wait`-класса не пишет состояние — минимальная правка pack-данных
действия, не движка: резолверы `account`-семьи уже пишут).
Минимальное отсутствие: 1–2 pack-декларации state-записи (например
`guild_ban` / `watch_doubled` флаги локации). Последствие: следующий
пожар встречает изменённый мир — замыкание петли A станет
проекционным, не только рендерским. Классификация: **MISSING
CONTENT** (pack-данные), не механика.

**J-3. Дорожное давление без потребителя.**
Провал: fear дорожных (drover/peddler/carrier) двигается (panic),
urgency-записей нет (B-класс). Отсутствующее звено: pressure→urgency.
Примитив: ambient-группа уже тикает конденсацией; запись urgency для
члена группы — существующая форма. Минимальное отсутствие: 1 запись
(например, peddler look_around при fear≥20). Последствие: паника
становится видимым поведением, амбиент перестаёт быть декоративным.
Классификация: **MISSING CONTENT**, низкий приоритет (амбиент by
design холоден — depth-7 агрегаты).

**Не-пробелы (проверено):** garrison-рука и murmur —Witness-окна,
доказаны своими тестами; LOD-молчание — by design; F/G-классы — пусты.

---

## Итог по критерию успеха (§18 брифа)

Достигнут третий исход из перечисленных:

```text
A2 confirmed
+ apparent temporal problem largely explained by missing substrate/integration
  (H3/H4: LOD-скоупинг, отсутствие mid-window потребителей, непрокинутые
   residue→consumer стыки, тихие институциональные ответы)
+ content/mechanic gap identified (J-1..J-3, все — pack-уровень)
+ B1 deferred (без новых evidence)
+ B2 достаточна на измеренной полосе (H2), с границей честности (H1-класс
  истекающих гейтов существует и зафиксирован)
+ B3 приобрела первого диагностического потребителя (timing); продакшн — нет
```

Никакой заранее выбранной архитектуры не доказывалось: scheduler не
тронут, B1 не открыт, B3 не откачен, A2 не расширен, новых
runtime-примитивов нет. Все находки — findings/proposals с evidence.

## Воспроизведение

```bash
PYTHONHASHSEED=0 python3 -m pytest tests/test_p1_composition.py -q   # 16 тестов
python3 scripts/mechanics.py timing  --pack content/province_pack \
    --script tests/playscripts/province_composition.json            # раздел D
python3 scripts/mechanics.py census  --pack content/province_pack \
    --script tests/playscripts/province_composition.json            # раздел C
python3 scripts/mechanics.py census  --pack content/province_pack   # статический
```

Сезон-пара (раздел D): scratch-замер по трансформации temp-1
(ожидание 129600 → 129600×wait 1), оракул `scripts/semantic_diff.py`;
команды и параметры зафиксированы выше по тексту.
