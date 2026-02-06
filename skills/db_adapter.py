"""DB adapter wrapper.

By default this module exposes `push_hitl()` which delegates to the
Postgres implementation when `DB_ADAPTER=postgres` is set in the env.
This keeps tests lightweight while allowing full integration tests to
swap in `skills.db_postgres`.
"""
import os

ADAPTER = os.environ.get("DB_ADAPTER", "stub")

if ADAPTER == "postgres":
    from .db_postgres import push_hitl  # type: ignore
else:
    def push_hitl(task_obj: dict) -> bool:
        """Stubbed push_hitl used for unit tests and CI by default."""
        return True
