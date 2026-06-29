# Project Log

## [2026-06-28] ingest | Competition folder

Parsed the local Byte2Beat workspace. The folder contains competition documents, an idea catalog, two tabular cardiovascular datasets, and one large ECG time-series CSV. No git repository or dependency scaffold existed at the start.

## [2026-06-28] ingest | LLM-wiki principle

Read the referenced gist describing an LLM-maintained persistent wiki over immutable raw sources. Adapted it into `AGENTS.md` and the `research/` directory structure.

## [2026-06-28] audit | Initial dataset profile

Ran a first-pass profile of the provided CSV files. Key findings: cardiac failure has 70,000 balanced rows but blood pressure outliers; heart attack has 918 rows and many zero cholesterol values; ECG CSV is 632 MB with 528 rows and roughly 124k columns, requiring special handling.

## [2026-06-28] eda | Tabular cleaning impact

Added `scripts/eda_tabular.py` and generated cleaning-impact tables. In `cardio_base.csv`, the initial body-and-BP plausibility filter removes 1,395 of 70,000 rows and shifts target rate from 0.4997 to 0.4947. In `heart_processed.csv`, treating zero cholesterol as unobserved affects 172 of 918 rows and changes target rate from 0.5534 to 0.4772 in the observed-cholesterol subset.

## [2026-06-28] model | Numpy logistic baseline

Added `scripts/baseline_tabular_numpy.py`, a dependency-light logistic-regression baseline. On the cleaned cardiac dataset, the held-out test AUROC is 0.7974 with accuracy 0.7359. On the small heart dataset, held-out test AUROC is 0.9411 with accuracy 0.8705, but this result is high-variance due to the small sample size.

## [2026-06-28] plan | Full ideal project operating plan

Expanded `research/project_plan.md` into the canonical execution plan. The plan now defines the project thesis, ideal-project criteria, phase-by-phase tasks, quality gates, risk register, execution cadence, Kaggle Writeup structure, and article/preprint path.

## [2026-06-28] foundation | Environment, sklearn models, and writeup artifacts

Created `.venv`, installed project dependencies, added reusable code under `src/byte2beat/`, generated EDA figures, and added `scripts/model_comparison.py`. Current best cardiac model is `hist_gradient_boosting` with held-out test AUROC 0.8037 and 5-fold CV AUROC 0.8013 +/- 0.0025. Added notebook/writeup/manuscript scaffolding for the final submission path.

## [2026-06-28] audit | ECG schema gate

Added `scripts/profile_ecg_schema.py` and generated `outputs/tables/ecg_schema_audit.json`. The ECG CSV has 123,995 columns, 528 rows, and 36,441 duplicate non-empty header names, confirming that ECG must remain a gated extension until row semantics and labels are understood.

## [2026-06-28] robustness | Cleaning sensitivity analysis

Added `scripts/cleaning_sensitivity.py` and shared cleaning profiles in `src/byte2beat/data.py`. Tested raw, lenient, current, and strict cardiac cleaning profiles with logistic regression and histogram gradient boosting. Current profile retained 68,605 rows and produced the best held-out boosting AUROC/Brier combination; boosting stayed stable around AUROC 0.80 across profiles, while raw outliers reduced logistic AUROC to 0.7776.

## [2026-06-29] evaluation | Error analysis for selected cardiac model

Added `scripts/error_analysis.py` and generated confusion/error tables plus figures. Main finding: the selected boosting model misses many actual positives in low systolic BP bands and overcalls the minority of negatives in high systolic BP/high cholesterol groups. Added `research/error_analysis.md` and updated the Kaggle notebook/writeup draft.

## [2026-06-29] submission | Kaggle submission scaffold

Added `submission/` package with team-facing writeup template, result cards, figure manifest, final checklist, and submission asset checker. This is intentionally a scaffold rather than final prose because the competition rules require the final written submission to be authored and reviewed by the team.

## [2026-06-29] submission | Final Kaggle notebook draft

Added `notebooks/02_final_kaggle_notebook.ipynb`, a polished submission-facing notebook that reads generated artifacts, presents the evidence flow, and can optionally regenerate the full pipeline. Added it to submission asset checks.

## [2026-06-29] submission | Submission quality gate

Expanded `scripts/check_submission_assets.py` from a presence-only check into a package quality gate. It now validates required assets, key table schemas, JSON audit evidence, figure readability and dimensions, notebook error outputs, final-notebook execution status, and private/local path leakage.

## [2026-06-29] submission | Claims and publication guardrails

Added `submission/claims_ledger.md` to map final writeup claims to concrete evidence artifacts and to separate safe wording from overclaims. Added `paper/publication_readiness.md` to track the extra work required before any blog, preprint, or article publication.

## [2026-06-29] submission | Review-ready writeup and publication plan

Added `submission/kaggle_writeup_review_draft.md` as an evidence-backed Kaggle writeup scaffold and expanded `paper/publication_readiness.md` into the arXiv/journal readiness plan. Added the review draft to the submission quality gate, including section and evidence-link validation, and linked it from project documentation.

## [2026-06-30] submission | Final writeup, data card, and model card

Added `submission/final_kaggle_writeup.md` with the final title, subtitle, and author block for Yaroslav Kholmirzayev. Added `submission/data_card.md` and `submission/model_card.md` to document dataset risks, intended use, model performance, robustness, failure modes, and limitations. Expanded the submission quality gate to validate the final writeup and cards.
