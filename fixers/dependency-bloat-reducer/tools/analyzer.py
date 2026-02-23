import json
import os
import re
import asyncio
import httpx
from typing import Dict, List, Any, Optional

class DependencyAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.package_json_path = os.path.join(project_path, "package.json")
        self.package_lock_path = os.path.join(project_path, "package-lock.json")

    def parse_package_json(self) -> Dict[str, str]:
        """Parses package.json to get dependencies."""
        data = self.parse_package_json_full()
        dependencies = data.get("dependencies", {})
        devDependencies = data.get("devDependencies", {})
        # Combine both for analysis
        return {**dependencies, **devDependencies}

    async def analyze_bundle_size(self, package_name: str, version: str) -> Dict[str, Any]:
        """Fetches bundle size from Bundlephobia API."""
        url = f"https://bundlephobia.com/api/size?package={package_name}@{version}"
        headers = {
            "User-Agent": "dependency-bloat-reducer/1.0",
            "X-Bundlephobia-User": "dependency-bloat-reducer"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Failed to fetch data: {response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    def find_unused_dependencies(self) -> List[str]:
        """
        Scans source files for imports and compares with package.json.
        Also checks 'scripts' in package.json for binary usage.
        Note: This is a heuristic approach using regex.
        """
        package_data = self.parse_package_json_full()
        dependencies = list(package_data.get("dependencies", {}).keys()) + \
                       list(package_data.get("devDependencies", {}).keys())

        used_dependencies = set()

        # Check scripts for binary usage
        scripts = package_data.get("scripts", {})
        for script_cmd in scripts.values():
            for dep in dependencies:
                # Simple check: if dependency name appears in script command
                # This is heuristic but catches common tools like 'rimraf', 'cross-env', 'tsc'
                if dep in script_cmd:
                    used_dependencies.add(dep)

        # Regex to match imports: import ... from 'package'; require('package');
        # Also handles dynamic imports: import('package')
        import_pattern = re.compile(r"""(?:import\s+.*?from\s+['"]([^'"]+)['"])|(?:require\s*\(\s*['"]([^'"]+)['"]\s*\))|(?:import\s*\(\s*['"]([^'"]+)['"]\s*\))""")

        # Walk through project files
        for root, _, files in os.walk(self.project_path):
            if "node_modules" in root or ".git" in root or "dist" in root or "build" in root:
                continue

            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                            matches = import_pattern.findall(content)
                            for match in matches:
                                # match is a tuple (import_from, require, dynamic_import)
                                imported_module = match[0] or match[1] or match[2]
                                if imported_module:
                                    # Handle scoped packages @scope/pkg
                                    parts = imported_module.split('/')
                                    if imported_module.startswith('@'):
                                        if len(parts) >= 2:
                                            pkg_name = f"{parts[0]}/{parts[1]}"
                                            used_dependencies.add(pkg_name)
                                    else:
                                        pkg_name = parts[0]
                                        used_dependencies.add(pkg_name)
                    except Exception:
                        pass # Ignore read errors

        unused = [dep for dep in dependencies if dep not in used_dependencies and not dep.startswith("@types/")]
        return unused

    def parse_package_json_full(self) -> Dict[str, Any]:
        """Parses package.json fully."""
        if not os.path.exists(self.package_json_path):
             # Return empty if not found, to avoid crash in tests without mock
            return {}

        with open(self.package_json_path, "r") as f:
            return json.load(f)

    def check_duplicates(self) -> Dict[str, List[str]]:
        """
        Checks package-lock.json for multiple versions of the same package.
        """
        duplicates = {}
        if not os.path.exists(self.package_lock_path):
            return {"error": "package-lock.json not found"}

        with open(self.package_lock_path, "r") as f:
            data = json.load(f)
            # In package-lock v2/v3, 'packages' key is used. In v1, 'dependencies' is nested.
            # Let's handle v2/v3 'packages' structure which is flat-ish, or nested 'dependencies'

            # Simple approach: traverse all dependencies
            all_versions = {} # pkg_name -> list of versions

            def traverse(deps):
                for pkg, info in deps.items():
                    version = info.get("version")
                    if version:
                        if pkg not in all_versions:
                            all_versions[pkg] = set()
                        all_versions[pkg].add(version)
                    if "dependencies" in info:
                        traverse(info["dependencies"])

            if "dependencies" in data:
                traverse(data["dependencies"])
            elif "packages" in data:
                 # v2/v3 structure: "node_modules/pkg": {...}
                 for pkg_path, info in data["packages"].items():
                     if not pkg_path: continue # Root package
                     pkg_name = pkg_path.split("node_modules/")[-1]
                     version = info.get("version")
                     if version:
                        if pkg_name not in all_versions:
                            all_versions[pkg_name] = set()
                        all_versions[pkg_name].add(version)

            for pkg, versions in all_versions.items():
                if len(versions) > 1:
                    duplicates[pkg] = list(versions)

        return duplicates
