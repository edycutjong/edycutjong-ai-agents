"""
HTML to Markdown Converter — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.converter import *


def main():
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown format")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nHTML to Markdown Converter")
        print("=" * len("HTML to Markdown Converter"))
        print("Convert HTML to Markdown format")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.converter for programmatic use.")


if __name__ == "__main__":
    main()
