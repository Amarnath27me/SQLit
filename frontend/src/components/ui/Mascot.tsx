"use client";

import { useEffect, useState } from "react";

type MascotMood = "celebrate" | "hint" | "error" | "thinking" | "wave" | "idle";

interface MascotProps {
  mood?: MascotMood;
  size?: number;
  animate?: boolean;
  className?: string;
}

/**
 * SQLit Mascot — A friendly database owl character.
 * Appears during: celebrations, hints, onboarding, errors.
 * Professional SVG — clean, minimal, delightful.
 */
export function Mascot({
  mood = "idle",
  size = 80,
  animate = true,
  className = "",
}: MascotProps) {
  const [bounce, setBounce] = useState(false);

  useEffect(() => {
    if (animate && mood === "celebrate") {
      setBounce(true);
      const timer = setTimeout(() => setBounce(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [mood, animate]);

  const animClass = bounce ? "animate-bounce" : "";

  return (
    <div className={`inline-flex ${animClass} ${className}`} style={{ width: size, height: size }}>
      <svg
        viewBox="0 0 120 120"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="h-full w-full"
      >
        {/* Body */}
        <ellipse
          cx="60"
          cy="68"
          rx="36"
          ry="38"
          className="fill-[var(--color-accent)]"
          opacity="0.15"
        />
        <ellipse
          cx="60"
          cy="68"
          rx="32"
          ry="34"
          className="fill-[var(--color-surface)] stroke-[var(--color-accent)]"
          strokeWidth="2.5"
        />

        {/* Ears / Tufts */}
        <path
          d="M32 42 L24 20 L40 36Z"
          className="fill-[var(--color-accent)]"
          opacity="0.8"
        />
        <path
          d="M88 42 L96 20 L80 36Z"
          className="fill-[var(--color-accent)]"
          opacity="0.8"
        />

        {/* Inner ears */}
        <path
          d="M33 40 L28 26 L39 36Z"
          className="fill-[var(--color-accent)]"
          opacity="0.3"
        />
        <path
          d="M87 40 L92 26 L81 36Z"
          className="fill-[var(--color-accent)]"
          opacity="0.3"
        />

        {/* Eye whites */}
        <ellipse cx="45" cy="60" rx="12" ry="13" className="fill-white dark:fill-gray-200" />
        <ellipse cx="75" cy="60" rx="12" ry="13" className="fill-white dark:fill-gray-200" />

        {/* Pupils — mood-dependent */}
        {mood === "celebrate" && (
          <>
            {/* Happy squint eyes */}
            <path d="M38 58 Q45 64 52 58" stroke="#1a1a2e" strokeWidth="3" strokeLinecap="round" fill="none" />
            <path d="M68 58 Q75 64 82 58" stroke="#1a1a2e" strokeWidth="3" strokeLinecap="round" fill="none" />
          </>
        )}
        {mood === "error" && (
          <>
            {/* Wide surprised eyes */}
            <circle cx="45" cy="59" r="7" fill="#1a1a2e" />
            <circle cx="75" cy="59" r="7" fill="#1a1a2e" />
            <circle cx="47" cy="57" r="2" fill="white" />
            <circle cx="77" cy="57" r="2" fill="white" />
          </>
        )}
        {mood === "thinking" && (
          <>
            {/* Looking up-right */}
            <circle cx="48" cy="57" r="6" fill="#1a1a2e" />
            <circle cx="78" cy="57" r="6" fill="#1a1a2e" />
            <circle cx="50" cy="55" r="2" fill="white" />
            <circle cx="80" cy="55" r="2" fill="white" />
          </>
        )}
        {mood === "hint" && (
          <>
            {/* One eye winking */}
            <circle cx="45" cy="59" r="5.5" fill="#1a1a2e" />
            <circle cx="47" cy="57" r="1.5" fill="white" />
            <path d="M68 60 Q75 56 82 60" stroke="#1a1a2e" strokeWidth="2.5" strokeLinecap="round" fill="none" />
          </>
        )}
        {(mood === "wave" || mood === "idle") && (
          <>
            {/* Normal eyes */}
            <circle cx="45" cy="59" r="5.5" fill="#1a1a2e" />
            <circle cx="75" cy="59" r="5.5" fill="#1a1a2e" />
            <circle cx="47" cy="57" r="1.5" fill="white" />
            <circle cx="77" cy="57" r="1.5" fill="white" />
          </>
        )}

        {/* Beak / Mouth */}
        {mood === "celebrate" ? (
          <path
            d="M52 72 Q60 80 68 72"
            className="stroke-[var(--color-accent)]"
            strokeWidth="2.5"
            strokeLinecap="round"
            fill="none"
          />
        ) : mood === "error" ? (
          <ellipse cx="60" cy="76" rx="5" ry="3" className="fill-[var(--color-accent)]" opacity="0.6" />
        ) : (
          <path
            d="M54 74 Q60 78 66 74"
            className="stroke-[var(--color-accent)]"
            strokeWidth="2"
            strokeLinecap="round"
            fill="none"
          />
        )}

        {/* Belly - database icon */}
        <rect
          x="49"
          y="82"
          width="22"
          height="14"
          rx="3"
          className="fill-[var(--color-accent)]"
          opacity="0.15"
          stroke="currentColor"
          strokeWidth="0"
        />
        <ellipse cx="60" cy="83" rx="11" ry="3" className="stroke-[var(--color-accent)]" strokeWidth="1.5" fill="none" />
        <ellipse cx="60" cy="89" rx="11" ry="3" className="stroke-[var(--color-accent)]" strokeWidth="1.5" fill="none" />
        <ellipse cx="60" cy="95" rx="11" ry="3" className="stroke-[var(--color-accent)]" strokeWidth="1.5" fill="none" />
        <line x1="49" y1="83" x2="49" y2="95" className="stroke-[var(--color-accent)]" strokeWidth="1.5" />
        <line x1="71" y1="83" x2="71" y2="95" className="stroke-[var(--color-accent)]" strokeWidth="1.5" />

        {/* Celebration sparkles */}
        {mood === "celebrate" && (
          <>
            <circle cx="18" cy="30" r="2" className="fill-amber-400" opacity="0.8">
              <animate attributeName="opacity" values="0.8;0.2;0.8" dur="1s" repeatCount="indefinite" />
            </circle>
            <circle cx="102" cy="28" r="2.5" className="fill-amber-400" opacity="0.6">
              <animate attributeName="opacity" values="0.6;0.1;0.6" dur="1.3s" repeatCount="indefinite" />
            </circle>
            <circle cx="14" cy="55" r="1.5" className="fill-emerald-400" opacity="0.7">
              <animate attributeName="opacity" values="0.7;0.2;0.7" dur="0.8s" repeatCount="indefinite" />
            </circle>
            <circle cx="106" cy="52" r="2" className="fill-emerald-400" opacity="0.5">
              <animate attributeName="opacity" values="0.5;0.1;0.5" dur="1.1s" repeatCount="indefinite" />
            </circle>
            <path d="M10 42 L14 40 L12 44Z" className="fill-amber-300" opacity="0.6">
              <animate attributeName="opacity" values="0.6;0;0.6" dur="1.5s" repeatCount="indefinite" />
            </path>
            <path d="M108 38 L112 36 L110 42Z" className="fill-amber-300" opacity="0.7">
              <animate attributeName="opacity" values="0.7;0;0.7" dur="1.2s" repeatCount="indefinite" />
            </path>
          </>
        )}

        {/* Hint lightbulb */}
        {mood === "hint" && (
          <g transform="translate(90, 30)">
            <circle cx="0" cy="0" r="8" className="fill-amber-400" opacity="0.2" />
            <circle cx="0" cy="0" r="5" className="fill-amber-400" opacity="0.4" />
            <text x="0" y="4" textAnchor="middle" fontSize="10" className="fill-amber-500">💡</text>
          </g>
        )}

        {/* Error exclamation */}
        {mood === "error" && (
          <g transform="translate(90, 30)">
            <circle cx="0" cy="0" r="8" className="fill-red-400" opacity="0.2" />
            <text x="0" y="5" textAnchor="middle" fontSize="12" fontWeight="bold" className="fill-red-500">!</text>
          </g>
        )}

        {/* Thinking dots */}
        {mood === "thinking" && (
          <g transform="translate(95, 35)">
            <circle cx="0" cy="0" r="2" className="fill-[var(--color-text-muted)]" opacity="0.5">
              <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite" />
            </circle>
            <circle cx="8" cy="-4" r="2.5" className="fill-[var(--color-text-muted)]" opacity="0.5">
              <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" begin="0.3s" repeatCount="indefinite" />
            </circle>
            <circle cx="16" cy="-9" r="3" className="fill-[var(--color-text-muted)]" opacity="0.5">
              <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" begin="0.6s" repeatCount="indefinite" />
            </circle>
          </g>
        )}
      </svg>
    </div>
  );
}
