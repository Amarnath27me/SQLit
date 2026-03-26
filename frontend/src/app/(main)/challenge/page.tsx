"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import Link from "next/link";
import { useUserStore } from "@/stores/useUserStore";

/* ── Timer-based SQL challenge mode ── */

interface Challenge {
  id: string;
  title: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
  timeLimit: number; // seconds
  dataset: string;
  problemSlugs: string[];
}

const CHALLENGES: Challenge[] = [
  {
    id: "speed-1",
    title: "SELECT Sprint",
    description: "Solve 5 basic SELECT problems as fast as you can. Perfect for warming up.",
    difficulty: "easy",
    timeLimit: 300,
    dataset: "ecommerce",
    problemSlugs: [
      "list-all-products",
      "customers-from-a-specific-state",
      "high-value-completed-orders",
      "products-in-a-price-range",
      "search-products-by-name",
    ],
  },
  {
    id: "agg-rush",
    title: "Aggregation Rush",
    description: "5 aggregation problems. GROUP BY, HAVING, COUNT — can you beat the clock?",
    difficulty: "medium",
    timeLimit: 600,
    dataset: "ecommerce",
    problemSlugs: [
      "total-number-of-orders",
      "total-revenue-by-category",
      "average-order-value",
      "orders-per-customer",
      "highest-and-lowest-priced-products",
    ],
  },
  {
    id: "join-gauntlet",
    title: "Join Gauntlet",
    description: "5 JOIN problems of increasing difficulty. Inner, left, multi-table — show your skills.",
    difficulty: "medium",
    timeLimit: 900,
    dataset: "ecommerce",
    problemSlugs: [
      "order-details-with-customer-name",
      "products-with-category-names",
      "customers-who-never-ordered",
      "order-items-with-full-details",
      "customer-order-summary",
    ],
  },
  {
    id: "finance-blitz",
    title: "Finance Blitz",
    description: "5 finance problems across different categories. Banking data, tight deadline.",
    difficulty: "medium",
    timeLimit: 600,
    dataset: "finance",
    problemSlugs: [
      "list-all-branches",
      "customers-in-california",
      "high-balance-active-accounts",
      "total-deposits-by-branch",
      "average-account-balance",
    ],
  },
  {
    id: "hard-mode",
    title: "Expert Challenge",
    description: "5 hard problems: window functions, CTEs, correlated subqueries. Only for the brave.",
    difficulty: "hard",
    timeLimit: 1200,
    dataset: "ecommerce",
    problemSlugs: [
      "customers-who-reviewed-their-purchases",
      "customers-who-ordered-from-every-category",
      "products-ordered-but-never-reviewed",
      "orders-above-customers-own-average",
      "revenue-ranking-by-category",
    ],
  },
];

const diffColors = {
  easy: "bg-green-500/20 text-green-400 border-green-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  hard: "bg-red-500/20 text-red-400 border-red-500/30",
};

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function ChallengePage() {
  const markSolved = useUserStore((s) => s.markSolved);
  const saveSolveToBackend = useUserStore((s) => s.saveSolveToBackend);
  const [activeChallenge, setActiveChallenge] = useState<Challenge | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);
  const [solved, setSolved] = useState<boolean[]>([]);
  const [started, setStarted] = useState(false);
  const [finished, setFinished] = useState(false);
  const restored = useRef(false);

  // Restore challenge state from sessionStorage on mount
  useEffect(() => {
    if (restored.current) return;
    restored.current = true;
    try {
      const saved = sessionStorage.getItem("sqlit-challenge");
      if (!saved) return;
      const s = JSON.parse(saved);
      const challenge = CHALLENGES.find((c) => c.id === s.challengeId);
      if (challenge && s.timeLeft > 0 && !s.finished) {
        setActiveChallenge(challenge);
        setCurrentIndex(s.currentIndex || 0);
        setTimeLeft(s.timeLeft);
        setSolved(s.solved || []);
        setStarted(true);
        setFinished(false);
      }
    } catch { /* ignore corrupt data */ }
  }, []);

  // Persist challenge state to sessionStorage
  useEffect(() => {
    if (!activeChallenge || !started) return;
    try {
      sessionStorage.setItem("sqlit-challenge", JSON.stringify({
        challengeId: activeChallenge.id,
        currentIndex,
        timeLeft,
        solved,
        finished,
      }));
    } catch { /* quota exceeded */ }
  }, [activeChallenge, currentIndex, timeLeft, solved, started, finished]);

  useEffect(() => {
    if (!started || finished || timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          setFinished(true);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [started, finished, timeLeft]);

  const startChallenge = useCallback((challenge: Challenge) => {
    setActiveChallenge(challenge);
    setCurrentIndex(0);
    setTimeLeft(challenge.timeLimit);
    setSolved(new Array(challenge.problemSlugs.length).fill(false));
    setStarted(true);
    setFinished(false);
  }, []);

  const solvedCount = solved.filter(Boolean).length;

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
        Challenge Mode
      </h1>
      <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
        Race against the clock. Solve SQL problems under time pressure to test your speed and accuracy.
      </p>

      {!activeChallenge ? (
        /* Challenge selection */
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {CHALLENGES.map((c) => (
            <button
              key={c.id}
              onClick={() => startChallenge(c)}
              className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5 text-left transition-all hover:border-[var(--color-accent)]/50 hover:shadow-lg"
            >
              <div className="mb-3 flex items-center gap-2">
                <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${diffColors[c.difficulty]}`}>
                  {c.difficulty}
                </span>
                <span className="text-[10px] text-[var(--color-text-muted)]">
                  {formatTime(c.timeLimit)}
                </span>
              </div>
              <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                {c.title}
              </h3>
              <p className="mt-1 text-xs text-[var(--color-text-muted)]">
                {c.description}
              </p>
              <div className="mt-3 flex items-center gap-2 text-[10px] text-[var(--color-text-muted)]">
                <span>{c.problemSlugs.length} problems</span>
                <span>•</span>
                <span className="capitalize">{c.dataset}</span>
              </div>
            </button>
          ))}
        </div>
      ) : (
        /* Active challenge */
        <div className="mt-6">
          <div className="mb-4 flex items-center justify-between">
            <button
              onClick={() => { sessionStorage.removeItem("sqlit-challenge"); setActiveChallenge(null); setStarted(false); setFinished(false); }}
              className="text-xs font-medium text-[var(--color-accent)] hover:underline"
            >
              ← Exit challenge
            </button>
            <div className="flex items-center gap-4">
              <span className="text-xs text-[var(--color-text-muted)]">
                {solvedCount}/{activeChallenge.problemSlugs.length} solved
              </span>
              <span className={`rounded-md px-3 py-1 font-mono text-sm font-bold ${
                timeLeft < 60 ? "bg-red-500/20 text-red-400" : "bg-[var(--color-surface)] text-[var(--color-text-primary)]"
              }`}>
                {formatTime(timeLeft)}
              </span>
            </div>
          </div>

          {/* Progress dots */}
          <div className="mb-6 flex items-center gap-2">
            {activeChallenge.problemSlugs.map((slug, i) => (
              <button
                key={slug}
                onClick={() => setCurrentIndex(i)}
                className={`h-3 w-3 rounded-full border transition-all ${
                  solved[i]
                    ? "border-green-500 bg-green-500"
                    : i === currentIndex
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]"
                    : "border-[var(--color-border)] bg-transparent"
                }`}
              />
            ))}
          </div>

          {finished ? (
            /* Results */
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-8 text-center">
              <div className="text-4xl">{solvedCount === activeChallenge.problemSlugs.length ? "🏆" : "⏰"}</div>
              <h2 className="mt-4 text-xl font-bold text-[var(--color-text-primary)]">
                {solvedCount === activeChallenge.problemSlugs.length ? "Challenge Complete!" : "Time's Up!"}
              </h2>
              <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
                You solved {solvedCount} of {activeChallenge.problemSlugs.length} problems
              </p>
              <div className="mt-4 flex justify-center gap-4">
                <button
                  onClick={() => startChallenge(activeChallenge)}
                  className="rounded-md bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white"
                >
                  Retry
                </button>
                <button
                  onClick={() => { sessionStorage.removeItem("sqlit-challenge"); setActiveChallenge(null); setStarted(false); setFinished(false); }}
                  className="rounded-md border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)]"
                >
                  Back to challenges
                </button>
              </div>
            </div>
          ) : (
            /* Current problem link */
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
              <p className="mb-2 text-xs text-[var(--color-text-muted)]">
                Problem {currentIndex + 1} of {activeChallenge.problemSlugs.length}
              </p>
              <Link
                href={`/practice/${activeChallenge.problemSlugs[currentIndex]}`}
                className="text-lg font-semibold text-[var(--color-accent)] hover:underline"
              >
                Open Problem →
              </Link>
              <div className="mt-4 flex gap-2">
                <button
                  onClick={() => {
                    const slug = activeChallenge.problemSlugs[currentIndex];
                    const next = [...solved];
                    next[currentIndex] = true;
                    setSolved(next);
                    // Sync solve to store and backend
                    markSolved(slug);
                    const xp = activeChallenge.difficulty === "easy" ? 10 : activeChallenge.difficulty === "medium" ? 20 : 30;
                    saveSolveToBackend(slug, xp);
                    if (currentIndex < activeChallenge.problemSlugs.length - 1) {
                      setCurrentIndex(currentIndex + 1);
                    } else {
                      setFinished(true);
                    }
                  }}
                  className="rounded-md bg-green-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                >
                  Mark Solved & Next
                </button>
                <button
                  onClick={() => {
                    if (currentIndex < activeChallenge.problemSlugs.length - 1)
                      setCurrentIndex(currentIndex + 1);
                  }}
                  className="rounded-md border border-[var(--color-border)] px-3 py-1.5 text-xs font-medium text-[var(--color-text-secondary)]"
                >
                  Skip
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
