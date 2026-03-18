from flask import Flask
from .config import Config
from .routes import bp
from .db import init_db, close_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(bp)

    init_db(app)
    app.teardown_appcontext(close_db)

    return app
