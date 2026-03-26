import Link from "next/link";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex flex-1 flex-col items-center justify-center px-6 py-24 text-center">
        <p className="text-6xl font-bold text-[var(--color-accent)]">404</p>
        <h1 className="mt-4 text-2xl font-bold text-[var(--color-text-primary)]">
          Page not found
        </h1>
        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <div className="mt-8 flex gap-4">
          <Link
            href="/"
            className="rounded-lg bg-[var(--color-accent)] px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[var(--color-accent-hover)]"
          >
            Go Home
          </Link>
          <Link
            href="/practice"
            className="rounded-lg border border-[var(--color-border)] px-6 py-2.5 text-sm font-medium text-[var(--color-text-primary)] transition-colors hover:bg-[var(--color-surface)]"
          >
            Practice SQL
          </Link>
        </div>
      </main>
      <Footer />
    </div>
  );
}
