<p align="center">
  <img src="https://img.shields.io/badge/SQL-Practice%20Platform-6C5CE7?style=for-the-badge&logo=postgresql&logoColor=white" alt="SQLit" />
</p>

<h1 align="center">SQLit — LeetCode for SQL</h1>

<p align="center">
  Master SQL through hands-on practice with real-world datasets, instant feedback, and an in-browser query engine.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16-black?logo=next.js" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/TailwindCSS-4-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind" />
</p>

---

## What is SQLit?

**SQLit** is a free, open-source platform to practice SQL — like LeetCode, but specifically designed for databases. Write real queries against real schemas, get instant results, and level up from beginner to expert.

Whether you're prepping for a data engineering interview, learning SQL for the first time, or brushing up on window functions — SQLit has you covered.

---

## Features

### Practice Problems
- **412 curated problems** across Easy, Medium, and Hard difficulties
- Covers JOINs, subqueries, CTEs, window functions, aggregations, and more
- Problems organized by concept tags and categories
- Hints, explanations, and multiple solution approaches for every problem

### In-Browser SQL Engine
- Write and execute SQL directly in the browser — no setup required
- Supports **SQLite** (instant, client-fallback) and **PostgreSQL** (production sandbox)
- **MySQL dialect support** via automatic syntax translation
- Sandboxed execution with timeout protection and rate limiting

### Real-World Datasets
- **E-Commerce** — customers, orders, products, reviews
- **Finance** — accounts, transactions, portfolios, market data
- **Healthcare** — patients, diagnoses, prescriptions, appointments
- Interactive dataset explorer with schema diagrams, column types, and sample data

### Query Optimization Lab
- Visual **EXPLAIN plan analyzer** with color-coded node types
- See Seq Scan vs Index Scan, Nested Loop vs Hash Join
- Learn to read and optimize execution plans

### Database Design Studio
- Interactive **ER Diagram Builder** — drag-and-drop entities on an SVG canvas
- Add tables, columns (19 PostgreSQL types), primary keys, and foreign keys
- **Export to SQL DDL** with one click
- **Import from SQL** — paste CREATE TABLE statements and get a visual diagram
- Schema normalization guide and best practices

### Interview Prep
- Timed SQL challenges simulating real interview conditions
- Company-style question sets (FAANG, startups, finance)
- Difficulty progression from phone screen to on-site level

### Daily Challenges
- Fresh SQL problem every day with a countdown timer
- Streak tracking to keep you consistent

### Profile & Progress
- **GitHub-style activity heatmap** showing your solve history
- **Concept badges** — earn Beginner → Learner → Proficient → Expert → Master per topic
- XP system with level progression
- Track solved problems, accuracy, and streaks

### Developer Experience
- Light and dark theme with smooth toggle
- Resizable editor panels
- Syntax-highlighted SQL editor with auto-formatting
- Mobile-responsive design
- SEO optimized with sitemap and meta tags

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
├── frontend/                # Next.js app
│   ├── src/
│   │   ├── app/             # Pages (App Router)
│   │   │   ├── (main)/      # All authenticated routes
│   │   │   │   ├── practice/ # Problem list + solver
│   │   │   │   ├── datasets/ # Dataset explorer
│   │   │   │   ├── db-design/# ER builder + normalization
│   │   │   │   ├── optimization/ # EXPLAIN visualizer
│   │   │   │   ├── interview/# Interview prep
│   │   │   │   ├── profile/  # Activity heatmap + badges
│   │   │   │   └── ...
│   │   │   └── api/          # API route proxies
│   │   ├── components/       # Reusable UI components
│   │   ├── stores/           # Zustand state stores
│   │   └── lib/              # Utilities, API client, schemas
│   └── package.json
│
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Config, auth, database, rate limiter
│   │   ├── datasets/         # E-commerce, Finance, Healthcare
│   │   ├── models/           # SQLAlchemy models
│   │   └── services/         # Query executor, problem service
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml        # Full-stack local development
```

---

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 16+ (optional — SQLite fallback works out of the box)

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

Open `http://localhost:3000` and start practicing!

### 4. (Optional) Full stack with Docker

```bash
docker-compose up --build
```

This starts the frontend, backend, and PostgreSQL together.

---

## Deployment

### Frontend → Vercel

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → Import your repo
3. Set **Root Directory** to `frontend`
4. Add environment variable: `BACKEND_URL` = your Railway backend URL
5. Deploy

### Backend → Railway

1. Go to [railway.com](https://railway.com) → New Project → Deploy from GitHub
2. Set **Root Directory** to `backend`
3. Add environment variables from `backend/.env.example`
4. Deploy — Railway auto-detects the Dockerfile

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/problems` | List all problems (with filters) |
| `GET` | `/api/problems/{slug}` | Get problem details |
| `POST` | `/api/query/execute` | Execute SQL query in sandbox |
| `GET` | `/api/progress` | Get user progress |

---

## Contributing

Contributions are welcome! Here are some areas where help is needed:

- [ ] More datasets (education, social media, logistics)
- [ ] Docker-based query sandbox for full isolation
- [ ] AI-powered query reviewer
- [ ] Skill tree visualization
- [ ] Onboarding tutorial tour

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for the SQL community
</p>
