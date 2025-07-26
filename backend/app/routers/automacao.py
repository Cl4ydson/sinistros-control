from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from ..repositories.sinistro_automacao_repository import SinistroAutomacaoRepository

router = APIRouter(prefix="/api/automacao", tags=["automacao"])

class ProgramacaoPagamentoItem(BaseModel):
    """Schema para item de programação de pagamento"""
    data: Optional[str] = ""
    valor: Optional[str] = ""
    doctoESL: Optional[str] = ""

class SinistroAutomacaoCreate(BaseModel):
    """Schema para criação/atualização de sinistro na automação"""
    nota_fiscal: Optional[str] = None
    numero_sinistro: Optional[str] = None
    status_geral: Optional[str] = "Não iniciado"
    status_pagamento: Optional[str] = "Aguardando ND"
    numero_nd: Optional[str] = None
    data_vencimento_nd: Optional[str] = None
    observacoes_pagamento: Optional[str] = None
    status_indenizacao: Optional[str] = "Pendente"
    valor_indenizacao: Optional[float] = 0.0
    responsavel_avaria: Optional[str] = None
    indenizado: Optional[bool] = False
    valor_salvados_vendido: Optional[float] = 0.0
    responsavel_compra_salvados: Optional[str] = None
    valor_venda_salvados: Optional[float] = 0.0
    percentual_desconto_salvados: Optional[float] = 0.0
    programacao_pagamento_salvados: Optional[str] = None
    setor_responsavel: Optional[str] = None
    responsavel_interno: Optional[str] = None
    data_liberacao: Optional[str] = None
    valor_liberado: Optional[float] = 0.0
    observacoes_internas: Optional[str] = None
    acionamento_juridico: Optional[bool] = False
    status_juridico: Optional[str] = "Não acionado"
    data_abertura_juridico: Optional[str] = None
    custas_juridicas: Optional[float] = 0.0
    acionamento_seguradora: Optional[bool] = False
    status_seguradora: Optional[str] = "Não acionado"
    nome_seguradora: Optional[str] = None
    data_abertura_seguradora: Optional[str] = None
    programacao_indenizacao_seguradora: Optional[str] = None
    programacao_pagamento: Optional[List[ProgramacaoPagamentoItem]] = []

@router.post("/sinistros")
def criar_sinistro_automacao(sinistro: SinistroAutomacaoCreate):
    """Cria um novo sinistro na tabela de automação"""
    try:
        repo = SinistroAutomacaoRepository()
        resultado = repo.criar_sinistro(sinistro.dict(exclude_unset=True))
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/sinistros/{sinistro_id}")
def obter_sinistro_automacao(sinistro_id: int):
    """Obtém um sinistro da tabela de automação pelo ID"""
    try:
        repo = SinistroAutomacaoRepository()
        resultado = repo.obter_sinistro_por_id(sinistro_id)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/sinistros/nota/{nota_fiscal}")
def obter_sinistro_por_nota(nota_fiscal: str):
    """Obtém um sinistro da tabela de automação pela nota fiscal"""
    try:
        repo = SinistroAutomacaoRepository()
        resultado = repo.obter_sinistro_por_nota(nota_fiscal)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.put("/sinistros/{sinistro_id}")
def atualizar_sinistro_automacao(sinistro_id: int, sinistro: SinistroAutomacaoCreate):
    """Atualiza um sinistro na tabela de automação"""
    try:
        repo = SinistroAutomacaoRepository()
        dados = sinistro.dict(exclude_unset=True)
        
        # Primeiro tentar atualizar o sinistro existente
        resultado = repo.atualizar_sinistro(sinistro_id, dados)
        
        # Se não encontrar o sinistro, tentar criar um novo usando a nota fiscal como identificador
        if not resultado["success"] and "não encontrado" in resultado["message"].lower():
            if "nota_fiscal" in dados and dados["nota_fiscal"]:
                resultado = repo.criar_ou_atualizar_sinistro(dados["nota_fiscal"], dados)
            else:
                # Se não tiver nota fiscal, usar o ID como identificador
                dados["numero_sinistro"] = str(sinistro_id)
                resultado = repo.criar_sinistro(dados)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/sinistros")
def listar_sinistros_automacao(
    skip: int = Query(0, description="Número de registros para pular"),
    limit: int = Query(100, description="Limite de registros por página"),
    status_geral: Optional[str] = Query(None, description="Filtrar por status geral"),
    nota_fiscal: Optional[str] = Query(None, description="Filtrar por nota fiscal"),
    status_pagamento: Optional[str] = Query(None, description="Filtrar por status de pagamento")
):
    """Lista sinistros da tabela de automação com filtros"""
    try:
        repo = SinistroAutomacaoRepository()
        
        filtros = {}
        if status_geral:
            filtros["status_geral"] = status_geral
        if nota_fiscal:
            filtros["nota_fiscal"] = nota_fiscal
        if status_pagamento:
            filtros["status_pagamento"] = status_pagamento
        
        resultado = repo.listar_sinistros(filtros, skip, limit)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.delete("/sinistros/{sinistro_id}")
def deletar_sinistro_automacao(sinistro_id: int):
    """Deleta um sinistro da tabela de automação"""
    try:
        repo = SinistroAutomacaoRepository()
        resultado = repo.deletar_sinistro(sinistro_id)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.post("/sinistros/criar-ou-atualizar/{identificador}")
def criar_ou_atualizar_sinistro(identificador: str, sinistro: SinistroAutomacaoCreate):
    """Cria ou atualiza um sinistro na tabela de automação usando nota fiscal como identificador"""
    try:
        repo = SinistroAutomacaoRepository()
        dados = sinistro.dict(exclude_unset=True)
        resultado = repo.criar_ou_atualizar_sinistro(identificador, dados)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado["message"]
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/test/connection")
def test_connection_automacao():
    """Testa a conexão com o banco de automação"""
    try:
        repo = SinistroAutomacaoRepository()
        # Tentar uma consulta simples
        resultado = repo.listar_sinistros(limit=1)
        
        if resultado["success"]:
            return {
                "success": True,
                "message": "Conexão com banco de automação OK",
                "database": "AUTOMACAO_BRSAMOR",
                "server": "SRVTOTVS02"
            }
        else:
            return {
                "success": False,
                "message": f"Erro na conexão: {resultado['message']}",
                "database": "AUTOMACAO_BRSAMOR",
                "server": "SRVTOTVS02"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao testar conexão: {str(e)}",
            "database": "AUTOMACAO_BRSAMOR",
            "server": "SRVTOTVS02"
        }