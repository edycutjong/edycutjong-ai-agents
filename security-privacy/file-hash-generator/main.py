"""
File Hash Generator — CLI Entry Point
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.hasher import *


def main():
    parser = argparse.ArgumentParser(description="Generate file hashes")
    parser.add_argument("input", nargs="?", help="Input value")
    parser.add_argument("--help-agent", action="store_true", help="Show agent info")
    args = parser.parse_args()

    if args.help_agent or not args.input:
        print("\nFile Hash Generator")
        print("=" * len("File Hash Generator"))
        print("Generate file hashes")
        print("\nUsage: python main.py <input>")
        return

    print(f"Input: {args.input}")
    print("Agent ready — import from agent.hasher for programmatic use.")


if __name__ == "__main__":
    main()
