"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ResizablePanel } from "@/components/ui/ResizablePanel";
import { ProblemPanel } from "@/components/practice/ProblemPanel";
import { SQLEditor } from "@/components/editor/SQLEditor";
import { OutputPanel } from "@/components/practice/OutputPanel";
import { NextProblemRecommender } from "@/components/practice/NextProblemRecommender";
import { usePracticeStore } from "@/stores/usePracticeStore";
import { useUserStore } from "@/stores/useUserStore";
import { apiClient } from "@/lib/api";
import { getSchemaForDataset } from "@/lib/schemas";
import type { Difficulty } from "@/types";

interface ProblemData {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  dataset: string;
  description: string;
  schema_hint: string[];
  concept_tags: string[];
  hints: string[];
  explanation: string;
  approach: string | string[];
  common_mistakes: string[];
}

interface ProblemListItem {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  dataset: string;
  concept_tags: string[];
}

export default function ProblemPage() {
  const params = useParams();
  const slug = params.slug as string;
  const store = usePracticeStore();
  const userStore = useUserStore();
  const isAuthenticated = userStore.isAuthenticated;
  const [problem, setProblem] = useState<ProblemData | null>(null);
  const [allProblems, setAllProblems] = useState<ProblemListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProblem = () => {
    if (!slug) return;
    setLoading(true);
    setError(null);
    apiClient<ProblemData>(`/api/problems/${slug}`)
      .then((data) => {
        setProblem(data);
        if (data.dataset) {
          store.setDataset(data.dataset);
        }
      })
      .catch(() => setError("Failed to load problem. Please try again."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    store.reset();
    fetchProblem();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  // Fetch all problems for recommendations (once)
  useEffect(() => {
    apiClient<{ problems: ProblemListItem[] }>("/api/problems")
      .then((data) => setAllProblems(data.problems))
      .catch(() => {});
  }, []);

  const handleRun = useCallback(async () => {
    if (!problem) return;
    store.setRunning();
    try {
      const response = await apiClient<{
        status: "accepted" | "wrong_answer" | "error";
        user_result: { columns: string[]; rows: unknown[][]; row_count: number; execution_time_ms: number } | null;
        expected_result: { columns: string[]; rows: unknown[][]; row_count: number; execution_time_ms: number } | null;
        diff: { matching_rows: number; total_expected_rows: number; mismatched_rows: number[]; mismatched_columns: string[] } | null;
        error: string | null;
        xp_earned: number;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({
          query: store.query,
          problem_id: problem.id,
          dialect: store.dialect,
          dataset: store.dataset,
        }),
      });

      store.setResult({
        status: response.status,
        userResult: response.user_result
          ? {
              columns: response.user_result.columns,
              rows: response.user_result.rows,
              rowCount: response.user_result.row_count,
              executionTimeMs: response.user_result.execution_time_ms,
            }
          : null,
        expectedResult: response.expected_result
          ? {
              columns: response.expected_result.columns,
              rows: response.expected_result.rows,
              rowCount: response.expected_result.row_count,
              executionTimeMs: response.expected_result.execution_time_ms,
            }
          : null,
        diff: response.diff
          ? {
              matchingRows: response.diff.matching_rows,
              totalExpectedRows: response.diff.total_expected_rows,
              mismatchedRows: response.diff.mismatched_rows,
              mismatchedColumns: response.diff.mismatched_columns,
            }
          : null,
        error: response.error,
        xpEarned: response.xp_earned,
      });

      // Track acceptance rate
      userStore.recordAttempt(response.status === "accepted");

      // Update XP on success
      if (response.status === "accepted" && response.xp_earned > 0) {
        userStore.addXP(response.xp_earned);
        userStore.markSolved(problem.id);
        // Persist to backend (fire-and-forget)
        userStore.saveSolveToBackend(problem.id, response.xp_earned);
      }
    } catch (err) {
      store.setResult({
        status: "error",
        userResult: null,
        expectedResult: null,
        diff: null,
        error: err instanceof Error ? err.message : "An error occurred",
        xpEarned: 0,
      });
    }
  }, [store, problem, userStore]);

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] items-center justify-center">
        <div className="flex flex-col items-center justify-center gap-4 py-20">
          <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-6 py-4 text-center">
            <p className="text-sm text-red-400">{error}</p>
          </div>
          <button
            onClick={() => { setError(null); fetchProblem(); }}
            className="rounded-lg bg-[var(--color-surface)] border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] items-center justify-center">
        <p className="text-[var(--color-text-muted)]">Problem not found.</p>
      </div>
    );
  }

  // Get schema for the problem's dataset
  const datasetSchema = getSchemaForDataset(problem.dataset || store.dataset);

  // Filter schema to only show relevant tables
  const relevantSchema = problem.schema_hint.length > 0
    ? datasetSchema.filter((t) => problem.schema_hint.includes(t.name))
    : datasetSchema;

  const tables = relevantSchema.map((t) => ({
    name: t.name,
    columns: t.columns.map((c) => c.name),
  }));

  const explanationStr = typeof problem.explanation === "string" ? problem.explanation : "";
  const approachStr = Array.isArray(problem.approach) ? problem.approach.join("\n") : (problem.approach ?? "");

  // Compute next unsolved problem
  const currentIndex = allProblems.findIndex((p) => p.id === problem.id);
  const nextProblem = allProblems.find(
    (p, i) => i > currentIndex && !userStore.solvedProblems.includes(p.id)
  ) || allProblems.find(
    (p) => !userStore.solvedProblems.includes(p.id) && p.id !== problem.id
  );

  return (
    <div className="h-[calc(100vh-3.5rem)]">
      <ResizablePanel
        left={
          <ProblemPanel
            title={problem.title}
            difficulty={problem.difficulty}
            acceptanceRate={userStore.acceptanceRate}
            description={problem.description}
            conceptTags={problem.concept_tags}
            schema={relevantSchema}
            dataset={store.dataset}
            dialect={store.dialect}
            onDatasetChange={store.setDataset}
            onDialectChange={(d) => store.setDialect(d as "postgresql" | "mysql")}
          />
        }
        center={
          <SQLEditor
            value={store.query}
            onChange={store.setQuery}
            onRun={handleRun}
            dialect={store.dialect}
            tables={tables}
          />
        }
        right={
          <OutputPanel
            status={store.status}
            userResult={store.userResult}
            expectedResult={store.expectedResult}
            diff={store.diff}
            error={store.error}
            xpEarned={store.xpEarned}
            hints={problem.hints}
            difficulty={problem.difficulty}
            explanation={explanationStr}
            approach={approachStr}
            commonMistakes={problem.common_mistakes}
            isSolved={store.status === "accepted"}
            streak={userStore.streak}
            problemTitle={problem.title}
            problemId={problem.id}
            nextProblemSlug={nextProblem?.slug}
            note={userStore.notes[problem.id] || ""}
            isFlagged={userStore.flaggedProblems.includes(problem.id)}
            onNoteChange={(note) => userStore.setNote(problem.id, note)}
            onToggleFlag={() => userStore.toggleFlag(problem.id)}
            recommendations={
              allProblems.length > 0 && (
                <NextProblemRecommender
                  problems={allProblems}
                  currentProblemId={problem.id}
                  currentDifficulty={problem.difficulty}
                  currentConceptTags={problem.concept_tags}
                />
              )
            }
          />
        }
      />
    </div>
  );
}
