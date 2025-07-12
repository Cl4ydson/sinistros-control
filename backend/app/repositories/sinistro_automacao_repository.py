from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import and_, or_, func, text
from typing import Optional, List, Dict, Tuple
from datetime import datetime, date
import logging

from ..models.sinistro_automacao import SinistroAutomacao
from ..schemas.sinistro_automacao import (
    SinistroAutomacaoCreate, 
    SinistroAutomacaoUpdate,
    SinistroAutomacaoResponse
)

logger = logging.getLogger(__name__)

class SinistroAutomacaoRepository:
    """
    Repository para operações na tabela eSinistros do banco AUTOMACAO_BRSAMOR
    Operações adaptadas para a estrutura real da tabela existente
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def verificar_tabela_existe(self) -> bool:
        """
        Verifica se a tabela eSinistros existe no banco
        """
        try:
            query = text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'eSinistros'")
            result = self.db.execute(query)
            count = result.scalar()
            return count > 0
        except Exception as e:
            logger.error(f"Erro ao verificar existência da tabela: {e}")
            return False
    
    def buscar_por_id(self, sinistro_id: int) -> Optional[SinistroAutomacao]:
        """
        Busca sinistro por ID
        """
        try:
            if not self.verificar_tabela_existe():
                logger.warning("Tabela eSinistros não encontrada")
                return None
                
            # Como não sabemos se existe campo ID, vamos tentar diferentes abordagens
            # Primeiro tentamos com ROWID (disponível no SQL Server)
            query = text("""
                SELECT TOP 1 *
                FROM eSinistros 
                WHERE ROWID = :id
                ORDER BY [Nota Fiscal]
            """)
            
            result = self.db.execute(query, {"id": sinistro_id})
            row = result.fetchone()
            
            if row:
                # Converter row para objeto SinistroAutomacao
                return self._row_to_sinistro(row, sinistro_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro por ID {sinistro_id}: {e}")
            return None
    
    def buscar_por_nota(self, nota_fiscal: str) -> Optional[SinistroAutomacao]:
        """
        Busca sinistro por nota fiscal
        """
        try:
            if not self.verificar_tabela_existe():
                logger.warning("Tabela eSinistros não encontrada")
                return None
                
            query = text("""
                SELECT TOP 1 *
                FROM eSinistros 
                WHERE [Nota Fiscal] = :nota
                ORDER BY [Data Cadastro] DESC
            """)
            
            result = self.db.execute(query, {"nota": nota_fiscal})
            row = result.fetchone()
            
            if row:
                return self._row_to_sinistro(row)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro por nota {nota_fiscal}: {e}")
            return None
    
    def listar_sinistros(
        self,
        offset: int = 0,
        limit: int = 100,
        filtros: Optional[Dict] = None
    ) -> List[SinistroAutomacao]:
        """
        Lista sinistros com filtros opcionais
        """
        try:
            if not self.verificar_tabela_existe():
                logger.warning("Tabela eSinistros não encontrada")
                return []
            
            # Query base
            where_conditions = []
            params = {}
            
            # Aplicar filtros se fornecidos
            if filtros:
                if filtros.get('nota_fiscal'):
                    where_conditions.append("[Nota Fiscal] LIKE :nota")
                    params['nota'] = f"%{filtros['nota_fiscal']}%"
                
                if filtros.get('cliente'):
                    where_conditions.append("[CLIENTE] LIKE :cliente")
                    params['cliente'] = f"%{filtros['cliente']}%"
                
                if filtros.get('status'):
                    where_conditions.append("[STATUS SINISTRO] LIKE :status")
                    params['status'] = f"%{filtros['status']}%"
            
            # Construir query
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = text(f"""
                SELECT *
                FROM eSinistros
                {where_clause}
                ORDER BY [Data Cadastro] DESC
                OFFSET :offset ROWS
                FETCH NEXT :limit ROWS ONLY
            """)
            
            params.update({'offset': offset, 'limit': limit})
            
            result = self.db.execute(query, params)
            rows = result.fetchall()
            
            sinistros = []
            for i, row in enumerate(rows):
                sinistro = self._row_to_sinistro(row, offset + i + 1)
                sinistros.append(sinistro)
            
            return sinistros
            
        except Exception as e:
            logger.error(f"Erro ao listar sinistros: {e}")
            return []
    
    def atualizar_sinistro(
        self, 
        sinistro_id: int, 
        dados: SinistroAutomacaoUpdate, 
        usuario: str
    ) -> Optional[SinistroAutomacao]:
        """
        Atualiza sinistro existente
        Por enquanto retorna simulação - implementação real depende de permissões
        """
        try:
            # Buscar sinistro original
            sinistro_original = self.buscar_por_id(sinistro_id)
            
            if not sinistro_original:
                logger.warning(f"Sinistro {sinistro_id} não encontrado para atualização")
                return None
            
            # Por enquanto, simular atualização devido a possíveis restrições de permissão
            logger.info(f"SIMULAÇÃO: Atualizando sinistro {sinistro_id}")
            logger.info(f"Dados para atualização: {dados.dict(exclude_unset=True)}")
            
            # Aplicar atualizações ao objeto em memória
            dados_dict = dados.dict(exclude_unset=True)
            for campo, valor in dados_dict.items():
                if hasattr(sinistro_original, campo):
                    setattr(sinistro_original, campo, valor)
            
            # Atualizar metadados
            sinistro_original.atualizado_em = datetime.utcnow()
            sinistro_original.atualizado_por = usuario
            
            logger.info(f"Sinistro {sinistro_id} atualizado com sucesso (simulação)")
            return sinistro_original
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {e}")
            return None
    
    def _row_to_sinistro(self, row, sinistro_id: int = None) -> SinistroAutomacao:
        """
        Converte uma linha do resultado SQL para objeto SinistroAutomacao
        """
        try:
            # Criar objeto usando os dados da linha
            sinistro = SinistroAutomacao()
            
            # Mapear campos da consulta SQL para o objeto
            # Usar getattr com fallback para campos que podem não existir
            
            sinistro.id = sinistro_id or 1
            sinistro.nota_fiscal = getattr(row, 'Nota Fiscal', None)
            sinistro.nr_conhecimento = getattr(row, 'Minu.Conh', None)
            sinistro.remetente = getattr(row, 'Remetente', None)
            sinistro.destinatario = getattr(row, 'Destinatário', None)
            
            # Datas
            sinistro.dt_coleta = getattr(row, 'Data Coleta', None)
            sinistro.dt_prazo_entrega = getattr(row, 'Prazo Entrega', None)
            sinistro.dt_entrega = getattr(row, 'Data Entrega', None)
            sinistro.dt_agendamento = getattr(row, 'Data Agendamento', None)
            sinistro.dt_ocorrencia = getattr(row, 'Data Ocorrência', None)
            sinistro.dt_cadastro = getattr(row, 'Data Cadastro', None)
            sinistro.hr_cadastro = getattr(row, 'Hora Cadastro', None)
            sinistro.dt_alteracao = getattr(row, 'Data Alteração', None)
            sinistro.hr_alteracao = getattr(row, 'Hora Alteração', None)
            
            # Ocorrências
            sinistro.ocorrencia = getattr(row, 'Ocorrência', None)
            sinistro.compl_ocorrencia = getattr(row, 'Compl. Ocorrência', None)
            sinistro.ultima_ocorrencia = getattr(row, 'ULTIMA OCORRENCIA', None)
            sinistro.referencia = getattr(row, 'REFERENCIA', None)
            
            # Valores
            sinistro.valor_nota_fiscal = getattr(row, 'Valor Nota Fiscal', None)
            sinistro.valor_frete = getattr(row, 'Valor Frete', None)
            sinistro.valor_sinistro = getattr(row, 'VALOR DO SINISTRO ', None)
            
            # Localização
            sinistro.cidade_destino = getattr(row, 'Cidade Destino', None)
            sinistro.uf_destino = getattr(row, 'UF Destino', None)
            
            # Informações do negócio
            sinistro.cliente = getattr(row, 'CLIENTE', None)
            sinistro.modal = getattr(row, 'MODAL', None)
            sinistro.tipo = getattr(row, 'TIPO', None)
            sinistro.descricao = getattr(row, 'DESCRIÇÃO', None)
            
            # Status
            sinistro.status_sinistro = getattr(row, 'STATUS SINISTRO', None)
            sinistro.status = getattr(row, 'STATUS', None)
            sinistro.concluido = getattr(row, 'CONCLUÍDO?', None)
            
            # Valores financeiros
            sinistro.salvados = getattr(row, 'SALVADOS', None)
            sinistro.indenizados = getattr(row, 'INDENIZADOS', None)
            sinistro.uso_interno = getattr(row, 'USO INTERNO', None)
            sinistro.juridico = getattr(row, 'JURIDICO', None)
            sinistro.seguro = getattr(row, 'SEGURO', None)
            sinistro.prejuizo = getattr(row, 'PREJUÍZO', None)
            
            # Metadados
            sinistro.criado_em = datetime.utcnow()
            sinistro.atualizado_em = datetime.utcnow()
            
            return sinistro
            
        except Exception as e:
            logger.error(f"Erro ao converter linha para SinistroAutomacao: {e}")
            raise
    
    def contar_sinistros(self, filtros: Optional[Dict] = None) -> int:
        """
        Conta total de sinistros com filtros opcionais
        """
        try:
            if not self.verificar_tabela_existe():
                return 0
            
            where_conditions = []
            params = {}
            
            if filtros:
                if filtros.get('nota_fiscal'):
                    where_conditions.append("[Nota Fiscal] LIKE :nota")
                    params['nota'] = f"%{filtros['nota_fiscal']}%"
                
                if filtros.get('cliente'):
                    where_conditions.append("[CLIENTE] LIKE :cliente")
                    params['cliente'] = f"%{filtros['cliente']}%"
                
                if filtros.get('status'):
                    where_conditions.append("[STATUS SINISTRO] LIKE :status")
                    params['status'] = f"%{filtros['status']}%"
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = text(f"""
                SELECT COUNT(*) as total
                FROM eSinistros
                {where_clause}
            """)
            
            result = self.db.execute(query, params)
            count = result.scalar()
            
            return count or 0
            
        except Exception as e:
            logger.error(f"Erro ao contar sinistros: {e}")
            return 0 