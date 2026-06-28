# Initial Data Audit

Generated from direct inspection of the local files on 2026-06-28.

## Cardiac Failure

Base file: `docs/drive-download-20260627T215828Z-3-001/Datasets/Cardiac Failure/cardio_base.csv`

- Shape: 70,000 rows, 13 columns.
- Separator: semicolon.
- Target: `cardio`, nearly balanced: 35,021 negative and 34,979 positive.
- Age in base file is measured in days, approximately 29.6 to 64.9 years.
- No missing values detected in the first audit.
- Data-quality risks:
  - `ap_hi <= 0`: 7 rows.
  - `ap_lo <= 0`: 22 rows.
  - `ap_hi > 250`: 40 rows.
  - `ap_lo > 200`: 953 rows.
  - `ap_lo > ap_hi`: 1,234 rows.
  - Height range 55-250 cm and weight range 10-200 kg suggest physiologic outliers.

Processed file: `docs/drive-download-20260627T215828Z-3-001/Datasets/Cardiac Failure/cardiac_failure_processed.csv`

- Shape: 70,000 rows, 14 columns.
- Contains `Unnamed: 0`, likely a saved index.
- Age is min-max scaled from 0 to 1.
- Blood-pressure anomalies remain present, so the processed file is not a fully cleaned modeling table.

Modeling implication: use the base file as the canonical input, perform transparent clinical plausibility cleaning, and report sensitivity analyses with and without exclusions.

Initial plausibility filter used in `scripts/eda_tabular.py`:

- Height 120-220 cm.
- Weight 30-250 kg.
- BMI 10-80.
- Systolic BP 80-250.
- Diastolic BP 40-150.
- Diastolic BP not greater than systolic BP.

This removes 1,395 rows, or 1.99% of the dataset. Target rate changes from 0.4997 to 0.4947.

Sensitivity profiles show that neighboring cleaning choices retain similar target rates:

- `raw`: 70,000 rows, target rate 0.4997.
- `lenient`: 68,644 rows, target rate 0.4947.
- `current`: 68,605 rows, target rate 0.4947.
- `strict`: 68,362 rows, target rate 0.4950.

This supports the current filter as a transparent plausibility rule rather than a performance-maximizing deletion scheme.

Among plausibility-filtered rows, cardiovascular-positive rate rises strongly by systolic BP band:

- `<120`: 0.2305.
- `120-129`: 0.3560.
- `130-139`: 0.5985.
- `>=140`: 0.8370.

## Heart Attack

File: `docs/drive-download-20260627T215828Z-3-001/Datasets/Heart Attack/heart_processed.csv`

- Shape: 918 rows, 16 columns.
- Target: `HeartDisease`, with 508 positive and 410 negative rows.
- Already one-hot encoded for sex, chest-pain type, resting ECG, exercise angina, and ST slope.
- Data-quality risks:
  - `RestingBP == 0`: 1 row.
  - `Cholesterol == 0`: 172 rows.
  - Male class count: 725 male-coded rows and 193 non-male-coded rows.

Modeling implication: this dataset is too small for complex modeling but useful for external-style comparison of tabular CVD risk factors, cleaning choices, and interpretability narratives.

Initial cleaning impact:

- Removing invalid resting BP removes 1 row and barely changes target rate.
- Treating `Cholesterol == 0` as unobserved affects 172 rows, or 18.7% of the dataset.
- Target rate is 0.5534 in the raw data and 0.4772 in the observed-cholesterol subset, so cholesterol missingness is strongly associated with the target and should not be silently dropped.

## ECG Timeseries

File: `docs/drive-download-20260627T215828Z-3-001/Datasets/ECG Timeseries/ecg_timeseries.csv`

- File size: approximately 632 MB.
- Header length: 123,995 columns.
- Row count: 528.
- Separate schema audit found 36,441 duplicate non-empty header names.
- First data rows show normalized-looking floating values between 0 and 1, but sampled values include a maximum of 4.0.
- Column names appear repeated or non-unique after the first block, so the structure must be validated before modeling.

Modeling implication: treat ECG as an extension track. Before any model, determine whether rows represent patients, leads, beats, or recordings; identify labels; then convert to a compact array/parquet format and extract physiologic features.

## Immediate Technical Risks

- The workspace initially had no git repository, no `requirements.txt`, and no notebook scaffold.
- The bundled Python runtime has `pandas`, `numpy`, `openpyxl`, `pypdf`, and `pdfplumber`, but not `scikit-learn`, `matplotlib`, `seaborn`, or `scipy`.
- A Kaggle or project virtual environment should include the missing scientific packages before baseline modeling.
