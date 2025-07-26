"""
Configuração de banco de dados para Vercel
Usa SQLAlchemy com connection pooling otimizado para serverless
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import logging

logger = logging.getLogger(__name__)

class VercelDatabase:
    """Classe para gerenciar conexões de banco no Vercel"""
    
    def __init__(self):
        self.connection_string = self._build_connection_string()
        self.engine = self._create_engine()
    
    def _build_connection_string(self) -> str:
        """Constrói string de conexão para SQL Server"""
        server = os.getenv("DB_SERVER", "SRVTOTVS02")
        database = os.getenv("DB_DATABASE", "AUTOMACAO_BRSAMOR") 
        username = os.getenv("DB_USERNAME", "adm")
        password = os.getenv("DB_PASSWORD", "")
        
        # Para Vercel, use uma connection string que funcione com serverless
        return f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    
    def _create_engine(self):
        """Cria engine SQLAlchemy otimizada para serverless"""
        return create_engine(
            self.connection_string,
            poolclass=NullPool,  # Sem pool para serverless
            echo=False,
            future=True
        )
    
    def execute_query(self, query: str, params: dict = None):
        """Executa query e retorna resultados"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            raise
    
    def execute_command(self, command: str, params: dict = None):
        """Executa comando (INSERT, UPDATE, DELETE)"""
        try:
            with self.engine.connect() as connection:
                with connection.begin():
                    result = connection.execute(text(command), params or {})
                    return result.rowcount
        except Exception as e:
            logger.error(f"Erro ao executar comando: {e}")
            raise

# Instância global para reutilização
vercel_db = VercelDatabase() 