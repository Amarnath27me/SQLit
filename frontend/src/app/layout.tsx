import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { Auth0Provider } from "@auth0/nextjs-auth0/client";
import { GoogleAnalytics } from "@/components/analytics/GoogleAnalytics";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: {
    default: "SQLit — Practice SQL on Real Databases",
    template: "%s | SQLit",
  },
  description:
    "LeetCode for SQL & Data Engineering. 400+ problems, real SQL execution, 3 industry datasets. Master SQL with hands-on practice.",
  keywords: [
    "SQL practice",
    "learn SQL",
    "SQL problems",
    "SQL interview prep",
    "LeetCode SQL",
    "data engineering",
    "SQL exercises",
    "PostgreSQL practice",
    "SQL query practice",
    "database practice",
    "SQL challenges",
    "SQL tutorial",
  ],
  authors: [{ name: "SQLit" }],
  creator: "SQLit",
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://sqlit-nu.vercel.app"),
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "SQLit",
    title: "SQLit — Practice SQL on Real Databases",
    description:
      "400+ problems, 3 industry datasets, real SQL execution. The platform for mastering SQL.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "SQLit — Practice SQL on Real Databases",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "SQLit — Practice SQL on Real Databases",
    description:
      "400+ problems, 3 industry datasets, real SQL execution. Master SQL with hands-on practice.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

// Inline script that runs before React hydration to prevent flash of wrong theme.
// It reads localStorage or falls back to the system preference and sets the `dark`
// class on <html> synchronously, before any paint.
const themeInitScript = `
(function(){
  try {
    var t = localStorage.getItem('sqlit-theme');
    if (t !== 'light' && t !== 'dark') {
      t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    if (t === 'dark') document.documentElement.classList.add('dark');
  } catch(e) {}
})();
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`} suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body className="min-h-screen font-[family-name:var(--font-geist-sans)] bg-[var(--color-background)] text-[var(--color-text-primary)]">
        <GoogleAnalytics />
        <Auth0Provider>
          {children}
        </Auth0Provider>
      </body>
    </html>
  );
}
