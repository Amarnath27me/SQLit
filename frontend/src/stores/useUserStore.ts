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

  // Actions
  addXP: (amount: number) => void;
  markSolved: (problemId: string) => void;
  recordAttempt: (correct: boolean) => void;
  syncFromAuth0: (user: { name?: string; email?: string; picture?: string; sub?: string }) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
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

      addXP: (amount) =>
        set((state) => {
          const multiplier = getStreakMultiplier(state.streak);
          const finalXP = Math.floor(amount * multiplier);
          const newXP = state.xp + finalXP;
          // Level up every ~100 XP with increasing thresholds
          let level = 1;
          let xpNeeded = 100;
          let remaining = newXP;
          while (remaining >= xpNeeded) {
            remaining -= xpNeeded;
            level++;
            xpNeeded = Math.floor(xpNeeded * 1.3);
          }
          return { xp: newXP, level };
        }),

      markSolved: (problemId) =>
        set((state) => {
          if (state.solvedProblems.includes(problemId)) return state;

          const now = new Date().toISOString();
          let newStreak = state.streak;

          if (!state.lastSolveDate) {
            // First ever solve
            newStreak = 1;
          } else if (isSameDay(state.lastSolveDate, now)) {
            // Same day, streak stays
          } else if (isConsecutiveDay(state.lastSolveDate, now)) {
            // Consecutive day, increment streak
            newStreak = state.streak + 1;
          } else {
            // Streak broken, reset to 1
            newStreak = 1;
          }

          return {
            solvedProblems: [...state.solvedProblems, problemId],
            totalSolves: state.totalSolves + 1,
            streak: newStreak,
            lastSolveDate: now,
          };
        }),

      recordAttempt: (correct) =>
        set((state) => ({
          acceptanceHistory: {
            correct: state.acceptanceHistory.correct + (correct ? 1 : 0),
            total: state.acceptanceHistory.total + 1,
          },
        })),

      syncFromAuth0: (user) =>
        set({
          isAuthenticated: true,
          displayName: user.name || user.email || "User",
          email: user.email || "",
          avatar: user.picture || null,
          auth0Id: user.sub || null,
        }),

      logout: () =>
        set({
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
      }),
    }
  )
);
