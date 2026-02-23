PACKAGE_JSON_PROMPT = """
You are an expert monorepo architect. Generate a root `package.json` for a {monorepo_tool} monorepo.
The project name is "{project_name}".
The package manager is "{package_manager}".

Requirements:
- Include "workspaces" configuration suitable for {package_manager} and {monorepo_tool}.
- Include basic scripts for "build", "dev", "lint", "test".
- Include devDependencies for {monorepo_tool}, typescript, eslint, prettier.
- Return ONLY the JSON content, no markdown formatting.

Context:
Project Name: {project_name}
Package Manager: {package_manager}
Monorepo Tool: {monorepo_tool}
"""

TSCONFIG_PROMPT = """
You are an expert TypeScript configuration specialist. Generate a base `tsconfig.json` for a {monorepo_tool} monorepo.
This config will be extended by packages and apps.

Requirements:
- Target ESNext.
- Use "node" module resolution.
- Enable strict mode.
- Include "paths" if necessary for {monorepo_tool}.
- Return ONLY the JSON content, no markdown formatting.
"""

CI_PIPELINE_PROMPT = """
You are a DevOps engineer specializing in CI/CD. Generate a CI pipeline configuration file for {ci_provider}.
The package manager is "{package_manager}".

Requirements:
- Install dependencies using {package_manager}.
- Run linting and tests.
- Build the project.
- Use caching for {package_manager} if applicable.
- Return ONLY the YAML content, no markdown formatting.
"""

README_PROMPT = """
You are a technical writer. Generate a `README.md` for a new monorepo project named "{project_name}".

Description: {description}

Requirements:
- Introduction.
- Getting Started section.
- Directory structure overview.
- Commands (dev, build, test).
- Return ONLY the Markdown content.
"""
