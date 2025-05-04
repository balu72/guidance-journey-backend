import logging
from datetime import datetime, timedelta
from app import create_app
from app.models import db
from app.models.client import Client
from app.models.session import Session
from app.models.document import Document
import uuid
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def seed_database():
    """Seed the database with initial data."""
    logger.info("Seeding database with initial data...")
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.session.query(Document).delete()
        db.session.query(Session).delete()
        db.session.query(Client).delete()
        db.session.commit()
        
        # Create clients
        clients = [
            Client(
                name="Alex Johnson",
                email="alex.johnson@example.com",
                phone="+1234567890",
                source="LinkedIn",
                status="Second Session Completed",
                notes="Looking to transition from marketing to product management"
            ),
            Client(
                name="Jamie Smith",
                email="jamie.smith@example.com",
                phone="+1987654321",
                source="Website",
                status="First Session Scheduled",
                notes="Recent graduate looking for career guidance in tech industry"
            ),
            Client(
                name="Taylor Davis",
                email="taylor.davis@example.com",
                phone="+1122334455",
                source="References",
                status="Info Shared",
                notes="Considering a career change after 10 years in finance"
            ),
            Client(
                name="Morgan Lee",
                email="morgan.lee@example.com",
                phone="+1599887766",
                source="Phone",
                status="Decision Pending",
                notes="Interested in exploring leadership development options"
            ),
            Client(
                name="Casey Wilson",
                email="casey.wilson@example.com",
                phone="+1443322110",
                source="LinkedIn",
                status="Follow-up Scheduled",
                notes="Looking for support with interview preparation"
            )
        ]
        
        for client in clients:
            db.session.add(client)
        
        db.session.commit()
        logger.info(f"Added {len(clients)} clients.")
        
        # Create sessions
        sessions = []
        
        # For each client, create appropriate sessions based on status
        for client in clients:
            if client.status in ["First Session Completed", "Second Session Scheduled", "Second Session Completed", "Follow-up Scheduled", "Process Completed"]:
                sessions.append(
                    Session(
                        client_id=client.id,
                        session_number=1,
                        date=datetime.utcnow() - timedelta(days=15),
                        completed=True,
                        notes="Discussed career goals and aspirations. Used Life Design Counselling framework.",
                        zoom_link=f"https://zoom.us/j/{uuid.uuid4().hex[:8]}"
                    )
                )
            
            if client.status in ["First Session Scheduled"]:
                sessions.append(
                    Session(
                        client_id=client.id,
                        session_number=1,
                        date=datetime.utcnow() + timedelta(days=5),
                        completed=False,
                        zoom_link=f"https://zoom.us/j/{uuid.uuid4().hex[:8]}"
                    )
                )
            
            if client.status in ["Second Session Completed", "Follow-up Scheduled", "Process Completed"]:
                sessions.append(
                    Session(
                        client_id=client.id,
                        session_number=2,
                        date=datetime.utcnow() - timedelta(days=5),
                        completed=True,
                        notes="Developed actionable goals based on LDC process framework.",
                        zoom_link=f"https://zoom.us/j/{uuid.uuid4().hex[:8]}"
                    )
                )
            
            if client.status in ["Second Session Scheduled"]:
                sessions.append(
                    Session(
                        client_id=client.id,
                        session_number=2,
                        date=datetime.utcnow() + timedelta(days=10),
                        completed=False,
                        zoom_link=f"https://zoom.us/j/{uuid.uuid4().hex[:8]}"
                    )
                )
            
            if client.status in ["Follow-up Scheduled"]:
                sessions.append(
                    Session(
                        client_id=client.id,
                        session_number=3,
                        date=datetime.utcnow() + timedelta(days=25),
                        completed=False,
                        notes="Follow-up session to review progress on goals.",
                        zoom_link=f"https://zoom.us/j/{uuid.uuid4().hex[:8]}"
                    )
                )
        
        for session in sessions:
            db.session.add(session)
        
        db.session.commit()
        logger.info(f"Added {len(sessions)} sessions.")
        
        # Create documents
        documents = []
        
        # For each client, create appropriate documents based on status
        for client in clients:
            if client.status in ["Info Shared", "Decision Pending", "First Session Scheduled", "First Session Completed", 
                                "Second Session Scheduled", "Second Session Completed", "Follow-up Scheduled", "Process Completed"]:
                documents.append(
                    Document(
                        client_id=client.id,
                        type="Counselling Objective",
                        content="Initial counselling objectives focusing on career transition and skill development.",
                        sent=True,
                        sent_date=datetime.utcnow() - timedelta(days=20)
                    )
                )
            
            if client.status in ["Second Session Completed", "Follow-up Scheduled", "Process Completed"]:
                documents.append(
                    Document(
                        client_id=client.id,
                        type="Session Summary",
                        content="Summary of sessions including key insights and action items discussed.",
                        sent=True,
                        sent_date=datetime.utcnow() - timedelta(days=3)
                    )
                )
                
                documents.append(
                    Document(
                        client_id=client.id,
                        type="Assessment Details",
                        content="Detailed assessment of strengths, areas for growth, and recommended actions.",
                        sent=True,
                        sent_date=datetime.utcnow() - timedelta(days=3)
                    )
                )
        
        for document in documents:
            db.session.add(document)
        
        db.session.commit()
        logger.info(f"Added {len(documents)} documents.")
        
        logger.info("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()
