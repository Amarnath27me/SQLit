"use client";

interface ResultTableProps {
  columns: string[];
  rows: unknown[][];
  highlightRows?: number[];
  highlightColumns?: string[];
  maxHeight?: string;
}

export function ResultTable({
  columns,
  rows,
  highlightRows = [],
  highlightColumns = [],
  maxHeight = "300px",
}: ResultTableProps) {
  if (columns.length === 0) {
    return (
      <p className="py-4 text-center text-sm text-[var(--color-text-muted)]">
        No results to display.
      </p>
    );
  }

  return (
    <div
      className="overflow-auto rounded-md border border-[var(--color-border)]"
      style={{ maxHeight }}
    >
      <table className="w-full text-left text-sm">
        <thead className="sticky top-0 bg-[var(--color-surface)]">
          <tr>
            <th className="border-b border-[var(--color-border)] px-3 py-2 text-xs font-medium text-[var(--color-text-muted)]">
              #
            </th>
            {columns.map((col) => (
              <th
                key={col}
                className={`border-b border-[var(--color-border)] px-3 py-2 text-xs font-medium ${
                  highlightColumns.includes(col)
                    ? "text-[var(--color-error)]"
                    : "text-[var(--color-text-muted)]"
                }`}
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="font-mono text-xs">
          {rows.map((row, i) => (
            <tr
              key={i}
              className={
                highlightRows.includes(i)
                  ? "bg-red-50 dark:bg-red-950/30"
                  : i % 2 === 0
                  ? "bg-[var(--color-surface)]"
                  : "bg-[var(--color-background)]"
              }
            >
              <td className="px-3 py-1.5 text-[var(--color-text-muted)]">
                {i + 1}
              </td>
              {row.map((cell, j) => (
                <td
                  key={j}
                  className={`px-3 py-1.5 ${
                    highlightRows.includes(i) &&
                    highlightColumns.includes(columns[j])
                      ? "font-semibold text-[var(--color-error)]"
                      : "text-[var(--color-text-primary)]"
                  }`}
                >
                  {cell === null ? (
                    <span className="italic text-[var(--color-text-muted)]">
                      NULL
                    </span>
                  ) : (
                    String(cell)
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
