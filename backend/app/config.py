import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interview.db")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
DEFAULT_QUESTION_COUNT = 7
