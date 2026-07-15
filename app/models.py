from sqlalchemy import Column, Integer, String
from app.connection import Base

class Currency(Base):
  __tablename__ = "currency"

  id = Column(Integer, primary_key=True, index=True)
  code = Column(String, unique=True, index=True, nullable=True)
  symbol = Column(String,   nullable=True)
  name = Column(String, nullable=True)