from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date
import logging

from ..database import get_db
from ..services.sinistro_automacao_service import SinistroAutomacaoService
from ..schemas.sinistro_automacao import (
    SinistroAutomacaoCreate,
    SinistroAutomacaoUpdate,
    SinistroAutomacaoResponse
)

router = APIRouter(prefix="/api/automacao/sinistros", tags=["Sinistros Automação"])
logger = logging.getLogger(__name__)

# ============================================================
# DEPENDÊNCIAS
# ============================================================

def get_sinistro_service(db: Session = Depends(get_db)) -> SinistroAutomacaoService:
    """Dependency para obter service dos sinistros"""
    return SinistroAutomacaoService(db)

def get_usuario_atual() -> str:
    """Mock do usuário atual - substituir pela autenticação real"""
    return "sistema"  # Por enquanto fixo

# ============================================================
# ENDPOINTS PRINCIPAIS
# ============================================================

# ============================================================
# ENDPOINTS DE STATUS E SAÚDE (DEVEM VIR PRIMEIRO)
# ============================================================

@router.get("/health")
async def verificar_saude():
    """Health check básico"""
    return {
        "status": "ok",
        "service": "sinistros_automacao",
        "timestamp": str(date.today())
    }

@router.get("/status/sistema")
async def verificar_status_sistema(
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Verifica status do sistema e conectividade com bancos"""
    try:
        status = service.verificar_status_sistema()
        
        return {
            "success": True,
            "data": status,
            "message": "Status do sistema verificado"
        }
        
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/buscar/{nota_fiscal}")
async def buscar_por_nota(
    nota_fiscal: str,
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Busca sinistro por nota fiscal"""
    try:
        sinistro = service.buscar_por_nota(nota_fiscal)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=Dict[str, Any])
async def listar_sinistros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    nota_fiscal: Optional[str] = Query(None),
    cliente: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Lista sinistros com filtros e paginação"""
    try:
        # Montar filtros
        filtros = {}
        if nota_fiscal:
            filtros['nota_fiscal'] = nota_fiscal
        if cliente:
            filtros['cliente'] = cliente
        if status:
            filtros['status'] = status
        
        sinistros, total = service.listar_sinistros(skip, limit, filtros)
        
        return {
            "success": True,
            "data": sinistros,
            "total": total,
            "skip": skip,
            "limit": limit,
            "filtros_aplicados": filtros
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar sinistros: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{sinistro_id}")
async def obter_sinistro(
    sinistro_id: int,
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Obtém sinistro por ID"""
    try:
        sinistro = service.buscar_sinistro(sinistro_id)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}")
async def atualizar_sinistro(
    sinistro_id: int,
    dados: SinistroAutomacaoUpdate,
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza dados específicos do sinistro"""
    try:
        sinistro_atualizado = service.atualizar_sinistro(sinistro_id, dados, usuario)
        
        if not sinistro_atualizado:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro_atualizado,
            "message": "Sinistro atualizado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============================================================
# ENDPOINTS ESPECÍFICOS PARA VALORES
# ============================================================

# ============================================================
# ENDPOINTS SIMPLIFICADOS PARA VALORES ESPECÍFICOS
# ============================================================

@router.put("/{sinistro_id}/valor")
async def atualizar_valor_sinistro(
    sinistro_id: int,
    valor_sinistro: float = Body(...),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza apenas o valor do sinistro"""
    try:
        from decimal import Decimal
        dados_atualizacao = SinistroAutomacaoUpdate(valor_sinistro=Decimal(str(valor_sinistro)))
        
        sinistro_atualizado = service.atualizar_sinistro(sinistro_id, dados_atualizacao, usuario)
        
        if not sinistro_atualizado:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro_atualizado,
            "message": f"Valor do sinistro atualizado para {valor_sinistro}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar valor: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}/status")
async def atualizar_status_sinistro(
    sinistro_id: int,
    status: str = Body(...),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza apenas o status do sinistro"""
    try:
        dados_atualizacao = SinistroAutomacaoUpdate(status_sinistro=status)
        
        sinistro_atualizado = service.atualizar_sinistro(sinistro_id, dados_atualizacao, usuario)
        
        if not sinistro_atualizado:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro_atualizado,
            "message": f"Status do sinistro atualizado para '{status}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}/descricao")
async def atualizar_descricao_sinistro(
    sinistro_id: int,
    descricao: str = Body(...),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza apenas a descrição do sinistro"""
    try:
        dados_atualizacao = SinistroAutomacaoUpdate(descricao=descricao)
        
        sinistro_atualizado = service.atualizar_sinistro(sinistro_id, dados_atualizacao, usuario)
        
        if not sinistro_atualizado:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro_atualizado,
            "message": "Descrição do sinistro atualizada com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar descrição: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}") 