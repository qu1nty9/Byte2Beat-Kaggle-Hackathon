# Kaggle Writeup Review Draft

Status: review-ready scaffold. The final Kaggle text must be reviewed, edited, and approved by the team before submission.

## Title

Data Quality-Aware Cardiovascular Risk Modeling

## Subtitle

An interpretable Byte2Beat workflow showing how plausibility checks, calibration, and error analysis change cardiovascular risk prediction.

## Executive Summary

This project treats cardiovascular risk prediction as both a modeling task and a data-quality task. Public biomedical datasets can contain implausible measurements, missing-like values, unclear provenance, and schema ambiguity. Instead of optimizing only for a headline score, we built a reproducible workflow that audits the data, applies transparent plausibility checks, compares simple and non-linear models, evaluates calibration, and inspects false-positive and false-negative patterns.

The main analysis uses the 70,000-row cardiac tabular dataset with the `cardio` target. A transparent plausibility filter removes 1,395 rows, or 1.99 percent of the data, mostly because of blood-pressure and body-measurement anomalies. The selected histogram gradient boosting model reaches held-out AUROC 0.8037, AUPRC 0.7892, accuracy 0.7355, and Brier score 0.1795; 5-fold cross-validation gives AUROC 0.8013 +/- 0.0025. The result is not threshold-fragile: the same model remains near AUROC 0.80 across raw, lenient, current, and strict cleaning profiles.

The most important finding is not that the most complex model wins by a large margin. It does not. Logistic regression is close behind with AUROC 0.7931 and gives a clinically plausible signal structure. The stronger contribution is the reliability story: the model learns recognizable cardiovascular patterns, but it misses many lower-BP positives and overcalls some high-BP/high-cholesterol negatives. This makes the work useful as an educational, transparent risk-modeling case study, not a clinical decision tool.

## Problem Framing

Cardiovascular risk modeling is often presented as a pure prediction problem. In real biomedical machine learning, however, the credibility of a model depends on what happened before and after fitting: source audit, measurement plausibility, missingness handling, split design, calibration, subgroup reliability, and cautious interpretation.

The project question is:

> Can we build a reproducible cardiovascular risk-modeling workflow that is accurate enough to be useful for analysis, but transparent enough to expose where the model is brittle?

This framing is deliberately different from a leaderboard-only approach. A medical AI project can be misleading if it reports AUROC without explaining data artifacts, calibration, and error modes. Our submission therefore emphasizes an auditable pipeline and honest limitations.

## Data Sources

The primary dataset is `cardio_base.csv`, a 70,000-row tabular cardiovascular dataset with demographic variables, body measurements, blood pressure, cholesterol, glucose, lifestyle indicators, and the binary `cardio` target. The target is nearly balanced: 35,021 negative and 34,979 positive rows.

We also audited two extension datasets:

- `heart_processed.csv`, a 918-row heart-disease dataset with one-hot encoded clinical features and a `HeartDisease` target.
- `ecg_timeseries.csv`, a large ECG-like table with 528 rows and 123,995 columns.

The cardiac dataset is the headline modeling dataset. The heart dataset is useful as a comparison source, but it is too small for strong primary claims. The ECG file is not used for headline modeling because the schema and labels are not yet validated; the audit found 36,441 duplicate non-empty header names.

Ethics note: this project is for educational and research analysis only. It is not a clinical device, medical recommendation, diagnosis system, or treatment guide.

## Data Audit

The cardiac base file contains no missing values in the initial audit, but it contains physiologically implausible measurements:

- `ap_hi <= 0`: 7 rows.
- `ap_lo <= 0`: 22 rows.
- `ap_hi > 250`: 40 rows.
- `ap_lo > 200`: 953 rows.
- `ap_lo > ap_hi`: 1,234 rows.
- Height and weight ranges suggest additional body-measurement outliers.

The processed cardiac file still contains blood-pressure anomalies, so we use the base file as the canonical input and apply explicit cleaning rules ourselves.

The heart dataset has 172 rows with `Cholesterol == 0`, which behaves like missingness rather than a valid clinical measurement. This is target-associated and should not be silently removed or treated as ordinary numeric zero.

The ECG dataset is kept as a future extension. Before using it, we would need to establish whether rows represent patients, recordings, leads, or beats; identify labels; and convert the raw wide table to a stable analysis format.

## Cleaning Strategy

The primary cardiac plausibility profile applies these rules:

- Height between 120 and 220 cm.
- Weight between 30 and 250 kg.
- BMI between 10 and 80.
- Systolic BP between 80 and 250.
- Diastolic BP between 40 and 150.
- Diastolic BP must not exceed systolic BP.

This removes 1,395 of 70,000 rows, or 1.99 percent. The target rate changes only modestly, from 0.4997 to 0.4947.

We do not treat this profile as the only possible truth. We compare four profiles:

| Profile | Rows | Removed fraction | Target rate |
|---|---:|---:|---:|
| Raw | 70,000 | 0.0000 | 0.4997 |
| Lenient | 68,644 | 0.0194 | 0.4947 |
| Current | 68,605 | 0.0199 | 0.4947 |
| Strict | 68,362 | 0.0234 | 0.4950 |

This makes the cleaning decision testable rather than hidden.

## Exploratory Findings

The cleaned cardiac dataset shows strong, clinically recognizable structure. Cardio-positive rate rises sharply with systolic BP band:

| Systolic BP band | Cardio-positive rate |
|---|---:|
| `<120` | 0.2305 |
| `120-129` | 0.3560 |
| `130-139` | 0.5985 |
| `>=140` | 0.8370 |

This is useful in two ways. First, it shows that the target aligns with known cardiovascular risk structure. Second, it warns us that the model may lean heavily on blood pressure and therefore needs subgroup error analysis.

## Modeling Methods

We compare:

- Dummy prior baseline.
- Logistic regression.
- Depth-4 decision tree.
- Random forest.
- Histogram gradient boosting.

Evaluation uses:

- Fixed stratified held-out test split.
- 5-fold stratified cross-validation.
- AUROC, AUPRC, accuracy, F1, Brier score, log loss, sensitivity, and specificity.
- Calibration bins and calibration curve.
- Subgroup and error analysis by blood-pressure band, age band, gender coding, and cholesterol category.

The selected model is histogram gradient boosting because it has the strongest held-out AUROC and AUPRC while remaining stable across cleaning profiles. Logistic regression is retained as the transparent baseline.

## Main Results

On the current cleaned cardiac dataset:

| Model | Test AUROC | Test AUPRC | Accuracy | Brier |
|---|---:|---:|---:|---:|
| Dummy prior | 0.5000 | 0.4947 | 0.5053 | 0.2500 |
| Logistic regression | 0.7931 | 0.7750 | 0.7267 | 0.1863 |
| Decision tree depth 4 | 0.7876 | 0.7598 | 0.7296 | 0.1844 |
| Random forest | 0.8024 | 0.7875 | 0.7355 | 0.1801 |
| Histogram gradient boosting | 0.8037 | 0.7892 | 0.7355 | 0.1795 |

The selected model has 5-fold CV AUROC 0.8013 +/- 0.0025. This narrow variation suggests that the result is not a lucky split artifact.

## Cleaning Sensitivity

Held-out AUROC by cleaning profile:

| Cleaning profile | Logistic regression | HistGradientBoosting |
|---|---:|---:|
| Raw | 0.7776 | 0.8004 |
| Lenient | 0.7917 | 0.8025 |
| Current | 0.7931 | 0.8037 |
| Strict | 0.7891 | 0.7991 |

The raw outliers hurt logistic regression more visibly than boosting. The selected boosting model stays near AUROC 0.80 under all profiles, which supports the robustness of the headline result. Strict filtering removes more rows without improving performance, so the current cleaning profile is a reasonable balance between clinical plausibility and data retention.

## Calibration and Interpretability

The Brier score for the selected model is 0.1795 on the held-out test set, and calibration bins are included in the public notebook. Calibration matters because a cardiovascular risk model is not useful only as a ranker; risk estimates should also be inspected as probabilities.

The transparent logistic baseline identifies systolic BP, age, cholesterol, and diastolic BP as major standardized effects. The selected model's permutation importance tells a similar story: the model is mostly using recognizable cardiovascular risk factors, especially systolic BP, age, and cholesterol.

These interpretations are predictive associations, not causal claims. The project does not estimate treatment effects or prove that changing a feature would change individual risk.

## Error Analysis

The selected model's held-out confusion counts are:

| Error type | Rows |
|---|---:|
| TN | 6,782 |
| FP | 1,885 |
| FN | 2,651 |
| TP | 5,834 |

The failures are clinically intuitive but important:

- False positives look high-risk: mean age 56.7, mean systolic BP 133.4, mean BMI 29.1, and mean cholesterol category 1.59.
- False negatives look more borderline: mean systolic BP 118.1 and mean cholesterol category 1.17.
- In the `<120` systolic BP band, false-negative rate among positives is 0.8596.
- In the `>=140` systolic BP band, the model predicts positive for every held-out case, giving zero false negatives but false-positive rate 1.0000 among the few actual negatives.
- Cholesterol category `3` has false-positive rate 0.8508 among negatives.

This is the central limitation story. The model learns recognizable risk structure, but this also creates asymmetric behavior: it can miss lower-BP positives and overcall high-risk-looking negatives.

## What Did Not Work

ECG modeling is not used as a headline result because the file schema and label semantics are unclear. Using it without validation would make the submission look more complex but less trustworthy.

The small heart dataset gives strong baseline performance, but the sample size is only 918 rows. We treat it as a comparison dataset, not as the core evidence base.

More complex tabular models only modestly outperform logistic regression. This supports the decision to focus the submission on data quality, calibration, and error analysis instead of claiming a major modeling breakthrough.

Strict cleaning does not improve performance. Removing more data is not automatically better; transparent sensitivity analysis is more credible than aggressive filtering.

## Limitations

- Public datasets may not represent real deployment populations.
- The targets are dataset-specific and may not match clinical outcome definitions.
- Measurement artifacts and unverified data-collection conditions remain possible.
- Subgroup analyses are descriptive and limited by available variables.
- Calibration is evaluated internally, not on an external clinical cohort.
- Predictive associations are not causal effects.
- The project is not a diagnostic system and should not be used for clinical decisions.

## Reproducibility

Core commands:

```bash
make setup
make all
make check
make submission-check
```

Preferred public notebook:

- `notebooks/02_final_kaggle_notebook.ipynb`

Working reproducibility notebook:

- `notebooks/01_eda_and_baseline.ipynb`

Important generated evidence:

- `outputs/tables/model_comparison.csv`
- `outputs/tables/cross_validation_summary.csv`
- `outputs/tables/cleaning_sensitivity_metrics.csv`
- `outputs/tables/error_analysis_summary.csv`
- `outputs/tables/error_analysis_by_group.csv`
- `outputs/figures/model_comparison_auroc.png`
- `outputs/figures/cleaning_sensitivity_auroc.png`
- `outputs/figures/calibration_curve.png`
- `outputs/figures/feature_importance.png`
- `outputs/figures/error_type_by_bp_band.png`

## Recommended Figure Set

Use seven figures if Kaggle space allows:

1. `outputs/figures/cardio_systolic_bp_raw_vs_clean.png`
2. `outputs/figures/cardio_target_by_bp_band.png`
3. `outputs/figures/cleaning_sensitivity_auroc.png`
4. `outputs/figures/model_comparison_auroc.png`
5. `outputs/figures/calibration_curve.png`
6. `outputs/figures/feature_importance.png`
7. `outputs/figures/error_type_by_bp_band.png`

## Claim-to-Evidence Map

| Claim | Evidence |
|---|---|
| The primary dataset is nearly balanced and large enough for stable tabular modeling. | `outputs/tables/data_audit.json`, `research/data_audit.md` |
| Plausibility cleaning removes a small, transparent subset. | `outputs/tables/cardio_cleaning_impact.csv`, `outputs/figures/cardio_cleaning_flow.png` |
| Blood pressure has strong target structure. | `outputs/tables/cardio_target_by_bp_band.csv`, `outputs/figures/cardio_target_by_bp_band.png` |
| Boosting is the selected model but only modestly beats logistic regression. | `outputs/tables/model_comparison.csv`, `outputs/figures/model_comparison_auroc.png` |
| Headline performance is not fragile to one cleaning profile. | `outputs/tables/cleaning_sensitivity_metrics.csv`, `outputs/figures/cleaning_sensitivity_auroc.png` |
| The model has meaningful asymmetric error modes. | `outputs/tables/error_analysis_by_group.csv`, `outputs/figures/error_type_by_bp_band.png` |
| ECG is not yet suitable for headline modeling. | `outputs/tables/ecg_schema_audit.json`, `research/data_audit.md` |

## AI Usage Disclosure

Generative AI tools were used to support code scaffolding, reproducibility setup, documentation structure, visualization planning, and internal research-note drafting. AI tools were not used as the core source of the research idea or main hypothesis. The final written submission, scientific interpretation, and claims must be reviewed and authored by the team before submission.

## Final Team Review Tasks

- Rewrite the final Kaggle prose in the team's own voice.
- Confirm all numbers against the final generated artifacts.
- Choose the final figure set and upload/render it in Kaggle.
- Verify raw-data access path in the public notebook.
- Confirm that no clinical deployment claim is made.
- Adapt the AI usage disclosure to the team's actual workflow.
- Notify Hack4Health organizers before broader public publication if required.
