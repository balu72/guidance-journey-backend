
from flask import Blueprint, jsonify, request
from ..models.session import Session


session_bp = Blueprint('session_routes', __name__)

# Sample data
sessions = [
    Session(1, 1, "2023-10-27").to_dict(),
    Session(2, 2, "2023-10-28").to_dict(),
    Session(3, 1, "2023-10-29").to_dict(),
]

@session_bp.route('/', methods=['GET'])
def get_sessions():
    try:
        return jsonify(sessions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
