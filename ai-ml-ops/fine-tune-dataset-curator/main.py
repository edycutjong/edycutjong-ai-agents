import argparse
import sys
import os

# Add the project root to sys.path to allow imports if running from main.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agent.curator import create_curator_agent
from config import Config

def main():
    parser = argparse.ArgumentParser(description="Fine-Tune Dataset Curator Agent")
    parser.add_argument("query", type=str, help="Instruction for the agent (e.g., 'Clean dataset.csv and format for OpenAI')")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file.")
        sys.exit(1)

    print("Initializing Curator Agent...")
    agent_executor = create_curator_agent()

    print(f"\nProcessing query: {args.query}\n")

    try:
        response = agent_executor.invoke({"input": args.query})
        print("\n--- Result ---")
        print(response['output'])
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
