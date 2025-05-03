import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from ..models import db
from ..models.session import Session
from ..models.client import Client
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

session_bp = Blueprint('session_routes', __name__)
CORS(session_bp)

@session_bp.route('/sessions', methods=['GET'])
def get_sessions():
    logger.info("Request received to get all sessions.")
    try:
        sessions = Session.query.all()
        session_list = [session.to_dict() for session in sessions]
        
        if session_list:
            logger.info(f"Successfully retrieved {len(session_list)} sessions.")
            return jsonify(session_list), 200
        else:
            logger.info("No sessions found.")
            return jsonify([]), 200
    except Exception as e:
        logger.error(f"Error retrieving sessions: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>', methods=['GET'])
def get_session(session_id):
    logger.info(f"Request received to get session with ID: {session_id}")
    try:
        session = Session.query.get(session_id)
        
        if session:
            logger.info(f"Successfully retrieved session with ID: {session_id}")
            return jsonify(session.to_dict()), 200
        
        logger.warning(f"Session with ID {session_id} not found.")
        return jsonify({"error": "Session not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving session with ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/clients/<uuid:client_id>/sessions', methods=['GET'])
def get_client_sessions(client_id):
    logger.info(f"Request received to get sessions for client with ID: {client_id}")
    try:
        # Check if client exists
        client = Client.query.get(client_id)
        if not client:
            logger.warning(f"Client with ID {client_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        sessions = Session.query.filter_by(client_id=client_id).all()
        session_list = [session.to_dict() for session in sessions]
        
        logger.info(f"Successfully retrieved {len(session_list)} sessions for client with ID: {client_id}")
        return jsonify(session_list), 200
    except Exception as e:
        logger.error(f"Error retrieving sessions for client with ID {client_id}: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    logger.info("Request received to create a new session.")
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('clientId') or not data.get('sessionNumber') or not data.get('date'):
            logger.warning("Missing required fields in session creation request.")
            return jsonify({"error": "Client ID, session number, and date are required fields"}), 400
        
        # Check if client exists
        client_id = uuid.UUID(data.get('clientId')) if isinstance(data.get('clientId'), str) else data.get('clientId')
        client = Client.query.get(client_id)
        if not client:
            logger.warning(f"Client with ID {client_id} not found.")
            return jsonify({"error": "Client not found"}), 404
        
        # Parse date
        try:
            date = datetime.fromisoformat(data.get('date').replace('Z', '+00:00'))
        except ValueError:
            logger.warning(f"Invalid date format: {data.get('date')}")
            return jsonify({"error": "Invalid date format. Use ISO format (e.g., 2023-01-01T12:00:00Z)"}), 400
        
        # Create new session
        new_session = Session(
            client_id=client_id,
            session_number=data.get('sessionNumber'),
            date=date,
            completed=data.get('completed', False),
            notes=data.get('notes'),
            zoom_link=data.get('zoomLink')
        )
        
        db.session.add(new_session)
        db.session.commit()
        
        logger.info(f"Successfully created new session with ID: {new_session.id}")
        return jsonify(new_session.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating session: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>', methods=['PUT'])
def update_session(session_id):
    logger.info(f"Request received to update session with ID: {session_id}")
    try:
        data = request.get_json()
        session = Session.query.get(session_id)
        
        if not session:
            logger.warning(f"Session with ID {session_id} not found.")
            return jsonify({"error": "Session not found"}), 404
        
        # Update session fields
        if 'clientId' in data:
            client_id = uuid.UUID(data['clientId']) if isinstance(data['clientId'], str) else data['clientId']
            client = Client.query.get(client_id)
            if not client:
                logger.warning(f"Client with ID {client_id} not found.")
                return jsonify({"error": "Client not found"}), 404
            session.client_id = client_id
            
        if 'sessionNumber' in data:
            session.session_number = data['sessionNumber']
            
        if 'date' in data:
            try:
                session.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except ValueError:
                logger.warning(f"Invalid date format: {data['date']}")
                return jsonify({"error": "Invalid date format. Use ISO format (e.g., 2023-01-01T12:00:00Z)"}), 400
                
        if 'completed' in data:
            session.completed = data['completed']
            
        if 'notes' in data:
            session.notes = data['notes']
            
        if 'zoomLink' in data:
            session.zoom_link = data['zoomLink']
        
        db.session.commit()
        
        logger.info(f"Successfully updated session with ID: {session_id}")
        return jsonify(session.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating session with ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>', methods=['DELETE'])
def delete_session(session_id):
    logger.info(f"Request received to delete session with ID: {session_id}")
    try:
        session = Session.query.get(session_id)
        
        if not session:
            logger.warning(f"Session with ID {session_id} not found.")
            return jsonify({"error": "Session not found"}), 404
        
        db.session.delete(session)
        db.session.commit()
        
        logger.info(f"Successfully deleted session with ID: {session_id}")
        return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting session with ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>/complete', methods=['POST'])
def complete_session(session_id):
    logger.info(f"Request received to mark session with ID {session_id} as completed.")
    try:
        session = Session.query.get(session_id)
        
        if not session:
            logger.warning(f"Session with ID {session_id} not found.")
            return jsonify({"error": "Session not found"}), 404
        
        session.completed = True
        db.session.commit()
        
        logger.info(f"Successfully marked session with ID {session_id} as completed.")
        return jsonify(session.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking session with ID {session_id} as completed: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>/zoom', methods=['POST'])
def set_zoom_link(session_id):
    logger.info(f"Request received to set zoom link for session with ID: {session_id}")
    try:
        data = request.get_json()
        
        if 'zoomLink' not in data:
            logger.warning("Missing zoom link in request.")
            return jsonify({"error": "Zoom link is required"}), 400
        
        session = Session.query.get(session_id)
        
        if not session:
            logger.warning(f"Session with ID {session_id} not found.")
            return jsonify({"error": "Session not found"}), 404
        
        session.zoom_link = data['zoomLink']
        db.session.commit()
        
        logger.info(f"Successfully set zoom link for session with ID: {session_id}")
        return jsonify(session.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error setting zoom link for session with ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<uuid:session_id>/notes', methods=['POST'])
def add_notes(session_id):
    logger.info(f"Request received to add notes to session with ID: {session_id}")
    try:
        data = request.get_json()
        
        if 'notes' not in data:
            logger.warning("Missing notes in request.")
            return jsonify({"error": "Notes are required"}), 400
        
        session = Session.query.get(session_id)
        
        if not session:
            logger.warning(f"Session with ID {session_id} not found.")
            return jsonify({"error": "Session not found"}), 404
        
        # Append new notes to existing notes
        if session.notes:
            session.notes += f"\n{data['notes']}"
        else:
            session.notes = data['notes']
            
        db.session.commit()
        
        logger.info(f"Successfully added notes to session with ID: {session_id}")
        return jsonify(session.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding notes to session with ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 500
