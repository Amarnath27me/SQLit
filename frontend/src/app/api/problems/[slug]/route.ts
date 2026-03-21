import { NextRequest } from "next/server";
import { proxyToBackend } from "@/lib/proxy";

export async function GET(
  req: NextRequest,
  { params }: { params: { slug: string } }
) {
  return proxyToBackend(req, `/api/problems/${params.slug}`);
}
