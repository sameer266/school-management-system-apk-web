from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/bca6"

# Create engine
engine = create_engine(DATABASE_URL)

# Bind session to engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()  # create a new session
    try:
        yield db
    finally:
        db.close()
    



