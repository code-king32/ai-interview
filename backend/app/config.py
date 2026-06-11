import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./interview.db")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_RESUME_EXTENSIONS: set = field(default_factory=lambda: {".pdf", ".docx", ".doc", ".txt"})
    DEFAULT_QUESTION_COUNT: int = 7
    # PostgreSQL: export DATABASE_URL="postgresql://user:pass@localhost:5432/interview"
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))


settings = Settings()

# 兼容旧代码的扁平导出
DATABASE_URL = settings.DATABASE_URL
ANTHROPIC_API_KEY = settings.ANTHROPIC_API_KEY
ANTHROPIC_MODEL = settings.ANTHROPIC_MODEL
UPLOAD_DIR = settings.UPLOAD_DIR
MAX_UPLOAD_SIZE = settings.MAX_UPLOAD_SIZE
ALLOWED_RESUME_EXTENSIONS = settings.ALLOWED_RESUME_EXTENSIONS
DEFAULT_QUESTION_COUNT = settings.DEFAULT_QUESTION_COUNT
