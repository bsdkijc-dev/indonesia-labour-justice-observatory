# Technical & Data Quality Report — ILJO v1.0 Pilot

**Date:** 2026-11-23  
**Mode:** `synthetic` (Offline sandbox fallback; live collection from [Direktori Putusan Mahkamah Agung RI](https://putusan3.mahkamahagung.go.id) blocked pending authorized workstation `robots.txt` check).

## 1. Pipeline Execution Summary
- **Input Raw Synthetic Records:** 154 (150 baseline + 4 adversarial edge cases)
- **Stage 5 (Deduplication):** 1 duplicate removed (`ILJO-2024-0151`), 153 remaining
- **Stage 6 (Validation & Quality Gate):** 2 records flagged (`ILJO-2024-0152` inverted date order; `ILJO-2024-0153` `ai_assisted` confidence `0.62 < 0.85`)
- **Stage 7 (Privacy Review):** 1 record flagged (`ILJO-2024-0154` unredacted NIK, email, honorific)
- **Analysis-Ready Output:** 150 records (`mean_quality_score = 0.9768`)

## 2. Environment & Dependency Notes
- Python `3.11.2`, `pandas 2.2.3`, `pyarrow 26.0.0`, `jsonschema 4.23.0`, `pyyaml 6.0`.
- `duckdb` is not installed in the sandbox VM; analytical persistence uses `sqlite3` (`data/processed/iljo_analytics.db`) alongside Parquet (`data/processed/phi_pilot_validated.parquet`) and UTF-8 CSV (`data/public/phi_synthetic_release_candidate.csv`).
- All 5 automated tests in `tests/test_pipeline.py` pass (`OK` in 0.541s).
