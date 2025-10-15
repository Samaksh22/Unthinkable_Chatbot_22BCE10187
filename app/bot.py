# app/bot.py

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer, util

# Import the database functions we created
from . import database

# --- Environment and Model Setup ---

# Load environment variables from the .env file
load_dotenv()

# Ensure the Google API key is available
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Define the exact phrase the LLM should use to trigger escalation
ESCALATION_PHRASE = "I am unable to answer this question."

# The instruction template for the LLM
PROMPT_TEMPLATE = """
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
"""


class Chatbot:
    def __init__(self, faq_path="data/faqs.csv"):
        """Initializes the chatbot, loads the LLM, embedding model, and FAQ data."""
        # Initialize the Gemini LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

        # Initialize the sentence transformer model for semantic search
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load and process the FAQ data
        self.faqs = pd.read_csv(faq_path)
        # Create a combined text column for embedding
        self.faqs['combined'] = self.faqs['question'] + " " + self.faqs['answer']
        # Pre-compute embeddings for all FAQs for efficient search
        self.faq_embeddings = self.embedding_model.encode(self.faqs['combined'].tolist(), convert_to_tensor=True)

    def _find_relevant_faq(self, user_query: str) -> str:
        """Finds the most relevant FAQ entry for a given user query."""
        query_embedding = self.embedding_model.encode(user_query, convert_to_tensor=True)
        # Calculate cosine similarity between user query and all FAQs
        similarities = util.pytorch_cos_sim(query_embedding, self.faq_embeddings)[0]
        # Find the index of the most similar FAQ
        best_match_idx = int(similarities.argmax().item())

        # If the similarity is very low, it's likely not a relevant FAQ
        if similarities[best_match_idx] < 0.5:
            return "No relevant FAQ found."

        return self.faqs['combined'].iloc[best_match_idx]

    def _format_history(self, history: list) -> str:
        """Formats the conversation history into a readable string for the LLM."""
        if not history:
            return "No history available."
        
        formatted = []
        for entry in history:
            sender = "Human" if entry.sender == 'user' else "AI"
            formatted.append(f"{sender}: {entry.message}")
        return "\n".join(formatted)

    def get_response(self, session_id: str, user_message: str) -> str:
        """The main method to get a response from the chatbot."""
        
        # --- NEW: Hardcoded Greeting Check ---
        # Normalize user input for a more reliable check
        normalized_message = user_message.lower().strip("?!., ")
        greetings = {"hello", "hi", "hii", "hey", "how are you"}
        
        if normalized_message in greetings:
            return "Hello! How can I assist you today?"
        # --- End of New Logic ---

        # 1. Retrieve conversation history from the database
        history_records = database.get_conversation_history(session_id)
        formatted_history = self._format_history(history_records)

        # 2. Find the most relevant FAQ context
        context = self._find_relevant_faq(user_message)

        # 3. Construct the prompt
        prompt = PROMPT_TEMPLATE.format(
            history=formatted_history,
            context=context,
            question=user_message,
            escalation_phrase=ESCALATION_PHRASE
        )

        # 4. Get the response from the LLM
        llm_response = str(self.llm.invoke(prompt).content)

        # 5. Check for escalation
        if ESCALATION_PHRASE in llm_response:
            return "I'm sorry, I can't seem to find the answer. I will escalate this to a human agent for you."
        else:
            return llm_response
        
# Create a single instance of the Chatbot.
# This is efficient as models are loaded only once when the app starts.
chatbot_instance = Chatbot()