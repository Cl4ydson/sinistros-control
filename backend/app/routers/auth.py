from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas.user import UserCreate, UserResponse, UserLogin, Token
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Configurações de segurança
import os
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
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

@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o login já existe
    if db.query(models.user.User).filter_by(login=user.login).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Login já cadastrado"
        )
    
    # Verifica se o email já existe
    if db.query(models.user.User).filter_by(email=user.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )

    # Cria novo usuário
    novo = models.user.User(**user.dict(exclude={'senha'}))
    novo.set_password(user.senha)
    
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )

@router.post("/login/", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    print(f"🔐 Tentativa de login para: {user_data.login}")
    
    try:
        user = db.query(models.user.User).filter_by(login=user_data.login).first()
        print(f"👤 Usuário encontrado: {user is not None}")
        
        if user:
            print(f"📧 Email do usuário: {user.email}")
            print(f"👤 Nome do usuário: {user.nome}")
            password_valid = user.verify_password(user_data.senha)
            print(f"🔑 Senha válida: {password_valid}")
        
        if not user or not user.verify_password(user_data.senha):
            print("❌ Login falhou - usuário não encontrado ou senha incorreta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print("✅ Login bem-sucedido!")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"💥 Erro durante login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )
