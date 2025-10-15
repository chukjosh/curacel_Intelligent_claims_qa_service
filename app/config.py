"""Configuration and environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    STORAGE_FILE: str = "document_store.json"
    
    # Model settings
    GEMINI_MODEL_PRIMARY: str = "gemini-2.5-pro"
    GEMINI_MODEL_FALLBACK: str = "gemini-2.5-flash"
    
    # File upload settings
    ALLOWED_EXTENSIONS: set = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

settings = Settings()
