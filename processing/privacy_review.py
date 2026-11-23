"""Stage 7: Automated Privacy & Re-Identification Risk Review."""

from __future__ import annotations

import re
import pandas as pd


PII_PATTERNS = {
    "NIK_16_DIGIT": re.compile(r"\b\d{16}\b"),
    "EMAIL": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "PHONE_ID": re.compile(r"\b(?:\+62|62|08)\d{8,12}\b"),
    "STREET_ADDRESS": re.compile(r"\b(?:Jl\.|Jalan)\s+[A-Z][A-Za-z0-9\s.,/-]{4,}\b"),
    "PERSONAL_HONORIFIC": re.compile(r"\b(?:Sdr\.|Sdri\.|Bpk\.|Ibu)\s+[A-Z][a-z]+\b"),
}


def scan_pii_text(text: str | None) -> list[str]:
    if not text or pd.isna(text):
        return []
    hits = []
    for label, pattern in PII_PATTERNS.items():
        if pattern.search(str(text)):
            hits.append(label)
    return hits


def run_privacy_review(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    out = df.copy()
    flags: list[dict] = []
    statuses: list[str] = []

    for _, row in out.iterrows():
        hits = scan_pii_text(row.get("claim_summary"))
        if hits:
            statuses.append("FLAGGED_PII")
            flags.append({"record_id": row.get("record_id"), "pii_hits": hits})
        else:
            statuses.append("PASS")

    out["privacy_review_status"] = statuses
    return out, flags
