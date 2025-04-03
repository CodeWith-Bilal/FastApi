from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')

#Login 

class Login(BaseModel):
    username: str
    password: str
class Register(BaseModel):
    id: str
    username: str
    password: str
    email: str

class ResponseSchema(BaseModel):
    message: str
    code: str
    status: str
    result: Optional[T] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str