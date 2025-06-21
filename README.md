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

## Database Schema

The service includes the following database tables:

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
- `goal_id`: Foreign key to goals (optional)
- `is_completed`: Completion status
- `priority`: Task priority (1=Low, 2=Medium, 3=High)
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