import os
os.environ['DB_ADAPTER'] = 'postgres'
from skills.db_adapter import push_hitl
import json

ok = push_hitl({"task": "review", "payload": {"foo": "bar"}})
print(json.dumps({"ok": bool(ok)}))
