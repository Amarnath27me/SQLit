// API_BASE should be empty ("") in production — requests go to /api/* on the
// same Vercel origin, which proxies to the backend server-side (no CORS issues).
// Only set NEXT_PUBLIC_API_URL for local dev if needed.
// Safety: ignore NEXT_PUBLIC_API_URL if it points to the backend directly
// (e.g., railway.app) — this would bypass the proxy and cause CORS/503 errors.
const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "";
const API_BASE = rawApiUrl.includes("railway.app") ? "" : rawApiUrl;

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = "ApiError";
  }
}

function friendlyMessage(status: number, detail: string | null): string {
  if (status === 502 || status === 503) {
    return "The SQL engine is warming up — please try again in a moment.";
  }
  if (status === 504) {
    return "The request timed out. Please try again.";
  }
  if (status === 500) {
    return detail || "A server error occurred. Please try again.";
  }
  return detail || "Something went wrong. Please try again.";
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
  _retries = 1
): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: null }));

    // Auto-retry once on cold-start / gateway errors (Railway warmup takes ~2-3 s)
    if ((res.status === 502 || res.status === 503) && _retries > 0) {
      await new Promise((r) => setTimeout(r, 3000));
      return apiClient(endpoint, options, 0);
    }

    throw new ApiError(
      friendlyMessage(res.status, error.detail ?? null),
      res.status
    );
  }

  return res.json();
}
