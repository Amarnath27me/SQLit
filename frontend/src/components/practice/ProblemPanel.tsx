"use client";

import { Badge } from "@/components/ui/Badge";
import { SchemaViewer } from "./SchemaViewer";
import type { Difficulty } from "@/types";

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

interface ProblemPanelProps {
  title: string;
  difficulty: Difficulty;
  acceptanceRate: number;
  description: string;
  conceptTags: string[];
  schema: Table[];
  dataset: string;
  dialect: string;
  onDatasetChange: (dataset: string) => void;
  onDialectChange: (dialect: string) => void;
}

export function ProblemPanel({
  title,
  difficulty,
  acceptanceRate,
  description,
  conceptTags,
  schema,
  dataset,
  dialect,
  onDatasetChange,
  onDialectChange,
}: ProblemPanelProps) {
  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b border-[var(--color-border)] bg-[var(--color-surface)] p-4">
        <div className="flex items-center gap-2">
          <Badge variant={difficulty}>{difficulty}</Badge>
          <span className="text-xs text-[var(--color-text-muted)]">
            {acceptanceRate}% acceptance
          </span>
        </div>
        <h2 className="mt-2 text-base font-semibold text-[var(--color-text-primary)]">
          {title}
        </h2>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {/* Description */}
          <div>
            <p className="text-sm leading-relaxed text-[var(--color-text-secondary)]">
              {description}
            </p>
          </div>

          {/* Concept tags — only shown for easy problems to guide beginners */}
          {difficulty === "easy" && conceptTags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {conceptTags.map((tag) => (
                <Badge key={tag} variant="default">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {/* Selectors */}
          <div className="flex gap-2">
            <select
              value={dataset}
              onChange={(e) => onDatasetChange(e.target.value)}
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-2 py-1 text-xs text-[var(--color-text-primary)]"
            >
              <option value="ecommerce">E-Commerce</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
            </select>
            <select
              value={dialect}
              onChange={(e) => onDialectChange(e.target.value)}
              className="rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] px-2 py-1 text-xs text-[var(--color-text-primary)]"
            >
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
            </select>
          </div>

          {/* Schema */}
          <SchemaViewer tables={schema} />
        </div>
      </div>
    </div>
  );
}
