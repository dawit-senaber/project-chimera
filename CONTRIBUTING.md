# Contributing to Project Chimera

Thank you for contributing. Project Chimera follows a Spec-Driven Development (SDD)
and strong governance model — please read this file before making changes.

## Core Principles
- **Specs are the Source of Truth:** Always consult `specs/` (especially `technical.md`) before implementing behavior.
- **Explain Before You Code:** For non-trivial changes, open an issue or draft a short design note describing how the change maps to the spec.
- **TDD-First for Safety:** Critical governance features should be introduced as failing tests first (see `tests/test_cfo_governance.py`).

## Branching & Commits
- Branch from `main` for each work item using short, descriptive names: `feature/`, `fix/`, `chore/`.
- Commit messages should follow this template:

  ```txt
  <type>(<scope>): <short summary>

  Longer description (optional). Reference spec or issue: #123
  ```

  - `type` = feat | fix | docs | chore | test | ci
  - `scope` = subsystem (e.g., trend_fetcher, media_gen)

## Pull Requests
- Open a PR against `main` with a clear description linking specs and tests updated.
- The CI must pass (spec-check + tests) before merge.
- At least one approver must verify spec alignment and security implications.

## Tests & Validation
- Run the unit and integration tests locally:

  ```bash
  uv run pytest
  ```

- Run the spec-check before pushing changes (this is also required by CI):

  ```bash
  make spec-check
  ```

- Important: Some tests are intentionally failing (TDD empty slots). Do not remove the failing test(s) without adding a spec-approved implementation and test updates.

## Spec-Driven Rules for Code Authors
- Map every new public function/class to a spec entry under `specs/`.
- If you change a spec, update the schema in `specs/schemas/` and the `scripts/spec_check.py` helpers.
- Add `fetch_interface()` helpers for skills to expose machine-readable input contracts.

## Security & Secrets
- Never commit secrets or credentials. Use environment variables and document required env vars in `SKILL.md` or `README.md`.

## MCP Telemetry & Demo Requirements
- Keep Tenx MCP Sense connected while developing where possible; capture and include a short telemetry snippet in demo artifacts.
- For the submission/demo, be prepared to show:
  - `make spec-check` passing
  - One integration test demonstrating an end-to-end flow
  - The failing TDD test that defines an empty slot for agents

## CI & Quality Gates
- CI runs `make spec-check` then builds and runs tests inside Docker. The PR must pass both gates.
- Linting and static checks are run via the dev toolchain (`black`, `ruff`) — run them locally before PR.

## Contacts
- Primary: Repo owner / maintainer (see `README.md`)

Thank you for helping keep Project Chimera robust, auditable, and spec-driven.
