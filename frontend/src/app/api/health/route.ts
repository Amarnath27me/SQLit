import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND_URL}/health`, { cache: "no-store" });
    const data = await res.json();
    return NextResponse.json({ ...data, frontend: "ok" });
  } catch {
    return NextResponse.json(
      { status: "error", frontend: "ok", backend: "unreachable" },
      { status: 502 }
    );
  }
}
