
from flask import Flask
from api.routes.client_routes import client_bp
from api.routes.session_routes import session_bp
from api.routes.document_routes import document_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(client_bp, url_prefix='/clients')
app.register_blueprint(session_bp, url_prefix='/sessions')
app.register_blueprint(document_bp, url_prefix='/documents')

if __name__ == '__main__':
    app.run(debug=True)
