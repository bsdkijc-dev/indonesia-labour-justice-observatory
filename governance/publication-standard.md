# Publication Standard — ILJO v1.0

## 1. Pre-Publication Checklist (Mandatory Gate)
No dataset, report, or dashboard may be published to GitHub (`bsdkijc-dev`) or Kaggle (`judicialcollege`) until all 8 checks pass:
1. **Data Governance Status:** Zero-imputation and epistemic distinction verified.
2. **Privacy & Re-Identification Risk:** Stage 7 `privacy_review.py` passes with 0 unredacted PII flags.
3. **Source Redistribution Permissions:** Confirmed that only de-identified structured metadata/aggregates are released (never raw case PDFs).
4. **Completeness & Validation Status:** Quality score threshold met; low-confidence AI-extracted fields excluded from published statistics.
5. **Release Manifest:** `publication/release_manifest.json` generated with exact file list, row counts, and version tag.
6. **Checksums:** SHA-256 checksums (`publication/SHA256SUMS.txt`) generated for all release artifacts.
7. **Publication Preview:** Summary preview generated for Research Director review.
8. **Human Approval:** Explicit sign-off from Research Director (Cecep Mustafa, Ph.D.).

## 2. Mandatory Disclaimers on All Releases
Every published dataset, notebook, and policy brief must state:
- Independent research status (not an official Mahkamah Agung RI initiative).
- Synthetic vs. empirical data provenance.
- Non-observability of judgment execution from decision texts alone.
