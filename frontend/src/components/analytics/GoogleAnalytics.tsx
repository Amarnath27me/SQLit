"use client";

import Script from "next/script";

const GA_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

export function GoogleAnalytics() {
  if (!GA_ID) return null;

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GA_ID}', {
            page_title: document.title,
            page_location: window.location.href,
          });
        `}
      </Script>
    </>
  );
}

/* ── Custom event helpers ─────────────────────────────────── */

export function trackEvent(action: string, params?: Record<string, string | number>) {
  if (typeof window !== "undefined" && typeof (window as any).gtag === "function") {
    (window as any).gtag("event", action, params);
  }
}

// Pre-defined event helpers
export const analytics = {
  problemSolved: (problemId: string, difficulty: string, xp: number) =>
    trackEvent("problem_solved", { problem_id: problemId, difficulty, xp_earned: xp }),

  problemAttempted: (problemId: string, correct: boolean) =>
    trackEvent("problem_attempted", { problem_id: problemId, result: correct ? "correct" : "wrong" }),

  queryExecuted: (dataset: string, executionTimeMs: number) =>
    trackEvent("query_executed", { dataset, execution_time_ms: executionTimeMs }),

  hintRevealed: (problemId: string, hintLevel: number) =>
    trackEvent("hint_revealed", { problem_id: problemId, hint_level: hintLevel }),

  pageView: (page: string) =>
    trackEvent("page_view", { page_path: page }),

  signIn: () => trackEvent("sign_in"),
  signUp: () => trackEvent("sign_up"),
};
