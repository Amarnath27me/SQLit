"use client";

import { useRef, useCallback, useState, useSyncExternalStore } from "react";

// ---------------------------------------------------------------------------
// useMediaQuery – SSR-safe hook using useSyncExternalStore
// ---------------------------------------------------------------------------
function useMediaQuery(query: string): boolean {
  const subscribe = useCallback(
    (callback: () => void) => {
      const mql = window.matchMedia(query);
      mql.addEventListener("change", callback);
      return () => mql.removeEventListener("change", callback);
    },
    [query]
  );

  const getSnapshot = useCallback(() => window.matchMedia(query).matches, [query]);

  // During SSR / first hydration, assume desktop (false = not mobile)
  const getServerSnapshot = useCallback(() => false, []);

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
interface ResizablePanelProps {
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
  defaultLeftWidth?: number;
  defaultRightWidth?: number;
  minWidth?: number;
}

type MobileTab = "problem" | "editor" | "output";

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
export function ResizablePanel({
  left,
  center,
  right,
  defaultLeftWidth = 320,
  defaultRightWidth = 384,
  minWidth = 200,
}: ResizablePanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [leftWidth, setLeftWidth] = useState(defaultLeftWidth);
  const [rightWidth, setRightWidth] = useState(defaultRightWidth);
  const [activeTab, setActiveTab] = useState<MobileTab>("editor");

  const isMobile = useMediaQuery("(max-width: 767px)");

  // ---- Desktop drag-resize logic (unchanged) ----
  const startResize = useCallback(
    (side: "left" | "right") => {
      const onMouseMove = (e: MouseEvent) => {
        if (!containerRef.current) return;
        const rect = containerRef.current.getBoundingClientRect();

        if (side === "left") {
          const newWidth = Math.max(minWidth, e.clientX - rect.left);
          setLeftWidth(Math.min(newWidth, rect.width - rightWidth - minWidth));
        } else {
          const newWidth = Math.max(minWidth, rect.right - e.clientX);
          setRightWidth(Math.min(newWidth, rect.width - leftWidth - minWidth));
        }
      };

      const onMouseUp = () => {
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", onMouseUp);
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
      };

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
    },
    [leftWidth, rightWidth, minWidth]
  );

  // ---- Mobile layout ----
  if (isMobile) {
    const tabs: { key: MobileTab; label: string }[] = [
      { key: "problem", label: "Problem" },
      { key: "editor", label: "Editor" },
      { key: "output", label: "Output" },
    ];

    return (
      <div className="flex h-full w-full flex-col overflow-hidden">
        {/* Tab bar */}
        <div
          className="flex shrink-0 border-b"
          style={{
            borderColor: "var(--color-border)",
            backgroundColor: "var(--color-bg-secondary, var(--color-background))",
          }}
        >
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className="relative flex-1 px-2 py-2 text-sm font-medium transition-colors"
              style={{
                color:
                  activeTab === tab.key
                    ? "var(--color-accent)"
                    : "var(--color-text-muted)",
                background: "transparent",
                border: "none",
                cursor: "pointer",
              }}
            >
              {tab.label}
              {/* Active indicator */}
              {activeTab === tab.key && (
                <span
                  className="absolute bottom-0 left-0 right-0 h-0.5"
                  style={{ backgroundColor: "var(--color-accent)" }}
                />
              )}
            </button>
          ))}
        </div>

        {/* Active panel */}
        <div className="flex-1 overflow-y-auto">
          {activeTab === "problem" && left}
          {activeTab === "editor" && center}
          {activeTab === "output" && right}
        </div>
      </div>
    );
  }

  // ---- Desktop layout (original) ----
  return (
    <div ref={containerRef} className="flex h-full w-full overflow-hidden">
      {/* Left panel */}
      <div
        className="shrink-0 overflow-y-auto"
        style={{ width: leftWidth }}
      >
        {left}
      </div>

      {/* Left resize handle */}
      <div
        className="w-1 shrink-0 cursor-col-resize bg-[var(--color-border)] transition-colors hover:bg-[var(--color-accent)]"
        onMouseDown={() => startResize("left")}
      />

      {/* Center panel */}
      <div className="flex-1 overflow-hidden">{center}</div>

      {/* Right resize handle */}
      <div
        className="w-1 shrink-0 cursor-col-resize bg-[var(--color-border)] transition-colors hover:bg-[var(--color-accent)]"
        onMouseDown={() => startResize("right")}
      />

      {/* Right panel */}
      <div
        className="shrink-0 overflow-y-auto"
        style={{ width: rightWidth }}
      >
        {right}
      </div>
    </div>
  );
}
