# Code Review Agent

## Overview
Agent that reviews PRs for security, performance, and style issues with explanations.

## Tech Stack
- TypeScript, tree-sitter, AST analysis

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
- Parse code diffs from GitHub PRs
- Security vulnerability detection
- Performance anti-pattern detection
- Code style consistency checking
- Inline comment suggestions
- Severity classification (critical/warning/info)
- Language support: JS/TS/Python/Go
- Configurable rule sets
- Summary report generation
- Integration with GitHub Checks API

## Design Notes
- Premium, modern UI with dark mode support
- Smooth animations and micro-interactions
- Responsive layout for all screen sizes
- Accessible (WCAG 2.1 AA compliant)
- No external API keys required for core functionality

## Testing
- Unit tests for core logic
- Target ≥80% code coverage
