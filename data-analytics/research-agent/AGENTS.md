# Research Agent

## Overview
Autonomous agent that researches a topic using web search and compiles structured reports.

## Tech Stack
- TypeScript, LangChain, web search API

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
- Accept research topic as input
- Multi-query web search strategy
- Source credibility scoring
- Structured report generation (intro, findings, sources)
- Key findings extraction
- Citation management
- Markdown and PDF output
- Iterative depth research
- Configurable search depth
- Rate-limited API calls

## Design Notes
- Premium, modern UI with dark mode support
- Smooth animations and micro-interactions
- Responsive layout for all screen sizes
- Accessible (WCAG 2.1 AA compliant)
- No external API keys required for core functionality

## Testing
- Unit tests for core logic
- Target ≥80% code coverage
