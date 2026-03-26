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

interface DayCell {
  date: string;
  count: number;
  dayOfWeek: number;
}

const CELL_SIZE = 11;
const CELL_GAP = 2;
const CELL_STEP = CELL_SIZE + CELL_GAP;

function computeGrid(data: Record<string, number>) {
  const today = new Date();
  const start = new Date(today);
  start.setDate(start.getDate() - 364);
  start.setDate(start.getDate() - start.getDay());

  const weeks: DayCell[][] = [];
  let currentWeek: DayCell[] = [];
  let lastMonth = -1;
  const cursor = new Date(start);
  let weekIndex = 0;

  // Track month boundaries with their pixel positions
  const monthPositions: { label: string; x: number }[] = [];

  while (cursor <= today || currentWeek.length > 0) {
    if (cursor > today && currentWeek.length > 0) {
      weeks.push(currentWeek);
      break;
    }

    const dateStr = cursor.toISOString().split("T")[0];
    const month = cursor.getMonth();
    const dayOfWeek = cursor.getDay();

    // Record month label at the start of each new month (only on Sunday)
    if (month !== lastMonth && dayOfWeek === 0) {
      monthPositions.push({ label: MONTHS[month], x: weekIndex * CELL_STEP });
      lastMonth = month;
    } else if (month !== lastMonth && currentWeek.length === 0) {
      // First day of the grid or start of a new week close to month boundary
      monthPositions.push({ label: MONTHS[month], x: weekIndex * CELL_STEP });
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

  // Deduplicate month labels that are too close
  const filteredMonths: { label: string; x: number }[] = [];
  for (const m of monthPositions) {
    const last = filteredMonths[filteredMonths.length - 1];
    if (!last || m.x - last.x >= CELL_STEP * 3) {
      filteredMonths.push(m);
    }
  }

  const totalSolves = Object.values(data).reduce((sum, v) => sum + v, 0);
  const activeDays = Object.values(data).filter((v) => v > 0).length;

  return { weeks, monthPositions: filteredMonths, totalSolves, activeDays };
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr + "T12:00:00");
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
}

export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  const [tooltip, setTooltip] = useState<{ date: string; count: number; x: number; y: number } | null>(null);
  const [grid, setGrid] = useState<ReturnType<typeof computeGrid> | null>(null);

  useEffect(() => {
    setGrid(computeGrid(data));
  }, [data]);

  const intensityColors = [
    "bg-[var(--color-border)]",
    "bg-emerald-300 dark:bg-emerald-800",
    "bg-emerald-500 dark:bg-emerald-600",
    "bg-emerald-700 dark:bg-emerald-400",
  ];

  if (!grid) {
    return (
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Activity</h3>
        </div>
        <div className="h-[120px]" />
      </div>
    );
  }

  const { weeks, monthPositions, totalSolves, activeDays } = grid;
  const gridWidth = weeks.length * CELL_STEP;
  const labelWidth = 30;

  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Activity</h3>
        <p className="text-xs text-[var(--color-text-muted)]">
          {totalSolves} solve{totalSolves !== 1 ? "s" : ""} &middot; {activeDays} active day{activeDays !== 1 ? "s" : ""}
        </p>
      </div>

      <div className="overflow-x-auto">
        {/* Month labels */}
        <div style={{ position: "relative", height: 18, marginLeft: labelWidth, width: gridWidth }}>
          {monthPositions.map((m, i) => (
            <span
              key={i}
              className="text-[10px] text-[var(--color-text-muted)]"
              style={{ position: "absolute", left: m.x, top: 0 }}
            >
              {m.label}
            </span>
          ))}
        </div>

        {/* Grid with day labels */}
        <div style={{ display: "flex" }} onMouseLeave={() => setTooltip(null)}>
          {/* Day labels */}
          <div style={{ width: labelWidth, flexShrink: 0 }}>
            {["", "Mon", "", "Wed", "", "Fri", ""].map((label, i) => (
              <div
                key={i}
                className="text-[10px] text-[var(--color-text-muted)]"
                style={{ height: CELL_STEP, display: "flex", alignItems: "center" }}
              >
                {label}
              </div>
            ))}
          </div>

          {/* Cells */}
          <div style={{ display: "flex", gap: CELL_GAP }}>
            {weeks.map((week, wi) => (
              <div key={wi} style={{ display: "flex", flexDirection: "column", gap: CELL_GAP }}>
                {Array.from({ length: 7 }).map((_, di) => {
                  const day = week.find((d) => d.dayOfWeek === di);
                  if (!day) {
                    return <div key={di} style={{ width: CELL_SIZE, height: CELL_SIZE }} />;
                  }

                  const intensity = getIntensity(day.count);
                  return (
                    <div
                      key={di}
                      className={`rounded-sm ${intensityColors[intensity]} transition-all hover:ring-1 hover:ring-[var(--color-text-muted)]`}
                      style={{ width: CELL_SIZE, height: CELL_SIZE, cursor: "pointer" }}
                      onMouseEnter={(e) => {
                        const rect = e.currentTarget.getBoundingClientRect();
                        setTooltip({
                          date: day.date,
                          count: day.count,
                          x: rect.left + rect.width / 2,
                          y: rect.top,
                        });
                      }}
                    />
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-3 flex items-center justify-end gap-1.5">
          <span className="text-[10px] text-[var(--color-text-muted)]">Less</span>
          {intensityColors.map((c, i) => (
            <div
              key={i}
              className={`rounded-sm ${c}`}
              style={{ width: CELL_SIZE, height: CELL_SIZE }}
            />
          ))}
          <span className="text-[10px] text-[var(--color-text-muted)]">More</span>
        </div>
      </div>

      {/* Tooltip */}
      {tooltip && (
        <div
          className="fixed z-50 rounded-md bg-[var(--color-text-primary)] px-2.5 py-1.5 text-[11px] font-medium text-[var(--color-background)] shadow-lg pointer-events-none whitespace-nowrap"
          style={{
            left: tooltip.x,
            top: tooltip.y - 32,
            transform: "translateX(-50%)",
          }}
        >
          <strong>{tooltip.count} solve{tooltip.count !== 1 ? "s" : ""}</strong> on {formatDate(tooltip.date)}
        </div>
      )}
    </div>
  );
}
