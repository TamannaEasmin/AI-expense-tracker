import os

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/expense_db")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
