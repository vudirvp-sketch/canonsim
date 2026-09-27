# Отчёт итерации iter-267 — поверхность обнаружения обиды раннера:
причинная строка едет на самой строке холда

> Первая строка зафиксированного владельцем порядка (W5-disposition
> iter-266: ADD DISCOVERY SURFACE — обида раннера, «минимальная
> причинная поверхность: standing → remembered incident → why the
> grudge exists, НЕ биография раннера»). Отвечает на datum живой
> полосы iter-208: человеческий читатель сам заметил standing обиды
> («гонец-фактор теперь держит что-то над Гарриком»), но причины и
> последствия не проходили через доступную поверхность.

## A. Главный ответ (коротко)

Поверхность приземлена READ-SIDE, ноль изменений канона, ноль цены
корпуса. Сама строка холда теперь несёт причинную строку —
пак-авторизованный глосс секрета через knows-границу:

```text
БЫЛО:  the factor's runner now holds something over Garrick.
СТАЛО: the factor's runner now holds something over Garrick — the
       camp's word: the honest count cut in the tally; the guild
       factor shaved the camp's weight two seasons back and the camp
       starved that winter, and the bloom has sat off the weighbeam
       since.
```

Три ячейки причинной строки владельца — все в одной строке:

| Ячейка | Как рендерится |
|---|---|
| standing | холд — слово лагеря: честный счёт, зарубленный на тали-палке |
| remembered incident | бритьё: фактор гильдии недовесил лагерь две зимы назад — голодная зима |
| why | удержка: блум со спящих весов с тех пор — ответ лагеря наклонному коромыслу |

Читатель теперь собирает всю дугу: гонец дома, который побрил лагерь,
держит доказательство ответа лагеря. Ирония §6.4 (обе половины
считают другую любимцем гильдии) собирается без единой новой строки
прозы.

## B. Механизм (rs-9 — глосса холда, форма семейства account/flow)

Повторена проверенная форма rs-2/rs-4, минимальное расширение
существующего механизма (AGENTS §2.8: existing mechanism → minimal
extension):

1. **Одна строка таблицы** — `templates.json::knows`,
   `the_camps_word` → проза причинной строки. Слова живут в паке.
2. **Одно плечо строки** — хвост-условие в строке `leverage_gained`:
   `{secret? — {secret}}` — точная форма банковского хвоста
   `{flow? — {flow}}` (rs-4).
3. **Одно расширение границы** — `render/chronicle.py`: исходящий
   ключ `secret` события проезжает через knows-границу (rs-1: одна
   таблица, каждый потребитель — путь рассказа, путь свидетеля,
   теперь путь холда). Без глоссы — предсеад "" (закон машинного
   токена из семейства flow): неглоссированный секрет НЕ меняет
   строку вообще, включая чужой лог.

Диспозиция rs-1 (iter-188) называла эту границу явно: «read-hinge
secrets рендерятся dry by design; их качество рендера — граница,
которую зонд называет, но не пре-эмптивная фича рендерера». Зов
владельца iter-266 открыл ряд — граница получила свою первую
авторизованную строку.

## C. Измеренные улики

- **Живая цепь** (seed 42, день + ночь): сказка несёт все ячейки
  строки; ночное плечо с partial-fidelity — то же слово, та же строка
  (кластер записывает «насколько хорошо», история — нет).
- **Неглоссированный закон на коммитнутом корпусе**: у фикстуры grim
  единственный leverage_gained (`scraps_pawned_by_maid`, без строки в
  таблице) рендерит сухую строку без хвоста; строка траты
  (`proposition_coerced`, тот же ключ исходящего события) не тронута.
- **Нулевая цена корпуса**: провинциальный smoke регенерирует
  байт-в-байт (шаблоны не меняют ни одного байта рантайма — закон
  iter-265); прочие четыре пака не имеют строк для своих секретов — их
  строки не изменились.
- **Твин**: одна (лог, пак) → одни и те же байты сказки.
- Свидетель: `tests/test_grudgesurface.py` — 9 тестов, claim-packet
  по TEST_PLAN §9 (включая плечо «строка едет и через путь
  рассказа» — слух с токеном рендерит ту же прозу, закон
  каждого-потребителя).

## D. Честные границы

- Ряд — только ПРИЧИННАЯ поверхность. Временная позиция бритья
  (раньше-сезон → голодная зима → событие → настоящее следствие) —
  материал СЛЕДУЮЩЕЙ строки порядка: dated-memory поверхность
  бритья. Здесь не предвосхищена.
- Остальные три read-hinge секрета (the_flood_story, the_winter_kin,
  figure_reaching_for_tin) остаются без глоссов: каждый — свой ряд по
  зову владельца (запрещение молчаливого расширения охвата, тот же
  закон iter-266: поверхность не должна лишь потому, что связь не
  собралась).
- Поверхность — строка СКАЗКИ. Токен в recalled_facts брифа остаётся
  сухим (закон брифа — рабочий документ медиатора, не читательская
  поверхность); pair-строка брифа после угла — своя форма, там же где
  была.
- D-строка в DECISIONS не заведена (файл на капитции 30/30, коллапс
  только по явному зову — форма всех записей станции W5): запись
  живёт в WORLD_TESTS §9 (хозяин), WORKPLAN §7 (порядок),
  ANCHOR_REGION §6.4 (ряд юнита), phases.md §6.

## E. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2470 passed + 9 skipped
✓ ruff check . — clean
✓ python scripts/docguard.py — clean
✓ python scripts/topology.py --check — clean
✓ LOG не тронут; фикстуры байт-в-байт (нулевая цена корпуса)
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest -q tests/test_grudgesurface.py
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

Изменённые пути (11): render/chronicle.py,
content/province_pack/templates.json,
tests/test_grudgesurface.py (новый),
docs/worldbuild/WORLD_TESTS.md, docs/worldbuild/WORLD_WORKPLAN.md,
docs/worldbuild/ANCHOR_REGION.md, docs/blueprint/phases.md,
docs/TASKS.md, docs/iterations/iter-267-runner-grudge-surface-report.md
(новый), STATUS.md, worklog.md.

## F. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add render/chronicle.py content/province_pack/templates.json tests/test_grudgesurface.py docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/worldbuild/ANCHOR_REGION.md docs/blueprint/phases.md docs/TASKS.md docs/iterations/iter-267-runner-grudge-surface-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-267-grudgesurface: the runner's grudge discovery surface — the hold's line carries the causal row through the knows boundary"
git push
```
