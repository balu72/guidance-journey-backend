
from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clients.id'), nullable=False)
    session_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), default='Initial Consultation')
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    zoom_link = db.Column(db.String(255))

    def __init__(self, client_id, session_number, date, category='Initial Consultation', completed=False, notes=None, zoom_link=None):
        self.client_id = client_id
        self.session_number = session_number
        self.date = date
        self.category = category
        self.completed = completed
        self.notes = notes
        self.zoom_link = zoom_link

    def to_dict(self):
        return {
            "id": str(self.id),
            "clientId": str(self.client_id),
            "sessionNumber": self.session_number,
            "date": self.date.isoformat() if self.date else None,
            "category": self.category,
            "completed": self.completed,
            "notes": self.notes,
            "zoomLink": self.zoom_link
        }
