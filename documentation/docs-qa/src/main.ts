#!/usr/bin/env node
/**
 * Documentation QA Agent — CLI entry point.
 *
 * Usage:
 *   npx ts-node src/main.ts index ./src          # Index a codebase
 *   npx ts-node src/main.ts ask "How does auth work?"  # Ask a question
 *   npx ts-node src/main.ts search "fetchUser"   # Search for a function
 */
import { Command } from "commander";
import chalk from "chalk";
import { CodeIndexer } from "./indexer";
import { QueryEngine } from "./query";
import { SourceParser } from "./parser";

const program = new Command();

program
  .name("docs-qa")
  .description("AI agent answering codebase questions by reading source files")
  .version("1.0.0");

program
  .command("index")
  .description("Index a codebase for querying")
  .argument("<directory>", "Directory to index")
  .option("--extensions <exts>", "File extensions to include (comma-separated)", ".ts,.js,.py,.md")
  .option("--ignore <dirs>", "Directories to ignore (comma-separated)", "node_modules,dist,.git,__pycache__")
  .action(async (directory: string, options) => {
    console.log(chalk.cyan.bold("📚 Docs QA") + " — Indexing codebase\n");

    const extensions = options.extensions.split(",").map((e: string) => e.trim());
    const ignore = options.ignore.split(",").map((d: string) => d.trim());

    const indexer = new CodeIndexer({ extensions, ignoreDirs: ignore });
    const result = await indexer.index(directory);

    console.log(chalk.green(`✅ Indexed ${result.fileCount} files`));
    console.log(`   Functions: ${result.functionCount}`);
    console.log(`   Classes: ${result.classCount}`);
    console.log(`   Comments: ${result.commentCount}`);
    console.log(`   Index saved to: ${result.indexPath}`);
  });

program
  .command("ask")
  .description("Ask a natural language question about the codebase")
  .argument("<question>", "Your question")
  .option("--index <path>", "Path to index file", ".docs-qa-index.json")
  .option("--top <n>", "Number of results", "5")
  .action(async (question: string, options) => {
    console.log(chalk.cyan.bold("📚 Docs QA") + " — Asking\n");
    console.log(chalk.dim(`Q: ${question}\n`));

    const engine = new QueryEngine(options.index);
    const results = await engine.query(question, parseInt(options.top));

    if (results.length === 0) {
      console.log(chalk.yellow("No relevant results found."));
      return;
    }

    for (const r of results) {
      console.log(chalk.cyan(`📄 ${r.file}:${r.line}`));
      console.log(chalk.bold(`   ${r.name}`) + chalk.dim(` (${r.type})`));
      if (r.signature) {
        console.log(chalk.green(`   ${r.signature}`));
      }
      if (r.doc) {
        console.log(chalk.dim(`   ${r.doc}`));
      }
      console.log();
    }
  });

program
  .command("search")
  .description("Search for a function, class, or symbol")
  .argument("<query>", "Search query")
  .option("--index <path>", "Path to index file", ".docs-qa-index.json")
  .action(async (query: string, options) => {
    console.log(chalk.cyan.bold("📚 Docs QA") + " — Search\n");

    const engine = new QueryEngine(options.index);
    const results = await engine.search(query);

    if (results.length === 0) {
      console.log(chalk.yellow("No matches found."));
      return;
    }

    console.log(chalk.bold(`Found ${results.length} match(es):\n`));
    for (const r of results) {
      console.log(`  ${chalk.cyan(r.file)}:${r.line}  ${chalk.bold(r.name)}  ${chalk.dim(r.type)}`);
      if (r.signature) {
        console.log(`    ${chalk.green(r.signature)}`);
      }
    }
  });

program.parse();
