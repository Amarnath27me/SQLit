"use client";

import { useEffect, useRef } from "react";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useUserStore } from "@/stores/useUserStore";

/**
 * Syncs Auth0 session data into Zustand store and fetches
 * persisted progress from backend on login.
 *
 * Handles two directions:
 * - Login:  Auth0 has user → sync auth info + fetch backend progress
 * - Logout: Auth0 has no user but store says authenticated → call store.logout()
 */
export function AuthSync() {
  const { user, isLoading } = useUser();
  const syncFromAuth0 = useUserStore((s) => s.syncFromAuth0);
  const syncFromBackend = useUserStore((s) => s.syncFromBackend);
  const logout = useUserStore((s) => s.logout);
  const isAuthenticated = useUserStore((s) => s.isAuthenticated);
  const auth0Id = useUserStore((s) => s.auth0Id);
  const hasSynced = useRef(false);

  useEffect(() => {
    if (isLoading) return;

    if (user) {
      // User is logged in via Auth0
      const isNewLogin = !isAuthenticated;
      const isDifferentUser = auth0Id && auth0Id !== user.sub;

      if (isNewLogin || isDifferentUser || !hasSynced.current) {
        syncFromAuth0({
          name: user.name ?? undefined,
          email: user.email ?? undefined,
          picture: user.picture ?? undefined,
          sub: user.sub ?? undefined,
        });

        // Always fetch backend progress on login / page load
        syncFromBackend();
        hasSynced.current = true;
      }
    } else if (!user && isAuthenticated) {
      // Auth0 session is gone but store thinks we're authenticated
      // → user logged out via /auth/logout
      logout();
      hasSynced.current = false;
    }
  }, [user, isLoading, isAuthenticated, auth0Id, syncFromAuth0, syncFromBackend, logout]);

  return null;
}
