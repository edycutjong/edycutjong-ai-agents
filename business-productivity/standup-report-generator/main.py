#!/usr/bin/env python3
"""CLI for Standup Report Generator."""
import argparse, sys, os, json
from datetime import datetime
sys.path.append(os.path.dirname(__file__))
from agent.standup import (
    StandupEntry, StandupStorage,
    generate_daily_report, generate_weekly_summary, generate_blocker_report,
)

def cmd_add(args):
    storage = StandupStorage()
    entry = StandupEntry(
        author=args.author,
        yesterday=args.yesterday.split(";") if args.yesterday else [],
        today=args.today.split(";") if args.today else [],
        blockers=args.blockers.split(";") if args.blockers else [],
        tags=args.tags.split(",") if args.tags else [],
        mood=args.mood or "",
    )
    storage.add(entry)
    print(f"✅ Standup added for {entry.author} ({entry.date})")

def cmd_daily(args):
    storage = StandupStorage()
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    print(generate_daily_report(storage.get_all(), date))

def cmd_weekly(args):
    storage = StandupStorage()
    entries = storage.get_last_n_days(7)
    print(generate_weekly_summary(entries))

def cmd_blockers(args):
    storage = StandupStorage()
    print(generate_blocker_report(storage.get_all()))

def cmd_list(args):
    storage = StandupStorage()
    entries = storage.get_by_author(args.author) if args.author else storage.get_all()
    for e in entries:
        blockers = f" 🚫{len(e.blockers)}" if e.blockers else ""
        print(f"  [{e.date}] {e.author}{blockers} — {len(e.today)} tasks planned")

def main():
    parser = argparse.ArgumentParser(description="Standup Report Generator")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("add"); p.add_argument("--author", required=True); p.add_argument("--yesterday", help="Items separated by ;"); p.add_argument("--today", help="Items separated by ;"); p.add_argument("--blockers", help="Blockers separated by ;"); p.add_argument("--tags", help="Tags comma-separated"); p.add_argument("--mood", choices=["🟢","🟡","🔴","good","okay","bad"]); p.set_defaults(func=cmd_add)
    p = sub.add_parser("daily"); p.add_argument("--date"); p.set_defaults(func=cmd_daily)
    p = sub.add_parser("weekly"); p.set_defaults(func=cmd_weekly)
    p = sub.add_parser("blockers"); p.set_defaults(func=cmd_blockers)
    p = sub.add_parser("list"); p.add_argument("--author"); p.set_defaults(func=cmd_list)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
