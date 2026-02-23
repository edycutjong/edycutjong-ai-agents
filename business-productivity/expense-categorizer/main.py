#!/usr/bin/env python3
"""CLI for Expense Categorizer."""
import argparse
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))

from agent.categorizer import (
    parse_bank_csv, categorize_transaction, generate_expense_report,
    format_report_markdown, detect_recurring, flag_unusual_spending,
)


def cmd_categorize(args):
    """Categorize a bank statement CSV."""
    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        content = f.read()

    transactions = parse_bank_csv(
        content,
        date_col=args.date_col,
        desc_col=args.desc_col,
        amount_col=args.amount_col,
    )

    report = generate_expense_report(transactions)

    if args.markdown:
        print(format_report_markdown(report, transactions))
    elif args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Total: ${report['total_spending']:,.2f} across {report['transaction_count']} transactions\n")
        print("Category Breakdown:")
        for cat, data in report["categories"].items():
            bar = "█" * int(data["percentage"] / 5)
            print(f"  {cat:<25} ${data['total']:>10,.2f}  {data['percentage']:>5.1f}%  {bar}")

        if report["recurring_count"] > 0:
            print(f"\n📌 {report['recurring_count']} recurring transactions (${report['recurring_total']:,.2f})")
        if report["unusual_count"] > 0:
            print(f"⚠️  {report['unusual_count']} unusual transactions flagged")


def cmd_check(args):
    """Categorize a single description."""
    category = categorize_transaction(args.description)
    print(f'"{args.description}" → {category}')


def main():
    parser = argparse.ArgumentParser(description="Expense Categorizer — Auto-categorize bank transactions")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("categorize", help="Categorize a bank CSV")
    p.add_argument("input", help="Path to bank statement CSV")
    p.add_argument("--date-col", default="Date", help="Date column name")
    p.add_argument("--desc-col", default="Description", help="Description column name")
    p.add_argument("--amount-col", default="Amount", help="Amount column name")
    p.add_argument("--markdown", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_categorize)

    p = sub.add_parser("check", help="Categorize a single description")
    p.add_argument("description", help="Transaction description")
    p.set_defaults(func=cmd_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
