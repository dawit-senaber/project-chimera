import os
import subprocess
import time
import pytest

# Skip this integration test if psycopg2 is not available in the environment.
psycopg2 = pytest.importorskip("psycopg2")

# Respect runtime DB settings; default to the composed DB name used in CI
DB_NAME = os.environ.get("POSTGRES_DB", "chimera")
DB_USER = os.environ.get("POSTGRES_USER", "chimera")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "chimera")


def wait_for_postgres(timeout=90):
    start = time.time()
    hosts = ("127.0.0.1", "localhost", "postgres")
    last_exc = None
    while time.time() - start < timeout:
        for host in hosts:
            try:
                conn = psycopg2.connect(
                    f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={host}"
                )
                conn.close()
                return True
            except Exception as e:
                last_exc = e
        time.sleep(1)
    if last_exc is not None:
        print(f"wait_for_postgres: last exception: {last_exc}")
    return False


def _docker_available():
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        return True
    except (FileNotFoundError, OSError):
        return False


def test_push_hitl_integration(tmp_path):
    """Integration test: ensure `push_hitl` writes a row.

    This test no longer insists on starting docker from inside the test runner.
    In containerized CI the services are brought up by the outer `docker compose`,
    so attempting to run `docker` inside the test will fail (no docker CLI).
    We skip the nested docker start and rely on the existing compose environment.
    """
    # If the docker CLI is available, start postgres locally; otherwise assume the
    # surrounding environment (outer compose) already started it.
    docker_here = _docker_available()
    if docker_here:
        subprocess.run(["docker", "compose", "up", "-d", "postgres"], check=True)

    try:
        # Try to connect directly to Postgres (service hostname 'postgres' is included)
        if wait_for_postgres():
            os.environ["DB_ADAPTER"] = "postgres"
            from skills.db_adapter import push_hitl

            ok = push_hitl({"task": "review", "payload": {"foo": "bar"}})
            assert ok
        else:
            # If direct connect failed, and docker is available, fall back to running
            # the helper inside the agent container. If docker is not available,
            # fail with helpful debugging output.
            if docker_here:
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
            else:
                pytest.fail(
                    "Postgres unreachable and docker CLI is not available inside test runner"
                )
    finally:
        # Tear down only if we started docker here
        if docker_here:
            try:
                subprocess.run(["docker", "compose", "down"], check=True)
            except Exception:
                pass
