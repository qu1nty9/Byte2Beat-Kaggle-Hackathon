# Data Card

## Project

From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

## Author

Yaroslav Kholmirzayev

yaric.kholm@gmail.com

## Data Sources

The project uses Byte2Beat/Hack4Health-provided public cardiovascular datasets stored locally under `docs/drive-download-20260627T215828Z-3-001/Datasets/`.

Primary modeling source:

- `Cardiac Failure/cardio_base.csv`

Audited comparison and extension sources:

- `Heart Attack/heart_processed.csv`
- `ECG Timeseries/ecg_timeseries.csv`

Raw datasets are not committed to the repository because of size and redistribution uncertainty. Generated tables and figures are committed under `outputs/`.

## Unit of Analysis

Primary analysis unit:

- One row in `cardio_base.csv`.

The project treats each row as an independent tabular record for modeling. The repository does not claim verified patient identity, longitudinal linkage, or clinical encounter semantics.

## Target

Primary target:

- `cardio`, a binary cardiovascular outcome label.

Target balance in the raw primary dataset:

- Negative: 35,021 rows.
- Positive: 34,979 rows.

## Primary Features

Primary cardiac features include:

- Age, converted from days to years.
- Gender coding as provided.
- Height and weight.
- Derived BMI.
- Systolic and diastolic blood pressure.
- Cholesterol and glucose categories.
- Smoking, alcohol, and activity indicators.

## Known Data Quality Issues

Primary cardiac dataset:

- `ap_hi <= 0`: 7 rows.
- `ap_lo <= 0`: 22 rows.
- `ap_hi > 250`: 40 rows.
- `ap_lo > 200`: 953 rows.
- `ap_lo > ap_hi`: 1,234 rows.
- Height and weight ranges include physiologic outliers.

Heart comparison dataset:

- 918 rows only.
- `Cholesterol == 0` in 172 rows, likely missing-like and target-associated.

ECG extension dataset:

- 528 rows.
- 123,995 columns.
- 36,441 duplicate non-empty header names.
- Row semantics and labels are not validated.

## Cleaning Rules

The primary cardiac plausibility filter keeps rows satisfying:

- Height 120-220 cm.
- Weight 30-250 kg.
- BMI 10-80.
- Systolic BP 80-250.
- Diastolic BP 40-150.
- Diastolic BP not greater than systolic BP.

Rows retained after current cleaning:

- 68,605 of 70,000.

Rows removed:

- 1,395, or 1.99 percent.

## Intended Use

Appropriate:

- Educational cardiovascular ML workflow.
- Reproducibility demonstration.
- Data-quality audit and sensitivity-analysis case study.
- Kaggle/Hack4Health writeup and public notebook.

Not appropriate:

- Diagnosis.
- Treatment recommendation.
- Clinical decision support.
- Patient-level deployment.
- Claims about real-world clinical generalization.

## Ethical and Publication Notes

The project is educational/research-only. Dataset license and redistribution requirements must be checked before any publication beyond Kaggle. Hack4Health organizers should be notified before public releases such as preprints, blog posts, GitHub releases, or conference submissions if required by the rules.

## Key Evidence Artifacts

- `outputs/tables/data_audit.json`
- `outputs/tables/cardio_cleaning_impact.csv`
- `outputs/tables/heart_cleaning_impact.csv`
- `outputs/tables/ecg_schema_audit.json`
- `research/data_audit.md`
- `docs/DATA.md`
