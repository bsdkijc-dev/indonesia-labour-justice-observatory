"""Stage 3b & 4: Metadata Extraction & Normalization."""

from __future__ import annotations

import re
import pandas as pd


COURT_NORMALIZATION = {
    "pn jakarta pusat": "PN Jakarta Pusat",
    "pn jkt.pst": "PN Jakarta Pusat",
    "pn surabaya": "PN Surabaya",
    "pn bandung": "PN Bandung",
    "pn medan": "PN Medan",
    "pn semarang": "PN Semarang",
    "pn makassar": "PN Makassar",
    "pn denpasar": "PN Denpasar",
    "mahkamah agung": "Mahkamah Agung RI",
    "mahkamah agung ri": "Mahkamah Agung RI",
}


def normalize_court_name(raw_name: str | None) -> str:
    if not raw_name or not str(raw_name).strip():
        return "Unknown"
    cleaned = re.sub(r"\s+", " ", str(raw_name)).strip()
    return COURT_NORMALIZATION.get(cleaned.lower(), cleaned)


def normalize_date_str(val: str | None) -> str | None:
    if val is None or pd.isna(val) or str(val).strip() == "":
        return None
    parsed = pd.to_datetime(str(val).strip(), errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y-%m-%d")


def normalize_records(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    df = df.copy()
    corrections: list[dict] = []

    for idx, row in df.iterrows():
        orig_court = row.get("court_name")
        norm_court = normalize_court_name(orig_court)
        if orig_court != norm_court:
            corrections.append({
                "record_id": row.get("record_id"),
                "field": "court_name",
                "old_value": orig_court,
                "new_value": norm_court,
                "reason": "Standardized court name",
            })
            df.at[idx, "court_name"] = norm_court

        for col in ("registration_date", "decision_date", "publication_date"):
            orig_d = row.get(col)
            norm_d = normalize_date_str(orig_d)
            if pd.notna(orig_d) and str(orig_d).strip() != "" and orig_d != norm_d:
                df.at[idx, col] = norm_d

    return df, corrections
