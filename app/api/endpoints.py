from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas import (
    HealthResponse, ErrorResponse, 
    QuestionnaireRequest, QuestionnaireResponse
)
from app.services.openai_service import get_openai_service, OpenAIService
from app.services.question_service import get_question_service, QuestionService
from app.database import get_db
from app.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to verify service status and configuration.
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        openai_configured=settings.is_openai_configured,
        database_configured=settings.is_database_configured
    )

@router.post("/process-answers", response_model=QuestionnaireResponse)
def process_questionnaire(
    request: QuestionnaireRequest,
    openai_service: OpenAIService = Depends(get_openai_service),
    db: Session = Depends(get_db)
):
    """
    Process questionnaire responses and generate insights using OpenAI.
    
    This endpoint takes a user ID and a map of question IDs to answers,
    builds a prompt from the answers, and returns an AI-generated analysis.
    """
    try:
        # Get question service
        question_service = get_question_service(openai_service)
        
        # Process the question-answer pairs
        result = question_service.process_question_answers(
            user_id=request.user_id,
            question_answers=request.question_answers,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            db=db
        )
        
        return QuestionnaireResponse(
            user_id=result["user_id"],
            prompt=result["prompt"],
            response=result["response"],
            model=result["model"],
            usage=result["usage"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/models", response_model=List[str])
def get_models(
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Get list of available OpenAI models.
    
    Returns a list of model names that can be used with the chat and
    text generation endpoints.
    """
    try:
        return openai_service.get_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

@router.get("/", response_model=dict)
def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "process-answers": "/process-answers",
            "models": "/models"
        }
    } 