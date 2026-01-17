import os
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, Enum as SQLEnum, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import enum
from urllib.parse import quote_plus

# =====================================================
# AZURE SQL CONFIG
# =====================================================
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

escaped_password = quote_plus(AZURE_SQL_PASSWORD)

DB_URL = f"mssql+pymssql://{AZURE_SQL_USERNAME}:{escaped_password}@{AZURE_SQL_SERVER}:1433/{AZURE_SQL_DATABASE}"

engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =====================================================
# MODELS
# =====================================================
class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, server_default=func.now())

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False)
    icon = Column(String(20))
    title = Column(String(100))
    resource_name = Column(String(200))
    description = Column(String(500))
    status = Column(String(20), default="Running")
    region = Column(String(50), default="East US")
    priority = Column(String(20), default="Medium")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# =====================================================
# HELPERS
# =====================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

def has_column(table_name: str, column_name: str) -> bool:
    inspector = inspect(engine)
    try:
        return column_name in [c["name"] for c in inspector.get_columns(table_name)]
    except Exception:
        return False
