

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from psycopg2.extras import RealDictCursor 
import psycopg2
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host= 'localhost', 
#     database= 'pythonApi1', 
#     user='postgres', 
#     password='1234',
#     cursor_factory= RealDictCursor
#     )
#     cursor = conn.cursor()
#     print("ok")
# except Exception as e:
#     print("paila")