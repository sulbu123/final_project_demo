from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 데이터베이스 설정
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/quiz_db"
    
    # JWT 설정
    SECRET_KEY: str = "dev_temporary_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI 설정
    OPENAI_API_KEY: str = "dummy_key_for_development"  # 개발 환경용 더미 키
    
    # Weaviate 설정
    WEAVIATE_URL: str = "http://localhost:8080"
    
    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379"
    
    # 파일 업로드 설정
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    class Config:
        env_file = ".env"

settings = Settings() 