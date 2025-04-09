# routes/auth.py

from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth, credentials
import os

auth_bp = Blueprint("auth", __name__)

# Initialize Firebase only once
if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase_admin.json')
    cred_path = os.path.abspath(cred_path)
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return jsonify({"message": "Auth route working ✅"})

@auth_bp.route("/verify", methods=["POST"])
def verify_user():
    try:
        # Extract ID token from Authorization header
        id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not id_token:
            return jsonify({"success": False, "error": "Missing ID token"}), 401

        # Verify token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email", "")
        name = decoded_token.get("name", "")

        return jsonify({
            "success": True,
            "uid": uid,
            "email": email,
            "name": name
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 401
