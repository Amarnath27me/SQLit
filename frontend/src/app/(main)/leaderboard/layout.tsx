import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Leaderboard",
  description: "See top SQL practitioners ranked by XP. Compete and track your progress.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
