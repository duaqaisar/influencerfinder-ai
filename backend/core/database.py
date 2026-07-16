from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database URL — creates/uses a local file called influencer.db
DATABASE_URL = "sqlite:///./influencer.db"

# Create the SQLAlchemy engine (entry point to the database)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite to allow use across multiple threads (e.g. FastAPI's async workers)
)

# Session factory — creates new DB session objects when called
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit transactions; commit must be explicit
    autoflush=False,   # Don't auto-flush pending changes before every query
    bind=engine         # Bind sessions to the engine created above
)

# Base class that all ORM models will inherit from
Base = declarative_base()

# Dependency function to get a DB session (used with FastAPI's Depends())
def get_db():
    db = SessionLocal()   # Open a new session
    try:
        yield db          # Provide the session to the endpoint that needs it
    finally:
        db.close()         # Ensure the session is closed after use, even if an error occurs
