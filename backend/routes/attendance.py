from flask import Blueprint, request, jsonify
from firebase_admin import auth
from models import db, Attendance, AttendanceSession
from datetime import datetime
import uuid

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/test", methods=["GET"])
def test_attendance():
    return jsonify({"message": "Attendance route working ✅"})

# Helper to verify Firebase ID token
def verify_token(request):
    id_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token["uid"]

# Start attendance session (scan 1)
@attendance_bp.route("/start", methods=["POST"])
def start_attendance():
    try:
        uid = verify_token(request)
        session_id = str(uuid.uuid4())  # unique session id
        new_session = AttendanceSession(session_id=session_id, started_by=uid, start_time=datetime.utcnow())
        db.session.add(new_session)
        db.session.commit()
        return jsonify({"success": True, "session_id": session_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401

# Mark attendance after second scan
@attendance_bp.route("/mark", methods=["POST"])
def mark_attendance():
    try:
        uid = verify_token(request)
        data = request.get_json()
        session_id = data.get("session_id")

        if not session_id:
            return jsonify({"success": False, "error": "Session ID required"}), 400

        existing = Attendance.query.filter_by(student_id=uid, session_id=session_id).first()
        if existing:
            return jsonify({"success": False, "message": "Already marked"}), 409

        attendance = Attendance(student_id=uid, session_id=session_id, timestamp=datetime.utcnow())
        db.session.add(attendance)
        db.session.commit()
        return jsonify({"success": True, "message": "Attendance marked!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401
