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
  "primaryFontFamily": "Noto Serif"
}
```

## 3) Execution Steps
1. Trigger via webhook endpoint `pdfainatory/translate`.
2. Validate and normalize request into per-file jobs.
3. Validate `.pdf` extension before command construction.
4. Build deterministic `pdf2zh-next` command.
5. Execute command with retry (2 tries, 3s wait).
6. If stderr contains `rate limit`, run fallback command (`--ignore-cache`).
7. Return success JSON with `runId`, `inputFile`, and `outputDir`.

## 4) Operational Expectations
- Current pipeline is scoped to `ja -> ru` only.
- Bilingual output is expected to be produced by PDFMathTranslate-next defaults/config.
- Each file executes independently, so one failed item should not block other items.

## 5) Next Hardening Steps
- Add encrypted/corrupt PDF detection before execution.
- Add explicit scanned PDF detection and OCR pre-route.
- Add structured log sink (ELK/OpenSearch/Loki) with trace IDs.
- Add persistent run-state store for resume/re-run by `runId`.
- Add artifact publication node (S3/MinIO) and signed URL response.
