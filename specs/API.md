# API Contract

Base prefix: `/api`

## Public

- `GET /health`
- `GET /categories`
- `GET /courses`
- `GET /courses/{course_slug}`
- `GET /lessons/{course_slug}/{lesson_slug}`

Public learning endpoints expose published courses and lessons only. A published course's modules remain visible even when a module has no published lessons.

## Authentication

- `GET /users/me`
- `GET /admin/ping`

Clerk authentication and local role authorization are provided by Phase 2.

## Admin Learning

Admin-only:

- `GET/POST /admin/categories`
- `PATCH/DELETE /admin/categories/{category_id}`
- `GET/POST /admin/courses`
- `PATCH/DELETE /admin/courses/{course_id}`
- `GET /admin/courses/{course_id}/modules`
- `POST /admin/modules`
- `PATCH/DELETE /admin/modules/{module_id}`
- `PATCH /admin/courses/{course_id}/modules/reorder`
- `GET /admin/modules/{module_id}/lessons`
- `POST /admin/lessons`
- `PATCH/DELETE /admin/lessons/{lesson_id}`
- `PATCH /admin/modules/{module_id}/lessons/reorder`

Reorder requests use `{"ordered_ids": [3, 1, 2]}` and must contain every child exactly once.

Quiz, progress, search, challenges, and AI endpoints remain future phases.
