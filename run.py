#!/usr/bin/env python3
"""
Simple script to run the EmotiTask backend service.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"Server will be available at http://{settings.HOST}:{settings.PORT}")
    print(f"API documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Health check: http://{settings.HOST}:{settings.PORT}/health")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 