import { NextRequest, NextResponse } from "next/server";
import { isAuth0Configured } from "@/lib/auth0";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

async function getSession() {
  if (!isAuth0Configured) return null;
  const { auth0 } = await import("@/lib/auth0");
  const session = await auth0.getSession();
  return session?.user?.sub ? session : null;
}

export async function GET() {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  try {
    const res = await fetch(`${BACKEND_URL}/api/progress/userdata`, {
      headers: {
        "Content-Type": "application/json",
        "X-User-Sub": session.user.sub,
      },
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[userdata] GET failed:", err);
    return NextResponse.json({ error: "Failed to fetch user data" }, { status: 502 });
  }
}

export async function PUT(req: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  try {
    const body = await req.json();
    const res = await fetch(`${BACKEND_URL}/api/progress/userdata`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-User-Sub": session.user.sub,
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[userdata] PUT failed:", err);
    return NextResponse.json({ error: "Failed to save user data" }, { status: 502 });
  }
}
