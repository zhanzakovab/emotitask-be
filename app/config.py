import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/emotitask_db")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EmotiTask Backend"
    VERSION: str = "1.0.0"
    
    @property
    def is_openai_configured(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY)
    
    @property
    def is_database_configured(self) -> bool:
        """Check if database URL is configured."""
        return bool(self.DATABASE_URL) and self.DATABASE_URL != "postgresql://username:password@localhost:5432/emotitask_db"

# Create global settings instance
settings = Settings() 