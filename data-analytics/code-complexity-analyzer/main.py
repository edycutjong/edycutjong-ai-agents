"""
Code Complexity Analyzer — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.analyzer import *


def main():
    parser = argparse.ArgumentParser(description="Analyze code complexity")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nCode Complexity Analyzer")
        print("=" * len("Code Complexity Analyzer"))
        print("Analyze code complexity")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.analyzer for programmatic use.")


if __name__ == "__main__":
    main()
