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

@router.get("/test/connection")
def test_connection():
    return {"success": True, "message": "Conexão OK"}

@router.get("/teste-todos")
def teste_todos_sinistros():
    repo = SinistroRepositoryPyODBC()
    try:
        sinistros = repo.buscar_sinistros(limit=100)
        return {"total": len(sinistros), "sinistros": sinistros}
    except Exception as e:
        return {"erro": str(e)}

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