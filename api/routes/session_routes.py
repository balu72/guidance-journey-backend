from flask import Blueprint, jsonify, request
from ..models.session import Session


session_bp = Blueprint('session_routes', __name__)

# Sample data
sessions = [
  {
    "id": "session-uuid-1",
    "clientId": "client-uuid-1",
    "sessionNumber": 1,
    "date": "2023-11-20T10:00:00Z",
    "completed": False,
    "notes": "Some notes about the session...",
    "zoomLink": "https://zoom.us/j/123456789"
  },
  {
    "id": "session-uuid-2",
    "clientId": "client-uuid-2",
    "sessionNumber": 2,
    "date": "2023-11-20T14:00:00Z",
    "completed": True,
    "notes": "Session completed successfully.",
    "zoomLink": None
  }
]


@session_bp.route('/api/sessions', methods=['GET'])
def get_sessions():
    try:
        if sessions:
            return jsonify(sessions), 200
        else:
            return jsonify({"message": "No sessions found"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@session_bp.route('/api/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        
        client_id = data.get('clientId')
        session_number = data.get('sessionNumber')
        date = data.get('date')
        completed = data.get('completed', False)
        notes = data.get('notes', '')
        zoom_link = data.get('zoomLink', None)

        new_session = Session(
            id=f"session-uuid-{len(sessions) + 1}",
            clientId=client_id,
            sessionNumber=session_number,
            date=date,
            completed=completed,
            notes=notes,
            zoomLink=zoom_link
        )
        
        sessions.append(new_session.__dict__)
        
        return jsonify(new_session.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@session_bp.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        if session:
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@session_bp.route('/api/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    try:
        data = request.get_json()
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            session['clientId'] = data.get('clientId', session['clientId'])
            session['sessionNumber'] = data.get('sessionNumber', session['sessionNumber'])
            session['date'] = data.get('date', session['date'])
            session['completed'] = data.get('completed', session['completed'])
            session['notes'] = data.get('notes', session['notes'])
            session['zoomLink'] = data.get('zoomLink', session['zoomLink'])
            
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@session_bp.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        global sessions
        sessions = [sess for sess in sessions if sess['id'] != session_id]
        
        return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@session_bp.route('/api/sessions/<session_id>/complete', methods=['POST'])
def complete_session(session_id):   
    try:
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            session['completed'] = True
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/zoom', methods=['POST'])
def set_zoom_link(session_id):
    try:
        data = request.get_json()
        zoom_link = data.get('zoomLink')
        
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            session['zoomLink'] = zoom_link
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/notes', methods=['POST'])
def add_notes(session_id):
    try:
        data = request.get_json()
        notes = data.get('notes')
        
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            session['notes'] += f"\n{notes}"
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/notes', methods=['GET'])
def get_notes(session_id):
    try:
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            return jsonify({"notes": session['notes']}), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/zoom', methods=['GET'])
def get_zoom_link(session_id):
    try:
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            return jsonify({"zoomLink": session['zoomLink']}), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/completed', methods=['GET'])
def get_session_status(session_id):
    try:
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            return jsonify({"completed": session['completed']}), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@session_bp.route('/api/sessions/<session_id>/completed', methods=['PUT'])
def update_session_status(session_id):  
    try:
        data = request.get_json()
        completed = data.get('completed')
        
        session = next((sess for sess in sessions if sess['id'] == session_id), None)
        
        if session:
            session['completed'] = completed
            return jsonify(session), 200
        else:
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500