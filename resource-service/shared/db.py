import os
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from pathlib import Path
import enum

# Database configuration - AZURE SQL IS MANDATORY
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

if not all([AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD]):
    raise RuntimeError(
        "❌ MISSING AZURE SQL CONFIGURATION. "
        "Please set AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, and AZURE_SQL_PASSWORD environment variables."
    )

# Use pymssql driver (uses FreeTDS, no Microsoft ODBC driver required)
# Format: mssql+pymssql://username:password@server:port/database
from urllib.parse import quote_plus

# Escape special characters in password
escaped_password = quote_plus(AZURE_SQL_PASSWORD)

# Build connection URL for pymssql
SHARED_DB_PATH = f"mssql+pymssql://{AZURE_SQL_USERNAME}:{escaped_password}@{AZURE_SQL_SERVER}:1433/{AZURE_SQL_DATABASE}"

print(f"✅ Using AZURE SQL database: {AZURE_SQL_SERVER}/{AZURE_SQL_DATABASE}")

engine = create_engine(SHARED_DB_PATH, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable=False)
    is_protected = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False, index=True)
    icon = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    resource_name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), default="Running")
    region = Column(String(50), default="East US")
    priority = Column(String(20), default="Medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ThemeConfig(Base):
    __tablename__ = "theme_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(String(2000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️ DB init note (tables may already exist): {type(e).__name__}")

from sqlalchemy import inspect

def has_column(table_name: str, column_name: str) -> bool:
    """
    Safely check whether a column exists in a table.
    Used for backward/forward DB compatibility across versions.
    """
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        return any(col["name"] == column_name for col in columns)
    except Exception as e:
        print(f"⚠️ has_column check failed: {e}")
        return False
