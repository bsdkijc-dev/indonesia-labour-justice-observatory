"""Stage 6: Automated Data Quality Validation & Scoring."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import jsonschema
import pandas as pd


CASE_PATTERN = re.compile(r"^\d+/(?:K/)?Pdt\.Sus-PHI/\d{4}/.+$")


def load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_dataframe(df: pd.DataFrame, schema_path: Path) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    schema = load_schema(schema_path)
    validator = jsonschema.Draft202012Validator(schema)

    issues: list[dict[str, Any]] = []
    quality_scores: list[float] = []
    val_statuses: list[str] = []

    for idx, row in df.iterrows():
        rec = {}
        for k, v in row.items():
            rec[k] = None if pd.isna(v) else v

        record_errors = []
        for err in validator.iter_errors(rec):
            record_errors.append(f"SCHEMA:{err.message}")

        if not CASE_PATTERN.match(str(rec.get("case_number", ""))):
            record_errors.append("CHK_01_CASE_NUMBER: invalid PHI docket pattern")

        reg = pd.to_datetime(rec.get("registration_date"), errors="coerce")
        dec = pd.to_datetime(rec.get("decision_date"), errors="coerce")
        pub = pd.to_datetime(rec.get("publication_date"), errors="coerce")

        if pd.notna(reg) and pd.notna(dec) and dec < reg:
            record_errors.append("CHK_02_DATE_ORDER: decision_date before registration_date")
        if pd.notna(dec) and pd.notna(pub) and pub < dec:
            record_errors.append("CHK_03_PUB_DATE_ORDER: publication_date before decision_date")

        conf = float(rec.get("extraction_confidence") or 0.0)
        method = rec.get("extraction_method")
        if method == "ai_assisted" and conf < 0.85:
            record_errors.append("CHK_08_AI_CONFIDENCE_GATE: ai_assisted confidence < 0.85")

        if rec.get("dispute_type") in ("Interest dispute", "Inter-union dispute") and rec.get("appeal_status") in ("Appealed to cassation", "Cassation decided"):
            record_errors.append("CHK_09_APPEAL_CONSISTENCY: non-cassable dispute marked appealed")

        # Compute quality score (1.0 minus weighted penalties)
        score = 1.0
        if pd.isna(reg) or pd.isna(dec):
            score -= 0.15
        if rec.get("dispute_type") == "Unknown":
            score -= 0.05
        if rec.get("judgment_outcome") == "Unknown":
            score -= 0.05
        score -= 0.25 * len(record_errors)
        score = round(max(0.0, min(1.0, score)), 3)

        quality_scores.append(score)
        if record_errors:
            val_statuses.append("Flagged")
            for msg in record_errors:
                issues.append({"record_id": rec.get("record_id"), "issue": msg, "quality_score": score})
        else:
            val_statuses.append("Validated")

    out = df.copy()
    out["quality_score"] = quality_scores
    out["validation_status"] = val_statuses
    return out, issues
