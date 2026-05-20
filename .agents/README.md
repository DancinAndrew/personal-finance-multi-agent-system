# Project-Local Agent Assets

This directory vendors the Everything Claude Code / ECC assets used by this repo.

- `skills/`: reusable workflow skills for coding standards, testing, API design, backend patterns, security review, search-first work, verification, and git workflow.
- `rules/ecc/common/`: common engineering rules.
- `rules/ecc/python/`: Python-specific engineering rules.

The root `AGENTS.md` explains when these assets should be consulted. If a rule or skill conflicts with user instructions, system instructions, or root `AGENTS.md`, the higher-priority instruction wins.
