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
    is_url = args.input.startswith("http://") or args.input.startswith("https://")
    content = args.input

    if not is_url:
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()

    print(f"Starting review for: {args.input}")
    print(f"Using model: {args.model}")

    try:
        reviewer = TechnicalBlogReviewer(model=args.model)
        report = reviewer.review(content, is_url=is_url)

        if "error" in report:
            print(f"Error during review: {report['error']}")
            sys.exit(1)

        # Print Summary to Console
        print("\n=== Review Summary ===")
        print(report["summary"])
        print("\n=== Technical Accuracy ===")
        print(report["technical_accuracy"][:500] + "...") # Preview

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"\nFull report saved to: {args.output}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
