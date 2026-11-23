# Changelog

## [1.0.0] - 2026-11-23
### Added
- Initialized Indonesia Labour Justice Observatory (ILJO) v1.0 repository structure.
- Added governance suite (`research-ethics.md`, `data-governance.md`, `privacy-policy.md`, `publication-standard.md`, `source-access-policy.md`).
- Added research design suite (`research-protocol.md`, `methodology.md`, `research-questions.md`, `limitations.md`, `legal-framework.md`).
- Added formal PHI schema (`phi_schema.json`), `data_dictionary.csv`, and `validation_rules.yaml`.
- Implemented polite crawler framework (`robots_check.py`, `source_discovery.py`, `polite_collector.py`, `provenance.py`).
- Implemented restartable, idempotent processing pipeline (`metadata_extraction.py`, `document_parser.py`, `deduplication.py`, `validation.py`, `privacy_review.py`, `run_pipeline.py`).
- Generated synthetic pilot dataset (`data/synthetic/phi_synthetic_pilot.csv`, 150 records, 2021–2026) due to sandbox offline/access constraints.
- Built 6 reproducible Jupyter notebooks (`analysis/01_corpus_profile.ipynb` to `06_legal_issues.ipynb`).
- Produced technical, statistical, policy, and public education reports plus GitHub/Kaggle/dashboard release candidates (awaiting human approval).
