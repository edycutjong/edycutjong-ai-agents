"""Data faker — generate realistic fake data for testing and development."""
from __future__ import annotations
import random, string, json, uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack", "Kate", "Leo", "Maya", "Noah", "Olivia", "Paul", "Quinn", "Ryan", "Sara", "Tom"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Moore", "Jackson", "White", "Harris", "Clark", "Lewis", "Young"]
DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "company.io", "example.com"]
CITIES = ["New York", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto", "Mumbai", "Seoul", "Dubai"]
COUNTRIES = ["US", "UK", "JP", "FR", "DE", "AU", "CA", "IN", "KR", "AE"]
COMPANIES = ["Acme Corp", "Globex", "Initech", "Umbrella", "Stark Industries", "Wayne Enterprises", "Cyberdyne", "Oscorp", "LexCorp", "Aperture Science"]
PRODUCTS = ["Widget Pro", "DataSync", "CloudBase", "API Gateway", "SmartDash", "LogFlow", "MetricHub", "CodePilot", "DevOps Suite", "Neural Engine"]

def fake_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def fake_email(name: str = "") -> str:
    if name:
        parts = name.lower().split()
        user = f"{parts[0]}.{parts[-1]}" if len(parts) > 1 else parts[0]
    else:
        user = f"user{random.randint(100,999)}"
    return f"{user}@{random.choice(DOMAINS)}"

def fake_phone() -> str:
    return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

def fake_uuid() -> str: return str(uuid.uuid4())
def fake_date(start_year: int = 2020, end_year: int = 2025) -> str:
    start = datetime(start_year, 1, 1)
    days = (datetime(end_year, 12, 31) - start).days
    return (start + timedelta(days=random.randint(0, days))).strftime("%Y-%m-%d")

def fake_address() -> dict:
    return {"street": f"{random.randint(1,999)} {random.choice(['Main','Oak','Elm','Park','Cedar'])} St", "city": random.choice(CITIES), "country": random.choice(COUNTRIES), "zip": f"{random.randint(10000,99999)}"}

def fake_user() -> dict:
    name = fake_name()
    return {"id": fake_uuid(), "name": name, "email": fake_email(name), "phone": fake_phone(), "address": fake_address(), "created_at": fake_date(), "active": random.choice([True, True, True, False])}

def fake_product() -> dict:
    return {"id": fake_uuid(), "name": random.choice(PRODUCTS), "price": round(random.uniform(9.99, 499.99), 2), "category": random.choice(["Software", "Hardware", "Service", "Subscription"]), "in_stock": random.choice([True, True, False]), "rating": round(random.uniform(1, 5), 1)}

def fake_order() -> dict:
    return {"id": fake_uuid(), "user_id": fake_uuid(), "product": random.choice(PRODUCTS), "quantity": random.randint(1, 10), "total": round(random.uniform(10, 2000), 2), "status": random.choice(["pending", "shipped", "delivered", "cancelled"]), "date": fake_date()}

GENERATORS = {"user": fake_user, "product": fake_product, "order": fake_order}

def generate_fake_data(schema: str, count: int = 10) -> list[dict]:
    gen = GENERATORS.get(schema.lower(), fake_user)
    return [gen() for _ in range(count)]

def export_json(data: list[dict]) -> str: return json.dumps(data, indent=2)

def export_csv(data: list[dict]) -> str:
    if not data: return ""
    flat = []
    for row in data:
        flat_row = {}
        for k, v in row.items():
            if isinstance(v, dict):
                for sk, sv in v.items(): flat_row[f"{k}_{sk}"] = sv
            else: flat_row[k] = v
        flat.append(flat_row)
    headers = list(flat[0].keys())
    lines = [",".join(headers)]
    for row in flat:
        lines.append(",".join(str(row.get(h, "")) for h in headers))
    return "\n".join(lines)

def list_schemas() -> list[str]: return sorted(GENERATORS.keys())
