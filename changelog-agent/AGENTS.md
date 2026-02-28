# Changelog Agent

## Overview
Agent that reads git history and generates semantic changelogs automatically.

## Tech Stack
- TypeScript, simple-git, conventional-commits-parser

## Agent Structure
```
├── src/
│   ├── index.ts
│   ├── agent.ts
│   └── tools/
├── package.json
├── tsconfig.json
└── AGENTS.md
```

## Commands
- Install: `npm install`
- Dev: `npm run dev`
- Build: `npm run build`
- Test: `npm test`

## Features
- Parse git log with conventional commits
- Categorize: Added, Changed, Fixed, Breaking
- Semantic version suggestion
- Markdown changelog generation
- Date-range filtering
- Author attribution
- PR/issue linking
- Multiple output formats (MD, JSON, HTML)
- Configurable categories
- Monorepo support

## Design Notes
- Premium, modern UI with dark mode support
- Smooth animations and micro-interactions
- Responsive layout for all screen sizes
- Accessible (WCAG 2.1 AA compliant)
- No external API keys required for core functionality

## Testing
- Unit tests for core logic
- Target ≥80% code coverage
