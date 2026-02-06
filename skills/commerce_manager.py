import os
import asyncio
from typing import Optional


class BudgetExceededError(Exception):
    pass


def budget_check(func):
    async def wrapper(self, to_address: str, amount_usdc: float, *args, **kwargs):
        key = f"{self.redis_key_prefix}:{self.agent_id or 'global'}"
        limit = float(os.getenv("MAX_DAILY_LIMIT", str(self.default_daily_limit)))
        # Reserve amount atomically via Redis EVAL script
        new_total = await asyncio.to_thread(self._reserve_amount, key, amount_usdc, limit)
        if new_total == -1:
            raise BudgetExceededError(f"Daily limit exceeded: {amount_usdc} would exceed {limit}")
        try:
            return await func(self, to_address, amount_usdc, *args, **kwargs)
        except Exception:
            # release reserved amount on failure
            await asyncio.to_thread(self._release_amount, key, amount_usdc)
            raise

    return wrapper


class CommerceManager:
    """Prototype CommerceManager integrating with Coinbase AgentKit (skeleton).

    This class is deliberately lightweight and testable. It expects a Redis-like
    client to be passed in that exposes `eval` and `incrbyfloat` methods (redis-py
    compatible). The `wallet_provider` should expose an async `transfer` method.
    """

    default_daily_limit = 50.0

    def __init__(self, redis_client, wallet_provider=None, agent_id: Optional[str] = None, redis_key_prefix: str = "daily_spend"):
        self.redis = redis_client
        self.wallet_provider = wallet_provider
        self.agent_id = agent_id
        self.redis_key_prefix = redis_key_prefix

        # Read env keys for AgentKit (not used by prototype)
        self.cdp_api_key_name = os.getenv("CDP_API_KEY_NAME")
        self.cdp_api_private = os.getenv("CDP_API_KEY_PRIVATE_KEY")

    def _reserve_amount(self, key: str, amount: float, limit: float):
        """Atomically check and add `amount` to `key` if it doesn't exceed `limit`.

        Returns new total as float, or -1 if would exceed limit.
        """
        # Lua script: if current + amount > limit then return -1 else INCRBYFLOAT and return new value
        script = r"""
local key = KEYS[1]
local amount = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local cur = tonumber(redis.call('GET', key) or '0')
if (cur + amount) > limit then
  return -1
end
local new = redis.call('INCRBYFLOAT', key, amount)
return new
"""
        # redis_client.eval returns result; ensure args are strings
        return self.redis.eval(script, 1, key, str(amount), str(limit))

    def _release_amount(self, key: str, amount: float):
        # decrement by amount
        return self.redis.incrbyfloat(key, -float(amount))

    async def _erc20_transfer(self, to_address: str, amount_usdc: float):
        """Perform the ERC20 transfer using the wallet provider.

        This is a thin wrapper to allow mocking in tests.
        """
        if not self.wallet_provider:
            raise RuntimeError("No wallet provider configured")
        # Expect wallet_provider.transfer to be async
        return await self.wallet_provider.transfer(to_address, amount_usdc)

    @budget_check
    async def send_payment(self, to_address: str, amount_usdc: float) -> dict:
        """Send payment in USDC to `to_address`.

        Returns provider response (transaction metadata).
        """
        resp = await self._erc20_transfer(to_address, amount_usdc)
        return resp
