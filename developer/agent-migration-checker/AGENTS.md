# Migration Checker Agent

## Overview
Agent that validates database migration files — checks for destructive operations, naming, and ordering.

## Tech Stack
- **Stack:** Node.js, TypeScript
- **Build:** No build step — open `index.html` in browser

## Features
- Parse SQL migration files
- Detect destructive operations (DROP, TRUNCATE)
- Naming convention validation
- Sequential ordering check
- Reversibility assessment
- Schema conflict detection
- PR comment with findings
- Configurable rules
- Support Prisma, Drizzle, raw SQL
- Exit codes for CI

## File Structure
- `index.html — main page`
- `styles.css — styles`
- `app.js — application logic`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Arctic Blue palette
- **Primary:** `#3B82F6`
- **Secondary:** `#60A5FA`
- **Accent:** `#F59E0B`
- **Background:** `#0A1022`
- **Border Radius:** 12px
