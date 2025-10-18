import re
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

download_nltk_data()

class NLPProcessor:
    def __init__(self, intents_file='intents.json'):
        self.intents = self.load_intents(intents_file)
        self.stop_words = set(stopwords.words('english'))
        print(f"Loaded {len(self.intents)} intents")  # Debug print
        
    def load_intents(self, intents_file):
        """Load intents from JSON file"""
        try:
            with open(intents_file, 'r') as file:
                data = json.load(file)
                print("Intents file loaded successfully")  # Debug print
                return data['intents']
        except FileNotFoundError:
            print(f"Error: {intents_file} not found.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {intents_file}: {e}")
            return []
    
    def preprocess_text(self, text):
        """Preprocess input text by tokenizing and cleaning"""
        # Convert to lowercase
        text = text.lower().strip()
        print(f"Original text: '{text}'")  # Debug print
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        
        print(f"Processed tokens: {tokens}")  # Debug print
        return tokens
    
    def calculate_similarity(self, input_tokens, pattern_tokens):
        """Calculate similarity between input and pattern using simple matching"""
        input_set = set(input_tokens)
        pattern_set = set(pattern_tokens)
        
        if not input_set or not pattern_set:
            return 0
            
        # Count matching words
        matches = len(input_set.intersection(pattern_set))
        total_unique = len(input_set.union(pattern_set))
        
        similarity = matches / total_unique if total_unique > 0 else 0
        print(f"Similarity: {similarity} (matches: {matches}, total: {total_unique})")  # Debug print
        return similarity
    
    def identify_intent(self, user_input):
        """Identify the intent of user input using keyword matching"""
        print(f"\n=== Identifying intent for: '{user_input}' ===")  # Debug print
        
        # First, check for exact matches (case-insensitive)
        user_input_lower = user_input.lower().strip()
        print(f"Checking exact matches for: '{user_input_lower}'")  # Debug print
        
        for intent in self.intents:
            for pattern in intent['patterns']:
                if user_input_lower == pattern.lower():
                    print(f"Exact match found: {intent['tag']}")  # Debug print
                    return intent
        
        # If no exact match, use similarity scoring
        user_tokens = self.preprocess_text(user_input)
        best_match = None
        highest_similarity = 0
        
        for intent in self.intents:
            print(f"Checking intent: {intent['tag']}")  # Debug print
            for pattern in intent['patterns']:
                pattern_tokens = self.preprocess_text(pattern)
                similarity = self.calculate_similarity(user_tokens, pattern_tokens)
                
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = intent
                    print(f"New best match: {intent['tag']} with similarity {similarity}")  # Debug print
        
        # Set threshold for matching
        print(f"Highest similarity: {highest_similarity}")  # Debug print
        if highest_similarity > 0.1:  # Lowered threshold for better matching
            print(f"Intent identified: {best_match['tag']}")  # Debug print
            return best_match
        else:
            # Return fallback intent
            for intent in self.intents:
                if intent['tag'] == 'fallback':
                    print("No good match found, using fallback")  # Debug print
                    return intent
            return None
    
    def get_response(self, intent):
        """Get a random response for the identified intent"""
        if intent and 'responses' in intent:
            response = random.choice(intent['responses'])
            print(f"Generated response: {response}")  # Debug print
            return response
        return "I'm sorry, I didn't understand that."