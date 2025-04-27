import logging
from flask import Blueprint, jsonify, request
from ..models.client import Client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample data (replace with a database in a real application)
clients = [
    {
        "id": "client-uuid-1",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "source": "Website",
        "status": "First Session Scheduled",
        "notes": "Some notes about John",
        "createdAt": "2023-10-26T10:00:00Z",
        "updatedAt": "2023-10-26T12:30:00Z"
    },
    {
        "id": "client-uuid-2",
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "987-654-3210",
        "source": "Referral",
        "status": "Second Session Completed",
        "notes": "Some notes about Jane",
        "createdAt": "2023-10-25T09:00:00Z",
        "updatedAt": "2023-10-25T11:00:00Z"
    },
]

client_bp = Blueprint('client_routes', __name__)
@client_bp.route('/clients', methods=['GET'])
def get_clients():
    logger.info("Request received to get all clients.")
    try:
        # Query the database to get all clients
       # clients = Client.query.all()

        # Convert the client objects to a list of dictionaries for JSON serialization
        #client_list = [client.to_dict() for client in clients]
       # logger.info(f"Successfully retrieved {len(client_list)} clients.")
        #return jsonify(client_list)
        return jsonify(clients), 200    
    except Exception as e:
        logger.error(f"Error retrieving clients: {e}")
        return jsonify({"error": str(e)}), 500


@client_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    logger.info(f"Request received to get client with ID: {client_id}")
    try:
        # Query the database to get a specific client by ID
        # client = Client.query.get(client_id)

        if client_id:
            logger.info(f"Successfully retrieved client with ID: {client_id}")
            #return jsonify(client.to_dict())
            return jsonify(clients[client_id]), 200
        else:
            logger.warning(f"Client with ID {client_id} not found.")
        return jsonify({"error": "Client not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving client with ID {client_id}: {e}")
        return jsonify({"Error": str(e)}), 500