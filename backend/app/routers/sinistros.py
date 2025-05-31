from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
import logging
from ..database import get_db_sinistro
from ..services.sinistro_service import SinistroService
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/sinistros",
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
    limit: int = Query(100, ge=1, le=1000, description="Limite por página"),
    db: Session = Depends(get_db_sinistro)
):
    """
    Lista sinistros com filtros opcionais
    """
    try:
        service = SinistroService(db)
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
async def obter_sinistro(
    sinistro_id: str,
    db: Session = Depends(get_db_sinistro)
):
    """
    Obtém um sinistro específico pelo ID
    """
    try:
        service = SinistroService(db)
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
    dados_atualizacao: dict,
    db: Session = Depends(get_db_sinistro)
):
    """
    Atualiza um sinistro (funcionalidade limitada)
    """
    try:
        service = SinistroService(db)
        
        # Verifica se o sinistro existe
        sinistro_existente = service.obter_sinistro(sinistro_id)
        if not sinistro_existente:
            raise HTTPException(
                status_code=404,
                detail="Sinistro não encontrado"
            )
        
        # Realiza a atualização
        sinistro_atualizado = service.atualizar_sinistro(sinistro_id, dados_atualizacao)
        
        return {
            "success": True,
            "data": sinistro_atualizado,
            "message": "Sinistro atualizado com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.delete("/{sinistro_id}")
async def deletar_sinistro(
    sinistro_id: str,
    db: Session = Depends(get_db_sinistro)
):
    """
    Deleta um sinistro (soft delete)
    """
    try:
        service = SinistroService(db)
        
        # Verifica se o sinistro existe
        sinistro_existente = service.obter_sinistro(sinistro_id)
        if not sinistro_existente:
            raise HTTPException(
                status_code=404,
                detail="Sinistro não encontrado"
            )
        
        # Realiza o soft delete
        service.deletar_sinistro(sinistro_id)
        
        return {
            "success": True,
            "data": None,
            "message": "Sinistro deletado com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar sinistro {sinistro_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/estatisticas/resumo")
async def obter_estatisticas_resumo(
    dt_ini: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db_sinistro)
):
    """
    Obtém estatísticas resumidas dos sinistros
    """
    try:
        service = SinistroService(db)
        estatisticas = service.obter_estatisticas_resumo(dt_ini, dt_fim)
        
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

@router.get("/relatorio/excel")
async def exportar_relatorio_excel(
    dt_ini: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    dt_fim: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    cliente: Optional[str] = Query(None, description="Nome do cliente/destinatário"),
    modal: Optional[str] = Query(None, description="Modal de transporte"),
    db: Session = Depends(get_db_sinistro)
):
    """
    Exporta relatório de sinistros para Excel
    """
    try:
        service = SinistroService(db)
        arquivo_excel = service.exportar_relatorio_excel(
            dt_ini=dt_ini,
            dt_fim=dt_fim,
            cliente=cliente,
            modal=modal
        )
        
        from fastapi.responses import FileResponse
        return FileResponse(
            path=arquivo_excel,
            filename=f"relatorio_sinistros_{date.today().strftime('%Y%m%d')}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        logger.error(f"Erro ao exportar relatório: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/test/connection")
async def testar_conexao(db: Session = Depends(get_db_sinistro)):
    """
    Endpoint para testar a conexão com o banco de dados
    """
    try:
        # Teste simples - contar registros na tabela principal
        result = db.execute(text("SELECT COUNT(*) as total FROM tbdOcorrenciaNota WITH (NOLOCK)"))
        count = result.scalar()
        
        # Teste da query de sinistros (limitando a 5 registros)
        service = SinistroService(db)
        sinistros_teste = service.listar_sinistros(limit=5)
        
        return {
            "success": True,
            "message": "Conexão com banco estabelecida com sucesso",
            "data": {
                "total_ocorrencias": count,
                "sinistros_teste": sinistros_teste,
                "database": "dtbTransporte",
                "server": "172.30.0.211"
            }
        }
    except Exception as e:
        logger.error(f"Erro na conexão com banco: {str(e)}")
        return {
            "success": False,
            "message": f"Erro na conexão: {str(e)}",
            "data": None
        }