import os
import re

def scan_env_vars(repo_path: str) -> list[dict]:
    """Scans for .env.example or .env.template and extracts required variables."""
    env_files = [".env.example", ".env.template", ".env.sample", ".env.dist"]
    variables = []
    
    for file_name in env_files:
        file_path = os.path.join(repo_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract VAR_NAME=value or VAR_NAME
                        match = re.match(r'^([A-Za-z0-9_]+)(?:=(.*))?$', line)
                        if match:
                            var_name = match.group(1)
                            default_val = match.group(2) if match.group(2) else ""
                            comments = []
                            # Very basic inline comment parsing
                            if "#" in default_val:
                                parts = default_val.split("#", 1)
                                default_val = parts[0].strip()
                                comments.append(parts[1].strip())
                            
                            variables.append({
                                "name": var_name,
                                "default": default_val.strip("'\""),
                                "description": " ".join(comments) if comments else "No description provided."
                            })
            # Only process the first found example file
            break
            
    return variables
