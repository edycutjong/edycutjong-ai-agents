# License Auditor Agent

Agent that audits all project dependencies for license compliance, flags incompatible licenses, and generates a license report.

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
\`\`\`bash
# Run in development mode
npm run dev

# Or build and use locally
npm run build
node dist/index.js -d path/to/project -o THIRD_PARTY_LICENSES.md -f md
\`\`\`
