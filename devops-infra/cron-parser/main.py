"""
Cron Parser — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.parser import *


def main():
    parser = argparse.ArgumentParser(description="Parse and explain cron expressions")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nCron Parser")
        print("=" * len("Cron Parser"))
        print("Parse and explain cron expressions")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.parser for programmatic use.")


if __name__ == "__main__":
    main()
