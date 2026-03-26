import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "SQL Interview Prep",
  description: "Practice SQL interview questions from top tech companies. Filter by company and role.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
