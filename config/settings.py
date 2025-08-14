import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration for Gemini and Groq
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Database Configuration (unchanged)
    POSTGRES_URL = "postgresql://aiuser:aipass@localhost:5432/ailifeos"
    REDIS_URL = "redis://localhost:6379/0"
    
    # Letta Configuration - Updated for local hosting
    LETTA_SERVER_URL = "http://localhost:8283"
    
    # Model Configuration - Fixed with required fields
    GEMINI_MODEL = "google_ai/gemini-2.5-flash"
    GROQ_MODEL = "groq/llama-3.3-70b-versatile"
    
    # Embedding Configuration - Fixed for Groq
    GEMINI_EMBEDDING = "google_ai/text-embedding-004"
    GROQ_EMBEDDING = "groq/nomic-embed-text-v1.5"  # Groq-supported embedding model
    
    # Model dimensions (required by Letta)
    GEMINI_EMBEDDING_DIM = 768  # text-embedding-004 dimension
    GROQ_EMBEDDING_DIM = 768    # nomic-embed-text-v1.5 dimension
    
    MEMORY_LIMIT = 8000
    
    # API Endpoints
    GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
    GROQ_API_BASE = "https://api.groq.com/openai/v1"
    
    # Event System (unchanged)
    EVENT_STREAM_NAME = "ai_life_events"
    
    # Development (unchanged)
    DEBUG = True
    LOG_LEVEL = "INFO"

settings = Settings()
