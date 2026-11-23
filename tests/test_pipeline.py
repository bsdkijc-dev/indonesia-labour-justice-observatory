"""Comprehensive unit and integration tests for ILJO v1.0 pipeline."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

from crawler.source_discovery import discover_sources
from processing.deduplication import deduplicate_records
from processing.metadata_extraction import normalize_court_name
from processing.privacy_review import scan_pii_text
from processing.run_pipeline import run_pipeline


BASE_DIR = Path(__file__).resolve().parent.parent


class TestILJOPipeline(unittest.TestCase):
    def test_court_normalization(self):
        self.assertEqual(normalize_court_name("pn jkt.pst"), "PN Jakarta Pusat")
        self.assertEqual(normalize_court_name("  "), "Unknown")

    def test_pii_scanner_catches_nik_and_email(self):
        hits = scan_pii_text("Sdr. Ahmad, NIK 3171012345678901, email ahmad@example.com")
        self.assertIn("NIK_16_DIGIT", hits)
        self.assertIn("EMAIL", hits)
        self.assertIn("PERSONAL_HONORIFIC", hits)

    def test_pii_scanner_passes_clean_text(self):
        hits = scan_pii_text("Termination dispute regarding severance pay under UU 2/2004.")
        self.assertEqual(hits, [])

    def test_offline_source_discovery_respects_governance(self):
        routes = discover_sources(offline_mode=True)
        self.assertEqual(len(routes), 1)
        self.assertFalse(routes[0].permitted)
        self.assertEqual(routes[0].access_mode, "synthetic_fallback")

    def test_end_to_end_pipeline_idempotent_and_gates_edge_cases(self):
        res1 = run_pipeline(mode="synthetic")
        res2 = run_pipeline(mode="synthetic")
        self.assertEqual(res1, res2)
        self.assertEqual(res1["raw_count"], 154)
        self.assertEqual(res1["duplicates_removed"], 1)
        self.assertGreaterEqual(res1["validation_flagged"], 2)  # bad date + low-conf AI
        self.assertEqual(res1["privacy_flagged"], 1)

        pub_csv = BASE_DIR / "data" / "public" / "phi_synthetic_release_candidate.csv"
        self.assertTrue(pub_csv.exists())
        pub_df = pd.read_csv(pub_csv)
        self.assertTrue((pub_df["privacy_review_status"] == "PASS").all())
        self.assertTrue((pub_df["validation_status"] == "Validated").all())
        self.assertTrue((pub_df["quality_score"] >= 0.80).all())
        self.assertTrue((pub_df["publication_status"] == "Synthetic_Only").all())

        summary_json = BASE_DIR / "data" / "processed" / "logs" / "pipeline_summary.json"
        self.assertTrue(summary_json.exists())
        loaded = json.loads(summary_json.read_text(encoding="utf-8"))
        self.assertEqual(loaded["analysis_ready_count"], len(pub_df))


if __name__ == "__main__":
    unittest.main()
