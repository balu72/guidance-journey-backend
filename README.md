# Mylo Backend

This is the backend server for the Mylo Career Counsel application. It provides API endpoints for managing clients, sessions, and documents.

## Setup

1. Make sure you have PostgreSQL installed and running on your system.
2. Create a database named "mylo" in PostgreSQL.
3. Update the database credentials in the `.env` file if needed:
   ```
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_NAME=mylo
   ```

## Running the Backend

You can run the backend server using the provided script:

```bash
./run_backend.sh
```

This script will:
1. Create the database tables
2. Seed the database with initial data
3. Start the backend server at http://127.0.0.1:5000

Alternatively, you can run each step manually:

```bash
# Create the database
python create_db.py

# Seed the database
python seed_db.py

# Run the backend server
python wsgi.py
```

## API Endpoints

The backend provides the following API endpoints:

### Clients
- `GET /api/clients` - Get all clients
- `GET /api/clients/<client_id>` - Get a specific client
- `POST /api/clients` - Create a new client
- `PUT /api/clients/<client_id>` - Update a client
- `DELETE /api/clients/<client_id>` - Delete a client
- `PUT /api/clients/<client_id>/status` - Update a client's status

### Sessions
- `GET /api/sessions` - Get all sessions
- `GET /api/sessions/<session_id>` - Get a specific session
- `GET /api/clients/<client_id>/sessions` - Get sessions for a specific client
- `POST /api/sessions` - Create a new session
- `PUT /api/sessions/<session_id>` - Update a session
- `DELETE /api/sessions/<session_id>` - Delete a session
- `POST /api/sessions/<session_id>/complete` - Mark a session as completed
- `POST /api/sessions/<session_id>/zoom` - Set a zoom link for a session
- `POST /api/sessions/<session_id>/notes` - Add notes to a session

### Documents
- `GET /api/documents` - Get all documents
- `GET /api/documents/<document_id>` - Get a specific document
- `GET /api/clients/<client_id>/documents` - Get documents for a specific client
- `POST /api/documents` - Create a new document
- `PUT /api/documents/<document_id>` - Update a document
- `DELETE /api/documents/<document_id>` - Delete a document
- `POST /api/documents/<document_id>/send` - Mark a document as sent
