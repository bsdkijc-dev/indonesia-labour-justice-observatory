# Data Governance Standard — ILJO v1.0

## 1. Data Lifecycle & Storage Zones
- `data/raw/` — Git-ignored. Stores authorized raw HTML/PDF documents with SHA-256 checksums and retrieval timestamps. Never committed or published.
- `data/staging/` — Git-ignored. Intermediate parsed text and raw extraction JSONs.
- `data/processed/` — Git-ignored (binary Parquet/SQLite/DuckDB). Normalized, deduplicated, and validated tables with quality scores.
- `data/public/` — Approved, de-identified, privacy-reviewed aggregate/record releases (CSV/Parquet) ready for human-approved publication.
- `data/synthetic/` — Non-sensitive synthetic test records used for pipeline verification, CI testing, and offline development.

## 2. Zero-Imputation & Epistemic Hygiene
- Missing information MUST remain `NULL` / empty or explicitly coded as `Unknown` or `Not observable`.
- Never coerce missing values to `"No"`, `False`, or `0`.
- Distinguish four epistemic states in every analytical output:
  1. **Explicitly recorded facts** (directly observed in verified judgment text).
  2. **Derived indicators** (deterministic calculations such as `decision_date - registration_date`).
  3. **Unknown information** (present in the underlying dispute but omitted or illegible in the document).
  4. **Not observable** (post-judgment events such as actual payment or execution, which cannot be observed from a judgment text alone).

## 3. Provenance & Correction Log
- Every record requires `record_id`, `source_url`, `source_retrieved_at`, `document_sha256`, `extraction_method`, `extraction_confidence`, `validation_status`, and `publication_status`.
- Manual or automated corrections must be appended to an immutable correction log rather than silently overwriting raw history.
