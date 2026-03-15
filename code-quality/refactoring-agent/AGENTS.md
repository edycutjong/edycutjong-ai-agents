# AGENTS.md — Refactoring Agent

## Overview
AI agent that identifies code smells, suggests refactoring patterns, and generates pull requests.

## Tech Stack
- TypeScript / Python
- LLM integration (OpenAI / Anthropic)
- GitHub API for PR creation

## Features
1. Core functionality as described above
2. Configurable via environment variables
3. Structured output parsing
4. Rate limiting and retry logic
5. Logging and audit trail
6. Dry-run mode

## File Structure
- `src/index.ts`
- `src/agent.ts`
- `package.json`
- `tsconfig.json`
