# iter-355 · cudakit — станционный CUDA-кит собран и валидирован живьём: настройка запуска станции под RTX 3080 Ti (12 ГБ) + 32 ГБ RAM передана владельцу в двойной-клик форме; девайс-класс-гейт (урок iter-354 §B) реализован инструментально; живой дефект найден валидацией (голый `-fa` в окне b11538+ умирает rc=1)

**Вызов владельца (2026-10-10, дословно):** «ты может быть сам
настроишь нужный запуск станции для меня? чтобы открывалось cuda и с
прочими нужными мне настройками, у меня rtx 3080ti и 32gb ram.» +
второй вопрос сессии (суть двух-LLM формы «типа kev» — для чего и как
работает) — отвечен в чате сессии (владелец-facing); репо-владелец
темы — iter-351 §A (рука F: свободная проза главной + грамматный
ультралайт-экстрактор), здесь не дублируется. Выгруженные в сессию
файлы (`canonsim_m3_station_pack_v3.7z`, chip-спека 2026-09-25,
«флаги llama.cpp.txt`) на ФС сессии НЕ ПРИЕХАЛИ (каталог upload пуст,
проверено трижды) — для кита они не нужны: ATTACH-форма не требует
исходников пака, а флаг-спека — внешние research-входы владельца
(D-024/D-200, никогда не вендорятся). Явный ввод сессии (D-198):
настройка запуска = текущая задача; она же — голова STATUS Next (1)
с предыдущей итерации («the M3 GPU re-run … one CUDA-build
llama-server.exe dropped into workbench/runtime/llama.cpp/ — OR a
manually started server + the probe's ATTACH form»). BASE_COMMIT:
`760bd3b` (iter-354; свежий клон).

**Класс риска:** R0/R1 (внутрирепо — только док-райдеры; нулевой код,
нулевые данные пака; INV-1..5 не тронуты, ЛОГ не тронут. Кит — внешний
инструмент вне репо, Rule 9 / D-046, форма iter-348/349/351/352/353;
md5 кита `06d85bea7913dda1c6609b0c4af0bb1c`, 24 682 байта — для сверки).

## A. Что сделано — THE CUDA STATION KIT v1 (9 файлов, вне репо)

Двойной-клик форма; кладётся куда угодно рядом с canonsim (лестница
репо кита — то же подмножество m2 v2: `--repo` > `CANONSIM_REPO` >
beside/above > OneDrive/Desktop; два маркёра AGENTS.md+pyproject.toml).

1. **station_cuda_setup.bat/.py** (одноразовый шаг 1): качает
   ОФИЦИАЛЬНЫЙ `llama-b11538-bin-win-cuda-12.4-x64.zip` (265 219 217
   байт, sha256 `631c1397231497dabcdd1eb21ae43ad235093c22c88cc64f09ac3be67285
   cd6e`, проверен живой загрузкой сессии) — ТОТ ЖЕ НОМЕР БИЛДА, что
   CPU-прогон станции: единственная сменная переменная повтора —
   ПОЛОСА, ровно форма закрытия iter-354 §I.3. Идемпотентен (sha256
   skip), офлайн-путь (локальный zip рядом со скриптом), распаковка в
   `llama.cpp/` кита (репо не трогает);
2. **CUDA-runtime резолюция** (датум: `ggml-cuda.dll` 572 МБ несжатый
   грузит `cudart64_12.dll` + `cublas64_12.dll`/`cublasLt64_12.dll`
   ДИНАМИЧЕСКИ — их НЕТ в архиве llama.cpp): (а) уже видны системой
   (System32/SysWOW64/PATH) → ничего не делает; (б) найдены в CUDA
   toolkit → копирует рядом с exe; (в) иначе — официальные
   NVIDIA-redist архивы (pinned от redistrib_12.4.1.json: cudart
   12.4.127 / libcublas 12.4.5.8, оба sha256-сверены). Установка
   заканчивается живым `--list-devices` — ГРОМКО, без CUDA-строки;
3. **station_cuda_start.bat/.py** (шаг 2, ПУТЬ А — рекомендуемый):
   поднимает llama-server на `127.0.0.1:8080` (цель ATTACH зонда v3)
   с полосой под 3080 Ti: `-ngl 99` (весь оффлоад; 9B Q4_K_M ≈ 5.5 ГБ
   + KV(4096) ≈ 1 ГБ ≈ 7 из 12 ГБ — экстрактор, если поднимется
   рядом, уместится своей лестницей) + `-fa on` (проектный пин,
   LLAMA_CPP_INFERENCE_CONTROL_LAW §4) + `-c 4096 -np 1 --jinja`
   (РОВНО форма автоспавна m2/m3 — латентностный леджер остаётся
   байт-сравнимым по форме; НИКАКИХ KV-квантов/сэмплеров — значения
   батареи ездят per-request). **ДЕВАЙС-КЛАСС ГЕЙТ** — урок iter-354
   §B инструментально: `--list-devices` пре-чек ДО спавна (нет CUDA →
   ГРОМКОЕ предупреждение + подтверждение владельца; не-TTY без
   `--yes` → честный отказ — слепой CPU-прогон больше не ездет) И grep
   `ggml_cuda_init`/`offloaded N/M` ПОСЛЕ health → вердикт полосы в
   `cuda_gate.json`. Лестница живучести OOM: `-ngl
   99(fa)→24(fa)→8(fa)→0(fa)→0`; каждая мёртвая попытка печатает
   хвост лога 25 строк (закон v3); heartbeat-ожидание 900 с (OneDrive
   закон m2); полный лог-ти сервера в `cuda_server_*.log`
   (print_timing-строки — источник леджера); Ctrl+C — чистый стоп;
   меню моделей с запоминанием прошлого выбора;
4. **station_cuda_swap.bat/.py** (ПУТЬ Б — минимальная форма iter-354
   §I.3): встраивает CUDA-билд кита в `workbench/runtime/llama.cpp/`
   (автоспавн зонда сам поднимет полосу; только gitignored-дерево),
   CPU-билд откладывается sibling-бэкапом `llama.cpp.cpu-bak-<ts>`
   ВНЕ зоны поиска движка, `--restore` возвращает;
5. **station_get_extractor.bat/.py** (опционально): качает
   Qwen3-0.6B-Q4_K_M (484 219 808 байт, md5 `541151b170814b2063fb8bc74073db7d`,
   lmstudio-community, живая проверка) в
   `workbench/runtime/models/` — РАБОЧИЙ ультралайт для руки F:
   оба станционных кандидата владельца нерабочие (Kev-4B — GGUF-битый
   на уровне тензоров; decider-4b — не извлекает), а валидированный
   класс iter-351/353 — именно 0.6B;
6. **README_CUDA.txt** (русский, руки владельца): оба пути пошагово,
   что отвечать в окнах зонда, ожидания (~10–20 мин против 2 ч 20),
   VRAM-бюджет, что присылать обратно (m3_*.zip + cuda_gate.json +
   cuda_server_*.log).

Доставка: архив в каталоге сессии + tmpfiles.org прямая ссылка
(`https://tmpfiles.org/dl/wxAdgs8ARLQy/canonsim_cuda_station_kit_v1.zip`)
+ md5 + размер (закон §12.2).

## B. Валидация (§13.1-класс, живая в сессии; разрешение окружения владельца 2026-10-10)

Сэндбокс: llama.cpp **b11540 ubuntu-x64** (та же генерация, что b11538)
+ Qwen3-0.6B-Q4_K_M (живая загрузка, md5 сверен):

- **ПОЛНЫЙ ПОТОК СТАРТЁРА насквозь**: лестница репо нашла `../canonsim`
  сам; пре-чек честно сказал «CUDA-устройство НЕ видно» (сэндбокс без
  GPU — правильное поведение ГРОМКО); `--yes` → спавн → health →
  `/v1/models` → вердикт «ПОЛОСА: CPU (!!!)» → `cuda_gate.json` со
  всеми полями; лог-ти пишет print_timing;
- **ЖИВОЙ ДЕФЕКТ, НАЙДЕННЫЙ ВАЛИДАЦИЕЙ** (закрыт в-итерации, закон
  iter-349 §C): голый `-fa` в окне b11538+ УМИРАЕТ rc=1
  (`error while handling argument "-fa": expected value for
  argument` — флаг теперь ЗНАЧЕМЫЙ, on|off|auto). До фикса: лестница
  пережила 4 мёртвых попытки и поднялась на 5-й (без -fa) — сама
  живучесть лестницы доказана живым отказом; после фикса (`-fa on`)
  попытка 1 поднимается сразу;
- **OAI-поверхность** (то, что будет звать зонд v3): `/health` 200;
  `/v1/models` отдаёт id; `POST /v1/chat/completions` с полем `model`
  (эхо id — закон v3) 200; **ГРАММАТИКА**: `grammar`-вызов вернул
  РОВНО JSON-литерал `{"ok": true}` — механизм батареи жив;
- **swap**: установка в runtime/llama.cpp → бэкап sibling → повторная
  установка с бэкапом → `--restore` 1:1; репо после чистки —
  `git status --porcelain -uall` пуст;
- **setup**: локальный zip (sha256 match → без скачивания) →
  распаковка 52 файла → llama-server.exe + ggml-cuda.dll на месте →
  честный не-Windows skip → честный «--list-devices не выполнился»
  (win-exe на Linux — ожидаемо, стартёр перевзюет полосу сам);
- **download()**: живая загрузка redist-cudart 2.5 МБ со сверкой
  sha256 — прогресс/ретраи/хэш работают;
- **get_extractor**: verified-skip путь (модель на месте, md5 ok).

## C. Датумы сессии (для леджера)

- Официальная CUDA-сборка b11538 СУЩЕСТВУЕТ и доступна (win-cuda-12.4
  x64; последняя видимая — b11540; выбор b11538 = сопоставимость с
  CPU-прогоном — единственная переменная повтора);
- `ggml-cuda.dll` НЕ статичен по рантайму: cudart/cublas нужно
  резолвить отдельно (архивы лламы их не несут; у m2-станции b11064
  winget-пакет, вероятно, нёс свои — потому «просто работало»);
- b11538+: `-fa` ЗНАЧЕМ (голый флаг — rc=1); `-ngl` дефолт `auto`;
  порт по умолчанию 9931 (не 8080!) — 8080 передаётся явно.

## D. Что НЕ сделано (честно)

- **Станционный GPU-прогон не сделан** — это и есть следующий шаг, и
  он за владельцем (двойной клик ×2 + зонд; ~10–20 мин); чтение
  закрывает GPU-полосу «тапок»;
- Пак v3 не патчен — v4-строки (девайс-класс в gate ЗОНДА,
  memory-pressure recycle, консоль зонда в zip) остаются вызовами
  владельца (iter-354 §I.4); кит закрывает тот же класс СНАРУЖИ пака
  (cuda_gate.json), не вторгаясь в батарею;
- Файлы сессии (пак 7z / chip-спека / флаги) не доехали на ФС —
  чтение флагов по живому `--help` билда (закон §19: бинарь —
  авторитет), не по выгрузке;
- Ничто из репо-очереди (replay-UI, W8, P1/P2/P3, lab-composite-1) не
  тронуто.

## E. Риски

- URL/хэши — снимок 2026-10-10: пере-выложенный релиз откажет по
  sha256 ГРОМКО (это фича, не риск — владелец увидит и перекачает);
  офлайн-путь и явные URL в сообщениях дают обход;
- Полоса меняет латентности, но не валидность: G-пин батареи
  воспроизводился и на CPU, и на GPU (m2: b11064 держал пин —
  четвёртая точка; если CUDA-полоса сдвинет пин — префлят зонда
  поймает, и это само по себе датум);
- Красная зона VRAM не прогнозируется точно (9B Q4 + lazy экстрактор):
  лестница 99→24→8→0 + degrade-закон пака v3 покрывают оба отказа;
  cuda_gate.json фиксирует использованную ступень.

## F. Проверки

- `PYTHONHASHSEED=0 python -m pytest -q` — 2660 passed, 1 skipped;
  `ruff check .` — clean; `python scripts/docguard.py` — clean;
  `python scripts/topology.py --check` — clean;
- Живая валидация кита — §B (полный поток стартёра, OAI+грамматика,
  swap/restore, setup, download, get_extractor);
- Самопроверка дельты: список путей == `git status --porcelain -uall`
  против базы `760bd3b` (блок Git ниже).

Замечание о док-лупе (AGENTS §2.5, превентивно): шестая подряд
riders-only итерация — функциональный прогресс здесь ВНЕ репо (кит —
инструмент, валидированный живым прогоном; форма m2/m3-паков
буквально), в репо едут чтение и леджер — та же конструкция, что
iter-348/349/351/352/353.

## G. Дальше (по порядку владельца)

1. **Станционный GPU-прогон M3 через кит** (сетап → старт → зонд;
   ~10–20 мин; прислать m3_*.zip + cuda_gate.json + cuda_server_*.log)
   — закрывает GPU-полосу «тапок», чтение следующей итерацией;
2. Решение M2 (block/downgrade/allow + C-tight/C-full — пакет
   iter-350 §G + m3-добавка §I.2) и решение M3-формы (H лидер / F с
   рабочим ультралайтом / verdict-aware G2) — оба за гейтом
   runtime-promotion;
3. Затем постоянные вызовы: replay-UI NOT-EXPOSED, W8, P1/P2/P3,
   lab-composite-1 + skip_probes-адрес (iter-347).

## H. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-355-cudakit-report.md
git status --short
git commit -m "iter-355-cudakit: THE CUDA STATION KIT v1 (9 files outside the repo per Rule 9) - the owner's RTX 3080 Ti / 32 GB station launch configured for the CUDA band (the pinned OFFICIAL b11538 win-cuda-12.4-x64 build - the SAME build number as the CPU run, the device band the only changed variable; sha256-pinned download, the CUDA-runtime DLL resolution: system > toolkit > the official NVIDIA redist archives) + the DEVICE-CLASS GATE implemented live (the iter-354 §B lesson: the --list-devices precheck before spawn with the loud no-CUDA refusal, the ggml_cuda_init/offload grep after health, cuda_gate.json) + the two owner paths (A the ATTACH form: a tuned llama-server on 8080 with -ngl 99 -fa on -c 4096 -np 1 --jinja - the pack autospawn form byte-comparable, the OOM ladder 99->24->8->0, the log tail in every failure, the 900s heartbeat; B the swap form: the CUDA build into workbench/runtime/llama.cpp with the sibling backup and --restore) + the recommended WORKING ultra-light extractor fetch (Qwen3-0.6B Q4_K_M, md5-pinned) for the F arm - both the owner's candidates broken (Kev GGUF / decider refusing); VALIDATED LIVE §13.1-class (b11540 ubuntu + Qwen3-0.6B: the full starter flow end-to-end incl. the honest CPU-band verdict, the OAI surface with the grammar field returning the exact JSON literal, swap+restore 1:1, setup sha256+unpack, the download function live) - the validation itself found and closed a live defect: the bare -fa flag DIES rc=1 in the b11538+ window (the flag is now valued on|off|auto - the ladder survived it pre-fix, the first attempt rises post-fix); zero repo code"
git push
```
