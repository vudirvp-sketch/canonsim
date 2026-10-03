# iter-320 · speech1 — контракт типизированных speech-актов и каналов (review-C8/C9/C10/C25/C26/D10)

**Вызов владельца (2026-10-04, дословно):** «продолжай работу
прошлой итерации, я принимаю Q1–Q7 как закон. Продолжай очередь с
speech-1 и так далее» — продолжение по подтверждённой очереди
(iter-315); Q1–Q7 (scale-1) приняты КАК ЗАКОН тем же вызовом
(заметка в §9); speech-1 — голова очереди.

## A. Что сделано

- **Контракт speech-1 ПРИЗЕМЛЁН** в `docs/CONTRACTS.md` §10 — семь
  пинированных решений P1..P7, каждое привязано к живому коду:
  - **P1 перечисление каналов, шесть, каждый с живым носителем:**
    (1) канонический факт — закоммиченный лог событий (INV-1);
    (2) знание-убеждение — записи знающих (L3: who/channel/
    fidelity/knows/at + source, проставленный писателем; enum
    `saw|heard|told|inferred`; цепочка fidelity
    `exact|partial|vague`); (3) восприятие — ФАЗА ПРИОБРЕТЕНИЯ
    канала (2), НИКОГДА второй стор: модель видимости
    (`rules.json::position_visibility`) + шаблоны знания действий
    чеканят saw/heard-записи; (4) типизированный speech-акт —
    ТИПИЗИРОВАННЫЙ акт через дверь интентов (грамматика действий
    пака: talk/coerce/document_check/ramble; `intent`-альтернатива
    парсера; IntentProposal медиатора) — ЕДИНСТВЕННЫЙ путь от
    социального языка к канону; (5) наррация — проза медиатора +
    рендер хроники (читающая сторона, L12); (6) диагностический
    след — метрики/обсерватория/хроника (производное, никогда
    канон).
  - **P2 свободная проза — никогда канон.** Документ ответа ЗАКРЫТ;
    `question`/`no_intent` парсера сурфейсятся и не фидятся;
    миро-утверждения прозы ПРОВЕРЯЮТСЯ против канона (клеймы),
    никогда не импортируются им.
  - **P3 путь повышения (пайплайн D10, размеченный):** проза →
    структура-кандидат (закрытое семейство документов) → нормальная
    авторизация (дверь интентов: validate_shape, предусловия, OCC)
    → семантическая валидация (цепочка резолверов, закон S1) →
    каноническое событие (`_commit`). НИКОГДА вторая дверь; два
    входа (mode-C парсер и mode-A/B медиатор) — ОДНА дверь.
    Забор namespace с auth-1 (D9): auth-1 владеет INPUT-стороны
    пайплайном, speech-1 — законами каналов.
  - **P4 изоляция каналов: допущенный структурированный акт ЗАМОРОЖЕН
    против ретраев презентации (C8) — сегодня границы НЕТ, пробел
    измерен.** Закон будущей строки: дефект презентации (форма
    прозы, пол выдуманных сущностей, противоречащий клейм) НИКОГДА
    не инвалидирует/не мутирует/не переоткрывает допущенный акт.
    Сегодня (измерено): документ монолитен — пустая проза убивает
    delta+proposal у парс-гейта; противоречащий клейм регенит ВЕСЬ
    обмен, валидные интенты умирают БЕССЛЕДНО.
  - **P5 заземление — только атомарные внешне-проверяемые
    утверждения (C9); закрытые половины по ссылке, не пересказ.**
    Виды клеймов `state|knowledge|event` (закрытый набор); вердикты
    против ТЕКУЩЕГО канона; метафоры/тон/пословное заземление ВНЕ
    ОБЛАСТИ по построению — отказ форма словаря, не суждение.
  - **P6 закон эпистемических областей: четыре; драматическая
    ирония — READ-сторона, никогда факт записи (C26).** ACTOR —
    только свои записи (фолд = память; EPIST-1); PLAYER — байты
    mode-A брифа; NARRATOR — документ вызова, ничего сверх (D-049);
    DEBUG — читающая сторона обсерватории: всё видимо, ничего
    записываемо. Ирония живёт ТОЛЬКО в композиции чтения; НИ ОДИН
    канонический канал не смешивает области.
  - **P7 явный словарь забывания (C10) + дома эпистемических полей.**
    Сегодня забывания НЕТ — фолд append-only (измерено). Забывание,
    когда потребитель назовёт себя, — ЯВНОЕ: новые события (INV-5),
    объявленный словарь, кэш может выселять для цены, но НИКОГДА не
    меняет семантический ответ (`holds` остаётся за фолдом). Дома
    полей: proposition=knows, source=id события (писатель),
    acquired_at=at, fidelity=цепочка, trust=оси relations/pare
    (НИКОГДА поле записи), status=вердикты читающей стороны
    (НИКОГДА хранимое состояние). Верованияческого графа НЕТ.
- **Фальсификатор-батарея ПРОГОНЕНА ВЖИВУЮ** (скрипт вне репо,
  Rule 9; НАСТОЯЩИЕ Simulator/Mediator/validator/ledger/knowledge
  поверх реального tavern-пака, seed 42) — см. §D.
- **Минимальный тест-сет будущей строки имплементации закреплён.**
- **Кап-проход CONTRACTS.md съехал** (кандидат из iter-319 §G):
  фальсификатор-ЗАПИСИ §6..§9 свёрнуты в указательную форму —
  дословные числа + md5-пины живут в отчётах итераций (единственный
  владелец, D-024); §10 приземлён сразу в этой форме; файл стоит
  сверх потолка (790/600) с обновлённым рационалом ALLOWLIST.

## B. Что НЕ сделано (честно)

- **Ни строчки кода** — ни канала, ни заморозки, ни словаря
  забывания, ни переписывания медиатора (закон строки).
  Имплементация — НЕ строка: владелец открывает после приёмки.
- **DECISIONS.md не тронут** (кап 30/30) — исполняется
  подтверждённая очередь; запись — CONTRACTS §10 + TASKS + этот
  отчёт.
- **llama.cpp не устанавливался** — R0/R1 строка (разрешение
  стоит, не нужно: как iter-316..319).
- **Глубокий кап-проход CONTRACTS** (сплит реестра на
  по-контрактные файлы) — НЕ сделан: превосходит названного
  кандидата, вынос на вызов владельца (см. §G).

## C. Связь с соседями

- sem-1 (§6): P3 — прямое следствие S1 (резолвер — единственный
  семантический владелец; speech-акт входит через нормальное
  допущение, гейт никогда не ре-выводит).
- scale-1 (§9): Q2-раскол «попытка vs обязательная работа» —
  фон для A2: погибший интент отказанного документа — НЕ due work
  (кандидат, никогда не допущенный); замороженный акт будущей
  строки станет видимой отсрочкой по Q2-форме.
- replay-1 (§8): INV-2-контроль тест-сета — байт-идентичность
  канона при изменении ПРОТОКОЛА обмена (заморозка меняет протокол,
  никогда поток канона).
- caus-1 (§7): клейм `event` (P5) — атомарное внешне-проверяемое
  утверждение о существовании события; необходимостная абляция
  K2 — отдельный инструмент, никогда не клейм.
- auth-1 (следующая строка): P3-забор — auth-1 владеет INPUT-пайплайном
  (интерпретация → классификация → авторизация), speech-1 —
  каналами; два словаря никогда не противоречат (двойник забора S3).
- core-1 (PARKED): P3/P4 отображаются на его C4 (LLM-граница при
  необычном взаимодействии) через пинированный namespace-забор.

## D. Проба — живой прогон (сокращённо; дословно в артефакте)

```
[ARM A] the C8 freeze gap (the measured GAP)
A1  empty prose + valid texture_delta + proposal -> NarratorError at the boundary:
    the structured half never reaches its gates (a presentation-shape defect
    kills the whole document)
A2  r1 (valid delta + valid take intent + ONE contradicted prose claim):
    status=regen — CONTRADICTED state pc_01.position == 'loc_moon' (canon: 'loc_tavern')
    events 7 -> 7: the VALID take intent died with ZERO trace
    (0 events, 0 withdrawal notes, 0 deferral records)
    ledger: tex_0000 live (the delta's accepted item stayed applied across the
    regen — the one standing partial-survival exemplar)
    r2 (the re-delivery): NO proposal at all -> accepted — the structured half
    re-delivered as ABSENT; no freeze constraint links r1's structure to r2's
A3  freeze machinery vocabulary: rg -i 'freez' over brief/ cli/ core/ = 0 hits
    ('frozen' hits are frozenset — the stdlib false friend, 74, none machinery)
[ARM B] the prose/canon boundary, BOTH ways (the LAW HELDS)
B1  prose-only ("She told the barkeep everything about the purse, and he nodded."):
    accepted, events 7 -> 7 (delta=0), the knowledge index unchanged —
    the prose rode the display channel only
B2  the SAME content as a TYPED act (proposal.intents: talk -> npc_barkeep_01):
    accepted, events 7 -> 9 (delta=2): talk (told/exact records to both) +
    rumor_told (the telling reaction) — two canonical facts from one typed act
B3  channels observed in the committed logs: {saw, told} ⊂ the schema enum
    {saw, heard, told, inferred}
[ARM C] the scope law + the forgetting inventory
C1  the live chorus drain: the player call (mode A) + 2 actor calls (mode B,
    the pack's chorus cap = 2); each document's knowledge block ⊆ its own
    knower's records (pc: 10/10, guard: 1/1, barkeep: 2/2 — OK);
    pc-only token scene_loc_tavern in NO actor doc; barkeep-only token
    conversation_with_pc_01 NOT in the guard's doc; scope separation HELD
C2  10,000 more ticks: tokens dropped by ANY holder: NONE (acquisition
    continued: +1); rg 'forget' over core/ = 2 (docstring prose only);
    rg 'belief' = 125 (docstring prose; the belief-GRAPH module ABSENT) —
    the explicit forgetting vocabulary is ABSENT (the gap record)
```

Артефакты (md5): probe `f321c149ec908d66df512866e573aa92`,
вывод `a0e73756932042f2c9e70378b405a853`. Скрипт вне репо (Rule 9).

**Смысл:** изоляция каналов (C8) сегодня ОТСУТСТВУЕТ — валидная
структурная половина умирает вместе с дефектом презентации
(пустая проза, противоречащий клейм) и не оставляет следа; граница
«проза ≠ канон» (C25/D10) ДЕРЖИТ в обе стороны — измерено живьём;
эпистемические области (C26) разделены на стороне записи; словарь
забывания (C10) ОТСУТСТВУЕТ — фолд append-only, ни один держатель
никогда не теряет токен. Риск review-C8 измерен точно; риски
C25/C26 закрыты живыми позитив-контролями; C10-пробел записан.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2557 passed + 1 skipped**
  (до/после идентично; ни один тест не удалён/ослаблен);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (ledger 10: iter-320 вошёл,
  iter-310 выселен; worklog 10: iter-310 выселен, iter-311
  восстановлен на своём месте; CONTRACTS.md — ALLOWLIST с
  обновлённым рационалом);
- `python scripts/topology.py --check` — clean;
- CONTRACTS.md 790 строк (сверх 600, ALLOWLIST + рационал в worklog
  — закон §6.1), TASKS.md 599 (кап 600), STATUS.md — форма выдержана
  (KI ≤2 строк, один DONE-блок).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/CONTRACTS.md scripts/docguard.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-320-speech1-report.md
git status --short
git commit -m "iter-320-speech1: the speech-1 contract landed (CONTRACTS §10 — the P1..P7 channel/prose/promotion/isolation/grounding/scope/forgetting definition + the live falsifier: the C8 freeze gap measured, the prose/canon boundary held both ways, the per-knower scope held, the forgetting vocabulary absent; the §6..§9 falsifier-record pointer cap pass)"
git push
```

## G. Риски и следующее

- Риск: P4-заморозка ЗАЯВЛЕНА, но носителя нет — до строки
  имплементации монолитный реген остаётся живым профилем; это
  сознательно (definition first, gate владельца).
- Риск: CONTRACTS.md стоит сверх капа (790/600) — названный
  кандидат (фальсификатор-записи → указатели) исполнен, но его
  выход мал: записи плотны по субстанции. Глубжележащие варианты —
  ВЛАДЕЛЬЦУ: (а) сплит реестра — CONTRACTS.md как индекс + каждый
  контракт своим файлом в docs/contracts/ (structural change,
  решение владельца); (б) принять стояние-сверх-потолка
  постоянной формой реестра (прецедент phases.md); (в) коллапс
  minimal-test-сетов §6..§9 в указатели (ещё ~60 строк, но слабее
  самодостаточность контрактов). По умолчанию — (б), allowlist
  обновлён.
- Риск: «perception как фаза приобретения» — терминологическое
  решение P1; имплементационная строка обязана не заводить второй
  стор (тест-сет это пинирует).
- Следующее — **auth-1** (последняя строка очереди, review-C11/C12/
  C20 + M4/D7–D9): пайплайн input → interpretation → classification
  → authorization → execution; valid != authorized; классы
  авторитета; коллапс неоднозначности только по эквивалентности
  канонических поверхностей эффекта; D7-инвариант директора +
  мутационная проба; ограниченная детерминированная агентность;
  M4-словарь — НЕСЁТ РЕШЕНИЕ ВЛАДЕЛЬЦА: M4 = ЖЁСТКИЙ КАНОН.
