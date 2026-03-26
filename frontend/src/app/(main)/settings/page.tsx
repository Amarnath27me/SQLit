"use client";

import { useState } from "react";
import { useUserStore } from "@/stores/useUserStore";
import { useThemeStore } from "@/stores/useThemeStore";
import { useSettingsStore } from "@/stores/useSettingsStore";

export default function SettingsPage() {
  const { displayName, isAuthenticated } = useUserStore();
  const { theme, toggle } = useThemeStore();
  const settings = useSettingsStore();

  const [name, setName] = useState(displayName);
  const [saved, setSaved] = useState(false);

  function handleSave() {
    // Persist display name to user store
    if (name !== displayName) {
      useUserStore.setState({ displayName: name });
    }
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-8">
      <h1 className="text-2xl font-bold">Settings</h1>
      <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
        Customize your SQLit experience.
      </p>

      <div className="mt-8 space-y-8">
        {/* Profile */}
        <section>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Profile</h2>
          <div className="mt-4 space-y-4">
            <div>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)]">
                Display Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 w-full rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
                placeholder="Your display name"
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[var(--color-text-secondary)]">Leaderboard Visibility</p>
                <p className="text-xs text-[var(--color-text-muted)]">Show your profile on the public leaderboard</p>
              </div>
              <button
                onClick={() => settings.setLeaderboardOptIn(!settings.leaderboardOptIn)}
                role="switch"
                aria-checked={settings.leaderboardOptIn}
                aria-label="Toggle leaderboard visibility"
                className={`relative h-6 w-11 rounded-full transition-colors ${
                  settings.leaderboardOptIn ? "bg-[var(--color-accent)]" : "bg-[var(--color-border)]"
                }`}
              >
                <span
                  className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform ${
                    settings.leaderboardOptIn ? "translate-x-[22px]" : "translate-x-0.5"
                  }`}
                />
              </button>
            </div>
          </div>
        </section>

        <hr className="border-[var(--color-border)]" />

        {/* Appearance */}
        <section>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Appearance</h2>
          <div className="mt-4 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[var(--color-text-secondary)]">Theme</p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  Currently: {theme === "dark" ? "Dark" : "Light"}
                </p>
              </div>
              <button
                onClick={toggle}
                className="rounded-md border border-[var(--color-border)] px-3 py-1.5 text-xs font-medium text-[var(--color-text-secondary)] transition-colors hover:border-[var(--color-accent)] hover:text-[var(--color-accent)]"
              >
                Switch to {theme === "dark" ? "Light" : "Dark"}
              </button>
            </div>
          </div>
        </section>

        <hr className="border-[var(--color-border)]" />

        {/* Editor */}
        <section>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Editor</h2>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)]">
                Font Size
              </label>
              <select
                value={settings.editorFontSize}
                onChange={(e) => settings.setEditorFontSize(Number(e.target.value))}
                aria-label="Font size"
                className="mt-1 w-full rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              >
                {[12, 13, 14, 15, 16, 18].map((s) => (
                  <option key={s} value={s}>{s}px</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)]">
                Tab Size
              </label>
              <select
                value={settings.editorTabSize}
                onChange={(e) => settings.setEditorTabSize(Number(e.target.value))}
                aria-label="Tab size"
                className="mt-1 w-full rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              >
                {[2, 4].map((s) => (
                  <option key={s} value={s}>{s} spaces</option>
                ))}
              </select>
            </div>
          </div>
        </section>

        <hr className="border-[var(--color-border)]" />

        {/* Defaults */}
        <section>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Defaults</h2>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)]">
                SQL Dialect
              </label>
              <select
                value={settings.defaultDialect}
                onChange={(e) => settings.setDefaultDialect(e.target.value as "postgresql" | "mysql")}
                className="mt-1 w-full rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              >
                <option value="postgresql">PostgreSQL</option>
                <option value="mysql">MySQL</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)]">
                Default Dataset
              </label>
              <select
                value={settings.defaultDataset}
                onChange={(e) => settings.setDefaultDataset(e.target.value)}
                className="mt-1 w-full rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              >
                <option value="ecommerce">E-Commerce</option>
                <option value="finance">Finance</option>
                <option value="healthcare">Healthcare</option>
              </select>
            </div>
          </div>
        </section>

        <hr className="border-[var(--color-border)]" />

        {/* Account */}
        <section>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Account</h2>
          <div className="mt-4 space-y-3">
            {isAuthenticated ? (
              <>
                <p className="text-sm text-[var(--color-text-secondary)]">
                  Signed in as <span className="font-medium text-[var(--color-text-primary)]">{displayName}</span>
                </p>
                <a href="/auth/logout" aria-label="Sign out" className="inline-block rounded-md border border-red-200 px-3 py-1.5 text-xs font-medium text-red-500 transition-colors hover:bg-red-50 dark:border-red-800 dark:hover:bg-red-950">
                  Sign Out
                </a>
              </>
            ) : (
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
                <p className="text-sm text-[var(--color-text-secondary)]">
                  Sign in to save your progress, sync across devices, and appear on the leaderboard.
                </p>
                <a
                  href="/auth/login"
                  className="mt-3 inline-block rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
                >
                  Sign In
                </a>
              </div>
            )}
          </div>
        </section>
      </div>

      {/* Save button */}
      <div className="mt-8 flex items-center gap-3">
        <button
          onClick={handleSave}
          className="rounded-lg bg-[var(--color-accent)] px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
        >
          Save Changes
        </button>
        {saved && (
          <span className="text-sm font-medium text-emerald-500">
            Settings saved
          </span>
        )}
      </div>
    </div>
  );
}
