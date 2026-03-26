"""Configuration for A11Y Fixer Agent."""

APP_NAME = "a11y-fixer"
APP_VERSION = "1.0.0"
DESCRIPTION = "Scans HTML for accessibility issues and auto-generates fixes including alt text, ARIA labels, and contrast improvements."

COMMANDS = {
    "scan": "Scan HTML for WCAG violations",
    "fix": "Auto-fix common accessibility issues",
    "report": "Generate accessibility audit report",
}

SEVERITY_LEVELS = ["critical", "serious", "moderate", "minor"]
