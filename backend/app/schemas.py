from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    nome:  str
    login: constr(strip_whitespace=True)
    email: EmailStr
    setor: Optional[str] = None

class UserCreate(UserBase):
    senha: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
