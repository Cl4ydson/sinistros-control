"""
Router simplificado para automação de sinistros
Implementação real com salvamento no banco eSinistros
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
import logging
from ..repositories.esinistros_repository import ESinistrosRepository

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
    Endpoint para atualizar sinistro - SALVAMENTO REAL no banco eSinistros
    """
    try:
        logger.info(f"Recebendo atualização para sinistro: {sinistro_id}")
        logger.info(f"Dados recebidos: {dados}")
        
        # Extrair nota fiscal e conhecimento do ID
        if '-' in sinistro_id:
            nota_fiscal, nr_conhecimento = sinistro_id.split('-', 1)
        else:
            nota_fiscal = sinistro_id
            nr_conhecimento = None
        
        # Adicionar nota fiscal e conhecimento aos dados se não estiverem presentes
        if 'nota_fiscal' not in dados:
            dados['nota_fiscal'] = nota_fiscal
        if 'nr_conhecimento' not in dados and nr_conhecimento:
            dados['nr_conhecimento'] = nr_conhecimento
        
        # Criar repositório e salvar no banco
        repo = ESinistrosRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Verificar/criar tabela
        repo.criar_tabela_se_nao_existe()
        
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
                "message": f"Sinistro {sinistro_id} salvo com sucesso no banco eSinistros",
                "data": {
                    "id": sinistro_id,
                    "status": "salvo_no_banco",
                    "campos_atualizados": list(dados.keys()),
                    "timestamp": "2024-01-01T00:00:00Z",
                    "banco": "AUTOMACAO_BRSAMOR",
                    "tabela": "eSinistros"
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
    Endpoint para obter sinistro - BUSCA REAL no banco eSinistros
    """
    try:
        logger.info(f"Buscando sinistro: {sinistro_id}")
        
        # Extrair nota fiscal e conhecimento do ID
        if '-' in sinistro_id:
            nota_fiscal, nr_conhecimento = sinistro_id.split('-', 1)
        else:
            nota_fiscal = sinistro_id
            nr_conhecimento = None
        
        # Criar repositório e buscar no banco
        repo = ESinistrosRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Buscar dados no banco
        sinistro_data = repo.buscar_por_nota_conhecimento(nota_fiscal, nr_conhecimento)
        
        if sinistro_data:
            logger.info(f"Sinistro {sinistro_id} encontrado no banco")
            return {
                "success": True,
                "data": sinistro_data,
                "message": "Dados recuperados do banco eSinistros"
            }
        else:
            # Se não encontrou no banco, retornar dados básicos
            logger.info(f"Sinistro {sinistro_id} não encontrado no banco, retornando dados básicos")
            return {
                "success": True,
                "data": {
                    "id": sinistro_id,
                    "Nota Fiscal": nota_fiscal,
                    "Minu.Conh": nr_conhecimento,
                    "STATUS SINISTRO": "Em análise",
                    "VALOR DO SINISTRO ": 0.0,
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
    Endpoint para listar todos os sinistros salvos na tabela eSinistros
    """
    try:
        logger.info("Listando sinistros salvos")
        
        # Criar repositório e buscar no banco
        repo = ESinistrosRepository()
        
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
            "message": f"Encontrados {len(sinistros)} sinistros na tabela eSinistros"
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
    Endpoint para criar sinistro - SALVAMENTO REAL no banco eSinistros
    """
    try:
        logger.info(f"Criando novo sinistro com dados: {dados}")
        
        # Criar repositório e salvar no banco
        repo = ESinistrosRepository()
        
        # Testar conexão primeiro
        if not repo.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Erro de conexão com o banco de dados"
            )
        
        # Verificar/criar tabela
        repo.criar_tabela_se_nao_existe()
        
        # Salvar dados
        sucesso = repo.salvar_ou_atualizar(dados)
        
        if sucesso:
            sinistro_id = f"{dados.get('nota_fiscal', 'NF000')}-{dados.get('nr_conhecimento', 'CT000')}"
            logger.info(f"Sinistro {sinistro_id} criado com sucesso no banco")
            
            return {
                "success": True,
                "message": "Sinistro criado com sucesso no banco eSinistros",
                "data": {
                    "id": sinistro_id,
                    "status": "criado_no_banco",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "banco": "AUTOMACAO_BRSAMOR",
                    "tabela": "eSinistros"
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