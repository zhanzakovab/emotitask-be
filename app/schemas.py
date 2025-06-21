from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuestionnaireRequest(BaseModel):
    """Model for questionnaire processing request."""
    user_id: int = Field(..., description="User ID")
    question_answers: Dict[str, str] = Field(..., description="Map of question ID to answer")
    model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    max_tokens: Optional[int] = Field(default=1000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(default=0.7, description="Sampling temperature")

class QuestionnaireResponse(BaseModel):
    """Model for questionnaire processing response."""
    user_id: int = Field(..., description="User ID")
    prompt: str = Field(..., description="Generated prompt from answers")
    response: str = Field(..., description="OpenAI response")
    model: str = Field(..., description="Model used for generation")
    usage: Optional[Dict[str, Any]] = Field(default=None, description="Token usage information")

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

class GoalBase(BaseModel):
    """Base Goal schema."""
    name: str = Field(..., description="Goal name")
    description: Optional[str] = Field(None, description="Goal description")

class GoalCreate(GoalBase):
    """Schema for creating a goal."""
    user_id: int

class GoalUpdate(BaseModel):
    """Schema for updating a goal."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class Goal(GoalBase):
    """Schema for goal response."""
    id: int
    user_id: int
    is_completed: bool
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    """Base Task schema."""
    name: str = Field(..., description="Task name")
    description: Optional[str] = Field(None, description="Task description")

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    user_id: int
    goal_id: Optional[int] = None
    priority: int = Field(default=1, description="Task priority (1=Low, 2=Medium, 3=High)")

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    name: Optional[str] = None
    description: Optional[str] = None
    goal_id: Optional[int] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = None

class Task(TaskBase):
    """Schema for task response."""
    id: int
    user_id: int
    goal_id: Optional[int]
    is_completed: bool
    priority: int
    
    class Config:
        from_attributes = True 