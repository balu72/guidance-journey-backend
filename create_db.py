import logging
from app import create_app
from app.models import db
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_database():
    """Create the database and tables."""
    logger.info("Creating database and tables...")
    app = create_app()
    with app.app_context():
        db.create_all()
    logger.info("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()
