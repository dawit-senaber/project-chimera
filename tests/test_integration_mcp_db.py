import pytest
from unittest.mock import patch

from main import ChimeraOrchestrator


def test_judge_escalates_to_hitl():
    orch = ChimeraOrchestrator()
    sample_result = {"content": "Test content", "confidence": 0.5}

    with patch("skills.db_adapter.push_hitl") as mock_push:
        # Call judge_step synchronously via asyncio run
        import asyncio

        res = asyncio.run(orch.judge_step(sample_result))
        assert res is False
        mock_push.assert_called_once_with(sample_result)
