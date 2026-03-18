# AGENTS.md — Commit Risk Scorer

## Overview
Agent that analyzes git commits and assigns a risk score (0-100) based on change blast radius, file criticality, test coverage gaps, and historical bug correlation. Helps teams prioritize code reviews and catch high-risk changes before they reach production. Works as a CLI tool or CI check.

## References
- Inspired by [OpenSSF Scorecard](https://scorecard.dev/) — automated security risk scoring for open source
- Inspired by [GitNexus](https://github.com/ArcadeAI/GitNexus) — impact analysis via codebase knowledge graphs

## Tech Stack
- **Stack:** Python 3.11+
- **Build:** `pip install -r requirements.txt`
- **Dependencies:** gitpython, click, rich, pyyaml

## Features
- Analyze any commit or range of commits via SHA reference
- File criticality scoring based on configurable path weights (e.g. `migrations/` = high)
- Blast radius estimation: count of downstream files importing changed modules
- Test coverage gap detection: flag changed files without corresponding test changes
- Historical bug signal: weight files that appear frequently in bug-fix commits
- Contributor familiarity score: lower risk if author frequently edits these files
- Aggregate risk score (0-100) with breakdown per dimension
- Color-coded Rich terminal output with risk breakdown table
- JSON output for CI integration with configurable threshold gates
- YAML config for custom path weights and thresholds

## File Structure
- `main.py` — CLI entry point (click-based)
- `lib/git_analyzer.py` — Git commit and diff parser
- `lib/criticality.py` — File criticality scoring engine
- `lib/blast_radius.py` — Import graph and downstream impact analysis
- `lib/test_coverage.py` — Test file correlation checker
- `lib/history.py` — Bug correlation from commit history
- `lib/scorer.py` — Aggregate risk score calculator
- `lib/reporter.py` — Rich terminal and JSON report generator
- `config.example.yaml` — Example risk weight configuration
- `requirements.txt` — Python dependencies
- `tests/` — Unit tests with fixture repos
- `README.md` — Usage documentation

## Design Guidelines
- **Theme:** Dark minimal with rose accents
- **Primary:** `#E11D48` (Rose)
- **Secondary:** `#FB7185` (Light Rose)
- **Accent:** `#10B981` (Emerald — safe scores)
- **Background:** `#1A0A0F` (Dark Rose)
- **Font:** JetBrains Mono (terminal output)
- **Style:** Clean CLI with color-gradient risk indicators (green → amber → red)

## Requirements
- No external API keys required
- Works with any git repository (local or cloned)
- CLI-friendly with `--format json|markdown|table` flag
- CI integration with `--threshold N` flag (exits non-zero if score > N)
- Configurable via YAML for custom risk weights per project
