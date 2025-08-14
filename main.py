from app.run import load_pages
from db.database import create_database, load_db
from services.rag import RAGService


create_database()

load_db()

load_pages()

# Initialize the rag service
RAGService()
