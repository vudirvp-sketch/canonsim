# iter-361 · m4fullrun — ПОЛНЫЙ ПРОГОН v4.3 ПРОЧИТАН: фикс подтверждён живьём (fire-cascade закоммичена реальной дверью), RU-полоса отвечает на заголовочный вопрос доверия (понимание русского безошибочно — все промахи это порог гейта 0.38–0.49 на низкоагентных глаголах), G-контроль даёт первый like-for-like (R 38.1% full против G 21.4% на одном корпусе)

**Владелец прислал:** `m4_20261010_170258.zip` — прогон
`m4_20261010_170002` пака **v4.3** (2026-10-10 17:00, станция RTX
3080 Ti / 32 ГБ, Kev-4B роутер + Gemma-4-E4B главная, обе FULL
offload, autospawn, порты 51071/53381). Прогон **ПОЛНЫЙ И БЕЗ
ЕДИНОГО КРАША** — первый в серии: v4.1 (140427) и оба v4.2
(150710/150805) умирали на s4 cycle 2. Прошли ВСЕ стадии:
preflight → reference **10/10** → R-рука **s1..s10 (42
say-цикла)** → G-контроль (42) → RU-полоса (12) → det-мини →
package. Явный ввод сессии (D-198): «вот архив, проанализируй» —
итерация чтения (R0/R1 riders-only, нулевой код репо, INV-1..5 не
тронуты).

**BASE_COMMIT:** `f11050c1e0e48ea6a53c98a51ad9e5cb1e2d4d33`
(HEAD iter-360 — фикс Verb уже в истории; этот прогон — его
живое доказательство).

## A. Фикс подтверждён ЖИВЬЁМ — не в сэндбоксе, на станции владельца

`arm_r/s4_fire_chain/run.jsonl` несёт полный event-лог юнита —
огненная цепочка закоммичена РЕАЛЬНОЙ дверью на GPU владельца,
событие за событием (идентификаторы дословно):

- `ev_0008 drop_break` — oil_lamp_01: carrier → None, condition →
  broken (`outcome.broken=true`), знание «noise_in_loc_backyard»
  четверым NPC по каналу heard/vague;
- `ev_0009 fire_started` — spot **back_wall** (фиксированная
  политика near, t=11, irreversible);
- `ev_0010 fire_spread` — spot **woodpile** (t=16);
- `ev_0011 smoke_rising` (t=21);
- `ev_0012 location_burned_out` — loc_backyard destroyed=true,
  irreversible, t=131 (жёсткий тик — честная цена каскада);
- `ev_0013 flee` — pc_01 → loc_street (t=135, коммит).

Census цикла 2 = **fields** (near=back_wall против золота
woodpile — ЗАДУМАННАЯ расходимость R-формы, ровно предсказание
GREEN из iter-360 §E); цикл 3 flee = full. Отличие от
сэндбокса-предсказания ровно одно и оно честное: cy4 (arson
«And the street itself will burn for me too») — **живой Kev
поставил гейт ниже порога** (gate_blocked → no_intent), тогда
как скриптованный ответ в сэндбоксе проходил и дверь отвечала
intent_rejected. Обе стороны отказывают — класс расходимости
другой (гейт раньше двери), краша нет. KI#117 мёртв и живьём:
ветка исполнилась на машине владельца и выжила.

## B. Кросс-рановая побайтовая идентичность — ЧЕТВЁРТЫЙ прогон

s1..s3 этого прогона совпадают с обоими упавшими v4.2 и с v4.1
до значений: gate_p `0.7082, 0.4605, 0.4313, 0.8438, 0.4884,
0.572, 0.6982, 0.8134, 0.2959, 0.4121, 0.7702, 0.7091`; itok
`1259, 1515, 1539, 1579, 1539, 1555, 1531…`; census s1
full4/blocked2/fp1, s2 kind1/not_intent1/blocked1, s3 full2.
**Четыре прогона, одна машина, одна модель — R-рука на Kev-4B
побайтово воспроизводима**, и этот прогон первый записал
поверхность s4..s10 целиком. Det-мини: router identical=True,
**digest `962b30a43bdb6363`** (первый записанный датаум дайджеста
ответов роутера); g identical=True (поле digest пусто —
инструментальный пробел на одну будущую строку, не итерация).

## C. R-рука, полный корпус (42 say-цикла) — цензус и доказательства

RAW: full **16 (38.1%)**, kind+ **21 (50.0%)**, kind 2, target 1,
fields 2, no_pin 2, gate_blocked 10 (23.8%), gate_fp 4 (9.5%),
not_intent 5 (11.9%), parse_error **0**. Исходы двери:
no_intent 17, move 4, steal 2, take 3, take_failed 3, look_around
3, rumor_told 2, intent_rejected 2, distract_ignored 1, flee 1,
**location_burned_out 1** (каскада), rest 1, wait 1, пустой 1
(см. §G). Доказательства R-формы на полном корпусе: **0
изобретений на 42 документах** (ledger дословно: «assembled docs:
42; with ANY key outside the pack's sets: 0») и
**output_tokens=[0] × 42** — негенеративность живьём на всём
корпусе. Суммарно по станции: 42+42+12 = **96 документов этого
прогона, 0 изобретений**; с упавшими прогонами — **0/132
live-документов** серии. Латентность: systemone med **0.556 s** /
min 0.475 / max 0.796 / mean 0.566 (n=42); цикл end-to-end med
0.560 s; itok med 1531. Gate sweep (31 gold-intent цикл):
**67.7%@0.5 → 87.1%@0.4 → 96.8%@0.3 → 100%@0.2** — монотонная
кривая, ручка измерена на полном корпусе.

## D. RU-ПОЛОСА — заголовочный вопрос доверия ОТВЕЧЕН

12 hand-authored золотых строк, русский естественный ввод, Kev-4B:

- **5/12 full (41.7%)** на дефолтном гейте 0.5;
- **КАЖДЫЙ прошедший гейт собран БЕЗ ОШИБКИ — 5/5 kind+target
  точные**: talk/npc_guard_01 (P=0.734), steal/npc_guard_01
  (0.581), move/loc_backyard (0.581), take/oil_lamp_01 (0.510),
  take/ale_mug_01 (0.443). Ноль ошибок сборки на русском;
- **2 честных отвержения**: ru_06 (чистая атмосфера «Огонь
  потрескивает в очаге…») → no_intent, census **full** (золото
  no_intent=atmosphere — совпало); ru_10 (вопрос «А что тут
  вообще можно сделать?») → not_intent (золото question=unclear);
- ru_05 («Возьму со стойки одну из свечей»): гейт прошёл, kind
  верный, дверь закоммитила take — census **no_pin**: золото
  хотело texture-pin (tex_0000/slot candles/value lit), форма R
  запинила дефолтный target oil_lamp_01 — документированная цена
  фиксированной политики полей;
- **Все 5 промахов — gate_blocked, и ВСЕ на низкоагентных
  глаголах**: look_around (gate_p 0.423), wait (0.385),
  talk/npc_drunk_01 (0.488), examine/npc_barkeep_01 (0.410),
  rest (0.382) — весь блок в полосе **0.38–0.49**, то
  есть ПОД линией 0.5, но НАД 0.3. Прошедшие строки: 0.588–0.830.
  Паттерн: гейт отделяет высокоагентные физические/социальные
  действия от перцептивно-ambientных глаголов — это история
  ПОРОГА, не понимания.

Честная оговорка: у заблокированных ответов **нет action_top3**
(гейт зануляет действие) — на пороге 0.4 три из пяти (0.423,
0.488, 0.410) прошли бы гейт и их сборка стала бы измеримой
только в том прогоне. Вердикт полосы: **Kev-4B понимает русский
ввод безошибочно на всём, что пропускает гейт; консервативный
слой — гейт, и его промахи пороговые (0.38–0.49), а не
компрехеншивные.** Walls: med 0.510 s (n=12).

## E. G-КОНТРОЛЬ — первый like-for-like R против G на ОДНОЙ батарее

Обе руки по 42 say-цикла на одном корпусе (G = грамматный маршрут
m3-формы на Gemma-4-E4B, GBNF через OAI-поверхность):

| Метрика | R (классифайер, Kev) | G (грамматика, Gemma) |
|---|---|---|
| full | **16 (38.1%)** | 9 (21.4%) |
| частичные сборки | kind 2 / target 1 / fields 2 / no_pin 2 | kind 6 / target 8 / no_pin 7 |
| отказы | 17 (gate_blocked 10 + not_intent 5 + …) | not_intent 12 (28.6%) |
| латентность | med 0.556 / max **0.796 s** | med 0.483 / mean 1.391 / max **2.907 s** |
| генерация | output_tokens=[0] | parse_ctok ~25 токенов/вызов |

R бьёт G по full-rate **×1.8** на том же корпусе; G дешевле в
медиане, но с тяжёлым хвостом генерации (max 2.9 s = 3.6× от
R-максимума); G routing'ит look_around втрое чаще (14 против 3) —
грамматный маршрут сильнее опирается на ambient-дефолт.
Drift-watch в сырье: R 27/42, G 32/42 (premise-drift статус —
живая рука коммитит не то, что референс, отпечаток сцены
расходится; статус, не дефект; m4_report его не поднимает —
записано как сырое наблюдение).

## F. Честные прорехи прогона (сырьё, не дефекты чтения)

- **s7 cy0**: роутер назвал ВЕРХНЕЕ действие верно — examine
  (top-3: examine 0.308, look_around 0.204, wait 0.102), гейт
  прошёл — но собранный док не нёс target (target_p в ответе
  отсутствует) → `door_error: «examine requires a target»` →
  census not_intent, door_outcome пустой. Дверь отказала честно и
  громко; класс — цена R-формы (действие распознано, таргет не
  разрешён), не краш и не изобретение.
- det g-дайджест пуст (§B); `cuda_gate.bands` по-прежнему `{}`
  (формализованный band-sweep остаётся инструментальной строкой);
  RU-промахи пороговые (§D).

## G. Что это даёт решениям M2/M3 (материал, решения за владельцем)

- **M3 (форма: H / G2 / F / R)**: батарея m4 впервые несёт live
  full-корпус обоих конкурирующих маршрутов в одинаковых
  условиях — R: 38.1% full, 0 изобретений, негенеративность,
  med 0.556 s, побайтово воспроизводим; G: 21.4% full, хвост
  2.9 s. H остаётся измеренным лидером m3-батареи (другой корпус
  — честная оговорка о like-for-like). R — теперь самая сильная
  измеренная строка на m4-корпусе.
- **M2 (block / downgrade / allow + C-tight/C-full)**: RU-полоса
  добавляет русскую колонку доверия — понимание идеальное, гейт
  консервативен; при runtime-promotion первый кандидат-ручка —
  порог (0.5 честный дефолт; 0.4 — измеренная точка возврата
  87.1% на английском золото-интентах и 3 из 5 RU-промахов).
- Пак v4.3 выполнил ВСЁ, что обещал iter-357: батарея закрыта,
  докаток не нужно; следующий шаг станции — решения владельца за
  гейтом, не новые прогоны.

## H. Верификация

- Чтение сверено с сырьём: скрипты разбора (вне репо, Rule 9)
  перечитали `arm_r.jsonl`, `arm_g.jsonl`, `ru.jsonl`, `det.jsonl`,
  `gate.json`, `cuda_gate.json`, `m4_report.txt`,
  `arm_r/s4_fire_chain/run.jsonl` — каждое число отчёта владельца
  воспроизведено из сырья (census-подсчёты, sweep, латентности,
  RU-вердикты, det, event-лог s4 дословно);
- `ruff check .` — clean (ruff 0.17.0);
- `python scripts/docguard.py` — clean; `python
  scripts/topology.py --check` — clean; `python scripts/digest.py`
  — парсит (заголовок iter-361 в STATUS.md);
- `PYTHONHASHSEED=0 python -m pytest -q` — 2616 passed + 28 failed
  + 1 skipped: все 28 — известные T1 byte-identical сбои на
  `python`-строке log-header (3.12.15 сэндбокс против 3.12.14
  golden), воспроизведённые 1:1 на чистом клоне ещё в iter-358 —
  riders-only, код репо не тронут;
- INV-1..5 не тронуты (R0/R1 чтение, нулевой код репо).

## I. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-361-m4fullrun-report.md
git status --short
git commit -m "iter-361-m4fullrun: THE FULL v4.3 RUN READ - the owner's m4_20261010_170258.zip is the FIRST complete station run of the series (preflight + reference 10/10 + R s1..s10 42 cycles + G 42 + RU 12 + det + package, ZERO crashes - the Verb fix proven LIVE on the station): s4's fire cascade committed by the REAL door event-by-event (drop_break broken=true -> fire_started back_wall -> fire_spread woodpile -> smoke_rising -> location_burned_out t=131 irreversible -> flee), census=fields the counted honest divergence exactly as iter-360's GREEN predicted; the arson cy4 divergence is gate-side (live Kev below threshold vs the sandbox's scripted pass - both refuse, no crash); KI#117's branch fired live and survived. FOURTH byte-identical run: s1..s3 gate_p/itok/census match v4.1 + both v4.2 exactly - the R-arm on Kev-4B reproducible to the byte, and this run records s4..s10 for the first time; det router identical=True digest 962b30a43bdb6363 (first recorded answers-digest datum). FULL-CORPUS R PROOFS: 0 inventions on 42 docs + output_tokens=[0] x42 (0/132 live docs series-wide); latency med 0.556 s max 0.796 s; gate sweep monotone 67.7%@0.5 / 87.1%@0.4 / 96.8%@0.3 / 100%@0.2 (31 gold-intent cycles). THE RU BAND - THE HEADLINE TRUST QUESTION ANSWERED: 5/12 full at gate 0.5, EVERY gate-passed row assembled PERFECTLY (5/5 kind+target exact: talk/npc_guard_01, steal/npc_guard_01, move/loc_backyard, take/oil_lamp_01, take/ale_mug_01 - zero assembly errors on Russian); 2 honest rejections (atmosphere -> census full; the question -> not_intent); ru_05 no_pin the documented fixed-policy cost (gold texture-pin vs the pinned default target); ALL 5 misses are gate_blocked on LOW-AGENCY verbs (look_around/wait/talk/examine/rest) with gate_p 0.38-0.49 just under the 0.5 line while passed rows sit 0.588-0.830 - a THRESHOLD story, not comprehension; blocked answers carry no action_top3 so a 0.4-threshold run would measure their assembly (3 of 5 above 0.4). THE G CONTROL - first like-for-like on ONE battery: R full 38.1% vs G 21.4% (x1.8), R max 0.796 s vs G max 2.907 s (the generation tail), G leans on look_around x4.7 (14 vs 3), G generates ~25 completion tokens while R generates zero. HONEST GAPS: s7 cy0 the router's top action was examine CORRECT (0.308) but the answer carried no target -> door_error 'examine requires a target' -> census not_intent (the R-form's target-resolution cost, the door refuses loud, not a crash); drift flags R 27/42 G 32/42 (premise-drift status, raw observation); det g-digest empty (one future line, not an iteration); cuda_gate.bands still {}. THE M2/M3 DECISION MATERIAL: the m4 battery now carries both routes' full-corpus live numbers (R the strongest measured row on this corpus: full-rate + non-generativity + byte-reproducibility; H remains the m3-battery leader, different corpus - the like-for-like caveat); the RU band adds the Russian-trust column (comprehension perfect, the gate conservative, the threshold the first knob: 0.5 honest default, 0.4 the measured recovery point); the pack v4.3 has now delivered everything iter-357 promised - the next station step is the owner's M2/M3 decisions behind the runtime-promotion gate, not new runs. Reading verified against the raw records (every m4_report number re-derived from arm_r/arm_g/ru/det/gate jsonl + the s4 event log verbatim); ruff clean, docguard clean, topology clean, digest parses; pytest 2616 passed + 28 failed (the known T1 log-header env caveat, 3.12.15 vs 3.12.14, reproduced 1:1 in iter-358) + 1 skipped; KI#116 deleted per AGENTS 5 (closed iter-354, more than two iterations); R0/R1 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## J. Доставка (§12.2 — оба канала)

- **Дельта-архив** (вложение): `canonsim_iter-361-m4fullrun_
  2026-10-11.zip` против BASE_COMMIT `f11050c33035ec740fb2844210e9
  1fa619feea8` — STATUS.md, worklog.md, docs/TASKS.md,
  docs/iterations/iter-361-m4fullrun-report.md, BASE_COMMIT.txt,
  DELETED_PATHS.txt (`None`); 81 774 Б, md5
  `87bad344b911d4bd2e2063e0b94a1730`; tmpfiles-ссылка — в
  финальном сообщении;
- Сырьё прогона владельца в репо не кладётся (INV-5/Rule 9) —
  зип владельца остаётся единственным носителем: md5
  `78f397e757244f56dd13c58b7d8e66d6`, 284 726 Б (записано для
  сверки).

**Done:** полный прогон v4.3 прочитан и сверен с сырьём; фикс
подтверждён живьём (event-лог s4 дословно); четвёртая
побайтовая идентичность; RU-полоса отвечена (понимание 5/5
безошибочно, промахи — порог 0.38–0.49 на низкоагентных
глаголах); G-контроль даёт like-for-like (R 38.1% против G
21.4%); det-дайджест роутера записан; материал M2/M3
сформулирован; KI#116 удалён по §5; райдеры прошли ruff +
docguard + topology + digest.
**Not done:** решения M2/M3 — за владельцем (гейт
runtime-promotion); формализованный band-sweep остаётся
инструментальной строкой; порог 0.4 RU-прогон не запрашивался.
**Next:** решения владельца M2 (block/downgrade/allow +
C-tight/C-full) и M3 (H/G2/F/R) по материалу §G; параллельно
стоящие вызовы — replay-UI NOT-EXPOSED, W8, P1/P2/P3,
lab-composite-1.
**Active KIs:** KI#113 (test_lab, как в STATUS).
