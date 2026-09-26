# AI Workflow Rules

AI is an engineering assistant, not the project owner.

## Before implementation
Read context → inspect repository → identify affected modules → make a plan → identify risks.

## During implementation
Build vertical slices. Reuse abstractions. Do not invent requirements. Keep changes reversible.

## Verification
Run targeted tests, type/lint checks where available, API/UI checks and a security review for sensitive changes.

## Prompt contract
CONTEXT → TASK → CONSTRAINTS → ACCEPTANCE CRITERIA → VERIFICATION

## OpenRouter
Use stronger models for architecture and difficult debugging; cheaper models for small edits/docs/tests. Never accept generated code without verification.
