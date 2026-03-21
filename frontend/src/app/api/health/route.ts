import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

export async function GET() {
  const backendTarget = `${BACKEND_URL}/health`;
  try {
    const res = await fetch(backendTarget, { cache: "no-store" });
    const data = await res.json();
    return NextResponse.json({
      frontend: "ok",
      backend: "ok",
      backend_url: BACKEND_URL,
      backend_response: data,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json(
      {
        frontend: "ok",
        backend: "unreachable",
        backend_url: BACKEND_URL,
        error: message,
      },
      { status: 502 }
    );
  }
}
