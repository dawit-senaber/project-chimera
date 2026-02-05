Title: CI: Add spec-check gating, JSON-schema validation, integration tests

Description
-----------
This PR implements the Orchestrator-level governance improvements requested for Project Chimera:

- Add `scripts/spec_check.py` to validate runtime skill interfaces against JSON schemas.
- Add JSON schemas under `specs/schemas/` for `TrendFetcher`, `MediaGenerator`, and `PaymentProcessor`.
- Integrate `jsonschema` into project dependencies (`pyproject.toml`) and make `make spec-check` run the script.
- Add `skills/db_adapter.py` stub and integration tests for HITL escalation.
- Implement `fetch_interface()` helpers for skills to support spec-checking.
- Add `skill_email_sender` with tests and integrated batch dry-run notifications.
- Add CONTRIBUTING.md describing Spec-Driven workflow and TDD story.

Why
---
These changes turn the `specs/` documents into active gatekeepers, enforcing contract alignment before tests run. This raises the project's governance posture for the FDE evaluation.

Testing
-------
Run locally:

```bash
make spec-check
uv run pytest
```

Checklist
---------
- [ ] `make spec-check` passes locally
- [ ] `uv run pytest` passes locally
- [ ] CI passes on PR (spec-check + tests)

Notes
-----
This is a draft PR. If you'd like, I can also open the PR remotely (requires git remote access). See the commands below to create the branch and push.
