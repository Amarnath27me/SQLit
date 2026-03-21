"use client";

import { useState, useEffect } from "react";
import { ResultTable } from "./ResultTable";
import { ShareCard } from "./ShareCard";
import { Mascot } from "@/components/ui/Mascot";

interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface ResultDiff {
  matchingRows: number;
  totalExpectedRows: number;
  mismatchedRows: number[];
  mismatchedColumns: string[];
}

interface OutputPanelProps {
  status: "idle" | "running" | "accepted" | "wrong_answer" | "error";
  userResult: QueryResult | null;
  expectedResult: QueryResult | null;
  diff: ResultDiff | null;
  error: string | null;
  xpEarned: number;
  hints: string[];
  difficulty: "easy" | "medium" | "hard";
  explanation: string | null;
  approach: string | null;
  commonMistakes: string[] | null;
  isSolved: boolean;
  streak?: number;
  recommendations?: React.ReactNode;
  problemTitle?: string;
}

/* ── Query comparison helper ───────────────────────────────── */
function getQueryComparison(problemTitle: string): { approaches: Array<{ name: string; description: string; pros: string[]; cons: string[]; bestFor: string }> } | null {
  const comparisons = [
    {
      name: "Subquery Approach",
      description: "Use a correlated or uncorrelated subquery in WHERE or SELECT",
      pros: ["Easy to understand", "Works in all SQL dialects", "Good for simple filtering"],
      cons: ["Can be slower on large datasets", "May execute once per row (correlated)"],
      bestFor: "Simple existence checks or single-value comparisons",
    },
    {
      name: "JOIN Approach",
      description: "Use JOIN to combine tables and filter in WHERE clause",
      pros: ["Generally faster", "Optimizer handles well", "Natural for multi-table queries"],
      cons: ["Can produce duplicates if not careful", "More complex with many tables"],
      bestFor: "When you need columns from multiple tables",
    },
    {
      name: "CTE Approach",
      description: "Use WITH clause to break query into named steps",
      pros: ["Most readable", "Easy to debug step by step", "Reusable within query"],
      cons: ["Not all older databases support CTEs", "May not always optimize better"],
      bestFor: "Complex multi-step logic or self-referencing queries",
    },
    {
      name: "Window Function Approach",
      description: "Use OVER() clause with aggregation or ranking functions",
      pros: ["Access row-level and aggregate data simultaneously", "No GROUP BY needed"],
      cons: ["More complex syntax", "Can be slower without proper indexes"],
      bestFor: "Rankings, running totals, and comparing rows to aggregates",
    },
  ];

  let hash = 0;
  for (let i = 0; i < problemTitle.length; i++) hash = ((hash << 5) - hash + problemTitle.charCodeAt(i)) | 0;
  const start = Math.abs(hash) % comparisons.length;
  const count = 2 + (Math.abs(hash >> 8) % 2);
  const selected = [];
  for (let i = 0; i < count; i++) {
    selected.push(comparisons[(start + i) % comparisons.length]);
  }
  return { approaches: selected };
}

/* ── Streak multiplier logic ────────────────────────────────── */
function getStreakMultiplier(streak: number): { mult: number; label: string } {
  if (streak >= 30) return { mult: 2.0, label: "30-day streak 2x" };
  if (streak >= 7) return { mult: 1.5, label: "7-day streak 1.5x" };
  if (streak >= 3) return { mult: 1.2, label: "3-day streak 1.2x" };
  return { mult: 1.0, label: "" };
}

/* ── Hint level labels ──────────────────────────────────────── */
const HINT_LABELS = [
  "Nudge",       // Level 1: very gentle direction
  "Direction",   // Level 2: which clause / concept to focus on
  "Approach",    // Level 3: specific technique to use
  "Walkthrough", // Level 4: step-by-step (only for easy)
];

export function OutputPanel({
  status,
  userResult,
  expectedResult,
  diff,
  error,
  xpEarned,
  hints,
  difficulty,
  explanation,
  approach,
  commonMistakes,
  isSolved,
  streak = 0,
  recommendations,
  problemTitle = "",
}: OutputPanelProps) {
  const [hintLevel, setHintLevel] = useState(0);
  const [activeTab, setActiveTab] = useState<"output" | "explanation" | "approach" | "mistakes" | "approaches">("output");
  const [hasViewedExplanation, setHasViewedExplanation] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  // Progressive hints: easy shows 4, medium shows 3, hard shows 2
  const maxHints = difficulty === "easy" ? Math.min(hints.length, 4) : difficulty === "medium" ? Math.min(hints.length, 3) : Math.min(hints.length, 2);
  const availableHints = hints.slice(0, maxHints);

  // Reset hint level and explanation viewed state when status changes back to idle
  useEffect(() => {
    if (status === "idle") {
      setHintLevel(0);
      setHasViewedExplanation(false);
      setShowCelebration(false);
    }
  }, [status]);

  // Show celebration animation on accepted
  useEffect(() => {
    if (status === "accepted") {
      setShowCelebration(true);
      const timer = setTimeout(() => setShowCelebration(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [status]);

  // Mark explanation as viewed when user clicks the tab
  useEffect(() => {
    if (activeTab === "explanation" && isSolved) {
      setHasViewedExplanation(true);
    }
  }, [activeTab, isSolved]);

  // Auto-switch to output tab when new result comes in
  useEffect(() => {
    if (status === "accepted" || status === "wrong_answer" || status === "error") {
      setActiveTab("output");
    }
  }, [status]);

  const streakInfo = getStreakMultiplier(streak);
  const totalXP = Math.floor(xpEarned * streakInfo.mult);

  // Determine which post-solve tabs to show
  const postSolveTabs: ("output" | "explanation" | "approach" | "mistakes" | "approaches")[] = ["output"];
  if (isSolved) {
    postSolveTabs.push("explanation", "approach", "mistakes", "approaches");
  }

  const queryComparison = isSolved ? getQueryComparison(problemTitle) : null;

  return (
    <div className="flex h-full flex-col">
      {/* Tabs */}
      <div role="tablist" aria-label="Output panel tabs" className="flex border-b border-[var(--color-border)] bg-[var(--color-surface)]">
        {postSolveTabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            aria-label={`${tab === "explanation" ? "Explanation" : tab === "approaches" ? "Query Comparison" : tab} tab`}
            aria-selected={activeTab === tab}
            role="tab"
            className={`relative px-4 py-2 text-xs font-medium capitalize transition-colors ${
              activeTab === tab
                ? "border-b-2 border-[var(--color-accent)] text-[var(--color-accent)]"
                : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
            }`}
          >
            {tab === "explanation" ? "Explanation" : tab === "approaches" ? "Query Comparison" : tab}
            {/* Indicator dot for unviewed explanation */}
            {tab === "explanation" && isSolved && !hasViewedExplanation && (
              <span className="absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-[var(--color-accent)] animate-pulse" />
            )}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {/* Output tab */}
        {activeTab === "output" && (
          <>
            {/* Idle */}
            {status === "idle" && (
              <div className="flex flex-col items-center justify-center gap-3 py-12 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[var(--color-background)]">
                  <svg className="h-6 w-6 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
                  </svg>
                </div>
                <p className="text-sm text-[var(--color-text-muted)]">
                  Run your query to see results
                </p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  Press <kbd className="rounded bg-[var(--color-background)] px-1.5 py-0.5 font-mono text-[10px]">Ctrl</kbd> + <kbd className="rounded bg-[var(--color-background)] px-1.5 py-0.5 font-mono text-[10px]">Enter</kbd> to execute
                </p>
              </div>
            )}

            {/* Running */}
            {status === "running" && (
              <div role="status" aria-live="polite" className="flex flex-col items-center justify-center gap-3 py-12">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" aria-hidden="true" />
                <span className="text-sm text-[var(--color-text-secondary)]">
                  Executing query...
                </span>
              </div>
            )}

            {/* Accepted */}
            {status === "accepted" && userResult && (
              <div className="space-y-4">
                {/* Celebration banner */}
                <div role="status" aria-live="polite" className={`rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-4 transition-all duration-500 ${showCelebration ? "scale-100 opacity-100" : "scale-95 opacity-90"}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {showCelebration ? (
                        <Mascot mood="celebrate" size={40} />
                      ) : (
                        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500 text-white text-sm font-bold">
                          ✓
                        </span>
                      )}
                      <div>
                        <span className="text-sm font-semibold text-emerald-500">
                          Accepted
                        </span>
                        <p className="text-xs text-emerald-500/70">
                          {userResult.rowCount} rows · {userResult.executionTimeMs}ms
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {totalXP > 0 && (
                        <div className="text-right">
                          <span className={`inline-block rounded-full bg-amber-500/10 px-3 py-1 text-sm font-bold text-amber-500 ${showCelebration ? "animate-bounce" : ""}`}>
                            +{totalXP} XP
                          </span>
                          {streakInfo.label && (
                            <p className="mt-0.5 text-[10px] text-amber-500/70">{streakInfo.label}</p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Share card */}
                <ShareCard
                  problemTitle={problemTitle}
                  difficulty={difficulty}
                  xpEarned={totalXP}
                  executionTimeMs={userResult.executionTimeMs}
                  streak={streak}
                />

                {/* Prompt to view explanation */}
                {!hasViewedExplanation && (
                  <button
                    onClick={() => setActiveTab("explanation")}
                    aria-label="View the step-by-step solution explanation"
                    className="flex w-full items-center gap-2 rounded-lg border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/5 px-4 py-3 text-left transition-colors hover:bg-[var(--color-accent)]/10"
                  >
                    <svg className="h-4 w-4 shrink-0 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                    </svg>
                    <div>
                      <p className="text-xs font-semibold text-[var(--color-accent)]">
                        View the Explanation
                      </p>
                      <p className="text-[10px] text-[var(--color-text-muted)]">
                        Review the step-by-step solution breakdown before moving on
                      </p>
                    </div>
                    <svg className="ml-auto h-4 w-4 shrink-0 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                )}

                {/* Result table */}
                <ResultTable
                  columns={userResult.columns}
                  rows={userResult.rows}
                />

                {/* Adaptive recommendations */}
                {recommendations && hasViewedExplanation && (
                  <div className="mt-2">{recommendations}</div>
                )}
              </div>
            )}

            {/* Wrong Answer */}
            {status === "wrong_answer" && (
              <div className="space-y-4">
                <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-full bg-red-500 text-white text-sm font-bold">
                      ✗
                    </span>
                    <div>
                      <span className="text-sm font-semibold text-red-500">
                        Wrong Answer
                      </span>
                      {diff && (
                        <p className="text-xs text-red-500/70">
                          {diff.matchingRows} of {diff.totalExpectedRows} rows match
                          {diff.mismatchedColumns.length > 0 && (
                            <> · Columns differ: <span className="font-mono">{diff.mismatchedColumns.join(", ")}</span></>
                          )}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Side-by-side diff */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <h4 className="mb-1 text-xs font-medium text-[var(--color-text-muted)]">
                      Your Output {userResult && <span className="text-[var(--color-text-muted)]">({userResult.rowCount} rows)</span>}
                    </h4>
                    {userResult && (
                      <ResultTable
                        columns={userResult.columns}
                        rows={userResult.rows}
                        highlightRows={diff?.mismatchedRows}
                        highlightColumns={diff?.mismatchedColumns}
                        maxHeight="200px"
                      />
                    )}
                  </div>
                  <div>
                    <h4 className="mb-1 text-xs font-medium text-[var(--color-text-muted)]">
                      Expected Output {expectedResult && <span className="text-[var(--color-text-muted)]">({expectedResult.rowCount} rows)</span>}
                    </h4>
                    {expectedResult && (
                      <ResultTable
                        columns={expectedResult.columns}
                        rows={expectedResult.rows}
                        highlightRows={diff?.mismatchedRows}
                        highlightColumns={diff?.mismatchedColumns}
                        maxHeight="200px"
                      />
                    )}
                  </div>
                </div>

                {/* Progressive hints — 4 levels */}
                {availableHints.length > 0 && (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-medium text-[var(--color-text-muted)]">
                        Progressive Hints
                      </h4>
                      <span className="text-[10px] text-[var(--color-text-muted)]">
                        {hintLevel} / {availableHints.length} revealed
                      </span>
                    </div>

                    {/* Hint progress bar */}
                    <div className="flex gap-1">
                      {availableHints.map((_, i) => (
                        <div
                          key={i}
                          className={`h-1 flex-1 rounded-full transition-colors ${
                            i < hintLevel ? "bg-[var(--color-accent)]" : "bg-[var(--color-border)]"
                          }`}
                        />
                      ))}
                    </div>

                    {/* Revealed hints */}
                    {availableHints.slice(0, hintLevel).map((hint, i) => (
                      <div
                        key={i}
                        className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-3"
                      >
                        <div className="mb-1 flex items-center gap-1.5">
                          <span className="flex h-4 w-4 items-center justify-center rounded-full bg-[var(--color-accent)]/10 text-[9px] font-bold text-[var(--color-accent)]">
                            {i + 1}
                          </span>
                          <span className="text-[10px] font-semibold uppercase tracking-wider text-[var(--color-accent)]">
                            {HINT_LABELS[i] || `Hint ${i + 1}`}
                          </span>
                        </div>
                        <p className="text-xs text-[var(--color-text-secondary)]">{hint}</p>
                      </div>
                    ))}

                    {/* Show next hint button */}
                    {hintLevel < availableHints.length && (
                      <button
                        onClick={() => setHintLevel((h) => h + 1)}
                        aria-label={`Reveal hint ${hintLevel + 1} of ${availableHints.length}: ${HINT_LABELS[hintLevel] || `Hint ${hintLevel + 1}`}`}
                        className="flex w-full items-center justify-center gap-2 rounded-lg border border-dashed border-[var(--color-border)] px-3 py-2.5 text-xs font-medium text-[var(--color-text-muted)] transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
                      >
                        <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                        </svg>
                        Reveal {HINT_LABELS[hintLevel] || `Hint ${hintLevel + 1}`} ({hintLevel + 1}/{availableHints.length})
                      </button>
                    )}

                    {hintLevel >= availableHints.length && (
                      <p className="text-center text-[10px] text-[var(--color-text-muted)]">
                        All hints revealed. Review the hints and try again!
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Error */}
            {status === "error" && error && (
              <div className="space-y-3">
                <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-full bg-red-500 text-white text-sm font-bold">
                      !
                    </span>
                    <span className="text-sm font-semibold text-red-500">
                      Error
                    </span>
                  </div>
                </div>
                <pre className="overflow-x-auto rounded-lg border border-red-500/10 bg-red-500/5 p-3 font-mono text-xs text-red-400">
                  {error}
                </pre>
                {/* Educational tips for common errors */}
                {error.toLowerCase().includes("no such table") && (
                  <div className="rounded-lg bg-amber-500/5 border border-amber-500/20 p-3 text-xs text-amber-500">
                    <strong>Tip:</strong> Check the table name. Look at the Schema tab on the left panel for available tables.
                  </div>
                )}
                {error.toLowerCase().includes("no such column") && (
                  <div className="rounded-lg bg-amber-500/5 border border-amber-500/20 p-3 text-xs text-amber-500">
                    <strong>Tip:</strong> Check column names and aliases. Expand the table in the Schema panel to see available columns.
                  </div>
                )}
                {error.toLowerCase().includes("syntax") && (
                  <div className="rounded-lg bg-amber-500/5 border border-amber-500/20 p-3 text-xs text-amber-500">
                    <strong>Tip:</strong> Check your SQL syntax. Common issues: missing commas, unclosed quotes, or misspelled keywords.
                  </div>
                )}
                {error.toLowerCase().includes("rate limit") && (
                  <div className="rounded-lg bg-amber-500/5 border border-amber-500/20 p-3 text-xs text-amber-500">
                    <strong>Tip:</strong> You&apos;ve exceeded the query limit (20/min). Take a moment to review your approach before trying again.
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {/* Post-solve: Explanation tab */}
        {activeTab === "explanation" && explanation && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <svg className="h-4 w-4 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
              </svg>
              <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
                Step-by-step Explanation
              </h4>
            </div>
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
              <p className="whitespace-pre-wrap text-xs leading-relaxed text-[var(--color-text-secondary)]">{explanation}</p>
            </div>
          </div>
        )}

        {/* Post-solve: Approach tab */}
        {activeTab === "approach" && approach && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <svg className="h-4 w-4 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
              </svg>
              <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
                Thinking Approach
              </h4>
            </div>
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
              <p className="whitespace-pre-wrap text-xs leading-relaxed text-[var(--color-text-secondary)]">{approach}</p>
            </div>
          </div>
        )}

        {/* Post-solve: Common mistakes tab */}
        {activeTab === "mistakes" && commonMistakes && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <svg className="h-4 w-4 text-amber-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
              </svg>
              <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
                Common Mistakes
              </h4>
            </div>
            {commonMistakes.map((m, i) => (
              <div
                key={i}
                className="flex items-start gap-2 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3"
              >
                <span className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-amber-500/10 text-[9px] font-bold text-amber-500">
                  {i + 1}
                </span>
                <p className="text-xs text-amber-600 dark:text-amber-400">{m}</p>
              </div>
            ))}
          </div>
        )}

        {/* Post-solve: Query Comparison tab */}
        {activeTab === "approaches" && queryComparison && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <svg className="h-4 w-4 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
              </svg>
              <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
                Query Comparison
              </h4>
            </div>
            <p className="text-xs text-[var(--color-text-muted)]">
              Multiple approaches can solve this problem. Compare the trade-offs:
            </p>
            {queryComparison.approaches.map((a, i) => (
              <div
                key={i}
                className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4 space-y-2"
              >
                <h5 className="text-xs font-bold text-[var(--color-text-primary)]">{a.name}</h5>
                <p className="text-xs text-[var(--color-text-secondary)]">{a.description}</p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-500">Pros</span>
                    <ul className="space-y-0.5">
                      {a.pros.map((pro, j) => (
                        <li key={j} className="flex items-start gap-1.5 text-xs text-[var(--color-text-secondary)]">
                          <svg className="mt-0.5 h-3 w-3 shrink-0 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                          </svg>
                          {pro}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-red-500">Cons</span>
                    <ul className="space-y-0.5">
                      {a.cons.map((con, j) => (
                        <li key={j} className="flex items-start gap-1.5 text-xs text-[var(--color-text-secondary)]">
                          <svg className="mt-0.5 h-3 w-3 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                          </svg>
                          {con}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div className="rounded bg-[var(--color-surface)] px-2.5 py-1.5">
                  <span className="text-[10px] font-semibold text-[var(--color-text-muted)]">Best for: </span>
                  <span className="text-[10px] text-[var(--color-text-secondary)]">{a.bestFor}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
