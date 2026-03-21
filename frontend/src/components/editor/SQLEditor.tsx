"use client";

import { useRef, useCallback } from "react";
import Editor, { OnMount, BeforeMount } from "@monaco-editor/react";
import type { editor, languages, Position, IRange } from "monaco-editor";

interface SQLEditorProps {
  value: string;
  onChange: (value: string) => void;
  onRun: () => void;
  dialect: "postgresql" | "mysql";
  readOnly?: boolean;
  tables?: { name: string; columns: string[] }[];
  guestLocked?: boolean;
}

export function SQLEditor({
  value,
  onChange,
  onRun,
  dialect,
  readOnly = false,
  tables = [],
  guestLocked = false,
}: SQLEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  const handleMount: OnMount = useCallback(
    (editor, monaco) => {
      editorRef.current = editor;

      // Ctrl+Enter / Cmd+Enter to run
      editor.addAction({
        id: "run-query",
        label: "Run Query",
        keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
        run: () => {
          if (!guestLocked) onRun();
        },
      });

      // Register table/column completions
      if (tables.length > 0) {
        monaco.languages.registerCompletionItemProvider("sql", {
          provideCompletionItems: (model: editor.ITextModel, position: Position): languages.ProviderResult<languages.CompletionList> => {
            const word = model.getWordUntilPosition(position);
            const range: IRange = {
              startLineNumber: position.lineNumber,
              endLineNumber: position.lineNumber,
              startColumn: word.startColumn,
              endColumn: word.endColumn,
            };

            const suggestions = [
              ...tables.map((t) => ({
                label: t.name,
                kind: monaco.languages.CompletionItemKind.Class,
                insertText: t.name,
                range,
                detail: "Table",
              })),
              ...tables.flatMap((t) =>
                t.columns.map((col) => ({
                  label: col,
                  kind: monaco.languages.CompletionItemKind.Field,
                  insertText: col,
                  range,
                  detail: `${t.name}.${col}`,
                }))
              ),
            ];

            return { suggestions };
          },
        });
      }

      editor.focus();
    },
    [onRun, tables, guestLocked]
  );

  return (
    <div className="relative flex h-full flex-col">
      {/* Dialect indicator + Run button */}
      <div className="flex items-center gap-2 border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2">
        <span className="text-xs font-medium uppercase tracking-wider text-[var(--color-text-muted)]" aria-label={`SQL dialect: ${dialect}`}>
          {dialect}
        </span>
        <div className="flex-1" />
        <button
          onClick={guestLocked ? undefined : onRun}
          disabled={guestLocked}
          aria-label="Run SQL query (Ctrl+Enter)"
          className={`flex items-center gap-1.5 rounded-md px-3 py-1 text-xs font-medium text-white transition-colors ${
            guestLocked
              ? "cursor-not-allowed bg-gray-400 dark:bg-gray-600"
              : "bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)]"
          }`}
        >
          <svg className="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z" />
          </svg>
          Run
          <kbd className="ml-1 rounded bg-white/20 px-1 py-0.5 text-[10px]">
            ⌘↵
          </kbd>
        </button>
      </div>

      {/* Editor */}
      <div className="flex-1">
        <Editor
          defaultLanguage="sql"
          value={value}
          onChange={(v) => onChange(v ?? "")}
          onMount={handleMount}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            fontFamily: "var(--font-geist-mono), 'Fira Code', monospace",
            lineNumbers: "on",
            renderLineHighlight: "line",
            scrollBeyondLastLine: false,
            wordWrap: "on",
            tabSize: 2,
            automaticLayout: true,
            readOnly,
            padding: { top: 12 },
            suggestOnTriggerCharacters: true,
          }}
        />
      </div>

      {/* Guest lock overlay */}
      {guestLocked && (
        <div className="absolute inset-0 top-[41px] flex items-center justify-center bg-black/40 backdrop-blur-[2px]">
          <div role="dialog" aria-modal="true" aria-describedby="guest-lock-description" className="mx-4 max-w-sm rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-center shadow-xl">
            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-[var(--color-accent)]/10">
              <svg className="h-6 w-6 text-[var(--color-accent)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
              Sign in to Run Queries
            </h3>
            <p id="guest-lock-description" className="mt-1 text-xs text-[var(--color-text-muted)]">
              Create a free account to execute SQL, track progress, and earn XP.
            </p>
            <a
              href="/auth/login"
              className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-[var(--color-accent)] px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
            >
              Sign In
              <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
