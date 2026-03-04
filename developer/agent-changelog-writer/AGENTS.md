# Changelog Writer Agent

## Overview
Agent that reads git commits, categorizes them, and generates formatted CHANGELOG.md following Keep a Changelog.

## Tech Stack
- **Stack:** Node.js, TypeScript
- **Build:** No build step — open `index.html` in browser

## Features
- Parse conventional commits
- Categorize: Added, Changed, Fixed, Removed
- Version number suggestion (semver)
- Breaking change detection
- PR/issue link extraction
- Author attribution
- Multiple output formats (Markdown, JSON)
- Configurable commit parsing rules
- Unreleased section management
- Dry-run preview mode

## File Structure
- `index.html — main page`
- `styles.css — styles`
- `app.js — application logic`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Sunset Glow palette
- **Primary:** `#F97316`
- **Secondary:** `#FB923C`
- **Accent:** `#06B6D4`
- **Background:** `#1A1008`
- **Border Radius:** 12px
