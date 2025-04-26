
from flask import Blueprint, jsonify, request
from ..models.document import Document

document_bp = Blueprint('document_routes', __name__)

# Sample data
documents = [
  {
    "id": "document-uuid-1",
    "clientId": "client-uuid-1",
    "type": "Counselling Objective",
    "content": "Document content...",
    "sent": true,
    "sentDate": "2023-11-15T10:00:00Z",
    "createdAt": "2023-11-10T09:00:00Z",
    "updatedAt": "2023-11-15T10:00:00Z"
  },
  {
    "id": "document-uuid-2",
    "clientId": "client-uuid-2",
    "type": "Session Summary",
    "content": "Document content...",
    "sent": false,
    "sentDate": null,
    "createdAt": "2023-11-12T14:00:00Z",
    "updatedAt": "2023-11-12T14:00:00Z"
  }
]


@document_bp.route('/api/documents', methods=['GET'])
def get_documents():
    try:
        if documents:
            return jsonify(documents), 200
        else:
            return jsonify({"message": "No documents found"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents', methods=['POST'])
def create_document():
    try:
        data = request.get_json()
        
        client_id = data.get('clientId')
        client_type = data.get('counselling_objective')
        content = data.get('new_document_content')
        sent = data.get('sent', False)

        new_document = Document(
            id=f"document-uuid-{len(documents) + 1}",
            clientId=client_id,
            type=client_type,
            content=content,
            sent=sent,
            sentDate=data.get('sentDate'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt')
        )
        documents.append(new_document.to_dict())
        return jsonify(documents), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"message": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
@document_bp.route('/api/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    try:
        data = request.get_json()
        
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            document['clientId'] = data.get('clientId', document['clientId'])
            document['type'] = data.get('type', document['type'])
            document['content'] = data.get('content', document['content'])
            document['sent'] = data.get('sent', document['sent'])
            document['sentDate'] = data.get('sentDate', document['sentDate'])
            document['updatedAt'] = data.get('updatedAt', data.get('updatedAt', document['updatedAt']))
            
            return jsonify(document), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        global documents
        documents = [doc for doc in documents if doc['id'] != document_id]
        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500      
    
@document_bp.route('/api/documents/<document_id>/send', methods=['POST'])
def send_document(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            document['sent'] = True
            document['sentDate'] = "2023-11-15T10:00:00Z"  # Example date
            return jsonify({"message": "Document sent successfully"}), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents/<document_id>/unsend', methods=['POST'])
def unsend_document(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            document['sent'] = False
            document['sentDate'] = None
            return jsonify({"message": "Document unsent successfully"}), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents/<document_id>/download', methods=['GET'])
def download_document(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            # Simulate file download
            return jsonify({"message": "Document downloaded successfully"}), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
    except Exception as e:
        return jsonify({"error": str(e)}), 500      
    
@document_bp.route('/api/documents/<document_id>/preview', methods=['GET'])
def preview_document(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@document_bp.route('/api/documents/<document_id>/send-reminder', methods=['POST'])
def send_reminder(document_id):
    try:
        document = next((doc for doc in documents if doc['id'] == document_id), None)
        if document:
            # Simulate sending a reminder
            return jsonify({"message": "Reminder sent successfully"}), 200
        else:
            return jsonify({"message": "Document not found"}), 404  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
