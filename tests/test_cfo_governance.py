import pytest


def test_cfo_budget_guardrail_blocks_overspend():
    """Failing spec: transferring above daily spend limit must be blocked.

    Specification: A `budget_check` guard or equivalent MUST prevent transfers
    that would exceed the configured `DAILY_SPEND_LIMIT_USDC` environment value.

    This test intentionally fails until the guardrail is implemented.
    """
    import os

    # Ensure a low daily limit to trigger the guard in the spec
    os.environ["DAILY_SPEND_LIMIT_USDC"] = "100.0"

    # Attempt to import the budget guard / payment API expected by the spec
    from skills.skill_onchain_payment.logic import PaymentProcessor

    processor = PaymentProcessor()

    # Attempt a payment that exceeds the daily limit (should be blocked)
    with pytest.raises(Exception):
        # The implementation should raise a BudgetExceededError (or similar)
        processor.execute_payment(amount=1000.0, recipient="0xdeadbeef")
