import json
from datetime import datetime

def save_conversation(conversation_history, filename=None):
    """Save conversation history to a file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    try:
        with open(filename, 'w') as file:
            json.dump(conversation_history, file, indent=2)
        print(f"Conversation saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False

def load_conversation(filename):
    """Load conversation history from a file"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading conversation: {e}")
        return []

def print_chat_message(sender, message):
    """Format and print chat messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {sender}: {message}")