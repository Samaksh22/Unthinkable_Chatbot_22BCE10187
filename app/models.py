# app/models.py

import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# --- Pydantic Model for API ---
# This defines the structure of the JSON request body for the /chat endpoint.
class ChatMessage(BaseModel):
    session_id: str
    message: str

# --- SQLAlchemy Model for Database ---
# This defines the structure of the 'conversations' table in our database.
Base = declarative_base()

class ConversationHistory(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    sender = Column(String)  # 'user' or 'bot'
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# This is a small utility to create the database file and the table.
# We'll call this from our main application file when it starts.
def create_db_and_tables(engine):
    Base.metadata.create_all(bind=engine)