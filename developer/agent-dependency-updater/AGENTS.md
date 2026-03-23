# Dependency Updater Agent

## Overview
Autonomous agent that scans npm projects for outdated dependencies, updates them one by one, runs tests after each update, and rolls back on failure.

## Tech Stack
- **Stack:** Node.js, TypeScript

## Features
- Scan package.json for outdated deps
- Prioritize security updates
- Update one dependency at a time
- Run test suite after each update
- Automatic rollback on test failure
- Generate update report
- Support major/minor/patch strategies
- Ignore list configuration
- PR creation with changelog
- Batch mode for monorepos

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
