"""API documentation generator — parse code and generate OpenAPI/Markdown docs."""
from __future__ import annotations
import re, json
from dataclasses import dataclass, field

@dataclass
class Endpoint:
    method: str = "GET"
    path: str = ""
    summary: str = ""
    description: str = ""
    parameters: list[dict] = field(default_factory=list)
    request_body: dict = field(default_factory=dict)
    responses: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        d = {"method": self.method, "path": self.path, "summary": self.summary}
        if self.description: d["description"] = self.description
        if self.parameters: d["parameters"] = self.parameters
        if self.request_body: d["requestBody"] = self.request_body
        if self.responses: d["responses"] = self.responses
        if self.tags: d["tags"] = self.tags
        return d

def parse_flask_routes(code: str) -> list[Endpoint]:
    """Parse Flask-style route decorators."""
    endpoints = []
    pattern = r'@\w+\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods=\[([^\]]+)\])?\)\s*\ndef\s+(\w+)\(([^)]*)\):\s*(?:"""([^"]*?)""")?'
    for m in re.finditer(pattern, code, re.DOTALL):
        path, methods, func_name, args, docstring = m.groups()
        method_list = [m.strip().strip("'\"") for m in methods.split(",")] if methods else ["GET"]
        for method in method_list:
            ep = Endpoint(method=method.upper(), path=path, summary=func_name.replace("_", " ").title(), description=(docstring or "").strip())
            if args:
                for arg in args.split(","):
                    arg = arg.strip()
                    if arg and arg != "self":
                        ep.parameters.append({"name": arg, "in": "path", "required": True, "schema": {"type": "string"}})
            ep.responses = {"200": {"description": "Success"}}
            endpoints.append(ep)
    return endpoints

def parse_express_routes(code: str) -> list[Endpoint]:
    """Parse Express.js-style route definitions."""
    endpoints = []
    pattern = r'(?:app|router)\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
    for m in re.finditer(pattern, code, re.IGNORECASE):
        method, path = m.groups()
        ep = Endpoint(method=method.upper(), path=path, summary=path.split("/")[-1].replace(":", "").title() or "Root", responses={"200": {"description": "Success"}})
        params = re.findall(r':(\w+)', path)
        for p in params:
            ep.parameters.append({"name": p, "in": "path", "required": True, "schema": {"type": "string"}})
        endpoints.append(ep)
    return endpoints

def parse_fastapi_routes(code: str) -> list[Endpoint]:
    """Parse FastAPI-style route decorators."""
    endpoints = []
    pattern = r'@\w+\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
    for m in re.finditer(pattern, code):
        method, path = m.groups()
        ep = Endpoint(method=method.upper(), path=path, summary=path.split("/")[-1].replace("{", "").replace("}", "").title() or "Root", responses={"200": {"description": "Success"}})
        params = re.findall(r'\{(\w+)\}', path)
        for p in params:
            ep.parameters.append({"name": p, "in": "path", "required": True, "schema": {"type": "string"}})
        endpoints.append(ep)
    return endpoints

PARSERS = {"flask": parse_flask_routes, "express": parse_express_routes, "fastapi": parse_fastapi_routes}

def detect_framework(code: str) -> str:
    if "@app.route" in code or "Flask(" in code: return "flask"
    if "@app.get(" in code or "@app.post(" in code or "FastAPI(" in code: return "fastapi"
    if "app.get(" in code or "router.get(" in code or "express(" in code: return "express"
    return "flask"

def generate_openapi(endpoints: list[Endpoint], title: str = "API", version: str = "1.0.0") -> dict:
    """Generate OpenAPI 3.0 spec."""
    paths = {}
    for ep in endpoints:
        if ep.path not in paths: paths[ep.path] = {}
        op = {"summary": ep.summary, "responses": ep.responses or {"200": {"description": "OK"}}}
        if ep.parameters: op["parameters"] = ep.parameters
        if ep.request_body: op["requestBody"] = ep.request_body
        if ep.tags: op["tags"] = ep.tags
        if ep.description: op["description"] = ep.description
        paths[ep.path][ep.method.lower()] = op
    return {"openapi": "3.0.0", "info": {"title": title, "version": version}, "paths": paths}

def generate_markdown_docs(endpoints: list[Endpoint], title: str = "API") -> str:
    """Generate Markdown API docs."""
    lines = [f"# {title} Documentation", f"**Endpoints:** {len(endpoints)}", ""]
    for ep in endpoints:
        lines.append(f"## `{ep.method}` {ep.path}")
        if ep.summary: lines.append(f"**{ep.summary}**")
        if ep.description: lines.append(f"\n{ep.description}")
        if ep.parameters:
            lines.append("\n**Parameters:**")
            for p in ep.parameters:
                req = "required" if p.get("required") else "optional"
                lines.append(f"- `{p['name']}` ({p.get('in', 'query')}, {req})")
        lines.append(f"\n**Responses:** {', '.join(ep.responses.keys())}")
        lines.append("---")
    return "\n".join(lines)
