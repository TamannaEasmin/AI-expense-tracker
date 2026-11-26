import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import SessionLocal, Expense
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Expense Tracker API")

# Initialize Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Pydantic Schemas
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Expense (POST)
@app.post("/expenses")
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"Message": "Expense added successfully", "Expense": new_expense}

# Get All Expenses (GET)
@app.get("/expenses")
def get_expense(db: Session = Depends(get_db)):
    return db.query(Expense).all()

# AI Analysis (POST)
@app.post("/analyze")
def analyze_expenses(db: Session = Depends(get_db)):
    # Get all expenses from database
    expenses = db.query(Expense).all()
    
    # Error handle
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found to analyze")

    # Prepare data for AI
    expense_data = "\n".join([f"- {e.title}: {e.amount} ({e.category})" for e in expenses])

    # Send prompt to AI
    prompt = f"""
    I have the following list of expenses:
    {expense_data}
    Please analyze these expenses and give me a short, friendly summary in 3 sentences.
    Tell me which category I am spending the most on.
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_message = response.choices[0].message.content
        return {"ai_analysis": ai_message}
    except Exception as e:
        return {"error": str(e)}
