from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas import (
    HealthResponse, ErrorResponse, 
    QuestionnaireRequest, QuestionnaireResponse,
    Task, TaskCreate, TaskUpdate,
    ChatHistory, ChatHistoryCreate, ChatHistoryUpdate, ChatHistoryUpdateMessages
)
from app.services.openai_service import get_openai_service, OpenAIService
from app.services.question_service import get_question_service, QuestionService
from app.database import get_db
from app.config import settings
from app.models.database_models import Task as TaskModel, ChatHistory as ChatHistoryModel

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

# Task Management Endpoints

@router.post("/tasks", response_model=Task)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    """
    try:
        db_task = TaskModel(
            name=task.name,
            description=task.description,
            user_id=task.user_id,
            goal_id=task.goal_id,
            priority=task.priority,
            is_completed=False
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@router.get("/tasks", response_model=List[Task])
def list_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    List all tasks for a specific user.
    """
    try:
        tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    """
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task: {str(e)}")

@router.put("/tasks/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a task as completed.
    """
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.is_completed = True
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error completing task: {str(e)}")

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task.
    """
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update only provided fields
        if task_update.name is not None:
            task.name = task_update.name
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.goal_id is not None:
            task.goal_id = task_update.goal_id
        if task_update.is_completed is not None:
            task.is_completed = task_update.is_completed
        if task_update.priority is not None:
            task.priority = task_update.priority
        
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    """
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

# Chat History Endpoints

@router.put("/chat-history/{chat_id}/messages", response_model=ChatHistory)
def update_chat_history_messages(
    chat_id: int,
    update_data: ChatHistoryUpdateMessages,
    db: Session = Depends(get_db)
):
    """
    Update the messages in a chat history.
    
    This endpoint allows updating the messages JSON string, model used, and tokens used
    for a specific chat history entry.
    """
    try:
        chat_history = db.query(ChatHistoryModel).filter(ChatHistoryModel.id == chat_id).first()
        if not chat_history:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        # Update the messages and related fields
        chat_history.messages = update_data.messages
        if update_data.model_used is not None:
            chat_history.model_used = update_data.model_used
        if update_data.tokens_used is not None:
            chat_history.tokens_used = update_data.tokens_used
        
        db.commit()
        db.refresh(chat_history)
        return chat_history
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating chat history messages: {str(e)}")

@router.get("/chat-history/{chat_id}", response_model=ChatHistory)
def get_chat_history(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific chat history by ID.
    """
    try:
        chat_history = db.query(ChatHistoryModel).filter(ChatHistoryModel.id == chat_id).first()
        if not chat_history:
            raise HTTPException(status_code=404, detail="Chat history not found")
        return chat_history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")

@router.get("/chat-history", response_model=List[ChatHistory])
def list_chat_histories(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    List all chat histories for a specific user.
    """
    try:
        chat_histories = db.query(ChatHistoryModel).filter(ChatHistoryModel.user_id == user_id).all()
        return chat_histories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat histories: {str(e)}")

@router.post("/chat-history", response_model=ChatHistory)
def create_chat_history(
    chat_history: ChatHistoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new chat history.
    """
    try:
        db_chat_history = ChatHistoryModel(
            name=chat_history.name,
            description=chat_history.description,
            user_id=chat_history.user_id,
            messages=chat_history.messages,
            model_used=chat_history.model_used,
            tokens_used=chat_history.tokens_used
        )
        db.add(db_chat_history)
        db.commit()
        db.refresh(db_chat_history)
        return db_chat_history
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chat history: {str(e)}")

@router.put("/chat-history/{chat_id}", response_model=ChatHistory)
def update_chat_history(
    chat_id: int,
    chat_history_update: ChatHistoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a chat history (general fields like name, description).
    """
    try:
        chat_history = db.query(ChatHistoryModel).filter(ChatHistoryModel.id == chat_id).first()
        if not chat_history:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        # Update only provided fields
        if chat_history_update.name is not None:
            chat_history.name = chat_history_update.name
        if chat_history_update.description is not None:
            chat_history.description = chat_history_update.description
        if chat_history_update.messages is not None:
            chat_history.messages = chat_history_update.messages
        if chat_history_update.model_used is not None:
            chat_history.model_used = chat_history_update.model_used
        if chat_history_update.tokens_used is not None:
            chat_history.tokens_used = chat_history_update.tokens_used
        
        db.commit()
        db.refresh(chat_history)
        return chat_history
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating chat history: {str(e)}")

@router.delete("/chat-history/{chat_id}")
def delete_chat_history(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a chat history.
    """
    try:
        chat_history = db.query(ChatHistoryModel).filter(ChatHistoryModel.id == chat_id).first()
        if not chat_history:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        db.delete(chat_history)
        db.commit()
        return {"message": "Chat history deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting chat history: {str(e)}")