"""Dockerfile generator — generate Dockerfiles from project configuration."""
from __future__ import annotations
from dataclasses import dataclass, field

TEMPLATES = {
    "python": {"base": "python:3.11-slim", "install": "pip install --no-cache-dir -r requirements.txt", "cmd": 'python main.py', "workdir": "/app", "copy_first": "requirements.txt"},
    "node": {"base": "node:20-alpine", "install": "npm ci --only=production", "cmd": "node index.js", "workdir": "/app", "copy_first": "package*.json"},
    "go": {"base": "golang:1.22-alpine", "install": "go mod download", "cmd": "./app", "workdir": "/app", "copy_first": "go.mod go.sum"},
    "rust": {"base": "rust:1.77-slim", "install": "cargo build --release", "cmd": "./target/release/app", "workdir": "/app", "copy_first": "Cargo.toml Cargo.lock"},
    "java": {"base": "eclipse-temurin:21-jdk", "install": "./mvnw package -DskipTests", "cmd": "java -jar target/app.jar", "workdir": "/app", "copy_first": "pom.xml"},
    "static": {"base": "nginx:alpine", "install": "", "cmd": "", "workdir": "/usr/share/nginx/html", "copy_first": ""},
}

@dataclass
class DockerfileResult:
    language: str = ""; content: str = ""; stages: int = 1; base_image: str = ""
    optimizations: list[str] = field(default_factory=list)
    def to_dict(self) -> dict: return {"language": self.language, "stages": self.stages, "base_image": self.base_image}

def generate_dockerfile(language: str, port: int = 0, env_vars: dict = None, multi_stage: bool = False) -> DockerfileResult:
    lang = language.lower()
    tmpl = TEMPLATES.get(lang)
    if not tmpl: return DockerfileResult(language=lang, content=f"# Unsupported language: {lang}")
    r = DockerfileResult(language=lang, base_image=tmpl["base"])
    lines = [f"FROM {tmpl['base']}", f"WORKDIR {tmpl['workdir']}", ""]
    r.optimizations.append("Using slim/alpine base image")
    if tmpl["copy_first"]:
        lines.append(f"COPY {tmpl['copy_first']} ./")
        lines.append(f"RUN {tmpl['install']}")
        r.optimizations.append("Dependency caching via COPY-first pattern")
    lines.extend(["", "COPY . ."])
    if env_vars:
        for k, v in env_vars.items(): lines.append(f"ENV {k}={v}")
    if port: lines.extend(["", f"EXPOSE {port}"]); r.optimizations.append(f"Exposing port {port}")
    if tmpl["cmd"]: lines.extend(["", f'CMD ["{tmpl["cmd"]}"]'])
    r.content = "\n".join(lines) + "\n"
    return r

def list_languages() -> list[str]:
    return sorted(TEMPLATES.keys())

def get_base_image(language: str) -> str:
    return TEMPLATES.get(language.lower(), {}).get("base", "")

def add_healthcheck(dockerfile: str, endpoint: str = "/health", port: int = 8080) -> str:
    hc = f'\nHEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:{port}{endpoint} || exit 1\n'
    return dockerfile.rstrip() + hc

def format_result_markdown(r: DockerfileResult) -> str:
    lines = [f"## Dockerfile Generator 🐳", f"**Language:** {r.language} | **Base:** `{r.base_image}`", ""]
    lines.append(f"```dockerfile\n{r.content}```")
    if r.optimizations:
        lines.append("\n### Optimizations")
        for o in r.optimizations: lines.append(f"- ✅ {o}")
    return "\n".join(lines)
