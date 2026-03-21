"use client";

import { useState, memo } from "react";

interface Column {
  name: string;
  type: string;
  isPrimaryKey: boolean;
  isForeignKey: boolean;
  references?: string;
  nullable: boolean;
}

interface Table {
  name: string;
  columns: Column[];
  sampleRows: Record<string, unknown>[];
}

interface SchemaViewerProps {
  tables: Table[];
}

export const SchemaViewer = memo(function SchemaViewer({ tables }: SchemaViewerProps) {
  const [expandedTable, setExpandedTable] = useState<string | null>(
    tables[0]?.name ?? null
  );
  const [showSample, setShowSample] = useState<string | null>(null);

  return (
    <div className="space-y-2">
      <h3 className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]">
        Schema
      </h3>
      {tables.map((table) => (
        <div
          key={table.name}
          className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)]"
        >
          {/* Table header */}
          <button
            onClick={() =>
              setExpandedTable(
                expandedTable === table.name ? null : table.name
              )
            }
            aria-label={`${expandedTable === table.name ? "Collapse" : "Expand"} table ${table.name} (${table.columns.length} columns)`}
            aria-expanded={expandedTable === table.name}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs font-medium transition-colors hover:bg-[var(--color-background)]"
          >
            <svg
              className={`h-3 w-3 text-[var(--color-text-muted)] transition-transform ${
                expandedTable === table.name ? "rotate-90" : ""
              }`}
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M9 5l7 7-7 7z" />
            </svg>
            <span className="font-mono text-[var(--color-text-primary)]">
              {table.name}
            </span>
            <span className="text-[var(--color-text-muted)]">
              ({table.columns.length})
            </span>
          </button>

          {/* Columns */}
          {expandedTable === table.name && (
            <div className="border-t border-[var(--color-border)] px-3 py-2">
              {table.columns.map((col) => (
                <div
                  key={col.name}
                  className="flex items-center gap-2 py-0.5 font-mono text-xs"
                >
                  {/* Key indicators */}
                  {col.isPrimaryKey && (
                    <span className="text-amber-500" title="Primary Key">
                      🔑
                    </span>
                  )}
                  {col.isForeignKey && (
                    <span className="text-blue-500" title={`FK → ${col.references}`}>
                      🔗
                    </span>
                  )}
                  {!col.isPrimaryKey && !col.isForeignKey && (
                    <span className="w-4" />
                  )}

                  <span className="text-[var(--color-text-primary)]">
                    {col.name}
                  </span>
                  <span className="text-[var(--color-text-muted)]">
                    {col.type}
                  </span>
                  {col.nullable && (
                    <span className="text-[var(--color-text-muted)] text-[10px]">
                      NULL
                    </span>
                  )}
                </div>
              ))}

              {/* Sample data toggle */}
              {table.sampleRows.length > 0 && (
                <button
                  onClick={() =>
                    setShowSample(
                      showSample === table.name ? null : table.name
                    )
                  }
                  aria-label={`${showSample === table.name ? "Hide" : "Show"} sample data for ${table.name}`}
                  aria-expanded={showSample === table.name}
                  className="mt-2 text-[10px] font-medium text-[var(--color-accent)] hover:underline"
                >
                  {showSample === table.name
                    ? "Hide sample"
                    : `Show ${table.sampleRows.length} sample rows`}
                </button>
              )}

              {showSample === table.name && (
                <div className="mt-2 overflow-x-auto">
                  <table className="w-full text-[10px]">
                    <thead>
                      <tr>
                        {table.columns.map((col) => (
                          <th
                            key={col.name}
                            className="px-1 py-0.5 text-left text-[var(--color-text-muted)]"
                          >
                            {col.name}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {table.sampleRows.map((row, i) => (
                        <tr key={i}>
                          {table.columns.map((col) => (
                            <td
                              key={col.name}
                              className="px-1 py-0.5 text-[var(--color-text-secondary)]"
                            >
                              {row[col.name] === null ? (
                                <span className="italic text-[var(--color-text-muted)]">
                                  NULL
                                </span>
                              ) : (
                                String(row[col.name])
                              )}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
});
