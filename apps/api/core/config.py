import os
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = PROJECT_ROOT.parent

# Locate database file reliably across different working directories
if (REPO_ROOT / "titan_silicon.db").exists():
    _DB_FILE = (REPO_ROOT / "titan_silicon.db").as_posix()
elif (PROJECT_ROOT / "titan_silicon.db").exists():
    _DB_FILE = (PROJECT_ROOT / "titan_silicon.db").as_posix()
else:
    _DB_FILE = (REPO_ROOT / "titan_silicon.db").as_posix()

class Settings(BaseSettings):
    PROJECT_NAME: str = "TECH STORE — Siêu Thị Điện Tử Cao Cấp"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database: Supports PostgreSQL or local SQLite fallback
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{_DB_FILE}"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "titan-silicon-super-secret-key-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
