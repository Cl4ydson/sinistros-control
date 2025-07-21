"""
Router de debug específico para problemas de conexão
"""
from fastapi import APIRouter
import pyodbc
import os
import sys
from typing import Dict, Any

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/connection-test")
def test_connection_comprehensive() -> Dict[str, Any]:
    """Teste abrangente de conexão no contexto FastAPI"""
    
    result = {
        "environment": {
            "python_path": sys.executable,
            "working_dir": os.getcwd(),
            "pythonpath": sys.path[:3]
        },
        "odbc_drivers": [],
        "connection_tests": []
    }
    
    try:
        # Listar drivers ODBC disponíveis
        result["odbc_drivers"] = pyodbc.drivers()
    except Exception as e:
        result["odbc_drivers_error"] = str(e)
    
    # Diferentes configurações para testar
    connection_configs = [
        {
            "name": "Configuração Original",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
        },
        {
            "name": "Com timeout",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;ConnectionTimeout=30;"
        },
        {
            "name": "Sem TrustServerCertificate", 
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;"
        }
    ]
    
    for config in connection_configs:
        test_result = {
            "name": config["name"],
            "success": False,
            "error": None,
            "result": None
        }
        
        try:
            conn = pyodbc.connect(config["conn_str"])
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test_value")
            row = cursor.fetchone()
            conn.close()
            
            test_result["success"] = True
            test_result["result"] = row[0]
            
        except Exception as e:
            test_result["error"] = str(e)
            test_result["error_type"] = type(e).__name__
        
        result["connection_tests"].append(test_result)
    
    return result

@router.get("/repository-test")
def test_repository_in_fastapi():
    """Testa o repository no contexto FastAPI"""
    try:
        # Import dinâmico para evitar problemas de path
        from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
        
        repo = SinistroRepositoryPyODBC()
        
        # Teste básico
        connection_ok = repo.test_connection()
        
        result = {
            "success": True,
            "connection_test": connection_ok,
            "conn_str": repo.conn_str[:50] + "...",
            "query_test": None
        }
        
        if connection_ok:
            try:
                sinistros = repo.buscar_sinistros(limit=1)
                result["query_test"] = {
                    "success": True,
                    "count": len(sinistros),
                    "first_result": sinistros[0] if sinistros else None
                }
            except Exception as e:
                result["query_test"] = {
                    "success": False,
                    "error": str(e)
                }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }