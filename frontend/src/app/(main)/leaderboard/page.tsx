"use client";

import { useUserStore } from "@/stores/useUserStore";

/* ------------------------------------------------------------------ */
/*  Stats card component                                               */
/* ------------------------------------------------------------------ */

function StatCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string | number;
  accent?: boolean;
}) {
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-center">
      <p
        className={`text-2xl font-bold ${
          accent ? "text-[var(--color-accent)]" : "text-[var(--color-text-primary)]"
        }`}
      >
        {value}
      </p>
      <p className="mt-1 text-xs text-[var(--color-text-muted)]">{label}</p>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

export default function LeaderboardPage() {
  const { xp, level, streak, solvedProblems, totalSolves, acceptanceRate } =
    useUserStore();

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Leaderboard</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          Track your SQL mastery. Community rankings coming soon.
        </p>
      </div>

      {/* Your stats */}
      <div className="mt-8">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Your Progress
        </h2>
        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
          <StatCard label="Level" value={level} />
          <StatCard label="Total XP" value={xp.toLocaleString()} accent />
          <StatCard label="Problems Solved" value={solvedProblems.length} />
          <StatCard
            label="Day Streak"
            value={streak > 0 ? `${streak}` : "—"}
          />
          <StatCard
            label="Acceptance Rate"
            value={totalSolves > 0 ? `${acceptanceRate}%` : "—"}
          />
        </div>
      </div>

      {/* Coming soon */}
      <div className="mt-12 flex flex-col items-center rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-16 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-accent)]/10">
          <svg
            className="h-7 w-7 text-[var(--color-accent)]"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-4.5A3.375 3.375 0 0012.75 11h-.5A3.375 3.375 0 009 14.25v4.5m7.5-10.5a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </div>
        <h3 className="mt-4 text-lg font-semibold text-[var(--color-text-primary)]">
          Community Rankings Coming Soon
        </h3>
        <p className="mt-2 max-w-md text-sm text-[var(--color-text-secondary)]">
          We&apos;re building a real-time leaderboard where you can compete with
          other SQL practitioners. Your progress is being tracked — you&apos;ll
          be ranked automatically once it launches.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3 text-xs text-[var(--color-text-muted)]">
          <span className="rounded-full border border-[var(--color-border)] px-3 py-1">
            Global rankings
          </span>
          <span className="rounded-full border border-[var(--color-border)] px-3 py-1">
            Weekly challenges
          </span>
          <span className="rounded-full border border-[var(--color-border)] px-3 py-1">
            Category leaders
          </span>
          <span className="rounded-full border border-[var(--color-border)] px-3 py-1">
            Streak champions
          </span>
        </div>
      </div>
    </div>
  );
}
