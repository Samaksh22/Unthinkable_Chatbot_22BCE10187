# AI Customer Support Bot

This project is an AI-powered customer support chatbot designed to handle frequently asked questions (FAQs) and simulate escalation to a human agent when it cannot find a relevant answer. The application is built with a Python backend using FastAPI and a simple, clean frontend interface.

## Demo Video

[![AI Chatbot Demo Video](https://raw.githubusercontent.com/Samaksh22/chatbot/main/thumbnail.png)](https://drive.google.com/file/d/1bWkkTjC2EQ0dTiBhsSTtd93ezGknnVra/view?usp=sharing)

**Click the thumbnail above or [click here to watch the full demo](https://drive.google.com/file/d/1bWkkTjC2EQ0dTiBhsSTtd93ezGknnVra/view?usp=sharing).**

## Features

* **FAQ Answering:** Uses semantic search to find the most relevant answer from a knowledge base.
* **Contextual Memory:** Retains conversation history for a given session to provide contextual responses.
* **Escalation Simulation:** If a query cannot be answered from the FAQs, the bot simulates an escalation to a human agent.
* **Conversational Handling:** Can handle simple greetings and pleasantries without needing an FAQ entry.
* **Session Management:** Includes options to clear the current chat history or reset the session entirely.

## Tech Stack

* **Backend:** Python, FastAPI
* **Database:** SQLite with SQLAlchemy
* **AI/LLM:** Google Gemini
* **Core Libraries:** LangChain, SentenceTransformers, Pandas
* **Frontend:** HTML, CSS, JavaScript

## Setup and Installation

Follow these steps to set up and run the project locally.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd chatbot
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # For Linux/macOS/WSL
    python3 -m venv venv
    source venv/bin/activate

    # For Windows (Command Prompt)
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    This project uses `pip` for package management.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a file named `.env` in the root directory of the project and add your Google Gemini API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## How to Run

Once the setup is complete, you can start the backend server using Uvicorn.

1.  **Run the Server**
    From the root directory of the project, run the following command:
    ```bash
    uvicorn app.main:app --reload
    ```
    The `--reload` flag will automatically restart the server when you make changes to the code.

2.  **Access the Application**
    Open your web browser and navigate to:
    ```
    [http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```

## API Endpoints

The application exposes the following REST endpoints:

* `POST /chat`: Sends a message to the chatbot and receives a response.
* `GET /history/{session_id}`: Retrieves the conversation history for a specific session.
* `DELETE /history/{session_id}`: Deletes the conversation history for a specific session.

## LLM Prompt

The core logic of the chatbot is guided by the following prompt sent to the LLM.

```
You are a helpful and friendly customer support agent. Your primary goal is to answer questions using the provided FAQ context.

1.  First, analyze the "User Question". If it is a simple greeting or conversational pleasantry (like "hello", "how are you?", "thanks"), respond naturally and kindly.
2.  For all other questions, you MUST use the "FAQ Context" to find the answer. Answer ONLY with the information from the FAQ context. Do not make up information.
3.  If the "FAQ Context" is 'No relevant FAQ found.' AND the question is not a simple greeting, you MUST respond with the exact phrase: '{escalation_phrase}'

---
Conversation History:
{history}

---
FAQ Context:
{context}

---
User Question:
{question}

Answer:
```
