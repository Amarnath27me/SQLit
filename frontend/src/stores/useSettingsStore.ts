"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsState {
  editorFontSize: number;
  editorTabSize: number;
  defaultDialect: "postgresql" | "mysql";
  defaultDataset: string;
  leaderboardOptIn: boolean;

  setEditorFontSize: (size: number) => void;
  setEditorTabSize: (size: number) => void;
  setDefaultDialect: (dialect: "postgresql" | "mysql") => void;
  setDefaultDataset: (dataset: string) => void;
  setLeaderboardOptIn: (optIn: boolean) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      editorFontSize: 14,
      editorTabSize: 2,
      defaultDialect: "postgresql",
      defaultDataset: "ecommerce",
      leaderboardOptIn: false,

      setEditorFontSize: (size) => set({ editorFontSize: size }),
      setEditorTabSize: (size) => set({ editorTabSize: size }),
      setDefaultDialect: (dialect) => set({ defaultDialect: dialect }),
      setDefaultDataset: (dataset) => set({ defaultDataset: dataset }),
      setLeaderboardOptIn: (optIn) => set({ leaderboardOptIn: optIn }),
    }),
    { name: "sqlit-settings" }
  )
);
