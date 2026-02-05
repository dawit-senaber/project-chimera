import pytest
from unittest.mock import patch, AsyncMock

from main import ChimeraOrchestrator
from skills.skill_email_sender.logic import EmailSender


@pytest.mark.asyncio
async def test_orchestrator_notification_integration():
    """Simulate one swarm tick and verify a summary notification is prepared and sent (dry-run)."""
    orch = ChimeraOrchestrator()

    with patch("skills.skill_trend_fetcher.logic.TrendFetcher.fetch_trends", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = ["AI Agents", "On-chain Identity"]

        with patch("skills.skill_email_sender.logic.EmailSender.send") as mock_send:
            # Run planner, worker, judge flow
            tasks = await orch.planner_step()
            published = []
            for t in tasks:
                worker_output = await orch.worker_step(t)
                approved = await orch.judge_step(worker_output)
                if approved:
                    published.append(worker_output["content"]) 

            # Ensure we got the expected published items
            assert len(published) == 2

            # Prepare a batch summary and call the notifier (dry-run)
            subject = f"Chimera Digest: {len(published)} published items"
            body = "Published items:\n" + "\n".join(f"- {p}" for p in published)
            sender = EmailSender()
            sender.send(subject=subject, body=body, to=["test@example.com"], dry_run=True)

            # Verify notifier was invoked and payload contains trend topics
            mock_send.assert_called_once()
            _, kwargs = mock_send.call_args
            assert "AI Agents" in kwargs.get("body", "")
            assert "On-chain Identity" in kwargs.get("body", "")
