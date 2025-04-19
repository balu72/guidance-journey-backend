
from flask import Blueprint, jsonify, request
from ..models.client import Client


client_bp = Blueprint('client_routes', __name__)

# Sample data (replace with a database in a real application)
clients = [
    Client(1, "Client A", "active").to_dict(),
    Client(2, "Client B", "inactive").to_dict(),
    Client(3, "Client C", "active").to_dict(),
    Client(4, "Client D", "inactive").to_dict(),
    Client(5, "Client E", "active").to_dict()
]

@client_bp.route('/', methods=['GET'])
def get_clients():
    try:
        return jsonify(clients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        client = next((c for c in clients if c["id"] == client_id), None)
        if client:
            return jsonify(client)
        return jsonify({"error": "Client not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
