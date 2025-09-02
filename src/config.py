# src/config.py - Configuration settings for Harry Potter RAG System
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Harry Potter RAG System"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    CHROMA_DB_PATH = DATA_DIR / "chroma_db"
    
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Model Configuration
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    DEFAULT_LLM_MODEL = "llama-3.1-8b-instant"
    FALLBACK_MODELS = [
        "mixtral-8x7b-32768",
        "llama3-8b-8192", 
        "llama2-70b-4096"
    ]
    
    # RAG Configuration
    RETRIEVAL_K = 5
    SCORE_THRESHOLD = 0.3
    
    # API Configuration
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7
    TOP_P = 0.9
    REQUEST_TIMEOUT = 45
    MAX_RETRIES = 3
    
    # UI Configuration
    GRADIO_PORT = 7860
    GRADIO_HOST = "127.0.0.1"
    SHARE_LINK = False
    DEBUG_MODE = True
    
    # Chroma Configuration
    COLLECTION_NAME = "langchain"
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check if Chroma DB exists
        if not cls.CHROMA_DB_PATH.exists():
            errors.append(f"Chroma database not found at: {cls.CHROMA_DB_PATH}")
        
        # Check API key
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY not set in environment variables")
        
        # Create directories if they don't exist
        cls.DATA_DIR.mkdir(exist_ok=True)
        
        return errors
    
    @classmethod
    def get_database_info(cls):
        """Get information about the existing database"""
        if not cls.CHROMA_DB_PATH.exists():
            return None
            
        db_files = list(cls.CHROMA_DB_PATH.glob("*"))
        total_size = sum(f.stat().st_size for f in db_files if f.is_file())
        
        return {
            "path": str(cls.CHROMA_DB_PATH),
            "files": len(db_files),
            "size_mb": round(total_size / (1024 * 1024), 2),
            "exists": True
        }

# Create a global config instance
config = Config()