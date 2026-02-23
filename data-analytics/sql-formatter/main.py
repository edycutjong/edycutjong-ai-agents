"""
SQL Formatter — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.formatter import *


def main():
    parser = argparse.ArgumentParser(description="Format SQL queries")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nSQL Formatter")
        print("=" * len("SQL Formatter"))
        print("Format SQL queries")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.formatter for programmatic use.")


if __name__ == "__main__":
    main()
