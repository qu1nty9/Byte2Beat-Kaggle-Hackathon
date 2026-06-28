# Byte2Beat Ideal Project Plan

This is the canonical operating plan for the Byte2Beat project. It is written for execution first: every phase should produce concrete artifacts that can be used in the Kaggle Writeup, public notebook, GitHub repository, and possible article/preprint.

## 1. Project Thesis

### Working Title

Data Quality-Aware and Interpretable Cardiovascular Risk Modeling Across Public Tabular Health Datasets

### Core Research Question

How much predictive signal is available in simple cardiovascular risk factors after transparent clinical plausibility checks, and which risk-factor patterns remain stable across related cardiovascular datasets?

### One-Sentence Kaggle Pitch

We build an interpretable cardiovascular risk modeling pipeline that treats data quality as a first-class biomedical problem, showing how cleaning decisions, calibration, and subgroup analysis change model behavior.

### Why This Is the Lead Direction

- It directly fits the challenge: cardiovascular AI, risk assessment, interpretability, and medically relevant modeling.
- It is feasible with the provided data and does not depend on restricted external EHR access.
- It has a strong story for judges: not just "train a model", but "audit the data, prove the model is stable, explain where it fails".
- It can produce publishable components: data-quality audit, sensitivity analysis, calibration, subgroup reliability, and reproducible open workflow.
- It leaves room for an ECG extension, but does not make the project depend on an unclear 632 MB timeseries file.

## 2. Definition of an Ideal Project

The ideal version of this project satisfies four goals at the same time.

### Competition Goal

Score well on usefulness, informativeness, documentation quality, and novelty by delivering:

- A clear cardiovascular problem.
- A reproducible public notebook.
- Strong visuals and tables.
- Honest discussion of limitations and failed attempts.
- A medically cautious interpretation.
- Optional lightweight demo if time allows.

### Engineering Goal

Make the project rerunnable by another person:

- Raw data stays in `docs/` and is not modified.
- Scripts generate audit tables and model outputs.
- Notebooks call reusable code where possible.
- Dependencies are declared in `requirements.txt`.
- Generated outputs live under `outputs/`.

### Research Goal

Make claims that are defensible:

- No performance claims without a fixed split or cross-validation.
- No use of ECG labels until the ECG schema is validated.
- No silent deletion of clinically meaningful missing-like values.
- Cleaning rules must be justified and sensitivity-tested.
- Interpretability must be tied to model behavior, not decorative plots.

### Publication Goal

Structure the project so it can become:

- A Kaggle Writeup.
- A GitHub repository release.
- A blog/article.
- A preprint-style manuscript if the results are sufficiently rigorous.

Before public publication outside Kaggle/GitHub release, notify Hack4Health organizers as required by the rules.

## 3. Current Evidence Base

### Competition Documents

Local documents establish the required deliverables:

- Kaggle Writeup.
- Public notebook.
- Optional public product/demo link.
- Repository or equivalent with pipelines, model code, reproducibility scaffolding, documentation, and evaluation notes.
- AI usage disclosure.

The local documents do not provide a reliable absolute deadline in the extracted text, so all scheduling below is relative. Once the official deadline is confirmed, map these phases backward from submission time.

### Initial Data Facts

Cardiac dataset:

- `cardio_base.csv`: 70,000 rows, 13 columns.
- Target: `cardio`, nearly balanced.
- Main risks: invalid blood pressures, body-measurement outliers, base file uses age in days.
- Initial plausibility filter removes 1,395 rows, or 1.99%.
- Systolic BP bands show a strong target gradient after cleaning.

Heart attack dataset:

- `heart_processed.csv`: 918 rows, 16 columns.
- Target: `HeartDisease`.
- Main risks: small sample, `Cholesterol == 0` in 172 rows, one invalid resting BP.
- Zero cholesterol is target-associated and should be modeled or explained, not silently dropped.

ECG dataset:

- `ecg_timeseries.csv`: approximately 632 MB.
- 528 rows and roughly 124k columns.
- Schema and labels are not yet validated.
- Treat as an extension until provenance is understood.

### Initial Baseline

Dependency-light logistic regression in `scripts/baseline_tabular_numpy.py`:

- Cleaned cardiac test AUROC: 0.7974.
- Cleaned cardiac test accuracy: 0.7359.
- Heart test AUROC: 0.9411, but high-variance due to only 918 rows.

These are baselines, not final claims.

## 4. Operating Principles

### Research Discipline

- Every claim must trace to a source file, generated table, figure, or notebook cell.
- Negative results are kept and explained.
- Prefer simple, interpretable models before complex models.
- Treat calibration and subgroup performance as core metrics, not extras.
- State clearly that this is research/education, not clinical deployment.

### LLM-Wiki Workflow

- `docs/` is immutable raw source material.
- `research/` is the maintained knowledge base.
- `research/log.md` is append-only.
- `research/index.md` is updated when new important artifacts appear.
- New experiments update `research/baseline_results.md`, `research/data_audit.md`, or a new topic page.

### Code Workflow

- `scripts/` for repeatable command-line steps.
- `src/byte2beat/` for reusable project code.
- `notebooks/` for Kaggle-facing narrative.
- `outputs/tables/` for CSV/JSON tables.
- `outputs/figures/` for final visuals.
- `outputs/models/` for saved models if needed.

## 5. Project Architecture

### Canonical Inputs

- Main training input: `cardio_base.csv`.
- Comparison input: `heart_processed.csv`.
- Optional extension input: `ecg_timeseries.csv`.

### Canonical Outputs

Required:

- `outputs/tables/data_audit.json`.
- `outputs/tables/cardio_cleaning_impact.csv`.
- `outputs/tables/heart_cleaning_impact.csv`.
- `outputs/tables/baseline_metrics.csv`.
- `outputs/tables/model_comparison.csv`.
- `outputs/tables/calibration_summary.csv`.
- `outputs/tables/subgroup_metrics.csv`.
- `outputs/figures/` writeup-ready figures.
- `notebooks/01_eda_and_baseline.ipynb`.
- `notebooks/02_model_comparison_and_interpretability.ipynb`.
- Final Kaggle public notebook, either as a polished combined notebook or exported from the two notebooks.

Optional:

- `notebooks/03_ecg_schema_and_features.ipynb`.
- `app/` or `demo/` for a lightweight risk explanation demo.
- `paper/` for a manuscript-style draft.

## 6. Phase Plan

### Phase 0: Source Grounding and Workspace Setup

Status: first iteration completed.

Objectives:

- Understand rules, deliverables, and AI policy.
- Build repo structure.
- Create LLM-wiki pages.
- Run initial dataset audit.
- Produce a first baseline.

Completed artifacts:

- `AGENTS.md`.
- `README.md`.
- `research/source_inventory.md`.
- `research/data_audit.md`.
- `research/baseline_results.md`.
- `scripts/profile_data.py`.
- `scripts/eda_tabular.py`.
- `scripts/baseline_tabular_numpy.py`.

Quality gate:

- A new collaborator can understand the project direction by reading `README.md` and `research/project_plan.md`.

### Phase 1: EDA and Clinical Plausibility Cleaning

Objective:

Turn the data audit into a polished, evidence-backed story.

Tasks:

1. Confirm canonical cleaning rules for cardiac data:
   - Age conversion from days to years.
   - Height, weight, BMI plausibility.
   - Systolic and diastolic BP plausibility.
   - Diastolic BP not greater than systolic BP.
2. Confirm handling of heart dataset:
   - Keep `Cholesterol_zero` indicator.
   - Sensitivity run with observed cholesterol only.
   - Avoid overclaiming because the dataset is small.
3. Produce EDA tables:
   - Missingness and invalid-value table.
   - Target rate by BP band.
   - Target rate by age band.
   - Feature summary by target.
   - Exclusion counts by cleaning rule.
4. Produce first figures:
   - Target rate by systolic BP band.
   - Distribution of systolic/diastolic BP before and after cleaning.
   - Age and cholesterol distributions by target.
   - Cleaning flow diagram.

Artifacts:

- `outputs/tables/eda_summary.csv`.
- `outputs/tables/cleaning_rule_counts.csv`.
- `outputs/figures/cardio_target_by_bp_band.png`.
- `outputs/figures/cardio_cleaning_flow.png`.
- `notebooks/01_eda_and_baseline.ipynb`.

Quality gate:

- Every cleaning rule has a rationale, count removed, and sensitivity plan.

### Phase 2: Baseline and Model Comparison

Objective:

Establish trustworthy predictive baselines and compare model classes without making the work a leaderboard chase.

Models:

- Majority and simple heuristic baselines.
- Logistic regression.
- Decision tree.
- Random forest.
- Gradient boosting or histogram gradient boosting.
- Optional calibrated classifier wrappers.

Metrics:

- AUROC.
- AUPRC.
- Accuracy.
- Sensitivity.
- Specificity.
- F1.
- Brier score.
- Log loss.
- Calibration slope/intercept if implemented.

Tasks:

1. Use fixed train/validation/test split for the main narrative.
2. Add repeated cross-validation, especially for the 918-row heart dataset.
3. Compare raw vs cleaned cardiac inputs.
4. Compare full feature set vs clinically minimal feature set.
5. Save model comparison table.
6. Select final model based on performance, calibration, interpretability, and stability.

Artifacts:

- `scripts/model_comparison.py`.
- `outputs/tables/model_comparison.csv`.
- `outputs/tables/cross_validation_summary.csv`.
- `outputs/figures/roc_curves.png`.
- `outputs/figures/pr_curves.png`.
- `outputs/figures/model_comparison_barplot.png`.

Quality gate:

- The chosen final model must beat transparent baselines, be calibrated or calibration-assessed, and have stable performance across splits.

### Phase 3: Calibration, Error Analysis, and Subgroups

Objective:

Move from "the model predicts" to "we understand where it is reliable and where it fails".

Tasks:

1. Generate calibration curves and reliability bins.
2. Report Brier score and log loss for each model.
3. Analyze false positives and false negatives:
   - Age.
   - BP bands.
   - Cholesterol/glucose categories.
   - Sex/gender coding.
   - Smoking/activity.
4. Produce subgroup metrics:
   - Age bands.
   - Systolic BP bands.
   - Sex/gender groups.
   - Cholesterol categories.
5. Identify failure modes that should appear in the writeup.

Artifacts:

- `scripts/evaluate_subgroups.py`.
- `outputs/tables/calibration_summary.csv`.
- `outputs/tables/subgroup_metrics.csv`.
- `outputs/tables/error_analysis.csv`.
- `outputs/figures/calibration_curve.png`.
- `outputs/figures/subgroup_auroc.png`.
- `outputs/figures/error_profile.png`.

Quality gate:

- The writeup can explain not only performance, but also calibration and known failure modes.

### Phase 4: Interpretability

Objective:

Produce clinically meaningful explanations without overstating causality.

Tasks:

1. For logistic regression:
   - Standardized coefficients.
   - Direction and relative magnitude.
   - Odds-ratio style interpretation if useful.
2. For tree/boosting models:
   - Permutation importance.
   - Partial dependence or simple stratified plots.
   - Optional SHAP if dependency setup is stable.
3. Compare feature effects across datasets:
   - Which signs are stable?
   - Which features behave differently?
   - Which differences are likely dataset artifacts?
4. Write interpretation guardrails:
   - Predictive association is not causation.
   - Dataset labels and collection process limit clinical claims.

Artifacts:

- `outputs/tables/feature_importance.csv`.
- `outputs/tables/stability_of_feature_effects.csv`.
- `outputs/figures/feature_importance.png`.
- `outputs/figures/partial_dependence_bp_age.png`.

Quality gate:

- Interpretability section contains actionable insight and explicit cautions.

### Phase 5: ECG Extension Decision Gate

Objective:

Decide whether ECG strengthens the project or distracts from it.

Gate questions:

1. What is one row?
2. Are columns timepoints, leads, records, or flattened groups?
3. Are labels available?
4. Is there patient-level linkage to tabular data?
5. Can we create medically plausible features?
6. Can we validate enough to make supervised claims?

If answers are strong:

- Convert ECG to compact format.
- Extract signal features.
- Train ECG-only or ECG-feature model.
- Compare to tabular model.

If answers are weak:

- Use ECG only as an exploratory appendix.
- Do not include ECG model claims in final headline.

Artifacts:

- `scripts/profile_ecg_schema.py`.
- `notebooks/03_ecg_schema_and_features.ipynb`.
- `outputs/tables/ecg_schema_audit.csv`.
- `outputs/tables/ecg_feature_summary.csv`.

Quality gate:

- No ECG result appears in the final headline unless label provenance and row semantics are clear.

### Phase 6: Demo Layer

Objective:

Create an optional interactive artifact that improves communication without weakening research rigor.

Preferred demo:

- A simple risk-factor scenario explorer.
- Inputs: age, BP, cholesterol, glucose, smoking, activity, BMI.
- Outputs: model risk estimate, nearest BP band context, and explanation of uncertainty.

Rules:

- The demo must say it is educational/research only.
- It must not present itself as medical advice.
- It must show limitations and data provenance.

Artifacts:

- `demo/` or `app/`.
- Public link if deployment is easy.
- Screenshots for Kaggle Writeup if deployment is not worth the time.

Quality gate:

- Demo is optional. It should be skipped if it competes with model rigor or writeup quality.

### Phase 7: Kaggle Writeup and Public Notebook

Objective:

Package the project into a judge-friendly narrative.

Notebook structure:

1. Setup and reproducibility.
2. Data provenance.
3. Data audit.
4. Cleaning rules.
5. EDA.
6. Baselines.
7. Model comparison.
8. Calibration and subgroup analysis.
9. Interpretability.
10. Limitations.
11. Reproducibility checklist.

Writeup structure:

1. Title.
2. Subtitle.
3. Problem framing.
4. Why data quality matters in cardiovascular AI.
5. Data sources and ethics.
6. Methods.
7. Results.
8. Interpretability.
9. What did not work.
10. Limitations.
11. Societal impact.
12. Reproducibility.
13. AI usage disclosure.

Quality gate:

- The writeup reads like a coherent research story, not a dump of model scores.

### Phase 8: Article or Preprint Path

Objective:

Upgrade the Kaggle project into a publishable artifact if the final results warrant it.

Manuscript structure:

1. Abstract.
2. Introduction.
3. Related work.
4. Materials and methods.
5. Data-quality audit.
6. Modeling and validation.
7. Results.
8. Calibration and subgroup reliability.
9. Discussion.
10. Limitations.
11. Reproducibility and data availability.
12. Ethics and AI assistance disclosure.

Extra requirements before preprint:

- Confirm dataset licenses and citation requirements.
- Confirm competition publication process with organizers.
- Add stronger related work.
- Add robustness checks.
- Make code and outputs clean enough for public release.

Quality gate:

- Publish only if the work has a clear contribution beyond a hackathon notebook.

## 7. Success Criteria

### Minimum Viable Submission

- Public notebook.
- Kaggle Writeup.
- Clean EDA.
- Logistic regression baseline.
- One stronger model.
- Core figures.
- Limitations and AI disclosure.

### Strong Submission

- Everything in minimum viable submission.
- Cross-validation.
- Calibration analysis.
- Subgroup metrics.
- Raw vs cleaned sensitivity analysis.
- Interpretable feature effects.
- Polished repository and reproducibility instructions.

### Ideal Submission

- Everything in strong submission.
- Stable final model.
- Error analysis with meaningful failure modes.
- Optional ECG schema appendix or validated ECG feature extension.
- Optional educational demo.
- Manuscript-ready outline and figures.

## 8. Risk Register

### Risk: ECG Is Unclear or Unlabeled

Mitigation:

- Do not depend on ECG for the main project.
- Treat ECG as a gate-based extension.

### Risk: Heart Dataset Result Is Overfit

Mitigation:

- Use repeated cross-validation.
- Present as comparison/replication, not as primary proof.

### Risk: Cleaning Rules Look Arbitrary

Mitigation:

- Show counts removed by each rule.
- Add sensitivity analysis with raw, strict, and lenient cleaning.

### Risk: Model Scores Become the Whole Story

Mitigation:

- Keep data audit, calibration, interpretability, and failure modes central.

### Risk: AI Policy Conflict

Mitigation:

- Human team owns final research framing and written submission.
- Maintain AI usage disclosure.
- Use AI for code assistance, analysis scaffolding, and visualization support only.

### Risk: Publication Overclaiming

Mitigation:

- Avoid clinical deployment language.
- State educational/research status.
- Focus on methods and data-quality lessons.

## 9. Execution Cadence

### Every Work Session

1. Start from `research/index.md`.
2. Check `research/log.md` for last completed step.
3. Run or update scripts, not manual one-off transformations.
4. Save generated tables/figures.
5. Update the relevant research page.
6. Append to `research/log.md`.

### Every Modeling Session

1. Define the hypothesis.
2. Define target and input rows.
3. Define split.
4. Run baseline first.
5. Run improved model.
6. Save metrics.
7. Interpret failure modes.
8. Decide whether the result enters the final story.

### Every Writeup Session

1. Convert one result into one claim.
2. Attach the table/figure supporting it.
3. Add limitation.
4. Add reproducibility pointer.
5. Keep language clear and non-clinical.

## 10. Immediate Next Steps

### Next 24 Hours of Work

1. Install or confirm modeling/plotting dependencies in a project environment.
2. Create `notebooks/01_eda_and_baseline.ipynb`.
3. Convert existing audit and baseline results into narrative cells.
4. Generate first writeup-ready plots.
5. Add `scripts/model_comparison.py` with sklearn models if dependencies are available.

### Next 48-72 Hours of Work

1. Add cross-validation.
2. Add calibration curves.
3. Add subgroup metrics.
4. Add raw vs cleaned sensitivity analysis.
5. Draft the Kaggle Writeup skeleton.

### Before Submission

1. Re-run all scripts from a clean state.
2. Execute final public notebook top-to-bottom.
3. Verify all figures and tables are generated.
4. Confirm no private or oversized raw data is accidentally committed.
5. Finalize AI usage disclosure.
6. Check publication/visibility note with organizers if publishing beyond Kaggle.

## 11. Current Best Next Command Sequence

After dependencies are available:

```bash
python scripts/profile_data.py
python scripts/eda_tabular.py
python scripts/baseline_tabular_numpy.py
```

Then build:

```bash
notebooks/01_eda_and_baseline.ipynb
scripts/model_comparison.py
scripts/evaluate_subgroups.py
```

## 12. Final Narrative We Are Building Toward

The final project should say:

> In cardiovascular ML, simple risk-factor models can perform surprisingly well, but the real work is validating the data and understanding reliability. We show that transparent plausibility checks, calibration, and subgroup/error analysis produce a more trustworthy risk-modeling workflow than score-only modeling. The resulting model is not a clinical tool, but a reproducible demonstration of how biomedical AI projects should handle noisy public health data.

