import json
import sys
from pathlib import Path

sys.path.append(".")

from app import create_app
from app.db import insert_session

log_path = Path("fake_openclaw_logs.jsonl")

if not log_path.exists():
    print("Missing fake_openclaw_logs.jsonl")
    raise SystemExit(1)

app = create_app()

with app.app_context():
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            session = json.loads(line)
            insert_session(session)

print("Logs imported into SQLite.")
