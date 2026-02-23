# Data Pipeline Validator Agent

This agent validates ETL pipelines by comparing Source and Destination data. It checks for row count mismatches, schema changes, data quality issues, and uses AI to verify transformation logic.

## Features

- **Row Count Validation:** Ensures no data loss during transfer.
- **Schema Validation:** Checks for missing columns and type mismatches.
- **Data Quality Check:** Identifies null values and duplicates.
- **Distribution Analysis:** Compares numeric column distributions (mean, histogram).
- **AI Verification:** Uses GPT-4o to analyze validation reports and verify complex transformation logic (e.g., natural language rules).
- **Scheduling:** Run periodic validation checks.
- **Alerting:** CLI alerts on validation failure.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Copy `.env.example` to `.env` and add your OpenAI API Key.
    ```bash
    cp .env.example .env
    # Edit .env
    ```

## Usage

### 1. Web UI (Recommended)
Launch the Streamlit interface for interactive validation and visualization.

```bash
streamlit run ui.py
```

### 2. CLI Tool
Run validation from the command line.

**One-off Validation:**
```bash
python main.py validate --source data/source.csv --dest data/dest.csv
```

**Scheduled Validation:**
Run checks every 60 minutes.
```bash
python main.py schedule --source data/source.csv --dest data/dest.csv --interval 60
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Tech Stack

- **Core:** Python, Pandas, NumPy
- **Agent/AI:** LangChain, OpenAI GPT-4o
- **UI:** Streamlit, Plotly
- **CLI/Scheduling:** Typer, APScheduler
