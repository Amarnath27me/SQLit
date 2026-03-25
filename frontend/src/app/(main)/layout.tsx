import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { AuthSync } from "@/components/auth/AuthSync";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <AuthSync />
      <Navbar />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
