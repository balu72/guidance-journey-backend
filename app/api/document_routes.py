
import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from ..models import db
from ..models.document import Document
from ..models.client import Client
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

document_bp = Blueprint('document_routes', __name__)
CORS(document_bp)

@document_bp.route('/documents', methods=['GET'])
def get_documents():
    logger.info("Request received to get all documents.")
    try:
        documents = Document.query.all()
        document_list = [document.to_dict() for document in documents]
        
        if document_list:
            logger.info(f"Successfully retrieved {len(document_list)} documents.")
            return jsonify(document_list), 200
        else:
            logger.info("No documents found.")
            return jsonify([]), 200
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>', methods=['GET'])
def get_document(document_id):
    logger.info(f"Request received to get document with ID: {document_id}")
    try:
        document = Document.query.get(document_id)
        
        if document:
            logger.info(f"Successfully retrieved document with ID: {document_id}")
            return jsonify(document.to_dict()), 200
        
        logger.warning(f"Document with ID {document_id} not found.")
        return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving document with ID {document_id}: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/clients/<uuid:client_id>/documents', methods=['GET'])
def get_client_documents(client_id):
    logger.info(f"Request received to get documents for client with ID: {client_id}")
    try:
        # Check if client exists
        client = Client.query.get(client_id)
        if not client:
            logger.warning(f"Client with ID {client_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        documents = Document.query.filter_by(client_id=client_id).all()
        document_list = [document.to_dict() for document in documents]
        
        logger.info(f"Successfully retrieved {len(document_list)} documents for client with ID: {client_id}")
        return jsonify(document_list), 200
    except Exception as e:
        logger.error(f"Error retrieving documents for client with ID {client_id}: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents', methods=['POST'])
def create_document():
    logger.info("Request received to create a new document.")
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('clientId') or not data.get('type') or not data.get('content'):
            logger.warning("Missing required fields in document creation request.")
            return jsonify({"error": "Client ID, type, and content are required fields"}), 400
        
        # Check if client exists
        client_id = uuid.UUID(data.get('clientId')) if isinstance(data.get('clientId'), str) else data.get('clientId')
        client = Client.query.get(client_id)
        if not client:
            logger.warning(f"Client with ID {client_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        # Create new document
        new_document = Document(
            client_id=client_id,
            type=data.get('type'),
            content=data.get('content'),
            sent=data.get('sent', False),
            sent_date=datetime.fromisoformat(data.get('sentDate').replace('Z', '+00:00')) if data.get('sentDate') else None
        )
        
        db.session.add(new_document)
        db.session.commit()
        
        logger.info(f"Successfully created new document with ID: {new_document.id}")
        return jsonify(new_document.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating document: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>', methods=['PUT'])
def update_document(document_id):
    logger.info(f"Request received to update document with ID: {document_id}")
    try:
        data = request.get_json()
        document = Document.query.get(document_id)
        
        if not document:
            logger.warning(f"Document with ID {document_id} not found.")
            return jsonify({"error": "Document not found"}), 404
        
        # Update document fields
        if 'clientId' in data:
            client_id = uuid.UUID(data['clientId']) if isinstance(data['clientId'], str) else data['clientId']
            client = Client.query.get(client_id)
            if not client:
                logger.warning(f"Client with ID {client_id} not found.")
                return jsonify({"error": "Client not found"}), 404
            document.client_id = client_id
            
        if 'type' in data:
            document.type = data['type']
            
        if 'content' in data:
            document.content = data['content']
            
        if 'sent' in data:
            document.sent = data['sent']
            
        if 'sentDate' in data:
            if data['sentDate']:
                try:
                    document.sent_date = datetime.fromisoformat(data['sentDate'].replace('Z', '+00:00'))
                except ValueError:
                    logger.warning(f"Invalid date format: {data['sentDate']}")
                    return jsonify({"error": "Invalid date format. Use ISO format (e.g., 2023-01-01T12:00:00Z)"}), 400
            else:
                document.sent_date = None
        
        db.session.commit()
        
        logger.info(f"Successfully updated document with ID: {document_id}")
        return jsonify(document.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating document with ID {document_id}: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>', methods=['DELETE'])
def delete_document(document_id):
    logger.info(f"Request received to delete document with ID: {document_id}")
    try:
        document = Document.query.get(document_id)
        
        if not document:
            logger.warning(f"Document with ID {document_id} not found.")
            return jsonify({"error": "Document not found"}), 404
        
        db.session.delete(document)
        db.session.commit()
        
        logger.info(f"Successfully deleted document with ID: {document_id}")
        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting document with ID {document_id}: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>/send', methods=['POST'])
def send_document(document_id):
    logger.info(f"Request received to mark document with ID {document_id} as sent.")
    try:
        document = Document.query.get(document_id)
        
        if not document:
            logger.warning(f"Document with ID {document_id} not found.")
            return jsonify({"error": "Document not found"}), 404
        
        document.sent = True
        document.sent_date = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Successfully marked document with ID {document_id} as sent.")
        return jsonify(document.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking document with ID {document_id} as sent: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>/unsend', methods=['POST'])
def unsend_document(document_id):
    logger.info(f"Request received to mark document with ID {document_id} as unsent.")
    try:
        document = Document.query.get(document_id)
        
        if not document:
            logger.warning(f"Document with ID {document_id} not found.")
            return jsonify({"error": "Document not found"}), 404
        
        document.sent = False
        document.sent_date = None
        db.session.commit()
        
        logger.info(f"Successfully marked document with ID {document_id} as unsent.")
        return jsonify(document.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking document with ID {document_id} as unsent: {e}")
        return jsonify({"error": str(e)}), 500

@document_bp.route('/documents/<uuid:document_id>/download', methods=['GET'])
def download_document(document_id):
    logger.info(f"Request received to download document with ID: {document_id}")
    try:
        document = Document.query.get(document_id)
        
        if not document:
            logger.warning(f"Document with ID {document_id} not found.")
            return jsonify({"error": "Document not found"}), 404
        
        # In a real application, you would generate a file and return it
        # For now, we'll just return the document content
        return jsonify({
            "content": document.content,
            "filename": f"{document.type.replace(' ', '_').lower()}_{document.id}.txt"
        }), 200
    except Exception as e:
        logger.error(f"Error downloading document with ID {document_id}: {e}")
        return jsonify({"error": str(e)}), 500
