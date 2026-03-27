"use client";

import { useState, useRef, useCallback, useEffect } from "react";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface ERColumn {
  name: string;
  type: string;
  isPK: boolean;
  isFK: boolean;
  fkRef?: string; // "tableName.columnName"
  isNullable: boolean;
  isUnique: boolean;
}

interface EREntity {
  id: string;
  name: string;
  columns: ERColumn[];
  x: number;
  y: number;
}

interface ERRelationship {
  id: string;
  fromEntity: string;
  fromColumn: string;
  toEntity: string;
  toColumn: string;
  type: "one-to-one" | "one-to-many" | "many-to-many";
}

const COLUMN_TYPES = [
  "SERIAL",
  "INTEGER",
  "BIGINT",
  "SMALLINT",
  "VARCHAR(50)",
  "VARCHAR(100)",
  "VARCHAR(255)",
  "TEXT",
  "BOOLEAN",
  "DATE",
  "TIMESTAMP",
  "TIMESTAMPTZ",
  "DECIMAL(10,2)",
  "NUMERIC(12,2)",
  "REAL",
  "DOUBLE PRECISION",
  "UUID",
  "JSON",
  "JSONB",
];

const ENTITY_HEADER_H = 36;
const ENTITY_ROW_H = 28;
const ENTITY_MIN_W = 220;
const ENTITY_PAD = 12;

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function uid(): string {
  return Math.random().toString(36).slice(2, 10);
}

function emptyColumn(): ERColumn {
  return { name: "", type: "INTEGER", isPK: false, isFK: false, fkRef: "", isNullable: true, isUnique: false };
}

function entityHeight(entity: EREntity): number {
  return ENTITY_HEADER_H + entity.columns.length * ENTITY_ROW_H + ENTITY_PAD;
}

/* ------------------------------------------------------------------ */
/*  SQL Export                                                         */
/* ------------------------------------------------------------------ */

function exportSQL(entities: EREntity[]): string {
  const lines: string[] = [];
  for (const ent of entities) {
    const colDefs: string[] = [];
    const pks: string[] = [];
    const fks: string[] = [];
    for (const col of ent.columns) {
      if (!col.name) continue;
      let def = `  ${col.name} ${col.type}`;
      if (!col.isNullable) def += " NOT NULL";
      if (col.isUnique) def += " UNIQUE";
      colDefs.push(def);
      if (col.isPK) pks.push(col.name);
      if (col.isFK && col.fkRef) {
        const [refTable, refCol] = col.fkRef.split(".");
        if (refTable && refCol) {
          fks.push(`  FOREIGN KEY (${col.name}) REFERENCES ${refTable}(${refCol})`);
        }
      }
    }
    if (pks.length > 0) {
      colDefs.push(`  PRIMARY KEY (${pks.join(", ")})`);
    }
    const all = [...colDefs, ...fks].join(",\n");
    lines.push(`CREATE TABLE ${ent.name} (\n${all}\n);\n`);
  }
  return lines.join("\n");
}

/* ------------------------------------------------------------------ */
/*  SQL Import (basic parser)                                          */
/* ------------------------------------------------------------------ */

function importSQL(sql: string): EREntity[] {
  const entities: EREntity[] = [];
  // Match CREATE TABLE blocks
  const tableRe = /CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\(([\s\S]*?)\);/gi;
  let match: RegExpExecArray | null;
  let offsetX = 40;

  while ((match = tableRe.exec(sql)) !== null) {
    const tableName = match[1];
    const body = match[2];
    const columns: ERColumn[] = [];

    // Collect table-level PKs and FKs
    const tablePKs = new Set<string>();
    const tableFKs = new Map<string, string>(); // colName -> table.col

    const pkRe = /PRIMARY\s+KEY\s*\(([^)]+)\)/gi;
    let pkM: RegExpExecArray | null;
    while ((pkM = pkRe.exec(body)) !== null) {
      pkM[1].split(",").forEach((c) => tablePKs.add(c.trim()));
    }

    const fkRe = /FOREIGN\s+KEY\s*\((\w+)\)\s*REFERENCES\s+(\w+)\s*\((\w+)\)/gi;
    let fkM: RegExpExecArray | null;
    while ((fkM = fkRe.exec(body)) !== null) {
      tableFKs.set(fkM[1], `${fkM[2]}.${fkM[3]}`);
    }

    // Parse column lines
    const colLines = body.split(",").map((l) => l.trim()).filter(Boolean);
    for (const line of colLines) {
      // Skip table-level constraints
      if (/^(PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK|CONSTRAINT)\s/i.test(line)) continue;
      const colMatch = line.match(/^(\w+)\s+([A-Z][A-Z0-9_() ,]*)/i);
      if (!colMatch) continue;
      const colName = colMatch[1];
      const colType = colMatch[2].trim();
      const upper = line.toUpperCase();

      const isPK = upper.includes("PRIMARY KEY") || tablePKs.has(colName);
      const isNullable = !upper.includes("NOT NULL") && !isPK;
      const isUnique = upper.includes("UNIQUE");

      // Inline REFERENCES
      let isFK = tableFKs.has(colName);
      let fkRef = tableFKs.get(colName) || "";
      const inlineRef = line.match(/REFERENCES\s+(\w+)\s*\((\w+)\)/i);
      if (inlineRef) {
        isFK = true;
        fkRef = `${inlineRef[1]}.${inlineRef[2]}`;
      }

      columns.push({ name: colName, type: colType, isPK, isFK, fkRef, isNullable, isUnique });
    }

    entities.push({ id: uid(), name: tableName, columns, x: offsetX, y: 40 });
    offsetX += ENTITY_MIN_W + 60;
  }

  return entities;
}

/* ------------------------------------------------------------------ */
/*  Derive relationships from FK columns                               */
/* ------------------------------------------------------------------ */

function deriveRelationships(entities: EREntity[]): ERRelationship[] {
  const rels: ERRelationship[] = [];
  const entityNames = new Set(entities.map((e) => e.name));
  for (const ent of entities) {
    for (const col of ent.columns) {
      if (col.isFK && col.fkRef) {
        const [refTable, refCol] = col.fkRef.split(".");
        if (refTable && refCol && entityNames.has(refTable)) {
          rels.push({
            id: `${ent.name}.${col.name}->${refTable}.${refCol}`,
            fromEntity: ent.name,
            fromColumn: col.name,
            toEntity: refTable,
            toColumn: refCol,
            type: "one-to-many",
          });
        }
      }
    }
  }
  return rels;
}

/* ------------------------------------------------------------------ */
/*  Sub-components                                                     */
/* ------------------------------------------------------------------ */

/* ---------- Column Form Row ---------- */
function ColumnFormRow({
  col,
  index,
  onChange,
  onRemove,
  fkTargets,
}: {
  col: ERColumn;
  index: number;
  onChange: (i: number, c: ERColumn) => void;
  onRemove: (i: number) => void;
  fkTargets: string[];
}) {
  const set = (patch: Partial<ERColumn>) => onChange(index, { ...col, ...patch });
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-2">
      {/* Name */}
      <input
        className="w-28 rounded border border-[var(--color-border)] bg-[var(--color-surface)] px-2 py-1 text-xs text-[var(--color-text-primary)] outline-none focus:border-[var(--color-accent)]"
        placeholder="column name"
        value={col.name}
        onChange={(e) => set({ name: e.target.value.replace(/\s/g, "_") })}
      />
      {/* Type */}
      <select
        className="w-32 rounded border border-[var(--color-border)] bg-[var(--color-surface)] px-1 py-1 text-xs text-[var(--color-text-primary)] outline-none"
        value={col.type}
        onChange={(e) => set({ type: e.target.value })}
      >
        {COLUMN_TYPES.map((t) => (
          <option key={t} value={t}>
            {t}
          </option>
        ))}
      </select>
      {/* Constraints */}
      <label className="flex items-center gap-1 text-xs text-[var(--color-text-secondary)]">
        <input type="checkbox" checked={col.isPK} onChange={(e) => set({ isPK: e.target.checked, isNullable: e.target.checked ? false : col.isNullable })} />
        PK
      </label>
      <label className="flex items-center gap-1 text-xs text-[var(--color-text-secondary)]">
        <input type="checkbox" checked={col.isFK} onChange={(e) => set({ isFK: e.target.checked })} />
        FK
      </label>
      {col.isFK && (
        <select
          className="w-36 rounded border border-[var(--color-border)] bg-[var(--color-surface)] px-1 py-1 text-xs text-[var(--color-text-primary)] outline-none"
          value={col.fkRef || ""}
          onChange={(e) => set({ fkRef: e.target.value })}
        >
          <option value="">-- ref --</option>
          {fkTargets.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      )}
      <label className="flex items-center gap-1 text-xs text-[var(--color-text-secondary)]">
        <input type="checkbox" checked={!col.isNullable} onChange={(e) => set({ isNullable: !e.target.checked })} />
        NOT NULL
      </label>
      <label className="flex items-center gap-1 text-xs text-[var(--color-text-secondary)]">
        <input type="checkbox" checked={col.isUnique} onChange={(e) => set({ isUnique: e.target.checked })} />
        UNIQUE
      </label>
      <button
        onClick={() => onRemove(index)}
        className="ml-auto rounded px-1.5 py-0.5 text-xs text-red-400 hover:bg-red-500/10 hover:text-red-300"
        title="Remove column"
      >
        x
      </button>
    </div>
  );
}

/* ---------- Entity Form Modal ---------- */
function EntityFormModal({
  initial,
  allEntities,
  onSave,
  onCancel,
}: {
  initial: EREntity | null;
  allEntities: EREntity[];
  onSave: (e: EREntity) => void;
  onCancel: () => void;
}) {
  const isEdit = initial !== null;
  const [name, setName] = useState(initial?.name || "");
  const [columns, setColumns] = useState<ERColumn[]>(initial?.columns.length ? [...initial.columns.map((c) => ({ ...c }))] : [emptyColumn()]);

  // FK target options: "otherTable.column" (only PK columns for simplicity)
  const fkTargets: string[] = [];
  for (const ent of allEntities) {
    if (isEdit && ent.id === initial?.id) continue;
    for (const col of ent.columns) {
      fkTargets.push(`${ent.name}.${col.name}`);
    }
  }

  const updateColumn = (i: number, c: ERColumn) => {
    const next = [...columns];
    next[i] = c;
    setColumns(next);
  };
  const removeColumn = (i: number) => setColumns(columns.filter((_, idx) => idx !== i));
  const addColumn = () => setColumns([...columns, emptyColumn()]);

  const handleSave = () => {
    if (!name.trim()) return;
    const filtered = columns.filter((c) => c.name.trim());
    if (filtered.length === 0) return;
    onSave({
      id: initial?.id || uid(),
      name: name.trim().replace(/\s/g, "_"),
      columns: filtered,
      x: initial?.x ?? 40,
      y: initial?.y ?? 40,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onCancel}>
      <div
        className="max-h-[85vh] w-full max-w-xl overflow-y-auto rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">{isEdit ? "Edit Entity" : "New Entity"}</h3>

        {/* Table name */}
        <div className="mt-3">
          <label className="text-xs text-[var(--color-text-secondary)]">Table Name</label>
          <input
            className="mt-1 block w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-1.5 text-sm text-[var(--color-text-primary)] outline-none focus:border-[var(--color-accent)]"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. users"
            autoFocus
          />
        </div>

        {/* Columns */}
        <div className="mt-4">
          <div className="flex items-center justify-between">
            <label className="text-xs text-[var(--color-text-secondary)]">Columns</label>
            <button onClick={addColumn} className="rounded bg-[var(--color-accent)] px-2 py-0.5 text-xs font-medium text-white hover:opacity-90">
              + Column
            </button>
          </div>
          <div className="mt-2 space-y-2">
            {columns.map((col, i) => (
              <ColumnFormRow key={i} col={col} index={i} onChange={updateColumn} onRemove={removeColumn} fkTargets={fkTargets} />
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="mt-5 flex justify-end gap-2">
          <button onClick={onCancel} className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]">
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="rounded bg-[var(--color-accent)] px-4 py-1.5 text-xs font-medium text-white hover:opacity-90"
          >
            {isEdit ? "Update" : "Create"}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ---------- SQL Panel (export / import) ---------- */
function SQLPanel({ mode, sql, onImport, onClose }: { mode: "export" | "import"; sql: string; onImport: (sql: string) => void; onClose: () => void }) {
  const [text, setText] = useState(mode === "export" ? sql : "");
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onClose}>
      <div
        className="max-h-[85vh] w-full max-w-2xl overflow-y-auto rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">{mode === "export" ? "Export SQL DDL" : "Import SQL DDL"}</h3>
          {mode === "export" && (
            <button onClick={copyToClipboard} className="rounded bg-[var(--color-accent)] px-3 py-1 text-xs font-medium text-white hover:opacity-90">
              {copied ? "Copied!" : "Copy"}
            </button>
          )}
        </div>
        <textarea
          className="mt-3 block h-72 w-full resize-y rounded border border-[var(--color-border)] bg-[var(--color-background)] p-3 font-mono text-xs text-[var(--color-text-primary)] outline-none focus:border-[var(--color-accent)]"
          value={text}
          onChange={(e) => setText(e.target.value)}
          readOnly={mode === "export"}
          placeholder={mode === "import" ? "Paste CREATE TABLE statements here..." : ""}
          spellCheck={false}
        />
        <div className="mt-4 flex justify-end gap-2">
          <button onClick={onClose} className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]">
            Close
          </button>
          {mode === "import" && (
            <button
              onClick={() => {
                onImport(text);
                onClose();
              }}
              className="rounded bg-[var(--color-accent)] px-4 py-1.5 text-xs font-medium text-white hover:opacity-90"
            >
              Import
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main Component                                                     */
/* ------------------------------------------------------------------ */

export type { EREntity, ERColumn, ERRelationship };

export default function ERBuilder({ initialEntities, onEntitiesChange }: { initialEntities?: EREntity[]; onEntitiesChange?: (entities: EREntity[]) => void } = {}) {
  const [entities, setEntities] = useState<EREntity[]>(initialEntities || []);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editEntity, setEditEntity] = useState<EREntity | null>(null);
  const [sqlPanel, setSqlPanel] = useState<"export" | "import" | null>(null);

  // Sync with parent
  useEffect(() => {
    if (onEntitiesChange) onEntitiesChange(entities);
  }, [entities, onEntitiesChange]);

  // Reset when initialEntities changes (new challenge selected)
  useEffect(() => {
    if (initialEntities) setEntities(initialEntities);
  }, [initialEntities]);

  // Drag state
  const svgRef = useRef<SVGSVGElement>(null);
  const dragRef = useRef<{ entityId: string; offsetX: number; offsetY: number } | null>(null);

  const relationships = deriveRelationships(entities);

  /* ---- CRUD ---- */
  const saveEntity = (ent: EREntity) => {
    setEntities((prev) => {
      const idx = prev.findIndex((e) => e.id === ent.id);
      if (idx >= 0) {
        const next = [...prev];
        next[idx] = ent;
        return next;
      }
      // auto-position new entity if it would overlap
      const newEnt = { ...ent };
      if (prev.length > 0) {
        const maxX = Math.max(...prev.map((e) => e.x + ENTITY_MIN_W));
        newEnt.x = maxX + 40;
        newEnt.y = 40;
      }
      return [...prev, newEnt];
    });
    setShowForm(false);
    setEditEntity(null);
  };

  const deleteEntity = (id: string) => {
    setEntities((prev) => prev.filter((e) => e.id !== id));
    if (selectedId === id) setSelectedId(null);
  };

  const clearAll = () => {
    setEntities([]);
    setSelectedId(null);
  };

  /* ---- Drag & Drop ---- */
  const handleMouseDown = useCallback(
    (entityId: string, e: React.MouseEvent) => {
      e.stopPropagation();
      const ent = entities.find((en) => en.id === entityId);
      if (!ent || !svgRef.current) return;
      const pt = svgRef.current.getBoundingClientRect();
      dragRef.current = {
        entityId,
        offsetX: e.clientX - pt.left - ent.x,
        offsetY: e.clientY - pt.top - ent.y,
      };
      setSelectedId(entityId);
    },
    [entities],
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!dragRef.current || !svgRef.current) return;
      const pt = svgRef.current.getBoundingClientRect();
      const nx = e.clientX - pt.left - dragRef.current.offsetX;
      const ny = e.clientY - pt.top - dragRef.current.offsetY;
      setEntities((prev) =>
        prev.map((en) => (en.id === dragRef.current!.entityId ? { ...en, x: Math.max(0, nx), y: Math.max(0, ny) } : en)),
      );
    },
    [],
  );

  const handleMouseUp = useCallback(() => {
    dragRef.current = null;
  }, []);

  /* ---- Import handler ---- */
  const handleImport = (sql: string) => {
    const imported = importSQL(sql);
    if (imported.length > 0) {
      setEntities(imported);
      setSelectedId(null);
    }
  };

  /* ---- Relationship line positions ---- */
  const getRelLine = (rel: ERRelationship) => {
    const from = entities.find((e) => e.name === rel.fromEntity);
    const to = entities.find((e) => e.name === rel.toEntity);
    if (!from || !to) return null;
    const fromColIdx = from.columns.findIndex((c) => c.name === rel.fromColumn);
    const toColIdx = to.columns.findIndex((c) => c.name === rel.toColumn);
    if (fromColIdx < 0 || toColIdx < 0) return null;

    const fromCx = from.x + ENTITY_MIN_W;
    const fromCy = from.y + ENTITY_HEADER_H + fromColIdx * ENTITY_ROW_H + ENTITY_ROW_H / 2;
    const toCx = to.x;
    const toCy = to.y + ENTITY_HEADER_H + toColIdx * ENTITY_ROW_H + ENTITY_ROW_H / 2;

    // Decide which side to connect from/to
    const fromRight = from.x + ENTITY_MIN_W;
    const fromLeft = from.x;
    const toRight = to.x + ENTITY_MIN_W;
    const toLeft = to.x;

    let x1: number, x2: number;
    if (fromRight < toLeft) {
      x1 = fromRight;
      x2 = toLeft;
    } else if (toRight < fromLeft) {
      x1 = fromLeft;
      x2 = toRight;
    } else {
      x1 = fromRight;
      x2 = toRight;
    }

    const y1 = fromCy;
    const y2 = toCy;

    return { x1, y1, x2, y2 };
  };

  /* ---- SVG Entity rendering ---- */
  const renderEntity = (ent: EREntity) => {
    const isSelected = selectedId === ent.id;
    const h = entityHeight(ent);
    return (
      <g key={ent.id} onMouseDown={(e) => handleMouseDown(ent.id, e)} onClick={() => setSelectedId(ent.id)} style={{ cursor: "grab" }}>
        {/* Shadow */}
        <rect x={ent.x + 2} y={ent.y + 2} width={ENTITY_MIN_W} height={h} rx={8} fill="rgba(0,0,0,0.12)" />
        {/* Body */}
        <rect
          x={ent.x}
          y={ent.y}
          width={ENTITY_MIN_W}
          height={h}
          rx={8}
          fill="var(--color-surface)"
          stroke={isSelected ? "var(--color-accent)" : "var(--color-border)"}
          strokeWidth={isSelected ? 2 : 1}
        />
        {/* Header */}
        <rect x={ent.x} y={ent.y} width={ENTITY_MIN_W} height={ENTITY_HEADER_H} rx={8} fill="var(--color-accent)" />
        {/* Bottom corners of header need to be square */}
        <rect x={ent.x} y={ent.y + ENTITY_HEADER_H - 8} width={ENTITY_MIN_W} height={8} fill="var(--color-accent)" />
        <text x={ent.x + 10} y={ent.y + 23} fontSize={13} fontWeight={600} fill="white">
          {ent.name}
        </text>
        {/* Columns */}
        {ent.columns.map((col, i) => {
          const cy = ent.y + ENTITY_HEADER_H + i * ENTITY_ROW_H;
          const isLast = i === ent.columns.length - 1;
          return (
            <g key={i}>
              {i > 0 && <line x1={ent.x + 8} y1={cy} x2={ent.x + ENTITY_MIN_W - 8} y2={cy} stroke="var(--color-border)" strokeWidth={0.5} />}
              {/* PK icon */}
              {col.isPK && (
                <text x={ent.x + 8} y={cy + 18} fontSize={11}>
                  {"🔑"}
                </text>
              )}
              {/* Column name */}
              <text x={ent.x + (col.isPK ? 26 : 10)} y={cy + 18} fontSize={12} fill="var(--color-text-primary)" fontFamily="monospace">
                {col.name}
              </text>
              {/* Column type */}
              <text x={ent.x + ENTITY_MIN_W - 10} y={cy + 18} fontSize={10} fill="var(--color-text-muted)" textAnchor="end" fontFamily="monospace">
                {col.type}
                {col.isFK && col.fkRef ? ` -> ${col.fkRef}` : ""}
              </text>
            </g>
          );
        })}
      </g>
    );
  };

  /* ---- Render ---- */
  return (
    <div className="mt-6">
      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
        <button
          onClick={() => {
            setEditEntity(null);
            setShowForm(true);
          }}
          className="rounded bg-[var(--color-accent)] px-3 py-1.5 text-xs font-medium text-white hover:opacity-90"
        >
          + Add Entity
        </button>
        {selectedId && (
          <>
            <button
              onClick={() => {
                const ent = entities.find((e) => e.id === selectedId);
                if (ent) {
                  setEditEntity(ent);
                  setShowForm(true);
                }
              }}
              className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]"
            >
              Edit Selected
            </button>
            <button
              onClick={() => deleteEntity(selectedId)}
              className="rounded border border-red-500/30 px-3 py-1.5 text-xs text-red-400 hover:bg-red-500/10"
            >
              Delete Selected
            </button>
          </>
        )}
        <div className="mx-2 h-5 w-px bg-[var(--color-border)]" />
        <button
          onClick={() => setSqlPanel("export")}
          disabled={entities.length === 0}
          className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)] disabled:opacity-40"
        >
          Export SQL
        </button>
        <button
          onClick={() => setSqlPanel("import")}
          className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]"
        >
          Import SQL
        </button>
        <button
          onClick={clearAll}
          disabled={entities.length === 0}
          className="rounded border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-border)] disabled:opacity-40"
        >
          Clear All
        </button>
        <span className="ml-auto text-xs text-[var(--color-text-muted)]">
          {entities.length} {entities.length === 1 ? "entity" : "entities"}
          {relationships.length > 0 && ` / ${relationships.length} ${relationships.length === 1 ? "relationship" : "relationships"}`}
        </span>
      </div>

      {/* Canvas */}
      <div className="mt-3 overflow-auto rounded-xl border border-[var(--color-border)] bg-[var(--color-background)]" style={{ height: 520 }}>
        {entities.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-sm text-[var(--color-text-muted)]">
            <svg width="48" height="48" fill="none" viewBox="0 0 24 24" className="mb-3 opacity-40">
              <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.5" />
              <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.5" />
              <rect x="8" y="14" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.5" />
              <line x1="10" y1="6.5" x2="14" y2="6.5" stroke="currentColor" strokeWidth="1.5" />
              <line x1="11.5" y1="10" x2="11.5" y2="14" stroke="currentColor" strokeWidth="1.5" />
            </svg>
            <p>No entities yet. Click <strong>+ Add Entity</strong> to get started,</p>
            <p>or use <strong>Import SQL</strong> to load from DDL.</p>
          </div>
        ) : (
          <svg
            ref={svgRef}
            width="100%"
            height="100%"
            style={{ minWidth: 900, minHeight: 500 }}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onClick={() => setSelectedId(null)}
          >
            {/* Grid */}
            <defs>
              <pattern id="er-grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="1" cy="1" r="0.5" fill="var(--color-border)" opacity="0.4" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#er-grid)" />

            {/* Relationship lines */}
            {relationships.map((rel) => {
              const coords = getRelLine(rel);
              if (!coords) return null;
              const { x1, y1, x2, y2 } = coords;
              const mx = (x1 + x2) / 2;
              return (
                <g key={rel.id}>
                  <path
                    d={`M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`}
                    fill="none"
                    stroke="var(--color-accent)"
                    strokeWidth={1.5}
                    strokeDasharray="6 3"
                    opacity={0.7}
                  />
                  {/* Arrow at destination */}
                  <circle cx={x2} cy={y2} r={4} fill="var(--color-accent)" opacity={0.7} />
                  {/* Label */}
                  <text x={mx} y={(y1 + y2) / 2 - 6} fontSize={9} fill="var(--color-text-muted)" textAnchor="middle">
                    {rel.fromColumn} {"-> "} {rel.toColumn}
                  </text>
                </g>
              );
            })}

            {/* Entities */}
            {entities.map(renderEntity)}
          </svg>
        )}
      </div>

      {/* Entity Form Modal */}
      {showForm && (
        <EntityFormModal
          initial={editEntity}
          allEntities={entities}
          onSave={saveEntity}
          onCancel={() => {
            setShowForm(false);
            setEditEntity(null);
          }}
        />
      )}

      {/* SQL Panel */}
      {sqlPanel && (
        <SQLPanel mode={sqlPanel} sql={exportSQL(entities)} onImport={handleImport} onClose={() => setSqlPanel(null)} />
      )}
    </div>
  );
}
