from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """User model representing application users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    user_mbti_types = relationship("UserMBTIType", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    """Task model representing tasks"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)  # 1=Low, 2=Medium, 3=High
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tasks")

class ChatHistory(Base):
    """ChatHistory model representing chat conversations."""
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    messages = Column(Text, nullable=True)  # JSON string of chat messages
    model_used = Column(String(100), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_histories")

class Question(Base):
    """Question model representing questionnaire questions."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

class Answer(Base):
    """Answer model representing answers to questions."""
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    question = relationship("Question", back_populates="answers")

class MBTIType(Base):
    """MBTI Type model representing different MBTI personality types."""
    __tablename__ = "mbti_types"
    
    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(String(10), unique=True, nullable=False)  # e.g., "INTJ", "ENFP"
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user_mbti_types = relationship("UserMBTIType", back_populates="mbti_type", cascade="all, delete-orphan")
    chat_styles = relationship("ChatStyle", back_populates="mbti_type", cascade="all, delete-orphan")

class UserMBTIType(Base):
    """User MBTI Type model representing the relationship between users and their MBTI types."""
    __tablename__ = "user_mbti_types"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mbti_type_id = Column(Integer, ForeignKey("mbti_types.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'mbti_type_id'),
    )
    
    # Relationships
    user = relationship("User", back_populates="user_mbti_types")
    mbti_type = relationship("MBTIType", back_populates="user_mbti_types")

class ChatStyle(Base):
    """Chat Style model representing chat styles for different MBTI types."""
    __tablename__ = "chat_styles"
    
    id = Column(Integer, primary_key=True, index=True)
    mbti_type_id = Column(Integer, ForeignKey("mbti_types.id"), nullable=False)
    keywords = Column(Text, nullable=True)  # JSON string of keywords
    temperature = Column(Float, nullable=False, default=0.7)  # 0-2 range
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mbti_type = relationship("MBTIType", back_populates="chat_styles")

