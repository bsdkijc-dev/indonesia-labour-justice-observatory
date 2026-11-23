# Statistical Summary Report — ILJO v1.0 (Synthetic Pilot)

> **Epistemic Notice:** All figures below derive from `data/public/phi_synthetic_release_candidate.csv` (`publication_status = Synthetic_Only`, `n = 150`) to validate the analytical engine. They are **not** empirical findings on Indonesian courts.

| Metric | Value / Breakdown | Denominator / Missingness |
| :--- | :--- | :--- |
| **Analysis-Ready Records** | `150` | 150 / 153 deduped (3 gated out by quality/privacy) |
| **Dispute Types** | Termination `93` (62.0%), Rights `40` (26.7%), Interest `13` (8.7%), Inter-union `4` (2.7%) | `n = 150` (0 missing) |
| **Judgment Outcomes** | Partly granted `57` (38.0%), Granted `37` (24.7%), Rejected `32` (21.3%), Dismissed on procedural grounds `20` (13.3%), Unknown `4` (2.7%) | `n = 150` |
| **Registration-to-Decision Duration** | Median `131.0` days (IQR: `94.5` – `170.5` days) | `131 / 150` valid (`19` missing = `12.7%`) |
| **Worker Representation** | Advocate `62` (41.3%), Union `34` (22.7%), Legal Aid `24` (16.0%), Self-represented `19` (12.7%), Unknown `11` (7.3%) | `n = 150` |
| **Execution Status** | Not observable `131` (87.3%), Unknown `19` (12.7%), Confirmed executed `0` | `n = 150` (zero-inference rule enforced) |

See `reports/statistical/synthetic_pilot_overview.png` and `analysis/01_corpus_profile.ipynb` – `06_legal_issues.ipynb` for full reproducible breakdowns.
