from sqlalchemy import Column , Integer , String , Boolean, DateTime
from config import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)