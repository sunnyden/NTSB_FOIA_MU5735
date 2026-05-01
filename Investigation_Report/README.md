# Investigation Report

This folder contains an **independent analytical reading** of the MU5735 (China Eastern, B-1791,
2022-03-21) accident, prepared from the materials in this repository.

| File | Description |
|---|---|
| [`Investigation_Report_EN.md`](Investigation_Report_EN.md) | Full investigation report (English) |
| [`Investigation_Report_CN.md`](Investigation_Report_CN.md) | Full investigation report (中文) |
| [`figures/`](figures/) | 12 PNG charts derived from `ExactSample.csv` |
| [`scripts/analyze.py`](scripts/analyze.py) | Reproducible script that re-creates every figure from `ExactSample.csv` |

Both reports describe the same analysis and reach the same conclusions; they cite the NTSB recorder
report and supporting NTSB ↔ CAAC correspondence already present in this repository.

This is **not** an official accident report. The State of Occurrence (CAAC) is the only authority
empowered under ICAO Annex 13 to publish the final report.

## Reproducing the figures

```bash
pip install pandas numpy matplotlib
python3 Investigation_Report/scripts/analyze.py
```

The script reads `ExactSample.csv` at the repository root and re-writes the PNGs into
`Investigation_Report/figures/`.
