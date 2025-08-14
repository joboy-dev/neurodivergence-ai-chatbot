import os
from app.run import load_pages
from db.database import create_database, load_db
from services.rag import RAGService


os.makedirs('logs', exist_ok=True)
create_database()

load_db()

load_pages()

# Initialize the rag service
RAGService()
