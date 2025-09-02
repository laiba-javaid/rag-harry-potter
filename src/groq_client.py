# src/groq_client.py - Groq API Client
import requests
import time
from typing import List
from config import config

class GroqClient:
    """Groq API client with fallback models and retry logic"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.models = [config.DEFAULT_LLM_MODEL] + config.FALLBACK_MODELS
    
    def chat(
        self, 
        prompt: str, 
        model: str = None,
        max_tokens: int = None,
        temperature: float = None
    ) -> str:
        """Send a chat request to Groq API with fallback support"""
        
        # Use provided model or default
        models_to_try = [model] if model else self.models
        
        # Default parameters
        max_tokens = max_tokens or config.MAX_TOKENS
        temperature = temperature or config.TEMPERATURE
        
        # System message for Harry Potter context
        system_message = (
            "You are a knowledgeable Harry Potter expert and helpful assistant. "
            "Provide detailed, accurate answers based on the given context. "
            "Reference specific books, characters, or events when possible. "
            "Maintain a warm, knowledgeable tone while being precise and informative."
        )
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # Try each model with retry logic
        for attempt, current_model in enumerate(models_to_try):
            for retry in range(config.MAX_RETRIES):
                try:
                    payload = {
                        "model": current_model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": config.TOP_P
                    }
                    
                    response = requests.post(
                        self.base_url,
                        headers=self.headers,
                        json=payload,
                        timeout=config.REQUEST_TIMEOUT
                    )
                    
                    # Success case
                    if response.status_code == 200:
                        result = response.json()["choices"][0]["message"]["content"]
                        if attempt > 0:
                            print(f"🔄 Used fallback model: {current_model}")
                        return result
                    
                    # Rate limit case
                    elif response.status_code == 429:
                        wait_time = 2 ** retry  # Exponential backoff
                        print(f"⏳ Rate limited, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        if retry == config.MAX_RETRIES - 1:
                            break
                        continue
                    
                    # Other API errors
                    else:
                        if retry == config.MAX_RETRIES - 1:
                            print(f"⚠️ API Error {response.status_code} with {current_model}")
                            if attempt < len(models_to_try) - 1:
                                print(f"🔄 Trying fallback model...")
                            break
                        continue
                
                except requests.exceptions.Timeout:
                    if retry == config.MAX_RETRIES - 1:
                        print(f"⏰ Timeout with {current_model}")
                        if attempt < len(models_to_try) - 1:
                            print(f"🔄 Trying fallback model...")
                        break
                    time.sleep(1)
                    continue
                
                except Exception as e:
                    if retry == config.MAX_RETRIES - 1:
                        print(f"❌ Error with {current_model}: {str(e)}")
                        if attempt < len(models_to_try) - 1:
                            print(f"🔄 Trying fallback model...")
                        break
                    time.sleep(1)
                    continue
        
        # All models failed
        return "🚫 All language models are currently unavailable. Please try again later."
    
    def test_connection(self) -> dict:
        """Test the Groq API connection"""
        try:
            test_response = self.chat(
                "Hello, this is a test message. Please respond with 'Test successful!'",
                max_tokens=50
            )
            
            return {
                "status": "success",
                "message": "Connection successful",
                "response": test_response,
                "api_key_valid": True
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Connection failed: {str(e)}",
                "api_key_valid": False
            }
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.models.copy()

# Create a global client instance
groq_client = GroqClient()