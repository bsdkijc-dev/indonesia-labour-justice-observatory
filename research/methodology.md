# Empirical Methodology — ILJO v1.0

## 1. Epistemic & Statistical Standards
- **Descriptive First:** Report exact numerators, denominators, missing-data rates, medians, and interquartile ranges (IQR) before any inferential modeling.
- **No Causal Overreach:** Observational court records suffer from selection bias (only disputes that survive bipartite/tripartite mediation and reach PHI are filed). Causal claims are prohibited unless justified by quasi-experimental design.
- **AI-Extraction Gate:** Fields extracted by NLP/LLM methods are tagged `extraction_method = ai_assisted` and must not enter published statistical tables unless `extraction_confidence >= 0.85` and `validation_status = Validated`.

## 2. Duration & Outcome Calculations
- `duration_days = (decision_date - registration_date).days` where both dates are valid and `decision_date >= registration_date`.
- Records with missing or inverted dates are excluded from duration quantiles and reported explicitly in the missing-data audit table.
- Statutory benchmark comparison: [UU No. 2 Tahun 2004](https://peraturan.bpk.go.id/Details/40452/uu-no-2-tahun-2004) sets a 50-working-day target at PHI first instance (Pasal 103) and 30 working days at Supreme Court cassation (Pasal 115); ILJO measures calendar days and notes this distinction explicitly.
