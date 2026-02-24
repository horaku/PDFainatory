# Requirements Traceability Matrix

This matrix maps the source requirements to concrete workflow behaviors and artifacts.

| Requirement Group | Key Requirements | Workflow Coverage | Gap/Follow-up |
|---|---|---|---|
| Group 1 — Upload/Input | Single PDF, batch, scanned warning, invalid/corrupt handling | `Webhook Trigger` accepts payload with `file` or `files`; validation nodes enforce schema and PDF extension; preflight node runs `qpdf --check` to reject corrupt/encrypted inputs. | Current routing uses request-level `scannedHint`; add automatic scanned heuristic detector as follow-up. |
| Group 2 — Parsing/Extraction | Preserve formulas/tables/layout; metadata fidelity | Delegated to PDFMathTranslate-next execution node, preserving layout through engine constraints. | Add post-run quality probe to detect parser warnings and tag output. |
| Group 3 — Translation | ja→ru translation, glossary/prompt/font controls, fallback provider | Command builder enforces `--lang-in ja --lang-out ru`; supports prompt/glossary/font and provider flags; fallback branch advances provider chain (`openai -> google -> ollama`) with `--ignore-cache`. | Add low-confidence fragment tagging and review queue contract. |
| Group 4 — Reconstruction/Output | Bilingual output, preserved styles/positions, downloadable artifact | Output path is deterministic and returned to caller; reconstruction performed by PDFMathTranslate-next. | Add node to publish signed download URL or object storage key. |
| Group 5 — Error handling | Retry, network handling, interruption resilience, per-file continuation | Workflow classifies translation failures into transient vs non-retryable input classes, retries transient errors once, and returns typed error responses (preflight 422, translation 502); pipeline is itemized per file for partial continuation. | Add richer class-specific backoff policy and external state index/query API. |
| Group 6 — n8n integration | Automated operation and observability | n8n JSON workflow provided; request/response pattern supports API integration; terminal responses now include per-file `audit` metadata (hash, command args, timing, status, error class). | Add trace IDs, persistent audit sink, and dashboard metrics export. |

## Artifact Index
- Workflow definition: `workflow/n8n-workflow.json`
- This traceability matrix: `docs/requirements-traceability.md`
