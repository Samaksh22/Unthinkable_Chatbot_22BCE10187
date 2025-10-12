// frontend/script.js

// Get references to the HTML elements
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

// API endpoint for the backend
const API_URL = 'http://127.0.0.1:8000/chat';

// Generate or retrieve a unique session ID for the user
let sessionId = localStorage.getItem('chat_session_id');
if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    localStorage.setItem('chat_session_id', sessionId);
}
console.log("Current Session ID:", sessionId); // Check if session ID is set

// Function to add a message to the chat box
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    
    const pElement = document.createElement('p');
    pElement.textContent = message;
    messageElement.appendChild(pElement);
    
    chatBox.appendChild(messageElement);
    // Scroll to the bottom of the chat box to see the new message
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Event listener for the form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission

    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    // Add user's message to the chat box
    addMessage(userMessage, 'user');
    userInput.value = ''; // Clear the input field

    console.log("Sending message to backend:", userMessage); // ADDED FOR DEBUGGING

    try {
        const requestBody = {
            session_id: sessionId,
            message: userMessage,
        };

        console.log("Request Body:", JSON.stringify(requestBody)); // ADDED FOR DEBUGGING

        // Send the message to the backend API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            // Log the error response from the server for more detail
            const errorText = await response.text();
            throw new Error(`Network response was not ok. Status: ${response.status}. Body: ${errorText}`);
        }

        const data = await response.json();
        const botResponse = data.response;

        // Add bot's response to the chat box
        addMessage(botResponse, 'bot');

    } catch (error) {
        // THIS IS THE MOST IMPORTANT PART FOR DEBUGGING
        console.error('Fetch Error:', error); 
        addMessage(`Sorry, there was an error connecting to the bot. Details: ${error.message}`, 'bot');
    }
});