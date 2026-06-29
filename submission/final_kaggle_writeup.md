# From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

## A data-quality-first Byte2Beat workflow where plausibility checks, calibration, and failure-mode analysis matter as much as AUROC

Author: Yaroslav Kholmirzayev

Contact: yaric.kholm@gmail.com

## Executive Summary

This project treats cardiovascular risk prediction as both a modeling problem and a data-quality problem. Public biomedical datasets are useful for learning and prototyping, but they can contain implausible measurements, missing-like values, unclear preprocessing history, and schema ambiguity. A model score is therefore not enough: a credible cardiovascular AI workflow also needs source audit, transparent cleaning, calibration, and error analysis.

The main analysis uses the 70,000-row cardiac tabular dataset with the binary `cardio` target. A transparent plausibility filter removes 1,395 rows, or 1.99 percent of the data, mostly due to blood-pressure and body-measurement anomalies. The selected histogram gradient boosting model reaches held-out AUROC 0.8037, AUPRC 0.7892, accuracy 0.7355, and Brier score 0.1795. Five-fold cross-validation gives AUROC 0.8013 +/- 0.0025.

The main result is not that a complex model dramatically outperforms every simple baseline. It does not. Logistic regression reaches AUROC 0.7931 and remains a useful transparent reference model. The stronger contribution is the reliability story: the selected model learns recognizable cardiovascular patterns, but it also misses many lower-BP positives and overcalls some high-BP or high-cholesterol negatives. This makes the project an educational, reproducible risk-modeling case study, not a clinical decision tool.

## Problem Framing

Cardiovascular AI is often presented as a pure prediction problem. In practice, the credibility of a biomedical model depends on what happens before and after fitting: source audit, measurement plausibility, missingness handling, split design, calibration, subgroup reliability, and cautious interpretation.

The guiding question for this work is:

> Can a public cardiovascular dataset support a useful and interpretable risk-modeling workflow while still exposing where the model is brittle?

This project is deliberately not a leaderboard-only submission. AUROC is reported, but it is not treated as sufficient evidence. The workflow is designed to answer three questions:

1. Are the source data plausible enough to model?
2. Is the headline model stable under reasonable cleaning choices?
3. Where does the selected model fail?

## Data Sources

The primary dataset is `cardio_base.csv`, a 70,000-row tabular cardiovascular dataset. It includes demographic variables, body measurements, blood pressure, cholesterol, glucose, lifestyle indicators, and the binary `cardio` target. The target is nearly balanced: 35,021 negative and 34,979 positive rows.

Two additional datasets were audited:

- `heart_processed.csv`: a 918-row heart-disease dataset with one-hot encoded clinical features and a `HeartDisease` target.
- `ecg_timeseries.csv`: a large ECG-like table with 528 rows and 123,995 columns.

The cardiac dataset is used for the headline model. The heart dataset is treated as a small comparison source. The ECG file is intentionally gated out of the headline result because its row semantics, labels, and schema need validation; the audit found 36,441 duplicate non-empty header names.

This submission is for educational and research analysis only. It is not a diagnostic system, treatment recommendation, medical device, or clinical decision-support tool.

## Data Audit

The cardiac base file has no missing values in the initial audit, but it contains physiologically implausible measurements:

- `ap_hi <= 0`: 7 rows.
- `ap_lo <= 0`: 22 rows.
- `ap_hi > 250`: 40 rows.
- `ap_lo > 200`: 953 rows.
- `ap_lo > ap_hi`: 1,234 rows.
- Height and weight ranges also suggest body-measurement outliers.

The processed cardiac file still contains blood-pressure anomalies, so the base file is used as the canonical input and cleaned transparently. The heart dataset has 172 rows where `Cholesterol == 0`, which behaves like missingness rather than a valid clinical measurement and is associated with the target.

## Cleaning Strategy

The primary cardiac plausibility profile uses the following rules:

- Height between 120 and 220 cm.
- Weight between 30 and 250 kg.
- BMI between 10 and 80.
- Systolic BP between 80 and 250.
- Diastolic BP between 40 and 150.
- Diastolic BP must not exceed systolic BP.

This removes 1,395 of 70,000 rows. The target rate changes from 0.4997 to 0.4947, so the cleaning process removes a small and transparent subset rather than redefining the dataset.

Cleaning is also tested as a sensitivity question. Four profiles are compared:

| Profile | Rows | Removed fraction | Target rate |
|---|---:|---:|---:|
| Raw | 70,000 | 0.0000 | 0.4997 |
| Lenient | 68,644 | 0.0194 | 0.4947 |
| Current | 68,605 | 0.0199 | 0.4947 |
| Strict | 68,362 | 0.0234 | 0.4950 |

This makes the cleaning decision explicit and testable.

## Exploratory Findings

The cleaned cardiac dataset shows strong cardiovascular structure. Cardio-positive rate rises sharply by systolic BP band:

| Systolic BP band | Cardio-positive rate |
|---|---:|
| `<120` | 0.2305 |
| `120-129` | 0.3560 |
| `130-139` | 0.5985 |
| `>=140` | 0.8370 |

This validates that the target aligns with recognizable cardiovascular risk patterns. It also foreshadows an important limitation: if blood pressure dominates the signal, the model may miss positives whose measured BP appears low and overcall negatives whose risk factors look high.

## Modeling Methods

The project compares:

- Dummy prior baseline.
- Logistic regression.
- Depth-4 decision tree.
- Random forest.
- Histogram gradient boosting.

Evaluation uses a fixed stratified held-out test split and 5-fold stratified cross-validation. Metrics include AUROC, AUPRC, accuracy, F1, Brier score, log loss, sensitivity, specificity, calibration bins, and subgroup/error analysis.

Histogram gradient boosting is selected because it has the strongest held-out AUROC and AUPRC while remaining stable across cleaning profiles. Logistic regression is retained as the transparent baseline and interpretability anchor.

## Main Results

On the current cleaned cardiac dataset:

| Model | Test AUROC | Test AUPRC | Accuracy | Brier |
|---|---:|---:|---:|---:|
| Dummy prior | 0.5000 | 0.4947 | 0.5053 | 0.2500 |
| Logistic regression | 0.7931 | 0.7750 | 0.7267 | 0.1863 |
| Decision tree depth 4 | 0.7876 | 0.7598 | 0.7296 | 0.1844 |
| Random forest | 0.8024 | 0.7875 | 0.7355 | 0.1801 |
| Histogram gradient boosting | 0.8037 | 0.7892 | 0.7355 | 0.1795 |

The selected model has 5-fold CV AUROC 0.8013 +/- 0.0025. Random forest is nearly tied, and logistic regression is only about 0.01 AUROC behind the selected model. This supports a conservative interpretation: the project is mainly about data quality and reliability, not about a dramatic model-complexity breakthrough.

## Cleaning Sensitivity

Held-out AUROC by cleaning profile:

| Cleaning profile | Logistic regression | HistGradientBoosting |
|---|---:|---:|
| Raw | 0.7776 | 0.8004 |
| Lenient | 0.7917 | 0.8025 |
| Current | 0.7931 | 0.8037 |
| Strict | 0.7891 | 0.7991 |

Raw implausible values hurt logistic regression more visibly than boosting. The selected boosting model stays near AUROC 0.80 across profiles, so the headline result is not fragile to a single threshold set. Strict filtering removes more rows without improving performance, which argues against aggressive deletion.

## Calibration and Interpretability

The selected model's held-out Brier score is 0.1795, and calibration bins are included in the public notebook. Calibration matters because a cardiovascular risk model should not only rank cases; predicted probabilities also need inspection.

The logistic baseline identifies systolic BP, age, cholesterol, and diastolic BP as major standardized effects. The selected model's permutation importance tells a similar story: systolic BP, age, cholesterol, and related body measurements dominate predictive signal.

These are predictive associations, not causal effects. This project does not estimate treatment effects or claim that changing one feature would change individual risk.

## Error Analysis

The selected model's held-out confusion counts are:

| Error type | Rows |
|---|---:|
| TN | 6,782 |
| FP | 1,885 |
| FN | 2,651 |
| TP | 5,834 |

The errors are clinically intuitive but important:

- False positives look high-risk: mean age 56.7, mean systolic BP 133.4, mean BMI 29.1, and mean cholesterol category 1.59.
- False negatives look more borderline: mean systolic BP 118.1 and mean cholesterol category 1.17.
- In the `<120` systolic BP band, false-negative rate among positives is 0.8596.
- In the `>=140` systolic BP band, the model predicts positive for every held-out case, giving zero false negatives but false-positive rate 1.0000 among the few actual negatives.
- Cholesterol category `3` has false-positive rate 0.8508 among negatives.

This is the central limitation. The model learns recognizable risk structure, but that same structure creates asymmetric behavior: lower-BP positives can be missed, while high-risk-looking negatives can be overcalled.

## What Did Not Work

ECG modeling is not included in the headline result because the file schema and label semantics are unclear. Using it without validation would add complexity without improving trust.

The small heart dataset gives strong baseline performance, but with only 918 rows it is better treated as a comparison source than as a primary evidence base.

More complex models only modestly outperform logistic regression. The final story is therefore not "deep complexity wins"; it is "transparent biomedical ML needs audit, calibration, and error analysis."

Strict cleaning does not improve performance. Removing more data is not automatically better.

## Limitations

- Public datasets may not represent real deployment populations.
- Target definitions are dataset-specific.
- Measurement artifacts and unverified collection conditions may remain.
- Subgroup analyses are descriptive and limited by available variables.
- Calibration is evaluated internally, not on an external clinical cohort.
- Predictive associations are not causal effects.
- The model is not suitable for diagnosis, treatment decisions, or patient-level deployment.

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

Key evidence files:

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

1. `outputs/figures/cardio_systolic_bp_raw_vs_clean.png`
2. `outputs/figures/cardio_target_by_bp_band.png`
3. `outputs/figures/cleaning_sensitivity_auroc.png`
4. `outputs/figures/model_comparison_auroc.png`
5. `outputs/figures/calibration_curve.png`
6. `outputs/figures/feature_importance.png`
7. `outputs/figures/error_type_by_bp_band.png`

## AI Usage Disclosure

Generative AI tools were used to support code scaffolding, reproducibility setup, documentation structure, visualization planning, and internal research-note drafting. AI tools were not used as the core source of the research idea or main hypothesis. The author remains responsible for the research framing, interpretation, written submission, and final claims.
