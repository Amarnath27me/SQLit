import { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://sqlit-nu.vercel.app";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
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

  // Dynamic problem pages
  let problemEntries: MetadataRoute.Sitemap = [];
  try {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8001";
    const res = await fetch(`${backendUrl}/api/problems`, { next: { revalidate: 3600 } });
    if (res.ok) {
      const data = await res.json();
      problemEntries = (data.problems || []).map((p: { slug: string; difficulty: string }) => ({
        url: `${BASE_URL}/practice/${p.slug}`,
        lastModified: new Date(),
        changeFrequency: "monthly" as const,
        priority: p.difficulty === "easy" ? 0.6 : p.difficulty === "medium" ? 0.65 : 0.7,
      }));
    }
  } catch {
    // Backend not available during build — skip dynamic entries
  }

  return [...staticEntries, ...problemEntries];
}
