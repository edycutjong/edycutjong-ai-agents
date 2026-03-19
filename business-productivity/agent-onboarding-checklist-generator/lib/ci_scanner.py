import os
import re

def scan_ci_config(repo_path: str) -> dict:
    """Scans CI/CD configurations for required secrets."""
    results = {
        "ci_systems": [],
        "secrets": []
    }
    
    secrets = set()
    
    # GitHub Actions
    gh_workflows_dir = os.path.join(repo_path, ".github", "workflows")
    if os.path.exists(gh_workflows_dir):
        results["ci_systems"].append("GitHub Actions")
        for root, _, files in os.walk(gh_workflows_dir):
            for file in files:
                if file.endswith((".yml", ".yaml")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Very simple heuristic to find ${{ secrets.SOMETHING }}
                            matches = re.findall(r'\${{\s*secrets\.([A-Za-z0-9_]+)\s*}}', content)
                            for match in matches:
                                if match != "GITHUB_TOKEN":
                                    secrets.add(match)
                    except Exception:
                        pass

    # GitLab CI
    gitlab_ci = os.path.join(repo_path, ".gitlab-ci.yml")
    if os.path.exists(gitlab_ci):
        results["ci_systems"].append("GitLab CI")
        # GitLab CI typically injects variables via project settings, 
        # so explicit secret references in script are harder to blindly extract.
        # But we can look for basic `$SECRET_` patterns if needed.

    results["secrets"] = sorted(list(secrets))
    return results
