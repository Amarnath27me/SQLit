import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Practice SQL Problems",
  description: "Browse 400+ SQL problems across 3 industry datasets. Filter by difficulty, category, and dataset.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
