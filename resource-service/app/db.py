import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.db import engine, SessionLocal, Base, User, UserRole, Resource, get_db, init_db

__all__ = ['get_db', 'init_db', 'User', 'UserRole', 'Resource', 'engine', 'SessionLocal', 'Base']

print("✅ Resource service using SHARED database")
