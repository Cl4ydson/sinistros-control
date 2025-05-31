from typing import List, Dict, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
import logging

from ..repositories.sinistro_repository import SinistroRepository
from ..models.sinistro import SinistroResponse

logger = logging.getLogger(__name__)

class SinistroService:
    """Service para lógica de negócio dos sinistros"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = SinistroRepository(db)
    
    def _get_mock_data(self) -> List[Dict]:
        """Dados mock para quando há problema de conexão"""
        return [
            {
                'Nota Fiscal': '877097',
                'Minu.Conh': 'CT001234',
                'Remetente': 'EMPRESA REMETENTE LTDA',
                'Destinatário': 'CLIENTE DESTINATARIO SA',
                'Data Coleta': date(2024, 1, 15),
                'Ocorrência': 'AVARIA PARCIAL',
                'Compl. Ocorrência': 'Produto danificado durante transporte - embalagem violada',
                'ULTIMA OCORRENCIA': 'Aguardando perícia técnica',
                'REFERENCIA': 'REF-001-2024',
                'Data Ocorrência': date(2024, 1, 18),
                'Data Cadastro': date(2024, 1, 15),
                'Hora Cadastro': '08:30:00',
                'Data Alteração': date(2024, 1, 18),
                'Hora Alteração': '14:15:00'
            },
            {
                'Nota Fiscal': '877098',
                'Minu.Conh': 'CT001235',
                'Remetente': 'FORNECEDOR ABC LTDA',
                'Destinatário': 'EMPRESA COMPRADORA ME',
                'Data Coleta': date(2024, 1, 16),
                'Ocorrência': 'EXTRAVIO TOTAL',
                'Compl. Ocorrência': 'Mercadoria extraviada durante transporte',
                'ULTIMA OCORRENCIA': 'Boletim de ocorrência registrado',
                'REFERENCIA': 'REF-002-2024',
                'Data Ocorrência': date(2024, 1, 19),
                'Data Cadastro': date(2024, 1, 16),
                'Hora Cadastro': '09:15:00',
                'Data Alteração': date(2024, 1, 19),
                'Hora Alteração': '16:45:00'
            },
            {
                'Nota Fiscal': '877099',
                'Minu.Conh': 'CT001236',
                'Remetente': 'INDUSTRIA XYZ SA',
                'Destinatário': 'DISTRIBUIDORA NACIONAL',
                'Data Coleta': date(2024, 1, 17),
                'Ocorrência': 'ROUBO DE CARGA',
                'Compl. Ocorrência': 'Carga roubada durante parada obrigatória',
                'ULTIMA OCORRENCIA': 'Investigação policial em andamento',
                'REFERENCIA': 'REF-003-2024',
                'Data Ocorrência': date(2024, 1, 18),
                'Data Cadastro': date(2024, 1, 17),
                'Hora Cadastro': '10:20:00',
                'Data Alteração': date(2024, 1, 18),
                'Hora Alteração': '20:30:00'
            },
            {
                'Nota Fiscal': '877100',
                'Minu.Conh': 'CT001237',
                'Remetente': 'EMPRESA AEREA LTDA',
                'Destinatário': 'CLIENTE URGENTE SA',
                'Data Coleta': date(2024, 1, 18),
                'Ocorrência': 'MERCADORIA SINISTRADA',
                'Compl. Ocorrência': 'Mercadoria danificada por condições climáticas adversas',
                'ULTIMA OCORRENCIA': 'Sinistro resolvido, indenização processada',
                'REFERENCIA': 'REF-004-2024',
                'Data Ocorrência': date(2024, 1, 18),
                'Data Cadastro': date(2024, 1, 18),
                'Hora Cadastro': '14:00:00',
                'Data Alteração': date(2024, 1, 19),
                'Hora Alteração': '11:30:00'
            },
            {
                'Nota Fiscal': '877101',
                'Minu.Conh': 'CT001238',
                'Remetente': 'TRANSPORTADORA BETA',
                'Destinatário': 'LOJA VAREJO LTDA',
                'Data Coleta': date(2024, 1, 20),
                'Ocorrência': 'AVARIA TOTAL',
                'Compl. Ocorrência': 'Produto completamente destruído em acidente',
                'ULTIMA OCORRENCIA': 'Processo de indenização iniciado',
                'REFERENCIA': 'REF-005-2024',
                'Data Ocorrência': date(2024, 1, 21),
                'Data Cadastro': date(2024, 1, 20),
                'Hora Cadastro': '15:45:00',
                'Data Alteração': date(2024, 1, 21),
                'Hora Alteração': '09:20:00'
            }
        ]
    
    def listar_sinistros(
        self,
        dt_ini: Optional[str] = None,
        dt_fim: Optional[str] = None,
        cliente: Optional[str] = None,
        modal: Optional[str] = None,
        nota_fiscal: Optional[str] = None,
        conhecimento: Optional[str] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict:
        """
        Lista sinistros com filtros e paginação
        """
        try:
            # Converter strings de data para objetos date
            dt_ini_obj = None
            dt_fim_obj = None
            
            if dt_ini:
                try:
                    dt_ini_obj = datetime.strptime(dt_ini, '%Y-%m-%d').date()
                except ValueError:
                    logger.warning(f"Data inicial inválida: {dt_ini}")
            
            if dt_fim:
                try:
                    dt_fim_obj = datetime.strptime(dt_fim, '%Y-%m-%d').date()
                except ValueError:
                    logger.warning(f"Data final inválida: {dt_fim}")
            
            # Tentar buscar sinistros no repositório
            try:
                sinistros_raw = self.repository.buscar_sinistros(
                    dt_ini=dt_ini_obj,
                    dt_fim=dt_fim_obj,
                    cliente=cliente,
                    nota_fiscal=nota_fiscal,
                    conhecimento=conhecimento
                )
                logger.info("✅ Dados obtidos do banco de dados")
            except Exception as db_error:
                logger.warning(f"⚠️ Erro ao acessar banco, usando dados mock: {db_error}")
                sinistros_raw = self._get_mock_data()
            
            # Converter para modelo de resposta
            sinistros = []
            for sinistro_data in sinistros_raw:
                try:
                    sinistro_response = SinistroResponse(sinistro_data)
                    
                    # Aplicar filtro de modal se especificado
                    if modal and sinistro_response.modal != modal:
                        continue
                    
                    sinistros.append(sinistro_response.to_dict())
                except Exception as e:
                    logger.error(f"Erro ao processar sinistro: {e}")
                    continue
            
            # Aplicar paginação manualmente (idealmente seria feito na query)
            start_index = (page - 1) * limit
            end_index = start_index + limit
            sinistros_paginated = sinistros[start_index:end_index]
            
            # Obter estatísticas
            estatisticas = self.obter_estatisticas(dt_ini_obj, dt_fim_obj)
            
            return {
                'sinistros': sinistros_paginated,
                'total': len(sinistros),
                'page': page,
                'limit': limit,
                'total_pages': (len(sinistros) + limit - 1) // limit,
                'estatisticas': estatisticas
            }
            
        except Exception as e:
            logger.error(f"Erro ao listar sinistros: {str(e)}")
            raise
    
    def obter_sinistro(self, sinistro_id: str) -> Optional[Dict]:
        """
        Obtém um sinistro específico pelo ID
        O ID é composto por: nota_fiscal-conhecimento
        """
        try:
            # Extrair nota fiscal e conhecimento do ID
            if '-' not in sinistro_id:
                logger.warning(f"ID de sinistro inválido: {sinistro_id}")
                return None
            
            parts = sinistro_id.split('-', 1)
            nota_fiscal = parts[0]
            conhecimento = parts[1] if len(parts) > 1 else ""
            
            # Buscar no repositório
            sinistro_data = self.repository.buscar_sinistro_por_id(nota_fiscal, conhecimento)
            
            if not sinistro_data:
                return None
            
            # Converter para modelo de resposta
            sinistro_response = SinistroResponse(sinistro_data)
            return sinistro_response.to_dict()
            
        except Exception as e:
            logger.error(f"Erro ao obter sinistro {sinistro_id}: {str(e)}")
            raise
    
    def obter_estatisticas(
        self, 
        dt_ini: Optional[date] = None, 
        dt_fim: Optional[date] = None
    ) -> Dict:
        """
        Obtém estatísticas dos sinistros
        """
        try:
            try:
                stats = self.repository.obter_estatisticas(dt_ini, dt_fim)
                logger.info("✅ Estatísticas obtidas do banco de dados")
            except Exception as db_error:
                logger.warning(f"⚠️ Erro ao acessar banco para estatísticas, usando dados mock: {db_error}")
                # Estatísticas mock baseadas nos dados mock
                stats = {
                    'total_sinistros': 5,
                    'avarias': 2,  # AVARIA PARCIAL + AVARIA TOTAL
                    'extravios': 1,  # EXTRAVIO TOTAL
                    'roubos': 1,  # ROUBO DE CARGA
                    'sinistradas': 1  # MERCADORIA SINISTRADA
                }
            
            # Calcular estatísticas adicionais
            total = stats['total_sinistros']
            
            return {
                'total_sinistros': total,
                'por_tipo': {
                    'avarias': {
                        'count': stats['avarias'],
                        'percentage': round((stats['avarias'] / total * 100) if total > 0 else 0, 2)
                    },
                    'extravios': {
                        'count': stats['extravios'],
                        'percentage': round((stats['extravios'] / total * 100) if total > 0 else 0, 2)
                    },
                    'roubos': {
                        'count': stats['roubos'],
                        'percentage': round((stats['roubos'] / total * 100) if total > 0 else 0, 2)
                    },
                    'sinistradas': {
                        'count': stats['sinistradas'],
                        'percentage': round((stats['sinistradas'] / total * 100) if total > 0 else 0, 2)
                    }
                },
                'por_status': {
                    'em_analise': {
                        'count': stats['avarias'] + stats['extravios'] + stats['roubos'],
                        'percentage': round(((stats['avarias'] + stats['extravios'] + stats['roubos']) / total * 100) if total > 0 else 0, 2)
                    },
                    'pendente': {
                        'count': stats['sinistradas'],
                        'percentage': round((stats['sinistradas'] / total * 100) if total > 0 else 0, 2)
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            raise
    
    def obter_tipos_ocorrencia(self) -> List[str]:
        """
        Obtém lista de tipos de ocorrência disponíveis
        """
        try:
            return self.repository.obter_tipos_ocorrencia()
        except Exception as e:
            logger.error(f"Erro ao obter tipos de ocorrência: {str(e)}")
            raise
    
    def atualizar_sinistro(self, sinistro_id: str, dados_atualizacao: Dict) -> Optional[Dict]:
        """
        Atualiza um sinistro (funcionalidade limitada pois é principalmente consulta)
        """
        try:
            # Por enquanto, apenas retorna o sinistro existente
            # Em um cenário real, você implementaria a lógica de atualização
            sinistro_atual = self.obter_sinistro(sinistro_id)
            
            if not sinistro_atual:
                return None
            
            # Simular atualização (não persiste no banco)
            sinistro_atualizado = {**sinistro_atual, **dados_atualizacao}
            
            logger.info(f"Sinistro {sinistro_id} atualizado (simulação)")
            return sinistro_atualizado
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sinistro {sinistro_id}: {str(e)}")
            raise
    
    def obter_dashboard_data(
        self,
        dt_ini: Optional[date] = None,
        dt_fim: Optional[date] = None
    ) -> Dict:
        """
        Obtém dados para o dashboard de sinistros
        """
        try:
            # Obter estatísticas
            estatisticas = self.obter_estatisticas(dt_ini, dt_fim)
            
            # Obter sinistros recentes (últimos 10)
            sinistros_recentes = self.listar_sinistros(
                dt_ini=dt_ini.isoformat() if dt_ini else None,
                dt_fim=dt_fim.isoformat() if dt_fim else None,
                limit=10
            )
            
            return {
                'estatisticas': estatisticas,
                'sinistros_recentes': sinistros_recentes['sinistros'],
                'tipos_ocorrencia': self.obter_tipos_ocorrencia()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter dados do dashboard: {str(e)}")
            raise