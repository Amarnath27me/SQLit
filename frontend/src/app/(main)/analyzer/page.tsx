"use client";

import { useState, useCallback, useRef } from "react";
import { SQLEditor } from "@/components/editor/SQLEditor";
import { apiClient } from "@/lib/api";

/* ── Example Queries ── */
const EXAMPLES = [
  {
    label: "Simple SELECT",
    query: "SELECT name, price\nFROM products\nWHERE price > 100\nORDER BY price DESC;",
    dataset: "ecommerce",
  },
  {
    label: "JOIN + Aggregation",
    query: "SELECT c.name, COUNT(o.id) AS order_count, SUM(o.total_amount) AS total_spent\nFROM customers c\nJOIN orders o ON c.id = o.customer_id\nGROUP BY c.name\nHAVING COUNT(o.id) > 5;",
    dataset: "ecommerce",
  },
  {
    label: "Subquery",
    query: "SELECT name, price\nFROM products\nWHERE price > (\n  SELECT AVG(price)\n  FROM products\n)\nORDER BY price;",
    dataset: "ecommerce",
  },
  {
    label: "Window Function",
    query: "SELECT name, price,\n  RANK() OVER (ORDER BY price DESC) AS price_rank,\n  price - LAG(price) OVER (ORDER BY price DESC) AS diff_from_prev\nFROM products;",
    dataset: "ecommerce",
  },
  {
    label: "CTE + JOIN",
    query: "WITH top_customers AS (\n  SELECT customer_id, SUM(total_amount) AS total\n  FROM orders\n  GROUP BY customer_id\n  ORDER BY total DESC\n  LIMIT 10\n)\nSELECT c.first_name, c.last_name, tc.total\nFROM top_customers tc\nJOIN customers c ON tc.customer_id = c.id;",
    dataset: "ecommerce",
  },
];

/* ── Types ── */
interface ExecutionStep {
  order: number;
  clause: string;
  keyword: string;
  sqlFragment: string;
  description: string;
  detail: string;
  rowCount: number | null;
  partialQuery: string | null;
}

/* ── SQL Execution Order ── */
const EXECUTION_ORDER = [
  "CTE", "FROM", "JOIN", "WHERE", "GROUP BY", "HAVING", "SELECT", "WINDOW", "DISTINCT", "ORDER BY", "LIMIT",
];

/* ── Parse query into execution steps ── */
function parseQuerySteps(sql: string): Omit<ExecutionStep, "rowCount">[] {
  const steps: Omit<ExecutionStep, "rowCount">[] = [];
  const trimmed = sql.trim().replace(/;+\s*$/, "");

  // CTE
  const cteMatch = trimmed.match(/^WITH\s+(\w+)\s+AS\s*\(/i);
  if (cteMatch) {
    const cteBody = extractCTEBody(trimmed);
    steps.push({
      order: 0,
      clause: "CTE",
      keyword: "WITH",
      sqlFragment: `WITH ${cteMatch[1]} AS (...)`,
      description: `Define temporary result set "${cteMatch[1]}"`,
      detail: "CTEs create named temporary results that exist only for this query. The database materializes this result first, then uses it in the main query. Think of it as a temporary table.",
      partialQuery: cteBody ? `${cteBody.fullCte}\nSELECT COUNT(*) AS rows FROM ${cteMatch[1]}` : null,
    });
  }

  // FROM
  const fromMatch = trimmed.match(/FROM\s+([\w.]+)(?:\s+(\w+))?/i);
  if (fromMatch) {
    const table = fromMatch[1];
    const alias = fromMatch[2] && !isKeyword(fromMatch[2]) ? ` ${fromMatch[2]}` : "";
    steps.push({
      order: 1,
      clause: "FROM",
      keyword: "FROM",
      sqlFragment: `FROM ${table}${alias}`,
      description: `Load all rows from "${table}"`,
      detail: `The database starts here — not at SELECT. It loads the entire "${table}" table into memory (or streams it). Every row is initially included. This is step 1 of every query.`,
      partialQuery: `SELECT COUNT(*) AS rows FROM ${table}`,
    });
  }

  // JOINs
  const joinRegex = /((?:INNER|LEFT|RIGHT|FULL|CROSS)\s+)?JOIN\s+([\w.]+)\s+(?:(\w+)\s+)?ON\s+(.+?)(?=\s+(?:WHERE|JOIN|INNER|LEFT|RIGHT|FULL|CROSS|GROUP|ORDER|HAVING|LIMIT|$))/gi;
  let jm;
  const joinSteps: Omit<ExecutionStep, "rowCount">[] = [];
  while ((jm = joinRegex.exec(trimmed)) !== null) {
    const jType = (jm[1] || "INNER").trim();
    const jTable = jm[2];
    const condition = jm[4].trim();
    joinSteps.push({
      order: 2,
      clause: "JOIN",
      keyword: `${jType} JOIN`,
      sqlFragment: `${jType} JOIN ${jTable} ON ${condition}`,
      description: `Combine with "${jTable}" on ${truncate(condition, 60)}`,
      detail: `${jType} JOIN matches every row from the current result with rows in "${jTable}" where ${condition}. ${jType === "LEFT" ? "All left-side rows are kept even without matches (NULLs fill in)." : jType === "INNER" ? "Only matching rows from both sides survive." : `${jType} join semantics apply.`} This can multiply or reduce rows.`,
      partialQuery: buildPartialUpTo(trimmed, "JOIN", jm.index + jm[0].length),
    });
  }
  steps.push(...joinSteps);

  // WHERE
  const whereMatch = trimmed.match(/WHERE\s+(.+?)(?=\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$))/i);
  if (whereMatch) {
    steps.push({
      order: 3,
      clause: "WHERE",
      keyword: "WHERE",
      sqlFragment: `WHERE ${truncate(whereMatch[1].trim(), 80)}`,
      description: `Filter rows: ${truncate(whereMatch[1].trim(), 60)}`,
      detail: "WHERE filters individual rows BEFORE any grouping. Only rows passing all conditions move to the next step. This is why you can't use aggregate functions (SUM, COUNT) in WHERE — groups don't exist yet.",
      partialQuery: buildPartialUpTo(trimmed, "WHERE"),
    });
  }

  // GROUP BY
  const groupMatch = trimmed.match(/GROUP\s+BY\s+(.+?)(?=\s+(?:HAVING|ORDER\s+BY|LIMIT|$))/i);
  if (groupMatch) {
    const cols = groupMatch[1].trim();
    steps.push({
      order: 4,
      clause: "GROUP BY",
      keyword: "GROUP BY",
      sqlFragment: `GROUP BY ${cols}`,
      description: `Group rows by: ${truncate(cols, 60)}`,
      detail: "GROUP BY collapses many rows into groups. 1000 rows might become 50 groups. After this step, you can only reference grouped columns or aggregate functions (SUM, COUNT, AVG). Each group becomes one row in the output.",
      partialQuery: buildPartialUpTo(trimmed, "GROUP BY"),
    });
  }

  // HAVING
  const havingMatch = trimmed.match(/HAVING\s+(.+?)(?=\s+(?:ORDER\s+BY|LIMIT|$))/i);
  if (havingMatch) {
    steps.push({
      order: 5,
      clause: "HAVING",
      keyword: "HAVING",
      sqlFragment: `HAVING ${truncate(havingMatch[1].trim(), 80)}`,
      description: `Filter groups: ${truncate(havingMatch[1].trim(), 60)}`,
      detail: "HAVING filters AFTER grouping — it's like WHERE but for groups. This is where you filter by aggregate values (e.g., HAVING COUNT(*) > 5). Groups that don't meet the condition are dropped.",
      partialQuery: buildPartialUpTo(trimmed, "HAVING"),
    });
  }

  // SELECT
  const selectMatch = trimmed.match(/SELECT\s+(.*?)(?=\s+FROM)/i);
  if (selectMatch) {
    const cols = selectMatch[1].trim();
    const hasAgg = /(?:COUNT|SUM|AVG|MIN|MAX)\s*\(/i.test(cols);
    const hasAlias = /\sAS\s/i.test(cols);
    steps.push({
      order: 6,
      clause: "SELECT",
      keyword: "SELECT",
      sqlFragment: `SELECT ${truncate(cols, 80)}`,
      description: `Choose columns: ${truncate(cols, 60)}`,
      detail: `SELECT determines the output columns. ${hasAgg ? "Aggregate functions (SUM, COUNT, etc.) are calculated here." : ""} ${hasAlias ? "Column aliases (AS ...) are created here — they can't be used in WHERE or GROUP BY because those ran earlier." : ""} This runs AFTER filtering and grouping, not before.`,
      partialQuery: null,
    });
  }

  // Window functions
  if (/OVER\s*\(/i.test(trimmed)) {
    steps.push({
      order: 7,
      clause: "WINDOW",
      keyword: "WINDOW",
      sqlFragment: "OVER(...)",
      description: "Evaluate window functions across partitions",
      detail: "Window functions run AFTER SELECT on the result rows. Unlike GROUP BY, they don't collapse rows — each row gets its own computed value based on its partition/window. RANK(), ROW_NUMBER(), LAG(), LEAD() all run here.",
      partialQuery: null,
    });
  }

  // DISTINCT
  if (/SELECT\s+DISTINCT\s/i.test(trimmed)) {
    steps.push({
      order: 8,
      clause: "DISTINCT",
      keyword: "DISTINCT",
      sqlFragment: "DISTINCT",
      description: "Remove duplicate rows from result",
      detail: "DISTINCT eliminates duplicate rows AFTER SELECT has computed all columns. Two rows are duplicates only if every column value matches. This can significantly reduce row count.",
      partialQuery: null,
    });
  }

  // ORDER BY
  const orderMatch = trimmed.match(/ORDER\s+BY\s+(.+?)(?=\s+(?:LIMIT|OFFSET|$))/i);
  if (orderMatch) {
    steps.push({
      order: 9,
      clause: "ORDER BY",
      keyword: "ORDER BY",
      sqlFragment: `ORDER BY ${orderMatch[1].trim()}`,
      description: `Sort by: ${truncate(orderMatch[1].trim(), 60)}`,
      detail: "ORDER BY sorts the final result. It runs near-last — after all filtering, grouping, and column selection. ASC is default. Sorting is expensive on large datasets — it requires comparing every row.",
      partialQuery: null,
    });
  }

  // LIMIT
  const limitMatch = trimmed.match(/LIMIT\s+(\d+)/i);
  if (limitMatch) {
    steps.push({
      order: 10,
      clause: "LIMIT",
      keyword: "LIMIT",
      sqlFragment: `LIMIT ${limitMatch[1]}`,
      description: `Return only ${limitMatch[1]} rows`,
      detail: `LIMIT is the very last operation. After everything else is done, LIMIT chops the result to ${limitMatch[1]} rows. Combined with ORDER BY, it gives you "top N" results.`,
      partialQuery: null,
    });
  }

  // Sort by execution order
  steps.sort((a, b) => a.order - b.order);
  return steps;
}

/* ── Helpers ── */
function truncate(s: string, len: number): string {
  return s.length > len ? s.substring(0, len) + "..." : s;
}

function isKeyword(s: string): boolean {
  return ["WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS", "ON", "GROUP", "ORDER", "HAVING", "LIMIT", "AS", "AND", "OR", "SET"].includes(s.toUpperCase());
}

function extractCTEBody(sql: string): { fullCte: string } | null {
  const match = sql.match(/^(WITH\s+\w+\s+AS\s*\([\s\S]*?\))/i);
  return match ? { fullCte: match[1] } : null;
}

function buildPartialUpTo(sql: string, clause: string, endPos?: number): string | null {
  const trimmed = sql.trim().replace(/;+\s*$/, "");

  // Extract FROM clause table
  const fromMatch = trimmed.match(/FROM\s+([\w.]+)(?:\s+(\w+))?/i);
  if (!fromMatch) return null;

  // Build partial query step by step
  let fromPart = `FROM ${fromMatch[1]}`;
  if (fromMatch[2] && !isKeyword(fromMatch[2])) fromPart += ` ${fromMatch[2]}`;

  // Add JOINs if clause is JOIN or later
  const joinOrder = EXECUTION_ORDER.indexOf("JOIN");
  const clauseOrder = EXECUTION_ORDER.indexOf(clause);

  let joins = "";
  if (clauseOrder >= joinOrder) {
    const joinRegex = /((?:INNER|LEFT|RIGHT|FULL|CROSS)\s+)?JOIN\s+[\w.]+\s+(?:\w+\s+)?ON\s+.+?(?=\s+(?:WHERE|JOIN|INNER|LEFT|RIGHT|FULL|CROSS|GROUP|ORDER|HAVING|LIMIT|$))/gi;
    let jm;
    while ((jm = joinRegex.exec(trimmed)) !== null) {
      if (clause === "JOIN" && endPos && jm.index + jm[0].length > endPos) break;
      joins += "\n" + jm[0];
    }
  }

  // Add WHERE if applicable
  let where = "";
  if (clauseOrder >= EXECUTION_ORDER.indexOf("WHERE")) {
    const wm = trimmed.match(/WHERE\s+(.+?)(?=\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$))/i);
    if (wm) where = `\nWHERE ${wm[1].trim()}`;
  }

  // Add GROUP BY if applicable
  let groupBy = "";
  if (clauseOrder >= EXECUTION_ORDER.indexOf("GROUP BY")) {
    const gm = trimmed.match(/GROUP\s+BY\s+(.+?)(?=\s+(?:HAVING|ORDER\s+BY|LIMIT|$))/i);
    if (gm) groupBy = `\nGROUP BY ${gm[1].trim()}`;
  }

  // Add HAVING if applicable
  let having = "";
  if (clauseOrder >= EXECUTION_ORDER.indexOf("HAVING")) {
    const hm = trimmed.match(/HAVING\s+(.+?)(?=\s+(?:ORDER\s+BY|LIMIT|$))/i);
    if (hm) having = `\nHAVING ${hm[1].trim()}`;
  }

  return `SELECT COUNT(*) AS rows ${fromPart}${joins}${where}${groupBy}${having}`;
}

/* ── Clause Colors ── */
const CLAUSE_COLORS: Record<string, string> = {
  CTE: "bg-purple-500/20 text-purple-400 border-purple-500/40",
  FROM: "bg-blue-500/20 text-blue-400 border-blue-500/40",
  JOIN: "bg-cyan-500/20 text-cyan-400 border-cyan-500/40",
  WHERE: "bg-amber-500/20 text-amber-400 border-amber-500/40",
  "GROUP BY": "bg-green-500/20 text-green-400 border-green-500/40",
  HAVING: "bg-emerald-500/20 text-emerald-400 border-emerald-500/40",
  SELECT: "bg-indigo-500/20 text-indigo-400 border-indigo-500/40",
  WINDOW: "bg-pink-500/20 text-pink-400 border-pink-500/40",
  DISTINCT: "bg-violet-500/20 text-violet-400 border-violet-500/40",
  "ORDER BY": "bg-orange-500/20 text-orange-400 border-orange-500/40",
  LIMIT: "bg-gray-500/20 text-gray-400 border-gray-500/40",
};

const CLAUSE_ICONS: Record<string, string> = {
  CTE: "📦", FROM: "📂", JOIN: "🔗", WHERE: "🔍",
  "GROUP BY": "📊", HAVING: "🎯", SELECT: "✂️",
  WINDOW: "🪟", DISTINCT: "🔲", "ORDER BY": "↕️", LIMIT: "✋",
};

/* ── Component ── */
export default function AnalyzerPage() {
  const [query, setQuery] = useState(EXAMPLES[0].query);
  const [dataset, setDataset] = useState(EXAMPLES[0].dataset);
  const [activeStep, setActiveStep] = useState<number | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [executionSteps, setExecutionSteps] = useState<ExecutionStep[]>([]);
  const [finalResult, setFinalResult] = useState<{
    columns: string[];
    rows: unknown[][];
    rowCount: number;
    executionTimeMs: number;
  } | null>(null);
  const [analyzed, setAnalyzed] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const handleAnalyze = useCallback(async () => {
    if (!query.trim()) return;

    setIsAnalyzing(true);
    setAnalyzed(false);
    setActiveStep(null);
    setFinalResult(null);

    // Parse the query into steps
    const parsed = parseQuerySteps(query);

    // Execute partial queries to get row counts at each step
    const stepsWithCounts: ExecutionStep[] = [];

    for (const step of parsed) {
      let rowCount: number | null = null;
      if (step.partialQuery) {
        try {
          const data = await apiClient<{
            user_result?: { columns: string[]; rows: unknown[][]; row_count?: number };
            error?: string;
          }>("/api/query/execute", {
            method: "POST",
            body: JSON.stringify({ query: step.partialQuery, dataset }),
          });
          if (data.user_result?.rows?.[0]?.[0] != null) {
            rowCount = Number(data.user_result.rows[0][0]);
          }
        } catch {
          // Partial query failed — that's fine, just skip the count
        }
      }
      stepsWithCounts.push({ ...step, rowCount });
    }

    // Execute the full query for final result
    try {
      const data = await apiClient<{
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        user_result?: any;
        error?: string;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({ query: query.trim(), dataset }),
      });
      if (data.user_result) {
        setFinalResult({
          columns: data.user_result.columns,
          rows: data.user_result.rows,
          rowCount: data.user_result.row_count ?? data.user_result.rowCount ?? 0,
          executionTimeMs: data.user_result.execution_time_ms ?? data.user_result.executionTimeMs ?? 0,
        });
      }
    } catch {
      // Full query failed
    }

    setExecutionSteps(stepsWithCounts);
    setAnalyzed(true);
    setIsAnalyzing(false);

    // Start playback
    setIsPlaying(true);
    let i = 0;
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setActiveStep(i);
      i++;
      if (i >= stepsWithCounts.length) {
        if (intervalRef.current) clearInterval(intervalRef.current);
        setIsPlaying(false);
      }
    }, 1200);
  }, [query, dataset]);

  const steps = analyzed ? executionSteps : parseQuerySteps(query).map((s) => ({ ...s, rowCount: null }));

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Query Execution Visualizer
          </h1>
          <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
            SQL doesn&apos;t execute top-to-bottom. See the real execution order with intermediate row counts.
          </p>
        </div>
        <div className="flex gap-2">
          <select
            value={dataset}
            onChange={(e) => setDataset(e.target.value)}
            className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
          >
            <option value="ecommerce">E-Commerce</option>
            <option value="finance">Finance</option>
            <option value="healthcare">Healthcare</option>
          </select>
          <select
            onChange={(e) => {
              const ex = EXAMPLES[parseInt(e.target.value)];
              if (ex) {
                setQuery(ex.query);
                setDataset(ex.dataset);
                setActiveStep(null);
                setAnalyzed(false);
                setExecutionSteps([]);
                setFinalResult(null);
              }
            }}
            className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
          >
            {EXAMPLES.map((ex, i) => (
              <option key={i} value={i}>{ex.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Key insight banner */}
      <div className="mt-4 rounded-lg border border-[var(--color-accent)]/20 bg-[var(--color-accent)]/5 px-4 py-3">
        <p className="text-xs text-[var(--color-text-secondary)]">
          <span className="font-semibold text-[var(--color-accent)]">Key insight:</span>{" "}
          SQL executes FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.
          The SELECT you write first actually runs near-last.
        </p>
      </div>

      {/* Editor + Controls */}
      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="overflow-hidden rounded-lg border border-[var(--color-border)]">
          <div className="h-[280px]">
            <SQLEditor
              value={query}
              onChange={(v) => {
                setQuery(v);
                setActiveStep(null);
                setAnalyzed(false);
                setExecutionSteps([]);
                setFinalResult(null);
              }}
              onRun={handleAnalyze}
              dialect="postgresql"
            />
          </div>
        </div>

        <div className="space-y-4">
          {/* Stats */}
          <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
            <div className="grid grid-cols-4 gap-3 text-center">
              <div>
                <p className="text-xl font-bold text-[var(--color-text-primary)]">{steps.length}</p>
                <p className="text-[10px] text-[var(--color-text-muted)]">Steps</p>
              </div>
              <div>
                <p className="text-xl font-bold text-[var(--color-text-primary)]">
                  {(query.match(/JOIN/gi) || []).length}
                </p>
                <p className="text-[10px] text-[var(--color-text-muted)]">Joins</p>
              </div>
              <div>
                <p className="text-xl font-bold text-[var(--color-text-primary)]">
                  {finalResult?.rowCount ?? "—"}
                </p>
                <p className="text-[10px] text-[var(--color-text-muted)]">Final Rows</p>
              </div>
              <div>
                <p className="text-xl font-bold text-[var(--color-text-primary)]">
                  {finalResult ? `${finalResult.executionTimeMs}ms` : "—"}
                </p>
                <p className="text-[10px] text-[var(--color-text-muted)]">Time</p>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleAnalyze}
              disabled={isPlaying || isAnalyzing || !query.trim()}
              className="flex items-center gap-2 rounded-md bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
            >
              {isAnalyzing ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Analyzing...
                </>
              ) : (
                <>
                  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  Analyze
                </>
              )}
            </button>
            <button
              onClick={() => {
                setActiveStep(null);
                if (intervalRef.current) clearInterval(intervalRef.current);
                setIsPlaying(false);
              }}
              className="rounded-md border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:bg-[var(--color-surface)]"
            >
              Reset
            </button>
            {steps.length > 0 && (
              <div className="flex items-center gap-1">
                {steps.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => { setActiveStep(i); setIsPlaying(false); if (intervalRef.current) clearInterval(intervalRef.current); }}
                    className={`h-2.5 w-2.5 rounded-full transition-all ${
                      activeStep !== null && i <= activeStep ? "bg-[var(--color-accent)] scale-110" : "bg-[var(--color-border)]"
                    }`}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Row flow visualization */}
          {analyzed && steps.some((s) => s.rowCount !== null) && (
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
              <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                Row Flow
              </h3>
              <div className="mt-3 flex items-center gap-1 overflow-x-auto">
                {steps.filter((s) => s.rowCount !== null).map((step, i, arr) => {
                  const prev = i > 0 ? arr[i - 1].rowCount! : null;
                  const change = prev !== null ? step.rowCount! - prev : null;
                  return (
                    <div key={i} className="flex items-center gap-1">
                      <div className="flex flex-col items-center">
                        <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold ${CLAUSE_COLORS[step.clause]?.split(" ").slice(0, 2).join(" ") || "bg-gray-500/20 text-gray-400"}`}>
                          {step.keyword}
                        </span>
                        <span className="mt-1 text-xs font-bold text-[var(--color-text-primary)]">
                          {step.rowCount?.toLocaleString()}
                        </span>
                        {change !== null && (
                          <span className={`text-[10px] ${change > 0 ? "text-green-400" : change < 0 ? "text-red-400" : "text-[var(--color-text-muted)]"}`}>
                            {change > 0 ? `+${change.toLocaleString()}` : change.toLocaleString()}
                          </span>
                        )}
                      </div>
                      {i < arr.length - 1 && (
                        <svg className="mx-1 h-4 w-4 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      )}
                    </div>
                  );
                })}
                {finalResult && (
                  <>
                    <svg className="mx-1 h-4 w-4 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    <div className="flex flex-col items-center">
                      <span className="rounded bg-[var(--color-accent)]/20 px-1.5 py-0.5 text-[10px] font-bold text-[var(--color-accent)]">
                        RESULT
                      </span>
                      <span className="mt-1 text-xs font-bold text-[var(--color-accent)]">
                        {finalResult.rowCount.toLocaleString()}
                      </span>
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Execution Steps */}
      <div className="mt-8">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Execution Order
          <span className="ml-2 text-xs font-normal text-[var(--color-text-muted)]">
            Click any step to jump to it
          </span>
        </h2>

        <div className="mt-4 space-y-2">
          {steps.map((step, i) => {
            const isActive = activeStep !== null && i <= activeStep;
            const isCurrent = activeStep === i;
            const colorClass = CLAUSE_COLORS[step.clause] || CLAUSE_COLORS.LIMIT;

            return (
              <button
                key={i}
                onClick={() => {
                  setActiveStep(i);
                  setIsPlaying(false);
                  if (intervalRef.current) clearInterval(intervalRef.current);
                }}
                className={`w-full text-left rounded-lg border p-4 transition-all ${
                  isCurrent
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/5 shadow-md"
                    : isActive
                      ? "border-[var(--color-border)] bg-[var(--color-surface)]"
                      : "border-[var(--color-border)] opacity-40"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[var(--color-accent)] text-xs font-bold text-white">
                    {i + 1}
                  </span>
                  <span className="text-base">{CLAUSE_ICONS[step.clause] || "📋"}</span>
                  <span className={`rounded-md border px-2 py-0.5 text-xs font-bold ${colorClass}`}>
                    {step.keyword}
                  </span>
                  <span className="flex-1 text-sm text-[var(--color-text-primary)]">
                    {step.description}
                  </span>
                  {step.rowCount !== null && (
                    <span className="shrink-0 rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-secondary)]">
                      {step.rowCount.toLocaleString()} rows
                    </span>
                  )}
                </div>

                {isCurrent && (
                  <div className="ml-10 mt-3 space-y-2">
                    <p className="text-xs leading-relaxed text-[var(--color-text-secondary)]">
                      {step.detail}
                    </p>
                    {step.sqlFragment && (
                      <div className="rounded bg-[var(--color-background)] px-3 py-2">
                        <code className="text-xs text-[var(--color-text-primary)]">
                          {step.sqlFragment}
                        </code>
                      </div>
                    )}
                  </div>
                )}
              </button>
            );
          })}

          {steps.length === 0 && (
            <div className="py-12 text-center">
              <p className="text-sm text-[var(--color-text-muted)]">
                Enter a SQL query and click Analyze to see how it executes step by step.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Final Result Preview */}
      {finalResult && finalResult.rows.length > 0 && (
        <div className="mt-6">
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Final Result
            <span className="ml-2 text-xs font-normal text-[var(--color-text-muted)]">
              {finalResult.rowCount} rows • {finalResult.executionTimeMs}ms
            </span>
          </h2>
          <div className="mt-3 max-h-64 overflow-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
            <table className="w-full text-xs">
              <thead className="sticky top-0 bg-[var(--color-surface)]">
                <tr className="border-b border-[var(--color-border)]">
                  {finalResult.columns.map((col) => (
                    <th key={col} className="px-3 py-2 text-left font-medium text-[var(--color-text-muted)]">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {finalResult.rows.map((row, i) => (
                  <tr key={i} className="border-b border-[var(--color-border)]/50 hover:bg-[var(--color-background)]">
                    {row.map((cell, j) => (
                      <td key={j} className={`px-3 py-1.5 font-mono ${cell === null ? "italic text-[var(--color-text-muted)]" : "text-[var(--color-text-secondary)]"}`}>
                        {cell === null ? "NULL" : String(cell)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
