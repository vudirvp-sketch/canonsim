# Отчёт итерации iter-273 — settlement: §6.4 SALE разрешён
# через генерализованный аккаунт-сабстрат (синтез владельца)

> Решение владельца 2026-09-27: развилка iter-271 — не выбор A/B/C, а
> свидетельство, что грамматика счетов уже тесна для авторской модели
> мира. Правильный ответ — синтез: минимальное генерическое расширение
> сабстрата, сняющее КЛАСС ограничений, никогда — дверца под случай.
> Эта итерация — первый пункт порядка исполнения: SALE разрешён,
> семантический результат закреплён регрессией.

## A. Главный ответ (коротко)

**Стена грамматики была настоящей — и она измерена ПЕРВОЙ.** Три
факта, закреплённые в свидетеле до всякой реализации: (1) закрытый
набор глаголов не несёт ключей эндпоинтов вовсе — сторона списания
ВСЕГДА актёр интента; (2) грамматика плейскрипта жёстко пинит актёров
к NPC — локация не может инициировать (громкий отказ); (3)
крафтовый transfer-зонд поверх кучи отказан мягко на СОБСТВЕННОМ
гейте актёра — гора bloom стоит у ног мастера, но закрытый глагол не
может списать ни одной ноши. Ограничение — в ГРАММАТИКЕ, не в
авторинге пака и не в маршрутизации действий.

**Синтез: четвёртый глагол `settle`.** Блок account получает форму
LEGS: каждая нога — свои from/to (существительные actor/target или
ЯВНЫЕ id сущностей, объявивших сток — закон флоу-эндпоинтов), свой
kind и amount; каждая нога — свой гейт платежеспособности (форма
HOLDER для явных id — словарь существительных не расширен); все ноги
— ОДНО атомарное каноническое событие `account_settled` (один чистый
state change на затронутый сток, пол коммит-гейта — нетто). Второго
транзакционного движка нет: дверь интента, реестр резолверов,
коммит-гейт и фолд не изменились по форме.

## B. Вооружение §6.4: `sell_bloom`

Продажа перегруза — освобождение удержки, ровно та семантика, что
стояла за развилкой:

- **нога bloom**: loc_crofts → loc_malby (одна ноша в приёмный сток
  луча — терминус фрахта стал стоком, loc_malby bloom 0);
- **нога coin**: loc_malby → loc_crofts (цена ТРИ монеты за ношу —
  собственная арифметика «gross nine at three the load» — из сундука
  гильдии в ЛАГЕРНУЮ КНИЖКУ ЛАГЕРЯ, loc_crofts coin 0: «banked at
  the crofts where the tally's notches record it», якорь rs-10).
  Куча НЕ пересажена — отказ (b)_record соблюдён;
- **инициатор — мастер** (вопрос взвешивания — его собственный:
  доставить bloom на луч или держать); стороны сделки — держатели
  самих ног, ни одна не инициатор: класс-закон владельца стал
  арифметикой;
- **география** — форма render_fund (продажа у луча, мастер в
  Малби); **повторяемость** — пока куча стоит и сундук покрывает
  (компаундинг — арифметика мира, не часы);
- **свидетели** (same_location, exact) узнают `the_bloom_sold`;
  строка сказки несёт глоссу вида через слот ноги (граница rs-2):
  «Garrick settles at Malby, the market town: 1 bloom kept off the
  weighbeam since the guild factor shaved the camp's weight two
  seasons back and the camp starved that winter — the withhold's own
  ledger for 3 coin.»;
- **безоружно по доктрине** (ни urgency, ни хука) — золотой корпус
  байт-в-байт, нулевая цена корпуса.

## C. Пин класса (пример самого владельца)

Крафтовая дверь покупки ПОКУПАТЕЛЕМ — «buyer pays coin + crofts
surrender bloom + buyer receives bloom + crofts receive coin» — на
ТОМ ЖЕ глаголе: ноги-существительные (from/to «actor»), явные id и
обе формы гейтов в одном блоке. Одно атомарное событие, четыре чистых
изменения (pc coin 6→3, книжка 0→3, куча 8→7, pc bloom 0→1). Тот же
механизм завтра обслужит пошлины, расчеты, изъятия, оплату труда,
движение институциональных запасов — без единой новой двери под
случай.

## D. Измеренное (seed 42, макро-480 твин)

- продажа: ОДНО событие, четыре изменения (куча 6→5, приёмник луча
  0→1, сундук 44→41, книжка 0→3 — одно пересечение года в дороге
  beforehand пополнило кучу и сундук);
- компаундинг: три продажи — куча 6→5→4→3, книжка 0→3→6→9;
- мягкие отказы: пустая куча → `loc_crofts.account_at_least`, тонкий
  сундук → `loc_malby.account_at_least` (попытки — факты, записей
  состояния нет);
- линт: 11 форм ног отбракованы на загрузке (закрытые словари
  блока и ноги, необъявленные эндпоинты/стоки, нога без гейта,
  self-leg, неверный restatement, нулевой amount, пустой список) —
  семейство KI#15;
- потолок шаблонов честно переобъявлен 75 → 80 (строка settle —
  корпусная цена четвёртого глагола), пины charcoalpaper/winterkin/
  debt1/freightvol пере-закреплены.

## E. Честные границы

- Изъятие из лагерной книжки в фонд мастера (withdrawal) — будущая
  строка, не эта: дверца не вооружена, грамматика уже выражает.
- Цена остаётся АВТОРСКОЙ (три за ношу, никогда производная формула
  — цена луча есть поверхность бритья, изъян Марен, закон freightvol
  не тронут).
- D-строка в DECISIONS не заведена: файл на капе 30/30, коллапс —
  только по вашему явному зову (D-034/D-185); PCC-запись R3 едет в
  phases.md §6 (полная форма) + WORLD_TESTS §9 (хозяин результата).
- Приёмный сток луча (loc_malby bloom) и лагерная книжка
  (loc_crofts coin) засеяны нулями — существование, а не запас;
  потоки их не трогают.

## F. Порядок исполнения (ваш, зафиксирован в WORKPLAN §7)

```text
1. §6.4 SALE через генерализованный синтез     ← СДЕЛАНО (iter-273)
2. Верификация + регрессионный пин             ← СДЕЛАНО (свидетель)
3. §6.5 (move-release, цена iter-263)          ← следующая строка
4. §6.2 (PRESENT / HATCH / NOTCH)
5. I0 World Ignition Witness (первое
   доказательство world-liveness / moving-meso)
6. Новая рантайм-механика — только если I0
   вскроет конкретный повторный субстратный лимит
7. W6 под полученной очевидностью
```

## G. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2506 passed + 9 skipped
✓ ruff check . — clean
✓ python scripts/docguard.py — clean
✓ python scripts/topology.py --check — clean
✓ LOG не тронут; золотой корпус байт-идентичен (нулевая цена)
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

Изменённые пути (19): core/economy.py, core/resolvers.py,
core/intent.py, core/packlint/actions.py, core/packlint/shared.py,
render/chronicle.py, content/province_pack/actions.json,
content/province_pack/entities.json,
content/province_pack/templates.json,
content/province_pack/rules.json, tests/test_settlement.py (новый),
tests/test_economy.py, tests/test_freightvol.py, tests/test_debt1.py,
tests/test_charcoalpaper.py, tests/test_winterkin.py,
docs/worldbuild/WORLD_TESTS.md, docs/worldbuild/WORLD_WORKPLAN.md,
docs/worldbuild/ANCHOR_REGION.md, docs/blueprint/phases.md,
docs/iterations/iter-273-settlement-report.md (новый), STATUS.md,
worklog.md — превышение мягкого лимита §2.3 отмечено: R3-срез
сабстрата не делится без потери атомарности.

## H. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/economy.py core/resolvers.py core/intent.py core/packlint/actions.py core/packlint/shared.py render/chronicle.py content/province_pack/actions.json content/province_pack/entities.json content/province_pack/templates.json content/province_pack/rules.json tests/test_settlement.py tests/test_economy.py tests/test_freightvol.py tests/test_debt1.py tests/test_charcoalpaper.py tests/test_winterkin.py docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/worldbuild/ANCHOR_REGION.md docs/blueprint/phases.md docs/iterations/iter-273-settlement-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-273-settlement: the §6.4 SALE fork resolved through the generalized account transaction — the fourth verb settle (legs over explicit owners, holder gates, one atomic event) + the re-weigh's sale armed + the class pinned with the buyer's purchase"
git push
```
