"""
Router simplificado para automação de sinistros
Implementação real com salvamento nas tabelas SinistrosControle e ProgramacaoPagamento
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
import logging
from ..repositories.sinistros_controle_repository import SinistrosControleRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/automacao/sinistros", tags=["Sinistros Automação Simples"])

@router.get("/health")
async def health_check():
    """Health check do sistema de automação"""
    return {
        "success": True,
        "message": "Sistema de automação funcionando",
        "status": "online"
    }

@router.put("/{sinistro_id}")
async def atualizar_sinistro_simples(
    sinistro_id: str,
    dados: Dict[str, Any] = Body(...)
):
    """
    Endpoint para atualizar sinistro - SALVAMENTO REAL nas tabelas SinistrosControle e ProgramacaoPagamento
    """
    try:
        logger.info(f"Recebendo atualização para sinistro: {sinistro_id}")
        logger.info(f"Dados recebidos: {dados}")
        
        # Extrair nota fiscal do ID
        if '-' in sinistro_id:
            nota_fiscal, _ = sinistro_id.split('-', 1)
        else:
            nota_fiscal = sinistro_id
        
        # Adicionar nota fiscal aos dados SEMPRE
        dados['nota_fiscal'] = nota_fiscal
        
        # Criar repositório e salvar no banco
        repo = SinistrosControleRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Verificar/criar tabelas
        repo.criar_tabelas_se_nao_existem()
        
        # Salvar dados
        try:
            sucesso = repo.salvar_ou_atualizar(dados)
            logger.info(f"Resultado do salvamento: {sucesso}")
        except Exception as e:
            logger.error(f"Erro detalhado no salvamento: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro detalhado no salvamento: {str(e)}"
            )
        
        if sucesso:
            logger.info(f"Sinistro {sinistro_id} salvo com sucesso no banco")
            return {
                "success": True,
                "message": f"Sinistro {sinistro_id} salvo com sucesso nas tabelas SinistrosControle e ProgramacaoPagamento",
                "data": {
                    "id": sinistro_id,
                    "status": "salvo_no_banco",
                    "campos_atualizados": list(dados.keys()),
                    "timestamp": "2024-01-01T00:00:00Z",
                    "banco": "AUTOMACAO_BRSAMOR",
                    "tabelas": ["SinistrosControle", "ProgramacaoPagamento"]
                }
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao salvar no banco de dados"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao atualizar sinistro: {str(e)}"
        )

@router.get("/{sinistro_id}")
async def obter_sinistro_simples(sinistro_id: str):
    """
    Endpoint para obter sinistro - BUSCA REAL nas tabelas SinistrosControle e ProgramacaoPagamento
    """
    try:
        logger.info(f"Buscando sinistro: {sinistro_id}")
        
        # Extrair nota fiscal do ID
        if '-' in sinistro_id:
            nota_fiscal, _ = sinistro_id.split('-', 1)
        else:
            nota_fiscal = sinistro_id
        
        # Criar repositório e buscar no banco
        repo = SinistrosControleRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Buscar dados no banco
        sinistro_data = repo.buscar_por_nota_fiscal(nota_fiscal)
        
        if sinistro_data:
            logger.info(f"Sinistro {sinistro_id} encontrado no banco")
            return {
                "success": True,
                "data": sinistro_data,
                "message": "Dados recuperados das tabelas SinistrosControle e ProgramacaoPagamento"
            }
        else:
            # Se não encontrou no banco, retornar dados básicos
            logger.info(f"Sinistro {sinistro_id} não encontrado no banco, retornando dados básicos")
            return {
                "success": True,
                "data": {
                    "id": sinistro_id,
                    "nota_fiscal": nota_fiscal,
                    "status_geral": "Em análise",
                    "valor_indenizacao": 0.0,
                    "message": "Sinistro não encontrado no histórico - dados básicos"
                }
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar sinistro {sinistro_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao buscar sinistro: {str(e)}"
        )

@router.get("/")
async def listar_sinistros_salvos():
    """
    Endpoint para listar todos os sinistros salvos nas tabelas SinistrosControle e ProgramacaoPagamento
    """
    try:
        logger.info("Listando sinistros salvos")
        
        # Criar repositório e buscar no banco
        repo = SinistrosControleRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Listar sinistros
        sinistros = repo.listar_todos(limit=100)
        
        return {
            "success": True,
            "data": sinistros,
            "total": len(sinistros),
            "message": f"Encontrados {len(sinistros)} sinistros nas tabelas SinistrosControle e ProgramacaoPagamento"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar sinistros: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao listar sinistros: {str(e)}"
        )

@router.post("/")
async def criar_sinistro_simples(dados: Dict[str, Any] = Body(...)):
    """
    Endpoint para criar sinistro - SALVAMENTO REAL nas tabelas SinistrosControle e ProgramacaoPagamento
    """
    try:
        logger.info(f"Criando novo sinistro com dados: {dados}")
        
        # Criar repositório e salvar no banco
        repo = SinistrosControleRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Verificar/criar tabelas
        repo.criar_tabelas_se_nao_existem()
        
        # Salvar dados
        sucesso = repo.salvar_ou_atualizar(dados)
        
        if sucesso:
            nota_fiscal = dados.get('nota_fiscal', 'NF000')
            sinistro_id = f"{nota_fiscal}"
            logger.info(f"Sinistro {sinistro_id} criado com sucesso no banco")
            
            return {
                "success": True,
                "message": "Sinistro criado com sucesso nas tabelas SinistrosControle e ProgramacaoPagamento",
                "data": {
                    "id": sinistro_id,
                    "status": "criado_no_banco",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "banco": "AUTOMACAO_BRSAMOR",
                    "tabelas": ["SinistrosControle", "ProgramacaoPagamento"]
                }
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar sinistro no banco de dados"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar sinistro: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao criar sinistro: {str(e)}"
        )