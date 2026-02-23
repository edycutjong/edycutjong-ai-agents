"""Expense categorization engine with rule-based pattern matching."""
from __future__ import annotations

import csv
import io
import re
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import defaultdict


# Category rules: keyword patterns → category
CATEGORY_RULES = {
    "Food & Dining": [
        "restaurant", "cafe", "coffee", "starbucks", "mcdonald", "pizza",
        "uber eats", "doordash", "grubhub", "chipotle", "subway", "burger",
        "bakery", "food", "dining", "lunch", "dinner", "breakfast", "taco",
        "sushi", "ramen", "noodle", "pho", "thai", "chinese", "indian",
    ],
    "Transportation": [
        "uber", "lyft", "taxi", "gas", "fuel", "parking", "toll",
        "transit", "metro", "bus", "train", "airline", "flight", "delta",
        "united", "american air", "southwest", "jetblue",
    ],
    "Shopping": [
        "amazon", "walmart", "target", "costco", "best buy", "ebay",
        "etsy", "ikea", "home depot", "lowes", "nordstrom", "zara",
        "h&m", "nike", "adidas", "apple store", "shop",
    ],
    "Subscriptions": [
        "netflix", "spotify", "hulu", "disney+", "hbo", "apple music",
        "youtube premium", "github", "adobe", "dropbox", "icloud",
        "aws", "google cloud", "heroku", "vercel", "notion", "slack",
        "zoom", "microsoft 365", "chatgpt", "openai", "anthropic",
        "subscription", "monthly", "annual",
    ],
    "Utilities": [
        "electric", "water", "gas bill", "internet", "phone", "mobile",
        "comcast", "verizon", "at&t", "t-mobile", "utility",
    ],
    "Health & Medical": [
        "pharmacy", "cvs", "walgreens", "doctor", "hospital", "medical",
        "dental", "vision", "gym", "fitness", "health", "insurance claim",
    ],
    "Entertainment": [
        "cinema", "movie", "concert", "theater", "game", "steam",
        "playstation", "xbox", "nintendo", "amusement", "museum", "zoo",
    ],
    "Education": [
        "udemy", "coursera", "book", "textbook", "tuition", "school",
        "university", "course", "training", "seminar", "conference",
    ],
    "Housing": [
        "rent", "mortgage", "property tax", "hoa", "lease", "apartment",
    ],
    "Insurance": [
        "insurance", "geico", "progressive", "allstate", "state farm",
    ],
}


@dataclass
class Transaction:
    """A single financial transaction."""
    date: str
    description: str
    amount: float
    category: str = ""
    currency: str = "USD"
    is_recurring: bool = False
    raw_line: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def categorize_transaction(description: str) -> str:
    """Categorize a transaction by matching description against rules."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return "Uncategorized"


def detect_recurring(transactions: list[Transaction], threshold: int = 2) -> list[Transaction]:
    """Detect likely recurring transactions (same description+amount appearing multiple times)."""
    seen = defaultdict(int)
    for t in transactions:
        key = (t.description.lower().strip(), round(t.amount, 2))
        seen[key] += 1

    for t in transactions:
        key = (t.description.lower().strip(), round(t.amount, 2))
        if seen[key] >= threshold:
            t.is_recurring = True

    return transactions


def flag_unusual_spending(transactions: list[Transaction], multiplier: float = 3.0) -> list[Transaction]:
    """Flag transactions that are unusually large compared to category average."""
    by_category = defaultdict(list)
    for t in transactions:
        by_category[t.category].append(abs(t.amount))

    unusual = []
    for t in transactions:
        amounts = by_category[t.category]
        if len(amounts) >= 3:
            avg = sum(amounts) / len(amounts)
            if abs(t.amount) > avg * multiplier:
                unusual.append(t)

    return unusual


def parse_bank_csv(content: str, date_col: str = "Date",
                   desc_col: str = "Description", amount_col: str = "Amount",
                   currency: str = "USD") -> list[Transaction]:
    """Parse a bank statement CSV into categorized transactions."""
    reader = csv.DictReader(io.StringIO(content))
    transactions = []

    for row in reader:
        date = row.get(date_col, "").strip()
        desc = row.get(desc_col, "").strip()
        amount_str = row.get(amount_col, "0").strip()

        # Clean amount: remove $ and commas
        amount_str = amount_str.replace("$", "").replace(",", "")
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0

        category = categorize_transaction(desc)
        t = Transaction(
            date=date,
            description=desc,
            amount=amount,
            category=category,
            currency=currency,
            raw_line=json.dumps(row),
        )
        transactions.append(t)

    # Detect recurring
    transactions = detect_recurring(transactions)

    return transactions


def generate_expense_report(transactions: list[Transaction]) -> dict:
    """Generate a comprehensive expense breakdown report."""
    total = sum(abs(t.amount) for t in transactions)
    by_category = defaultdict(lambda: {"total": 0.0, "count": 0, "transactions": []})

    for t in transactions:
        by_category[t.category]["total"] += abs(t.amount)
        by_category[t.category]["count"] += 1

    # Convert to regular dict with percentages
    report_categories = {}
    for cat, data in sorted(by_category.items(), key=lambda x: x[1]["total"], reverse=True):
        pct = round((data["total"] / total) * 100, 1) if total > 0 else 0
        report_categories[cat] = {
            "total": round(data["total"], 2),
            "count": data["count"],
            "percentage": pct,
        }

    recurring = [t for t in transactions if t.is_recurring]
    recurring_total = sum(abs(t.amount) for t in recurring)

    unusual = flag_unusual_spending(transactions)

    return {
        "total_spending": round(total, 2),
        "transaction_count": len(transactions),
        "categories": report_categories,
        "recurring_count": len(recurring),
        "recurring_total": round(recurring_total, 2),
        "unusual_count": len(unusual),
    }


def format_report_markdown(report: dict, transactions: list[Transaction] | None = None) -> str:
    """Format expense report as Markdown."""
    lines = [
        "# Expense Report",
        "",
        f"**Total Spending:** ${report['total_spending']:,.2f}",
        f"**Transactions:** {report['transaction_count']}",
        f"**Recurring:** {report['recurring_count']} (${report['recurring_total']:,.2f})",
        "",
        "## By Category",
        "| Category | Amount | Count | % |",
        "|----------|--------|-------|---|",
    ]

    for cat, data in report["categories"].items():
        lines.append(f"| {cat} | ${data['total']:,.2f} | {data['count']} | {data['percentage']}% |")

    lines.append("")

    if report.get("unusual_count", 0) > 0:
        lines.append(f"⚠️ **{report['unusual_count']} unusual transaction(s)** flagged")
        lines.append("")

    if transactions:
        recurring = [t for t in transactions if t.is_recurring]
        if recurring:
            lines.append("## Recurring Subscriptions")
            seen = set()
            for t in recurring:
                key = f"{t.description}|{t.amount}"
                if key not in seen:
                    seen.add(key)
                    lines.append(f"- **{t.description}** — ${abs(t.amount):,.2f}/mo")
            lines.append("")

    return "\n".join(lines)
