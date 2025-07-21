from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional

from ..services.sinistro_service_pyodbc import SinistroServicePyODBC
from fastapi import Depends, Query, HTTPException, status
from ..core.auth import get_current_user
from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC

router = APIRouter(prefix="/sinistros", tags=["sinistros"])

@router.get("/")
def list_sinistros(
    dt_ini: Optional[str] = Query(None, description="Data inicial do filtro (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final do filtro (YYYY-MM-DD)"),
    modal: Optional[str] = Query(None, description="Modal de transporte"),
    cliente: Optional[str] = Query(None, description="Nome do cliente"),
    nota_fiscal: Optional[str] = Query(None, description="Nota fiscal"),
    conhecimento: Optional[str] = Query(None, description="Conhecimento"),
    page: int = Query(1, description="Página"),
    limit: int = Query(100, description="Limite por página")
    # current_user: dict = Depends(get_current_user)  # Temporariamente removido para teste
):
    try:
        service = SinistroServicePyODBC()
        result = service.listar_sinistros(
            dt_ini=dt_ini,
            dt_fim=dt_fim,
            cliente=cliente,
            modal=modal,
            nota_fiscal=nota_fiscal,
            conhecimento=conhecimento,
            page=page,
            limit=limit
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar sinistros: {str(e)}"
        )

@router.get("/dashboard/resumo")
def dashboard_resumo():
    return {"success": True, "data": {}}

@router.get("/estatisticas/resumo")
def estatisticas_resumo():
    return {"success": True, "data": {}}

@router.get("/debug-connection")
def debug_connection():
    """Debug endpoint ultra-simples"""
    import pyodbc
    
    try:
        # Teste direto sem repository
        conn_str = "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        conn.close()
        
        return {
            "success": True,
            "message": "Conexão direta funcionou",
            "result": result[0],
            "drivers": pyodbc.drivers()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "drivers": pyodbc.drivers()
        }

@router.get("/test/connection")
def test_connection():
    repo = SinistroRepositoryPyODBC()
    result = repo.test_connection()
    return {
        "success": result, 
        "message": "Conexão OK" if result else "Falha na conexão",
        "connection_string": repo.conn_str
    }

@router.get("/teste-todos")
def teste_todos_sinistros():
    import pyodbc
    import sys
    import os
    
    repo = SinistroRepositoryPyODBC()
    
    debug_info = {
        "python_executable": sys.executable,
        "working_directory": os.getcwd(),
        "available_drivers": pyodbc.drivers(),
        "repo_conn_str": repo.conn_str
    }
    
    try:
        # First test basic connection
        conn_test = repo.test_connection()
        debug_info["basic_connection_test"] = conn_test
        
        if not conn_test:
            return {"erro": "Falha na conexão básica", "debug": debug_info}
        
        # Test direct pyodbc connection
        try:
            conn = pyodbc.connect(repo.conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()
            debug_info["direct_pyodbc_test"] = f"SUCCESS: {result[0]}"
        except Exception as e:
            debug_info["direct_pyodbc_test"] = f"ERROR: {str(e)}"
        
        # Then test the query
        sinistros = repo.buscar_sinistros(limit=2)
        return {
            "total": len(sinistros), 
            "sinistros": sinistros,
            "debug": debug_info,
            "success": True
        }
    except Exception as e:
        import traceback
        return {
            "erro": str(e), 
            "traceback": traceback.format_exc(),
            "debug": debug_info,
            "success": False
        }

@router.get("/sem-auth")
def list_sinistros_sem_auth(
    dt_ini: Optional[str] = Query(None, description="Data inicial do filtro (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final do filtro (YYYY-MM-DD)"),
    modal: Optional[str] = Query(None, description="Modal de transporte"),
    cliente: Optional[str] = Query(None, description="Nome do cliente"),
    nota_fiscal: Optional[str] = Query(None, description="Nota fiscal"),
    conhecimento: Optional[str] = Query(None, description="Conhecimento"),
    page: int = Query(1, description="Página"),
    limit: int = Query(100, description="Limite por página")
):
    """Endpoint temporário sem autenticação para teste"""
    try:
        service = SinistroServicePyODBC()
        result = service.listar_sinistros(
            dt_ini=dt_ini,
            dt_fim=dt_fim,
            cliente=cliente,
            modal=modal,
            nota_fiscal=nota_fiscal,
            conhecimento=conhecimento,
            page=page,
            limit=limit
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar sinistros: {str(e)}"
        )