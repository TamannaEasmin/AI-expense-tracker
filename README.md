# AI Expense Tracker API

A FastAPI-based backend that tracks expenses and uses AI (via Groq) to analyze spending habits.

## Features
- Create and list expenses.
- AI-powered analysis of expenses (category-wise spending summary).
- Secure API key management using `.env`.

## Tech Stack
- FastAPI, SQLAlchemy, PostgreSQL
- OpenAI Python Client (Groq API)
- Python-dotenv

## How to Run
1. Clone the repo.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn main:app --reload`
6. Open `http://127.0.0.1:8000/docs` to test.

