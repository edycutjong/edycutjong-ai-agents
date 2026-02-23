"""Tests for Data Faker."""
import sys, os, pytest, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.faker import fake_name, fake_email, fake_phone, fake_uuid, fake_date, fake_address, fake_user, fake_product, fake_order, generate_fake_data, export_json, export_csv, list_schemas

def test_fake_name():
    n = fake_name()
    assert " " in n and len(n) > 3

def test_fake_email():
    assert "@" in fake_email()

def test_fake_email_from_name():
    e = fake_email("Alice Smith")
    assert "alice" in e and "@" in e

def test_fake_phone():
    p = fake_phone()
    assert p.startswith("+1-")

def test_fake_uuid():
    u = fake_uuid()
    assert len(u) == 36 and "-" in u

def test_fake_date():
    d = fake_date()
    assert len(d) == 10 and d[4] == "-"

def test_fake_address():
    a = fake_address()
    assert "city" in a and "country" in a

def test_fake_user():
    u = fake_user()
    assert "name" in u and "email" in u and "id" in u

def test_fake_product():
    p = fake_product()
    assert "name" in p and "price" in p and p["price"] > 0

def test_fake_order():
    o = fake_order()
    assert "status" in o and "total" in o

def test_generate_users():
    data = generate_fake_data("user", 5)
    assert len(data) == 5

def test_generate_products():
    data = generate_fake_data("product", 3)
    assert len(data) == 3

def test_generate_orders():
    data = generate_fake_data("order", 7)
    assert len(data) == 7

def test_export_json():
    data = generate_fake_data("user", 2)
    j = export_json(data)
    parsed = json.loads(j)
    assert len(parsed) == 2

def test_export_csv():
    data = generate_fake_data("product", 3)
    csv = export_csv(data)
    lines = csv.strip().split("\n")
    assert len(lines) == 4  # header + 3 rows

def test_list_schemas():
    s = list_schemas()
    assert "user" in s and "product" in s and "order" in s

def test_unique_ids():
    data = generate_fake_data("user", 10)
    ids = [d["id"] for d in data]
    assert len(set(ids)) == 10
