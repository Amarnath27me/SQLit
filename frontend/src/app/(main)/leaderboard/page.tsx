"use client";

import { useEffect, useState } from "react";
import { useUserStore } from "@/stores/useUserStore";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface LeaderboardEntry {
  rank: number;
  display_name: string;
  xp: number;
  level: number;
  total_solved: number;
  streak: number;
}

/* ------------------------------------------------------------------ */
/*  Stats card                                                         */
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
/*  Rank badge                                                         */
/* ------------------------------------------------------------------ */

function RankBadge({ rank }: { rank: number }) {
  if (rank === 1) return <span className="text-lg">🥇</span>;
  if (rank === 2) return <span className="text-lg">🥈</span>;
  if (rank === 3) return <span className="text-lg">🥉</span>;
  return (
    <span className="text-sm font-medium text-[var(--color-text-muted)]">
      {rank}
    </span>
  );
}

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

export default function LeaderboardPage() {
  const { xp, level, streak, solvedProblems, totalSolves, acceptanceRate } =
    useUserStore();

  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/leaderboard")
      .then((res) => res.json())
      .then((data) => {
        setEntries(data.entries || []);
        setTotalUsers(data.total_users || 0);
      })
      .catch(() => setError("Failed to load leaderboard. Please try again later."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Leaderboard</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          Compete with other SQL practitioners.
          {totalUsers > 0 && ` ${totalUsers} active users.`}
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

      {/* Rankings table */}
      <div className="mt-10">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Global Rankings
        </h2>

        {loading ? (
          <div className="mt-6 flex justify-center py-12">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
          </div>
        ) : error ? (
          <div className="mt-6 rounded-xl border border-dashed border-red-500/30 bg-red-500/5 px-6 py-16 text-center">
            <p className="text-sm text-red-400">{error}</p>
          </div>
        ) : entries.length === 0 ? (
          <div className="mt-6 rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-16 text-center">
            <p className="text-sm text-[var(--color-text-secondary)]">
              No rankings yet. Solve problems to appear on the leaderboard!
            </p>
          </div>
        ) : (
          <div className="mt-4 overflow-hidden rounded-xl border border-[var(--color-border)]">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[var(--color-border)] bg-[var(--color-surface)]">
                  <th className="px-4 py-3 text-left font-medium text-[var(--color-text-muted)] w-16">
                    Rank
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-[var(--color-text-muted)]">
                    User
                  </th>
                  <th className="px-4 py-3 text-right font-medium text-[var(--color-text-muted)]">
                    XP
                  </th>
                  <th className="hidden px-4 py-3 text-right font-medium text-[var(--color-text-muted)] sm:table-cell">
                    Level
                  </th>
                  <th className="hidden px-4 py-3 text-right font-medium text-[var(--color-text-muted)] md:table-cell">
                    Solved
                  </th>
                  <th className="hidden px-4 py-3 text-right font-medium text-[var(--color-text-muted)] md:table-cell">
                    Streak
                  </th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry) => (
                  <tr
                    key={entry.rank}
                    className={`border-b border-[var(--color-border)] last:border-0 ${
                      entry.rank <= 3
                        ? "bg-[var(--color-accent)]/5"
                        : "bg-[var(--color-background)]"
                    }`}
                  >
                    <td className="px-4 py-3 text-center">
                      <RankBadge rank={entry.rank} />
                    </td>
                    <td className="px-4 py-3 font-medium text-[var(--color-text-primary)]">
                      {entry.display_name}
                    </td>
                    <td className="px-4 py-3 text-right font-semibold text-[var(--color-accent)]">
                      {entry.xp.toLocaleString()}
                    </td>
                    <td className="hidden px-4 py-3 text-right text-[var(--color-text-secondary)] sm:table-cell">
                      {entry.level}
                    </td>
                    <td className="hidden px-4 py-3 text-right text-[var(--color-text-secondary)] md:table-cell">
                      {entry.total_solved}
                    </td>
                    <td className="hidden px-4 py-3 text-right text-[var(--color-text-secondary)] md:table-cell">
                      {entry.streak > 0 ? `${entry.streak}d` : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
