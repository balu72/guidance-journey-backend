
from . import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    display_id = db.Column(db.String(13), unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    sent_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, client_id, type, content, sent=False, sent_date=None):
        self.client_id = client_id
        self.type = type
        self.content = content
        self.sent = sent
        self.sent_date = sent_date

    def to_dict(self):
        return {
            "id": self.display_id,  # Return display_id as the public ID
            "clientId": self.client.display_id,  # Return client's display_id
            "type": self.type,
            "content": self.content,
            "sent": self.sent,
            "sentDate": self.sent_date.isoformat() if self.sent_date else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
