# Final Submission Checklist

## Kaggle Writeup

- [ ] Final text reviewed and approved by the author, not copied blindly from scaffolding.
- [ ] `submission/final_kaggle_writeup.md` has the final title, subtitle, and author block.
- [ ] `submission/kaggle_writeup_review_draft.md` has been reviewed against the final artifacts.
- [ ] Title and subtitle are concise.
- [ ] Problem framing is clear in the first paragraph.
- [ ] Data sources and provenance are described.
- [ ] Data audit includes anomalies and ECG caveat.
- [ ] Cleaning rules include counts removed.
- [ ] Sensitivity analysis explains why the result is not threshold-fragile.
- [ ] Main model result includes AUROC, AUPRC, Brier score, and CV result.
- [ ] Calibration is discussed, not only discrimination.
- [ ] Error analysis includes false positives and false negatives.
- [ ] Every major claim has an evidence pointer in `submission/claims_ledger.md`.
- [ ] `submission/data_card.md` and `submission/model_card.md` are aligned with the final writeup.
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
- [ ] `make submission-check` passes without failures.
- [ ] `Makefile` targets work: `make all`, `make check`.
- [ ] GitHub repository is public or accessible to judges.

## Publication Path

- [ ] Decide whether this is Kaggle-only, blog, GitHub release, or preprint.
- [ ] Review `paper/publication_readiness.md` before any public release beyond Kaggle.
- [ ] Notify Hack4Health organizers before broader public publication if required.
- [ ] Verify dataset citation and license requirements.
- [ ] Complete `paper/publication_readiness.md` before any preprint or article submission.
