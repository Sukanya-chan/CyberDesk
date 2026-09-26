# CyberDesk — Phase 1: Foundation

This is the Phase 1 foundation: a running frontend and backend shell with a
health check connecting them, no domain features yet. See `specs/` and
`context/` for the full project plan; see `context/Progress_tracker.md` for
current status.

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Run the backend

```bash
uvicorn app.main:app --reload
```

The API is served at `http://localhost:8000`. Health check:
`http://localhost:8000/api/health`

### Run backend tests

```bash
pytest
```

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env
```

### Run the frontend

```bash
npm run dev
```

The app is served at `http://localhost:5173` and calls the backend's
`/api/health` endpoint on load.

### Run frontend tests

```bash
npm run test
```

## Verifying the full stack

1. Start the backend (`uvicorn app.main:app --reload`) in one terminal.
2. Start the frontend (`npm run dev`) in another terminal.
3. Open `http://localhost:5173` — it should show `Status: ok` and
   `Database: ok`, confirming frontend → backend → database connectivity.

## What's in Phase 1

- FastAPI backend with `/api/health`, CORS restricted to the local
  frontend origin, and consistent JSON error responses (no stack traces
  leaked to clients).
- SQLAlchemy connection layer against SQLite (`DATABASE_URL` in `.env`),
  with no domain tables yet.
- React + TypeScript frontend shell that calls the backend on load and
  renders loading / success / error states.
- Backend tests (`pytest`) and frontend tests (`vitest`).

## What's intentionally NOT in Phase 1

Authentication (Clerk), roles, dashboard, lessons, quizzes, search,
CTF challenges, admin panel, notifications, AI features, and production
deployment. These are planned in later phases per `specs/FEATURES.md`.

## Known limitations

- No client-side routing yet — a single page is rendered directly. Routing
  will be introduced once a second real page exists (Phase 2+).
- No domain database schema yet — only the connection layer is verified.
- No CI pipeline configured yet; tests are run locally.
