"use client";

import { useState, useCallback } from "react";
import { SQLEditor } from "@/components/editor/SQLEditor";

const EXAMPLE_QUERIES = [
  {
    label: "Simple SELECT",
    query: "SELECT name, price\nFROM products\nWHERE price > 100\nORDER BY price DESC;",
  },
  {
    label: "JOIN + Aggregation",
    query: "SELECT c.name, COUNT(o.id) AS order_count, SUM(o.total_amount) AS total_spent\nFROM customers c\nJOIN orders o ON c.id = o.customer_id\nGROUP BY c.name\nHAVING COUNT(o.id) > 5;",
  },
  {
    label: "Subquery",
    query: "SELECT name, price\nFROM products\nWHERE price > (\n  SELECT AVG(price)\n  FROM products\n)\nORDER BY price;",
  },
  {
    label: "Window Function",
    query: "SELECT name, price,\n  RANK() OVER (ORDER BY price DESC) AS price_rank,\n  price - LAG(price) OVER (ORDER BY price DESC) AS diff_from_prev\nFROM products;",
  },
  {
    label: "CTE + JOIN",
    query: "WITH top_customers AS (\n  SELECT customer_id, SUM(total_amount) AS total\n  FROM orders\n  GROUP BY customer_id\n  ORDER BY total DESC\n  LIMIT 10\n)\nSELECT c.first_name, c.last_name, tc.total\nFROM top_customers tc\nJOIN customers c ON tc.customer_id = c.id;",
  },
];

interface ClauseStep {
  clause: string;
  keyword: string;
  description: string;
  detail: string;
}

function parseQueryClauses(sql: string): ClauseStep[] {
  const upper = sql.toUpperCase();
  const steps: ClauseStep[] = [];

  // CTE detection
  if (upper.trimStart().startsWith("WITH")) {
    const cteMatch = sql.match(/WITH\s+(\w+)\s+AS/i);
    steps.push({
      clause: "CTE",
      keyword: "WITH",
      description: `Define temporary result set${cteMatch ? ` "${cteMatch[1]}"` : ""}`,
      detail: "Common Table Expressions create named temporary results that can be referenced in the main query. They improve readability and allow recursive queries.",
    });
  }

  // FROM clause
  const fromMatch = sql.match(/FROM\s+([\w,\s]+?)(?:\s+(?:WHERE|JOIN|INNER|LEFT|RIGHT|FULL|CROSS|GROUP|ORDER|HAVING|LIMIT|;|$))/i);
  if (fromMatch) {
    const tables = fromMatch[1].trim().split(/\s*,\s*/);
    steps.push({
      clause: "FROM",
      keyword: "FROM",
      description: `Read from ${tables.length > 1 ? "tables" : "table"}: ${tables.join(", ")}`,
      detail: `The database engine starts by identifying the source table(s). ${tables.length > 1 ? "Multiple tables listed here will produce a cross join unless filtered by WHERE." : "All rows from this table are initially considered."}`,
    });
  }

  // JOIN clauses
  const joinRegex = /((?:INNER|LEFT|RIGHT|FULL|CROSS)\s+)?JOIN\s+(\w+)\s+(?:\w+\s+)?ON\s+([^)]+?)(?=\s+(?:WHERE|JOIN|INNER|LEFT|RIGHT|FULL|GROUP|ORDER|HAVING|LIMIT|;|$))/gi;
  let joinMatch;
  while ((joinMatch = joinRegex.exec(sql)) !== null) {
    const joinType = (joinMatch[1] || "INNER").trim();
    const table = joinMatch[2];
    const condition = joinMatch[3].trim();
    steps.push({
      clause: "JOIN",
      keyword: `${joinType} JOIN`,
      description: `Combine with "${table}" on ${condition}`,
      detail: `${joinType} JOIN matches rows from the current result with rows in "${table}" where ${condition}. ${joinType === "LEFT" ? "All rows from the left table are kept, even without matches." : joinType === "INNER" ? "Only matching rows from both sides are kept." : ""}`,
    });
  }

  // WHERE clause
  const whereMatch = sql.match(/WHERE\s+(.+?)(?=\s+(?:GROUP|ORDER|HAVING|LIMIT|;|$))/i);
  if (whereMatch) {
    steps.push({
      clause: "WHERE",
      keyword: "WHERE",
      description: `Filter: ${whereMatch[1].trim().substring(0, 80)}`,
      detail: "WHERE filters individual rows before any grouping occurs. Only rows satisfying all conditions pass through to the next step.",
    });
  }

  // GROUP BY
  const groupMatch = sql.match(/GROUP\s+BY\s+(.+?)(?=\s+(?:HAVING|ORDER|LIMIT|;|$))/i);
  if (groupMatch) {
    steps.push({
      clause: "GROUP BY",
      keyword: "GROUP BY",
      description: `Group rows by: ${groupMatch[1].trim()}`,
      detail: "GROUP BY collapses multiple rows into groups. Each group becomes one output row. Any non-aggregated column in SELECT must appear in GROUP BY.",
    });
  }

  // HAVING
  const havingMatch = sql.match(/HAVING\s+(.+?)(?=\s+(?:ORDER|LIMIT|;|$))/i);
  if (havingMatch) {
    steps.push({
      clause: "HAVING",
      keyword: "HAVING",
      description: `Filter groups: ${havingMatch[1].trim()}`,
      detail: "HAVING filters after grouping (unlike WHERE which filters before). Use HAVING for conditions on aggregate values like COUNT, SUM, AVG.",
    });
  }

  // SELECT
  const selectMatch = sql.match(/SELECT\s+(.*?)(?=\s+FROM)/i);
  if (selectMatch) {
    const cols = selectMatch[1].trim();
    steps.push({
      clause: "SELECT",
      keyword: "SELECT",
      description: `Choose columns: ${cols.substring(0, 80)}${cols.length > 80 ? "..." : ""}`,
      detail: "SELECT determines which columns appear in the final output. Expressions, aliases, and aggregate functions are evaluated here.",
    });
  }

  // Window functions
  if (/OVER\s*\(/i.test(sql)) {
    steps.push({
      clause: "WINDOW",
      keyword: "OVER()",
      description: "Evaluate window functions across partitions",
      detail: "Window functions compute values across a set of rows related to the current row. Unlike GROUP BY, they don't collapse rows — each row keeps its identity.",
    });
  }

  // ORDER BY
  const orderMatch = sql.match(/ORDER\s+BY\s+(.+?)(?=\s+(?:LIMIT|;|$))/i);
  if (orderMatch) {
    steps.push({
      clause: "ORDER BY",
      keyword: "ORDER BY",
      description: `Sort by: ${orderMatch[1].trim()}`,
      detail: "ORDER BY sorts the final result set. ASC (ascending) is the default. This is one of the last operations — it works on the already-filtered, grouped result.",
    });
  }

  // LIMIT
  const limitMatch = sql.match(/LIMIT\s+(\d+)/i);
  if (limitMatch) {
    steps.push({
      clause: "LIMIT",
      keyword: "LIMIT",
      description: `Return first ${limitMatch[1]} rows`,
      detail: "LIMIT restricts the number of rows returned. Applied after all other operations. Combined with ORDER BY, it gives you the top N results.",
    });
  }

  return steps;
}

const CLAUSE_COLORS: Record<string, string> = {
  CTE: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
  FROM: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  JOIN: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300",
  WHERE: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
  "GROUP BY": "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  HAVING: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
  SELECT: "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300",
  WINDOW: "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300",
  "ORDER BY": "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300",
  LIMIT: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
};

export default function AnalyzerPage() {
  const [query, setQuery] = useState(EXAMPLE_QUERIES[0].query);
  const [activeStep, setActiveStep] = useState<number | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const steps = parseQueryClauses(query);

  const handleAnalyze = useCallback(() => {
    setActiveStep(null);
    setIsPlaying(true);
    let i = 0;
    const interval = setInterval(() => {
      setActiveStep(i);
      i++;
      if (i >= steps.length) {
        clearInterval(interval);
        setIsPlaying(false);
      }
    }, 1200);
    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Query Analyzer</h1>
          <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
            Visualize how SQL queries execute step by step
          </p>
        </div>
        <select
          onChange={(e) => {
            const ex = EXAMPLE_QUERIES[parseInt(e.target.value)];
            if (ex) { setQuery(ex.query); setActiveStep(null); }
          }}
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          {EXAMPLE_QUERIES.map((ex, i) => (
            <option key={i} value={i}>{ex.label}</option>
          ))}
        </select>
      </div>

      {/* Editor + Visualization */}
      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Editor */}
        <div className="overflow-hidden rounded-lg border border-[var(--color-border)]">
          <div className="h-[300px]">
            <SQLEditor
              value={query}
              onChange={(v) => { setQuery(v); setActiveStep(null); }}
              onRun={handleAnalyze}
              dialect="postgresql"
            />
          </div>
        </div>

        {/* Stats */}
        <div className="space-y-4">
          <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
            <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
              Query Stats
            </h3>
            <div className="mt-3 grid grid-cols-3 gap-4">
              <div>
                <p className="text-2xl font-bold text-[var(--color-text-primary)]">{steps.length}</p>
                <p className="text-xs text-[var(--color-text-muted)]">Clauses</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-[var(--color-text-primary)]">
                  {(query.match(/JOIN/gi) || []).length}
                </p>
                <p className="text-xs text-[var(--color-text-muted)]">Joins</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-[var(--color-text-primary)]">
                  {query.split("\n").length}
                </p>
                <p className="text-xs text-[var(--color-text-muted)]">Lines</p>
              </div>
            </div>
          </div>

          {/* Playback controls */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleAnalyze}
              disabled={isPlaying}
              className="flex items-center gap-2 rounded-md bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
              {isPlaying ? "Playing..." : "Analyze"}
            </button>
            <button
              onClick={() => setActiveStep(null)}
              className="rounded-md border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:bg-[var(--color-surface)]"
            >
              Reset
            </button>
            {steps.length > 0 && (
              <div className="flex items-center gap-1">
                {steps.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setActiveStep(i)}
                    className={`h-2 w-2 rounded-full transition-all ${
                      activeStep !== null && i <= activeStep
                        ? "bg-[var(--color-accent)]"
                        : "bg-[var(--color-border)]"
                    }`}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Execution steps */}
      <div className="mt-8">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Execution Order
          <span className="ml-2 text-xs font-normal text-[var(--color-text-muted)]">
            SQL executes in a specific order, not top-to-bottom
          </span>
        </h2>

        <div className="mt-4 space-y-3">
          {steps.map((step, i) => {
            const isActive = activeStep !== null && i <= activeStep;
            const isCurrent = activeStep === i;
            const colorClass = CLAUSE_COLORS[step.clause] || CLAUSE_COLORS.LIMIT;

            return (
              <button
                key={i}
                onClick={() => setActiveStep(i)}
                className={`w-full text-left rounded-lg border p-4 transition-all ${
                  isCurrent
                    ? "border-[var(--color-accent)] shadow-md"
                    : isActive
                    ? "border-[var(--color-border)] bg-[var(--color-surface)]"
                    : "border-[var(--color-border)] opacity-50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[var(--color-accent)] text-xs font-bold text-white">
                    {i + 1}
                  </span>
                  <span className={`rounded-md px-2 py-0.5 text-xs font-bold ${colorClass}`}>
                    {step.keyword}
                  </span>
                  <span className="text-sm text-[var(--color-text-primary)]">
                    {step.description}
                  </span>
                </div>
                {isCurrent && (
                  <p className="mt-2 ml-9 text-xs leading-relaxed text-[var(--color-text-secondary)]">
                    {step.detail}
                  </p>
                )}
              </button>
            );
          })}

          {steps.length === 0 && (
            <p className="py-8 text-center text-sm text-[var(--color-text-muted)]">
              Enter a SQL query and click Analyze to see the execution steps.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
