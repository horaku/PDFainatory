# tasks.md — Execution Backlog for PDFainatory

This backlog operationalizes `requirements.md` and `plan.md` into executable phases with dependency and release evidence.

## Conventions
- **Priority**: P0 (critical), P1 (high), P2 (medium)
- **Status**: TODO / IN_PROGRESS / BLOCKED / DONE
- **Type**: Build / Test / Ops / Docs
- **Traceability**: each task maps to requirement groups R1..R7
- **Evidence rule**: a task can be `DONE` only if there is repository evidence (workflow node, validator assertion, or documented runbook contract)

---

## T00 — Governance & Traceability

- [x] **T00.1** Define execution docs baseline (`runbook`, `traceability`, `test strategy`, `integration matrix`).  
  - Priority: P0 | Type: Docs | Status: DONE  
  - Maps to: R7  
  - Evidence: `docs/runbook.md`, `docs/requirements-traceability.md`, `docs/test-strategy.md`, `docs/integration-test-matrix.md`

- [ ] **T00.2** Adopt branch-level run correlation standard (`runId/jobId/fileId/pageRange/traceId`) and enforce in all logs/notifications.  
  - Priority: P1 | Type: Ops | Status: TODO  
  - Depends on: T00.1  
  - Maps to: R5, R7

---

## T01 — Intake & Validation

- [x] **T01.1** Input normalization for single/batch payloads and schema guards.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R1, R7

- [x] **T01.2** PDF extension/readability validation and unsafe-path rejection.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R1

- [x] **T01.3** Corrupt/password-protected detection with explicit 4xx response.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R1, R5

- [ ] **T01.4** Scanned-page policy routing.  
  - Priority: P0 | Type: Build | Status: IN_PROGRESS  
  - Maps to: R1, R6  
  - Note: request-level `scannedHint` route exists; automatic scanned heuristic detector is still pending.

---

## T02 — Command Orchestration

- [x] **T02.1** Deterministic command builder (`--lang-in ja --lang-out ru --bilingual --output`).  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R3, R4, R7

- [ ] **T02.2** Service selection strategy and fallback chain.  
  - Priority: P0 | Type: Build | Status: IN_PROGRESS  
  - Maps to: R3, R5  
  - Note: implemented for `openai/google/ollama`; broader provider matrix (e.g., DeepL/HF endpoint strategy) pending.

- [x] **T02.3** Optional page-range rerun (`--pages`) and worker controls.  
  - Priority: P1 | Type: Build | Status: DONE  
  - Maps to: R1, R5, R7

- [x] **T02.4** Prompt/glossary/font controls and command/audit metadata persistence.  
  - Priority: P1 | Type: Build/Ops | Status: DONE  
  - Maps to: R3, R4, R5, R7

---

## T03 — Resilience & Error Handling

- [x] **T03.1** Error classification (`transient` / `non_retryable_input` / `unknown`).  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R5

- [x] **T03.2** Retry policy and fallback chain preserving progress.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R3, R5

- [ ] **T03.3** Atomic output guarantees and interruption-safe writes.  
  - Priority: P0 | Type: Build | Status: IN_PROGRESS  
  - Maps to: R5  
  - Note: output integrity checks exist; strict atomic-write guarantees are not yet proven by integration evidence.

- [x] **T03.4** Continue unaffected files/pages on partial failure and emit typed error payloads.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R5, R7

---

## T04 — Output, Fidelity, and Publication

- [x] **T04.1** Output naming/versioning and integrity checks.  
  - Priority: P0 | Type: Build | Status: DONE  
  - Maps to: R4, R7

- [ ] **T04.2** Artifact publication.  
  - Priority: P0 | Type: Build | Status: IN_PROGRESS  
  - Maps to: R4, R7  
  - Note: metadata publication exists; real S3/MinIO upload + signed URLs pending.

- [ ] **T04.3** Fidelity checklist and visual regression quality gates.  
  - Priority: P0 | Type: Build/Test | Status: IN_PROGRESS  
  - Maps to: R2, R4  
  - Note: checklist exists (heuristic); robust visual diff gates/tolerances still pending.

---

## T05 — OCR & Embedded Image Text

- [ ] **T05.1** Define OCR decision tree for scanned pages and image-text regions.  
  - Priority: P0 | Type: Docs | Status: TODO  
  - Maps to: R6

- [ ] **T05.2** Implement OCR preprocessing integration path (tool-agnostic).  
  - Priority: P1 | Type: Build | Status: TODO  
  - Maps to: R6

- [ ] **T05.3** Route OCR text through translation controls (prompt/glossary/fallback).  
  - Priority: P1 | Type: Build | Status: TODO  
  - Maps to: R3, R6

- [ ] **T05.4** Reinsertion policy (replace vs annotation) with position fidelity and low-confidence warnings.  
  - Priority: P1 | Type: Build | Status: TODO  
  - Maps to: R4, R6, R7

---

## T06 — Observability & Notifications

- [x] **T06.1** Structured audit metadata and run-state persistence.  
  - Priority: P1 | Type: Ops | Status: DONE  
  - Maps to: R5, R7

- [x] **T06.2** Optional operator webhook notifications (success/partial/failure) with non-blocking delivery.  
  - Priority: P1 | Type: Build/Ops | Status: DONE  
  - Maps to: R5, R7

- [ ] **T06.3** Persistent audit sink + trace IDs + dashboard metrics export.  
  - Priority: P1 | Type: Ops | Status: TODO  
  - Maps to: R5, R7

---

## T07 — Verification & Readiness

- [x] **T07.1** Workflow structural validator and dry-run contract validator.  
  - Priority: P0 | Type: Test | Status: DONE  
  - Maps to: R1..R7

- [x] **T07.2** Integration scenario matrix and fixture catalog scaffold.  
  - Priority: P0 | Type: Test/Docs | Status: DONE  
  - Maps to: R1..R7

- [ ] **T07.3** Executable E2E scenario runs with captured reports (single/batch/scanned/fallback/partial).  
  - Priority: P0 | Type: Test | Status: TODO  
  - Maps to: R1, R3, R5, R7

- [ ] **T07.4** Visual fidelity regression runbook + thresholds + baseline artifacts.  
  - Priority: P1 | Type: Test | Status: TODO  
  - Maps to: R2, R4

- [ ] **T07.5** Release readiness checklist publication with known limitations and mitigations.  
  - Priority: P1 | Type: Docs/Ops | Status: TODO  
  - Maps to: R5, R7

---

## Milestone Mapping
- **M1 (Implemented core)**: T01 + T02 + T03.1/3.2/3.4 + T04.1
- **M2 (Stabilization in progress)**: T03.3 + T04.2 + T04.3 + T06
- **M3 (Completeness pending)**: T05 + T06.3
- **M4 (Readiness pending)**: T07.3 + T07.4 + T07.5

## Immediate Next Actions
1. Implement executable E2E runner/reporting for matrix scenarios (T07.3).
2. Implement real artifact upload (S3/MinIO) with signed URLs (T04.2).
3. Add trace IDs and persistent audit sink (T06.3).
4. Define visual fidelity thresholds and baseline artifacts (T07.4).
