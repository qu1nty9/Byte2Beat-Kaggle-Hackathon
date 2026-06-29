# Publication Readiness Plan

Status: planning document for a possible arXiv preprint, blog post, or journal-style manuscript. Do not publish externally until the team has checked Hack4Health notification requirements, dataset licenses, and author approvals.

## Current Status

Status: not publication-ready yet.

The project is close to a strong Kaggle submission because it has a reproducible pipeline, a public notebook, generated figures, sensitivity analysis, calibration reporting, a claims ledger, and error analysis. A publication requires a higher evidence standard: verified dataset provenance, related work, stronger external-validity discussion, and explicit publication coordination with Hack4Health organizers.

## Proposed Manuscript Positioning

Working title:

> Data Quality-Aware Cardiovascular Risk Modeling Across Public Tabular Health Datasets

Core contribution:

> A reproducible case study showing that cardiovascular tabular models can reach moderate discrimination, but credible reporting depends on source audit, plausibility checks, calibration, subgroup error analysis, and explicit limits on clinical interpretation.

This should be positioned as an educational and methodological case study, not as a clinical model validation paper.

## Candidate Contribution

Working contribution:

> A reproducible, data-quality-aware workflow for public cardiovascular risk modeling that combines plausibility checks, cleaning sensitivity, calibration, interpretability, and subgroup error analysis.

This contribution is methodological and educational. It should not be framed as a new clinical risk score or a deployable medical device.

## Best-Fit Publication Formats

| Venue type | Fit | Requirements before submission |
|---|---|---|
| Kaggle Writeup | Strong | Final team-authored prose, public notebook, figures, AI disclosure. |
| Project blog / GitHub article | Strong | Clear visuals, reproducible commands, cautious medical framing. |
| arXiv preprint | Moderate | Related work, stronger citation layer, author approval, license checks. |
| Student workshop / hackathon proceedings | Strong | Short methods, reproducibility, limitations, figures. |
| Peer-reviewed journal | Weak to moderate | External validation, deeper clinical context, risk-of-bias assessment, stronger dataset provenance. |

## Must-Complete Before Public Publication Beyond Kaggle

- Notify Hack4Health organizers before public publication if required by the competition rules.
- Verify dataset licenses, citation requirements, and allowed redistribution boundaries.
- Confirm that no raw restricted datasets are committed or exposed.
- Add a related-work section based on verified primary sources.
- Add a data availability statement explaining how readers can access raw inputs.
- Add a code availability statement pointing to the public repository and commit or release.
- Add an ethics and limitations section that states the model is not clinical advice.
- Ensure final text is team-authored and AI assistance is disclosed accurately.

## Reporting Guideline Alignment

Use these as reporting anchors, not as claims of clinical readiness:

- TRIPOD+AI: relevant because this is a prediction-modeling study using regression and machine-learning methods.
- PROBAST / PROBAST+AI: relevant if the manuscript makes risk-of-bias or applicability claims.
- STROBE: relevant if the manuscript is framed as observational secondary-data analysis.
- DECIDE-AI: not directly applicable now because this is not an early clinical evaluation of an AI decision-support system, but it is useful for future translation planning.
- CONSORT-AI / SPIRIT-AI: not applicable now because this is not a randomized clinical trial or trial protocol.

Reference seed links:

- TRIPOD+AI statement: https://www.bmj.com/content/385/bmj-2023-078378
- Original TRIPOD statement: https://www.acpjournals.org/doi/10.7326/M14-0697
- DECIDE-AI reporting guideline: https://www.nature.com/articles/s41591-022-01772-9
- CONSORT-AI extension: https://www.nature.com/articles/s41591-020-1034-x
- STROBE statement: https://www.strobe-statement.org/

## Evidence Already Available

| Evidence type | Artifact |
|---|---|
| Data audit | `research/data_audit.md`, `outputs/tables/data_audit.json` |
| Cleaning sensitivity | `outputs/tables/cleaning_sensitivity_metrics.csv`, `outputs/figures/cleaning_sensitivity_auroc.png` |
| Model comparison | `outputs/tables/model_comparison.csv`, `outputs/tables/cross_validation_summary.csv` |
| Calibration | `outputs/tables/cardio_clean_calibration_bins.csv`, `outputs/figures/calibration_curve.png` |
| Interpretability | `outputs/tables/feature_importance.csv`, `outputs/tables/cardio_logreg_coefficients.csv`, `outputs/figures/feature_importance.png` |
| Error analysis | `research/error_analysis.md`, `outputs/tables/error_analysis_by_group.csv`, `outputs/figures/error_type_by_bp_band.png` |
| Claim guardrails | `submission/claims_ledger.md` |
| Reproducibility | `Makefile`, `scripts/`, `notebooks/02_final_kaggle_notebook.ipynb` |
| AI disclosure | `research/ai_usage_disclosure.md` |

## Manuscript Outline

### Abstract

Background: Public cardiovascular datasets are widely used for education and prototyping, but they may contain measurement artifacts and unclear preprocessing histories.

Objective: Evaluate how plausibility checks, model choice, calibration, and subgroup error analysis affect cardiovascular risk prediction in public tabular data.

Methods: Audit Byte2Beat tabular datasets, define transparent plausibility filters, compare dummy baseline, logistic regression, decision tree, random forest, and histogram gradient boosting, and evaluate discrimination, calibration, sensitivity to cleaning thresholds, and error patterns.

Results: The selected histogram gradient boosting model reaches held-out AUROC 0.8037, AUPRC 0.7892, accuracy 0.7355, and Brier score 0.1795 on the cleaned cardiac dataset. 5-fold CV AUROC is 0.8013 +/- 0.0025. Performance remains near AUROC 0.80 across cleaning profiles, while logistic regression is more sensitive to raw implausible values.

Conclusion: Public cardiovascular tabular data can support moderate predictive performance, but responsible reporting should foreground data quality, calibration, and failure modes rather than only model score.

### Introduction

- Public biomedical datasets are common in education and prototyping.
- Cardiovascular risk prediction is familiar enough for interpretable sanity checks.
- Public datasets can contain physiologic outliers, missing-like values, and unclear preprocessing.
- The manuscript contribution is a transparent workflow, not a clinical deployment claim.

### Related Work

Cover:

- Clinical prediction model reporting: TRIPOD and TRIPOD+AI.
- Risk-of-bias thinking: PROBAST and PROBAST+AI.
- Observational reporting: STROBE.
- Clinical AI translation: DECIDE-AI and CONSORT-AI as future-stage guidance.
- Data quality and dataset shift in health AI.
- Calibration and subgroup reliability in medical prediction.

Do not add unverified citations. Use primary sources or official reporting guidelines where possible.

### Methods

Include:

- Dataset provenance and local paths.
- Inclusion/exclusion rules.
- Target definition and unit of analysis.
- Cleaning profiles: raw, lenient, current, strict.
- Feature definitions, including age conversion and BMI.
- Split strategy and leakage controls.
- Model classes and hyperparameter summary.
- Metrics and why each matters.
- Calibration method.
- Error and subgroup analysis definitions.

### Results

Minimum tables:

1. Data audit summary.
2. Cleaning profile comparison.
3. Model comparison.
4. Cross-validation summary.
5. Error analysis by subgroup.

Minimum figures:

1. Raw vs cleaned systolic BP.
2. Target rate by systolic BP band.
3. Cleaning sensitivity AUROC.
4. Model comparison AUROC.
5. Calibration curve.
6. Feature importance.
7. Error type by BP band.

### Discussion

Key points:

- The selected model is moderately discriminative, not clinically validated.
- Logistic regression remains competitive and interpretable.
- Plausibility cleaning improves validity and helps linear modeling, but the boosting headline is robust across profiles.
- Error modes show dependence on familiar risk factors.
- ECG modeling should wait until schema and labels are validated.

### Limitations

Must include:

- No external clinical validation.
- Public dataset representativeness is unknown.
- Dataset-specific target definition.
- No causal inference.
- Limited protected-attribute analysis.
- Calibration is internal only.
- ECG source not modeled due unresolved schema.
- No deployment, diagnosis, or treatment recommendation.

### Ethics and Governance

Include:

- Educational/research-only use.
- No clinical-use claim.
- Dataset provenance and license check before publication.
- AI assistance disclosure.
- Hack4Health organizer notification before public release beyond Kaggle, if required.

### Data and Code Availability

Draft statement:

> Code, notebooks, generated tables, and generated figures are available in the project repository. Raw datasets are not redistributed in the repository unless the competition license explicitly permits redistribution; users should access raw data through the original Byte2Beat/Hack4Health or Kaggle source.

## Work Needed Before arXiv

- Verify all dataset licenses and permitted redistribution terms.
- Add full references in BibTeX or CSL JSON.
- Add a related-work section with at least 10-15 sources.
- Re-run `make all`, `make check`, and `make submission-check` from a clean clone or fresh environment.
- Add random seed and software-version table.
- Consider bootstrap confidence intervals for selected metrics.
- Add external validation only if a clearly compatible public dataset is identified.
- Confirm author list, author contributions, and acknowledgments.
- Notify Hack4Health organizers before public preprint or blog release if required by the rules.

## Robustness Work Needed

- Add repeated cross-validation or bootstrap confidence intervals for the small `heart_processed.csv` comparison.
- Decide whether the heart dataset remains an appendix or a secondary result.
- Add a stricter written rationale for plausibility thresholds.
- Consider a compact threshold analysis for clinical operating points, clearly marked as illustrative.
- If ECG is included, validate row semantics, labels, and linkage before any supervised claim.

## Work Needed Before Journal Submission

- Add a formal TRIPOD+AI checklist.
- Add a PROBAST/PROBAST+AI-style risk-of-bias table.
- Strengthen clinical context with cardiology/public-health references.
- Add external validation or clearly frame the study as internal validation only.
- Add a fuller missingness and measurement-artifact analysis.
- Create a data dictionary for every modeling feature.
- Add confidence intervals for major metrics.
- Add a reproducibility appendix with exact commands and environment details.

## Manuscript Guardrails

Allowed:

- "Predictive association."
- "Educational/research workflow."
- "Public dataset limitations."
- "Data-quality-aware modeling."
- "Held-out and cross-validation performance on this dataset."

Avoid:

- "Diagnosis."
- "Clinical decision support."
- "Patient-level deployment."
- "Causal effect."
- "Clinically validated."
- "Generalizes to real-world care."

## Preprint Abstract Checklist

- One sentence on why public cardiovascular ML needs data-quality checks.
- One sentence describing datasets and plausibility filtering.
- One sentence describing models and metrics.
- One sentence with the selected model's AUROC/AUPRC/Brier/CV result.
- One sentence on cleaning sensitivity.
- One sentence on asymmetric errors and limitations.
- One sentence stating educational/research status.

## Release Checklist

- `make all` passes from a clean working tree with raw data available locally.
- `make check` passes.
- `notebooks/02_final_kaggle_notebook.ipynb` is executed top-to-bottom.
- `submission/claims_ledger.md` matches the final writeup.
- `submission/kaggle_writeup_review_draft.md` has been reviewed and rewritten by the team.
- Repository README explains data access and reproducibility.
- A release tag or final commit hash is recorded in the writeup.
- Publication/visibility permission has been checked with organizers.

## Current Publication Decision

Best current path:

1. Submit Kaggle Writeup and public notebook.
2. Publish GitHub repository if judges can access it and rules allow it.
3. Prepare a blog-style article or arXiv preprint only after organizer notification and license review.
4. Treat journal submission as a later target after external validation and formal reporting checklists.
