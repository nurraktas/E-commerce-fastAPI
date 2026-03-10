from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cok-gizli-bir-key")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
