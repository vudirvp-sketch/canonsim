# iter-332 · stageb1impl1 — механики материального цикла посажены: конверсия (B2), износ через use-hook (B3), ёмкость (B4) + руки линта; unarmed-закон держится

**Вызов владельца:** продолжение «можешь начинать (stageb-1 и
scale-1) и прочее» — строка `stageb-1-impl`, половина движка
(порядок rng-1 исполнен: byte-identical строки scale-1 посажены
iter-330/331, стена теперь ~линейна — рёбра stageb садятся на
ускоренную машину). BASE_COMMIT: рабочее дерево iter-331. Задача
ID: `iter-332-stageb1impl1`.

**llama.cpp не устанавливался** — механики сабстрата счета,
LLM-free.

## A. Что сделано

### A.1 B2 — глагол конверсии (account_converted)

`core/economy.py::convert_resolution` + резолверная рука в
`core/resolvers.py`: действие объявляет
`account: {verb: "convert", recipe: "<id>"}`; рецепт — данные пака
(`economy.recipes`: id, inputs [{holder, kind, amount}],
outputs [...]); событие ОДНО — входные ноги сливают, выходные
производят, чистое изменение на каждый тронутый (entity, kind)
(агрегационный закон settle); outcome несёт recipe + разрешённые
ноги (диагностируемость флоу-формы). Консервация ПО РЕЦЕПТУ на
kind — сворачиваемо проверяема (закон теста). Float-закон по
построению: никакая вторая цепочка не читает до-первое состояние.

### A.2 B3 — износ через use-hook

`core/loop.py`: действие объявляет
`instrument: {holder, kind, amount}` — на УСПЕШНОЕ завершение
действия коммитится ОДНО `account_consumed` (актор = работник,
target = держатель, outcome `use` = действие — инструмент ПОИМЁН).
Слом на нуле: переход через 0 — ПОСЛЕДНИЙ use (коммитится); ниже
нуля — мировая невозможность, мягкий отказ двери (линт-обязательный
гейт account_at_least — попытки суть факты). Никаких часов
настенных (забор I5 цел). Неудачная проверка (on_failure) — износа
нет (попытка — факт, запас — нет).

### A.3 B4 — ёмкость источника

`flow_drafts`: source-флоу с `capacity` — минт
min(declared, capacity − stock); при полном запасе флоу НЕ
наступил (ноль событий, форма every-miss). `_commit`-пол: запись
выше объявленной ёмкости — ГРОМКО, любой глагол (рука B1 «никогда»);
свои минты машина не нарушает (min()-арифметика), потому прорыв =
рука или баг пака. Арифметика тик+запас, без жребия (INV-2-чисто).

### A.4 Руки линта (B8) + рендерер

`core/packlint/economy.py`: recipes (форма, словарь, суммы,
уникальность id; cross-phase — явные держатели объявляют счёт) +
capacity (int ≥ 1, только source, ОДНА ёмкость на запас).
`core/packlint/actions.py`: convert-форма (закрытые ключи, рецепт
существует, per-input-leg гейт = KI#15-семейство, restatement
типа события) + instrument-блок (форма, гейт ≥ amount, holder
объявляет счёт). Рендерер: input_/output_ индексные слоты (закон
ног settle, один префикс на сторону).

## B. Измерено

- **2603 passed + 1 skipped** (+11 законов), ruff clean, docguard
  clean, topology clean.
- **B5 unarmed-закон**: farthest 2y segmented md5
  `c7a6959a29c2…` — равен эталону ДО механик (ни одно
  коммитнутое оружие не тронуто, корпус-цена ноль; вооружение
  farthest — цена строки iter-333).
- **Законы** (tests/test_stageb_impl.py): атомичность+консервация
  на фолде; мягкая дверь (insolvent → intent_rejected, попытки —
  факты); громкий пол ёмкости (ручной драфт 99 против cap 7 →
  ValueError, запись не landed); плато (mint 3 → запас 7 →
  тишина); частичный минт (6/7 → минт 1); спаривание износа
  (wears == completions, инструмент поименён, запас/итог на
  фолде); break-at-zero (0-переход коммитится, следующая попытка
  мягко отвергнута); read-дисциплина (B7: поверхности — чтения
  проекции, громкие backstop'ы EconomyError); 8 отказов линта;
  детерминизм вооружённого прогона (двойной прогон байт-в-байт).

## C. Что НЕ сделано (честно)

- **Вооружение farthest** (рецепт forge, привязки износа,
  ёмкости) + **батарея B6 REALIZED_DELTA** — iter-333 (цена
  корпуса едет с вооружением, не с механиками).
- DECISIONS.md не тронут: кап 30 держится docguard'ом жёстко;
  **R3 PCC-запись едет в §G этого отчёта** (прецедент iter-322 —
  «приёмки/записи едят своих конкретных владельцев»; D-252 была
  попытана и откачена по флагу стража).

## D. Риски

- R3: механики кросс-модульные (economy/resolvers/loop/packlint/
  render), но семантика едет ТОЛЬКО на декларациях пака (B5
  измерен); INV-1 (всё через `_commit`), INV-2 (без жребия,
  детерминизм тестом), INV-3 (стоплист зелёный), INV-4/5 не
  тронуты.
- Пол ёмкости «любой глагол» (рука B1 «никогда») — строже буквы
  B4 («source-запись»):transfer в заполненный capped-запас теперь
  невозможен тоже; семантически честно (ёмкость = физическая граница
  запаса), зафиксировано в докстринге пола. Если владельцу нужна
  «магическая переливка свыше cap» — пак просто не объявляет
  capacity.

## E. Дальше

1. **iter-333 stageb1impl2** — вооружение farthest (рецепт
   forge_tool: входы ore+wood мастерской, выход tool; износ на
   рабочих глаголах; ёмкости четырёх источников) + батарея B6
   (мёртвая куча умирает / линейный рост ломается о ёмкость /
   оборот инструментов ограничен) + расширение закона консервации
   в test_farstead_pack.
2. Стоящие вызовы владельца сохранены (P0.5-C, rng-1, E02/E31,
   M2, replay-UI, W8, фронтовые P1/P2/P3).

## F. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/economy.py core/resolvers.py core/loop.py core/packlint/economy.py core/packlint/actions.py render/chronicle.py tests/test_stageb_impl.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-332-stageb1impl1-report.md
git status --short
git commit -m "iter-332-stageb1impl1: the material cycle's engine mechanics — the convert verb (B2) + the use-hook wear (B3) + the capacity cap (B4) + the lint arms (B8); the unarmed law held"
git push
```

## G. R3 PCC-запись (§2.9; DECISIONS на капе 30 — запись едет здесь, прецедент iter-322)

**(R3)** [PCC: intent=посадить три ребра материального цикла как
механики движка над сабстратом счёта, пак-декларируемые, за
открытым владельцем runtime-promotion-гейтом (контракт §12
принят тем же вызовом); invariants=INV-1 (каждое ребро коммитит
через единственную `_commit`-дверь — событие рецепта, износ,
ёмкостный минт — все EventDraft), INV-2 (арифметика ёмкости
тик+запас без жребия, рецепты без жребия, износ детерминирован —
вооружённый двойной прогон байт-в-байт, тест), INV-3 (ноль
сеттинг-слов — стоплист зелёный; рецепты/износ/ёмкость — данные
пака, движок несёт механику), INV-4/5 не тронуты (сети нет,
лог не редактируется); delta=core/economy.py (+CONVERT_EVENT,
RECIPE_KEYS, recipe_of/convert_resolution/source_caps/wear_draft
+ ёмкостный flow_drafts), core/resolvers.py (convert-рука),
core/loop.py (use-hook на _complete + мемо ёмкостей + пол ёмкости
в _commit + _instrument_holder), core/packlint/economy.py
(recipes+capacity+cross-phase), core/packlint/actions.py
(convert+instrument), render/chronicle.py (input_/output_-слоты),
tests/test_stageb_impl.py (11 законов); verification=2603+1 +
ruff + docguard + topology clean + unarmed byte-identity (md5
farthest 2y равен) + вооружённые законы (атомичность/консервация,
мягкая дверь, громкие полы, плато, частичный минт, спаривание
износа, break-at-zero, 8 отказов линта, детерминизм);
provenance=вызов владельца «§12 (B1..B8) = принимаю, можешь
начинать (stageb-1 и scale-1) и прочее» — контракт принят тем же
сообщением; runtime=рёбра стреляют только на декларациях пака
(unarmed-закон), вооружение farthest — следующая строка со своей
ценой корпуса; rollback=git revert — механики аддитивны, ни один
коммитнутый пак не вооружён.]
