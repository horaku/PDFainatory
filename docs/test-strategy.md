# Test Strategy — PDFainatory

## 1) Coverage Matrix: R1..R7 → test suites

> Цель: каждый acceptance criterion из `requirements.md` должен иметь минимум один автотест (или полуавтоматический visual test для fidelity).

### R1 — Upload and Input Data

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Single PDF accepted and started | ✅ schema smoke (`file`) | ✅ E2E single file run |  |  | Проверка перехода в `execute` без ошибок |
| Batch directory/files processed in parallel |  | ✅ E2E batch run (`files[]`) | ✅ partial continuation under one-file failure |  | Проверка отсутствия потерь и статусов per-file |
| Scanned pages require pre-OCR warning | ✅ scanned detector unit | ✅ E2E route to OCR gate | ✅ degraded OCR path warning |  | Не запускать перевод без policy |
| Password-protected/corrupted PDF rejected | ✅ precheck smoke (`qpdf/pdfinfo`) | ✅ E2E returns 4xx structured error |  |  | Без вызова `pdf2zh-next` |
| Invalid PDF rejected with clear message | ✅ MIME/ext/path checks | ✅ E2E validation error payload |  |  | Читаемый reason code |

### R2 — Parsing and Content Extraction

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Formulas preserved (no translation) |  | ✅ formula fixture E2E |  | ✅ formula overlay diff | Проверка неизменности LaTeX блоков |
| Complex layout metadata preserved |  | ✅ multi-column fixture E2E |  | ✅ bbox/layout regression | TOC, annotations, cross-page |
| Large/rare cases without memory errors |  | ✅ large fixture E2E | ✅ memory pressure retries/chunking |  | Проверка page chunk policy |
| Lists recognized and markers preserved |  | ✅ list fixture E2E |  | ✅ marker diff check | bullet/number consistency |
| Headers/footers/page numbers extracted separately |  | ✅ E2E header/footer fixture |  | ✅ position regression | per-page zones |
| Relative text placement consistency |  | ✅ placement assertions |  | ✅ geometry tolerance checks | tolerance threshold |

### R3 — Text Translation

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Middleware/prompt/glossary pipeline | ✅ command build smoke | ✅ E2E with prompt+glossary |  |  | Проверка CLI flags |
| Font mapping for Kanji/Cyrillic issues | ✅ font arg smoke | ✅ E2E with `--primary-font-family` |  | ✅ rendered glyph sanity | Нет tofu/□ символов |
| Rate-limit fallback provider switch |  | ✅ fallback E2E | ✅ retry chain (`openai→google→ollama`) |  | Обязательно с сохранением progress |
| Non-Japanese text preserved |  | ✅ mixed-language fixture E2E |  | ✅ text diff whitelist | numbers/latin/codes unchanged |
| Low-confidence translation flagged/logged |  | ✅ confidence log E2E | ✅ low-quality fragment handling |  | reason codes in logs |

### R4 — Reconstruction and Output

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Dynamic scaling for longer RU text |  | ✅ long-text fixture E2E |  | ✅ overflow/cropping regression | no crop/shift |
| Bilingual output generated | ✅ output naming smoke | ✅ E2E bilingual artifact |  | ✅ page pair sanity | side-by-side required |
| Graphics/styles/positions preserved |  | ✅ E2E style fixture |  | ✅ pixel/layout diff | tolerance-based |
| Lists/headers/footers/page numbers/tables restored |  | ✅ E2E structure fixture |  | ✅ structure regression | exactness policy |
| Table layout/cell alignment preserved |  | ✅ table-heavy fixture E2E |  | ✅ table-grid regression | row/column alignment |
| Image text reinsertion/annotation |  | ✅ image-text fixture E2E | ✅ fallback annotation mode | ✅ position/color tolerance | if safe replace else annotation |
| Page count coherence rule | ✅ metadata smoke | ✅ E2E page-count assertion | ✅ overflow-to-next-page behavior |  | logical coherence if count differs |
| Download option/link provided | ✅ response schema smoke | ✅ artifact publication E2E | ✅ transient storage retry |  | API/web link correctness |

### R5 — Error Handling and Robustness

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Memory issue → chunk + continue |  | ✅ large-doc E2E | ✅ chunking policy test |  | includes `--ignore-cache` fallback knob |
| Network/API error → retries + HF endpoint |  | ✅ network-fault E2E | ✅ retry/backoff/mirror switch |  | structured exception logs |
| Interruption → no corrupted partial PDF |  | ✅ kill-process E2E | ✅ atomic write recovery |  | output integrity checks mandatory |
| Partial page failure → others continue + notify |  | ✅ partial-fail E2E | ✅ per-page continuation |  | no data mixing |

### R6 — Images and Embedded Elements

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| OCR text area detection in images/scans | ✅ OCR route smoke | ✅ image/scanned fixtures E2E | ✅ low-res OCR robustness | ✅ OCR box overlay diff | tool: Tesseract/EasyOCR/PaddleOCR |
| OCR text goes through common translation pipeline |  | ✅ pipeline linkage E2E |  |  | same glossary/prompt controls |
| Reinsertion with visual integrity |  | ✅ reinsertion E2E | ✅ annotation fallback | ✅ visual integrity checks | preserve style/position |
| Image without text unchanged | ✅ no-text detector smoke | ✅ unchanged-image E2E |  | ✅ binary/pixel equality | strict no-op expectation |
| Low OCR quality warning |  | ✅ low-confidence fixture E2E | ✅ warning propagation |  | user-visible warning |

### R7 — n8n Integration and UX

| AC | Smoke | Integration | Resilience | Visual | Notes |
|---|---|---|---|---|---|
| Workflow launch via exec node with CLI flags | ✅ workflow JSON lint | ✅ n8n E2E command invocation |  |  | check `ja->ru` flags |
| GUI/Zotero input support path |  | ✅ adapter contract tests | ✅ malformed source payload handling |  | persistent output paths |
| Targeted page translation with `--pages` | ✅ command option smoke | ✅ partial rerun E2E | ✅ resume semantics under failures |  | page-scope correctness |

---

## 2) Test Levels

### 2.1 Smoke (каждый PR)
- Проверка схем payload и обязательных полей.
- Линт/валидность workflow JSON.
- Проверка сборки CLI-команды (language flags, output, pages, prompt/glossary/font).
- Быстрые проверки валидации входа (invalid/corrupt/password-protected).

### 2.2 Integration (workflow end-to-end)
- Полный прогон n8n webhook → validation → command execution → artifact response.
- Сценарии: single, batch, scanned path, table-heavy, formula-heavy, partial pages.
- Проверка артефактов: наличие, структура, ожидаемый metadata response.

### 2.3 Resilience (retry/fallback/partial failure)
- Инъекция сбоев: rate limit, network timeout, provider unavailability, process interruption.
- Проверка fallback-цепочки провайдеров и сохранения прогресса.
- Проверка атомарной записи и отсутствия битых partial outputs.
- Проверка продолжения обработки оставшихся файлов/страниц.

### 2.4 Visual fidelity regression
- Эталонные PDF-наборы для таблиц/формул/многоколонки/headers-footers/annotations.
- Сравнение по геометрии и/или рендер-диффу с порогами.
- Отдельные проверки: таблицы (grid alignment), формулы (unchanged math), overflow/cropping.

---

## 3) Test Data Catalog

| Dataset ID | Type | Purpose |
|---|---|---|
| D01-small-single | small/single PDF | Базовый happy-path single file |
| D02-batch | batch (3–10 PDFs) | Параллельная обработка и per-file статусы |
| D03-scanned | scanned PDF | OCR gate/warning и OCR routing |
| D04-table-heavy | table-heavy PDF | Проверка layout/cell alignment |
| D05-formula-heavy | formula-heavy PDF | Проверка сохранности формул/LaTeX |
| D06-corrupt | corrupted PDF | Отказ до запуска движка |
| D07-password | password-protected PDF | Structured 4xx и корректное сообщение |

Минимальные метаданные для каждого датасета:
- source hash,
- expected outcome (pass/warn/fail),
- required checks (schema/layout/visual),
- permitted tolerances (если visual regression).

---

## 4) Gates по этапам `tasks.md`

Ниже этапы T01..T07 используются как исполнимые вехи из backlog:
- T01: Input validation (invalid/corrupt/password/scanned pre-route)
- T02: Command orchestration and safe argument handling
- T03: Retry/fallback provider chain
- T04: Progress persistence + output integrity
- T05: Artifact publication + response contract
- T06: Fidelity checks + visual regression baseline
- T07: Notifications + operational readiness

### Gate T02 → T03
Должно пройти:
- 100% smoke для R1 validation и R3 command-build.
- Integration: D01, D02, D06, D07.
- Security checks: command injection negative tests (payload fuzz) без bypass.

### Gate T04 → T05
Должно пройти:
- Resilience: rate-limit/network interruption сценарии.
- Partial-failure continuation: batch продолжается при сбое 1 файла/страницы.
- Output integrity: нет поврежденных PDF после принудительного прерывания.

### Gate T05 → T06
Должно пройти:
- Artifact publish integration с валидными download ссылками.
- Response schema contract tests (успех/частичный успех/ошибка).
- Backward compatibility для клиентов webhook API.

### Gate T06 → T07
Должно пройти:
- Visual fidelity suite для D04/D05/multi-column fixtures.
- Acceptance criteria по R2/R4 покрыты минимум одним integration+visual тестом.
- Стабильные пороги регрессии (зафиксированы в репозитории).

---

## 5) Release Gate (перед статусом DONE для M5)

Обязательные pass criteria:
1. **Coverage completeness:** для каждого AC из R1..R7 есть как минимум 1 тест-кейс в каталоге.
2. **PR gate health:** последние N PR (рекомендуемо 5) проходят smoke без flaky-блокеров.
3. **Integration health:** все обязательные E2E сценарии D01..D07 зелёные.
4. **Resilience health:** fallback/retry/partial-failure тесты зелёные, без corruption outputs.
5. **Visual fidelity health:** ключевые наборы (таблицы, формулы, многоколонка) в пределах agreed tolerance.
6. **Observability:** в логах есть runId, fileId/hash, provider path, error class, artifact location.
7. **Operational readiness:** runbook обновлен, известные ограничения задокументированы, rollback procedure проверена.

Если любой критерий не выполнен — релиз на M5 блокируется.
