#!/usr/bin/env python3
"""CLI for CSV Cleaner.

Usage:
    python main.py input.csv                        # Clean with defaults
    python main.py input.csv -o cleaned.csv         # Specify output
    python main.py input.csv --strategy fill_mean   # Fill missing values
    python main.py input.csv --report               # Print quality report
    python main.py input.csv --report --markdown     # Markdown report
"""
import argparse
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))

from agent.cleaner import CSVCleaner


def main():
    parser = argparse.ArgumentParser(
        description="CSV Cleaner — Fix messy CSV files automatically.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("-o", "--output", help="Path for cleaned CSV (default: input_cleaned.csv)")
    parser.add_argument("--strategy", choices=["drop", "fill_mean", "fill_mode", "fill_empty"],
                        default="drop", help="Missing value strategy (default: drop)")
    parser.add_argument("--no-dedup", action="store_true", help="Skip duplicate removal")
    parser.add_argument("--no-types", action="store_true", help="Skip type fixing")
    parser.add_argument("--no-dates", action="store_true", help="Skip date standardization")
    parser.add_argument("--report", action="store_true", help="Print quality report")
    parser.add_argument("--markdown", action="store_true", help="Output report as Markdown")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, don't save")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    cleaner = CSVCleaner()

    # Load
    print(f"Loading {args.input}...")
    df = cleaner.load_csv(filepath=args.input)
    print(f"  {len(df)} rows, {len(df.columns)} columns")

    if args.report and args.dry_run:
        # Just show quality report, don't clean
        quality = cleaner.get_quality_summary(df)
        print(f"\nData Quality Summary:")
        print(f"  Rows: {quality['rows']}")
        print(f"  Columns: {quality['columns']}")
        print(f"  Missing: {quality['missing_cells']} ({quality['missing_percent']}%)")
        print(f"  Duplicates: {quality['duplicate_rows']}")
        print(f"\nColumn types:")
        for col, dtype in quality["dtypes"].items():
            print(f"  {col}: {dtype}")
        return

    # Clean
    df = cleaner.clean(
        df,
        missing_strategy=args.strategy,
        remove_dupes=not args.no_dedup,
        fix_types=not args.no_types,
        standardize_dates_flag=not args.no_dates,
    )

    # Report
    if args.report or args.markdown:
        if args.markdown:
            print(cleaner.report.to_markdown())
        else:
            report = cleaner.report.to_dict()
            print(f"\nCleaning Report:")
            print(f"  Original: {report['original_rows']} rows")
            print(f"  Final: {report['final_rows']} rows")
            print(f"  Removed: {report['rows_removed']} rows")
            print(f"\nActions:")
            for action in report["actions"]:
                print(f"  • {action}")

    # Save
    if not args.dry_run:
        output_path = args.output or args.input.replace(".csv", "_cleaned.csv")
        cleaner.save(df, output_path)
        print(f"\n✅ Saved cleaned CSV to {output_path}")
    else:
        print(f"\n📋 Dry run — no file saved.")


if __name__ == "__main__":
    main()
