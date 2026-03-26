import argparse
import sys
import os
import json
from dotenv import load_dotenv

# Ensure we can import modules from local package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import TechnicalBlogReviewer
from config import DEFAULT_MODEL

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Technical Blog Reviewer Agent")
    parser.add_argument("input", help="Path to a text file or a URL to review")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model to use")
    parser.add_argument("--output", help="Path to save the review report (JSON)")

    args = parser.parse_args()

    # Determine if input is URL or file
    is_url = args.input.startswith("http://") or args.input.startswith("https://")  # pragma: no cover
    content = args.input  # pragma: no cover

    if not is_url:  # pragma: no cover
        if not os.path.exists(args.input):  # pragma: no cover
            print(f"Error: File not found: {args.input}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
        with open(args.input, "r", encoding="utf-8") as f:  # pragma: no cover
            content = f.read()  # pragma: no cover

    print(f"Starting review for: {args.input}")  # pragma: no cover
    print(f"Using model: {args.model}")  # pragma: no cover

    try:  # pragma: no cover
        reviewer = TechnicalBlogReviewer(model=args.model)  # pragma: no cover
        report = reviewer.review(content, is_url=is_url)  # pragma: no cover

        if "error" in report:  # pragma: no cover
            print(f"Error during review: {report['error']}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        # Print Summary to Console
        print("\n=== Review Summary ===")  # pragma: no cover
        print(report["summary"])  # pragma: no cover
        print("\n=== Technical Accuracy ===")  # pragma: no cover
        print(report["technical_accuracy"][:500] + "...") # Preview  # pragma: no cover

        if args.output:  # pragma: no cover
            with open(args.output, "w", encoding="utf-8") as f:  # pragma: no cover
                json.dump(report, f, indent=2)  # pragma: no cover
            print(f"\nFull report saved to: {args.output}")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        print(f"An unexpected error occurred: {str(e)}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

if __name__ == "__main__":
    main()
