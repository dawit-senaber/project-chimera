import os


class BudgetExceededError(Exception):
    pass


class PaymentProcessor:
    def __init__(self):
        self.network = "testnet"

    def execute_payment(self, amount: float, recipient: str) -> dict:
        """Simulates an on-chain transaction with a CFO budget guard.

        Reads `DAILY_SPEND_LIMIT_USDC` from the environment and raises
        `BudgetExceededError` if the requested `amount` exceeds the limit.
        """
        limit_val = os.getenv("DAILY_SPEND_LIMIT_USDC")
        if limit_val is not None:
            try:
                limit = float(limit_val)
            except ValueError:
                limit = float("inf")
        else:
            limit = float("inf")

        if amount > limit:
            raise BudgetExceededError(f"Requested amount {amount} exceeds daily limit {limit}")

        return {
            "tx_hash": f"0x_chimera_{amount}_{recipient[:5]}",
            "status": "success",
            "network": self.network
        }

    def fetch_interface(self) -> dict:
        """Return a simple input contract description for spec-checking."""
        return {
            "title": "PaymentProcessor Input Contract",
            "type": "object",
            "properties": {
                "recipient_address": {"type": "string"},
                "amount_usdc": {"type": "number"},
                "memo": {"type": "string"}
            },
            "required": ["recipient_address", "amount_usdc"]
        }