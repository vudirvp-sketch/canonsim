# iter-318 · replay1 — контракт тождества семантического replay + долговечности восстановления (review-C4/C7/C13/D4)

**Вызов владельца (2026-10-03, дословно):** «продолжай работу прошлой
итерации, я принимаю S1–S7 и K1–K6 как закон. Продолжай очередь с
replay-1 и так далее» — приёмка двух контрактов предыдущей пары + очередь
с replay-1.

## A. Что сделано

- **Приёмка зафиксирована:** S1–S7 (sem-1) и K1–K6 (caus-1) ПРИНЯТЫ
  ВЛАДЕЛЬЦЕМ КАК ЗАКОН — однострочные заметки в CONTRACTS.md §6/§7.
  Строки имплементации НЕ открыты (gate владельца: отдельный вызов).
- **Контракт replay-1 ПРИЗЕМЛЁН** в `docs/CONTRACTS.md` §8 — шесть
  пинированных решений, каждое привязано к живому коду:
  - **E1 identity-кортеж, шесть компонент**:
    `log_prefix_digest + engine_semantic_version + schema_identity +
    pack_semantic_digest + execution_config_digest + seed`. Отвечает на
    вопрос «может ли это исполнение легитимно ПРОДОЛЖИТЬ другое или
    сравнивать БУДУЩЕЕ с ним» — никогда «равны ли логи байт-в-байт»
    (это T1, другой вопрос). Против живых носителей: seed,
    prefix-digest, schema-версия — НОСЯТСЯ И ПРОВЕРЯЮТСЯ; pack-контент
    / commit движка / execution-config — ТРИ ИМЕНОВАННЫХ ПРОБЕЛА
    (триаж iter-315, теперь кодово обоснованы).
  - **E2 семантическая тождественность ≠ состояние продолжения.**
    Identity спрашивает «тот же мир?» — несовпадение = ОТКАЗ (другой
    мир, никогда предупреждение); continuation спрашивает «где в этом
    мире остановилась сессия?» — несовпадение = УСТАРЕВАНИЕ (другая
    точка того же мира, тоже громко — действующий закон
    против save-scumming). Никогда не смешиваются: identity-компонент
    не ездит в курсоре, continuation никогда не становится identity.
  - **E3 неприводимое состояние продолжения — ЗАКРЫТОЕ МНОЖЕСТВО**:
    позиции банка, director-метки, тик часов, курсоры пересечений
    (rotation/beat/macro/calendar), intent-счётчик, живой тумблер
    директора. Ничего сверх: новое рантайм-поле обязано объявить свою
    сторону (identity / continuation / non-canon) и доказать
    неприводимость.
  - **E4 жизненный цикл: proposed → accepted → durable → committed.**
    Draft продюсера → проверки двери `_commit` (schema + delta +
    chain) → граница долговечности (сегодня — flush; её OS-семантика
    не доказана, E6) → commit с инвариантами продолжения. Потерянное
    не-durable событие НИКОГДА НЕ СУЩЕСТВОВАЛО — не откат, а
    непроизошедшее событие.
  - **E5 crash-контракт, три границы:** append-before-durable (правда
    — последний durable префикс; детекция ГРОМКО: оборванная строка —
    LogError, хвост за пином курсора — отказ; ремонт — дело строки
    имплементации со своим crash-куррикулумом); post-durable (лог
    ушёл за пин — энтропия невосстановима, громкий отказ — действующий
    закон); derived-state (чекпоинты/индексы/хроника — производное,
    никогда правда; краш стоит цены пересборки, никогда канона).
  - **E6 `flush == durable` ОТВЕРГНУТО** как бездоказательное
    утверждение: писатель делает flush (3 места: header, append,
    close) и НИ РАЗУ fsync (0 вызовов по core/). Доказано: логическая
    долговечность чистых границ (D-139, test_resume —
    байт-тождественность на каждой точке сплита, то же окружение).
    НЕ доказано: OS-уровень. fsync-политика / crash-куррикулум —
    строка имплементации, никогда «durable» на одном flush.
- **Фальсификатор ПРОГОНЁН ВЖИВУЮ** (скрипт вне репо, Rule 9; корпус
  test_resume: seed 42, move/steal/wait-760/move, сплит после шага 2) —
  см. §D.
- **KI#111 открыт и закрыт по ходу** (AGENTS §5 record-then-fix):
  Arm C нашёл живой дефект — `read_log` на оборванной строке бросал
  ГОЛЫЙ `JSONDecodeError` вместо контрактного `LogError` (читательский
  конверт, ноль изменений сериализации). Фикс — обёртка в `core/log.py`
  + 1 тест (RED→GREEN). Единственное кодовое изменение итерации.
- **Минимальный тест-сет будущей строки имплементации закреплён.**

## B. Что НЕ сделано (честно)

- **Ни строчки сериализации** — ни поля дайджеста в header/cursor, ни
  fsync-политики, ни crash-куррикулума (закон строки: сериализация не
  меняется до приёмки контракта). Имплементация — НЕ строка: владелец
  открывает после приёмки.
- **DECISIONS.md не тронут** (кап 30/30) — исполняется подтверждённая
  очередь (review-D4 принят iter-315); запись — CONTRACTS §8 + TASKS +
  этот отчёт.
- **llama.cpp не устанавливался** — R0/R1 строка (разрешение стоит,
  не нужно: как iter-316/317).

## C. Связь с соседями

- sem-1 (§6) / caus-1 (§7): та же дисциплина «определение сначала,
  фальсификатор с ним»; E5(a)-детекция — читательский близнец S4/S5
  (громкая граница, один владелец на закон).
- scale-1 (следующая строка): replay-тождество — предпосылка любых
  масштабных заявлений о «той же истории» (core-1-C5 берёт
  byte-identical replay как планку; E1 — её семантическое расширение).
- core-1-C3 (история/масштаб): цена replay/чекпоинтов на больших
  логах — measured-native-limit-вопрос core-1, не этот контракт.
- M4/жёсткий канон: E4 «commit необратим, потерянное не-durable
  событие не существовало» — согласовано с решением владельца
  (невозможность реткона), но не перекрывается.

## D. Проба — живой прогон

```
[CONTROL] uninterrupted: 25 lines, 24 events, md5 6cc1e753ccf1066f3bc472054947a228
[CONTROL] split+resume byte-identical to uninterrupted: True   ← D-139 держится
[ARM A] drift pack: name_version unchanged (tavern_pack@0.1),
        beat_ticks [360,720,1080] -> [100,200,300]
[ARM A] resume with the DRIFT pack: ACCEPTED (no refusal)
[ARM A] cursor pin: 7 events; shared prefix identical: True
[ARM A] control tail (17 events): [watch_change, expectation_violation,
        suspicion_changed, knowledge_transfer, ...]
[ARM A] drift   tail (23 events): [status_decayed x23]
[ARM A] first divergence at appended-event index 0 (watch_change vs
        status_decayed) — SAME identity, DIFFERENT future execution
[ARM B] the split log's header commit: '0000000'
[ARM B] Simulator.resume reads/compares header['commit']: False
[ARM B] resume with commit='deadbee2': ACCEPTED silently
[ARM C] EventLogWriter: fsync calls = 0, flush() calls = 3
[ARM C] 'os.fsync' occurrences across core/*.py: 0
[ARM C] torn tail: LOUD LogError — torn.jsonl:25: malformed JSON line
[ARM C] lost pre-pin tail (log 6, cursor pins 7): LOUD CursorError
[SUMMARY] CONTROL HELD; Arm A DEMONSTRATED; Arm B DEMONSTRATED;
        Arm C DEMONSTRATED
```

Артефакты (md5): вывод пробы `52cba69fcca1040fb4f0c19053293c99`;
контрольный лог `6cc1e753ccf1066f3bc472054947a228` (= сплит:
байт-тождественность); дрейф-лог `c496695d1ada24cbddaa29d80b49c7c6`.
Скрипт вне репо (Rule 9).

**Смысл:** тождество, которое сегодня видит курсор (seed +
pack@version + prefix-digest), пропускает ДРЕЙФ КОНТЕНТА ПАКА под тем
же именем — resume молча принимает, и продолжение расходится с ПЕРВОГО
добавленного события (17 против 23 событий, разные семейства). Метка
движка в заголовке декоративна — resume её не читает. `flush` не
является долговечностью (0 fsync), но детекция крашей на обеих
границах — громкая (torn/lost хвосты). Риск review-C4 («same log
prefix can produce a different future execution») продемонстрирован
вживую; найденный по пути KI#111 закрыт в той же итерации.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2557 passed + 1 skipped**
  (до: 2556+1; +1 — тест KI#111; ни один тест не удалён/ослаблен);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (ledger 10: iter-318 вошёл,
  iter-308 выселен; worklog 10: iter-308 выселен);
- `python scripts/topology.py --check` — clean;
- CONTRACTS.md 589 строк (кап 600), TASKS.md 599 (кап 600),
  STATUS.md — форма выдержана (KI ≤2 строк, один DONE-блок).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/CONTRACTS.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-318-replay1-report.md core/log.py tests/test_core.py
git status --short
git commit -m "iter-318-replay1: the replay-1 contract landed (CONTRACTS §8 — the identity tuple E1..E6 + the live falsifier: same-name pack drift resumes and diverges, the commit label unchecked, flush!=durable; KI#111 closed — read_log's torn-line LogError)"
git push
```

## G. Риски и следующее

- Риск: identity-кортеж определён, но его компоненты НЕ реализованы —
  до строки имплементации дрейф пака под тем же именем остаётся
  живым; это сознательно (definition first, gate владельца).
- Риск: «durable» в E4 сегодня = flush — контракт фиксирует это как
  ЧЕСТНУЮ, но неполную границу; любое заявление об OS-долговечности
  требует fsync + crash-куррикулум (строка имплементации).
- Риск: commit-метка — прокси семантической версии движка (два коммита
  могут быть семантически идентичны, грязное дерево — лжёт); вопрос
  гранулярности — открытая точка для строки имплементации.
- Следующее — **scale-1** (каузальная локичность спроса + бюджет
  работы + сертифицированная коммутативность, review-C5/C6/C16/C28/
  D5+D6): LOCAL/REGIONAL/GLOBAL от каузального спроса; бюджет явный —
  исчерпание = отложить (семантический долг), никогда молча бросить;
  параллельная когорта только с proof obligation; измерение
  `world size × fan-out × operation → inspected/candidate/committed +
  wall time`; в задаче определения — никаких индексов, CRDT/MVCC,
  планировщиков.
