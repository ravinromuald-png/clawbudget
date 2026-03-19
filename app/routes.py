from flask import Blueprint, render_template
from .db import get_db

bp = Blueprint("main", __name__)

@bp.route("/")
def dashboard():
    db = get_db()

    cost_today = db.execute("""
        SELECT COALESCE(SUM(estimated_cost), 0) AS total_cost
        FROM sessions
    """).fetchone()["total_cost"]

    saved_tokens = db.execute("""
        SELECT COALESCE(SUM(saved_tokens), 0) AS total_saved_tokens
        FROM sessions
    """).fetchone()["total_saved_tokens"]

    session_count = db.execute("""
        SELECT COUNT(*) AS total_sessions
        FROM sessions
    """).fetchone()["total_sessions"]

    alert_count = db.execute("""
        SELECT COUNT(*) AS total_alerts
        FROM alerts
    """).fetchone()["total_alerts"]

    recent_sessions = db.execute("""
        SELECT ts, agent_name, model_name, estimated_cost, status, saved_tokens
        FROM sessions
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    return render_template(
        "dashboard.html",
        cost_today=cost_today,
        saved_tokens=saved_tokens,
        session_count=session_count,
        alert_count=alert_count,
        recent_sessions=recent_sessions
    )

@bp.route("/sessions")
def sessions():
    db = get_db()

    all_sessions = db.execute("""
        SELECT ts, agent_name, model_name, input_tokens, output_tokens,
               saved_tokens, estimated_cost, saved_cost, status
        FROM sessions
        ORDER BY id DESC
    """).fetchall()

    return render_template("sessions.html", sessions=all_sessions)
