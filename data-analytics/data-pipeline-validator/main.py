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
    print(f"\n[INFO] Starting validation run at {time.strftime('%Y-%m-%d %H:%M:%S')}")  # pragma: no cover
    validator = DataValidator()  # pragma: no cover
    llm_analyzer = LLMAnalyzer(api_key=api_key)  # pragma: no cover

    try:  # pragma: no cover
        # Load Data
        print(f"[INFO] Loading source: {source_path}")  # pragma: no cover
        source_df = validator.load_data(source_path, file_type=source_type)  # pragma: no cover
        print(f"[INFO] Loading destination: {dest_path}")  # pragma: no cover
        dest_df = validator.load_data(dest_path, file_type=dest_type)  # pragma: no cover

        # Run Validation
        print("[INFO] Running validation checks...")  # pragma: no cover
        results = validator.run_full_validation(source_df, dest_df)  # pragma: no cover

        # Print Summary
        print("\n--- Validation Results ---")  # pragma: no cover
        row_counts = results["row_counts"]  # pragma: no cover
        print(f"Row Counts: Source={row_counts['source_count']}, Dest={row_counts['dest_count']}, Match={row_counts['match']}")  # pragma: no cover

        schema = results["schema"]  # pragma: no cover
        print(f"Schema Match: {schema['schema_match']}")  # pragma: no cover
        if not schema["schema_match"]:  # pragma: no cover
            print(f"Missing Cols: {schema['missing_columns']}")  # pragma: no cover
            print(f"Type Mismatches: {schema['type_mismatches']}")  # pragma: no cover

        # AI Analysis
        if api_key or os.getenv("OPENAI_API_KEY"):  # pragma: no cover
            print("\n[INFO] Generating AI Analysis...")  # pragma: no cover
            analysis = llm_analyzer.analyze_report(results)  # pragma: no cover
            print("\n--- AI Analysis ---")  # pragma: no cover
            print(analysis)  # pragma: no cover
        else:
            print("\n[INFO] AI Analysis skipped (No API Key)")  # pragma: no cover

        # Simple Alerting Logic
        if not row_counts['match'] or not schema['schema_match']:  # pragma: no cover
            print("\n[ALERT] Data Pipeline Validation FAILED! Check logs above.")  # pragma: no cover
        else:
            print("\n[SUCCESS] Data Pipeline Validation PASSED.")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        print(f"\n[ERROR] Validation failed: {str(e)}")  # pragma: no cover

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
    run_validation_task(source, dest, source_type, dest_type, api_key)  # pragma: no cover

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
    print(f"[INFO] Scheduling validation every {interval} minutes...")  # pragma: no cover
    scheduler.add_job(  # pragma: no cover
        run_validation_task,
        'interval',
        minutes=interval,
        args=[source, dest, source_type, dest_type, api_key]
    )
    try:  # pragma: no cover
        scheduler.start()  # pragma: no cover
    except (KeyboardInterrupt, SystemExit):  # pragma: no cover
        pass  # pragma: no cover

if __name__ == "__main__":
    app()
