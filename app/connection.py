from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

#Create global database engine
engine = create_engine(
  settings.DATABASE_URL,
  pool_size = 10, # Max persistent connections in the pools
  max_overflow=20, # Max extra temporary connections
  pool_pre_ping=True #Check if connectin is alive before using it
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db  = SessionLocal()
  try:
    yield db
  finally:
    db.close()