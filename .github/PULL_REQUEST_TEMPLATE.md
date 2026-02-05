<!-- Title -->
<!-- Short summary of the change -->

## Summary
Describe the change and why it's needed. Link to specs or issues when applicable.

## Changes
- Add spec-check and JSON-schema validation
- Add integration tests for notification and HITL escalation
- Add `jsonschema` dependency to `pyproject.toml`

## How to test locally
```bash
make spec-check
uv run pytest
```

## Checklist
- [ ] Spec-check passes locally
- [ ] Tests pass locally
- [ ] CI passes

## Notes for reviewers
Please check that spec changes (if any) are intentional and that new failing tests are preserved as TDD empty slots.
