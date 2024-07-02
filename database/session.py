from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database.models import base, Student, User, Club, Event, Registration
from sqlalchemy import create_engine
from datetime import datetime
import os




load_dotenv('.env')
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Db Successfully Loaded")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise
    finally:
        db.close()


session = next(get_db())

