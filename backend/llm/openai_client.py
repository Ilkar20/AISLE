import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class OpenAIClient:
    def __init__(self):
        """
        Initializes the OpenAI client using the API key from environment variables.
        """
        # Fetch the API key from the .env file
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing from the .env file!")
            
        self.client = OpenAI(api_key=self.api_key)
        
        # GPT-5 mini is chosen for its balance of performance and cost-effectiveness
        self.model = "gpt-4o-mini" 

    def get_completion(self, messages: list):
        """
        Sends a list of messages to the OpenAI API and returns the response content.
        
        Args:
            messages (list): A list of message objects (role and content).
            
        Returns:
            str: The raw JSON string from the AI model, or None if an error occurs.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                # Low temperature ensures consistent and professional pedagogical feedback
                temperature=0.3, 
                # Force the model to output a valid JSON object
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log the specific error for debugging
            print(f"OpenAI API Error: {e}")
            return None