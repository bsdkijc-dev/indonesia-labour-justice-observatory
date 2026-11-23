"""Stage 5: Deterministic Deduplication of Judgment Records."""

from __future__ import annotations

import pandas as pd


def deduplicate_records(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Removes duplicate documents by document_sha256 and (case_number, court_name).

    Keeps the highest-confidence / first-seen record and returns (deduped_df, duplicates_df).
    """
    working = df.copy()
    working["_sort_conf"] = pd.to_numeric(working["extraction_confidence"], errors="coerce").fillna(0.0)
    working = working.sort_values(by=["_sort_conf", "record_id"], ascending=[False, True])

    dup_hash = working.duplicated(subset=["document_sha256"], keep="first")
    dup_case = working.duplicated(subset=["case_number", "court_name"], keep="first")
    is_dup = dup_hash | dup_case

    duplicates_df = working[is_dup].drop(columns=["_sort_conf"]).copy()
    deduped_df = working[~is_dup].drop(columns=["_sort_conf"]).sort_values("record_id").reset_index(drop=True)
    return deduped_df, duplicates_df
