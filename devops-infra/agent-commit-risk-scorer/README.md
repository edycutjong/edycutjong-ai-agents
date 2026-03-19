# Agent: Commit Risk Scorer

A Python CLI agent designed to analyze Git commits and calculate a risk score based on various vectors like blast radius, path criticality, test coverage gaps, and historical bug patterns. This aids in enforcing CI/CD risk thresholds before automated deployments.

## Features
- **Criticality Scoring:** Assign custom weights to specific file paths (e.g., higher risk for `/security` or `/migrations`).
- **Blast Radius:** Estimates impact potential based on the spread of files changed across directories.
- **Coverage Gap:** Penalty for modifying source code without accompanying test modifications.
- **Historical Risk:** Analyzes recent commit history to detect bug patterns and apply a familiarity discount for frequent committers.
- **Outputs:** Supports terminal table, JSON, and Markdown formats.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure settings:
   Copy `config.example.yaml` to `config.yaml` and adjust path weights, thresholds, and max scores based on your project's risk tolerance.

## Usage

```bash
python main.py --repo . --sha HEAD --format table
```

### Options
- `--repo`: Path to the Git repository (default: `.`)
- `--sha`: Commit SHA or ref to analyze (default: `HEAD`)
- `--config`: Path to the YAML configuration file (default: `config.yaml`)
- `--format`: Output format, choices are `table`, `json`, `markdown` (default: `table`)
- `--threshold`: The score above which the command exits with code 1 (default: `75`, override via config or flag).

## Testing

```bash
# Run tests with coverage
pytest --cov=lib --cov=main --cov-report=term-missing
```
