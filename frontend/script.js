// frontend/script.js

// --- Element References ---
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const clearBtn = document.getElementById('clear-btn');
const resetBtn = document.getElementById('reset-btn');

// --- API URLs ---
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

// Adds a single message to the chat box
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    const pElement = document.createElement('p');
    pElement.textContent = message;
    messageElement.appendChild(pElement);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Loads chat history from the server
async function loadChatHistory() {
    try {
        const response = await fetch(`${HISTORY_API_URL}/${sessionId}`);
        if (!response.ok) throw new Error('No history found.');
        
        const history = await response.json();
        chatBox.innerHTML = '';
        if (history.length > 0) {
            history.forEach(item => addMessage(item.message, item.sender));
        } else {
            addMessage("Hello! How can I help you today?", "bot");
        }
    } catch (error) {
        chatBox.innerHTML = '';
        addMessage("Hello! How can I help you today?", "bot");
    }
}

// --- Event Listeners ---

// Handle sending a message
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
            body: JSON.stringify({ session_id: sessionId, message: userMessage }),
        });
        if (!response.ok) throw new Error('Network response was not ok.');
        const data = await response.json();
        addMessage(data.response, 'bot');
    } catch (error) {
        console.error('Fetch Error:', error);
        addMessage('Sorry, something went wrong. Please try again.', 'bot');
    }
});

// NEW: Clear Chat Button
clearBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear this chat history?')) return;
    try {
        await fetch(`${HISTORY_API_URL}/${sessionId}`, { method: 'DELETE' });
        chatBox.innerHTML = ''; // Visually clear the chat
        addMessage("Hello! How can I help you today?", "bot"); // Add welcome message back
    } catch (error) {
        console.error('Failed to clear chat:', error);
    }
});

// NEW: Reset Session Button
resetBtn.addEventListener('click', () => {
    if (!confirm('Are you sure you want to start a new session?')) return;
    localStorage.removeItem('chat_session_id'); // Remove old session ID
    location.reload(); // Reload the page to generate a new session
});

// --- Initial Load ---
document.addEventListener('DOMContentLoaded', loadChatHistory);