import json
import os

try:
    import tomli
except ImportError:
    tomli = None

def detect_stack(repo_path: str) -> dict:
    """Detects the tech stack and system dependencies of a repository."""
    stack = {
        "languages": [],
        "frameworks": [],
        "package_managers": [],
        "tools": []
    }
    
    # Node.js
    package_json = os.path.join(repo_path, "package.json")
    if os.path.exists(package_json):
        stack["languages"].append("JavaScript/TypeScript")
        stack["package_managers"].append("npm/yarn/pnpm")
        try:
            with open(package_json, "r") as f:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "react" in deps:
                    stack["frameworks"].append("React")
                if "next" in deps:
                    stack["frameworks"].append("Next.js")
                if "express" in deps:
                    stack["frameworks"].append("Express")
                if "vue" in deps:
                    stack["frameworks"].append("Vue")
                if "svelte" in deps:
                    stack["frameworks"].append("Svelte")
        except Exception:
            pass

    # Python
    reqs_txt = os.path.join(repo_path, "requirements.txt")
    pyproject = os.path.join(repo_path, "pyproject.toml")
    if os.path.exists(reqs_txt) or os.path.exists(pyproject):
        stack["languages"].append("Python")
        if os.path.exists(pyproject) and tomli:
            stack["package_managers"].append("Poetry/Pipenv/Hatch")
        else:
            stack["package_managers"].append("pip")

    # Rust
    cargo = os.path.join(repo_path, "Cargo.toml")
    if os.path.exists(cargo):
        stack["languages"].append("Rust")
        stack["package_managers"].append("Cargo")

    # Go
    gomod = os.path.join(repo_path, "go.mod")
    if os.path.exists(gomod):
        stack["languages"].append("Go")
        stack["package_managers"].append("go mod")

    # Java/Kotlin
    pom_xml = os.path.join(repo_path, "pom.xml")
    build_gradle = os.path.join(repo_path, "build.gradle")
    build_gradle_kts = os.path.join(repo_path, "build.gradle.kts")
    if os.path.exists(pom_xml):
        stack["languages"].append("Java")
        stack["package_managers"].append("Maven")
    elif os.path.exists(build_gradle) or os.path.exists(build_gradle_kts):
        stack["languages"].append("Java/Kotlin")
        stack["package_managers"].append("Gradle")
        
    # Docker
    dockerfile = os.path.join(repo_path, "Dockerfile")
    docker_compose = os.path.join(repo_path, "docker-compose.yml")
    if os.path.exists(dockerfile) or os.path.exists(docker_compose):
        stack["tools"].append("Docker")
        if os.path.exists(docker_compose):
            stack["tools"].append("Docker Compose")

    # Makefile
    makefile = os.path.join(repo_path, "Makefile")
    if os.path.exists(makefile):
        stack["tools"].append("Make")

    # Deduplicate lists
    for key in stack:
        stack[key] = list(sorted(set(stack[key])))
        
    return stack
