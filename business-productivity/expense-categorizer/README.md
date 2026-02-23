# Expense Categorizer 💰

Auto-categorize bank transactions into spending categories. Parse CSVs, detect recurring subscriptions, flag unusual spending.

## Features

- **10 Categories** — Food, Transport, Shopping, Subscriptions, Utilities, Health, Entertainment, Education, Housing, Insurance
- **100+ Keywords** — Smart pattern matching for major vendors
- **CSV Parsing** — Reads standard bank statement exports
- **Recurring Detection** — Flags subscriptions automatically
- **Unusual Spending** — Flags outlier transactions
- **Reports** — Text, JSON, and Markdown output

## Quick Start

```bash
pip install -r requirements.txt

# Categorize a bank CSV
python main.py categorize bank_statement.csv
python main.py categorize bank_statement.csv --markdown
python main.py categorize bank_statement.csv --json

# Check a single description
python main.py check "STARBUCKS COFFEE"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
expense-categorizer/
├── main.py                  # CLI
├── config.py
├── requirements.txt
├── agent/
│   └── categorizer.py       # Categorization engine
└── tests/
    └── test_categorizer.py  # 20 tests
```
