# AGENTS.md — Onboarding Checklist Generator

## Overview
Agent that scans a repository's structure and generates a developer onboarding checklist. Detects tech stack from package files, identifies setup steps from README/Makefile/docker-compose, catalogs environment variables from .env.example, and produces a step-by-step Markdown checklist a new developer can follow to get the project running locally.

## References
- Inspired by [ChiefOnboarding](https://github.com/chiefonboarding/ChiefOnboarding) — open source onboarding platform
- Inspired by [osodevops/devops-onboarding-checklist](https://github.com/osodevops/devops-onboarding-checklist) — DevOps onboarding templates

## Tech Stack
- **Stack:** Python 3.11+
- **Build:** `pip install -r requirements.txt`
- **Dependencies:** click, rich, pyyaml, tomli

## Features
- Auto-detect tech stack from package.json, requirements.txt, Cargo.toml, go.mod, etc.
- Extract setup commands from README, Makefile, docker-compose.yml
- Catalog required environment variables from .env.example or .env.template
- Detect CI/CD configuration and list required secrets/tokens
- Identify required system dependencies (Node.js version, Python version, Docker)
- Generate prerequisite checklist (tools to install before starting)
- Generate setup checklist (clone, install, configure, run)
- Generate verification checklist (run tests, lint, build)
- Output formats: Markdown checklist, JSON, interactive terminal
- Customizable via .onboarding.yaml override file

## File Structure
- `main.py` — CLI entry point (click-based)
- `lib/detector.py` — Tech stack and dependency detector
- `lib/readme_parser.py` — README command extractor
- `lib/env_scanner.py` — Environment variable cataloger
- `lib/ci_scanner.py` — CI/CD config analyzer
- `lib/checklist.py` — Checklist builder and formatter
- `lib/reporter.py` — Markdown, JSON, and terminal output
- `requirements.txt` — Python dependencies
- `tests/` — Unit tests with fixture repositories
- `README.md` — Usage documentation

## Design Guidelines
- **Theme:** Dark minimal with forest accents
- **Primary:** `#10B981` (Emerald)
- **Secondary:** `#34D399` (Light Emerald)
- **Accent:** `#6EE7B7` (Soft Green)
- **Background:** `#0A1A15` (Deep Forest)
- **Font:** JetBrains Mono (terminal output)
- **Style:** Clean CLI with numbered checklist output and progress indicators

## Requirements
- No external API keys required
- Works with any git repository (local path or cloned)
- CLI-friendly with `--format json|markdown|terminal` flag
- Supports monorepo detection (workspaces, lerna, turborepo)
- Outputs actionable, copy-pasteable commands in the checklist
