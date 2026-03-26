import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "SQL Sandbox",
  description: "Write and execute SQL queries freely against real datasets. No problem constraints.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
