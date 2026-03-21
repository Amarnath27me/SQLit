"use client";

import { create } from "zustand";

type Theme = "light" | "dark";

interface ThemeStore {
  theme: Theme;
  toggle: () => void;
  hydrate: () => void;
}

function applyTheme(theme: Theme) {
  if (typeof document !== "undefined") {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }
}

function getInitialTheme(): Theme {
  if (typeof window === "undefined") return "light";

  const stored = localStorage.getItem("sqlit-theme") as Theme | null;
  if (stored === "light" || stored === "dark") return stored;

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export const useThemeStore = create<ThemeStore>((set, get) => ({
  theme: "light", // SSR-safe default; real value set in hydrate()
  toggle: () => {
    const next = get().theme === "light" ? "dark" : "light";
    localStorage.setItem("sqlit-theme", next);
    applyTheme(next);
    set({ theme: next });
  },
  hydrate: () => {
    const theme = getInitialTheme();
    localStorage.setItem("sqlit-theme", theme);
    applyTheme(theme);
    set({ theme });
  },
}));
