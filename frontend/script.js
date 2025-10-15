// Get references to the HTML elements
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

// API URLs for the backend
const CHAT_API_URL = 'http://127.0.0.1:8000/chat';
const HISTORY_API_URL = 'http://127.0.0.1:8000/history';

// --- Session ID Management ---
let sessionId = localStorage.getItem('chat_session_id');
if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    localStorage.setItem('chat_session_id', sessionId);
}
console.log("Current Session ID:", sessionId);

// --- Functions ---

// Function to add a single message to the chat box
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    const pElement = document.createElement('p');
    pElement.textContent = message;
    messageElement.appendChild(pElement);
    chatBox.appendChild(messageElement);
    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

// NEW: Function to load chat history from the server
async function loadChatHistory() {
    if (!sessionId) return; // Don't run if there's no session

    try {
        const response = await fetch(`${HISTORY_API_URL}/${sessionId}`);
        if (!response.ok) {
            // If history is not found (404), it's okay, it's just a new chat.
            if (response.status === 404) return;
            throw new Error('Failed to fetch history');
        }
        const history = await response.json();
        
        // If history exists, clear the default welcome message
        if (history.length > 0) {
            chatBox.innerHTML = ''; 
            history.forEach(item => {
                addMessage(item.message, item.sender);
            });
        }
    } catch (error) {
        console.error("Could not load chat history:", error);
    }
}

// --- Event Listeners ---

// Event listener for the form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    addMessage(userMessage, 'user');
    userInput.value = '';

    try {
        const response = await fetch(CHAT_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                message: userMessage,
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Network response was not ok. Status: ${response.status}. Body: ${errorText}`);
        }

        const data = await response.json();
        addMessage(data.response, 'bot');

    } catch (error) {
        console.error('Fetch Error:', error);
        addMessage(`Sorry, there was an error connecting to the bot. Details: ${error.message}`, 'bot');
    }
});

// --- Initial Load ---
// Load the chat history as soon as the page is ready
document.addEventListener('DOMContentLoaded', loadChatHistory);