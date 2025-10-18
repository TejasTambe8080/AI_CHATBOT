from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Simple intent matching without NLTK
def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Simple keyword matching
    if any(word in user_input for word in ['hello', 'hi', 'hey']):
        return random.choice([
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?",
            "Hey! Welcome to our customer service."
        ])
    elif any(word in user_input for word in ['bye', 'goodbye', 'see you']):
        return random.choice([
            "Goodbye! Have a great day!",
            "See you later! Thanks for visiting.",
            "Bye! Come back anytime."
        ])
    elif any(word in user_input for word in ['thanks', 'thank you']):
        return random.choice([
            "You're welcome!",
            "Happy to help!",
            "Anytime!"
        ])
    elif any(word in user_input for word in ['hours', 'open', 'time']):
        return "We're open Monday to Friday from 9 AM to 6 PM."
    elif any(word in user_input for word in ['location', 'address', 'where']):
        return "We're located at 123 Main Street, Cityville."
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f0f0f0;
            }
            .chat-container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .chat-header {
                background: #4CAF50;
                color: white;
                padding: 20px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }
            .chat-messages {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                border-bottom: 1px solid #ddd;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
            }
            .user-message {
                background: #e3f2fd;
                text-align: right;
            }
            .bot-message {
                background: #f5f5f5;
                text-align: left;
            }
            .chat-input {
                padding: 20px;
                display: flex;
                gap: 10px;
            }
            #userInput {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🤖 Simple Chatbot</h1>
                <p>Type "hello" to test</p>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    <strong>Bot:</strong> Hello! I'm a simple chatbot. Type "hello" to start!
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="userInput" placeholder="Type your message here...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                const chatMessages = document.getElementById('chatMessages');
                
                if (!message) return;
                
                // Add user message
                const userMsg = document.createElement('div');
                userMsg.className = 'message user-message';
                userMsg.innerHTML = '<strong>You:</strong> ' + message;
                chatMessages.appendChild(userMsg);
                
                // Clear input
                input.value = '';
                
                // Show typing
                const typingMsg = document.createElement('div');
                typingMsg.className = 'message bot-message';
                typingMsg.innerHTML = '<strong>Bot:</strong> ...';
                typingMsg.id = 'typing';
                chatMessages.appendChild(typingMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // Send to server
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Remove typing message
                    document.getElementById('typing').remove();
                    
                    // Add bot response
                    const botMsg = document.createElement('div');
                    botMsg.className = 'message bot-message';
                    botMsg.innerHTML = '<strong>Bot:</strong> ' + data.response;
                    chatMessages.appendChild(botMsg);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                })
                .catch(error => {
                    document.getElementById('typing').remove();
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'message bot-message';
                    errorMsg.innerHTML = '<strong>Bot:</strong> Sorry, I encountered an error.';
                    chatMessages.appendChild(errorMsg);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                });
            }
            
            // Allow Enter key
            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        print(f"Received message: {user_input}")  # Debug print
        
        response = get_bot_response(user_input)
        
        print(f"Sending response: {response}")  # Debug print
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Sorry, I encountered an error.'})

if __name__ == '__main__':
    print("🚀 Starting SUPER SIMPLE Chatbot...")
    print("📍 Access at: http://localhost:5000")
    print("💡 Type 'hello' to test")
    app.run(debug=True, port=5000)