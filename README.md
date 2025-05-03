# Mylo Backend

This is the backend API for the Mylo application, a counseling client management system.

## Features

- RESTful API for managing clients, sessions, and documents
- PostgreSQL database integration
- Comprehensive error handling
- Logging

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mylo-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Create a database named `mylo`
   - Update the database connection string in `config.py` if needed

5. Create the database tables:
   ```bash
   python create_db.py
   ```

6. Seed the database with initial data:
   ```bash
   python seed_db.py
   ```

## Running the Application

Start the development server:
```bash
python wsgi.py
```

The API will be available at `http://127.0.0.1:5000/api`.

## API Endpoints

### Clients

- `GET /api/clients` - Get all clients
- `GET /api/clients/{id}` - Get a specific client
- `POST /api/clients` - Create a new client
- `PUT /api/clients/{id}` - Update a client
- `DELETE /api/clients/{id}` - Delete a client
- `PUT /api/clients/{id}/status` - Update a client's status

### Sessions

- `GET /api/sessions` - Get all sessions
- `GET /api/sessions/{id}` - Get a specific session
- `GET /api/clients/{id}/sessions` - Get all sessions for a specific client
- `POST /api/sessions` - Create a new session
- `PUT /api/sessions/{id}` - Update a session
- `DELETE /api/sessions/{id}` - Delete a session
- `POST /api/sessions/{id}/complete` - Mark a session as completed
- `POST /api/sessions/{id}/zoom` - Set a zoom link for a session
- `POST /api/sessions/{id}/notes` - Add notes to a session

### Documents

- `GET /api/documents` - Get all documents
- `GET /api/documents/{id}` - Get a specific document
- `GET /api/clients/{id}/documents` - Get all documents for a specific client
- `POST /api/documents` - Create a new document
- `PUT /api/documents/{id}` - Update a document
- `DELETE /api/documents/{id}` - Delete a document
- `POST /api/documents/{id}/send` - Mark a document as sent
- `POST /api/documents/{id}/unsend` - Mark a document as unsent
- `GET /api/documents/{id}/download` - Download a document

## Project Structure

- `app/` - Main application package
  - `api/` - API routes
  - `models/` - Database models
  - `utils/` - Utility functions
- `config.py` - Application configuration
- `wsgi.py` - WSGI entry point
- `create_db.py` - Script to create database tables
- `seed_db.py` - Script to seed the database with initial data
