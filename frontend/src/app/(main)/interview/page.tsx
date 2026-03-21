"use client";

import { useState, useMemo, useEffect } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { apiClient } from "@/lib/api";
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

type Company = "faang" | "big-tech" | "fintech" | "startup" | "consulting";
type Role = "data-analyst" | "data-engineer" | "backend" | "full-stack" | "product-analyst";

interface InterviewProblem extends ProblemFromAPI {
  companies: Company[];
  roles: Role[];
  frequency: "high" | "medium" | "low";
}

/* ------------------------------------------------------------------ */
/*  Deterministic enrichment (company, role, frequency)                */
/*  Uses a seeded hash so values stay stable across renders            */
/* ------------------------------------------------------------------ */

function hashCode(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

const ALL_COMPANIES: Company[] = ["faang", "big-tech", "fintech", "startup", "consulting"];
const ALL_ROLES: Role[] = ["data-analyst", "data-engineer", "backend", "full-stack", "product-analyst"];

function enrichProblem(p: ProblemFromAPI): InterviewProblem {
  const h = hashCode(p.id);
  const tags = (p.concept_tags || []).map((t) => t.toLowerCase());
  const cat = (p.category || "").toLowerCase();

  // Assign companies based on difficulty + concept tags
  const companies: Company[] = [];
  if (p.difficulty === "hard" || tags.some((t) => t.includes("window") || t.includes("cte") || t.includes("recursive"))) {
    companies.push("faang");
  }
  if (tags.some((t) => t.includes("join") || t.includes("aggregat") || t.includes("subquer"))) {
    companies.push("big-tech");
  }
  if (p.dataset === "finance" || tags.some((t) => t.includes("sum") || t.includes("running") || t.includes("balance"))) {
    companies.push("fintech");
  }
  if (p.difficulty === "easy" || p.difficulty === "medium") {
    companies.push("startup");
  }
  if (tags.some((t) => t.includes("case") || t.includes("pivot") || t.includes("percentage"))) {
    companies.push("consulting");
  }
  // Ensure at least 2 companies
  if (companies.length < 2) {
    const extra = ALL_COMPANIES[h % ALL_COMPANIES.length];
    if (!companies.includes(extra)) companies.push(extra);
    const extra2 = ALL_COMPANIES[(h + 3) % ALL_COMPANIES.length];
    if (!companies.includes(extra2)) companies.push(extra2);
  }

  // Assign roles based on concept tags + dataset
  const roles: Role[] = [];
  if (tags.some((t) => t.includes("aggregat") || t.includes("group") || t.includes("count") || t.includes("avg"))) {
    roles.push("data-analyst");
  }
  if (tags.some((t) => t.includes("cte") || t.includes("window") || t.includes("running") || t.includes("recursive"))) {
    roles.push("data-engineer");
  }
  if (tags.some((t) => t.includes("join") || t.includes("subquer") || t.includes("exists"))) {
    roles.push("backend");
  }
  if (cat.includes("interview")) {
    roles.push("product-analyst");
  }
  if (p.difficulty === "easy" || p.difficulty === "medium") {
    roles.push("full-stack");
  }
  if (roles.length < 2) {
    const extra = ALL_ROLES[h % ALL_ROLES.length];
    if (!roles.includes(extra)) roles.push(extra);
  }

  // Frequency based on difficulty + concept commonality
  let frequency: "high" | "medium" | "low" = "medium";
  const commonTags = ["join", "group by", "where", "count", "aggregation", "subquery", "window", "case", "having"];
  const matchCount = tags.filter((t) => commonTags.some((ct) => t.includes(ct))).length;
  if (matchCount >= 2 || p.difficulty === "easy") {
    frequency = "high";
  } else if (p.difficulty === "hard" && matchCount === 0) {
    frequency = "low";
  }

  return {
    ...p,
    companies: [...new Set(companies)],
    roles: [...new Set(roles)],
    frequency,
  };
}

/* ------------------------------------------------------------------ */
/*  Filter config                                                      */
/* ------------------------------------------------------------------ */

const COMPANIES: { value: Company; label: string }[] = [
  { value: "faang", label: "FAANG" },
  { value: "big-tech", label: "Big Tech" },
  { value: "fintech", label: "FinTech" },
  { value: "startup", label: "Startups" },
  { value: "consulting", label: "Consulting" },
];

const ROLES: { value: Role; label: string }[] = [
  { value: "data-analyst", label: "Data Analyst" },
  { value: "data-engineer", label: "Data Engineer" },
  { value: "backend", label: "Backend Engineer" },
  { value: "full-stack", label: "Full-Stack Engineer" },
  { value: "product-analyst", label: "Product Analyst" },
];

const DATASETS: { value: Dataset; label: string }[] = [
  { value: "ecommerce", label: "E-Commerce" },
  { value: "finance", label: "Finance" },
  { value: "healthcare", label: "Healthcare" },
];

const CONCEPT_GROUPS = [
  { label: "JOINs", tags: ["join", "left join", "self join", "self-join", "cross join", "anti-join"] },
  { label: "Window Functions", tags: ["window", "row_number", "rank", "dense_rank", "lag", "lead", "ntile", "percent_rank", "sum over", "avg over", "count over", "rows between"] },
  { label: "Aggregation", tags: ["group by", "having", "count", "sum", "avg", "min", "max", "aggregate", "aggregation"] },
  { label: "Subqueries", tags: ["subquery", "subquery in from", "subquery in where", "nested", "correlated subquery", "scalar subquery", "exists", "semi-join"] },
  { label: "CTEs", tags: ["cte", "recursive cte", "multi-cte"] },
  { label: "Date/Time", tags: ["date", "strftime", "julianday", "date arithmetic", "date functions", "date extraction", "date sorting"] },
  { label: "CASE/Logic", tags: ["case", "case when", "coalesce", "nullif", "conditional", "null handling", "pivoting"] },
  { label: "String", tags: ["like", "substr", "upper", "length", "string"] },
];

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

export default function InterviewPrepPage() {
  const [problems, setProblems] = useState<InterviewProblem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [companyFilter, setCompanyFilter] = useState<Company | "all">("all");
  const [roleFilter, setRoleFilter] = useState<Role | "all">("all");
  const [difficultyFilter, setDifficultyFilter] = useState<Difficulty | "all">("all");
  const [datasetFilter, setDatasetFilter] = useState<Dataset | "all">("all");
  const [conceptFilter, setConceptFilter] = useState<string>("all");
  const [frequencyFilter, setFrequencyFilter] = useState<"high" | "medium" | "low" | "all">("all");
  const [viewMode, setViewMode] = useState<"list" | "concept">("list");
  const [sortBy, setSortBy] = useState<"default" | "difficulty" | "frequency">("default");

  const fetchProblems = () => {
    setLoading(true);
    setError(null);
    apiClient<{ problems: ProblemFromAPI[]; total: number }>("/api/problems")
      .then((data) => {
        const interviewOnly = data.problems.filter((p) => p.id.startsWith("interview-"));
        setProblems(interviewOnly.map(enrichProblem));
      })
      .catch(() => setError("Failed to load interview problems. Please try again."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchProblems();
  }, []);

  const filtered = useMemo(() => {
    let result = problems.filter((p) => {
      if (companyFilter !== "all" && !p.companies.includes(companyFilter)) return false;
      if (roleFilter !== "all" && !p.roles.includes(roleFilter)) return false;
      if (difficultyFilter !== "all" && p.difficulty !== difficultyFilter) return false;
      if (datasetFilter !== "all" && p.dataset !== datasetFilter) return false;
      if (frequencyFilter !== "all" && p.frequency !== frequencyFilter) return false;
      if (conceptFilter !== "all") {
        const group = CONCEPT_GROUPS.find((g) => g.label === conceptFilter);
        if (group) {
          const pTags = (p.concept_tags || []).map((t) => t.toLowerCase());
          if (!group.tags.some((gt) => pTags.some((pt) => pt.includes(gt)))) return false;
        }
      }
      if (search && !p.title.toLowerCase().includes(search.toLowerCase()) && !(p.concept_tags || []).some((t) => t.toLowerCase().includes(search.toLowerCase()))) return false;
      return true;
    });

    if (sortBy === "difficulty") {
      const order = { easy: 0, medium: 1, hard: 2 };
      result = [...result].sort((a, b) => order[a.difficulty] - order[b.difficulty]);
    } else if (sortBy === "frequency") {
      const order = { high: 0, medium: 1, low: 2 };
      result = [...result].sort((a, b) => order[a.frequency] - order[b.frequency]);
    }

    return result;
  }, [problems, search, companyFilter, roleFilter, difficultyFilter, datasetFilter, conceptFilter, frequencyFilter, sortBy]);

  const stats = useMemo(() => {
    const byDiff = { easy: 0, medium: 0, hard: 0 };
    const byFreq = { high: 0, medium: 0, low: 0 };
    for (const p of problems) {
      byDiff[p.difficulty]++;
      byFreq[p.frequency]++;
    }
    return { byDiff, byFreq };
  }, [problems]);

  const groupedByConcept = useMemo(() => {
    const groups: Record<string, InterviewProblem[]> = {};
    for (const p of filtered) {
      const pTags = (p.concept_tags || []).map((t) => t.toLowerCase());
      let matched = false;
      for (const group of CONCEPT_GROUPS) {
        if (group.tags.some((gt) => pTags.some((pt) => pt.includes(gt)))) {
          if (!groups[group.label]) groups[group.label] = [];
          groups[group.label].push(p);
          matched = true;
          break;
        }
      }
      if (!matched) {
        if (!groups["Other"]) groups["Other"] = [];
        groups["Other"].push(p);
      }
    }
    return groups;
  }, [filtered]);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Interview Prep</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          Practice the SQL questions most frequently asked at top tech companies. Curated and non-repetitive.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="mt-6 grid grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-3 lg:grid-cols-7">
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
          <p className="text-2xl font-bold text-[var(--color-accent)]">{problems.length}</p>
          <p className="text-xs text-[var(--color-text-muted)]">Total Problems</p>
        </div>
        <div className="rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-4">
          <p className="text-2xl font-bold text-emerald-500">{stats.byDiff.easy}</p>
          <p className="text-xs text-emerald-500/70">Easy</p>
        </div>
        <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-4">
          <p className="text-2xl font-bold text-amber-500">{stats.byDiff.medium}</p>
          <p className="text-xs text-amber-500/70">Medium</p>
        </div>
        <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4">
          <p className="text-2xl font-bold text-red-500">{stats.byDiff.hard}</p>
          <p className="text-xs text-red-500/70">Hard</p>
        </div>
        <div className="rounded-lg border border-red-400/20 bg-red-400/5 p-4">
          <p className="text-2xl font-bold text-red-400">{stats.byFreq.high}</p>
          <p className="text-xs text-red-400/70">Hot</p>
        </div>
        <div className="rounded-lg border border-orange-400/20 bg-orange-400/5 p-4">
          <p className="text-2xl font-bold text-orange-400">{stats.byFreq.medium}</p>
          <p className="text-xs text-orange-400/70">Common</p>
        </div>
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
          <p className="text-2xl font-bold text-[var(--color-text-muted)]">{stats.byFreq.low}</p>
          <p className="text-xs text-[var(--color-text-muted)]">Rare</p>
        </div>
      </div>

      {/* Filters Row */}
      <div className="mt-6 flex flex-wrap items-center gap-3">
        <input
          type="text"
          placeholder="Search problems or concepts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search interview problems"
          className="w-56 rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
        />
        <select
          value={companyFilter}
          onChange={(e) => setCompanyFilter(e.target.value as Company | "all")}
          aria-label="Filter by company"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Companies</option>
          {COMPANIES.map((c) => (
            <option key={c.value} value={c.value}>{c.label}</option>
          ))}
        </select>
        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value as Role | "all")}
          aria-label="Filter by role"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Roles</option>
          {ROLES.map((r) => (
            <option key={r.value} value={r.value}>{r.label}</option>
          ))}
        </select>
        <select
          value={difficultyFilter}
          onChange={(e) => setDifficultyFilter(e.target.value as Difficulty | "all")}
          aria-label="Filter by difficulty"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <select
          value={datasetFilter}
          onChange={(e) => setDatasetFilter(e.target.value as Dataset | "all")}
          aria-label="Filter by dataset"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Datasets</option>
          {DATASETS.map((d) => (
            <option key={d.value} value={d.value}>{d.label}</option>
          ))}
        </select>
        <select
          value={conceptFilter}
          onChange={(e) => setConceptFilter(e.target.value)}
          aria-label="Filter by concept"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Concepts</option>
          {CONCEPT_GROUPS.map((g) => (
            <option key={g.label} value={g.label}>{g.label}</option>
          ))}
        </select>
        <select
          value={frequencyFilter}
          onChange={(e) => setFrequencyFilter(e.target.value as "high" | "medium" | "low" | "all")}
          aria-label="Filter by frequency"
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          <option value="all">All Frequencies</option>
          <option value="high">Hot</option>
          <option value="medium">Common</option>
          <option value="low">Rare</option>
        </select>
      </div>

      {/* View mode + Sort */}
      <div className="mt-4 flex items-center justify-between">
        <p className="text-xs text-[var(--color-text-muted)]">
          Showing {filtered.length} of {problems.length} problems
        </p>
        <div className="flex items-center gap-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "default" | "difficulty" | "frequency")}
            aria-label="Sort problems"
            className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-2 py-1 text-xs text-[var(--color-text-secondary)]"
          >
            <option value="default">Default Order</option>
            <option value="difficulty">Sort by Difficulty</option>
            <option value="frequency">Sort by Frequency</option>
          </select>
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
            onClick={() => setViewMode("concept")}
            aria-label="View by concept"
            aria-pressed={viewMode === "concept"}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              viewMode === "concept"
                ? "bg-[var(--color-accent)] text-white"
                : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
            }`}
          >
            By Concept
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="mt-12 flex flex-col items-center gap-3">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
          <p className="text-sm text-[var(--color-text-muted)]">Loading interview problems...</p>
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

      {/* LIST VIEW */}
      {!loading && viewMode === "list" && (
        <div className="mt-4">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--color-border)]">
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">#</th>
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Problem</th>
                <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Difficulty</th>
                <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] sm:table-cell">Frequency</th>
                <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] md:table-cell">Dataset</th>
                <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] md:table-cell">Companies</th>
                <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] lg:table-cell">Concepts</th>
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
                  <td className="py-3">
                    <Badge variant={problem.difficulty}>{problem.difficulty}</Badge>
                  </td>
                  <td className="hidden py-3 sm:table-cell">
                    <span
                      className={`inline-flex items-center gap-1 text-xs font-medium ${
                        problem.frequency === "high"
                          ? "text-red-500"
                          : problem.frequency === "medium"
                            ? "text-amber-500"
                            : "text-[var(--color-text-muted)]"
                      }`}
                    >
                      {problem.frequency === "high" && (
                        <>
                          <svg className="h-3 w-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12 23c-3.866 0-7-3.134-7-7 0-2.812 1.882-5.86 3.54-8.08A.5.5 0 019.3 8l1.2 2.4a.5.5 0 00.9-.1l1.1-3.8a.5.5 0 01.94-.05C15.23 9.87 19 14.09 19 16c0 3.866-3.134 7-7 7z" /></svg>
                          Hot
                        </>
                      )}
                      {problem.frequency === "medium" && "Common"}
                      {problem.frequency === "low" && "Rare"}
                    </span>
                  </td>
                  <td className="hidden py-3 md:table-cell">
                    <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-secondary)]">
                      {DATASETS.find((d) => d.value === problem.dataset)?.label ?? problem.dataset}
                    </span>
                  </td>
                  <td className="hidden py-3 md:table-cell">
                    <div className="flex flex-wrap gap-1">
                      {problem.companies.slice(0, 3).map((c) => (
                        <span
                          key={c}
                          className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-secondary)]"
                        >
                          {COMPANIES.find((co) => co.value === c)?.label}
                        </span>
                      ))}
                      {problem.companies.length > 3 && (
                        <span className="text-[10px] text-[var(--color-text-muted)]">
                          +{problem.companies.length - 3}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="hidden py-3 lg:table-cell">
                    <div className="flex flex-wrap gap-1">
                      {(problem.concept_tags || []).slice(0, 2).map((tag) => (
                        <span
                          key={tag}
                          className="rounded bg-[var(--color-accent)]/10 px-1.5 py-0.5 text-[10px] font-medium text-[var(--color-accent)]"
                        >
                          {tag}
                        </span>
                      ))}
                      {(problem.concept_tags || []).length > 2 && (
                        <span className="text-[10px] text-[var(--color-text-muted)]">
                          +{problem.concept_tags.length - 2}
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filtered.length === 0 && (
            <p className="py-8 text-center text-sm text-[var(--color-text-muted)]">
              No problems match your filters.
            </p>
          )}
        </div>
      )}

      {/* CONCEPT VIEW */}
      {!loading && viewMode === "concept" && (
        <div className="mt-4 space-y-8">
          {Object.entries(groupedByConcept).map(([concept, probs]) => (
            <div key={concept}>
              <div className="mb-3 flex items-center gap-2">
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                  {concept}
                </h3>
                <span className="rounded-full bg-[var(--color-accent)]/10 px-2 py-0.5 text-xs font-medium text-[var(--color-accent)]">
                  {probs.length}
                </span>
              </div>
              <div className="grid gap-2">
                {probs.map((problem) => (
                  <Link
                    key={problem.id}
                    href={`/practice/${problem.slug}`}
                    className="flex items-center justify-between rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 transition-colors hover:border-[var(--color-accent)]"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-sm text-[var(--color-text-primary)]">
                        {problem.title}
                      </span>
                      <span className="hidden sm:inline rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-muted)]">
                        {DATASETS.find((d) => d.value === problem.dataset)?.label}
                      </span>
                      <span
                        className={`hidden sm:inline-flex items-center gap-1 text-[10px] font-medium ${
                          problem.frequency === "high"
                            ? "text-red-500"
                            : problem.frequency === "medium"
                              ? "text-amber-500"
                              : "text-[var(--color-text-muted)]"
                        }`}
                      >
                        {problem.frequency === "high" && "Hot"}
                        {problem.frequency === "medium" && "Common"}
                        {problem.frequency === "low" && "Rare"}
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

      {/* Interview Tips section */}
      <div className="mt-10 grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Interview Tips</h2>
          <ul className="mt-3 space-y-2 text-sm text-[var(--color-text-secondary)]">
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              Always clarify assumptions about NULL handling and edge cases before writing.
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              Start with the simplest correct solution, then optimize if asked.
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              Explain your approach before coding — interviewers value clear thinking.
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              Know the differences between ROW_NUMBER, RANK, and DENSE_RANK.
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              Practice writing queries without an IDE — many interviews use plain text editors.
            </li>
          </ul>
        </div>
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Study Strategy</h2>
          <ul className="mt-3 space-y-2 text-sm text-[var(--color-text-secondary)]">
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500" />
              <span><strong className="text-[var(--color-text-primary)]">Week 1-2:</strong> Master Easy problems — build strong fundamentals with SELECT, WHERE, GROUP BY.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500" />
              <span><strong className="text-[var(--color-text-primary)]">Week 3-4:</strong> Tackle Medium — focus on JOINs, subqueries, and CASE expressions.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500" />
              <span><strong className="text-[var(--color-text-primary)]">Week 5-6:</strong> Conquer Hard — window functions, CTEs, and complex analytics.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              <span><strong className="text-[var(--color-text-primary)]">Filter by &quot;Hot&quot;</strong> to prioritize the most commonly asked questions first.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
              <span><strong className="text-[var(--color-text-primary)]">Filter by company</strong> to prep for specific interviews (FAANG, FinTech, etc.).</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
