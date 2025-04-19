
from flask import Blueprint, jsonify, request
from ..models.document import Document

document_bp = Blueprint('document_routes', __name__)

# Sample data
documents = [
    Document(1, 1, "Document 1").to_dict(),
    Document(2, 2, "Document 2").to_dict(),
    Document(3, 1, "Document 3").to_dict(),
]

@document_bp.route('/', methods=['GET'])
def get_documents():
    try:
        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
