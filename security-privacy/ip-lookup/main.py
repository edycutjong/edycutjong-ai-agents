"""
IP Lookup — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.lookup import *


def main():
    parser = argparse.ArgumentParser(description="Look up IP address information")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nIP Lookup")
        print("=" * len("IP Lookup"))
        print("Look up IP address information")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.lookup for programmatic use.")


if __name__ == "__main__":
    main()
