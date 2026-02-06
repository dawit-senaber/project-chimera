import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

# Build DSN from `DATABASE_URL` if provided, otherwise compose from postgres-related env vars.
db_name = os.environ.get("POSTGRES_DB") or os.environ.get("DB_NAME") or "chimera_test"
db_user = os.environ.get("POSTGRES_USER") or os.environ.get("DB_USER") or "chimera"
db_pass = os.environ.get("POSTGRES_PASSWORD") or os.environ.get("DB_PASSWORD") or "chimera"
db_host = os.environ.get("POSTGRES_HOST") or os.environ.get("DB_HOST") or os.environ.get("DATABASE_HOST") or "postgres"

DB_DSN = os.environ.get("DATABASE_URL") or f"dbname={db_name} user={db_user} password={db_pass} host={db_host}"

def wait_for_db(timeout: int = 30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            conn = psycopg2.connect(DB_DSN)
            conn.close()
            return True
        except Exception:
            # Sleep and retry; caller can inspect container logs for details if needed.
            time.sleep(1)
    return False

def push_hitl(task_obj: dict) -> bool:
    """Insert a HITL task into a `hitl_tasks` table.

    Creates the table if missing. Returns True on success.
    """
    if not wait_for_db():
        return False
    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS hitl_tasks (id SERIAL PRIMARY KEY, payload JSONB, created_at TIMESTAMP DEFAULT now())"
    )
    cur.execute("INSERT INTO hitl_tasks (payload) VALUES (%s)", (psycopg2.extras.Json(task_obj),))
    conn.commit()
    cur.close()
    conn.close()
    return True
