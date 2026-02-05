"""Lightweight DB adapter stub used by orchestrator and tests.

In production this would be a real Postgres adapter; here it's a small
pluggable module so integration tests can patch its behavior.
"""
def push_hitl(task_obj: dict) -> bool:
    """Push a task into the HITL queue (stub).

    Returns True on success. Tests can patch this function to assert calls.
    """
    # No-op for now; real implementation would insert into PostgreSQL.
    return True
