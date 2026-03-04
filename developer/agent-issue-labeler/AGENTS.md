# Issue Labeler Agent

## Overview
Agent that auto-labels GitHub issues based on title, body, and file references using keyword matching.

## Tech Stack
- **Stack:** Node.js, TypeScript
- **Build:** No build step — open `index.html` in browser

## Features
- GitHub webhook integration
- Keyword-based label matching
- File path reference detection
- Priority assessment (P0-P3)
- Duplicate issue detection
- Auto-assign to team members
- Configurable label rules (YAML)
- Confidence score threshold
- Activity log dashboard
- Dry-run mode

## File Structure
- `index.html — main page`
- `styles.css — styles`
- `app.js — application logic`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Neon Lime palette
- **Primary:** `#84CC16`
- **Secondary:** `#A3E635`
- **Accent:** `#8B5CF6`
- **Background:** `#0A1A0A`
- **Border Radius:** 12px
