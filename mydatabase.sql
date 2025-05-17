PRAGMA foreign_keys = ON;

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    source TEXT,
    status TEXT NOT NULL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_id TEXT UNIQUE NOT NULL,
    client_id INTEGER NOT NULL,
    session_number INTEGER NOT NULL,
    date DATETIME NOT NULL,
    category TEXT DEFAULT 'Initial Consultation',
    completed BOOLEAN DEFAULT 0,
    notes TEXT,
    zoom_link TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_id TEXT UNIQUE NOT NULL,
    client_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    sent BOOLEAN DEFAULT 0,
    sent_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Triggers to generate display_id values
CREATE TRIGGER generate_client_display_id AFTER INSERT ON clients
BEGIN
    UPDATE clients 
    SET display_id = 'CLIENT-' || substr('000' || new.id, -3, 3)
    WHERE id = new.id;
END;

CREATE TRIGGER generate_session_display_id AFTER INSERT ON sessions
BEGIN
    UPDATE sessions 
    SET display_id = 'SESSION-' || substr('000' || new.id, -3, 3)
    WHERE id = new.id;
END;

CREATE TRIGGER generate_document_display_id AFTER INSERT ON documents
BEGIN
    UPDATE documents 
    SET display_id = 'DOCUMENT-' || substr('000' || new.id, -3, 3)
    WHERE id = new.id;
END;
