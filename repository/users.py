from typing import TypeVar, Optional, Generic
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM

T = TypeVar('T')

class BaseRepo():
    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

class UserRepo(BaseRepo):
    @staticmethod
    def get_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()

class JWTRepo:
    @staticmethod
    def generate_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=1) 

        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded
        except JWTError:
            return {"error": "Token is invalid or expired"}