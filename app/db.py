import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config.get("DATABASE_PATH", "clawbudget.db"))
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config.get("DATABASE_PATH", "clawbudget.db"))

        db.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            saved_tokens INTEGER DEFAULT 0,
            estimated_cost REAL DEFAULT 0,
            saved_cost REAL DEFAULT 0,
            status TEXT DEFAULT 'ok'
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """)

        session_count = db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        if session_count == 0:
            db.executescript("""
            INSERT INTO sessions (ts, agent_name, model_name, input_tokens, output_tokens, saved_tokens, estimated_cost, saved_cost, status)
            VALUES
            ('2026-03-18 16:00', 'email-agent', 'cheap-model', 12000, 3000, 8000, 0.18, 0.12, 'ok'),
            ('2026-03-18 16:20', 'calendar-agent', 'cheap-model', 9000, 2000, 5000, 0.11, 0.07, 'cut'),
            ('2026-03-18 16:45', 'browser-agent', 'premium-model', 18000, 5000, 15000, 0.64, 0.31, 'ok');

            INSERT INTO alerts (ts, level, message)
            VALUES
            ('2026-03-18 16:22', 'warning', 'Session coupée : budget session dépassé'),
            ('2026-03-18 16:46', 'info', 'Réduction de contexte appliquée');
            """)
        db.commit()
        db.close()
def insert_session(session):
    db = get_db()
    db.execute("""
        INSERT INTO sessions (
            ts, agent_name, model_name,
            input_tokens, output_tokens,
            saved_tokens, estimated_cost,
            saved_cost, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session["ts"],
        session["agent_name"],
        session["model_name"],
        session.get("input_tokens", 0),
        session.get("output_tokens", 0),
        session.get("saved_tokens", 0),
        session.get("estimated_cost", 0),
        session.get("saved_cost", 0),
        session.get("status", "ok")
    ))
    db.commit()
