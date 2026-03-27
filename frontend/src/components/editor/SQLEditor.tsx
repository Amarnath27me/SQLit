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
}

export function SQLEditor({
  value,
  onChange,
  onRun,
  dialect,
  readOnly = false,
  tables = [],
}: SQLEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  const handleBeforeMount: BeforeMount = useCallback((monaco) => {
    monaco.editor.defineTheme("sqlit-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [],
      colors: {
        "editor.background": "#0A0A0A",
        "editor.lineHighlightBackground": "#171717",
        "editorGutter.background": "#0A0A0A",
        "editorLineNumber.foreground": "#4B5563",
        "editorLineNumber.activeForeground": "#9CA3AF",
        "editor.selectionBackground": "#2563EB44",
        "editorCursor.foreground": "#3B82F6",
        "editorWidget.background": "#171717",
        "editorWidget.border": "#262626",
        "editorSuggestWidget.background": "#171717",
        "editorSuggestWidget.border": "#262626",
        "editorSuggestWidget.selectedBackground": "#262626",
      },
    });
  }, []);

  const handleMount: OnMount = useCallback(
    (editor, monaco) => {
      editorRef.current = editor;

      // Ctrl+Enter / Cmd+Enter to run
      editor.addAction({
        id: "run-query",
        label: "Run Query",
        keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
        run: () => {
          onRun();
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
    [onRun, tables]
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
          onClick={onRun}
          aria-label="Run SQL query (Ctrl+Enter)"
          className="flex items-center gap-1.5 rounded-md bg-[var(--color-accent)] px-3 py-1 text-xs font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
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
      <div className="flex-1 min-h-0">
        <Editor
          defaultLanguage="sql"
          value={value}
          onChange={(v) => onChange(v ?? "")}
          beforeMount={handleBeforeMount}
          onMount={handleMount}
          theme="sqlit-dark"
          loading={
            <div className="flex h-full items-center justify-center bg-[var(--color-background)]">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-[var(--color-accent)] border-t-transparent" />
            </div>
          }
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            fontFamily: "'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace",
            lineNumbers: "on",
            renderLineHighlight: "line",
            scrollBeyondLastLine: false,
            wordWrap: "on",
            tabSize: 2,
            automaticLayout: true,
            readOnly,
            padding: { top: 12, bottom: 12 },
            suggestOnTriggerCharacters: true,
            lineDecorationsWidth: 8,
            folding: false,
            glyphMargin: false,
            contextmenu: true,
            smoothScrolling: true,
            cursorBlinking: "smooth",
            cursorSmoothCaretAnimation: "on",
          }}
        />
      </div>

    </div>
  );
}
