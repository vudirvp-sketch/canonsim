# Отчёт итерации iter-271 — repricing: первая посадка ряда §6.4
# (FACTOR NEGOTIATION приземлён, SALE ушёл на вашу развилку,
# TAG измерен на своей границе)

> Fill-list (порядок владельца, iter-266): §6.4 → §6.1 → §6.5 → §6.2
> → W6. Эта итерация — первый ряд: FACTOR NEGOTIATION + SALE + GUILD
> ROLES + TAG TRANSFER. Приземлена переговорная дверь; продажа
> упёрлась в стену грамматики сабстрата — развилка записана на вас;
> тег измерен: механика уже живёт в паре drop+take.

## A. Главный ответ (коротко)

**Переговоры приземлены как живая арифметика: гильдия пережимает
бумагу.** Новая дверь `reprice_paper` — четвёртая в семействе
charcoalpaper (reckon_paper / render_fund / pass_the_seat /
reprice_paper), чистые пак-данные, ноль ядра. Squeeze = +2 бумаг на
стоящие условия (число самого удерживаемого маржинального запаса:
лагерь держит два воза мимо коромысла — гильдия накидывает две
бумаги на долг). Honest residue «переговоры остаются authored»
(сервис-заметка iter-189) — ЗАКРЫТ.

Ряд не закрыт целиком, и это не недоделка, а находка: **продажа
(осушение кучи) в принципе не выражается чистыми пак-данными поверх
закрытого набора глаголов** — развилка записана на ваш зов (§C).
Тег (передача значка) механикой уже живёт — граница признана
(§D).

## B. Дверь (B.1) и роли (B.2)

**B.1. `reprice_paper` — «re-price the terms».** Резолвер account,
глагол source: две бумаги минтятся на стоящие условия. Гейты:

- **standing-terms gate** — бумаг ≥ 16 на актёре: пережимать можно
  только стоящий долг; упавшая бумага не имеет условий для
  переговоров — мягкий отказ (попытка = факт);
- **receiving-stock gate** на цели — форма pass_the_seat (цель
  обязана объявить бумажный сток);
- **повторяемость** — пока условия стоят, squeeze может повторяться
  (16→18→20): компаундинг — собственная арифметика мира, не часы;
- **география — инсценировка, не гей**: бумага есть инструмент,
  слово гильдии доходит до мастера там, где дорога его найдёт
  (сказка ставит бит у коромысла — маршрут самого поручения).

Знание: свидетели (same_location, exact) узнают
`the_paper_repriced` — новые условия публичны, как публичен был
старт. Глосса несёт причинную строку: «the squeeze answering the
withhold: two more paper owed for the loads kept off the weighbeam,
the debt climbing while the bloom stays unweighed».

**B.2. Роли гильдии.** Фактор остаётся бескачельным КАК СУЩНОСТЬ —
бит едет через дверь принятия условий местом (мастер — акцептует),
агентность гильдии несут сами условия (арифметика сундука —
зеркало). Собственная сила пережима у раннера (аудит как
инструмент против мастера) — отдельная будущая строка, не эта
дверь. Так «gateless, no committed surface» закрыт честно:
поверхность есть, сущности — нет.

## C. Развилка: SALE (осушение кучи) — стена грамматики

Измерение, не мнение. Резолвер account имеет закрытый набор из трёх
глаголов с жёсткой географией сторон:

- **source** минтит ТОЛЬКО актёру;
- **transfer** идёт ТОЛЬКО от актёра к цели;
- **consume** снимает ТОЛЬКО с актёра.

Куча (ledger удержки) лежит на **loc_crofts** — локации. Локация в
интенте бывает только ЦЕЛЬЮ (trade_at_market/render_fund передают
coin В loc_malby), но никогда ИСТОЧНИКОМ: акторами могут быть
только PC/NPC. Значит, «bloom уходит со стока локации» не
выражается никакой комбинацией закрытого набора. Кандидаты:

| Вариант | Цена | Вердикт по записи |
|---|---|---|
| (a) дверь цены: coin покупателя → сток лагеря, осушение ledger — residue | ноль ядра; куча НЕ падает (память удержки не тратится) | на ваш зов —_semantically тонко |
| (b) пересадить кучу на мастера | сток меняет владельца; стоки в тестах перепинываются; **главное: место ledger семантично** — «banked at the crofts where the tally's notches record it», якорь rs-10 | ОТКЛОНЁН по записи |
| (c) глагол осушения со стороны локации (location-side drain verb) | ядро, R3+ (schema/резолвер/линт), инварианты сабстрата | на ваш зов — если продажа обязана тратить кучу |

Выбор не сделан молча (§11 AGENTS/D-198): развилка записана в
ANCHOR_REGION §6.4, WORLD_TESTS §9, WORKPLAN §7 и в economy-notes
правил.

## D. TAG TRANSFER — граница

Передача значка (camp_tally_01, несёт мастер): механика УЖЕ живёт в
паре **drop + take** — закон переносимости носителя (drop кладёт
значок бесхозным, take поднимает новой рукой; give-глагола не
существует и не должен). Чего нет — минта признания (слово артели:
«badge follows the camp's word») — бессурсная поверхность, закон
iter-185 не тронут. Вывод: тегу не нужна дверь, ему нужна строка
признания — будущая, по вашему зову.

## E. Измеренное

- Твин (macro 480, seed 42): бумага 16→18→20 на двух повторах
  squeeze; свидетели (Maren на рынке) несут the_paper_repriced;
  сказка несёт строку с глоссой вида: «Garrick comes by 2 paper
  owed to the guild's chest at Malby since the starved winter at
  the year's reckoning.»;
- упавший мир (бумага 0): мягкий отказ intent_rejected;
- цель без стока (Maren): мягкий отказ;
- золотой корпус байт-в-байт (нулевая цена корпуса: дверь не
  вооружена доктриной — ни urgency, ни хука);
- твин детерминирован.

## F. Честные границы

- Ряд §6.4 не закрыт: продажа — ваша развилка (§C), признание тега
  — будущая строка (§D). Fill-list продолжается: §6.1 → §6.5 →
  §6.2 → W6.
- Фактор не получил сущность (осознанно: агентность в терминах,
  не в энтити).
- Направление пережима — ВВЕРХ (squeeze) — авторский зов этой
  посадки; примирение ВНИЗ (реконcилиация: побритый маржин
  возвращён) — контрфактическая рука той же двери, ваша будущая
  строка.
- D-строка в DECISIONS не заведена (кап 30/30, коллапс только по
  вашему явному зову): запись живёт в WORLD_TESTS §9 (хозяин),
  WORKPLAN §7, ANCHOR_REGION §6.4, phases.md §6.

## G. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2484 passed + 9 skipped
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

Изменённые пути (10): content/province_pack/actions.json,
content/province_pack/templates.json,
content/province_pack/rules.json, tests/test_repricing.py (новый),
docs/worldbuild/WORLD_TESTS.md, docs/worldbuild/WORLD_WORKPLAN.md,
docs/worldbuild/ANCHOR_REGION.md, docs/blueprint/phases.md,
docs/TASKS.md, docs/iterations/iter-271-repricing-report.md (новый),
STATUS.md, worklog.md.

## H. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add content/province_pack/actions.json content/province_pack/templates.json content/province_pack/rules.json tests/test_repricing.py docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/worldbuild/ANCHOR_REGION.md docs/blueprint/phases.md docs/TASKS.md docs/iterations/iter-271-repricing-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-271-repricing: the §6.4 fill row's first landing — the renegotiation door (the squeeze) + the sale's measured grammar-wall fork + the tag's boundary; the honest residue 'the renegotiation stays authored' closed"
git push
```
