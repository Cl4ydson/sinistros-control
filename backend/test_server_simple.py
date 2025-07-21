#!/usr/bin/env python3

from fastapi import FastAPI
from app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
import uvicorn
import pyodbc

# Criar app simples para teste
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server OK"}

@app.get("/test-db")
def test_database():
    """Teste direto de banco no contexto do servidor"""
    try:
        # Teste 1: pyodbc direto
        conn_str = "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result1 = cursor.fetchone()
        conn.close()
        
        # Teste 2: Repository
        repo = SinistroRepositoryPyODBC()
        result2 = repo.test_connection()
        
        # Teste 3: Busca de sinistros
        sinistros = repo.buscar_sinistros(limit=1)
        
        return {
            "success": True,
            "pyodbc_direct": result1[0],
            "repository_test": result2,
            "sinistros_found": len(sinistros),
            "first_sinistro": sinistros[0] if sinistros else None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

if __name__ == "__main__":
    print("Iniciando servidor de teste...")
    uvicorn.run(app, host="127.0.0.1", port=8004)