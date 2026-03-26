import {
  Code2,
  Bug,
  BarChart3,
  BookOpen,
  ArrowRight,
  Database,
  Terminal,
  ChevronRight,
  Trophy,
  Briefcase,
  Timer,
  Layers,
} from "lucide-react";
import type { Metadata } from "next";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { AuthSync } from "@/components/auth/AuthSync";

export const metadata: Metadata = {
  title: "SQLit — LeetCode for SQL & Data Engineering",
  description:
    "400+ problems, 3 industry datasets, real SQL execution. Master SQL through hands-on practice on production-style databases.",
};

const features = [
  {
    icon: Terminal,
    title: "Practice Arena",
    description:
      "400+ problems across 6 difficulty levels with real SQL execution and instant feedback",
    href: "/practice",
  },
  {
    icon: Bug,
    title: "Data Debugging",
    description:
      "Find duplicates, NULL bugs, wrong joins — skills no other platform teaches",
    href: "/debug",
  },
  {
    icon: BarChart3,
    title: "Query Analyzer",
    description:
      "Step through SQL execution visually and understand every clause",
    href: "/analyzer",
  },
  {
    icon: BookOpen,
    title: "Documentation",
    description:
      "Comprehensive SQL reference with real examples and practice links",
    href: "/docs",
  },
  {
    icon: Briefcase,
    title: "Interview Prep",
    description:
      "97 curated problems from FAANG, Big Tech, and FinTech interviews",
    href: "/interview",
  },
  {
    icon: Timer,
    title: "Challenge Mode",
    description:
      "Timed challenges with difficulty selection and bonus XP rewards",
    href: "/challenge",
  },
  {
    icon: Layers,
    title: "DB Design & Optimization",
    description:
      "Learn normalization, ER modeling, and query optimization techniques",
    href: "/db-design",
  },
  {
    icon: Trophy,
    title: "Leaderboard",
    description:
      "Compete with other SQL practitioners and track your ranking",
    href: "/leaderboard",
  },
];

const levels = [
  { name: "Fundamentals", count: 70 },
  { name: "Aggregations", count: 65 },
  { name: "Joins", count: 70 },
  { name: "Subqueries", count: 55 },
  { name: "Window Functions", count: 50 },
  { name: "Advanced", count: 102 },
];

const datasets = [
  {
    name: "E-Commerce",
    tables: 8,
    problems: 140,
    description:
      "Orders, products, customers, reviews — a full retail data model",
  },
  {
    name: "Finance",
    tables: 7,
    problems: 137,
    description:
      "Transactions, accounts, loans, cards — real banking data",
  },
  {
    name: "Healthcare",
    tables: 8,
    problems: 135,
    description:
      "Patients, doctors, prescriptions, billing — clinical data at scale",
  },
];

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <AuthSync />
      <Navbar />
      <main className="flex-1 flex flex-col items-center">
      {/* ── Hero ── */}
      <section className="w-full px-6 pt-32 pb-20">
        <div className="mx-auto max-w-6xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-medium text-[var(--color-text-secondary)]">
              412 problems · 3 datasets · Real SQL execution
            </span>
          </div>

          <h1 className="text-5xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-6xl lg:text-7xl">
            Practice SQL on{" "}
            <span className="text-[var(--color-accent)]">Real Databases</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-[var(--color-text-secondary)]">
            The LeetCode for SQL & Data Engineering. Solve problems on
            production-style schemas, debug data issues, and prep for interviews
            — all with real SQL execution.
          </p>

          <div className="mt-10 flex items-center justify-center gap-4">
            <a
              href="/practice"
              className="inline-flex items-center gap-2 rounded-lg bg-[var(--color-accent)] px-8 py-3 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
            >
              Start Practicing
              <ArrowRight className="h-4 w-4" />
            </a>
            <a
              href="/interview"
              className="inline-flex items-center gap-2 rounded-lg border border-[var(--color-border)] px-8 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-colors hover:bg-[var(--color-surface)]"
            >
              Interview Prep
            </a>
          </div>

          {/* Code snippet preview */}
          <div className="mx-auto mt-16 max-w-xl">
            <div className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]">
              <div className="flex items-center gap-2 border-b border-[var(--color-border)] px-4 py-3">
                <span className="h-3 w-3 rounded-full bg-[#ef4444]/40" />
                <span className="h-3 w-3 rounded-full bg-[#eab308]/40" />
                <span className="h-3 w-3 rounded-full bg-[#22c55e]/40" />
                <span className="ml-2 text-xs text-[var(--color-text-muted)]">
                  query.sql
                </span>
              </div>
              <pre className="p-5 text-left text-sm leading-relaxed">
                <code>
                  <span className="text-[#2563eb] font-semibold">SELECT</span>
                  <span className="text-[var(--color-text-primary)]"> c.name, </span>
                  <span className="text-[#2563eb] font-semibold">COUNT</span>
                  <span className="text-[var(--color-text-muted)]">(</span>
                  <span className="text-[var(--color-text-primary)]">o.id</span>
                  <span className="text-[var(--color-text-muted)]">)</span>
                  <span className="text-[var(--color-text-primary)]"> </span>
                  <span className="text-[#2563eb] font-semibold">AS</span>
                  <span className="text-[var(--color-text-primary)]"> total_orders</span>
                  {"\n"}
                  <span className="text-[#2563eb] font-semibold">FROM</span>
                  <span className="text-[#16a34a]"> customers</span>
                  <span className="text-[var(--color-text-primary)]"> c</span>
                  {"\n"}
                  <span className="text-[#2563eb] font-semibold">JOIN</span>
                  <span className="text-[#16a34a]"> orders</span>
                  <span className="text-[var(--color-text-primary)]"> o </span>
                  <span className="text-[#2563eb] font-semibold">ON</span>
                  <span className="text-[var(--color-text-primary)]"> c.id = o.customer_id</span>
                  {"\n"}
                  <span className="text-[#2563eb] font-semibold">GROUP BY</span>
                  <span className="text-[var(--color-text-primary)]"> c.name</span>
                  {"\n"}
                  <span className="text-[#2563eb] font-semibold">HAVING</span>
                  <span className="text-[var(--color-text-primary)]"> </span>
                  <span className="text-[#2563eb] font-semibold">COUNT</span>
                  <span className="text-[var(--color-text-muted)]">(</span>
                  <span className="text-[var(--color-text-primary)]">o.id</span>
                  <span className="text-[var(--color-text-muted)]">)</span>
                  <span className="text-[var(--color-text-primary)]"> &gt; </span>
                  <span className="text-[#d97706]">5</span>
                  <span className="text-[var(--color-text-muted)]">;</span>
                </code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats bar ── */}
      <section className="w-full border-y border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-10">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-8 text-center sm:grid-cols-4">
          <div>
            <p className="text-3xl font-bold text-[var(--color-accent)]">412</p>
            <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
              Problems
            </p>
          </div>
          <div>
            <p className="text-3xl font-bold text-[var(--color-text-primary)]">3</p>
            <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
              Industry Datasets
            </p>
          </div>
          <div>
            <p className="text-3xl font-bold text-[var(--color-text-primary)]">23</p>
            <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
              Tables
            </p>
          </div>
          <div>
            <p className="text-3xl font-bold text-emerald-500">Real</p>
            <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
              SQL Execution
            </p>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="w-full px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-4xl">
              Everything you need to master SQL
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-[var(--color-text-secondary)]">
              A complete platform built for learning by doing, not just reading.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <a
                key={feature.title}
                href={feature.href}
                className="group rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 transition-all hover:border-[var(--color-accent)]/30 hover:shadow-lg hover:shadow-[var(--color-accent)]/5"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--color-accent)]/10 transition-colors group-hover:bg-[var(--color-accent)]/20">
                  <feature.icon className="h-5 w-5 text-[var(--color-accent)]" />
                </div>
                <h3 className="mt-4 text-sm font-semibold text-[var(--color-text-primary)]">
                  {feature.title}
                </h3>
                <p className="mt-1.5 text-xs leading-relaxed text-[var(--color-text-secondary)]">
                  {feature.description}
                </p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* ── Problem categories ── */}
      <section className="w-full border-t border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-4xl">
              6 levels of mastery
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-[var(--color-text-secondary)]">
              Progress from basics to advanced topics at your own pace.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            {levels.map((level, i) => (
              <div
                key={level.name}
                className="rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] p-5 text-center transition-colors hover:border-[var(--color-accent)]/30"
              >
                <p className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Level {i + 1}
                </p>
                <p className="mt-2 text-sm font-semibold text-[var(--color-text-primary)]">
                  {level.name}
                </p>
                <p className="mt-1 text-2xl font-bold text-[var(--color-accent)]">
                  {level.count}
                </p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  problems
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Datasets ── */}
      <section className="w-full px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-4xl">
              Real-world datasets
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-[var(--color-text-secondary)]">
              Practice on production-style schemas with realistic data.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-3">
            {datasets.map((ds) => (
              <div
                key={ds.name}
                className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-8 transition-colors hover:border-[var(--color-accent)]/30"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--color-accent)]/10">
                  <Database className="h-5 w-5 text-[var(--color-accent)]" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-[var(--color-text-primary)]">
                  {ds.name}
                </h3>
                <div className="mt-1 flex items-center gap-3">
                  <span className="text-sm font-medium text-[var(--color-accent)]">
                    {ds.tables} tables
                  </span>
                  <span className="text-xs text-[var(--color-text-muted)]">·</span>
                  <span className="text-sm text-[var(--color-text-secondary)]">
                    {ds.problems} problems
                  </span>
                </div>
                <p className="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                  {ds.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="w-full border-t border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-24">
        <div className="mx-auto max-w-6xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-4xl">
            Ready to master SQL?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-[var(--color-text-secondary)]">
            Stop reading tutorials. Start writing real queries against real
            databases. Free to get started.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <a
              href="/practice"
              className="inline-flex items-center gap-2 rounded-lg bg-[var(--color-accent)] px-8 py-3 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
            >
              Start Practicing
              <ChevronRight className="h-4 w-4" />
            </a>
            <a
              href="/sandbox"
              className="inline-flex items-center gap-2 rounded-lg border border-[var(--color-border)] px-8 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-colors hover:bg-[var(--color-background)]"
            >
              Try the Sandbox
            </a>
          </div>
        </div>
      </section>
    </main>
      <Footer />
    </div>
  );
}
