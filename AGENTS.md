AGENTS.md — Governance and Operational Runbook

Purpose

This document defines roles, escalation paths, and privacy/compliance rules for Project Chimera. It is the authoritative governance artifact for agent lifecycle and incident handling.

Roles

- Super-Orchestrator: human lead; final authority for policy changes and emergency operations.
- Manager Agents: supervisor agents that coordinate Worker Swarms.
- Worker Agents: ephemeral executors that perform atomic tasks.
- Judge Agents: automated reviewers that validate Worker outputs before commit.
- HITL Moderators: human reviewers responsible for escalated content.

Escalation Path

1. Normal Flow: Worker produces result → Judge reviews.
2. If Judge approves: result is committed to GlobalState.
3. If Judge rejects: Planner receives feedback and re-queues/new tasks are generated.
4. If Judge cannot decide (confidence below threshold or safety flag): the task is routed to the HITL Queue for human review (this is the primary escalation path).
5. If HITL fails to resolve within SLA: escalate to Super-Orchestrator with full audit trace.

Privacy & Compliance

- PII Scrubbing: All Personally Identifiable Information (PII) MUST be redacted prior to being sent to any LLM or external MCP Server. Implement a centralized `redact_pii()` utility that runs on any data crossing the MCP boundary.
- Secrets Handling: Private keys, API secrets, and other sensitive material MUST be stored in an enterprise secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault). Secrets are injected into runtime via ephemeral environment variables and never logged.
- Data Minimization: Only the minimum context needed for task execution is forwarded to models; full transcripts or raw user data are not forwarded unless explicit user consent exists.
- Audit & Traceability: All actions (tool calls, approvals, transactions) are logged with immutable identifiers and stored in an append-only ledger (Postgres + optional chain anchor).

Operational Policies

- Budget Controls: All transaction-related tasks are gated by the CFO Judge and daily budget checks in Redis.
- Disclosure: Agents must self-disclose if directly asked about their nature. A standardized response template is enforced by the Judge.
- Rate Limits & Throttling: The MCP layer enforces platform rate limits to avoid account suspension or policy violations.

Adding / Updating Policies

- Governance changes must be proposed via a PR that updates `AGENTS.md` and the machine-enforceable policies under `specs/` and `.cursor/rules`.
- All changes require at least one human reviewer (Super-Orchestrator) and a passing CI run that validates schema/contract alignment.
