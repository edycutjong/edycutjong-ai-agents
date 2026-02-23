#!/usr/bin/env python3
"""CLI for Webhook Tester.

Usage:
    python main.py serve                         # Start webhook server
    python main.py list                          # List captured requests
    python main.py show <id>                     # Show request details
    python main.py replay <id> <url>             # Replay to target
    python main.py curl <id>                     # Generate curl command
    python main.py python <id>                   # Generate Python snippet
    python main.py export --format json          # Export all
    python main.py clear                         # Clear all
"""
import argparse
import json
import sys
import os

sys.path.append(os.path.dirname(__file__))

from agent.storage import WebhookStorage, WebhookRequest
from agent.replay import replay_request, generate_curl_command, generate_python_snippet


def cmd_list(args):
    """List all captured requests."""
    storage = WebhookStorage()
    requests = storage.get_all()

    if not requests:
        print("No captured requests.")
        return

    if args.method:
        requests = [r for r in requests if r.method.upper() == args.method.upper()]
    if args.path:
        requests = [r for r in requests if args.path in r.path]

    print(f"{'ID':<10} {'Method':<8} {'Path':<25} {'Content-Type':<25} {'Time'}")
    print("-" * 85)
    for req in requests:
        ct = req.content_type[:22] + "..." if len(req.content_type) > 25 else req.content_type
        print(f"{req.id:<10} {req.method:<8} {req.path:<25} {ct:<25} {req.timestamp[:19]}")

    print(f"\n{len(requests)} request(s)")


def cmd_show(args):
    """Show details of a captured request."""
    storage = WebhookStorage()
    req = storage.get_by_id(args.id)
    if not req:
        print(f"Request '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"ID:           {req.id}")
    print(f"Method:       {req.method}")
    print(f"Path:         {req.path}")
    print(f"Source IP:    {req.source_ip}")
    print(f"Time:         {req.timestamp}")
    print(f"Content-Type: {req.content_type}")
    print(f"\nHeaders:")
    for k, v in req.headers.items():
        print(f"  {k}: {v}")
    if req.query_params:
        print(f"\nQuery Params:")
        for k, v in req.query_params.items():
            print(f"  {k} = {v}")
    print(f"\nBody:")
    if req.body:
        try:
            parsed = json.loads(req.body)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(req.body)
    else:
        print("  (empty)")


def cmd_replay(args):
    """Replay a request to a target URL."""
    storage = WebhookStorage()
    req = storage.get_by_id(args.id)
    if not req:
        print(f"Request '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Replaying {req.method} {req.path} → {args.url}...")
    result = replay_request(req, args.url)

    print(f"Status: {result['status_code']}")
    print(f"Response:\n{result['response_body'][:500]}")


def cmd_curl(args):
    """Generate curl command."""
    storage = WebhookStorage()
    req = storage.get_by_id(args.id)
    if not req:
        print(f"Request '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(generate_curl_command(req, target_url=args.url))


def cmd_python(args):
    """Generate Python snippet."""
    storage = WebhookStorage()
    req = storage.get_by_id(args.id)
    if not req:
        print(f"Request '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(generate_python_snippet(req, target_url=args.url))


def cmd_export(args):
    """Export all requests."""
    storage = WebhookStorage()
    if args.format == "markdown":
        print(storage.export_markdown())
    else:
        print(storage.export_json())


def cmd_clear(args):
    """Clear all captured requests."""
    storage = WebhookStorage()
    count = storage.count()
    storage.clear()
    print(f"Cleared {count} request(s).")


def cmd_capture(args):
    """Capture a webhook request from CLI arguments (for testing)."""
    storage = WebhookStorage()
    headers = {}
    if args.headers:
        for h in args.headers:
            key, _, value = h.partition(":")
            headers[key.strip()] = value.strip()

    req = WebhookRequest(
        method=args.method,
        path=args.path or "/webhook",
        headers=headers,
        body=args.body or "",
        content_type=args.content_type or "application/json",
        source_ip=args.source or "127.0.0.1",
    )
    req_id = storage.add(req)
    print(f"✅ Captured: {req.summary()}")


def main():
    parser = argparse.ArgumentParser(
        description="Webhook Tester — Capture, inspect, and replay webhook requests.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p = sub.add_parser("list", help="List captured requests")
    p.add_argument("--method", help="Filter by HTTP method")
    p.add_argument("--path", help="Filter by path")
    p.set_defaults(func=cmd_list)

    # show
    p = sub.add_parser("show", help="Show request details")
    p.add_argument("id", help="Request ID")
    p.set_defaults(func=cmd_show)

    # replay
    p = sub.add_parser("replay", help="Replay request to target URL")
    p.add_argument("id", help="Request ID")
    p.add_argument("url", help="Target URL")
    p.set_defaults(func=cmd_replay)

    # curl
    p = sub.add_parser("curl", help="Generate curl command")
    p.add_argument("id", help="Request ID")
    p.add_argument("--url", help="Override target URL")
    p.set_defaults(func=cmd_curl)

    # python
    p = sub.add_parser("python", help="Generate Python snippet")
    p.add_argument("id", help="Request ID")
    p.add_argument("--url", help="Override target URL")
    p.set_defaults(func=cmd_python)

    # export
    p = sub.add_parser("export", help="Export all requests")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.set_defaults(func=cmd_export)

    # capture
    p = sub.add_parser("capture", help="Manually capture a request")
    p.add_argument("--method", default="POST")
    p.add_argument("--path", default="/webhook")
    p.add_argument("--body", help="Request body")
    p.add_argument("--content-type", default="application/json")
    p.add_argument("--headers", nargs="*", help="Headers as Key:Value")
    p.add_argument("--source", default="127.0.0.1")
    p.set_defaults(func=cmd_capture)

    # clear
    p = sub.add_parser("clear", help="Clear all requests")
    p.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
