# Privacy & Re-Identification Policy — ILJO v1.0

## 1. Guiding Principle
Public availability of court decisions on [Direktori Putusan Mahkamah Agung RI](https://putusan3.mahkamahagung.go.id) does **not** extinguish privacy or data-protection obligations.

## 2. Personal Identifiable Information (PII) Handling
The following identifiers MUST be redacted or excluded prior to any `data/public/` release:
- Full names, aliases, NIK/KTP numbers, phone numbers, email addresses, and home addresses of individual workers, witnesses, and family members.
- Names of individual judges, registrars (*panitera*), and legal counsel in public analytical tables (consistent with our ban on individual judge/lawyer rankings).
- Sensitive personal attributes (health conditions, union membership of named individuals, criminal history, or financial account numbers).

## 3. Automated Privacy Review Gate (Stage 7)
Before any dataset receives `publication_status = Approved`:
1. Run `processing/privacy_review.py` to scan all string fields (`claim_summary`, `case_category`, etc.) for regex patterns matching NIK (16-digit), phone numbers, email addresses, street addresses (`Jl.`, `RT/RW`), and personal honorifics (`Sdr.`, `Sdri.`, `Bpk.`, `Ibu`).
2. Flag any record failing the PII scan with `privacy_review_status = FLAGGED` and block it from `data/public/`.
3. Assess k-anonymity / small-cell re-identification risk (e.g., rare dispute types in small district courts in a single year).
4. Require explicit human Privacy Officer sign-off before release.
