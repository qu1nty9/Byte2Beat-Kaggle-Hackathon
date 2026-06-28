from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ECG_PATH = (
    ROOT
    / "docs"
    / "drive-download-20260627T215828Z-3-001"
    / "Datasets"
    / "ECG Timeseries"
    / "ecg_timeseries.csv"
)
OUT_JSON = ROOT / "outputs" / "tables" / "ecg_schema_audit.json"


def main() -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    with ECG_PATH.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        first_rows = []
        row_count = 0
        row_lengths = Counter()
        sampled_values: list[float] = []

        sample_cols = {0, len(header) - 1}
        sample_cols.update(range(1, len(header), 1000))

        for row in reader:
            row_count += 1
            row_lengths[len(row)] += 1
            if len(first_rows) < 5:
                first_rows.append(row[:10] + ["..."] + row[-5:])
            for idx in sample_cols:
                if idx == 0 or idx >= len(row):
                    continue
                try:
                    sampled_values.append(float(row[idx]))
                except ValueError:
                    pass

    nonempty_header = [col for col in header if col != ""]
    duplicate_header_count = len(nonempty_header) - len(set(nonempty_header))
    repeated_names = [name for name, count in Counter(nonempty_header).items() if count > 1][:20]

    audit = {
        "path": str(ECG_PATH.relative_to(ROOT)),
        "file_size_mb": ECG_PATH.stat().st_size / (1024 * 1024),
        "header_len": len(header),
        "row_count": row_count,
        "row_lengths": dict(row_lengths),
        "first_header": header[:12],
        "last_header": header[-12:],
        "duplicate_nonempty_header_count": duplicate_header_count,
        "first_repeated_header_names": repeated_names,
        "first_rows_excerpt": first_rows,
        "sampled_numeric_values": len(sampled_values),
        "sampled_min": float(np.min(sampled_values)) if sampled_values else None,
        "sampled_mean": float(np.mean(sampled_values)) if sampled_values else None,
        "sampled_max": float(np.max(sampled_values)) if sampled_values else None,
    }
    OUT_JSON.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(json.dumps({k: audit[k] for k in ["header_len", "row_count", "duplicate_nonempty_header_count"]}, indent=2))


if __name__ == "__main__":
    main()

