from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

# Load environment variables from .env file
load_dotenv()

class Config:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    POOL_SIZE = 5
    MAX_OVERFLOW = 10
    POOL_TIMEOUT = 30

app = Flask(__name__)

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=Config.POOL_SIZE,
    max_overflow=Config.MAX_OVERFLOW,
    pool_timeout=Config.POOL_TIMEOUT
)

@app.route('/')
def home():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
        return jsonify({"status": "OK", "db_version": version})
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host='0.0.0.0', port=5000, debug=debug)