# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import ConversationHistory, create_db_and_tables

# Define the database file. SQLite will create this file in the project root.
DATABASE_URL = "sqlite:///./chat_history.db"

# Create the SQLAlchemy engine. The 'check_same_thread' argument is needed for SQLite.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory. This is what we'll use to interact with the DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database and the 'conversations' table if they don't exist.
create_db_and_tables(engine)


# --- Database Interaction Functions ---

def save_message(session_id: str, sender: str, message: str):
    """Saves a message from the user or bot to the database."""
    db = SessionLocal()
    try:
        db_message = ConversationHistory(
            session_id=session_id,
            sender=sender,
            message=message
        )
        db.add(db_message)
        db.commit()
    finally:
        db.close()


def get_conversation_history(session_id: str, limit: int = 10):
    """Retrieves the last 'limit' messages for a given session_id."""
    db = SessionLocal()
    try:
        history = (
            db.query(ConversationHistory)
            .filter(ConversationHistory.session_id == session_id)
            .order_by(ConversationHistory.timestamp.desc())
            .limit(limit)
            .all()
        )
        # We queried in descending order, so we reverse it to get chronological order.
        return list(reversed(history))
    finally:
        db.close()