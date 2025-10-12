# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import the components we've built
from .models import ChatMessage
from .bot import chatbot_instance
from .database import save_message

# --- FastAPI Application Setup ---

app = FastAPI(
    title="AI Customer Support Bot API",
    description="An API for interacting with an AI-powered customer support chatbot.",
    version="1.0.0"
)

# Configure CORS (still good practice)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoint ---

@app.post("/chat", tags=["Chat"])
def chat_endpoint(request: ChatMessage):
    """
    This endpoint receives a user message and returns the chatbot's response.
    """
    save_message(
        session_id=request.session_id,
        sender="user",
        message=request.message
    )
    bot_response = chatbot_instance.get_response(
        session_id=request.session_id,
        user_message=request.message
    )
    save_message(
        session_id=request.session_id,
        sender="bot",
        message=bot_response
    )
    return {"response": bot_response}

# --- Serve Frontend ---
# Mount the 'frontend' directory to serve static files like CSS and JS
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", tags=["Frontend"])
async def read_index():
    """Serves the main index.html file."""
    return FileResponse('frontend/index.html')