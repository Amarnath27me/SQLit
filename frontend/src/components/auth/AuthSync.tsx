"use client";

import { useEffect } from "react";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useUserStore } from "@/stores/useUserStore";

/**
 * Syncs Auth0 session data into Zustand store.
 * Place this inside the Auth0Provider (e.g., in root layout).
 */
export function AuthSync() {
  const { user, isLoading } = useUser();
  const syncFromAuth0 = useUserStore((s) => s.syncFromAuth0);
  const isAuthenticated = useUserStore((s) => s.isAuthenticated);

  useEffect(() => {
    if (!isLoading && user && !isAuthenticated) {
      syncFromAuth0({
        name: user.name ?? undefined,
        email: user.email ?? undefined,
        picture: user.picture ?? undefined,
        sub: user.sub ?? undefined,
      });
    }
  }, [user, isLoading, isAuthenticated, syncFromAuth0]);

  return null;
}
