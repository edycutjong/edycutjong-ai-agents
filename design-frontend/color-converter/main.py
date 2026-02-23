"""
Color Converter — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.converter import *


def main():
    parser = argparse.ArgumentParser(description="Convert between color formats")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nColor Converter")
        print("=" * len("Color Converter"))
        print("Convert between color formats")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.converter for programmatic use.")


if __name__ == "__main__":
    main()
