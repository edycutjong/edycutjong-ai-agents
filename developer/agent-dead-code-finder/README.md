# Dead Code Finder Agent

Agent that statically analyzes a codebase to find unused exports, unreachable code, unused variables, and orphaned files.

## Features
- Find unused exported functions
- Detect unreachable code paths
- Identify unused variables
- Find orphaned files (not imported anywhere)
- Detect unused CSS classes
- Analyze unused dependencies in package.json
- Generate removal report
- Confidence scoring per finding

## Usage
\`\`\`bash
# Run in development mode
npm run dev

# Or build and use locally
npm run build
node dist/index.js -p path/to/tsconfig.json
\`\`\`
