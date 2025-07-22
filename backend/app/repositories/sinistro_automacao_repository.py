from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func
from typing import Optional, List, Dict, Tuple
from datetime import datetime, date
import logging

from ..models.sinistro_automacao import SinistroAutomacao
from ..schemas.sinistro_automacao import (
    SinistroAutomacaoCreate, 
    SinistroAutomacaoUpdate,
    StatusPagamento,
    StatusIndenizacao,
    StatusJuridico,
    StatusSeguradora,
    StatusGeral
)
from ..database import get_db

logger = logging.getLogger(__name__)

class SinistroAutomacaoRepository:
    """
    Repository para operações na tabela Sinistros do banco AUTOMACAO_BRSAMOR
    Suporte completo a UPSERT para atualizações constantes
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def buscar_por_nota_conhecimento(
        self, 
        nota_fiscal: str, 
        nr_conhecimento: Optional[str] = None
    ) -> Optional[SinistroAutomacao]:
        """
        Busca sinistro por nota fiscal e conhecimento (identificação única)
        """
        try:
            query = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.nota_fiscal == nota_fiscal
            )
            
            if nr_conhecimento:
                query = query.filter(SinistroAutomacao.nr_conhecimento == nr_conhecimento)
            else:
                query = query.filter(SinistroAutomacao.nr_conhecimento.is_(None))
                
            return query.first()
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro por nota/conhecimento: {e}")
            return None
    
    def criar_ou_atualizar(
        self, 
        dados: SinistroAutomacaoCreate, 
        usuario: str
    ) -> Tuple[SinistroAutomacao, bool]:
        """
        UPSERT: Cria novo sinistro ou atualiza existente
        Retorna: (sinistro, foi_criado)
        """
        try:
            # Verificar se já existe
            sinistro_existente = self.buscar_por_nota_conhecimento(
                dados.nota_fiscal, 
                dados.nr_conhecimento
            )
            
            if sinistro_existente:
                # ATUALIZAR
                logger.info(f"Atualizando sinistro existente: {dados.nota_fiscal}")
                return self._atualizar_sinistro(sinistro_existente, dados, usuario), False
            else:
                # CRIAR NOVO
                logger.info(f"Criando novo sinistro: {dados.nota_fiscal}")
                return self._criar_sinistro(dados, usuario), True
                
        except Exception as e:
            logger.error(f"Erro no UPSERT do sinistro: {e}")
            self.db.rollback()
            raise
    
    def _criar_sinistro(self, dados: SinistroAutomacaoCreate, usuario: str) -> SinistroAutomacao:
        """Cria novo sinistro"""
        sinistro = SinistroAutomacao(
            **dados.dict(exclude={'criado_por'}),
            criado_por=usuario,
            atualizado_por=usuario,
            status_geral=StatusGeral.NAO_INICIADO.value
        )
        
        self.db.add(sinistro)
        self.db.commit()
        self.db.refresh(sinistro)
        return sinistro
    
    def _atualizar_sinistro(
        self, 
        sinistro: SinistroAutomacao, 
        dados: SinistroAutomacaoCreate, 
        usuario: str
    ) -> SinistroAutomacao:
        """Atualiza sinistro existente com novos dados básicos"""
        
        # Atualizar apenas campos básicos vindos do outro banco
        campos_basicos = [
            'remetente', 'destinatario', 'cliente', 'modal',
            'dt_coleta', 'dt_prazo_entrega', 'dt_entrega_real', 
            'dt_agendamento', 'dt_ocorrencia', 'dt_cadastro',
            'hr_cadastro', 'dt_alteracao', 'hr_alteracao',
            'tipo_ocorrencia', 'descricao_ocorrencia', 
            'ultima_ocorrencia', 'referencia', 'valor_mercadoria'
        ]
        
        for campo in campos_basicos:
            valor = getattr(dados, campo, None)
            if valor is not None:
                setattr(sinistro, campo, valor)
        
        sinistro.atualizado_por = usuario
        sinistro.atualizado_em = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(sinistro)
        return sinistro
    
    def atualizar_campos_especificos(
        self, 
        sinistro_id: int, 
        dados: SinistroAutomacaoUpdate, 
        usuario: str
    ) -> Optional[SinistroAutomacao]:
        """
        Atualiza campos específicos do sinistro (preenchidos pelo usuário)
        """
        try:
            sinistro = self.db.query(SinistroAutomacao).filter(
                SinistroAutomacao.id == sinistro_id
            ).first()
            
            if not sinistro:
                return None
            
            # Atualizar apenas campos não-nulos
            campos_atualizacao = dados.dict(exclude_unset=True, exclude={'atualizado_por'})
            
            for campo, valor in campos_atualizacao.items():
                if hasattr(sinistro, campo):
                    setattr(sinistro, campo, valor)
            
            sinistro.atualizado_por = usuario
            sinistro.atualizado_em = datetime.utcnow()
            
            # Atualizar status geral automaticamente
            self._atualizar_status_geral(sinistro)
            
            self.db.commit()
            self.db.refresh(sinistro)
            return sinistro
            
        except Exception as e:
            logger.error(f"Erro ao atualizar campos específicos: {e}")
            self.db.rollback()
            raise
    
    def _atualizar_status_geral(self, sinistro: SinistroAutomacao):
        """Atualiza status geral baseado nos outros status"""
        
        # Se tem algum acionamento ativo
        tem_acionamento = (
            sinistro.acionamento_juridico or 
            sinistro.acionamento_seguradora or
            sinistro.status_pagamento not in [StatusPagamento.AGUARDANDO_ND.value] or
            sinistro.status_indenizacao not in [StatusIndenizacao.PENDENTE.value]
        )
        
        # Se tudo está finalizado
        tudo_finalizado = (
            sinistro.status_pagamento == StatusPagamento.PAGO.value and
            sinistro.status_indenizacao == StatusIndenizacao.PAGO.value and
            (not sinistro.acionamento_juridico or sinistro.status_juridico == StatusJuridico.INDENIZADO.value) and
            (not sinistro.acionamento_seguradora or sinistro.status_seguradora == StatusSeguradora.INDENIZADO.value)
        )
        
        if tudo_finalizado:
            sinistro.status_geral = StatusGeral.CONCLUIDO.value
        elif tem_acionamento:
            sinistro.status_geral = StatusGeral.EM_ANDAMENTO.value
        else:
            sinistro.status_geral = StatusGeral.NAO_INICIADO.value
    
    def buscar_por_id(self, sinistro_id: int) -> Optional[SinistroAutomacao]:
        """Busca sinistro por ID"""
        return self.db.query(SinistroAutomacao).filter(
            SinistroAutomacao.id == sinistro_id
        ).first()
    
    def listar_sinistros(
        self,
        skip: int = 0,
        limit: int = 100,
        filtros: Optional[Dict] = None
    ) -> List[SinistroAutomacao]:
        """Lista sinistros com filtros opcionais"""
        
        query = self.db.query(SinistroAutomacao)
        
        if filtros:
            if filtros.get('status_geral'):
                query = query.filter(SinistroAutomacao.status_geral == filtros['status_geral'])
            
            if filtros.get('setor_responsavel'):
                query = query.filter(SinistroAutomacao.setor_responsavel == filtros['setor_responsavel'])
            
            if filtros.get('dt_ocorrencia_inicio'):
                query = query.filter(SinistroAutomacao.dt_ocorrencia >= filtros['dt_ocorrencia_inicio'])
            
            if filtros.get('dt_ocorrencia_fim'):
                query = query.filter(SinistroAutomacao.dt_ocorrencia <= filtros['dt_ocorrencia_fim'])
            
            if filtros.get('cliente'):
                query = query.filter(SinistroAutomacao.cliente.ilike(f"%{filtros['cliente']}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def contar_sinistros(self, filtros: Optional[Dict] = None) -> int:
        """Conta total de sinistros com filtros"""
        query = self.db.query(func.count(SinistroAutomacao.id))
        
        if filtros:
            if filtros.get('status_geral'):
                query = query.filter(SinistroAutomacao.status_geral == filtros['status_geral'])
            
            if filtros.get('setor_responsavel'):
                query = query.filter(SinistroAutomacao.setor_responsavel == filtros['setor_responsavel'])
        
        return query.scalar()
    
    def obter_estatisticas(self) -> Dict:
        """Obtém estatísticas consolidadas dos sinistros"""
        try:
            total = self.db.query(func.count(SinistroAutomacao.id)).scalar()
            
            # Por status
            nao_iniciados = self.db.query(func.count(SinistroAutomacao.id)).filter(
                SinistroAutomacao.status_geral == StatusGeral.NAO_INICIADO.value
            ).scalar()
            
            em_andamento = self.db.query(func.count(SinistroAutomacao.id)).filter(
                SinistroAutomacao.status_geral == StatusGeral.EM_ANDAMENTO.value
            ).scalar()
            
            concluidos = self.db.query(func.count(SinistroAutomacao.id)).filter(
                SinistroAutomacao.status_geral == StatusGeral.CONCLUIDO.value
            ).scalar()
            
            # Valores
            valores = self.db.query(
                func.sum(SinistroAutomacao.valor_mercadoria),
                func.sum(SinistroAutomacao.valor_sinistro_total),
                func.sum(SinistroAutomacao.valor_indenizado_total)
            ).first()
            
            # Acionamentos
            juridicos = self.db.query(func.count(SinistroAutomacao.id)).filter(
                SinistroAutomacao.acionamento_juridico == True
            ).scalar()
            
            seguradoras = self.db.query(func.count(SinistroAutomacao.id)).filter(
                SinistroAutomacao.acionamento_seguradora == True
            ).scalar()
            
            return {
                'total_sinistros': total or 0,
                'nao_iniciados': nao_iniciados or 0,
                'em_andamento': em_andamento or 0,
                'concluidos': concluidos or 0,
                'valor_total_mercadorias': float(valores[0] or 0),
                'valor_total_sinistros': float(valores[1] or 0),
                'valor_total_indenizacoes': float(valores[2] or 0),
                'sinistros_juridicos': juridicos or 0,
                'sinistros_seguradoras': seguradoras or 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def deletar(self, sinistro_id: int) -> bool:
        """Deleta sinistro (usar com cuidado)"""
        try:
            sinistro = self.buscar_por_id(sinistro_id)
            if sinistro:
                self.db.delete(sinistro)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao deletar sinistro: {e}")
            self.db.rollback()
            return False 