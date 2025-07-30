from fastapi import APIRouter, HTTPException, status
from ..schemas.user import UserLogin, Token
from ..demo_data import get_demo_user_by_login, verify_demo_password
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
import os

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

router = APIRouter(              
    prefix="/auth",
    tags=["auth"]
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login/", response_model=Token)
def login_demo(user_data: UserLogin):
    """Login em modo demonstração"""
    user = get_demo_user_by_login(user_data.login)
    if not user or not verify_demo_password(user_data.senha, user["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["login"], "user_id": user["id"], "nome": user["nome"]}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_demo():
    """Retorna informações do usuário atual em modo demo"""
    return {
        "id": 1,
        "login": "demo",
        "nome": "Usuário Demo",
        "email": "demo@brsamor.com.br"
    }