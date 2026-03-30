/**
 * Static problem data — embedded at build time so the practice arena,
 * interview simulator, and profile pages work without a live backend.
 * Only query execution requires the backend.
 */

import problemsData from "@/data/problems.json";

export interface ProblemListItem {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  category: string;
  dataset: string;
  concept_tags: string[];
}

export interface ProblemDetail extends ProblemListItem {
  description: string;
  schema_hint: string[];
  hints: string[];
  explanation: string;
  approach: string | string[];
  common_mistakes: string[];
}

const problems = problemsData.problems as ProblemDetail[];

/** Get all problems (optionally filtered). */
export function getAllProblems(filters?: {
  dataset?: string;
  difficulty?: string;
  category?: string;
}): ProblemDetail[] {
  if (!filters) return problems;
  return problems.filter((p) => {
    if (filters.dataset && p.dataset !== filters.dataset) return false;
    if (filters.difficulty && p.difficulty !== filters.difficulty) return false;
    if (filters.category && p.category !== filters.category) return false;
    return true;
  });
}

/** Get a single problem by slug. */
export function getProblemBySlug(slug: string): ProblemDetail | undefined {
  return problems.find((p) => p.slug === slug);
}

/** Get total count. */
export function getProblemCount(): number {
  return problems.length;
}
