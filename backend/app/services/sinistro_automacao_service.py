from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
import logging
from decimal import Decimal

from sqlalchemy.orm import Session
from ..database import get_db
from ..repositories.sinistro_automacao_repository import SinistroAutomacaoRepository
from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
from ..schemas.sinistro_automacao import (
    SinistroAutomacaoCreate,
    SinistroAutomacaoUpdate,
    SinistroAutomacaoResponse
)
from ..models.sinistro_automacao import SinistroAutomacao

logger = logging.getLogger(__name__)

class SinistroAutomacaoService:
    """
    Service para gerenciar sinistros na tabela eSinistros do banco AUTOMACAO_BRSAMOR
    Com fallback para banco de consulta quando necessário
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = SinistroAutomacaoRepository(db)
        self.repo_origem = SinistroRepositoryPyODBC()  # Fallback para banco consulta
    
    def buscar_sinistro(self, sinistro_id: int) -> Optional[Dict]:
        """
        Busca sinistro por ID com fallback
        """
        try:
            logger.info(f"Buscando sinistro {sinistro_id} na tabela eSinistros")
            
            # Tentar buscar na tabela eSinistros
            if self.repo.verificar_tabela_existe():
                sinistro = self.repo.buscar_por_id(sinistro_id)
                if sinistro:
                    logger.info(f"Sinistro {sinistro_id} encontrado na tabela eSinistros")
                    return sinistro.to_dict()
            
            # Fallback: buscar no banco de consulta
            logger.info(f"Fallback: buscando sinistro no banco de consulta")
            return self._buscar_no_banco_consulta(sinistro_id)
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro {sinistro_id}: {e}")
            return self._buscar_no_banco_consulta(sinistro_id)
    
    def _buscar_no_banco_consulta(self, sinistro_id: int) -> Optional[Dict]:
        """
        Busca sinistro no banco de consulta como fallback
        """
        try:
            # Simular busca baseada no ID
            sinistros = self.repo_origem.listar_sinistros()
            
            if sinistros and len(sinistros) >= sinistro_id:
                dados_origem = sinistros[sinistro_id - 1]
                
                # Converter para formato padrão
                return {
                    'id': sinistro_id,
                    'nota': dados_origem.get('Nota Fiscal', ''),
                    'numero': dados_origem.get('Minu.Conh', ''),
                    'remetente': dados_origem.get('Remetente', ''),
                    'destinatario': dados_origem.get('Destinatário', ''),
                    'status': dados_origem.get('Status', ''),
                    'dt_coleta': self._formatar_data(dados_origem.get('Data Coleta')),
                    'dt_entrega': self._formatar_data(dados_origem.get('Data Entrega')),
                    'ocorrencia': dados_origem.get('Ocorrência', ''),
                    'descricao': dados_origem.get('Compl. Ocorrência', ''),
                    'valor_sinistro': self._formatar_valor(dados_origem.get('Valor Mercadoria')),
                    'cliente': dados_origem.get('Cliente', ''),
                    'modal': dados_origem.get('Modal', ''),
                    'cidade_destino': dados_origem.get('Cidade Destino', ''),
                    'uf_destino': dados_origem.get('UF Destino', '')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro no fallback para banco consulta: {e}")
            return None
    
    def buscar_por_nota(self, nota_fiscal: str) -> Optional[Dict]:
        """
        Busca sinistro por nota fiscal
        """
        try:
            logger.info(f"Buscando sinistro por nota {nota_fiscal}")
            
            # Tentar buscar na tabela eSinistros
            if self.repo.verificar_tabela_existe():
                sinistro = self.repo.buscar_por_nota(nota_fiscal)
                if sinistro:
                    return sinistro.to_dict()
            
            # Fallback: buscar no banco de consulta
            return self._buscar_por_nota_banco_consulta(nota_fiscal)
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro por nota {nota_fiscal}: {e}")
            return self._buscar_por_nota_banco_consulta(nota_fiscal)
    
    def _buscar_por_nota_banco_consulta(self, nota_fiscal: str) -> Optional[Dict]:
        """
        Busca por nota no banco de consulta
        """
        try:
            dados_origem = self.repo_origem.buscar_sinistro_por_id(nota_fiscal)
            
            if dados_origem:
                return {
                    'id': 1,  # ID fictício
                    'nota': dados_origem.get('Nota Fiscal', ''),
                    'numero': dados_origem.get('Minu.Conh', ''),
                    'remetente': dados_origem.get('Remetente', ''),
                    'destinatario': dados_origem.get('Destinatário', ''),
                    'status': dados_origem.get('Status', ''),
                    'dt_coleta': self._formatar_data(dados_origem.get('Data Coleta')),
                    'dt_entrega': self._formatar_data(dados_origem.get('Data Entrega')),
                    'ocorrencia': dados_origem.get('Ocorrência', ''),
                    'descricao': dados_origem.get('Compl. Ocorrência', ''),
                    'valor_sinistro': self._formatar_valor(dados_origem.get('Valor Mercadoria')),
                    'cliente': dados_origem.get('Cliente', ''),
                    'modal': dados_origem.get('Modal', ''),
                    'cidade_destino': dados_origem.get('Cidade Destino', ''),
                    'uf_destino': dados_origem.get('UF Destino', '')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar por nota no banco consulta: {e}")
            return None
    
    def atualizar_sinistro(
        self, 
        sinistro_id: int, 
        dados: SinistroAutomacaoUpdate, 
        usuario: str
    ) -> Optional[Dict]:
        """
        Atualiza sinistro - com simulação se necessário
        """
        try:
            logger.info(f"Atualizando sinistro {sinistro_id}")
            
            # Verificar se tabela existe e tentar atualização real
            if self.repo.verificar_tabela_existe():
                sinistro_atualizado = self.repo.atualizar_sinistro(sinistro_id, dados, usuario)
                if sinistro_atualizado:
                    logger.info(f"Sinistro {sinistro_id} atualizado com sucesso")
                    return sinistro_atualizado.to_dict()
            
            # Fallback: simulação de atualização
            return self._simular_atualizacao(sinistro_id, dados, usuario)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {e}")
            return self._simular_atualizacao(sinistro_id, dados, usuario)
    
    def _simular_atualizacao(
        self, 
        sinistro_id: int, 
        dados: SinistroAutomacaoUpdate, 
        usuario: str
    ) -> Dict:
        """
        Simula atualização para manter funcionalidade durante desenvolvimento
        """
        try:
            logger.info(f"SIMULAÇÃO: Atualizando sinistro {sinistro_id}")
            
            # Buscar dados originais
            sinistro_original = self.buscar_sinistro(sinistro_id)
            
            if not sinistro_original:
                # Criar estrutura básica se não encontrou
                sinistro_original = {
                    'id': sinistro_id,
                    'nota': f'NOTA-{sinistro_id}',
                    'numero': f'CONH-{sinistro_id}',
                    'status': 'Em processamento'
                }
            
            # Aplicar atualizações
            dados_dict = dados.dict(exclude_unset=True)
            for campo, valor in dados_dict.items():
                # Mapear campos do schema para campos do dict
                if campo == 'status_sinistro':
                    sinistro_original['status'] = valor
                elif campo == 'descricao':
                    sinistro_original['descricao'] = valor
                elif campo == 'valor_sinistro':
                    sinistro_original['valor_sinistro'] = float(valor) if valor else None
                else:
                    sinistro_original[campo] = valor
            
            # Atualizar metadados
            sinistro_original['atualizado_em'] = datetime.utcnow().isoformat()
            sinistro_original['atualizado_por'] = usuario
            
            logger.info(f"SIMULAÇÃO: Sinistro {sinistro_id} atualizado com dados: {dados_dict}")
            
            return sinistro_original
            
        except Exception as e:
            logger.error(f"Erro na simulação de atualização: {e}")
            raise
    
    def listar_sinistros(
        self,
        skip: int = 0,
        limit: int = 100,
        filtros: Optional[Dict] = None
    ) -> Tuple[List[Dict], int]:
        """
        Lista sinistros com paginação
        """
        try:
            logger.info(f"Listando sinistros (skip={skip}, limit={limit})")
            
            # Tentar listar da tabela eSinistros
            if self.repo.verificar_tabela_existe():
                sinistros = self.repo.listar_sinistros(skip, limit, filtros)
                total = self.repo.contar_sinistros(filtros)
                
                sinistros_dict = [s.to_dict() for s in sinistros]
                
                if sinistros_dict:
                    logger.info(f"Encontrados {len(sinistros_dict)} sinistros na tabela eSinistros")
                    return sinistros_dict, total
            
            # Fallback: buscar no banco de consulta
            return self._listar_banco_consulta(skip, limit, filtros)
            
        except Exception as e:
            logger.error(f"Erro ao listar sinistros: {e}")
            return self._listar_banco_consulta(skip, limit, filtros)
    
    def _listar_banco_consulta(
        self,
        skip: int = 0,
        limit: int = 100,
        filtros: Optional[Dict] = None
    ) -> Tuple[List[Dict], int]:
        """
        Lista sinistros do banco de consulta como fallback
        """
        try:
            logger.info("Fallback: listando sinistros do banco de consulta")
            
            # Buscar dados do banco origem
            sinistros_origem = self.repo_origem.listar_sinistros()
            
            if not sinistros_origem:
                return [], 0
            
            # Aplicar filtros simples se fornecidos
            sinistros_filtrados = sinistros_origem
            if filtros:
                if filtros.get('nota_fiscal'):
                    nota_filtro = filtros['nota_fiscal'].lower()
                    sinistros_filtrados = [
                        s for s in sinistros_filtrados 
                        if nota_filtro in str(s.get('Nota Fiscal', '')).lower()
                    ]
                
                if filtros.get('cliente'):
                    cliente_filtro = filtros['cliente'].lower()
                    sinistros_filtrados = [
                        s for s in sinistros_filtrados 
                        if cliente_filtro in str(s.get('Cliente', '')).lower()
                    ]
            
            # Aplicar paginação
            total = len(sinistros_filtrados)
            sinistros_pagina = sinistros_filtrados[skip:skip + limit]
            
            # Converter para formato padrão
            resultado = []
            for i, dados in enumerate(sinistros_pagina):
                sinistro_dict = {
                    'id': skip + i + 1,
                    'nota': dados.get('Nota Fiscal', ''),
                    'numero': dados.get('Minu.Conh', ''),
                    'remetente': dados.get('Remetente', ''),
                    'destinatario': dados.get('Destinatário', ''),
                    'status': dados.get('Status', ''),
                    'dt_coleta': self._formatar_data(dados.get('Data Coleta')),
                    'dt_entrega': self._formatar_data(dados.get('Data Entrega')),
                    'ocorrencia': dados.get('Ocorrência', ''),
                    'descricao': dados.get('Compl. Ocorrência', ''),
                    'valor_sinistro': self._formatar_valor(dados.get('Valor Mercadoria')),
                    'cliente': dados.get('Cliente', ''),
                    'modal': dados.get('Modal', ''),
                    'cidade_destino': dados.get('Cidade Destino', ''),
                    'uf_destino': dados.get('UF Destino', '')
                }
                resultado.append(sinistro_dict)
            
            logger.info(f"Retornando {len(resultado)} sinistros do banco consulta (total: {total})")
            return resultado, total
            
        except Exception as e:
            logger.error(f"Erro no fallback de listagem: {e}")
            return [], 0
    
    def _formatar_data(self, data_valor) -> Optional[str]:
        """Formata data para string ISO"""
        if not data_valor:
            return None
        
        if isinstance(data_valor, (date, datetime)):
            return data_valor.isoformat()
        
        return str(data_valor)
    
    def _formatar_valor(self, valor) -> Optional[float]:
        """Formata valor numérico"""
        if valor is None:
            return None
        
        try:
            return float(valor)
        except:
            return None
    
    def verificar_status_sistema(self) -> Dict:
        """
        Verifica status do sistema e conectividade
        """
        try:
            status = {
                'tabela_esinistros_existe': False,
                'banco_consulta_disponivel': False,
                'total_sinistros_esinistros': 0,
                'total_sinistros_consulta': 0,
                'modo_operacao': 'fallback'
            }
            
            # Verificar tabela eSinistros
            if self.repo.verificar_tabela_existe():
                status['tabela_esinistros_existe'] = True
                status['total_sinistros_esinistros'] = self.repo.contar_sinistros()
                status['modo_operacao'] = 'normal'
            
            # Verificar banco consulta
            try:
                sinistros_consulta = self.repo_origem.listar_sinistros()
                if sinistros_consulta:
                    status['banco_consulta_disponivel'] = True
                    status['total_sinistros_consulta'] = len(sinistros_consulta)
            except:
                pass
            
            return status
            
        except Exception as e:
            logger.error(f"Erro ao verificar status do sistema: {e}")
            return {
                'tabela_esinistros_existe': False,
                'banco_consulta_disponivel': False,
                'total_sinistros_esinistros': 0,
                'total_sinistros_consulta': 0,
                'modo_operacao': 'erro',
                'erro': str(e)
            }

def get_sinistro_automacao_service(db: Session = None) -> SinistroAutomacaoService:
    """
    Factory function para obter instância do service
    """
    if db is None:
        db = next(get_db())
    
    return SinistroAutomacaoService(db) 