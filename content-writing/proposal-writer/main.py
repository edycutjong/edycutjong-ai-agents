import argparse
import sys
import os

# Add the current directory to sys.path to ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.generator import ProposalGenerator
from agent.pdf_generator import create_pdf, create_markdown

def main():
    parser = argparse.ArgumentParser(description="AI Proposal Writer")
    parser.add_argument("requirements", help="Path to requirements file or requirements string")
    parser.add_argument("--pdf", default="proposal.pdf", help="Output PDF filename")
    parser.add_argument("--md", default="proposal.md", help="Output Markdown filename")

    args = parser.parse_args()

    # Check if requirements is a file
    requirements = args.requirements
    if os.path.exists(requirements):
        try:
            with open(requirements, 'r') as f:
                requirements = f.read()
        except Exception:
            # If it looks like a path but can't be read, treat as string or fail?
            # But the user might provide a string that happens to be a filename (unlikely for "project requirements").
            # If it exists, we assume it's a file.
            pass
    else:
        # It doesn't exist as a file, so it must be the string content
        pass

    print("Generating proposal...")
    try:
        generator = ProposalGenerator()
        proposal = generator.generate_proposal(requirements)

        print(f"Proposal '{proposal.project_title}' generated.")

        if args.pdf:
            print(f"Saving PDF to {args.pdf}...")
            create_pdf(proposal, args.pdf)

        if args.md:
            print(f"Saving Markdown to {args.md}...")
            create_markdown(proposal, args.md)

        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
