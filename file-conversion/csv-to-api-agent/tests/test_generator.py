import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.generator import Generator

def test_generate():
    schema = [
        {"original_name": "name", "name": "name", "type": "str"},
        {"original_name": "age", "name": "age", "type": "int"}
    ]

    generator = Generator()
    files = generator.generate(schema)

    assert "app.py" in files
    assert "models.py" in files
    assert "requirements.txt" in files

    assert "class Item(db.Model):" in files["models.py"]
    # Check if mappings worked
    assert "name = db.Column(db.String(255))" in files["models.py"]
    assert "age = db.Column(db.Integer)" in files["models.py"]

def test_generate_with_csv():
    schema = [{"original_name": "name", "name": "name", "type": "str"}]
    csv_bytes = b"name\nAlice"
    generator = Generator()
    files = generator.generate(schema, csv_data=csv_bytes)

    assert files['data.csv'] == csv_bytes
