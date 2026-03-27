"use client";

import { useState, useCallback } from "react";
import { apiClient } from "@/lib/api";
import { SQLEditor } from "@/components/editor/SQLEditor";
import INVESTIGATIONS from "@/data/debug-investigations";
import type { Investigation } from "@/data/debug-investigations";

/* ── Types ── */
interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface QueryLog {
  query: string;
  result: QueryResult | null;
  error: string | null;
  timestamp: number;
}

/* ── Colors ── */
const difficultyColor = {
  easy: "bg-green-500/20 text-green-400 border-green-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  hard: "bg-red-500/20 text-red-400 border-red-500/30",
};

const issueTypeColor: Record<string, string> = {
  "Duplicate Data": "bg-orange-500/20 text-orange-400",
  "Pipeline Gap": "bg-purple-500/20 text-purple-400",
  "Join Explosion": "bg-red-500/20 text-red-400",
  "NULL Handling": "bg-cyan-500/20 text-cyan-400",
  "Aggregation Error": "bg-yellow-500/20 text-yellow-400",
  "Duplicate Counting": "bg-pink-500/20 text-pink-400",
  "Timezone Bug": "bg-blue-500/20 text-blue-400",
  "Pipeline Failure": "bg-amber-500/20 text-amber-400",
  "Refund Miscalculation": "bg-emerald-500/20 text-emerald-400",
  "Referential Integrity": "bg-indigo-500/20 text-indigo-400",
  "Invalid Values": "bg-rose-500/20 text-rose-400",
  "Missing Data": "bg-violet-500/20 text-violet-400",
  "Stale Data": "bg-amber-500/10 text-amber-400",
  "Business Logic": "bg-teal-500/20 text-teal-400",
  "Status Filter Bug": "bg-orange-500/10 text-orange-400",
  "Incorrect Metric": "bg-pink-500/10 text-pink-400",
  "Calculation Error": "bg-red-500/10 text-red-400",
  "Race Condition": "bg-red-500/20 text-red-300",
  "Temporal Anomaly": "bg-cyan-500/10 text-cyan-400",
  "Data Type Truncation": "bg-yellow-500/10 text-yellow-400",
  "Data Type Issue": "bg-yellow-500/10 text-yellow-400",
  "Multi-Source Mismatch": "bg-purple-500/10 text-purple-400",
  "Funnel Logic Error": "bg-blue-500/10 text-blue-400",
  "Statistical Error": "bg-emerald-500/10 text-emerald-400",
  "Window Function Bug": "bg-violet-500/10 text-violet-400",
  "Survivorship Bias": "bg-amber-500/20 text-amber-300",
  "SCD Issue": "bg-indigo-500/10 text-indigo-400",
  "Cohort Analysis Bug": "bg-teal-500/10 text-teal-400",
  "Pattern Detection": "bg-red-500/10 text-red-300",
  "Double Entry Error": "bg-orange-500/20 text-orange-300",
  "Cross-Record Analysis": "bg-blue-500/20 text-blue-300",
  "Attribution Error": "bg-pink-500/20 text-pink-300",
  "Timestamp Arithmetic": "bg-cyan-500/20 text-cyan-300",
  "ETL Dedup Failure": "bg-purple-500/20 text-purple-300",
  "Overlap Counting": "bg-amber-500/10 text-amber-300",
  "Metric Paradox": "bg-emerald-500/20 text-emerald-300",
  "Metric Definition Error": "bg-indigo-500/20 text-indigo-300",
  "Data Migration Bug": "bg-rose-500/10 text-rose-400",
  "Classification Error": "bg-violet-500/20 text-violet-300",
  "Refund Double Counting": "bg-emerald-500/20 text-emerald-400",
};

const datasetLabel: Record<string, string> = {
  ecommerce: "E-Commerce",
  finance: "Finance",
  healthcare: "Healthcare",
};

export default function DebugPage() {
  const [selected, setSelected] = useState<Investigation | null>(null);
  const [query, setQuery] = useState("");
  const [queryHistory, setQueryHistory] = useState<QueryLog[]>([]);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [revealedHints, setRevealedHints] = useState<number>(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [showRootCause, setShowRootCause] = useState(false);
  const [startTime, setStartTime] = useState<number>(0);
  const [tablesExplored, setTablesExplored] = useState<Set<string>>(new Set());
  const [filterDifficulty, setFilterDifficulty] = useState<string>("all");
  const [filterDataset, setFilterDataset] = useState<string>("all");
  const [filterType, setFilterType] = useState<string>("all");

  const issueTypes = [...new Set(INVESTIGATIONS.map((i) => i.issueType))].sort();

  const trackTables = useCallback(
    (sql: string) => {
      if (!selected) return;
      const lower = sql.toLowerCase();
      const found = new Set(tablesExplored);
      selected.tables.forEach((t) => {
        if (lower.includes(t.toLowerCase())) found.add(t);
      });
      setTablesExplored(found);
    },
    [selected, tablesExplored]
  );

  const handleRun = useCallback(async () => {
    if (!selected || !query.trim()) return;
    setRunning(true);
    setError(null);
    setResult(null);
    trackTables(query);

    try {
      const data = await apiClient<{
        user_result: QueryResult;
        status: string;
        error?: string;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({ query: query.trim(), dataset: selected.dataset }),
      });

      if (data.error) {
        setError(data.error);
        setQueryHistory((h) => [{ query: query.trim(), result: null, error: data.error!, timestamp: Date.now() }, ...h]);
      } else if (data.user_result) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const ur = data.user_result as any;
        const normalized: QueryResult = {
          columns: ur.columns,
          rows: ur.rows,
          rowCount: ur.row_count ?? ur.rowCount ?? 0,
          executionTimeMs: ur.execution_time_ms ?? ur.executionTimeMs ?? 0,
        };
        setResult(normalized);
        setQueryHistory((h) => [{ query: query.trim(), result: normalized, error: null, timestamp: Date.now() }, ...h]);
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Query execution failed";
      setError(msg);
      setQueryHistory((h) => [{ query: query.trim(), result: null, error: msg, timestamp: Date.now() }, ...h]);
    } finally {
      setRunning(false);
    }
  }, [query, selected, trackTables]);


  const elapsed = startTime ? Math.floor((Date.now() - startTime) / 1000 / 60) : 0;

  const filtered = INVESTIGATIONS.filter((inv) => {
    if (filterDifficulty !== "all" && inv.difficulty !== filterDifficulty) return false;
    if (filterDataset !== "all" && inv.dataset !== filterDataset) return false;
    if (filterType !== "all" && inv.issueType !== filterType) return false;
    return true;
  });

  const counts = {
    easy: INVESTIGATIONS.filter((i) => i.difficulty === "easy").length,
    medium: INVESTIGATIONS.filter((i) => i.difficulty === "medium").length,
    hard: INVESTIGATIONS.filter((i) => i.difficulty === "hard").length,
  };

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {!selected ? (
        <div>
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Data Debugging
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--color-text-secondary)]">
              Don&apos;t just write SQL — learn to investigate data issues like a real analyst.
              Each scenario presents a business problem with messy data.
              Your job: find what&apos;s wrong, prove it with queries, and explain the root cause.
            </p>
            <div className="mt-4 flex gap-4 text-xs">
              <span className="rounded-full bg-green-500/10 px-3 py-1 text-green-400">
                {counts.easy} Easy
              </span>
              <span className="rounded-full bg-yellow-500/10 px-3 py-1 text-yellow-400">
                {counts.medium} Medium
              </span>
              <span className="rounded-full bg-red-500/10 px-3 py-1 text-red-400">
                {counts.hard} Hard
              </span>
              <span className="rounded-full bg-[var(--color-accent)]/10 px-3 py-1 text-[var(--color-accent)]">
                {INVESTIGATIONS.length} Total
              </span>
            </div>
          </div>

          {/* Filters */}
          <div className="mb-6 flex flex-wrap gap-3">
            <select
              value={filterDataset}
              onChange={(e) => setFilterDataset(e.target.value)}
              aria-label="Filter by dataset"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Datasets</option>
              <option value="ecommerce">E-Commerce</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
            </select>
            <select
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
              aria-label="Filter by difficulty"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              aria-label="Filter by issue type"
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Issue Types</option>
              {issueTypes.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            {(filterDataset !== "all" || filterDifficulty !== "all" || filterType !== "all") && (
              <button
                onClick={() => { setFilterDataset("all"); setFilterDifficulty("all"); setFilterType("all"); }}
                className="rounded-md px-3 py-1.5 text-xs text-[var(--color-accent)] hover:underline"
              >
                Clear filters
              </button>
            )}
          </div>

          {/* Results count */}
          <p className="mb-4 text-xs text-[var(--color-text-muted)]">
            Showing {filtered.length} of {INVESTIGATIONS.length} investigations
          </p>

          {/* Grid */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((inv) => (
              <button
                key={inv.id}
                onClick={() => {
                  setSelected(inv);
                  setQuery("");
                  setResult(null);
                  setError(null);
                  setQueryHistory([]);
                  setRevealedHints(0);
                  setCurrentStep(0);
                  setShowRootCause(false);
                  setStartTime(Date.now());
                  setTablesExplored(new Set());
                }}
                className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5 text-left transition-all hover:border-[var(--color-accent)]/50 hover:shadow-lg"
              >
                <div className="mb-3 flex flex-wrap items-center gap-2">
                  <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${difficultyColor[inv.difficulty]}`}>
                    {inv.difficulty}
                  </span>
                  <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${issueTypeColor[inv.issueType] || "bg-gray-500/20 text-gray-400"}`}>
                    {inv.issueType}
                  </span>
                  <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-muted)]">
                    {datasetLabel[inv.dataset]}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                  {inv.title}
                </h3>
                <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-[var(--color-text-muted)]">
                  {inv.context}
                </p>
                <div className="mt-3 text-[10px] text-[var(--color-text-muted)]">
                  Tables: {inv.tables.join(", ")}
                </div>
              </button>
            ))}
          </div>

          {filtered.length === 0 && (
            <div className="mt-8 text-center text-sm text-[var(--color-text-muted)]">
              No investigations match your filters.
            </div>
          )}
        </div>
      ) : (
        /* ── Investigation Detail ── */
        <div>
          <button
            onClick={() => setSelected(null)}
            className="mb-4 text-xs font-medium text-[var(--color-accent)] hover:underline"
          >
            ← Back to investigations
          </button>

          <div className="grid gap-6 lg:grid-cols-[1fr_1fr]">
            {/* Left Column */}
            <div className="space-y-4">
              {/* Business Context */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
                <div className="mb-3 flex flex-wrap items-center gap-2">
                  <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${difficultyColor[selected.difficulty]}`}>
                    {selected.difficulty}
                  </span>
                  <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${issueTypeColor[selected.issueType] || "bg-gray-500/20 text-gray-400"}`}>
                    {selected.issueType}
                  </span>
                  <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-muted)]">
                    {datasetLabel[selected.dataset]}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-[var(--color-text-primary)]">
                  {selected.title}
                </h2>
                <p className="mt-3 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                  {selected.context}
                </p>
                <div className="mt-4 rounded-md bg-[var(--color-background)] p-3">
                  <p className="text-xs font-medium text-[var(--color-accent)]">Your Task</p>
                  <p className="mt-1 text-sm text-[var(--color-text-primary)]">{selected.task}</p>
                </div>
                <div className="mt-3 text-xs text-[var(--color-text-muted)]">
                  <span className="font-medium">Available tables:</span>{" "}
                  {selected.tables.map((t, i) => (
                    <span key={t}>
                      <code className="rounded bg-[var(--color-background)] px-1 py-0.5 text-[var(--color-accent)]">{t}</code>
                      {i < selected.tables.length - 1 && ", "}
                    </span>
                  ))}
                </div>
              </div>

              {/* Investigation Steps */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Investigation Steps
                </h3>
                <div className="mt-3 space-y-3">
                  {selected.steps.map((step, i) => (
                    <div
                      key={i}
                      className={`flex gap-3 rounded-md p-2 transition-colors ${
                        i === currentStep ? "bg-[var(--color-accent)]/10" : i < currentStep ? "opacity-60" : "opacity-40"
                      }`}
                    >
                      <div className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${
                        i < currentStep ? "bg-green-500/20 text-green-400" : i === currentStep ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]" : "bg-[var(--color-border)] text-[var(--color-text-muted)]"
                      }`}>
                        {i < currentStep ? "✓" : i + 1}
                      </div>
                      <div>
                        <p className="text-xs font-medium text-[var(--color-text-primary)]">{step.title}</p>
                        <p className="mt-0.5 text-[11px] leading-relaxed text-[var(--color-text-muted)]">{step.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
                {currentStep < selected.steps.length && (
                  <button onClick={() => setCurrentStep((s) => Math.min(s + 1, selected.steps.length))} className="mt-3 text-xs font-medium text-[var(--color-accent)] hover:underline">
                    Mark step as done →
                  </button>
                )}
              </div>

              {/* Hints */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Hints ({revealedHints}/{selected.hints.length})
                </h3>
                <div className="mt-3 space-y-2">
                  {selected.hints.map((hint, i) =>
                    i < revealedHints ? (
                      <div key={i} className="rounded-md bg-[var(--color-background)] p-3 text-xs text-[var(--color-text-secondary)]">
                        <span className="font-medium text-[var(--color-accent)]">{hint.label}:</span> {hint.text}
                      </div>
                    ) : null
                  )}
                  {revealedHints < selected.hints.length && (
                    <button onClick={() => setRevealedHints((h) => h + 1)} className="text-xs font-medium text-[var(--color-accent)] hover:underline">
                      Reveal {selected.hints[revealedHints].label}
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-4">
              {/* SQL Editor */}
              <div className="overflow-hidden rounded-lg border border-[var(--color-border)]">
                <div className="h-[200px]">
                  <SQLEditor
                    value={query}
                    onChange={(v) => setQuery(v)}
                    onRun={handleRun}
                    dialect="postgresql"
                    tables={selected.tables.map((t) => ({ name: t, columns: [] }))}
                  />
                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4">
                  <h3 className="text-xs font-medium text-red-400">Error</h3>
                  <p className="mt-1 font-mono text-xs text-red-300">{error}</p>
                </div>
              )}

              {/* Results */}
              {result && (
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
                  <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
                    <span className="text-xs font-medium text-[var(--color-text-primary)]">Results</span>
                    <span className="text-[10px] text-[var(--color-text-muted)]">
                      {result.rowCount} row{result.rowCount !== 1 ? "s" : ""} • {result.executionTimeMs}ms
                    </span>
                  </div>
                  {result.rowCount === 0 ? (
                    <div className="p-6 text-center">
                      <p className="text-sm text-[var(--color-text-muted)]">Query returned 0 rows. Try a different approach.</p>
                    </div>
                  ) : (
                    <div className="max-h-72 overflow-auto">
                      <table className="w-full text-xs">
                        <thead className="sticky top-0 bg-[var(--color-surface)]">
                          <tr className="border-b border-[var(--color-border)]">
                            {result.columns.map((col) => (
                              <th key={col} className="px-3 py-2 text-left font-medium text-[var(--color-text-muted)]">{col}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {result.rows.map((row, i) => (
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
                  )}
                </div>
              )}

              {/* Idle state */}
              {!result && !error && (
                <div className="flex h-48 items-center justify-center rounded-lg border border-dashed border-[var(--color-border)] bg-[var(--color-surface)]">
                  <div className="text-center">
                    <p className="text-sm text-[var(--color-text-muted)]">Run queries to investigate the issue</p>
                    <p className="mt-1 text-[10px] text-[var(--color-text-muted)]">Ctrl+Enter to execute</p>
                  </div>
                </div>
              )}

              {/* Investigation Panel */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">Investigation Progress</h3>
                <div className="mt-3 grid grid-cols-3 gap-3">
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">{queryHistory.length}</p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">Queries Run</p>
                  </div>
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">{elapsed}m</p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">Time Spent</p>
                  </div>
                  <div className="rounded-md bg-[var(--color-background)] p-3 text-center">
                    <p className="text-lg font-bold text-[var(--color-accent)]">{tablesExplored.size}/{selected.tables.length}</p>
                    <p className="text-[10px] text-[var(--color-text-muted)]">Tables Explored</p>
                  </div>
                </div>
              </div>

              {/* Query History */}
              {queryHistory.length > 0 && (
                <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                  <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">Query History</h3>
                  <div className="mt-3 max-h-48 space-y-2 overflow-auto">
                    {queryHistory.map((log, i) => (
                      <button
                        key={i}
                        onClick={() => setQuery(log.query)}
                        className="w-full rounded-md bg-[var(--color-background)] p-2 text-left transition-colors hover:bg-[var(--color-border)]/50"
                      >
                        <code className="line-clamp-1 text-[11px] text-[var(--color-text-secondary)]">{log.query}</code>
                        <div className="mt-1 flex items-center gap-2 text-[10px] text-[var(--color-text-muted)]">
                          {log.error ? (
                            <span className="text-red-400">Error</span>
                          ) : (
                            <span>{log.result?.rowCount} row{log.result?.rowCount !== 1 ? "s" : ""} • {log.result?.executionTimeMs}ms</span>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Root Cause Reveal */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                {showRootCause ? (
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-red-400">Root Cause</h3>
                      <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">{selected.rootCause}</p>
                    </div>
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-green-400">The Fix</h3>
                      <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">{selected.fix}</p>
                    </div>
                    <div>
                      <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-accent)]">What You Learned</h3>
                      <ul className="mt-2 space-y-1">
                        {selected.learnings.map((l, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]">
                            <span className="mt-0.5 text-[var(--color-accent)]">•</span> {l}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <button onClick={() => setShowRootCause(true)} className="w-full text-center text-xs font-medium text-[var(--color-accent)] hover:underline">
                    Reveal Root Cause & Solution
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
