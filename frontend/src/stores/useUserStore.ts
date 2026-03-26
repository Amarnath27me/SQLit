"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

/* ── Streak multiplier ──────────────────────────────────────── */
function getStreakMultiplier(streak: number): number {
  if (streak >= 30) return 2.0;
  if (streak >= 7) return 1.5;
  if (streak >= 3) return 1.2;
  return 1.0;
}

function isSameDay(d1: string, d2: string): boolean {
  return d1.slice(0, 10) === d2.slice(0, 10);
}

function isConsecutiveDay(prev: string, current: string): boolean {
  const p = new Date(prev);
  const c = new Date(current);
  p.setDate(p.getDate() + 1);
  return p.toISOString().slice(0, 10) === c.toISOString().slice(0, 10);
}

function computeLevel(xp: number): number {
  let level = 1;
  let xpNeeded = 100;
  let remaining = xp;
  while (remaining >= xpNeeded) {
    remaining -= xpNeeded;
    level++;
    xpNeeded = Math.floor(xpNeeded * 1.3);
  }
  return level;
}

interface UserState {
  isAuthenticated: boolean;
  displayName: string;
  email: string;
  avatar: string | null;
  auth0Id: string | null;
  xp: number;
  level: number;
  streak: number;
  lastSolveDate: string | null;
  solvedProblems: string[];
  totalSolves: number;
  acceptanceHistory: { correct: number; total: number };
  activityData: Record<string, number>; // date string → solve count
  notes: Record<string, string>; // problemId → note text
  flaggedProblems: string[]; // problem IDs flagged for review

  // Computed
  readonly acceptanceRate: number;

  // Actions
  addXP: (amount: number) => void;
  markSolved: (problemId: string) => void;
  recordAttempt: (correct: boolean) => void;
  setNote: (problemId: string, note: string) => void;
  toggleFlag: (problemId: string) => void;
  syncFromAuth0: (user: { name?: string; email?: string; picture?: string; sub?: string }) => void;
  syncFromBackend: () => Promise<void>;
  saveSolveToBackend: (problemId: string, xpEarned: number) => Promise<void>;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      displayName: "Guest",
      email: "",
      avatar: null,
      auth0Id: null,
      xp: 0,
      level: 1,
      streak: 0,
      lastSolveDate: null,
      solvedProblems: [],
      totalSolves: 0,
      acceptanceHistory: { correct: 0, total: 0 },
      activityData: {},
      notes: {},
      flaggedProblems: [],

      get acceptanceRate() {
        const { correct, total } = get().acceptanceHistory;
        return total > 0 ? Math.round((correct / total) * 100) : 0;
      },

      addXP: (amount) =>
        set((state) => {
          const multiplier = getStreakMultiplier(state.streak);
          const finalXP = Math.floor(amount * multiplier);
          const newXP = state.xp + finalXP;
          return { xp: newXP, level: computeLevel(newXP) };
        }),

      markSolved: (problemId) =>
        set((state) => {
          if (state.solvedProblems.includes(problemId)) return state;

          const now = new Date().toISOString();
          const todayStr = now.slice(0, 10);
          let newStreak = state.streak;

          if (!state.lastSolveDate) {
            newStreak = 1;
          } else if (isSameDay(state.lastSolveDate, now)) {
            // Same day, streak stays
          } else if (isConsecutiveDay(state.lastSolveDate, now)) {
            newStreak = state.streak + 1;
          } else {
            newStreak = 1;
          }

          // Update activity data
          const newActivity = { ...state.activityData };
          newActivity[todayStr] = (newActivity[todayStr] || 0) + 1;

          return {
            solvedProblems: [...state.solvedProblems, problemId],
            totalSolves: state.totalSolves + 1,
            streak: newStreak,
            lastSolveDate: now,
            activityData: newActivity,
          };
        }),

      recordAttempt: (correct) =>
        set((state) => ({
          acceptanceHistory: {
            correct: state.acceptanceHistory.correct + (correct ? 1 : 0),
            total: state.acceptanceHistory.total + 1,
          },
        })),

      setNote: (problemId, note) =>
        set((state) => {
          const newNotes = { ...state.notes };
          if (note.trim()) {
            newNotes[problemId] = note;
          } else {
            delete newNotes[problemId];
          }
          return { notes: newNotes };
        }),

      toggleFlag: (problemId) =>
        set((state) => ({
          flaggedProblems: state.flaggedProblems.includes(problemId)
            ? state.flaggedProblems.filter((id) => id !== problemId)
            : [...state.flaggedProblems, problemId],
        })),

      syncFromAuth0: (user) =>
        set({
          isAuthenticated: true,
          displayName: user.name || user.email || "User",
          email: user.email || "",
          avatar: user.picture || null,
          auth0Id: user.sub || null,
        }),

      syncFromBackend: async () => {
        try {
          const res = await fetch("/api/progress");
          if (!res.ok) return;
          const data = await res.json();

          const solves: { problem_id: string; solved_at: string }[] = data.solved || [];
          const backendSolvedIds = solves.map((s) => s.problem_id);

          // If backend has no data, keep localStorage data (don't wipe it)
          const local = get();
          if (backendSolvedIds.length === 0 && local.solvedProblems.length > 0) {
            // Backend is empty but we have local data — skip overwrite.
            // The local solves will be pushed to backend on next solve.
            return;
          }

          // Merge: use backend as source of truth, but keep any local solves
          // that haven't been synced yet
          const mergedSolvedIds = [...new Set([...backendSolvedIds, ...local.solvedProblems])];

          // Build activity data from solve timestamps
          const activity: Record<string, number> = { ...local.activityData };
          // Count backend solves per day
          const backendCounts: Record<string, number> = {};
          for (const s of solves) {
            if (s.solved_at) {
              const dateStr = s.solved_at.slice(0, 10);
              backendCounts[dateStr] = (backendCounts[dateStr] || 0) + 1;
            }
          }
          // Merge: take the higher of backend vs local for each day
          for (const [dateStr, count] of Object.entries(backendCounts)) {
            activity[dateStr] = Math.max(count, activity[dateStr] || 0);
          }

          // Use the higher value between backend and local for XP/streak
          const backendXP = data.xp ?? 0;
          const finalXP = Math.max(backendXP, local.xp);

          set({
            xp: finalXP,
            level: computeLevel(finalXP),
            streak: Math.max(data.streak ?? 0, local.streak),
            solvedProblems: mergedSolvedIds,
            totalSolves: mergedSolvedIds.length,
            lastSolveDate: data.last_solve_date || local.lastSolveDate,
            activityData: activity,
          });
        } catch {
          // Backend unavailable — keep localStorage data
        }
      },

      saveSolveToBackend: async (problemId, xpEarned) => {
        try {
          const res = await fetch("/api/progress/solve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              problem_id: problemId,
              xp_earned: xpEarned,
            }),
          });
          if (!res.ok) {
            console.warn("[SQLit] Failed to save solve to backend:", res.status);
          }
        } catch (err) {
          console.warn("[SQLit] Backend unavailable for save:", err);
        }
      },

      logout: () =>
        set({
          isAuthenticated: false,
          displayName: "Guest",
          email: "",
          avatar: null,
          auth0Id: null,
          // Keep progress data in localStorage — it will be synced
          // from backend on next login
        }),
    }),
    {
      name: "sqlit-user",
      partialize: (state) => ({
        xp: state.xp,
        level: state.level,
        streak: state.streak,
        lastSolveDate: state.lastSolveDate,
        solvedProblems: state.solvedProblems,
        totalSolves: state.totalSolves,
        acceptanceHistory: state.acceptanceHistory,
        activityData: state.activityData,
        notes: state.notes,
        flaggedProblems: state.flaggedProblems,
      }),
    }
  )
);
