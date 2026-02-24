# Integration Test Matrix (Phase 7)

This matrix defines end-to-end workflow scenarios mapped to expected runtime behavior and response contracts.

| ID | Scenario | Input Highlights | Expected Path | Expected Result |
|---|---|---|---|---|
| IT-01 | Happy path single PDF | `file`, `service=openai` | preflight -> primary success -> integrity pass | `status=completed`, `reasonCode=success.completed`, `outputFile` present |
| IT-02 | Batch mixed outcomes | `files=[good,bad]` | per-item execution branches independently | good item `completed/partial`; bad item error without blocking sibling |
| IT-03 | Corrupt/encrypted PDF | corrupt file | preflight fail branch | HTTP 422 with `PDF_PREFLIGHT_FAILED`, `audit.errorClass` preflight class |
| IT-04 | Scanned blocked policy | `scannedHint=true`, `allowOcrWorkaround=false` | scanned policy block | HTTP 409 warning response, translation not executed |
| IT-05 | Retryable primary failure recovery | transient primary failure | classify -> retry -> success | success response with `status=partial` and recovery reason code |
| IT-06 | Provider fallback recovery | primary+retry fail, fallback succeeds | fallback chain (`openai->google->ollama`) | success response with `status=partial`, provider switched |
| IT-07 | Provider chain exhausted | all providers fail | translation error branch | HTTP 502 with `TRANSLATION_FAILED`, `providerTried`, retry metadata |
| IT-08 | Output integrity failure | empty/missing produced output | integrity fail -> translation error audit | HTTP 502 with integrity-related error classification |
| IT-09 | Notification enabled success | `notificationWebhookUrl`, `notifyOnSuccess=true` | success notify path via HTTP Request | response unchanged; notification POST attempted |
| IT-10 | Notification delivery failure | unreachable notification URL | notify node `continueOnFail=true` | response still returned (no status mutation) |
| IT-11 | Partial-notify policy | recovered success + `notifyOnPartial=true` | partial success notify path | notification payload has `status=partial`, `reasonCode=success.partial_recovered` |
| IT-12 | OCR workaround allowed | `scannedHint=true`, `allowOcrWorkaround=true` | translation command includes OCR flag | translation proceeds, command contains `--auto-enable-ocr-workaround` |

## Execution Notes
- Validate structural invariants with `python tests/validate_workflow.py`.
- Validate dry-run contract with `python tests/dry_run_validate.py`.
- Integration runs should capture request payload, terminal response body, and node-level execution traces for each scenario.

## Fixture Source
Use the fixture scaffold and catalog in `tests/fixtures/` (`README.md`, `catalog.json`) to map each integration scenario to concrete PDFs.
