# Architecture Decisions

ADR-001: Modular monolith — simpler development, testing, deployment and viva explanation.
ADR-002: SQLite MVP — zero infrastructure and easy demonstration.
ADR-003: AI optional — avoids provider dependency and API cost.
ADR-004: Safe CTF model — prevents arbitrary code execution.
ADR-005: Vertical slices — each milestone becomes demonstrable and testable.

ADR-006: Clerk for authentication (Phase 2) — CyberDesk uses Clerk (frontend:
`@clerk/react`, backend: `clerk-backend-api`) for identity instead of local
password-based authentication. Clerk owns credentials, sessions, and
sign-up/sign-in/sign-out UI; CyberDesk never stores or hashes a password.
This supersedes the password-hash based flow implied by the original
`specs/AUTHENTICATION.md` and the `password_hash` field in
`specs/DATABASE.md`'s `User` entity, and replaces the originally specced
`POST /auth/register`, `POST /auth/login`, `POST /auth/logout` backend
routes (handled client-side against Clerk instead) with `GET /api/users/me`.
Rationale: avoids building/maintaining secure credential storage ourselves,
which is unnecessary complexity for an academic MVP and a larger security
surface to defend in a viva. `specs/AUTHENTICATION.md`, `specs/API.md`, and
`specs/DATABASE.md` should be treated as superseded on these specific points
by this ADR; the underlying goals they express (registration, login, roles,
server-side authorization) are still met, just via Clerk.

ADR-007: Minimal local AppUser table — CyberDesk stores only
`clerk_user_id`, `role`, and timestamps locally (see specs/DATABASE.md
discussion in Phase 2 report). Profile data (email, name) stays in Clerk
and is not duplicated locally, avoiding sync drift. A local integer `id`
exists so future tables (progress, quiz attempts, challenge submissions)
have a stable local FK target instead of joining on an external string ID.

ADR-008: Role assignment — a Clerk-authenticated user with no existing
`AppUser` row is lazily created with `role="student"` on first
authenticated request. There is no self-service endpoint to change one's
own role. Promoting a user to `admin` is an out-of-band manual action
(direct DB update) in Phase 2; a safe admin-management endpoint is
deferred to a later phase. This keeps privilege escalation outside the
Phase 2 attack surface entirely.
