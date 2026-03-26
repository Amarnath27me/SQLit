import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Challenge Mode",
  description: "Race against the clock solving SQL problems. Test your speed and accuracy.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
