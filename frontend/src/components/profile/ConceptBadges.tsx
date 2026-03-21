"use client";

interface ConceptBadge {
  concept: string;
  solved: number;
  total: number;
  icon: string;
}

interface ConceptBadgesProps {
  badges: ConceptBadge[];
}

function getBadgeLevel(solved: number, total: number): { label: string; color: string } {
  const pct = total > 0 ? solved / total : 0;
  if (pct >= 1) return { label: "Master", color: "text-amber-500" };
  if (pct >= 0.75) return { label: "Expert", color: "text-purple-500" };
  if (pct >= 0.5) return { label: "Proficient", color: "text-blue-500" };
  if (pct >= 0.25) return { label: "Learner", color: "text-emerald-500" };
  return { label: "Beginner", color: "text-[var(--color-text-muted)]" };
}

export function ConceptBadges({ badges }: ConceptBadgesProps) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-3">Concept Mastery</h3>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        {badges.map((badge) => {
          const pct = badge.total > 0 ? (badge.solved / badge.total) * 100 : 0;
          const level = getBadgeLevel(badge.solved, badge.total);
          const isUnlocked = badge.solved > 0;

          return (
            <div
              key={badge.concept}
              className={`rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4 transition-all ${
                isUnlocked ? "hover:border-[var(--color-accent)]/30" : "opacity-60"
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">{badge.icon}</span>
                <div className="min-w-0">
                  <p className="text-xs font-semibold text-[var(--color-text-primary)] truncate">
                    {badge.concept}
                  </p>
                  <p className={`text-[10px] font-medium ${level.color}`}>{level.label}</p>
                </div>
              </div>

              {/* Progress bar */}
              <div className="mt-3">
                <div className="h-1.5 w-full rounded-full bg-[var(--color-border)]">
                  <div
                    className="h-1.5 rounded-full bg-[var(--color-accent)] transition-all duration-500"
                    style={{ width: `${Math.min(pct, 100)}%` }}
                  />
                </div>
                <p className="mt-1 text-[10px] text-[var(--color-text-muted)]">
                  {badge.solved}/{badge.total} solved
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
