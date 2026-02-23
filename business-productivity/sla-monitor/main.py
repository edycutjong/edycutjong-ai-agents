#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.monitor import SLADefinition, check_compliance, format_sla_dashboard
def cmd_check(args):
    sla = SLADefinition(name=args.name, metric=args.metric, target=args.target, unit=args.unit or "%", warning_threshold=args.warning or 0)
    status = check_compliance(sla, args.value)
    if args.json: print(json.dumps(status.to_dict(), indent=2))
    else: print(format_sla_dashboard([status]))
def main():
    p = argparse.ArgumentParser(description="SLA Monitor"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("check"); c.add_argument("name"); c.add_argument("--metric", required=True); c.add_argument("--target", type=float, required=True); c.add_argument("--value", type=float, required=True); c.add_argument("--unit"); c.add_argument("--warning", type=float); c.add_argument("--json", action="store_true"); c.set_defaults(func=cmd_check)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
