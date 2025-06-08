#!/usr/bin/env python3
"""
API simples para teste
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar apenas o repositório
try:
    from backend.app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
    print("✅ Repositório importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar repositório: {e}")
    SinistroRepositoryPyODBC = None

app = FastAPI(title="API Simples de Sinistros", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API Simples funcionando!", "status": "OK"}

@app.get("/test")
def test():
    """Teste simples"""
    if SinistroRepositoryPyODBC is None:
        return {"error": "Repositório não disponível"}
    
    try:
        repo = SinistroRepositoryPyODBC()
        if repo.test_connection():
            sinistros = repo.buscar_sinistros(limit=3)
            return {
                "success": True,
                "connection": "OK",
                "sinistros_found": len(sinistros),
                "sample": sinistros[0] if sinistros else None
            }
        else:
            return {"error": "Falha na conexão com banco"}
    except Exception as e:
        return {"error": f"Erro: {str(e)}"}

if __name__ == "__main__":
    print("🚀 Iniciando API Simples...")
    uvicorn.run(app, host="127.0.0.1", port=8001) 