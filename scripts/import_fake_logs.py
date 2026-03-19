import json
import sys
from pathlib import Path

sys.path.append(".")

from app import create_app
from app.db import get_db, insert_session

log_path = Path("fake_openclaw_logs.jsonl")

if not log_path.exists():
    print("Missing fake_openclaw_logs.jsonl")
    raise SystemExit(1)

app = create_app()

with app.app_context():
    db = get_db()

    existing_keys = set()
    rows = db.execute("""
        SELECT ts, agent_name, model_name, input_tokens, output_tokens
        FROM sessions
    """).fetchall()

    for row in rows:
        existing_keys.add((
            row["ts"],
            row["agent_name"],
            row["model_name"],
            row["input_tokens"],
            row["output_tokens"],
        ))

    imported = 0
    skipped = 0

    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            session = json.loads(line)
            key = (
                session["ts"],
                session["agent_name"],
                session["model_name"],
                session.get("input_tokens", 0),
                session.get("output_tokens", 0),
            )

            if key in existing_keys:
                skipped += 1
                continue

            insert_session(session)
            existing_keys.add(key)
            imported += 1

print(f"Imported: {imported}")
print(f"Skipped duplicates: {skipped}")
