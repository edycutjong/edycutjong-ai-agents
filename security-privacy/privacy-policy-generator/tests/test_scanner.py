import pytest
from pathlib import Path
from agent.scanner import CodeScanner

def test_scan_pii(tmp_path):
    """Test that scanner detects PII."""
    d = tmp_path / "src"
    d.mkdir()
    p = d / "user_data.py"
    p.write_text("email_address = 'user@example.com'")

    scanner = CodeScanner(str(tmp_path))
    results = scanner.scan()

    assert "email" in results["pii"]
    assert len(results["details"]["email"]) == 1
    # Check relative path match
    assert "src/user_data.py" in results["details"]["email"][0] or "src\\user_data.py" in results["details"]["email"][0]

def test_scan_multiple_pii(tmp_path):
    """Test detecting multiple PII types in one file."""
    p = tmp_path / "config.json"
    p.write_text('{"password": "secret", "location": "US"}')

    scanner = CodeScanner(str(tmp_path))
    results = scanner.scan()

    assert "password" in results["pii"]
    assert "location" in results["pii"]

def test_scan_third_party(tmp_path):
    """Test detecting third-party services."""
    p = tmp_path / "index.html"
    p.write_text('<script src="https://js.stripe.com/v3/"></script>')

    scanner = CodeScanner(str(tmp_path))
    results = scanner.scan()

    assert "Stripe" in results["third_parties"]

def test_skip_ignored_files(tmp_path):
    """Test that scanner skips ignored files and directories."""
    # Create ignored directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("email = git@github.com")

    # Create ignored file extension
    img_file = tmp_path / "image.png"
    img_file.write_text("email")

    scanner = CodeScanner(str(tmp_path))
    results = scanner.scan()

    assert "email" not in results["pii"]
    assert results["files_scanned"] == 0

def test_scan_empty_dir(tmp_path):
    """Test scanning an empty directory."""
    scanner = CodeScanner(str(tmp_path))
    results = scanner.scan()

    assert results["files_scanned"] == 0
    assert not results["pii"]
    assert not results["third_parties"]
