import os
import re

def parse_readme(repo_path: str) -> dict:
    """Extracts potential setup and run commands from README.md or Makefile."""
    extracted = {
        "setup_commands": [],
        "run_commands": []
    }
    
    # Check Makefile
    makefile = os.path.join(repo_path, "Makefile") # Fixed path spelling
    if os.path.exists(makefile):
        try:
            with open(makefile, "r", encoding="utf-8") as f:
                content = f.read()
                # Find targets like `install:`, `start:`, `dev:`, `run:`
                targets = re.findall(r'^([a-zA-Z0-9_-]+):', content, re.MULTILINE)
                for t in targets:
                    if "install" in t or "setup" in t or "build" in t:
                        extracted["setup_commands"].append(f"make {t}")
                    elif "start" in t or "dev" in t or "run" in t:
                        extracted["run_commands"].append(f"make {t}")
        except Exception:
            pass
            
    # Check README.md
    for readme_name in ["README.md", "README", "readme.md"]:
        readme_path = os.path.join(repo_path, readme_name)
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Very simple extraction: grab code blocks inside typical sections
                # We'll just look for bash/sh blocks or npm/yarn/pip commands
                code_blocks = re.findall(r'```(?:bash|sh)?\n(.*?)\n```', content, re.DOTALL)
                for block in code_blocks:
                    lines = [ln.strip() for ln in block.split('\n') if ln.strip()]
                    for ln in lines:
                        ln = re.sub(r'^\$\s+', '', ln) # remove leading $
                        ln_lower = ln.lower()
                        if "install" in ln_lower or "build" in ln_lower or "pip" in ln_lower or "npm i" in ln_lower or "yarn" in ln_lower and "start" not in ln_lower:
                            if ln not in extracted["setup_commands"]:
                                extracted["setup_commands"].append(ln)
                        elif "start" in ln_lower or "dev" in ln_lower or "run" in ln_lower or "serve" in ln_lower:
                            if ln not in extracted["run_commands"]:
                                extracted["run_commands"].append(ln)
            except Exception:
                pass
            break # only parse the first found readme

    return extracted
