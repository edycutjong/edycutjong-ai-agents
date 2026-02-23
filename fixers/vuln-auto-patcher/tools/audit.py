import json
import subprocess
from typing import List, Dict, Any

def run_npm_audit(project_path: str = ".") -> Dict[str, Any]:
    """Runs npm audit json and returns the parsed output."""
    try:
        # npm audit exits with 1 if vulnerabilities are found, so we suppress check=True
        result = subprocess.run(
            ["npm", "audit", "json"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse npm audit output", "raw": result.stdout}
    except Exception as e:
        return {"error": str(e)}

def extract_vulnerabilities(audit_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extracts a simplified list of vulnerabilities from the audit report."""
    vulnerabilities = []
    if "vulnerabilities" in audit_report:
        for pkg_name, details in audit_report["vulnerabilities"].items():
            # Handle different npm audit formats (v6 vs v7+)
            # v7+ structure: details is a dict with 'via', 'effects', 'range', 'nodes', 'fixAvailable'

            severity = details.get("severity", "unknown")
            fix_available = details.get("fixAvailable", False)

            fix_version = None
            if isinstance(fix_available, dict):
                fix_version = fix_available.get("version")

            # Simple extraction, can be expanded
            vulnerabilities.append({
                "package": pkg_name,
                "severity": severity,
                "fix_available": bool(fix_available), # keep boolean for easy check
                "fix_version": fix_version,
                "range": details.get("range", ""),
                "via": details.get("via", [])
            })

    return vulnerabilities
