import typer
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from agent.core import DataValidator
from agent.llm import LLMAnalyzer
from typing import Optional
import pandas as pd
import json

app = typer.Typer()
scheduler = BlockingScheduler()

def run_validation_task(source_path: str, dest_path: str, source_type: str, dest_type: str, api_key: Optional[str] = None):
    """
    Core validation logic used by CLI and Scheduler.
    """
    print(f"\n[INFO] Starting validation run at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    validator = DataValidator()
    llm_analyzer = LLMAnalyzer(api_key=api_key)

    try:
        # Load Data
        print(f"[INFO] Loading source: {source_path}")
        source_df = validator.load_data(source_path, file_type=source_type)
        print(f"[INFO] Loading destination: {dest_path}")
        dest_df = validator.load_data(dest_path, file_type=dest_type)

        # Run Validation
        print("[INFO] Running validation checks...")
        results = validator.run_full_validation(source_df, dest_df)

        # Print Summary
        print("\n--- Validation Results ---")
        row_counts = results["row_counts"]
        print(f"Row Counts: Source={row_counts['source_count']}, Dest={row_counts['dest_count']}, Match={row_counts['match']}")

        schema = results["schema"]
        print(f"Schema Match: {schema['schema_match']}")
        if not schema["schema_match"]:
            print(f"Missing Cols: {schema['missing_columns']}")
            print(f"Type Mismatches: {schema['type_mismatches']}")

        # AI Analysis
        if api_key or os.getenv("OPENAI_API_KEY"):
            print("\n[INFO] Generating AI Analysis...")
            analysis = llm_analyzer.analyze_report(results)
            print("\n--- AI Analysis ---")
            print(analysis)
        else:
            print("\n[INFO] AI Analysis skipped (No API Key)")

        # Simple Alerting Logic
        if not row_counts['match'] or not schema['schema_match']:
            print("\n[ALERT] Data Pipeline Validation FAILED! Check logs above.")
        else:
            print("\n[SUCCESS] Data Pipeline Validation PASSED.")

    except Exception as e:
        print(f"\n[ERROR] Validation failed: {str(e)}")

@app.command()
def validate(
    source: str = typer.Option(..., help="Path to source file"),
    dest: str = typer.Option(..., help="Path to destination file"),
    source_type: str = typer.Option("csv", help="Source file type (csv, parquet, excel)"),
    dest_type: str = typer.Option("csv", help="Destination file type (csv, parquet, excel)"),
    api_key: str = typer.Option(None, envvar="OPENAI_API_KEY", help="OpenAI API Key")
):
    """
    Run a one-off data pipeline validation.
    """
    run_validation_task(source, dest, source_type, dest_type, api_key)

@app.command()
def schedule(
    source: str = typer.Option(..., help="Path to source file"),
    dest: str = typer.Option(..., help="Path to destination file"),
    interval: int = typer.Option(60, help="Interval in minutes"),
    source_type: str = typer.Option("csv", help="Source file type (csv, parquet, excel)"),
    dest_type: str = typer.Option("csv", help="Destination file type (csv, parquet, excel)"),
    api_key: str = typer.Option(None, envvar="OPENAI_API_KEY", help="OpenAI API Key")
):
    """
    Schedule recurring validation checks.
    """
    print(f"[INFO] Scheduling validation every {interval} minutes...")
    scheduler.add_job(
        run_validation_task,
        'interval',
        minutes=interval,
        args=[source, dest, source_type, dest_type, api_key]
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    app()
