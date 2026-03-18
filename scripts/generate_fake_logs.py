import json
from pathlib import Path

logs = [
    {
        "ts": "2026-03-18 18:10",
        "agent_name": "email-agent",
        "model_name": "cheap-model",
        "input_tokens": 14000,
        "output_tokens": 3500,
        "saved_tokens": 6000,
        "estimated_cost": 0.22,
        "saved_cost": 0.09,
        "status": "ok"
    },
    {
        "ts": "2026-03-18 18:12",
        "agent_name": "browser-agent",
        "model_name": "premium-model",
        "input_tokens": 26000,
        "output_tokens": 7000,
        "saved_tokens": 18000,
        "estimated_cost": 0.81,
        "saved_cost": 0.42,
        "status": "cut"
    },
    {
        "ts": "2026-03-18 18:14",
        "agent_name": "calendar-agent",
        "model_name": "cheap-model",
        "input_tokens": 8000,
        "output_tokens": 1800,
        "saved_tokens": 3000,
        "estimated_cost": 0.10,
        "saved_cost": 0.04,
        "status": "ok"
    }
]

output_path = Path("fake_openclaw_logs.jsonl")

with output_path.open("w", encoding="utf-8") as f:
    for row in logs:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"Fake logs written to {output_path}")
