# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the components we've built
from .models import ChatMessage
from .bot import chatbot_instance
from .database import save_message

# --- FastAPI Application Setup ---

# Create the FastAPI app instance
app = FastAPI(
    title="AI Customer Support Bot API",
    description="An API for interacting with an AI-powered customer support chatbot.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is necessary to allow our frontend (on a different "origin")
# to communicate with this backend API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity. For production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# --- API Endpoints ---

@app.get("/", tags=["Status"])
def read_root():
    """A simple root endpoint to check if the API is running."""
    return {"status": "API is running"}


@app.post("/chat", tags=["Chat"])
def chat_endpoint(request: ChatMessage):
    """
    This endpoint receives a user message and returns the chatbot's response.
    It handles the full conversation turn.
    """
    # 1. Save the user's message to the database.
    save_message(
        session_id=request.session_id,
        sender="user",
        message=request.message
    )

    # 2. Get the bot's response using the logic from bot.py.
    bot_response = chatbot_instance.get_response(
        session_id=request.session_id,
        user_message=request.message
    )

    # 3. Save the bot's response to the database.
    save_message(
        session_id=request.session_id,
        sender="bot",
        message=bot_response
    )

    # 4. Return the response to the client.
    return {"response": bot_response}