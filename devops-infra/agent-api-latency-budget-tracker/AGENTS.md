# AGENTS.md — API Latency Budget Tracker

## Overview
Agent that monitors API endpoint latency against defined SLO (Service Level Objective) budgets. Reads endpoint definitions with target p50/p95/p99 latencies, runs synthetic probes or parses access logs, and generates burn-rate reports showing how fast your error/latency budget is being consumed. Alerts when budget consumption exceeds threshold.

## References
- Inspired by [Google SRE Workbook](https://sre.google/workbook/alerting-on-slos/) — error budget alerting philosophy
- Inspired by [Sloth](https://github.com/slok/sloth) — SLO-based Prometheus alerting

## Tech Stack
- **Stack:** Python 3.11+
- **Build:** `pip install -r requirements.txt`
- **Dependencies:** httpx, click, pyyaml, rich

## Features
- Define SLO budgets per endpoint in YAML config (target p50, p95, p99)
- Synthetic probe mode: periodically hit endpoints and measure latency
- Log parser mode: ingest access logs (nginx, CloudFront, custom JSON)
- Calculate error budget consumption rate (burn rate)
- Multi-window analysis (1h, 6h, 24h, 7d, 30d rolling windows)
- Color-coded terminal dashboard with Rich tables
- Budget exhaustion prediction (ETA to 100% consumed)
- Alerting via webhook (Slack, Discord, generic HTTP)
- Historical trend storage in SQLite
- JSON/Markdown report export for CI integration

## File Structure
- `main.py` — CLI entry point (click-based)
- `lib/prober.py` — Synthetic HTTP probe engine
- `lib/log_parser.py` — Access log parser (nginx, JSON)
- `lib/budget.py` — SLO budget calculation engine
- `lib/reporter.py` — Rich terminal dashboard and export
- `lib/alerter.py` — Webhook alerter for budget violations
- `config.example.yaml` — Example SLO configuration
- `requirements.txt` — Python dependencies
- `tests/` — Unit tests with fixture logs
- `README.md` — Usage documentation

## Design Guidelines
- **Theme:** Dark minimal with ocean accents
- **Primary:** `#0EA5E9` (Sky Blue)
- **Secondary:** `#38BDF8` (Light Blue)
- **Accent:** `#EF4444` (Red — budget violations)
- **Background:** `#0C1222` (Deep Navy)
- **Font:** JetBrains Mono (terminal output)
- **Style:** Clean CLI dashboard with color-coded burn rate indicators

## Requirements
- No external API keys required (optional webhook URLs)
- Supports both active probing and passive log analysis
- CLI-friendly with `--format json|markdown|table` flag
- CI integration with non-zero exit codes on budget violations
- YAML-based configuration for endpoint SLO definitions
