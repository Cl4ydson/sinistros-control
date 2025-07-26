from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any, List
from datetime import datetime

from ..models.sinistro_automacao import SinistroAutomacao
from ..models.programacao_pagamento import ProgramacaoPagamento
from ..models.base import Base
from ..database import SessionLocal_Principal, engine_principal
from .programacao_pagamento_repository import ProgramacaoPagamentoRepository

class SinistroAutomacaoRepository:
    """Repository para gerenciar sinistros na tabela de automação (AUTOMACAO_BRSAMOR)"""
    
    def __init__(self):
        self.db = SessionLocal_Principal()
        # Criar tabelas se não existirem
        try:
            Base.metadata.create_all(bind=engine_principal)
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
        
        # Repository para programação de pagamentos
        self.pagamento_repo = ProgramacaoPagamentoRepository()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def criar_sinistro(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo sinistro na tabela de automação"""
        try:
            # Criar objeto SinistroAutomacao
            sinistro = SinistroAutomacao(**dados)
            
            self.db.add(sinistro)
            self.db.commit()
            self.db.refresh(sinistro)
            
            return {
                "success": True,
                "message": "Sinistro criado com sucesso",
                "data": sinistro.to_dict()
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao criar sinistro: {str(e)}",
                "data": None
            }
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro inesperado: {str(e)}",
                "data": None
            }
    
    def obter_sinistro_por_id(self, sinistro_id: int) -> Dict[str, Any]:
        """Obtém um sinistro pelo ID"""
        try:
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.id == sinistro_id
            ).first()
            
            if not sinistro:
                return {
                    "success": False,
                    "message": "Sinistro não encontrado",
                    "data": None
                }
            
            return {
                "success": True,
                "message": "Sinistro encontrado",
                "data": sinistro.to_dict()
            }
        except SQLAlchemyError as e:
            return {
                "success": False,
                "message": f"Erro ao buscar sinistro: {str(e)}",
                "data": None
            }
    
    def obter_sinistro_por_nota(self, nota_fiscal: str) -> Dict[str, Any]:
        """Obtém um sinistro pela nota fiscal"""
        try:
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.nota_fiscal == nota_fiscal
            ).first()
            
            if not sinistro:
                return {
                    "success": False,
                    "message": "Sinistro não encontrado para esta nota fiscal",
                    "data": None
                }
            
            return {
                "success": True,
                "message": "Sinistro encontrado",
                "data": sinistro.to_dict()
            }
        except SQLAlchemyError as e:
            return {
                "success": False,
                "message": f"Erro ao buscar sinistro: {str(e)}",
                "data": None
            }
    
    def atualizar_sinistro(self, sinistro_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um sinistro existente"""
        try:
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.id == sinistro_id
            ).first()
            
            if not sinistro:
                return {
                    "success": False,
                    "message": "Sinistro não encontrado",
                    "data": None
                }
            
            # Atualizar campos
            for key, value in dados.items():
                if hasattr(sinistro, key):
                    setattr(sinistro, key, value)
            
            # Atualizar timestamp
            sinistro.data_atualizacao = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(sinistro)
            
            return {
                "success": True,
                "message": "Sinistro atualizado com sucesso",
                "data": sinistro.to_dict()
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao atualizar sinistro: {str(e)}",
                "data": None
            }
    
    def criar_ou_atualizar_sinistro(self, identificador: str, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Cria ou atualiza um sinistro. Se existir (por nota fiscal), atualiza. Se não, cria."""
        try:
            # Extrair programação de pagamento dos dados se existir
            programacao_pagamento = dados.pop('programacao_pagamento', [])
            
            # Primeiro tentar encontrar por nota fiscal
            dados['nota_fiscal'] = identificador
            
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.nota_fiscal == identificador
            ).first()
            
            if sinistro:
                # Atualizar existente
                for key, value in dados.items():
                    if hasattr(sinistro, key):
                        setattr(sinistro, key, value)
                
                sinistro.data_atualizacao = datetime.utcnow()
                self.db.commit()
                self.db.refresh(sinistro)
                
                # Salvar programação de pagamento
                if programacao_pagamento:
                    self.pagamento_repo.salvar_programacao_pagamentos(sinistro.id, programacao_pagamento)
                
                return {
                    "success": True,
                    "message": "Sinistro atualizado com sucesso",
                    "data": sinistro.to_dict()
                }
            else:
                # Criar novo
                resultado = self.criar_sinistro(dados)
                
                # Se criou com sucesso e tem programação de pagamento, salvar
                if resultado["success"] and programacao_pagamento:
                    sinistro_id = resultado["data"]["id"]
                    self.pagamento_repo.salvar_programacao_pagamentos(sinistro_id, programacao_pagamento)
                    
                    # Buscar novamente com os pagamentos
                    sinistro_atualizado = self.obter_sinistro_por_id(sinistro_id)
                    if sinistro_atualizado["success"]:
                        resultado["data"] = sinistro_atualizado["data"]
                
                return resultado
                
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao criar ou atualizar sinistro: {str(e)}",
                "data": None
            }
    
    def listar_sinistros(self, filtros: Dict[str, Any] = None, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Lista sinistros com filtros opcionais"""
        try:
            query = self.db.query(SinistroAutomacao)
            
            # Aplicar filtros se fornecidos
            if filtros:
                if 'status_geral' in filtros and filtros['status_geral']:
                    query = query.filter(SinistroAutomacao.status_geral == filtros['status_geral'])
                
                if 'nota_fiscal' in filtros and filtros['nota_fiscal']:
                    query = query.filter(SinistroAutomacao.nota_fiscal.like(f"%{filtros['nota_fiscal']}%"))
                
                if 'status_pagamento' in filtros and filtros['status_pagamento']:
                    query = query.filter(SinistroAutomacao.status_pagamento == filtros['status_pagamento'])
            
            # Contagem total
            total = query.count()
            
            # Paginação - SQL Server requer ORDER BY com OFFSET
            sinistros = query.order_by(SinistroAutomacao.id).offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "message": f"Encontrados {len(sinistros)} sinistros",
                "data": [sinistro.to_dict() for sinistro in sinistros],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        except SQLAlchemyError as e:
            return {
                "success": False,
                "message": f"Erro ao listar sinistros: {str(e)}",
                "data": [],
                "total": 0
            }
    
    def deletar_sinistro(self, sinistro_id: int) -> Dict[str, Any]:
        """Deleta um sinistro"""
        try:
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.id == sinistro_id
            ).first()
            
            if not sinistro:
                return {
                    "success": False,
                    "message": "Sinistro não encontrado",
                    "data": None
                }
            
            self.db.delete(sinistro)
            self.db.commit()
            
            return {
                "success": True,
                "message": "Sinistro deletado com sucesso",
                "data": None
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao deletar sinistro: {str(e)}",
                "data": None
            }