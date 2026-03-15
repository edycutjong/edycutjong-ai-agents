/**
 * Code indexer — builds a searchable index of codebase symbols.
 */
import * as fs from "fs";
import * as path from "path";
import { SourceParser, ParsedSymbol } from "./parser";

export interface IndexOptions {
  extensions: string[];
  ignoreDirs: string[];
}

export interface IndexResult {
  fileCount: number;
  functionCount: number;
  classCount: number;
  commentCount: number;
  indexPath: string;
}

export class CodeIndexer {
  private parser: SourceParser;
  private extensions: string[];
  private ignoreDirs: string[];

  constructor(options: IndexOptions) {
    this.parser = new SourceParser();
    this.extensions = options.extensions;
    this.ignoreDirs = options.ignoreDirs;
  }

  async index(directory: string): Promise<IndexResult> {
    const absDir = path.resolve(directory);
    const files = this.collectFiles(absDir);
    const symbols: ParsedSymbol[] = [];

    for (const file of files) {
      try {
        const fileSymbols = this.parser.parseFile(file);
        symbols.push(...fileSymbols);
      } catch {
        // Skip files that can't be parsed
      }
    }

    const indexPath = path.join(absDir, ".docs-qa-index.json");
    fs.writeFileSync(indexPath, JSON.stringify(symbols, null, 2));

    return {
      fileCount: files.length,
      functionCount: symbols.filter((s) => s.type === "function" || s.type === "method").length,
      classCount: symbols.filter((s) => s.type === "class").length,
      commentCount: symbols.filter((s) => s.doc).length,
      indexPath,
    };
  }

  private collectFiles(dir: string): string[] {
    const results: string[] = [];

    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (!this.ignoreDirs.includes(entry.name) && !entry.name.startsWith(".")) {
          results.push(...this.collectFiles(fullPath));
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        if (this.extensions.includes(ext)) {
          results.push(fullPath);
        }
      }
    }

    return results;
  }
}
