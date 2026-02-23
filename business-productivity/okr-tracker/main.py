#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.tracker import Objective, KeyResult, OKRStore, format_okrs_markdown
def cmd_add(args):
    krs = [KeyResult(title=t, target=args.target) for t in args.key_results] if args.key_results else []
    obj = Objective(title=args.title, owner=args.owner or "", quarter=args.quarter or "", key_results=krs)
    s = OKRStore(); oid = s.add_objective(obj); print(f"Added objective {oid}")
def cmd_list(args):
    s = OKRStore(); data = s.get_all()
    if args.json: print(json.dumps(data, indent=2))
    else: print(format_okrs_markdown(data))
def cmd_update(args):
    s = OKRStore(); ok = s.update_key_result(args.objective_id, args.kr_id, args.value)
    print("Updated" if ok else "Not found")
def main():
    p = argparse.ArgumentParser(description="OKR Tracker"); sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add"); a.add_argument("title"); a.add_argument("--owner"); a.add_argument("--quarter"); a.add_argument("--key-results", nargs="*"); a.add_argument("--target", type=float, default=100); a.set_defaults(func=cmd_add)
    l = sub.add_parser("list"); l.add_argument("--json", action="store_true"); l.set_defaults(func=cmd_list)
    u = sub.add_parser("update"); u.add_argument("objective_id"); u.add_argument("kr_id"); u.add_argument("value", type=float); u.set_defaults(func=cmd_update)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
