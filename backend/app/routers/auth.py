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

@router.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    """Endpoint para testar conexão com banco de dados"""
    try:
        # Testa conexão
        from sqlalchemy import text
        result = db.execute(text("SELECT COUNT(*) as total FROM [dbo].[Cadastro]")).fetchone()
        return {
            "status": "success",
            "message": f"Conexão OK. {result.total} usuários cadastrados.",
            "database": "AUTOMACAO_BRSAMOR",
            "table": "[dbo].[Cadastro]"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro de conexão com banco: {str(e)}"
        )

@router.post("/login/", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    print(f"🔐 Tentativa de login para: {user_data.login}")
    
    try:
        # Testa conexão com banco
        try:
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            print("✅ Conexão com banco OK")
        except Exception as conn_error:
            print(f"❌ Erro de conexão com banco: {str(conn_error)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro de conexão com banco de dados: {str(conn_error)}"
            )
        
        # Busca usuário
        user = db.query(models.user.User).filter_by(login=user_data.login).first()
        print(f"👤 Usuário encontrado: {user is not None}")
        
        if not user:
            print("❌ Usuário não encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Usuário '{user_data.login}' não encontrado no sistema",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"📧 Email do usuário: {user.email}")
        print(f"👤 Nome do usuário: {user.nome}")
        
        # Verifica senha
        password_valid = user.verify_password(user_data.senha)
        print(f"🔑 Senha válida: {password_valid}")
        
        if not password_valid:
            print("❌ Senha incorreta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha incorreta para este usuário",
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
        print(f"💥 Erro inesperado durante login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado no servidor: {str(e)}"
        )
