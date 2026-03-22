# Dependency Updater Agent

Autonomous agent that scans npm projects for outdated dependencies, updates them one by one, runs tests after each update, and rolls back on failure.

## Features
- Scan package.json for outdated deps
- Prioritize security updates
- Update one dependency at a time
- Run test suite after each update
- Automatic rollback on test failure
- Generate update report
- Support major/minor/patch strategies
- Ignore list configuration
- Batch mode for monorepos

## Commands
\`\`\`bash
# Run in development mode
npm run dev

# Or build and use locally
npm run build
node dist/index.js -d path/to/project -t "npm test"
\`\`\`
