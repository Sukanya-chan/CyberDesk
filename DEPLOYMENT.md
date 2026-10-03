# CyberDesk Deployment & Production Readiness

## Local production-style run

Backend:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm run build
npm run preview
```

## Required backend environment

Copy `backend/.env.example` to `backend/.env` and set:

- `CLERK_SECRET_KEY`
- `CLERK_JWT_KEY` (optional)
- `CORS_ALLOWED_ORIGINS`
- `DATABASE_URL`

Optional:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`

Never commit `.env`.

## Database

SQLite is the documented MVP database. The SQLAlchemy layer uses `DATABASE_URL`, so a PostgreSQL deployment can be introduced without changing the REST contracts.

For production data, use a persistent database volume or a managed PostgreSQL database rather than an ephemeral SQLite filesystem.

## Security checklist

- Clerk authentication is required for student-owned progress, attempts and challenge submissions.
- Admin operations are protected server-side.
- Progress is calculated from server records.
- Gemini keys stay on the backend.
- CTF challenges never execute submitted code.
- Public learning APIs expose published content only.
- CORS is explicit rather than wildcard.
- Error responses avoid stack traces and implementation details.
- Secrets and local databases are excluded from Git.

## Release checklist

1. Configure environment variables.
2. Initialize the database.
3. Seed demonstration learning content if desired.
4. Run backend tests.
5. Run frontend tests.
6. Run the frontend production build.
7. Exercise login → dashboard → lesson completion → quiz → challenge → AI (if configured).
8. Review `git diff` for secrets and generated files.
