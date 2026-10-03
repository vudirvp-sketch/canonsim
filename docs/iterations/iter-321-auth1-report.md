# iter-321 · auth1 — контракт границы интент/агентность/директор (review-C11/C12/C20 + словарь M4/D7–D9)

**Вызов владельца (2026-10-04, дословно):** «продолжай работу
прошлой итерации, я принимаю Q1–Q7 как закон. Продолжай очередь с
speech-1 и так далее» — продолжение по подтверждённой очереди
(iter-315); speech-1 приземлён итерацией ранее этим же вызовом;
auth-1 — ПОСЛЕДНЯЯ строка очереди. Сессия закрыла обе строки
(форма iter-316+317 — две итерации, один вызов).

## A. Что сделано

- **Контракт auth-1 ПРИЗЕМЛЁН** в `docs/CONTRACTS.md` §11 — семь
  пинированных решений A1..A7, каждое привязано к живому коду:
  - **A1 пайплайн, пять стадий, каждая с живым носителем (INPUT-сторона
    D9):** ввод (свободный текст игрока mode C / документ ответа
    нарратора mode A/B / шаги пьесы / автономные продюсеры — через
    ТУ ЖЕ дверь) → интерпретация (закрытый гейт `intent|question|
    no_intent` / документ предложения) → классификация (kind/target/
    fields против грамматики действий пака — INV-3) → авторизация
    (дверь интентов: validate_shape + закрытый набор предусловий +
    OCC) → исполнение (цепочка резолверов + `_commit`, закон S1).
  - **A2 valid ≠ authorized — ТРИ РАЗНЫЕ оси, три словаря отказа.**
    Malformed → громкое семейство (RunnerError/ParseError/
    ProposalError), НОЛЬ событий; well-formed, но мировой-невозможный
    → закоммиченный `intent_rejected` (попытка — ФАКТ); valid +
    authorized → событие, INV-5-неизменяемое.
  - **A3 классы авторитета INPUT-стороны: player | NPC | director |
    system | pack.** NPC — гейт вызывателя mode B («ответ предлагает
    действия ТОЛЬКО своего вызывателя»); director — релизы хуков
    через дверь с `origin_hook`-провенансом; system — механические
    продюсеры (эмиссии, не интенты); pack — засеянные хуки/follow-up'ы/
    ожидания. Забор с S3 (sem-1, emit-сторона): два словаря никогда
    не противоречат.
  - **A4 неоднозначность коллапсирует ТОЛЬКО по эквивалентности
    канонических поверхностей эффекта (D9); глобальный confidence-score
    ЗАПРЕЩЁН.** Иначе — уточнение (альтернатива `question`) или
    отказ. Сегодня машинерии коллапса НЕТ — она дело строки
    имплементации, с доказательством эквивалентности.
  - **A5 инвариант D7: `DirectorOutput ⊆ EligibleConsequences(world,
    pack, current_state)` + мутационная проба.** Допустимое
    множество = буфер засеянных хуков (паковые хуки, засеянные в
    момент события, D-005); пути релиза только ВЫБИРАЮТ из буфера
    (бюджет 1-релиз-на-бит, чистый выбор опций без RNG); релизы едут
    через дверь интентов (D-037). Директор НИКОГДА не изобретает
    сущность, мотив, цель, причину, факт. Мутационная проба:
    придуманный kind умирает громко у двери; незасеянное последствие
    не имеет пути релиза (API релиза-по-тегу НЕТ).
  - **A6 ограниченная детерминированная агентность там, где назван
    потребитель (D8); НИ генерического планировщика, НИ LLM-планировщика.**
    Носители: срочности (per-NPC шаблоны целей, d100 на бит,
    изолированные стримы, предусловия, шумовой пол), кристаллизованные
    черты, семейства обид/долгов. Дисциплина через-дверь (D-037):
    один механизм, никогда два.
  - **A7 словарь M4 + ЖЁСТКИЙ КАНОН (решение владельца от
    2026-10-03):** instruction (протокольные строки документа вызова —
    никогда канон) / proposal (типизированный кандидат) / authority
    (авторизация двери) / realised intervention (закоммиченное
    событие) / canonical consequence (даунстрим-эффекты фолда).
    ЗАКОН: ошибочное-но-закоммиченное модель-опосредованное действие
    INV-5-неизменяемо — пути восстановления/спора НЕТ ВООБЩЕ;
    коррекция — НОВОЕ событие; реткон-путь потребовал бы нового
    дизайна за гейтом владельца — ОТКЛОНЕНО стоящим решением.
- **Фальсификатор-батарея ПРОГОНЕНА ВЖИВУЮ** (скрипт вне репо,
  Rule 9; НАСТОЯЩИЕ Simulator/Mediator/ParserDoor/дверь интентов/
  директор/писатель, сиды 42 + 8 — day1-корпус) — см. §D.
- **Минимальный тест-сет будущей строки имплементации закреплён.**
- **ОЧЕРЕДЬ РАЗРЯЖЕНА** — все шесть контрактов подтверждённой
  очереди 2026-10-03 приземлены (sem/caus/replay/scale/speech/auth).

## B. Что НЕ сделано (честно)

- **Ни строчки кода** — ни пайплайна, ни реестра авторитета, ни
  машинерии директора/медиатора (закон строки). Имплементация — НЕ
  строка: владелец открывает после приёмки.
- **DECISIONS.md не тронут** (кап 30/30) — A7 несёт уже записанное
  решение владельца (iter-315), не новое.
- **llama.cpp не устанавливался** — R0/R1 строка (разрешение стоит,
  не нужно: как iter-316..320).
- **Коллапс неоднозначности не реализован** — заявление A4, носителя
  нет до строки имплементации (сознательно).

## C. Связь с соседями

- sem-1 (§6): A2 — трёхосный двойник S5 (loud/soft); A3 — забор
  input-side ↔ S3 emit-side; A5(iii) опирается на S3/S5.
- speech-1 (§10): P3-забор исполнен — auth-1 владеет INPUT-пайплайном,
  speech-1 каналами; два словаря не противоречат.
- caus-1 (§7): `origin_hook`/`assignment_tick` — провенанс релизов
  директора остаётся линейным, никогда вторая каузальная онтология.
- replay-1 (§8): M4-жёсткость опирается на INV-5 + E4 (закоммиченное
  = произошло; не-дюрабельное «не существовало» — другая ось).
- scale-1 (§9): бюджет директора (1-релиз-на-бит) — PACING-бюджет,
  НЕ work-бюджет (Q2 различает — тест-сет это пинирует).
- core-1 (PARKED): A5 отображается на его C4 (LLM-граница) через
  namespace-забор.

## D. Проба — живой прогон (сокращённо; дословно в артефакте)

```
[ARM A] the pipeline + valid != authorized (seed 42)
A1  talk -> npc_guard_02 (present in the guardroom, pc in the tavern):
    committed ev_0006 t=2 type=intent_rejected actor=pc_01 target=npc_guard_02
    state_changes=0 — the world unchanged; the rejection IS the fact
A2  unknown kind 'seduce': RunnerError (loud) "unknown intent 'seduce'
    (not in the pack's actions)"; events 7 -> 7 — nothing in the world
A3  move -> loc_backyard: committed (delta=1) — the execution axis
A4  rg -i 'confidence'|'risk_score'|'truth_score' over core/ brief/ cli/: 0 hits
[ARM B] the authority classes + D7 + M4 (seeds 42 + 8)
B1  the npc_guard_01 actor reply proposing pc_01's talk: status=accepted,
    events 7 -> 7 (delta=0) — "BEAT intents: 0 fed, 1 withdrawn";
    the note rides the player's next call: "WITHDRAWN intent talk (actor
    'pc_01' is not the caller 'npc_guard_01' — a reply proposes its own
    caller's actions only)"
B2a the day1 run (seed 8): the seeded-hook buffer (EligibleConsequences)
    = 5 instances (ambient_drunkard_ramble x3, barkeep_wary_sweep x2 —
    each with its pack-declared payload); released ids: [] (the quiet/
    explicit paths did not fire in the short run — honest)
B2b the Director's public surface: beat_count, export_run_state, hooks,
    next_beat, pacing, pack, policy, releases, restore_run_state, seed —
    NO release-by-tag API; an unseeded consequence has NO release path
B2c the invented kind 'spawn_dragon': PACK.action -> None; the door
    refuses loud (RunnerError "unknown intent") — the invented
    consequence dies at the grammar
B3  EventLogWriter's public surface: append, appended, close,
    event_count, last_id, path, write_header — NO edit, NO undo, NO
    retcon; rg 'retcon'|undo|rewrite_event over core/: 0 hits
[ARM C] ambiguity by effect-equivalence (seed 42)
C1  "look at the thing over there" -> reply {question: "Look at what
    exactly — the purse, the lamp, or the barkeep?"}: status=question,
    events 6 -> 6 — the uncertainty SURFACED, nothing fed
C2  rg -i 'effect_equivalence'|'auto_collapse'|'auto-collapse': 0 hits —
    the closed gate's exactly-one alternative law stands; the collapse
    is the implementation row's, with its equivalence proof
```

Артефакты (md5): probe `cac2608e0759fc7848ea7acae8a3ac0c`,
вывод `f69d1a355ed5560b8ad308a4fbe2692b`. Скрипт вне репо (Rule 9).

**Смысл:** три оси valid/authorized/committed РАЗЛИЧЕНЫ и живы —
мир-невозможная попытка закоммичена как факт (`intent_rejected`,
ноль изменений состояния), малформ погибает громко до мира,
валидная команда исполняется; input-сторона авторитета держит
гейт вызывателя (чужой интент отозван, ноль событий); D7-инвариант
держит форму — допустимое множество = засеянный буфер, изобретённый
kind умирает у грамматики, пути релиза незасеянного нет; M4-жёсткость
канона = поверхность писателя append/close (ни редактирования, ни
отмены, ни реткона нигде). Риски review-C20 (valid ≠ authorized) и
C11 (директор-изобретатель) закрыты живыми пробами; риск C12 —
законом A6 (запрет планировщиков, носители перечислены); M4 —
решение владельца записано в словарь контракта.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2557 passed + 1 skipped**
  (до/после идентично; ни один тест не удалён/ослаблен);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (ledger 10: iter-321 вошёл,
  iter-311 выселен; worklog 10: iter-311 выселен; CONTRACTS.md —
  ALLOWLIST с рационалом на семь определений);
- `python scripts/topology.py --check` — clean;
- CONTRACTS.md 929 строк (сверх 600, ALLOWLIST + рационал — закон
  §6.1, форма-указатель с iter-320), TASKS.md 599 (кап 600),
  STATUS.md — форма выдержана (KI ≤2 строк, один DONE-блок).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/CONTRACTS.md scripts/docguard.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-320-speech1-report.md docs/iterations/iter-321-auth1-report.md
git status --short
git commit -m "iter-320-speech1 + iter-321-auth1: the speech-1 and auth-1 contracts landed (CONTRACTS §10 P1..P7 + §11 A1..A7 — the channel/prose/promotion/isolation/grounding/scope/forgetting definition + the pipeline/authority/ambiguity/director/agency/M4-hard-canon definition; the live falsifiers: the C8 freeze gap measured, the prose/canon boundary held, the three valid/authorized/committed axes live, the D7 eligibility set enumerated, M4 append-only; the §6..§9 falsifier-record pointer cap pass) — THE CONFIRMED QUEUE DISCHARGED, all six contracts landed"
git push
```

## G. Риски и следующее

- Риск: P4 (заморозка) и A4 (коллапс) — ЗАЯВЛЕННЫЕ законы без
  носителей; до строк имплементации текущие профили живы (монолитный
  реген; вопрос-путь без коллапса). Сознательно (definition first).
- Риск: A7 опирается на решение владельца, записанное iter-315; если
  владелец когда-либо откроет реткон-дизайн — это НОВОЕ решение,
  обходящее A7 явно, никогда тихо.
- Риск: CONTRACTS.md 929/600 — реестр семи определений стоит сверх
  потолка с ALLOWLIST; варианты за владельцем (iter-320 §G): сплит
  на по-контрактные файлы / принять постоянной формой / коллапс
  тест-сетов. По умолчанию — стояние с рационалом.
- Следующее — ВЫЗОВЫ ВЛАДЕЛЬЦА (очередь разряжена): приёмка P1..P7
  и A1..A7 (как закон или с правками); открытие строк имплементации
  (каждая — отдельно, за runtime-promotion гейтом); M2 — станционная
  батарея по вызову; стоящие строки фронтенда/мира; судьба реестра
  CONTRACTS.
