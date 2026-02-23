#!/usr/bin/env python3
"""CLI for Invoice Generator."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.invoice import Invoice, InvoiceStorage, format_invoice_markdown, format_invoice_text

def cmd_create(args):
    inv = Invoice(from_name=args.from_name or "My Company", to_name=args.to_name or "Client", currency=args.currency or "USD", notes=args.notes or "")
    if args.items:
        for item_str in args.items:
            parts = item_str.split(",")
            inv.add_item(parts[0], float(parts[1]), float(parts[2]), float(parts[3]) if len(parts) > 3 else 0.0)
    storage = InvoiceStorage()
    storage.save(inv)
    if args.markdown: print(format_invoice_markdown(inv))
    elif args.json: print(json.dumps(inv.to_dict(), indent=2))
    else: print(format_invoice_text(inv))
    print(f"\n✅ Saved: {inv.invoice_number}")

def cmd_list(args):
    storage = InvoiceStorage()
    invoices = storage.get_by_status(args.status) if args.status else storage.get_all()
    for inv in invoices:
        sym = {"USD": "$", "EUR": "€"}.get(inv.currency, inv.currency)
        print(f"  {inv.invoice_number}  {inv.date}  {inv.to_name:<20}  {sym}{inv.grand_total:>10.2f}  [{inv.status}]")

def cmd_show(args):
    storage = InvoiceStorage()
    inv = storage.get_by_number(args.number)
    if not inv: print("Not found"); sys.exit(1)
    if args.markdown: print(format_invoice_markdown(inv))
    else: print(format_invoice_text(inv))

def main():
    parser = argparse.ArgumentParser(description="Invoice Generator")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create"); p.add_argument("--from-name"); p.add_argument("--to-name"); p.add_argument("--items", nargs="*", help="desc,qty,price[,tax]"); p.add_argument("--currency", default="USD"); p.add_argument("--notes"); p.add_argument("--markdown", action="store_true"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_create)
    p = sub.add_parser("list"); p.add_argument("--status"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("show"); p.add_argument("number"); p.add_argument("--markdown", action="store_true"); p.set_defaults(func=cmd_show)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
