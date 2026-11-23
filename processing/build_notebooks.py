"""Generates and executes all 6 reproducible ILJO analytical notebooks (nbformat 4)."""

from __future__ import annotations

import base64
import contextlib
import io
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
REPORTS_STAT_DIR = BASE_DIR / "reports" / "statistical"


NOTEBOOK_SPECS = [
    (
        "01_corpus_profile.ipynb",
        "# 01 — Corpus Profile (Synthetic Pilot Validation)\n\n> **Notice:** Analysis runs on `data/public/phi_synthetic_release_candidate.csv` (`publication_status = Synthetic_Only`).",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
print(f"Total analysis-ready synthetic records: {len(df)}")
print("\\nDistribution by Decision Year:")
print(df['decision_date'].str[:4].value_counts().sort_index())
print("\\nDistribution by Court Level:")
print(df['court_level'].value_counts(dropna=False))
print("\\nDistribution by Dispute Type:")
print(df['dispute_type'].value_counts(dropna=False))
""",
    ),
    (
        "02_case_distribution.ipynb",
        "# 02 — Access to Justice: Court & Representation Distribution",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
print("Top Courts:")
print(df['court_name'].value_counts())
print("\\nWorker Representation:")
print(df['worker_representation'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')
print("\\nEmployer Representation:")
print(df['employer_representation'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')
""",
    ),
    (
        "03_case_duration.ipynb",
        "# 03 — Timeliness & Duration Analysis (Registration to Decision)",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
valid_dur = df['duration_days'].dropna()
missing_rate = df['duration_days'].isna().mean() * 100
print(f"Valid duration numerator/denominator: {len(valid_dur)}/{len(df)} (Missing rate: {missing_rate:.1f}%)")
print(f"Overall Median: {valid_dur.median():.1f} days | IQR: {valid_dur.quantile(0.25):.1f} - {valid_dur.quantile(0.75):.1f} days")
print("\\nMedian & IQR by Court Level:")
print(df.groupby('court_level')['duration_days'].agg(['count', 'median', lambda s: s.quantile(0.25), lambda s: s.quantile(0.75)]).rename(columns={'<lambda_0>': 'q25', '<lambda_1>': 'q75'}))
""",
    ),
    (
        "04_judgment_outcomes.ipynb",
        "# 04 — Judgment Outcomes & Procedural Dismissals",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
print("Judgment Outcomes (Counts & %):")
ct = pd.DataFrame({'count': df['judgment_outcome'].value_counts(), 'pct': df['judgment_outcome'].value_counts(normalize=True).mul(100).round(1)})
print(ct)
print("\\nOutcomes by Worker Representation (%):")
print(pd.crosstab(df['worker_representation'], df['judgment_outcome'], normalize='index').mul(100).round(1))
""",
    ),
    (
        "05_remedies_analysis.ipynb",
        "# 05 — Remedies & Execution Observability Gap",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
print("Remedy Types:")
print(df['remedy_type'].value_counts())
print("\\nExecution Status (Never inferred from judgment text alone):")
print(df['execution_status'].value_counts(dropna=False))
""",
    ),
    (
        "06_legal_issues.ipynb",
        "# 06 — Appeal Patterns & Statutory Context",
        """import pandas as pd
df = pd.read_csv('../data/public/phi_synthetic_release_candidate.csv')
print("Appeal Status by Dispute Type:")
print(pd.crosstab(df['dispute_type'], df['appeal_status']))
""",
    ),
]


def _make_nb(md_text: str, code_text: str, stdout_text: str) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.2"},
        },
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": md_text.splitlines(keepends=True)},
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": stdout_text.splitlines(keepends=True),
                    }
                ],
                "source": code_text.splitlines(keepends=True),
            },
        ],
    }


def build_and_run_all() -> dict:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_STAT_DIR.mkdir(parents=True, exist_ok=True)

    # Execute each notebook's code in analysis/ working directory
    import os
    orig_cwd = os.getcwd()
    os.chdir(ANALYSIS_DIR)
    try:
        for fname, md_text, code_text in NOTEBOOK_SPECS:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(code_text, fname, "exec"), {})
            nb_dict = _make_nb(md_text, code_text, buf.getvalue())
            (ANALYSIS_DIR / fname).write_text(json.dumps(nb_dict, indent=2), encoding="utf-8")
    finally:
        os.chdir(orig_cwd)

    # Compute verified summary metrics JSON + chart for reports
    df = pd.read_csv(BASE_DIR / "data" / "public" / "phi_synthetic_release_candidate.csv")
    valid_dur = df["duration_days"].dropna()
    metrics = {
        "dataset_status": "SYNTHETIC_PILOT_ONLY",
        "n_analysis_ready": int(len(df)),
        "dispute_types": df["dispute_type"].value_counts().to_dict(),
        "outcomes": df["judgment_outcome"].value_counts().to_dict(),
        "execution_status": df["execution_status"].value_counts().to_dict(),
        "duration_valid_n": int(len(valid_dur)),
        "duration_missing_n": int(df["duration_days"].isna().sum()),
        "duration_median_days": round(float(valid_dur.median()), 1),
        "duration_q25_days": round(float(valid_dur.quantile(0.25)), 1),
        "duration_q75_days": round(float(valid_dur.quantile(0.75)), 1),
        "worker_representation": df["worker_representation"].value_counts().to_dict(),
    }
    (REPORTS_STAT_DIR / "synthetic_pilot_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # Generate summary chart
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    df["dispute_type"].value_counts().plot(kind="barh", ax=axes[0], color="#1f4e79")
    axes[0].set_title("Synthetic Pilot: Dispute Types (n=150)")
    axes[0].set_xlabel("Records")
    df["judgment_outcome"].value_counts().plot(kind="barh", ax=axes[1], color="#2e7d32")
    axes[1].set_title("Synthetic Pilot: Judgment Outcomes (n=150)")
    axes[1].set_xlabel("Records")
    plt.tight_layout()
    plt.savefig(REPORTS_STAT_DIR / "synthetic_pilot_overview.png", dpi=150)
    plt.close(fig)
    return metrics


if __name__ == "__main__":
    print(json.dumps(build_and_run_all(), indent=2))
