"use client";

import { useState, useCallback, useMemo } from "react";
import ERBuilder from "@/components/db-design/ERBuilder";
import type { EREntity } from "@/components/db-design/ERBuilder";
import CHALLENGES from "@/data/db-design-challenges";
import type { DesignChallenge, SolutionTable } from "@/data/db-design-challenges";

/* ── Level Config ── */
const LEVELS = [
  { key: "beginner" as const, label: "Beginner", color: "text-green-400 bg-green-500/20 border-green-500/30", desc: "Understand tables, columns, and primary keys" },
  { key: "intermediate" as const, label: "Intermediate", color: "text-yellow-400 bg-yellow-500/20 border-yellow-500/30", desc: "One-to-many relationships and foreign keys" },
  { key: "advanced" as const, label: "Advanced", color: "text-blue-400 bg-blue-500/20 border-blue-500/30", desc: "Many-to-many, junction tables, real systems" },
  { key: "expert" as const, label: "Expert", color: "text-red-400 bg-red-500/20 border-red-500/30", desc: "Real-world systems and design tradeoffs" },
];

const modeBadge = {
  build: "bg-indigo-500/20 text-indigo-400",
  fix: "bg-orange-500/20 text-orange-400",
};

/* ── Validation ── */
interface ValidationResult {
  passed: boolean;
  message: string;
}

function validateSchema(entities: EREntity[], challenge: DesignChallenge): ValidationResult[] {
  const results: ValidationResult[] = [];

  for (const rule of challenge.validationRules) {
    switch (rule.check) {
      case "table_exists": {
        const found = entities.some((e) => e.name.toLowerCase() === rule.table?.toLowerCase());
        results.push({ passed: found, message: found ? rule.message : rule.failMessage });
        break;
      }
      case "has_pk": {
        const table = entities.find((e) => e.name.toLowerCase() === rule.table?.toLowerCase());
        const hasPk = table?.columns.some((c) => c.isPK) ?? false;
        results.push({ passed: hasPk, message: hasPk ? rule.message : rule.failMessage });
        break;
      }
      case "column_exists": {
        const table = entities.find((e) => e.name.toLowerCase() === rule.table?.toLowerCase());
        const hasCol = table?.columns.some((c) => c.name.toLowerCase() === rule.column?.toLowerCase()) ?? false;
        results.push({ passed: hasCol, message: hasCol ? rule.message : rule.failMessage });
        break;
      }
      case "has_fk": {
        const table = entities.find((e) => e.name.toLowerCase() === rule.table?.toLowerCase());
        const hasFk = table?.columns.some((c) =>
          c.isFK && c.fkRef?.toLowerCase().startsWith(rule.targetTable?.toLowerCase() + ".")
        ) ?? false;
        results.push({ passed: hasFk, message: hasFk ? rule.message : rule.failMessage });
        break;
      }
      default:
        break;
    }
  }

  return results;
}

/* ── Convert SolutionTable[] to EREntity[] for "fix" mode ── */
function solutionToEntities(tables: SolutionTable[]): EREntity[] {
  return tables.map((t, i) => ({
    id: `fix-${t.name}-${i}`,
    name: t.name,
    x: 40 + (i % 3) * 280,
    y: 40 + Math.floor(i / 3) * 200,
    columns: t.columns
      .filter((c) => c.name !== "")
      .map((c) => ({
        name: c.name,
        type: c.type,
        isPK: c.constraints.includes("PRIMARY KEY"),
        isFK: c.constraints.includes("FK"),
        fkRef: c.constraints.match(/FK\s*->\s*(\w+\.\w+)/)?.[1] || undefined,
        isNullable: !c.constraints.includes("NOT NULL") && !c.constraints.includes("PRIMARY KEY"),
        isUnique: c.constraints.includes("UNIQUE"),
      })),
  }));
}

/* ── Page ── */
export default function DBDesignPage() {
  const [selected, setSelected] = useState<DesignChallenge | null>(null);
  const [filterLevel, setFilterLevel] = useState<string>("all");
  const [filterMode, setFilterMode] = useState<string>("all");
  const [userEntities, setUserEntities] = useState<EREntity[]>([]);
  const [validationResults, setValidationResults] = useState<ValidationResult[] | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [revealedHints, setRevealedHints] = useState(0);

  const filtered = useMemo(() =>
    CHALLENGES.filter((ch) => {
      if (filterLevel !== "all" && ch.level !== filterLevel) return false;
      if (filterMode !== "all" && ch.mode !== filterMode) return false;
      return true;
    }),
  [filterLevel, filterMode]);

  const counts = useMemo(() => ({
    beginner: CHALLENGES.filter((c) => c.level === "beginner").length,
    intermediate: CHALLENGES.filter((c) => c.level === "intermediate").length,
    advanced: CHALLENGES.filter((c) => c.level === "advanced").length,
    expert: CHALLENGES.filter((c) => c.level === "expert").length,
  }), []);

  const handleValidate = useCallback(() => {
    if (!selected) return;
    const results = validateSchema(userEntities, selected);
    setValidationResults(results);
  }, [selected, userEntities]);

  const selectChallenge = (ch: DesignChallenge) => {
    setSelected(ch);
    setValidationResults(null);
    setShowSolution(false);
    setRevealedHints(0);
    // For "fix" mode, load the broken schema
    if (ch.mode === "fix" && ch.brokenSchema) {
      setUserEntities(solutionToEntities(ch.brokenSchema));
    } else {
      setUserEntities([]);
    }
  };

  const passedCount = validationResults?.filter((r) => r.passed).length ?? 0;
  const totalChecks = validationResults?.length ?? 0;
  const allPassed = validationResults !== null && passedCount === totalChecks;

  return (
    <div className="mx-auto max-w-[var(--max-width-content)] px-6 py-8">
      {!selected ? (
        /* ═══ Challenge List ═══ */
        <div>
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Database Design
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--color-text-secondary)]">
              Learn to think in data models. Build schemas, fix broken designs, and get instant feedback.
              Progress from single tables to complex real-world systems.
            </p>
          </div>

          {/* Level cards */}
          <div className="mb-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {LEVELS.map((level) => (
              <button
                key={level.key}
                onClick={() => setFilterLevel(filterLevel === level.key ? "all" : level.key)}
                className={`rounded-lg border p-4 text-left transition-all ${
                  filterLevel === level.key
                    ? `${level.color} border-current`
                    : "border-[var(--color-border)] bg-[var(--color-surface)] hover:border-[var(--color-accent)]/50"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className={`text-sm font-semibold ${filterLevel === level.key ? "" : "text-[var(--color-text-primary)]"}`}>
                    {level.label}
                  </span>
                  <span className="text-xs text-[var(--color-text-muted)]">
                    {counts[level.key]}
                  </span>
                </div>
                <p className={`mt-1 text-[11px] ${filterLevel === level.key ? "opacity-80" : "text-[var(--color-text-muted)]"}`}>
                  {level.desc}
                </p>
              </button>
            ))}
          </div>

          {/* Filters */}
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <select
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value)}
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-1.5 text-xs text-[var(--color-text-primary)]"
            >
              <option value="all">All Modes</option>
              <option value="build">Build Schema</option>
              <option value="fix">Fix Schema</option>
            </select>
            <span className="text-xs text-[var(--color-text-muted)]">
              {filtered.length} of {CHALLENGES.length} challenges
            </span>
            {(filterLevel !== "all" || filterMode !== "all") && (
              <button
                onClick={() => { setFilterLevel("all"); setFilterMode("all"); }}
                className="text-xs text-[var(--color-accent)] hover:underline"
              >
                Clear filters
              </button>
            )}
          </div>

          {/* Challenge Grid */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((ch) => {
              const levelConfig = LEVELS.find((l) => l.key === ch.level)!;
              return (
                <button
                  key={ch.id}
                  onClick={() => selectChallenge(ch)}
                  className="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5 text-left transition-all hover:border-[var(--color-accent)]/50 hover:shadow-lg"
                >
                  <div className="mb-3 flex flex-wrap items-center gap-2">
                    <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${levelConfig.color}`}>
                      {levelConfig.label}
                    </span>
                    <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${modeBadge[ch.mode]}`}>
                      {ch.mode === "build" ? "Build" : "Fix"}
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
                    {ch.title}
                  </h3>
                  <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-[var(--color-text-muted)]">
                    {ch.scenario}
                  </p>
                  <div className="mt-3 text-[10px] text-[var(--color-text-muted)]">
                    {ch.solution.length} tables expected
                  </div>
                </button>
              );
            })}
          </div>

          {filtered.length === 0 && (
            <div className="mt-8 text-center text-sm text-[var(--color-text-muted)]">
              No challenges match your filters.
            </div>
          )}
        </div>
      ) : (
        /* ═══ Challenge Detail — Build/Fix Mode ═══ */
        <div>
          <button
            onClick={() => setSelected(null)}
            className="mb-4 text-xs font-medium text-[var(--color-accent)] hover:underline"
          >
            &#8592; Back to challenges
          </button>

          <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
            {/* Left — Brief + Guidance */}
            <div className="space-y-4">
              {/* Context */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
                <div className="mb-3 flex flex-wrap items-center gap-2">
                  <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${LEVELS.find((l) => l.key === selected.level)!.color}`}>
                    {LEVELS.find((l) => l.key === selected.level)!.label}
                  </span>
                  <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${modeBadge[selected.mode]}`}>
                    {selected.mode === "build" ? "Build Schema" : "Fix Schema"}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-[var(--color-text-primary)]">{selected.title}</h2>
                <p className="mt-3 text-sm leading-relaxed text-[var(--color-text-secondary)]">{selected.scenario}</p>

                {selected.mode === "fix" && selected.brokenDescription && (
                  <div className="mt-3 rounded-md border border-red-500/30 bg-red-500/10 p-3">
                    <p className="text-xs font-medium text-red-400">What&apos;s broken:</p>
                    <p className="mt-1 text-xs text-red-300">{selected.brokenDescription}</p>
                  </div>
                )}

                <div className="mt-4">
                  <h4 className="text-xs font-semibold text-[var(--color-text-primary)]">Requirements</h4>
                  <ul className="mt-2 space-y-1.5">
                    {selected.requirements.map((req, i) => (
                      <li key={i} className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--color-accent)]" />
                        {req}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Hints */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
                  Hints ({revealedHints}/{selected.hints.length})
                </h3>
                <div className="mt-3 space-y-2">
                  {selected.hints.slice(0, revealedHints).map((hint, i) => (
                    <div key={i} className="rounded-md bg-[var(--color-background)] p-3 text-xs text-[var(--color-text-secondary)]">
                      <span className="font-medium text-[var(--color-accent)]">Hint {i + 1}:</span> {hint}
                    </div>
                  ))}
                  {revealedHints < selected.hints.length && (
                    <button
                      onClick={() => setRevealedHints((h) => h + 1)}
                      className="text-xs font-medium text-[var(--color-accent)] hover:underline"
                    >
                      Reveal Hint {revealedHints + 1}
                    </button>
                  )}
                </div>
              </div>

              {/* Validate Button */}
              <button
                onClick={handleValidate}
                disabled={userEntities.length === 0}
                className="w-full rounded-lg bg-[var(--color-accent)] px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-[var(--color-accent-hover)] disabled:opacity-50"
              >
                Validate My Schema
              </button>

              {/* Validation Results */}
              {validationResults && (
                <div className={`rounded-lg border p-4 ${allPassed ? "border-green-500/30 bg-green-500/10" : "border-[var(--color-border)] bg-[var(--color-surface)]"}`}>
                  <div className="mb-3 flex items-center justify-between">
                    <h3 className={`text-xs font-medium uppercase tracking-wider ${allPassed ? "text-green-400" : "text-[var(--color-text-muted)]"}`}>
                      {allPassed ? "All Checks Passed!" : `${passedCount}/${totalChecks} Checks Passed`}
                    </h3>
                    {allPassed && <span className="text-lg">&#x2705;</span>}
                  </div>
                  <div className="space-y-2">
                    {validationResults.map((r, i) => (
                      <div key={i} className="flex items-start gap-2 text-xs">
                        <span className={`mt-0.5 shrink-0 ${r.passed ? "text-green-400" : "text-red-400"}`}>
                          {r.passed ? "\u2714" : "\u2718"}
                        </span>
                        <span className={r.passed ? "text-green-300" : "text-red-300"}>
                          {r.message}
                        </span>
                      </div>
                    ))}
                  </div>

                  {allPassed && (
                    <div className="mt-4 space-y-2">
                      <h4 className="text-xs font-semibold text-green-400">What You Learned</h4>
                      <ul className="space-y-1">
                        {selected.learnings.map((l, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-[var(--color-text-secondary)]">
                            <span className="mt-0.5 text-[var(--color-accent)]">&#8226;</span> {l}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Show Solution */}
              <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
                {showSolution ? (
                  <div className="space-y-3">
                    <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-accent)]">
                      Reference Solution
                    </h3>
                    {selected.solution.map((table) => (
                      <div key={table.name} className="rounded-md bg-[var(--color-background)] p-3">
                        <p className="mb-2 text-xs font-bold text-[var(--color-text-primary)]">{table.name}</p>
                        <div className="space-y-0.5">
                          {table.columns.filter((c) => c.name).map((col) => (
                            <div key={col.name} className="flex items-center gap-2 text-[11px]">
                              <span className="font-mono text-[var(--color-accent)]">{col.name}</span>
                              <span className="text-[var(--color-text-muted)]">{col.type}</span>
                              {col.constraints && (
                                <span className="text-[var(--color-text-muted)] opacity-60">{col.constraints}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                    {selected.relationships.length > 0 && (
                      <div className="mt-2">
                        <p className="mb-1 text-[10px] font-medium uppercase text-[var(--color-text-muted)]">Relationships</p>
                        {selected.relationships.map((r, i) => (
                          <p key={i} className="text-[11px] text-[var(--color-text-secondary)]">{r}</p>
                        ))}
                      </div>
                    )}
                    <button
                      onClick={() => setShowSolution(false)}
                      className="text-xs text-[var(--color-text-muted)] hover:underline"
                    >
                      Hide solution
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowSolution(true)}
                    className="w-full text-center text-xs font-medium text-[var(--color-accent)] hover:underline"
                  >
                    Stuck? Reveal Reference Solution
                  </button>
                )}
              </div>
            </div>

            {/* Right — ER Builder */}
            <div className="rounded-lg border border-[var(--color-border)] overflow-hidden" style={{ minHeight: 500 }}>
              <ERBuilder
                key={selected.id}
                initialEntities={selected.mode === "fix" && selected.brokenSchema ? solutionToEntities(selected.brokenSchema) : undefined}
                onEntitiesChange={setUserEntities}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
