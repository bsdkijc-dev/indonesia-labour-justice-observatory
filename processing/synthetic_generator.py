"""Synthetic Pilot Dataset Generator (150 records, 2021-2026) for Offline Testing.

Clearly tagged with extraction_method='synthetic' and publication_status='Synthetic_Only'.
Includes intentional edge cases (duplicates, date inversion, low-confidence AI record,
and 1 PII-flagged summary) to verify all pipeline quality and privacy gates.
"""

from __future__ import annotations

import hashlib
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


COURTS = [
    ("PN Jakarta Pusat", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Jkt.Pst"),
    ("PN Surabaya", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Sby"),
    ("PN Bandung", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Bdg"),
    ("PN Medan", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Mdn"),
    ("PN Semarang", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Smg"),
    ("PN Makassar", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Mks"),
    ("PN Denpasar", "PHI_First_Instance", "Pdt.Sus-PHI", "PN Dps"),
    ("Mahkamah Agung RI", "MA_Cassation", "K/Pdt.Sus-PHI", "MA"),
]

DISPUTES = [
    ("Termination dispute", 0.58),
    ("Rights dispute", 0.30),
    ("Interest dispute", 0.08),
    ("Inter-union dispute", 0.04),
]

OUTCOMES = [
    ("Partly granted", 0.38),
    ("Granted", 0.24),
    ("Rejected", 0.22),
    ("Dismissed on procedural grounds", 0.12),
    ("Unknown", 0.04),
]

WORKER_REP = ["Advocate", "Union", "Legal Aid", "Self-represented", "Unknown"]
EMP_REP = ["Advocate", "In-house Legal", "Self-represented", "Unknown"]


def _weighted_choice(rng: random.Random, items: list[tuple[str, float]]) -> str:
    labels, weights = zip(*items)
    return rng.choices(labels, weights=weights, k=1)[0]


def generate_synthetic_pilot(output_csv: Path, n_records: int = 150, seed: int = 20261123) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []

    for i in range(1, n_records + 1):
        year = rng.choices([2021, 2022, 2023, 2024, 2025, 2026], weights=[14, 16, 20, 22, 18, 10], k=1)[0]
        court_name, court_level, cat, code = rng.choice(COURTS)
        dispute = _weighted_choice(rng, DISPUTES)
        outcome = _weighted_choice(rng, OUTCOMES)

        reg_dt = date(year, 1, 1) + timedelta(days=rng.randint(0, 280))
        dur = rng.randint(45, 210) if court_level == "PHI_First_Instance" else rng.randint(35, 160)
        dec_dt = reg_dt + timedelta(days=dur)
        pub_dt = dec_dt + timedelta(days=rng.randint(7, 45))

        # Realistic missingness (zero-imputation: leave None)
        reg_str = None if rng.random() < 0.06 else reg_dt.isoformat()
        dec_str = dec_dt.isoformat()
        pub_str = None if rng.random() < 0.08 else pub_dt.isoformat()

        w_rep = rng.choices(WORKER_REP, weights=[0.35, 0.28, 0.12, 0.17, 0.08], k=1)[0]
        e_rep = rng.choices(EMP_REP, weights=[0.52, 0.28, 0.08, 0.12], k=1)[0]

        if outcome in ("Granted", "Partly granted"):
            if dispute == "Termination dispute":
                remedy = rng.choice(["Severance pay; Unpaid wages", "Severance pay; Compensation", "Reinstatement; Unpaid wages"])
            elif dispute == "Rights dispute":
                remedy = rng.choice(["Unpaid wages", "Compensation", "Unpaid wages; Compensation"])
            else:
                remedy = "Other"
        elif outcome in ("Rejected", "Dismissed on procedural grounds"):
            remedy = "None"
        else:
            remedy = "Unknown"

        if dispute in ("Interest dispute", "Inter-union dispute"):
            appeal = "Not appealable"
        elif court_level == "MA_Cassation":
            appeal = "Cassation decided"
        else:
            appeal = rng.choice(["Not appealed", "Appealed to cassation", "Not observable"])

        exec_status = rng.choices(["Not observable", "Unknown"], weights=[0.88, 0.12], k=1)[0]
        case_num = f"{100 + i}/{cat}/{year}/{code}"
        payload_hash = hashlib.sha256(f"SYNTHETIC-{case_num}".encode()).hexdigest()

        rows.append({
            "record_id": f"ILJO-{year}-{i:04d}",
            "case_number": case_num,
            "court_name": court_name,
            "court_level": court_level,
            "case_category": cat,
            "dispute_type": dispute,
            "registration_date": reg_str,
            "decision_date": dec_str,
            "publication_date": pub_str,
            "plaintiff_type": "Worker" if dispute != "Inter-union dispute" else "Union",
            "defendant_type": "Employer" if dispute != "Inter-union dispute" else "Union",
            "worker_representation": w_rep,
            "employer_representation": e_rep,
            "claim_summary": f"Synthetic de-identified {dispute.lower()} claim regarding statutory entitlements under UU 2/2004.",
            "judgment_outcome": outcome,
            "remedy_type": remedy,
            "appeal_status": appeal,
            "execution_status": exec_status,
            "source_url": f"https://putusan3.mahkamahagung.go.id/direktori/putusan/synthetic-{i:04d}.html",
            "source_retrieved_at": "2026-11-23T03:45:00+00:00",
            "document_sha256": payload_hash,
            "extraction_method": "synthetic",
            "extraction_confidence": 1.0,
            "validation_status": "Pending",
            "publication_status": "Synthetic_Only",
        })

    # Add 4 intentional edge cases to test pipeline gates (rows 151-154)
    # 1. Exact duplicate hash of row 1
    dup_row = dict(rows[0])
    dup_row["record_id"] = "ILJO-2024-0151"
    rows.append(dup_row)

    # 2. Invalid date order (decision before registration)
    bad_date = dict(rows[1])
    bad_date["record_id"] = "ILJO-2024-0152"
    bad_date["case_number"] = "952/Pdt.Sus-PHI/2024/PN Sby"
    bad_date["document_sha256"] = hashlib.sha256(b"SYNTHETIC-BAD-DATE").hexdigest()
    bad_date["registration_date"] = "2024-10-10"
    bad_date["decision_date"] = "2024-05-01"
    rows.append(bad_date)

    # 3. Low-confidence AI extraction
    low_ai = dict(rows[2])
    low_ai["record_id"] = "ILJO-2024-0153"
    low_ai["case_number"] = "953/Pdt.Sus-PHI/2024/PN Bdg"
    low_ai["document_sha256"] = hashlib.sha256(b"SYNTHETIC-LOW-AI").hexdigest()
    low_ai["extraction_method"] = "ai_assisted"
    low_ai["extraction_confidence"] = 0.62
    rows.append(low_ai)

    # 4. Unredacted PII in claim_summary
    pii_row = dict(rows[3])
    pii_row["record_id"] = "ILJO-2024-0154"
    pii_row["case_number"] = "954/Pdt.Sus-PHI/2024/PN Mdn"
    pii_row["document_sha256"] = hashlib.sha256(b"SYNTHETIC-PII-TEST").hexdigest()
    pii_row["claim_summary"] = "Synthetic PII test: Sdr. Budi Santoso, NIK 3171012345678901, email budi@example.com."
    rows.append(pii_row)

    df = pd.DataFrame(rows)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    return df
