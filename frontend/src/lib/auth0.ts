import { Auth0Client } from "@auth0/nextjs-auth0/server";

// Auth0 client — works when env vars are configured, gracefully degrades otherwise.
// Required env vars: AUTH0_SECRET, AUTH0_BASE_URL, AUTH0_ISSUER_BASE_URL, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
export const auth0 = new Auth0Client();

// Check if Auth0 is configured
export const isAuth0Configured = Boolean(
  process.env.AUTH0_SECRET &&
  process.env.AUTH0_ISSUER_BASE_URL &&
  process.env.AUTH0_CLIENT_ID &&
  process.env.AUTH0_CLIENT_SECRET
);
