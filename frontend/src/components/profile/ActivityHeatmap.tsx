"use client";

import { useState, useEffect } from "react";

interface ActivityHeatmapProps {
  data: Record<string, number>;
}

function getIntensity(count: number): number {
  if (count === 0) return 0;
  if (count <= 2) return 1;
  if (count <= 5) return 2;
  return 3;
}

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const DAYS = ["", "Mon", "", "Wed", "", "Fri", ""];

interface WeekDay {
  date: string;
  count: number;
  dayOfWeek: number;
}

interface MonthLabel {
  label: string;
  weekIndex: number;
}

function computeGrid(data: Record<string, number>) {
  const today = new Date();
  const start = new Date(today);
  start.setDate(start.getDate() - 364);
  start.setDate(start.getDate() - start.getDay());

  const weeks: WeekDay[][] = [];
  const monthLabels: MonthLabel[] = [];
  let currentWeek: WeekDay[] = [];
  let lastMonth = -1;
  const cursor = new Date(start);
  let weekIndex = 0;

  while (cursor <= today || currentWeek.length > 0) {
    if (cursor > today && currentWeek.length > 0) {
      weeks.push(currentWeek);
      break;
    }

    const dateStr = cursor.toISOString().split("T")[0];
    const month = cursor.getMonth();
    const dayOfWeek = cursor.getDay();

    if (month !== lastMonth) {
      monthLabels.push({ label: MONTHS[month], weekIndex });
      lastMonth = month;
    }

    currentWeek.push({ date: dateStr, count: data[dateStr] || 0, dayOfWeek });

    if (dayOfWeek === 6) {
      weeks.push(currentWeek);
      currentWeek = [];
      weekIndex++;
    }

    cursor.setDate(cursor.getDate() + 1);
  }

  const totalSolves = Object.values(data).reduce((sum, v) => sum + v, 0);
  const activeDays = Object.values(data).filter((v) => v > 0).length;

  return { weeks, monthLabels, totalSolves, activeDays };
}

export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  const [tooltip, setTooltip] = useState<{ date: string; count: number; x: number; y: number } | null>(null);
  const [grid, setGrid] = useState<ReturnType<typeof computeGrid> | null>(null);

  // Compute grid client-side only to avoid SSR hydration mismatch from new Date()
  useEffect(() => {
    setGrid(computeGrid(data));
  }, [data]);

  const intensityColors = [
    "bg-[var(--color-border)]",
    "bg-emerald-200 dark:bg-emerald-900",
    "bg-emerald-400 dark:bg-emerald-600",
    "bg-emerald-600 dark:bg-emerald-400",
  ];

  // Show placeholder during SSR / before mount
  if (!grid) {
    return (
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Activity</h3>
        </div>
        <div className="h-[140px] rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]" />
      </div>
    );
  }

  const { weeks, monthLabels, totalSolves, activeDays } = grid;

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Activity</h3>
        <p className="text-xs text-[var(--color-text-muted)]">
          {totalSolves} solves in the last year · {activeDays} active days
        </p>
      </div>

      <div className="overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
        {/* Month labels */}
        <div className="flex ml-8" style={{ gap: 0 }}>
          {monthLabels.map((m, i) => (
            <span
              key={i}
              className="text-[10px] text-[var(--color-text-muted)]"
              style={{
                position: "relative",
                left: m.weekIndex * 15 - (i > 0 ? monthLabels[i - 1].weekIndex * 15 + (monthLabels[i - 1]?.label.length * 5 || 0) : 0),
              }}
            >
              {m.label}
            </span>
          ))}
        </div>

        <div className="flex gap-0.5 mt-1 relative" onMouseLeave={() => setTooltip(null)}>
          {/* Day labels */}
          <div className="flex flex-col gap-0.5 mr-1 shrink-0">
            {DAYS.map((d, i) => (
              <span key={i} className="flex h-[13px] items-center text-[9px] text-[var(--color-text-muted)] leading-none">
                {d}
              </span>
            ))}
          </div>

          {/* Grid */}
          {weeks.map((week, wi) => (
            <div key={wi} className="flex flex-col gap-0.5">
              {Array.from({ length: 7 }).map((_, di) => {
                const day = week.find((d) => d.dayOfWeek === di);
                if (!day) return <div key={di} className="h-[13px] w-[13px]" />;

                const intensity = getIntensity(day.count);
                return (
                  <div
                    key={di}
                    className={`h-[13px] w-[13px] rounded-[2px] ${intensityColors[intensity]} cursor-pointer transition-colors`}
                    onMouseEnter={(e) => {
                      const rect = e.currentTarget.getBoundingClientRect();
                      setTooltip({ date: day.date, count: day.count, x: rect.left, y: rect.top });
                    }}
                  />
                );
              })}
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-3 flex items-center justify-end gap-1.5">
          <span className="text-[10px] text-[var(--color-text-muted)]">Less</span>
          {intensityColors.map((c, i) => (
            <div key={i} className={`h-[11px] w-[11px] rounded-[2px] ${c}`} />
          ))}
          <span className="text-[10px] text-[var(--color-text-muted)]">More</span>
        </div>
      </div>

      {/* Tooltip */}
      {tooltip && (
        <div
          className="fixed z-50 rounded-md bg-[var(--color-text-primary)] px-2.5 py-1.5 text-[11px] font-medium text-[var(--color-background)] shadow-lg pointer-events-none"
          style={{ left: tooltip.x - 30, top: tooltip.y - 36 }}
        >
          {tooltip.count} solve{tooltip.count !== 1 ? "s" : ""} on {tooltip.date}
        </div>
      )}
    </div>
  );
}
