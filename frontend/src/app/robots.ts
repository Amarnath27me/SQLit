import { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://sqlit-nu.vercel.app";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/auth/", "/settings", "/profile"],
      },
    ],
    sitemap: `${BASE_URL}/sitemap.xml`,
  };
}
