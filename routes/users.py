from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config import get_db
from passlib.context import CryptContext
from repository.users import UserRepo, JWTRepo
from models.users import ResponseSchema, TokenResponse, Register, Login
from tables.users import User

router = APIRouter(
    tags=["Authentication"]
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/signup')
async def signup(request: Register, db: Session = Depends(get_db)):
    try:
        existing_user = UserRepo.get_by_username(db, User, request.username)
        if existing_user:
            return ResponseSchema(
                code="400",
                status="error",
                message="Username already exists"
            ).dict(exclude_none=True)
        
        hashed_password = pwd_context.hash(request.password)
        _user = User(
            username=request.username,
            email=request.email,
            password=hashed_password 
        )
        UserRepo.insert(db, _user)
        return ResponseSchema(
            code="200",
            status="success",
            message="Successfully inserted"
        ).dict(exclude_none=True)
    except IntegrityError:
        db.rollback()
        return ResponseSchema(
            code="400",
            status="error",
            message="Username already exists"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500",
            status="error",
            message="internal error"
        ).dict(exclude_none=True)

@router.post('/login')
async def login(request: Login, db: Session = Depends(get_db)):
    try:
        _user = UserRepo.get_by_username(db, User, request.username)
        if not _user:
            return ResponseSchema(
                code="401",
                status="error",
                message="invalid credentials"
            ).dict(exclude_none=True)
        if not pwd_context.verify(request.password, _user.password):
            return ResponseSchema(
                code="401",
                status="error",
                message="invalid credentials"
            ).dict(exclude_none=True)
        token = JWTRepo.generate_token({'sub': _user.username})
        return ResponseSchema(
            code="200",
            status="OK",
            message="SUCCESS LOGIN",
            result=TokenResponse(access_token=token, token_type="bearer").dict(exclude_none=True)
        )
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500",
            status="error",
            message="internal error"
        ).dict(exclude_none=True)
