from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String, primary_key=True)  # Firebase UID or custom
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    attendances = db.relationship('Attendance', backref='student', lazy=True)
    responses = db.relationship('QuizResponse', backref='student', lazy=True)

class AttendanceSession(db.Model):
    __tablename__ = 'attendance_sessions'

    id = db.Column(db.String, primary_key=True)
    teacher_id = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)

    attendances = db.relationship('Attendance', backref='session', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey("students.id"), nullable=False)
    session_id = db.Column(db.String, db.ForeignKey("attendance_sessions.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending / present / absent
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, nullable=False)
    options = db.Column(db.PickleType)  # list of strings
    answer = db.Column(db.String)

    responses = db.relationship('QuizResponse', backref='question', lazy=True)

class QuizResponse(db.Model):
    __tablename__ = 'quiz_responses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey("students.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False)
    answer = db.Column(db.String)
