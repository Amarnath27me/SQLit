"use client";

import { useState, useMemo } from "react";

/* ------------------------------------------------------------------ */
/*  Types & mock data                                                  */
/* ------------------------------------------------------------------ */

interface LeaderboardEntry {
  rank: number;
  displayName: string;
  level: number;
  xp: number;
  solved: number;
  streak: number;
  topCategory: string;
}

type TimeRange = "all-time" | "weekly" | "monthly";
type SortBy = "xp" | "solved" | "streak" | "level";

// Mock leaderboard data — will be replaced with API calls
// Seeded pseudo-random to avoid hydration mismatch
function seeded(i: number) {
  return ((i * 9301 + 49297) % 233280) / 233280;
}

const MOCK_ENTRIES: LeaderboardEntry[] = Array.from({ length: 50 }, (_, i) => ({
  rank: i + 1,
  displayName: [
    "DataWizard", "SQLNinja", "QueryMaster", "JoinHero", "IndexPro",
    "AggKing", "SubqueryAce", "CTELord", "WindowFan", "TableTamer",
    "NullHunter", "SchemaGuru", "PivotPro", "UnionBoss", "GroupByGod",
    "HavingHero", "OrderPrince", "LimitLord", "DistinctDuke", "SelectSage",
    "FromFanatic", "WhereMaster", "JoinJunkie", "AggAddict", "CTECrusader",
    "WindowWarrior", "SQLSensei", "DataDiver", "QueryQueen", "JoinJester",
    "CodeCrafter", "ByteBoss", "PixelPusher", "LogicLord", "AlgoAce",
    "BugBuster", "SyntaxStar", "DevDynamo", "HashHero", "StackSage",
    "TreeTamer", "GraphGuru", "CacheCaptain", "LoopLord", "BitBaron",
    "RecurseRanger", "MergeMaster", "SortSovereign", "ParsePro", "CompileKing",
  ][i],
  level: Math.max(1, 20 - Math.floor(i * 0.35)),
  xp: Math.max(50, 5000 - i * 85 + Math.floor(seeded(i) * 40)),
  solved: Math.max(3, 120 - i * 2 + Math.floor(seeded(i + 100) * 5)),
  streak: Math.max(0, 30 - i + Math.floor(seeded(i + 200) * 3)),
  topCategory: ["Joins", "Window Functions", "Aggregations", "CTEs", "Subqueries", "SELECT", "Advanced"][i % 7],
}));

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

export default function LeaderboardPage() {
  const [timeRange, setTimeRange] = useState<TimeRange>("all-time");
  const [sortBy, setSortBy] = useState<SortBy>("xp");

  const sorted = useMemo(() => {
    const copy = [...MOCK_ENTRIES];
    copy.sort((a, b) => {
      if (sortBy === "xp") return b.xp - a.xp;
      if (sortBy === "solved") return b.solved - a.solved;
      if (sortBy === "streak") return b.streak - a.streak;
      return b.level - a.level;
    });
    return copy.map((e, i) => ({ ...e, rank: i + 1 }));
  }, [sortBy]);

  const TIME_TABS: { value: TimeRange; label: string }[] = [
    { value: "all-time", label: "All Time" },
    { value: "weekly", label: "This Week" },
    { value: "monthly", label: "This Month" },
  ];

  const SORT_OPTIONS: { value: SortBy; label: string }[] = [
    { value: "xp", label: "XP" },
    { value: "solved", label: "Problems Solved" },
    { value: "streak", label: "Streak" },
    { value: "level", label: "Level" },
  ];

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Leaderboard</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          See how you rank against other SQL practitioners. Opt-in from settings.
        </p>
      </div>

      {/* Controls */}
      <div className="mt-6 flex flex-wrap items-center gap-3">
        {/* Time range tabs */}
        <div className="flex items-center rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-0.5">
          {TIME_TABS.map((tab) => (
            <button
              key={tab.value}
              onClick={() => setTimeRange(tab.value)}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                timeRange === tab.value
                  ? "bg-[var(--color-accent)] text-white"
                  : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Sort by */}
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as SortBy)}
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
        >
          {SORT_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              Sort by {opt.label}
            </option>
          ))}
        </select>
      </div>

      {/* Top 3 podium */}
      <div className="mt-8 grid grid-cols-3 gap-4">
        {sorted.slice(0, 3).map((entry, i) => {
          const colors = [
            "from-amber-400 to-amber-600",
            "from-gray-300 to-gray-500",
            "from-orange-400 to-orange-600",
          ];
          const sizes = ["h-20 w-20", "h-16 w-16", "h-16 w-16"];
          const order = [1, 0, 2]; // center 1st place
          return (
            <div
              key={entry.displayName}
              className="flex flex-col items-center rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6"
              style={{ order: order[i] }}
            >
              <div
                className={`flex ${sizes[i]} items-center justify-center rounded-full bg-gradient-to-br ${colors[i]} text-lg font-bold text-white`}
              >
                #{entry.rank}
              </div>
              <p className="mt-3 text-sm font-semibold text-[var(--color-text-primary)]">{entry.displayName}</p>
              <p className="mt-1 text-xs text-[var(--color-text-muted)]">Level {entry.level}</p>
              <p className="mt-2 text-lg font-bold text-[var(--color-accent)]">{entry.xp.toLocaleString()} XP</p>
              <p className="text-xs text-[var(--color-text-muted)]">{entry.solved} solved</p>
            </div>
          );
        })}
      </div>

      {/* Full table */}
      <div className="mt-8">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)]">
              <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Rank</th>
              <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">User</th>
              <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">Level</th>
              <th className="pb-3 text-xs font-medium text-[var(--color-text-muted)]">XP</th>
              <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] sm:table-cell">Solved</th>
              <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] md:table-cell">Streak</th>
              <th className="hidden pb-3 text-xs font-medium text-[var(--color-text-muted)] lg:table-cell">Top Category</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((entry) => (
              <tr
                key={entry.displayName}
                className="border-b border-[var(--color-border)] transition-colors hover:bg-[var(--color-surface)]"
              >
                <td className="py-3">
                  <span
                    className={`font-semibold ${
                      entry.rank <= 3 ? "text-amber-500" : "text-[var(--color-text-muted)]"
                    }`}
                  >
                    {entry.rank}
                  </span>
                </td>
                <td className="py-3">
                  <div className="flex items-center gap-2">
                    <div className="flex h-7 w-7 items-center justify-center rounded-full bg-[var(--color-accent)]/10 text-xs font-bold text-[var(--color-accent)]">
                      {entry.displayName.charAt(0)}
                    </div>
                    <span className="font-medium text-[var(--color-text-primary)]">{entry.displayName}</span>
                  </div>
                </td>
                <td className="py-3 text-[var(--color-text-secondary)]">{entry.level}</td>
                <td className="py-3 font-semibold text-[var(--color-accent)]">{entry.xp.toLocaleString()}</td>
                <td className="hidden py-3 text-[var(--color-text-secondary)] sm:table-cell">{entry.solved}</td>
                <td className="hidden py-3 md:table-cell">
                  {entry.streak > 0 ? (
                    <span className="inline-flex items-center gap-1 text-orange-500">
                      <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 23c-3.866 0-7-3.134-7-7 0-2.812 1.882-5.86 3.54-8.08A.5.5 0 019.3 8l1.2 2.4a.5.5 0 00.9-.1l1.1-3.8a.5.5 0 01.94-.05C15.23 9.87 19 14.09 19 16c0 3.866-3.134 7-7 7z" />
                      </svg>
                      {entry.streak}
                    </span>
                  ) : (
                    <span className="text-[var(--color-text-muted)]">-</span>
                  )}
                </td>
                <td className="hidden py-3 lg:table-cell">
                  <span className="rounded-full bg-[var(--color-background)] px-2 py-0.5 text-[10px] font-medium text-[var(--color-text-secondary)]">
                    {entry.topCategory}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
