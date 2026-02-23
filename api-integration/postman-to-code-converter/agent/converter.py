"""Convert Postman collections to code in multiple languages."""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class ParsedRequest:
    """A parsed HTTP request from Postman."""
    name: str = ""
    method: str = "GET"
    url: str = ""
    headers: dict = field(default_factory=dict)
    body: str = ""
    body_type: str = ""  # raw, formdata, urlencoded
    auth_type: str = ""
    auth_token: str = ""
    description: str = ""

    def to_dict(self) -> dict:
        return {"name": self.name, "method": self.method, "url": self.url,
                "headers": self.headers, "body": self.body, "body_type": self.body_type}


def parse_collection(collection: dict) -> list[ParsedRequest]:
    """Parse a Postman collection (v2.1) into requests."""
    requests = []
    items = collection.get("item", [])
    _parse_items(items, requests)
    return requests


def _parse_items(items: list, requests: list[ParsedRequest]):
    for item in items:
        if "item" in item:  # folder
            _parse_items(item["item"], requests)
        elif "request" in item:
            req = item["request"]
            parsed = ParsedRequest(
                name=item.get("name", ""),
                method=req.get("method", "GET"),
                description=req.get("description", ""),
            )
            # URL
            url = req.get("url", "")
            if isinstance(url, dict):
                parsed.url = url.get("raw", "")
            else:
                parsed.url = url

            # Headers
            for h in req.get("header", []):
                if not h.get("disabled"):
                    parsed.headers[h.get("key", "")] = h.get("value", "")

            # Body
            body = req.get("body", {})
            parsed.body_type = body.get("mode", "")
            if parsed.body_type == "raw":
                parsed.body = body.get("raw", "")
            elif parsed.body_type == "urlencoded":
                params = body.get("urlencoded", [])
                parsed.body = "&".join(f"{p['key']}={p['value']}" for p in params if not p.get("disabled"))
            elif parsed.body_type == "formdata":
                params = body.get("formdata", [])
                parsed.body = json.dumps({p["key"]: p["value"] for p in params if not p.get("disabled")})

            # Auth
            auth = req.get("auth", {})
            parsed.auth_type = auth.get("type", "")
            if parsed.auth_type == "bearer":
                tokens = auth.get("bearer", [])
                for t in tokens:
                    if t.get("key") == "token":
                        parsed.auth_token = t.get("value", "")

            requests.append(parsed)


# --- Code Generators ---

def to_python(req: ParsedRequest) -> str:
    """Generate Python requests code."""
    lines = [f"# {req.name}" if req.name else "", "import requests", ""]
    lines.append(f'url = "{req.url}"')

    if req.headers:
        lines.append(f"headers = {json.dumps(req.headers, indent=4)}")
    if req.auth_token:
        h = "headers" if req.headers else "headers = {}"
        if not req.headers:
            lines.append(h)
        lines.append(f'headers["Authorization"] = "Bearer {req.auth_token}"')

    args = ["url"]
    if req.headers or req.auth_token:
        args.append("headers=headers")
    if req.body and req.body_type == "raw":
        lines.append(f"data = '''{req.body}'''")
        args.append("data=data")
    elif req.body and req.body_type == "urlencoded":
        lines.append(f'data = "{req.body}"')
        args.append("data=data")

    lines.append(f'response = requests.{req.method.lower()}({", ".join(args)})')
    lines.append("print(response.status_code)")
    lines.append("print(response.json())")
    return "\n".join(l for l in lines if l is not None)


def to_curl(req: ParsedRequest) -> str:
    """Generate curl command."""
    parts = [f"curl -X {req.method} '{req.url}'"]
    for k, v in req.headers.items():
        parts.append(f"  -H '{k}: {v}'")
    if req.auth_token:
        parts.append(f"  -H 'Authorization: Bearer {req.auth_token}'")
    if req.body:
        parts.append(f"  -d '{req.body}'")
    return " \\\n".join(parts)


def to_javascript(req: ParsedRequest) -> str:
    """Generate JavaScript fetch code."""
    lines = [f"// {req.name}" if req.name else ""]

    opts = {"method": req.method}
    if req.headers or req.auth_token:
        h = dict(req.headers)
        if req.auth_token:
            h["Authorization"] = f"Bearer {req.auth_token}"
        opts["headers"] = h
    if req.body:
        opts["body"] = req.body

    lines.append(f"const response = await fetch('{req.url}', {json.dumps(opts, indent=2)});")
    lines.append("const data = await response.json();")
    lines.append("console.log(data);")
    return "\n".join(l for l in lines if l is not None)


def to_go(req: ParsedRequest) -> str:
    """Generate Go net/http code."""
    lines = [
        "package main",
        "",
        'import (',
        '    "fmt"',
        '    "net/http"',
        '    "io"',
    ]
    if req.body:
        lines.append('    "strings"')
    lines.extend([')', "", "func main() {"])

    if req.body:
        lines.append(f'    body := strings.NewReader(`{req.body}`)')
        lines.append(f'    req, _ := http.NewRequest("{req.method}", "{req.url}", body)')
    else:
        lines.append(f'    req, _ := http.NewRequest("{req.method}", "{req.url}", nil)')

    for k, v in req.headers.items():
        lines.append(f'    req.Header.Set("{k}", "{v}")')
    if req.auth_token:
        lines.append(f'    req.Header.Set("Authorization", "Bearer {req.auth_token}")')

    lines.extend([
        "    client := &http.Client{}",
        "    resp, _ := client.Do(req)",
        "    defer resp.Body.Close()",
        "    body_bytes, _ := io.ReadAll(resp.Body)",
        '    fmt.Println(string(body_bytes))',
        "}",
    ])
    return "\n".join(lines)


GENERATORS = {
    "python": to_python,
    "curl": to_curl,
    "javascript": to_javascript,
    "go": to_go,
}


def convert_request(req: ParsedRequest, language: str) -> str:
    """Convert a single request to code."""
    gen = GENERATORS.get(language)
    if not gen:
        return f"# Unsupported language: {language}"
    return gen(req)


def convert_collection(collection: dict, language: str) -> str:
    """Convert an entire Postman collection to code."""
    requests = parse_collection(collection)
    snippets = [convert_request(r, language) for r in requests]
    return "\n\n---\n\n".join(snippets)
