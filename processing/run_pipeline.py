"""End-to-End Restartable & Idempotent ILJO Pipeline Runner (Stages 1-9)."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd

from crawler.provenance import record_provenance
from crawler.source_discovery import discover_sources
from processing.deduplication import deduplicate_records
from processing.metadata_extraction import normalize_records
from processing.privacy_review import run_privacy_review
from processing.synthetic_generator import generate_synthetic_pilot
from processing.validation import validate_dataframe


BASE_DIR = Path(__file__).resolve().parent.parent


def run_pipeline(mode: str = "synthetic") -> dict:
    logs_dir = BASE_DIR / "data" / "processed" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    prov_log = logs_dir / "provenance.jsonl"
    if prov_log.exists():
        prov_log.unlink()  # Idempotent fresh run log

    # Stage 1: Source Discovery
    sources = [s.to_dict() for s in discover_sources(offline_mode=(mode == "synthetic"))]
    record_provenance(prov_log, "STAGE_1_SOURCE_DISCOVERY", 0, len(sources), "COMPLETED", {"sources": sources})

    # Stage 2 & 3: Collection / Synthetic Generation
    synth_csv = BASE_DIR / "data" / "synthetic" / "phi_synthetic_pilot.csv"
    raw_df = generate_synthetic_pilot(synth_csv, n_records=150)
    record_provenance(prov_log, "STAGE_2_3_COLLECTION_EXTRACTION", 0, len(raw_df), "COMPLETED", {"mode": mode, "file": str(synth_csv)})

    # Stage 4: Normalization
    norm_df, corrections = normalize_records(raw_df)
    (logs_dir / "correction_log.json").write_text(json.dumps(corrections, indent=2), encoding="utf-8")
    record_provenance(prov_log, "STAGE_4_NORMALIZATION", len(raw_df), len(norm_df), "COMPLETED", {"corrections_count": len(corrections)})

    # Stage 5: Deduplication
    dedup_df, dups_df = deduplicate_records(norm_df)
    dups_df.to_csv(logs_dir / "duplicates_removed.csv", index=False, encoding="utf-8")
    record_provenance(prov_log, "STAGE_5_DEDUPLICATION", len(norm_df), len(dedup_df), "COMPLETED", {"duplicates_removed": len(dups_df)})

    # Stage 6: Validation & Quality Scoring
    schema_path = BASE_DIR / "schemas" / "phi_schema.json"
    val_df, val_issues = validate_dataframe(dedup_df, schema_path)
    (logs_dir / "validation_report.json").write_text(json.dumps(val_issues, indent=2), encoding="utf-8")
    record_provenance(prov_log, "STAGE_6_VALIDATION", len(dedup_df), len(val_df), "COMPLETED", {"flagged_issues": len(val_issues)})

    # Stage 7: Privacy Review
    priv_df, pii_flags = run_privacy_review(val_df)
    (logs_dir / "privacy_report.json").write_text(json.dumps(pii_flags, indent=2), encoding="utf-8")
    record_provenance(prov_log, "STAGE_7_PRIVACY_REVIEW", len(val_df), len(priv_df), "COMPLETED", {"pii_flagged": len(pii_flags)})

    # Compute derived duration_days (zero-imputation: keep NaN where invalid or missing)
    reg = pd.to_datetime(priv_df["registration_date"], errors="coerce")
    dec = pd.to_datetime(priv_df["decision_date"], errors="coerce")
    dur = (dec - reg).dt.days
    priv_df["duration_days"] = dur.where(dur >= 0)

    # Save processed Parquet & analytical DB (DuckDB if available, else SQLite fallback)
    proc_parquet = BASE_DIR / "data" / "processed" / "phi_pilot_validated.parquet"
    priv_df.to_parquet(proc_parquet, index=False)

    db_path = BASE_DIR / "data" / "processed" / "iljo_analytics.db"
    with sqlite3.connect(db_path) as conn:
        priv_df.to_sql("phi_judgments", conn, if_exists="replace", index=False)

    # Stage 8/9: Filter approved analysis-ready records (Validated + PASS privacy + quality >= 0.80)
    public_df = priv_df[
        (priv_df["validation_status"] == "Validated")
        & (priv_df["privacy_review_status"] == "PASS")
        & (priv_df["quality_score"] >= 0.80)
    ].copy()
    public_csv = BASE_DIR / "data" / "public" / "phi_synthetic_release_candidate.csv"
    public_df.to_csv(public_csv, index=False, encoding="utf-8")

    summary = {
        "mode": mode,
        "raw_count": len(raw_df),
        "deduped_count": len(dedup_df),
        "duplicates_removed": len(dups_df),
        "validation_flagged": int((priv_df["validation_status"] == "Flagged").sum()),
        "privacy_flagged": len(pii_flags),
        "analysis_ready_count": len(public_df),
        "mean_quality_score": round(float(priv_df["quality_score"].mean()), 4),
    }
    (logs_dir / "pipeline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    record_provenance(prov_log, "STAGE_8_9_PUBLICATION_CANDIDATE", len(priv_df), len(public_df), "COMPLETED", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ILJO v1.0 Pipeline")
    parser.add_argument("--mode", default="synthetic", choices=["synthetic", "live"])
    args = parser.parse_args()
    res = run_pipeline(mode=args.mode)
    print(json.dumps(res, indent=2))
