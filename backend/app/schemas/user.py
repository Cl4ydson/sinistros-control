from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    nome: str
    login: constr(strip_whitespace=True)
    email: EmailStr
    setor: Optional[str] = None

class UserCreate(UserBase):
    senha: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    login: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: Optional[str] = None
