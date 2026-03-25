import { NextRequest, NextResponse } from "next/server";
import { isAuth0Configured } from "@/lib/auth0";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

export async function GET(req: NextRequest) {
  if (!isAuth0Configured) {
    return NextResponse.json(
      { error: "Authentication not configured" },
      { status: 503 }
    );
  }

  try {
    const { auth0 } = await import("@/lib/auth0");
    const session = await auth0.getSession();

    if (!session?.user?.sub) {
      return NextResponse.json(
        { error: "Not authenticated" },
        { status: 401 }
      );
    }

    const res = await fetch(`${BACKEND_URL}/api/progress`, {
      headers: {
        "Content-Type": "application/json",
        "X-User-Sub": session.user.sub,
      },
    });

    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[progress] Failed:", err);
    return NextResponse.json(
      { error: "Failed to fetch progress" },
      { status: 502 }
    );
  }
}
