from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.database_models import User
from app.services.openai_service import OpenAIService

class QuestionService:
    """Service class for processing question-answer pairs and generating prompts."""
    
    def __init__(self, openai_service: OpenAIService):
        """Initialize the question service with OpenAI service."""
        self.openai_service = openai_service
    
    def build_prompt_from_answers(self, question_answers: Dict[str, str], user_name: str = "User") -> str:
        """
        Build a prompt from question-answer pairs.
        
        Args:
            question_answers: Dictionary mapping question IDs to answers
            user_name: Name of the user (optional)
            
        Returns:
            Formatted prompt string
        """
        if not question_answers:
            raise ValueError("Question answers cannot be empty")
        
        # Build the prompt
        prompt_parts = [
            f"Based on the following answers from {user_name}, please provide insights and recommendations:",
            "",
            "Answers:"
        ]
        
        # Add each question-answer pair
        for question_id, answer in question_answers.items():
            prompt_parts.append(f"Question {question_id}: {answer}")
        
        prompt_parts.extend([
            "",
            "Please analyze these answers and provide:",
            "1. A summary of the key points",
            "2. Potential insights or patterns",
            "3. Recommendations based on the responses",
            "4. Any follow-up questions that might be helpful"
        ])
        
        return "\n".join(prompt_parts)
    
    def process_question_answers(
        self,
        user_id: int,
        question_answers: Dict[str, str],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Process question-answer pairs and generate OpenAI response.
        
        Args:
            user_id: ID of the user
            question_answers: Dictionary mapping question IDs to answers
            model: OpenAI model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            db: Database session (optional)
            
        Returns:
            Dictionary containing prompt, response, and usage information
        """
        # Get user information if database is available
        user_name = "User"
        if db:
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user_name = user.name
            except Exception as e:
                # Log error but continue with default user name
                print(f"Error fetching user: {e}")
        
        # Build prompt from answers
        prompt = self.build_prompt_from_answers(question_answers, user_name)
        
        # Generate response using OpenAI
        result = self.openai_service.text_completion(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "user_id": user_id,
            "prompt": prompt,
            "response": result["generated_text"],
            "model": result["model"],
            "usage": result["usage"]
        }

# Global question service instance
question_service: Optional[QuestionService] = None

def get_question_service(openai_service: OpenAIService) -> QuestionService:
    """Get or create question service instance."""
    global question_service
    if question_service is None:
        question_service = QuestionService(openai_service)
    return question_service 