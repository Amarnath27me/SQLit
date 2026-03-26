import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Your Profile",
  description: "View your SQL practice progress, solved problems, and achievements.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
