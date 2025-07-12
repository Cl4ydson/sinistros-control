from sqlalchemy import Column, Integer, String
from ..database import Base
from passlib.context import CryptContext

# Configuração para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "[dbo].[Cadastro]"

    id    = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome  = Column(String(60),  nullable=False)
    login = Column(String(60),  nullable=False, unique=True, index=True)
    senha = Column(String(128), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    setor = Column(String(60))

    def set_password(self, password: str):
        """Define a senha com hash"""
        self.senha = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        if self.senha is None:
            return False
        return pwd_context.verify(password, str(self.senha))
