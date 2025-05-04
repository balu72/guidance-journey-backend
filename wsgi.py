import logging
import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()

# Explicitly set environment variables
os.environ["DB_HOST"] = "localhost"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "postgres"
os.environ["DB_NAME"] = "mylo"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
