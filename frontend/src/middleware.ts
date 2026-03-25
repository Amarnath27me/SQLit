import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

// Only import auth0 if configured (Auth0 v4 env var names)
const isAuth0Configured = Boolean(
  process.env.AUTH0_SECRET &&
  process.env.AUTH0_DOMAIN &&
  process.env.AUTH0_CLIENT_ID &&
  process.env.AUTH0_CLIENT_SECRET
);

export async function middleware(request: NextRequest) {
  // If Auth0 is not configured, skip all auth middleware
  if (!isAuth0Configured) {
    // Redirect auth and protected routes to home when Auth0 isn't set up
    const authPaths = ["/auth/", "/profile", "/settings"];
    const needsAuth = authPaths.some((p) => request.nextUrl.pathname.startsWith(p));
    if (needsAuth) {
      return NextResponse.redirect(new URL("/", request.url));
    }
    return NextResponse.next();
  }

  try {
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
  } catch {
    // If Auth0 middleware fails, allow the request to proceed
    return NextResponse.next();
  }
}

export const config = {
  matcher: [
    // Match all paths except static files, Next.js internals, and API routes
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|api/).*)",
  ],
};
