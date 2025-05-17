import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from ..models import db
from ..models.client import Client
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client_bp = Blueprint('client_routes', __name__)
CORS(client_bp)

@client_bp.route('/clients', methods=['GET'])
def get_clients():
    logger.info("Request received to get all clients.")
    try:
        # Query the database to get all clients
        clients = Client.query.all()

        # Convert the client objects to a list of dictionaries for JSON serialization
        client_list = [client.to_dict() for client in clients]
        logger.info(f"Successfully retrieved {len(client_list)} clients.")
        return jsonify(client_list), 200
    except Exception as e:
        logger.error(f"Error retrieving clients: {e}")
        return jsonify({"error": str(e)}), 500

@client_bp.route('/clients/<string:client_display_id>', methods=['GET'])
def get_client(client_display_id):
    logger.info(f"Request received to get client with ID: {client_display_id}")
    try:
        # Query the database to get a specific client by display_id
        client = Client.query.filter_by(display_id=client_display_id).first()
        
        if client:
            logger.info(f"Successfully retrieved client with ID: {client_display_id}")
            return jsonify(client.to_dict()), 200
        
        logger.warning(f"Client with ID {client_display_id} not found.")
        return jsonify({"error": "Client not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving client with ID {client_display_id}: {e}")
        return jsonify({"error": str(e)}), 500

@client_bp.route('/clients', methods=['POST'])
def create_client():
    logger.info("Request received to create a new client.")
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email'):
            logger.warning("Missing required fields in client creation request.")
            return jsonify({"error": "Name and email are required fields"}), 400
        
         # Check if client with this email already exists
        existing_client = Client.query.filter_by(email=data.get('email')).first()
        if existing_client:
            logger.warning(f"Client with email {data.get('email')} already exists.")
            return jsonify({"error": "A client with this email already exists"}), 409
        
        # Generate display_id
        max_id_result = db.session.query(db.func.max(Client.id)).first()
        next_id = 1 if max_id_result[0] is None else max_id_result[0] + 1
        display_id = f"CLIENT-{next_id:03d}"
        
        # Create new client with display_id
        new_client = Client(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            source=data.get('source'),
            status=data.get('status', 'Initial Contact'),
            notes=data.get('notes')
        )
        new_client.display_id = display_id
        
        db.session.add(new_client)
        db.session.commit()
        
        logger.info(f"Successfully created new client with ID: {display_id}")
        return jsonify(new_client.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating client: {e}")
        return jsonify({"error": str(e)}), 500

@client_bp.route('/clients/<string:client_display_id>', methods=['PUT'])
def update_client(client_display_id):
    logger.info(f"Request received to update client with ID: {client_display_id}")
    try:
        data = request.get_json()
        client = Client.query.filter_by(display_id=client_display_id).first()
        
        if not client:
            logger.warning(f"Client with ID {client_display_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        # Update client fields
        if 'name' in data:
            client.name = data['name']
        if 'email' in data:
            # Check if email is being changed and if it's already in use
            if data['email'] != client.email:
                existing_client = Client.query.filter_by(email=data['email']).first()
                if existing_client:
                    logger.warning(f"Email {data['email']} is already in use.")
                    return jsonify({"error": "Email is already in use"}), 409
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']
        if 'source' in data:
            client.source = data['source']
        if 'status' in data:
            client.status = data['status']
        if 'notes' in data:
            client.notes = data['notes']
        
        db.session.commit()
        
        logger.info(f"Successfully updated client with ID: {client_display_id}")
        return jsonify(client.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating client with ID {client_display_id}: {e}")
        return jsonify({"error": str(e)}), 500

@client_bp.route('/clients/<string:client_display_id>', methods=['DELETE'])
def delete_client(client_display_id):
    logger.info(f"Request received to delete client with ID: {client_display_id}")
    try:
        client = Client.query.filter_by(display_id=client_display_id).first()
        
        if not client:
            logger.warning(f"Client with ID {client_display_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        db.session.delete(client)
        db.session.commit()
        
        logger.info(f"Successfully deleted client with ID: {client_display_id}")
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting client with ID {client_display_id}: {e}")
        return jsonify({"error": str(e)}), 500

@client_bp.route('/clients/<string:client_display_id>/status', methods=['PUT'])
def update_client_status(client_display_id):
    logger.info(f"Request received to update status for client with ID: {client_display_id}")
    try:
        data = request.get_json()
        
        if 'status' not in data:
            logger.warning("Missing status in request.")
            return jsonify({"error": "Status is required"}), 400
        
        client = Client.query.filter_by(display_id=client_display_id).first()
        
        if not client:
            logger.warning(f"Client with ID {client_display_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        client.status = data['status']
        db.session.commit()
        
        logger.info(f"Successfully updated status for client with ID: {client_display_id}")
        return jsonify(client.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating status for client with ID {client_display_id}: {e}")
        return jsonify({"error": str(e)}), 500
