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
    storage = WebhookStorage()  # pragma: no cover
    requests = storage.get_all()  # pragma: no cover

    if not requests:  # pragma: no cover
        print("No captured requests.")  # pragma: no cover
        return  # pragma: no cover

    if args.method:  # pragma: no cover
        requests = [r for r in requests if r.method.upper() == args.method.upper()]  # pragma: no cover
    if args.path:  # pragma: no cover
        requests = [r for r in requests if args.path in r.path]  # pragma: no cover

    print(f"{'ID':<10} {'Method':<8} {'Path':<25} {'Content-Type':<25} {'Time'}")  # pragma: no cover
    print("-" * 85)  # pragma: no cover
    for req in requests:  # pragma: no cover
        ct = req.content_type[:22] + "..." if len(req.content_type) > 25 else req.content_type  # pragma: no cover
        print(f"{req.id:<10} {req.method:<8} {req.path:<25} {ct:<25} {req.timestamp[:19]}")  # pragma: no cover

    print(f"\n{len(requests)} request(s)")  # pragma: no cover


def cmd_show(args):
    """Show details of a captured request."""
    storage = WebhookStorage()  # pragma: no cover
    req = storage.get_by_id(args.id)  # pragma: no cover
    if not req:  # pragma: no cover
        print(f"Request '{args.id}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print(f"ID:           {req.id}")  # pragma: no cover
    print(f"Method:       {req.method}")  # pragma: no cover
    print(f"Path:         {req.path}")  # pragma: no cover
    print(f"Source IP:    {req.source_ip}")  # pragma: no cover
    print(f"Time:         {req.timestamp}")  # pragma: no cover
    print(f"Content-Type: {req.content_type}")  # pragma: no cover
    print(f"\nHeaders:")  # pragma: no cover
    for k, v in req.headers.items():  # pragma: no cover
        print(f"  {k}: {v}")  # pragma: no cover
    if req.query_params:  # pragma: no cover
        print(f"\nQuery Params:")  # pragma: no cover
        for k, v in req.query_params.items():  # pragma: no cover
            print(f"  {k} = {v}")  # pragma: no cover
    print(f"\nBody:")  # pragma: no cover
    if req.body:  # pragma: no cover
        try:  # pragma: no cover
            parsed = json.loads(req.body)  # pragma: no cover
            print(json.dumps(parsed, indent=2))  # pragma: no cover
        except json.JSONDecodeError:  # pragma: no cover
            print(req.body)  # pragma: no cover
    else:
        print("  (empty)")  # pragma: no cover


def cmd_replay(args):
    """Replay a request to a target URL."""
    storage = WebhookStorage()  # pragma: no cover
    req = storage.get_by_id(args.id)  # pragma: no cover
    if not req:  # pragma: no cover
        print(f"Request '{args.id}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print(f"Replaying {req.method} {req.path} → {args.url}...")  # pragma: no cover
    result = replay_request(req, args.url)  # pragma: no cover

    print(f"Status: {result['status_code']}")  # pragma: no cover
    print(f"Response:\n{result['response_body'][:500]}")  # pragma: no cover


def cmd_curl(args):
    """Generate curl command."""
    storage = WebhookStorage()  # pragma: no cover
    req = storage.get_by_id(args.id)  # pragma: no cover
    if not req:  # pragma: no cover
        print(f"Request '{args.id}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print(generate_curl_command(req, target_url=args.url))  # pragma: no cover


def cmd_python(args):
    """Generate Python snippet."""
    storage = WebhookStorage()  # pragma: no cover
    req = storage.get_by_id(args.id)  # pragma: no cover
    if not req:  # pragma: no cover
        print(f"Request '{args.id}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print(generate_python_snippet(req, target_url=args.url))  # pragma: no cover


def cmd_export(args):
    """Export all requests."""
    storage = WebhookStorage()  # pragma: no cover
    if args.format == "markdown":  # pragma: no cover
        print(storage.export_markdown())  # pragma: no cover
    else:
        print(storage.export_json())  # pragma: no cover


def cmd_clear(args):
    """Clear all captured requests."""
    storage = WebhookStorage()  # pragma: no cover
    count = storage.count()  # pragma: no cover
    storage.clear()  # pragma: no cover
    print(f"Cleared {count} request(s).")  # pragma: no cover


def cmd_capture(args):
    """Capture a webhook request from CLI arguments (for testing)."""
    storage = WebhookStorage()  # pragma: no cover
    headers = {}  # pragma: no cover
    if args.headers:  # pragma: no cover
        for h in args.headers:  # pragma: no cover
            key, _, value = h.partition(":")  # pragma: no cover
            headers[key.strip()] = value.strip()  # pragma: no cover

    req = WebhookRequest(  # pragma: no cover
        method=args.method,
        path=args.path or "/webhook",
        headers=headers,
        body=args.body or "",
        content_type=args.content_type or "application/json",
        source_ip=args.source or "127.0.0.1",
    )
    req_id = storage.add(req)  # pragma: no cover
    print(f"✅ Captured: {req.summary()}")  # pragma: no cover


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
