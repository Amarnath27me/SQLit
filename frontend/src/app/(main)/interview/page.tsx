"use client";

import { useState, useEffect, useCallback, useRef, useMemo } from "react";
import { Badge } from "@/components/ui/Badge";
import { SQLEditor } from "@/components/editor/SQLEditor";
import { apiClient } from "@/lib/api";
import { getSchemaForDataset } from "@/lib/schemas";
import type { Difficulty, Dataset } from "@/types";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface ProblemFromAPI {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  dataset: Dataset;
  concept_tags: string[];
}

interface ProblemDetail {
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

type Company = "faang" | "big-tech" | "fintech" | "startup" | "consulting";
type Role =
  | "data-analyst"
  | "data-engineer"
  | "backend"
  | "full-stack"
  | "product-analyst";
type Phase = "setup" | "loading" | "interview" | "results";

interface QuestionResult {
  problem: ProblemDetail;
  status: "accepted" | "wrong_answer" | "error" | "skipped" | "timeout";
  query: string;
  timeSpentMs: number;
  userResult: {
    columns: string[];
    rows: unknown[][];
    row_count: number;
  } | null;
}

/* ------------------------------------------------------------------ */
/*  Config                                                             */
/* ------------------------------------------------------------------ */

const COMPANIES: { value: Company; label: string; icon: string }[] = [
  { value: "faang", label: "FAANG", icon: "F" },
  { value: "big-tech", label: "Big Tech", icon: "B" },
  { value: "fintech", label: "FinTech", icon: "$" },
  { value: "startup", label: "Startup", icon: "S" },
  { value: "consulting", label: "Consulting", icon: "C" },
];

const ROLES: { value: Role; label: string }[] = [
  { value: "data-analyst", label: "Data Analyst" },
  { value: "data-engineer", label: "Data Engineer" },
  { value: "backend", label: "Backend Engineer" },
  { value: "full-stack", label: "Full-Stack Engineer" },
  { value: "product-analyst", label: "Product Analyst" },
];

const QUESTION_COUNTS = [3, 5, 7, 10];
const TIME_OPTIONS = [
  { value: 5, label: "5 min" },
  { value: 10, label: "10 min" },
  { value: 15, label: "15 min" },
  { value: 20, label: "20 min" },
  { value: 30, label: "30 min" },
];

const DIFFICULTY_MIXES: {
  value: string;
  label: string;
  mix: Record<Difficulty, number>;
}[] = [
  { value: "easy", label: "Warm Up", mix: { easy: 0.6, medium: 0.3, hard: 0.1 } },
  { value: "balanced", label: "Balanced", mix: { easy: 0.2, medium: 0.5, hard: 0.3 } },
  { value: "hard", label: "Challenge", mix: { easy: 0.1, medium: 0.3, hard: 0.6 } },
  { value: "faang", label: "FAANG Style", mix: { easy: 0.0, medium: 0.4, hard: 0.6 } },
];

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function shuffle<T>(arr: T[], seed: number): T[] {
  const a = [...arr];
  let s = seed;
  for (let i = a.length - 1; i > 0; i--) {
    s = ((s * 9301 + 49297) % 233280) | 0;
    const j = Math.abs(s) % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function formatTime(ms: number): string {
  const totalSec = Math.max(0, Math.floor(ms / 1000));
  const min = Math.floor(totalSec / 60);
  const sec = totalSec % 60;
  return `${min}:${sec.toString().padStart(2, "0")}`;
}

function getPerformanceRating(
  solved: number,
  total: number,
  avgTimeSec: number,
  diffMix: string
): { label: string; color: string; description: string } {
  const ratio = solved / total;
  const fast = avgTimeSec < 300; // under 5 min avg

  if (ratio >= 0.9 && fast)
    return {
      label: "Strong Hire",
      color: "text-emerald-400",
      description: "Outstanding performance. You solved nearly everything quickly and accurately.",
    };
  if (ratio >= 0.7)
    return {
      label: "Hire",
      color: "text-green-400",
      description: "Solid performance. You demonstrated strong SQL fundamentals and problem-solving.",
    };
  if (ratio >= 0.5)
    return {
      label: "Lean Hire",
      color: "text-amber-400",
      description: "Decent showing with room to improve. Focus on the concepts you missed.",
    };
  if (ratio >= 0.3)
    return {
      label: "Lean No Hire",
      color: "text-orange-400",
      description:
        diffMix === "faang"
          ? "FAANG-level questions are tough. Review window functions and CTEs."
          : "Keep practicing. Review the solutions to understand the patterns.",
    };
  return {
    label: "No Hire",
    color: "text-red-400",
    description: "Don't be discouraged — every expert was once a beginner. Study the solutions and retry.",
  };
}

/* ------------------------------------------------------------------ */
/*  SETUP PHASE                                                        */
/* ------------------------------------------------------------------ */

function SetupPhase({
  onStart,
}: {
  onStart: (config: {
    company: Company;
    role: Role;
    questionCount: number;
    timePerQuestion: number;
    difficultyMix: string;
  }) => void;
}) {
  const [company, setCompany] = useState<Company>("faang");
  const [role, setRole] = useState<Role>("data-analyst");
  const [questionCount, setQuestionCount] = useState(5);
  const [timePerQuestion, setTimePerQuestion] = useState(15);
  const [difficultyMix, setDifficultyMix] = useState("balanced");

  return (
    <div className="mx-auto max-w-2xl px-6 py-12">
      {/* Header */}
      <div className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-[var(--color-accent)]/10">
          <svg
            className="h-8 w-8 text-[var(--color-accent)]"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z"
            />
          </svg>
        </div>
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
          Mock SQL Interview
        </h1>
        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
          Simulate a real SQL interview. Timed questions, no hints, no peeking at
          solutions. Just you and the query editor.
        </p>
      </div>

      {/* Config */}
      <div className="mt-10 space-y-8">
        {/* Company */}
        <div>
          <label className="mb-3 block text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
            Target Company
          </label>
          <div className="grid grid-cols-5 gap-2">
            {COMPANIES.map((c) => (
              <button
                key={c.value}
                onClick={() => setCompany(c.value)}
                className={`flex flex-col items-center gap-1.5 rounded-xl border-2 p-4 text-sm font-medium transition-all ${
                  company === c.value
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                    : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-text-muted)]"
                }`}
              >
                <span className="text-lg font-bold">{c.icon}</span>
                <span className="text-xs">{c.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Role */}
        <div>
          <label className="mb-3 block text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
            Role
          </label>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {ROLES.map((r) => (
              <button
                key={r.value}
                onClick={() => setRole(r.value)}
                className={`rounded-xl border-2 px-4 py-3 text-sm font-medium transition-all ${
                  role === r.value
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                    : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-text-muted)]"
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        {/* Difficulty Mix */}
        <div>
          <label className="mb-3 block text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
            Difficulty
          </label>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {DIFFICULTY_MIXES.map((d) => (
              <button
                key={d.value}
                onClick={() => setDifficultyMix(d.value)}
                className={`rounded-xl border-2 px-4 py-3 transition-all ${
                  difficultyMix === d.value
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10"
                    : "border-[var(--color-border)] hover:border-[var(--color-text-muted)]"
                }`}
              >
                <span
                  className={`block text-sm font-medium ${
                    difficultyMix === d.value
                      ? "text-[var(--color-accent)]"
                      : "text-[var(--color-text-secondary)]"
                  }`}
                >
                  {d.label}
                </span>
                <div className="mt-2 flex gap-0.5">
                  {/* Visual difficulty bar */}
                  {Array.from({ length: 10 }).map((_, i) => {
                    const easyEnd = Math.round(d.mix.easy * 10);
                    const medEnd = easyEnd + Math.round(d.mix.medium * 10);
                    let color = "bg-red-500";
                    if (i < easyEnd) color = "bg-emerald-500";
                    else if (i < medEnd) color = "bg-amber-500";
                    return (
                      <div
                        key={i}
                        className={`h-1.5 flex-1 rounded-full ${color} opacity-60`}
                      />
                    );
                  })}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Questions + Time */}
        <div className="grid grid-cols-2 gap-6">
          <div>
            <label className="mb-3 block text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
              Questions
            </label>
            <div className="flex gap-2">
              {QUESTION_COUNTS.map((n) => (
                <button
                  key={n}
                  onClick={() => setQuestionCount(n)}
                  className={`flex-1 rounded-xl border-2 py-3 text-center text-sm font-bold transition-all ${
                    questionCount === n
                      ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                      : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-text-muted)]"
                  }`}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="mb-3 block text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
              Time / Question
            </label>
            <div className="flex flex-wrap gap-2">
              {TIME_OPTIONS.map((t) => (
                <button
                  key={t.value}
                  onClick={() => setTimePerQuestion(t.value)}
                  className={`flex-1 rounded-xl border-2 py-3 text-center text-xs font-bold transition-all ${
                    timePerQuestion === t.value
                      ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                      : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-text-muted)]"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Summary + Start */}
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-[var(--color-text-secondary)]">
                <span className="font-semibold text-[var(--color-text-primary)]">
                  {questionCount} questions
                </span>{" "}
                &middot; {timePerQuestion} min each &middot;{" "}
                {formatTime(questionCount * timePerQuestion * 60 * 1000)} total
              </p>
              <p className="mt-1 text-xs text-[var(--color-text-muted)]">
                {COMPANIES.find((c) => c.value === company)?.label} &middot;{" "}
                {ROLES.find((r) => r.value === role)?.label} &middot;{" "}
                {DIFFICULTY_MIXES.find((d) => d.value === difficultyMix)?.label}
              </p>
            </div>
            <button
              onClick={() =>
                onStart({
                  company,
                  role,
                  questionCount,
                  timePerQuestion,
                  difficultyMix,
                })
              }
              className="rounded-xl bg-[var(--color-accent)] px-8 py-3 text-sm font-bold text-white shadow-lg shadow-[var(--color-accent)]/25 transition-all hover:brightness-110"
            >
              Start Interview
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  INTERVIEW PHASE                                                    */
/* ------------------------------------------------------------------ */

function InterviewPhase({
  problems,
  timePerQuestion,
  onFinish,
}: {
  problems: ProblemDetail[];
  timePerQuestion: number;
  onFinish: (results: QuestionResult[]) => void;
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<QuestionResult[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [timeLeft, setTimeLeft] = useState(timePerQuestion * 60 * 1000);
  const [feedback, setFeedback] = useState<{
    status: "accepted" | "wrong_answer" | "error";
    message: string;
  } | null>(null);
  const questionStartRef = useRef(Date.now());
  const timerRef = useRef<ReturnType<typeof setInterval>>(undefined);

  const problem = problems[currentIndex];
  const isLast = currentIndex === problems.length - 1;

  // Timer
  useEffect(() => {
    questionStartRef.current = Date.now();
    setTimeLeft(timePerQuestion * 60 * 1000);
    setQuery("");
    setFeedback(null);

    timerRef.current = setInterval(() => {
      const elapsed = Date.now() - questionStartRef.current;
      const remaining = timePerQuestion * 60 * 1000 - elapsed;
      setTimeLeft(remaining);

      if (remaining <= 0) {
        clearInterval(timerRef.current);
        // Auto-submit as timeout
        handleTimeout();
      }
    }, 1000);

    return () => clearInterval(timerRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIndex]);

  const handleTimeout = useCallback(() => {
    const elapsed = Date.now() - questionStartRef.current;
    const result: QuestionResult = {
      problem,
      status: "timeout",
      query,
      timeSpentMs: elapsed,
      userResult: null,
    };

    if (isLast) {
      onFinish([...results, result]);
    } else {
      setResults((prev) => [...prev, result]);
      setCurrentIndex((prev) => prev + 1);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [problem, query, isLast, results, onFinish]);

  const handleSubmit = useCallback(async () => {
    if (!query.trim() || submitting) return;
    setSubmitting(true);
    setFeedback(null);
    const elapsed = Date.now() - questionStartRef.current;

    try {
      const response = await apiClient<{
        status: "accepted" | "wrong_answer" | "error";
        user_result: {
          columns: string[];
          rows: unknown[][];
          row_count: number;
          execution_time_ms: number;
        } | null;
        error: string | null;
      }>("/api/query/execute", {
        method: "POST",
        body: JSON.stringify({
          query,
          problem_id: problem.id,
          dialect: "postgresql",
          dataset: problem.dataset,
        }),
      });

      const result: QuestionResult = {
        problem,
        status: response.status,
        query,
        timeSpentMs: elapsed,
        userResult: response.user_result
          ? {
              columns: response.user_result.columns,
              rows: response.user_result.rows,
              row_count: response.user_result.row_count,
            }
          : null,
      };

      if (response.status === "accepted") {
        // Correct — brief feedback then auto-advance
        setFeedback({ status: "accepted", message: "Correct! Well done." });
        clearInterval(timerRef.current);
        setTimeout(() => {
          if (isLast) {
            onFinish([...results, result]);
          } else {
            setResults((prev) => [...prev, result]);
            setCurrentIndex((prev) => prev + 1);
          }
        }, 1500);
      } else {
        // Wrong answer — show brief feedback, let them retry
        setFeedback({
          status: response.status,
          message:
            response.status === "error"
              ? response.error || "Query error. Check your syntax."
              : "Wrong answer. You can retry or skip.",
        });
      }
    } catch {
      setFeedback({
        status: "error",
        message: "Network error. Try submitting again.",
      });
    } finally {
      setSubmitting(false);
    }
  }, [query, submitting, problem, isLast, results, onFinish]);

  const handleSkip = useCallback(() => {
    clearInterval(timerRef.current);
    const elapsed = Date.now() - questionStartRef.current;
    const result: QuestionResult = {
      problem,
      status: "skipped",
      query,
      timeSpentMs: elapsed,
      userResult: null,
    };

    if (isLast) {
      onFinish([...results, result]);
    } else {
      setResults((prev) => [...prev, result]);
      setCurrentIndex((prev) => prev + 1);
    }
  }, [problem, query, isLast, results, onFinish]);

  const handleEndEarly = useCallback(() => {
    clearInterval(timerRef.current);
    const elapsed = Date.now() - questionStartRef.current;
    // Mark remaining questions as skipped
    const remaining: QuestionResult[] = problems
      .slice(currentIndex)
      .map((p, i) => ({
        problem: p,
        status: "skipped" as const,
        query: i === 0 ? query : "",
        timeSpentMs: i === 0 ? elapsed : 0,
        userResult: null,
      }));
    onFinish([...results, ...remaining]);
  }, [problems, currentIndex, query, results, onFinish]);

  // Schema for this problem
  const datasetSchema = getSchemaForDataset(problem.dataset);
  const relevantSchema =
    problem.schema_hint.length > 0
      ? datasetSchema.filter((t) => problem.schema_hint.includes(t.name))
      : datasetSchema;
  const tables = relevantSchema.map((t) => ({
    name: t.name,
    columns: t.columns.map((c) => c.name),
  }));

  const timerWarning = timeLeft < 60000;
  const timerCritical = timeLeft < 30000;

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col">
      {/* Top Bar */}
      <div className="flex items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2">
        <div className="flex items-center gap-4">
          {/* Progress dots */}
          <div className="flex items-center gap-1.5">
            {problems.map((_, i) => (
              <div
                key={i}
                className={`h-2.5 w-2.5 rounded-full transition-all ${
                  i < currentIndex
                    ? results[i]?.status === "accepted"
                      ? "bg-emerald-500"
                      : "bg-red-500"
                    : i === currentIndex
                      ? "bg-[var(--color-accent)] ring-2 ring-[var(--color-accent)]/30"
                      : "bg-[var(--color-border)]"
                }`}
              />
            ))}
          </div>
          <span className="text-sm font-medium text-[var(--color-text-secondary)]">
            Question {currentIndex + 1} of {problems.length}
          </span>
          <Badge variant={problem.difficulty}>{problem.difficulty}</Badge>
        </div>

        <div className="flex items-center gap-4">
          {/* Timer */}
          <div
            className={`rounded-lg px-4 py-1.5 font-mono text-lg font-bold tabular-nums ${
              timerCritical
                ? "animate-pulse bg-red-500/20 text-red-400"
                : timerWarning
                  ? "bg-amber-500/10 text-amber-400"
                  : "text-[var(--color-text-primary)]"
            }`}
          >
            {formatTime(timeLeft)}
          </div>
          <button
            onClick={handleEndEarly}
            className="rounded-lg border border-red-500/30 px-3 py-1.5 text-xs font-medium text-red-400 transition-colors hover:bg-red-500/10"
          >
            End Interview
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Problem Description */}
        <div className="w-[40%] overflow-y-auto border-r border-[var(--color-border)] p-6">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)]">
            {problem.title}
          </h2>
          <div className="mt-1 flex flex-wrap gap-1.5">
            {(problem.concept_tags || []).map((tag) => (
              <span
                key={tag}
                className="rounded bg-[var(--color-accent)]/10 px-1.5 py-0.5 text-[10px] font-medium text-[var(--color-accent)]"
              >
                {tag}
              </span>
            ))}
          </div>

          <div className="mt-4 text-sm leading-relaxed text-[var(--color-text-secondary)] whitespace-pre-wrap">
            {problem.description}
          </div>

          {/* Schema */}
          <div className="mt-6">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
              Available Tables
            </h3>
            <div className="mt-2 space-y-2">
              {relevantSchema.map((table) => (
                <details
                  key={table.name}
                  className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)]"
                >
                  <summary className="cursor-pointer px-3 py-2 text-xs font-medium text-[var(--color-text-primary)]">
                    {table.name}{" "}
                    <span className="text-[var(--color-text-muted)]">
                      ({table.columns.length} cols)
                    </span>
                  </summary>
                  <div className="border-t border-[var(--color-border)] px-3 py-2">
                    <div className="flex flex-wrap gap-x-3 gap-y-1">
                      {table.columns.map((col) => (
                        <span
                          key={col.name}
                          className="text-[11px] text-[var(--color-text-secondary)]"
                        >
                          <span
                            className={
                              col.isPrimaryKey
                                ? "font-bold text-amber-500"
                                : col.isForeignKey
                                  ? "text-blue-400"
                                  : ""
                            }
                          >
                            {col.name}
                          </span>
                          <span className="ml-1 text-[var(--color-text-muted)]">
                            {col.type}
                          </span>
                        </span>
                      ))}
                    </div>
                  </div>
                </details>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Editor + Actions */}
        <div className="flex w-[60%] flex-col">
          {/* Editor */}
          <div className="flex-1 overflow-hidden">
            <SQLEditor
              value={query}
              onChange={setQuery}
              onRun={handleSubmit}
              dialect="postgresql"
              tables={tables}
            />
          </div>

          {/* Feedback Bar */}
          {feedback && (
            <div
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium ${
                feedback.status === "accepted"
                  ? "bg-emerald-500/10 text-emerald-400"
                  : "bg-red-500/10 text-red-400"
              }`}
            >
              {feedback.status === "accepted" ? (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
              {feedback.message}
            </div>
          )}

          {/* Bottom Actions */}
          <div className="flex items-center justify-between border-t border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3">
            <button
              onClick={handleSkip}
              className="rounded-lg border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:border-amber-500/50 hover:text-amber-400"
            >
              Skip Question
            </button>
            <button
              onClick={handleSubmit}
              disabled={!query.trim() || submitting}
              className="rounded-lg bg-[var(--color-accent)] px-6 py-2 text-sm font-bold text-white transition-all hover:brightness-110 disabled:opacity-40"
            >
              {submitting ? (
                <span className="flex items-center gap-2">
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Checking...
                </span>
              ) : (
                "Submit Answer"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  RESULTS PHASE                                                      */
/* ------------------------------------------------------------------ */

function ResultsPhase({
  results,
  difficultyMix,
  config,
  onRetry,
  onNewInterview,
}: {
  results: QuestionResult[];
  difficultyMix: string;
  config: {
    company: Company;
    role: Role;
    questionCount: number;
    timePerQuestion: number;
  };
  onRetry: () => void;
  onNewInterview: () => void;
}) {
  const [reviewIndex, setReviewIndex] = useState<number | null>(null);

  const solved = results.filter((r) => r.status === "accepted").length;
  const totalTimeMs = results.reduce((sum, r) => sum + r.timeSpentMs, 0);
  const avgTimeSec = totalTimeMs / results.length / 1000;
  const rating = getPerformanceRating(solved, results.length, avgTimeSec, difficultyMix);

  const conceptStats = useMemo(() => {
    const map: Record<string, { total: number; solved: number }> = {};
    for (const r of results) {
      for (const tag of r.problem.concept_tags || []) {
        if (!map[tag]) map[tag] = { total: 0, solved: 0 };
        map[tag].total++;
        if (r.status === "accepted") map[tag].solved++;
      }
    }
    return Object.entries(map)
      .sort((a, b) => a[1].solved / a[1].total - b[1].solved / b[1].total)
      .slice(0, 8);
  }, [results]);

  const reviewProblem = reviewIndex !== null ? results[reviewIndex] : null;

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
          Interview Complete
        </h1>
        <p className="mt-1 text-sm text-[var(--color-text-muted)]">
          {COMPANIES.find((c) => c.value === config.company)?.label} &middot;{" "}
          {ROLES.find((r) => r.value === config.role)?.label}
        </p>
      </div>

      {/* Score Card */}
      <div className="mt-8 rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-8 text-center">
        <div className="text-6xl font-black text-[var(--color-text-primary)]">
          {solved}
          <span className="text-2xl text-[var(--color-text-muted)]">
            /{results.length}
          </span>
        </div>
        <p className={`mt-2 text-xl font-bold ${rating.color}`}>
          {rating.label}
        </p>
        <p className="mt-2 max-w-md mx-auto text-sm text-[var(--color-text-secondary)]">
          {rating.description}
        </p>

        <div className="mt-6 flex items-center justify-center gap-8 text-sm">
          <div>
            <p className="text-2xl font-bold text-[var(--color-text-primary)]">
              {formatTime(totalTimeMs)}
            </p>
            <p className="text-xs text-[var(--color-text-muted)]">Total Time</p>
          </div>
          <div className="h-8 w-px bg-[var(--color-border)]" />
          <div>
            <p className="text-2xl font-bold text-[var(--color-text-primary)]">
              {formatTime(avgTimeSec * 1000)}
            </p>
            <p className="text-xs text-[var(--color-text-muted)]">Avg / Question</p>
          </div>
          <div className="h-8 w-px bg-[var(--color-border)]" />
          <div>
            <p className="text-2xl font-bold text-[var(--color-text-primary)]">
              {Math.round((solved / results.length) * 100)}%
            </p>
            <p className="text-xs text-[var(--color-text-muted)]">Accuracy</p>
          </div>
        </div>
      </div>

      {/* Concept Strengths */}
      {conceptStats.length > 0 && (
        <div className="mt-8">
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Concept Breakdown
          </h2>
          <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
            {conceptStats.map(([tag, stat]) => {
              const pct = Math.round((stat.solved / stat.total) * 100);
              return (
                <div
                  key={tag}
                  className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-3"
                >
                  <p className="text-xs font-medium text-[var(--color-text-primary)] truncate">
                    {tag}
                  </p>
                  <div className="mt-2 flex items-center gap-2">
                    <div className="h-1.5 flex-1 rounded-full bg-[var(--color-border)]">
                      <div
                        className={`h-1.5 rounded-full ${
                          pct >= 75
                            ? "bg-emerald-500"
                            : pct >= 50
                              ? "bg-amber-500"
                              : "bg-red-500"
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-bold text-[var(--color-text-muted)]">
                      {stat.solved}/{stat.total}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Question-by-Question */}
      <div className="mt-8">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Question Review
        </h2>
        <div className="mt-3 space-y-2">
          {results.map((r, i) => (
            <div key={i}>
              <button
                onClick={() =>
                  setReviewIndex(reviewIndex === i ? null : i)
                }
                className="flex w-full items-center gap-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 text-left transition-colors hover:border-[var(--color-accent)]/50"
              >
                {/* Status icon */}
                <div
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                    r.status === "accepted"
                      ? "bg-emerald-500/20 text-emerald-400"
                      : r.status === "skipped"
                        ? "bg-gray-500/20 text-gray-400"
                        : r.status === "timeout"
                          ? "bg-amber-500/20 text-amber-400"
                          : "bg-red-500/20 text-red-400"
                  }`}
                >
                  {r.status === "accepted"
                    ? "\u2713"
                    : r.status === "skipped"
                      ? "\u2014"
                      : r.status === "timeout"
                        ? "\u23F1"
                        : "\u2717"}
                </div>

                <div className="flex-1 min-w-0">
                  <span className="text-sm font-medium text-[var(--color-text-primary)] truncate block">
                    {r.problem.title}
                  </span>
                </div>

                <Badge variant={r.problem.difficulty}>
                  {r.problem.difficulty}
                </Badge>

                <span className="ml-2 text-xs font-mono text-[var(--color-text-muted)] tabular-nums">
                  {formatTime(r.timeSpentMs)}
                </span>

                <svg
                  className={`h-4 w-4 text-[var(--color-text-muted)] transition-transform ${
                    reviewIndex === i ? "rotate-180" : ""
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>

              {/* Expanded Review */}
              {reviewIndex === i && reviewProblem && (
                <div className="mt-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-5">
                  <div className="grid gap-4 md:grid-cols-2">
                    {/* Your query */}
                    <div>
                      <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                        Your Query
                      </h4>
                      <pre className="mt-2 overflow-x-auto rounded-lg bg-[var(--color-surface)] p-3 text-xs text-[var(--color-text-secondary)]">
                        {r.query || "(no query submitted)"}
                      </pre>
                    </div>

                    {/* Explanation */}
                    <div>
                      <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                        Solution Approach
                      </h4>
                      <div className="mt-2 text-xs text-[var(--color-text-secondary)] leading-relaxed whitespace-pre-wrap">
                        {r.problem.explanation || "No explanation available."}
                      </div>
                    </div>
                  </div>

                  {/* Approach */}
                  {r.problem.approach && (
                    <div className="mt-4">
                      <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                        Step-by-Step Approach
                      </h4>
                      <div className="mt-2 text-xs text-[var(--color-text-secondary)] leading-relaxed whitespace-pre-wrap">
                        {Array.isArray(r.problem.approach)
                          ? r.problem.approach.join("\n")
                          : r.problem.approach}
                      </div>
                    </div>
                  )}

                  {/* Common Mistakes */}
                  {r.problem.common_mistakes &&
                    r.problem.common_mistakes.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">
                          Common Mistakes
                        </h4>
                        <ul className="mt-2 space-y-1">
                          {r.problem.common_mistakes.map((m, j) => (
                            <li
                              key={j}
                              className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]"
                            >
                              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500/50" />
                              {m}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="mt-8 flex items-center justify-center gap-4">
        <button
          onClick={onRetry}
          className="rounded-xl border border-[var(--color-border)] px-6 py-3 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
        >
          Retry Same Questions
        </button>
        <button
          onClick={onNewInterview}
          className="rounded-xl bg-[var(--color-accent)] px-6 py-3 text-sm font-bold text-white shadow-lg shadow-[var(--color-accent)]/25 transition-all hover:brightness-110"
        >
          New Interview
        </button>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  MAIN PAGE                                                          */
/* ------------------------------------------------------------------ */

export default function InterviewPage() {
  const [phase, setPhase] = useState<Phase>("setup");
  const [problems, setProblems] = useState<ProblemDetail[]>([]);
  const [results, setResults] = useState<QuestionResult[]>([]);
  const [config, setConfig] = useState<{
    company: Company;
    role: Role;
    questionCount: number;
    timePerQuestion: number;
    difficultyMix: string;
  } | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const allProblemsRef = useRef<ProblemFromAPI[]>([]);

  // Prefetch problem list on mount
  useEffect(() => {
    apiClient<{ problems: ProblemFromAPI[]; total: number }>("/api/problems")
      .then((data) => {
        allProblemsRef.current = data.problems;
      })
      .catch(() => {});
  }, []);

  const handleStart = useCallback(
    async (cfg: {
      company: Company;
      role: Role;
      questionCount: number;
      timePerQuestion: number;
      difficultyMix: string;
    }) => {
      setConfig(cfg);
      setPhase("loading");
      setLoadError(null);

      try {
        // If problems haven't been fetched yet
        if (allProblemsRef.current.length === 0) {
          const data = await apiClient<{
            problems: ProblemFromAPI[];
            total: number;
          }>("/api/problems");
          allProblemsRef.current = data.problems;
        }

        const all = allProblemsRef.current;
        const mix =
          DIFFICULTY_MIXES.find((d) => d.value === cfg.difficultyMix)?.mix ?? {
            easy: 0.3,
            medium: 0.4,
            hard: 0.3,
          };

        // Select problems by difficulty ratio
        const byDiff: Record<Difficulty, ProblemFromAPI[]> = {
          easy: shuffle(
            all.filter((p) => p.difficulty === "easy"),
            Date.now()
          ),
          medium: shuffle(
            all.filter((p) => p.difficulty === "medium"),
            Date.now() + 1
          ),
          hard: shuffle(
            all.filter((p) => p.difficulty === "hard"),
            Date.now() + 2
          ),
        };

        const counts: Record<Difficulty, number> = {
          easy: Math.round(cfg.questionCount * mix.easy),
          medium: Math.round(cfg.questionCount * mix.medium),
          hard: 0,
        };
        counts.hard = cfg.questionCount - counts.easy - counts.medium;

        const selected: ProblemFromAPI[] = [];
        for (const diff of ["easy", "medium", "hard"] as Difficulty[]) {
          selected.push(...byDiff[diff].slice(0, counts[diff]));
        }

        // Fill if we don't have enough
        while (selected.length < cfg.questionCount) {
          const remaining = all.filter(
            (p) => !selected.some((s) => s.id === p.id)
          );
          if (remaining.length === 0) break;
          selected.push(
            remaining[Math.floor(Math.random() * remaining.length)]
          );
        }

        // Shuffle the final selection so difficulties are mixed
        const finalSelection = shuffle(selected, Date.now() + 3);

        // Fetch full details for each selected problem in parallel
        const details = await Promise.all(
          finalSelection.map((p) =>
            apiClient<ProblemDetail>(`/api/problems/${p.slug}`)
          )
        );

        setProblems(details);
        setPhase("interview");
      } catch {
        setLoadError(
          "Failed to load interview questions. Please try again."
        );
        setPhase("setup");
      }
    },
    []
  );

  const handleFinish = useCallback((questionResults: QuestionResult[]) => {
    setResults(questionResults);
    setPhase("results");
  }, []);

  const handleRetry = useCallback(() => {
    setResults([]);
    setPhase("interview");
  }, []);

  const handleNewInterview = useCallback(() => {
    setResults([]);
    setProblems([]);
    setConfig(null);
    setPhase("setup");
  }, []);

  if (phase === "setup") {
    return (
      <>
        {loadError && (
          <div className="mx-auto mt-4 max-w-md rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2 text-center text-sm text-red-400">
            {loadError}
          </div>
        )}
        <SetupPhase onStart={handleStart} />
      </>
    );
  }

  if (phase === "loading") {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] flex-col items-center justify-center gap-4">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
        <p className="text-sm text-[var(--color-text-secondary)]">
          Preparing your interview questions...
        </p>
        <p className="text-xs text-[var(--color-text-muted)]">
          Selecting {config?.questionCount} questions based on your preferences
        </p>
      </div>
    );
  }

  if (phase === "interview" && problems.length > 0) {
    return (
      <InterviewPhase
        problems={problems}
        timePerQuestion={config?.timePerQuestion ?? 15}
        onFinish={handleFinish}
      />
    );
  }

  if (phase === "results" && config) {
    return (
      <ResultsPhase
        results={results}
        difficultyMix={config.difficultyMix}
        config={config}
        onRetry={handleRetry}
        onNewInterview={handleNewInterview}
      />
    );
  }

  return null;
}
