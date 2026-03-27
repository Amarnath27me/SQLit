"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useThemeStore } from "@/stores/useThemeStore";
import { useUserStore } from "@/stores/useUserStore";

const primaryLinks = [
  { href: "/practice", label: "Practice" },
  { href: "/interview", label: "Interview" },
  { href: "/sandbox", label: "Sandbox" },
  { href: "/optimization", label: "Optimization" },
  { href: "/docs", label: "Docs" },
  { href: "/datasets", label: "Datasets" },
  { href: "/debug", label: "Data Debugging" },
];

const moreLinks = [
  { href: "/analyzer", label: "Query Analyzer" },
  { href: "/challenge", label: "Challenge Mode" },
  { href: "/db-design", label: "Database Design" },
  { href: "/leaderboard", label: "Leaderboard" },
];

const allNavLinks = [...primaryLinks, ...moreLinks];

/** Sun icon — shown when in dark mode (click to go light) */
function SunIcon() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  );
}

/** Moon icon — shown when in light mode (click to go dark) */
function MoonIcon() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
  );
}

/** User dropdown menu */
function UserMenu({ name, picture }: { name: string; picture?: string | null }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const initial = name?.charAt(0)?.toUpperCase() || "U";

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--color-accent)]/10 text-sm font-bold text-[var(--color-accent)] transition-colors hover:bg-[var(--color-accent)]/20 overflow-hidden"
        aria-label="User menu"
      >
        {picture ? (
          <img src={picture} alt={name} className="h-full w-full rounded-full object-cover" />
        ) : (
          initial
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-10 z-50 w-48 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] py-1 shadow-lg">
          <div className="border-b border-[var(--color-border)] px-4 py-2">
            <p className="text-sm font-medium text-[var(--color-text-primary)] truncate">{name}</p>
          </div>
          <Link
            href="/profile"
            onClick={() => setOpen(false)}
            className="block px-4 py-2 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
          >
            Profile
          </Link>
          <Link
            href="/settings"
            onClick={() => setOpen(false)}
            className="block px-4 py-2 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
          >
            Settings
          </Link>
          <hr className="my-1 border-[var(--color-border)]" />
          <a
            href="/auth/logout"
            className="block px-4 py-2 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-950"
          >
            Sign Out
          </a>
        </div>
      )}
    </div>
  );
}

/** "More" dropdown for secondary nav links */
function MoreDropdown({ pathname }: { pathname: string }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const isAnyActive = moreLinks.some(
    (l) => pathname === l.href || pathname.startsWith(l.href + "/")
  );

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        aria-label="More navigation links"
        aria-expanded={open}
        aria-haspopup="true"
        className={`flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
          isAnyActive
            ? "text-[var(--color-accent)]"
            : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
        }`}
      >
        More
        <svg className={`h-3.5 w-3.5 transition-transform ${open ? "rotate-180" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="absolute left-0 top-10 z-50 w-52 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] py-1 shadow-lg">
          {moreLinks.map((link) => {
            const isActive = pathname === link.href || pathname.startsWith(link.href + "/");
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={`block px-4 py-2 text-sm transition-colors ${
                  isActive
                    ? "text-[var(--color-accent)] bg-[var(--color-accent)]/5"
                    : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { theme, toggle, hydrate } = useThemeStore();
  const { xp, streak } = useUserStore();
  const { user, isLoading } = useUser();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--color-border)] bg-[var(--color-surface)]">
      <nav className="mx-auto flex h-14 max-w-[var(--max-width-content)] items-center justify-between px-6">
        {/* Logo */}
        <Link href="/" className="text-lg font-bold tracking-tight text-[var(--color-text-primary)]">
          <span className="text-[var(--color-accent)]">SQL</span>it
        </Link>

        {/* Nav tabs — desktop */}
        <nav aria-label="Main navigation" className="hidden items-center gap-1 md:flex">
          {primaryLinks.map((link) => {
            const isActive = pathname === link.href || pathname.startsWith(link.href + "/");
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-label={link.label}
                aria-current={isActive ? "page" : undefined}
                className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "text-[var(--color-accent)] border-b-2 border-[var(--color-accent)]"
                    : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
          <MoreDropdown pathname={pathname} />
        </nav>

        {/* User area */}
        <div className="flex items-center gap-3">
          {/* Streak display */}
          {streak > 0 && (
            <span aria-label={`${streak}-day streak`} className="flex items-center gap-1 rounded-full bg-orange-500/10 px-2.5 py-0.5 text-xs font-semibold text-orange-500">
              <svg className="h-3.5 w-3.5" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 23c-3.866 0-7-3.134-7-7 0-2.812 1.882-5.86 3.54-8.08A.5.5 0 019.3 8l1.2 2.4a.5.5 0 00.9-.1l1.1-3.8a.5.5 0 01.94-.05C15.23 9.87 19 14.09 19 16c0 3.866-3.134 7-7 7z" />
              </svg>
              {streak}
            </span>
          )}

          {/* XP display */}
          {xp > 0 && (
            <span aria-label={`${xp} experience points`} className="rounded-full bg-[var(--color-accent)]/10 px-2.5 py-0.5 text-xs font-semibold text-[var(--color-accent)]">
              {xp} XP
            </span>
          )}

          {/* Theme toggle */}
          <button
            onClick={toggle}
            className="rounded-md p-1.5 text-[var(--color-text-secondary)] transition-colors hover:bg-[var(--color-background)]"
            aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          >
            {theme === "dark" ? <SunIcon /> : <MoonIcon />}
          </button>

          {/* Auth: user menu or sign-in button */}
          {!isLoading && (
            <>
              {user ? (
                <UserMenu
                  name={user.name || user.nickname || user.email || "User"}
                  picture={user.picture}
                />
              ) : (
                <a
                  href="/auth/login"
                  className="rounded-lg bg-[var(--color-accent)] px-4 py-1.5 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
                >
                  Sign In
                </a>
              )}
            </>
          )}

          {/* Hamburger menu — mobile */}
          <button
            className="rounded-md p-1.5 text-[var(--color-text-secondary)] transition-colors hover:bg-[var(--color-background)] md:hidden"
            aria-label="Toggle menu"
            onClick={() => setMobileMenuOpen((prev) => !prev)}
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </nav>

      {/* Mobile nav menu */}
      {mobileMenuOpen && (
        <div className="border-t border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-3 md:hidden">
          <div className="flex flex-col gap-1">
            {allNavLinks.map((link) => {
              const isActive = pathname === link.href || pathname.startsWith(link.href + "/");
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    isActive
                      ? "text-[var(--color-accent)] bg-[var(--color-accent)]/5"
                      : "text-[var(--color-text-secondary)] hover:bg-[var(--color-background)] hover:text-[var(--color-text-primary)]"
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
            {/* Mobile auth links */}
            <hr className="my-2 border-[var(--color-border)]" />
            {user ? (
              <>
                <Link
                  href="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="rounded-md px-3 py-2 text-sm font-medium text-[var(--color-text-secondary)] hover:bg-[var(--color-background)]"
                >
                  Profile
                </Link>
                <a
                  href="/auth/logout"
                  className="rounded-md px-3 py-2 text-sm font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-950"
                >
                  Sign Out
                </a>
              </>
            ) : (
              <a
                href="/auth/login"
                className="rounded-md px-3 py-2 text-sm font-medium text-[var(--color-accent)] hover:bg-[var(--color-accent)]/5"
              >
                Sign In
              </a>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
