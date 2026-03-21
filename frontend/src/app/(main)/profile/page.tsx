"use client";

import { useMemo, useState, useEffect } from "react";
import Link from "next/link";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useUserStore } from "@/stores/useUserStore";
import { Badge } from "@/components/ui/Badge";
import { ConceptBadges } from "@/components/profile/ConceptBadges";
import { ActivityHeatmap } from "@/components/profile/ActivityHeatmap";

/* ------------------------------------------------------------------ */
/*  XP helpers                                                         */
/* ------------------------------------------------------------------ */

function xpForLevel(level: number): number {
  let xp = 100;
  for (let i = 1; i < level; i++) xp = Math.floor(xp * 1.3);
  return xp;
}

function xpProgress(totalXP: number): { current: number; needed: number; pct: number } {
  let remaining = totalXP;
  let needed = 100;
  while (remaining >= needed) {
    remaining -= needed;
    needed = Math.floor(needed * 1.3);
  }
  return { current: remaining, needed, pct: Math.round((remaining / needed) * 100) };
}

/* ------------------------------------------------------------------ */
/*  Concept badges                                                     */
/* ------------------------------------------------------------------ */

const CONCEPT_BADGES = [
  { id: "select-master", name: "SELECT Master", desc: "Solve 10 SELECT problems", icon: "S", threshold: 10, category: "select" },
  { id: "agg-guru", name: "Aggregation Guru", desc: "Solve 10 aggregation problems", icon: "A", threshold: 10, category: "aggregation" },
  { id: "join-expert", name: "Join Expert", desc: "Solve 10 join problems", icon: "J", threshold: 10, category: "joins" },
  { id: "subquery-sage", name: "Subquery Sage", desc: "Solve 10 subquery problems", icon: "Q", threshold: 10, category: "subqueries" },
  { id: "window-wizard", name: "Window Wizard", desc: "Solve 10 window function problems", icon: "W", threshold: 10, category: "window-functions" },
  { id: "cte-champion", name: "CTE Champion", desc: "Solve 5 CTE problems", icon: "C", threshold: 5, category: "cte" },
  { id: "streak-3", name: "On Fire", desc: "Maintain a 3-day streak", icon: "3", threshold: 3, category: "_streak" },
  { id: "streak-7", name: "Week Warrior", desc: "Maintain a 7-day streak", icon: "7", threshold: 7, category: "_streak" },
  { id: "first-solve", name: "First Blood", desc: "Solve your first problem", icon: "1", threshold: 1, category: "_total" },
  { id: "fifty-club", name: "Fifty Club", desc: "Solve 50 problems", icon: "50", threshold: 50, category: "_total" },
];

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

export default function ProfilePage() {
  const { user } = useUser();
  const { displayName, xp, level, streak, solvedProblems, avatar } = useUserStore();
  const progress = xpProgress(xp);
  const solved = solvedProblems.length;
  const name = user?.name || displayName;
  const picture = user?.picture || avatar;

  // Generate activity data client-side only to avoid SSR hydration mismatch
  const [activityData, setActivityData] = useState<Record<string, number>>({});
  useEffect(() => {
    const data: Record<string, number> = {};
    const today = new Date();
    for (let i = 0; i < 365; i++) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split("T")[0];
      const hash = ((i * 2654435761) >>> 0) % 100;
      const recencyBoost = Math.max(0, 1 - i / 365);
      const threshold = 30 * recencyBoost + 5;
      if (hash < threshold) {
        data[dateStr] = (hash % 6) + 1;
      }
    }
    setActivityData(data);
  }, []);

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/10 text-2xl font-bold text-[var(--color-accent)] overflow-hidden">
            {picture ? (
              <img src={picture} alt={name} className="h-full w-full rounded-full object-cover" />
            ) : (
              name.charAt(0).toUpperCase()
            )}
          </div>
          <div>
            <h1 className="text-2xl font-bold">{name}</h1>
            <p className="text-sm text-[var(--color-text-secondary)]">
              Level {level} &middot; {solved} problems solved
            </p>
          </div>
        </div>
        <Link
          href="/settings"
          className="rounded-lg border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
        >
          Edit Profile
        </Link>
      </div>

      {/* Stats cards */}
      <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
        {[
          { label: "Total XP", value: xp.toLocaleString(), color: "text-[var(--color-accent)]" },
          { label: "Level", value: level.toString(), color: "text-purple-500" },
          { label: "Streak", value: `${streak} day${streak !== 1 ? "s" : ""}`, color: "text-orange-500" },
          { label: "Solved", value: solved.toString(), color: "text-emerald-500" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
          >
            <p className="text-xs font-medium text-[var(--color-text-muted)]">{stat.label}</p>
            <p className={`mt-1 text-2xl font-bold ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      {/* XP Progress bar */}
      <div className="mt-6 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-[var(--color-text-primary)]">Level {level} Progress</span>
          <span className="text-[var(--color-text-muted)]">
            {progress.current} / {progress.needed} XP
          </span>
        </div>
        <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--color-border)]">
          <div
            className="h-full rounded-full bg-[var(--color-accent)] transition-all duration-500"
            style={{ width: `${progress.pct}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-[var(--color-text-muted)]">
          {progress.needed - progress.current} XP to Level {level + 1}
        </p>
      </div>

      {/* Activity Heatmap */}
      <div className="mt-8">
        <ActivityHeatmap data={activityData} />
      </div>

      {/* Concept Mastery Badges */}
      <div className="mt-8 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
        <ConceptBadges
          badges={[
            { concept: "SELECT Basics", solved: 12, total: 15, icon: "📋" },
            { concept: "WHERE Clauses", solved: 10, total: 15, icon: "🔍" },
            { concept: "Aggregations", solved: 8, total: 15, icon: "📊" },
            { concept: "JOINs", solved: 14, total: 20, icon: "🔗" },
            { concept: "Subqueries", solved: 5, total: 15, icon: "🎯" },
            { concept: "Window Functions", solved: 7, total: 15, icon: "🪟" },
            { concept: "CTEs", solved: 3, total: 10, icon: "🔄" },
            { concept: "Advanced", solved: 2, total: 20, icon: "⚡" },
          ]}
        />
      </div>

      {/* Badges */}
      <div className="mt-8">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">Badges</h2>
        <p className="mt-1 text-sm text-[var(--color-text-muted)]">
          Earn badges by mastering SQL concepts and maintaining streaks.
        </p>
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {CONCEPT_BADGES.map((badge) => {
            const unlocked =
              badge.category === "_streak"
                ? streak >= badge.threshold
                : badge.category === "_total"
                  ? solved >= badge.threshold
                  : false; // would check per-category solved count with backend data

            return (
              <div
                key={badge.id}
                className={`rounded-lg border p-4 text-center transition-colors ${
                  unlocked
                    ? "border-[var(--color-accent)]/40 bg-[var(--color-accent)]/5"
                    : "border-[var(--color-border)] bg-[var(--color-surface)] opacity-50"
                }`}
              >
                <div
                  className={`mx-auto flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold ${
                    unlocked
                      ? "bg-[var(--color-accent)] text-white"
                      : "bg-[var(--color-border)] text-[var(--color-text-muted)]"
                  }`}
                >
                  {badge.icon}
                </div>
                <p className="mt-2 text-xs font-semibold text-[var(--color-text-primary)]">{badge.name}</p>
                <p className="mt-0.5 text-[10px] text-[var(--color-text-muted)]">{badge.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Solved (placeholder) */}
      <div className="mt-8 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
        <h2 className="mb-4 text-sm font-semibold text-[var(--color-text-primary)]">Recently Solved</h2>
        {solved === 0 ? (
          <div className="py-8 text-center">
            <p className="text-sm text-[var(--color-text-muted)]">No problems solved yet.</p>
            <Link
              href="/practice"
              className="mt-3 inline-block rounded-lg bg-[var(--color-accent)] px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
            >
              Start Practicing
            </Link>
          </div>
        ) : (
          <p className="text-sm text-[var(--color-text-muted)]">
            You&apos;ve solved {solved} problem{solved !== 1 ? "s" : ""}. Keep going!
          </p>
        )}
      </div>
    </div>
  );
}
