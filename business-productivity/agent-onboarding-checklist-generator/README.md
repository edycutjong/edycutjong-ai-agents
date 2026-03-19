# Agent Onboarding Checklist Generator

This agent scans a repository's structure and generates a comprehensive developer onboarding checklist. It detects the tech stack from configuration files, identifies setup steps from READMEs or Makefiles, catalogs environment variables from `.env.example`, and produces a step-by-step checklist.

## Features

- **Stack Detection**: Identifies Node.js, Python, Rust, Go, Java/Kotlin, and tools like Docker and Make.
- **Environment Scanning**: Parses `.env.example` to list required variables.
- **CI/CD Scanning**: Inspects `.github/workflows/` and `.gitlab-ci.yml` for required secrets.
- **Setup Command Extraction**: Extracts `install`, `dev`, `build`, and `start` commands from README code blocks or Makefiles.
- **Multiple Formats**: Outputs interactive terminal UI, JSON, or Markdown formats.
- **Custom Overrides**: Supports an optional `.onboarding.yaml` file to manually override prerequisite, setup, and verification steps.

## Usage

You can run the agent CLI using `main.py`:

```bash
python main.py --path /path/to/your/repo --format terminal
```

### Options

- `--path`: The absolute or relative path to the repository to inspect. Defaults to current directory (`.`).
- `--format`: The output format style. Options are `terminal` (default interactive UI using `rich`), `json`, and `markdown`.

## Customization

You can place a `.onboarding.yaml` file in the root of the targeted repository to override generated steps:

```yaml
prerequisites:
  - Install custom internal VPN tool
setup_steps:
  - Run internal proxy configuration `npm run setup:proxy`
verification_steps:
  - Ensure the app is running on localhost:3000
```
