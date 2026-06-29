# Kaggle Writeup Draft

## Title

Data Quality-Aware Cardiovascular Risk Modeling

## Subtitle

An interpretable machine-learning workflow showing how plausibility checks, calibration, and subgroup analysis change cardiovascular risk prediction.

## Problem Framing

Cardiovascular risk prediction is often presented as a modeling problem, but public biomedical datasets frequently contain implausible measurements, missing-like values, and uncertain provenance. In this project, we treat data quality as part of the cardiovascular AI problem rather than a preprocessing footnote.

Our goal is to build a reproducible and interpretable risk-modeling pipeline using the Byte2Beat tabular datasets, then evaluate not only predictive performance but also calibration, subgroup reliability, and failure modes.

## Data

Primary dataset:

- `cardio_base.csv`: 70,000 rows with demographic, body measurement, blood pressure, cholesterol/glucose, lifestyle, and `cardio` target fields.

Comparison dataset:

- `heart_processed.csv`: 918 rows with heart-disease target and one-hot encoded clinical features.

ECG dataset:

- `ecg_timeseries.csv`: large ECG-like table. It is kept as an extension until row semantics and labels are validated.

## Data Audit

Key findings:

- The cardiac dataset is balanced but contains implausible blood-pressure and body-measurement values.
- The processed cardiac file still contains blood-pressure anomalies, so the base file plus transparent cleaning is preferred.
- The heart dataset has `Cholesterol == 0` in 172 of 918 rows. This behaves like missingness and is target-associated.
- The ECG file is wide and heavy, with unclear schema; it should not anchor the main project unless validated.

## Cleaning

Initial cardiac plausibility rules:

- Height 120-220 cm.
- Weight 30-250 kg.
- BMI 10-80.
- Systolic BP 80-250.
- Diastolic BP 40-150.
- Diastolic BP not greater than systolic BP.

This removes 1,395 of 70,000 rows, or 1.99%.

We also run a sensitivity analysis across four profiles:

- `raw`: no plausibility filtering.
- `lenient`: broad plausibility rules.
- `current`: primary rules used in the main model.
- `strict`: stricter thresholds for robustness checking.

The current profile is not treated as the only possible truth; it is tested against neighboring choices.

## EDA Findings

After plausibility cleaning, observed cardio-positive rate rises sharply by systolic BP band:

- `<120`: 23.0%.
- `120-129`: 35.6%.
- `130-139`: 59.9%.
- `>=140`: 83.7%.

This confirms that the target aligns with known cardiovascular risk structure, while also making it clear that blood pressure dominates much of the available signal.

## Methods

Models:

- Dummy prior baseline.
- Logistic regression.
- Depth-4 decision tree.
- Random forest.
- Histogram gradient boosting.

Evaluation:

- Fixed stratified held-out test split.
- 5-fold stratified cross-validation.
- AUROC, AUPRC, accuracy, F1, Brier score, log loss, sensitivity, specificity.
- Calibration bins and curve.
- Subgroup metrics by BP band, age band, gender coding, and cholesterol category.

## Current Results

On the cleaned cardiac dataset, the strongest current model is histogram gradient boosting:

- Held-out test AUROC: 0.8037.
- Held-out test AUPRC: 0.7892.
- Held-out test accuracy: 0.7355.
- Held-out test Brier score: 0.1795.
- 5-fold CV AUROC: 0.8013 +/- 0.0025.

Random forest is nearly tied, while logistic regression is slightly weaker but more transparent:

- Random forest test AUROC: 0.8024.
- Logistic regression test AUROC: 0.7931.

Cleaning sensitivity:

- Raw logistic regression AUROC: 0.7776.
- Current logistic regression AUROC: 0.7931.
- Raw histogram gradient boosting AUROC: 0.8004.
- Current histogram gradient boosting AUROC: 0.8037.
- Strict histogram gradient boosting AUROC: 0.7991.

Interpretation: implausible raw values hurt the linear model more than the tree-based model. The selected boosting model remains stable around AUROC 0.80 across cleaning profiles, so the headline result does not depend on one fragile threshold set.

## Interpretability

The first logistic baseline identified systolic BP, age, cholesterol, and diastolic BP as the largest standardized effects. This is clinically plausible and supports the project narrative that the model is learning recognizable cardiovascular risk structure.

The final interpretation should compare:

- Logistic coefficients.
- Permutation importance from the selected model.
- Subgroup reliability and calibration.

## Error Analysis

The selected cardiac model has asymmetric errors:

- True negatives have lower mean age, systolic BP, BMI, and cholesterol.
- False positives look clinically high-risk: mean age 56.7, mean systolic BP 133.4, mean BMI 29.1, mean cholesterol category 1.59.
- False negatives look more borderline: mean systolic BP 118.1 and mean cholesterol category 1.17.
- In the `<120` systolic BP band, false-negative rate among positives is 0.8596.
- In the `>=140` systolic BP band, the model predicts positive for every held-out case, giving zero false negatives but a false-positive rate of 1.0000 among the few actual negatives.

This is a useful limitation: the model learns recognizable cardiovascular risk structure, but it can miss lower-BP positives and overcall very high-BP negatives.

## What Did Not Work Yet

- ECG modeling is not included in the headline result because the schema and labels are not yet validated.
- The small heart dataset gives high AUROC, but this should be treated as a high-variance comparison rather than a primary claim.
- More complex models improve over logistic regression, but the improvement is modest; the final story should not be a model-complexity story.
- Strict cleaning does not improve performance, suggesting that removing more rows is not automatically better.
- Error analysis shows the model leans heavily on blood pressure and cholesterol, producing asymmetric subgroup errors.

## Limitations

- Public datasets may not represent real deployment populations.
- The target definitions are dataset-specific.
- Measurements may include artifacts and unverified collection conditions.
- Predictive associations are not causal effects.
- The model is not a clinical device and should not be used for diagnosis or treatment decisions.

## Reproducibility

Core commands:

```bash
.venv/bin/python scripts/profile_data.py
.venv/bin/python scripts/eda_tabular.py
.venv/bin/python scripts/generate_eda_figures.py
.venv/bin/python scripts/baseline_tabular_numpy.py
.venv/bin/python scripts/model_comparison.py
```

## AI Usage Disclosure

Draft: AI assistance was used for coding support, project organization, documentation scaffolding, and visualization planning. The team remains responsible for the research question, interpretation, written submission, and final claims.
