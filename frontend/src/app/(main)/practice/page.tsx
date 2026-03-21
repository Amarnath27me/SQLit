"use client";

import { useState, useMemo, useEffect } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { apiClient } from "@/lib/api";
import type { Difficulty, ProblemCategory, Dataset } from "@/types";

interface ProblemListItem {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: ProblemCategory;
  dataset: Dataset;
  concept_tags: string[];
}

const DIFFICULTIES: Difficulty[] = ["easy", "medium", "hard"];
const CATEGORIES: { value: ProblemCategory; label: string }[] = [
  { value: "select", label: "SELECT" },
  { value: "where", label: "WHERE" },
  { value: "aggregation", label: "Aggregation" },
  { value: "joins", label: "Joins" },
  { value: "subqueries", label: "Subqueries" },
  { value: "window-functions", label: "Window Functions" },
  { value: "cte", label: "CTEs" },
  { value: "advanced", label: "Advanced" },
];
const DATASETS: { value: Dataset; label: string }[] = [
  { value: "ecommerce", label: "E-Commerce" },
  { value: "finance", label: "Finance" },
  { value: "healthcare", label: "Healthcare" },
];

export default function PracticePage() {
  const [problems, setProblems] = useState<ProblemListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState<Difficulty | "all">("all");
  const [categoryFilter, setCategoryFilter] = useState<ProblemCategory | "all">("all");
  const [datasetFilter, setDatasetFilter] = useState<Dataset | "all">("all");
  const [viewMode, setViewMode] = useState<"list" | "category">("list");

  const fetchProblems = () => {
    setLoading(true);
    setError(null);
    apiClient<{ problems: ProblemListItem[]; total: number }>("/api/problems")
      .then((data) => setProblems(data.problems))
      .catch(() => setError("Failed to load problems. Please try again."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchProblems();
  }, []);

  const filtered = useMemo(() => {
    return problems.filter((p) => {
      if (difficultyFilter !== "all" && p.difficulty !== difficultyFilter) return false;
      if (categoryFilter !== "all" && p.category !== categoryFilter) return false;
      if (datasetFilter !== "all" && p.dataset !== datasetFilter) return false;
      if (search && !p.title.toLowerCase().includes(search.toLowerCase())) return false;
      return true;
    });
  }, [problems, search, difficultyFilter, categoryFilter, datasetFilter]);

  const grouped = useMemo(() => {
    const groups: Record<string, ProblemListItem[]> = {};
    for (const p of filtered) {
      const cat = CATEGORIES.find((c) => c.value === p.category)?.label ?? p.category;
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(p);
    }
    return groups;
  }, [filtered]);

  // Count problems per dataset for the header
  const datasetCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const p of problems) {
      counts[p.dataset] = (counts[p.dataset] || 0) + 1;
    }
    return counts;
  }, [problems]);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Practice Arena</h1>
          <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
            {problems.length} problems
            {Object.keys(datasetCounts).length > 1 && (
              <span>
                {" "}across {Object.keys(datasetCounts).length} datasets
              </span>
            )}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode("list")}
            aria-label="View as list"
            aria-pressed={viewMode === "list"}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              viewMode === "list"
                ? "bg-[var(--color-accent)] text-white"
                : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
            }`}
          >
            List
          </button>
          <button
            onClick={() => setViewMode("category")}
            aria-label="View by category"
            aria-pressed={viewMode === "category"}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              viewMode === "category"
                ? "bg-[var(--color-accent)] text-white"
                : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
            }`}
          >
            By Category
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="mt-6 flex flex-wrap items-center gap-3">
        <input
          type="text"
          placeholder="Search problems..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search problems"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
        />
        <select
          value={datasetFilter}
          onChange={(e) => setDatasetFilter(e.target.value as Dataset | "all")}
          aria-label="Filter by dataset"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Datasets</option>
          {DATASETS.map((d) => (
            <option key={d.value} value={d.value}>
              {d.label} {datasetCounts[d.value] ? `(${datasetCounts[d.value]})` : ""}
            </option>
          ))}
        </select>
        <select
          value={difficultyFilter}
          onChange={(e) => setDifficultyFilter(e.target.value as Difficulty | "all")}
          aria-label="Filter by difficulty"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Difficulties</option>
          {DIFFICULTIES.map((d) => (
            <option key={d} value={d}>
              {d.charAt(0).toUpperCase() + d.slice(1)}
            </option>
          ))}
        </select>
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value as ProblemCategory | "all")}
          aria-label="Filter by category"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Categories</option>
          {CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>
      </div>

      {/* Loading */}
      {loading && (
        <div className="mt-12 flex justify-center">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex flex-col items-center justify-center gap-4 py-20">
          <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-6 py-4 text-center">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
          <button
            onClick={() => { setError(null); fetchProblems(); }}
            className="rounded-lg bg-[var(--color-surface)] border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Problem List */}
      {!loading && viewMode === "list" && (
        <div className="mt-6">
          <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--color-border)]">
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">#</th>
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Title</th>
                <th className="hidden md:table-cell pb-3 text-xs font-medium text-[var(--color-text-muted)]">Dataset</th>
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Difficulty</th>
                <th className="hidden md:table-cell pb-3 text-xs font-medium text-[var(--color-text-muted)]">Category</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((problem, i) => (
                <tr
                  key={problem.id}
                  className="border-b border-[var(--color-border)] transition-colors hover:bg-[var(--color-surface)]"
                >
                  <td className="py-3 text-[var(--color-text-muted)]">{i + 1}</td>
                  <td className="py-3">
                    <Link
                      href={`/practice/${problem.slug}`}
                      className="font-medium text-[var(--color-text-primary)] hover:text-[var(--color-accent)]"
                    >
                      {problem.title}
                    </Link>
                  </td>
                  <td className="hidden md:table-cell py-3">
                    <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-secondary)]">
                      {DATASETS.find((d) => d.value === problem.dataset)?.label ?? problem.dataset}
                    </span>
                  </td>
                  <td className="py-3">
                    <Badge variant={problem.difficulty}>{problem.difficulty}</Badge>
                  </td>
                  <td className="hidden md:table-cell py-3">
                    <span className="text-xs text-[var(--color-text-muted)]">
                      {CATEGORIES.find((c) => c.value === problem.category)?.label ?? problem.category}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
          {filtered.length === 0 && (
            <p className="py-8 text-center text-sm text-[var(--color-text-muted)]">
              No problems match your filters.
            </p>
          )}
        </div>
      )}

      {!loading && viewMode === "category" && (
        <div className="mt-6 space-y-8">
          {Object.entries(grouped).map(([category, probs]) => (
            <div key={category}>
              <h3 className="mb-3 text-sm font-semibold text-[var(--color-text-primary)]">
                {category}
                <span className="ml-2 text-xs font-normal text-[var(--color-text-muted)]">
                  {probs.length} problems
                </span>
              </h3>
              <div className="grid gap-2">
                {probs.map((problem) => (
                  <Link
                    key={problem.id}
                    href={`/practice/${problem.slug}`}
                    className="flex items-center justify-between rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 transition-colors hover:border-[var(--color-accent)]"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-[var(--color-text-primary)]">
                        {problem.title}
                      </span>
                      <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-muted)]">
                        {DATASETS.find((d) => d.value === problem.dataset)?.label ?? problem.dataset}
                      </span>
                    </div>
                    <Badge variant={problem.difficulty}>{problem.difficulty}</Badge>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
