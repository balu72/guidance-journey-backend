import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "mydatabase.db")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

