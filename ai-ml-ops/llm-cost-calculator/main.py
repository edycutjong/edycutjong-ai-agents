#!/usr/bin/env python3
"""CLI for LLM Cost Calculator.

Usage:
    python main.py calc gpt-4o 1000 500         # Calculate single call cost
    python main.py compare 1000 500              # Compare all models
    python main.py cheapest gpt-4-turbo          # Find cheaper alternatives
    python main.py log gpt-4o 1000 500 --label chat  # Log usage
    python main.py report                        # Generate cost report
    python main.py forecast --days 7             # Forecast monthly cost
    python main.py budget 50.00                  # Check against budget
    python main.py models                        # List all models
    python main.py providers                     # List all providers
"""
import argparse
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from agent.pricing import (
    PRICING, list_models, list_providers, get_provider_models,
    find_cheapest_alternative, get_model_price,
)
from agent.calculator import (
    UsageEntry, calculate_cost, generate_cost_report,
    forecast_monthly_cost, check_budget, format_report_markdown,
)
from agent.storage import UsageStorage


def cmd_calc(args):
    """Calculate cost for a single API call."""
    result = calculate_cost(args.model, args.input_tokens, args.output_tokens)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return
    print(f"Model:         {result['model']} ({result['provider']})")
    print(f"Input:         {result['input_tokens']:,} tokens → ${result['input_cost']:.6f}")
    print(f"Output:        {result['output_tokens']:,} tokens → ${result['output_cost']:.6f}")
    print(f"Total Cost:    ${result['total_cost']:.6f}")


def cmd_compare(args):
    """Compare costs across all models for given token counts."""
    print(f"Cost comparison for {args.input_tokens:,} input + {args.output_tokens:,} output tokens:\n")
    print(f"{'Model':<25} {'Provider':<12} {'Cost':>12}")
    print("-" * 52)

    results = []
    for model in sorted(PRICING.keys()):
        result = calculate_cost(model, args.input_tokens, args.output_tokens)
        results.append(result)

    results.sort(key=lambda x: x["total_cost"])
    for r in results:
        print(f"{r['model']:<25} {r['provider']:<12} ${r['total_cost']:>10.6f}")


def cmd_cheapest(args):
    """Find cheaper alternatives to a model."""
    alternatives = find_cheapest_alternative(args.model)
    if not alternatives:
        print(f"No cheaper alternatives found for {args.model}.")
        return

    current = get_model_price(args.model)
    print(f"Cheaper alternatives to {args.model} (${current['input']}/M in, ${current['output']}/M out):\n")
    print(f"{'Model':<25} {'Provider':<12} {'Input/M':>10} {'Output/M':>10} {'Savings':>8}")
    print("-" * 68)
    for a in alternatives:
        print(f"{a['model']:<25} {a['provider']:<12} ${a['input_price']:>8.3f} ${a['output_price']:>8.3f} {a['savings_percent']:>6.1f}%")


def cmd_log(args):
    """Log a usage entry."""
    storage = UsageStorage()
    entry = UsageEntry(
        model=args.model,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        timestamp=datetime.now().isoformat(),
        label=args.label or "",
    )
    storage.add_entry(entry)
    cost = calculate_cost(args.model, args.input_tokens, args.output_tokens)
    print(f"✅ Logged: {args.model} ({args.input_tokens:,} in / {args.output_tokens:,} out) = ${cost['total_cost']:.6f}")
    if args.label:
        print(f"   Label: {args.label}")


def cmd_report(args):
    """Generate cost report from logged usage."""
    storage = UsageStorage()
    entries = storage.get_all_entries()
    if not entries:
        print("No usage data logged yet. Use 'log' command to add entries.")
        return

    report = generate_cost_report(entries)

    if args.markdown:
        print(format_report_markdown(report))
    else:
        print(f"Total Cost:    ${report['total_cost']:.4f}")
        print(f"Total Calls:   {report['total_calls']}")
        print(f"Input Tokens:  {report['total_input_tokens']:,}")
        print(f"Output Tokens: {report['total_output_tokens']:,}")
        print()
        print("By Model:")
        for model, data in sorted(report["by_model"].items(), key=lambda x: x[1]["cost"], reverse=True):
            print(f"  {model:<25} {data['calls']} calls  ${data['cost']:.4f}")
        print()
        print("By Provider:")
        for provider, data in sorted(report["by_provider"].items(), key=lambda x: x[1]["cost"], reverse=True):
            print(f"  {provider:<15} {data['calls']} calls  ${data['cost']:.4f}")


def cmd_forecast(args):
    """Forecast monthly costs."""
    storage = UsageStorage()
    entries = storage.get_all_entries()
    if not entries:
        print("No usage data logged yet.")
        return

    forecast = forecast_monthly_cost(entries, days_in_window=args.days)
    print(f"Forecast (based on {args.days} days of data):")
    print(f"  Daily average:      ${forecast['daily_avg']:.4f}")
    print(f"  Weekly projection:  ${forecast['weekly_projection']:.4f}")
    print(f"  Monthly projection: ${forecast['monthly_projection']:.4f}")


def cmd_budget(args):
    """Check spend against budget."""
    storage = UsageStorage()
    entries = storage.get_all_entries()
    result = check_budget(entries, args.amount)

    status = "🔴 OVER BUDGET" if result["over_budget"] else "🟢 Within budget"
    print(f"Budget Check: {status}")
    print(f"  Spend:     ${result['spend']:.4f}")
    print(f"  Budget:    ${result['budget']:.2f}")
    print(f"  Remaining: ${result['remaining']:.4f}")
    print(f"  Usage:     {result['usage_percent']:.1f}%")


def cmd_models(args):
    """List all available models."""
    print(f"{'Model':<25} {'Provider':<12} {'Input/M':>10} {'Output/M':>10}")
    print("-" * 60)
    for model in list_models():
        p = PRICING[model]
        print(f"{model:<25} {p['provider']:<12} ${p['input']:>8.3f} ${p['output']:>8.3f}")
    print(f"\nTotal: {len(PRICING)} models across {len(list_providers())} providers")


def cmd_providers(args):
    """List all providers and their model counts."""
    for provider in list_providers():
        models = get_provider_models(provider)
        print(f"\n{provider} ({len(models)} models):")
        for name, price in sorted(models.items(), key=lambda x: x[1]["input"]):
            print(f"  {name:<25} ${price['input']:.3f} / ${price['output']:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="LLM Cost Calculator — Track and optimize AI spending.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # calc
    p = sub.add_parser("calc", help="Calculate cost for a single call")
    p.add_argument("model", help="Model name (e.g. gpt-4o)")
    p.add_argument("input_tokens", type=int, help="Input token count")
    p.add_argument("output_tokens", type=int, help="Output token count")
    p.set_defaults(func=cmd_calc)

    # compare
    p = sub.add_parser("compare", help="Compare all models for given tokens")
    p.add_argument("input_tokens", type=int)
    p.add_argument("output_tokens", type=int)
    p.set_defaults(func=cmd_compare)

    # cheapest
    p = sub.add_parser("cheapest", help="Find cheaper alternatives")
    p.add_argument("model", help="Current model")
    p.set_defaults(func=cmd_cheapest)

    # log
    p = sub.add_parser("log", help="Log a usage entry")
    p.add_argument("model")
    p.add_argument("input_tokens", type=int)
    p.add_argument("output_tokens", type=int)
    p.add_argument("--label", help="Usage label (e.g. chat, summarization)")
    p.set_defaults(func=cmd_log)

    # report
    p = sub.add_parser("report", help="Generate cost report")
    p.add_argument("--markdown", action="store_true", help="Output as Markdown")
    p.set_defaults(func=cmd_report)

    # forecast
    p = sub.add_parser("forecast", help="Forecast monthly costs")
    p.add_argument("--days", type=int, default=7, help="Days of data to base forecast on")
    p.set_defaults(func=cmd_forecast)

    # budget
    p = sub.add_parser("budget", help="Check against monthly budget")
    p.add_argument("amount", type=float, help="Monthly budget in USD")
    p.set_defaults(func=cmd_budget)

    # models
    p = sub.add_parser("models", help="List all models and pricing")
    p.set_defaults(func=cmd_models)

    # providers
    p = sub.add_parser("providers", help="List all providers")
    p.set_defaults(func=cmd_providers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
