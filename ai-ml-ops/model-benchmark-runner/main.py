#!/usr/bin/env python3
"""CLI for Model Benchmark Runner."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.benchmark import BenchmarkCase, run_benchmark, format_report_markdown, BenchmarkStorage

def cmd_run(args):
    data = json.load(open(args.config))
    cases = [BenchmarkCase(**c) for c in data.get("cases", [])]
    outputs = data.get("model_outputs", {})
    report = run_benchmark(cases, outputs)
    if args.save: BenchmarkStorage().save(report)
    if args.json: print(json.dumps(report.to_dict(), indent=2))
    else: print(format_report_markdown(report))

def cmd_history(args):
    for r in BenchmarkStorage().get_all():
        print(f"  {r.get('timestamp', '?')}  Models: {', '.join(r.get('models', []))}  Winner: {r.get('summary', {}).get('winner', 'N/A')}")

def main():
    parser = argparse.ArgumentParser(description="Model Benchmark Runner")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("run"); p.add_argument("config"); p.add_argument("--json", action="store_true"); p.add_argument("--save", action="store_true"); p.set_defaults(func=cmd_run)
    p = sub.add_parser("history"); p.set_defaults(func=cmd_history)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
