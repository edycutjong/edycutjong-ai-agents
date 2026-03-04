# License Auditor Agent

## Overview
Agent that scans project dependencies and reports licenses. Flags incompatible or risky licenses.

## Tech Stack
- **Stack:** Node.js, TypeScript
- **Build:** No build step — open `index.html` in browser

## Features
- Scan package.json dependencies recursively
- License identification per package
- Compatibility matrix check (MIT/Apache/GPL)
- Risk assessment (copyleft detection)
- SPDX expression parsing
- Export license report (Markdown/JSON)
- Configurable allowed/denied license lists
- PR comment with audit results
- Badge generation for README
- CI-friendly exit codes

## File Structure
- `index.html — main page`
- `styles.css — styles`
- `app.js — application logic`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Midnight Amber palette
- **Primary:** `#D97706`
- **Secondary:** `#FBBF24`
- **Accent:** `#6366F1`
- **Background:** `#1A1400`
- **Border Radius:** 12px
