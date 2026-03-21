"use client";

import { useMemo, memo } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { useUserStore } from "@/stores/useUserStore";
import type { Difficulty } from "@/types";

interface Problem {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  dataset: string;
  concept_tags: string[];
}

interface NextProblemRecommenderProps {
  problems: Problem[];
  currentProblemId: string;
  currentDifficulty: Difficulty;
  currentConceptTags: string[];
}

const DIFFICULTY_ORDER: Difficulty[] = ["easy", "medium", "hard"];

export const NextProblemRecommender = memo(function NextProblemRecommender({
  problems,
  currentProblemId,
  currentDifficulty,
  currentConceptTags,
}: NextProblemRecommenderProps) {
  const solvedProblems = useUserStore((s) => s.solvedProblems);
  const acceptanceHistory = useUserStore((s) => s.acceptanceHistory);

  const recommendations = useMemo(() => {
    const unsolved = problems.filter(
      (p) => p.id !== currentProblemId && !solvedProblems.includes(p.id)
    );

    if (unsolved.length === 0) return [];

    // Calculate acceptance rate
    const rate = acceptanceHistory.total > 0
      ? acceptanceHistory.correct / acceptanceHistory.total
      : 0.5;

    // Determine recommended difficulty
    const currentIdx = DIFFICULTY_ORDER.indexOf(currentDifficulty);
    let recommendedDifficulty: Difficulty;
    if (rate >= 0.7 && currentIdx < 2) {
      // Doing well — suggest harder
      recommendedDifficulty = DIFFICULTY_ORDER[currentIdx + 1];
    } else if (rate < 0.3 && currentIdx > 0) {
      // Struggling — suggest easier
      recommendedDifficulty = DIFFICULTY_ORDER[currentIdx - 1];
    } else {
      // Stay at current level
      recommendedDifficulty = currentDifficulty;
    }

    // Score each problem
    const scored = unsolved.map((p) => {
      let score = 0;

      // Same difficulty as recommended = high score
      if (p.difficulty === recommendedDifficulty) score += 10;
      // Same difficulty as current = decent score
      else if (p.difficulty === currentDifficulty) score += 5;

      // Shared concept tags boost score (practice same concepts)
      const sharedTags = p.concept_tags.filter((t) =>
        currentConceptTags.some((ct) => ct.toLowerCase() === t.toLowerCase())
      ).length;
      score += sharedTags * 3;

      // Same dataset gets a small boost
      if (p.dataset === problems.find((pr) => pr.id === currentProblemId)?.dataset) {
        score += 2;
      }

      return { ...p, score };
    });

    // Sort by score descending, take top 3
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 3);
  }, [problems, currentProblemId, currentDifficulty, currentConceptTags, solvedProblems, acceptanceHistory]);

  if (recommendations.length === 0) return null;

  // Label based on acceptance rate
  const rate = acceptanceHistory.total > 0
    ? acceptanceHistory.correct / acceptanceHistory.total
    : 0.5;
  const label = rate >= 0.7 ? "Ready for a challenge" : rate < 0.3 ? "Build your foundation" : "Keep practicing";

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <svg className="h-4 w-4 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
        </svg>
        <h4 className="text-xs font-semibold text-[var(--color-text-primary)]">
          Up Next: {label}
        </h4>
      </div>
      {recommendations.map((p) => (
        <Link
          key={p.id}
          href={`/practice/${p.slug}`}
          className="flex items-center justify-between rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 transition-colors hover:border-[var(--color-accent)]/40"
        >
          <span className="text-xs font-medium text-[var(--color-text-primary)]">
            {p.title}
          </span>
          <Badge variant={p.difficulty}>{p.difficulty}</Badge>
        </Link>
      ))}
    </div>
  );
});
