# Human-in-the-Loop (HITL) Guidelines

Purpose
-------
This document defines when and how human moderators (HITL) should review, approve,
or escalate tasks that the automated system cannot safely resolve. It implements the
operational side of the project's governance runbook and ensures consistent, auditable
decisions for PII, safety, and high-value operations.

Trigger Criteria (When to Intervene)
-----------------------------------
- PII Detection or Ambiguity: Any payload where `redact_pii()` reports ambiguity, or
  where patterns are found but confidence is low.
- Safety Flags: Any task flagged by Judge agents for policy, safety, toxicity, or
  hallucination risks.
- High-Value Financial Actions: Transactions above configured thresholds (see
  corporate `Budget Controls`) or any payment/withdrawal where the `CFO Judge` flags risk.
- Low Confidence Decisions: Judge confidence below configured threshold or failing
  automated schema/contract checks.
- Legal / Compliance Requests: Requests that appear to contain regulated data (e.g., SSNs,
  health data, legal documents) or that require consent to forward.

Reviewer Checklist (Actionable Steps)
------------------------------------
1. Confirm Identity & Scope
   - Verify the task id, agent id, and relevant metadata are present.
   - Confirm the scope of requested action and the minimal data needed.

2. Verify Redaction
   - Inspect what `redact_pii()` removed or replaced.
   - If the redaction appears incomplete or ambiguous, perform manual redaction.
   - Record the redaction method and exact fields redacted in the audit entry.

3. Validate Budget & Authorization
   - For commerce actions, check budget limits and approvals via the `CFO Judge` UI.
   - Confirm that payment recipients and amounts match supporting evidence.

4. Confirm Disclosure & Consent
   - Ensure any user-consent flags are present before forwarding raw data.
   - If consent is missing and required, pause the task and request consent via the appropriate channel.

5. Execute or Reject
   - If safe, annotate the task with the moderator decision, sign it (moderator id),
     and mark the task as approved for commit.
   - If rejecting, provide a clear reason and recommended remediation for the Planner.

6. Log & Notify
   - Create an immutable audit record containing: unique audit id, timestamp, moderator id,
     redaction summary, decision, and any uploaded evidence. Store in the append-only ledger.
   - Notify downstream Judge/Planner agents and relevant managers of the decision.

Escalation Path
---------------
1. If the moderator cannot decide (policy ambiguity or missing evidence), escalate to the
   HITL Queue lead or on-call human reviewer.
2. If the HITL lead cannot resolve within SLA, escalate to the Super-Orchestrator with the
   full audit trace and a clear summary of outstanding questions.
3. For incidents involving secrets exposure or suspected data breach, immediately follow
   the incident response playbook and notify Security and the Super-Orchestrator.

Audit Requirements
------------------
- Every human decision must be logged to the immutable ledger (Postgres append-only table
  with optional chain anchoring). Logs must include: audit id, task id, agent id, moderator id,
  timestamp, redaction details, decision, and free-text rationale.
- Logs must never include raw secrets or unredacted PII. If raw evidence is required for legal
  reasons, store it only in a secure evidence vault with restricted access, and reference it
  by artifact id in the audit record.

SLA & Timing
------------
- Default HITL SLA: 4 hours for non-critical tasks, 30 minutes for high-risk or financial tasks.
- If SLA will be missed, the moderator must escalate to the HITL lead and document the reason.

Moderator Tools & Templates
--------------------------
- Use the `HITL Review Template` in the moderation UI which auto-populates task metadata.
- For redaction review, use the `redaction diff` view that highlights removed substrings.
- For financial review, refer to the `CFO Judge` audit ledger and approval matrix.

Operational Notes
-----------------
- Training: Moderators must complete base privacy, compliance, and redaction training.
- Rotation & On-call: Maintain an on-call schedule for HITL leads with contact information.
- Continuous Improvement: Moderators should flag recurring patterns that suggest improved
  automated redaction or Judge rule updates; file these as policy PRs against `AGENTS.md`.

Appendix: Example HITL Review Template (fields)
- Audit ID
- Task ID
- Agent ID
- Detected PII Summary
- Redaction Actions Taken
- Decision (Approve / Reject / Escalate)
- Moderator ID
- Timestamp
- Notes / Rationale
