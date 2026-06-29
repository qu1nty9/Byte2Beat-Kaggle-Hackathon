# Final Submission Checklist

## Kaggle Writeup

- [ ] Final text rewritten by the team, not copied directly from AI-generated scaffolding.
- [ ] Title and subtitle are concise.
- [ ] Problem framing is clear in the first paragraph.
- [ ] Data sources and provenance are described.
- [ ] Data audit includes anomalies and ECG caveat.
- [ ] Cleaning rules include counts removed.
- [ ] Sensitivity analysis explains why the result is not threshold-fragile.
- [ ] Main model result includes AUROC, AUPRC, Brier score, and CV result.
- [ ] Calibration is discussed, not only discrimination.
- [ ] Error analysis includes false positives and false negatives.
- [ ] Limitations are explicit and medically cautious.
- [ ] AI usage disclosure is included and accurate.

## Public Notebook

- [ ] Notebook runs top-to-bottom in Kaggle or a clean local environment.
- [ ] `notebooks/02_final_kaggle_notebook.ipynb` is the preferred public notebook unless the team chooses to publish the longer working notebook.
- [ ] All plots render.
- [ ] No private absolute paths remain.
- [ ] Raw data access path is documented.
- [ ] Notebook includes enough narrative for judges to follow.
- [ ] Notebook does not claim clinical readiness.

## Repository

- [ ] `README.md` explains quickstart.
- [ ] `requirements.txt` is current.
- [ ] Raw large datasets are not committed.
- [ ] Generated figures/tables needed for review are committed.
- [ ] `Makefile` targets work: `make all`, `make check`.
- [ ] GitHub repository is public or accessible to judges.

## Publication Path

- [ ] Decide whether this is Kaggle-only, blog, GitHub release, or preprint.
- [ ] Notify Hack4Health organizers before broader public publication if required.
- [ ] Verify dataset citation and license requirements.
