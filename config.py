import os

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

# Database configuration

db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "postgres")
db_host = os.environ.get("DB_HOST", "localhost")
db_name = os.environ.get("DB_NAME", "mylo")
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
