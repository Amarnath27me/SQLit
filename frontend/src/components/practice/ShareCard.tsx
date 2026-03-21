"use client";

import { useState, useRef, useCallback, memo } from "react";

interface ShareCardProps {
  problemTitle: string;
  difficulty: "easy" | "medium" | "hard";
  xpEarned: number;
  executionTimeMs: number;
  streak: number;
}

const DIFFICULTY_COLORS = {
  easy: { bg: "#059669", text: "Easy" },
  medium: { bg: "#d97706", text: "Medium" },
  hard: { bg: "#dc2626", text: "Hard" },
};

export const ShareCard = memo(function ShareCard({
  problemTitle,
  difficulty,
  xpEarned,
  executionTimeMs,
  streak,
}: ShareCardProps) {
  const [showCard, setShowCard] = useState(false);
  const [copied, setCopied] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  const shareText = `I just solved "${problemTitle}" (${DIFFICULTY_COLORS[difficulty].text}) on SQLit! +${xpEarned} XP in ${executionTimeMs}ms${streak > 1 ? ` | ${streak}-day streak` : ""} 🔥\n\nPractice SQL at sqlit.dev`;

  const handleCopyText = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // fallback
    }
  }, [shareText]);

  const handleShareTwitter = useCallback(() => {
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`;
    window.open(url, "_blank", "width=550,height=420");
  }, [shareText]);

  const handleShareLinkedIn = useCallback(() => {
    const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent("https://sqlit.dev")}&summary=${encodeURIComponent(shareText)}`;
    window.open(url, "_blank", "width=550,height=420");
  }, [shareText]);

  if (!showCard) {
    return (
      <button
        onClick={() => setShowCard(true)}
        aria-label="Share your solution"
        className="flex items-center gap-1.5 rounded-lg border border-[var(--color-border)] px-3 py-1.5 text-xs font-medium text-[var(--color-text-muted)] transition-colors hover:border-[var(--color-accent)]/40 hover:text-[var(--color-accent)]"
      >
        <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
        </svg>
        Share
      </button>
    );
  }

  return (
    <div className="space-y-3">
      {/* Share card preview */}
      <div
        ref={cardRef}
        className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-gradient-to-br from-[var(--color-surface)] to-[var(--color-background)]"
      >
        <div className="p-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-[var(--color-accent)]">SQLit</span>
            <span className="text-xs text-[var(--color-text-muted)]">Problem Solved</span>
          </div>
          <h3 className="mt-2 text-sm font-semibold text-[var(--color-text-primary)]">
            {problemTitle}
          </h3>
          <div className="mt-2 flex items-center gap-2">
            <span
              className="rounded-full px-2 py-0.5 text-[10px] font-bold text-white"
              style={{ backgroundColor: DIFFICULTY_COLORS[difficulty].bg }}
            >
              {DIFFICULTY_COLORS[difficulty].text}
            </span>
            <span className="text-xs font-medium text-amber-500">+{xpEarned} XP</span>
            <span className="text-[10px] text-[var(--color-text-muted)]">{executionTimeMs}ms</span>
            {streak > 1 && (
              <span className="text-xs text-orange-500">{streak}-day streak 🔥</span>
            )}
          </div>
        </div>
      </div>

      {/* Share buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={handleShareTwitter}
          aria-label="Share on X (Twitter)"
          className="flex items-center gap-1.5 rounded-lg bg-[#1DA1F2]/10 px-3 py-1.5 text-xs font-medium text-[#1DA1F2] transition-colors hover:bg-[#1DA1F2]/20"
        >
          <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
          </svg>
          Post
        </button>
        <button
          onClick={handleShareLinkedIn}
          aria-label="Share on LinkedIn"
          className="flex items-center gap-1.5 rounded-lg bg-[#0A66C2]/10 px-3 py-1.5 text-xs font-medium text-[#0A66C2] transition-colors hover:bg-[#0A66C2]/20"
        >
          <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z" />
          </svg>
          Share
        </button>
        <button
          onClick={handleCopyText}
          aria-label={copied ? "Copied to clipboard" : "Copy share text to clipboard"}
          className="flex items-center gap-1.5 rounded-lg border border-[var(--color-border)] px-3 py-1.5 text-xs font-medium text-[var(--color-text-secondary)] transition-colors hover:border-[var(--color-accent)]/40"
        >
          {copied ? (
            <>
              <svg className="h-3.5 w-3.5 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
              Copied!
            </>
          ) : (
            <>
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 0 1-.75.75H9.75a.75.75 0 0 1-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 0 1-2.25 2.25H6.75A2.25 2.25 0 0 1 4.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 0 1 1.927-.184" />
              </svg>
              Copy
            </>
          )}
        </button>
        <button
          onClick={() => setShowCard(false)}
          aria-label="Close share card"
          className="ml-auto text-xs text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
        >
          Close
        </button>
      </div>
    </div>
  );
});
