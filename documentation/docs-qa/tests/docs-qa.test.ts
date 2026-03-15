/**
 * Tests for Docs QA agent components.
 */
import { SourceParser, ParsedSymbol } from "../src/parser";
import { QueryEngine } from "../src/query";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

describe("SourceParser", () => {
  let parser: SourceParser;
  let tmpDir: string;

  beforeEach(() => {
    parser = new SourceParser();
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "docs-qa-test-"));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test("parses Python functions", () => {
    const pyFile = path.join(tmpDir, "sample.py");
    fs.writeFileSync(
      pyFile,
      'def greet(name):\n    """Say hello."""\n    return f"Hello, {name}"\n'
    );
    const symbols = parser.parseFile(pyFile);
    expect(symbols.length).toBeGreaterThan(0);
    expect(symbols[0].name).toBe("greet");
    expect(symbols[0].type).toBe("function");
  });

  test("parses Python classes", () => {
    const pyFile = path.join(tmpDir, "models.py");
    fs.writeFileSync(pyFile, "class User:\n    pass\n");
    const symbols = parser.parseFile(pyFile);
    expect(symbols.some((s) => s.name === "User" && s.type === "class")).toBe(true);
  });

  test("parses TypeScript functions", () => {
    const tsFile = path.join(tmpDir, "utils.ts");
    fs.writeFileSync(tsFile, "export function add(a: number, b: number): number {\n  return a + b;\n}\n");
    const symbols = parser.parseFile(tsFile);
    expect(symbols.length).toBeGreaterThan(0);
    expect(symbols[0].name).toBe("add");
  });

  test("parses Markdown headings", () => {
    const mdFile = path.join(tmpDir, "README.md");
    fs.writeFileSync(mdFile, "# Getting Started\n\n## Installation\n\nSome text.\n");
    const symbols = parser.parseFile(mdFile);
    expect(symbols.length).toBe(2);
  });

  test("returns empty for unknown extensions", () => {
    const txtFile = path.join(tmpDir, "data.csv");
    fs.writeFileSync(txtFile, "a,b,c\n1,2,3\n");
    const symbols = parser.parseFile(txtFile);
    expect(symbols.length).toBe(0);
  });
});

describe("QueryEngine", () => {
  let tmpDir: string;
  let indexPath: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "docs-qa-query-"));
    indexPath = path.join(tmpDir, "index.json");
    const symbols: ParsedSymbol[] = [
      { name: "fetchUser", type: "function", file: "api.ts", line: 10, signature: "async function fetchUser(id: string)", doc: "Fetch user by ID" },
      { name: "UserService", type: "class", file: "service.ts", line: 5, doc: "User management service" },
      { name: "calculateTotal", type: "function", file: "utils.ts", line: 20, signature: "function calculateTotal(items: Item[])" },
    ];
    fs.writeFileSync(indexPath, JSON.stringify(symbols));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test("query returns relevant results", async () => {
    const engine = new QueryEngine(indexPath);
    const results = await engine.query("how to fetch user");
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].name).toBe("fetchUser");
  });

  test("search finds exact matches", async () => {
    const engine = new QueryEngine(indexPath);
    const results = await engine.search("UserService");
    expect(results.length).toBe(1);
    expect(results[0].name).toBe("UserService");
  });

  test("search is case insensitive", async () => {
    const engine = new QueryEngine(indexPath);
    const results = await engine.search("userservice");
    expect(results.length).toBe(1);
  });

  test("handles missing index gracefully", async () => {
    const engine = new QueryEngine("/nonexistent/index.json");
    const results = await engine.query("anything");
    expect(results.length).toBe(0);
  });
});
