import os
from app.run import load_pages
from db.database import create_database, load_db
from services.rag import RAGService


os.makedirs('logs', exist_ok=True)
log_file_path = os.path.join('logs', 'app_logs.log')
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        pass

create_database()

load_db()

load_pages()

# Initialize the rag service
RAGService()
