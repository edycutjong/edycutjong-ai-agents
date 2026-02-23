import pytest
from pathlib import Path
from tools.file_scanner import AssetScanner
from tools.code_scanner import CodeScanner

def test_asset_scanner(tmp_path):
    # Create structure
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    (img_dir / "test.png").touch()
    (img_dir / "test.jpg").touch()
    (img_dir / "ignored.txt").touch()

    # Create ignored directory
    ignored_dir = tmp_path / "node_modules"
    ignored_dir.mkdir()
    (ignored_dir / "bad.png").touch()

    scanner = AssetScanner(str(tmp_path))
    assets = scanner.scan()

    asset_names = {p.name for p in assets}
    assert "test.png" in asset_names
    assert "test.jpg" in asset_names
    assert "ignored.txt" not in asset_names
    assert "bad.png" not in asset_names

def test_code_scanner(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()

    code_file = src_dir / "index.js"
    # Testing exact match with extension
    code_file.write_text("import logo from './logo.png';")

    asset1 = tmp_path / "logo.png"
    asset2 = tmp_path / "unused.png"

    scanner = CodeScanner(str(tmp_path))
    assets = [asset1, asset2]

    refs = scanner.find_references(assets)

    assert len(refs[asset1]) == 1
    assert list(refs[asset1])[0].name == "index.js"
    assert len(refs[asset2]) == 0

def test_code_scanner_extensionless(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()

    code_file = src_dir / "App.js"
    # Testing extensionless import
    code_file.write_text("import logo from './logo';")

    asset1 = tmp_path / "logo.png"
    asset2 = tmp_path / "other.jpg"

    scanner = CodeScanner(str(tmp_path))
    assets = [asset1, asset2]

    refs = scanner.find_references(assets)

    assert len(refs[asset1]) == 1
    assert list(refs[asset1])[0].name == "App.js"
    assert len(refs[asset2]) == 0
