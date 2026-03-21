import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

// Only import auth0 if configured
const isAuth0Configured = Boolean(
  process.env.AUTH0_SECRET &&
  process.env.AUTH0_ISSUER_BASE_URL &&
  process.env.AUTH0_CLIENT_ID &&
  process.env.AUTH0_CLIENT_SECRET
);

export async function middleware(request: NextRequest) {
  // If Auth0 is not configured, skip all auth middleware
  if (!isAuth0Configured) {
    return NextResponse.next();
  }

  // Dynamically import auth0 only when configured
  const { auth0 } = await import("@/lib/auth0");

  // Let Auth0 SDK handle session refresh/rolling
  const authRes = await auth0.middleware(request);

  // For auth routes, just return the Auth0 response
  if (request.nextUrl.pathname.startsWith("/auth/")) {
    return authRes;
  }

  // Protected routes — redirect to login if not authenticated
  const protectedPaths = ["/profile", "/settings"];
  const isProtected = protectedPaths.some((p) => request.nextUrl.pathname.startsWith(p));

  if (isProtected) {
    const session = await auth0.getSession(request);
    if (!session) {
      const loginUrl = new URL("/auth/login", request.url);
      loginUrl.searchParams.set("returnTo", request.nextUrl.pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  return authRes;
}

export const config = {
  matcher: [
    // Match all request paths except static files and Next.js internals
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};
