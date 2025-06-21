from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuestionnaireRequest(BaseModel):
    """Model for questionnaire processing request."""
    user_id: int = Field(..., description="User ID")
    question_answers: Dict[str, str] = Field(..., description="Map of question ID to answer")

class QuestionnaireResponse(BaseModel):
    """Model for questionnaire processing response."""
    user_id: int = Field(..., description="User ID")

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    openai_configured: bool = Field(..., description="Whether OpenAI is configured")
    database_configured: bool = Field(..., description="Whether database is configured")

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")

# Database schemas
class UserBase(BaseModel):
    """Base User schema."""
    name: str = Field(..., description="User name")
    description: Optional[str] = Field(None, description="User description")
    email: str = Field(..., description="User email")

class UserCreate(UserBase):
    """Schema for creating a user."""
    pass

class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    """Base Task schema."""
    name: str = Field(..., description="Task name")
    description: Optional[str] = Field(None, description="Task description")

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    user_id: int
    priority: int = Field(default=1, description="Task priority (1=Low, 2=Medium, 3=High)")

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = None

class Task(TaskBase):
    """Schema for task response."""
    id: int
    user_id: int
    is_completed: bool
    priority: int
    
    class Config:
        from_attributes = True

class ChatHistoryBase(BaseModel):
    """Base ChatHistory schema."""
    name: str = Field(..., description="Chat history name")
    description: Optional[str] = Field(None, description="Chat history description")

class ChatHistoryCreate(ChatHistoryBase):
    """Schema for creating a chat history."""
    user_id: int
    messages: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None

class ChatHistoryUpdate(BaseModel):
    """Schema for updating a chat history."""
    name: Optional[str] = None
    description: Optional[str] = None
    messages: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None

class ChatHistoryUpdateMessages(BaseModel):
    """Schema for updating chat history messages specifically."""
    messages: str = Field(..., description="JSON string of chat messages")
    model_used: Optional[str] = Field(None, description="Model used for the conversation")
    tokens_used: Optional[int] = Field(None, description="Total tokens used in the conversation")

class ChatHistory(ChatHistoryBase):
    """Schema for chat history response."""
    id: int
    user_id: int
    messages: Optional[str]
    model_used: Optional[str]
    tokens_used: Optional[int]
    
    class Config:
        from_attributes = True

class UserMBTITypeBase(BaseModel):
    """Base User MBTI Type schema."""
    user_id: int = Field(..., description="User ID")
    mbti_type_id: int = Field(..., description="MBTI Type ID")

class UserMBTITypeCreate(UserMBTITypeBase):
    """Schema for creating a user MBTI type relationship."""
    pass

class UserMBTITypeUpdate(BaseModel):
    """Schema for updating a user MBTI type relationship."""
    mbti_type_id: Optional[int] = None

class UserMBTIType(UserMBTITypeBase):
    """Schema for user MBTI type response."""
    
    class Config:
        from_attributes = True 