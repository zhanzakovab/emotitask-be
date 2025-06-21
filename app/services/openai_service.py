import openai
from typing import List, Dict, Any, Optional
from app.config import settings

class OpenAIService:
    """Service class for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI client with API key."""
        if not settings.is_openai_configured:
            raise ValueError("OpenAI API key not configured")
        
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate chat completion using OpenAI API.
        
        Args:
            messages: List of chat messages as dicts
            model: OpenAI model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dictionary containing response and usage information
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None
            }
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def text_completion(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate text completion using OpenAI API.
        
        Args:
            prompt: Input prompt for text generation
            model: OpenAI model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dictionary containing generated text and usage information
        """
        try:
            response = self.client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "generated_text": response.choices[0].text.strip(),
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None
            }
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def get_models(self) -> List[str]:
        """
        Get list of available OpenAI models.
        
        Returns:
            List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise Exception(f"Failed to fetch models: {str(e)}")

# Global OpenAI service instance
openai_service: Optional[OpenAIService] = None

def get_openai_service() -> OpenAIService:
    """Get or create OpenAI service instance."""
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service 