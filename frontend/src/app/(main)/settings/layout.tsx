import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Settings",
  description: "Customize your SQLit experience. Editor preferences, dialect defaults, and account settings.",
};
export default function Layout({ children }: { children: React.ReactNode }) { return children; }
