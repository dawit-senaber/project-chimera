import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock

from skills.commerce_manager import CommerceManager, BudgetExceededError


@pytest.mark.asyncio
async def test_budget_check_rejects_when_over_limit():
    mock_redis = MagicMock()
    # Simulate Redis eval returning -1 (would exceed limit)
    mock_redis.eval.return_value = -1
    mock_wallet = AsyncMock()
    mgr = CommerceManager(redis_client=mock_redis, wallet_provider=mock_wallet, agent_id="agentA")

    with pytest.raises(BudgetExceededError):
        await mgr.send_payment("0xabc", 1000.0)

    mock_redis.eval.assert_called_once()
    mock_wallet.transfer.assert_not_called()


@pytest.mark.asyncio
async def test_send_payment_success_and_redis_updated():
    mock_redis = MagicMock()
    # Simulate successful reservation returning new total (string or float)
    mock_redis.eval.return_value = 25.0
    mock_wallet = AsyncMock()
    mock_wallet.transfer.return_value = {"tx_hash": "0xdeadbeef"}

    mgr = CommerceManager(redis_client=mock_redis, wallet_provider=mock_wallet, agent_id="agentB")

    resp = await mgr.send_payment("0xdef", 10.0)

    assert resp["tx_hash"] == "0xdeadbeef"
    mock_redis.eval.assert_called_once()
    mock_wallet.transfer.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_payment_rolls_back_on_provider_failure():
    mock_redis = MagicMock()
    mock_redis.eval.return_value = 5.0
    # Make wallet.transfer raise
    mock_wallet = AsyncMock()
    mock_wallet.transfer.side_effect = RuntimeError("provider down")

    mgr = CommerceManager(redis_client=mock_redis, wallet_provider=mock_wallet, agent_id="agentC")

    with pytest.raises(RuntimeError):
        await mgr.send_payment("0xghi", 3.0)

    # On failure, release (incrbyfloat) should be called to revert reservation
    mock_redis.incrbyfloat.assert_called()
    mock_redis.eval.assert_called_once()
