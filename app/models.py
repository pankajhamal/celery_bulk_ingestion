from sqlalchemy import Column, Integer, String
from app.connection import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=True)
  email = Column(String, unique=True, index=True, nullable=True)