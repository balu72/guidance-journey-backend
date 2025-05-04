#!/bin/bash

echo "Starting Mylo Backend Setup and Server..."

# Create the database
echo "Creating database..."
python create_db.py

# Seed the database
echo "Seeding database with initial data..."
python seed_db.py

# Run the backend server
echo "Starting backend server..."
python wsgi.py
