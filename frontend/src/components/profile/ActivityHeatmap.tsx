"use client";

import { useState, useEffect, useRef } from "react";

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
const DAY_LABELS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

interface DayCell {
  date: string;
  count: number;
  dayOfWeek: number;
}

interface MonthLabel {
  label: string;
  weekIndex: number;
}

const CELL_SIZE = 12;
const CELL_GAP = 3;
const CELL_STEP = CELL_SIZE + CELL_GAP; // 15px per cell
const LEFT_LABEL_WIDTH = 28;

function computeGrid(data: Record<string, number>) {
  const today = new Date();
  const start = new Date(today);
  start.setDate(start.getDate() - 364);
  // Align to start of week (Sunday)
  start.setDate(start.getDate() - start.getDay());

  const weeks: DayCell[][] = [];
  const monthLabels: MonthLabel[] = [];
  let currentWeek: DayCell[] = [];
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

    if (month !== lastMonth && dayOfWeek <= 3) {
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

function formatDate(dateStr: string): string {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" });
}

export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  const [tooltip, setTooltip] = useState<{ date: string; count: number; x: number; y: number } | null>(null);
  const [grid, setGrid] = useState<ReturnType<typeof computeGrid> | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

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

  const { weeks, monthLabels, totalSolves, activeDays } = grid;
  const gridWidth = weeks.length * CELL_STEP;

  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">Activity</h3>
        <p className="text-xs text-[var(--color-text-muted)]">
          {totalSolves} solve{totalSolves !== 1 ? "s" : ""} in the last year &middot; {activeDays} active day{activeDays !== 1 ? "s" : ""}
        </p>
      </div>

      <div className="overflow-x-auto" ref={containerRef}>
        <div style={{ minWidth: gridWidth + LEFT_LABEL_WIDTH + 16 }}>
          {/* Month labels row */}
          <div className="flex" style={{ paddingLeft: LEFT_LABEL_WIDTH, marginBottom: 6 }}>
            {monthLabels.map((m, i) => {
              // Only show label if there's enough space (skip if too close to next)
              const nextWeekIndex = i < monthLabels.length - 1 ? monthLabels[i + 1].weekIndex : weeks.length;
              const span = nextWeekIndex - m.weekIndex;
              if (span < 2) return null;

              return (
                <span
                  key={i}
                  className="text-[11px] text-[var(--color-text-muted)] font-medium"
                  style={{
                    position: "absolute",
                    left: LEFT_LABEL_WIDTH + m.weekIndex * CELL_STEP,
                  }}
                >
                  {m.label}
                </span>
              );
            })}
            {/* Spacer for absolute-positioned labels */}
            <div style={{ height: 16 }} />
          </div>

          {/* Grid + day labels */}
          <div className="flex" style={{ position: "relative" }}>
            {/* Day-of-week labels */}
            <div className="shrink-0 flex flex-col" style={{ width: LEFT_LABEL_WIDTH }}>
              {DAY_LABELS.map((label, i) => (
                <div
                  key={i}
                  className="text-[10px] text-[var(--color-text-muted)] flex items-center"
                  style={{ height: CELL_STEP }}
                >
                  {i % 2 === 1 ? label : ""}
                </div>
              ))}
            </div>

            {/* Heatmap grid */}
            <div
              className="flex"
              style={{ gap: CELL_GAP }}
              onMouseLeave={() => setTooltip(null)}
            >
              {weeks.map((week, wi) => (
                <div key={wi} className="flex flex-col" style={{ gap: CELL_GAP }}>
                  {Array.from({ length: 7 }).map((_, di) => {
                    const day = week.find((d) => d.dayOfWeek === di);
                    if (!day) {
                      return (
                        <div
                          key={di}
                          style={{ width: CELL_SIZE, height: CELL_SIZE }}
                        />
                      );
                    }

                    const intensity = getIntensity(day.count);
                    return (
                      <div
                        key={di}
                        className={`rounded-sm ${intensityColors[intensity]} cursor-pointer transition-all hover:ring-1 hover:ring-[var(--color-text-muted)]`}
                        style={{ width: CELL_SIZE, height: CELL_SIZE }}
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
                style={{ width: CELL_SIZE - 1, height: CELL_SIZE - 1 }}
              />
            ))}
            <span className="text-[10px] text-[var(--color-text-muted)]">More</span>
          </div>
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
