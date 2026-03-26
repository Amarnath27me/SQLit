import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/progress/leaderboard`, {
      headers: { "Content-Type": "application/json" },
    });

    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[leaderboard] Failed:", err);
    return NextResponse.json(
      { entries: [], total_users: 0 },
      { status: 502 }
    );
  }
}
