from flask import Blueprint, request, jsonify
from models import db, QuizQuestion, QuizResponse
from firebase_admin import auth

quiz_bp = Blueprint("quiz", __name__)

# Utility to verify Firebase token
def get_user_from_token(request):
    try:
        id_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None

# Route: Teacher creates quiz questions
@quiz_bp.route("/create", methods=["POST"])
def create_quiz():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json
    question = QuizQuestion(
        question=data.get("question"),
        options=data.get("options"),  # Should be a list
        correct_answer=data.get("correct_answer"),
        created_by=user.get("uid")
    )
    db.session.add(question)
    db.session.commit()

    return jsonify({"success": True, "message": "Quiz created"}), 201

# Route: Student fetches quiz questions
@quiz_bp.route("/questions", methods=["GET"])
def get_quiz_questions():
    questions = QuizQuestion.query.all()
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "question": q.question,
            "options": q.options  # Already stored as list
        })
    return jsonify(result), 200

# Route: Student submits quiz response
@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json
    for item in data.get("responses", []):
        response = QuizResponse(
            user_id=user.get("uid"),
            question_id=item.get("question_id"),
            selected_option=item.get("selected_option")
        )
        db.session.add(response)

    db.session.commit()
    return jsonify({"success": True, "message": "Responses submitted"}), 200

# Route: Teacher views responses (optional)
@quiz_bp.route("/responses", methods=["GET"])
def view_responses():
    all_responses = QuizResponse.query.all()
    result = []
    for r in all_responses:
        result.append({
            "user_id": r.user_id,
            "question_id": r.question_id,
            "selected_option": r.selected_option
        })
    return jsonify(result), 200
