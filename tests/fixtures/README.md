# Test Fixtures Catalog

This directory defines representative fixture slots for integration and resilience testing.

## Layout
- `small-single/` — small, single scientific PDF for smoke/happy-path tests.
- `batch/` — multi-file batch set with mixed complexity.
- `scanned/` — scanned/image-heavy PDFs for OCR/scanned policy tests.
- `table-heavy/` — PDFs with dense tables for layout/fidelity checks.
- `formula-heavy/` — PDFs with dense formulas/equations.
- `corrupted-password/` — intentionally corrupt and password-protected PDFs for preflight failure tests.

## Naming Convention
Use deterministic names to simplify automation:
- `fx-<category>-<id>.pdf`
- Optional metadata sidecar: `fx-<category>-<id>.json`

Example:
- `fx-small-001.pdf`
- `fx-small-001.json`

## Metadata Sidecar Schema (recommended)
```json
{
  "id": "fx-small-001",
  "category": "small-single",
  "expected": {
    "path": "primary_success",
    "status": "completed",
    "reasonCode": "success.completed"
  },
  "notes": "Baseline single-file smoke fixture"
}
```

## Security / Storage Note
Do not commit proprietary or sensitive PDFs. Use sanitized/public or synthetic documents only.
