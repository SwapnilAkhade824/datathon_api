from flask import jsonify

def success(data=None, message="Success"):
    return jsonify({"success": True, "message": message, "data": data}), 200

def error(message="An error occurred", code=400):
    return jsonify({"success": False, "message": message}), code
