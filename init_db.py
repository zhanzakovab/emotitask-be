#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables and sets up the database.
"""

import os
import sys
from sqlalchemy import create_engine
from app.config import settings
from app.models.database_models import Base

def init_database():
    """Initialize the database by creating all tables."""
    
    if not settings.is_database_configured:
        print("❌ Database not configured. Please set DATABASE_URL in your .env file.")
        sys.exit(1)
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Create all tables
        print("🔄 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        print(f"📊 Database URL: {settings.DATABASE_URL}")
        
        # List created tables
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Initializing EmotiTask Database...")
    print("=" * 50)
    init_database()
    print("=" * 50)
    print("🎉 Database initialization complete!") 