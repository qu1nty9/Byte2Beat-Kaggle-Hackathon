# Byte2Beat Hackathon Workspace

This repository is the working area for a Kaggle Byte2Beat / Hack4Health project on cardiovascular AI.

## Current Sources

- `docs/Byte2Beat - description.pdf`: Kaggle-facing description and writeup instructions.
- `docs/drive-download-20260627T215828Z-3-001/Byte2Beat Competition Packet.docx`: competition overview and suggested workflow.
- `docs/drive-download-20260627T215828Z-3-001/Hack4Health Hackathon Rules General.docx`: official rules, deliverables, AI policy, and publishing note.
- `docs/drive-download-20260627T215828Z-3-001/Byte2Beat Project Ideas.xlsm`: 102 idea catalog with datasets and method tags.
- `docs/drive-download-20260627T215828Z-3-001/Datasets/`: provided sample datasets.

## Working Structure

- `research/`: LLM-maintained project wiki, planning notes, source summaries, and decision log.
- `scripts/`: reproducible utility scripts for profiling and data checks.
- `src/byte2beat/`: reusable project code.
- `notebooks/`: Kaggle/Colab-style notebooks for EDA, baselines, and final public notebook drafts.
- `outputs/`: generated tables, figures, model artifacts, and audit outputs.
- `paper/`: optional manuscript/preprint outline and publication readiness notes.
- `demo/`: optional educational demo scaffold.
- `submission/`: team-facing Kaggle submission template, result cards, claims ledger, figure manifest, and final checklist.

## Quickstart

Create the environment and run the current foundation pipeline:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/profile_data.py
.venv/bin/python scripts/eda_tabular.py
.venv/bin/python scripts/generate_eda_figures.py
.venv/bin/python scripts/baseline_tabular_numpy.py
.venv/bin/python scripts/model_comparison.py
.venv/bin/python scripts/cleaning_sensitivity.py
.venv/bin/python scripts/error_analysis.py
```

The scripts write audit tables, model metrics, calibration bins, subgroup metrics, and writeup-ready figures under `outputs/`.

Equivalent Makefile commands:

```bash
make setup
make all
make check
```

For submission readiness checks:

```bash
make submission-check
```

This gate validates required assets, core result table schemas, JSON audit artifacts, required figures, notebook execution status, notebook error outputs, and private/local path leaks in notebooks.
It also checks that the claims ledger and review-ready writeup point only to existing evidence artifacts.

Notebook roles:

- `notebooks/01_eda_and_baseline.ipynb`: working reproducible analysis notebook.
- `notebooks/02_final_kaggle_notebook.ipynb`: polished submission-facing notebook for Kaggle review.

Submission writing assets:

- `submission/final_kaggle_writeup.md`: final Kaggle writeup text with title, subtitle, and author block.
- `submission/kaggle_writeup_review_draft.md`: review-ready evidence-backed Kaggle writeup scaffold.
- `submission/data_card.md`: project-level data card for sources, cleaning, risks, and intended use.
- `submission/model_card.md`: selected model card with metrics, failure modes, and limitations.
- `submission/claims_ledger.md`: claim-by-claim evidence map and overclaiming guardrails.
- `paper/publication_readiness.md`: arXiv/journal path, reporting-guideline alignment, and publication prerequisites.

## Current Baseline

On the plausibility-cleaned cardiac dataset, the current best sklearn model is `hist_gradient_boosting`:

- Held-out test AUROC: 0.8037.
- Held-out test AUPRC: 0.7892.
- Held-out test Brier score: 0.1795.
- 5-fold CV AUROC: 0.8013 +/- 0.0025.

These are foundation results, not final claims. The project still needs deeper sensitivity analysis, calibration reporting, subgroup interpretation, and a polished Kaggle Writeup.

Cleaning sensitivity is now included. The selected boosting model remains stable near AUROC 0.80 across raw, lenient, current, and strict cleaning profiles, while raw implausible values hurt logistic regression more clearly.

Error analysis is also included. The selected model misses many lower-BP positives and overcalls some high-BP negatives, which is central to the final limitations story.

## Working Principle

The project follows an LLM-wiki pattern:

1. Raw sources in `docs/` are immutable.
2. Research synthesis lives in `research/` as markdown pages.
3. `AGENTS.md` defines the workflow and conventions for updating the wiki.
4. Every experiment should leave a trace: hypothesis, data used, cleaning choices, metric, result, and limitation.
