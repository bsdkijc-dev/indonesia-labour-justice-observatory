<div align="center">

<img src="assets/logo.svg" alt="Indonesia Labour Justice Observatory (ILJO) Logo" width="140">

# Indonesia Labour Justice Observatory (ILJO)

### Empirical research on Industrial Relations Court (PHI) decisions and workers' access to justice in Indonesia.

[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE) ![Stack](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white) [![CI](https://github.com/bsdkijc-dev/indonesia-labour-justice-observatory/actions/workflows/validate-data.yml/badge.svg)](https://github.com/bsdkijc-dev/indonesia-labour-justice-observatory/actions/workflows/validate-data.yml)

[Documentation](research/) · [Repository](https://github.com/bsdkijc-dev/indonesia-labour-justice-observatory)

</div>

---

**Research Question:** *"What Do Indonesian Court Decisions Tell Us About Workers' Access to Justice?"*  
**Research Director:** Cecep Mustafa, Ph.D.  
**Institutional Model:** Independent, evidence-based, AI-assisted research initiative (JPAIS architecture).

> **Important Notice:** This is an independent research initiative and is **not** an official initiative of Mahkamah Agung Republik Indonesia. Published court judgments do not constitute proof that remedies were executed or paid. All empirical outputs in this v1.0 sandbox pilot are generated from **synthetic test data** (`data/synthetic/`) pending authorized access verification to [Direktori Putusan Mahkamah Agung RI](https://putusan3.mahkamahagung.go.id).

## Repository Structure

```text
indonesia-labour-justice-observatory/
├── governance/        # Ethics, data governance, privacy, publication, source access policies
├── research/          # Protocol, methodology, research questions, limitations, legal framework
├── schemas/           # JSON Schema, data dictionary CSV, YAML validation rules
├── crawler/           # Robots check, source discovery, polite collector, provenance logger
├── processing/        # Extraction, parsing, deduplication, validation, privacy review
├── data/              # raw/, staging/, processed/, public/, synthetic/
├── analysis/          # 6 reproducible Jupyter notebooks (01_corpus_profile .. 06_legal_issues)
├── reports/           # Technical, statistical, policy, and public education outputs
├── publication/       # GitHub, Kaggle, and dashboard release candidates (pending approval)
├── tests/             # Automated unit, schema, quality, and privacy tests
└── .github/workflows/ # CI validation workflows
```

## Quick Start (Local Validation & Synthetic Pilot)

```bash
python3 -m pip install -r requirements.txt
python3 -m processing.run_pipeline --mode synthetic
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Governance & Citation

See `CITATION.cff`, `LICENSE`, and `governance/` for ethical, privacy, and redistribution rules.

---

<div align="center">

**Indonesia Labour Justice Observatory (ILJO)**

[github.com/bsdkijc-dev/indonesia-labour-justice-observatory](https://github.com/bsdkijc-dev/indonesia-labour-justice-observatory)

</div>
