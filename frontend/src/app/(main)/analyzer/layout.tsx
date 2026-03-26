import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Query Analyzer",
  description: "Step through SQL execution visually. Understand every clause and optimize your queries.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
