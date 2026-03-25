import { Auth0Client } from "@auth0/nextjs-auth0/server";

// Auth0 client — works when env vars are configured, gracefully degrades otherwise.
// Required env vars for @auth0/nextjs-auth0 v4:
//   AUTH0_DOMAIN        — e.g., dev-xxxxx.us.auth0.com
//   AUTH0_CLIENT_ID     — from Auth0 app settings
//   AUTH0_CLIENT_SECRET — from Auth0 app settings
//   AUTH0_SECRET         — random string for session encryption (openssl rand -hex 32)
//   APP_BASE_URL        — e.g., https://sqlit-nu.vercel.app
export const auth0 = new Auth0Client();

// Check if Auth0 is configured
export const isAuth0Configured = Boolean(
  process.env.AUTH0_SECRET &&
  process.env.AUTH0_DOMAIN &&
  process.env.AUTH0_CLIENT_ID &&
  process.env.AUTH0_CLIENT_SECRET
);
