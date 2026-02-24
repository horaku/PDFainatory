# PDFainatory Task Backlog

This backlog translates the current gaps into concrete implementation tasks for the next iteration.

## P0 — Correctness & Safety
- [x] Add encrypted/corrupt PDF validation node before translation execution.
  - Acceptance: invalid/encrypted PDFs return a structured 4xx error and never invoke `pdf2zh-next`.
- [x] Add scanned-PDF detection and OCR routing policy.
  - Acceptance: scanned-heavy files are flagged and routed to OCR pre-processing path (or blocked with explicit guidance).
- [x] Fix fallback behavior to actually switch provider flags (not only `--ignore-cache`).
  - Acceptance: fallback chain is explicit (e.g., `--openai` → `--google` → `--ollama`) and recorded in run metadata.
- [x] Add shell-safe command argument handling to avoid injection from payload fields.
  - Acceptance: workflow uses strict escaping/allowlists for all user-provided values.

## P1 — Reliability & Observability
- [x] Add structured run metadata per file/page (runId, file hash, command args, start/end, status, error class).
  - Acceptance: every file emits a machine-readable audit record.
- [x] Implement error classification and retry policy by class.
  - Acceptance: transient errors retry with backoff; non-retryable validation errors fail fast.
- [x] Persist partial-progress state for resumable reruns by page range.
  - Acceptance: a failed batch can be resumed without reprocessing successful files/pages.
- [ ] Add output integrity checks for produced artifacts.
  - Acceptance: incomplete/corrupt outputs are detected and marked failed.

## P2 — Product Completeness
- [ ] Add artifact publication node (S3/MinIO/local download URL).
  - Acceptance: API response includes a downloadable link or storage key for each output file.
- [ ] Enforce bilingual output naming/versioning convention.
  - Acceptance: predictable output path schema includes runId + source file stem + mode.
- [ ] Add fidelity verification checklist execution (formula/table/list/header/footer checks).
  - Acceptance: workflow returns a quality summary with pass/warn/fail flags.
- [ ] Add operator notifications for success/partial/failure outcomes.
  - Acceptance: webhook caller and optional channel (email/chat) receive status with reason codes.

## Test Tasks
- [ ] Add workflow-level dry-run validation script for payload schemas and command generation.
- [ ] Add integration test matrix for scenarios in `plan.md` Phase 7.
- [ ] Add representative fixture set: normal scientific PDF, scanned PDF, large PDF, formula/table-heavy PDF.

## Definition of Ready for Next PR
- [ ] At least one P0 task fully implemented with tests.
- [ ] Updated `docs/runbook.md` and `docs/requirements-traceability.md` reflecting the new behavior.
- [ ] Example request/response payloads updated for new error and metadata fields.
