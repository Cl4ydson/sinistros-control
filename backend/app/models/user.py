from sqlalchemy import Column, Integer, String
from ..database import Base
from passlib.context import CryptContext
import logging

# Configurar logging
logger = logging.getLogger(__name__)

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
        try:
            self.senha = pwd_context.hash(password)
            logger.info(f"Senha definida para usuário: {self.login}")
        except Exception as e:
            logger.error(f"Erro ao definir senha para {self.login}: {str(e)}")
            raise

    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        try:
            # Debug: mostrar informações sobre a verificação
            logger.info(f"Verificando senha para usuário: {self.login}")
            logger.debug(f"Senha fornecida: {password[:3]}***")  # Apenas primeiros 3 chars
            logger.debug(f"Hash armazenado: {self.senha[:20]}...")  # Apenas início do hash
            
            ok = pwd_context.verify(password, self.senha)
            
            logger.info(f"Resultado verificação senha '{self.login}': {ok}")
            print(f"DEBUG - Verificando senha '{self.login}': {ok}")  # Manter o print para debug imediato
            
            return ok
            
        except Exception as e:
            logger.error(f"Erro ao verificar senha para {self.login}: {str(e)}")
            print(f"ERRO - Verificação senha '{self.login}': {str(e)}")
            return False

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}', nome='{self.nome}')>"