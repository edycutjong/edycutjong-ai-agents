"""GitHub Actions workflow generator — create CI/CD pipelines from templates."""
from __future__ import annotations
import json
from dataclasses import dataclass, field

WORKFLOW_TEMPLATES = {
    "node-ci": {
        "name": "Node.js CI",
        "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
        "jobs": {"build": {
            "runs-on": "ubuntu-latest",
            "strategy": {"matrix": {"node-version": ["18.x", "20.x"]}},
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Use Node.js ${{ matrix.node-version }}", "uses": "actions/setup-node@v4", "with": {"node-version": "${{ matrix.node-version }}"}},
                {"run": "npm ci"},
                {"run": "npm run build --if-present"},
                {"run": "npm test"},
            ],
        }},
    },
    "python-ci": {
        "name": "Python CI",
        "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
        "jobs": {"test": {
            "runs-on": "ubuntu-latest",
            "strategy": {"matrix": {"python-version": ["3.11", "3.12"]}},
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Set up Python", "uses": "actions/setup-python@v5", "with": {"python-version": "${{ matrix.python-version }}"}},
                {"run": "pip install -r requirements.txt"},
                {"run": "pytest"},
            ],
        }},
    },
    "docker-build": {
        "name": "Docker Build",
        "on": {"push": {"branches": ["main"]}},
        "jobs": {"build": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Set up Docker Buildx", "uses": "docker/setup-buildx-action@v3"},
                {"name": "Build", "uses": "docker/build-push-action@v5", "with": {"context": ".", "push": False}},
            ],
        }},
    },
    "deploy-vercel": {
        "name": "Deploy to Vercel",
        "on": {"push": {"branches": ["main"]}},
        "jobs": {"deploy": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Deploy", "uses": "amondnet/vercel-action@v25", "with": {"vercel-token": "${{ secrets.VERCEL_TOKEN }}", "vercel-org-id": "${{ secrets.VERCEL_ORG_ID }}", "vercel-project-id": "${{ secrets.VERCEL_PROJECT_ID }}", "vercel-args": "--prod"}},
            ],
        }},
    },
    "lint": {
        "name": "Lint",
        "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
        "jobs": {"lint": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Run ESLint", "run": "npx eslint . --ext .js,.jsx,.ts,.tsx"},
            ],
        }},
    },
    "release": {
        "name": "Release",
        "on": {"push": {"tags": ["v*"]}},
        "jobs": {"release": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"name": "Create Release", "uses": "softprops/action-gh-release@v1", "with": {"generate_release_notes": True}},
            ],
        }},
    },
}

@dataclass
class WorkflowConfig:
    template: str
    name: str = ""
    branches: list[str] = field(default_factory=lambda: ["main"])
    node_versions: list[str] = field(default_factory=lambda: ["18.x", "20.x"])
    python_versions: list[str] = field(default_factory=lambda: ["3.11", "3.12"])
    extra_steps: list[dict] = field(default_factory=list)

def _yaml_dump_value(value, indent=0):
    """Simple YAML serializer (no pyyaml dependency)."""
    prefix = "  " * indent
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if any(c in value for c in ":{}&*!|>'\"%@`#,[]"): return f'"{value}"'
        return value
    if isinstance(value, list):
        if not value: return "[]"
        lines = []
        for item in value:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    val = _yaml_dump_value(v, indent + 1)
                    if first: lines.append(f"{prefix}- {k}: {val}"); first = False
                    else: lines.append(f"{prefix}  {k}: {val}")
            else:
                lines.append(f"{prefix}- {_yaml_dump_value(item)}")
        return "\n" + "\n".join(lines)
    if isinstance(value, dict):
        if not value: return "{}"
        lines = []
        for k, v in value.items():
            val = _yaml_dump_value(v, indent + 1)
            if isinstance(v, (dict, list)) and v: lines.append(f"{prefix}{k}:{val}")
            else: lines.append(f"{prefix}{k}: {val}")
        return "\n" + "\n".join(lines)
    return str(value)

def generate_workflow(config: WorkflowConfig) -> dict:
    """Generate a workflow from config."""
    tmpl = WORKFLOW_TEMPLATES.get(config.template)
    if not tmpl: raise ValueError(f"Unknown template: {config.template}")
    workflow = json.loads(json.dumps(tmpl))  # deep copy
    if config.name: workflow["name"] = config.name
    return workflow

def workflow_to_yaml(workflow: dict) -> str:
    """Convert workflow dict to YAML string."""
    lines = []
    for key, value in workflow.items():
        val = _yaml_dump_value(value, 0)
        if isinstance(value, (dict, list)) and value: lines.append(f"{key}:{val}")
        else: lines.append(f"{key}: {val}")
    return "\n".join(lines) + "\n"

def list_templates() -> dict:
    return {k: v["name"] for k, v in WORKFLOW_TEMPLATES.items()}

def format_templates_markdown() -> str:
    lines = ["# GitHub Actions Templates", f"**Available:** {len(WORKFLOW_TEMPLATES)}", ""]
    for k, v in WORKFLOW_TEMPLATES.items():
        jobs = list(v.get("jobs", {}).keys())
        lines.append(f"- **{k}**: {v['name']} ({', '.join(jobs)})")
    return "\n".join(lines)
