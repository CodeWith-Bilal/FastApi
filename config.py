from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql://postgres:8080*Bilal@localhost:5432/crudOperation'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#JWT
SECRET_KEY = "double_dog123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440