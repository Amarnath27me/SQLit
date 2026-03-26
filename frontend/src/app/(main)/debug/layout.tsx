import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Data Debugging",
  description: "Find and fix data quality issues: duplicates, NULL bugs, wrong joins, and more.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
