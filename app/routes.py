from flask import Blueprint, render_template_string

bp = Blueprint("main", __name__)

@bp.route("/")
def dashboard():
    return render_template_string("""
    <h1>ClawBudget</h1>
    <p>Déploiement Render OK</p>
    """)
