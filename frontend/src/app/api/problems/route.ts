import { NextRequest } from "next/server";
import { proxyToBackend } from "@/lib/proxy";

export async function GET(req: NextRequest) {
  const search = req.nextUrl.searchParams.toString();
  const path = `/api/problems/${search ? `?${search}` : ""}`;
  return proxyToBackend(req, path);
}
