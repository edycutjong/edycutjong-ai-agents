"""Replay engine for captured webhook requests."""
from __future__ import annotations

import json
import logging
import urllib.request
import urllib.error
from agent.storage import WebhookRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def replay_request(request: WebhookRequest, target_url: str,
                   override_headers: dict | None = None) -> dict:
    """Replay a captured webhook request to a target URL.

    Args:
        request: The captured WebhookRequest to replay.
        target_url: URL to send the replay to.
        override_headers: Optional headers to override.

    Returns:
        dict with status_code, response_body, and error if any.
    """
    headers = dict(request.headers)
    if override_headers:
        headers.update(override_headers)

    # Remove hop-by-hop headers
    for h in ["Host", "Transfer-Encoding", "Connection"]:
        headers.pop(h, None)

    body = request.body.encode("utf-8") if request.body else None

    req = urllib.request.Request(
        target_url,
        data=body,
        headers=headers,
        method=request.method,
    )

    try:
        response = urllib.request.urlopen(req, timeout=10)
        return {
            "status": "success",
            "status_code": response.status,
            "response_body": response.read().decode("utf-8", errors="replace"),
            "original_id": request.id,
        }
    except urllib.error.HTTPError as e:
        return {
            "status": "error",
            "status_code": e.code,
            "response_body": e.read().decode("utf-8", errors="replace"),
            "original_id": request.id,
        }
    except Exception as e:
        return {
            "status": "error",
            "status_code": 0,
            "response_body": str(e),
            "original_id": request.id,
        }


def generate_curl_command(request: WebhookRequest, target_url: str | None = None) -> str:
    """Generate a curl command to replay this request."""
    url = target_url or f"http://localhost:8765{request.path}"
    parts = [f"curl -X {request.method}"]

    for key, value in request.headers.items():
        if key.lower() not in ("host", "content-length"):
            parts.append(f"  -H '{key}: {value}'")

    if request.body:
        # Escape single quotes in body
        escaped = request.body.replace("'", "'\\''")
        parts.append(f"  -d '{escaped}'")

    parts.append(f"  '{url}'")
    return " \\\n".join(parts)


def generate_python_snippet(request: WebhookRequest, target_url: str | None = None) -> str:
    """Generate a Python requests snippet to replay this request."""
    url = target_url or f"http://localhost:8765{request.path}"
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in ("host", "content-length")}

    lines = [
        "import requests",
        "",
        f'url = "{url}"',
        f"headers = {json.dumps(headers, indent=2)}",
    ]

    if request.body:
        try:
            body_dict = json.loads(request.body)
            lines.append(f"payload = {json.dumps(body_dict, indent=2)}")
            lines.append(f'response = requests.{request.method.lower()}(url, json=payload, headers=headers)')
        except json.JSONDecodeError:
            lines.append(f'data = """{request.body}"""')
            lines.append(f'response = requests.{request.method.lower()}(url, data=data, headers=headers)')
    else:
        lines.append(f'response = requests.{request.method.lower()}(url, headers=headers)')

    lines.extend([
        "",
        "print(response.status_code)",
        "print(response.text)",
    ])
    return "\n".join(lines)
