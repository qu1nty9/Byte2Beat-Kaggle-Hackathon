# Manuscript Outline

## Working Title

Data Quality-Aware Cardiovascular Risk Modeling Across Public Tabular Health Datasets

## Abstract Skeleton

Background: Public cardiovascular datasets are useful for education and prototyping but often contain measurement artifacts and missing-like values.

Objective: Evaluate how plausibility checks, calibration, and subgroup analysis affect interpretable cardiovascular risk prediction.

Methods: Use the Byte2Beat cardiac and heart datasets; audit data quality; define transparent cleaning rules; compare logistic regression, decision tree, random forest, and histogram gradient boosting; evaluate performance, calibration, and subgroup reliability.

Results: Current foundation result on the cleaned cardiac dataset shows histogram gradient boosting test AUROC 0.8037 and 5-fold CV AUROC 0.8013 +/- 0.0025.

Sensitivity: Cleaning-profile analysis shows histogram gradient boosting remains near AUROC 0.80 across raw, lenient, current, and strict profiles, while logistic regression is more sensitive to raw implausible values.

Error analysis: False negatives concentrate among lower-BP positives, while false positives are more common among high-risk-looking negatives, especially high systolic BP and high cholesterol groups.

Conclusion: Simple cardiovascular risk factors contain substantial predictive signal, but a credible biomedical ML workflow must foreground data quality, calibration, and limitations.

## Sections

1. Introduction.
2. Related Work.
3. Data Sources.
4. Data Quality Audit.
5. Preprocessing and Plausibility Checks.
6. Modeling Methods.
7. Evaluation Protocol.
8. Results.
9. Calibration and Subgroup Reliability.
10. Interpretability.
11. Discussion.
12. Limitations.
13. Reproducibility and Data Availability.
14. Ethics and AI Assistance Disclosure.

## Preprint Readiness Checklist

- Verify all dataset licenses and citation requirements.
- Confirm publication coordination with Hack4Health organizers.
- Add related work and clinical context.
- Add robustness checks for cleaning thresholds.
- Add repeated CV or bootstrap intervals for the small heart dataset.
- Ensure GitHub repository is clean and reproducible.
