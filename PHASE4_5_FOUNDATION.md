# Phase 4 + Phase 5 Foundation

This checkpoint starts the two workstreams in parallel without adding paid
services or an AI runtime dependency.

## Phase 4A — Assessment foundation

Implemented SQLAlchemy models for the MVP multiple-choice assessment system:

- `Quiz` — course-scoped, draft/published.
- `Question` — ordered MCQ question.
- `QuestionOption` — ordered answer option with server-side `is_correct`.
- Cascading quiz -> questions -> options deletion.
- Database checks for valid quiz status and MCQ type.

Security rule: public quiz response schemas must not expose `is_correct` before
submission. Exactly one correct option per question is a service-layer rule,
not a cross-row SQL constraint.

## Phase 5A — Safe challenge foundation

Implemented the safe flag-based `Challenge` model with:

- unique slug
- title/description/instructions/hint
- easy/medium/hard difficulty
- challenge category
- positive point value
- draft/published status
- server-side `flag_hash`

Plaintext flags are intentionally not stored in the model and must never be
returned by public APIs.

The MVP remains restricted to safe challenge patterns from `specs/CTF_SYSTEM.md`:
static flag discovery, encoded-message decoding, log/packet/configuration
analysis, and simulated security logic. No arbitrary shell/code execution,
external target scanning, malware execution, or credential theft.

## Verification

From `backend/`:

```bash
PYTHONPATH=. pytest -v
```

The Phase 4/5 model tests are in `tests/test_phase4_5_models.py`.
