from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any
from datetime import datetime

from ..models.programacao_pagamento import ProgramacaoPagamento
from ..models.base import Base
from ..database import SessionLocal_Principal, engine_principal

class ProgramacaoPagamentoRepository:
    """Repository para gerenciar programação de pagamentos"""
    
    def __init__(self):
        self.db = SessionLocal_Principal()
        # Criar tabelas se não existirem
        try:
            Base.metadata.create_all(bind=engine_principal)
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def salvar_programacao_pagamentos(self, sinistro_id: int, programacao_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Salva toda a programação de pagamentos de um sinistro (substitui a existente)"""
        try:
            # Primeiro, deletar todas as programações existentes do sinistro
            self.db.query(ProgramacaoPagamento).filter(
                ProgramacaoPagamento.sinistro_id == sinistro_id
            ).delete()
            
            # Inserir as novas programações
            pagamentos_criados = []
            for i, pagamento_data in enumerate(programacao_list):
                if pagamento_data.get('data') or pagamento_data.get('valor') or pagamento_data.get('doctoESL'):
                    # Só criar se pelo menos um campo estiver preenchido
                    pagamento = ProgramacaoPagamento(
                        sinistro_id=sinistro_id,
                        data_pagamento=pagamento_data.get('data', ''),
                        valor_pagamento=float(pagamento_data.get('valor', 0)) if pagamento_data.get('valor') else 0.0,
                        documento_esl=pagamento_data.get('doctoESL', ''),
                        ordem=i + 1
                    )
                    self.db.add(pagamento)
                    pagamentos_criados.append(pagamento)
            
            self.db.commit()
            
            # Refresh para obter os IDs
            for pagamento in pagamentos_criados:
                self.db.refresh(pagamento)
            
            return {
                "success": True,
                "message": f"Programação de pagamentos salva com sucesso. {len(pagamentos_criados)} pagamentos criados.",
                "data": [pagamento.to_dict() for pagamento in pagamentos_criados]
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao salvar programação de pagamentos: {str(e)}",
                "data": []
            }
    
    def obter_programacao_pagamentos(self, sinistro_id: int) -> Dict[str, Any]:
        """Obtém toda a programação de pagamentos de um sinistro"""
        try:
            pagamentos = self.db.query(ProgramacaoPagamento).filter(
                ProgramacaoPagamento.sinistro_id == sinistro_id
            ).order_by(ProgramacaoPagamento.ordem).all()
            
            return {
                "success": True,
                "message": f"Encontrados {len(pagamentos)} pagamentos programados",
                "data": [pagamento.to_dict() for pagamento in pagamentos]
            }
        except SQLAlchemyError as e:
            return {
                "success": False,
                "message": f"Erro ao obter programação de pagamentos: {str(e)}",
                "data": []
            }
    
    def deletar_programacao_pagamentos(self, sinistro_id: int) -> Dict[str, Any]:
        """Deleta toda a programação de pagamentos de um sinistro"""
        try:
            deleted_count = self.db.query(ProgramacaoPagamento).filter(
                ProgramacaoPagamento.sinistro_id == sinistro_id
            ).delete()
            
            self.db.commit()
            
            return {
                "success": True,
                "message": f"{deleted_count} pagamentos deletados",
                "data": None
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao deletar programação de pagamentos: {str(e)}",
                "data": None
            }
    
    def adicionar_pagamento(self, sinistro_id: int, pagamento_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona um pagamento individual à programação"""
        try:
            # Obter a próxima ordem
            max_ordem = self.db.query(ProgramacaoPagamento.ordem).filter(
                ProgramacaoPagamento.sinistro_id == sinistro_id
            ).order_by(ProgramacaoPagamento.ordem.desc()).first()
            
            nova_ordem = (max_ordem[0] + 1) if max_ordem else 1
            
            pagamento = ProgramacaoPagamento(
                sinistro_id=sinistro_id,
                data_pagamento=pagamento_data.get('data', ''),
                valor_pagamento=float(pagamento_data.get('valor', 0)) if pagamento_data.get('valor') else 0.0,
                documento_esl=pagamento_data.get('doctoESL', ''),
                ordem=nova_ordem
            )
            
            self.db.add(pagamento)
            self.db.commit()
            self.db.refresh(pagamento)
            
            return {
                "success": True,
                "message": "Pagamento adicionado com sucesso",
                "data": pagamento.to_dict()
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao adicionar pagamento: {str(e)}",
                "data": None
            }
    
    def atualizar_pagamento(self, pagamento_id: int, pagamento_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um pagamento específico"""
        try:
            pagamento = self.db.query(ProgramacaoPagamento).filter(
                ProgramacaoPagamento.id == pagamento_id
            ).first()
            
            if not pagamento:
                return {
                    "success": False,
                    "message": "Pagamento não encontrado",
                    "data": None
                }
            
            # Atualizar campos
            if 'data' in pagamento_data:
                pagamento.data_pagamento = pagamento_data['data']
            if 'valor' in pagamento_data:
                pagamento.valor_pagamento = float(pagamento_data['valor']) if pagamento_data['valor'] else 0.0
            if 'doctoESL' in pagamento_data:
                pagamento.documento_esl = pagamento_data['doctoESL']
            
            pagamento.data_atualizacao = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(pagamento)
            
            return {
                "success": True,
                "message": "Pagamento atualizado com sucesso",
                "data": pagamento.to_dict()
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erro ao atualizar pagamento: {str(e)}",
                "data": None
            }