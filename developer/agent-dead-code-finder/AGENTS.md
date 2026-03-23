# Dead Code Finder Agent

## Overview
Agent that statically analyzes a codebase to find unused exports, unreachable code, unused variables, and orphaned files.

## Tech Stack
- **Stack:** Node.js, TypeScript

## Features
- Find unused exported functions
- Detect unreachable code paths
- Identify unused variables
- Find orphaned files (not imported anywhere)
- Detect unused CSS classes
- Analyze unused dependencies in package.json
- Generate removal report
- Confidence scoring per finding
- Safe-to-delete recommendations
- Ignore patterns configuration

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
