"""Tests for pricing module."""
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.pricing import (
    PRICING, get_model_price, get_provider_models,
    list_providers, list_models, find_cheapest_alternative,
)


def test_pricing_data_exists():
    """Pricing database is not empty."""
    assert len(PRICING) > 20


def test_all_entries_have_required_fields():
    """Every model has input, output, and provider."""
    for model, data in PRICING.items():
        assert "input" in data, f"{model} missing input price"
        assert "output" in data, f"{model} missing output price"
        assert "provider" in data, f"{model} missing provider"
        assert data["input"] >= 0
        assert data["output"] >= 0


def test_get_model_price_known():
    """Returns pricing for known model."""
    price = get_model_price("gpt-4o")
    assert price is not None
    assert price["input"] == 2.50
    assert price["provider"] == "OpenAI"


def test_get_model_price_unknown():
    """Returns None for unknown model."""
    assert get_model_price("nonexistent-model-99") is None


def test_get_provider_models():
    """Filters models by provider."""
    models = get_provider_models("OpenAI")
    assert len(models) >= 5
    assert all(v["provider"] == "OpenAI" for v in models.values())


def test_get_provider_models_case_insensitive():
    """Provider lookup is case-insensitive."""
    models = get_provider_models("openai")
    assert len(models) >= 5


def test_list_providers():
    """Lists all unique providers."""
    providers = list_providers()
    assert "OpenAI" in providers
    assert "Anthropic" in providers
    assert "Google" in providers
    assert len(providers) >= 4


def test_list_models():
    """Lists all model names."""
    models = list_models()
    assert "gpt-4o" in models
    assert "claude-3.5-sonnet" in models
    assert len(models) == len(PRICING)


def test_find_cheapest_alternative():
    """Finds cheaper alternatives to expensive model."""
    alternatives = find_cheapest_alternative("gpt-4-turbo")
    assert len(alternatives) > 0
    # All alternatives should be cheaper
    for a in alternatives:
        assert a["input_price"] <= 10.00  # gpt-4-turbo input price
        assert a["savings_percent"] >= 0


def test_find_cheapest_unknown_model():
    """Returns empty for unknown model."""
    assert find_cheapest_alternative("nonexistent") == []
