import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8001";

export async function proxyToBackend(
  req: NextRequest,
  path: string
): Promise<NextResponse> {
  const url = `${BACKEND_URL}${path}`;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const init: RequestInit = {
    method: req.method,
    headers,
  };

  if (req.method !== "GET" && req.method !== "HEAD") {
    init.body = await req.text();
  }

  try {
    const res = await fetch(url, init);
    const text = await res.text();
    // Try parsing as JSON, fall back to plain text error
    try {
      const data = JSON.parse(text);
      return NextResponse.json(data, { status: res.status });
    } catch {
      return NextResponse.json(
        { detail: `Backend returned non-JSON: ${text.slice(0, 200)}` },
        { status: res.status }
      );
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    console.error(`[proxy] Failed to reach ${url}: ${message}`);
    return NextResponse.json(
      { detail: `Backend unavailable: ${message}` },
      { status: 502 }
    );
  }
}
