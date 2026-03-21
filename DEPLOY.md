# Deploying SQLit

## Architecture

```
[Vercel]  ──>  [Railway / Render]  ──>  [PostgreSQL]
 Next.js         FastAPI Backend          Database
 Frontend        + SQL Sandbox
```

---

## Quick Start (5 minutes)

### 1. Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New Project** → import your `sqlit` repo
3. Set **Root Directory** to `frontend`
4. Add environment variables (see table below)
5. Click **Deploy**

### 3. Deploy Backend on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **New Project** → **Deploy from GitHub Repo**
3. Select your repo, set **Root Directory** to `backend`
4. Add a **PostgreSQL** plugin from the Railway dashboard
5. Add environment variables (see table below)
6. Deploy

### 4. Connect them

Update Vercel environment variables with your Railway backend URL:
- `NEXT_PUBLIC_API_URL` = `https://your-backend.up.railway.app`
- `BACKEND_URL` = `https://your-backend.up.railway.app`

Redeploy the frontend from Vercel dashboard.

---

## Environment Variables

### Frontend (Vercel)

| Variable | Example | Required |
|---|---|---|
| `AUTH0_SECRET` | `openssl rand -hex 32` | Yes |
| `AUTH0_BASE_URL` | `https://sqlit.vercel.app` | Yes |
| `AUTH0_ISSUER_BASE_URL` | `https://your-tenant.us.auth0.com` | Yes |
| `AUTH0_CLIENT_ID` | From Auth0 dashboard | Yes |
| `AUTH0_CLIENT_SECRET` | From Auth0 dashboard | Yes |
| `NEXT_PUBLIC_API_URL` | `https://your-backend.up.railway.app` | Yes |
| `NEXT_PUBLIC_SITE_URL` | `https://sqlit.vercel.app` | No |
| `BACKEND_URL` | `https://your-backend.up.railway.app` | Yes |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | `G-XXXXXXXXXX` | No |

### Backend (Railway / Render)

| Variable | Example | Required |
|---|---|---|
| `DATABASE_URL` | Auto-provided by Railway PG plugin | Yes |
| `SANDBOX_DATABASE_URL` | Same or separate PG instance | Yes |
| `AUTH0_DOMAIN` | `your-tenant.us.auth0.com` | Yes |
| `AUTH0_API_AUDIENCE` | `https://api.sqlit.dev` | Yes |
| `CORS_ORIGINS` | `["https://sqlit.vercel.app"]` | Yes |

---

## Auth0 Setup

1. Create an application in [Auth0 Dashboard](https://manage.auth0.com)
2. Type: **Regular Web Application**
3. Configure URLs:
   - Allowed Callback URLs: `https://YOUR_DOMAIN/api/auth/callback`
   - Allowed Logout URLs: `https://YOUR_DOMAIN`
   - Allowed Web Origins: `https://YOUR_DOMAIN`
4. Create an API with your chosen identifier
5. Enable **Bot Detection** under Security settings

---

## Local Development with Docker

```bash
docker-compose up -d
```

This starts PostgreSQL, the backend, and frontend locally.

- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- PostgreSQL: localhost:5432

---

## Custom Domain

1. Purchase a domain (e.g., sqlit.dev)
2. Vercel → Settings → Domains → Add your domain
3. Set DNS records as instructed by Vercel
4. Update `AUTH0_BASE_URL` and Auth0 callback URLs
5. Update `CORS_ORIGINS` on the backend

---

## Scaling Notes

| Users | Recommended Setup |
|---|---|
| 1-50 | Free tiers (Vercel + Railway + 500MB PG) |
| 50-500 | Railway Pro ($5-20/mo), dedicated PG |
| 500+ | Railway with multiple workers, PG connection pooling |
| 1000+ | Consider dedicated VPS, Redis caching, Docker Swarm/K8s |
