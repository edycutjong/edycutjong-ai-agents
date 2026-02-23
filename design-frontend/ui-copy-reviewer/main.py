import os
import argparse
import sys

# Ensure current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.extractor import TextExtractor
from agent.reviewer import ReviewerAgent
from agent.report import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="UI Copy Reviewer Agent")
    parser.add_argument("path", help="Path to file or directory to review")
    parser.add_argument("--output", default="copy_review_report.md", help="Output file path for the report")
    args = parser.parse_args()

    target_path = args.path
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    print(f"Starting review for: {target_path}")

    extractor = TextExtractor()
    reviewer = ReviewerAgent()

    all_extracted_items = []

    if os.path.isfile(target_path):
        files_to_process = [target_path]
    else:
        files_to_process = []
        for root, _, files in os.walk(target_path):
            for file in files:
                filepath = os.path.join(root, file)
                files_to_process.append(filepath)

    print(f"Found {len(files_to_process)} file(s) to process.")

    total_issues = 0
    reviewed_files_count = 0

    final_report_items = []

    for filepath in files_to_process:
        try:
            items = extractor.extract_text_from_file(filepath)
            if not items:
                continue

            print(f"Reviewing {filepath} ({len(items)} items)...")
            reviewed_files_count += 1

            reviewed_items = reviewer.review_items(items)

            if reviewed_items:
                # Add file info to items
                for item in reviewed_items:
                    item['file'] = filepath
                    final_report_items.append(item)
                    total_issues += 1

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nReview complete. Found issues in {len(final_report_items)} items across {reviewed_files_count} files.")

    if final_report_items:
        report_gen = ReportGenerator(final_report_items)
        report_gen.save_report(args.output)
    else:
        print("No issues found. Great job!")

if __name__ == "__main__":
    main()
