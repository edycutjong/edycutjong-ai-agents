# License Scanner

Scans all project dependencies for license types and flags incompatibilities with the project's license.

## Features
- Scan npm/pip/cargo dependencies recursively
- Identify license type per package
- Check license compatibility matrix
- Flag copyleft in permissive projects
- Detect missing license files
- Generate SBOM (Software Bill of Materials)
- Support SPDX identifiers
- Create compliance report
- Configurable allowlist/blocklist
- Export for legal review

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
