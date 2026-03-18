import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clawbudget-dev-key")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "clawbudget.db")
