"""Invoice generation engine."""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from config import Config


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    tax_rate: float = 0.0

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    @property
    def tax_amount(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax_amount, 2)

    def to_dict(self) -> dict:
        return {**asdict(self), "subtotal": self.subtotal, "tax_amount": self.tax_amount, "total": self.total}


@dataclass
class Invoice:
    invoice_number: str = ""
    date: str = ""
    due_date: str = ""
    from_name: str = ""
    from_address: str = ""
    to_name: str = ""
    to_address: str = ""
    items: list[LineItem] = field(default_factory=list)
    currency: str = "USD"
    notes: str = ""
    status: str = "draft"  # draft, sent, paid, overdue

    def __post_init__(self):
        if not self.invoice_number:
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")
        if not self.due_date:
            self.due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    @property
    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    @property
    def tax_total(self) -> float:
        return round(sum(item.tax_amount for item in self.items), 2)

    @property
    def grand_total(self) -> float:
        return round(self.subtotal + self.tax_total, 2)

    def add_item(self, description: str, quantity: float, unit_price: float, tax_rate: float = 0.0):
        self.items.append(LineItem(description, quantity, unit_price, tax_rate))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["items"] = [item.to_dict() for item in self.items]
        d["subtotal"] = self.subtotal
        d["tax_total"] = self.tax_total
        d["grand_total"] = self.grand_total
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Invoice":
        items = [LineItem(**{k: v for k, v in i.items() if k in LineItem.__dataclass_fields__})
                 for i in data.pop("items", [])]
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        inv = cls(**filtered)
        inv.items = items
        return inv


class InvoiceStorage:
    def __init__(self, filepath: str | None = None):
        self.filepath = filepath or Config.STORAGE_FILE
        self._ensure()

    def _ensure(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w") as f: json.dump([], f)

    def _load(self) -> list[dict]:
        try:
            with open(self.filepath) as f: return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): return []

    def _save(self, data): 
        with open(self.filepath, "w") as f: json.dump(data, f, indent=2)

    def save(self, invoice: Invoice) -> str:
        data = self._load()
        data.append(invoice.to_dict())
        self._save(data)
        return invoice.invoice_number

    def get_all(self) -> list[Invoice]:
        return [Invoice.from_dict(d) for d in self._load()]

    def get_by_number(self, number: str) -> Invoice | None:
        for d in self._load():
            if d.get("invoice_number") == number: return Invoice.from_dict(d)
        return None

    def get_by_status(self, status: str) -> list[Invoice]:
        return [i for i in self.get_all() if i.status == status]


def format_invoice_markdown(invoice: Invoice) -> str:
    """Format invoice as professional Markdown."""
    sym = {"USD": "$", "EUR": "€", "GBP": "£"}.get(invoice.currency, invoice.currency + " ")
    lines = [
        f"# INVOICE {invoice.invoice_number}",
        "",
        f"**Date:** {invoice.date} | **Due:** {invoice.due_date} | **Status:** {invoice.status.upper()}",
        "",
        "---",
        "",
        f"**From:** {invoice.from_name}",
        f"{invoice.from_address}" if invoice.from_address else "",
        "",
        f"**To:** {invoice.to_name}",
        f"{invoice.to_address}" if invoice.to_address else "",
        "",
        "---",
        "",
        "| Description | Qty | Unit Price | Tax | Total |",
        "|-------------|-----|-----------|-----|-------|",
    ]

    for item in invoice.items:
        tax_str = f"{item.tax_rate*100:.0f}%" if item.tax_rate > 0 else "—"
        lines.append(
            f"| {item.description} | {item.quantity} | {sym}{item.unit_price:,.2f} | {tax_str} | {sym}{item.total:,.2f} |"
        )

    lines.extend([
        "",
        f"**Subtotal:** {sym}{invoice.subtotal:,.2f}",
        f"**Tax:** {sym}{invoice.tax_total:,.2f}",
        f"### Total: {sym}{invoice.grand_total:,.2f}",
    ])

    if invoice.notes:
        lines.extend(["", f"**Notes:** {invoice.notes}"])

    return "\n".join(lines)


def format_invoice_text(invoice: Invoice) -> str:
    """Format as plain text for email/terminal."""
    sym = {"USD": "$", "EUR": "€", "GBP": "£"}.get(invoice.currency, invoice.currency + " ")
    lines = [
        f"INVOICE {invoice.invoice_number}",
        f"Date: {invoice.date}  Due: {invoice.due_date}",
        f"From: {invoice.from_name}",
        f"To: {invoice.to_name}",
        "-" * 50,
    ]
    for item in invoice.items:
        lines.append(f"  {item.description:<30} {item.quantity:>5} x {sym}{item.unit_price:>8.2f} = {sym}{item.total:>8.2f}")
    lines.extend([
        "-" * 50,
        f"  {'Subtotal':<30} {sym}{invoice.subtotal:>20.2f}",
        f"  {'Tax':<30} {sym}{invoice.tax_total:>20.2f}",
        f"  {'TOTAL':<30} {sym}{invoice.grand_total:>20.2f}",
    ])
    return "\n".join(lines)
