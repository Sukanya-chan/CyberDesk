# API Contract

Base prefix: `/api`

Health: GET `/health`
Auth: POST `/auth/register`, POST `/auth/login`, POST `/auth/logout`, GET `/auth/me`
Learning: GET `/categories`, GET `/courses`, GET `/courses/{id}`, GET `/lessons/{id}`, POST `/lessons/{id}/complete`
Quiz: GET `/quizzes`, GET `/quizzes/{id}`, POST `/quizzes/{id}/attempts`, GET `/quizzes/{id}/attempts`
Progress: GET `/progress/me`
Search: GET `/search?q=...`
Admin: protected CRUD endpoints for approved management functions.

Define exact request/response schemas before implementing each module.
