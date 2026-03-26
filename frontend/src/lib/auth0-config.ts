// Shared Auth0 configuration check — used by both middleware and auth0.ts
export const isAuth0Configured = Boolean(
  process.env.AUTH0_SECRET &&
  process.env.AUTH0_DOMAIN &&
  process.env.AUTH0_CLIENT_ID &&
  process.env.AUTH0_CLIENT_SECRET
);
