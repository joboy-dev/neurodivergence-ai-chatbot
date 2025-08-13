from app.run import load_pages
from db.database import create_database, load_db


create_database()

load_db()

load_pages()
