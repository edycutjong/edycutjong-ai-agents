/**
 * Source code parser — extracts functions, classes, and comments.
 */
import * as fs from "fs";
import * as path from "path";

export interface ParsedSymbol {
  name: string;
  type: "function" | "class" | "method" | "variable" | "interface";
  file: string;
  line: number;
  signature?: string;
  doc?: string;
}

export class SourceParser {
  /**
   * Parse a file and extract symbols.
   */
  parseFile(filePath: string): ParsedSymbol[] {
    const content = fs.readFileSync(filePath, "utf-8");
    const ext = path.extname(filePath);

    if (ext === ".py") return this.parsePython(content, filePath);
    if ([".ts", ".js", ".tsx", ".jsx"].includes(ext)) return this.parseTypeScript(content, filePath);
    if (ext === ".md") return this.parseMarkdown(content, filePath);

    return [];
  }

  private parsePython(content: string, file: string): ParsedSymbol[] {
    const symbols: ParsedSymbol[] = [];
    const lines = content.split("\n");

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Functions
      const funcMatch = line.match(/^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)/);
      if (funcMatch) {
        const doc = this.extractPythonDocstring(lines, i + 1);
        symbols.push({
          name: funcMatch[1],
          type: "function",
          file,
          line: i + 1,
          signature: `def ${funcMatch[1]}(${funcMatch[2]})`,
          doc,
        });
      }

      // Classes
      const classMatch = line.match(/^class\s+(\w+)(?:\(([^)]*)\))?:/);
      if (classMatch) {
        const doc = this.extractPythonDocstring(lines, i + 1);
        symbols.push({
          name: classMatch[1],
          type: "class",
          file,
          line: i + 1,
          signature: `class ${classMatch[1]}${classMatch[2] ? `(${classMatch[2]})` : ""}`,
          doc,
        });
      }
    }

    return symbols;
  }

  private parseTypeScript(content: string, file: string): ParsedSymbol[] {
    const symbols: ParsedSymbol[] = [];
    const lines = content.split("\n");

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Functions
      const funcMatch = line.match(
        /(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)/
      );
      if (funcMatch) {
        const doc = this.extractJSDoc(lines, i);
        symbols.push({
          name: funcMatch[1],
          type: "function",
          file,
          line: i + 1,
          signature: `function ${funcMatch[1]}(${funcMatch[2].trim()})`,
          doc,
        });
      }

      // Arrow functions
      const arrowMatch = line.match(
        /(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(/
      );
      if (arrowMatch) {
        symbols.push({
          name: arrowMatch[1],
          type: "function",
          file,
          line: i + 1,
          signature: line.trim(),
        });
      }

      // Classes
      const classMatch = line.match(
        /(?:export\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?/
      );
      if (classMatch) {
        const doc = this.extractJSDoc(lines, i);
        symbols.push({
          name: classMatch[1],
          type: "class",
          file,
          line: i + 1,
          signature: line.trim(),
          doc,
        });
      }

      // Interfaces
      const ifaceMatch = line.match(
        /(?:export\s+)?interface\s+(\w+)/
      );
      if (ifaceMatch) {
        symbols.push({
          name: ifaceMatch[1],
          type: "interface",
          file,
          line: i + 1,
          signature: line.trim(),
        });
      }
    }

    return symbols;
  }

  private parseMarkdown(content: string, file: string): ParsedSymbol[] {
    const symbols: ParsedSymbol[] = [];
    const lines = content.split("\n");

    for (let i = 0; i < lines.length; i++) {
      const hMatch = lines[i].match(/^(#{1,3})\s+(.+)/);
      if (hMatch) {
        symbols.push({
          name: hMatch[2].trim(),
          type: "variable", // Using variable type for headings
          file,
          line: i + 1,
          doc: `Heading level ${hMatch[1].length}`,
        });
      }
    }

    return symbols;
  }

  private extractPythonDocstring(lines: string[], startLine: number): string | undefined {
    if (startLine >= lines.length) return undefined;
    const line = lines[startLine].trim();
    if (line.startsWith('"""') || line.startsWith("'''")) {
      const quote = line.slice(0, 3);
      if (line.endsWith(quote) && line.length > 6) {
        return line.slice(3, -3).trim();
      }
      // Multi-line docstring
      const parts = [line.slice(3)];
      for (let i = startLine + 1; i < lines.length; i++) {
        if (lines[i].trim().endsWith(quote)) {
          parts.push(lines[i].trim().slice(0, -3));
          break;
        }
        parts.push(lines[i].trim());
      }
      return parts.join(" ").trim();
    }
    return undefined;
  }

  private extractJSDoc(lines: string[], funcLine: number): string | undefined {
    if (funcLine === 0) return undefined;
    // Look for /** ... */ above function
    let i = funcLine - 1;
    while (i >= 0 && lines[i].trim() === "") i--;
    if (i < 0) return undefined;

    if (lines[i].trim().endsWith("*/")) {
      const parts: string[] = [];
      while (i >= 0) {
        const trimmed = lines[i].trim();
        parts.unshift(trimmed.replace(/^\/?\*+\s?/, "").replace(/\*\/\s*$/, "").trim());
        if (trimmed.startsWith("/**") || trimmed.startsWith("/*")) break;
        i--;
      }
      return parts.filter(Boolean).join(" ").trim() || undefined;
    }

    return undefined;
  }
}
