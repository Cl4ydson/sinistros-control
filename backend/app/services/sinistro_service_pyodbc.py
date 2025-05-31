from typing import List, Dict, Optional
from datetime import date, datetime
import logging

from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
from ..models.sinistro import SinistroResponse

logger = logging.getLogger(__name__)

class SinistroServicePyODBC:
    """Service usando pyodbc diretamente"""
    
    def __init__(self):
        self.repository = SinistroRepositoryPyODBC()
    
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
            
            # Buscar sinistros no repositório
            sinistros_raw = self.repository.buscar_sinistros(
                dt_ini=dt_ini_obj,
                dt_fim=dt_fim_obj,
                cliente=cliente,
                nota_fiscal=nota_fiscal,
                conhecimento=conhecimento,
                limit=limit * page  # Buscar mais para fazer paginação
            )
            
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
            stats = self.repository.obter_estatisticas(dt_ini, dt_fim)
            
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