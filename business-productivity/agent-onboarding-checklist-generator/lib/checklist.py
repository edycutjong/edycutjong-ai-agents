from .detector import detect_stack
from .env_scanner import scan_env_vars
from .ci_scanner import scan_ci_config
from .readme_parser import parse_readme

def generate_checklist(repo_path: str, overrides: dict = None) -> dict:
    """Generates the full structured checklist."""
    if overrides is None:
        overrides = {}
        
    stack = detect_stack(repo_path)
    env_vars = scan_env_vars(repo_path)
    ci_config = scan_ci_config(repo_path)
    readme_info = parse_readme(repo_path)
    
    checklist = {
        "prerequisites": [],
        "setup_steps": [],
        "verification_steps": []
    }
    
    # Prerequisites
    if "JavaScript/TypeScript" in stack["languages"]:
        checklist["prerequisites"].append("Install Node.js (check nvm/nvmrc if present).")
    if "Python" in stack["languages"]:
        checklist["prerequisites"].append("Install Python 3.x.")
    if "Go" in stack["languages"]:
        checklist["prerequisites"].append("Install Go workspace.")
    if "Rust" in stack["languages"]:
        checklist["prerequisites"].append("Install Rust (rustup).")
    if "Docker" in stack["tools"]:
        checklist["prerequisites"].append("Install Docker and ensure the daemon is running.")
        
    if not checklist["prerequisites"]:
        checklist["prerequisites"].append("Review repository documentation for system dependencies.")

    # Setup Steps
    checklist["setup_steps"].append("Clone the repository.")
    
    if ci_config["secrets"]:
        checklist["setup_steps"].append(f"Obtain necessary secrets/tokens: {', '.join(ci_config['secrets'])}")
        
    if env_vars:
        checklist["setup_steps"].append("Copy environment template: `cp .env.example .env` (or similar).")
        checklist["setup_steps"].append("Fill in the following environment variables:\n" + 
            "\n".join([f"  - {v['name']} ({v['description']})" for v in env_vars]))
            
    # Install commands
    if readme_info["setup_commands"]:
        for cmd in readme_info["setup_commands"]:
            checklist["setup_steps"].append(f"Run setup command: `{cmd}`")
    else:
        # Fallback based on package manager
        if "npm/yarn/pnpm" in stack["package_managers"]:
            checklist["setup_steps"].append("Install dependencies: `npm install` or `yarn install` or `pnpm install`")
        if "pip" in stack["package_managers"]:
            checklist["setup_steps"].append("Install dependencies: `pip install -r requirements.txt`")
        if "Poetry/Pipenv/Hatch" in stack["package_managers"]:
            checklist["setup_steps"].append("Install dependencies using Poetry/Pipenv/Hatch.")
        if "Cargo" in stack["package_managers"]:
            checklist["setup_steps"].append("Fetch Rust dependencies: `cargo fetch`")

    # Run commands
    if readme_info["run_commands"]:
        for cmd in readme_info["run_commands"]:
            checklist["verification_steps"].append(f"Start the application: `{cmd}`")
    else:
        # Fallback
        if "npm/yarn/pnpm" in stack["package_managers"]:
            checklist["verification_steps"].append("Start the dev server: `npm start` or `npm run dev`")
        if "Docker Compose" in stack["tools"]:
            checklist["verification_steps"].append("Start services: `docker-compose up`")

    checklist["verification_steps"].append("Run test suite if available (e.g. `npm test`, `pytest`, `cargo test`).")
    checklist["verification_steps"].append("Verify application is running at expected localhost port.")
    
    # Apply user overrides if any
    if "prerequisites" in overrides:
        checklist["prerequisites"] = overrides["prerequisites"]
    if "setup_steps" in overrides:
        checklist["setup_steps"] = overrides["setup_steps"]
    if "verification_steps" in overrides:
        checklist["verification_steps"] = overrides["verification_steps"]

    # Deduplicate steps preserving order
    for key in checklist:
        seen = set()
        deduped = []
        for item in checklist[key]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        checklist[key] = deduped

    return checklist
