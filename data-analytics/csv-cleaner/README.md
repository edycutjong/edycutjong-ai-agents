# CSV Cleaner 🧹

Ingests messy CSV files, detects and fixes encoding issues, duplicates, missing values, and type mismatches.

## Features

- **Encoding Detection** — Auto-detect and convert to UTF-8
- **Whitespace Trimming** — Strip columns and cell values
- **Duplicate Removal** — Exact and subset-based dedup
- **Missing Values** — 4 strategies: drop, fill_mean, fill_mode, fill_empty
- **Date Standardization** — Auto-detect and convert to YYYY-MM-DD
- **Type Fixing** — Convert string numbers to numeric
- **Quality Reports** — Data quality summary with metrics
- **Cleaning Reports** — Detailed log of all actions taken

## Quick Start

```bash
pip install -r requirements.txt

# Basic clean
python main.py messy_data.csv

# Specify output and strategy
python main.py data.csv -o cleaned.csv --strategy fill_mean

# Dry run with report
python main.py data.csv --dry-run --report

# Markdown report
python main.py data.csv --report --markdown
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests use in-memory DataFrames — no external files needed.

## Project Structure

```
csv-cleaner/
├── main.py          # CLI interface
├── config.py        # Settings
├── requirements.txt # Dependencies (pandas, chardet)
├── agent/
│   └── cleaner.py   # Core cleaning engine
└── tests/
    └── test_cleaner.py  # 22 comprehensive tests
```
