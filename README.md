<div align="center">

# 🗄️ SQLit

### LeetCode for SQL — Practice with Real Datasets, Get Instant Feedback

[![Live Demo](https://img.shields.io/badge/Live%20Demo-sqlit--nu.vercel.app-blue?style=for-the-badge&logo=vercel)](https://sqlit-nu.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)

**[🚀 Try it Live](https://sqlit-nu.vercel.app) · [📖 Docs](#getting-started) · [🤝 Contribute](#contributing)**

</div>

---

## What is SQLit?

SQLit is a **free, open-source SQL practice platform** — like LeetCode, but purpose-built for databases. Write real queries against real schemas, get instant results in the browser, and level up from beginner to expert.

Whether you're prepping for a data engineering or analytics interview, learning SQL from scratch, or sharpening your window functions — SQLit has you covered with 412 curated problems, real-world datasets, and a built-in query optimizer.

> **No account required to start. No setup needed. Just open the browser and write SQL.**

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### 📝 Practice Problems
- **412 curated problems** across Easy, Medium, and Hard difficulties
- Covers JOINs, subqueries, CTEs, window functions, aggregations, and more
- Problems organized by concept tags and categories
- Hints, explanations, and multiple solution approaches for every problem

### ⚡ In-Browser SQL Engine
- Write and execute SQL **directly in the browser** — no setup required
- Supports **SQLite** (instant, client-side fallback) and **PostgreSQL** (production sandbox)
- **MySQL dialect support** via automatic syntax translation
- Sandboxed execution with timeout protection and rate limiting

### 🗂️ Real-World Datasets
| Domain | Tables |
|--------|--------|
| 🛒 E-Commerce | customers, orders, products, reviews |
| 💰 Finance | accounts, transactions, portfolios, market data |
| 🏥 Healthcare | patients, diagnoses, prescriptions, appointments |

Interactive dataset explorer with schema diagrams, column types, and sample data.

### 🔍 Query Optimization Lab
- **Visual EXPLAIN plan analyzer** with color-coded node types
- See `Seq Scan` vs `Index Scan`, `Nested Loop` vs `Hash Join`
- Learn to read and optimize execution plans hands-on

### 🏗️ Database Design Studio
- **Interactive ER Diagram Builder** — drag-and-drop entities on an SVG canvas
- Add tables, columns (19 PostgreSQL types), primary keys, and foreign keys
- **Export to SQL DDL** with one click
- **Import from SQL** — paste `CREATE TABLE` statements and get a visual diagram
- Schema normalization guide and best practices

### 🎯 Interview Prep
- Timed SQL challenges simulating real interview conditions
- Company-style question sets (FAANG, startups, finance)
- Difficulty progression from phone screen to on-site level

### 📅 Daily Challenges
- Fresh SQL problem every day with a countdown timer
- Streak tracking to keep you consistent

### 📊 Profile & Progress
- **GitHub-style activity heatmap** showing your full solve history
- **Concept badges** — earn Beginner → Learner → Proficient → Expert → Master per topic
- XP system with level progression
- Track solved problems, accuracy, and streaks

### 🛠️ Developer Experience
- Light and dark theme with smooth toggle
- Resizable editor panels
- Syntax-highlighted SQL editor with auto-formatting
- Mobile-responsive design

---

## Screenshots

> 📸 *Screenshots coming soon — [try the live demo](https://sqlit-nu.vercel.app) in the meantime.*

<!--
  To add screenshots:
  1. Take screenshots of: problem solver, query optimizer, ER builder, profile page
  2. Add to /docs/screenshots/
  3. Uncomment and update the lines below

![Problem Solver](docs/screenshots/solver.png)
![Query Optimizer](docs/screenshots/optimizer.png)
![ER Diagram Builder](docs/screenshots/er-builder.png)
-->

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, TypeScript, Tailwind CSS 4 |
| **Backend** | FastAPI, Python 3.12, Uvicorn |
| **Database** | PostgreSQL (production), SQLite (fallback) |
| **State** | Zustand with localStorage persistence |
| **Auth** | Auth0 (optional) |
| **Deployment** | Vercel (frontend) + Railway (backend) |

---

## Project Structure

```
SQLit/
├── frontend/                  # Next.js app
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   │   ├── (main)/        # All authenticated routes
│   │   │   │   ├── practice/  # Problem list + solver
│   │   │   │   ├── datasets/  # Dataset explorer
│   │   │   │   ├── db-design/ # ER builder + normalization
│   │   │   │   ├── optimization/ # EXPLAIN visualizer
│   │   │   │   ├── interview/ # Interview prep
│   │   │   │   └── profile/   # Activity heatmap + badges
│   │   │   └── api/           # API route proxies
│   │   ├── components/        # Reusable UI components
│   │   ├── stores/            # Zustand state stores
│   │   └── lib/               # Utilities, API client, schemas
│   └── package.json
│
├── backend/                   # FastAPI app
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   ├── core/              # Config, auth, database, rate limiter
│   │   ├── datasets/          # E-commerce, Finance, Healthcare
│   │   ├── models/            # SQLAlchemy models
│   │   └── services/          # Query executor, problem service
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml         # Full-stack local development
```

---

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 16+ *(optional — SQLite fallback works out of the box)*

### 1. Clone the repository

```bash
git clone https://github.com/Amarnath27me/SQLit.git
cd SQLit
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Edit if you have PostgreSQL
uvicorn app.main:app --port 8001 --reload
```

The API will be running at `http://localhost:8001`. Test it:

```bash
curl http://localhost:8001/health
# → {"status": "ok", "service": "sqlit-api"}
```

### 3. Start the frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and start practicing!

### 4. Full stack with Docker *(recommended)*

```bash
docker-compose up --build
```

This starts the frontend, backend, and PostgreSQL together in one command.

---

## Deployment

<details>
<summary><strong>Frontend → Vercel</strong></summary>

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → Import your repo
3. Set **Root Directory** to `frontend`
4. Add environment variable: `BACKEND_URL = your Railway backend URL`
5. Deploy

</details>

<details>
<summary><strong>Backend → Railway</strong></summary>

1. Go to [railway.com](https://railway.com) → New Project → Deploy from GitHub
2. Set **Root Directory** to `backend`
3. Add environment variables from `backend/.env.example`
4. Deploy — Railway auto-detects the Dockerfile

</details>

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/problems` | List all problems (with filters) |
| `GET` | `/api/problems/{slug}` | Get problem details |
| `POST` | `/api/query/execute` | Execute SQL query in sandbox |
| `GET` | `/api/progress` | Get user progress |

Full API docs available at `http://localhost:8001/docs` (Swagger UI) when running locally.

---

## Roadmap

- [ ] **AI-powered query reviewer** — get natural language feedback on your SQL
- [ ] **Docker-based query sandbox** for full execution isolation
- [ ] **Skill tree visualization** — see your learning path across concepts
- [ ] **More datasets** — education, social media, logistics, SaaS metrics
- [ ] **Onboarding tutorial tour** for new users
- [ ] **Community solutions** — browse and upvote top solutions per problem
- [ ] **SQL interview simulator** — live timer, hints disabled, score report

---

## Contributing

Contributions are welcome! If you'd like to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

**High-priority areas:**
- Adding new datasets (education, social media, logistics)
- More SQL problems (especially hard-level window function challenges)
- AI-powered query review integration
- UI/UX improvements

Please open an issue first for major changes so we can discuss the approach.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ for the SQL community by [Amarnath Allamraju](https://www.linkedin.com/in/amarnathallamraju/)

⭐ **If SQLit helped you, consider starring the repo!**

</div>
