# PDFainatory n8n Runbook (v0)

## 1) Purpose
Operate a resilient n8n endpoint for Japanese→Russian scientific PDF translation using PDFMathTranslate-next as the mandatory backend.

## 2) Input Contract
POST payload (example):

```json
{
  "runId": "run-20260221-001",
  "files": ["/data/in/paper1.pdf", "/data/in/paper2.pdf"],
  "outputDir": "/data/out",
  "langIn": "ja",
  "langOut": "ru",
  "service": "openai",
  "poolMaxWorkers": 2,
  "pages": "1-5",
  "customPromptPath": "/data/config/science_prompt.txt",
  "glossaryPath": "/data/config/terms.csv",
  "primaryFontFamily": "Noto Serif",
  "scannedHint": false,
  "allowOcrWorkaround": false,
  "runStateDir": "/data/state",
  "artifactBaseUrl": "https://files.example.com",
  "artifactStoragePrefix": "/pdfainatory/out",
  "fidelityChecklistMode": "basic",
  "fidelityWarnMinBytes": 20480,
  "notificationWebhookUrl": "https://ops.example.com/hooks/pdfainatory",
  "notifyOnSuccess": false,
  "notifyOnPartial": true,
  "notifyOnFailure": true
}
```

## 3) Execution Steps
1. Trigger via webhook endpoint `pdfainatory/translate`.
2. Validate and normalize request into per-file jobs.
3. Validate `.pdf` extension before command construction.
4. Evaluate scanned-PDF policy: if `scannedHint=true` and `allowOcrWorkaround=false`, return warning (`409`) and stop translation.
5. Run preflight integrity check (`qpdf --check`) and fail fast on corrupt/encrypted PDFs.
6. Build deterministic `pdf2zh-next` command with provider flag and bilingual mode (plus OCR workaround flag when allowed).
7. Execute primary command.
8. If primary fails, classify the error (`translation.transient` vs `translation.non_retryable_input` vs `translation.unknown`).
9. Retry once only for transient/retryable errors; fail fast for non-retryable input errors.
10. If retry still fails, advance through provider fallback chain (`openai -> google -> ollama`) with `--ignore-cache`.
11. Build output naming metadata with convention `runId-sourceStem-bilingual-v1`.
12. Validate output integrity by checking that a non-empty output PDF artifact exists in `outputDir` for the expected naming base.
13. Build structured audit metadata (`runId`, `inputFileHash`, command args, start/end timestamps, status, error class) for every terminal path.
14. Persist per-file run-state JSON (`runStateDir`, default `/data/state`) for resumable reruns.
15. Build artifact publication metadata (`artifact.storageKey`, optional `artifact.downloadUrl`) for successful outputs.
16. Build fidelity checklist summary (`formula/table/multiColumn/headersFooters`) with pass/warn verdict.
17. Build optional operator notifications for success/partial/preflight-failure/translation-failure and POST JSON payload to `notificationWebhookUrl` via n8n HTTP Request nodes when enabled.
18. Return response JSON with operation status (`completed` or `partial`) and `reasonCode`, plus `audit` object, retry fields (`retryable`, `retryAttempt`), `runStateFile`, and (on success) `outputFile` + `outputNaming` + `artifact` + `qualitySummary`.

## 4) Operational Expectations
- Current pipeline is scoped to `ja -> ru` only.
- Input paths are sanitized with an allowlist to reduce command-injection risk.
- Scanned inputs can be blocked for mandatory pre-OCR unless OCR workaround is explicitly enabled.
- Bilingual output is explicitly requested via `--bilingual`.
- Each file executes independently, so one failed item should not block other items.
- Notifications are optional and non-blocking; delivery failures from notification HTTP requests do not change API response status.

## 5) Next Hardening Steps
- Add explicit scanned PDF detection and OCR pre-route.
- Wire audit objects to a persistent log sink (ELK/OpenSearch/Loki) with trace IDs.
- Add persistent run-state store for resume/re-run by `runId`.
- Add artifact publication node (S3/MinIO) and signed URL response.
- Add email/chat adapters and dedup/rate-limit policy for notifications.

## 6) Validation Tooling
- Run `python tests/dry_run_validate.py` for dry-run contract checks (payload normalization fields, command generation invariants, and success response schema fields).
- Run `python tests/validate_workflow.py` for graph/node wiring invariants.
