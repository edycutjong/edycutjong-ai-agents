"""Tests for Invoice Generator."""
import sys, os, json, tempfile, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.invoice import LineItem, Invoice, InvoiceStorage, format_invoice_markdown, format_invoice_text

@pytest.fixture
def temp_path():
    with tempfile.TemporaryDirectory() as d: yield os.path.join(d, "inv.json")

@pytest.fixture
def sample_invoice():
    inv = Invoice(from_name="Acme Corp", to_name="Client Inc", currency="USD")
    inv.add_item("Web Development", 40, 150.00) 
    inv.add_item("Hosting", 1, 99.00, tax_rate=0.10)
    return inv

# --- Line Item Tests ---
def test_line_item_subtotal():
    item = LineItem("Work", 10, 50.0)
    assert item.subtotal == 500.0

def test_line_item_tax():
    item = LineItem("Work", 10, 100.0, tax_rate=0.1)
    assert item.tax_amount == 100.0
    assert item.total == 1100.0

def test_line_item_no_tax():
    item = LineItem("Work", 5, 200.0)
    assert item.tax_amount == 0.0
    assert item.total == 1000.0

# --- Invoice Tests ---
def test_invoice_auto_number():
    inv = Invoice()
    assert inv.invoice_number.startswith("INV-")

def test_invoice_auto_dates():
    inv = Invoice()
    assert inv.date != ""
    assert inv.due_date != ""

def test_invoice_subtotal(sample_invoice):
    assert sample_invoice.subtotal == 6099.0  # 40*150 + 1*99

def test_invoice_tax(sample_invoice):
    assert sample_invoice.tax_total == 9.9  # 99*0.10

def test_invoice_grand_total(sample_invoice):
    assert sample_invoice.grand_total == 6108.9

def test_invoice_add_item():
    inv = Invoice()
    inv.add_item("Test", 2, 50.0)
    assert len(inv.items) == 1
    assert inv.subtotal == 100.0

def test_invoice_to_dict(sample_invoice):
    d = sample_invoice.to_dict()
    assert "grand_total" in d
    assert "items" in d
    assert len(d["items"]) == 2

def test_invoice_from_dict(sample_invoice):
    d = sample_invoice.to_dict()
    restored = Invoice.from_dict(d)
    assert restored.grand_total == sample_invoice.grand_total
    assert len(restored.items) == 2

# --- Storage Tests ---
def test_save_and_retrieve(temp_path, sample_invoice):
    s = InvoiceStorage(filepath=temp_path)
    s.save(sample_invoice)
    invoices = s.get_all()
    assert len(invoices) == 1

def test_get_by_number(temp_path, sample_invoice):
    s = InvoiceStorage(filepath=temp_path)
    s.save(sample_invoice)
    found = s.get_by_number(sample_invoice.invoice_number)
    assert found is not None
    assert found.to_name == "Client Inc"

def test_get_by_status(temp_path, sample_invoice):
    s = InvoiceStorage(filepath=temp_path)
    s.save(sample_invoice)
    drafts = s.get_by_status("draft")
    assert len(drafts) == 1

# --- Format Tests ---
def test_markdown_format(sample_invoice):
    md = format_invoice_markdown(sample_invoice)
    assert "INVOICE" in md
    assert "Web Development" in md
    assert "Total" in md

def test_text_format(sample_invoice):
    txt = format_invoice_text(sample_invoice)
    assert "INVOICE" in txt
    assert "Web Development" in txt

def test_markdown_currency_symbol():
    inv = Invoice(currency="EUR")
    inv.add_item("Work", 1, 100)
    md = format_invoice_markdown(inv)
    assert "€" in md
