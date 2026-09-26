# CyberDesk AI Context System

Use this as the source-of-truth context package for AI-assisted development.

Recommended workflow:
1. Put these files in the CyberDesk repository.
2. Tell the agent to read `AGENTS.md`.
3. Keep `context/` stable project knowledge.
4. Keep `specs/` feature contracts.
5. Use `.ai/prompts/` for repeatable engineering tasks.
6. Update `context/Progress_tracker.md` after real milestones.
7. Record architecture changes in `context/Decisions.md`.

The agent must not convert its own assumptions into requirements.
