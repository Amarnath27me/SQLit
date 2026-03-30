import { MetadataRoute } from "next";
import { getAllProblems } from "@/lib/problems";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://sqlit-nu.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  // Static pages
  const staticPages = [
    "",
    "/practice",
    "/debug",
    "/sandbox",
    "/analyzer",
    "/docs",
    "/datasets",
    "/interview",
    "/leaderboard",
    "/challenge",
    "/optimization",
    "/db-design",
  ];

  const staticEntries: MetadataRoute.Sitemap = staticPages.map((path) => ({
    url: `${BASE_URL}${path}`,
    lastModified: new Date(),
    changeFrequency: path === "" ? "weekly" : "daily",
    priority: path === "" ? 1.0 : path === "/practice" ? 0.9 : 0.7,
  }));

  // Dynamic problem pages from static data
  const problems = getAllProblems();
  const problemEntries: MetadataRoute.Sitemap = problems.map((p) => ({
    url: `${BASE_URL}/practice/${p.slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly" as const,
    priority: p.difficulty === "easy" ? 0.6 : p.difficulty === "medium" ? 0.65 : 0.7,
  }));

  return [...staticEntries, ...problemEntries];
}
