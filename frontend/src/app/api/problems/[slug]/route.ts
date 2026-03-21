import { NextRequest } from "next/server";
import { proxyToBackend } from "@/lib/proxy";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params;
  return proxyToBackend(req, `/api/problems/${slug}`);
}
