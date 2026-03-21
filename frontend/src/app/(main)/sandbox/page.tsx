"use client";

import { useState, useCallback, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { getSchemaForDataset } from "@/lib/schemas";

interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface QueryHistoryItem {
  id: string;
  query: string;
  dataset: string;
  result: QueryResult | null;
  error: string | null;
  timestamp: number;
  bookmarked: boolean;
}

const datasetLabels: Record<string, string> = {
  ecommerce: "E-Commerce",
  finance: "Finance",
  healthcare: "Healthcare",
};

const STORAGE_KEY = "sqlit-sandbox-history";
const MAX_HISTORY = 50;

function loadHistory(): QueryHistoryItem[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(items: QueryHistoryItem[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, MAX_HISTORY)));
  } catch {
    // storage full, ignore
  }
}

export default function SandboxPage() {
  const [query, setQuery] = useState("SELECT * FROM ");
  const [dataset, setDataset] = useState("ecommerce");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [history, setHistory] = useState<QueryHistoryItem[]>([]);
  const [showSchema, setShowSchema] = useState(true);
  const [showHistory, setShowHistory] = useState(false);
  const [historyFilter, setHistoryFilter] = useState<"all" | "bookmarked">("all");

  const schema = getSchemaForDataset(dataset);

  // Load persisted history on mount
  useEffect(() => {
    setHistory(loadHistory());
  }, []);

  const addToHistory = useCallback((item: Omit<QueryHistoryItem, "id" | "bookmarked">) => {
    setHistory((prev) => {
      const updated = [
        { ...item, id: `q-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`, bookmarked: false },
        ...prev,
      ].slice(0, MAX_HISTORY);
      saveHistory(updated);
      return updated;
    });
  }, []);

  const toggleBookmark = useCallback((id: string) => {
    setHistory((prev) => {
      const updated = prev.map((item) =>
        item.id === id ? { ...item, bookmarked: !item.bookmarked } : item
      );
      saveHistory(updated);
      return updated;
    });
  }, []);

  const deleteHistoryItem = useCallback((id: string) => {
    setHistory((prev) => {
      const updated = prev.filter((item) => item.id !== id);
      saveHistory(updated);
      return updated;
    });
  }, []);

  const clearHistory = useCallback(() => {
    setHistory((prev) => {
      // Keep bookmarked items
      const bookmarked = prev.filter((item) => item.bookmarked);
      saveHistory(bookmarked);
      return bookmarked;
    });
  }, []);

  const handleRun = useCallback(async () => {
    if (!query.trim()) return;
    setRunning(true);
    setError(null);
    setResult(null);

    try {
      const data = await apiClient<{
        user_result: QueryResult & { row_count?: number; execution_time_ms?: number };
        status: string;
        error?: string;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({
          query: query.trim(),
          dataset,
        }),
      });

      if (data.error) {
        setError(data.error);
        addToHistory({ query: query.trim(), dataset, result: null, error: data.error!, timestamp: Date.now() });
      } else if (data.user_result) {
        const normalized: QueryResult = {
          columns: data.user_result.columns,
          rows: data.user_result.rows,
          rowCount: data.user_result.row_count ?? data.user_result.rowCount ?? 0,
          executionTimeMs: data.user_result.execution_time_ms ?? data.user_result.executionTimeMs ?? 0,
        };
        setResult(normalized);
        addToHistory({ query: query.trim(), dataset, result: normalized, error: null, timestamp: Date.now() });
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Query execution failed";
      setError(msg);
      addToHistory({ query: query.trim(), dataset, result: null, error: msg, timestamp: Date.now() });
    } finally {
      setRunning(false);
    }
  }, [query, dataset, addToHistory]);

  const filteredHistory = historyFilter === "bookmarked"
    ? history.filter((item) => item.bookmarked)
    : history;

  const bookmarkedCount = history.filter((h) => h.bookmarked).length;

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col">
      {/* Toolbar */}
      <div className="flex items-center gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2">
        <h1 className="text-sm font-semibold text-[var(--color-text-primary)]">
          SQL Sandbox
        </h1>
        <div className="h-4 w-px bg-[var(--color-border)]" />
        <select
          value={dataset}
          onChange={(e) => {
            setDataset(e.target.value);
            setResult(null);
            setError(null);
          }}
          aria-label="Select dataset"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-background)] px-2 py-1 text-xs text-[var(--color-text-primary)]"
        >
          {Object.entries(datasetLabels).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
        <div className="flex-1" />
        <button
          onClick={() => setShowSchema((s) => !s)}
          aria-label="Toggle schema panel"
          className={`rounded-md px-2 py-1 text-[10px] font-medium transition-colors ${
            showSchema
              ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]"
              : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
          }`}
        >
          Schema
        </button>
        <button
          onClick={() => setShowHistory((h) => !h)}
          aria-label="Toggle query history"
          className={`flex items-center gap-1 rounded-md px-2 py-1 text-[10px] font-medium transition-colors ${
            showHistory
              ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]"
              : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
          }`}
        >
          History
          {history.length > 0 && (
            <span className="rounded-full bg-[var(--color-accent)]/10 px-1.5 text-[9px] text-[var(--color-accent)]">
              {history.length}
            </span>
          )}
          {bookmarkedCount > 0 && (
            <span className="text-amber-500">★</span>
          )}
        </button>
        <button
          onClick={handleRun}
          disabled={running || !query.trim()}
          className="rounded-md bg-[var(--color-accent)] px-4 py-1.5 text-xs font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {running ? "Running..." : "Run ▶"}
        </button>
      </div>

      <div className="flex flex-1 flex-col md:flex-row overflow-hidden">
        {/* Schema sidebar */}
        {showSchema && (
          <div className="w-full md:w-56 md:shrink-0 max-h-48 md:max-h-none overflow-y-auto border-b md:border-b-0 md:border-r border-[var(--color-border)] bg-[var(--color-surface)] p-3">
            <h3 className="mb-2 text-[10px] font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
              {datasetLabels[dataset]} Tables
            </h3>
            <div className="space-y-3">
              {schema.map((table) => (
                <div key={table.name}>
                  <button
                    onClick={() =>
                      setQuery((q) =>
                        q.endsWith("FROM ") || q.endsWith("JOIN ")
                          ? q + table.name
                          : q
                      )
                    }
                    className="mb-1 text-xs font-semibold text-[var(--color-accent)] hover:underline"
                  >
                    {table.name}
                  </button>
                  <div className="space-y-0.5 pl-2">
                    {table.columns.map((col) => (
                      <button
                        key={col.name}
                        onClick={() => setQuery((q) => q + col.name)}
                        className="flex w-full items-center gap-1.5 text-left text-[10px] hover:text-[var(--color-accent)]"
                      >
                        {col.isPrimaryKey && (
                          <span className="text-[8px] font-bold text-yellow-500">PK</span>
                        )}
                        {col.isForeignKey && (
                          <span className="text-[8px] font-bold text-blue-400">FK</span>
                        )}
                        <span className="text-[var(--color-text-secondary)]">{col.name}</span>
                        <span className="text-[var(--color-text-muted)]">{col.type}</span>
                        {col.nullable && (
                          <span className="text-[8px] text-[var(--color-text-muted)]">NULL</span>
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Main area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Editor */}
          <div className="shrink-0 border-b border-[var(--color-border)]">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter") handleRun();
              }}
              placeholder="Write your SQL query here..."
              className="h-40 w-full resize-none bg-[var(--color-background)] p-4 font-mono text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none"
              spellCheck={false}
            />
          </div>

          {/* Results */}
          <div className="flex-1 overflow-auto">
            {error && (
              <div className="border-b border-red-500/30 bg-red-500/10 p-4">
                <span className="text-xs font-medium text-red-400">Error: </span>
                <span className="font-mono text-xs text-red-300">{error}</span>
              </div>
            )}

            {result && (
              <div>
                <div className="flex items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2">
                  <span className="text-xs text-[var(--color-text-primary)]">
                    {result.rowCount} row{result.rowCount !== 1 ? "s" : ""} returned
                  </span>
                  <span className="text-[10px] text-[var(--color-text-muted)]">
                    {result.executionTimeMs}ms
                  </span>
                </div>
                {result.rowCount > 0 ? (
                  <table className="w-full text-xs">
                    <thead className="sticky top-0 bg-[var(--color-surface)]">
                      <tr className="border-b border-[var(--color-border)]">
                        {result.columns.map((col) => (
                          <th key={col} className="px-3 py-2 text-left font-medium text-[var(--color-text-muted)]">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {result.rows.map((row, i) => (
                        <tr key={i} className="border-b border-[var(--color-border)]/30 hover:bg-[var(--color-surface)]">
                          {row.map((cell, j) => (
                            <td
                              key={j}
                              className={`px-3 py-1.5 font-mono ${
                                cell === null
                                  ? "italic text-[var(--color-text-muted)]"
                                  : "text-[var(--color-text-secondary)]"
                              }`}
                            >
                              {cell === null ? "NULL" : String(cell)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <div className="p-8 text-center text-sm text-[var(--color-text-muted)]">
                    Query returned 0 rows
                  </div>
                )}
              </div>
            )}

            {!result && !error && (
              <div className="flex h-full items-center justify-center">
                <div className="text-center">
                  <p className="text-sm text-[var(--color-text-muted)]">Run a query to see results</p>
                  <p className="mt-1 text-[10px] text-[var(--color-text-muted)]">
                    <kbd className="rounded bg-[var(--color-surface)] px-1.5 py-0.5 font-mono">Ctrl</kbd> + <kbd className="rounded bg-[var(--color-surface)] px-1.5 py-0.5 font-mono">Enter</kbd> to execute
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* History sidebar with bookmarks */}
        {showHistory && (
          <div className="w-full md:w-80 md:shrink-0 flex flex-col max-h-48 md:max-h-none overflow-hidden border-t md:border-t-0 md:border-l border-[var(--color-border)] bg-[var(--color-surface)]">
            {/* History header */}
            <div className="flex items-center justify-between border-b border-[var(--color-border)] px-3 py-2">
              <div className="flex items-center gap-2">
                <h3 className="text-[10px] font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Query History
                </h3>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setHistoryFilter("all")}
                  aria-label="Show all history"
                  className={`rounded px-1.5 py-0.5 text-[10px] font-medium transition-colors ${
                    historyFilter === "all"
                      ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]"
                      : "text-[var(--color-text-muted)]"
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setHistoryFilter("bookmarked")}
                  aria-label="Show bookmarked history"
                  className={`flex items-center gap-0.5 rounded px-1.5 py-0.5 text-[10px] font-medium transition-colors ${
                    historyFilter === "bookmarked"
                      ? "bg-amber-500/20 text-amber-500"
                      : "text-[var(--color-text-muted)]"
                  }`}
                >
                  ★ {bookmarkedCount}
                </button>
                {history.length > 0 && (
                  <button
                    onClick={clearHistory}
                    aria-label="Clear history"
                    className="ml-1 text-[10px] text-[var(--color-text-muted)] hover:text-red-400"
                    title="Clear non-bookmarked history"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>

            {/* History list */}
            <div className="flex-1 overflow-y-auto p-2">
              {filteredHistory.length === 0 ? (
                <p className="py-4 text-center text-xs text-[var(--color-text-muted)]">
                  {historyFilter === "bookmarked" ? "No bookmarked queries" : "No queries yet"}
                </p>
              ) : (
                <div className="space-y-1.5">
                  {filteredHistory.map((item) => (
                    <div
                      key={item.id}
                      className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-2 transition-colors hover:border-[var(--color-accent)]/40"
                    >
                      {/* Header */}
                      <div className="mb-1 flex items-center gap-1.5">
                        <span
                          className={`h-1.5 w-1.5 rounded-full ${
                            item.error ? "bg-red-400" : "bg-emerald-400"
                          }`}
                        />
                        <span className="text-[10px] text-[var(--color-text-muted)]">
                          {datasetLabels[item.dataset]}
                        </span>
                        {item.result && (
                          <span className="text-[10px] text-[var(--color-text-muted)]">
                            · {item.result.rowCount} rows · {item.result.executionTimeMs}ms
                          </span>
                        )}
                        <div className="flex-1" />
                        {/* Bookmark button */}
                        <button
                          onClick={() => toggleBookmark(item.id)}
                          aria-label={item.bookmarked ? "Remove bookmark" : "Bookmark this query"}
                          className={`text-xs transition-colors ${
                            item.bookmarked
                              ? "text-amber-500"
                              : "text-transparent group-hover:text-[var(--color-text-muted)]"
                          }`}
                          title={item.bookmarked ? "Remove bookmark" : "Bookmark this query"}
                        >
                          ★
                        </button>
                        {/* Delete button */}
                        <button
                          onClick={() => deleteHistoryItem(item.id)}
                          aria-label="Delete history item"
                          className="text-xs text-transparent transition-colors group-hover:text-[var(--color-text-muted)] hover:!text-red-400"
                          title="Delete"
                        >
                          ✕
                        </button>
                      </div>
                      {/* Query text — click to load */}
                      <button
                        onClick={() => {
                          setQuery(item.query);
                          setDataset(item.dataset);
                        }}
                        className="w-full text-left"
                      >
                        <p className="line-clamp-3 font-mono text-[10px] leading-relaxed text-[var(--color-text-secondary)]">
                          {item.query}
                        </p>
                      </button>
                      {/* Timestamp */}
                      <p className="mt-1 text-[9px] text-[var(--color-text-muted)]">
                        {new Date(item.timestamp).toLocaleTimeString()} · {new Date(item.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
