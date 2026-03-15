/**
 * Query engine — searches the index for relevant symbols.
 */
import * as fs from "fs";
import { ParsedSymbol } from "./parser";

export interface QueryResult {
  name: string;
  type: string;
  file: string;
  line: number;
  signature?: string;
  doc?: string;
  score: number;
}

export class QueryEngine {
  private indexPath: string;
  private symbols: ParsedSymbol[] = [];

  constructor(indexPath: string) {
    this.indexPath = indexPath;
    this.loadIndex();
  }

  private loadIndex(): void {
    try {
      const raw = fs.readFileSync(this.indexPath, "utf-8");
      this.symbols = JSON.parse(raw);
    } catch {
      this.symbols = [];
    }
  }

  /**
   * Natural language query — ranks results by relevance.
   */
  async query(question: string, topN: number = 5): Promise<QueryResult[]> {
    const terms = question.toLowerCase().split(/\s+/).filter(Boolean);
    const scored: QueryResult[] = [];

    for (const sym of this.symbols) {
      let score = 0;
      const haystack = [
        sym.name,
        sym.type,
        sym.signature || "",
        sym.doc || "",
        sym.file,
      ]
        .join(" ")
        .toLowerCase();

      for (const term of terms) {
        if (sym.name.toLowerCase().includes(term)) score += 10;
        if (sym.doc?.toLowerCase().includes(term)) score += 5;
        if (sym.signature?.toLowerCase().includes(term)) score += 3;
        if (haystack.includes(term)) score += 1;
      }

      if (score > 0) {
        scored.push({ ...sym, score });
      }
    }

    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, topN);
  }

  /**
   * Exact symbol search.
   */
  async search(query: string): Promise<QueryResult[]> {
    const q = query.toLowerCase();
    return this.symbols
      .filter((s) => s.name.toLowerCase().includes(q))
      .map((s) => ({ ...s, score: s.name.toLowerCase() === q ? 100 : 50 }))
      .sort((a, b) => b.score - a.score);
  }
}
