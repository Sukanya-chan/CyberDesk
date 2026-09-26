# Architecture

## Style
Modular monolith for the MVP.

## Frontend
React + TypeScript.

Suggested:
src/
  app/
  components/
  features/
  pages/
  hooks/
  services/
  types/
  utils/

## Backend
Python + FastAPI.

Suggested:
backend/app/
  api/
  core/
  models/
  schemas/
  services/
  repositories/
  db/
  main.py

## Database
SQLite for MVP. Keep schema choices reasonably PostgreSQL-compatible.

## API
REST + JSON with consistent validation, status codes, response schemas, errors and pagination.

## Boundaries
Auth = identity/roles.
Learning = courses/topics/lessons.
Quiz = questions/attempts/scoring.
Challenge = safe exercises/submissions.
Progress = completion/learning metrics.
Admin = management.
Search = approved searchable content.
AI = optional integration layer.

Prefer simple explicit interfaces over hidden cross-module behavior.
