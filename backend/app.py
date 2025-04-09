# backend/app.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load env variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup DB
from models import db  # ✅ Use the single shared db instance
from config import Config
app.config.from_object(Config)

db.init_app(app)  # ✅ Only initialize once

# Register blueprints
from routes.auth import auth_bp
from routes.attendance import attendance_bp
from routes.quiz import quiz_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')

@app.route("/")
def home():
    return "🎉 Flask is running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
