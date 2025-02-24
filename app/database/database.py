import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()  # Load environment variables

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
