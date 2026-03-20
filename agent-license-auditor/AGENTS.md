# License Auditor Agent

## Overview
Agent that audits all project dependencies for license compliance, flags incompatible licenses, and generates a license report.

## Tech Stack
- **Stack:** Node.js, TypeScript

## Features
- Scan all npm dependencies recursively
- Identify license type per package
- Flag copyleft licenses (GPL, AGPL)
- Detect missing license files
- Check license compatibility
- Generate THIRD_PARTY_LICENSES file
- SPDX identifier mapping
- Allowlist/blocklist configuration
- Report in Markdown/JSON/CSV
- CI pipeline integration

## Commands
- Dev: `npm run dev`
- Build: `npm run build`
- Test: `npm test`

## Design Guidelines
- **Theme:** Dark mode
- **Primary:** `#EC4899`
- **Accent:** `#DB2777`
- **Background:** `#0D1117`

## Requirements
- No external API keys required for core features
- Works standalone and self-contained
