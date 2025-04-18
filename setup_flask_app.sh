#!/bin/bash

# Set project root directory
PROJECT_NAME="guidance-journey-backend"
cd $PROJECT_NAME

# Create folders
mkdir -p app instance

# Create __init__.py with create_app function
cat > app/__init__.py <<EOL
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    from .routes import main
    app.register_blueprint(main)

    return app
EOL

# Create routes.py with a sample route
cat > app/routes.py <<EOL
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, Flask!"
EOL

# Create empty models.py and utils.py
touch app/models.py
touch app/utils.py

# Create config files
cat > config.py <<EOL
import os

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
EOL

cat > instance/config.py <<EOL
# Local instance-specific config (ignored by Git)
EOL

# Create run.py entry point
cat > run.py <<EOL
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create .gitignore
cat > .gitignore <<EOL
__pycache__/
*.pyc
*.pyo
.env
instance/
venv/
EOL

# Create README
cat > README.md <<EOL
# Flask App

This is a basic Flask application using the application factory pattern.
EOL

# Optional: Set up virtual environment and install Flask
python3 -m venv venv
source venv/bin/activate
pip install flask
pip freeze > requirements.txt

echo "✅ Flask app structure created successfully in '$PROJECT_NAME'."
