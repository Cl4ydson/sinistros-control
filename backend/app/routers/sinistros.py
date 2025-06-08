from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date
import logging
from ..services.sinistro_service_pyodbc import SinistroServicePyODBC
from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sinistros",  # removendo /api para ficar compatível com o frontend
    tags=["sinistros"]
)

@router.get("/")
async def listar_sinistros(
    dt_ini: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    cliente: Optional[str] = Query(None, description="Nome do cliente/destinatário"),
    modal: Optional[str] = Query(None, description="Modal de transporte"),
    nota_fiscal: Optional[str] = Query(None, description="Número da nota fiscal"),
    conhecimento: Optional[str] = Query(None, description="Número do conhecimento"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(None, description="Limite por página (None = todos os registros)")
):
    """
    Lista sinistros com filtros opcionais - Retorna TODOS os registros se limit=None
    """
    try:
        # Se limit não foi especificado, buscar TODOS os registros (8 mil+)
        if limit is None:
            limit = 50000  # Limite alto para garantir que pegue todos os registros
        
        service = SinistroServicePyODBC()
        resultado = service.listar_sinistros(
            dt_ini=dt_ini,
            dt_fim=dt_fim,
            cliente=cliente,
            modal=modal,
            nota_fiscal=nota_fiscal,
            conhecimento=conhecimento,
            page=page,
            limit=limit
        )
        
        return {
            "success": True,
            "data": resultado,
            "message": f"Encontrados {resultado['total']} sinistros"
        }
    except Exception as e:
        logger.error(f"Erro ao listar sinistros: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/{sinistro_id}")
async def obter_sinistro(sinistro_id: str):
    """
    Obtém um sinistro específico pelo ID
    """
    try:
        service = SinistroServicePyODBC()
        sinistro = service.obter_sinistro(sinistro_id)
        
        if not sinistro:
            raise HTTPException(
                status_code=404,
                detail="Sinistro não encontrado"
            )
        
        return {
            "success": True,
            "data": sinistro,
            "message": "Sinistro encontrado com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter sinistro {sinistro_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.put("/{sinistro_id}")
async def atualizar_sinistro(
    sinistro_id: str,
    dados_atualizacao: dict
):
    """
    Atualiza um sinistro (funcionalidade limitada - apenas para demonstração)
    """
    try:
        service = SinistroServicePyODBC()
        
        # Verifica se o sinistro existe
        sinistro_existente = service.obter_sinistro(sinistro_id)
        if not sinistro_existente:
            raise HTTPException(
                status_code=404,
                detail="Sinistro não encontrado"
            )
        
        # Como é uma consulta read-only, apenas simular a atualização
        # Em um cenário real, você implementaria a lógica de update
        
        return {
            "success": True,
            "data": {**sinistro_existente, **dados_atualizacao},
            "message": "Sinistro atualizado com sucesso (simulado)"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/estatisticas/resumo")
async def obter_estatisticas_resumo(
    dt_ini: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Obtém estatísticas resumidas dos sinistros
    """
    try:
        service = SinistroServicePyODBC()
        
        # Converter strings para datas se fornecidas
        dt_ini_obj = None
        dt_fim_obj = None
        
        if dt_ini:
            from datetime import datetime
            dt_ini_obj = datetime.strptime(dt_ini, '%Y-%m-%d').date()
        if dt_fim:
            from datetime import datetime
            dt_fim_obj = datetime.strptime(dt_fim, '%Y-%m-%d').date()
        
        estatisticas = service.obter_estatisticas(dt_ini_obj, dt_fim_obj)
        
        return {
            "success": True,
            "data": estatisticas,
            "message": "Estatísticas obtidas com sucesso"
        }
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/test/connection")
async def testar_conexao():
    """
    Endpoint para testar a conexão com o banco de dados
    """
    try:
        repository = SinistroRepositoryPyODBC()
        
        # Testa a conexão
        conexao_ok = repository.test_connection()
        
        if not conexao_ok:
            raise HTTPException(
                status_code=500,
                detail="Falha na conexão com o banco de dados"
            )
        
        # Busca uma amostra de dados para teste
        sinistros_teste = repository.buscar_sinistros(limit=5)
        
        return {
            "success": True,
            "message": "Conexão com banco estabelecida com sucesso",
            "data": {
                "conexao": "OK",
                "sinistros_amostra": len(sinistros_teste),
                "database": "dtbTransporte",
                "server": "172.30.0.211",
                "total_estimado": "~8000 registros"
            }
        }
    except Exception as e:
        logger.error(f"Erro na conexão com banco: {str(e)}")
        return {
            "success": False,
            "message": f"Erro na conexão: {str(e)}",
            "data": None
        }