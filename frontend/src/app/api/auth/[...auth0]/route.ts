import { NextRequest, NextResponse } from "next/server";
import { isAuth0Configured } from "@/lib/auth0";

function authUnavailableResponse(req: NextRequest) {
  // Redirect browser requests back to home; return JSON for API calls
  const accept = req.headers.get("accept") || "";
  if (accept.includes("text/html")) {
    return NextResponse.redirect(new URL("/?auth=unavailable", req.url));
  }
  return NextResponse.json(
    { error: "Authentication is not configured." },
    { status: 503 }
  );
}

export async function GET(req: NextRequest) {
  if (!isAuth0Configured) {
    return authUnavailableResponse(req);
  }

  const { auth0 } = await import("@/lib/auth0");
  try {
    return await auth0.middleware(req);
  } catch {
    return authUnavailableResponse(req);
  }
}

export async function POST(req: NextRequest) {
  if (!isAuth0Configured) {
    return authUnavailableResponse(req);
  }

  const { auth0 } = await import("@/lib/auth0");
  try {
    return await auth0.middleware(req);
  } catch {
    return authUnavailableResponse(req);
  }
}
