// API_BASE should be empty ("") in production — requests go to /api/* on the
// same Vercel origin, which proxies to the backend server-side (no CORS issues).
// Only set NEXT_PUBLIC_API_URL for local dev if needed.
// Safety: ignore NEXT_PUBLIC_API_URL if it points to the backend directly
// (e.g., railway.app) — this would bypass the proxy and cause CORS/503 errors.
const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "";
const API_BASE = rawApiUrl.includes("railway.app") ? "" : rawApiUrl;

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "API request failed");
  }

  return res.json();
}
