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
    SinistroAutomacaoOut,
    SinistroAutomacaoResumo,
    EstatisticasSinistros,
    StatusPagamento,
    StatusIndenizacao,
    StatusJuridico,
    StatusSeguradora
)
from ..core.auth import get_current_user
from ..schemas.user import UserResponse

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
# ENDPOINTS DE SINCRONIZAÇÃO
# ============================================================

@router.post("/sincronizar/{nota_fiscal}")
async def sincronizar_sinistro(
    nota_fiscal: str,
    nr_conhecimento: Optional[str] = Query(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """
    Sincroniza um sinistro específico do banco origem para AUTOMACAO_BRSAMOR
    Se já existir, atualiza os dados básicos
    """
    try:
        sinistro, foi_criado = service.sincronizar_sinistro_do_banco_origem(
            nota_fiscal, nr_conhecimento, usuario
        )
        
        return {
            "success": True,
            "data": sinistro,
            "message": f"Sinistro {'criado' if foi_criado else 'sincronizado'} com sucesso",
            "acao": "criado" if foi_criado else "atualizado"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao sincronizar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sincronizar-multiplos")
async def sincronizar_multiplos_sinistros(
    filtros: Dict[str, Any] = Body(...),
    limite: int = Body(100, le=500),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """
    Sincroniza múltiplos sinistros do banco origem
    Aceita filtros como data_inicio, data_fim, cliente, etc.
    """
    try:
        resultado = service.sincronizar_multiplos_sinistros(filtros, usuario, limite)
        
        return {
            "success": True,
            "data": resultado,
            "message": f"Processados {resultado['total_processados']} sinistros. "
                      f"Criados: {resultado['criados']}, Atualizados: {resultado['atualizados']}, "
                      f"Erros: {resultado['erros']}"
        }
        
    except Exception as e:
        logger.error(f"Erro ao sincronizar múltiplos sinistros: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============================================================
# ENDPOINTS CRUD PRINCIPAIS
# ============================================================

@router.get("/", response_model=Dict[str, Any])
async def listar_sinistros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    status_geral: Optional[str] = Query(None),
    setor_responsavel: Optional[str] = Query(None),
    dt_ocorrencia_inicio: Optional[date] = Query(None),
    dt_ocorrencia_fim: Optional[date] = Query(None),
    cliente: Optional[str] = Query(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Lista sinistros com filtros e paginação"""
    try:
        # Montar filtros
        filtros = {}
        if status_geral:
            filtros['status_geral'] = status_geral
        if setor_responsavel:
            filtros['setor_responsavel'] = setor_responsavel
        if dt_ocorrencia_inicio:
            filtros['dt_ocorrencia_inicio'] = dt_ocorrencia_inicio
        if dt_ocorrencia_fim:
            filtros['dt_ocorrencia_fim'] = dt_ocorrencia_fim
        if cliente:
            filtros['cliente'] = cliente
        
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

@router.get("/{sinistro_id}", response_model=SinistroAutomacaoOut)
async def obter_sinistro(
    sinistro_id: int,
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Obtém sinistro por ID"""
    try:
        sinistro = service.buscar_sinistro(sinistro_id)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return sinistro
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/buscar/{nota_fiscal}")
async def buscar_por_nota_conhecimento(
    nota_fiscal: str,
    nr_conhecimento: Optional[str] = Query(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Busca sinistro por nota fiscal e conhecimento"""
    try:
        sinistro = service.buscar_por_nota_conhecimento(nota_fiscal, nr_conhecimento)
        
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

@router.post("/", response_model=SinistroAutomacaoOut)
async def criar_sinistro_manual(
    dados: SinistroAutomacaoCreate,
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Cria sinistro manualmente (sem sincronização)"""
    try:
        sinistro = service.criar_sinistro_manual(dados, usuario)
        
        return sinistro
        
    except Exception as e:
        logger.error(f"Erro ao criar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}")
async def atualizar_sinistro(
    sinistro_id: int,
    dados: SinistroAutomacaoUpdate,
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza campos específicos do sinistro"""
    try:
        sinistro = service.atualizar_sinistro(sinistro_id, dados, usuario)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro,
            "message": "Sinistro atualizado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{sinistro_id}")
async def deletar_sinistro(
    sinistro_id: int,
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Deleta sinistro (usar com cuidado)"""
    try:
        sucesso = service.deletar_sinistro(sinistro_id)
        
        if not sucesso:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "message": "Sinistro deletado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar sinistro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============================================================
# ENDPOINTS DE ATUALIZAÇÃO ESPECÍFICA
# ============================================================

@router.put("/{sinistro_id}/pagamento")
async def atualizar_dados_pagamento(
    sinistro_id: int,
    status_pagamento: StatusPagamento = Body(...),
    numero_nd: Optional[str] = Body(None),
    valor_nd: Optional[float] = Body(None),
    dt_vencimento_nd: Optional[date] = Body(None),
    observacoes_pagamento: Optional[str] = Body(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza especificamente dados de pagamento"""
    try:
        dados = SinistroAutomacaoUpdate(
            status_pagamento=status_pagamento,
            numero_nd=numero_nd,
            valor_nd=valor_nd,
            dt_vencimento_nd=dt_vencimento_nd,
            observacoes_pagamento=observacoes_pagamento
        )
        
        sinistro = service.atualizar_sinistro(sinistro_id, dados, usuario)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro,
            "message": f"Status de pagamento atualizado para: {status_pagamento.value}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar pagamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}/indenizacao")
async def atualizar_dados_indenizacao(
    sinistro_id: int,
    status_indenizacao: StatusIndenizacao = Body(...),
    valor_indenizacao: Optional[float] = Body(None),
    programacao_pagamento: Optional[Dict] = Body(None),
    observacoes_indenizacao: Optional[str] = Body(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza especificamente dados de indenização"""
    try:
        dados = SinistroAutomacaoUpdate(
            status_indenizacao=status_indenizacao,
            valor_indenizacao=valor_indenizacao,
            programacao_pagamento=programacao_pagamento,
            observacoes_indenizacao=observacoes_indenizacao
        )
        
        sinistro = service.atualizar_sinistro(sinistro_id, dados, usuario)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro,
            "message": f"Status de indenização atualizado para: {status_indenizacao.value}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar indenização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{sinistro_id}/uso-interno")
async def atualizar_uso_interno(
    sinistro_id: int,
    setor_responsavel: Optional[str] = Body(None),
    responsavel_interno: Optional[str] = Body(None),
    valor_liberado: Optional[float] = Body(None),
    observacoes_internas: Optional[str] = Body(None),
    service: SinistroAutomacaoService = Depends(get_sinistro_service),
    usuario: str = Depends(get_usuario_atual)
):
    """Atualiza dados de uso interno"""
    try:
        dados = SinistroAutomacaoUpdate(
            setor_responsavel=setor_responsavel,
            responsavel_interno=responsavel_interno,
            valor_liberado=valor_liberado,
            observacoes_internas=observacoes_internas
        )
        
        sinistro = service.atualizar_sinistro(sinistro_id, dados, usuario)
        
        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")
        
        return {
            "success": True,
            "data": sinistro,
            "message": "Dados de uso interno atualizados com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar uso interno: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============================================================
# ENDPOINTS DE ESTATÍSTICAS E RELATÓRIOS
# ============================================================

@router.get("/estatisticas/resumo", response_model=EstatisticasSinistros)
async def obter_estatisticas(
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Obtém estatísticas consolidadas dos sinistros"""
    try:
        stats = service.obter_estatisticas()
        return stats
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/dashboard/metricas")
async def obter_metricas_dashboard(
    service: SinistroAutomacaoService = Depends(get_sinistro_service)
):
    """Obtém métricas para dashboard"""
    try:
        stats = service.obter_estatisticas()
        
        # Calcular métricas adicionais
        total = stats.total_sinistros
        taxa_conclusao = (stats.concluidos / total * 100) if total > 0 else 0
        
        return {
            "success": True,
            "data": {
                "total_sinistros": total,
                "em_andamento": stats.em_andamento,
                "concluidos": stats.concluidos,
                "taxa_conclusao": round(taxa_conclusao, 2),
                "valor_total_prejuizo": float(stats.valor_total_prejuizo),
                "sinistros_juridicos": stats.sinistros_com_acionamento_juridico,
                "sinistros_seguradoras": stats.sinistros_com_acionamento_seguradora
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ============================================================
# ENDPOINT DE SAÚDE DO SISTEMA
# ============================================================

@router.get("/health")
async def verificar_saude():
    """Verifica saúde do sistema de automação"""
    try:
        return {
            "success": True,
            "message": "Sistema de automação funcionando",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Erro na verificação de saúde: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}") 