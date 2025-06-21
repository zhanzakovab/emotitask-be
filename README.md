# EmotiTask Backend Service

A simple Python backend service built with FastAPI that provides endpoints for OpenAI integration and PostgreSQL database management.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **OpenAI Integration**: Chat completion and text generation endpoints
- **Questionnaire Processing**: Intelligent analysis of user responses
- **PostgreSQL Database**: Full database integration with SQLAlchemy ORM
- **Database Models**: User, Goal, and Task management
- **Database Migrations**: Alembic for schema versioning
- **Health Monitoring**: Built-in health check endpoint
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Environment Configuration**: Flexible configuration via environment variables
- **Error Handling**: Comprehensive error handling and validation
- **Chat History Management**: Full CRUD operations for chat conversations
- **Question Management**: Full CRUD operations for questionnaire questions
- **Answer Management**: Full CRUD operations for question answers
- **MBTI Type Management**: Full CRUD operations for personality types
- **User MBTI Type Management**: Full CRUD operations for user-personality relationships
- **Chat Style Management**: Full CRUD operations for personality-based chat styles

## Database Schema

The application uses the following database tables:

- **users**: User information
- **goals**: User goals
- **tasks**: User tasks with priority and completion status
- **chat_histories**: Conversation history with AI responses
- **questions**: Questionnaire questions
- **answers**: Answers to questions
- **mbti_types**: MBTI personality types
- **user_mbti_types**: User-MBTI type relationships
- **chat_styles**: Personality-based chat styles

### Users Table
- `id`: Primary key
- `name`: User name
- `description`: User description
- `email`: Unique email address
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Goals Table
- `id`: Primary key
- `name`: Goal name
- `description`: Goal description
- `user_id`: Foreign key to users
- `is_completed`: Completion status
- `created_at`, `updated_at`: Timestamps

### Tasks Table
- `id`: Primary key
- `name`: Task name
- `description`: Task description
- `user_id`: Foreign key to users
- `is_completed`: Completion status
- `priority`: Task priority (1=Low, 2=Medium, 3=High)
- `created_at`, `updated_at`: Timestamps

### Chat Histories Table
- `id`: Primary key
- `name`: Chat history name
- `description`: Chat history description
- `user_id`: Foreign key to users
- `messages`: Chat history messages
- `model_used`: Model used for the chat
- `tokens_used`: Tokens used for the chat
- `created_at`, `updated_at`: Timestamps

### Questions Table
- `id`: Primary key
- `question`: Question text
- `created_at`, `updated_at`: Timestamps

### Answers Table
- `id`: Primary key
- `question_id`: Foreign key to questions
- `answer`: Answer text
- `created_at`, `updated_at`: Timestamps

### MBTI Types Table
- `id`: Primary key
- `persona_id`: MBTI persona ID (e.g., INTJ, ENFP)
- `name`: MBTI type name
- `description`: MBTI type description
- `created_at`, `updated_at`: Timestamps

### User MBTI Types Table
- `user_id`: Foreign key to users (part of composite primary key)
- `mbti_type_id`: Foreign key to mbti_types (part of composite primary key)
- `created_at`, `updated_at`: Timestamps

### Chat Styles Table
- `id`: Primary key
- `mbti_type_id`: Foreign key to mbti_types
- `keywords`: JSON string of keywords
- `temperature`: Temperature for chat style (0-2)
- `created_at`, `updated_at`: Timestamps

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd emotitask-be
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your OpenAI API key and database URL
```

4. Set up the database:
```bash
# Option 1: Initialize database directly
python init_db.py

# Option 2: Use Alembic migrations (recommended for production)
alembic init alembic  # Only needed once
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Run the service:
```bash
python run.py
```

The service will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Check service status and configuration

### Questionnaire Processing
- **POST** `/api/v1/process-answers` - Process questionnaire responses and generate insights

**Request Body:**
```json
{
  "user_id": 1,
  "question_answers": {
    "1": "I want to improve my productivity at work",
    "2": "I struggle with time management",
    "3": "I work in software development",
    "4": "I have about 2 hours of free time daily"
  },
  "model": "gpt-3.5-turbo",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "user_id": 1,
  "prompt": "Based on the following answers from John, please provide insights and recommendations:...",
  "response": "Based on your responses, here are my insights and recommendations...",
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 300,
    "total_tokens": 450
  }
}
```

### Available Models
- **GET** `/api/v1/models` - Get list of available OpenAI models

### Task Management
- **POST** `/api/v1/tasks` - Create a new task
- **GET** `/api/v1/tasks` - List all tasks for a user
- **GET** `/api/v1/tasks/{task_id}` - Get a specific task
- **PUT** `/api/v1/tasks/{task_id}/complete` - Mark a task as completed
- **PUT** `/api/v1/tasks/{task_id}` - Update a task
- **DELETE** `/api/v1/tasks/{task_id}` - Delete a task

### Chat History Management
- **POST** `/api/v1/chat-history` - Create a new chat history
- **GET** `/api/v1/chat-history` - List all chat histories for a user
- **GET** `/api/v1/chat-history/{chat_id}` - Get a specific chat history
- **PUT** `/api/v1/chat-history/{chat_id}/messages` - Update chat history messages
- **PUT** `/api/v1/chat-history/{chat_id}` - Update chat history general fields
- **DELETE** `/api/v1/chat-history/{chat_id}` - Delete a chat history

### Question Management
- **POST** `/api/v1/questions` - Create a new question
- **GET** `/api/v1/questions` - List all questions
- **GET** `/api/v1/questions/{question_id}` - Get a specific question
- **PUT** `/api/v1/questions/{question_id}` - Update a question
- **DELETE** `/api/v1/questions/{question_id}` - Delete a question

### Answer Management
- **POST** `/api/v1/answers` - Create a new answer
- **GET** `/api/v1/answers` - List all answers (optionally filtered by question_id)
- **GET** `/api/v1/answers/{answer_id}` - Get a specific answer
- **PUT** `/api/v1/answers/{answer_id}` - Update an answer
- **DELETE** `/api/v1/answers/{answer_id}` - Delete an answer

### MBTI Type Management
- **POST** `/api/v1/mbti-types` - Create a new MBTI type
- **GET** `/api/v1/mbti-types` - List all MBTI types
- **GET** `/api/v1/mbti-types/{mbti_type_id}` - Get a specific MBTI type
- **PUT** `/api/v1/mbti-types/{mbti_type_id}` - Update an MBTI type
- **DELETE** `/api/v1/mbti-types/{mbti_type_id}` - Delete an MBTI type

### User MBTI Type Management
- **POST** `/api/v1/user-mbti-types` - Create a new user MBTI type relationship
- **GET** `/api/v1/user-mbti-types` - List all user MBTI type relationships (optionally filtered by user_id)
- **GET** `/api/v1/user-mbti-types/{user_id}/{mbti_type_id}` - Get a specific user MBTI type relationship
- **PUT** `/api/v1/user-mbti-types/{user_id}/{mbti_type_id}` - Update a user MBTI type relationship
- **DELETE** `/api/v1/user-mbti-types/{user_id}/{mbti_type_id}` - Delete a user MBTI type relationship

### Chat Style Management
- **POST** `/api/v1/chat-styles` - Create a new chat style
- **GET** `/api/v1/chat-styles` - List all chat styles (optionally filtered by mbti_type_id)
- **GET** `/api/v1/chat-styles/{chat_style_id}` - Get a specific chat style
- **PUT** `/api/v1/chat-styles/{chat_style_id}` - Update a chat style
- **DELETE** `/api/v1/chat-styles/{chat_style_id}` - Delete a chat style

## Configuration

Environment variables (set in `.env` file):

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: PostgreSQL connection string (required)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: False)

### Database URL Format
```
postgresql://username:password@host:port/database_name
```

Example:
```
postgresql://myuser:mypassword@localhost:5432/emotitask_db
```

## Database Management

### Creating Migrations
```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Database Operations
```bash
# Initialize database (creates all tables)
python init_db.py

# Check migration status
alembic current

# View migration history
alembic history
```

## API Documentation

Once the service is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
emotitask-be/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database configuration
│   ├── schemas.py           # Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── database_models.py # SQLAlchemy models
│   └── services/
│       ├── __init__.py
│       ├── openai_service.py # OpenAI integration
│       └── question_service.py # Questionnaire processing
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
├── init_db.py              # Database initialization script
├── run.py                  # Server startup script
├── test_api.py             # API testing script
└── README.md               # This file
```

## Development

### Running in Development Mode

```bash
python run.py
```

The server will automatically reload when you make changes to the code.

### Testing the API

```bash
# Run the test script to verify all endpoints
python test_api.py
```

### Database Development

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "Add new field"

# Apply the migration
alembic upgrade head

# Reset database (WARNING: This will delete all data)
alembic downgrade base
alembic upgrade head
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in your environment
2. Configure proper CORS origins
3. Use a production WSGI server like Gunicorn
4. Set up proper logging and monitoring
5. Use environment-specific database URLs
6. Set up database backups

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

[Add your license here]