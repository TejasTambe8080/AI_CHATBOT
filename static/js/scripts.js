class ChatInterface {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearButton = document.getElementById('clearButton');
        this.saveButton = document.getElementById('saveButton');
        
        this.initializeEventListeners();
        console.log("🤖 ChatInterface initialized successfully!");
    }
    
    initializeEventListeners() {
        // Send button click
        this.sendButton.onclick = () => this.sendMessage();
        
        // Enter key in input field
        this.userInput.onkeypress = (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        };
        
        // Clear button
        this.clearButton.onclick = () => this.clearChat();
        
        // Save button
        this.saveButton.onclick = () => this.saveConversation();
        
        console.log("✅ Event listeners initialized");
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        console.log("📤 Sending message:", message);
        
        if (!message) {
            console.log("❌ No message to send");
            return;
        }
        
        // Clear input and add user message
        this.userInput.value = '';
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            console.log("🔄 Sending request to server...");
            
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            console.log("✅ Response status:", response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("📥 Received data:", data);
            
            // Remove typing indicator and add bot response
            this.removeTypingIndicator();
            this.addMessage(data.response, 'bot');
            
        } catch (error) {
            console.error('❌ Error:', error);
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        console.log(`💬 Message added: ${sender} - ${content}`);
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content typing';
        contentDiv.innerHTML = 'Bot is typing...';
        
        typingDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(typingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    async clearChat() {
        console.log("🧹 Clearing chat");
        this.chatMessages.innerHTML = '';
        this.addMessage('Chat cleared. How can I help you?', 'bot');
        
        try {
            await fetch('/clear_history', { method: 'POST' });
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    }
    
    async saveConversation() {
        console.log("💾 Saving conversation");
        try {
            const response = await fetch('/save_conversation', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                alert('✅ Conversation saved successfully!');
            } else {
                alert('❌ Failed to save conversation.');
            }
        } catch (error) {
            console.error('Error saving conversation:', error);
            alert('❌ Error saving conversation.');
        }
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 DOM loaded, initializing chat...");
    new ChatInterface();
});