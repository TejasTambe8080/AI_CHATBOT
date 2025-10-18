from nlp_processor import NLPProcessor  # Fixed import

class Chatbot:
    def __init__(self, intents_file='intents.json'):
        self.nlp_processor = NLPProcessor(intents_file)
        self.conversation_history = []
    
    def process_message(self, user_input):
        """Process user input and generate response"""
        # Identify intent
        intent = self.nlp_processor.identify_intent(user_input)
        
        # Generate response
        response = self.nlp_processor.get_response(intent)
        
        # Store conversation
        self.conversation_history.append({
            'user': user_input,
            'bot': response,
            'intent': intent['tag'] if intent else 'unknown'
        })
        
        return response
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []