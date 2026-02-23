"""Pricing data for major LLM providers.

Prices are in USD per 1M tokens (as of Feb 2026).
Source: Official pricing pages for each provider.
"""

# Format: { model_name: { "input": price_per_1M_input_tokens, "output": price_per_1M_output_tokens } }

PRICING = {
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00, "provider": "OpenAI"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "provider": "OpenAI"},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00, "provider": "OpenAI"},
    "gpt-4": {"input": 30.00, "output": 60.00, "provider": "OpenAI"},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50, "provider": "OpenAI"},
    "o1": {"input": 15.00, "output": 60.00, "provider": "OpenAI"},
    "o1-mini": {"input": 3.00, "output": 12.00, "provider": "OpenAI"},
    "o3-mini": {"input": 1.10, "output": 4.40, "provider": "OpenAI"},

    # Anthropic
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00, "provider": "Anthropic"},
    "claude-3.5-haiku": {"input": 0.80, "output": 4.00, "provider": "Anthropic"},
    "claude-3-opus": {"input": 15.00, "output": 75.00, "provider": "Anthropic"},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00, "provider": "Anthropic"},
    "claude-3-haiku": {"input": 0.25, "output": 1.25, "provider": "Anthropic"},

    # Google
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40, "provider": "Google"},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00, "provider": "Google"},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30, "provider": "Google"},

    # Mistral
    "mistral-large": {"input": 2.00, "output": 6.00, "provider": "Mistral"},
    "mistral-small": {"input": 0.20, "output": 0.60, "provider": "Mistral"},
    "codestral": {"input": 0.30, "output": 0.90, "provider": "Mistral"},

    # Meta (via providers)
    "llama-3.1-405b": {"input": 3.00, "output": 3.00, "provider": "Meta"},
    "llama-3.1-70b": {"input": 0.35, "output": 0.40, "provider": "Meta"},
    "llama-3.1-8b": {"input": 0.05, "output": 0.08, "provider": "Meta"},
}


def get_model_price(model: str) -> dict | None:
    """Get pricing for a specific model. Returns None if not found."""
    return PRICING.get(model)


def get_provider_models(provider: str) -> dict:
    """Get all models for a specific provider."""
    return {k: v for k, v in PRICING.items() if v["provider"].lower() == provider.lower()}


def list_providers() -> list[str]:
    """List all unique providers."""
    return sorted(set(v["provider"] for v in PRICING.values()))


def list_models() -> list[str]:
    """List all available models."""
    return sorted(PRICING.keys())


def find_cheapest_alternative(model: str, max_price_ratio: float = 1.0) -> list[dict]:
    """Find cheaper alternatives to a given model.

    Args:
        model: The current model name.
        max_price_ratio: Maximum price as ratio of current model (1.0 = same price).

    Returns:
        List of cheaper models sorted by input cost.
    """
    current = PRICING.get(model)
    if not current:
        return []

    max_input = current["input"] * max_price_ratio
    alternatives = []
    for name, price in PRICING.items():
        if name != model and price["input"] <= max_input:
            savings_pct = round((1 - price["input"] / current["input"]) * 100, 1)
            alternatives.append({
                "model": name,
                "provider": price["provider"],
                "input_price": price["input"],
                "output_price": price["output"],
                "savings_percent": savings_pct,
            })
    return sorted(alternatives, key=lambda x: x["input_price"])
