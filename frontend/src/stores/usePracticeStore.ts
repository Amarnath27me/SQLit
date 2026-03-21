"use client";

import { create } from "zustand";

interface QueryResult {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  executionTimeMs: number;
}

interface ResultDiff {
  matchingRows: number;
  totalExpectedRows: number;
  mismatchedRows: number[];
  mismatchedColumns: string[];
}

interface PracticeState {
  // Editor
  query: string;
  dialect: "postgresql" | "mysql";
  dataset: string;

  // Execution
  status: "idle" | "running" | "accepted" | "wrong_answer" | "error";
  userResult: QueryResult | null;
  expectedResult: QueryResult | null;
  diff: ResultDiff | null;
  error: string | null;
  xpEarned: number;

  // Actions
  setQuery: (query: string) => void;
  setDialect: (dialect: "postgresql" | "mysql") => void;
  setDataset: (dataset: string) => void;
  setRunning: () => void;
  setResult: (result: {
    status: "accepted" | "wrong_answer" | "error";
    userResult: QueryResult | null;
    expectedResult: QueryResult | null;
    diff: ResultDiff | null;
    error: string | null;
    xpEarned: number;
  }) => void;
  reset: () => void;
}

export const usePracticeStore = create<PracticeState>((set) => ({
  query: "SELECT * FROM ",
  dialect: "postgresql",
  dataset: "ecommerce",
  status: "idle",
  userResult: null,
  expectedResult: null,
  diff: null,
  error: null,
  xpEarned: 0,

  setQuery: (query) => set({ query }),
  setDialect: (dialect) => set({ dialect }),
  setDataset: (dataset) => set({ dataset }),
  setRunning: () =>
    set({
      status: "running",
      userResult: null,
      expectedResult: null,
      diff: null,
      error: null,
      xpEarned: 0,
    }),
  setResult: (result) => set({ ...result }),
  reset: () =>
    set({
      query: "SELECT * FROM ",
      status: "idle",
      userResult: null,
      expectedResult: null,
      diff: null,
      error: null,
      xpEarned: 0,
    }),
}));
