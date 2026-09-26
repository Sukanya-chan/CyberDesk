# CyberDesk — AI Engineering Instructions

## Mission
CyberDesk is a student-focused cybersecurity learning and practical toolkit platform. Build it as a secure, explainable, testable academic project.

## Before changing code
Read:
1. `AGENTS.md`
2. `context/Project_Overview.md`
3. `context/Architecture.md`
4. `context/Technology_stack.md`
5. `context/Constraints.md`
6. `context/Code_standards.md`
7. `context/Security.md`
8. the relevant file in `specs/`
9. `context/Progress_tracker.md`

Do not invent undocumented requirements.

## Workflow
UNDERSTAND → INSPECT → PLAN → IMPLEMENT → TEST → REVIEW → DOCUMENT

Inspect existing code before creating replacements. Make the smallest coherent change. Do not rewrite unrelated code.

## Architecture
Use a modular monolith:
Browser/UI → REST API → services → repositories/data access → database.

## Security
- Never execute arbitrary user code on the host.
- CTF challenges must be safe and isolated.
- Validate external input.
- Enforce authorization server-side.
- Never commit secrets.
- Treat uploads as untrusted.
- Do not expose stack traces or sensitive internals.
- Apply least privilege.

## AI
AI is optional. Core learning, quizzes, progress, search and admin functionality must work without AI.
Provider-specific AI code must be isolated behind a service layer and use environment variables.

## Scope discipline
- No unnecessary frameworks.
- No duplicate utilities/services.
- No silent database/API contract changes.
- No speculative features.
- No unrelated refactors.
- Prefer a finished small feature over a half-finished large feature.

## After every task report
- changed files
- behavior implemented
- tests/checks run and results
- API/database changes
- security considerations
- limitations
