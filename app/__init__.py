import logging
from flask import Flask
from flask_cors import CORS
from app.models import db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app(config_object="config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.api.client_routes import client_bp
    from app.api.session_routes import session_bp
    from app.api.document_routes import document_bp
    
    app.register_blueprint(client_bp, url_prefix='/api')
    app.register_blueprint(session_bp, url_prefix='/api')
    app.register_blueprint(document_bp, url_prefix='/api')
    
    logger.info("App created and blueprints registered.")
    
    return app
