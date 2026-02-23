import json
import os
import sys
import pytest

# Add parent directory to path to allow importing 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.locales import LocaleManager

@pytest.fixture
def locale_dir(tmp_path):
    d = tmp_path / "locales"
    d.mkdir()

    en = d / "en.json"
    with open(en, 'w', encoding='utf-8') as f:
        json.dump({
            "common": {
                "hello": "Hello",
                "nested": {
                    "key": "Value"
                }
            },
            "flat_key": "Flat"
        }, f)

    fr = d / "fr.json"
    with open(fr, 'w', encoding='utf-8') as f:
        json.dump({
            "common": {
                "hello": "Bonjour"
            }
        }, f)

    return d

def test_load_locales(locale_dir):
    manager = LocaleManager(str(locale_dir))
    locales = manager.load_locales()

    assert "en" in locales
    assert "fr" in locales

    assert locales["en"]["common.hello"] == "Hello"
    assert locales["en"]["common.nested.key"] == "Value"
    assert locales["en"]["flat_key"] == "Flat"

    assert locales["fr"]["common.hello"] == "Bonjour"
    assert "common.nested.key" not in locales["fr"]

def test_save_locale(tmp_path):
    manager = LocaleManager(str(tmp_path))

    data = {
        "new.key": "New Value",
        "nested.item": "Item"
    }

    manager.save_locale("es", data)

    filepath = tmp_path / "es.json"
    assert filepath.exists()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = json.load(f)

    assert content["new"]["key"] == "New Value"
    assert content["nested"]["item"] == "Item"

def test_flatten_unflatten():
    nested = {"a": {"b": "c"}, "d": "e"}
    flat = LocaleManager.flatten_dict(nested)
    assert flat == {"a.b": "c", "d": "e"}

    unflat = LocaleManager.unflatten_dict(flat)
    assert unflat == nested

def test_unflatten_conflict():
    # Conflict: a='x', a.b='y'
    # Should resolve by making 'a' a dict, losing 'x'
    flat = {"a": "x", "a.b": "y"}
    # Sort keys to ensure deterministic behavior if iteration order matters (though dicts are ordered in py3.7+)
    # However, 'a' comes before 'a.b' lexicographically.
    unflat = LocaleManager.unflatten_dict(flat)

    assert isinstance(unflat["a"], dict)
    assert unflat["a"]["b"] == "y"
