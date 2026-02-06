import os
import subprocess
import time
import pytest

# Skip this integration test if psycopg2 is not available in the environment.
psycopg2 = pytest.importorskip("psycopg2")


def wait_for_postgres(timeout=90):
    start = time.time()
    while time.time() - start < timeout:
        for host in ("127.0.0.1", "localhost"):
            try:
                conn = psycopg2.connect(
                    "dbname=chimera_test user=chimera password=chimera host=%s" % host
                )
                conn.close()
                return True
            except Exception as e:
                # record the exception and try the next host/iteration
                last_exc = e
        time.sleep(1)
    return False


def test_push_hitl_integration(tmp_path):
    """Integration test: run docker-compose postgres and verify `push_hitl` writes a row."""
    # Start postgres via docker-compose (uses service name 'postgres')
    subprocess.run(["docker", "compose", "up", "-d", "postgres"], check=True)

    # First try to connect from the host environment
    if wait_for_postgres():
        os.environ["DB_ADAPTER"] = "postgres"
        from skills.db_adapter import push_hitl

        ok = push_hitl({"task": "review", "payload": {"foo": "bar"}})
        assert ok
    else:
        # Fallback: invoke a one-off command inside the `agent-chimera` container
        # which runs in the same Docker network and can reach the `postgres` host.
        # Fallback: run helper script inside the agent container (avoids quoting issues)
        # Ensure the container's working directory is the project root so imports work
        # Force `/app` onto PYTHONPATH so the project package is importable
        res = subprocess.run(
            [
                "docker",
                "compose",
                "run",
                "--rm",
                "-w",
                "/app",
                "-e",
                "PYTHONPATH=/app",
                "agent-chimera",
                "python",
                "scripts/run_push_hitl.py",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        print(res.stdout)
        print(res.stderr)
        assert res.returncode == 0, "Container run failed; see output above"

    # Tear down
    subprocess.run(["docker", "compose", "down"], check=True)
